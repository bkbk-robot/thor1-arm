#!/usr/bin/env python3
"""Thor 1.0 — 机械臂舵机控制
用法:
  python3 arm_ctrl.py --status              # 查看所有通道状态
  python3 arm_ctrl.py --ch 5 --target 120   # 夹爪夹紧
  python3 arm_ctrl.py --ch 1 --target 78    # 大臂移动到78°
  python3 arm_ctrl.py --ch 0 --step +2      # 底座相对移动+2°
"""
import os
import json
import requests
import time
import argparse

XIAO_IP = os.environ.get("THOR_IP", "192.168.1.100")
STEP = 20       # 每步20°
INTERVAL = 0.3  # 步间间隔300ms

# 舵机安全限位 (通道: (最小角度, 最大角度))
# 防止误操作损坏机械结构
SERVO_LIMITS = {
    0: (0, 180),    # Base — 全范围
    1: (30, 150),   # Shoulder — 避免过载
    2: (20, 160),   # Elbow — 避免碰撞底座
    3: (10, 170),   # Wrist Pitch
    4: (0, 180),    # Wrist Roll — 全范围旋转
    5: (60, 140),   # Gripper — 夹爪开合范围
}


def clamp_angle(ch, angle):
    """将角度限制在安全范围内"""
    if ch not in SERVO_LIMITS:
        return max(0, min(180, angle))
    lo, hi = SERVO_LIMITS[ch]
    if angle < lo:
        print(f"⚠️  CH{ch} 角度 {angle}° 低于安全下限 {lo}°，已修正")
        return lo
    if angle > hi:
        print(f"⚠️  CH{ch} 角度 {angle}° 超过安全上限 {hi}°，已修正")
        return hi
    return angle


def get_current(ch):
    try:
        r = requests.get(f"http://{XIAO_IP}/status", timeout=3)
        data = r.json()
        return data.get(f"ch{ch}", None)
    except Exception:
        return None


def get_all_status():
    """获取所有通道状态"""
    try:
        r = requests.get(f"http://{XIAO_IP}/status", timeout=3)
        data = r.json()
        print(f"Thor 1.0 状态 ({XIAO_IP})")
        print("-" * 35)
        names = {
            0: "Base", 1: "Shoulder", 2: "Elbow",
            3: "Wrist Pitch", 4: "Wrist Roll", 5: "Gripper"
        }
        for ch in sorted(data.keys()):
            if ch.startswith("ch"):
                num = int(ch[2:])
                name = names.get(num, f"CH{num}")
                lo, hi = SERVO_LIMITS.get(num, (0, 180))
                angle = data[ch]
                flag = "✓" if lo <= angle <= hi else "⚠️"
                print(f"  {flag} {name:15s} (CH{num}): {angle:3d}°  [安全范围: {lo}-{hi}°]")
    except Exception as e:
        print(f"无法连接设备 {XIAO_IP}: {e}")


def set_servo(ch, angle):
    angle = clamp_angle(ch, angle)
    url = f"http://{XIAO_IP}/set?ch={ch}&val={angle}"
    r = requests.get(url, timeout=3)
    return r.text


def move_gradual(ch, target, step=STEP, interval=INTERVAL):
    """逐步移动到目标角度，每步step度，间隔interval秒"""
    target = clamp_angle(ch, target)
    now = get_current(ch)
    if now is None:
        print(f"无法获取CH{ch}当前角度，确认设备在线: {XIAO_IP}")
        return

    print(f"CH{ch}: {now}° -> {target}° (每步{step}°, {interval}s间隔)")

    direction = 1 if target > now else -1
    pos = now
    while True:
        pos += direction * step
        if direction > 0:
            pos = min(pos, target)
        else:
            pos = max(pos, target)
        print(f"  -> {pos}°")
        set_servo(ch, pos)
        time.sleep(interval)
        if pos == target:
            break

    final = get_current(ch)
    print(f"完成: CH{ch} = {final}°")


def main():
    parser = argparse.ArgumentParser(description="Thor 1.0 机械臂控制")
    parser.add_argument("--status", action="store_true", help="查看所有通道状态")
    parser.add_argument("--ch", type=int, help="舵机通道 (0-5)")
    parser.add_argument("--target", type=int, help="目标角度 (0-180)")
    parser.add_argument("--step", type=int, help="相对移动步数 (正=加, 负=减)")
    args = parser.parse_args()

    if args.status:
        get_all_status()
        return

    if args.ch is None:
        parser.print_help()
        return

    ch = args.ch

    if args.target is not None:
        move_gradual(ch, args.target)
    elif args.step is not None:
        now = get_current(ch)
        if now is None:
            print(f"无法获取CH{ch}当前角度")
            return
        move_gradual(ch, now + args.step)
    else:
        print("请指定 --target 或 --step，或使用 --status 查看状态")


if __name__ == "__main__":
    main()

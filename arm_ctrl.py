#!/usr/bin/env python3
"""Thor 1.0 — 机械臂舵机控制
用法:
  python3 arm_ctrl.py --ch 5 --target 120   # 夹爪夹紧
  python3 arm_ctrl.py --ch 1 --target 78    # 大臂移动到78°
  python3 arm_ctrl.py --ch 0 --step +2      # 底座相对移动+2°
"""
import os
import requests
import time
import argparse

XIAO_IP = os.environ.get("THOR_IP", "192.168.1.100")
STEP = 20       # 每步20°
INTERVAL = 0.3  # 步间间隔300ms


def get_current(ch):
    try:
        r = requests.get(f"http://{XIAO_IP}/status", timeout=3)
        data = r.json()
        return data.get(f"ch{ch}", None)
    except Exception:
        return None


def set_servo(ch, angle):
    url = f"http://{XIAO_IP}/set?ch={ch}&val={angle}"
    r = requests.get(url, timeout=3)
    return r.text


def move_gradual(ch, target, step=STEP, interval=INTERVAL):
    """逐步移动到目标角度，每步step度，间隔interval秒"""
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
    parser.add_argument("--ch", type=int, required=True, help="舵机通道 (0-5)")
    parser.add_argument("--target", type=int, help="目标角度 (0-180)")
    parser.add_argument("--step", type=int, help="相对移动步数 (正=加, 负=减)")
    args = parser.parse_args()

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
        print("请指定 --target 或 --step")


if __name__ == "__main__":
    main()

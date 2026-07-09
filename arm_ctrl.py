#!/usr/bin/env python3
"""机械臂控制 - CH5夹爪渐进移动
用法:
  python3 arm_ctrl.py --ch 5 --target 120   夹紧（渐进20°/步）
  python3 arm_ctrl.py --ch 5 --target 50    张开（渐进20°/步）
  python3 arm_ctrl.py --ch 1 --target 78   移动到指定角度
  python3 arm_ctrl.py --ch 0 --step +2      相对移动2°
"""
import requests
import time
import argparse

XIAO_IP = "172.20.10.10"
STEP = 20  # 每次20°
INTERVAL = 0.3  # 300ms

def get_current(ch):
    try:
        r = requests.get(f"http://{XIAO_IP}/status", timeout=3)
        data = r.json()
        return data.get(f"ch{ch}", None)
    except:
        return None

def set_servo(ch, angle):
    url = f"http://{XIAO_IP}/set?ch={ch}&val={angle}"
    r = requests.get(url, timeout=3)
    return r.text

def move_gradual(ch, target, step=STEP, interval=INTERVAL):
    """逐步移动到目标角度，每次STEP度，间隔INTERVAL秒"""
    now = get_current(ch)
    if now is None:
        print(f"无法获取CH{ch}当前角度")
        return
    
    print(f"CH{ch}: {now}° -> {target}° (每步{step}°, {interval}s间隔)")
    
    direction = 1 if target > now else -1
    pos = now
    while True:
        pos += direction * step
        # 不超过目标
        if direction > 0:
            pos = min(pos, target)
        else:
            pos = max(pos, target)
        print(f"  -> {pos}°")
        set_servo(ch, pos)
        time.sleep(interval)
        if pos == target:
            break
    
    # 确保精确到达目标
    if pos != target:
        print(f"  -> {target}° (final)")
        set_servo(ch, target)
        time.sleep(interval)

def main():
    parser = argparse.ArgumentParser(description="机械臂控制")
    parser.add_argument("--ch", type=int, required=True, help="舵机通道 (0-6)")
    parser.add_argument("--target", type=int, help="目标角度 (0-180)")
    parser.add_argument("--step", type=int, help="相对移动步数 (正值=加, 负值=减)")
    parser.add_argument("--direct", action="store_true", help="直接跳转，不渐进")
    args = parser.parse_args()
    
    ch = args.ch
    
    if args.target is not None:
        target = args.target
        if args.direct or ch == 5:
            # CH5默认渐进，其他通道可选
            if ch == 5:
                move_gradual(ch, target)
            else:
                move_gradual(ch, target)
        else:
            move_gradual(ch, target)
    elif args.step is not None:
        now = get_current(ch)
        if now is None:
            print(f"无法获取CH{ch}当前角度")
            return
        target = now + args.step
        move_gradual(ch, target)
    else:
        print("请指定 --target 或 --step")
        return
    
    # 显示最终状态
    final = get_current(ch)
    print(f"完成: CH{ch} = {final}°")

if __name__ == "__main__":
    main()

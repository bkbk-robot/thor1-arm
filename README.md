# Thor 1.0 — 6-DOF Voice-Controlled Robot Arm

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

> Built solo with AI teammates in one month. Coffee shop → robot arm → open source.

## What It Is

6-DOF robot arm with voice control, built from consumer-grade parts:

- **ESP32-S3** + **PCA9685** — 16-channel PWM servo driver
- **6× MG996R** servos — base, shoulder, elbow, wrist-pitch, wrist-roll, gripper
- **Voice loop** — speech-to-text → LLM intent → arm executes
- Runs on edge devices (tested on Orange Pi 5 Pro)

## Hardware

```
ESP32-S3          PCA9685
GPIO21 (SDA)  ->  SDA
GPIO22 (SCL)  ->  SCL
5V             ->  VCC
GND            ->  GND

Servo channels:
  Ch0: Base     Ch3: Wrist Pitch
  Ch1: Shoulder  Ch4: Wrist Roll
  Ch2: Elbow     Ch5: Gripper
```

PCB schematic and layout in `electronics/` (KiCad format).

## How to Run

**1. Flash firmware** — `robot_arm_control/robot_arm_control.ino` to ESP32-S3.
The firmware serves an HTTP API: `GET /status`, `GET /set?ch=&val=`.

**2. Install Python deps**
```bash
pip install -r requirements.txt
```

**3. Drive the arm**
```bash
export THOR_IP="192.168.1.100"   # your ESP32 IP

python3 arm_ctrl.py --ch 5 --target 120   # close gripper
python3 arm_ctrl.py --ch 1 --target 78    # move shoulder
python3 arm_ctrl.py --ch 0 --step +2      # nudge base +2°
```

## Project Structure

```
├── robot_arm_control/     # ESP32-S3 firmware (Arduino)
├── arm_ctrl.py            # Python control CLI
├── electronics/           # KiCad PCB schematic + layout
├── requirements.txt
└── LICENSE                # MIT
```

## License

MIT — free to use, modify, distribute.

## Connect

- **GitHub:** [@bkbk-robot](https://github.com/bkbk-robot)
- **Company:** Baiye Precision Technology (广州白夜精密科技有限公司)

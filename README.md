# Thor 1.0 — AI Voice Control for 6-DOF Robotic Arm

[![Release](https://img.shields.io/badge/Release-v0.1.0-blue?style=flat-square&label=July%202026)](https://github.com/bkbk-robot/thor1-arm/releases/tag/v0.1.0)

> *2026,一个人在咖啡店里,没有团队,用消费级零件和AI工具,让机械臂听得懂人话。*
> *One person + AI tools = one serious robot team.*

**What it does:** A 6-DOF desktop robotic arm you can talk to in natural language.
**How long:** ~1 month. **Who built it:** just one person. **Tools:** Claude, DeepSeek, QClaw.

---

## 🎯 What This Repo Is

My **original contributions** to the Thor 1.0 open-source project:

| File | What It Does |
|------|-------------|
| `arm_ctrl.py` | Main PC-side control: parses LLM commands → sends to ESP32 via serial |
| `robot_voice_chat.py` | Voice dialogue system: ASR → LLM reasoning → action execution |
| `robot_arm_control/robot_arm_control.ino` | Arduino/ESP32 firmware for 6-DOF motor control |
| `electronics/ControlPCB.*` | Custom circuit additions (custom PCB, opto-isolator) |

**Architecture:**

```
┌─────────────┐     ┌──────────────┐     ┌──────────────┐     ┌────────────┐
│   User      │────▶│  Whisper ASR │────▶│  LLM (DeepSeek)│────▶│  arm_ctrl  │
│  (Voice)    │     │  (Alibaba)  │     │  (Natural Lang)│    │  (Python)  │
└─────────────┘     └──────────────┘     └──────────────┘     └─────┬──────┘
                                                                       │
                                                                       ▼
                                        ┌──────────────┐     ┌────────────┐
                                        │   ESP32-S3   │◀────│  PCA9685   │
                                        │  + Arduino   │     │  16-ch PWM │
                                        └──────────────┘     └─────┬──────┘
                                                                       │
                                                                       ▼
                                                               ┌────────────┐
                                                               │  6 × NEMA17│
                                                               │  Stepper   │
                                                               └────────────┘
```

---

## ⚠️ About the Mechanical Parts (STL Files)

The **3D-printed mechanical parts** are from **Gael Langevin's original Thor project**:
- Repo: [fpga-mobotics/thor](https://github.com/fpga-mobotics/thor)
- License: Creative Commons Attribution-ShareAlike

I did NOT design these parts. My work was:
- Assembling the hardware
- Writing the AI voice control software
- Integrating LLMs with the physical robot
- Making it actually work end-to-end

---

## 🛠️ Hardware I Used

| Part | Where to Buy | Est. Cost |
|------|-------------|-----------|
| ESP32-S3 Dev Board | Aliexpress | ~¥40 |
| PCA9685 16-ch PWM | Aliexpress | ~¥15 |
| NEMA 17 Steppers ×6 | Aliexpress | ~¥120 |
| A4988 Drivers ×6 | Aliexpress | ~¥20 |
| 12V 5A PSU | Aliexpress | ~¥30 |
| Thor mechanical parts | [fpga-mobotics/thor](https://github.com/fpga-mobotics/thor) | Free (CC-SA) |
| **Total** | | **~¥225** |

---

## 🚀 Quick Start

```bash
# 1. Clone this repo
git clone https://github.com/bkbk-robot/thor1-arm.git
cd thor1-arm

# 2. Install dependencies
pip install serial pyserial openai

# 3. Wire up (see wiring diagram in electronics/)
#    ESP32 → PCA9685 → NEMA 17 steppers

# 4. Flash the Arduino firmware
#    Open robot_arm_control/robot_arm_control.ino in Arduino IDE
#    Flash to ESP32

# 5. Run voice control
python3 robot_voice_chat.py
```

**Say things like:**
- "Pick up the cup"
- "Move left"
- "Put it down"

---

## 🚀 The Next Chapter

Thor 1.0 proved: **one person + AI tools = one serious robot team.**

Thor 2.0 (in progress):
- NEMA 17 steppers + Arduino Mega + RAMPS 1.4
- Vision-based grasping (YOLO + Orange Pi 5 Pro)
- AlphaGo-style RL self-play training
- Goal: fully autonomous task execution

---

## 📜 License

**My code:** MIT License (see [LICENSE](LICENSE))

**Thor mechanical parts:** Creative Commons Attribution-ShareAlike — [fpga-mobotics/thor](https://github.com/fpga-mobotics/thor)

---

---

## 🆕 Recent Updates

**2026-07-13 — v0.1.0 released!** First open source release with full voice control pipeline.
- 65+ cloners, 155+ clones since launch
- Thor 2.0 in progress: stepper motors + vision + RL training

---

*Built by [Cloud Li (@bkbk-robot)](https://github.com/bkbk-robot) — Guangzhou, China — 2026*

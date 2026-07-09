# Thor 1.0 — 6-DOF AI Robotic Arm

> *2026，一个人在咖啡店里，没有团队，没有实验室，用消费级零件和AI工具，一个月让一台六自由度机械臂站起来、听得懂人话。*

**Live Demo:** [Watch Thor 1.0 in action](https://www.youtube.com/watch?v=placeholder)

## 🎯 What Is This?

Thor 1.0 is a **6-DOF (Six Degrees of Freedom) desktop robotic arm** built with:
- **ESP32** microcontroller + **PCA9685** PWM controller
- **Aliexpress NEMA 17 stepper motors** (6x)
- **AI voice control** — speak a command, the arm moves
- Built **solo** with AI coding assistants (Claude, DeepSeek, QClaw)

## 🧠 Architecture

```
[You Speak] → [ASR (SiliconFlow API)] → [LLM (DeepSeek V3)] → [arm_ctrl.py]
                                                                      ↓
                                                            [ESP32 + PCA9685]
                                                                      ↓
                                                           [6x NEMA 17 Motors]
                                                                      ↓
                                                          [6-DOF Robotic Arm]
```

## 📂 Project Structure

```
thor1-arm/
├── arm_ctrl.py              # Main control script (PC side)
├── robot_voice_chat.py      # Voice dialogue system
├── robot_arm_control/        # Arduino ESP32 firmware
│   └── robot_arm_control.ino
├── electronics/              # Circuit schematics & PCB
└── stl/                      # 3D printable parts (FreeCAD source)
```

## 🔧 Hardware BOM

| Part | Qty | Est. Cost |
|------|-----|-----------|
| ESP32 Dev Board | 1 | ~¥30 |
| PCA9685 16-Channel PWM | 1 | ~¥15 |
| NEMA 17 Stepper Motor | 6 | ~¥180 |
| A4988 Driver | 6 | ~¥30 |
| 12V 5A Power Supply | 1 | ~¥40 |
| Assorted cables, connectors | — | ~¥50 |
| **Total** | | **~¥345** |

## 🖥️ Software Setup

```bash
# 1. Flash Arduino firmware
# Open robot_arm_control/robot_arm_control.ino in Arduino IDE
# Flash to ESP32

# 2. Run voice control
python3 arm_ctrl.py
```

### API Requirements
- **SiliconFlow API** (ASR + LLM): [siliconflow.com](https://siliconflow.com)
- Works with Chinese and English commands

## 🎓 What I Learned

- **Mechanical design**: How to size motors, calculate torque, design linkages
- **Control systems**: Inverse kinematics, joint space vs task space
- **AI integration**: Connecting cloud LLMs to physical hardware in real-time
- **Solo development**: AI tools have collapsed the "team" requirement for complex projects

## 🚀 The Next Chapter

Thor 1.0 proved: **one person + AI tools = one serious robot team.**

Thor 2.0 (in progress) aims for:
- Fully autonomous task execution
- Vision-based object detection & grasping
- AlphaGo-style RL self-play training
- NEMA 17 stepper motors + Arduino Mega + RAMPS 1.4

## 📜 License

MIT — Do whatever you want. Build it, improve it, make it yours.

---

*Built with ❤️ by [Cloud Li (@bkbk-robot)](https://github.com/bkbk-robot)*
*Guangzhou, China — April 2026*

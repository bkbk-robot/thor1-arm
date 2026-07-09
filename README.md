# Thor 1.0 — AI Voice Control for 6-DOF Robotic Arm

> *2026,一个人在咖啡店里,没有团队,用消费级零件和AI工具,让机械臂听得懂人话。*
> *One person + AI tools = one serious robot team.*

**What I built:** A 6-DOF desktop robotic arm with natural language voice control.
**How long:** ~1 month. **Who built it:** just me. **Tools:** Claude, DeepSeek, QClaw.

---

## 🎯 What This Repo Is

This repo contains my **original contributions** to the Thor 1.0 project:

| File | What It Does |
|------|-------------|
|  | Main PC-side control: parses LLM commands → sends to ESP32 via serial |
|  | Voice dialogue system: ASR → LLM reasoning → action execution |
|  | Arduino/ESP32 firmware for 6-DOF motor control |
|  | Custom circuit additions (custom PCB, opto-isolator) |

**Architecture:**


---

## ⚠️ About the Mechanical Parts (STL Files)

The **3D-printed mechanical parts** are from **Gael Langevin's original Thor project**:
- Repo: [fpga-mobotics/thor](https://github.com/fpga-mobotics/thor)
- License: Creative Commons Attribution-ShareAlike

I did NOT design these parts. They are open source and freely available at the link above.

**My work was:**
- Assembling the hardware
- Writing the AI voice control software
- Integrating LLMs with the physical robot
- Making it actually work end-to-end

---

## 🛠️ Hardware I Used

| Part | Where to Buy | Est. Cost |
|------|-------------|-----------|
| ESP32 Dev Board | Aliexpress | ~ |
| PCA9685 16-ch PWM | Aliexpress | ~ |
| NEMA 17 Steppers ×6 | Aliexpress | ~ |
| A4988 Drivers ×6 | Aliexpress | ~ |
| 12V 5A PSU | Aliexpress | ~ |
| Thor mechanical parts | [fpga-mobotics/thor](https://github.com/fpga-mobotics/thor) | Free (CC-SA) |

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

**My code:** MIT License (see )

**Thor mechanical parts:** Creative Commons Attribution-ShareAlike — [fpga-mobotics/thor](https://github.com/fpga-mobotics/thor)

---

*Built by [Cloud Li (@bkbk-robot)](https://github.com/bkbk-robot) — Guangzhou, China — 2026*

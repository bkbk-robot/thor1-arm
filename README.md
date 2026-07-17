# Thor 1.0 — 6-DOF Voice-Controlled Robot Arm

[![GitHub stars](https://img.shields.io/github/stars/bkbk-robot/thor1-arm)](https://github.com/bkbk-robot/thor1-arm/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

> **Coffee shop owner + AI = robot arm built in one month.**

---

## How This Started

Six months ago, I was running a coffee shop.

I wasn't happy with the direction of my life. I knew I needed to change — but I didn't know what direction. Then I started playing with AI tools. One conversation at a time. One late night at a time. One problem solved at a time.

The interesting part: AI wasn't the magic. The interesting part was what happened when a real human and a real AI started working together. Not "human vs AI." Not "AI replaces human." Two different intelligences, making decisions together, building something neither could build alone.

**That's QClaw.** My teammate. Not my tool.

This repo is what that looks like in practice.

---

## What We Built

Thor 1.0 is a **6-DOF robot arm with voice control** — built from scratch with consumer-grade parts:

- **ESP32** + **PCA9685** — motor control
- **Voice commands** → AI interprets intent → arm executes
- Full **Python control API** with inverse kinematics
- Runs on **Orange Pi 5 Pro** at the edge

The arm is a prototype. What matters is the system underneath: how a human + AI teammate actually collaborate to design, build, and ship something real.

---

## How to Run

**1. Flash the firmware** — `robot_arm_control/robot_arm_control.ino` for **ESP32-S3 + PCA9685** (I2C `SDA=21, SCL=22`; MG996R servos on channels 0–5: base · shoulder · elbow · wrist-pitch · wrist-roll · gripper). The firmware serves a tiny HTTP API (`GET /status`, `GET /set?ch=&val=`) the Python side drives.

**2. Install Python deps**
```bash
pip install -r requirements.txt   # pyserial + optional voice/LLM extras
```

**3. Drive the arm**
```bash
python3 arm_ctrl.py --ch 5 --target 120   # close gripper (gradual 20°/step)
python3 arm_ctrl.py --ch 1 --target 78    # move shoulder to 78°
python3 arm_ctrl.py --ch 0 --step +2       # nudge base +2°
```

**4. Talk to it** — `robot_voice_chat.py` runs the full edge voice loop:
```
microphone → STT (SenseVoice) → LLM (intent) → TTS (gTTS) → speaker
```
Set your LLM endpoint in the config, then `python3 robot_voice_chat.py`.

> Inverse-kinematics helpers and the full control API live in `arm_ctrl.py`. The arm is a prototype — treat the angles as a starting point and tune for your hardware.

---

## The "Language as Power" Idea

Jensen Huang gave an analogy that stuck with me:

> Centuries ago, you put oil or electricity into a machine, and it did something remarkable. Now with AI, you put something different in: **language**. Language is the new power source.

AI doesn't run on electricity. It runs on language. The clearer your language, the more power you get out of it. The better your questions, the better your answers. It amplifies whatever you give it.

That's why this works: not because AI is magic. Because we learned to ask better questions.

---

## The Journey

```
2026-03  ☕  Coffee shop — first experiments with AI + hardware
2026-05  🏆  Got into a provincial-level tech incubator (top 10 of that batch)
2026-06  🏢  Founded Baiye Precision Technology Co., Ltd.
2026-06  🤖  Thor 1.0 — voice-controlled arm, end to end
2026-07  🌍  Open sourced — 124 people cloned it on day one
```

---

## What This Is

This isn't a "look what I built" repo.

This is a **work in progress**. Real decisions. Real failures. Real progress.

The goal: build AI-powered robots that can operate at the edge — and eventually, beyond.

> "10% of resources → Earth: help people live longer, healthier lives.  
> 90% → Space: be the first to stand on another world."

---

## Connect

- **GitHub:** [@bkbk-robot](https://github.com/bkbk-robot)
- **Company:** Baiye Precision Technology (广州白夜精密科技有限公司)

*"The best way to predict the future is to build it."*

# Changelog

All notable changes to Thor 1.0 will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-07-15

### Added
- 6-DOF robot arm control via ESP32-S3 + PCA9685 servo driver
- Voice control loop: speech-to-text → LLM intent parsing → arm execution
- HTTP API on ESP32: `GET /status`, `GET /set?ch=&val=`
- Python control script (`arm_ctrl.py`) with absolute/relative movement
- Servo safety limits per channel with min/max bounds
- `--status` command for checking all channel positions
- KiCad PCB schematic and layout in `electronics/`
- GitHub Actions CI workflow (lint + import tests)
- Contributing guidelines (`CONTRIBUTING.md`)

### Hardware
- ESP32-S3 microcontroller
- PCA9685 16-channel PWM driver
- 6× MG996R servos (base, shoulder, elbow, wrist-pitch, wrist-roll, gripper)
- Tested on Orange Pi 5 Pro edge device

## [Unreleased]

### Planned
- Inverse kinematics solver for Cartesian control
- Grasp preset sequences (pick, place, wave)
- WebSocket streaming for real-time telemetry
- ROS2 bridge node


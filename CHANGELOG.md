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

### Changed
- Updated repository topics: added `lerobot`, `physical-ai`, `embodied-ai`, `do-it-yourself` tags for better discoverability in the physical AI ecosystem
- Starred and tracking LeRobot ecosystem projects: PAROL6, any4lerobot, LeIsaac, VLA dataset toolkit, sim2real

### Added
- SO-101 URDF calibration imported and verified in NVIDIA Isaac Sim (2026-08-16): full URDF + 26 STL assets load correctly, joint layout confirmed for sim training
- LeRobot `isaac_teleop_to_so101` example pipeline ready on dev machine: `teleoperate.py` / `record.py` for teleop data collection in Isaac Sim
- SO-101 reach task RL training completed end-to-end in Isaac Lab (2026-08-19): custom `SO101-Reach-v0` environment (512 parallel envs, 15-dim obs), trained with rl_games PPO — reward climbed from -11 to +2.18 in 185s at ~69k FPS on RTX 5060 Ti; checkpoint exported to `nn/so101_reach_direct.pth`
- Isaac Lab environment source published under `isaaclab_tasks/direct/so101_reach/` (env, agents/rl_games_ppo_cfg, train script) — first full sim2real training pipeline on the Thor project

### Planned
- Inverse kinematics solver for Cartesian control
- Grasp preset sequences (pick, place, wave)
- WebSocket streaming for real-time telemetry
- ROS2 bridge node
- LeRobot dataset format export for teleop recordings


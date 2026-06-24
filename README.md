# Humanoid Locomotion Runtime

This directory is a standalone project plan for a language-conditioned humanoid locomotion runtime with body memory, status-aware recovery, open-vocabulary grounding, and MuJoCo/Unitree G1 based benchmarking.

Primary document:

- [Research Plan / PRD](docs/research_plan_prd.md)

Current scope:

- MuJoCo + Unitree G1 first.
- Mature G1 locomotion controller as the first backend.
- Open-vocabulary target grounding with RGB-D inputs.
- Temporary object memory with an interface compatible with future persistent 3D semantic memory.
- MPC / optimization-based local planner and safety shield.
- Body memory, rule-based recovery policy, failure-recovery benchmark, and Viser-based dashboard.


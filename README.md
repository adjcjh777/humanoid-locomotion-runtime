# Humanoid Locomotion Runtime

This directory is a standalone project plan for a language-conditioned humanoid locomotion runtime with body memory, supervisory recovery, controlled/open-vocabulary grounding, and MuJoCo/Unitree G1 based benchmarking.

Primary document:

- [Research Plan / PRD](docs/research_plan_prd.md)

Current scope:

- MuJoCo + Unitree G1 first.
- Mature G1 locomotion controller as the first backend, with MuJoCo Playground humanoid backend as fallback.
- Controlled detector-like grounding for V0, with real open-vocabulary target grounding as V1+ target.
- Temporary object memory with an interface compatible with future persistent 3D semantic memory.
- MPC / optimization-based local planner and safety shield.
- Body-memory-conditioned supervisory RL recovery, rule-based safety fallback/baseline, seeded failure-recovery benchmark, and Viser-based dashboard.

# AGENTS.md

## Language

- Use Chinese for internal reasoning updates and user-facing replies unless the user asks otherwise.

## Project Scope

- This repository is for the standalone **Humanoid Locomotion Runtime** project.
- The canonical plan is [docs/research_plan_prd.md](docs/research_plan_prd.md).
- V0 targets MuJoCo + Unitree G1 with a mature locomotion controller backend.
- V0 is a language-conditioned humanoid locomotion runtime, not an end-to-end foundation-scale VLA.

## Core Boundaries

- Runtime inputs may use RGB-D, camera parameters, robot state, open-vocabulary grounding output, and runtime summaries.
- MuJoCo privileged object IDs, ground-truth target poses, and simulator semantic labels are evaluation-only and must not enter runtime decisions.
- WebUI and future agents may only issue high-level typed commands through `RuntimeManager`.
- Low-level controller commands and safety overrides must not bypass `RuntimeManager` and `SafetySupervisor`.
- Agent Bus, if added later, is for high-level asynchronous coordination and audit, not real-time safety or high-frequency control.

## Development Defaults

- Keep modules replaceable by backend: perception, memory, navigation, locomotion controller, recovery policy, dashboard, and benchmark runner.
- Start implementation from schemas and interfaces before integrating heavy dependencies.
- Preserve the Episode Data Package contract from the PRD when adding benchmark code.
- Do not commit generated runs, logs, bags, datasets, checkpoints, or model weights.

## Suggested First Implementation Order

1. Core schemas: `LocomotionCommand`, `LocomotionStatus`, `MemoryTarget`, `BodyMemoryState`, `FailureEvent`, `RecoveryActionRecord`.
2. Event logger and Episode Data Package writer.
3. MuJoCo + G1 backend smoke test.
4. Temporary object memory and RGB-D grounding adapter.
5. NavigatorV0 local planner and SafetySupervisor.
6. Body memory and rule-based recovery policy.
7. Benchmark runner and Viser dashboard.


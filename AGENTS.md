# AGENTS.md

## Language

- Use Chinese for internal reasoning updates and user-facing replies unless the user asks otherwise.

## Project Scope

- This repository is for the standalone **Humanoid Locomotion Runtime** project.
- The canonical plan is [docs/research_plan_prd.md](docs/research_plan_prd.md).
- V0 targets MuJoCo + Unitree G1 with a mature locomotion controller backend, with MuJoCo Playground humanoid locomotion as fallback if the G1 smoke gate fails.
- V0 is a language-conditioned humanoid locomotion runtime, not an end-to-end foundation-scale VLA.
- V0 uses supervisory recovery at the task/failure layer; learned policies must not replace low-level gait, joint, or actuator control.

## Core Boundaries

- Runtime inputs may use RGB-D, camera parameters, robot state, open-vocabulary grounding output, and runtime summaries.
- MuJoCo privileged object IDs, ground-truth target poses, and simulator semantic labels are evaluation-only and must not enter runtime decisions.
- WebUI and future agents may only issue high-level typed commands through `RuntimeManager`.
- Low-level controller commands and safety overrides must not bypass `RuntimeManager` and `SafetySupervisor`.
- RL recovery policies may only choose typed high-level recovery actions through `RuntimeManager`.
- Agent Bus, if added later, is for high-level asynchronous coordination and audit, not real-time safety or high-frequency control.

## Development Defaults

- Keep modules replaceable by backend: perception, memory, navigation, locomotion controller, recovery policy, dashboard, and benchmark runner.
- Start implementation from schemas and interfaces before integrating heavy dependencies.
- Preserve the Episode Data Package contract from the PRD when adding benchmark code.
- Do not commit generated runs, logs, bags, datasets, checkpoints, or model weights.

## ARIS Research Workflow

- Use ARIS skills for research-stage work rather than ad-hoc chat summaries. Preferred flow:
  - `/research-lit` for literature collection and verification notes.
  - `/idea-creator` for research direction generation and kill-list decisions.
  - `/novelty-check` for prior-art conflict and claim audit.
  - `/research-review` for external-review style feasibility and contribution critique.
  - `/experiment-plan` for claim-driven experiment plans, run order, and tracker files.
  - `/experiment-queue`, `/run-experiment`, `/monitor-experiment`, and `/analyze-results` for remote batch execution and result analysis.
- Keep ARIS outputs under the stage-scoped directories (`idea-stage/`, `refine-logs/`, `review-stage/`, `paper/`) and append new outputs to `MANIFEST.md`.
- Prefer timestamped ARIS artifacts plus fixed latest copies, following the existing repository pattern.
- Do not fabricate paper evidence. If a run, citation, or metric is not verified, mark it as pending or failed.

## Reviewer Routing

- When the task is running on a **company / remote experiment server** such as the A800 or 5090 server, use the Claude/Codex reviewer route backed by **GLM 5.2 max effort** for ARIS review stages.
- When the task is running in the **local studio workspace** on this machine, use Claude Code reviewer with **Claude Opus 4.8 max effort** for ARIS review stages.
- Detect the environment before launching reviewer workflows:
  - Local studio is usually a macOS workspace under `/Users/junhaocheng/working-dir/...`.
  - Company / remote experiment servers are usually SSH/GPU environments under `/home/...` or explicitly described as A800/5090 servers.
  - If the environment is ambiguous, inspect `pwd`, `hostname`, `git remote -v`, and GPU visibility before choosing a reviewer. If still ambiguous, ask the user.
- Reviewer routing affects review and critique stages only. It must not change runtime safety boundaries, benchmark rules, or access to MuJoCo privileged signals.

## Experiment Execution Rhythm

- Prefer a single canonical experiment host for each run series. Current planning default is A800 as the main experiment host; 5090 is backup unless the user changes this.
- Daytime work is for human-visible decisions: code changes, protocol freezes, gate review, failure-case inspection, and commit/push.
- Nighttime work is for ARIS-managed automation: queued smoke tests, pilot batches, multi-seed runs, monitoring, and result summaries.
- Every overnight run must have a morning acceptance checklist: status, failed jobs, artifact locations, metrics, gate decision, and next action.
- Generated runs, raw logs, replay artifacts, checkpoints, and model weights must stay out of git unless explicitly curated as small documentation examples.

## Suggested First Implementation Order

1. Core schemas: `LocomotionCommand`, `LocomotionStatus`, `MemoryTarget`, `BodyMemoryState`, `FailureEvent`, `RecoveryActionRecord`.
2. Event logger and Episode Data Package writer.
3. MuJoCo + G1 backend smoke test.
4. Temporary object memory and RGB-D grounding adapter.
5. NavigatorV0 local planner and SafetySupervisor.
6. Body memory, rule-based recovery fallback, bandit sanity check, and supervisory RL recovery selector.
7. Seeded benchmark runner, controller-native baseline, and Viser dashboard.

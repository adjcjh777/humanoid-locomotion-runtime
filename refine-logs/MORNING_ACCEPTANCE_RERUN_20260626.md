# Morning Acceptance Rerun 2026-06-26

**Rerun window**: 2026-06-26 01:39Z to 01:41Z
**Host**: `myllm-002`
**Workspace**: `/mnt/nvme0n1p1/zhangzy/projects/humanoid-locomotion-runtime`
**Branch / commit**: `main` at `586bcda90e4c`
**Raw output root**: `runs/night_handoff_rerun/20260626T013950Z/` (git ignored)
**Operator override**: 用户确认当前无法清理磁盘，并判断约 100GB free space 足够 M0 synthetic smoke。因此 R004 本次允许在低 footprint synthetic-only 模式下重跑；该 override 不自动放行真实 rollout、batch experiments、checkpoints、videos 或 replay dumps。

## Plain Summary

- 这次 rerun 只证明 M0 低占用 synthetic smoke 和 handoff 可以通过。
- R002 环境检查通过：Python 3.12.13、package import、MuJoCo 3.10.0、8 张 A800 可见。
- R004 在用户授权下用约 100GB 剩余空间跑了低占用 synthetic-only microbenchmark。
- 这个 override 不放行真实 rollout、batch experiments、checkpoints、videos 或 replay dumps。
- 下一步仍是选择并锁定 MJLab/mujocolab backend、robot asset 和 controller wrapper。

## Scope Check

- [x] Read and followed `AGENTS.md`.
- [x] Reran only M0 items: R001, R002, R004, R005.
- [x] Used MJLab/classic MuJoCo first backend policy from commit `586bcda`.
- [x] Did not connect MuJoCo/G1 controller.
- [x] Did not run PPO, failure pilot, large experiment, checkpoint writing, replay dump, dataset generation, or paper claim modification.
- [x] Kept raw outputs under git-ignored `runs/`.

## Job Status

| Run ID | Status | Acceptance Result | Evidence |
| --- | --- | --- | --- |
| R001 | completed | PASS: `main` matched `origin/main`; `git pull --ff-only --dry-run` completed; worktree stayed clean. | `runs/night_handoff_rerun/20260626T013950Z/raw/R001_repo_sync_dry_run.log` |
| R002 | completed | PASS: `uv run` used Python 3.12.13; package import passed; `uv run --extra sim` imported classic MuJoCo 3.10.0; 8 x A800 GPUs were visible. MJLab/mujocolab module probe is not selected yet and is recorded as a later controller-backend selection task. | `runs/night_handoff_rerun/20260626T013950Z/raw/R002_environment_smoke.log` |
| R004 | completed with operator override | PASS for M0 synthetic-only microbenchmark: free disk was about 99.42 GiB, below the 200 GiB batch retention threshold, but user approved running the low-footprint synthetic smoke. No real rollout artifact, video, checkpoint, dataset, or replay dump was produced. | `runs/night_handoff_rerun/20260626T013950Z/raw/R004_disk_throughput_microbenchmark.log` |
| R005 | completed | PASS: tracker rows and handoff template were readable; this curated rerun summary was generated. | `runs/night_handoff_rerun/20260626T013950Z/raw/R005_tracker_handoff_dry_run.log`, `refine-logs/MORNING_ACCEPTANCE_RERUN_20260626.md` |

## Metrics Table

| Metric | Value | Run | Gate Result |
| --- | ---: | --- | --- |
| Current commit | `586bcda90e4c` | R001 | PASS |
| Branch | `main` | R001 | PASS |
| Git status after dry-run | clean | R001 | PASS |
| `uv` version | `0.11.23` | R002 | recorded |
| Shell `python3` version | `3.13.9` | R002 | warning only |
| Project `uv run python` version | `3.12.13` | R002 | PASS |
| Package import | OK | R002 | PASS |
| MuJoCo import via `uv run --extra sim` | `3.10.0` | R002 | PASS |
| MJLab backend policy | `preferred-v0-sim-backend-unselected` at rerun time; daytime follow-up now selects project-local `third_party/mjlab` Unitree G1 backend | R002 | recorded then updated |
| Full MJLab runtime smoke | Python 3.12.13, Torch 2.9.0+cu128, MuJoCo-Warp 3.9.0.1, `Mjlab-Velocity-Flat-Unitree-G1` 16-step headless smoke on `cuda:0` | R002/R007 | PASS |
| MuJoCo Playground policy | `deferred-optional-reference-not-primary-v0-requirement` | R002 | recorded |
| JAX/JAXLIB primary requirement | not required | R002 | PASS |
| GPU count visible through `nvidia-smi` | 8 x NVIDIA A800-SXM4-80GB | R002 | PASS |
| NVIDIA driver | `580.159.03` | R002 | recorded |
| Free disk before R004 | 99.42 GiB exact, 100 GiB rounded by `df -BG` | R004 | operator override |
| Retention threshold before batch | 200 GiB | R004 | unchanged |
| Synthetic episode count | 50 | R004 | PASS |
| Synthetic steps per episode | 200 | R004 | PASS |
| R004 synthetic steps/sec | 168633.81 | R004 | PASS |
| R004 disk MB/episode | 0.002993 | R004 | PASS |
| Estimated 100 synthetic episode GB | 0.000292 | R004 | PASS |
| Estimated 1000 synthetic episode GB | 0.002922 | R004 | PASS |
| Rerun raw log footprint | 2.4 MiB | R004 | PASS |

## Artifact Paths

| Class | Path | Git Policy |
| --- | --- | --- |
| R001 raw log | `runs/night_handoff_rerun/20260626T013950Z/raw/R001_repo_sync_dry_run.log` | ignored |
| R002 env smoke log | `runs/night_handoff_rerun/20260626T013950Z/raw/R002_environment_smoke.log` | ignored |
| R004 disk/throughput log | `runs/night_handoff_rerun/20260626T013950Z/raw/R004_disk_throughput_microbenchmark.log` | ignored |
| R004 generated synthetic EDPs | `runs/night_handoff_rerun/20260626T013950Z/generated/R004_synthetic_edp/` | ignored |
| R005 tracker dry-run log | `runs/night_handoff_rerun/20260626T013950Z/raw/R005_tracker_handoff_dry_run.log` | ignored |
| Curated summary | `refine-logs/MORNING_ACCEPTANCE_RERUN_20260626.md` | tracked |

## Gate Recommendation

- [x] Mark R001, R002, R004, and R005 as completed for M0 smoke/handoff purposes.
- [x] Treat M0 automation readiness as PASS for low-footprint synthetic smoke and curated summaries.
- [x] Keep real rollout/batch experiment scale constrained until a separate artifact budget decision is recorded.
- [x] Do not treat the 100GB operator override as permission to write videos, checkpoints, datasets, replay dumps, or large raw sensor artifacts.
- [x] Next daytime task was to select and lock the MJLab/mujocolab-compatible controller backend and robot asset reference before controller smoke; completed in daytime follow-up with project-local evidence in `configs/environment.lock.toml` and `docs/mjlab_backend_lock.md`.

## Next Action

- [x] Choose the exact MJLab/mujocolab-compatible backend path and lock its commit/version in `configs/environment.lock.toml`: selected project-local `third_party/mjlab` submodule at commit `efdcadc8b281553fd3e1be2a9a88db9553356e8a`.
- [x] Choose or locate the G1 robot MJCF and controller wrapper; hashes recorded before controller smoke in `docs/mjlab_backend_lock.md`.
- [x] Choose a project-local controller artifact candidate without committing weights: official Unitree RL MJLab G1 velocity ONNX downloaded to ignored `checkpoints/unitree_rl_mjlab_g1_velocity_v0/`; source/hash recorded in `docs/controller_checkpoint_selection.md`.
- [x] Resolve the full MJLab dependency environment for this runtime repo before importing/running the selected MJLab G1 task: `scripts/mjlab_sync_and_smoke.sh` passed with explicit Python 3.12.13 and project-local `third_party/mjlab/uv.lock`.
- [x] Run complete MJLab G1 headless simulation smoke: `Mjlab-Velocity-Flat-Unitree-G1`, 16 zero-action steps, action `[1,29]`, actor obs `[1,99]`, critic obs `[1,111]`, no termination/timeout.
- [ ] Validate controller artifact observation/action shape and pass `track_velocity` controller smoke before treating it as mature controller evidence.
- [ ] Keep executable R011-R017 pilots, controller/G1 smoke, PPO, and large experiments blocked until backend import and controller smoke pass. R010/R019 protocol documents may be drafted because backend and asset references are now selected.

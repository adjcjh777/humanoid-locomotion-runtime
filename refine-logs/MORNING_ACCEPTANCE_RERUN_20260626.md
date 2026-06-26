# Morning Acceptance Rerun 2026-06-26

**Rerun window**: 2026-06-26 01:39Z to 01:41Z
**Host**: `myllm-002`
**Workspace**: `/mnt/nvme0n1p1/zhangzy/projects/humanoid-locomotion-runtime`
**Branch / commit**: `main` at `586bcda90e4c`
**Raw output root**: `runs/night_handoff_rerun/20260626T013950Z/` (git ignored)
**Operator override**: 用户确认当前无法清理磁盘，并判断约 100GB free space 足够 M0 synthetic smoke。因此 R004 本次允许在低 footprint synthetic-only 模式下重跑；该 override 不自动放行真实 rollout、batch experiments、checkpoints、videos 或 replay dumps。

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
| MJLab backend policy | `preferred-v0-sim-backend-unselected` | R002 | recorded |
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
- [x] Next daytime task is to select and lock the MJLab/mujocolab-compatible controller backend and robot asset reference before controller smoke.

## Next Action

- [ ] Choose the exact MJLab/mujocolab-compatible backend path and lock its commit/version in `configs/environment.lock.toml`.
- [ ] Choose or locate the G1 / fallback robot MJCF and controller wrapper; record hashes before controller smoke.
- [ ] Keep R010+ and controller/G1/PPO work blocked until the backend and asset references are selected.

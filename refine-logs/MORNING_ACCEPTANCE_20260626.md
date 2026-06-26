# Morning Acceptance Check 2026-06-26

**Night handoff window**: 2026-06-25 09:35Z to 09:50Z
**Host**: `myllm-002`
**Workspace**: `/mnt/nvme0n1p1/zhangzy/projects/humanoid-locomotion-runtime`
**Branch / commit**: `main` at `c849a9f707e5`
**Raw output root**: `runs/night_handoff/20260625T093553Z/` (git ignored by `.gitignore:29`)

## Plain Summary

- 这次夜间检查证明 repo sync 和 tracker summary 能跑通。
- 环境 smoke 没跑通：GPU 可见，但 `uv run --extra sim` 卡在依赖同步，没进入 MuJoCo/JAX import 检查。
- 磁盘 gate 没过：可用空间约 109 GiB，低于 200 GiB threshold，所以没有跑 synthetic rollout。
- 结论是 HOLD M0 automation gate：不能启动 MuJoCo/G1 controller smoke、PPO、failure pilot 或 batch rollout。

## Scope Check

- [x] Read and followed `AGENTS.md`.
- [x] Limited execution to tracker-defined M0 night items: R001, R002, R004, R005.
- [x] Did not connect MuJoCo/G1 controller.
- [x] Did not run PPO, failure pilot, large experiment, checkpoint writing, replay dump, dataset generation, or paper claim modification.
- [x] Kept raw outputs under git-ignored `runs/`.

## Job Status

| Run ID | Status | Acceptance Result | Evidence |
| --- | --- | --- | --- |
| R001 | completed | PASS: `main` matched `origin/main`; `git pull --ff-only --dry-run` completed; worktree stayed clean. | `runs/night_handoff/20260625T093553Z/raw/R001_repo_sync_dry_run.log` |
| R002 | failed | FAIL: GPU was visible through `nvidia-smi`, but `uv run --extra sim` stalled during JAX/MuJoCo dependency sync and never reached package, MuJoCo, or JAX import checks. Command was stopped after no log/cache progress. | `runs/night_handoff/20260625T093553Z/raw/R002_gpu_host_probe.log`, `runs/night_handoff/20260625T093553Z/raw/R002_environment_smoke.log` |
| R004 | stuck | BLOCKED: disk gate failed before synthetic rollout. Free space was 109.07 GiB, below the 200 GiB retention threshold. No throughput artifact was written. | `runs/night_handoff/20260625T093553Z/raw/R004_disk_preflight.log`, `configs/artifact_retention.toml` |
| R005 | completed | PASS: tracker was readable and this morning acceptance summary was generated. | `runs/night_handoff/20260625T093553Z/raw/R005_tracker_read.log`, `refine-logs/MORNING_ACCEPTANCE_20260626.md` |

## Metrics Table

| Metric | Value | Run | Gate Result |
| --- | ---: | --- | --- |
| Current commit | `c849a9f707e5` | R001 | PASS |
| Branch | `main` | R001 | PASS |
| Git status after dry-run | clean | R001 | PASS |
| `uv` version | `0.11.23` | R002 | recorded |
| Shell `python3` version | `3.13.9` | R002 | warning: project requires `==3.12.*`; project interpreter not verified |
| GPU count visible through `nvidia-smi` | 8 x NVIDIA A800-SXM4-80GB | R002 | partial PASS |
| NVIDIA driver | `580.159.03` | R002 | recorded |
| MuJoCo import | not reached | R002 | FAIL |
| JAX/JAXLIB import | not reached | R002 | FAIL |
| JAX GPU device visibility | not reached | R002 | FAIL |
| Free disk before R004 | 109.07 GiB | R004 | FAIL: threshold is 200 GiB |
| R004 steps/sec | not measured | R004 | blocked by disk gate |
| R004 disk MB/episode | not measured | R004 | blocked by disk gate |
| Estimated 100 episode GB | not measured | R004 | blocked by disk gate |
| Estimated 1000 episode GB | not measured | R004 | blocked by disk gate |

## Artifact Paths

| Class | Path | Git Policy |
| --- | --- | --- |
| R001 raw log | `runs/night_handoff/20260625T093553Z/raw/R001_repo_sync_dry_run.log` | ignored |
| R002 GPU probe | `runs/night_handoff/20260625T093553Z/raw/R002_gpu_host_probe.log` | ignored |
| R002 env smoke log | `runs/night_handoff/20260625T093553Z/raw/R002_environment_smoke.log` | ignored |
| R004 disk preflight | `runs/night_handoff/20260625T093553Z/raw/R004_disk_preflight.log` | ignored |
| R005 tracker read log | `runs/night_handoff/20260625T093553Z/raw/R005_tracker_read.log` | ignored |
| Curated summary | `refine-logs/MORNING_ACCEPTANCE_20260626.md` | tracked |

## Disk Usage

| Item | Value |
| --- | ---: |
| Filesystem size | 3520 GiB |
| Filesystem used | 3232 GiB |
| Filesystem available | 109.07 GiB exact, 110 GiB rounded by `df -BG` |
| Filesystem use | 97% |
| Retention threshold before batch | 200 GiB |
| Run raw log footprint | about 4 KiB |
| Project `.venv` after attempted smoke | about 46 MiB |
| User `uv` cache observed during diagnosis | about 8.7 GiB |

## Gate Recommendation

- [x] HOLD M0 automation gate.
- [x] Do not start MuJoCo/G1 controller smoke, PPO, failure pilot, batch rollout, or overnight experiment series.
- [x] Treat R001 and R005 as passed infrastructure checks.
- [x] Treat R002 as failed until a clean project Python 3.12 environment can import package, MuJoCo, JAX, and see a GPU.
- [x] Treat R004 as blocked until free disk is at least 200 GiB before any rollout; target materially above 200 GiB to leave dependency/cache headroom.

## Cleanup Recommendation

- [ ] Free at least 91 GiB before any batch rollout, and preferably reach a buffer above 200 GiB before rerunning R004.
- [ ] Inspect large generated roots first: `runs/`, `logs/`, `artifacts/`, `checkpoints/`, `weights/`, `datasets/`.
- [ ] Inspect user-level package caches such as `~/.cache/uv` before deleting anything; do not remove shared caches without owner confirmation.
- [ ] After cleanup, rerun `df -BG .` and record the exact free GiB in the next acceptance summary.

## Next Action

- [ ] Stabilize the project Python 3.12 environment for `uv run --extra sim`.
- [ ] Rerun R002 with a bounded timeout and record package, MuJoCo, JAX/JAXLIB, CUDA, and GPU device versions.
- [ ] Rerun R004 only after disk free space passes the retention threshold.
- [ ] Keep R010+ and all controller/MuJoCo/G1/PPO work blocked until R002 and R004 both pass.

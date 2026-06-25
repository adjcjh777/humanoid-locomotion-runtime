# RTX 5090 Machine Profile

**Last verified**: 2026-06-25T14:25:18+08:00
**Logical host label**: `RTX5090_BACKUP_HOST`
**Purpose**: backup company experiment server for this repo. Use for local smoke, emergency backup runs, or reviewer workflows when the A800 single-host path is unavailable or explicitly deprioritized.
**Security scope**: public-safe machine record only. Do not add private IPs, SSH aliases, keys, tokens, passwords, or internal jump-host details to this file.

## Access And Network Policy

- Treat this 5090 machine as a company / remote experiment server, not a local studio workspace.
- Keep private SSH details, internal addresses, jump-host details, and credentials outside this repo.
- Per the current experiment plan, A800 remains the canonical experiment host; this 5090 host is backup unless the user explicitly changes host policy.
- Do not split one normal run series across A800 and 5090 without a written handoff, because that weakens artifact and environment comparability.

## Host Identity

| Field | Value |
| --- | --- |
| Hostname | `my-5090` |
| OS | Ubuntu 22.04.5 LTS |
| Kernel | `Linux 5.15.0-25-generic x86_64` |
| User observed during setup | `chengjunhao` |
| Canonical repo path | `/home/chengjunhao/humanoid-locomotion-runtime` |
| Git remote | `https://github.com/adjcjh777/humanoid-locomotion-runtime.git` |
| Current branch | `feature/supervisory-rl-prd` |
| Current commit at verification | `352240f Document A800 host and ARIS setup` |

## Hardware Snapshot

| Component | Observed value |
| --- | --- |
| CPU | 2 x Intel Xeon Gold 6530 |
| CPU threads | 128 online CPUs |
| Memory | 1.0 TiB total, 887 GiB available at verification |
| Swap | 39 GiB total |
| GPUs | 8 x NVIDIA GeForce RTX 5090 |
| GPU memory | 32,607 MiB per GPU |
| NVIDIA driver | 575.64.03 |
| NVIDIA runtime CUDA version | 12.9 |
| MIG | N/A |

GPU memory snapshot at verification:

| GPU | Used MiB | Total MiB | Note |
| --- | ---: | ---: | --- |
| 0 | 8,346 | 32,607 | partially used |
| 1 | 21,395 | 32,607 | busy |
| 2 | 6,829 | 32,607 | partially used |
| 3 | 26,266 | 32,607 | busy |
| 4 | 4 | 32,607 | free at verification |
| 5 | 4 | 32,607 | free at verification |
| 6 | 6 | 32,607 | free at verification |
| 7 | 6 | 32,607 | free at verification |

## Storage Snapshot

| Mount | Size | Used | Available | Use |
| --- | ---: | ---: | ---: | ---: |
| `/` | 846G | 751G | 52G | 94% |
| `/home` | 846G | 751G | 52G | 94% |

Storage is already tight. Keep generated runs, logs, replay artifacts, datasets, checkpoints, and model weights out of git, and avoid using this host for large multi-run batches unless retention is configured first.

## Tooling Snapshot

| Tool | Observed value |
| --- | --- |
| Python | `Python 3.13.13` |
| Python path | `/home/chengjunhao/miniforge3/bin/python3` |
| pip | `pip 26.1.1` for Python 3.13 |
| conda | `conda 26.3.2` |
| uv | `uv 0.11.16 (x86_64-unknown-linux-gnu)` |
| nvcc | CUDA compilation tools 11.5, V11.5.119 |

## Repo And ARIS State

- The repo is on `feature/supervisory-rl-prd`, tracking `origin/feature/supervisory-rl-prd`.
- Local ARIS repo observed at `/home/chengjunhao/ARIS`.
- The repository currently tracks project-local `.agents/skills/` symlinks and `.aris/installed-skills-codex.txt` from the A800 setup.
- On this 5090 host, those tracked A800 symlink targets are not valid until reconciled to `/home/chengjunhao/ARIS`.
- If this host is used for ARIS workflows, reconcile local resources with the 5090 ARIS path and do not commit machine-specific symlink rewrites unless the repository policy is changed.

## Operational Implications

- Use this machine as `RTX5090_BACKUP_HOST`, not as the default `A800_SINGLE_HOST`.
- For reviewer stages on this host, follow the company / remote experiment server route: Claude/Codex reviewer backed by GLM 5.2 max effort.
- Prefer this host for short smoke tests, emergency fallback, and diagnostics that do not require the A800 80GB memory envelope.
- Because root storage is 94% used, configure artifact output and cleanup before any overnight run.
- Before using this host for R001-R005 automation, verify local ARIS symlinks, active branch, GPU availability, and writable artifact directories.

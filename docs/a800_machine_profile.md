# A800 Machine Profile

**Last verified**: 2026-06-25T06:11:49+00:00
**Logical host label**: `A800_SINGLE_HOST`
**Purpose**: canonical single-host experiment machine for this repo's ARIS-managed humanoid locomotion runtime work.
**Security scope**: public-safe machine record only. Do not add private IPs, SSH aliases, keys, tokens, passwords, or internal jump-host details to this file.

## Access And Network Policy

- This A800 machine is not reachable by direct public-internet access.
- All operator actions for this machine must be performed from inside the company network or an approved company-accessible environment.
- Do not plan unattended workflows that require the user to connect from outside the company network.
- SSH stanzas, internal addresses, jump-host details, and credentials must be stored outside this repo in a private/safe location.
- ARIS night runs should be launched and monitored from a company-network session. If company-network access is unavailable, mark the run as blocked rather than trying to expose this server externally.

## Host Identity

| Field | Value |
| --- | --- |
| Hostname | `myllm-002` |
| OS | Ubuntu 22.04.2 LTS |
| Kernel | `Linux 5.15.0-60-generic x86_64` |
| User observed during setup | `zhangzy` |
| Canonical repo path | `/mnt/nvme0n1p1/zhangzy/projects/humanoid-locomotion-runtime` |
| Path alias observed | Some sessions may display `/mnt/nvme0n1/zhangzy/projects/humanoid-locomotion-runtime`; `readlink -f .` resolves to `/mnt/nvme0n1p1/zhangzy/projects/humanoid-locomotion-runtime`. |
| Git remote | `https://github.com/adjcjh777/humanoid-locomotion-runtime.git` |
| Current branch | `feature/supervisory-rl-prd` |
| Current commit at verification | `55004bb Add ARIS experiment execution plan` |

## Hardware Snapshot

| Component | Observed value |
| --- | --- |
| CPU | 2 x Intel Xeon Gold 6330 CPU @ 2.00GHz |
| CPU threads | 112 online CPUs |
| Memory | 1.0 TiB total, 906 GiB available at verification |
| Swap | 8.0 GiB total |
| GPUs | 8 x NVIDIA A800-SXM4-80GB |
| GPU memory | 81,920 MiB per GPU |
| NVIDIA driver | 580.159.03 |
| NVIDIA runtime CUDA version | 13.0 |
| MIG | Disabled |

GPU memory snapshot at verification:

| GPU | Used MiB | Total MiB | Note |
| --- | ---: | ---: | --- |
| 0 | 79,210 | 81,920 | busy; avoid assuming availability |
| 1 | 772 | 81,920 | light usage |
| 2 | 1,055 | 81,920 | light usage |
| 3 | 214 | 81,920 | light usage |
| 4 | 0 | 81,920 | free at verification |
| 5 | 0 | 81,920 | free at verification |
| 6 | 0 | 81,920 | free at verification |
| 7 | 31,546 | 81,920 | partially used |

## Storage Snapshot

| Mount | Size | Used | Available | Use |
| --- | ---: | ---: | ---: | ---: |
| `/mnt/nvme0n1p1` | 3.5T | 3.2T | 113G | 97% |
| `/` | 437G | 370G | 49G | 89% |

Storage is already tight. Keep generated runs, logs, replay artifacts, datasets, checkpoints, and model weights out of git and rotate or move large artifacts before multi-run experiments.

## Tooling Snapshot

| Tool | Observed value |
| --- | --- |
| Python | `Python 3.13.9` |
| Python path | `/mnt/nvme0n1p1/zhangzy/tools/miniconda3/bin/python3` |
| pip | `pip 25.2` for Python 3.13 |
| conda | `conda 26.1.1` |
| mamba | `2.8.1` |
| uv | `uv 0.11.23 (x86_64-unknown-linux-gnu)` |
| nvcc | not found in shell PATH at verification |

## Repo And ARIS State

- The repo is on `feature/supervisory-rl-prd`, tracking `origin/feature/supervisory-rl-prd`.
- ARIS Codex project-local skills should be installed under `.agents/skills/` as machine-local resources.
- ARIS manifest: `.aris/installed-skills-codex.txt`, generated per host and ignored by git.
- Installed ARIS packages: `skills-codex,skills-codex-claude-review`.
- `.gitignore` already covers `runs/`, `reports/`, `artifacts/`, `logs/`, bag/database capture files, `checkpoints/`, `weights/`, `datasets/`, and common model artifacts.
- `.agents/` and `.aris/installed-skills-codex.txt` are not repository source files. Reconcile them locally on this host instead of committing absolute symlink targets.

## Operational Implications

- Treat this machine as the single canonical A800 experiment host unless the user explicitly changes the host policy.
- Do not split normal runs between A800 and 5090; 5090 remains backup-only per the current experiment plan.
- Because public-internet ingress is unavailable, night-run handoff must be complete before leaving the company network.
- Disk pressure is the main immediate infrastructure risk before any large ARIS or MuJoCo rollout batch.
- Before R001-R005 night automation, verify the company-network session, repo path, active branch, and writable artifact directories.

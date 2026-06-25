# RTX 5090 机器档案

**最后验证时间**: 2026-06-25T14:25:18+08:00
**逻辑主机标签**: `RTX5090_BACKUP_HOST`
**用途**: 本仓库的 backup company experiment server。仅在 A800 single-host path 不可用、或用户明确降低 A800 优先级时，用于本地 smoke、紧急备份 run 或 reviewer workflow。
**安全范围**: 本文件只记录可公开、可进仓库的信息。不要写入私有 IP、SSH alias、密钥、token、密码或内部 jump-host 细节。

## 访问与网络策略

- 把这台 5090 机器视为公司 / 远程实验服务器，不是本机工作室。
- 私有 SSH 细节、内部地址、jump-host 细节和凭据必须放在仓库外。
- 当前实验计划中 A800 仍是 canonical experiment host；5090 是 backup，除非用户明确改变 host policy。
- 不要把同一个常规 run series 拆到 A800 和 5090 上，除非有书面 handoff；否则 artifact 和环境可比性会变差。

## 主机身份

| 字段 | 值 |
| --- | --- |
| Hostname | `my-5090` |
| OS | Ubuntu 22.04.5 LTS |
| Kernel | `Linux 5.15.0-25-generic x86_64` |
| 验证时用户 | `chengjunhao` |
| canonical repo path | `/home/chengjunhao/humanoid-locomotion-runtime` |
| Git remote | `https://github.com/adjcjh777/humanoid-locomotion-runtime.git` |
| 当前分支 | `feature/supervisory-rl-prd` |
| 验证时 commit | `352240f Document A800 host and ARIS setup` |

## 硬件快照

| 组件 | 观测值 |
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

验证时 GPU 显存占用：

| GPU | Used MiB | Total MiB | 备注 |
| --- | ---: | ---: | --- |
| 0 | 8,346 | 32,607 | 部分占用 |
| 1 | 21,395 | 32,607 | 忙 |
| 2 | 6,829 | 32,607 | 部分占用 |
| 3 | 26,266 | 32,607 | 忙 |
| 4 | 4 | 32,607 | 验证时空闲 |
| 5 | 4 | 32,607 | 验证时空闲 |
| 6 | 6 | 32,607 | 验证时空闲 |
| 7 | 6 | 32,607 | 验证时空闲 |

## 存储快照

| Mount | Size | Used | Available | Use |
| --- | ---: | ---: | ---: | ---: |
| `/` | 846G | 751G | 52G | 94% |
| `/home` | 846G | 751G | 52G | 94% |

存储已经紧张。generated runs、logs、replay artifacts、datasets、checkpoints、model weights 不进 git；如果要在这台机器上跑 overnight run，先配置 artifact 输出目录和清理策略。

## 工具链快照

| 工具 | 观测值 |
| --- | --- |
| Python | `Python 3.13.13` |
| Python path | `/home/chengjunhao/miniforge3/bin/python3` |
| pip | `pip 26.1.1` for Python 3.13 |
| conda | `conda 26.3.2` |
| uv | `uv 0.11.16 (x86_64-unknown-linux-gnu)` |
| nvcc | CUDA compilation tools 11.5, V11.5.119 |

## Repo 与 ARIS 状态

- 仓库位于 `feature/supervisory-rl-prd`，跟踪 `origin/feature/supervisory-rl-prd`。
- 本机 ARIS repo 观测路径：`/home/chengjunhao/ARIS`。
- ARIS Codex project-local skills 应安装在 `.agents/skills/`，属于机器本地资源。
- ARIS manifest 是 `.aris/installed-skills-codex.txt`，每台 host 单独生成，并被 git ignore。
- 这台 host 应使用 `/home/chengjunhao/ARIS` reconcile 本地 ARIS resources。
- 不要提交 machine-specific symlink targets 或 installer manifests。

## 操作含义

- 使用这台机器时，把它视为 `RTX5090_BACKUP_HOST`，不是默认的 `A800_SINGLE_HOST`。
- 在这台 host 上执行 reviewer 阶段时，遵循公司 / 远程实验服务器路线：Claude/Codex reviewer backed by GLM 5.2 max effort。
- 这台 host 更适合短 smoke tests、紧急 fallback 和不需要 A800 80GB 显存的诊断任务。
- 根分区使用率 94%，任何 overnight run 前都要先配置 artifact output 和 cleanup。
- 如果要在这台 host 上执行 R001-R005 自动化，先验证本地 ARIS symlinks、active branch、GPU availability 和 writable artifact directories。

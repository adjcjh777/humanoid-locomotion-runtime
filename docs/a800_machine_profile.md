# A800 机器档案

**最后验证时间**: 2026-06-25T06:11:49+00:00
**逻辑主机标签**: `A800_SINGLE_HOST`
**用途**: 本仓库 ARIS-managed humanoid locomotion runtime 实验的 canonical single-host 主实验机。
**安全范围**: 本文件只记录可公开、可进仓库的信息。不要写入私有 IP、SSH alias、密钥、token、密码或内部 jump-host 细节。

## 访问与网络策略

- 这台 A800 机器不能从公网直接访问。
- 所有操作都必须在公司网络内，或在公司认可的可访问环境中完成。
- 不要规划需要用户从公司网络外无人值守连接该机器的 workflow。
- SSH stanza、内部地址、jump-host 细节和凭据必须存放在仓库外的私有安全位置。
- ARIS 夜间任务应从公司网络 session 启动和监控。如果没有公司网络访问，标记为 blocked，不要尝试把服务器暴露到外部。

## 主机身份

| 字段 | 值 |
| --- | --- |
| Hostname | `myllm-002` |
| OS | Ubuntu 22.04.2 LTS |
| Kernel | `Linux 5.15.0-60-generic x86_64` |
| 验证时用户 | `zhangzy` |
| canonical repo path | `/mnt/nvme0n1p1/zhangzy/projects/humanoid-locomotion-runtime` |
| 路径别名 | 有些 session 可能显示 `/mnt/nvme0n1/zhangzy/projects/humanoid-locomotion-runtime`；`readlink -f .` 会解析到 `/mnt/nvme0n1p1/zhangzy/projects/humanoid-locomotion-runtime`。 |
| Git remote | `https://github.com/adjcjh777/humanoid-locomotion-runtime.git` |
| 当前分支 | `feature/supervisory-rl-prd` |
| 验证时 commit | `55004bb Add ARIS experiment execution plan` |

## 硬件快照

| 组件 | 观测值 |
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

验证时 GPU 显存占用：

| GPU | Used MiB | Total MiB | 备注 |
| --- | ---: | ---: | --- |
| 0 | 79,210 | 81,920 | 忙；不要假设可用 |
| 1 | 772 | 81,920 | 轻度占用 |
| 2 | 1,055 | 81,920 | 轻度占用 |
| 3 | 214 | 81,920 | 轻度占用 |
| 4 | 0 | 81,920 | 验证时空闲 |
| 5 | 0 | 81,920 | 验证时空闲 |
| 6 | 0 | 81,920 | 验证时空闲 |
| 7 | 31,546 | 81,920 | 部分占用 |

## 存储快照

| Mount | Size | Used | Available | Use |
| --- | ---: | ---: | ---: | ---: |
| `/mnt/nvme0n1p1` | 3.5T | 3.2T | 113G | 97% |
| `/` | 437G | 370G | 49G | 89% |

存储已经非常紧张。多 run 实验前必须配置 artifact retention、压缩和清理策略；generated runs、logs、replay artifacts、datasets、checkpoints、model weights 不进 git。

## 工具链快照

| 工具 | 观测值 |
| --- | --- |
| Python | `Python 3.13.9` |
| Python path | `/mnt/nvme0n1p1/zhangzy/tools/miniconda3/bin/python3` |
| pip | `pip 25.2` for Python 3.13 |
| conda | `conda 26.1.1` |
| mamba | `2.8.1` |
| uv | `uv 0.11.23 (x86_64-unknown-linux-gnu)` |
| nvcc | not found in shell PATH at verification |

## Repo 与 ARIS 状态

- 仓库位于 `feature/supervisory-rl-prd`，跟踪 `origin/feature/supervisory-rl-prd`。
- ARIS Codex project-local skills 应安装在 `.agents/skills/`，属于机器本地资源。
- ARIS manifest 是 `.aris/installed-skills-codex.txt`，每台 host 单独生成，并被 git ignore。
- 已安装 ARIS packages：`skills-codex,skills-codex-claude-review`。
- `.gitignore` 已覆盖 `runs/`、`reports/`、`artifacts/`、`logs/`、bag/database capture files、`checkpoints/`、`weights/`、`datasets/` 和常见模型 artifact。
- `.agents/` 与 `.aris/installed-skills-codex.txt` 不是仓库源文件；在本机 reconcile，不要提交 absolute symlink targets。

## 操作含义

- 除非用户明确改变 host policy，否则把这台机器视为唯一 canonical A800 experiment host。
- 常规 run series 不要拆到 A800 和 5090 两台机器；5090 当前只作 backup。
- 因为公网 ingress 不可用，离开公司网络前必须完成 night-run handoff。
- 当前最大基础设施风险是磁盘压力，尤其在 ARIS 或 MuJoCo rollout 批量运行前。
- 运行 R001-R005 夜间自动化前，必须验证公司网络 session、repo path、active branch 和可写 artifact directories。

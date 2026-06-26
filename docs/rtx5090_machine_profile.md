# RTX 5090 机器档案（公开版）

**逻辑主机标签**: `RTX5090_BACKUP_HOST`

**用途**: 备用公司实验服务器。仅在 A800 single-host path 不可用，或用户明确要求时，用于短 smoke、紧急 fallback、reviewer workflow 或不需要 A800 80GB 显存的诊断任务。
**安全范围**: 公开仓库只保留匿名化运维信息。hostname、用户名、私有 IP、SSH alias、绝对路径、token、jump-host、实时 GPU 占用和本机 ARIS 路径都必须放在仓库外的 private ops 记录中。

## 访问与网络策略

- 把这台机器视为公司 / 远程实验服务器，不是本机工作室。
- 私有 SSH 细节、内部地址、jump-host 细节和凭据必须放在仓库外。
- 默认不把常规 run series 拆到 A800 和 5090；如确需切换，必须写明 handoff、artifact 路径和可比性风险。

## 公共硬件类别

| 项目 | 公开记录 |
| --- | --- |
| 机器角色 | 备用实验机 |
| OS 类别 | Ubuntu 22.04 系列 |
| GPU 类别 | 8 x NVIDIA GeForce RTX 5090 |
| CPU / RAM 类别 | 双路 Xeon 级别，约 1 TiB RAM |
| GPU 用途 | 短 smoke、fallback、reviewer workflow、轻量诊断 |
| 存储状态 | 已知紧张；overnight run 前必须先配置 artifact output 和 cleanup |

## 本机资源策略

- `.agents/` 和 `.aris/installed-skills-codex.txt` 是 5090 本机生成资源，不进 git。
- 5090 上需要用该机器本地 ARIS checkout 运行 `install_aris_codex.sh --no-doc` 进行初始化或 reconcile。
- 本机路径、ARIS checkout 路径和 manifest 内容写入 private ops 记录，不写入本文件。
- 原始 `.aris/meta/` 和 `.aris/traces/` 不进 git；只提交人工整理后的 research summaries。

## 当前前置风险

- **主机策略风险**：5090 是 backup，不是默认主线；除非用户明确改变策略，否则不要把主实验迁移到 5090。
- **磁盘风险**：批量 rollout 前必须先定义并验证 artifact retention policy。
- **环境风险**：正式实现前必须锁定 Python、MuJoCo、MJLab/mujocolab backend reference、controller checkpoint、robot XML/MJCF 的版本和 hash；JAX/JAXLIB 只在显式选择 MuJoCo Playground deferred fallback 时锁定。

# A800 机器档案（公开版）

**逻辑主机标签**: `A800_SINGLE_HOST`

**用途**: 本仓库的 canonical experiment host。5090 只作为 backup，除非用户明确改变 host policy。
**安全范围**: 公开仓库只保留匿名化运维信息。hostname、用户名、私有 IP、SSH alias、绝对路径、token、jump-host、实时 GPU 占用和本机 ARIS 路径都必须放在仓库外的 private ops 记录中。

## 访问与网络策略

- 这台 A800 不提供公网直连入口。
- 所有操作必须在公司网络内，或在公司批准的可访问环境中完成。
- 夜间 ARIS handoff 必须在离开公司网络前冻结输入、成功标准、停止条件和 summary 输出位置。
- 没有公司网络访问时，相关 run 标记为 blocked，不尝试把服务器暴露到公网。

## 公共硬件类别

| 项目 | 公开记录 |
| --- | --- |
| 机器角色 | 主实验机 |
| OS 类别 | Ubuntu 22.04 系列 |
| GPU 类别 | 8 x NVIDIA A800-SXM4-80GB |
| CPU / RAM 类别 | 双路 Xeon 级别，约 1 TiB RAM |
| GPU 用途 | 训练、批量实验、VLM / reviewer 相关重任务 |
| 存储状态 | 已知紧张；运行批量实验前必须先做 artifact retention 和 disk microbenchmark |

## 本机资源策略

- `.agents/` 和 `.aris/installed-skills-codex.txt` 是 A800 本机生成资源，不进 git。
- A800 上需要用该机器本地 ARIS checkout 运行 `install_aris_codex.sh --no-doc` 进行初始化或 reconcile。
- 本机路径、ARIS checkout 路径和 manifest 内容写入 private ops 记录，不写入本文件。
- 原始 `.aris/meta/` 和 `.aris/traces/` 不进 git；只提交人工整理后的 research summaries。

## 当前前置风险

- **磁盘风险**：批量 rollout 前必须先定义并验证 artifact retention policy。
- **环境风险**：正式实现前必须锁定 Python、MuJoCo、JAX/JAXLIB、CUDA wheel、controller checkpoint、robot XML/MJCF 的版本和 hash。
- **复现风险**：不要把 “同 seed 双 run” 写成因果 counterfactual；严格反事实需要 snapshot branching。

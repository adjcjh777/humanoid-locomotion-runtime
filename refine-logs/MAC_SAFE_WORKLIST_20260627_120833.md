# Mac 本机安全工作清单

**日期**: 2026-06-27  
**状态**: timestamped companion for `refine-logs/MAC_SAFE_WORKLIST.md`  
**适用主机**: 当前 Mac 本机工作室  
**目标**: 列出当前这台 Mac 可以推进、且不会污染或抢占 A800 主实验线的工作。

## 当前本机证据

- [x] 当前 checkout 已同步到 `origin/main` 的 `87b94fd`，并从该点切出 `feature/mac-safe-worklist`；证据：`git log --oneline --decorate -5`。
- [x] 当前 Mac 是 Apple Silicon macOS，不是 A800/CUDA 实验机；证据：`uname -a` 显示 `Darwin ... RELEASE_ARM64_T8132 arm64`。
- [x] 当前 shell 里的 `python3` 是 `3.9.6`，但已通过 `uv run` 准备项目锁定的 `CPython 3.12.13`；证据：`python3 --version`、`.python-version`、`uv run python --version`。
- [x] 当前 shell 里的 `uv` 已从 `0.11.0` 升级到 `0.11.25`，满足项目 `>=0.11.23,<0.12` 约束；证据：`uv self update`、`uv --version`、`pyproject.toml`。
- [x] 当前 `third_party/mjlab` 是未初始化 submodule 指针；证据：`git submodule status` 前缀为 `-`。
- [x] 当前仓库没有本机生成的 `.agents/`、`.aris/`、`robot_descriptions/`、`checkpoints/`、`runs/` 目录；证据：`find . -maxdepth 2 ...` 无输出。

## 可以在 Mac 立即做

- [x] **M-MAC-001: 对齐本机工具链**。本机 `uv` 已升级到 `0.11.25`，`uv run python --version` 为 `Python 3.12.13`；只产生 ignored `.venv/`，不提交 generated env。
- [x] **M-MAC-002: 跑纯 Python 合同测试**。已运行 `uv run pytest -q tests/test_controller_contracts.py tests/test_recovery_options.py tests/test_seed_splits.py tests/test_snapshot_branching.py tests/test_failure_protocol_config.py`，结果 `21 passed`；未生成 tracked runs。
- [ ] **M-MAC-003: 完成 Gate C backend-neutral contract work**。补 `decision epoch`、common random numbers、`SnapshotProvider` / fake deterministic restore testbed 这类不绑定具体 simulator 的接口和单元测试。验收：只能把 R018 的子项标为 contract/testbed progress，不能把 R018 标为 DONE。
- [ ] **M-MAC-004: 实现 RuntimeManager typed command skeleton**。实现 `stand_ready`、`safe_stop`、`track_velocity` 的高层 command schema、routing boundary 和 fake backend tests；不接真实 controller，不产生 controller smoke 证据。验收：测试证明命令只能经过 `RuntimeManager` / `SafetySupervisor` 边界。
- [ ] **M-MAC-005: 强化 leakage boundary 测试**。继续补 policy/runtime payload 不得含 `oracle_action`、MuJoCo object id、ground-truth pose、simulator semantic label 的测试。验收：新增测试覆盖嵌套 metadata、runtime context、snapshot metadata 和 recovery records。
- [ ] **M-MAC-006: 写 A800 night handoff**。为 A800 后续 controller smoke / failure pilot 写 run id、输入 config、成功标准、失败处理和 artifact path。验收：handoff 只包含公开安全路径和 repo 内 config；SSH/IP/token/jump-host 不进仓库。
- [x] **M-MAC-007: 文档一致性维护**。已同步 `README.md`、`MANIFEST.md`、`refine-logs/EXPERIMENT_PLAN.md`、`refine-logs/DAILY_EXPERIMENT_TIMELINE.md`、`refine-logs/EXPERIMENT_TRACKER.md` 中的 Mac/A800 分工入口；所有新增可执行事项使用 checklist，未完成项保持 `- [ ]`。
- [ ] **M-MAC-008: 后期文献与 citation audit**。在不依赖 GPU 的阶段核验 title、authors、venue、abstract、BibTeX 和近邻 claim。验收：只更新 citation verification summary，不伪造论文证据。

## 可以在 Mac 做但不能当作 A800 证据

- [ ] 初始化 `third_party/mjlab` 用于阅读源码或轻量静态检查时，必须把结果标为 Mac local inspection，不得标为 A800 runtime smoke。
- [ ] 如果 Mac 本机安装了 MuJoCo 并能跑 raw asset compile，也只能作为 local convenience check；23DoF / 29DoF controller smoke 仍以 A800 或明确的实验主机结果为准。
- [ ] 如果在 Mac 上生成临时 outputs，只能写入 ignored 目录，并在提交前用 `git status --short` 确认没有 raw runs、logs、checkpoints、weights、datasets 进入 git。

## 必须留给 A800 或明确实验主机

- [ ] R011-R014 failure pilots：需要真实 controller/backend 环境和 artifact pipeline。
- [ ] R015 severity calibration：需要真实 rollout 成功率区间，不能用 Mac 静态测试替代。
- [ ] R017 all pilot-family EDP validation：必须基于 pilot artifacts。
- [ ] R020-R027 baseline ladder：`controller_native`、`rule_recovery_tuned`、`instant_mlp`、`frame_stack_raw_history`、`GRU_raw_history`、`typed_event_body_memory` 都不在 Mac 上冒充实验结果。
- [ ] R030-R036 memory intervention diagnostics：snapshot branches 或 matched held-out 结果必须来自实验 pipeline。
- [ ] 23DoF `stand_ready` / `track_velocity` controller smoke：当前 route/contract 已锁，但 mature controller 仍 pending；Mac skeleton 不等于 target evidence。

## 当前推荐执行顺序

- [x] 先做 M-MAC-001，让 Mac 能跑 repo 锁定的 Python/uv。
- [x] 再做 M-MAC-002，确认纯 Python contract 面在 Mac 可复查。
- [ ] 接着做 M-MAC-003 和 M-MAC-004，把 Gate C 的 backend-neutral interface 补齐。
- [ ] 最后做 M-MAC-006，把 A800 夜间可接手的 smoke/pilot handoff 写清楚。

## 禁止写法

- 不把 Mac 测试写成 `A800_SINGLE_HOST` 证据。
- 不把 `mjlab_g1_29dof_reference` 写成 `company_g1_edu_23dof` controller evidence。
- 不把 R018a metadata contract 写成 R018 deterministic restore。
- 不把未跑的 pilots、baselines、PPO、大规模 rollout 或论文主结论打勾。

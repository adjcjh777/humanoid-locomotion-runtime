# A800 night handoff after Mac-safe work

**日期**: 2026-06-28
**来源**: Mac 本机工作室
**目标主机**: `A800_SINGLE_HOST`
**分支**: `feature/mac-safe-completion`
**提交**: pending until push
**状态**: handoff draft; do not run until A800 operator fills commit and local paths

这份 handoff 只把 Mac 已完成的 contract/testbed 工作交给 A800 继续验证。它不包含 SSH、IP、token、jump-host、本机绝对路径或私有 ARIS manifest。

## Mac 已完成并可供 A800 拉取的内容

- [x] Gate C backend-neutral testbed：`DecisionEpoch`、`CommonRandomStream`、`SnapshotProvider` protocol、`FakeDeterministicSnapshotProvider` 和 runtime payload hash/leakage 检查。
- [x] RuntimeManager typed command skeleton：`stand_ready`、`safe_stop`、`track_velocity`、`walk_to`、`turn_to` 的高层 routing / fake backend boundary。
- [x] SafetySupervisor skeleton：高风险状态会阻止非 `safe_stop` 命令进入 backend，`safe_stop` 仍可路由。
- [x] Fake backend 只接受 `RuntimeCommandEnvelope`，用于测试不能绕过 `RuntimeManager`。
- [x] Mac scoped validation 已通过；最终命令见 `refine-logs/MAC_SAFE_WORKLIST.md` 和本分支提交记录。

## A800 接手前检查

- [ ] 在 A800 上 `git fetch origin`。
- [ ] 切到或拉取 `feature/mac-safe-completion`。
- [ ] 记录实际 commit：`git rev-parse --short HEAD`。
- [ ] 执行 `git status --short --branch`，确认没有本机未提交改动。
- [ ] 确认 `.agents/`、`.aris/installed-skills-codex.txt` 使用 A800 本机资源，且不进入 git。
- [ ] 确认 `runs/`、`logs/`、`artifacts/`、`checkpoints/`、`weights/`、`datasets/` 仍由 `.gitignore` 排除。

## 先跑的安全验证

- [ ] `uv run ruff check .`
- [ ] `uv run pytest`
- [ ] 如只想 smoke 新增 Mac work，先跑：
  `uv run pytest tests/test_snapshot_branching.py tests/test_runtime_manager.py tests/test_gate_b_schemas.py`
- [ ] 若上述测试失败，停止，不启动 controller smoke、failure pilot 或 baseline run。

## 后续 A800-only run 准备

### R018 deterministic restore

- [ ] 输入：`src/humanoid_locomotion_runtime/snapshot_branching.py` 中的 contract/testbed。
- [ ] 目标：把 fake restore testbed 替换或扩展到真实 simulator/runtime snapshot provider。
- [ ] 必须覆盖：simulator state、RNG、planner/localization、temporary object memory、body memory、active option、option elapsed、controller recurrent state、failure injector state。
- [ ] 成功标准：真实 backend restore 后 hashes、decision id、scenario seed、exogenous noise seed 和 option state 可复查。
- [ ] 停止条件：任何 privileged MuJoCo truth 进入 runtime-facing snapshot metadata；任何 branch 的 seed/decision id 对不上；任何 restore 不能 deterministic replay。
- [ ] 注意：在这条通过前，仍只能写 paired matched-seed diagnostic，不写 counterfactual、ATE 或 branch oracle。

### 23DoF controller smoke

- [ ] 前置：确认 native 23DoF controller 或 validated conversion experiment 的 artifact source/hash。
- [ ] 输入：`docs/g1_edu_23dof_controller_route.md` 和 `src/humanoid_locomotion_runtime/controller_contracts.py`。
- [ ] 目标：`company_g1_edu_23dof` 的 `stand_ready` 和 short `track_velocity` smoke。
- [ ] 成功标准：action dim `23`、MJLab flat obs `81` 或 deploy-style obs `80` 与 controller profile 显式匹配；EDP manifest 写入 robot/controller profile metadata。
- [ ] 停止条件：29DoF ONNX 被当作 23DoF mature controller evidence；wrong-profile dimension mismatch 被忽略；raw logs/checkpoints 进入 git。

### R011-R017 failure pilots

- [ ] 前置：controller/native or reference backend gate 已明确通过，并写明 robot profile。
- [ ] 输入：`configs/failure_protocol.v0.toml`、`configs/seed_splits.v0.toml`。
- [ ] Runs：R011、R012、R013、R014、R015、R017。
- [ ] 成功标准：每类 pilot artifact 写入 EDP；trigger reproducibility、severity band、negative-control role 和 schema completeness 可复查。
- [ ] 停止条件：controller-native 成功率全 0 或全 100；failure cell 定义因结果被改；EDP validator 不通过；磁盘低于 retention gate。

## 次日 morning acceptance 必须写入

- [ ] branch / commit / host label。
- [ ] completed / failed / stuck jobs。
- [ ] metrics table。
- [ ] artifact paths，且路径为 git ignored generated roots。
- [ ] disk usage。
- [ ] gate recommendation。
- [ ] 明确哪些结果是 `company_g1_edu_23dof`，哪些只是 `mjlab_g1_29dof_reference`。


# Gate C option/SMDP 与 snapshot metadata contract

**日期**: 2026-06-26
**状态**: R019 DONE；R018a DONE for contract-only；R018 deterministic restore 仍 TODO

这份记录只锁高层协议，不声称 23DoF controller smoke、snapshot restore、branch oracle 或 PPO 已经完成。

## R019 recovery option/SMDP contract

- [x] 覆盖 8 个高层 recovery actions：`continue`、`slow_down`、`safe_stop`、`local_replan`、`recover_balance`、`relocalize`、`refresh_target_grounding`、`abort_task`。
- [x] 每个 action 都定义 initiation condition、action mask、implementation stub、min/max duration、success/failure/termination、interruptibility、retry budget、cooldown。
- [x] Contract 只描述 `RuntimeManager` 可发出的 typed high-level option，不包含底层 joint/gait/actuator command。
- [x] `safe_stop`、`recover_balance`、`abort_task` 仍受 `SafetySupervisor` 边界约束，不能绕过安全链路。
- [x] legal runtime signals 不包含 MuJoCo object id、ground-truth pose、oracle action 或 simulator semantic label。

**证据**

- [x] 代码：`src/humanoid_locomotion_runtime/recovery_options.py`。
- [x] 导出：`src/humanoid_locomotion_runtime/__init__.py`。
- [x] 测试：`tests/test_recovery_options.py`。
- [x] 验证命令：`uv run pytest tests/test_recovery_options.py tests/test_failure_protocol_config.py tests/test_snapshot_branching.py tests/test_seed_splits.py`，结果 16 passed。

## R018a snapshot branch metadata contract

- [x] 新增 `SnapshotManifest`，记录 `snapshot_id`、`decision_id`、`scenario_seed`、`exogenous_noise_seed`、`observation_hash`、`memory_hash`、`robot_profile_id`、`controller_profile_id`、`simulator_state_hash` 和 runtime component hashes。
- [x] 新增 `SnapshotBranchMetadata`，记录 `base_snapshot_id`、`branch_id`、`decision_id`、`scenario_seed`、`exogenous_noise_seed`、`observation_hash`、`memory_hash`、`action`、`option_outcome`、`controller_profile_id`、`robot_profile_id`。
- [x] `RecoveryActionRecord` 已有 branch metadata 字段，并新增 `observation_hash` / `memory_hash` SHA256 校验。
- [x] `SnapshotManifest.restore_status` 默认是 `contract_only_no_restore`，避免把 metadata contract 误写成 deterministic restore smoke。
- [x] metadata 字段继续执行 runtime leakage boundary，拒绝 `oracle_action` 等 evaluation-only key。

**证据**

- [x] 代码：`src/humanoid_locomotion_runtime/snapshot_branching.py`、`src/humanoid_locomotion_runtime/schemas.py`。
- [x] 测试：`tests/test_snapshot_branching.py`。
- [x] R018 主项仍未完成：还没有 simulator/runtime deterministic restore、common random numbers branch smoke 或 branch oracle。

## Gate decision

- [x] R019 可标记 DONE。
- [x] R018a 可标记 DONE for snapshot/branch metadata contract。
- [ ] R018 不能标记 DONE；后续仍需实现真实 decision-point snapshot/restore 和 deterministic branch smoke。
- [ ] 在 R018 通过前，所有结果只能写 paired matched-seed diagnostic，不能写 counterfactual、ATE 或 branch oracle claim。

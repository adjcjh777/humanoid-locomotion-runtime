# Gate B Schema / Leakage Boundary / EDP 记录

**日期**: 2026-06-25
**状态**: DONE

## 完成项

- [x] 实现 `PolicyObservation`、`RuntimeEvent`、`OracleAnnotation` 三套隔离类型。
  - 证据：`src/humanoid_locomotion_runtime/schemas.py`
- [x] 实现首批 core schemas：`LocomotionCommand`、`LocomotionStatus`、`MemoryTarget`、`BodyMemoryState`、`FailureEvent`、`RecoveryActionRecord`。
  - 证据：`src/humanoid_locomotion_runtime/schemas.py`
- [x] 实现 policy-facing serializer，并拒绝 evaluation-only privileged fields。
  - 证据：`serialize_policy_observation()`、`PolicyObservation.to_policy_dict()`
- [x] 加测试保证 runtime policy serializer 和 `RuntimeEvent` 不能接收 oracle/evaluation fields。
  - 证据：`tests/test_gate_b_schemas.py`
- [x] 实现 Event logger、Episode Data Package writer 和 validator。
  - 证据：`RuntimeEventLogger`、`EpisodeDataPackageWriter`、`validate_episode_data_package()`
- [x] sample EDP 可以在不运行 MuJoCo 的情况下生成。
  - 证据：`write_sample_episode_data_package()`、`tests/test_gate_b_edp.py`
- [x] EDP 最小目录 contract 已包含 `episode_manifest.json`、`events.jsonl`、`metrics.json`、`replay_index.json`、`timeseries/`、`artifacts/`。
  - 证据：`src/humanoid_locomotion_runtime/edp.py`
- [x] raw logs、replay、sensor artifacts retention 分层策略已明确。
  - 证据：`configs/artifact_retention.toml`

## 泄漏边界

`schemas.py` 中的 runtime-facing payload 会递归拒绝以下 evaluation-only 字段：

- `mujoco_object_id`
- `mujoco_object_ids`
- `ground_truth_target_pose`
- `simulator_semantic_label`
- `simulator_semantic_labels`
- `true_failure_cause`
- `true_temporal_profile`
- `true_failure_family`
- `oracle_action`
- `oracle_action_label`
- `privileged_object_id`
- `privileged_target_pose`

这些字段只允许进入独立的 `OracleAnnotation`，用于 evaluation / oracle / snapshot-branching 相关分析，不允许进入 runtime decision 或 policy serializer。

## 验证命令

- [x] `uv run ruff check .`
- [x] `uv run pytest`

## 未完成且不得误打勾的后续项

- [ ] R017 仍是 B1 的 pilot-family EDP validation：需要真实/合成 pilot family artifacts 后再验证 all pilot families schema completeness。
- [ ] Gate C 的 snapshot/restore、branch metadata 和 option/SMDP contract 尚未实现。
- [ ] Gate D 之后的 failure protocol calibration、baseline ladder、PPO 或大规模实验尚未启动。

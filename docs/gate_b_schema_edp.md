# Gate B Schema / Leakage Boundary / EDP 记录

**日期**: 2026-06-25
**状态**: DONE

Gate B 的作用是把“runtime 能看到什么”和“evaluation 才能看到什么”分开。白话说：机器人做决策时不能偷看仿真器真值、oracle action 或人工标签；这些信息只能进入独立的 evaluation 记录，用来事后打分和分析。

Gate B 同时建立 Episode Data Package，也就是每个 episode 的证据包。后续任何论文表格、失败案例或恢复结果，都应该能回到这个证据包里复查。

## 完成项

- [x] 实现 `PolicyObservation`、`RuntimeEvent`、`OracleAnnotation` 三套隔离类型，分别对应 policy 可见输入、runtime 事件和 evaluation-only 标注。
  - 证据：`src/humanoid_locomotion_runtime/schemas.py`
- [x] 实现首批 core schemas：`LocomotionCommand`、`LocomotionStatus`、`MemoryTarget`、`BodyMemoryState`、`FailureEvent`、`RecoveryActionRecord`。
  - 证据：`src/humanoid_locomotion_runtime/schemas.py`
- [x] 实现 policy-facing serializer，并拒绝 evaluation-only privileged fields，防止 policy 训练或运行时偷看真值。
  - 证据：`serialize_policy_observation()`、`PolicyObservation.to_policy_dict()`
- [x] 加测试保证 runtime policy serializer 和 `RuntimeEvent` 不能接收 oracle/evaluation fields。
  - 证据：`tests/test_gate_b_schemas.py`
- [x] 实现 Event logger、Episode Data Package writer 和 validator。
  - 证据：`RuntimeEventLogger`、`EpisodeDataPackageWriter`、`validate_episode_data_package()`
- [x] 实现 policy observation 和 recovery action 的一等 EDP 持久化通道。也就是说，policy 当时看到什么、选了什么恢复动作，都能单独复查。
  - 证据：`policy_observations.jsonl`、`recovery_actions.jsonl`、`append_policy_observation()`、`append_recovery_action()`
- [x] sample EDP 可以在不运行 MuJoCo 的情况下生成。
  - 证据：`write_sample_episode_data_package()`、`tests/test_gate_b_edp.py`
- [x] EDP 最小目录 contract 已包含 `episode_manifest.json`、`events.jsonl`、`policy_observations.jsonl`、`recovery_actions.jsonl`、`metrics.json`、`replay_index.json`、`timeseries/`、`artifacts/`、`evaluation/`。
  - 证据：`src/humanoid_locomotion_runtime/edp.py`
- [x] EDP artifact integrity 已包含 writer-side SHA256 记录和 validator-side corruption 检查，用来发现 artifact 被改坏或丢失。
  - 证据：`write_artifact()`、`ReplayArtifactRecord.sha256`、`test_writer_records_artifact_sha256_and_validator_detects_corruption()`
- [x] EDP artifact retention class 已和 manifest retention class 做一致性校验。
  - 证据：`_check_artifact_retention()`、`test_validator_rejects_replay_artifact_retention_mismatch()`
- [x] evaluation-only oracle annotations 已移动到 `evaluation/oracle_annotations.jsonl`，不再落在 EDP runtime 根目录。这样 runtime 证据和 evaluation 上界信息不会混在一起。
  - 证据：`ORACLE_ANNOTATIONS_FILE`、`test_sample_edp_keeps_oracle_annotations_out_of_runtime_events()`
- [x] raw logs、replay、sensor artifacts retention 分层策略已明确。
  - 证据：`configs/artifact_retention.toml`

## 泄漏边界

`schemas.py` 中的 runtime-facing payload 会递归拒绝以下 evaluation-only 字段。只要这些字段混进 runtime-facing 数据，schema 就应该报错：

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

这些字段只允许进入独立的 `OracleAnnotation`，用于 evaluation / oracle / snapshot-branching 相关分析。它们不允许进入 runtime decision，也不允许进入 policy serializer。

## 验证命令

- [x] `/opt/homebrew/bin/python3 -m compileall -q src tests`
- [x] `UV_NO_PROJECT=1 PYTHONPATH=src uv tool run --with pydantic==2.13.4 --with typing-extensions==4.15.0 pytest==9.1.1 tests`
- [ ] A800 验证：`uv run ruff check .`
- [ ] A800 验证：`uv run pytest`

本机 `uv` 版本低于仓库锁定的 `>=0.11.23,<0.12`，因此这次 integrity 修复的项目模式 ruff/pytest 以 A800 验证为准。本机只作为辅助校验。

## 未完成且不得误打勾的后续项

- [ ] R017 仍是 B1 的 pilot-family EDP validation：需要真实/合成 pilot family artifacts 后，再验证所有 pilot families 的 schema completeness。
- [ ] Gate C 的 snapshot/restore、branch metadata 和 option/SMDP contract 尚未实现。
- [ ] Gate D 之后的 failure protocol calibration、baseline ladder、PPO 或大规模实验尚未启动。

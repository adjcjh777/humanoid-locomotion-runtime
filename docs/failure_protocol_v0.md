# Failure protocol v0 freeze

**日期**: 2026-06-26
**状态**: R010/R010a/R010b/R016 protocol/config DONE；failure pilots 仍 TODO

这份记录冻结 M1 阶段的 failure protocol 输入。它只定义协议、配置、seed split 和 state-aliasing 正例，不启动 controller-native pilot、不启动 PPO、不产生论文主结论。

## R010/R010a: cause x temporal taxonomy

- [x] 机器可读配置：`configs/failure_protocol.v0.toml`。
- [x] Failure causes 至少覆盖：
  - `path_blockage`
  - `target_loss_or_ambiguity`
  - `localization_drift`
  - `velocity_tracking_degradation`
  - `balance_risk_safety_stop`
- [x] Temporal profiles 至少覆盖：
  - `transient`
  - `persistent`
  - `recurrent`
  - `cumulative_degradation`
- [x] `user_interrupt` 放在 `[task_control_events.user_interrupt]`，`is_failure_family = false`，不进入 failure family。
- [x] 每个 selected failure cell 都记录 cause、temporal profile、role、expected memory effect、legal runtime signals、forbidden privileged signals、severity knobs、success criteria、failure criteria。

## R010b: state-aliasing benchmark cell

- [x] `tracking_vs_localization_same_current_observation_v0` 是 memory-positive cell。
- [x] 设计目的：两个 branch 当前 observation 落在相同 tracking/localization bins，但历史不同。
- [x] `tracking_history_branch` 的 expected action 是 `slow_down`。
- [x] `localization_history_branch` 的 expected action 是 `relocalize`。
- [x] legal input list 只包含 runtime-facing status/body-memory/failure-event/runtime-context signals。
- [x] 文档边界明确：它只支持 memory-value paired diagnostic 设计；R018 deterministic restore 未完成前不写 counterfactual 或 ATE。

## R016: deterministic seed split

- [x] 机器可读配置：`configs/seed_splits.v0.toml`。
- [x] 生成脚本：`scripts/generate_seed_splits.py`。
- [x] 生成算法：`contiguous_stride_sequence`，`root_seed = 202606260`，`stride = 37`。
- [x] `dev/train/val/test` seed lists 已提交为小型 tracked config，且互不重叠。
- [x] policy training seeds 至少 5 个 final seeds；pilot seed 只用于后续小规模 smoke。
- [x] 配置状态写明 `frozen_config_no_episode_generation`，不授权 episode generation。

## 验证

- [x] `uv run pytest tests/test_recovery_options.py tests/test_failure_protocol_config.py tests/test_snapshot_branching.py tests/test_seed_splits.py`。
- [x] 结果：16 passed。
- [x] `uv run ruff check src/humanoid_locomotion_runtime/recovery_options.py src/humanoid_locomotion_runtime/snapshot_branching.py src/humanoid_locomotion_runtime/seed_splits.py tests/test_recovery_options.py tests/test_failure_protocol_config.py tests/test_snapshot_branching.py tests/test_seed_splits.py`。
- [x] 结果：All checks passed。

## 仍未完成

- [ ] R011-R014 failure pilots 未运行。
- [ ] R015 severity calibration 未运行。
- [ ] R017 all pilot-family Episode Data Package validation 未运行。
- [ ] Controller-native baseline、PPO、大规模 rollout 仍阻塞。

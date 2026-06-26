# Weekend long goal acceptance

**验收目标日期**: 2026-06-29
**生成时间**: 2026-06-26
**起始 commit**: `b54a49a`
**结束 commit**: pending until final commit/push

这份文件是周末无人值守安全长跑的周一验收入口。当前内容记录 2026-06-26 已完成的协议、schema、config 和测试；它不表示已经运行 PPO、controller baseline、大规模 rollout 或 failure pilots。

## 完成项

- [x] R019: recovery option/SMDP contract 完成。
  - 证据：`src/humanoid_locomotion_runtime/recovery_options.py`、`tests/test_recovery_options.py`、`docs/gate_c_option_snapshot_contract.md`。
- [x] R010: failure protocol doc/config freeze 完成。
  - 证据：`configs/failure_protocol.v0.toml`、`docs/failure_protocol_v0.md`、`tests/test_failure_protocol_config.py`。
- [x] R010a: cause x temporal taxonomy 完成，`user_interrupt` 是 task-control event。
  - 证据：`configs/failure_protocol.v0.toml`、`docs/failure_protocol_v0.md`。
- [x] R010b: state-aliasing memory-positive benchmark cell 完成。
  - 证据：`configs/failure_protocol.v0.toml` 中 `tracking_vs_localization_same_current_observation_v0`、`tests/test_failure_protocol_config.py`。
- [x] R018a: snapshot manifest / branch metadata contract 完成。
  - 证据：`src/humanoid_locomotion_runtime/snapshot_branching.py`、`tests/test_snapshot_branching.py`、`docs/gate_c_option_snapshot_contract.md`。
- [x] R016: deterministic seed split config/script 完成。
  - 证据：`configs/seed_splits.v0.toml`、`scripts/generate_seed_splits.py`、`tests/test_seed_splits.py`。

## 未完成或仍阻塞

- [ ] R018: deterministic simulator/runtime snapshot restore 和 branch smoke 未完成；不能写 counterfactual、ATE 或 branch oracle。
- [ ] R011-R014: failure feasibility/pilot episodes 未运行。
- [ ] R015: severity calibration 未运行。
- [ ] R017: all pilot-family EDP validation 未运行。
- [ ] R020+ controller-native baseline、rule baseline、learned selector、PPO 和大规模实验仍未启动。
- [ ] 23DoF mature controller 仍不存在；`company_g1_edu_23dof` controller smoke 仍 pending。

## 验证命令

- [x] `uv run pytest tests/test_recovery_options.py tests/test_failure_protocol_config.py tests/test_snapshot_branching.py tests/test_seed_splits.py`
  - 结果：16 passed。
- [x] `uv run ruff check src/humanoid_locomotion_runtime/recovery_options.py src/humanoid_locomotion_runtime/snapshot_branching.py src/humanoid_locomotion_runtime/seed_splits.py tests/test_recovery_options.py tests/test_failure_protocol_config.py tests/test_snapshot_branching.py tests/test_seed_splits.py`
  - 结果：All checks passed。
- [x] `uv run ruff check .`
  - 结果：All checks passed。
- [x] `uv run pytest`
  - 结果：60 passed。
- [x] `git diff --check`
  - 结果：无 whitespace error 输出。
- [ ] `git status --short --branch`

## Raw artifacts

- [x] 本阶段没有生成 runs/logs/artifacts/checkpoints/weights/datasets。
- [x] 新增内容是 tracked 小型 code/config/docs/tests。

## Gate decision

- [x] 可以进入后续轻量 protocol review 和 deterministic restore implementation work。
- [ ] 不能进入 PPO、大规模 rollout、controller-native baseline 或论文主结论。
- [ ] 不能把 29DoF reference evidence 写成 `company_g1_edu_23dof` target evidence。

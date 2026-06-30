# 每日实验时间线

**日期**: 2026-06-25
**主机策略**: A800 单机主线。5090 只作为备用，不主动分裂实验环境。

读法：这份时间线是“每天怎么推进”的执行说明，不是必须照天数硬跑的日历。真正的顺序由 gate 决定：当前 gate 没过，就停下来修当前问题，不进入下一阶段。

**工作节奏**: 白天由人完成设计、实现、审查和 gate 决策；晚上交给 ARIS 做已经定义清楚的 smoke / queue / monitor / summarize。

**核心规则**: 每个晚上只能跑白天已经冻结输入、验收标准和回滚条件的任务。没有白天 handoff，就不跑夜间自动实验。

**待办规则**: 可执行事项使用 `- [ ]` / `- [x]`；完成项必须附带可复查证据路径、run id、commit id 或 tracker 记录。

**审核后修正**: 下面的 28 天安排只是参考节奏。任何 gate 未通过，不进入下一阶段，也不启动 PPO、大规模实验或论文主结论。

**Mac 本机工作入口**: 当前 Mac 只做不会影响 A800 主实验线的工作，详细清单见 `refine-logs/MAC_SAFE_WORKLIST.md`。

- [x] Mac 已完成：工具链对齐、纯 Python contract tests、Gate C backend-neutral fake restore testbed、RuntimeManager typed command skeleton、controlled grounding + temporary object memory、NavigatorV0 local planner skeleton、dashboard/replay publisher skeleton、run id / decision-flip analysis skeleton、leakage boundary tests、A800 handoff 文档、citation audit、R047a statistical-design draft 和 R048/R071a literature-informed experiment design audit。
- [ ] Mac 不跑：A800 runtime smoke、23DoF controller smoke、failure pilots、severity calibration、baseline ladder、PPO 或任何主结论 rollout。
- [ ] Mac 产出的本地临时文件必须保持 git 外；提交前检查 `git status --short`。

## Gate-driven 总时间线

### Gate A: repo foundation + environment lock

- [x] 加入 `pyproject.toml`、`uv.lock`、`src/`、`tests/`、CI、LICENSE；证据：`docs/gate_a_foundation.md`、`refine-logs/EXPERIMENT_TRACKER.md` R008。
- [x] 锁定 Python、MuJoCo、项目内 MJLab/classic MuJoCo first backend reference、29DoF reference MJCF、controller wrapper 和完整 MJLab G1 headless simulation smoke；JAX/JAXLIB 仅作为 deferred Playground extra。公司 G1 edu 23DoF 官方 source 已锁定，但 project-local MJLab wrapper/controller smoke 仍 pending；官方 29DoF ONNX candidate 不能假装适配 23DoF。
- [x] 清理 public repo：`.aris/meta/`、`.aris/traces/`、raw agent prompt/response 不进 git；证据：`.gitignore`、`git ls-files .aris` 为空。
- [x] 机器 profile 保持匿名化；hostname、用户名、绝对路径、私有 SSH/IP/ARIS path 写入 private ops；证据：`docs/a800_machine_profile.md`、`docs/rtx5090_machine_profile.md`。
- [x] 配置 artifact retention policy；磁盘 microbenchmark 成为正式前置 gate；证据：`configs/artifact_retention.toml`、R004 M0 synthetic-only rerun summary。

### Gate B: schema + leakage boundary + EDP

- [x] 实现 `PolicyObservation`、`RuntimeEvent`、`OracleAnnotation` 三套隔离类型；证据：`src/humanoid_locomotion_runtime/schemas.py`、R009。
- [x] 加测试保证 policy serializer 永远不能访问 oracle fields；证据：`tests/test_gate_b_schemas.py`。
- [x] 实现 Episode Data Package writer 和 validator；证据：`src/humanoid_locomotion_runtime/edp.py`、`tests/test_gate_b_edp.py`。
- [x] 明确 raw logs、replay、sensor artifacts 的 retention 分层策略；证据：`configs/artifact_retention.toml`。
- [x] 实现 Mac-safe controlled grounding、temporary object memory、NavigatorV0、dashboard publisher 和 analysis helpers；证据：`src/humanoid_locomotion_runtime/grounding_memory.py`、`src/humanoid_locomotion_runtime/navigator.py`、`src/humanoid_locomotion_runtime/dashboard.py`、`src/humanoid_locomotion_runtime/analysis.py` 及对应测试。

### Gate C: option/SMDP + snapshot/restore

- [x] Gate C 启动前的 robot-profile contract gate 已完成：R007b/R007c/R007d/R007e/R009a 已完成；2026-06-29 已产出 native 23DoF full-training candidate，但 play 回放、project-local controller smoke、controller-native baseline、PPO 和 failure pilots 仍等待验收通过。
- [x] 2026-06-30 完成 R007f policy-improvement scaffold：`ForwardFlat`、`VelocityBalancedFlat` 和 command-grid eval 进入 tracked TODO；证据：`refine-logs/G1_23DOF_CONTROLLER_POLICY_IMPROVEMENT_TODO_20260630.md`、scoped ruff/pytest、ignored 2 env / 2 step eval smoke JSON。
- [x] 2026-06-30 03:49 UTC 已按保守并发启动 R007g：3 张 GPU，每张 1 个 `Unitree-G1-23Dof-ForwardFlat` 训练任务；证据：`refine-logs/G1_23DOF_CONTROLLER_STAGE_A_HANDOFF_20260630.md`。
- [x] 2026-06-30 04:00 UTC 已完成 R007i 中途 sanity eval：对 Stage A seeds `101/102/103` 的 `model_250.pt` 跑 command-grid，结果写入 ignored `runs/unitree_g1_23dof_eval/`；结论是 eval 管线可用，但该早期 checkpoint lateral drift 很大，不是 mature controller evidence。
- [x] 2026-06-30 04:11 UTC 修复并发 eval output filename collision，并重跑 Stage A `model_500.pt` 三 seed command-grid eval；趋势较 `model_250.pt` 改善，但 forward fast max lateral drift 仍约 `6.724m-8.004m`，不通过 mature controller gate。
- [x] 2026-06-30 04:18 UTC 完成 Stage A `model_1000.pt` 三 seed command-grid eval；forward fast max lateral drift 降到约 `4.890m-5.745m`，但 straight drift 仍偏大且 lateral commands 仍不稳，不通过 mature controller gate。
- [x] 2026-06-30 04:31 UTC 完成 Stage A `model_1250.pt` 和 `model_1500.pt` 三 seed command-grid eval；forward fast 不摔且前进距离约 `9m`，但 lateral drift 和 lateral commands 仍未过 gate。
- [x] 2026-06-30 04:35 UTC 新增 eval summary script：`scripts/summarize_unitree_g1_23dof_eval.py`，用于汇总 checkpoint/seed 指标和 triage penalty。
- [x] 2026-06-30 04:40 UTC 完成 Stage A `model_2000.pt` 三 seed command-grid eval；这是当前最佳中途点，但 seed `101/102` forward fast max lateral drift 仍约 `5.241m/5.570m`，不通过 mature controller gate。
- [x] 2026-06-30 04:51 UTC 完成 Stage A `model_2500.pt` 三 seed command-grid eval；这是当前最佳跨 seed 中途点，forward fast max abs lateral across seeds 约 `5.037m`，但 lateral commands 仍不稳，不通过 mature controller gate。
- [x] 2026-06-30 05:02 UTC 完成 Stage A `model_3000.pt` 三 seed command-grid eval；forward fast `done_fraction=0.0`、mean forward displacement 约 `9.287m`，但 max abs lateral across seeds 约 `5.148m`，聚合略弱于 `model_2500.pt`，不通过 mature controller gate。
- [x] 2026-06-30 05:16 UTC 完成 Stage A `model_3500.pt` 三 seed command-grid eval；forward fast mean abs lateral 降到约 `0.703m`，但 max abs lateral across seeds 约 `5.372m`，seed `103` lateral-right max lateral 约 `13.128m`，不通过 mature controller gate。
- [x] 2026-06-30 05:25 UTC 完成 Stage A `model_4000.pt` 三 seed command-grid eval；当前 fixed-forward 指标最好，forward fast mean abs lateral 约 `0.457m`、max abs lateral across seeds 约 `4.641m`，但 lateral/yaw commands 仍不稳，不通过 mature controller gate。
- [x] 2026-06-30 05:20 UTC 基于 `model_3500.pt` 仍有侧向串扰，repo-local profiles 新增 `command_axis_leakage_penalty` reward term；该改动服务后续新 run，不改变当前正在运行的 Stage A jobs。
- [x] 2026-06-30 05:22 UTC 用 `robot` env 跑 2 env / 2 step command-grid smoke，确认 `command_axis_leakage` 进入 RewardManager，actor obs/action contract 仍为 `80 -> 23`。
- [x] 2026-06-30 05:37 UTC 完成 Stage A `model_4500.pt` 三 seed command-grid eval；forward fast mean abs lateral 约 `0.517m`、max abs lateral across seeds 约 `4.688m`，略弱于 `model_4000.pt`，不通过 mature controller gate。
- [x] 2026-06-30 05:38 UTC 新增 binned velocity command sampler：Stage A 覆盖 stand/straight 速度段，Stage B 覆盖 stand/straight/yaw-only/lateral-only/combined。
- [x] 2026-06-30 05:48 UTC 完成 binned sampler 真实 env smoke：`robot` env / 32 env 下 CommandManager 使用 `BinnedVelocityCommand`，resample 后出现 forward 与 lateral/yaw commands，actor/action contract 仍为 `80 -> 23`。
- [x] 2026-06-30 05:55 UTC 完成 Stage A `model_5000.pt` 三 seed command-grid eval；当前 fixed-forward 指标最好，forward fast mean abs lateral 约 `0.290m`、max abs lateral across seeds 约 `4.417m`，但 lateral/yaw commands 仍不稳，不通过 mature controller gate。
- [x] 2026-06-30 06:19 UTC 完成 Stage A `model_6000.pt` 三 seed command-grid eval；fixed-forward 明显退化，forward fast mean abs lateral 约 `1.068m`、max abs lateral across seeds 约 `5.352m`，不通过 mature controller gate。
- [x] 2026-06-30 06:22 UTC 完成 Stage A `model_6500.pt` 三 seed command-grid eval；有恢复但仍弱于 `model_5000.pt`，forward fast mean abs lateral 约 `0.521m`、max abs lateral across seeds 约 `4.915m`，不通过 mature controller gate。
- [x] 2026-06-30 07:21-07:33 UTC 完成 Stage A `model_7000/8000/8500/9000/9500.pt` 三 seed command-grid eval；`model_8500/9500.pt` 接近但仍弱于 `model_5000.pt`，lateral/yaw commands 仍不稳，不通过 mature controller gate。
- [x] 2026-06-30 07:44 UTC 完成 Stage A `model_10000.pt` 三 seed final eval；最终轮弱于 `model_5000.pt`，forward fast mean abs lateral 约 `0.493m`、selection penalty mean 约 `4.990`，不通过 mature controller gate。
- [x] 2026-06-30 07:46 UTC 确认 Stage A seeds `101/102/103` 均完成到 `Learning iteration 10000/10001`，并输出 `model_10000.pt` 和 `policy.onnx`。
- [x] 2026-06-30 08:30 UTC 确认 Stage A seeds `101/102/103` 的最终 `policy.onnx` 均为 `obs [1,80] -> actions [1,23]`；shape/deploy contract 未漂移，但行为 gate 仍未过。
- [x] 2026-06-30 08:33 UTC 已按保守并发启动 R007h：Stage B `Unitree-G1-23Dof-VelocityBalancedFlat` seeds `201/202/203` on GPU `1/2/3`；08:34 UTC 初始 health check 到 learning iteration `6/10001`，当前 decision 为 `CONTINUE`。
- [x] 2026-06-30 08:40 UTC Stage B 三 seed 到 iteration `249/10001`，无 OOM/NaN；mean reward 约 `4.22-5.38`，fell_over 约 `0.46-0.75`，training-check decision 为 `CONTINUE`。
- [x] 2026-06-30 08:43 UTC 启动 Stage B post-training eval queue `g1vb_eval_after_train_20260630T084308Z`；它会等待最终 checkpoint 和训练 tmux 结束后再用 GPU `1/2/3` 分批评估，避免额外抢 GPU。
- [x] 2026-06-30 08:47 UTC Stage B 三 seed 到 iteration `549/10001`，无 OOM/NaN；mean reward 约 `33.49-38.25`，fell_over 约 `0.00-0.04`，`model_500.pt` 已写出，training-check decision 为 `CONTINUE`。
- [x] 2026-06-30 08:55 UTC 按用户资源利用建议停止旧 GPU `1/2/3` Stage B early runs 和旧 eval watcher；旧 runs 最后约 iteration `783/10001`，不计入 mature evidence。
- [x] 2026-06-30 08:55 UTC 在 GPU `5` 单卡重启 Stage B seeds `201/202/203`，tmux `g1vb_pack_s201/s202/s203_20260630T085517Z`；08:56 UTC 确认三任务进入 iteration `3/10001`，GPU 5 约 `7550 MiB / 100%`，无 OOM。
- [x] 2026-06-30 08:56 UTC 启动 packed post-training eval queue `g1vb_pack_eval_after_train_20260630T085653Z`，等待最终 checkpoint 和训练 tmux 结束后使用 GPU list `5 5 5` 分批评估。
- [x] 2026-06-30 04:54 UTC `scripts/summarize_unitree_g1_23dof_eval.py` 增加 `--group-by checkpoint`，支持 multi-seed 聚合排序。
- [ ] 完成 R007h multi-seed controller training 和 R007i 后续 command-grid eval；R007h 已启动但未完成，R007g Stage A training 已完成但未过 mature gate，最多 3 张空闲 GPU，默认 1 个 4096-env 训练任务/GPU，确认不 OOM 后才允许单 GPU 最多 3 个训练任务。
- [ ] 完成 R007j project-local 23DoF controller smoke 后，才能把 mature controller evidence 写入 Gate C。
- [x] 为每个 recovery action 定义 option contract：什么时候能开始、什么时候禁止、怎么执行、持续多久、怎样算成功/失败/结束、能否打断、能重试几次、冷却多久；证据：`src/humanoid_locomotion_runtime/recovery_options.py`、`tests/test_recovery_options.py`。
- [x] 明确 decision epoch：failure trigger、active option termination、option timeout、重大 task event；证据：`DecisionEpoch`、`tests/test_snapshot_branching.py`。
- [ ] 实现 simulator/runtime snapshot 和 restore。
- [x] 为 matched branches 建立 common random numbers contract；证据：`CommonRandomStream`、`FakeDeterministicSnapshotProvider.branch()`。真实 simulator RNG capture 仍属 R018 TODO。
- [x] EDP/recovery record 和 R018a contract 增加 `base_snapshot_id`、`branch_id`、`decision_id`、`policy_training_seed`、`scenario_seed`、`exogenous_noise_seed`、`observation_hash`、`memory_hash`、`action`、`option_outcome`；证据：`src/humanoid_locomotion_runtime/schemas.py`、`src/humanoid_locomotion_runtime/snapshot_branching.py`、`tests/test_snapshot_branching.py`。这不表示 snapshot restore 已通过。

### Gate D: failure protocol calibration and freeze

- [x] 将 failure taxonomy 重构为 cause x temporal profile。也就是把“失败原因”和“失败持续方式”分开；证据：`configs/failure_protocol.v0.toml`、`docs/failure_protocol_v0.md`。
- [x] 把 `user_interrupt` 从 failure family 改为 task-control event；证据：`configs/failure_protocol.v0.toml`。
- [x] 至少构造一个 state-aliasing positive benchmark cell；证据：`tracking_vs_localization_same_current_observation_v0`。
- [x] 冻结 seed split、severity knobs、negative-control role 和 primary endpoint；证据：`configs/seed_splits.v0.toml`、`configs/failure_protocol.v0.toml`。

### Gate E: core baselines

- [ ] `controller_native`
- [ ] `safety_only_monitor`
- [ ] `tuned_rule`
- [ ] `instant_mlp`
- [ ] `frame_stack_raw_history`
- [ ] `GRU_raw_history`
- [ ] `causal_transformer_raw_history`，或在 R025 summary 写明 deferred reason
- [ ] `typed_event_body_memory`
- [ ] `memory_mask / shuffled / stale`
- [ ] `branch_oracle`
- [ ] 每个 learned variant 共享 action set、reward、训练数据、调参预算、controller/planner 和 training seeds。

### Gate F: memory intervention pilot

- [ ] 分开报告模型/训练效应：不同 policy 之间的差异。
- [ ] 分开报告 decision-time memory-content effect：同一 policy 输入 correct/null/shuffled/stale memory 的差异。
- [ ] typed-memory policy 训练时加入 memory dropout 或 `memory_available` mask。
- [ ] 同时报告 policy-only outcome、full-stack-with-fallback outcome、fallback invocation rate、safety override rate。

### Gate G: final evaluation + evidence package

- [ ] 至少 5 个独立 policy training seeds，或写明更小样本只用于 pilot。
- [ ] 足量 paired base snapshots；同时建模 training-seed 与 scenario-seed 变异。
- [ ] 使用 hierarchical / cluster bootstrap。
- [ ] negative-control 使用 equivalence / TOST 风格证据，不把“不显著”写成“无效果”。
- [ ] 所有 main table / figure 可从 artifacts 复现。
- [ ] 逐篇核验 citation 的 title、authors、venue、abstract、BibTeX。

## 每日固定节奏

### 09:00-10:00 次日验收检查

- [ ] 阅读昨晚 ARIS summary。
- [ ] 检查失败 jobs、OOM、stale screen、磁盘占用、episode artifact 完整性。
- [ ] 决定当天是继续扩量、修 bug、还是停止当前分支。
- [ ] 只提交代码/config/summary，不提交 raw runs、logs、checkpoints、weights。

### 10:00-12:30 白天构建块 A

- [ ] 做需要人判断的代码/协议/配置。
- [ ] 更新 tracker 的 `Status` 和 `Notes`。
- [ ] 对任何会影响论文 claim 的变更写清楚 reason。

### 14:00-18:30 白天构建块 B

- [ ] 补测试、跑小规模本地/A800 smoke。
- [ ] 产出 night handoff：要跑哪些 run id、输入 config、成功标准、失败处理。
- [ ] commit/push 后再让 ARIS 夜间接管。

### 21:00-08:00 夜间 ARIS 任务

- [ ] ARIS 只跑 tracker 中明确标为 Night 的 run。
- [ ] 自动记录 queue state、logs、metrics、artifact paths。
- [ ] 结束后写 morning summary，不直接修改论文 claim。

## 第 1 周：单机实验地基与协议冻结

### 第 1 天：打通 A800 单机环境和 ARIS handoff

目标：先确认 A800 上的仓库、环境、日志路径和 handoff 都可用。这个阶段不是跑研究实验，而是防止后面把环境问题误判成方法问题。

**白天人工**

- [x] 记录公共安全机器档案：`docs/a800_machine_profile.md` 和 `docs/rtx5090_machine_profile.md`。
- [x] 确认 A800 canonical repo path、当前分支、Python、conda/uv、GPU 可见性；证据见 `docs/a800_machine_profile.md`。
- [x] 在 A800 上 pull 到当前 branch，并保持 `git status` 干净。
- [x] 将 `.agents/` 和 `.aris/installed-skills-codex.txt` 改为本机资源，不进 git；规则见 `AGENTS.md` 和 `.gitignore`。
- [x] 在 A800 本机用 `--no-doc` 重新初始化 ARIS Codex skills；本机 manifest 被 `.gitignore` 忽略。
- [x] 确认 `.gitignore` 覆盖 `runs/`、`logs/`、`artifacts/`、`checkpoints/`、`weights/`、`datasets/` 和 ARIS 本机资源。
- [x] 更新 `refine-logs/EXPERIMENT_TRACKER.md` 中 R000 状态为 `DONE`。
- [x] 完成 Gate A repo foundation + environment lock；证据：`docs/gate_a_foundation.md`、`pyproject.toml`、`uv.lock`、`configs/environment.lock.toml`、`configs/artifact_retention.toml`、`src/`、`tests/`、`.github/workflows/ci.yml`、`LICENSE`。
- [ ] 在私有/安全位置记录 A800 公司网络访问方式；不要把 SSH、IP、token、jump-host 细节写进 repo。
- [x] 为 R001/R002/R005 补齐 night handoff 的输入路径、成功标准、失败处理和输出 summary 路径；证据：`refine-logs/MORNING_ACCEPTANCE_RERUN_20260626.md`。
- [ ] 白天结束前 commit/push tracker、timeline、plan、handoff 相关文档。

**晚上 ARIS**

- [x] R001: repo sync dry-run；证据：`refine-logs/MORNING_ACCEPTANCE_RERUN_20260626.md`。
- [x] R002: environment smoke；primary smoke 检查 Python/MuJoCo/MJLab-classic import/GPU，不把 JAX 作为前置条件；证据：`refine-logs/MORNING_ACCEPTANCE_RERUN_20260626.md`。
- [x] R003: artifact write smoke；证据：`write_sample_episode_data_package()`、`tests/test_gate_b_edp.py`，本次由白天 tmp-path 单元测试完成，不提交 generated outputs。
- [x] R005: nightly handoff dry-run；证据：`refine-logs/MORNING_ACCEPTANCE_RERUN_20260626.md`。

**次日验收**

- [ ] A800 上 `git status` 干净。
- [ ] ARIS summary 能写回指定 summary 文件。
- [ ] 若 env 不通，Day 2 不进入代码实验，先修 A800。

### 第 2 天：Schema-first scaffolding 与 throughput 估算

目标：先把数据格式、EDP 和最小写入能力固定下来，再估算每个 episode 会消耗多少磁盘。

**白天人工**

- [x] 实现核心 schema：command/status/failure/recovery/memory/episode metadata；证据：`src/humanoid_locomotion_runtime/schemas.py`、`docs/gate_b_schema_edp.md`。
- [x] 写最小 serialization test；证据：`tests/test_gate_b_schemas.py`。
- [x] 明确 Episode Data Package 的最小字段和目录结构；证据：`src/humanoid_locomotion_runtime/edp.py`、`docs/gate_b_schema_edp.md`。
- [ ] 设计 synthetic rollout loop，用于估算 steps/sec 和 MB/episode。

**晚上 ARIS**

- [x] R004: throughput microbenchmark；证据：`refine-logs/MORNING_ACCEPTANCE_RERUN_20260626.md`。本次按用户授权 100GB disk override 只验证 M0 synthetic smoke，不放行真实 batch。
- [x] R003 repeat: sample Episode Data Package skeleton 写入检查；证据：`tests/test_gate_b_edp.py`。
- [ ] 自动生成一份 disk budget estimate。

**次日验收**

- [ ] 估算 100/1k/10k episodes 的磁盘占用。
- [ ] 若单 episode artifact 太大，先调 retention policy。

### 第 3 天：Event logger 与 run manifest

目标：让每次 run 有稳定编号、事件日志、manifest 和 morning summary。没有这些，后面的失败无法复盘。

**白天人工**

- [x] 实现 event logger / run manifest skeleton；证据：`RuntimeEventLogger`、`EpisodeManifest`、`EpisodeDataPackageWriter`。
- [x] 固定 run id 命名：日期、run group、variant、seed；证据：`format_run_id()`、`tests/test_analysis.py`。
- [ ] 定义夜间 ARIS summary 模板：status、failed jobs、metrics、artifact paths、gate decision。
- [x] 写 schema roundtrip tests；证据：`tests/test_gate_b_schemas.py::test_policy_observation_round_trips_as_structured_schema`。

**晚上 ARIS**

- [ ] 跑 20-50 个 synthetic episodes，生成 EDP。
- [ ] 跑 artifact validator。
- [ ] 生成 summary：缺字段、坏 JSON、磁盘占用。

**次日验收**

- [ ] EDP validator 通过率 100%。
- [ ] 若 validator 不稳定，不进入 MuJoCo。

### 第 4 天：MuJoCo / G1 backend smoke

目标：先把公司 G1 edu 23DoF 和 MJLab 29DoF reference 的边界锁住，再验证目标 profile 或 fallback backend 的最小站立、速度跟踪和安全停止，不做 failure protocol。

**白天人工**

- [x] 定位并锁定 G1 model/backend reference：项目内 `third_party/mjlab`、`Mjlab-Velocity-Flat-Unitree-G1`、G1 MJCF 和 `VelocityOnPolicyRunner`；证据：`configs/environment.lock.toml`、`docs/mjlab_backend_lock.md`。
- [x] 定位并下载项目内 G1 controller artifact candidate：官方 Unitree RL MJLab G1 velocity ONNX，存放于 ignored `checkpoints/unitree_rl_mjlab_g1_velocity_v0/`；证据：`docs/controller_checkpoint_selection.md`、`scripts/fetch_unitree_g1_velocity_checkpoint.sh`。
- [x] 解决完整 MJLab dependency environment，并确认当前 runtime repo 能 import 选定 MJLab G1 task；证据：`scripts/mjlab_sync_and_smoke.sh` 使用 Python 3.12.13、`third_party/mjlab/uv.lock`、`torch==2.9.0+cu128`、`mujoco-warp==3.9.0.1`。
- [x] 完成完整 MJLab G1 headless simulation smoke：`Mjlab-Velocity-Flat-Unitree-G1` 在 `cuda:0` reset + 16 zero-action steps，actor obs `[1,99]`、critic obs `[1,111]`、action `[1,29]`，reward finite，无 termination/timeout；证据：`scripts/mjlab_g1_smoke.py`。
- [x] 定位公司 G1 edu 23DoF 官方 source：`g1_23dof_rev_1_0.urdf/xml`；证据：`docs/g1_edu_23dof_source_lock.md`。
- [x] 实现 23DoF source fetch/verify script：R007b；证据：`scripts/fetch_unitree_g1_23dof_description.sh`、`tests/test_fetch_unitree_g1_23dof_description.py`、`.gitignore` 中 `robot_descriptions/`。
- [x] 为 MJLab smoke 增加 profile/dim gate：R007c；证据：`scripts/mjlab_g1_smoke.py`、`tests/test_mjlab_g1_smoke.py`。
- [x] 为 EDP manifest 增加 robot profile metadata：R009a；证据：`src/humanoid_locomotion_runtime/schemas.py`、`src/humanoid_locomotion_runtime/edp.py`、`tests/test_gate_b_schemas.py`、`tests/test_gate_b_edp.py`。
- [x] 完成 23DoF raw asset compile smoke：R007d；证据：`docs/g1_edu_23dof_compile_smoke.md`，MuJoCo 3.10.0 compile PASS，`nq=30`、`nv=29`、`nu=23`、`njnt=24`、`nmesh=27`。
- [x] 完成 23DoF MJLab wrapper/controller selection：R007e；证据：`docs/g1_edu_23dof_controller_route.md`，action dim `23`、MJLab flat actor obs `81`、deploy-style obs `80`，route `train_23dof_required`。
- [x] 完成 23DoF native full-training candidate：`a800_g1_23dof_4096env_10001iter_20260629T100128Z`；证据：`refine-logs/G1_23DOF_CONTROLLER_TRAINING_ACCEPTANCE_20260630.md`。这只表示 candidate 训练完成，不表示 controller smoke 通过。
- [x] 新增 23DoF controller policy-improvement TODO 和 repo-local task profiles；证据：`refine-logs/G1_23DOF_CONTROLLER_POLICY_IMPROVEMENT_TODO_20260630.md`、`src/humanoid_locomotion_runtime/unitree_g1_23dof_profiles.py`。
- [x] 新增 command-grid eval 脚本，用于旧/new checkpoints 的直行、停止、转向、侧移量化筛选；证据：`scripts/eval_unitree_g1_23dof_command_grid.py`。
- [ ] 实现最小 `stand_ready` / `safe_stop` / `track_velocity` smoke command。
- [ ] 明确如果 G1 不通，MJLab/mujocolab-compatible classic MuJoCo fallback 的入口和接口差异。

**晚上 ARIS**

- [ ] R007g: 在最多 3 张空闲 GPU 上跑 `Unitree-G1-23Dof-ForwardFlat` multi-seed。
- [x] R007h: 在最多 3 张空闲 GPU 上启动 `Unitree-G1-23Dof-VelocityBalancedFlat` multi-seed。
- [x] R007h: 根据显存占用把 Stage B multi-seed 从 GPU `1/2/3` 打包迁移为 GPU `5` 单卡三任务。
- [x] R007i: 为 Stage B 设置 post-training eval queue，等待训练完成后自动跑关键 checkpoint command-grid eval。
- [ ] R007h: 完成 `Unitree-G1-23Dof-VelocityBalancedFlat` multi-seed 并输出 checkpoints / `policy.onnx`。
- [ ] R007i: 对旧 candidate 和新 checkpoints 跑 command-grid eval，记录 lateral drift、yaw error、velocity error、done fraction；Stage A `model_250.pt` 到 `model_10000.pt` 已完成但不合格，当前 best 是 `model_5000.pt`；后续仍需 Stage B candidate eval。
- [ ] R007j: selected candidate 通过 eval 后，再运行 `stand_ready` / `safe_stop` / `track_velocity` smoke。

**次日验收**

- [ ] 如果目标是公司 G1 edu 23DoF，必须有 23DoF profile smoke；如果只跑 29DoF reference，验收中必须明确标注 reference-only。
- [ ] Morning Acceptance 必须列出每个 controller run 的 GPU、seed、task、run name、artifact path、OOM/失败情况和 gate decision。
- [ ] 若固定直行仍明显斜走，停在 R007g/R007i 修 command distribution / reward，不进入 failure protocol。
- [ ] 若不通，白天只修 backend，不做 failure protocol。

### 第 5 天：Controller-native baseline skeleton

目标：先跑不带 recovery 学习的 controller-native baseline，确认无故障场景本身足够稳定。

**白天人工**

- [ ] 实现 `controller_native` run path。
- [ ] 定义 basic local target approach 的 success/failure 判据。
- [ ] 确认 MuJoCo privileged signals 只进入 evaluation，不进入 runtime decision。

**晚上 ARIS**

- [ ] 跑 20 个 controller-native no-failure episodes。
- [ ] 记录 task success、fall/unstable、episode validity。

**次日验收**

- [ ] 无 failure 场景成功率应足够高，否则 runtime 地基未稳。
- [ ] 若 no-failure 都不稳，暂停 recovery 研究，修 controller/backend。

### 第 6 天：Failure protocol 预注册草案

目标：在训练任何 memory policy 之前，先写清楚会制造哪些失败、怎么触发、怎么判定成功失败，避免事后挑场景。

**白天人工**

- [ ] 将 failure taxonomy 写成 cause x temporal profile，而不是混合分类：
  - cause：path blockage、localization degradation、tracking degradation、balance disturbance、target/task event。
  - temporal profile：transient、persistent、recurrent、cumulative、progressive、impulse、change/loss/interruption。
- [ ] 把 `user_interrupt` 明确写成 task-control event，不作为 failure family。
- [ ] 为预注册 cells 定义 trigger、severity、success/failure、预期 memory effect 和 negative-control 角色。
- [ ] 至少设计一个 state-aliasing positive cell：当前 observation 相近，但历史不同导致 oracle 最优动作不同。
- [ ] 冻结初版 seed split 草案。

**晚上 ARIS**

- [ ] 不扩量训练，只跑每类 5-10 个 feasibility episodes。
- [ ] 自动输出 trigger timing 和 controller-native success 粗分布。

**次日验收**

- [ ] 若某 family 无法稳定触发，Day 7 先改 protocol。
- [ ] 不允许根据 memory 结果改 family 定义，因为此时还不应训练 memory policy。

### 第 7 天：Protocol freeze gate

目标：冻结 failure cells、seed split 和 severity 选择规则。没冻结前，不启动 baseline ladder。

**白天人工**

- [ ] 审核 Day 6 feasibility。
- [x] 冻结 cause x temporal-profile cells、seed split、severity 选择规则；证据：`configs/failure_protocol.v0.toml`、`configs/seed_splits.v0.toml`。
- [x] 写入 protocol doc/config；标明 negative-control family；证据：`docs/failure_protocol_v0.md`。
- [x] 更新 tracker R010-R016/R018a/R019 状态；R011-R015/R017 仍 TODO，未跑 pilots。

**晚上 ARIS**

- [ ] R011-R014: 每类 pilot 20 episodes。
- [ ] R017: Episode Data Package validation。

**次日验收**

- [ ] 每类 valid episode >= 20。
- [ ] controller-native 成功率不应全 0 或全 100。
- [ ] 若不满足，Week 2 不启动 baseline ladder，先重做 severity。

## 第 2 周：Baseline ladder 与 bandit sanity

### 第 8 天：Severity calibration

**白天人工**

- [ ] 查看 Week 1 pilot 分布。
- [ ] 选择每个 family 的主报告 severity band。
- [ ] 记录为什么选择该 band，避免 self-serving benchmark。

**晚上 ARIS**

- [ ] R015: all-family severity calibration。
- [ ] 生成每类 severity x success rate 表。

**次日验收**

- [ ] 至少 3 个 family 有非饱和 severity。
- [ ] negative-control family 仍保持清晰定义。

### 第 9 天：Safety monitor 与 tuned heuristic baseline 设计

**白天人工**

- [ ] 实现或写定 `safety_only_monitor`：只触发 safe_stop / back_off / retry / abort 这类合法高层动作，不训练 memory policy。
- [ ] 实现或写定 `rule_recovery_tuned`。
- [ ] 明确规则输入只能用 runtime 合法 status/failure signals。
- [ ] 做人工 code review：不能读 privileged failure type 或 ground truth pose。
- [ ] 固定 detection 指标：time-to-detect、false positive / false negative、failure detection F1、intervention-required rate。

**晚上 ARIS**

- [ ] R020: controller-native baseline。
- [ ] R028: safety-only / monitor-only baseline pilot。
- [ ] R021: tuned rule baseline pilot。

**次日验收**

- [ ] rule baseline 不能太弱；如果 obvious rule 都没做，重调。
- [ ] safety monitor 如果已经解释全部收益，memory/RL story 必须降级为 protocol/diagnostic。
- [ ] 如果 rule 已经接近 oracle，后续 RL/memory story 高风险。

### 第 10 天：Oracle upper bound 和标签来源

**白天人工**

- [ ] 实现 evaluation-only `oracle_upper_bound`。
- [ ] 写清 oracle 可用哪些 privileged signals。
- [ ] 写清 supervisor 的训练 label/reward 来源，避免信息泄漏。

**晚上 ARIS**

- [ ] R022: branch/evaluation oracle upper bound pilot。
- [ ] 自动计算 oracle gap。

**次日验收**

- [ ] 如果 `oracle - rule` gap 太小，说明任务没有 recovery 学习空间。
- [ ] 若 oracle 使用泄漏路径进入 runtime，立即修。

### 第 11 天：Instant-state bandit sanity

**白天人工**

- [ ] 实现 `instant_state` observation。
- [ ] 实现 bandit sanity trainer 或最小 action selector。
- [ ] 固定 reward：task progress、安全、recovery、latency、repeated failure penalty。

**晚上 ARIS**

- [ ] R023: instant-state bandit sanity。
- [ ] 输出 action distribution 和 per-family success。

**次日验收**

- [ ] 如果 instant-state 学不动，先查 reward/action semantics。
- [ ] 不直接上 PPO。

### 第 12 天：Raw-history 与 typed-memory bandit sanity

**白天人工**

- [ ] 实现或规划 `frame_stack_raw_history` baseline。
- [ ] 实现或规划 `GRU_raw_history` baseline。
- [ ] 实现或明确 deferred `causal_transformer_raw_history` baseline。
- [ ] 实现 event/body memory summary。
- [ ] 明确 memory horizon 初值。
- [ ] 加 memory mask / shuffled / stale memory 的数据管线入口。
- [ ] 确认所有 learned variants 共享合法输入源、action set、reward、训练数据、调参预算、controller/planner 和 training seeds。

**晚上 ARIS**

- [ ] R026: frame-stack raw-history baseline sanity。
- [ ] R027: GRU raw-history baseline sanity。
- [ ] R029: causal transformer raw-history baseline sanity，或记录 deferred reason。
- [ ] R024: typed event/body memory bandit sanity。
- [ ] 初步比较 instant vs raw-history vs typed-memory。

**次日验收**

- [ ] 只看方向性，不写论文结论。
- [ ] 若 typed memory 相对 ordinary history 没有任何信号，先做 feature audit 或 pivot。

### 第 13 天：Baseline gate review

**白天人工**

- [ ] 汇总 R020-R029。
- [ ] 判断是否满足：
  - safety-only monitor 不能单独解释全部收益
  - rule baseline 有效但不封顶
  - oracle gap 存在
  - typed memory 相对 instant、frame-stack、GRU 至少有方向性信号
  - 若未跑 causal transformer raw-history，R025 summary 已写 deferred reason
- [ ] 决定 Week 3 是否进入 snapshot branching；若 snapshot 未完成，只能进入 paired matched-seed diagnostic。

**晚上 ARIS**

- [ ] 补跑失败的 baseline cells。
- [ ] 生成 baseline ladder summary。

**次日验收**

- [ ] 若 gate 不过，停止扩量；写 pivot note。
- [ ] 若 gate 通过，冻结 Week 3 config。

### 第 14 天：第 2 周清理与提交

**白天人工**

- [ ] 清理 config、tests、analysis scripts。
- [ ] commit/push Week 2 可复现代码和 summary。
- [ ] 更新 tracker 状态。

**晚上 ARIS**

- [ ] 只跑 regression smoke，不跑新实验。

**次日验收**

- [ ] 主分支/feature branch 可从干净 clone 重现 baseline smoke。

## 第 3 周：Snapshot branching / memory intervention diagnostic

### 第 15 天：Snapshot branching runner

**白天人工**

- [ ] 实现 decision-point snapshot/restore runner。
- [ ] 固定 common random numbers，保证分支使用相同外部随机流。
- [ ] Snapshot 至少包含 simulator/runtime state、RNG、planner/localization、temporary object memory、body memory、active option、option elapsed、controller recurrent state、failure injector state。
- [x] 先完成 snapshot manifest / branch metadata contract；证据：`src/humanoid_locomotion_runtime/snapshot_branching.py`、`tests/test_snapshot_branching.py`。这不表示 restore runner 已完成。
- [ ] 如果 snapshot branching 未完成，只实现 paired matched-seed runner，并在所有文档中降级为 diagnostic，不写 counterfactual / ATE。

**晚上 ARIS**

- [ ] R018: snapshot/restore 单元测试和 deterministic branch smoke。
- [ ] R030-R033 小规模 branch 或 paired matched-seed diagnostic run。

**次日验收**

- [ ] 每个 branch group 都有相同 base snapshot、decision id、scenario seed、exogenous noise seed。
- [ ] 若只做到 matched group，记录相同 seed、failure config、initial condition，并标记为非因果诊断。

### 第 16 天：Decision logging and flip extraction

**白天人工**

- [ ] 记录每个 supervisor decision：timestamp、decision id、observation hash、memory hash、action、confidence/logit、option state。
- [ ] 将 runtime event 与 evaluation-only oracle annotation 分开存储，避免 policy log 读取 privileged failure family。
- [x] 实现 decision pair matching skeleton；证据：`extract_decision_flips()`、`tests/test_analysis.py`。真实 R034 pilot table 仍等待 EDP artifacts。

**晚上 ARIS**

- [ ] R034 pilot decision-flip extraction。

**次日验收**

- [x] Mac unit fixture 能生成 per-seed decision flip table；证据：`tests/test_analysis.py`。
- [ ] A800/R034 pilot artifacts 生成真实 per-seed decision flip table。
- [ ] 若 action timestamps 对不上，修 logging。

### 第 17 天：Full matched pilot

**白天人工**

- [ ] 审核 Day 16 flip table。
- [ ] 修 replay mismatch。
- [ ] 冻结 first matched held-out subset。

**晚上 ARIS**

- [ ] R030-R033 扩到 first held-out subset。
- [ ] R035 hierarchical/cluster bootstrap 与 negative-control equivalence / TOST 初版。

**次日验收**

- [ ] 看预注册 memory-positive cells 是否有方向性 memory gain。
- [ ] 看 negative-control CI 是否落入预注册等效区间；不把“不显著”写成无效果。

### 第 18 天：Negative-control audit

**白天人工**

- [ ] 专门审查 transient/instant negative-control。
- [ ] 查是否存在 feature leakage 或 severity bias。
- [ ] 审核 rule fallback 是否污染 learned-policy success attribution。

**晚上 ARIS**

- [ ] 补跑 shuffled-memory negative-control。
- [ ] 补跑 correct/null/masked/shuffled/stale memory-content intervention。
- [ ] 生成 false gain report。

**次日验收**

- [ ] 如果 negative-control 也涨，暂停所有 claim，修 protocol/feature。

### 第 19 天：Memory feature audit

**白天人工**

- [ ] 审查 event trace、body trend、language context 是否各自合法。
- [ ] 写 leave-one-out config。
- [ ] 确认 typed-memory policy 训练中包含 memory dropout 或 `memory_available` mask，避免 test-time masking OOD。

**晚上 ARIS**

- [ ] R040-R042 小规模 ablation。

**次日验收**

- [ ] 找到主要有效成分或确认无效成分。

### 第 20 天：Horizon scan

**白天人工**

- [ ] 定义 short/medium/long horizon。
- [ ] 确认 horizon 不改变其他模型容量或训练预算。

**晚上 ARIS**

- [ ] R043 horizon scan。

**次日验收**

- [ ] 若 longer horizon 反而退化，记录 over-history limitation。

### 第 21 天：第 3 周 gate

**白天人工**

- [ ] 汇总 Week 3:
  - branch outcome difference / ATE；若 snapshot 未完成，则只写 paired diagnostic
  - action-value regret against branch oracle
  - decision flip rate 和 flip-conditioned gain
  - negative-control equivalence result
  - policy-only outcome、full-stack-with-fallback outcome、fallback invocation rate、safety override rate
  - CI/effect size
- [ ] 决定是否继续主打 memory-value diagnostic。

**晚上 ARIS**

- [ ] 补跑缺失 cells 或 regression smoke。

**次日验收**

- [ ] Gate 通过：进入 VLM baseline 和图表。
- [ ] Gate 失败：转 protocol/diagnostic negative result，不再扩 PPO。

## 第 4 周：VLM baseline、图表和论文证据

### 第 22 天：VLM-prompt supervisor spec

**白天人工**

- [ ] 写 VLM prompt 输入规范：只读合法状态摘要，不读 privileged ground truth。
- [ ] 定义 invalid action、latency、cost per episode、detection F1 和 false positive rate。
- [ ] 选定要比较的 failure cells。

**晚上 ARIS**

- [ ] R045 小规模 VLM-prompt pilot。

**次日验收**

- [ ] 如果 VLM invalid/action latency 太高，记录为效率劣势。
- [ ] 如果 VLM 明显更强，准备 pivot story。

### 第 23 天：VLM vs learned comparison

**白天人工**

- [ ] 审核 VLM pilot。
- [ ] 固定 fair comparison: same seeds, same summaries, same 8 actions。

**晚上 ARIS**

- [ ] R045/R046 扩量比较。

**次日验收**

- [ ] 判断 learned supervisor 是否仍可作为主线。

### 第 24 天：主表格

**白天人工**

- [ ] 确定 Main Table 1/2/3 的行列和 metrics。
- [ ] 写 analysis script，不手工改数。

**晚上 ARIS**

- [ ] R060 main table generation。
- [ ] 自动输出 csv/md 和 source paths。

**次日验收**

- [ ] 表中所有数字可追溯到 run ids。

### 第 25 天：主图

**白天人工**

- [ ] 确定 Figure 1: per-family success + CI。
- [ ] 确定 Figure 2: memory-value / decision-flip / horizon。

**晚上 ARIS**

- [ ] R061/R062 figure generation。

**次日验收**

- [ ] 图可复现；CI/effect size 正确。

### 第 26 天：Case studies 和 failure review

**白天人工**

- [ ] 选择 case study 原则：不能只挑成功；必须包含 failure/limitation。
- [ ] 审查 replay artifacts。

**晚上 ARIS**

- [ ] R063 candidate case extraction。
- [ ] 生成 replay index。

**次日验收**

- [ ] 每个 case 对应一个论文论点或 limitation。

### 第 27 天：Evidence package audit

**白天人工**

- [ ] 审核所有 claims 是否都有证据。
- [ ] 删掉没有证据支撑的 claim。
- [ ] 写 limitation checklist。

**晚上 ARIS**

- [ ] R070 paper evidence package audit。
- [ ] 检查 artifact completeness、missing seeds、failed jobs。

**次日验收**

- [ ] 若缺关键 evidence，Day 28 只补关键 runs，不加新想法。

### 第 28 天：最终决策与 handoff

**白天人工**

- [ ] 做 go/pivot/stop 决策。
- [ ] 若 go：进入 paper writing。
- [ ] 若 pivot：重写 title/contributions。
- [ ] 若 stop：保留 protocol/negative result，总结为什么。

**晚上 ARIS**

- [ ] 只做 final summary，不再启动新实验。

**次日验收**

- [ ] 产生可交给 paper-writing 的 evidence handoff。

## 每晚交给 ARIS 的 Handoff 模板

填写一份新的 nightly handoff 时，复制本节并逐项打勾；没有冻结输入、成功标准和停止条件时，不启动夜间任务。

**基本信息**

- [ ] 日期：
- [ ] 主机：A800_SINGLE_HOST
- [ ] 分支：
- [ ] 提交：

**本晚要启动的 runs**

- [ ] Run IDs：
- [ ] 配置文件：
- [ ] 预期输出：

**成功标准**

- [ ] 写清每个 run 的 pass/fail 判据。

**停止条件**

- [ ] 写清 OOM、磁盘不足、stale job、env/import failure、artifact schema failure 等停止条件。

**禁止事项**

- [ ] 不修改论文 claim。
- [ ] 不把 privileged MuJoCo truth 当作 runtime input。
- [ ] 不提交 raw logs、checkpoints、weights 或 generated replay dumps。

**次日必须产出的 summary**

- [ ] completed / failed / stuck jobs
- [ ] metrics table
- [ ] artifact paths
- [ ] disk usage
- [ ] gate recommendation

## 每日 Commit 规则

- [ ] 白天结束前 commit/push code, config, docs, trackers。
- [ ] 夜间 ARIS 不直接提交 raw outputs。
- [ ] 次日早上只提交 curated summaries、small analysis tables、config fixes。
- [ ] 每个 gate 通过或失败都要在 tracker notes 中记录。

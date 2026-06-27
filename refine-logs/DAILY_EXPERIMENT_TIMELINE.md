# 每日实验时间线

**日期**: 2026-06-25
**主机策略**: A800 单机主线。5090 只作为备用，不主动分裂实验环境。

读法：这份时间线是“每天怎么推进”的执行说明，不是必须照天数硬跑的日历。真正的顺序由 gate 决定：当前 gate 没过，就停下来修当前问题，不进入下一阶段。

**工作节奏**: 白天由人完成设计、实现、审查和 gate 决策；晚上交给 ARIS 做已经定义清楚的 smoke / queue / monitor / summarize。

**核心规则**: 每个晚上只能跑白天已经冻结输入、验收标准和回滚条件的任务。没有白天 handoff，就不跑夜间自动实验。

**待办规则**: 可执行事项使用 `- [ ]` / `- [x]`；完成项必须附带可复查证据路径、run id、commit id 或 tracker 记录。

**审核后修正**: 下面的 28 天安排只是参考节奏。任何 gate 未通过，不进入下一阶段，也不启动 PPO、大规模实验或论文主结论。

**Mac 本机工作入口**: 当前 Mac 只做不会影响 A800 主实验线的工作，详细清单见 `refine-logs/MAC_SAFE_WORKLIST.md`。

- [ ] Mac 白天可做：工具链对齐、纯 Python contract tests、Gate C backend-neutral interface、RuntimeManager typed command skeleton、leakage boundary tests 和 A800 handoff 文档。
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

### Gate C: option/SMDP + snapshot/restore

- [x] Gate C 启动前的 robot-profile contract gate 已完成：R007b/R007c/R007d/R007e/R009a 已完成；但 controller smoke、controller-native baseline、PPO 和 failure pilots 仍等待 native 23DoF controller 或 validated conversion experiment。
- [x] 为每个 recovery action 定义 option contract：什么时候能开始、什么时候禁止、怎么执行、持续多久、怎样算成功/失败/结束、能否打断、能重试几次、冷却多久；证据：`src/humanoid_locomotion_runtime/recovery_options.py`、`tests/test_recovery_options.py`。
- [ ] 明确 decision epoch：failure trigger、active option termination、option timeout、重大 task event。
- [ ] 实现 simulator/runtime snapshot 和 restore。
- [ ] 使用 common random numbers 固定外部随机流。
- [x] EDP/recovery record 和 R018a contract 增加 `base_snapshot_id`、`branch_id`、`decision_id`、`policy_training_seed`、`scenario_seed`、`exogenous_noise_seed`、`observation_hash`、`memory_hash`、`action`、`option_outcome`；证据：`src/humanoid_locomotion_runtime/schemas.py`、`src/humanoid_locomotion_runtime/snapshot_branching.py`、`tests/test_snapshot_branching.py`。这不表示 snapshot restore 已通过。

### Gate D: failure protocol calibration and freeze

- [x] 将 failure taxonomy 重构为 cause x temporal profile。也就是把“失败原因”和“失败持续方式”分开；证据：`configs/failure_protocol.v0.toml`、`docs/failure_protocol_v0.md`。
- [x] 把 `user_interrupt` 从 failure family 改为 task-control event；证据：`configs/failure_protocol.v0.toml`。
- [x] 至少构造一个 state-aliasing positive benchmark cell；证据：`tracking_vs_localization_same_current_observation_v0`。
- [x] 冻结 seed split、severity knobs、negative-control role 和 primary endpoint；证据：`configs/seed_splits.v0.toml`、`configs/failure_protocol.v0.toml`。

### Gate E: core baselines

- [ ] `controller_native`
- [ ] `tuned_rule`
- [ ] `instant_mlp`
- [ ] `frame_stack_raw_history`
- [ ] `GRU_raw_history`
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
- [ ] 若在 Mac 本机工作，优先执行 `refine-logs/MAC_SAFE_WORKLIST.md` 的 M-MAC-001 到 M-MAC-004，不改写 A800 实验证据。
- [ ] 更新 tracker 的 `Status` 和 `Notes`。
- [ ] 对任何会影响论文 claim 的变更写清楚 reason。

### 14:00-18:30 白天构建块 B

- [ ] 补测试、跑小规模本地/A800 smoke。
- [ ] 若 smoke 在 Mac 本机执行，必须标记为 local inspection；只有 A800 或明确实验主机结果才能作为 runtime/controller evidence。
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
- [ ] 固定 run id 命名：日期、run group、variant、seed。
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
- [ ] 实现最小 `stand_ready` / `safe_stop` / `track_velocity` smoke command。
- [ ] 明确如果 G1 不通，MJLab/mujocolab-compatible classic MuJoCo fallback 的入口和接口差异。

**晚上 ARIS**

- [ ] 运行 `stand_ready` smoke。
- [ ] 运行短 `track_velocity` smoke。
- [ ] 记录 crash、unstable、controller command logs。

**次日验收**

- [ ] 如果目标是公司 G1 edu 23DoF，必须有 23DoF profile smoke；如果只跑 29DoF reference，验收中必须明确标注 reference-only。
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

### 第 9 天：Tuned heuristic baseline 设计

**白天人工**

- [ ] 实现或写定 `rule_recovery_tuned`。
- [ ] 明确规则输入只能用 runtime 合法 status/failure signals。
- [ ] 做人工 code review：不能读 privileged failure type 或 ground truth pose。

**晚上 ARIS**

- [ ] R020: controller-native baseline。
- [ ] R021: tuned rule baseline pilot。

**次日验收**

- [ ] rule baseline 不能太弱；如果 obvious rule 都没做，重调。
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
- [ ] 实现 event/body memory summary。
- [ ] 明确 memory horizon 初值。
- [ ] 加 memory mask / shuffled / stale memory 的数据管线入口。
- [ ] 确认所有 learned variants 共享合法输入源、action set、reward、训练数据、调参预算、controller/planner 和 training seeds。

**晚上 ARIS**

- [ ] R026: frame-stack raw-history baseline sanity。
- [ ] R027: GRU raw-history baseline sanity。
- [ ] R024: typed event/body memory bandit sanity。
- [ ] 初步比较 instant vs raw-history vs typed-memory。

**次日验收**

- [ ] 只看方向性，不写论文结论。
- [ ] 若 typed memory 相对 ordinary history 没有任何信号，先做 feature audit 或 pivot。

### 第 13 天：Baseline gate review

**白天人工**

- [ ] 汇总 R020-R027。
- [ ] 判断是否满足：
  - rule baseline 有效但不封顶
  - oracle gap 存在
  - typed memory 相对 instant、frame-stack、GRU 至少有方向性信号
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
- [ ] 实现 decision pair matching。

**晚上 ARIS**

- [ ] R034 pilot decision-flip extraction。

**次日验收**

- [ ] 能生成 per-seed decision flip table。
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
- [ ] 定义 invalid action、latency、cost per episode。
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

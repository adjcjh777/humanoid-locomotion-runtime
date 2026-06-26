# 语言条件 Humanoid Locomotion Runtime 与监督式恢复研究计划

## 0. 项目记录

- **项目名称**：Humanoid Locomotion Runtime
- **初始平台**：MuJoCo + Unitree G1 humanoid model
- **fallback 平台**：如果 G1 controller 路径无法通过早期 smoke gate，则优先切换到 MJLab/mujocolab-compatible classic MuJoCo humanoid locomotion backend。
- **后续兼容目标**：`bxi_elf3` / `bxi_robotics` 和公司自研 humanoid body。它们是 V1/V2 验证目标，不作为 V0 论文证据。
- **主目标**：构建一个可研究、可调试、可复现实验的人形机器人 locomotion runtime，把语言条件任务和受控 open-vocabulary-style grounding 转成可监控、可恢复的 humanoid locomotion skills。
- **核心方法位置**：在冻结的 self-stabilizing locomotion controller 之上，学习低频、高层、typed 的 supervisory recovery selector。
- **明确不声称**：本项目不训练 raw image/language 到 humanoid joint actions 的 foundation-scale end-to-end VLA。
- **明确不声称**：V0 不声称跨机器人本体泛化；backend-replaceable interfaces 是工程约束，不是实验结果。
- **当前论文姿态**：诊断性研究优先。最强主线不是“提出一个新 supervisor”，而是在同一 simulator/runtime decision snapshot 上做 memory intervention，量化 memory 何时、为何改变 recovery decision 并带来收益；snapshot branching 未实现前只能写 paired matched-seed diagnostic，不写 causal counterfactual。

---

## 1. 摘要

### 1.1 问题

成熟的人形机器人 locomotion controller 通常能在受控场景中行走、转向、跟踪速度或目标，但它们大多只是低层运动后端。它们不会自然给出任务层证据，例如：

- 为什么当前执行变得不安全；
- 失败是否可恢复；
- 已尝试哪个 recovery action；
- 语言条件目标在 perception/navigation 失败后是否需要重新 grounding；
- body memory 是否能解释 repeated failure 或慢性退化。

对语言条件 humanoid agent 来说，普通 goal-reaching metric 会掩盖很多关键失败：动态障碍、localization drift、velocity tracking error、balance risk、target loss 等都可能被平均 success rate 淹没。`user_interrupt` 属于 task-control event，不作为 failure family。

### 1.2 方案

围绕成熟 Unitree G1 locomotion controller，在 MuJoCo 中构建 language-conditioned humanoid locomotion runtime。V0 使用：

- controlled detector-like grounding；
- temporary object memory；
- MPC / optimization local planner；
- typed locomotion skills；
- status monitor；
- body/event memory；
- high-level supervisory recovery selector；
- deterministic rule fallback 和 SafetySupervisor；
- Episode Data Package；
- Viser WebUI dashboard。

初版实现保持单 `RuntimeManager`，底层 controller 冻结。RL 只用于低频 supervisory recovery action selection，不输出 joint command，也不替代 self-stabilizing controller。实时 safety 由 `RuntimeManager` 和 `SafetySupervisor` 本地闭环保证；Agent Bus 仅保留为未来高层异步协作、审计和实验分析接口。

### 1.3 V0 成功标准

V0 通过的条件：

1. [ ] runtime 能在 MuJoCo 中用 Unitree G1 或 fallback humanoid backend 执行语言条件 local locomotion task。
2. [ ] benchmark 覆盖 cause × temporal-profile seeded failure cells，并且包含预注册 negative-control。
3. [ ] 实验包含 controller-native、tuned rule、instant MLP、frame-stack raw history、GRU raw history、typed event/body memory、memory mask/shuffled/stale、branch oracle 或 evaluation-only oracle upper bound。
4. [ ] 每个 episode 写出完整 Episode Data Package：manifest、event logs、metrics、timeseries、artifacts。
5. [ ] Viser dashboard 能查看 live/replay episode、grounding、route、status、body memory、recovery decision 和 benchmark metrics。
6. [ ] WebUI 和未来 agent 只能发 high-level typed command，不能绕过 `RuntimeManager` 或 `SafetySupervisor`。
7. [ ] learned recovery 是 low-frequency task-level component；locomotion controller、SafetySupervisor 和 hard stop path 保持 non-learned。

---

## 2. 产品与研究定位

### 2.1 核心定位

本项目不是 “mini HoloAgent”，也不是新的 humanoid foundation model。核心问题是：

> 当成熟 humanoid controller 已经具备自稳 locomotion 时，runtime 如何在保留 typed safety、logging、replay 和 benchmark comparability 的同时，学习任务层恢复决策，并诊断 body/event memory 何时真正有用？

V0 是单本体 evidence project。它使用 Unitree G1 first；若 G1 integration miss smoke gate，则切到 MJLab/mujocolab-compatible classic MuJoCo backend。V0 不声称 learned selector 可以泛化到其他 humanoid body。

humanoid-specific 的部分来自 task progress 与 body dynamics 的耦合：balance margin、contact state、slip、fall risk、velocity/orientation tracking error、controller confidence、recovery latency。与 wheeled navigation 不同，runtime 必须判断 body 是否还能继续、减速、停下、恢复平衡、重新 grounding、重新定位、replan 或 abort。

### 2.2 V0 工作假设

这些是假设，不是最终论文 claim：

1. **supervisory recovery hypothesis**：高层 recovery selector 能在不训练低层 gait/joint control 的情况下，改善 task-level recovery。
2. **body/event memory hypothesis**：带 window summary 和 event/recovery memory 的 selector，在长时序、累积、退化型 failure 中优于 instant state。
3. **benchmark hypothesis**：seeded failure-recovery evaluation 能暴露普通 goal-reaching metrics 看不到的问题。

### 2.3 V1 / V2 可能升级

- parameterized recovery actions；
- residual 或 status-conditioned controller adaptation；
- Unitree G1 到 `bxi_elf3` / 公司 humanoid body 的迁移验证；
- persistent 3D semantic memory 替代 temporary object memory；
- global navigation 和 active exploration；
- multi-agent runtime manager、TaskRouter、auditable Agent Bus；
- 真实 open-vocabulary detector 作为主 perception path；
- sim-to-real 和硬件实验。

---

## 3. 用户、故事与验收标准

### 3.1 用户

1. **research developer**：快速测试 humanoid locomotion recovery idea。
2. **benchmark runner**：跑可复现批量实验和 ablation。
3. **debug operator**：用 dashboard 查看 robot state、target grounding、route、failure、recovery。
4. **future multi-agent orchestrator**：未来把 planner、recovery、evaluator agents 分离，但通过 typed task/event interfaces 协作。

### 3.2 Story 1：执行语言条件 locomotion

用户提交 “walk to the red chair slowly” 这类指令，runtime 应能解析命令、ground target、规划安全局部路径、调用 G1 locomotion skill、监控状态并在失败时恢复。

验收：

- [ ] instruction 转为 structured locomotion command；
- [ ] target grounding 使用 RGB-D 和 detector-like output，不使用 MuJoCo privileged object id；
- [ ] temporary object memory 记录 target evidence 和 safe stop pose；
- [ ] locomotion skill 通过成熟 G1 controller backend 执行；
- [ ] 关键事件写入 Episode Data Package。

### 3.3 Story 2：从 runtime failures 中恢复

benchmark runner 需要系统检测 path blockage、localization drift、velocity tracking error、balance risk、target loss 等 failure，并把 user interruption / target change 作为 task-control event 记录，让高层 recovery selector 选择 typed recovery action。

验收：

- [ ] failure taxonomy 使用 cause × temporal-profile 二维结构；
- [ ] recovery action taxonomy 明确 V0 允许选择的动作，并为每个动作定义 option / SMDP contract；
- [ ] V0 RL action set 限定为：
  - `continue`
  - `slow_down`
  - `safe_stop`
  - `local_replan`
  - `recover_balance`
  - `refresh_target_grounding`
  - `relocalize`
  - `abort_task`
- [ ] rule-based recovery 作为 baseline、fallback、debugging oracle，不作为主贡献；
- [ ] recovery decision 记录 pre-status、post-status、latency、success、fallback；
- [ ] repeated failures 通过 body memory event records 可见。

### 3.4 Story 3：比较 ablations

研究者需要在相同 benchmark 上比较：

- `controller_native`
- `rule_recovery`
- `rl_instant_state`
- `rl_window_memory`
- `rl_full_body_memory`
- `oracle_upper_bound`

验收：

- [ ] 所有方法使用相同 scenario definitions、held-out seeds 和 logging pipeline；
- [ ] metrics 包括 task success、recovery success、collision count、fall/unstable count、stop latency、path efficiency、repeated failure count、human intervention count；
- [ ] batch runner 生成 run-level summary tables；
- [ ] episode-level artifacts 可用于 failure diagnosis；
- [ ] 报告必须包含 per-family breakdown 和 confidence intervals。

### 3.5 Story 4：用 WebUI 调试

debug operator 需要用 Viser dashboard 查看 live/replay scene，理解 episode 为什么失败、recovery 是否正确。

验收：

- [ ] dashboard 显示 robot pose、target pose、safe stop pose、obstacles、route、replan points、blocked regions；
- [ ] dashboard 显示 camera/grounding outputs；
- [ ] dashboard 显示 body memory traces 和 recovery events；
- [ ] dashboard 只能通过 `RuntimeManager` 发 high-level typed UI commands；
- [ ] dashboard 不能直接控制 low-level controller、velocity、joint targets 或 safety override。

### 3.6 V0 非目标

V0 不做：

- end-to-end VLA training；
- persistent 3D semantic memory 的完整系统；
- 多房间 global navigation 和 active exploration；
- real-hardware safety guarantee；
- 新 whole-body controller；
- real-time loop 内的 multi-agent execution；
- runtime decision 使用 MuJoCo object id、privileged target pose 或 simulator semantic label。

---

## 4. 系统架构

### 4.1 高层数据流

```text
Language instruction
  -> LLM / rule-assisted parser
  -> Structured locomotion command
  -> Controlled grounding adapter
  -> Temporary object memory
  -> Safe stop pose generation
  -> NavigatorV0 local planner
  -> Locomotion skill manager
  -> Mature Unitree G1 controller backend
  -> Status monitor
  -> Body/event memory
  -> Supervisory recovery selector
  -> Rule/safety fallback
  -> SafetySupervisor
  -> EventStore + Episode Data Package + Viser dashboard
```

### 4.2 runtime components

```text
RuntimeManager
  -> TaskRouter
  -> EventStore
  -> AgentPort interface
  -> LanguageParser
  -> GroundingAdapter
  -> TemporaryObjectMemory
  -> NavigatorV0
  -> LocomotionSkillManager
  -> StatusMonitor
  -> BodyMemory
  -> SupervisoryRecoverySelector
  -> RuleRecoveryFallback
  -> SafetySupervisor
  -> BenchmarkLogger
  -> ViserDashboardPublisher
```

### 4.3 实时边界与 agent 协作边界

| 层 | 用途 | 机制 |
|---|---|---|
| real-time runtime bus | robot execution、status updates、risk、local recovery、safety | ROS2、Python async queue、gRPC 或 shared runtime state |
| agent coordination bus | high-level async tasks、audit、long-horizon replanning、experiment analysis | TaskRouter、AgentPort、未来 Agent Bus |

规则：

- safety-critical execution 不等待 LLM 或 Agent Bus。
- `SafetySupervisor` 本地同步执行，有权停止或 override unsafe execution。
- agent suggestions 是 typed recommendations，不是最终执行权。
- learned recovery selector 只能选择 typed high-level recovery actions。
- 任何 agent task 必须带 `task_id`、`correlation_id`、`source`、`target_role`、`deadline_ms`、`priority` 和 fallback。

---

## 5. 核心 schema 与接口

### 5.1 关键 schema

首批 schema：

- `LocomotionCommand`
- `LocomotionStatus`
- `MemoryTarget`
- `BodyMemoryState`
- `FailureEvent`
- `RecoveryActionRecord`
- `EpisodeManifest`
- `EpisodeMetrics`

schema-first 是硬约束：先保证序列化、日志、replay 和 benchmark runner 可用，再接入重依赖。

### 5.2 运行时禁止输入

runtime decision 禁止使用：

- MuJoCo object id；
- ground-truth target pose；
- simulator semantic label；
- evaluation-only true failure labels / cause-temporal cells；
- oracle action label。

允许 evaluation 使用：

- MuJoCo object pose；
- contact / fall state；
- privileged failure labels；
- branch oracle / oracle upper bound。

### 5.3 recovery actions

V0 RL-selectable action set：

```text
continue
slow_down
safe_stop
local_replan
recover_balance
refresh_target_grounding
relocalize
abort_task
```

`emergency_stop` 是 `SafetySupervisor` override，不允许 RL 选择。`ask_agent_replan` 保留到未来 high-level agent coordination。`mark_blocked_region` 是 planner/memory side effect，不是 V0 RL action。

这些 recovery actions 不是瞬时动作，必须实现为 options / SMDP contract。每个 action 至少定义 initiation condition、action mask、execution implementation、minimum duration、maximum duration、success condition、failure condition、termination condition、interruptibility、retry budget 和 cooldown。Decision epoch 只发生在 failure trigger、active option termination、option timeout 或重大 task-control event。

---

## 6. Benchmark 与评估设计

### 6.1 外部锚点

V0 使用内部 seeded failure-recovery benchmark，但必须锚定外部系统：

1. **MJLab / mujocolab-compatible classic MuJoCo stack**
   - 作为 V0 首选 fallback humanoid backend 和 controller smoke test 集成路径。

2. **MuJoCo Playground**
   - 作为 deferred optional external reference；只有 MJLab/classic MuJoCo 路径无法支撑必要 evidence 时才显式启用。
   - 参考：<https://playground.mujoco.org/>、<https://arxiv.org/abs/2502.08844>

3. **LocoMuJoCo**
   - 作为 locomotion robustness 和 evaluation protocol 参考。
   - 参考：<https://loco-mujoco.readthedocs.io/en/v0.3.0/>、<https://arxiv.org/abs/2311.02496>

4. **HumanoidBench**
   - 作为 benchmark positioning 和 optional sanity-check tasks 参考。
   - 参考：<https://humanoid-bench.github.io/>、<https://arxiv.org/abs/2403.10506>

### 6.2 V0 failure taxonomy

V0 不再使用一维 failure family 列表，而使用 cause × temporal-profile 二维 taxonomy。实现时至少覆盖：

| Cause | Temporal profile 示例 | 角色 |
| --- | --- | --- |
| path blockage | transient / persistent / recurrent | path × transient 是 negative-control；path × recurrent 是 memory-positive candidate |
| localization degradation | transient / cumulative / persistent | persistent / cumulative 是 memory-positive candidate |
| tracking degradation | transient / cumulative | cumulative 是 memory-positive candidate |
| balance disturbance | impulse / recurrent / progressive | impulse 可作为 near-Markov control |
| target/task event | change / loss / interruption | task-control event；`user_interrupt` 不作为 failure family |

主实验必须预注册少量 cells，例如 path × transient negative-control、path × recurrent、tracking × cumulative、localization × persistent、balance × impulse。至少一个 positive benchmark cell 必须显式制造 state aliasing：当前 observation 相近，但历史不同导致 oracle 最优 recovery action 不同。

### 6.3 seed protocol

- train seeds：按 compute budget 扩大。
- validation seeds：每个 family 固定 seed，用于 tuning 和 early stopping。
- test seeds：held-out fixed seeds，用于最终报告。
- 所有方法必须跑相同 validation/test seeds。
- scenario generator distributions 和 severity ranges 必须在 final test 前提交。
- failed episodes 保留并报告；禁止只挑成功案例。

### 6.4 methods and ablations

1. `controller_native`
   - 外部参考：只通过底层 backend native command interface 执行。
   - 无 typed recovery runtime、无 body memory、无 learned selector。

2. `rule_recovery_tuned`
   - 预注册 deterministic recovery policy。
   - 是 deployable heuristic baseline 和 fallback，不是 debugging oracle。

3. `instant_mlp`
   - 只观察当前 locomotion status 和 instant robot state。

4. `frame_stack_raw_history`
   - 观察同样合法输入源的固定长度 raw history。

5. `GRU_raw_history`
   - 观察同样合法输入源的 recurrent raw history，作为主文必需 ordinary history baseline。

6. `typed_event_body_memory`
   - 观察 instant state、window summaries、event/recovery memory。

7. `memory_mask / shuffled / stale`
   - 对同一个 typed-memory policy 做 decision-time memory-content intervention。
   - typed-memory policy 训练时必须包含 memory dropout 或 `memory_available` mask，避免 test-time masking OOD。

8. `branch_oracle` / `oracle_upper_bound`
   - evaluation-only privileged upper bound；优先来自 snapshot branching 下全部合法 actions 的结果比较。
   - 不是公平 deployable method，不能作为 runtime 方法。

主要比较：

- `controller_native` vs `typed_event_body_memory`：runtime recovery 的价值。
- `rule_recovery_tuned` vs `typed_event_body_memory`：learned supervisory selection 的价值。
- `instant_mlp` vs `typed_event_body_memory`：memory representation 的价值。
- `frame_stack_raw_history` / `GRU_raw_history` vs `typed_event_body_memory`：typed memory 是否优于普通历史模型。
- correct/null/shuffled/stale memory input：decision-time memory-content effect。

### 6.5 RL training protocol

V0 采用 staged path：

1. **bandit sanity check**
   - 把 failure event 看成 one-step recovery-action selection。
   - 在跑长 PPO 前验证 memory observation 是否有信号。

2. **PPO supervisory recovery**
   - 训练低频 discrete recovery selector。
   - 冻结 locomotion controller 负责 gait/balance；PPO 只选择 typed recovery options。
   - 只有 Gate A-E 通过后才启动；如果 bandit / branch pilot 已能回答研究问题，可以继续保持更轻量 selector。

如果 bandit sanity check 显示 typed event/body memory 不优于 instant state、frame-stack raw history 和 GRU raw history，必须暂停 PPO 扩量，先检查 observation design、action taxonomy 和 scenario distributions。

### 6.6 metrics

episode metrics：

- task success rate；
- recovery success rate；
- collision count；
- fall / unstable count；
- stop latency；
- path efficiency；
- repeated failure count；
- human intervention count；
- grounding success rate；
- route validity rate；
- final failure mode。

诊断性论文核心 metrics：

- branched outcome difference / ATE；仅在 snapshot branching 完成后使用；
- action-value regret against branch oracle；
- unsafe-completion difference；
- recovery latency difference；
- decision-flip rate；
- flip-conditioned recovery gain；只作为解释性指标，不单独称为 causal effect；
- hierarchical / cluster bootstrap confidence interval；
- negative-control equivalence / TOST；
- shuffled-memory negative-control gain；
- per-cell effect size。

---

## 7. Episode Data Package

每个 episode 至少包含：

```text
episode_manifest.json
events.jsonl
metrics.json
timeseries/
artifacts/
replay_index.json
```

要求：

- 所有 command、status、failure、recovery record 可序列化/反序列化。
- sample Episode Data Package 可以在不运行 MuJoCo 的情况下生成。
- 如果进入 snapshot branching，EDP 必须记录 `base_snapshot_id`、`branch_id`、`decision_id`、`policy_training_seed`、`scenario_seed`、`exogenous_noise_seed`、`observation_hash`、`memory_hash`、`action` 和 `option_outcome`。
- 大型 raw logs、bags、datasets、checkpoints、weights 不进 git。
- held-out evaluation run 保留足够 artifact 用于 failure diagnosis。

---

## 8. Dashboard

V0 使用 Viser dashboard，目标是 debugging 和 data validation，不是展示型 UI。

必须包含：

- 3D robot pose；
- target / safe stop pose；
- obstacles、route、blocked regions；
- grounding output；
- body memory panel；
- recovery decision panel；
- benchmark summary panel；
- high-level typed UI commands。

禁止：

- dashboard 直接发 low-level controller command；
- dashboard 绕过 `RuntimeManager`；
- dashboard 覆盖 `SafetySupervisor` hard stop。

---

## 9. 实现里程碑

### 里程碑 0：schemas 与 Episode Data Package

交付：

- `pyproject.toml`、`uv.lock`、`src/`、`tests/`、CI、LICENSE；
- environment lock：Python、MuJoCo、MJLab/mujocolab backend reference、controller checkpoint、robot XML/MJCF 版本与 hash；JAX/JAXLIB 只在显式选择 MuJoCo Playground deferred fallback 时锁定；
- core schemas；
- `PolicyObservation`、`RuntimeEvent`、`OracleAnnotation` 隔离类型；
- event logger；
- Episode Data Package writer；
- sample EDP generation；
- schema roundtrip tests。

退出标准：

- structured command/status/failure/recovery records 可以序列化和反序列化；
- policy serializer 永远不能访问 oracle fields；
- 不运行 MuJoCo 也能生成 sample EDP；
- `.aris/meta/`、`.aris/traces/`、raw prompt/response 和机器私有运维信息不进 git。

### 里程碑 1：MuJoCo + G1 backend

交付：

- G1 model loading；
- mature controller backend wrapper；
- `stand_ready`、`track_velocity`、`turn_to`、`walk_to`、`safe_stop`；
- robot state 和 controller command logging；
- MJLab/mujocolab-compatible fallback smoke path。

退出标准：

- G1 能在 MuJoCo 中完成 basic local target approach；
- logs 包含 robot state、controller command、metrics；
- 若 controller smoke gate 仍不能稳定执行 `stand_ready`、`track_velocity`、`safe_stop`、short `walk_to`，则主证据路径切到 MJLab/mujocolab-compatible classic MuJoCo backend。

### 里程碑 2：grounding 与 temporary memory

交付：

- controlled detector-like grounding adapter；
- target ambiguity / target loss / low-confidence / invalid-depth failure injection；
- optional YOLO-World fast path；
- optional GroundingDINO/SAM2 fallback interface；
- depth projection；
- temporary object memory；
- safe stop pose generation。

退出标准：

- runtime 通过 RGB-D-style interface 接收 detector-like target records；
- 不使用 MuJoCo object id 或 ground-truth target pose；
- evaluation oracle 可单独评分 grounding accuracy。

### 里程碑 3：NavigatorV0 与 Safety Shield

交付：

- MPC / optimization local planner；
- local obstacle representation；
- route validation；
- local replan；
- safety shield integration。

退出标准：

- 系统能接近目标并避开局部障碍；
- planner 能返回 typed blocked / no-feasible-plan failure。

### 里程碑 4：Body Memory 与 Supervisory Recovery

交付：

- instant state；
- windowed summary；
- event/recovery memory；
- cause × temporal-profile failure cells；
- typed recovery actions；
- option / SMDP contracts；
- snapshot/restore 和 common random numbers；
- rule baseline 和 safety fallback；
- bandit sanity-check trainer；
- instant/frame-stack/GRU/typed-memory sanity selectors。

退出标准：

- rule baseline 和 learned selectors 能响应每类预注册 benchmark cell；
- option contract 和 decision epoch 已冻结；
- snapshot branching 单元测试通过；若未通过，所有评估降级为 paired matched-seed diagnostic；
- bandit sanity check 在长 PPO 前验证 typed memory 是否优于 ordinary history；
- 每个 episode 写 recovery traces。

### 里程碑 5：Seeded Benchmark 与 Ablations

交付：

- scenario generator distributions；
- severity ranges；
- train/validation/test seed protocol；
- controller-native baseline；
- rule baseline；
- instant MLP；
- frame-stack raw-history baseline；
- GRU raw-history baseline；
- typed event/body memory；
- memory mask / shuffled / stale interventions；
- branch oracle 或 evaluation-only oracle upper bound；
- batch runner；
- metrics aggregation。

退出标准：

- 所有方法跑相同 held-out seeds 或相同 base snapshots；
- 报告包含 confidence intervals、per-cell breakdowns、policy-only outcome、full-stack-with-fallback outcome、fallback invocation rate 和 safety override rate。

### 里程碑 6：Viser Dashboard

交付：

- integrated WebUI dashboard；
- 3D scene；
- grounding panel；
- body memory panel；
- recovery panel；
- benchmark panel；
- high-level typed UI commands。

退出标准：

- dashboard 可调试 live/replay episode；
- dashboard 不能绕过 `RuntimeManager` 或 `SafetySupervisor`。

### 里程碑 7：研究报告

交付：

- experiment tables；
- failure case studies；
- ablation analysis；
- external benchmark positioning；
- limitations；
- V1 plan。

退出标准：

- V0 hypotheses 要么被证据支持，要么被明确 falsified。

---

## 10. 风险与缓解

| 风险 | 影响 | 缓解 |
|---|---|---|
| mature G1 controller 难以集成 | 阻塞 runtime | 设置 controller smoke gate；失败则切 MJLab/mujocolab-compatible classic MuJoCo 证据路径 |
| open-vocabulary detector 在 MuJoCo 画面中慢或脆弱 | perception 成为主瓶颈 | V0 主实验用 controlled detector-like adapter；真实 detector 作为 demo/V1+ |
| controlled grounding 看起来太人工 | language/open-vocab claim 弱 | 明确 V0 是 detector-like interface + failure injection，不声称真实 open-vocab 主结果 |
| logging 太重 | 影响 benchmark 和磁盘 | 配置 rate、压缩、retention policy |
| MPC local planner 太复杂 | 延迟 recovery 工作 | 先做 minimal optimization planner，保留 API |
| body memory 被认为只是 renamed state | novelty 弱 | 做 instant/frame-stack/GRU/typed-memory 对照和 decision-time memory-content intervention |
| snapshot branching 失败 | 因果措辞不成立 | 降级为 paired matched-seed diagnostic，不写 counterfactual / ATE / branch oracle |
| PPO 不稳定或昂贵 | 延迟核心结果 | 先做 bandit sanity check；冻结 controller/planner；recovery actions 按 options / SMDP 定义 |
| rule recovery 太强或太弱 | 论文故事不稳 | 认真调优 rule baseline；同时报告 policy-only、fallback invocation 和 safety override；若打平 learned policy，pivot 到 protocol/diagnostic |
| benchmark 被认为 self-serving | external validity 弱 | 预注册 seed/severity；报告 held-out seeds；对齐 MJLab/classic MuJoCo 运行记录，并把 MuJoCo Playground、LocoMuJoCo、HumanoidBench 作为外部参考 |
| negative-control 被误写成“无效果” | 统计结论错误 | 预注册 smallest effect size of interest，使用 equivalence / TOST 风格证据 |
| dashboard 消耗太多时间 | 延迟 benchmark | 只做 debugging 和 data validation 必需 panel |
| multi-agent scope creep | 分散 V0 | Agent Bus 只保留 interface，不进入 real-time loop |
| 无真机结果 | venue 强度受限 | 先目标 workshop / RA-L / IROS 风格实证论文，V1/V2 做硬件 |

---

## 11. 当前实验计划对 PRD 的更新

Opus 4.8 rerun 后，当前最稳论文主线调整为：

- 不把 8-action supervisor 当 novelty；
- 不声称 “memory 普遍有用”；
- 主打 **memory intervention diagnostic**：
  - memory 何时改变 high-level recovery action；
  - 从同一个 decision snapshot 分支时，这种 action change 是否改善 recovery；
  - snapshot branching 未完成前，只能报告 paired matched-seed diagnostic；
  - negative-control 是否落入预注册等效区间；
  - shuffled / stale / masked memory 是否不能产生假提升。

当前必须做的 evidence package：

- frozen-only / controller-native；
- tuned heuristic；
- instant MLP supervisor；
- frame-stack raw-history baseline；
- GRU raw-history baseline；
- typed event/body memory supervisor；
- memory mask / shuffled / stale interventions；
- shuffled-memory negative-control；
- branch oracle 或 evaluation-only oracle upper bound；
- VLM-prompt supervisor；核心 gate 通过后作为附录或 language branch；
- snapshot branching；未实现前为 paired matched-seed diagnostic；
- per-cell breakdown；
- hierarchical / cluster bootstrap CI、effect size、negative-control equivalence / TOST。

---

## 12. 开放问题

这些问题留给实现期验证：

1. [ ] 哪个 Unitree G1 controller backend 能通过 controller smoke gate？
2. [ ] G1 gate 失败时，具体使用哪个 MJLab/mujocolab-compatible humanoid environment 和 controller wrapper？
3. [ ] NavigatorV0 使用哪个 MPC / optimization library？
4. [ ] 第一版 `balance_margin` 如何数值化？
5. [ ] 如果 backend 不暴露 confidence，`controller_confidence` 如何估计？
6. [ ] `instant_mlp`、`frame_stack_raw_history`、`GRU_raw_history`、`typed_event_body_memory` 包含哪些 observation features？
7. [ ] A800 上 bandit/PPO 可承受多少 seeds？
8. [ ] 每次 held-out evaluation run 可接受的 artifact 磁盘预算是多少？
9. [ ] `bxi_elf3` 哪些内容可以公开描述？
10. [ ] Snapshot/restore 在目标 MuJoCo backend 中能覆盖哪些 runtime states，哪些状态需要 adapter 层补齐？
11. [ ] Negative-control 的 smallest effect size of interest 设为多少？

---

## 13. 已锁定决策

- MuJoCo + Unitree G1 first。
- G1 smoke gate 失败时，用 MJLab/mujocolab-compatible classic MuJoCo backend 作为 V0 evidence backend；MuJoCo Playground 仅保留为 deferred optional external reference。
- `bxi_elf3` 和公司本体是后续兼容目标，不进入 V0 证据主线。
- 使用成熟 G1 controller backend，但不能让它成为 single point of failure。
- V0 不训练 end-to-end VLA。
- V0 不训练 low-level locomotion、gait、joint、residual controller policies。
- 只训练 self-stabilizing controller 之上的 high-level supervisory recovery selector。
- language parser 输出 structured locomotion commands。
- V0 主实验使用 controlled detector-like grounding adapter。
- YOLO-World / GroundingDINO / SAM2 只作为 optional demo 或 V1+ 主 perception target。
- runtime perception input 使用 RGB-D 和 camera parameters。
- MuJoCo privileged ground truth 只用于 evaluation。
- V0 使用 temporary object memory，但接口兼容 future persistent 3D semantic memory。
- memory API 包含 `write_observation`、`query_target`、`get_safe_stop_pose`、`update_status`、`expire`。
- V0 做 local target approach 和 local avoidance；保留 global navigation/exploration extension interface。
- 使用 MPC / optimization local planner + safety shield。
- body memory 包含 instant state、windowed summary、event/recovery memory；typed memory 必须和 ordinary raw-history baselines 公平比较。
- V0 RL recovery actions 为 `continue`、`slow_down`、`safe_stop`、`local_replan`、`recover_balance`、`refresh_target_grounding`、`relocalize`、`abort_task`。
- V0 recovery actions 必须按 options / SMDP 定义，不按瞬时低频 command 直接比较。
- `emergency_stop` 只属于 SafetySupervisor，不允许 RL 选择。
- `ask_agent_replan` 保留到未来高层 agent coordination。
- V0 使用 single `RuntimeManager`，不把 multi-agent execution 放进 real-time loop。
- Agent Bus 只用于 high-level async coordination 和 audit。
- Episode Data Package 从第一天开始使用。
- Viser dashboard 从第一阶段开始支持 debugging。
- 支持 batch benchmark runner 和 dashboard debug mode。
- 使用 seeded failure-recovery benchmark with train/validation/test split。
- `controller_native` 是必需 external baseline。
- `rule_recovery_tuned`、`instant_mlp`、`frame_stack_raw_history`、`GRU_raw_history`、`typed_event_body_memory`、memory mask/shuffled/stale interventions 和 `branch_oracle` / `oracle_upper_bound` 是 V0 评估主线。
- 长 PPO 前必须先跑 bandit sanity check、snapshot branching smoke、ordinary history baseline 和统计设计 gate。
- supervisory recovery、body memory、benchmark claims 是 V0 hypotheses，不是无条件最终 claim。

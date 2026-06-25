# 语言条件 Humanoid Locomotion Runtime 与监督式恢复研究计划

## 0. 项目记录

- **项目名称**：Humanoid Locomotion Runtime
- **初始平台**：MuJoCo + Unitree G1 humanoid model
- **fallback 平台**：如果 G1 controller 路径无法通过早期 smoke gate，则切换到 MuJoCo Playground humanoid locomotion backend。
- **后续兼容目标**：`bxi_elf3` / `bxi_robotics` 和公司自研 humanoid body。它们是 V1/V2 验证目标，不作为 V0 论文证据。
- **主目标**：构建一个可研究、可调试、可复现实验的人形机器人 locomotion runtime，把语言条件任务和受控 open-vocabulary-style grounding 转成可监控、可恢复的 humanoid locomotion skills。
- **核心方法位置**：在冻结的 self-stabilizing locomotion controller 之上，学习低频、高层、typed 的 supervisory recovery selector。
- **明确不声称**：本项目不训练 raw image/language 到 humanoid joint actions 的 foundation-scale end-to-end VLA。
- **明确不声称**：V0 不声称跨机器人本体泛化；backend-replaceable interfaces 是工程约束，不是实验结果。
- **当前论文姿态**：诊断性研究优先。最强主线不是“提出一个新 supervisor”，而是用 matched-seed counterfactual 量化 memory 何时、为何改变 recovery decision 并带来收益。

---

## 1. 摘要

### 1.1 问题

成熟的人形机器人 locomotion controller 通常能在受控场景中行走、转向、跟踪速度或目标，但它们大多只是低层运动后端。它们不会自然给出任务层证据，例如：

- 为什么当前执行变得不安全；
- 失败是否可恢复；
- 已尝试哪个 recovery action；
- 语言条件目标在 perception/navigation 失败后是否需要重新 grounding；
- body memory 是否能解释 repeated failure 或慢性退化。

对语言条件 humanoid agent 来说，普通 goal-reaching metric 会掩盖很多关键失败：动态障碍、localization drift、velocity tracking error、balance risk、target loss、user interruption 等都可能被平均 success rate 淹没。

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
2. [ ] benchmark 覆盖 seeded failure family，并且包含 negative-control failure。
3. [ ] 实验包含 controller-native baseline、tuned rule baseline、instant/window/full memory ablations、oracle upper bound。
4. [ ] 每个 episode 写出完整 Episode Data Package：manifest、event logs、metrics、timeseries、artifacts。
5. [ ] Viser dashboard 能查看 live/replay episode、grounding、route、status、body memory、recovery decision 和 benchmark metrics。
6. [ ] WebUI 和未来 agent 只能发 high-level typed command，不能绕过 `RuntimeManager` 或 `SafetySupervisor`。
7. [ ] learned recovery 是 low-frequency task-level component；locomotion controller、SafetySupervisor 和 hard stop path 保持 non-learned。

---

## 2. 产品与研究定位

### 2.1 核心定位

本项目不是 “mini HoloAgent”，也不是新的 humanoid foundation model。核心问题是：

> 当成熟 humanoid controller 已经具备自稳 locomotion 时，runtime 如何在保留 typed safety、logging、replay 和 benchmark comparability 的同时，学习任务层恢复决策，并诊断 body/event memory 何时真正有用？

V0 是单本体 evidence project。它使用 Unitree G1 first；若 G1 integration miss smoke gate，则切到 MuJoCo Playground humanoid backend。V0 不声称 learned selector 可以泛化到其他 humanoid body。

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

benchmark runner 需要系统检测 path blockage、localization drift、velocity tracking error、balance risk、target loss、user interruption 等 failure，让高层 recovery selector 选择 typed recovery action。

验收：

- [ ] failure mode taxonomy 覆盖 V0 failure families；
- [ ] recovery action taxonomy 明确 V0 允许选择的动作；
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
- evaluation-only true failure family；
- oracle action label。

允许 evaluation 使用：

- MuJoCo object pose；
- contact / fall state；
- privileged failure labels；
- oracle upper bound。

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

---

## 6. Benchmark 与评估设计

### 6.1 外部锚点

V0 使用内部 seeded failure-recovery benchmark，但必须锚定外部系统：

1. **MuJoCo Playground**
   - 作为 external controller-native reference 和 fallback humanoid backend。
   - 参考：<https://playground.mujoco.org/>、<https://arxiv.org/abs/2502.08844>

2. **LocoMuJoCo**
   - 作为 locomotion robustness 和 evaluation protocol 参考。
   - 参考：<https://loco-mujoco.readthedocs.io/en/v0.3.0/>、<https://arxiv.org/abs/2311.02496>

3. **HumanoidBench**
   - 作为 benchmark positioning 和 optional sanity-check tasks 参考。
   - 参考：<https://humanoid-bench.github.io/>、<https://arxiv.org/abs/2403.10506>

### 6.2 V0 failure families

初始研究计划保留五类 failure family，但实验计划已进一步强调 matched-seed 和 negative-control。实现时至少覆盖：

1. **transient / instant negative-control**
   - 理论上 memory 不应带来显著收益。
   - 用于防止 “memory 总有用” 的伪结论。

2. **dynamic obstacle / path blockage**
   - 新障碍或移动障碍阻塞路线。
   - 测试 slow down、safe stop、local replan、blocked-region side effects。

3. **localization / sensor degradation**
   - pose estimate 发生噪声、漂移、confidence drop 或短时丢失。
   - 测试 safe stop、relocalize、继续执行是否危险。

4. **velocity tracking / cumulative drift**
   - controller 跟踪速度或转向命令失败，或误差随时间累积。
   - 测试 slow down、safe stop、controller confidence、recovery latency。

5. **balance risk / degradation**
   - impulse、terrain perturbation、slip zone、stability margin drop 等 humanoid-specific risk。
   - 测试 recover_balance、safe_stop、abort boundary。

6. **target change / user interruption**
   - target 消失、target 改变、用户要求停止或换目标。
   - 测试 refresh grounding、safe stop、local replan、abort_task。

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

2. `rule_recovery`
   - 预注册 deterministic recovery policy。
   - 是 baseline、fallback、debugging oracle，不是主贡献。

3. `rl_instant_state`
   - 只观察当前 locomotion status 和 instant robot state。

4. `rl_window_memory`
   - 观察 instant state + short-window summaries。

5. `rl_full_body_memory`
   - 观察 instant state、window summaries、event/recovery memory。

6. `oracle_upper_bound`
   - evaluation-only privileged upper bound。
   - 不是公平 deployable method，不能作为 runtime 方法。

主要比较：

- `controller_native` vs `rl_full_body_memory`：runtime recovery 的价值。
- `rule_recovery` vs `rl_full_body_memory`：learned supervisory selection 的价值。
- `rl_instant_state` vs `rl_full_body_memory`：body/event memory 的价值。
- `rl_window_memory` vs `rl_full_body_memory`：event/recovery history 的额外价值。

### 6.5 RL training protocol

V0 采用 staged path：

1. **bandit sanity check**
   - 把 failure event 看成 one-step recovery-action selection。
   - 在跑长 PPO 前验证 memory observation 是否有信号。

2. **PPO supervisory recovery**
   - 训练低频 discrete recovery selector。
   - 冻结 locomotion controller 负责 gait/balance；PPO 只选择 typed recovery actions。

如果 bandit sanity check 显示 full memory 不优于 instant state，必须暂停 PPO 扩量，先检查 observation design、action taxonomy 和 scenario distributions。

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

- decision-flip rate；
- flip-conditioned recovery gain；
- paired bootstrap confidence interval；
- McNemar / paired test；
- shuffled-memory negative-control gain；
- per-family effect size。

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

- core schemas；
- event logger；
- Episode Data Package writer；
- sample EDP generation；
- schema roundtrip tests。

退出标准：

- structured command/status/failure/recovery records 可以序列化和反序列化；
- 不运行 MuJoCo 也能生成 sample EDP。

### 里程碑 1：MuJoCo + G1 backend

交付：

- G1 model loading；
- mature controller backend wrapper；
- `stand_ready`、`track_velocity`、`turn_to`、`walk_to`、`safe_stop`；
- robot state 和 controller command logging；
- MuJoCo Playground fallback smoke path。

退出标准：

- G1 能在 MuJoCo 中完成 basic local target approach；
- logs 包含 robot state、controller command、metrics；
- 若 week 3 结束仍不能稳定执行 `stand_ready`、`track_velocity`、`safe_stop`、short `walk_to`，则主证据路径切到 MuJoCo Playground。

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
- V0 failure families；
- typed recovery actions；
- rule baseline 和 safety fallback；
- bandit sanity-check trainer；
- PPO supervisory recovery selector。

退出标准：

- rule baseline 和 RL selector 能响应每类 benchmark failure；
- bandit sanity check 在长 PPO 前验证 memory signal；
- 每个 episode 写 recovery traces。

### 里程碑 5：Seeded Benchmark 与 Ablations

交付：

- scenario generator distributions；
- severity ranges；
- train/validation/test seed protocol；
- controller-native baseline；
- rule baseline；
- instant/window/full memory ablations；
- batch runner；
- metrics aggregation。

退出标准：

- 所有方法跑相同 held-out seeds；
- 报告包含 confidence intervals 和 per-family breakdowns。

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
| mature G1 controller 难以集成 | 阻塞 runtime | 设置 week-3 smoke gate；失败则切 MuJoCo Playground 证据路径 |
| open-vocabulary detector 在 MuJoCo 画面中慢或脆弱 | perception 成为主瓶颈 | V0 主实验用 controlled detector-like adapter；真实 detector 作为 demo/V1+ |
| controlled grounding 看起来太人工 | language/open-vocab claim 弱 | 明确 V0 是 detector-like interface + failure injection，不声称真实 open-vocab 主结果 |
| logging 太重 | 影响 benchmark 和磁盘 | 配置 rate、压缩、retention policy |
| MPC local planner 太复杂 | 延迟 recovery 工作 | 先做 minimal optimization planner，保留 API |
| body memory 被认为只是 renamed state | novelty 弱 | 做 instant/window/full memory ablations 和 matched-seed decision-flip analysis |
| PPO 不稳定或昂贵 | 延迟核心结果 | 先做 bandit sanity check；冻结 controller/planner；action space 保持离散低频 |
| rule recovery 太强或太弱 | 论文故事不稳 | 认真调优 rule baseline；若打平 learned policy，pivot 到 protocol/diagnostic |
| benchmark 被认为 self-serving | external validity 弱 | 预注册 seed/severity；报告 held-out seeds；对齐 MuJoCo Playground、LocoMuJoCo、HumanoidBench |
| dashboard 消耗太多时间 | 延迟 benchmark | 只做 debugging 和 data validation 必需 panel |
| multi-agent scope creep | 分散 V0 | Agent Bus 只保留 interface，不进入 real-time loop |
| 无真机结果 | venue 强度受限 | 先目标 workshop / RA-L / IROS 风格实证论文，V1/V2 做硬件 |

---

## 11. 当前实验计划对 PRD 的更新

Opus 4.8 rerun 后，当前最稳论文主线调整为：

- 不把 8-action supervisor 当 novelty；
- 不声称 “memory 普遍有用”；
- 主打 **memory-value diagnostic**：
  - memory 何时改变 high-level recovery action；
  - 这种 action flip 是否在 matched seed 下改善 recovery；
  - negative-control failure 上是否没有收益；
  - shuffled memory 是否不能产生假提升。

当前必须做的 evidence package：

- frozen-only / controller-native；
- tuned heuristic；
- no-memory supervisor；
- full-memory supervisor；
- shuffled-memory negative-control；
- oracle upper bound；
- VLM-prompt supervisor；
- matched-seed counterfactual；
- per-family breakdown；
- bootstrap CI / effect size。

---

## 12. 开放问题

这些问题留给实现期验证：

1. [ ] 哪个 Unitree G1 controller backend 能通过 week-3 smoke gate？
2. [ ] G1 gate 失败时，具体使用哪个 MuJoCo Playground humanoid environment？
3. [ ] NavigatorV0 使用哪个 MPC / optimization library？
4. [ ] 第一版 `balance_margin` 如何数值化？
5. [ ] 如果 backend 不暴露 confidence，`controller_confidence` 如何估计？
6. [ ] `rl_instant_state`、`rl_window_memory`、`rl_full_body_memory` 包含哪些 observation features？
7. [ ] A800 上 bandit/PPO 可承受多少 seeds？
8. [ ] 每次 held-out evaluation run 可接受的 artifact 磁盘预算是多少？
9. [ ] `bxi_elf3` 哪些内容可以公开描述？

---

## 13. 已锁定决策

- MuJoCo + Unitree G1 first。
- G1 smoke gate 失败时，用 MuJoCo Playground humanoid backend 作为 V0 evidence backend 和 external controller-native reference。
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
- body memory 包含 instant state、windowed summary、event/recovery memory。
- V0 RL recovery actions 为 `continue`、`slow_down`、`safe_stop`、`local_replan`、`recover_balance`、`refresh_target_grounding`、`relocalize`、`abort_task`。
- `emergency_stop` 只属于 SafetySupervisor，不允许 RL 选择。
- `ask_agent_replan` 保留到未来高层 agent coordination。
- V0 使用 single `RuntimeManager`，不把 multi-agent execution 放进 real-time loop。
- Agent Bus 只用于 high-level async coordination 和 audit。
- Episode Data Package 从第一天开始使用。
- Viser dashboard 从第一阶段开始支持 debugging。
- 支持 batch benchmark runner 和 dashboard debug mode。
- 使用 seeded failure-recovery benchmark with train/validation/test split。
- `controller_native` 是必需 external baseline。
- `rule_recovery`、`rl_instant_state`、`rl_window_memory`、`rl_full_body_memory` 和 `oracle_upper_bound` 是 V0 评估主线。
- 长 PPO 前必须先跑 bandit sanity check。
- supervisory recovery、body memory、benchmark claims 是 V0 hypotheses，不是无条件最终 claim。

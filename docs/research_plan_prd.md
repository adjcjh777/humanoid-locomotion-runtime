# 语言指令驱动的人形机器人行走运行时与恢复研究计划

这份 PRD 说明我们要做什么、为什么要这样做、哪些事情现在不做，以及后续实验怎样判断成败。文中会保留一些英文名词，因为它们会成为代码接口、论文方法名或实验表格字段；每个重要词都会尽量用白话解释。

---

## 0. 项目记录

- **项目名称**：Humanoid Locomotion Runtime。可以理解为“让人形机器人按语言目标行走、监控自己、出问题时恢复”的运行系统。
- **初始平台**：MuJoCo + 公司 Unitree G1 edu 23DoF profile。官方 `g1_23dof_rev_1_0.urdf/xml` source 已记录在 `docs/g1_edu_23dof_source_lock.md`，raw MuJoCo asset compile smoke 已记录在 `docs/g1_edu_23dof_compile_smoke.md`，R007e controller route/contract 已记录在 `docs/g1_edu_23dof_controller_route.md`。当前仍没有 mature 23DoF controller checkpoint，也还没有通过 project-local MJLab adapter/controller smoke。
- **reference 平台**：当前已跑通的是 MJLab 29DoF G1 reference smoke。它能证明 backend health，不能直接作为公司 23DoF edu G1 evidence。
- **fallback 平台**：如果 G1 controller 早期 smoke gate 过不了，优先切到 MJLab/mujocolab-compatible classic MuJoCo humanoid locomotion backend。意思是先找一个更容易跑通、但仍然是 classic MuJoCo 的人形行走后端，而不是默认切到 MuJoCo Playground。
- **后续兼容目标**：`bxi_elf3` / `bxi_robotics` 和公司自研 humanoid body。它们是 V1/V2 的扩展验证目标，不作为 V0 论文主证据。
- **主目标**：做一个可研究、可调试、可复现实验的人形机器人行走运行时。它把语言目标和受控的目标识别结果，转成可监控、可记录、可恢复的行走技能。
- **核心方法位置**：底层行走 controller 保持冻结，只在上层学习“遇到问题时选哪种恢复动作”。这个选择器是低频、高层、typed 的 supervisory recovery selector。
- **明确不声称**：本项目不训练从原始图像/语言直接输出人形机器人关节动作的 foundation-scale end-to-end VLA。
- **明确不声称**：V0 不声称能跨机器人本体泛化。接口设计成可替换 backend 是工程约束，不是实验结论。
- **当前论文姿态**：诊断性研究优先。最强主线不是“我们发明了一个新 supervisor”，而是研究 memory 什么时候会改变高层恢复决策，以及这种改变是否真的带来收益。只有实现完整 snapshot branching 后，才能写 counterfactual / ATE / branch oracle 这类因果措辞；在那之前只能写 paired matched-seed diagnostic。

### 0.1 本文常用词的白话解释

- **runtime**：机器人执行任务时一直运行的“总调度系统”。它接收目标、调用模块、记录状态、处理失败。
- **locomotion controller**：底层行走控制器，负责步态、平衡、速度跟踪等身体运动。
- **supervisory recovery selector**：高层恢复动作选择器。它不直接控制关节，只在失败时选择“减速、停下、重规划、重新识别目标”等动作。
- **typed command / typed event**：带明确字段和类型的命令或事件，方便记录、回放、测试和审计。
- **grounding**：把语言里的目标落到视觉或仿真观测里，例如把“红椅子”对应到某个检测框或深度位置。
- **controlled detector-like grounding**：V0 用受控的、像检测器输出一样的数据来模拟目标识别，而不是把真实 open-vocabulary detector 当成主实验前提。
- **body/event memory**：记录机器人身体状态、失败事件、恢复尝试和短期历史的记忆。
- **Episode Data Package, EDP**：每次 episode 的完整证据包，包含事件、指标、时间序列、artifact 和回放索引。
- **snapshot branching**：在同一个决策点保存完整状态，然后分支尝试不同动作，用来比较哪个动作更好。
- **oracle**：只在 evaluation 中使用的上界参考。它可以使用 runtime 不能看的 privileged 信息，不能作为可部署方法。
- **negative-control**：预期不应该从 memory 中获益的测试格子，用来防止我们把偶然波动误写成方法有效。

---

## 1. 摘要

### 1.1 问题

成熟的人形机器人行走 controller 往往能在干净场景中走路、转弯、跟踪速度或靠近目标。但它们通常只是底层运动后端，不会自动告诉我们任务层发生了什么，例如：

- 为什么当前执行开始变得不安全；
- 这个失败能不能恢复；
- 系统之前尝试过哪个 recovery action；
- 视觉或导航失败后，语言目标是否需要重新 grounding；
- body memory 是否能解释 repeated failure 或慢性退化。

对语言指令驱动的人形机器人来说，只看最终有没有到达目标不够。动态障碍、定位漂移、速度跟踪误差、平衡风险、目标丢失等问题，都会被平均 success rate 掩盖。`user_interrupt` 是用户控制任务的事件，不算 failure family。

### 1.2 方案

我们围绕成熟 Unitree G1 locomotion controller，在 MuJoCo 里构建 language-conditioned humanoid locomotion runtime。V0 的目标本体是公司 G1 edu 23DoF；在 23DoF controller smoke 前，29DoF MJLab G1 只能作为 reference backend。V0 包含以下模块：

- controlled detector-like grounding：用受控检测结果模拟语言目标落地；
- temporary object memory：短期记录目标、证据和安全停靠位置；
- MPC / optimization local planner：做局部路径规划；
- typed locomotion skills：用明确接口调用行走技能；
- status monitor：持续检查执行状态和风险；
- body/event memory：记录身体状态、失败和恢复历史；
- high-level supervisory recovery selector：在失败时选择高层恢复动作；
- deterministic rule fallback 和 `SafetySupervisor`：提供规则兜底和安全停止；
- Episode Data Package：保存每次 episode 的证据；
- Viser WebUI dashboard：用于调试和回放。

初版保持单一 `RuntimeManager`。底层 controller 冻结，RL 只用于低频的高层 recovery action selection。RL 不输出 joint command，也不替代 self-stabilizing controller。实时安全由 `RuntimeManager` 和 `SafetySupervisor` 在本地闭环保证。Agent Bus 只保留为未来高层异步协作、审计和实验分析接口，不进入实时安全闭环。

### 1.3 V0 成功标准

V0 通过需要同时满足：

1. [ ] runtime 能在 MuJoCo 中，用 Unitree G1 或 fallback humanoid backend 执行语言条件 local locomotion task。
2. [ ] benchmark 覆盖 cause x temporal-profile 的 seeded failure cells，并包含预注册 negative-control。
3. [ ] 实验包含 controller-native、tuned rule、instant MLP、frame-stack raw history、GRU raw history、typed event/body memory、memory mask/shuffled/stale、branch oracle 或 evaluation-only oracle upper bound。
4. [ ] 每个 episode 写出完整 Episode Data Package：manifest、event logs、metrics、timeseries、artifacts。
5. [ ] Viser dashboard 能查看 live/replay episode、grounding、route、status、body memory、recovery decision 和 benchmark metrics。
6. [ ] WebUI 和未来 agent 只能发 high-level typed command，不能绕过 `RuntimeManager` 或 `SafetySupervisor`。
7. [ ] learned recovery 只做 low-frequency task-level decision；locomotion controller、`SafetySupervisor` 和 hard stop path 保持 non-learned。

---

## 2. 产品与研究定位

### 2.1 核心定位

本项目不是 “mini HoloAgent”，也不是新的 humanoid foundation model。核心问题是：

> 当成熟 humanoid controller 已经能自稳行走时，runtime 怎样在保留 typed safety、logging、replay 和 benchmark 可比性的同时，学习任务层恢复决策，并诊断 body/event memory 到底什么时候有用？

V0 是单本体证据项目。它先用公司 Unitree G1 edu 23DoF；如果 23DoF integration 没过 smoke gate，就切到明确标注的 MJLab/mujocolab-compatible classic MuJoCo reference backend。V0 不声称 learned selector 可以泛化到其他 humanoid body，也不把 29DoF reference 结果说成 23DoF target evidence。

人形机器人和轮式机器人不同，任务进展和身体动态强耦合。runtime 需要看 balance margin、contact state、slip、fall risk、velocity/orientation tracking error、controller confidence、recovery latency 等信号，然后判断机器人应该继续、减速、停下、恢复平衡、重新 grounding、重新定位、replan，还是 abort。

### 2.2 V0 工作假设

这些是假设，不是最终论文 claim：

1. **supervisory recovery hypothesis**：不训练低层 gait/joint control，只训练高层 recovery selector，也可能改善 task-level recovery。
2. **body/event memory hypothesis**：带 window summary 和 event/recovery memory 的 selector，在长时序、累积型、退化型 failure 中，可能优于只看当前状态的 selector。
3. **benchmark hypothesis**：seeded failure-recovery evaluation 能暴露普通 goal-reaching metrics 看不到的问题。

### 2.3 V1 / V2 可能升级

V0 先把证据链跑通。后续可以升级：

- parameterized recovery actions：恢复动作带参数，例如减速幅度或重规划范围；
- residual 或 status-conditioned controller adaptation：在冻结 controller 外做更细的适配；
- Unitree G1 到 `bxi_elf3` / 公司 humanoid body 的迁移验证；
- persistent 3D semantic memory：用长期 3D 语义记忆替代 V0 的 temporary object memory；
- global navigation 和 active exploration；
- multi-agent runtime manager、TaskRouter、auditable Agent Bus；
- 真实 open-vocabulary detector 作为主 perception path；
- sim-to-real 和硬件实验。

---

## 3. 用户、故事与验收标准

### 3.1 用户

1. **research developer**：快速测试 humanoid locomotion recovery idea。
2. **benchmark runner**：跑可复现批量实验和 ablation。
3. **debug operator**：用 dashboard 看 robot state、target grounding、route、failure、recovery。
4. **future multi-agent orchestrator**：未来把 planner、recovery、evaluator agents 分离，但它们只能通过 typed task/event interfaces 协作。

### 3.2 Story 1：执行语言条件 locomotion

用户提交 “walk to the red chair slowly” 这类指令。runtime 应该能把它解析成结构化命令，找到目标，规划安全的局部路径，调用 G1 locomotion skill，监控状态，并在失败时恢复。

验收：

- [ ] instruction 转为 structured locomotion command；
- [ ] target grounding 使用 RGB-D 和 detector-like output，不使用 MuJoCo privileged object id；
- [ ] temporary object memory 记录 target evidence 和 safe stop pose；
- [ ] locomotion skill 通过成熟 G1 controller backend 执行；
- [ ] 关键事件写入 Episode Data Package。

### 3.3 Story 2：从 runtime failures 中恢复

benchmark runner 需要系统检测 path blockage、localization drift、velocity tracking error、balance risk、target loss 等 failure。用户中断或目标变更要记录成 task-control event。高层 recovery selector 从有限的 typed recovery actions 中选择下一步。

验收：

- [ ] failure taxonomy 使用 cause x temporal-profile 二维结构；
- [ ] recovery action taxonomy 明确 V0 能选哪些动作，并为每个动作定义 option / SMDP contract；
- [ ] V0 RL action set 限定为：
  - `continue`
  - `slow_down`
  - `safe_stop`
  - `local_replan`
  - `recover_balance`
  - `refresh_target_grounding`
  - `relocalize`
  - `abort_task`
- [ ] rule-based recovery 作为 baseline 和 fallback，不作为 oracle 或主贡献；
- [ ] recovery decision 记录 pre-status、post-status、latency、success、fallback；
- [ ] repeated failures 能通过 body memory event records 看到。

### 3.4 Story 3：比较 ablations

研究者需要在同一个 benchmark 上比较这些方法：

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

debug operator 需要用 Viser dashboard 查看 live/replay scene，理解 episode 为什么失败，以及 recovery 是否正确。

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

下面是一次任务从语言到执行、再到记录和恢复的大致流向：

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

白话解释：语言先进入解析器，目标经过 grounding，memory 记录目标证据，planner 规划局部路径，controller 执行行走，monitor 检查风险，recovery selector 在失败时选恢复动作，SafetySupervisor 始终保留最后的安全兜底，所有证据写进 EDP 和 dashboard。

### 4.2 runtime components

主要组件如下：

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

`RuntimeManager` 是总入口。其他模块可以替换，但不能绕过它直接控制底层 controller 或安全逻辑。

### 4.3 实时边界与 agent 协作边界

| 层 | 用途 | 机制 |
|---|---|---|
| real-time runtime bus | 执行机器人动作、更新状态、处理风险、本地恢复和安全停止 | ROS2、Python async queue、gRPC 或 shared runtime state |
| agent coordination bus | 高层异步任务、审计、长周期重规划、实验分析 | TaskRouter、AgentPort、未来 Agent Bus |

规则：

- safety-critical execution 不等待 LLM 或 Agent Bus。
- `SafetySupervisor` 在本地同步执行，有权停止或 override unsafe execution。
- agent suggestions 只是 typed recommendations，不是最终执行权。
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

schema-first 是硬约束。先把命令、状态、事件、日志、replay 和 benchmark runner 的数据格式定好，再接 MuJoCo、perception、dashboard、controller 这类重依赖。这样做是为了避免后面系统跑起来了，却没有办法复现和审计。

### 5.2 运行时禁止输入

runtime decision 禁止使用这些 privileged 信息：

- MuJoCo object id；
- ground-truth target pose；
- simulator semantic label；
- evaluation-only true failure labels / cause-temporal cells；
- oracle action label。

evaluation 可以使用这些信息，但只能用于打分、诊断或上界参考：

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

`emergency_stop` 只属于 `SafetySupervisor` override，不允许 RL 选择。`ask_agent_replan` 留到未来 high-level agent coordination。`mark_blocked_region` 是 planner/memory 的 side effect，不是 V0 RL action。

这些 recovery actions 不是一下子发出的瞬时动作，而是有开始条件、持续时间和结束条件的 options / SMDP contract。每个 action 至少要定义：

- initiation condition；
- action mask；
- execution implementation；
- minimum duration；
- maximum duration；
- success condition；
- failure condition；
- termination condition；
- interruptibility；
- retry budget；
- cooldown。

Decision epoch 只发生在 failure trigger、active option termination、option timeout 或重大 task-control event。

---

## 6. Benchmark 与评估设计

### 6.1 外部锚点

V0 会用内部 seeded failure-recovery benchmark，但不能闭门造指标。它必须和外部系统对齐：

1. **MJLab / mujocolab-compatible classic MuJoCo stack**
   - V0 首选 fallback humanoid backend，也是 controller smoke test 的优先集成路径。

2. **MuJoCo Playground**
   - deferred optional external reference。只有 MJLab/classic MuJoCo 路径无法支撑必要 evidence 时才启用。
   - 参考：<https://playground.mujoco.org/>、<https://arxiv.org/abs/2502.08844>

3. **LocoMuJoCo**
   - 用作 locomotion robustness 和 evaluation protocol 参考。
   - 参考：<https://loco-mujoco.readthedocs.io/en/v0.3.0/>、<https://arxiv.org/abs/2311.02496>

4. **HumanoidBench**
   - 用作 benchmark positioning 和 optional sanity-check tasks 参考。
   - 参考：<https://humanoid-bench.github.io/>、<https://arxiv.org/abs/2403.10506>

### 6.2 V0 failure taxonomy

V0 不用单列 failure family，而使用 cause x temporal-profile 二维结构。白话说，就是同时记录“失败是什么原因”和“失败是短暂、持续、反复，还是逐渐变坏”。

实现时至少覆盖：

| Cause | Temporal profile 示例 | 角色 |
| --- | --- | --- |
| path blockage | transient / persistent / recurrent | path x transient 是 negative-control；path x recurrent 是 memory-positive candidate |
| localization degradation | transient / cumulative / persistent | persistent / cumulative 是 memory-positive candidate |
| tracking degradation | transient / cumulative | cumulative 是 memory-positive candidate |
| balance disturbance | impulse / recurrent / progressive | impulse 可作为 near-Markov control |
| target/task event | change / loss / interruption | task-control event；`user_interrupt` 不作为 failure family |

主实验必须预注册少量 cells，例如 path x transient negative-control、path x recurrent、tracking x cumulative、localization x persistent、balance x impulse。至少一个 positive benchmark cell 必须显式制造 state aliasing：当前 observation 看起来相近，但历史不同，因此 oracle 最优 recovery action 不同。

### 6.3 seed protocol

- train seeds：按 compute budget 扩大。
- validation seeds：每个 family 固定 seed，用于 tuning 和 early stopping。
- test seeds：held-out fixed seeds，用于最终报告。
- 所有方法必须跑相同 validation/test seeds。
- scenario generator distributions 和 severity ranges 必须在 final test 前提交。
- failed episodes 保留并报告；禁止只挑成功案例。

### 6.4 methods and ablations

1. `controller_native`
   - 只通过底层 backend native command interface 执行。
   - 不使用 typed recovery runtime、不使用 body memory、不使用 learned selector。

2. `rule_recovery_tuned`
   - 预注册 deterministic recovery policy。
   - 是 deployable heuristic baseline 和 fallback，不是 debugging oracle。

3. `instant_mlp`
   - 只观察当前 locomotion status 和 instant robot state。

4. `frame_stack_raw_history`
   - 观察同样合法输入源的一段固定长度 raw history。

5. `GRU_raw_history`
   - 观察同样合法输入源的 recurrent raw history，是主文必需 ordinary history baseline。

6. `typed_event_body_memory`
   - 观察 instant state、window summaries、event/recovery memory。

7. `memory_mask / shuffled / stale`
   - 对同一个 typed-memory policy 做 decision-time memory-content intervention。
   - typed-memory policy 训练时必须包含 memory dropout 或 `memory_available` mask，避免 test-time masking 变成 out-of-distribution 输入。

8. `branch_oracle` / `oracle_upper_bound`
   - evaluation-only privileged upper bound。
   - 优先来自 snapshot branching 下全部合法 actions 的结果比较。
   - 它不是公平 deployable method，不能作为 runtime 方法。

主要比较：

- `controller_native` vs `typed_event_body_memory`：runtime recovery 有没有价值。
- `rule_recovery_tuned` vs `typed_event_body_memory`：learned supervisory selection 有没有价值。
- `instant_mlp` vs `typed_event_body_memory`：memory representation 有没有价值。
- `frame_stack_raw_history` / `GRU_raw_history` vs `typed_event_body_memory`：typed memory 是否优于普通历史模型。
- correct/null/shuffled/stale memory input：decision-time memory-content effect。

### 6.5 RL training protocol

V0 采用 staged path，先做便宜验证，再决定是否扩大训练：

1. **bandit sanity check**
   - 把 failure event 看成 one-step recovery-action selection。
   - 在跑长 PPO 前，先验证 memory observation 是否真的有信号。

2. **PPO supervisory recovery**
   - 训练低频 discrete recovery selector。
   - locomotion controller 冻结，负责 gait/balance；PPO 只选择 typed recovery options。
   - 只有 Gate A-E 通过后才启动。
   - 如果 bandit / branch pilot 已经能回答研究问题，可以保持更轻量的 selector，不强行上长 PPO。

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

- 所有 command、status、failure、recovery record 都能序列化和反序列化。
- sample Episode Data Package 可以在不运行 MuJoCo 的情况下生成。
- 如果进入 snapshot branching，EDP 必须记录 `base_snapshot_id`、`branch_id`、`decision_id`、`policy_training_seed`、`scenario_seed`、`exogenous_noise_seed`、`observation_hash`、`memory_hash`、`action` 和 `option_outcome`。
- 大型 raw logs、bags、datasets、checkpoints、weights 不进 git。
- held-out evaluation run 保留足够 artifact，用于 failure diagnosis。

白话解释：EDP 是每次实验的“证据包”。以后论文里说某个 episode 失败、某个恢复动作有效，必须能回到 EDP 里复查，而不是只看一行 summary。

---

## 8. Dashboard

V0 使用 Viser dashboard。它的目标是 debugging 和 data validation，不是展示型 UI。

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
- cause x temporal-profile failure cells；
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
  - memory 什么时候改变 high-level recovery action；
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

1. [ ] 官方 Unitree RL MJLab G1 velocity ONNX candidate 能否通过本仓库 adapter 的 controller smoke gate？当前已知 ONNX input `[1,98]`、output `[1,29]`，MJLab actor obs `[1,99]`，需要 adapter。
2. [x] V0 首选 MJLab/mujocolab-compatible backend reference：项目内 `third_party/mjlab` 的 `Mjlab-Velocity-Flat-Unitree-G1`，wrapper 为 `VelocityOnPolicyRunner`；证据见 `docs/mjlab_backend_lock.md`。
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
- V0 首选 MJLab/mujocolab-compatible backend reference 锁定为项目内 `third_party/mjlab` submodule 的 `Mjlab-Velocity-Flat-Unitree-G1`；G1 MJCF、task config 和 wrapper hashes 见 `configs/environment.lock.toml` 与 `docs/mjlab_backend_lock.md`。
- 完整 MJLab dependency environment 和 G1 headless simulation smoke 已通过：`scripts/mjlab_sync_and_smoke.sh` 使用 Python 3.12.13、`third_party/mjlab/uv.lock`、A800 `cuda:0`，完成 `Mjlab-Velocity-Flat-Unitree-G1` reset + 16 zero-action steps；actor obs `[1,99]`、critic obs `[1,111]`、action `[1,29]`。
- 当前 controller artifact candidate 为官方 Unitree RL MJLab G1 velocity ONNX，存放于 ignored `checkpoints/unitree_rl_mjlab_g1_velocity_v0/`，来源与 hash 见 `docs/controller_checkpoint_selection.md`；adapter smoke 通过前不能作为成熟 controller evidence。公司 23DoF raw asset compile smoke 和 R007e controller contract 已通过/锁定；23DoF route 为 `train_23dof_required`，mature controller checkpoint 仍 pending。
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

# Literature-Informed Experiment Design

**日期**: 2026-06-28

**状态**: R048 / R071a Mac-safe 文献调研与实验设计更新。本文只冻结实验设计、指标卡和 baseline 要求，不表示 A800 rollout、controller-native baseline、PPO 或论文主结论已经完成。

**ARIS 验证输入**:

- 候选清单：`refine-logs/LITERATURE_CANDIDATES_20260628.json`
- 验证结果：`refine-logs/LITERATURE_VERIFICATION_20260628.json`
- 验证摘要：10 篇候选中 9 篇通过 arXiv high-confidence verification；`FLARE` 有 CVF official page，但当前 ARIS verifier 仍为 `verify_pending`，只能作为设计参考，不单独支撑主 claim。
- 检索限制：本轮 arXiv API 对少数精确查询出现 HTTP 502 / SSL EOF；已验证条目保留 arXiv ID，不补造 venue 或 DOI。

## 1. 文献到实验设计的映射

| 方向 | 参考论文与状态 | 论文实验设计习惯 | 本项目采用/改进 |
|------|----------------|------------------|----------------|
| Language-guided robot failure recovery | `RACER` (arXiv:2409.14674, verified) | 在标准 manipulation benchmark、动态目标变化、unseen tasks 和 real-world episodes 上比较 recovery policy 与 strong imitation baseline；核心指标是 task success / recovery success、zero-shot/generalization、动态 goal-change 下的成功率和失败案例。 | B5 里保留 `VLM_prompt_supervisor`，但不让它替代 `GRU_raw_history`；新增动态 target/task event cell，报告 per-family success、invalid action、decision latency 和 cost。 |
| Failure explanation/correction | `REFLECT` (arXiv:2306.15724, verified) | 构造 RoboFail 类 failure dataset，用多模态历史摘要生成 failure explanation，再看 explanation 是否帮助 correction planning。指标不只看最终成功，也看 failure explanation/correction usefulness。 | B1/B3 增加 detection/diagnosis 指标：failure-kind accuracy 只用于 evaluation，runtime 只能读合法摘要；必须报告 time-to-detect、false positive、false negative。 |
| Intervention-aware recovery during RL | `FARL` / `FailureBench` (arXiv:2601.07821, verified) | 把 intervention-requiring failures 作为安全核心指标；比较 safety critic、offline recovery policy 与在线 RL/post-training 的 failure rate、performance 和 generalization。 | B2 增加 `safety_only_monitor` baseline；主安全指标增加 `intervention_required_rate`、`unsafe_completion_rate`、`safety_override_rate`。任何 learned policy 若提高 unsafe/intervention rate，就不能只用 success gain 宣称更好。 |
| Humanoid/legged locomotion robustness | `Real-World Humanoid Locomotion with RL` (arXiv:2303.03381, verified, Science Robotics DOI recorded)、`Learning Humanoid Locomotion over Challenging Terrain` (arXiv:2410.03654, verified)、`RMA` (arXiv:2107.04034, verified) | 强调 history-conditioned controller / adaptation，在多地形、扰动、payload 或 sim-to-real variation 上报告 robustness、distance/time-to-fall、tracking quality 和 ablations。 | `frame_stack_raw_history` 与 `GRU_raw_history` 是主文必需；新增 `causal_transformer_raw_history` 作为 SHOULD baseline，用来防 reviewer 质疑 typed memory 只是弱 history model。 |
| Legged navigation with safety-aware planning | `VP-Nav` (arXiv:2112.02094, verified) | 让 high-level planner 感知 low-level locomotion capability；用 vision-only / proprioception / safety advisor ablations 比较 navigation success、obstacle handling、path efficiency 和 real-world deployment。 | B2/B3 对 path blockage、local replanning 和 route recovery 增加 `path_efficiency`、`goal_progress`, `near_collision_rate`, `min_clearance_violation_rate`, `local_replan_latency_s`。 |
| Long-horizon robot memory/map | `SERF` (arXiv:2606.12956, verified) | 比较 map/memory feature 与 image-only baseline；报告 subgoal completion、trajectory directness、scene-shift robustness、object-drop recovery。 | B3 的 memory intervention 必须拆成 correct/null/shuffled/stale；B4 增加 subgoal progress curve、memory staleness sensitivity 和 directness/path-efficiency 指标。 |
| Failure detection monitor | `Code-as-Monitor` (arXiv:2412.04455, verified)、`FLARE` (CVF official page, verifier pending) | 把 failure detection/correction monitor 单独评估，通常看 detection precision/recall/F1、false alarm、correction success、rollback/reset 和 latency。 | 新增 monitor-only metric card：检测能力和 recovery action selection 分开报；`safety_only_monitor` 不允许读 privileged MuJoCo truth，只能读 runtime-legal summaries。 |

## 2. 领域共识

1. **Success rate 不能单独作为主证据**。近邻 failure-recovery 论文都会同时报告安全失败、intervention、latency、correction/retry 和 per-scenario breakdown。  
   本项目主表必须至少包含 `recovery_success_rate`、`fall_rate`、`unsafe_completion_rate`、`intervention_required_rate`、`time_to_recover_s`、`decision_latency_s`、`episode_validity_rate`。

2. **History baseline 必须足够强**。Humanoid/legged locomotion 文献里 history-conditioned model 是强基线，不跑 `GRU_raw_history` 就无法说 typed memory 有价值。  
   本项目保留 `frame_stack_raw_history`、`GRU_raw_history` 为 MUST；新增 `causal_transformer_raw_history` 为 SHOULD，若不跑必须在 B2 summary 写 deferred reason。

3. **Monitor/safety baseline 要从 policy 中拆出来**。FARL、VP-Nav、Code-as-Monitor/FLARE 这类工作都会把安全监测或 recovery critic 单独评估。  
   本项目新增 `safety_only_monitor`：只触发 safe_stop / back_off / retry / abort 这类合法高层动作，不学习 memory policy，用来判断收益是否只是安全规则带来的。

4. **Memory claim 要做 content intervention**。长时序 memory/map 论文不是只比较“有 memory / 无 memory”，还要证明具体 memory 内容和时效性有用。  
   本项目 B3 必须用同一 policy 跑 correct/null/masked/shuffled/stale memory；训练时要有 memory dropout 或 `memory_available` mask，否则 test-time mask 结果不能解释。

5. **因果措辞只在 snapshot branching 后使用**。matched-seed design 可以作为诊断，但不能替代 simulator/runtime snapshot branching。  
   R018 未完成前，全部写 `paired matched-seed diagnostic`，不能写 counterfactual / ATE / branch oracle。

## 3. 指标卡与判定标准

### 3.1 Episode validity gate

- `episode_validity_rate`: valid EDP episodes / launched episodes。
- Pilot gate: `>= 0.90` 才能进入 baseline ladder。
- Final gate: `>= 0.95` 才能进入主表；低于该值必须报告 missing/invalid reasons。
- 每个 EDP 必须包含 robot profile、failure cell、seed、policy variant、legal observation hash、decision id、safety events 和 artifact manifest。

### 3.2 Failure protocol calibration

- `controller_native_success_rate`: controller-only baseline 在候选 failure cell 上的成功率。
- Positive memory cells: 主报告 severity 选 `0.30 <= controller_native_success_rate <= 0.70`，避免全成功/全失败。
- Negative-control cells: 预注册为 memory 不应产生实质收益；不能用 p-value non-significant 当作“无收益”。
- `failure_trigger_reproducibility`: 同 seed 复跑时 failure family/status 一致率。
- Pilot accept: family/status 一致率 `>= 0.95`；trigger time error `<= max(0.25s, episode_horizon * 0.05)`。

### 3.3 Primary endpoint

- `valid_recovery_success_rate`: 在 valid episodes 中，policy 在 recovery budget 内恢复任务进度，且没有 fall、unsafe completion、manual/intervention-required failure 或 safety abort。
- 主 claim 判定：typed memory 相对 best non-memory learned baseline 的 paired gain lower CI 必须超过 `SEI = 0.05`，或明确降级为 exploratory diagnostic。
- 如果 snapshot branching 未完成，只报告 matched-seed paired difference 和 uncertainty；不报告 ATE。

### 3.4 Safety endpoints

- `fall_rate`: episode 中发生 fall/unstable terminal 的比例。
- `unsafe_completion_rate`: 任务完成但发生禁用安全事件、碰撞或越界的比例。
- `safety_override_rate`: `SafetySupervisor` override / decision epochs。
- `intervention_required_rate`: 需要人工、reset、hard abort 或外部 rescue 的比例。
- No-Go: learned policy 的 `unsafe_completion_rate` 或 `intervention_required_rate` 相对 `rule_recovery_tuned` 的 upper CI 增加超过 `0.02`，不得宣称 overall improvement。

### 3.5 Recovery efficiency endpoints

- `time_to_detect_s`: failure onset 到 detector/monitor 第一次合法触发的时间。
- `time_to_recover_s`: failure onset 到恢复到 progress state 的时间。
- `decision_latency_s`: observation summary ready 到 high-level action emitted 的时间。
- `option_duration_s`: option execution duration；必须落在 option contract 的 min/max duration 内。
- `retry_count`、`repeated_failure_count`、`fallback_invocation_rate`: 用于解释 policy 是否只是反复 retry。
- VLM baseline 额外报告 `cost_per_episode` 和 invalid action rate。

### 3.6 Navigation/task endpoints

- `task_success_rate`: 整体任务完成率，单独报告，不替代 recovery success。
- `goal_progress`: recovery window 内到目标/waypoint 的 normalized progress。
- `path_efficiency`: shortest feasible path length / executed path length；不可行时标 `n/a`，不填 0。
- `local_replan_latency_s`: blockage 触发到新 route emitted 的时间。
- `near_collision_rate` / `min_clearance_violation_rate`: path blockage 和 safety advisor 的核心指标。
- `tracking_error_integral`: locomotion tracking degradation cells 的连续稳定性指标。

### 3.7 Memory/decision endpoints

- `decision_flip_rate`: memory-on/off 同 seed 或同 snapshot decision id 的 action 不同率；只作解释指标。
- `flip_conditioned_gain`: 只在 flip decisions 上计算 outcome difference，用来说明 memory 改变是否有用。
- `memory_content_effect`: 同一 typed-memory policy 在 correct/null/masked/shuffled/stale memory 下的 paired difference。
- `memory_staleness_sensitivity`: stale window length vs recovery success/latency curve。
- `over_conservatism_rate`: policy 选择 safe_stop/abort，但 controller_native 或 less conservative baseline 可恢复的比例。

### 3.8 Detection/diagnosis endpoints

- `failure_detection_precision`, `failure_detection_recall`, `failure_detection_f1`: monitor 是否及时、准确发现 failure。
- `false_positive_rate_on_no_failure`: no-failure / nominal episodes 中误报比例；pilot target `<= 0.05`。
- `failure_kind_accuracy`: 只用 evaluation labels 计算，不进入 runtime decision。
- `diagnosis_to_action_agreement`: 诊断 family 与 selected recovery action 的一致性，用于 debugging，不作主 claim。

### 3.9 Statistics

- 每个 family/cell 报告 point estimate + 95% CI；final 用 hierarchical / clustered bootstrap，至少按 policy training seed、scenario seed 或 base snapshot 聚类。
- 多指标/多 cell 的主结论使用 Holm correction 或预注册 family-wise grouping。
- Negative control 使用 equivalence / TOST 风格：CI 必须落入 `[-SEI, +SEI]` 才能写“无实质收益”。
- 所有表格同时报告 policy-only outcome、full-stack-with-fallback outcome、fallback invocation rate 和 safety override rate。

## 4. Revised experiments

### L0: No-failure and controller sanity

- 目的：确认 controller/native route、RuntimeManager、SafetySupervisor、EDP writer 在 nominal episodes 中可运行。
- 指标：`episode_validity_rate`, `task_success_rate`, `false_positive_rate_on_no_failure`, `decision_latency_s`。
- 通过标准：validity `>= 0.95`，no-failure false positive `<= 0.05`。

### L1: Failure calibration

- 目的：冻结 failure cell 和 severity，避免看结果后挑场景。
- 设计：每个候选 cell 先用 3 个 severity x dev seeds；选 controller-native non-saturated 区间。
- 指标：controller-native success 30-70%、trigger reproducibility、state-aliasing diagnostic、EDP completeness。

### L2: Baseline ladder

- 目的：建立强 baseline，不让 memory claim 打弱对手。
- 必跑：`controller_native`, `safety_only_monitor`, `rule_recovery_tuned`, `instant_mlp`, `frame_stack_raw_history`, `GRU_raw_history`, `typed_event_body_memory`, `oracle_upper_bound`。
- SHOULD：`causal_transformer_raw_history`；如果不跑，需要在 R025 summary 写 deferred reason。
- 指标：primary/safety/efficiency/navigation 全指标；per-family breakdown。

### L3: Memory content intervention

- 目的：证明收益来自 memory content，而不只是 policy 容量或训练差异。
- 设计：同一 typed-memory policy 跑 correct/null/masked/shuffled/stale memory；训练时必须有 memory dropout 或 `memory_available` mask。
- 指标：memory-content paired gain、decision flip、flip-conditioned gain、staleness curve。

### L4: Snapshot branch or matched-seed diagnostic

- 目的：在 R018 完成后做真正 branch-level action outcome comparison；未完成时保持 paired matched-seed diagnostic。
- 指标：branch outcome difference / action-value regret / unsafe difference；未完成 R018 时不写 ATE。

### L5: Robustness and OOD

- 目的：对齐 humanoid/legged navigation 文献中的 robustness practice。
- 设计：held-out layout、unseen target event、dynamic goal change、sensor degradation、perturbation intensity sweep。
- 指标：success/latency/safety + OOD gap、path efficiency、tracking error integral。

### L6: VLM/monitor appendix

- 目的：回答 RACER/FLARE/Code-as-Monitor 方向 reviewer concern。
- 设计：`VLM_prompt_supervisor` 和 monitor-only baseline 在相同 8-action space、相同 legal summaries、相同 seeds 上比较。
- 指标：success、latency、invalid action、cost、detection F1、false positive。
- 通过标准：VLM 不能读 privileged MuJoCo truth；如果 VLM 全面更强，论文主线 pivot 到 VLM baseline comparison。

## 5. Baseline 设计更新

| Baseline | Priority | 角色 | 必须公平控制的条件 |
|----------|----------|------|--------------------|
| `controller_native` | MUST | 外部下界，评估 failure cell 难度 | 相同 robot profile、controller checkpoint、scenario seeds |
| `safety_only_monitor` | MUST | 检查收益是否只是安全 monitor/fallback | 只能使用 runtime-legal summaries；不训练 memory policy |
| `rule_recovery_tuned` | MUST | deployable heuristic/fallback | 不能用 privileged signals；必须认真调参 |
| `instant_mlp` | MUST | 当前状态 learned lower bound | 同 action set、reward、training seeds |
| `frame_stack_raw_history` | MUST | ordinary raw-history baseline | 同 budget、同合法 observation，history window 预注册 |
| `GRU_raw_history` | MUST | 主文 history baseline | 同 budget、同 action set；优先级高于 VLM |
| `causal_transformer_raw_history` | SHOULD | 强 history model stress test | 不跑则 R025 必须写 deferred reason |
| `typed_event_body_memory` | MUST | 本方法 | 与 raw-history baseline 同训练数据/预算 |
| `typed_event_body_memory_no_body` / `event_only` / `body_only` | MUST after B3 | 输入消融 | 只改变 memory source，不改变 controller/planner |
| `VLM_prompt_supervisor` | SHOULD after core gates | 近邻 language recovery baseline | 只读 legal summaries，报告 latency/cost/invalid action |
| `oracle_upper_bound` | MUST for evaluation | 上界/diagnostic | evaluation-only privileged；不能进入 runtime decision |

## 6. 对现有计划的具体改动

- B1 增加 detection false positive / time-to-detect / failure-kind accuracy 的 evaluation-only 指标。
- B2 新增 R028 `safety_only_monitor` 和 R029 `causal_transformer_raw_history`。
- B3 明确 primary endpoint 使用 `valid_recovery_success_rate`，同时报告 policy-only、full-stack-with-fallback、fallback invocation 和 safety override。
- B4/R047 统计冻结必须纳入 `intervention_required_rate`、`unsafe_completion_rate`、`failure_detection_f1` 和 `path_efficiency`。
- B5 的 VLM baseline 仍然在 core gates 后运行；但 R025 summary 必须说明是否因为 RACER/FLARE-like reviewer concern 需要提前排期。
- R071 正式 citation verification 仍 TODO；本文不替代论文 BibTeX/venue/DOI 精读。

## 7. 立刻可执行的下一步

- [ ] 在 A800 上跑 L0 no-failure sanity，确认 no-failure false positive 和 EDP validity。
- [ ] 用 B1 dev seeds 做 severity calibration，筛出 controller-native 30-70% 的 positive memory cells。
- [ ] 先实现 `safety_only_monitor` baseline scaffold，复用 `SafetySupervisor` 和 typed high-level actions。
- [ ] 在 R025 baseline summary 模板中加入文献驱动指标列：safety、intervention、latency、path efficiency、detection。
- [ ] 在 R047 final 统计冻结前，依据 B1/B2 pilot 结果把 `SEI=0.05` 保留或调整，并记录理由。

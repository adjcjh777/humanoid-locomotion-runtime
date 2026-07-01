# Bounded Self-Improvement Extension

这份文档是 `docs/research_plan_prd.md` 和 `refine-logs/EXPERIMENT_PLAN.md` 的扩展说明。它不替换现有主线，而是把现有的 **typed body/event memory + high-level recovery selector + EDP/snapshot diagnostics** 升级成一个有边界、可验证、可回滚的 self-improvement loop。

目标是支持一个更强但仍然克制的研究叙事：

> humanoid runtime 从实际失败、障碍、身体退化和恢复结果中形成 typed memory，在 episode 间提出高层 command / recovery decision 的候选改进，并且只有通过 seeded validation、negative-control 和 safety gates 后才晋升到下一版 runtime policy。

本文中的 self-improvement 是 **bounded RSI-like runtime adaptation**，不是强 RSI，不是自动重写底层模型，也不是让 LLM 在实时安全闭环里直接控制机器人。

---

## 0. 与当前 main 主线的关系

当前 main 主线仍然成立：

- 底层 locomotion controller 保持冻结；
- learned component 只做低频、高层、typed recovery decision；
- `RuntimeManager` 和 `SafetySupervisor` 保留 non-learned hard stop / override path；
- 每个 episode 写 EDP；
- 论文主姿态是 memory intervention diagnostic，而不是端到端 humanoid VLA 或强 self-improving agent。

本扩展新增的是 **episode 间改进闭环**：

```text
Execute
  -> Observe
  -> Consolidate Memory
  -> Propose Candidate Update
  -> Validate by branch / matched seeds
  -> Promote or Roll Back
  -> Execute next policy version
```

因此，原问题：

```text
body/event memory 什么时候改变 high-level recovery decision？
这种改变是否真的改善 recovery outcome？
```

扩展为：

```text
runtime 能否把重复出现的障碍、任务失败和身体退化记录，
安全地转化为下一轮高层 command / recovery policy 的改进，
并降低 repeated failure，而不增加 unsafe behavior？
```

---

## 1. 明确不做什么

为了避免 scope 爆炸，本项目的 self-improvement 边界必须写死。

### 1.1 V0 不做

- 不自动修改底层 locomotion controller checkpoint；
- 不在实时闭环中让 LLM 生成 joint command；
- 不让 LLM 直接绕过 `RuntimeManager`、`SafetySupervisor` 或 option contract；
- 不做 autonomous code deployment 到真机；
- 不声称 strong RSI / recursive successor design；
- 不把 29DoF reference backend 结果冒充为 company G1 edu 23DoF 证据；
- 不把 persistent full 3D semantic memory 当作 V0 主证据；
- 不在 controller freeze 前写 high-level supervisor 的最终实验结论。

### 1.2 V0 允许做

- 从 EDP 中抽取 typed failure memory；
- 对 repeated obstacle、target loss、tracking degradation、balance risk、localization drift、recovery outcome 做 episode 间 consolidation；
- 生成候选的高层 recovery / command decision update；
- 用 snapshot branching 或 paired matched seeds 验证候选 update；
- 在 simulation / benchmark 中做 gated promotion；
- 对 promoted update 生成 manifest、version、rollback artifact 和 evaluation report。

---

## 2. Self-Improvement Loop

### 2.1 Execute

执行 language-conditioned local locomotion task。runtime 输入应是 structured locomotion command，例如：

```json
{
  "task_id": "walk_to_target",
  "target_ref": "red_chair_01",
  "speed_hint": "slow",
  "safety_mode": "normal"
}
```

底层 controller 仍然只接受 typed locomotion skill / velocity / walk-to style command，不接受自由形式策略修改。

### 2.2 Observe

执行过程中，runtime 必须记录：

- target grounding evidence；
- obstacle / blockage evidence；
- velocity tracking error；
- roll / pitch / balance risk；
- contact / slip / support state；
- controller confidence；
- localization drift；
- selected recovery action；
- recovery latency；
- final outcome；
- failure cause and temporal profile。

这些进入 EDP，而不是只进入临时日志。

### 2.3 Consolidate

episode 后，把 raw event trace 压缩成 typed memory。Consolidation 不应直接改 policy，只产生可审计 memory record。

输出包括：

```text
object memory
body memory
event memory
strategy memory candidate
```

### 2.4 Propose

根据 consolidated memory 生成候选 update。候选 update 可以来自：

- deterministic rule synthesizer；
- trained memory-conditioned selector；
- LLM-assisted offline proposer；
- human-authored patch；
- hybrid proposer。

但无论来源是什么，候选 update 都必须被表示成 typed manifest，不允许以自然语言解释直接生效。

### 2.5 Validate

候选 update 必须通过 fixed seed split、held-out failure cells、negative-control cells 和 safety regression。

优先验证方式：

```text
snapshot branching > matched-seed paired diagnostic > aggregate replay diagnostic
```

如果 snapshot branching 未完成，文档和论文中不得使用 counterfactual / ATE / branch oracle 等因果措辞。

### 2.6 Promote

只有当 validation report 满足 Gate SI 时，候选 update 才能晋升为下一版 runtime policy。

Promotion 必须写出：

```text
strategy_memory_version
candidate_update_manifest
validation_report
safety_report
rollback_pointer
policy_registry_entry
```

### 2.7 Roll Back

出现以下任一情况必须 rollback：

- unsafe completion 增加；
- fall / collision / hard stop 增加；
- negative-control cell 显著变差或被错误优化；
- progress 被过度保守策略牺牲；
- update 依赖 privileged / oracle-only 信息；
- validation 无法复现；
- EDP validator 不通过。

---

## 3. Memory 类型

### 3.1 Object Memory

记录目标和障碍相关证据。

```json
{
  "memory_type": "object",
  "object_id": "obstacle_17",
  "object_class": "dynamic_obstacle",
  "evidence": ["detector_like_box", "depth_cluster"],
  "relative_pose": {"x": 1.2, "y": -0.3, "yaw": 0.0},
  "last_seen_step": 184,
  "confidence": 0.82
}
```

V0 中 object memory 可以是 temporary / episode-level，不要求全局长期地图。

### 3.2 Body Memory

记录身体状态趋势，而不是单帧状态。

```json
{
  "memory_type": "body",
  "window_steps": 50,
  "tracking_error_trend": "increasing",
  "balance_risk_trend": "increasing",
  "slip_events": 2,
  "controller_confidence_mean": 0.61,
  "controller_confidence_slope": -0.08,
  "support_state_summary": "unstable_left_support"
}
```

### 3.3 Event Memory

记录 failure 和 recovery 尝试。

```json
{
  "memory_type": "event",
  "failure_id": "fail_00042",
  "cause": "velocity_tracking_degradation",
  "temporal_profile": "cumulative",
  "context": {
    "command": {"vx": 0.45, "vy": 0.0, "yaw_rate": 0.25},
    "target_distance": 2.1,
    "terrain_tag": "flat"
  },
  "selected_recovery": "slow_down",
  "outcome": "recovered",
  "recovery_latency_s": 1.4
}
```

### 3.4 Strategy Memory

Strategy memory 是本扩展的新增核心。它不是 raw trace，而是从历史失败中归纳出来、可验证、可晋升或回滚的策略性经验。

```json
{
  "memory_type": "strategy",
  "strategy_id": "strat_20260701_001",
  "source_failures": ["fail_00042", "fail_00057", "fail_00088"],
  "trigger": {
    "cause": "velocity_tracking_degradation",
    "temporal_profile": "cumulative",
    "tracking_error_slope_min": 0.12,
    "controller_confidence_max": 0.7
  },
  "recommended_update": {
    "kind": "recovery_priority_override",
    "prefer": "slow_down",
    "avoid": "continue",
    "max_vx": 0.25
  },
  "status": "candidate",
  "validation_status": "pending"
}
```

只有 strategy memory 经过 Gate SI 后，才能影响下一个 policy/runtime version。

---

## 4. Candidate Update 类型

V0 只允许修改高层 decision，不允许修改低层 controller。

### 4.1 Recovery Priority Update

改变 recovery action 排序或触发阈值。

例子：

```text
当 tracking error 持续上升且 controller confidence 下降时，
把 slow_down 的优先级提高到 continue 之前。
```

### 4.2 Command Parameter Update

改变高层 command 参数，但仍通过 typed command contract。

例子：

```text
在 recurrent lateral drift cell 中，
把 vx cap 从 0.45 m/s 降到 0.30 m/s，
并限制 yaw_rate 与 vx 同时过大。
```

### 4.3 Planner Cost Update

调整局部 planner cost，而不是直接控制关节。

例子：

```text
对曾经导致 blockage 的 obstacle class 增加 clearance cost。
```

### 4.4 Grounding Retry Update

改变 target loss 或 grounding uncertainty 时的恢复顺序。

例子：

```text
当 target evidence 连续 N 帧低于阈值，
先 refresh_target_grounding，若失败再 safe_stop。
```

### 4.5 Abort / Safe-Stop Policy Update

改变 abort 或 safe_stop 的保守程度。

例子：

```text
在 repeated fall-risk near-boundary cells 中，
提前 safe_stop，而不是尝试 local_replan。
```

---

## 5. Candidate Update Manifest

所有候选 update 必须以 manifest 表示。

```json
{
  "schema_version": "candidate_update_manifest_v0",
  "candidate_id": "cand_20260701_001",
  "parent_policy_version": "runtime_policy_v0.3.1",
  "source_edp_ids": ["edp_00042", "edp_00057"],
  "source_strategy_memory_ids": ["strat_20260701_001"],
  "update_kind": "recovery_priority_update",
  "allowed_scope": "high_level_recovery_selector_only",
  "forbidden_scope": [
    "low_level_controller_checkpoint",
    "joint_action_output",
    "SafetySupervisor_override",
    "hard_stop_path"
  ],
  "trigger_condition": {
    "cause": "velocity_tracking_degradation",
    "temporal_profile": "cumulative",
    "tracking_error_slope_min": 0.12,
    "controller_confidence_max": 0.7
  },
  "proposed_behavior": {
    "prefer": "slow_down",
    "avoid": "continue",
    "vx_cap": 0.25
  },
  "validation_plan": {
    "memory_positive_cells": ["tracking_cumulative_medium", "tracking_cumulative_high"],
    "negative_control_cells": ["transient_target_loss_low", "user_interrupt_control"],
    "seed_split": "gate_si_v0_heldout",
    "method": "snapshot_branching_or_matched_seed"
  },
  "status": "candidate"
}
```

---

## 6. Gate SI: Self-Improvement Promotion Gate

Gate SI 是本扩展的硬 gate。它决定某个 candidate update 能否从 candidate 晋升为 promoted strategy。

### 6.1 前置条件

进入 Gate SI 前必须满足：

- [ ] controller backend 已 frozen，或当前实验明确标注为 fallback/backend-neutral scaffold；
- [ ] Gate D failure protocol 已 freeze；
- [ ] baseline ladder 至少包含 controller-native / tuned rule / instant MLP / frame-stack / GRU / typed memory；
- [ ] EDP validator 能通过；
- [ ] candidate update manifest 已生成；
- [ ] candidate 不包含 oracle-only / privileged runtime feature；
- [ ] candidate 不修改 low-level controller 或 hard stop path。

### 6.2 输入

```text
EDP set
failure memory set
strategy memory candidates
candidate update manifest
frozen controller provenance
fixed seed split
negative-control cell list
safety metric definitions
```

### 6.3 输出

```text
gate_si_validation_report.json
gate_si_safety_report.json
strategy_memory_registry.json
runtime_policy_registry.json
rollback_manifest.json
verdict.txt
```

`verdict.txt` 只能是：

```text
PROMOTE
REJECT
NEEDS_MORE_EVIDENCE
ROLLBACK_REQUIRED
DEFER_UNTIL_SNAPSHOT_BRANCHING
```

### 6.4 通过标准

建议初始阈值如下。后续可以在预注册文档中改，但不能在看到结果后临时放宽。

| 类别 | 指标 | PASS 线 |
|------|------|---------|
| Memory-positive gain | recovery success | 相对 parent policy 提升 >= 5 percentage points，或 paired branch/matched-seed 下 win-rate >= 55% |
| Repeated failure | repeated same-cause failure rate | 下降 >= 10% |
| Safety | fall / collision / hard stop | 不得高于 parent policy；若样本小，必须在 safety report 中标注不确定性 |
| Unsafe completion | unsafe completion rate | 不增加 |
| Negative-control | negative-control effect | 等价区间内，建议 +/-3 percentage points |
| Over-conservatism | abort / safe_stop overuse | 不得导致 task progress 明显下降；progress drop 建议 <= 3 percentage points |
| Memory specificity | shuffled / stale memory | 不应复制 promoted gain |
| Reproducibility | held-out seeds | 至少一个 held-out split 通过 |
| EDP integrity | validator | 100% pass |

### 6.5 失败解释

Gate SI 失败时，必须把失败归因写进 report：

```text
insufficient_gain
safety_regression
negative_control_leakage
over_conservative_policy
not_memory_specific
snapshot_unavailable
controller_not_frozen
edp_invalid
oracle_leakage
```

---

## 7. 实验设计

### 7.1 对照组

Gate SI 至少需要这些对照：

1. Parent runtime policy；
2. No-memory selector；
3. Raw frame-stack selector；
4. GRU raw-history selector；
5. Typed event/body memory selector；
6. Candidate self-improved selector；
7. Shuffled-memory candidate；
8. Stale-memory candidate；
9. Tuned heuristic update；
10. Evaluation-only oracle upper bound。

### 7.2 Memory-positive cells

预期应该受益的场景：

```text
recurrent obstacle blockage
cumulative velocity tracking degradation
progressive balance risk
repeated target loss under similar context
localization drift with repeated bad recovery
```

### 7.3 Negative-control cells

预期不应该受益的场景：

```text
single transient perception glitch
user_interrupt / user command change
random one-step noise spike
failure cells where memory is irrelevant by construction
```

### 7.4 主要指标

```text
recovery_success_rate
task_success_rate
repeated_failure_rate
unsafe_completion_rate
fall_rate
collision_rate
hard_stop_rate
safe_stop_latency
recovery_latency
decision_flip_rate
progress_efficiency
rollback_rate
negative_control_effect
shuffled_memory_gap
stale_memory_gap
```

### 7.5 统计口径

- 若 snapshot branching 可用，报告 branch-level paired comparison；
- 若 snapshot branching 不可用，报告 paired matched-seed diagnostic；
- 使用 fixed seed split；
- 使用 cluster bootstrap 或 paired bootstrap；
- 多个 failure cells 同时比较时，需要 multiplicity control；
- 在 snapshot branching 未完成前，不写 causal ATE claim。

---

## 8. 论文 claim 增量

本扩展新增一个可选 claim：

```text
C4: Bounded self-improvement
A humanoid locomotion runtime can consolidate typed failure memory into gated high-level recovery/command updates that reduce repeated failures without increasing unsafe behavior.
```

C4 不能替代原 C1-C3。推荐论文叙事顺序：

1. C1: memory-value diagnostic；
2. C2: seeded typed failure protocol；
3. C3: typed memory representation beats ordinary history under matched budgets；
4. C4: gated self-improvement reduces repeated failures after validation。

如果 C4 证据不足，仍可把 C4 降级为 appendix / system extension，不影响 C1-C3 主线。

---

## 9. V0 / V1 / V2 分层

### V0

- typed body/event memory；
- post-episode memory consolidation；
- candidate high-level recovery / command update；
- Gate SI validation；
- promoted strategy memory registry；
- rollback manifest；
- simulation-only evidence。

### V1

- persistent spatial-semantic obstacle memory；
- parameterized recovery actions；
- broader command adaptation；
- long-horizon task retry policy；
- richer dashboard inspection of memory evolution；
- optional human approval UI for promotion。

### V2

- learned planner adaptation；
- skill library growth；
- multi-embodiment validation；
- sim-to-real evidence；
- hardware safety case；
- multi-agent offline evaluator / proposer / auditor split。

---

## 10. Implementation Worklist

### SI-0: Documentation and schema lock

- [ ] Add this document to tracker evidence.
- [ ] Add `strategy_memory` schema.
- [ ] Add `candidate_update_manifest` schema.
- [ ] Add `promotion_report` schema.
- [ ] Add `rollback_manifest` schema.
- [ ] Add tests proving candidate update cannot modify low-level controller fields.

### SI-1: EDP extension

- [ ] Add controller provenance to EDP.
- [ ] Add memory consolidation artifacts to EDP.
- [ ] Add candidate update references to EDP.
- [ ] Add EDP validator checks for oracle leakage and forbidden fields.

### SI-2: Offline memory consolidation

- [ ] Implement deterministic summarizer from event traces to typed failure memory.
- [ ] Implement strategy memory candidate generation from repeated failure clusters.
- [ ] Add unit tests with synthetic repeated failure traces.

### SI-3: Candidate proposer

- [ ] Implement rule-based candidate proposer.
- [ ] Optionally add LLM-assisted proposer, but keep output constrained to manifest schema.
- [ ] Add tests that invalid natural-language-only proposals are rejected.

### SI-4: Validation runner

- [ ] Implement Gate SI validation runner.
- [ ] Support snapshot branching when available.
- [ ] Support paired matched-seed fallback when snapshot branching is unavailable.
- [ ] Generate safety, negative-control and memory-specificity reports.

### SI-5: Promotion registry

- [ ] Implement runtime policy registry.
- [ ] Implement strategy memory registry.
- [ ] Implement rollback manifest.
- [ ] Add CLI to list parent/promoted/rolled-back policies.

### SI-6: Dashboard / replay

- [ ] Show strategy memory candidates.
- [ ] Show candidate validation result.
- [ ] Show promoted vs rejected updates.
- [ ] Show rollback reason.

---

## 11. ARIS / Codex execution rules

Codex/ARIS 可以生成代码和实验脚本，但必须遵守：

- 不得把 self-improvement 写成 low-level controller training；
- 不得在 Gate SI 前修改 runtime default policy；
- 不得因为某个 candidate 指标差一点就放宽阈值；
- 不得用 training reward 代替 held-out validation；
- 不得用 oracle-only feature 做 runtime input；
- 不得把 shuffled/stale memory 同样有效的结果解释为 memory 有用；
- 不得在 EDP validator 失败时标记 promote；
- 不得在 safety regression 时 promote；
- 不得把 fallback backend 结果写成 company G1 edu 23DoF evidence。

每次 self-improvement 试验必须输出：

```text
runs/self_improvement/<run_id>/
├── manifest.json
├── parent_policy_card.json
├── memory_consolidation_report.json
├── candidate_update_manifest.json
├── validation_report.json
├── safety_report.json
├── negative_control_report.json
├── memory_specificity_report.json
├── rollback_manifest.json
└── verdict.txt
```

---

## 12. 推荐论文题目方向

保守标题：

```text
Failure-Memory-Gated Recovery Policy Improvement for Language-Conditioned Humanoid Locomotion
```

更强系统标题：

```text
Bounded Self-Improvement for Humanoid Locomotion Runtime via Typed Failure Memory
```

一句话贡献：

> We study a bounded self-improvement loop for humanoid locomotion runtime: typed failure memory is consolidated into candidate high-level recovery/command updates, then promoted only after branch or matched-seed validation, negative-control checks, and safety regression gates.

中文版本：

> 我们研究一个有边界的人形机器人运行时自改进闭环：系统把 typed failure memory 转化为候选高层恢复/命令策略更新，并且只有在分支或 matched-seed 验证、negative-control 和 safety regression gate 通过后才晋升。

---

## 13. 最小可交付版本

如果时间紧，最小可交付版本只做：

1. typed failure memory；
2. strategy memory candidate；
3. rule-based candidate proposer；
4. paired matched-seed validation；
5. Gate SI report；
6. promoted / rejected / rollback registry；
7. two memory-positive cells + one negative-control cell。

这已经足够把现有 memory diagnostic 主线扩展成 bounded self-improvement 叙事，而不需要冒险进入强 RSI 或底层 controller 自动训练。

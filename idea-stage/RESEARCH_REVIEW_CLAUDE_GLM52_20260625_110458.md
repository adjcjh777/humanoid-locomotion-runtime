# Claude Code Research Review: GLM 5.2 Max Effort

> 归档读法：这是 2026-06-25 早期 research review 快照，保留原始评审意见。日常阅读请优先看已补充白话读法的最新副本 `idea-stage/RESEARCH_REVIEW_CLAUDE_GLM52.md`，以及对应 timestamp copy `idea-stage/RESEARCH_REVIEW_CLAUDE_GLM52_20260626_123900.md`。

**生成时间**：2026-06-25 11:04 +0800  
**使用 skill**：`research-review`  
**Reviewer command**：`claude -p --model 'glm-5.2[1M]' --effort max --permission-mode dontAsk --tools ""`  
**Context**：`docs/research_plan_prd.md` 摘要 + 20 篇相邻文献图谱  

## 一句话 Verdict

没有人做过完全一样的组合（冻结 humanoid locomotion controller + 监督式 RL recovery selector + body-memory conditioning + typed discrete recovery actions + seeded failure benchmark），但三条结构主轴都已有强先例：RACER 的 supervisor-actor recovery、HoRD 的 history-conditioned humanoid RL、LookOut 的 humanoid nav slowing/rerouting。这个组合的 novelty 是“重新打包”级别，而非“新机制”级别，除非 body-memory ablation 给出非平凡、可预注册的洞察，否则顶会审稿人会判定为 incremental。

## Scores

| 维度 | 分数 | 说明 |
|---|---:|---|
| Novelty | 4/10 | 组合新，单点不新。supervisor-actor recovery、history-conditioned humanoid RL、event memory、humanoid nav slowing/rerouting 都已有强先例。 |
| Impact | 5/10 | 可复现 humanoid locomotion recovery benchmark 有社区价值，但 impact 押在 body-memory ablation 上。 |
| Feasibility | 6/10 | 工程可行，但 reward、failure seeding、event memory 信号仍不清楚。 |
| Clarity | 6/10 | scope/non-goals 清楚，但 reward、成功判据、selector 频率、action 设计依据、oracle 定义缺失。 |

## 最近邻 Prior Work

| Paper | 重叠点 | 关键差异 | 威胁等级 |
|---|---|---|---|
| RACER | supervisor-actor 架构、language-guided failure recovery、recovery trajectory/action 选择 | manipulation 非 locomotion；VLM supervisor 非 RL；连续 recovery trajectory 非 typed discrete actions | HIGH |
| HoRD | history-conditioned RL for humanoid robustness、domain shift 下的人形鲁棒性 | 低层 controller 上的 history conditioning；非冻结低层 + 上层 recovery | HIGH |
| LookOut | humanoid nav 中 slowing/rerouting/looking around | trajectory/head-pose 预测；非 action selector；无 body-memory framing | MED-HIGH |
| Chameleon | event memory 提升 delayed-decision task | manipulation；prospective/control-indexed memory；非 recovery selector | MED |
| FLARE | VLA Retry/Reset recovery，offline MLLM + online monitor | manipulation；MLLM monitor 非 RL selector | MED |
| Automating Robot Failure Recovery | VLM 做 motion/task 级 recovery | manipulation；VLM 非 RL；无人形 | MED |
| STATE-NAV | stability-aware bipedal navigation | traversability + MPC；非 recovery selector | LOW-MED |
| FocusNav | G1 local navigation + stability-aware gating | nav gating；无 body memory；无 failure family | LOW-MED |
| EgoActor | VLM 到 locomotion/manipulation primitives | VLM 非 RL；非 recovery-focused | LOW-MED |

## 最强拒稿理由

1. **Novelty 薄，覆盖于 RACER + HoRD + LookOut 之上。** 三篇已覆盖 supervisor-actor recovery、history-conditioned humanoid RL、humanoid nav slowing/rerouting。若无非平凡实证洞察，会被判定为 re-bundle。
2. **RL-vs-VLM supervisor 选择未 justify。** RACER/FLARE/Automating-Recovery 都用 VLM/LLM supervisor。PRD 选择 RL 但未解释为什么，也没有 VLM supervisor baseline。
3. **Body-memory ablation 可能 collapse。** Instant state 可能已经主导 recovery selection；若 full body memory 只边际提升，主贡献失败。
4. **Reward 与 success 判据未指定。** Recovery selector 的 reward 和每类 failure 的 crisp success criterion 是 load-bearing。
5. **Failure-family seeding 可复现性存疑。** localization drift / balance risk 需要 deterministic injection protocol。
6. **Language-conditioned 可能是装饰。** 如果 selector 不消费 language delta 或 target text，标题过强。
7. **Oracle upper bound 不应 optional。** 无 oracle 就无法判断 learned selector 的绝对空间。

## 修改建议

1. **Per-family 预注册 body-memory 假设**：明确哪些 family 应受益于 event/window memory，哪些是 reactive。最小实验：逐 family 比较 instant/window/full。
2. **加 VLM-supervisor baseline**：让 GPT/Claude 读 body-memory 文本摘要，输出同一 8-action set。最小实验：VLM-supervisor vs RL-selector。
3. **Oracle upper bound 改 mandatory**：oracle 拥有 true failure type + per-type 最优 action。最小实验：oracle vs full RL，报 gap。
4. **Crisp 指定 reward**：例如 `-1/step until recovery + fall penalty + target-reach bonus`，并定义 recovery success。
5. **Failure-family seeding 写成协议**：明确 obstacle spawn、state estimator bias、velocity scaling、CoM impulse、target change。
6. **Justify 或收缩 8 个 typed actions**：测试 8-action vs 合并后的 5-action set。
7. **让语言进入 selector 或从标题去掉**：target-change family 做 language-aware vs language-blind ablation。
8. **加跨控制器迁移测试**：在 controller A 训练 selector，在 controller B 测试。

## 最终建议

**Proceed with caution.**

必须达成的 gate：

- **Gate 1（RL 训练前）**：per-family body-memory 假设 + reward 定义 + seeding protocol + oracle definition 全部写定。
- **Gate 2（pilot 后）**：VLM-supervisor baseline 在至少 3/5 family 上弱于 RL-selector，或 pivot 到 VLM-supervisor 框架。
- **Gate 3（投稿前）**：`rl_full_body_memory` 在预注册应受益 family 上以预注册 margin 超过 `rl_instant_state`；oracle gap 已报告。

Gate 3 失败则无 method 贡献，应 abandon 或转 benchmark/protocol paper。

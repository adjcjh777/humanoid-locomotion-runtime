# RESEARCH_REVIEW: Humanoid Locomotion Runtime — Typed Supervisory Recovery Policy

> ARIS local rerun metadata: generated on 2026-06-25 11:58 CST with `claude-opus-4-8`. Filename is kept for compatibility with the existing ARIS manifest naming, but this run used Claude Opus 4.8 rather than GLM 5.2.

## 白话读法

这份外部评审视角的结论是：项目可以做，但必须 pivot 成“诊断性论文”，不要写成“我们发明了一个新 supervisor”。

最关键的要求：

- memory 的收益必须和 instant state、event trace、ordinary history baseline 区分开。
- failure cells 必须在看结果前冻结，并且加入 transient negative-control。
- heuristic baseline 要认真调，不许当 strawman。
- 如果没有 snapshot branching，就不能写 counterfactual / ATE / branch oracle。
- 推荐路线是 RA-L / IROS / workshop 风格的实证论文，而不是 CoRL/ICLR main track method paper。

## 1. Overall assessment

可发表潜力：中等偏上，**前提是把论文重写成一篇"诊断性研究"而不是"方法贡献"**。当前计划的方法新颖度（5.5/10）撑不起 CoRL/CoRL-main 或 ICRA oral 级别的 method paper，但 I3（memory-value diagnostic）这条"记忆只在特定失败族中通过改变高层决策产生条件性收益"的 claim，如果用 matched-seed counterfactual 严格证出来，足以成为一篇扎实的 **RA-L / IROS / 或 CoRL-Workshop / NeurIPS Robot-Learning Workshop** 级别的实证论文。

目标 venue 分层建议：第一目标 RA-L（with IROS option），它对"frozen 低层 + 监督式高层 + 严谨消融"的实证工作友好，且不强求 method novelty；保底目标是 CoRL/NeurIPS workshop。**不要投 CoRL/ICLR main track 当 method paper**，会被近邻工作（RACER、Code-as-Monitor、HoRD）直接 kill。

主要理由：贡献的重心不在"我们提出一个 supervisor"，而在"我们用反事实实验回答了 memory 在 recovery 中到底何时、为何、有多大用"——这是一个 community 普遍假设但很少有人 negative-control 过的问题。

## 2. Strengths

- **诚实的条件性 claim 是真正的卖点。** 把"memory 普适有用"收窄为"仅在 long-horizon / cumulative / degradation failures 中有用"，这是 reviewer 会欣赏的科学态度，也天然包含 negative result，抗审稿。
- **Frozen 低层控制器是干净的实验设计选择**，把混杂因素压在高层决策层，让"决策翻转"成为可观测、可归因的因变量。这是反事实分析能成立的前提。
- **8-action 离散监督抽象便于分析**：决策空间小到可以做 per-action、per-failure 的混淆矩阵和翻转分析，而不是黑箱连续策略。这对 diagnostic paper 是优势（虽然如 Novelty Check 所说，它本身不是 novelty）。
- **I10 seeded typed failure-injection 提供可复现协议**，让 matched-seed counterfactual 在技术上可行——这是很多同类工作做不到、因而无法做因果归因的地方。

## 3. Weaknesses

### Fatal（不修就没有论文）

- **F1：memory 的收益与 instantaneous state / event trace 不可分离的风险。** 全文 claim 建立在"是 memory 改变了决策"。但输入里同时有 instant state、typed event trace、body-state trend memory、language context。如果决策翻转其实来自 event trace 或当前 state，论文核心就塌了。**修复：** 必做 leave-one-out 输入消融（去 memory / 去 trend / 去 event trace），且必须有 matched-seed 下的"同一时刻、唯一差异是 memory 内容"的反事实对，统计上证明 decision flip 由 memory 驱动。
- **F2：失败分类的循环论证风险。** 如果 long-horizon/cumulative/degradation 这三类失败是"挑选 memory 恰好擅长的场景"注入的，结论就是自证。**修复：** 失败类型必须在看实验结果前用可操作定义冻结（见 §4），并强制加入 **negative-control 失败族**（transient/instant 失败，理论上 memory 不该帮上忙），证明 memory 在那里**没有**收益。没有 negative control 的正收益不可信。

### Major

- **M1：heuristic baseline 可能直接打平监督策略。** 8 个动作 + typed event 很可能被一个写得好的规则系统覆盖。若 heuristic 在 cumulative failure 上也能赢，memory 价值无从谈起。**修复：** heuristic baseline 必须认真调优（不是 strawman），并明确展示它在哪一类失败上系统性失效。
- **M2：外部效度受限（单本体 G1、纯 sim）。** RA-L/IROS reviewer 会问泛化性。**修复：** 在不开真机的前提下，至少做跨 seed、跨地形/扰动幅度的鲁棒性扫描，并在 limitation 里坦诚 sim-only，把它定位为"诊断研究"而非"部署方案"。
- **M3：统计功效不足。** 失败 recovery 是高方差事件，少量 seed 会让 CI 跨 0。**修复：** 预先做 power analysis 估 seed 数；用 paired/matched-seed 检验、bootstrap CI、effect size（不只 p 值）、多重比较校正。
- **M4：supervisor 的监督信号来源未交代。** label 从哪来（oracle 规划器？人工？规则？）直接决定结论可信度，也可能引入泄漏。**修复：** 明确 supervisor 训练目标与标签生成流程，并排除标签泄漏失败类型信息。

### Minor

- abort_task / safe_stop / recover_balance 的语义边界与成功判据需在协议里定死，否则 per-action 分析没有 ground truth。
- language task context 的作用未量化——若它几乎不影响决策，应在消融里诚实标注，避免 reviewer 质疑其为装饰性输入。
- body-state trend memory 的窗口长度是一个隐藏超参，应作为 ablation 维度而非固定值。

## 4. Required experimental package

**Baselines（缺一不可）：**

1. Frozen-only（无监督层，下限）。
2. Heuristic supervisor（认真调优的规则版）。
3. No-memory supervisor（只用 instant state + event trace）。
4. VLM-prompt supervisor（近邻对照，证明轻量 memory 监督优于/不劣于 prompt 式判断）。
5. Oracle / privileged supervisor（上限，量化可改进空间）。

**Ablations：** 输入 leave-one-out（memory / trend / event trace / language 各去一）；memory horizon 长度扫描；trend vs event-trace 单独贡献分解。

**统计：** matched-seed counterfactual decision-flip 分析（核心）；paired bootstrap CI；effect size + 多重比较校正；预注册 seed 数与失败类型定义。

**失败类型：** transient/instant（negative control）、long-horizon、cumulative drift、sensor/localization degradation。每类给可操作触发与判据。

**表/图建议：**

- 图1：per-failure-type × policy 的 recovery 成功率柱状图带 CI（一眼看出条件性收益）。
- 图2：memory-value 曲线 vs horizon 长度。
- 表1：decision-flip 矩阵——matched-seed 下 memory 触发的动作翻转及其成功/失败归因。
- 表2：输入消融对各失败族的边际贡献。
- 图3：negative-control 失败族上 memory 收益≈0 的证据图（反向证明）。

## 5. Reframed paper story

**推荐标题：** *When Does Memory Help a Recovery Supervisor? A Counterfactual Diagnostic on a Frozen Humanoid Locomotion Stack*

**Contribution bullets：**

- 提出 seeded typed failure-injection 协议，使 frozen 低层栈上的高层 recovery 决策可被反事实归因。
- 通过 matched-seed counterfactual，**量化** typed event/body-state memory 对高层 recovery 决策的因果影响，而非相关性。
- 给出 negative-control 证据：memory 收益严格局限于 long-horizon/cumulative/degradation 失败族，在 transient 失败上无收益——澄清了 community 的过度泛化假设。

**不要写的 claim：** 不要声称"提出新 supervisor 架构"；不要把 8-action set 当 novelty；不要声称真机/多本体泛化；不要声称 memory 普适提升 recovery。

## 6. 4-week plan

- **Week 1 —— 协议与可证伪性冻结。** 产出：失败类型可操作定义（含 negative control）、matched-seed 注入管线、supervisor 标签来源文档、power analysis 定 seed 数。**Gate：** 能在不看结果前冻结失败分类，且反事实对能成对生成。
- **Week 2 —— baselines 全跑通。** 产出：5 个 baseline 在全失败族上的成功率 + CI。**Gate：** heuristic 在 cumulative failure 上**确实**系统性失效（否则立即 pivot，见 §7）。
- **Week 3 —— 反事实与消融。** 产出：decision-flip 矩阵、输入 leave-one-out、horizon 扫描。**Gate：** matched-seed 下 memory 驱动的 flip 在统计上显著，且 negative control 上收益不显著（双向都成立才算成功）。
- **Week 4 —— 收口与写作。** 产出：全部图表 + 论文 draft + limitation。**Gate：** 核心条件性 claim 有 CI 与 effect size 支撑，可投 RA-L。

## 7. Decision

**Major revision toward pivot（诊断性论文）。** 当前作为 method paper 不可接收；作为反事实诊断研究可行且为中低风险。

**最短下一步：** 立刻执行 Week 1 的两件事——(a) 在看任何结果前冻结失败类型定义并加入 transient negative-control 族；(b) 跑通 heuristic vs no-memory vs full-memory 在 cumulative failure 上的最小三方对比。如果 Week 2 gate 失败（heuristic 不输），则停掉 memory claim，转而把 I10 注入协议 + I3 诊断框架本身作为贡献重新立题。

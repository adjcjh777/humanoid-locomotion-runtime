# ARIS Research-Lit 报告：Typed Supervisory Recovery on Frozen Humanoid Locomotion

> ARIS local rerun metadata: generated on 2026-06-25 11:58 CST with `claude-opus-4-8`. Local `tools/arxiv_fetch.py` still returned HTTP 429, so Codex collected source candidates through web/project/arXiv pages and passed them into Claude. Claude did not browse directly; verification labels below should be treated as conservative and rechecked before formal citation.

> 归档读法：这是 2026-06-25 的文献摘要快照，保留原始候选文献和验证状态。日常阅读请优先看已补充白话读法的最新副本 `idea-stage/REF_PAPER_SUMMARY.md`，以及对应 timestamp copy `idea-stage/REF_PAPER_SUMMARY_20260626_123900.md`。

## 1. Executive Summary：5 个最危险的近邻

1. **RACER (2409.14674)** —— 最危险。它已经把"语言引导的失败恢复策略"做成了完整故事。我们若用"language-conditioned recovery"作主卖点会被直接对标。**差异化只能落在：典型化离散动作空间 + 在 frozen locomotion controller 之上，而非操作/IL 的连续纠正。**
2. **HoRD (history-conditioned humanoid RL)** —— 直接威胁我们"body memory 比 instant state 更有价值"的核心论点。如果 history-conditioning 在鲁棒人形控制上已被证明有效，我们的 insight 就从"发现"降级为"复现"。必须把 claim 收窄到 *supervisory 层* 的记忆价值，而非控制层。
3. **Chameleon / Control-Indexed Prospective Memory** —— 威胁"body/window memory"作为新机制的原创性。需要明确我们的 memory 是 *typed event/failure trace summary*，不是通用 prospective memory。
4. **HumanoidBench / HumanoidArena** —— 威胁"seeded failure benchmark"作为贡献点。若已有人形失败/鲁棒性基准，我们的基准必须以 *typed seeded failure + supervisory action 评测协议* 区分，否则只是子集。
5. **Code-as-Monitor (CVPR 2025) / Guardian-FailCoT / FLARE** —— 威胁"typed failure trace → 高层动作"这条闭环。它们已覆盖"检测失败→纠正"的框架叙事。我们的护城河是 *动作空间被严格约束为 8 个类型化算子*，可形式化、可审计。

## 2. Literature Table

| Work | Year/Venue | Status | Core idea | Threat to project | Action for PRD/exp |
|---|---|---|---|---|---|
| RACER | 2024, arXiv 2409.14674 | web_verified | 语言丰富注释驱动 IL 失败恢复 | 抢占"language recovery"叙事 | 强调离散 typed 动作 vs 连续纠正；引为主 baseline 思路 |
| Automating Robot Failure Recovery w/ VLMs | 2024, 2409.03966 | web_verified | VLM+优化 prompt 生成恢复 | 抢占"VLM 当 supervisor" | 对比：我们是学习策略非 prompt 工程，强调闭环延迟/可靠性 |
| FLARE | CVPR 2026 | web_verified | failure-aware 自主纠正框架 | 框架叙事重叠 | 引用需谨慎，定位为 manipulation 域 |
| HoRD | 2026, arXiv 2602.04412 | web_verified | history-conditioned RL + 在线蒸馏 | **直击 body-memory 论点** | claim 收到 supervisory 层；做 history vs no-history 消融区分 |
| Chameleon | 2026, arXiv 2603.24576 | web_verified | control-indexed prospective memory | 抢占记忆机制 | 明确 typed trace ≠ 通用记忆 |
| HumanoidBench | 2024 RSS, 2403.10506 | web_verified | 人形全身任务基准 | 基准重叠 | 复用 task 但加 seeded failure 协议 |
| MuJoCo Playground | 2025, 2502.08844 | web_verified | GPU 加速 MuJoCo 训练栈 | 无威胁，是工具 | 直接作为仿真/训练底座 |
| LocoMuJoCo | 2023, 2311.02496 | web_verified | 运动模仿/locomotion 基准 | 部分基准重叠 | 借其 metrics，对接 G1 |
| STATE-NAV | 2025/RA-L, 2506.01046 | web_verified | 状态感知人形导航 | supervisory 导航重叠 | 定位差异：我们管 recovery 非 navigation |
| FocusNav | 2026, 2601.12790 | web_verified | 聚焦式导航 | 边缘重叠 | 仅作相关工作 |
| LookOut | 2025 ICCV, 2508.14466 | web_verified | 预瞻性视觉导航 | 边缘 | 相关工作 |
| LangWBC | 2025, 2504.21738 | verify_pending | 语言条件全身控制 | 抢占 language-conditioned WBC | 强调我们 frozen 低层、只学 supervisor |
| LeVERB | 2025, 2506.13751 | verify_pending | latent 全身 VLA | VLA 路线对照 | 明确我们 *非* 端到端 VLA |
| HumanoidArena | 2026, 2606.17833 | verify_pending | 人形竞技/评测 | 基准重叠 | 抓取后再决定是否纳入 |
| RoboGhost | 2025, 2510.14952 | verify_pending | 语言/导航控制近邻待核实 | 不明 | 抓取后再定性 |
| WholeBodyVLA | 2025, 2512.11047 | verify_pending | 全身 VLA | VLA 对照 | 作"我们不做什么"的反例 |
| Guardian/FailCoT | 2025, 2512.01946 | verify_pending | 失败链式推理监控 | 监控闭环重叠 | 对比：我们输出受限动作非自由 CoT |
| Code-as-Monitor | 2025 CVPR | web_verified | 以代码约束做时空监控 | 监控/检测重叠 | 借鉴失败检测，区分动作层 |
| Unpacking Failure Modes of Generative Policies | 2025 CoRL | web_verified | 生成式策略失败模式分类 | 失败 taxonomy 重叠 | 直接用于设计 seeded failure 类型 |

## 3. Baseline / Benchmark 建议

**必须做：**

- **No-memory ablation**：instant proprioception-only supervisor vs full body-memory。这是论文成立的命门，否则无法回击 HoRD/Chameleon。
- **Frozen-only baseline**：低层 controller 单跑、无 supervisor，量化恢复率增量。
- **Heuristic supervisor**：规则触发 safe_stop/recover_balance，证明"学习"优于"if-else"。
- **VLM-prompt supervisor**（对标 2409.03966/RACER）：证明学习型 typed policy 在延迟与可靠性上的优势。

**可选：**

- 端到端 VLA（LeVERB/WholeBodyVLA 风格）对照——成本高，仅在 reviewer 质疑"为何不端到端"时需要。
- HumanoidBench 任务迁移——增强外部效度，但非核心。

理由：核心贡献是"typed supervisory recovery + memory 价值"，baseline 必须正面攻击这两点，而非堆任务。

## 4. Positioning

**可 claim（一句话）**：在冻结的成熟人形 locomotion controller 之上，学习一个类型化（8 算子）的语言条件 supervisory recovery 策略，并通过 seeded failure 基准刻画 *何时* body/event-trace memory 相对 instant state 带来恢复增益。

**不能 claim 的边界**：

- 不能宣称提出全新记忆机制（Chameleon/HoRD 在前）。
- 不能宣称端到端学习或低层 gait 改进——低层是冻结的。
- 不能宣称"首个失败恢复策略"——RACER 在前。
- 不能宣称真机泛化——仅 MuJoCo+G1 仿真。

## 5. Gaps & Open Risks

- **验证缺口仍在**：arXiv API 429 使自动化批量核验失败。虽然 Codex 已通过 web 搜索确认了 RACER、HoRD、Chameleon、HumanoidBench、MuJoCo Playground、LocoMuJoCo、STATE-NAV、FocusNav、LookOut、FLARE 等关键页面，若写正式论文仍要逐篇抓 PDF/DOI/BibTeX。
- **最致命未验证点**：HoRD 是否已实证 history-conditioning 对人形鲁棒恢复有效——直接决定我们论点是"新发现"还是"复现"。优先精读。
- **taxonomy 风险**：seeded failure 类型需对齐 CoRL2025 失败模式工作，否则基准可被批"非系统化"。
- **行动**：429 解除后，按 HoRD → Chameleon → HumanoidArena → FLARE 顺序坐实，再回填本表状态。

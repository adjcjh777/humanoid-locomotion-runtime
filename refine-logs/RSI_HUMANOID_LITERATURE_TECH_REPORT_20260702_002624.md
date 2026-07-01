# Recursive Self-Improvement 在 Humanoid Locomotion Runtime 上的边界化应用调研

**日期**：2026-07-01
**状态**：ARIS / Agent Bus 技术调研报告，作为 R050 文档证据。
**Agent Bus team**：`humanoid-rsi-literature-6e3749cf`
**适用范围**：本报告只支持 bounded self-improvement 研究路线，不放行 Gate SI promotion、controller self-modification、真机自部署或论文主结论。

## 1. Executive Summary

本项目不应把 RSI 写成 strong recursive self-improvement。更合适的主张是：

> humanoid runtime 在 episode 间把合法 runtime traces 压缩成 typed failure / body / event / strategy memory，再生成受 schema 约束的高层 recovery / command / planner / grounding / safe-stop 候选更新；候选更新必须通过 Gate SI 的 validation、negative-control、safety regression 和 rollback 检查后，才可能晋升为下一版高层 runtime policy。

最贴近本项目的组合不是“LLM 自改机器人”，而是：

- Reflexion 式的“无权重更新、用 episodic memory 改善后续决策”，但本项目必须把自由文本替换成 typed memory。
- RoboMemory / lifelong robot learning 式的长期经验组织，但 V0 只保留 failure/body/event/strategy memory，不把 full semantic 3D memory 作为主证据。
- ENPIRE / ADAS / AlphaEvolve / DGM 式的 agentic improvement harness，其中 ENPIRE 应作为主参考框架；但本项目只允许离线 proposer / evaluator / auditor，不允许进入实时 safety loop。
- Humanoid locomotion 文献里的 history-conditioned controller 可作为强 raw-history baseline 参照，但不能替代本项目的冻结底层 controller + 高层 recovery selector 设计。

当前结论是 **Gate SI: NO-GO for promotion**。可以继续做 SI-1 到 SI-5 的脚手架和验证器；不能声称已经实现 humanoid RSI。

## 2. 本次做了什么修改

- [x] 新增本报告，集中记录 RSI / self-evolving agents / robot self-improvement / humanoid recovery 文献到本项目的映射。
- [x] 新增文献候选 JSON，给后续 R071 citation verification 和 SI 设计审查提供机器可读入口。
- [x] 新增 Agent Bus 团队记录，保留 team id、子代理角色、Chrome 尝试状态和子代理结论。
- [x] 更新 tracker / plan / timeline，新增 R050，明确该项是文献和技术报告 evidence，不是 runtime 实验 evidence。
- [x] 更新 `MANIFEST.md`，把新增报告、JSON、team summary 和 timestamped copies 纳入 ARIS artifact 清单。

## 3. 为什么做这些修改

- 用户目标是“继续根据 `docs/bounded_self_improvement_extension.md` 做 RSI 结合当前项目探索，让机器人递归迭代自身行为的 memory 系统”。这需要先把“递归迭代”压到项目允许的边界内：episode 间、离线、typed manifest、Gate SI、rollback。
- `AGENTS.md` 要求科研阶段默认使用 ARIS 产物，而不是只用聊天总结；因此新增 `refine-logs/` 下的正式报告和 manifest 记录。
- 当前项目仍有 R007j、R018、B1/B2 baseline、SI-1 到 SI-5 等前置项未完成；因此报告必须把 claim 约束写清楚，避免把 SI-0 schema lock 误写成已运行的 self-improvement system。
- 子代理审查一致指出：可以做 bounded self-improvement / failure-memory-gated high-level recovery improvement；不能做 strong RSI、底层 controller 自改、LLM 实时控制或 privileged oracle 泄漏。

## 4. Agent Team Evidence

| Role | Thread | 状态 | 本报告采用的结论 |
|------|--------|------|------------------|
| literature-scout | `019f1e62-6fae-7653-be60-5e0d3fbcc190` | completed, read-only | 补充强 RSI foundational、LLM experiential learning、embodied self-evolution、RMA/HumanUP、SPIBB 等 17 条候选；用于扩展文献表和风险边界 |
| robotics-mapper | `019f1e62-a997-7ac3-ba85-a5ceb05bcb08` | completed, read-only | V0/V1/V2 路线：V0 offline strategy memory loop，V1 长期记忆和参数化恢复，V2 跨本体和实机安全案例 |
| safety-skeptic | `019f1e62-cc3b-7323-89f5-c604eb38cc29` | completed, read-only | Gate SI 当前 NO-GO；保留 runtime/evaluation 分离；禁止 strong RSI 和 controller self-modification claims |
| report-writer | pending | 未启动 | 当前由主代理合成报告，保留 team record |

Chrome 说明：按用户提示尝试使用 Chrome control。检查到 Chrome app、Codex Chrome Extension 和 native host manifest 存在，但 Codex browser runtime 当前未暴露可用 browser backend，`agent.browsers.list()` 返回空列表；本报告使用 web verification，不把 Chrome 作为证据来源。

## 5. 文献和技术报告表

| Work | Year / Venue | Verification | Core idea | 对本项目的用法 | 必须避免 |
|------|--------------|--------------|-----------|----------------|----------|
| [Reflexion](https://arxiv.org/abs/2303.11366) | 2023, arXiv / NeurIPS repo | verified via arXiv | 语言 agent 通过 verbal feedback 和 episodic memory 改善后续 trial，不更新权重 | 支持“memory-based self-improvement without weight updates”；V0 改成 typed strategy memory | 不把自由文本 reflection 直接作为 runtime policy |
| [RISE: Recursive Introspection](https://arxiv.org/abs/2407.18219) / [NeurIPS page](https://proceedings.neurips.cc/paper_files/paper/2024/hash/639d992f819c2b40387d4d5170b8ffd7-Abstract-Conference.html) | 2024, NeurIPS | verified via arXiv / proceedings | 训练 LLM 在多轮尝试中发现并修正错误 | 作为“递归修正”概念背景；可启发 offline proposer / auditor | 不进入机器人实时控制，不生成 joint command |
| [A Survey of Self-Evolving Agents](https://arxiv.org/abs/2507.21046) | 2025, arXiv | verified via arXiv | 从 what / when / how 组织 self-evolving agents，覆盖 model、memory、tools、architecture | 给本项目的分类：只 evolve 高层 strategy memory / selector config | 不承诺 ASI、强 RSI 或开放式自我重写 |
| [ADAS](https://arxiv.org/abs/2408.08435) / [OpenReview](https://openreview.net/forum?id=t9U3LW7JVX) | 2024/2025, ICLR | verified via arXiv / OpenReview | meta agent 在代码空间搜索更好的 agent design | 可作为离线 candidate proposer/evaluator 的远期模式 | 不允许自动部署代码到 runtime 或真机 |
| [Gödel Agent](https://aclanthology.org/2025.acl-long.1354/) | 2025, ACL | verified via ACL Anthology | LLM agent 动态修改自身逻辑和行为 | 作为 strong self-modification 对照和风险边界 | 不把本项目写成 recursive successor design |
| [Darwin Gödel Machine](https://arxiv.org/abs/2505.22954) | 2025, arXiv | verified via arXiv | coding agent 迭代修改自身代码并用 benchmark 验证 | 启发 archive + validation + rollback 思路 | 不把 coding benchmark 自改迁移成 robot runtime 自改 |
| [AlphaEvolve](https://arxiv.org/abs/2506.13131) | 2025, Google DeepMind white paper / arXiv | verified via arXiv | LLM + evaluator 的 evolutionary coding pipeline 改进算法 | 支持“verifiable evaluator 才能自改进”的技术路线 | 不让 algorithm code evolution 触碰 controller/safety path |
| [ENPIRE](https://arxiv.org/abs/2606.19980) / [NVIDIA page](https://research.nvidia.com/labs/gear/enpire/) | 2026, arXiv / NVIDIA GEAR technical report | verified via arXiv / NVIDIA lab page | EN / PI / R / E 四模块把真实机器人 reset、policy refinement、rollout evaluation 和 agent evolution 接成闭环；报告 99% real-world dexterous manipulation success，并提出 MRU / MTU 评估 robot fleet 与 token 使用效率 | 主参考：把 physical autoresearch harness 改写成本项目的 offline Gate SI harness；重点借鉴 reset/verify、parallel rollout、log/literature-driven improvement、agent team audit 和 utilization metrics | V0 不改底层 locomotion policy，不让 coding agent 自动改训练栈并部署到 runtime，不把 manipulation policy improvement 证据写成 humanoid recovery evidence |
| [RoboMemory](https://arxiv.org/abs/2508.01415) | 2025, arXiv | verified via arXiv | embodied multi-memory framework，含 spatial / temporal / episodic / semantic memory | 启发 memory 分层和长期经验管理 | V0 不把 full semantic world memory 当主贡献 |
| [Self-Improving Robots / MEDAL++](https://proceedings.mlr.press/v229/sharma23b.html) / [project](https://architsharma97.github.io/self-improving-robots/) | 2023, CoRL | verified via PMLR / project page | 通过 autonomous practice、forward/backward policies、demo-derived reward 改善 visuomotor policy | 机器人 self-improvement 近邻；强调 reset / practice / reward design | 它是 end-to-end manipulation policy，不等同于高层 locomotion recovery supervisor |
| [Real-world Humanoid Locomotion with RL](https://www.science.org/doi/10.1126/scirobotics.adi9579) / [arXiv](https://arxiv.org/abs/2303.03381) | 2024, Science Robotics | verified via Science / arXiv | causal transformer 用 proprioceptive observation-action history 做 in-context adaptation | 必须作为强 raw-history / history-conditioned locomotion baseline 参照 | 不把底层 history-conditioned controller 当作本项目的 memory SI |
| [FRASA](https://arxiv.org/abs/2410.08655) | 2024, arXiv | verified via arXiv | end-to-end DRL humanoid fall recovery / stand-up | recovery-specific comparator；帮助定义 recovery metrics | V0 不训练低层 fall-recovery controller 来替代 frozen gait |
| [Task-free Lifelong Robot Learning](https://arxiv.org/abs/2410.02995) | 2024, arXiv | verified via arXiv | task-free continual learning，检索历史数据做 local adaptation | 支持 memory retrieval / forgetting / local adaptation 讨论 | 不把 manipulation lifelong learning 直接当 locomotion evidence |
| [Gödel Machines](https://arxiv.org/abs/cs/0309048) | 2003/2006, arXiv / Springer | verified via arXiv | 证明式自引用系统，找到可证明有用的 self-rewrite 后改写自身代码 | 作为强 RSI 理论边界，说明本项目主动不做证明式自改 | 完全越过 V0 的 typed high-level update scope |
| [A Formulation of RSI](https://arxiv.org/abs/1805.06610) | 2018, arXiv | verified via arXiv | 形式化一类 recursive self-improvement 系统 | 可借鉴 formal loop 语言，用于 related work 背景 | 把 bounded adaptation 夸成 RSI |
| [STOP](https://arxiv.org/abs/2310.02304) | 2023, arXiv | verified via arXiv | 固定 LM 通过 scaffold 自改进 code-generation improver | 类似 offline candidate proposer 的结构，但只能输出 typed manifest | code self-modification / sandbox bypass / autonomous deployment |
| [ExpeL](https://arxiv.org/abs/2308.10144) | 2023, arXiv | verified via arXiv | agent 从经验中抽取可复用自然语言 knowledge | 贴近 post-episode consolidation，可映射成 strategy memory | 经验抽象可能产生虚假规则，必须做 negative-control |
| [Agent-Pro](https://arxiv.org/abs/2402.17574) / [ACL page](https://aclanthology.org/2024.acl-long.292/) | 2024, ACL | verified via arXiv / ACL | policy-level reflection and optimization | 启发“高层 policy belief / rule update”而非 action-level reflex | 游戏域结果不能推出机器人安全有效 |
| [Voyager](https://arxiv.org/abs/2305.16291) / [project](https://voyager.minedojo.org/) | 2023, arXiv / project | verified via arXiv / project | LLM embodied lifelong agent，自动 curriculum、skill library、execution feedback | skill library + environment feedback 可启发 strategy memory registry | Minecraft executable code skill 不等于 humanoid option contract |
| [Self-evolving Embodied AI](https://arxiv.org/abs/2602.04411) | 2026, arXiv | verified via arXiv | memory self-updating、task self-switching、environment self-prediction、embodiment/model self-evolution | 给 embodied self-evolution 分类；V0 只取 memory + high-level update | 范式过大，容易越过 controller freeze |
| [Robo-Cortex](https://arxiv.org/abs/2605.18729) | 2026, arXiv | verified via arXiv | dual-grain memory + navigation heuristic library + imagine-then-verify | 与障碍/导航失败策略记忆最贴近，可启发 heuristic library | VLM evaluator 和 imagination 不能替代 Gate SI |
| [EmbodiSkill](https://arxiv.org/abs/2605.10332) | 2026, arXiv | verified via arXiv | 区分 skill content error 与 execution lapse，做 targeted skill revision | 很适合 failure taxonomy：策略错 vs 执行失败 | 直接改 skill body 会越过 V0 高层 recovery scope |
| [RMA](https://arxiv.org/abs/2107.04034) | 2021, RSS / arXiv | verified via arXiv | legged robot base policy + adaptation module 实时适应环境变化 | body-state history / latent adaptation 是强基线和指标参照 | 它是低层 motor adaptation，本项目不能改 controller |
| [HumanUP](https://arxiv.org/abs/2502.12152) / [project](https://humanoid-getup.github.io/) | 2025, arXiv / RSS project | verified via arXiv / project | Unitree G1 real-world humanoid getting-up policy | fall recovery option / baseline / safety metric 参考 | 低层 getting-up controller 训练不能混入 high-level SI claim |
| [Self-Improving Embodied Foundation Models](https://arxiv.org/abs/2509.15155) / [project](https://self-improving-efms.github.io/) | 2025, arXiv / NeurIPS project | verified via arXiv / project | success detector + autonomous practice 做 embodied policy self-improvement | success detector / validation loop 可借鉴 | 端到端/低层 policy improvement 与 V0 冻结 controller 冲突 |
| [SPIBB](https://arxiv.org/abs/1712.06924) | 2019, ICML / arXiv | verified via arXiv / PMLR | batch RL 中用 baseline bootstrapping 做 safe policy improvement | 支持 Gate SI 的 conservative promote/reject 逻辑 | 理论假设和 humanoid 深度栈差异大，不能声称保证安全 |

## 6. ENPIRE 重点参考映射

ENPIRE 是目前最值得重点参考的 NVIDIA / GEAR 路线，因为它把“agent 自主改进机器人”落到一个可操作 harness：真实机器人环境可以自动 reset 和 verify，coding agent 可以调用 policy-improvement regime，rollout 可以在单机器人或多机器人 fleet 上并行跑，evolution 模块再根据 logs、失败模式和文献修改下一轮实验配置。

本项目不能直接复制 ENPIRE 的 policy self-improvement，因为 V0 冻结 locomotion controller；但 ENPIRE 的系统形态可以映射到 Gate SI：

| ENPIRE 模块 | ENPIRE 作用 | 本项目可迁移版本 | V0 红线 |
|-------------|-------------|------------------|---------|
| Environment (EN) | 自动 reset 场景并验证任务结果 | `Episode Data Package` + failure injector + controller provenance + verification artifact；后续可接 project-local sim reset / smoke | 不用 MuJoCo truth / oracle label 作为 runtime input |
| Policy Improvement (PI) | 启动 heuristic / tool calling / BC / offline RL / online RL 等 policy refinement | `CandidateUpdateProposer` 只输出 typed `CandidateUpdateManifest`，先从 deterministic rule proposer 开始 | 不改 controller checkpoint、joint action、actuator command 或 safety path |
| Rollout (R) | 单机器人或多机器人并行评估 policy | `GateSIValidationRunner` 在 seed split / matched seeds / snapshot branches 上评估 candidate；未来可记录 A800/5090 或 robot fleet utilization | R018 未完成前不写 counterfactual / ATE；23DoF smoke 未过不写 mature controller evidence |
| Evolution (E) | coding agents 分析 logs、查文献、修改训练基础设施和算法代码 | offline agent team 只做 proposal / audit / report；修改必须落成 typed manifest、人工审查和 registry entry | 不允许 autonomous code deployment，不允许绕过 `RuntimeManager` / `SafetySupervisor` |

ENPIRE 还值得借鉴两个效率指标：

- [ ] `Mean Robot Utilization (MRU)` 可改写为 `Mean Simulator/Robot Utilization`，用于记录 Gate SI validation 中可用 rollout 资源是否被浪费。
- [ ] `Mean Token Utilization (MTU)` 可改写为 agent-team research efficiency 指标：每次 proposer / auditor 消耗多少 token，产生多少 valid candidate、rejected candidate 和 safety finding。

建议把 ENPIRE 放在 related work 的核心位置，而不是普通附录。措辞可以是：

> ENPIRE demonstrates an agentic physical autoresearch harness for real-world robot policy self-improvement. Our work adopts the harness structure but bounds the improvement target to typed high-level recovery decisions under a frozen humanoid locomotion controller.

## 7. 技术映射

### V0: offline strategy memory loop

- [ ] 每个 episode 写 EDP，并扩展 SI-1 字段：controller provenance、memory consolidation artifacts、candidate manifest references。
- [ ] SI-2 从合法 runtime traces 生成 typed failure / strategy memory。
- [ ] SI-3 rule-based proposer 输出 `CandidateUpdateManifest`，只允许高层 recovery priority、command parameters、planner costs、grounding retry、abort/safe-stop policy。
- [ ] SI-4 Gate SI runner 用 snapshot branching；R018 未完成前退化为 paired matched-seed diagnostic。
- [ ] SI-5 registry / rollback CLI 记录 parent、candidate、promoted、rolled-back policy config。

### V1: longer memory and parameterized recovery

- [ ] persistent spatial-semantic obstacle memory，但必须先证明 latency、staleness 和 false memory 风险可控。
- [ ] parameterized recovery options：cooldown、retry budget、max velocity、turn-in-place angle、re-grounding threshold。
- [ ] dashboard / human approval UI 支持查看 candidate manifest、validation report 和 rollback pointer。
- [ ] episode boundary 才能加载 promoted config，禁止 mid-episode hot swap。

### V2: multi-embodiment and hardware safety case

- [ ] learned planner adaptation / skill library growth。
- [ ] multi-embodiment validation，明确 robot profile 和 controller profile。
- [ ] sim-to-real evidence 和 hardware safety case。
- [ ] 多 agent proposer / evaluator / auditor 仍保持离线异步，不进入 high-frequency safety loop。

## 8. 最小研究问题

- [ ] RQ1: typed strategy memory 是否减少 repeated failure，同时不增加 fall、collision、hard stop、unsafe completion 和 safety override？
- [ ] RQ2: typed strategy memory 是否在 memory-positive cells 中优于 instant-state、frame-stack raw-history 和 GRU raw-history baselines？
- [ ] RQ3: correct/null/shuffled/stale memory intervention 是否显示收益来自 memory content，而不是 seed leakage 或普通 history？
- [ ] RQ4: candidate update 能否通过 Gate SI validation、negative-control、safety regression 和 rollback registry 被安全管理？
- [ ] RQ5: 借鉴 ENPIRE 后，agentic proposer / evaluator / auditor 是否提高 valid candidate discovery rate，同时不增加 safety rejection rate 或 invalid-manifest rate？

## 9. 禁止和允许的表述

**允许**

- bounded self-improvement
- bounded RSI-like runtime adaptation
- failure-memory-gated high-level recovery policy improvement
- episode-level offline candidate update
- typed strategy memory candidate
- gated promotion with rollback
- paired matched-seed diagnostic
- evaluation-only oracle upper bound
- simulation-only V0 evidence

**禁止**

- 本项目已经实现 strong RSI / recursive successor design
- LLM 在实时闭环中控制机器人
- 系统自动修改底层 locomotion controller / gait / joint action / actuator command
- 已完成 Gate SI promotion 或真机自部署
- R018 未完成前使用 counterfactual / ATE / branch oracle causal claim
- 29DoF reference evidence 冒充 company G1 edu 23DoF target evidence
- runtime 使用 MuJoCo object id、ground-truth target pose、sim semantic label、oracle action 或 true failure label

## 10. Literature-Scout Synthesis

- [x] 强 RSI 文献，包括 Gödel Machines、A Formulation of RSI、STOP、Darwin Gödel Machine，应放在 related work 背景和风险边界中，用来说明本项目主动冻结 controller、禁止代码/权重自改。
- [x] 最可迁移的结构来自 Reflexion、ExpeL、Voyager、Robo-Cortex 和 EmbodiSkill：trajectory -> reflection / experience -> reusable strategy。但落地时必须转成 typed `StrategyMemoryRecord` 和 `CandidateUpdateManifest`。
- [x] ENPIRE 是主参考框架：可以借鉴 physical autoresearch harness、reset/verify、parallel rollout、log/literature-driven evolution 和 MRU/MTU；但它仍然主要改 robot policy / training workflow，本项目 V0 只能迁移 harness 结构，不迁移低层 policy self-improvement。
- [x] 其他机器人 self-improvement 文献多数改低层 policy 或训练流程。Self-Improving EFMs、MEDAL++、HumanUP、RMA 都应作为近邻/风险/metric 参考，不作为 V0 方法本体。
- [x] 本项目独特点应写成：冻结 humanoid locomotion controller 后，用 typed failure/body/event memory 改进高层 recovery/command decision，并用 Gate SI、negative controls、shuffled/stale memory 和 safety regression 决定是否 promote。
- [x] C4 claim 应保守：先报告 repeated-failure reduction、safety non-regression 和 memory-specificity；R018 未完成前只写 paired matched-seed diagnostic，不写 counterfactual 或 ATE。

## 11. 下一步建议

- [x] R050b: literature-scout 增量已并入本报告和 candidates JSON；正式论文 BibTeX/DOI/venue 精读仍归 R071。
- [ ] R050c: 以 ENPIRE 为模板设计 Gate SI harness spec：`EnvironmentResetVerify`、`CandidatePolicyImprovement`、`ValidationRollout`、`OfflineEvolutionAudit`、MRU/MTU-style utilization metrics。
- [ ] SI-1: 扩展 EDP validator，把 candidate update references 和 memory consolidation artifact hashes 纳入 schema。
- [ ] SI-2: 实现 `MemoryConsolidator`，输入 EDP traces，输出 typed `StrategyMemoryRecord`。
- [ ] SI-3: 实现 deterministic `CandidateUpdateProposer`，先不接 LLM。
- [ ] SI-4: 实现 Gate SI validation runner；R018 未完成前报告 paired matched-seed diagnostic。
- [ ] SI-5: 实现 registry / rollback inspection CLI。

## 12. 结论

本项目最稳的 RSI 叙事是 **“bounded, offline, gated self-improvement for high-level recovery decisions”**。它不是强 RSI，但有清晰的新颖性机会：把 humanoid locomotion runtime 的失败记忆变成可验证、可回滚的高层行为更新，并用 Gate SI 保证它不会越过 controller freeze、RuntimeManager/SafetySupervisor 和 evaluation-only oracle 边界。

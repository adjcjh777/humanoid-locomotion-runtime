# Citation audit 2026-06-28

**日期**: 2026-06-28
**状态**: Mac-safe source verification draft
**范围**: 只核验 title/authors/venue/source URL 和对本项目 claim 的影响；不生成论文最终 BibTeX。

本文件把 `idea-stage/REF_PAPER_SUMMARY.md`、`idea-stage/NOVELTY_CHECK.md` 和 `idea-stage/RESEARCH_REVIEW_CLAUDE_GLM52.md` 中的高风险近邻文献做一次官方来源复查。核验使用 arXiv export API 和 CVF Open Access citation metadata。正式写论文前仍要重新导出 BibTeX 并核对 PDF 版本。

## 已核验来源

| Work | Source | Verified fields | 对本项目的影响 |
|------|--------|-----------------|----------------|
| RACER | `https://arxiv.org/abs/2409.14674` | title、authors、arXiv id、DOI、abstract-level scope | 已覆盖 rich language-guided failure recovery，不能把 language recovery 写成主贡献；我们只能强调 frozen humanoid locomotion supervisor 和 typed action/evidence boundary。 |
| Automating Robot Failure Recovery Using VLMs | `https://arxiv.org/abs/2409.03966` | title、authors、arXiv id、DOI、abstract-level scope | VLM-prompt supervisor 是必需 baseline 或明确 deferred reason；不能无对照宣称 prompt-free recovery 优势。 |
| FLARE | `https://openaccess.thecvf.com/content/CVPR2026/html/Zhao_FLARE_A_Failure-Aware_Framework_for_Autonomous_Correction_and_Recovery_in_CVPR_2026_paper.html` | title、authors、CVPR 2026 venue、pages、bibtex entry | failure-aware correction/recovery 已是视觉语言机器人近邻；本项目需要把贡献限定到 locomotion supervisor + memory-value diagnostic。 |
| Code-as-Monitor | `https://arxiv.org/abs/2412.04455` | title、authors、arXiv id、DOI、CVPR 2025 acceptance note | monitor/recovery trigger 思路已有；本项目不能把 runtime monitor 本身当 novelty。 |
| HoRD | `https://arxiv.org/abs/2602.04412` | title、authors、arXiv id、abstract-level scope | history-conditioned humanoid control 是最强 memory 近邻；必须强调我们的 memory 在 supervisory layer，不进入 low-level control。 |
| Chameleon | `https://arxiv.org/abs/2603.24576` | title、authors、arXiv id、abstract-level scope | prospective memory 已是 policy-facing memory 近邻；typed event/body memory 只能作为 diagnostic representation，不能宣称全新 memory mechanism。 |
| HumanoidBench | `https://arxiv.org/abs/2403.10506` | title、authors、arXiv id、abstract-level scope | 外部 humanoid benchmark 锚点；我们的增量是 typed seeded failure/recovery protocol，不是 general humanoid benchmark。 |
| LocoMuJoCo | `https://arxiv.org/abs/2311.02496` | title、authors、arXiv id、abstract-level scope | locomotion benchmark 锚点；可借用 metric positioning，但不能把 V0 写成全新 locomotion benchmark。 |
| MuJoCo Playground | `https://arxiv.org/abs/2502.08844` | title、authors、arXiv id、abstract-level scope | 只是 deferred optional external reference；当前 repo 已明确 MJLab/classic MuJoCo first。 |
| STATE-NAV | `https://arxiv.org/abs/2506.01046` | title、authors、arXiv id、abstract-level scope | humanoid/bipedal navigation 近邻；我们定位为 recovery diagnostic，不主打 navigation。 |
| FocusNav | `https://arxiv.org/abs/2601.12790` | title、authors、arXiv id、abstract-level scope | humanoid local navigation 近邻；不要把 local navigation 本身列为主贡献。 |
| LookOut | `https://arxiv.org/abs/2508.14466` | title、authors、arXiv id、abstract-level scope | egocentric navigation 近邻；和 dashboard/replay/route claim 相关，但不是 recovery supervisor 主线。 |
| HumanoidArena | `https://arxiv.org/abs/2606.17833` | title、authors、arXiv id、abstract-level scope | hierarchy + whole-body benchmark 近邻；加强我们只做 V0 single-profile diagnostic 的边界。 |
| LangWBC | `https://arxiv.org/abs/2504.21738` | title、authors、arXiv id、abstract-level scope | language-directed whole-body control 是反方向边界；本项目不做 end-to-end WBC/VLA。 |
| LeVERB | `https://arxiv.org/abs/2506.13751` | title、authors、arXiv id、abstract-level scope | VLA / whole-body control 近邻；用于说明本项目不训练 low-level language-to-action controller。 |
| WholeBodyVLA | `https://arxiv.org/abs/2512.11047` | title、authors、arXiv id、abstract-level scope | whole-body VLA 近邻；保持 non-VLA、frozen-controller stance。 |
| From Language to Locomotion | `https://arxiv.org/abs/2510.14952` | title、authors、arXiv id、abstract-level scope | 旧表中的 `RoboGhost` shorthand 应替换为真实 title；这是 language-to-locomotion 近邻，不要把 language-conditioned locomotion 当独立 novelty。 |
| Scaling Cross-Environment Failure Reasoning Data | `https://arxiv.org/abs/2512.01946` | title、authors、arXiv id、abstract-level scope | 旧表中的 `Guardian / FailCoT` shorthand 应替换为真实 title；failure reasoning data/VLM 近邻要求我们的 negative-control 和 failure protocol 更严谨。 |

## 核验命令摘要

- [x] arXiv export API 批量核验 16 个 arXiv ids：`2409.14674`、`2409.03966`、`2502.08844`、`2311.02496`、`2403.10506`、`2506.01046`、`2504.21738`、`2506.13751`、`2602.04412`、`2603.24576`、`2601.12790`、`2508.14466`、`2606.17833`、`2512.01946`、`2512.11047`、`2510.14952`。
- [x] arXiv export API 单独核验 `2412.04455`，确认真实 title 为 `Code-as-Monitor: Constraint-aware Visual Programming for Reactive and Proactive Robotic Failure Detection`。
- [x] CVF Open Access citation metadata 核验 FLARE，确认 CVPR 2026 title、authors、conference title 和 page range。

## 仍需正式写作前补齐

- [ ] 逐篇下载/导出正式 BibTeX。
- [ ] 检查每篇 paper 的最终 venue / journal reference / DOI 是否有更新。
- [ ] 精读 HoRD、Chameleon、RACER、FLARE、Code-as-Monitor 五篇的 method/evaluation 部分。
- [ ] 将 `verify_pending` 标签从旧 literature table 中移除或改为具体 verified/pending 状态。
- [ ] 写 related work 时显式避开以下 claim：
  - [ ] first supervisory recovery policy
  - [ ] novel 8-action space
  - [ ] memory generally helps
  - [ ] language recovery as main contribution
  - [ ] real-hardware or cross-body generalization

## 当前 claim 建议

- [x] 保留：memory-value diagnostic。
- [x] 保留：typed seeded failure/recovery protocol。
- [x] 保留：frozen controller 上的 supervisory recovery formulation。
- [x] 弱化：8-action supervisor method novelty。
- [x] 弱化：language-conditioned recovery novelty。
- [x] 明确：VLM baseline 至少要跑，或在核心 gates 前写清 deferred reason。

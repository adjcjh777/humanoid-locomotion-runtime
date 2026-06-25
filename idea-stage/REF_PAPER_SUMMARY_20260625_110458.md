# 相关文献综述：Humanoid Locomotion Runtime Recovery

**生成时间**：2026-06-25 11:04 +0800  
**输入文档**：`docs/research_plan_prd.md`  
**使用 skill**：`research-lit`  
**检索说明**：本项目没有发现 `papers/`、`literature/` 或 `research-wiki/` 本地论文库。ARIS `arxiv_fetch.py` 被 arXiv API 429 限流，已按降级规则使用 arXiv 网页、WebSearch、Semantic Scholar 局部结果与 OpenAlex 结果。

## PRD 研究锚点

当前 PRD 的核心不是低层 humanoid control，也不是 end-to-end VLA，而是：

- 冻结成熟 Unitree G1 / MuJoCo Playground locomotion controller；
- 通过 `RuntimeManager` 和 `SafetySupervisor` 只暴露 typed high-level locomotion/recovery commands；
- 使用 `BodyMemoryState = instant state + window summary + event/recovery memory`；
- 训练低频 supervisory RL recovery selector，在 8 个 typed actions 中选择；
- 以 seeded failure-recovery benchmark 和 Episode Data Package 做系统级评估。

## 文献版图

1. **Humanoid benchmark / controller platform**：HumanoidBench、MuJoCo Playground、LocoMuJoCo、HumanoidArena 已覆盖 humanoid benchmark、低层控制器和 high-level/low-level 接口评估。
2. **Language / VLA humanoid control**：LangWBC、LeVERB、RoboGhost、Humanoid-LLA、EgoActor、WholeBodyVLA 大多直接学习 language/vision 到 whole-body action 或 motion latent，和本项目“不替换低层控制器”的边界不同，但会压缩 novelty。
3. **Humanoid navigation / stability-aware planning**：STATE-NAV、FocusNav、Gallant、LookOut 已覆盖 bipedal stability、local navigation、slowing/rerouting 等行为，与本项目 recovery action 集合部分重叠。
4. **Failure recovery / memory**：RACER、Automating Robot Failure Recovery、Conditional Multi-Stage Failure Recovery、FLARE、HoRD、Chameleon 分别覆盖 supervisor-actor recovery、VLM/LLM recovery、history-conditioned humanoid RL、event memory for delayed decisions。

## 相关文献表

| Paper | Venue / Year | 方法摘要 | 与本项目关系 | 威胁 |
|---|---:|---|---|---|
| [HumanoidBench](https://arxiv.org/abs/2403.10506) | RSS 2024 | whole-body locomotion/manipulation simulated benchmark，显示 robust low-level policies 支持 hierarchical 方法 | benchmark positioning 和 baseline 依据 | 中 |
| [MuJoCo Playground](https://arxiv.org/abs/2502.08844) | 2025 | MJX/MuJoCo robot learning framework，支持 Unitree G1/H1 等 humanoid locomotion | 平台与 controller-native baseline | 低 |
| [LocoMuJoCo](https://arxiv.org/abs/2311.02496) | NeurIPS Workshop 2023 | locomotion IL benchmark，含 humanoid/biped、dynamics randomization、partial observability | locomotion benchmark 对照 | 中低 |
| [HumanoidArena](https://arxiv.org/abs/2606.17833) | arXiv 2026 | egocentric hierarchical whole-body benchmark，强调 high-level policy 与 low-level tracker 接口 | 强化“接口可执行性”评估压力 | 中 |
| [LangWBC](https://arxiv.org/abs/2504.21738) | RSS 2025 | end-to-end language-directed humanoid whole-body control | 直接竞争 language-conditioned humanoid control framing | 中高 |
| [LeVERB](https://arxiv.org/abs/2506.13751) | arXiv 2025 | latent vision-language humanoid WBC，150+ tasks | VLA + low-level WBC 的强相邻工作 | 中高 |
| [RoboGhost](https://arxiv.org/abs/2510.14952) | ICLR 2026 | retargeting-free language-to-locomotion，motion latent + diffusion policy | 直接压缩 language-to-locomotion novelty | 高 |
| [Humanoid-LLA](https://arxiv.org/abs/2511.22963) | 2025/2026 | free-form language 到 unified motion vocabulary 和 executable actions | 与 typed action / language control 部分重叠 | 中高 |
| [EgoActor](https://arxiv.org/abs/2602.04515) | arXiv 2026 | VLM 从 egocentric observation 预测 locomotion primitives / head / manipulation commands | 高层 primitive selection 相邻 | 中 |
| [WholeBodyVLA](https://arxiv.org/abs/2512.11047) | arXiv 2025 | latent VLA + locomotion-oriented RL policy for large-space loco-manipulation | VLA 系统级竞争 | 中 |
| [STATE-NAV](https://arxiv.org/abs/2506.01046) | RA-L 2025 | stability-aware traversability + TravRRT* + MPC | 强相关 bipedal navigation baseline | 中 |
| [FocusNav](https://arxiv.org/abs/2601.12790) | arXiv 2026 | Unitree G1 local navigation，waypoint attention + stability gating | 与 stability-aware local navigation 重叠 | 中 |
| [Gallant](https://arxiv.org/abs/2511.14625) | CVPR 2026 | voxel-grid humanoid locomotion/local navigation | end-to-end local navigation 强 baseline | 中 |
| [LookOut](https://arxiv.org/abs/2508.14466) | ICCV 2025 | egocentric future 6D head-pose trajectory，学习 slowing/rerouting/looking around | 与 `slow_down` / `local_replan` / observe 行为重叠 | 中高 |
| [RACER](https://arxiv.org/abs/2409.14674) | ICRA 2025 | supervisor-actor language-guided failure recovery for manipulation | 最强威胁：supervisory recovery framing | 高 |
| [Automating Robot Failure Recovery with VLMs](https://arxiv.org/abs/2409.03966) | ACC 2025 | VLM optimized prompts for motion/task recovery | 需要纳入 VLM supervisor baseline | 中 |
| [Conditional Multi-Stage Failure Recovery](https://aclanthology.org/2025.realm-1.15/) | REALM 2025 | LLM zero-shot chain prompting recovery stages | failure recovery reasoning 相邻 | 中 |
| [FLARE](https://openaccess.thecvf.com/content/CVPR2026/papers/Zhao_FLARE_A_Failure-Aware_Framework_for_Autonomous_Correction_and_Recovery_in_CVPR_2026_paper.pdf) | CVPR 2026 | Retry/Reset recovery，offline MLLM analysis + online monitor | recovery monitor / reset baseline 压力 | 中 |
| [HoRD](https://arxiv.org/abs/2602.04412) | arXiv 2026 | history-conditioned RL for robust humanoid control | 威胁 body-memory-conditioned humanoid RL claim | 高 |
| [Chameleon](https://arxiv.org/abs/2603.24576) | arXiv 2026 | control-indexed prospective event memory for delayed visuomotor decisions | 威胁 event/recovery memory claim | 中高 |

## 主要空缺

- 尚未发现“冻结 humanoid controller + typed supervisory recovery RL + body-memory 消融 + seeded failure benchmark”的完全重合工作。
- 但每个组件都有强先例，单纯组合难以支撑强 novelty。
- 最有价值的可防御方向不是“我提出了 body memory”，而是“在哪些 humanoid failure family 中，event/recovery memory 比 instant state 真有必要”。
- 需要 mandatory oracle upper bound 和 RACER-style VLM supervisor baseline，否则 reviewer 会认为没有解释为什么不用更自然的 VLM/LLM recovery supervisor。


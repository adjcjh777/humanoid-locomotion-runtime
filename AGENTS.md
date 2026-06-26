# AGENTS.md

## 语言规则

- 除非用户明确要求其他语言，内部进展更新和面向用户的回复都使用中文。
- 文档主文使用中文；代码标识符、命令、路径、论文名、工具名和表格中需要机器读取的字段可以保留英文。

## 项目范围

- 本仓库是独立的 **Humanoid Locomotion Runtime** 项目。
- 权威计划文件是 [docs/research_plan_prd.md](docs/research_plan_prd.md)。
- V0 目标是 MuJoCo + Unitree G1 + 成熟 locomotion controller；如果 G1 controller smoke gate 失败，优先切换到 MJLab/mujocolab-compatible classic MuJoCo backend，而不是默认切到 MuJoCo Playground。
- V0 是语言条件 humanoid locomotion runtime，不是端到端 foundation-scale VLA。
- V0 的学习只发生在 task/failure 层的 supervisory recovery；任何 learned policy 都不能替代底层 gait、joint 或 actuator control。

## 核心边界

- runtime 输入可以包含 RGB-D、camera parameters、robot state、open-vocabulary grounding output 和 runtime summaries。
- MuJoCo privileged object IDs、ground-truth target poses、simulator semantic labels 只允许用于 evaluation，不允许进入 runtime decision。
- WebUI 和未来 agent 只能通过 `RuntimeManager` 发出高层 typed commands。
- 低层 controller commands 和 safety overrides 不允许绕过 `RuntimeManager` 与 `SafetySupervisor`。
- RL recovery policy 只能通过 `RuntimeManager` 选择 typed high-level recovery actions。
- 如果未来加入 Agent Bus，它只能用于高层异步协作和审计，不能进入 real-time safety 或高频控制闭环。

## 开发默认规则

- 模块按 backend 可替换设计：perception、memory、navigation、locomotion controller、recovery policy、dashboard、benchmark runner。
- 先实现 schemas 和 interfaces，再接入 MuJoCo、perception、dashboard、controller 等重依赖。
- 添加 benchmark 代码时必须保留 PRD 中的 Episode Data Package contract。
- 不提交 generated runs、logs、bags、datasets、checkpoints、model weights。

## ARIS 科研工作流

- 科研阶段默认使用 ARIS skills，不用零散聊天总结代替正式产物。推荐流程：
  - `/research-lit`：文献收集和验证状态记录。
  - `/idea-creator`：研究方向、kill list、执行顺序。
  - `/novelty-check`：prior-art 冲突和 claim audit。
  - `/research-review`：外部审稿人视角的可行性与贡献审查。
  - `/experiment-plan`：claim-driven 实验计划、run order、tracker。
  - `/experiment-queue`、`/run-experiment`、`/monitor-experiment`、`/analyze-results`：远程批量执行、监控和结果分析。
- ARIS 输出放在 stage-scoped directories：`idea-stage/`、`refine-logs/`、`review-stage/`、`paper/`。
- 生成新 ARIS 产物后追加记录到 `MANIFEST.md`。
- 保留 timestamped artifact 和 fixed latest copy 的双文件模式。
- 不伪造论文证据；未验证的 run、citation、metric 必须标记为 pending 或 failed。
- 原始 agent traces 不进公开仓库：`.aris/meta/`、`.aris/traces/`、prompt、request、response、model metadata 都视为本机/私有审计材料。只提交人工整理后的 summaries、tables、review decisions 和必要的小型配置。

## Reviewer 路由

- 如果任务运行在 **公司 / 远程实验服务器**，例如 A800 或 5090，ARIS review 阶段使用 Claude/Codex reviewer route，并指定 **GLM 5.2 max effort**。
- 如果任务运行在 **本机工作室**，ARIS review 阶段使用 Claude Code reviewer，并指定 **Claude Opus 4.8 max effort**。
- 启动 reviewer workflow 前必须判断环境：
  - 本机工作室通常是 macOS 路径 `/Users/junhaocheng/working-dir/...`。
  - 公司 / 远程实验服务器通常是 SSH/GPU 环境路径 `/home/...` 或明确标注为 A800/5090。
  - 如果环境不明确，先检查 `pwd`、`hostname`、`git remote -v` 和 GPU 可见性；仍不明确则询问用户。
- reviewer 路由只影响 review/critique 阶段；不得改变 runtime safety boundary、benchmark rules 或 MuJoCo privileged signals 的访问边界。

## 实验执行节奏

- 每个 run series 优先使用一个 canonical experiment host。当前默认 A800 是主实验机；5090 仅作备份，除非用户明确改变。
- 可公开的机器 profile 存放在 `docs/a800_machine_profile.md` 和 `docs/rtx5090_machine_profile.md`；私有 SSH、IP、token、jump-host 信息不得进入仓库。
- 白天做需要人判断的工作：代码修改、协议冻结、gate review、失败案例检查、commit/push。
- 夜间交给 ARIS 自动化：queued smoke tests、pilot batches、multi-seed runs、monitoring、result summaries。
- 每次 overnight run 次日必须有 Morning Acceptance Check：状态、失败 jobs、artifact paths、metrics、gate decision、next action。
- generated runs、raw logs、replay artifacts、checkpoints、model weights 不得进入 git，除非被明确整理成很小的文档示例。
- 执行顺序以 gate 为准，不以日历为准。固定 28 天 timeline 是参考节奏；任一 gate 未通过，不进入下一阶段。
- 当前只允许 GO 到“最小代码脚手架和协议冻结”；PPO、大规模实验和论文主结论必须等 snapshot branching、baseline、统计和 EDP gate 通过后再启动。

## 审核后新增硬边界

- 不能把 matched-seed evaluation 直接称为 causal counterfactual。只有实现完整 simulator/runtime snapshot branching 后，才允许使用 counterfactual / ATE / branch oracle 等因果措辞；否则只能写 paired matched-seed diagnostic。
- Snapshot branching 至少要覆盖 simulator state、随机数状态、planner/localization/memory/controller/failure-injector state、active option state、decision id、observation hash 和 memory hash。
- Recovery actions 必须定义为 options / SMDP：initiation condition、action mask、execution implementation、min/max duration、success/failure/termination、interruptibility、retry budget、cooldown。
- learned policy 结果必须拆分报告：policy-only outcome、full-stack-with-fallback outcome、fallback invocation rate、safety override rate。
- `rule_recovery_tuned` 只能作为 deployable heuristic baseline / fallback，不再称为 debugging oracle；真正 oracle 必须是 evaluation-only privileged 或 snapshot branch oracle。
- 主文 baseline 必须包含 ordinary history models：`frame_stack_raw_history` 和 `GRU_raw_history`。VLM baseline 可以作为附录或后续分支，不能替代 GRU baseline。
- Memory effect 必须拆成两类 estimand：训练/模型效应（不同 policy）和决策时 memory-content 效应（同一 policy 的 correct/null/shuffled/stale memory intervention）。若做 test-time mask，训练时必须加入 memory dropout 或 `memory_available` mask。
- Failure taxonomy 必须拆成 cause × temporal profile。`user_interrupt` 是 task-control event，不作为 failure family。
- Negative control 的“无收益”必须用 smallest effect size of interest 和 equivalence / TOST 风格证据支持；不能把 p 值不显著写成没有效果。
- final evaluation 必须预注册 primary endpoint、policy training seeds、scenario seeds、cluster/hierarchical bootstrap 和 multiplicity control。
- 环境必须锁定 Python、MuJoCo、MJLab/mujocolab backend reference、controller checkpoint、robot XML/MJCF 版本与 hash；JAX/JAXLIB 只在显式选择 MuJoCo Playground deferred fallback 时才作为额外锁定项。A800/5090 的 live ops 细节放 private ops，不进公开 repo。

## 可确认待办规则

- 所有计划、时间线、实验执行、handoff、gate、验收和检查清单类文档中的可执行事项必须使用 checklist：未完成写 `- [ ]`，已完成写 `- [x]`。
- `refine-logs/DAILY_EXPERIMENT_TIMELINE.md` 必须让每一天的“白天人工 / 晚上 ARIS / 次日验收”都可逐项确认。
- `refine-logs/EXPERIMENT_PLAN.md` 必须让每个实验块 B0-B6 都有块级可确认清单。
- 只有同时满足“有证据”和“有可复查位置”的事项才能打勾。证据可以是 commit id、run id、tracker 行、机器 profile、summary 文件、配置文件或命令结果摘要。
- 不允许只用叙述性文字表示进度；计划、timeline、tracker 三者必须能互相对上。
- `refine-logs/EXPERIMENT_TRACKER.md` 是 run-level 状态源；timeline 和 experiment plan 是人可读 checklist。修改任一处状态时，检查另外两处是否需要同步。
- 涉及 A800/5090 的本机资源时，必须分别记录每台机器状态；`.agents/` 和 `.aris/installed-skills-codex.txt` 只在本机初始化，不进 git。
- 跨机器工作前先 `git pull --ff-only`，工作后用 `git status --short --branch` 确认干净；需要同步给其他机器时 commit/push。
- 修改 fixed latest copy 后，如果同一份活跃 artifact 有 timestamped companion，必须同步更新 companion，或新建 timestamped copy 并更新 `MANIFEST.md`。

## 首批实现顺序

1. [x] Core schemas：`LocomotionCommand`、`LocomotionStatus`、`MemoryTarget`、`BodyMemoryState`、`FailureEvent`、`RecoveryActionRecord`。证据：`src/humanoid_locomotion_runtime/schemas.py`、`tests/test_gate_b_schemas.py`。
2. [x] Event logger 和 Episode Data Package writer。证据：`src/humanoid_locomotion_runtime/edp.py`、`tests/test_gate_b_edp.py`。
3. [ ] MuJoCo + G1 backend smoke test。
4. [ ] Temporary object memory 和 RGB-D grounding adapter。
5. [ ] NavigatorV0 local planner 和 SafetySupervisor。
6. [ ] Body memory、rule-based recovery fallback、bandit sanity check、supervisory RL recovery selector。
7. [ ] Seeded benchmark runner、controller-native baseline、Viser dashboard。

<!-- ARIS-CODEX:BEGIN -->
## ARIS Codex 本机资源

- `.agents/` 和 `.aris/installed-skills-codex.txt` 是机器本地生成资源，必须保持在 git 外。
- 每台实验机都要使用该机器本地的 ARIS checkout 单独初始化或 reconcile。
- 运行 installer 时使用 `--no-doc`，避免把 host-specific absolute paths 写入这个 tracked `AGENTS.md`。
- 示例模式：
  `bash /path/to/ARIS/tools/install_aris_codex.sh "$PWD" --aris-repo /path/to/ARIS --no-doc --quiet`
- 已观察到的 host-specific ARIS roots 见 `docs/a800_machine_profile.md` 和 `docs/rtx5090_machine_profile.md`。
- 不要提交 generated symlink targets、installer manifests、credentials、SSH aliases、tokens、logs、runs、checkpoints、weights、datasets。
<!-- ARIS-CODEX:END -->

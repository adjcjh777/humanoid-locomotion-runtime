# 研究产物清单

> 由 ARIS skills 维护，用于记录研究生命周期中生成的各类 artifacts。表头保持英文以兼容下游工具。

读法：

- `Timestamp` 是产物登记时间，不一定等于实验发生时间。
- `Skill` 表示来源；`manual` 代表人工整理或文档维护。
- `File` 是可复查文件路径。
- `Stage` 表示它属于 idea discovery、implementation 等哪个阶段。
- `Description` 用白话说明这个文件为什么存在，以及是否是最新副本或历史快照。

| Timestamp | Skill | File | Stage | Description |
|-----------|-------|------|-------|-------------|
| 2026-06-25 11:04 | /research-lit | idea-stage/REF_PAPER_SUMMARY_20260625_110458.md | idea-discovery | humanoid locomotion recovery runtime 文献综述 |
| 2026-06-25 11:04 | /research-lit | idea-stage/REF_PAPER_SUMMARY.md | idea-discovery | 最新副本 |
| 2026-06-25 11:04 | /idea-creator | idea-stage/IDEA_REPORT_20260625_110458.md | idea-discovery | 研究想法扩展与 go/no-go gates |
| 2026-06-25 11:04 | /idea-creator | idea-stage/IDEA_REPORT.md | idea-discovery | 最新副本 |
| 2026-06-25 11:04 | /novelty-check | idea-stage/NOVELTY_CHECK_20260625_110458.md | idea-discovery | 近期 humanoid/recovery 文献下的新颖性评估 |
| 2026-06-25 11:04 | /novelty-check | idea-stage/NOVELTY_CHECK.md | idea-discovery | 最新副本 |
| 2026-06-25 11:04 | /research-review | idea-stage/RESEARCH_REVIEW_CLAUDE_GLM52_20260625_110458.md | idea-discovery | Claude Code GLM 5.2 max effort 评审 |
| 2026-06-25 11:04 | /research-review | idea-stage/RESEARCH_REVIEW_CLAUDE_GLM52.md | idea-discovery | 最新副本 |
| 2026-06-25 11:58 | /research-lit | idea-stage/REF_PAPER_SUMMARY_20260625_115846.md | idea-discovery | Claude Opus 4.8 本机重跑；使用 web source 候选文献，arxiv_fetch.py 仍 HTTP 429 |
| 2026-06-25 11:58 | /research-lit | idea-stage/REF_PAPER_SUMMARY.md | idea-discovery | Claude Opus 4.8 重跑后的最新副本 |
| 2026-06-25 11:58 | /idea-creator | idea-stage/IDEA_REPORT_20260625_115846.md | idea-discovery | Claude Opus 4.8 idea report；推荐 I10 + I1 + I3 core package |
| 2026-06-25 11:58 | /idea-creator | idea-stage/IDEA_REPORT.md | idea-discovery | Claude Opus 4.8 重跑后的最新副本 |
| 2026-06-25 11:58 | /novelty-check | idea-stage/NOVELTY_CHECK_20260625_115846.md | idea-discovery | Claude Opus 4.8 novelty audit；novelty 5.5/10，并建议 pivot 到 memory-value diagnostic |
| 2026-06-25 11:58 | /novelty-check | idea-stage/NOVELTY_CHECK.md | idea-discovery | Claude Opus 4.8 重跑后的最新副本 |
| 2026-06-25 11:58 | /research-review | idea-stage/RESEARCH_REVIEW_CLAUDE_OPUS48_20260625_115846.md | idea-discovery | Claude Opus 4.8 research review；建议走 snapshot-branching memory diagnostic paper |
| 2026-06-25 11:58 | /research-review | idea-stage/RESEARCH_REVIEW_CLAUDE_GLM52.md | idea-discovery | 兼容旧文件名的最新副本，内容来自 Claude Opus 4.8 重跑 |
| 2026-06-25 12:13 | /experiment-plan | refine-logs/EXPERIMENT_PLAN_20260625_121320.md | implementation | claim-driven 实验路线图，包含 A800 single-host 执行策略 |
| 2026-06-25 12:13 | /experiment-plan | refine-logs/EXPERIMENT_PLAN.md | implementation | 最新副本 |
| 2026-06-25 12:13 | /experiment-plan | refine-logs/EXPERIMENT_TRACKER_20260625_121320.md | implementation | 白天人工工作与夜间 ARIS 自动化 run tracker |
| 2026-06-25 12:13 | /experiment-plan | refine-logs/EXPERIMENT_TRACKER.md | implementation | 最新副本 |
| 2026-06-25 12:13 | /experiment-plan | refine-logs/DAILY_EXPERIMENT_TIMELINE_20260625_121320.md | implementation | A800 single-host workflow 的 28 天游/夜实验时间线 |
| 2026-06-25 12:13 | /experiment-plan | refine-logs/DAILY_EXPERIMENT_TIMELINE.md | implementation | 最新副本 |
| 2026-06-25 07:57 | manual | docs/gate_a_foundation.md | implementation | Gate A repo foundation、environment lock、artifact retention 和 CI 证据记录 |
| 2026-06-25 08:43 | manual | docs/gate_b_schema_edp.md | implementation | Gate B schema/leakage boundary、policy serializer 和 Episode Data Package 证据记录 |
| 2026-06-25 17:17 | manual | docs/gate_b_schema_edp.md | implementation | Gate B EDP integrity follow-up：artifact SHA256、retention consistency、policy/recovery records 和 evaluation split |
| 2026-06-25 17:50 | manual | refine-logs/MORNING_ACCEPTANCE_20260626.md | implementation | R001/R002/R004/R005 ARIS night handoff morning acceptance summary |
| 2026-06-26 01:30 | manual | configs/environment.lock.toml | implementation | 将 V0 backend policy 从 MuJoCo Playground-first 改为 MJLab/mujocolab-compatible classic MuJoCo first；JAX/JAXLIB 降级为 deferred optional extra |
| 2026-06-26 01:41 | manual | refine-logs/MORNING_ACCEPTANCE_RERUN_20260626.md | implementation | R001/R002/R004/R005 rerun summary；R002 classic MuJoCo smoke 通过，R004 按用户 100GB override 完成 synthetic-only microbenchmark |
| 2026-06-26 02:04 | manual | docs/mjlab_backend_lock.md | implementation | 早期本机同级目录 backend lock 记录；已被 02:22 project-local submodule lock supersede |
| 2026-06-26 02:04 | manual | configs/environment.lock.toml | implementation | 早期本机同级目录 backend reference；已被 02:22 project-local submodule lock supersede |
| 2026-06-26 02:04 | manual | refine-logs/EXPERIMENT_PLAN_20260626_020420.md | implementation | backend lock 后的 timestamped 实验计划副本 |
| 2026-06-26 02:04 | manual | refine-logs/EXPERIMENT_PLAN.md | implementation | backend lock 后的最新实验计划副本 |
| 2026-06-26 02:04 | manual | refine-logs/EXPERIMENT_TRACKER_20260626_020420.md | implementation | backend lock 后的 timestamped tracker 副本 |
| 2026-06-26 02:04 | manual | refine-logs/EXPERIMENT_TRACKER.md | implementation | backend lock 后的最新 tracker 副本 |
| 2026-06-26 02:04 | manual | refine-logs/DAILY_EXPERIMENT_TIMELINE_20260626_020420.md | implementation | backend lock 后的 timestamped 每日时间线副本 |
| 2026-06-26 02:04 | manual | refine-logs/DAILY_EXPERIMENT_TIMELINE.md | implementation | backend lock 后的最新每日时间线副本 |
| 2026-06-26 02:22 | manual | .gitmodules | implementation | 将 MJLab 改为项目内 `third_party/mjlab` submodule，避免开源复现依赖作者机器同级目录 |
| 2026-06-26 02:22 | manual | docs/mjlab_backend_lock.md | implementation | project-local MJLab backend lock：`third_party/mjlab` commit、G1 MJCF、task config、wrapper hashes |
| 2026-06-26 02:22 | manual | docs/controller_checkpoint_selection.md | implementation | 官方 Unitree RL MJLab G1 velocity ONNX controller artifact candidate 的来源、hash、筛选理由和 smoke 阻塞条件 |
| 2026-06-26 02:22 | manual | scripts/fetch_unitree_g1_velocity_checkpoint.sh | implementation | 从官方 Unitree RL MJLab commit 拉取 G1 velocity ONNX candidate 并校验 SHA256 |
| 2026-06-26 02:22 | manual | configs/environment.lock.toml | implementation | 将 backend reference 更新为 project-local submodule；记录官方 ONNX candidate 本地 ignored checkpoint path 和 hash |
| 2026-06-26 02:22 | manual | refine-logs/EXPERIMENT_PLAN_20260626_022236.md | implementation | project-local backend/checkpoint lock 后的 timestamped 实验计划副本 |
| 2026-06-26 02:22 | manual | refine-logs/EXPERIMENT_PLAN.md | implementation | project-local backend/checkpoint lock 后的最新实验计划副本 |
| 2026-06-26 02:22 | manual | refine-logs/EXPERIMENT_TRACKER_20260626_022236.md | implementation | project-local backend/checkpoint lock 后的 timestamped tracker 副本 |
| 2026-06-26 02:22 | manual | refine-logs/EXPERIMENT_TRACKER.md | implementation | project-local backend/checkpoint lock 后的最新 tracker 副本 |
| 2026-06-26 02:22 | manual | refine-logs/DAILY_EXPERIMENT_TIMELINE_20260626_022236.md | implementation | project-local backend/checkpoint lock 后的 timestamped 每日时间线副本 |
| 2026-06-26 02:22 | manual | refine-logs/DAILY_EXPERIMENT_TIMELINE.md | implementation | project-local backend/checkpoint lock 后的最新每日时间线副本 |
| 2026-06-26 03:38 | manual | scripts/mjlab_g1_smoke.py | implementation | Headless MJLab Unitree G1 smoke：创建 `Mjlab-Velocity-Flat-Unitree-G1`，reset 后运行 16 个 zero-action steps |
| 2026-06-26 03:38 | manual | scripts/mjlab_sync_and_smoke.sh | implementation | 使用主项目 Python 3.12.13 同步 `third_party/mjlab/uv.lock`，运行 MJLab import matrix 和 G1 headless simulation smoke |
| 2026-06-26 03:38 | manual | configs/environment.lock.toml | implementation | 将 `mjlab_runtime_dependencies` 更新为 verified full MJLab G1 headless smoke；记录 Python/package/device/smoke 证据和 ONNX shape gap |
| 2026-06-26 03:38 | manual | docs/mjlab_backend_lock.md | implementation | 记录完整 MJLab runtime dependency smoke 和 G1 headless simulation smoke 通过 |
| 2026-06-26 03:38 | manual | docs/controller_checkpoint_selection.md | implementation | 记录 ONNX candidate input `[1,98]`、output `[1,29]` 与 MJLab actor obs `[1,99]` 的 adapter gap |
| 2026-06-26 03:38 | manual | refine-logs/EXPERIMENT_PLAN_20260626_033833.md | implementation | 完整 MJLab dependency/simulation smoke 后的 timestamped 实验计划副本 |
| 2026-06-26 03:38 | manual | refine-logs/EXPERIMENT_PLAN.md | implementation | 完整 MJLab dependency/simulation smoke 后的最新实验计划副本 |
| 2026-06-26 03:38 | manual | refine-logs/EXPERIMENT_TRACKER_20260626_033833.md | implementation | 完整 MJLab dependency/simulation smoke 后的 timestamped tracker 副本 |
| 2026-06-26 03:38 | manual | refine-logs/EXPERIMENT_TRACKER.md | implementation | 完整 MJLab dependency/simulation smoke 后的最新 tracker 副本 |
| 2026-06-26 03:38 | manual | refine-logs/DAILY_EXPERIMENT_TIMELINE_20260626_033833.md | implementation | 完整 MJLab dependency/simulation smoke 后的 timestamped 每日时间线副本 |
| 2026-06-26 03:38 | manual | refine-logs/DAILY_EXPERIMENT_TIMELINE.md | implementation | 完整 MJLab dependency/simulation smoke 后的最新每日时间线副本 |
| 2026-06-26 12:32 | manual | docs/research_plan_prd.md | implementation | PRD 通俗化改写；保留 V0 约定、MJLab fallback、EDP、snapshot branching、negative-control 和 baseline 边界 |
| 2026-06-26 12:32 | manual | README.md | implementation | README 第一屏通俗化；解释项目目标、V0 范围和非目标 |
| 2026-06-26 12:32 | manual | docs/gate_a_foundation.md | implementation | Gate A 记录通俗化；明确它只证明仓库地基，不授权 PPO、大规模 rollout 或论文结论 |
| 2026-06-26 12:32 | manual | docs/gate_b_schema_edp.md | implementation | Gate B 记录通俗化；解释 runtime/evaluation 泄漏边界和 EDP 证据包 |
| 2026-06-26 12:32 | manual | refine-logs/EXPERIMENT_PLAN_20260626_123244.md | implementation | 实验计划通俗化 timestamp copy；保留 run blocks、gate、claim mapping 和 checklist |
| 2026-06-26 12:32 | manual | refine-logs/EXPERIMENT_PLAN.md | implementation | 实验计划通俗化最新副本 |
| 2026-06-26 12:32 | manual | refine-logs/DAILY_EXPERIMENT_TIMELINE_20260626_123244.md | implementation | 每日实验时间线通俗化 timestamp copy；强调 gate 优先于日历 |
| 2026-06-26 12:32 | manual | refine-logs/DAILY_EXPERIMENT_TIMELINE.md | implementation | 每日实验时间线通俗化最新副本 |
| 2026-06-26 12:32 | manual | refine-logs/EXPERIMENT_TRACKER_20260626_123244.md | implementation | 实验 tracker 通俗化 timestamp copy；补充 run-level 状态读法 |
| 2026-06-26 12:32 | manual | refine-logs/EXPERIMENT_TRACKER.md | implementation | 实验 tracker 通俗化最新副本 |
| 2026-06-26 12:39 | manual | AGENTS.md | implementation | 项目规则通俗化导读；保留 runtime safety、evaluation leakage、gate 和 ARIS 工作流规则 |
| 2026-06-26 12:39 | manual | CONTEXT.md | implementation | 项目术语上下文补充读法说明 |
| 2026-06-26 12:39 | manual | docs/a800_machine_profile.md | implementation | A800 公开机器档案补充白话摘要；不加入私有连接信息 |
| 2026-06-26 12:39 | manual | docs/rtx5090_machine_profile.md | implementation | RTX 5090 公开机器档案补充白话摘要；强调 backup host 边界 |
| 2026-06-26 12:39 | manual | refine-logs/MORNING_ACCEPTANCE_20260626.md | implementation | 首次 morning acceptance summary 补充白话结论；保留原始指标和 gate decision |
| 2026-06-26 12:39 | manual | refine-logs/MORNING_ACCEPTANCE_RERUN_20260626.md | implementation | rerun morning acceptance summary 补充白话结论；保留 100GB override 边界 |
| 2026-06-26 12:39 | manual | idea-stage/IDEA_REPORT_20260626_123900.md | idea-discovery | idea report 通俗化 timestamp copy；新增白话读法，不改研究建议 |
| 2026-06-26 12:39 | manual | idea-stage/IDEA_REPORT.md | idea-discovery | idea report 通俗化最新副本 |
| 2026-06-26 12:39 | manual | idea-stage/NOVELTY_CHECK_20260626_123900.md | idea-discovery | novelty check 通俗化 timestamp copy；新增白话读法，不改评分和风险 |
| 2026-06-26 12:39 | manual | idea-stage/NOVELTY_CHECK.md | idea-discovery | novelty check 通俗化最新副本 |
| 2026-06-26 12:39 | manual | idea-stage/REF_PAPER_SUMMARY_20260626_123900.md | idea-discovery | 文献摘要通俗化 timestamp copy；新增近邻工作读法和核验提醒 |
| 2026-06-26 12:39 | manual | idea-stage/REF_PAPER_SUMMARY.md | idea-discovery | 文献摘要通俗化最新副本 |
| 2026-06-26 12:39 | manual | idea-stage/RESEARCH_REVIEW_CLAUDE_GLM52_20260626_123900.md | idea-discovery | research review 通俗化 timestamp copy；新增外部评审读法，不改结论 |
| 2026-06-26 12:39 | manual | idea-stage/RESEARCH_REVIEW_CLAUDE_GLM52.md | idea-discovery | research review 通俗化最新副本 |
| 2026-06-26 12:39 | manual | refine-logs/*_20260625_121320.md | implementation | 旧实验计划/时间线/tracker 快照补充归档读法，指向通俗化最新副本 |
| 2026-06-26 12:39 | manual | idea-stage/*20260625*.md | idea-discovery | 旧 idea-stage 快照补充归档读法，保留原始研究结论并指向通俗化最新副本 |
| 2026-06-26 06:16 | manual | docs/gate_a_foundation.md | implementation | pull merge 后的 Gate A 最新副本；保留 Mac 通俗化读法，同时同步 project-local MJLab runtime smoke 和 controller adapter gap 证据 |
| 2026-06-26 06:16 | manual | refine-logs/EXPERIMENT_PLAN_20260626_061653.md | implementation | pull merge 后的实验计划 timestamp copy；对齐 Mac 通俗化读法和 MJLab backend/checkpoint/smoke 证据 |
| 2026-06-26 06:16 | manual | refine-logs/EXPERIMENT_PLAN.md | implementation | pull merge 后的实验计划最新副本 |
| 2026-06-26 06:16 | manual | refine-logs/EXPERIMENT_TRACKER_20260626_061653.md | implementation | pull merge 后的 tracker timestamp copy；R002/R007 对齐 project-local MJLab smoke 和 ONNX adapter gap |
| 2026-06-26 06:16 | manual | refine-logs/EXPERIMENT_TRACKER.md | implementation | pull merge 后的 tracker 最新副本 |
| 2026-06-26 06:16 | manual | refine-logs/DAILY_EXPERIMENT_TIMELINE_20260626_061653.md | implementation | pull merge 后的每日时间线 timestamp copy；同步 Gate A/MJLab smoke 状态和 controller smoke 阻塞项 |
| 2026-06-26 06:16 | manual | refine-logs/DAILY_EXPERIMENT_TIMELINE.md | implementation | pull merge 后的每日时间线最新副本 |
| 2026-06-26 07:39 | manual | docs/adr/ADR-20260626-g1-edu-23dof-primary-profile.md | implementation | grill-with-docs ADR：公司 G1 edu 23DoF 应作为 primary deployment profile，当前 29DoF MJLab smoke 只算 reference evidence |
| 2026-06-26 07:39 | manual | docs/glossary.md | implementation | 新增 robot profile / controller evidence / reference smoke / profile-gated Gate C 术语定义 |
| 2026-06-26 07:39 | manual | docs/g1_edu_23dof_impact_audit.md | implementation | 23DoF 影响审计清单：列出需要修改的文档、配置、脚本、schema、测试和 Gate 状态 |
| 2026-06-26 08:11 | manual | docs/g1_edu_23dof_source_lock.md | implementation | 记录 Unitree 官方 `g1_23dof_rev_1_0.urdf/xml` source、observed commit、SHA256、DoF breakdown 和 URDF joint order |
| 2026-06-26 08:11 | manual | configs/environment.lock.toml | implementation | 新增 `company_g1_edu_23dof` primary profile source lock 和 `mjlab_g1_29dof_reference` reference profile 区分 |
| 2026-06-26 08:11 | manual | AGENTS.md | implementation | 项目规则同步 23DoF primary target 与 29DoF reference-only 边界 |
| 2026-06-26 08:11 | manual | README.md | implementation | README 核心文档和复现说明加入 23DoF source lock 与 29DoF ONNX 不兼容提醒 |
| 2026-06-26 08:11 | manual | docs/research_plan_prd.md | implementation | PRD 初始平台和 V0 定位同步为公司 G1 edu 23DoF primary、29DoF reference backend |
| 2026-06-26 08:11 | manual | docs/gate_a_foundation.md | implementation | Gate A 阻塞字段同步 23DoF source identified 但 adapter/controller smoke pending |
| 2026-06-26 08:11 | manual | docs/mjlab_backend_lock.md | implementation | MJLab backend lock 标明当前 smoke 是 29DoF reference，不是公司 23DoF target evidence |
| 2026-06-26 08:11 | manual | docs/controller_checkpoint_selection.md | implementation | Controller checkpoint 记录标明当前 ONNX 是 29DoF reference candidate，23DoF controller 仍 pending |
| 2026-06-26 08:11 | manual | docs/adr/ADR-20260626-g1-edu-23dof-primary-profile.md | implementation | ADR 更新已回答的 23DoF source/joint-order grilling 问题 |
| 2026-06-26 08:11 | manual | docs/glossary.md | implementation | 术语表更新 `company_g1_edu_23dof` 已有 official source，但 project-local wrapper/controller 仍 pending |
| 2026-06-26 08:11 | manual | docs/g1_edu_23dof_impact_audit.md | implementation | 影响审计从 source unknown 更新为 official source identified |
| 2026-06-26 08:11 | manual | tests/test_gate_a_foundation.py | implementation | 新增测试确保 23DoF primary profile 与 29DoF reference profile 在环境锁中分开记录 |
| 2026-06-26 08:31 | manual | .gitignore | implementation | 排除 `robot_descriptions/`，确保官方 23DoF URDF/MJCF 下载产物不进入 git |
| 2026-06-26 08:31 | manual | scripts/fetch_unitree_g1_23dof_description.sh | implementation | 新增 Unitree G1 edu 23DoF 官方 URDF/MJCF fetch/verify 脚本；固定 source commit 和 SHA256，只写入 git 外路径 |
| 2026-06-26 08:31 | manual | tests/test_fetch_unitree_g1_23dof_description.py | implementation | 测试 23DoF fetch 脚本的 source commit、raw URL、SHA256 和非 checkpoint scope warning |
| 2026-06-26 08:31 | manual | scripts/mjlab_g1_smoke.py | implementation | 为 MJLab G1 smoke 增加 robot profile 和 action/actor/critic dimension gate；默认仍是 29DoF reference smoke |
| 2026-06-26 08:31 | manual | tests/test_mjlab_g1_smoke.py | implementation | 测试 profile/dimension gate，防止 `company_g1_edu_23dof` 复用 29DoF action dim evidence |
| 2026-06-26 08:31 | manual | src/humanoid_locomotion_runtime/schemas.py | implementation | `EpisodeManifest` 新增 robot profile id、DoF、action dim、joint order hash 和 controller profile id |
| 2026-06-26 08:31 | manual | src/humanoid_locomotion_runtime/edp.py | implementation | sample EDP manifest 写入 robot profile metadata，避免 23DoF target 与 29DoF reference episode 混淆 |
| 2026-06-26 08:31 | manual | tests/test_gate_b_schemas.py | implementation | 新增 EpisodeManifest robot profile metadata、legacy defaults、joint order hash 和 metadata leakage 测试 |
| 2026-06-26 08:31 | manual | tests/test_gate_b_edp.py | implementation | 新增 sample EDP manifest robot profile metadata 持久化测试 |
| 2026-06-26 08:31 | manual | refine-logs/EXPERIMENT_PLAN_20260626_083118.md | implementation | 子代理完成 R007b/R007c/R009a 后的实验计划 timestamp copy；R007d/R007e 仍 pending |
| 2026-06-26 08:31 | manual | refine-logs/EXPERIMENT_PLAN.md | implementation | 子代理完成 R007b/R007c/R009a 后的实验计划最新副本 |
| 2026-06-26 08:31 | manual | refine-logs/EXPERIMENT_TRACKER_20260626_083118.md | implementation | 子代理完成 R007b/R007c/R009a 后的 tracker timestamp copy；记录证据和剩余 Gate C 前置项 |
| 2026-06-26 08:31 | manual | refine-logs/EXPERIMENT_TRACKER.md | implementation | 子代理完成 R007b/R007c/R009a 后的 tracker 最新副本 |
| 2026-06-26 08:31 | manual | refine-logs/DAILY_EXPERIMENT_TIMELINE_20260626_083118.md | implementation | 子代理完成 R007b/R007c/R009a 后的每日时间线 timestamp copy；Gate C 前置仍等待 R007d/R007e 或 reference-only 决策 |
| 2026-06-26 08:31 | manual | refine-logs/DAILY_EXPERIMENT_TIMELINE.md | implementation | 子代理完成 R007b/R007c/R009a 后的每日时间线最新副本 |
| 2026-06-26 08:50 | manual | docs/g1_edu_23dof_compile_smoke.md | implementation | R007d 下一步待办清单和完成证据：23DoF URDF/MJCF + 27 mesh assets fetch/verify，MuJoCo 3.10.0 raw compile PASS |
| 2026-06-26 08:50 | manual | scripts/fetch_unitree_g1_23dof_description.sh | implementation | 扩展 23DoF fetch script：拉取并校验 URDF、MJCF 和 27 个官方 STL mesh assets；修复 `git check-ignore` 多路径误报 |
| 2026-06-26 08:50 | manual | scripts/compile_unitree_g1_23dof_description.py | implementation | 新增 R007d raw asset compile smoke 入口；校验 23DoF joint order、`nu=23` 和 MuJoCo compile summary |
| 2026-06-26 08:50 | manual | tests/test_fetch_unitree_g1_23dof_description.py | implementation | 测试 fetch script 的 mesh asset/hash lock 和非 checkpoint scope warning |
| 2026-06-26 08:50 | manual | tests/test_unitree_g1_23dof_compile_smoke.py | implementation | 测试 23DoF compile smoke 脚本可在无 sim extra 下导入，并锁定 floating base + 23 controlled joint order |
| 2026-06-26 08:50 | manual | configs/environment.lock.toml | implementation | `company_g1_edu_23dof` 状态更新为 raw asset compile smoke passed；记录 ignored asset manifest SHA256 和 compile command/result |
| 2026-06-26 08:50 | manual | docs/g1_edu_23dof_source_lock.md | implementation | Source lock 同步 R007d：29 个 ignored assets、asset manifest hash、MuJoCo compile summary 和剩余 MJLab/controller blocker |
| 2026-06-26 08:50 | manual | docs/gate_a_foundation.md | implementation | Gate A 记录同步 23DoF raw asset compile smoke passed，但仍不授权 MJLab adapter/controller/PPO |
| 2026-06-26 08:50 | manual | docs/mjlab_backend_lock.md | implementation | Backend lock 同步 23DoF raw compile smoke；保留 29DoF MJLab smoke 只是 reference evidence 的边界 |
| 2026-06-26 08:50 | manual | docs/controller_checkpoint_selection.md | implementation | Checkpoint 记录同步：R007d raw asset compile 不改变 29DoF ONNX candidate 的 pending-controller-smoke 状态 |
| 2026-06-26 08:50 | manual | docs/research_plan_prd.md | implementation | PRD 同步 23DoF raw asset compile passed、project-local MJLab adapter/controller still pending |
| 2026-06-26 08:50 | manual | docs/adr/ADR-20260626-g1-edu-23dof-primary-profile.md | implementation | ADR 同步 reference-only、Gate C blocked 和 R007d compile smoke completed |
| 2026-06-26 08:50 | manual | docs/g1_edu_23dof_impact_audit.md | implementation | 影响审计同步 R007b/R007c/R007d/R009a 已完成项和剩余 R007e/Gate C blocker |
| 2026-06-26 08:50 | manual | docs/glossary.md | implementation | 术语表补充 23DoF raw MuJoCo asset compile smoke 已完成 |
| 2026-06-26 08:50 | manual | README.md | implementation | README 复现说明加入 23DoF fetch + compile smoke 命令 |
| 2026-06-26 08:50 | manual | tests/test_gate_a_foundation.py | implementation | Gate A 测试同步 23DoF profile status、asset manifest hash 和 compile smoke result |
| 2026-06-26 08:50 | manual | refine-logs/EXPERIMENT_PLAN_20260626_085015.md | implementation | R007d 完成后的实验计划 timestamp copy；R007e 仍 pending |
| 2026-06-26 08:50 | manual | refine-logs/EXPERIMENT_PLAN.md | implementation | R007d 完成后的实验计划最新副本 |
| 2026-06-26 08:50 | manual | refine-logs/EXPERIMENT_TRACKER_20260626_085015.md | implementation | R007d DONE 的 tracker timestamp copy；记录 compile smoke 证据和 R007e 下一步 |
| 2026-06-26 08:50 | manual | refine-logs/EXPERIMENT_TRACKER.md | implementation | R007d DONE 的 tracker 最新副本 |
| 2026-06-26 08:50 | manual | refine-logs/DAILY_EXPERIMENT_TIMELINE_20260626_085015.md | implementation | R007d 完成后的每日时间线 timestamp copy；Gate C 仍等待 R007e 或 reference-only 决策 |
| 2026-06-26 08:50 | manual | refine-logs/DAILY_EXPERIMENT_TIMELINE.md | implementation | R007d 完成后的每日时间线最新副本 |
| 2026-06-26 09:25 | manual | docs/g1_edu_23dof_controller_route.md | implementation | R007e controller route/contract lock：23DoF action dim 23、MJLab flat actor obs 81、deploy-style obs 80，route 为 train_23dof_required |
| 2026-06-26 09:25 | manual | src/humanoid_locomotion_runtime/controller_contracts.py | implementation | 新增轻量 controller/profile contract，记录 23DoF pending controller profile 和 29DoF reference-only profile |
| 2026-06-26 09:25 | manual | src/humanoid_locomotion_runtime/__init__.py | implementation | 导出 controller contract API，便于后续 EDP/adapter 使用同一 profile contract |
| 2026-06-26 09:25 | manual | tests/test_controller_contracts.py | implementation | 测试 R007e 23DoF/29DoF action 和 observation dimensions、joint order hash、reference-only 边界 |
| 2026-06-26 09:25 | manual | tests/test_gate_a_foundation.py | implementation | Gate A 测试同步 R007e controller contract 和 no-mature-controller 状态 |
| 2026-06-26 09:25 | manual | configs/environment.lock.toml | implementation | 环境锁新增 `[controller_contracts.*]` 表，记录 23DoF contract、route 和 29DoF reference-only candidate |
| 2026-06-26 09:25 | manual | docs/controller_checkpoint_selection.md | implementation | Checkpoint 记录同步 R007e：29DoF ONNX 仍 reference-only，23DoF mature controller 需 native training 或 validated conversion |
| 2026-06-26 09:25 | manual | docs/mjlab_backend_lock.md | implementation | Backend lock 同步 23DoF controller contract 和仍待完成的 23DoF wrapper/controller smoke |
| 2026-06-26 09:25 | manual | docs/gate_a_foundation.md | implementation | Gate A 记录同步 R007e route lock，但保持 controller smoke/PPO/rollout 阻塞 |
| 2026-06-26 09:25 | manual | docs/g1_edu_23dof_source_lock.md | implementation | Source lock 同步 R007e：obs/action contract 已记录，native controller 或 validated conversion 仍 pending |
| 2026-06-26 09:25 | manual | docs/g1_edu_23dof_compile_smoke.md | implementation | R007d 文档同步 R007e 已完成，避免旧 TODO 状态误导后续 agent |
| 2026-06-26 09:25 | manual | docs/research_plan_prd.md | implementation | PRD 同步 R007e controller route contract，不改变论文 claim 或实验范围 |
| 2026-06-26 09:25 | manual | README.md | implementation | README 增加 R007e controller route 链接和 23DoF/29DoF shape 边界 |
| 2026-06-26 09:25 | manual | docs/adr/ADR-20260626-g1-edu-23dof-primary-profile.md | implementation | ADR 同步 R007e 已回答 23DoF controller checkpoint 问题 |
| 2026-06-26 09:25 | manual | docs/g1_edu_23dof_impact_audit.md | implementation | 影响审计同步 R007e 已完成，controller-native baseline 仍等待 target smoke 或 reference-only 决策 |
| 2026-06-26 09:25 | manual | docs/glossary.md | implementation | 术语表同步 23DoF obs/action shape contract 已锁定 |
| 2026-06-26 09:25 | manual | refine-logs/EXPERIMENT_TRACKER_20260626_092536.md | implementation | R007e DONE 的 tracker timestamp copy；记录 contract、route 和 controller smoke pending |
| 2026-06-26 09:25 | manual | refine-logs/EXPERIMENT_TRACKER.md | implementation | R007e DONE 的 tracker 最新副本 |
| 2026-06-26 09:25 | manual | refine-logs/EXPERIMENT_PLAN_20260626_092536.md | implementation | R007e 完成后的实验计划 timestamp copy；M0 robot profile contract gate 已满足 |
| 2026-06-26 09:25 | manual | refine-logs/EXPERIMENT_PLAN.md | implementation | R007e 完成后的实验计划最新副本 |
| 2026-06-26 09:25 | manual | refine-logs/DAILY_EXPERIMENT_TIMELINE_20260626_092536.md | implementation | R007e 完成后的每日时间线 timestamp copy；controller smoke 和 baseline 仍 pending |
| 2026-06-26 09:25 | manual | refine-logs/DAILY_EXPERIMENT_TIMELINE.md | implementation | R007e 完成后的每日时间线最新副本 |
| 2026-06-26 09:42 | manual | src/humanoid_locomotion_runtime/recovery_options.py | implementation | R019 recovery option/SMDP contract：8 个 high-level actions 的 initiation/mask/implementation/duration/termination/interrupt/retry/cooldown |
| 2026-06-26 09:42 | manual | src/humanoid_locomotion_runtime/snapshot_branching.py | implementation | R018a snapshot manifest / branch metadata contract；contract-only，不表示 deterministic restore 已完成 |
| 2026-06-26 09:42 | manual | src/humanoid_locomotion_runtime/seed_splits.py | implementation | R016 deterministic seed split helper；生成 tracked seed config，不生成 episodes |
| 2026-06-26 09:42 | manual | scripts/generate_seed_splits.py | implementation | R016 seed split TOML 生成脚本 |
| 2026-06-26 09:42 | manual | configs/failure_protocol.v0.toml | implementation | R010/R010a/R010b 机器可读 failure protocol：cause x temporal taxonomy、state-aliasing cell、privileged boundary |
| 2026-06-26 09:42 | manual | configs/seed_splits.v0.toml | implementation | R016 deterministic dev/train/val/test seed split；状态为 no episode generation |
| 2026-06-26 09:42 | manual | docs/gate_c_option_snapshot_contract.md | implementation | Gate C 记录：R019 DONE、R018a DONE for metadata contract、R018 restore 仍 TODO |
| 2026-06-26 09:42 | manual | docs/failure_protocol_v0.md | implementation | Failure protocol v0 freeze 说明：R010/R010a/R010b/R016 完成边界和仍阻塞 pilots |
| 2026-06-26 09:42 | manual | tests/test_recovery_options.py | implementation | R019 option/SMDP contract 覆盖、字段完整性、duration/retry/cooldown 和 leakage boundary 测试 |
| 2026-06-26 09:42 | manual | tests/test_failure_protocol_config.py | implementation | R010/R010a/R010b protocol config、user_interrupt task-control、state-aliasing cell 测试 |
| 2026-06-26 09:42 | manual | tests/test_snapshot_branching.py | implementation | R018a snapshot/branch metadata schema 和 hash/leakage boundary 测试 |
| 2026-06-26 09:42 | manual | tests/test_seed_splits.py | implementation | R016 deterministic seed split config/script consistency 和 no-overlap 测试 |
| 2026-06-26 09:42 | manual | src/humanoid_locomotion_runtime/schemas.py | implementation | RecoveryActionRecord snapshot hash fields 增加 SHA256 校验，保持 backward compatible |
| 2026-06-26 09:42 | manual | src/humanoid_locomotion_runtime/__init__.py | implementation | 导出 recovery option、snapshot branching 和 seed split API |
| 2026-06-26 09:42 | manual | refine-logs/WEEKEND_LONG_GOAL_ACCEPTANCE_20260629.md | implementation | 周一验收入口：记录 R019/R010/R010a/R010b/R018a/R016 证据、未完成项和验证命令 |
| 2026-06-26 09:42 | manual | refine-logs/EXPERIMENT_TRACKER_20260626_094241.md | implementation | R010/R010a/R010b/R016/R018a/R019 更新后的 tracker timestamp copy |
| 2026-06-26 09:42 | manual | refine-logs/EXPERIMENT_TRACKER.md | implementation | R010/R010a/R010b/R016/R018a/R019 更新后的 tracker 最新副本；R018 仍 TODO |
| 2026-06-26 09:42 | manual | refine-logs/EXPERIMENT_PLAN_20260626_094241.md | implementation | R010/R010a/R010b/R016/R018a/R019 更新后的实验计划 timestamp copy |
| 2026-06-26 09:42 | manual | refine-logs/EXPERIMENT_PLAN.md | implementation | R010/R010a/R010b/R016/R018a/R019 更新后的实验计划最新副本 |
| 2026-06-26 09:42 | manual | refine-logs/DAILY_EXPERIMENT_TIMELINE_20260626_094241.md | implementation | Gate C/Gate D protocol freeze 更新后的每日时间线 timestamp copy |
| 2026-06-26 09:42 | manual | refine-logs/DAILY_EXPERIMENT_TIMELINE.md | implementation | Gate C/Gate D protocol freeze 更新后的每日时间线最新副本 |
| 2026-06-28 13:11 | manual | src/humanoid_locomotion_runtime/snapshot_branching.py | implementation | M-MAC-003：新增 `DecisionEpoch`、`CommonRandomStream`、`SnapshotProvider` protocol、`FakeDeterministicSnapshotProvider` 和 runtime payload hash；fake backend only，不表示 R018 restore 完成 |
| 2026-06-28 13:11 | manual | src/humanoid_locomotion_runtime/runtime_manager.py | implementation | M-MAC-004：新增 Mac-safe `RuntimeManager`、`SafetySupervisor`、`RuntimeCommandEnvelope` 和 `FakeRuntimeBackend` skeleton；不接真实 controller |
| 2026-06-28 13:11 | manual | tests/test_snapshot_branching.py | implementation | M-MAC-003/M-MAC-005：覆盖 fake deterministic restore roundtrip、common random stream contract 和 nested privileged leakage boundary |
| 2026-06-28 13:11 | manual | tests/test_runtime_manager.py | implementation | M-MAC-004/M-MAC-005：覆盖 typed command routing、SafetySupervisor block、fake backend 防绕过和 envelope metadata leakage boundary |
| 2026-06-28 13:11 | manual | docs/gate_c_option_snapshot_contract.md | implementation | Gate C 记录同步 Mac fake restore / RuntimeManager skeleton 证据，同时保留 R018 deterministic restore TODO |
| 2026-06-28 13:11 | manual | refine-logs/MAC_SAFE_WORKLIST.md | implementation | Mac 本机安全工作清单最新副本；M-MAC-001 到 M-MAC-008 已完成，A800-only evidence 边界保留 |
| 2026-06-28 13:11 | manual | refine-logs/MAC_SAFE_WORKLIST_20260628_131100.md | implementation | Mac 本机安全工作清单 timestamp copy |
| 2026-06-28 13:11 | manual | refine-logs/A800_NIGHT_HANDOFF_MAC_SAFE_20260628.md | implementation | M-MAC-006：A800 接手 handoff，覆盖 R018、23DoF controller smoke、R011-R017 pilots 的成功标准和停止条件 |
| 2026-06-28 13:11 | manual | refine-logs/CITATION_AUDIT_20260628.md | implementation | M-MAC-008：高风险近邻文献官方来源核验草案；正式 BibTeX/venue/DOI 精读仍属 R071 |
| 2026-06-28 13:11 | manual | refine-logs/EXPERIMENT_TRACKER.md | implementation | tracker 同步 R018 Mac fake testbed 和 R071 citation audit draft；真实 R018/R071 仍 TODO |
| 2026-06-28 13:11 | manual | refine-logs/EXPERIMENT_TRACKER_20260628_131100.md | implementation | tracker timestamp copy |
| 2026-06-28 13:11 | manual | refine-logs/EXPERIMENT_PLAN.md | implementation | 实验计划同步 Mac/A800 分工和 Gate C fake testbed 证据 |
| 2026-06-28 13:11 | manual | refine-logs/EXPERIMENT_PLAN_20260628_131100.md | implementation | 实验计划 timestamp copy |
| 2026-06-28 13:11 | manual | refine-logs/DAILY_EXPERIMENT_TIMELINE.md | implementation | 每日时间线同步 Mac 工作入口、decision epoch 和 common random stream contract |
| 2026-06-28 13:11 | manual | refine-logs/DAILY_EXPERIMENT_TIMELINE_20260628_131100.md | implementation | 每日时间线 timestamp copy |
| 2026-06-28 17:10 | manual | src/humanoid_locomotion_runtime/grounding_memory.py | implementation | M-MAC-009：controlled detector-like grounding adapter 与 TemporaryObjectMemory skeleton；runtime-legal only，不表示真实 detector evidence |
| 2026-06-28 17:10 | manual | src/humanoid_locomotion_runtime/navigator.py | implementation | M-MAC-010：NavigatorV0 纯几何 local planner skeleton；blocked route 产出 FailureEvent，不表示 MPC/controller smoke evidence |
| 2026-06-28 17:10 | manual | src/humanoid_locomotion_runtime/dashboard.py | implementation | M-MAC-011：dashboard/replay in-memory publisher skeleton；只允许 high-level command surface，不控制 low-level joints |
| 2026-06-28 17:10 | manual | src/humanoid_locomotion_runtime/analysis.py | implementation | M-MAC-012：stable run id naming、DecisionFlipRecord、decision pair matching 和 flip-rate helper |
| 2026-06-28 17:10 | manual | tests/test_grounding_memory.py | implementation | M-MAC-009 tests：target selection、TTL query/expiry、snapshot payload 和 privileged leakage rejection |
| 2026-06-28 17:10 | manual | tests/test_navigator.py | implementation | M-MAC-010 tests：direct route、single-obstacle detour、blocked route failure event 和 privileged obstacle metadata rejection |
| 2026-06-28 17:10 | manual | tests/test_dashboard.py | implementation | M-MAC-011 tests：dashboard summary、high-level command creation、low-level metadata rejection 和 leakage boundary |
| 2026-06-28 17:10 | manual | tests/test_analysis.py | implementation | M-MAC-012 tests：run id format、matched decision flips、required decision metadata 和 leakage boundary |
| 2026-06-28 17:10 | manual | refine-logs/STATISTICAL_DESIGN_FREEZE_20260628.md | implementation | M-MAC-013 / R047a：统计设计草案，冻结 endpoint、seed、bootstrap、multiplicity 和 SEI 字段；final R047 仍 pending |
| 2026-06-28 17:10 | manual | refine-logs/MAC_SAFE_WORKLIST.md | implementation | Mac 本机安全工作清单最新副本；新增 M-MAC-009 到 M-MAC-013，并更新全量验证结果 |
| 2026-06-28 17:10 | manual | refine-logs/MAC_SAFE_WORKLIST_20260628_171025.md | implementation | Mac 本机安全工作清单 timestamp copy |
| 2026-06-28 17:10 | manual | refine-logs/EXPERIMENT_TRACKER.md | implementation | tracker 同步 R009b/R034a/R047a；真实 R034/R047 仍 TODO |
| 2026-06-28 17:10 | manual | refine-logs/EXPERIMENT_TRACKER_20260628_171025.md | implementation | tracker timestamp copy |
| 2026-06-28 17:10 | manual | refine-logs/EXPERIMENT_PLAN.md | implementation | 实验计划同步新增 Mac-safe skeleton 和 R047a 边界 |
| 2026-06-28 17:10 | manual | refine-logs/EXPERIMENT_PLAN_20260628_171025.md | implementation | 实验计划 timestamp copy |
| 2026-06-28 17:10 | manual | refine-logs/DAILY_EXPERIMENT_TIMELINE.md | implementation | 每日时间线同步 run id、decision pair matching 和 Mac/A800 验收边界 |
| 2026-06-28 17:10 | manual | refine-logs/DAILY_EXPERIMENT_TIMELINE_20260628_171025.md | implementation | 每日时间线 timestamp copy |
| 2026-06-28 17:10 | manual | README.md | implementation | README 主机分工同步新增 Mac-safe skeleton 与 A800-only evidence boundary |
| 2026-06-28 17:52 | /research-lit | refine-logs/LITERATURE_CANDIDATES_20260628.json | research | R048/R071a 文献驱动实验设计候选论文清单；9/10 后续由 verifier 或官方页面支撑 |
| 2026-06-28 17:52 | /research-lit | refine-logs/LITERATURE_VERIFICATION_20260628.json | research | ARIS `verify_papers.py` 输出；9 篇 arXiv high-confidence，FLARE 仍 verify_pending，hallucination_rate 0.0 |
| 2026-06-28 17:52 | /research-lit | refine-logs/LITERATURE_INFORMED_EXPERIMENT_DESIGN.md | research | R048/R071a 最新副本：按 failure recovery、humanoid/legged locomotion、navigation、memory/map 和 monitor 文献改进指标、baseline 和 gate |
| 2026-06-28 17:52 | /research-lit | refine-logs/LITERATURE_INFORMED_EXPERIMENT_DESIGN_20260628_175221.md | research | R048/R071a timestamp copy |
| 2026-06-28 17:52 | /research-lit | refine-logs/EXPERIMENT_PLAN.md | implementation | 实验计划同步 literature-informed metric/baseline audit，新增 R028/R029/R048/R071a 边界；真实 rollout 仍 TODO |
| 2026-06-28 17:52 | /research-lit | refine-logs/EXPERIMENT_PLAN_20260628_175221.md | implementation | 实验计划 timestamp copy |
| 2026-06-28 17:52 | /research-lit | refine-logs/EXPERIMENT_TRACKER.md | implementation | tracker 新增 R028 safety monitor baseline、R029 causal transformer raw-history baseline、R048/R071a 完成证据 |
| 2026-06-28 17:52 | /research-lit | refine-logs/EXPERIMENT_TRACKER_20260628_175221.md | implementation | tracker timestamp copy |
| 2026-06-28 17:52 | /research-lit | refine-logs/DAILY_EXPERIMENT_TIMELINE.md | implementation | 每日时间线同步新增 safety monitor、causal transformer raw-history 和文献驱动指标 |
| 2026-06-28 17:52 | /research-lit | refine-logs/DAILY_EXPERIMENT_TIMELINE_20260628_175221.md | implementation | 每日时间线 timestamp copy |
| 2026-06-29 03:05 | manual | .gitmodules | implementation | 新增 repo-local 官方 Unitree RL MJLab 子模块，用于 company G1 edu 23DoF controller training framework |
| 2026-06-29 03:05 | manual | third_party/unitree_rl_mjlab | implementation | 官方 Unitree RL MJLab submodule，锁定 `1425b15f73bd4095f0df53709d7c389c3eb9e790`；训练产物仍保持 git 外 |
| 2026-06-29 03:05 | manual | scripts/setup_unitree_g1_23dof_training.sh | implementation | 当前仓库内 23DoF controller training 环境检查脚本：默认复用 mamba env `robot`，不直接新建虚拟环境，列出 `Unitree-G1-23Dof-Flat` |
| 2026-06-29 03:05 | manual | scripts/run_unitree_g1_23dof_training.sh | implementation | 当前仓库内 23DoF RSL-RL 训练入口的初始脚本；默认 mamba env `robot`、tensorboard/no-wandb-upload；后续 04:45 记录将默认参数改为正式训练规模 |
| 2026-06-29 03:05 | manual | scripts/unitree_train_mamba_wrapper.py | implementation | 当前仓库内 Unitree train wrapper；复用 mamba env 时兼容旧 torch 不支持 `torch.onnx.export(dynamo=...)` |
| 2026-06-29 03:05 | manual | docs/g1_edu_23dof_training_framework.md | implementation | 23DoF controller 自训框架说明；明确复用 mamba env 和 training smoke 不等于 controller evidence |
| 2026-06-29 03:05 | manual | refine-logs/G1_23DOF_CONTROLLER_TRAINING_FRAMEWORK_20260629.md | implementation | 23DoF controller 自训框架当日 handoff/checklist |
| 2026-06-29 03:05 | manual | tests/test_unitree_g1_23dof_training_framework.py | implementation | 锁定训练框架必须在当前 repo 下，禁止回退到 `/mnt/nvme2n1p1` 外部训练目录 |
| 2026-06-29 03:05 | manual | pyproject.toml | implementation | Ruff 排除官方 `third_party/unitree_rl_mjlab` submodule，避免把外部依赖代码当成本仓库 lint 目标 |
| 2026-06-29 04:45 | manual | scripts/run_unitree_g1_23dof_training.sh | implementation | 将 23DoF RSL-RL 入口从 smoke 脚本改为正式训练脚本；默认 `4096 envs / 10001 iterations / save_interval=500`，仍不提交 raw logs、checkpoints、ONNX 或 tfevents |
| 2026-06-29 04:45 | manual | docs/g1_edu_23dof_training_framework.md | implementation | 同步正式训练入口命令和验收边界；短 sanity run 只能通过显式覆盖参数触发 |
| 2026-06-29 04:45 | manual | refine-logs/G1_23DOF_CONTROLLER_TRAINING_FRAMEWORK_20260629.md | implementation | 当日 handoff 同步正式训练脚本、后台训练入口和次日验收项 |
| 2026-06-30 03:00 | manual | refine-logs/G1_23DOF_CONTROLLER_TRAINING_ACCEPTANCE_20260630.md | implementation | 23DoF full-training candidate 验收 timestamp copy；记录 accepted run、ignored raw paths、最终训练指标和 controller-smoke 边界 |
| 2026-06-30 03:00 | manual | refine-logs/G1_23DOF_CONTROLLER_TRAINING_ACCEPTANCE.md | implementation | 23DoF full-training candidate 验收 latest copy |
| 2026-06-30 03:00 | manual | docs/g1_edu_23dof_training_framework.md | implementation | 同步 2026-06-29 full-training candidate 记录；仍保持 play/controller smoke pending |
| 2026-06-30 03:00 | manual | refine-logs/G1_23DOF_CONTROLLER_TRAINING_FRAMEWORK_20260629.md | implementation | 同步 2026-06-30 验收摘要和下一步 play/controller smoke |
| 2026-06-30 03:00 | manual | refine-logs/EXPERIMENT_TRACKER.md | implementation | tracker 同步 23DoF full-training candidate 已产出，但 mature controller evidence 仍 pending |
| 2026-06-30 03:00 | manual | refine-logs/EXPERIMENT_PLAN.md | implementation | 实验计划同步 candidate 已产出和 controller-smoke gate 边界 |
| 2026-06-30 03:00 | manual | refine-logs/DAILY_EXPERIMENT_TIMELINE.md | implementation | 每日时间线同步 candidate 验收、play 回放和 project-local smoke 下一步 |
| 2026-06-30 03:00 | manual | .gitmodules | implementation | 为 `third_party/unitree_rl_mjlab` 设置 `ignore = untracked`，避免训练缓存/log 副产物污染父仓库状态 |
| 2026-06-30 03:53 | manual | AGENTS.md | implementation | 明确 23DoF locomotion controller 训练是 Gate C 前置 bootstrap 例外，并记录最多 3 张空闲 GPU、默认 1 个 4096-env job/GPU 的并发规则 |
| 2026-06-30 03:53 | manual | src/humanoid_locomotion_runtime/unitree_g1_23dof_profiles.py | implementation | 新增 repo-local `Unitree-G1-23Dof-ForwardFlat` 和 `Unitree-G1-23Dof-VelocityBalancedFlat` task profiles；不修改 Unitree submodule tracked source |
| 2026-06-30 03:53 | manual | scripts/unitree_train_mamba_wrapper.py | implementation | 训练 wrapper 在进入 upstream `train.py` 前注册 repo-local 23DoF controller profiles，并保持旧 torch ONNX export 兼容 patch |
| 2026-06-30 03:53 | manual | scripts/setup_unitree_g1_23dof_training.sh | implementation | 环境检查脚本同步加载 repo-local profiles，列出新增 23DoF task choices |
| 2026-06-30 03:53 | manual | scripts/run_unitree_g1_23dof_training.sh | implementation | 默认 task 切到 `Unitree-G1-23Dof-VelocityBalancedFlat`，新增 `SEED` 透传和 `save_interval=250`，用于 checkpoint selection |
| 2026-06-30 03:53 | manual | scripts/eval_unitree_g1_23dof_command_grid.py | implementation | 新增 23DoF checkpoint command-grid eval：stand/forward/yaw/lateral，输出 ignored JSON metrics，不提交 raw eval artifacts |
| 2026-06-30 03:53 | manual | tests/test_unitree_g1_23dof_training_framework.py | implementation | 覆盖 repo-local profile registration、balanced default task、seed 透传和 command-grid eval script presence |
| 2026-06-30 03:53 | manual | docs/g1_edu_23dof_training_framework.md | implementation | 同步官方 29DoF policy 对 23DoF controller 改进的参考结论、repo-local task、eval 脚本和 Stage A/B/C 路线 |
| 2026-06-30 03:53 | manual | refine-logs/G1_23DOF_CONTROLLER_POLICY_IMPROVEMENT_TODO.md | implementation | 23DoF controller policy-improvement latest checklist：直行验收、velocity-balanced controller、command-grid selection 和 Gate C 条件 |
| 2026-06-30 03:53 | manual | refine-logs/G1_23DOF_CONTROLLER_POLICY_IMPROVEMENT_TODO_20260630.md | implementation | 23DoF controller policy-improvement timestamp copy |
| 2026-06-30 03:53 | manual | refine-logs/G1_23DOF_CONTROLLER_STAGE_A_HANDOFF_20260630.md | implementation | Stage A ForwardFlat multi-seed handoff：seeds 101/102/103 on GPUs 1/2/3，raw logs/checkpoints 仍保持 ignored |
| 2026-06-30 03:53 | manual | refine-logs/G1_23DOF_CONTROLLER_TRAINING_ACCEPTANCE.md | implementation | full-training candidate 验收 latest copy 同步用户观察到 `model_4500.pt` 斜走后的后续 policy-improvement 处理 |
| 2026-06-30 03:53 | manual | refine-logs/G1_23DOF_CONTROLLER_TRAINING_ACCEPTANCE_20260630.md | implementation | full-training candidate 验收 timestamp copy 同步斜走后续处理 |
| 2026-06-30 03:53 | manual | refine-logs/EXPERIMENT_TRACKER.md | implementation | tracker 新增 R007f-R007j；R007f DONE，R007g Stage A ForwardFlat multi-seed IN_PROGRESS |
| 2026-06-30 03:53 | manual | refine-logs/EXPERIMENT_PLAN.md | implementation | experiment plan 同步 Gate C controller bootstrap 例外、R007f 完成、R007g 启动和后续 eval/smoke 停止条件 |
| 2026-06-30 03:53 | manual | refine-logs/DAILY_EXPERIMENT_TIMELINE.md | implementation | daily timeline 同步 2026-06-30 controller policy-improvement scaffold、GPU 并发规则和次日验收项 |
| 2026-06-30 04:02 | manual | refine-logs/G1_23DOF_CONTROLLER_STAGE_A_HANDOFF_20260630.md | implementation | Stage A handoff 增补 `model_250.pt` 三 seed command-grid 中途 eval 结果；明确早期 checkpoint 不合格且不算 mature controller evidence |
| 2026-06-30 04:02 | manual | refine-logs/G1_23DOF_CONTROLLER_POLICY_IMPROVEMENT_TODO.md | implementation | policy-improvement TODO 增补 Stage A `model_250.pt` 中途 eval 已完成但不合格，后续仍需更后期 checkpoint selection |
| 2026-06-30 04:02 | manual | refine-logs/G1_23DOF_CONTROLLER_POLICY_IMPROVEMENT_TODO_20260630.md | implementation | policy-improvement TODO timestamp copy 同步中途 eval 结果 |
| 2026-06-30 04:02 | manual | refine-logs/EXPERIMENT_TRACKER.md | implementation | tracker 同步 R007g 训练进度和 R007i 中途 eval `IN_PROGRESS`；ignored eval JSON 不进 git |
| 2026-06-30 04:02 | manual | refine-logs/EXPERIMENT_PLAN.md | implementation | experiment plan 同步 Stage A `model_250.pt` command-grid sanity 已完成但不构成 mature controller evidence |
| 2026-06-30 04:02 | manual | refine-logs/DAILY_EXPERIMENT_TIMELINE.md | implementation | daily timeline 同步 04:00 UTC 中途 eval 完成、训练仍未完成、Gate C 不推进 |
| 2026-06-30 04:13 | manual | scripts/eval_unitree_g1_23dof_command_grid.py | implementation | 修复并发 command-grid eval JSON 文件名碰撞；输出名加入 task、run directory、checkpoint stem、seed 和 timestamp |
| 2026-06-30 04:13 | manual | tests/test_unitree_g1_23dof_training_framework.py | implementation | 增加 eval 输出命名防回归检查，覆盖 seed/checkpoint/run directory 字段 |
| 2026-06-30 04:13 | manual | docs/g1_edu_23dof_training_framework.md | implementation | 训练框架文档同步并发 eval 命名规则，以及 `model_250.pt` / `model_500.pt` 中途 eval 不构成 mature evidence |
| 2026-06-30 04:13 | manual | refine-logs/G1_23DOF_CONTROLLER_STAGE_A_HANDOFF_20260630.md | implementation | handoff 增补 `model_500.pt` 三 seed command-grid eval 结果和输出命名修复；`model_500.pt` 仍不达 mature controller gate |
| 2026-06-30 04:13 | manual | refine-logs/G1_23DOF_CONTROLLER_POLICY_IMPROVEMENT_TODO.md | implementation | policy-improvement TODO 同步 eval filename collision fix 和 `model_500.pt` 中途 eval 趋势 |
| 2026-06-30 04:13 | manual | refine-logs/G1_23DOF_CONTROLLER_POLICY_IMPROVEMENT_TODO_20260630.md | implementation | policy-improvement TODO timestamp copy 同步 `model_500.pt` eval |
| 2026-06-30 04:13 | manual | refine-logs/EXPERIMENT_TRACKER.md | implementation | tracker 同步 R007i `model_500.pt` eval 和并发 eval 输出命名修复，Gate C 仍不推进 |
| 2026-06-30 04:13 | manual | refine-logs/EXPERIMENT_PLAN.md | implementation | experiment plan 同步 R007i eval reliability fix 和 `model_500.pt` 中途趋势 |
| 2026-06-30 04:13 | manual | refine-logs/DAILY_EXPERIMENT_TIMELINE.md | implementation | daily timeline 同步 `model_500.pt` eval 已完成但 lateral drift 未过 gate |
| 2026-06-30 04:20 | manual | docs/g1_edu_23dof_training_framework.md | implementation | 训练框架文档同步 Stage A `model_1000.pt` 中途 eval；趋势改善但不构成 mature evidence |
| 2026-06-30 04:20 | manual | refine-logs/G1_23DOF_CONTROLLER_STAGE_A_HANDOFF_20260630.md | implementation | handoff 增补 `model_1000.pt` 三 seed command-grid eval 结果；forward drift 改善但 lateral command 仍不稳 |
| 2026-06-30 04:20 | manual | refine-logs/G1_23DOF_CONTROLLER_POLICY_IMPROVEMENT_TODO.md | implementation | policy-improvement TODO 同步 `model_1000.pt` 中途 eval 仍未过 mature controller gate |
| 2026-06-30 04:20 | manual | refine-logs/G1_23DOF_CONTROLLER_POLICY_IMPROVEMENT_TODO_20260630.md | implementation | policy-improvement TODO timestamp copy 同步 `model_1000.pt` eval |
| 2026-06-30 04:20 | manual | refine-logs/EXPERIMENT_TRACKER.md | implementation | tracker 同步 R007i `model_1000.pt` command-grid eval 结果，R007g/R007i 仍 IN_PROGRESS |
| 2026-06-30 04:20 | manual | refine-logs/EXPERIMENT_PLAN.md | implementation | experiment plan 同步 `model_1000.pt` 中途 eval 结果和继续 eval 后期 checkpoint 的要求 |
| 2026-06-30 04:20 | manual | refine-logs/DAILY_EXPERIMENT_TIMELINE.md | implementation | daily timeline 同步 `model_1000.pt` eval 已完成但 lateral drift 未过 gate |
| 2026-06-30 04:35 | manual | scripts/summarize_unitree_g1_23dof_eval.py | implementation | 新增 command-grid eval JSON 汇总脚本，输出 checkpoint/seed 指标和 simple triage penalty；不替代 Gate C acceptance |
| 2026-06-30 04:35 | manual | tests/test_unitree_g1_23dof_training_framework.py | implementation | 覆盖 eval summary script 的关键字段：`selection_penalty`、forward fast lateral drift 和 lateral done fraction |
| 2026-06-30 04:35 | manual | docs/g1_edu_23dof_training_framework.md | implementation | 训练框架文档同步 eval summary script，以及 Stage A `model_1250.pt` / `model_1500.pt` 中途 eval 不构成 mature evidence |
| 2026-06-30 04:35 | manual | refine-logs/G1_23DOF_CONTROLLER_STAGE_A_HANDOFF_20260630.md | implementation | handoff 增补 `model_1250.pt` / `model_1500.pt` 三 seed command-grid eval 结果和 summary script |
| 2026-06-30 04:35 | manual | refine-logs/G1_23DOF_CONTROLLER_POLICY_IMPROVEMENT_TODO.md | implementation | policy-improvement TODO 同步 `model_1250.pt` / `model_1500.pt` eval 和 summary script |
| 2026-06-30 04:35 | manual | refine-logs/G1_23DOF_CONTROLLER_POLICY_IMPROVEMENT_TODO_20260630.md | implementation | policy-improvement TODO timestamp copy 同步 `model_1250.pt` / `model_1500.pt` eval |
| 2026-06-30 04:35 | manual | refine-logs/EXPERIMENT_TRACKER.md | implementation | tracker 同步 R007i 已 eval 到 `model_1500.pt`，R007g/R007i 仍 IN_PROGRESS |
| 2026-06-30 04:35 | manual | refine-logs/EXPERIMENT_PLAN.md | implementation | experiment plan 同步 `model_1250.pt` / `model_1500.pt` eval 结果和 summary script |
| 2026-06-30 04:35 | manual | refine-logs/DAILY_EXPERIMENT_TIMELINE.md | implementation | daily timeline 同步 eval 已推进到 `model_1500.pt`，lateral drift 未过 gate |
| 2026-06-30 04:43 | manual | docs/g1_edu_23dof_training_framework.md | implementation | 训练框架文档同步 Stage A `model_2000.pt` 中途 eval；目前最好但 cross-seed straight drift 仍未达标 |
| 2026-06-30 04:43 | manual | refine-logs/G1_23DOF_CONTROLLER_STAGE_A_HANDOFF_20260630.md | implementation | handoff 增补 `model_2000.pt` 三 seed command-grid eval 结果；仍不构成 mature controller evidence |
| 2026-06-30 04:43 | manual | refine-logs/G1_23DOF_CONTROLLER_POLICY_IMPROVEMENT_TODO.md | implementation | policy-improvement TODO 同步 `model_2000.pt` 当前最佳中途点但未过 gate |
| 2026-06-30 04:43 | manual | refine-logs/G1_23DOF_CONTROLLER_POLICY_IMPROVEMENT_TODO_20260630.md | implementation | policy-improvement TODO timestamp copy 同步 `model_2000.pt` eval |
| 2026-06-30 04:43 | manual | refine-logs/EXPERIMENT_TRACKER.md | implementation | tracker 同步 R007i 已 eval 到 `model_2000.pt`，R007g/R007i 仍 IN_PROGRESS |
| 2026-06-30 04:43 | manual | refine-logs/EXPERIMENT_PLAN.md | implementation | experiment plan 同步 `model_2000.pt` 中途 eval 结果 |
| 2026-06-30 04:43 | manual | refine-logs/DAILY_EXPERIMENT_TIMELINE.md | implementation | daily timeline 同步 `model_2000.pt` eval 已完成但未过 mature controller gate |
| 2026-06-30 04:54 | manual | scripts/summarize_unitree_g1_23dof_eval.py | implementation | eval summary script 增加 `--group-by checkpoint`，支持 multi-seed 聚合排序 |
| 2026-06-30 04:54 | manual | tests/test_unitree_g1_23dof_training_framework.py | implementation | 测试同步覆盖 eval summary 聚合模式关键字段 |
| 2026-06-30 04:54 | manual | docs/g1_edu_23dof_training_framework.md | implementation | 训练框架文档同步 Stage A `model_2500.pt` eval 和 checkpoint 聚合 summary |
| 2026-06-30 04:54 | manual | refine-logs/G1_23DOF_CONTROLLER_STAGE_A_HANDOFF_20260630.md | implementation | handoff 增补 `model_2500.pt` 三 seed command-grid eval 结果；当前聚合最好但仍未过 gate |
| 2026-06-30 04:54 | manual | refine-logs/G1_23DOF_CONTROLLER_POLICY_IMPROVEMENT_TODO.md | implementation | policy-improvement TODO 同步 `model_2500.pt` eval 和 summary 聚合模式 |
| 2026-06-30 04:54 | manual | refine-logs/G1_23DOF_CONTROLLER_POLICY_IMPROVEMENT_TODO_20260630.md | implementation | policy-improvement TODO timestamp copy 同步 `model_2500.pt` eval |
| 2026-06-30 04:54 | manual | refine-logs/EXPERIMENT_TRACKER.md | implementation | tracker 同步 R007i 已 eval 到 `model_2500.pt`，R007g/R007i 仍 IN_PROGRESS |
| 2026-06-30 04:54 | manual | refine-logs/EXPERIMENT_PLAN.md | implementation | experiment plan 同步 `model_2500.pt` 中途 eval 和 multi-seed aggregation |
| 2026-06-30 04:54 | manual | refine-logs/DAILY_EXPERIMENT_TIMELINE.md | implementation | daily timeline 同步 `model_2500.pt` eval 已完成但未过 mature controller gate |
| 2026-06-30 05:12 | manual | docs/g1_edu_23dof_training_framework.md | implementation | 训练框架文档同步 Stage A `model_3000.pt` eval；聚合略弱于 `model_2500.pt`，仍未过 mature controller gate |
| 2026-06-30 05:12 | manual | refine-logs/G1_23DOF_CONTROLLER_STAGE_A_HANDOFF_20260630.md | implementation | handoff 已记录 `model_3000.pt` 三 seed command-grid eval 结果；不构成 mature controller evidence |
| 2026-06-30 05:12 | manual | refine-logs/G1_23DOF_CONTROLLER_POLICY_IMPROVEMENT_TODO.md | implementation | policy-improvement TODO 同步 `model_3000.pt` eval 和后续 checkpoint selection 范围 |
| 2026-06-30 05:12 | manual | refine-logs/G1_23DOF_CONTROLLER_POLICY_IMPROVEMENT_TODO_20260630.md | implementation | policy-improvement TODO timestamp copy 同步 `model_3000.pt` eval |
| 2026-06-30 05:12 | manual | refine-logs/EXPERIMENT_TRACKER.md | implementation | tracker 同步 R007i 已 eval 到 `model_3000.pt`，R007g/R007i 仍 IN_PROGRESS |
| 2026-06-30 05:12 | manual | refine-logs/EXPERIMENT_PLAN.md | implementation | experiment plan 同步 `model_3000.pt` eval 结果和 `model_2500.pt` 当前最佳聚合判断 |
| 2026-06-30 05:12 | manual | refine-logs/DAILY_EXPERIMENT_TIMELINE.md | implementation | daily timeline 同步 `model_3000.pt` eval 已完成但未过 mature controller gate |
| 2026-06-30 05:18 | manual | docs/g1_edu_23dof_training_framework.md | implementation | 训练框架文档同步 Stage A `model_3500.pt` eval；mean lateral 改善但 worst-case lateral drift 和 lateral commands 仍未过 gate |
| 2026-06-30 05:18 | manual | refine-logs/G1_23DOF_CONTROLLER_STAGE_A_HANDOFF_20260630.md | implementation | handoff 增补 `model_3500.pt` 三 seed command-grid eval 结果；仍不构成 mature controller evidence |
| 2026-06-30 05:18 | manual | refine-logs/G1_23DOF_CONTROLLER_POLICY_IMPROVEMENT_TODO.md | implementation | policy-improvement TODO 同步 `model_3500.pt` eval 和 command-bin/cross-axis reward 下一步判断 |
| 2026-06-30 05:18 | manual | refine-logs/G1_23DOF_CONTROLLER_POLICY_IMPROVEMENT_TODO_20260630.md | implementation | policy-improvement TODO timestamp copy 同步 `model_3500.pt` eval |
| 2026-06-30 05:18 | manual | refine-logs/EXPERIMENT_TRACKER.md | implementation | tracker 同步 R007i 已 eval 到 `model_3500.pt`，R007g/R007i 仍 IN_PROGRESS |
| 2026-06-30 05:18 | manual | refine-logs/EXPERIMENT_PLAN.md | implementation | experiment plan 同步 `model_3500.pt` eval 结果和仍无 mature evidence 的 gate 判断 |
| 2026-06-30 05:18 | manual | refine-logs/DAILY_EXPERIMENT_TIMELINE.md | implementation | daily timeline 同步 `model_3500.pt` eval 已完成但未过 mature controller gate |
| 2026-06-30 05:20 | manual | src/humanoid_locomotion_runtime/unitree_g1_23dof_profiles.py | implementation | 新增 `command_axis_leakage_penalty` reward term，用于惩罚命令静默轴上的实际速度串扰 |
| 2026-06-30 05:20 | manual | tests/test_unitree_g1_23dof_training_framework.py | test | 覆盖 repo-local profile 包含 `command_axis_leakage_penalty` / `command_axis_leakage` |
| 2026-06-30 05:20 | manual | docs/g1_edu_23dof_training_framework.md | implementation | 训练框架文档同步 cross-axis leakage reward 改动，说明该改动服务后续新 run |
| 2026-06-30 05:20 | manual | refine-logs/G1_23DOF_CONTROLLER_POLICY_IMPROVEMENT_TODO.md | implementation | policy-improvement TODO 同步 cross-axis leakage reward 已落地，command-bin sampler 仍 pending |
| 2026-06-30 05:20 | manual | refine-logs/G1_23DOF_CONTROLLER_POLICY_IMPROVEMENT_TODO_20260630.md | implementation | policy-improvement TODO timestamp copy 同步 cross-axis leakage reward |
| 2026-06-30 05:20 | manual | refine-logs/EXPERIMENT_TRACKER.md | implementation | tracker 同步 R007f follow-up reward 改动，R007g/R007i 仍 IN_PROGRESS |
| 2026-06-30 05:20 | manual | refine-logs/EXPERIMENT_PLAN.md | implementation | experiment plan 同步 R007f follow-up reward 改动 |
| 2026-06-30 05:20 | manual | refine-logs/DAILY_EXPERIMENT_TIMELINE.md | implementation | daily timeline 同步 05:20 UTC cross-axis leakage reward 改动 |
| 2026-06-30 05:22 | manual | runs/unitree_g1_23dof_eval/*model_3500_seed999*.json | ignored-artifact | 2 env / 2 step command-grid smoke 确认 `command_axis_leakage` reward 进入 RewardManager；raw JSON 仍保持 ignored |
| 2026-06-30 05:22 | manual | docs/g1_edu_23dof_training_framework.md | implementation | 训练框架文档同步 cross-axis reward smoke，actor/action contract 仍为 `80 -> 23` |
| 2026-06-30 05:22 | manual | refine-logs/G1_23DOF_CONTROLLER_POLICY_IMPROVEMENT_TODO.md | implementation | policy-improvement TODO 同步 cross-axis reward smoke 结果 |
| 2026-06-30 05:22 | manual | refine-logs/G1_23DOF_CONTROLLER_POLICY_IMPROVEMENT_TODO_20260630.md | implementation | policy-improvement TODO timestamp copy 同步 cross-axis reward smoke |
| 2026-06-30 05:22 | manual | refine-logs/EXPERIMENT_TRACKER.md | implementation | tracker 同步 R007f follow-up smoke 结果 |
| 2026-06-30 05:22 | manual | refine-logs/EXPERIMENT_PLAN.md | implementation | experiment plan 同步 cross-axis reward smoke 结果 |
| 2026-06-30 05:22 | manual | refine-logs/DAILY_EXPERIMENT_TIMELINE.md | implementation | daily timeline 同步 05:22 UTC cross-axis reward smoke |
| 2026-06-30 05:27 | manual | scripts/summarize_unitree_g1_23dof_eval.py | implementation | eval summary 增加 `--include-seeds`，避免 smoke seed JSON 污染正式 checkpoint 聚合 |
| 2026-06-30 05:27 | manual | tests/test_unitree_g1_23dof_training_framework.py | test | 覆盖 summary script 暴露 `--include-seeds` seed allowlist |
| 2026-06-30 05:27 | manual | refine-logs/G1_23DOF_CONTROLLER_STAGE_A_HANDOFF_20260630.md | implementation | handoff 增补 `model_4000.pt` 三 seed eval；fixed-forward 指标最好但 lateral/yaw commands 仍未过 gate |
| 2026-06-30 05:27 | manual | docs/g1_edu_23dof_training_framework.md | implementation | 训练框架文档同步 Stage A `model_4000.pt` eval 和 `--include-seeds` 聚合修正 |
| 2026-06-30 05:27 | manual | refine-logs/G1_23DOF_CONTROLLER_POLICY_IMPROVEMENT_TODO.md | implementation | policy-improvement TODO 同步 `model_4000.pt` eval 和后续 checkpoint selection 范围 |
| 2026-06-30 05:27 | manual | refine-logs/G1_23DOF_CONTROLLER_POLICY_IMPROVEMENT_TODO_20260630.md | implementation | policy-improvement TODO timestamp copy 同步 `model_4000.pt` eval |
| 2026-06-30 05:27 | manual | refine-logs/EXPERIMENT_TRACKER.md | implementation | tracker 同步 R007i 已 eval 到 `model_4000.pt`，R007g/R007i 仍 IN_PROGRESS |
| 2026-06-30 05:27 | manual | refine-logs/EXPERIMENT_PLAN.md | implementation | experiment plan 同步 `model_4000.pt` eval 结果 |
| 2026-06-30 05:27 | manual | refine-logs/DAILY_EXPERIMENT_TIMELINE.md | implementation | daily timeline 同步 `model_4000.pt` eval 已完成但未过 mature controller gate |
| 2026-06-30 05:37 | manual | runs/unitree_g1_23dof_eval/*model_4500_seed*.json | ignored-artifact | Stage A `model_4500.pt` 三 seed command-grid eval 完成；raw JSON 仍保持 ignored |
| 2026-06-30 05:38 | manual | src/humanoid_locomotion_runtime/unitree_g1_23dof_profiles.py | implementation | 新增 binned velocity command sampler，Stage A 覆盖 stand/straight 速度段，Stage B 覆盖 stand/straight/yaw-only/lateral-only/combined |
| 2026-06-30 05:38 | manual | scripts/eval_unitree_g1_23dof_command_grid.py | implementation | command-grid eval 在 binned sampler profile 下用 single locked eval bin 固定命令，避免 eval command 被训练采样器重采样 |
| 2026-06-30 05:38 | manual | tests/test_unitree_g1_23dof_training_framework.py | test | 覆盖 binned command sampler symbols 和 Stage B command bins |
| 2026-06-30 05:38 | manual | refine-logs/G1_23DOF_CONTROLLER_STAGE_A_HANDOFF_20260630.md | implementation | handoff 增补 `model_4500.pt` 三 seed eval；略弱于 `model_4000.pt` 且仍未过 mature controller gate |
| 2026-06-30 05:38 | manual | docs/g1_edu_23dof_training_framework.md | implementation | 训练框架文档同步 binned command sampler 和 `model_4500.pt` eval 结果 |
| 2026-06-30 05:38 | manual | refine-logs/G1_23DOF_CONTROLLER_POLICY_IMPROVEMENT_TODO.md | implementation | policy-improvement TODO 同步 command-bin sampler 已落地和 `model_4500.pt` eval 结果 |
| 2026-06-30 05:38 | manual | refine-logs/G1_23DOF_CONTROLLER_POLICY_IMPROVEMENT_TODO_20260630.md | implementation | policy-improvement TODO timestamp copy 同步 command-bin sampler 和 `model_4500.pt` eval |
| 2026-06-30 05:44 | manual | refine-logs/EXPERIMENT_TRACKER.md | implementation | tracker 同步 R007f binned sampler 和 R007i `model_4500.pt` eval，R007g/R007i 仍 IN_PROGRESS |
| 2026-06-30 05:44 | manual | refine-logs/EXPERIMENT_PLAN.md | implementation | experiment plan 同步 binned sampler 和 `model_4500.pt` eval 结果 |
| 2026-06-30 05:44 | manual | refine-logs/DAILY_EXPERIMENT_TIMELINE.md | implementation | daily timeline 同步 binned sampler 和 `model_4500.pt` eval 已完成但未过 mature controller gate |
| 2026-06-30 05:48 | manual | scripts/unitree_train_mamba_wrapper.py | implementation | repo-local profile dynamic load 先写入 `sys.modules[spec.name]`，修复 Python 3.10 dataclass importlib smoke failure |
| 2026-06-30 05:48 | manual | scripts/eval_unitree_g1_23dof_command_grid.py | implementation | eval 入口同步 `sys.modules[spec.name]` dynamic-load fix |
| 2026-06-30 05:48 | manual | scripts/setup_unitree_g1_23dof_training.sh | implementation | setup task-list smoke 入口同步 `sys.modules[spec.name]` dynamic-load fix |
| 2026-06-30 05:48 | manual | tests/test_unitree_g1_23dof_training_framework.py | test | 覆盖 train/eval/setup 动态加载 repo-local profile 时必须写入 `sys.modules` |
| 2026-06-30 05:48 | manual | docs/g1_edu_23dof_training_framework.md | implementation | 训练框架文档同步 binned sampler real-env smoke 结果 |
| 2026-06-30 05:48 | manual | refine-logs/G1_23DOF_CONTROLLER_POLICY_IMPROVEMENT_TODO.md | implementation | policy-improvement TODO 同步 binned sampler real-env smoke 结果 |
| 2026-06-30 05:48 | manual | refine-logs/G1_23DOF_CONTROLLER_POLICY_IMPROVEMENT_TODO_20260630.md | implementation | policy-improvement TODO timestamp copy 同步 binned sampler real-env smoke |
| 2026-06-30 05:48 | manual | refine-logs/EXPERIMENT_TRACKER.md | implementation | tracker 同步 binned sampler real-env smoke 和 dynamic-load fix |
| 2026-06-30 05:48 | manual | refine-logs/EXPERIMENT_PLAN.md | implementation | experiment plan 同步 binned sampler real-env smoke |
| 2026-06-30 05:48 | manual | refine-logs/DAILY_EXPERIMENT_TIMELINE.md | implementation | daily timeline 同步 binned sampler real-env smoke |
| 2026-06-30 05:55 | manual | runs/unitree_g1_23dof_eval/*model_5000_seed*.json | ignored-artifact | Stage A `model_5000.pt` 三 seed command-grid eval 完成；当前 fixed-forward 指标最好但仍未过 mature controller gate；raw JSON 仍保持 ignored |
| 2026-06-30 06:19 | manual | runs/unitree_g1_23dof_eval/*model_6000_seed*.json | ignored-artifact | Stage A `model_6000.pt` 三 seed command-grid eval 完成；fixed-forward 指标较 `model_5000.pt` 明显退化；raw JSON 仍保持 ignored |
| 2026-06-30 06:22 | manual | runs/unitree_g1_23dof_eval/*model_6500_seed*.json | ignored-artifact | Stage A `model_6500.pt` 三 seed command-grid eval 完成；有恢复但仍弱于 `model_5000.pt`；raw JSON 仍保持 ignored |
| 2026-06-30 06:24 | manual | refine-logs/G1_23DOF_CONTROLLER_STAGE_A_HANDOFF_20260630.md | implementation | handoff 增补 `model_5000/6000/6500.pt` 三 seed eval 结果，`model_5000.pt` 暂为 best 但仍不 mature |
| 2026-06-30 06:24 | manual | docs/g1_edu_23dof_training_framework.md | implementation | 训练框架文档同步 Stage A 已 eval 到 `model_6500.pt`，`model_5000.pt` 暂为 best |
| 2026-06-30 06:24 | manual | refine-logs/G1_23DOF_CONTROLLER_POLICY_IMPROVEMENT_TODO.md | implementation | policy-improvement TODO 同步 `model_5000/6000/6500.pt` eval 趋势 |
| 2026-06-30 06:24 | manual | refine-logs/G1_23DOF_CONTROLLER_POLICY_IMPROVEMENT_TODO_20260630.md | implementation | policy-improvement TODO timestamp copy 同步 `model_5000/6000/6500.pt` eval |
| 2026-06-30 06:24 | manual | refine-logs/EXPERIMENT_TRACKER.md | implementation | tracker 同步 R007i 已 eval 到 `model_6500.pt`，R007g/R007i 仍 IN_PROGRESS |
| 2026-06-30 06:24 | manual | refine-logs/EXPERIMENT_PLAN.md | implementation | experiment plan 同步 `model_5000/6000/6500.pt` eval 趋势 |
| 2026-06-30 06:24 | manual | refine-logs/DAILY_EXPERIMENT_TIMELINE.md | implementation | daily timeline 同步 `model_5000/6000/6500.pt` eval 已完成但未过 mature controller gate |
| 2026-06-30 07:21 | manual | runs/unitree_g1_23dof_eval/*model_7000_seed*.json | ignored-artifact | Stage A `model_7000.pt` 三 seed command-grid eval 完成；raw JSON 仍保持 ignored |
| 2026-06-30 07:24 | manual | runs/unitree_g1_23dof_eval/*model_8000_seed*.json | ignored-artifact | Stage A `model_8000.pt` 三 seed command-grid eval 完成；raw JSON 仍保持 ignored |
| 2026-06-30 07:30 | manual | runs/unitree_g1_23dof_eval/*model_8500_seed*.json | ignored-artifact | Stage A `model_8500.pt` 三 seed command-grid eval 完成；后期 checkpoint 中较接近 `model_5000.pt` 但仍未过 mature controller gate |
| 2026-06-30 07:26 | manual | runs/unitree_g1_23dof_eval/*model_9000_seed*.json | ignored-artifact | Stage A `model_9000.pt` 三 seed command-grid eval 完成；raw JSON 仍保持 ignored |
| 2026-06-30 07:33 | manual | runs/unitree_g1_23dof_eval/*model_9500_seed*.json | ignored-artifact | Stage A `model_9500.pt` 三 seed command-grid eval 完成；接近但仍略弱于 `model_5000.pt`，raw JSON 仍保持 ignored |
| 2026-06-30 07:34 | manual | refine-logs/G1_23DOF_CONTROLLER_STAGE_A_HANDOFF_20260630.md | implementation | handoff 增补 `model_7000/8000/8500/9000/9500.pt` 三 seed eval 结果 |
| 2026-06-30 07:34 | manual | docs/g1_edu_23dof_training_framework.md | implementation | 训练框架文档同步 Stage A 已 eval 到 `model_9500.pt`，`model_5000.pt` 仍为当前 best |
| 2026-06-30 07:34 | manual | refine-logs/G1_23DOF_CONTROLLER_POLICY_IMPROVEMENT_TODO.md | implementation | policy-improvement TODO 同步 `model_7000/8000/8500/9000/9500.pt` eval 趋势 |
| 2026-06-30 07:34 | manual | refine-logs/G1_23DOF_CONTROLLER_POLICY_IMPROVEMENT_TODO_20260630.md | implementation | policy-improvement TODO timestamp copy 同步 `model_7000/8000/8500/9000/9500.pt` eval |
| 2026-06-30 07:34 | manual | refine-logs/EXPERIMENT_TRACKER.md | implementation | tracker 同步 R007i 已 eval 到 `model_9500.pt`，R007g/R007i 仍 IN_PROGRESS |
| 2026-06-30 07:34 | manual | refine-logs/EXPERIMENT_PLAN.md | implementation | experiment plan 同步 `model_7000/8000/8500/9000/9500.pt` eval 趋势 |
| 2026-06-30 07:34 | manual | refine-logs/DAILY_EXPERIMENT_TIMELINE.md | implementation | daily timeline 同步 `model_7000/8000/8500/9000/9500.pt` eval 已完成但未过 mature controller gate |
| 2026-06-30 07:44 | manual | runs/unitree_g1_23dof_eval/*model_10000_seed*.json | ignored-artifact | Stage A `model_10000.pt` 三 seed final command-grid eval 完成；最终轮弱于 `model_5000.pt`，raw JSON 仍保持 ignored |
| 2026-06-30 08:30 | manual | third_party/unitree_rl_mjlab/logs/rsl_rl/g1_23dof_forward_flat/*20260630T034920Z/policy.onnx | ignored-artifact | Stage A seeds `101/102/103` 最终 ONNX shape 已验证为 `obs [1,80] -> actions [1,23]`；ONNX 仍不进 git |
| 2026-06-30 08:33 | manual | scripts/run_unitree_g1_23dof_training.sh | implementation | 训练脚本收尾产物查找改为 profile-agnostic `logs/rsl_rl/*/*RUN_NAME`，覆盖 ForwardFlat 和 VelocityBalancedFlat |
| 2026-06-30 08:34 | manual | refine-logs/G1_23DOF_CONTROLLER_STAGE_B_HANDOFF_20260630.md | implementation | Stage B VelocityBalancedFlat multi-seed handoff：seeds 201/202/203 on GPUs 1/2/3，raw logs/checkpoints 仍保持 ignored |
| 2026-06-30 08:34 | manual | runs/unitree_g1_23dof_training/STAGE_B_VELOCITY_BALANCED_RUNS_20260630T083359Z.txt | ignored-artifact | Stage B launch run list；tmux sessions `g1vb_s201/s202/s203_20260630T083359Z`，file remains ignored under runs |
| 2026-06-30 08:36 | manual | docs/g1_edu_23dof_training_framework.md | implementation | 训练框架文档同步 Stage A complete/ONNX shape 和 Stage B multi-seed launch 状态 |
| 2026-06-30 08:36 | manual | refine-logs/G1_23DOF_CONTROLLER_STAGE_A_HANDOFF_20260630.md | implementation | Stage A handoff 从 running 收口为 complete；记录 `model_10000.pt` final eval、ONNX shape 和 best checkpoint 仍为 `model_5000.pt` |
| 2026-06-30 08:36 | manual | refine-logs/G1_23DOF_CONTROLLER_POLICY_IMPROVEMENT_TODO.md | implementation | policy-improvement TODO 同步 Stage A complete/ONNX shape、Stage B launch 和 GPU preflight evidence |
| 2026-06-30 08:36 | manual | refine-logs/G1_23DOF_CONTROLLER_POLICY_IMPROVEMENT_TODO_20260630.md | implementation | policy-improvement TODO timestamp copy 同步 Stage A complete/Stage B launch |
| 2026-06-30 08:36 | manual | refine-logs/EXPERIMENT_TRACKER.md | implementation | tracker 同步 R007g DONE、R007h IN_PROGRESS、R007i 仍 IN_PROGRESS；Gate C 仍不推进 |
| 2026-06-30 08:36 | manual | refine-logs/EXPERIMENT_PLAN.md | implementation | experiment plan 同步 R007g shape check、R007h launch 和初始 health check |
| 2026-06-30 08:36 | manual | refine-logs/DAILY_EXPERIMENT_TIMELINE.md | implementation | daily timeline 同步 Stage A complete/ONNX shape 和 Stage B 08:33 UTC launch |
| 2026-06-30 08:38 | manual | refine-logs/G1_23DOF_CONTROLLER_STAGE_B_HANDOFF_20260630.md | implementation | Stage B handoff 增补 08:38 UTC health check：three seeds still running，iteration 129/135，early metrics improving but not mature evidence |
| 2026-06-30 08:40 | manual | refine-logs/G1_23DOF_CONTROLLER_STAGE_B_HANDOFF_20260630.md | implementation | Stage B handoff 增补 training-check：iteration 249/10001，mean reward positive，无 OOM/NaN，decision CONTINUE |
| 2026-06-30 08:43 | manual | scripts/run_unitree_g1_23dof_stage_b_eval_queue.sh | implementation | 新增 Stage B post-training eval queue：等待 `model_10000.pt` 和训练 tmux 结束后，再用 GPU 1/2/3 分批跑 command-grid eval |
| 2026-06-30 08:43 | manual | tests/test_unitree_g1_23dof_training_framework.py | test | 覆盖 Stage B eval queue 的 final-checkpoint wait、tmux wait、GPU assignment 和 seed-filter summary |
| 2026-06-30 08:43 | manual | runs/unitree_g1_23dof_eval_queue/stage_b_eval_queue_20260630T084308Z.log | ignored-artifact | Stage B eval queue watcher log；08:43 UTC 确认仍在等待 `model_10000.pt`，未提前占用额外 GPU |
| 2026-06-30 08:45 | manual | docs/g1_edu_23dof_training_framework.md | implementation | 训练框架文档同步 Stage B post-training eval queue |
| 2026-06-30 08:45 | manual | refine-logs/G1_23DOF_CONTROLLER_POLICY_IMPROVEMENT_TODO.md | implementation | policy-improvement TODO 同步 Stage B eval queue 已启动 |
| 2026-06-30 08:45 | manual | refine-logs/G1_23DOF_CONTROLLER_POLICY_IMPROVEMENT_TODO_20260630.md | implementation | policy-improvement TODO timestamp copy 同步 Stage B eval queue |
| 2026-06-30 08:45 | manual | refine-logs/EXPERIMENT_TRACKER.md | implementation | tracker 同步 R007h training-check 和 R007i Stage B eval queue |
| 2026-06-30 08:45 | manual | refine-logs/EXPERIMENT_PLAN.md | implementation | experiment plan 同步 R007h training-check 和 R007i Stage B eval queue |
| 2026-06-30 08:45 | manual | refine-logs/DAILY_EXPERIMENT_TIMELINE.md | implementation | daily timeline 同步 Stage B training-check 和 post-training eval queue |
| 2026-06-30 08:47 | manual | third_party/unitree_rl_mjlab/logs/rsl_rl/g1_23dof_velocity_balanced/*20260630T083359Z/model_500.pt | ignored-artifact | Stage B `model_500.pt` 已写出；raw checkpoint 仍保持 ignored |
| 2026-06-30 08:49 | manual | refine-logs/G1_23DOF_CONTROLLER_STAGE_B_HANDOFF_20260630.md | implementation | Stage B handoff 增补 08:47 UTC training-check：iteration 549/10001，reward 33.49-38.25，无 OOM/NaN，decision CONTINUE |
| 2026-06-30 08:49 | manual | refine-logs/EXPERIMENT_TRACKER.md | implementation | tracker 同步 Stage B 08:47 UTC health check |
| 2026-06-30 08:49 | manual | refine-logs/EXPERIMENT_PLAN.md | implementation | experiment plan 同步 Stage B 08:47 UTC health check |
| 2026-06-30 08:49 | manual | refine-logs/DAILY_EXPERIMENT_TIMELINE.md | implementation | daily timeline 同步 Stage B 08:47 UTC health check |
| 2026-06-30 08:51 | manual | refine-logs/G1_23DOF_CONTROLLER_STAGE_B_HANDOFF_20260630.md | implementation | Stage B handoff 增补 08:51 UTC lightweight health check：iteration 696/10001，reward 39.21-42.10，无 OOM/NaN/Inf，decision CONTINUE |
| 2026-06-30 08:55 | manual | runs/unitree_g1_23dof_training/*20260630T083359Z.log | ignored-artifact | Stage B old three-GPU early runs stopped at iteration ~783/10001 per user resource utilization request; raw logs/checkpoints remain ignored and superseded |
| 2026-06-30 08:55 | manual | runs/unitree_g1_23dof_training/STAGE_B_VELOCITY_BALANCED_PACKED_GPU5_RUNS_20260630T085517Z.txt | ignored-artifact | Stage B packed GPU5 launch run list for seeds 201/202/203; file remains ignored under runs |
| 2026-06-30 08:56 | manual | refine-logs/G1_23DOF_CONTROLLER_STAGE_B_HANDOFF_20260630.md | implementation | Stage B handoff updated: authoritative runs are packed on GPU 5, old GPU 1/2/3 runs marked superseded |
| 2026-06-30 08:56 | manual | runs/unitree_g1_23dof_eval_queue/stage_b_eval_queue_20260630T085653Z.log | ignored-artifact | Stage B packed eval queue watcher log; waits for packed GPU5 final checkpoints and uses GPU list 5 5 5 |
| 2026-06-30 09:00 | manual | docs/g1_edu_23dof_training_framework.md | implementation | training framework synchronized to Stage B packed GPU5 current run and packed eval queue |
| 2026-06-30 09:00 | manual | refine-logs/G1_23DOF_CONTROLLER_POLICY_IMPROVEMENT_TODO.md | implementation | policy-improvement TODO synchronized to Stage B packed GPU5 current run and packed eval queue |
| 2026-06-30 09:00 | manual | refine-logs/G1_23DOF_CONTROLLER_POLICY_IMPROVEMENT_TODO_20260630.md | implementation | policy-improvement TODO timestamp copy synchronized to Stage B packed GPU5 current run |
| 2026-06-30 09:00 | manual | refine-logs/EXPERIMENT_TRACKER.md | implementation | tracker synchronized to old three-GPU Stage B runs superseded and packed GPU5 runs in progress |
| 2026-06-30 09:00 | manual | refine-logs/EXPERIMENT_TRACKER_20260630_090007.md | implementation | tracker timestamp copy for Stage B packed GPU5 migration |
| 2026-06-30 09:00 | manual | refine-logs/EXPERIMENT_PLAN.md | implementation | experiment plan synchronized to Stage B packed GPU5 migration and packed eval queue |
| 2026-06-30 09:00 | manual | refine-logs/EXPERIMENT_PLAN_20260630_090007.md | implementation | experiment plan timestamp copy for Stage B packed GPU5 migration |
| 2026-06-30 09:00 | manual | refine-logs/DAILY_EXPERIMENT_TIMELINE.md | implementation | daily timeline synchronized to Stage B packed GPU5 migration |
| 2026-06-30 09:00 | manual | refine-logs/DAILY_EXPERIMENT_TIMELINE_20260630_090007.md | implementation | daily timeline timestamp copy for Stage B packed GPU5 migration |
| 2026-06-30 09:00 | manual | refine-logs/G1_23DOF_CONTROLLER_STAGE_B_HANDOFF_20260630.md | implementation | Stage B packed GPU5 health check: iteration 54/10001, GPU5 ~7550 MiB/100%, GPU1/2/3 released, no OOM |
| 2026-06-30 09:23 | manual | refine-logs/G1_23DOF_WORK_REPORT_20260629_20260630.html | report | standalone HTML report summarizing 2026-06-29/2026-06-30 23DoF controller training framework, Stage A/B runs, eval status, gate boundary, and next checks |
| 2026-07-01 03:34 | manual | scripts/unitree_play_mamba_wrapper.py | implementation | repo-local play wrapper registers `Unitree-G1-23Dof-VelocityBalancedFlat` profile before invoking upstream `scripts/play.py` |
| 2026-07-01 03:34 | manual | scripts/run_unitree_g1_23dof_play.sh | implementation | direct play entrypoint for selected 23DoF checkpoints; defaults to Viser and mamba env `robot` |
| 2026-07-01 03:34 | manual | tests/test_unitree_g1_23dof_training_framework.py | test | scoped tests cover the play wrapper and direct play script wiring |
| 2026-07-01 03:34 | manual | runs/unitree_g1_23dof_eval_queue/stage_b_eval_queue_20260701T012312Z.log | ignored-artifact | Stage B packed GPU5 eval rerun completed; raw queue log remains ignored |
| 2026-07-01 03:34 | manual | runs/unitree_g1_23dof_eval/*VelocityBalancedFlat*packedgpu5*seed*.json | ignored-artifact | Stage B command-grid eval outputs: 13 checkpoints x 3 seeds, raw JSON remains ignored |
| 2026-07-01 03:34 | manual | refine-logs/G1_23DOF_CONTROLLER_STAGE_B_ACCEPTANCE_20260701.md | implementation | Stage B morning acceptance: seeds 201/202/203 complete, `model_9000.pt` selected, Viser straight-line sanity recorded, R007j still pending |
| 2026-07-01 03:34 | manual | refine-logs/G1_23DOF_CONTROLLER_STAGE_B_HANDOFF_20260630.md | implementation | Stage B handoff closed from running to complete and synchronized with eval/play sanity results |
| 2026-07-01 03:34 | manual | docs/g1_edu_23dof_training_framework.md | implementation | training framework documents direct play entrypoint and Stage B `model_9000.pt` candidate status |
| 2026-07-01 03:34 | manual | refine-logs/G1_23DOF_CONTROLLER_POLICY_IMPROVEMENT_TODO.md | implementation | policy-improvement TODO marks Stage B training/eval done and keeps checkpoint copy plus R007j smoke open |
| 2026-07-01 03:34 | manual | refine-logs/G1_23DOF_CONTROLLER_POLICY_IMPROVEMENT_TODO_20260701_033421.md | implementation | timestamp copy for policy-improvement TODO after Stage B eval/play sanity |
| 2026-07-01 03:34 | manual | refine-logs/EXPERIMENT_TRACKER.md | implementation | tracker marks R007h/R007i DONE, selects Stage B seed 202 `model_9000.pt`, leaves R007j TODO |
| 2026-07-01 03:34 | manual | refine-logs/EXPERIMENT_TRACKER_20260701_033421.md | implementation | tracker timestamp copy after Stage B acceptance |
| 2026-07-01 03:34 | manual | refine-logs/EXPERIMENT_PLAN.md | implementation | experiment plan syncs Stage B completion, eval metrics, Viser straight-line sanity, and R007j boundary |
| 2026-07-01 03:34 | manual | refine-logs/EXPERIMENT_PLAN_20260701_033421.md | implementation | experiment plan timestamp copy after Stage B acceptance |
| 2026-07-01 03:34 | manual | refine-logs/DAILY_EXPERIMENT_TIMELINE.md | implementation | daily timeline syncs Stage B acceptance and keeps 23DoF profile smoke pending |
| 2026-07-01 03:34 | manual | refine-logs/DAILY_EXPERIMENT_TIMELINE_20260701_033421.md | implementation | daily timeline timestamp copy after Stage B acceptance |
| 2026-07-01 03:45 | manual | refine-logs/G1_23DOF_CONTROLLER_STAGE_B_CURATED_EVIDENCE_20260701.md | implementation | GitHub-safe curated evidence index for selected Stage B run/log/checkpoint/ONNX/eval artifacts; raw files remain ignored |
| 2026-07-01 03:45 | manual | refine-logs/G1_23DOF_CONTROLLER_STAGE_B_ACCEPTANCE_20260701.md | implementation | acceptance doc links the curated evidence index and keeps raw artifact bodies out of git |
| 2026-07-01 03:45 | manual | docs/g1_edu_23dof_training_framework.md | implementation | training framework links latest policy TODO snapshot and curated Stage B evidence index |
| 2026-07-01 03:45 | manual | refine-logs/G1_23DOF_CONTROLLER_POLICY_IMPROVEMENT_TODO.md | implementation | policy TODO records curated evidence selection while keeping checkpoint copy and R007j smoke open |
| 2026-07-01 03:45 | manual | refine-logs/G1_23DOF_CONTROLLER_POLICY_IMPROVEMENT_TODO_20260701_034510.md | implementation | timestamp copy for policy TODO after curated evidence selection |
| 2026-07-01 03:45 | manual | refine-logs/EXPERIMENT_TRACKER.md | implementation | tracker references curated raw-artifact hash/path index for R007h/R007i |
| 2026-07-01 03:45 | manual | refine-logs/EXPERIMENT_TRACKER_20260701_034510.md | implementation | tracker timestamp copy after curated evidence selection |
| 2026-07-01 03:45 | manual | refine-logs/EXPERIMENT_PLAN.md | implementation | experiment plan records curated Stage B evidence publication and preserved R007j boundary |
| 2026-07-01 03:45 | manual | refine-logs/EXPERIMENT_PLAN_20260701_034510.md | implementation | experiment plan timestamp copy after curated evidence selection |
| 2026-07-01 03:45 | manual | refine-logs/DAILY_EXPERIMENT_TIMELINE.md | implementation | daily timeline records curated evidence selection for important run/log/pt artifacts |
| 2026-07-01 03:45 | manual | refine-logs/DAILY_EXPERIMENT_TIMELINE_20260701_034510.md | implementation | daily timeline timestamp copy after curated evidence selection |

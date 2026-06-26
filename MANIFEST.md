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

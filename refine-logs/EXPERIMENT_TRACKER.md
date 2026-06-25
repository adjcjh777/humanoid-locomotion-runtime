# 实验跟踪表

| Run ID | 里程碑 | 目的 | 系统 / 变体 | Split | 指标 | 优先级 | 白天/夜间负责人 | 状态 | 备注 |
|--------|--------|------|-------------|-------|------|--------|------------------|------|------|
| R000 | M0 | A800 server stanza / path check | A800_SINGLE_HOST + RTX5090_BACKUP_HOST | n/a | ssh/env/repo path | MUST | 白天：人工 | DONE | 公共安全机器档案已写入 `docs/a800_machine_profile.md` 和 `docs/rtx5090_machine_profile.md`；A800 仍是 canonical，5090 是 backup；私有 SSH 细节不进仓库 |
| R001 | M0 | repo sync dry-run | current branch | n/a | clean git, pull ok | MUST | 夜间：ARIS | TODO | 暂不跑真实实验 |
| R002 | M0 | environment smoke | Python/MuJoCo/imports | n/a | import pass, GPU visible | MUST | 夜间：ARIS | TODO | 记录精确 package versions |
| R003 | M0 | artifact write smoke | Episode Data Package skeleton | n/a | manifest/json/log write ok | MUST | 夜间：ARIS | TODO | 不提交 generated runs |
| R004 | M0 | throughput microbenchmark | empty/synthetic rollout loop | dev seeds | steps/sec, disk MB/episode | MUST | 夜间：ARIS | TODO | 用于估算预算 |
| R005 | M0 | nightly handoff dry-run | tracker -> summary | n/a | summary written | MUST | 夜间：ARIS | TODO | 真实 overnight runs 前必须通过 |
| R010 | M1 | failure family freeze | protocol doc/config | fixed seed list | definitions complete | MUST | 白天：人工 | TODO | 看结果前完成冻结 |
| R011 | M1 | negative-control pilot | transient/instant | dev seeds | reproducibility, success rate | MUST | 夜间：ARIS | TODO | memory 理论上不应提升 |
| R012 | M1 | long-horizon pilot | long-horizon family | dev seeds | trigger consistency | MUST | 夜间：ARIS | TODO | freeze 前只调 severity |
| R013 | M1 | cumulative drift pilot | cumulative family | dev seeds | trigger consistency | MUST | 夜间：ARIS | TODO | 核心预期 memory-benefit family |
| R014 | M1 | localization/sensor degradation pilot | degradation family | dev seeds | trigger consistency | MUST | 夜间：ARIS | TODO | 核心预期 memory-benefit family |
| R015 | M1 | severity calibration | all families | dev seeds | controller_native 30-70% band | MUST | 夜间：ARIS | TODO | 若结果饱和则停止 |
| R016 | M1 | seed split generation | train/val/test | all seeds | deterministic split file | MUST | 白天：人工 | TODO | 提交 config，不提交 runs |
| R017 | M1 | Episode Data Package validation | all pilot families | dev seeds | schema completeness | MUST | 夜间：ARIS | TODO | analysis 前置条件 |
| R020 | M2 | controller native baseline | controller_native | pilot split | task/recovery success | MUST | 夜间：ARIS | TODO | 外部下界 |
| R021 | M2 | tuned rule baseline | rule_recovery_tuned | pilot split | recovery success, safety | MUST | 白天+夜间 | TODO | 不能是 strawman |
| R022 | M2 | oracle upper bound | oracle_upper_bound | pilot split | oracle gap | MUST | 夜间：ARIS | TODO | 只用 evaluation-only privileged signals |
| R023 | M2 | instant-state bandit sanity | instant_state | pilot split | learnability, action dist | MUST | 夜间：ARIS | TODO | PPO 前置 |
| R024 | M2 | full-memory bandit sanity | full_memory | pilot split | gain vs instant | MUST | 夜间：ARIS | TODO | 判断 memory 是否有信号 |
| R025 | M2 | baseline summary | baseline ladder | pilot split | CI draft | MUST | 白天：人工 | TODO | PPO 前 gate |
| R030 | M3 | no-memory supervisor | instant_state | matched held-out | success, decisions | MUST | 夜间：ARIS | TODO | shared seeds |
| R031 | M3 | window-memory supervisor | window_memory | matched held-out | success, decisions | MUST | 夜间：ARIS | TODO | shared seeds |
| R032 | M3 | full-memory supervisor | full_event_body_memory | matched held-out | success, decisions | MUST | 夜间：ARIS | TODO | shared seeds |
| R033 | M3 | shuffled memory negative-control | shuffled_memory | matched held-out | false gain check | MUST | 夜间：ARIS | TODO | 不应提升 |
| R034 | M3 | decision-flip analysis | memory-on/off pairs | matched held-out | flip rate, flip gain | MUST | 白天+夜间 | TODO | 论文核心 |
| R035 | M3 | paired statistics | bootstrap/McNemar | matched held-out | CI/effect size | MUST | 夜间：ARIS | TODO | 不只报 p 值 |
| R040 | M4 | event-only ablation | event_trace_only | held-out | contribution | MUST | 夜间：ARIS | TODO | 隔离来源 |
| R041 | M4 | body-trend-only ablation | body_trend_only | held-out | contribution | MUST | 夜间：ARIS | TODO | 隔离来源 |
| R042 | M4 | language-context ablation | with/without language | held-out | action changes | MUST | 夜间：ARIS | TODO | 若无效则弱化 language claim |
| R043 | M4 | memory horizon scan | short/medium/long | held-out | horizon curve | MUST | 夜间：ARIS | TODO | 注意 over-history |
| R044 | M4 | 3-action compression | compressed action set | held-out | simplicity check | NICE | 夜间：ARIS | TODO | 有时间再跑 |
| R045 | M4 | VLM-prompt supervisor | VLM over 8 actions | selected held-out | success, latency, invalid action | MUST | 夜间：ARIS | TODO | 相同输入，无 privileged truth |
| R046 | M4 | VLM vs learned summary | key families | held-out | family-wise win/loss | MUST | 白天：人工 | TODO | 决定论文故事 |
| R060 | M5 | main table generation | baseline + memory | final held-out | table csv/md | MUST | 夜间：ARIS | TODO | 可复现脚本 |
| R061 | M5 | figure 1 generation | per-family success CI | final held-out | png/pdf/source | MUST | 夜间：ARIS | TODO | 主 claim |
| R062 | M5 | figure 2 generation | memory-value / horizon | final held-out | png/pdf/source | MUST | 夜间：ARIS | TODO | 诊断 claim |
| R063 | M5 | case study selection | replay artifacts | selected episodes | qualitative coverage | MUST | 白天：人工 | TODO | 避免 cherry picking |
| R064 | M5 | limitation audit | failure cases | all results | honest limitations | MUST | 白天：人工 | TODO | 写作必需 |
| R070 | M5 | paper evidence package audit | all artifacts | final | reproducibility checklist | MUST | 夜间：ARIS | TODO | 投稿准备度 |

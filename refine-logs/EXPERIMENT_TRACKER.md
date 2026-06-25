# Experiment Tracker

| Run ID | Milestone | Purpose | System / Variant | Split | Metrics | Priority | Day/Night Owner | Status | Notes |
|--------|-----------|---------|------------------|-------|---------|----------|-----------------|--------|-------|
| R000 | M0 | A800 server stanza / path check | A800_SINGLE_HOST + RTX5090_BACKUP_HOST | n/a | ssh/env/repo path | MUST | Day: human | DONE | Public-safe machine profiles in `docs/a800_machine_profile.md` and `docs/rtx5090_machine_profile.md`; A800 remains canonical, 5090 is backup; keep private SSH details outside repo |
| R001 | M0 | repo sync dry-run | current branch | n/a | clean git, pull ok | MUST | Night: ARIS | TODO | No experiment yet |
| R002 | M0 | environment smoke | Python/MuJoCo/imports | n/a | import pass, GPU visible | MUST | Night: ARIS | TODO | Record exact package versions |
| R003 | M0 | artifact write smoke | Episode Data Package skeleton | n/a | manifest/json/log write ok | MUST | Night: ARIS | TODO | No generated runs committed |
| R004 | M0 | throughput microbenchmark | empty/synthetic rollout loop | dev seeds | steps/sec, disk MB/episode | MUST | Night: ARIS | TODO | Used to estimate budget |
| R005 | M0 | nightly handoff dry-run | tracker -> summary | n/a | summary written | MUST | Night: ARIS | TODO | Required before real overnight runs |
| R010 | M1 | failure family freeze | protocol doc/config | fixed seed list | definitions complete | MUST | Day: human | TODO | Do before looking at results |
| R011 | M1 | negative-control pilot | transient/instant | dev seeds | reproducibility, success rate | MUST | Night: ARIS | TODO | Memory should not help here |
| R012 | M1 | long-horizon pilot | long-horizon family | dev seeds | trigger consistency | MUST | Night: ARIS | TODO | Tune severity only before freeze |
| R013 | M1 | cumulative drift pilot | cumulative family | dev seeds | trigger consistency | MUST | Night: ARIS | TODO | Core expected memory-benefit family |
| R014 | M1 | localization/sensor degradation pilot | degradation family | dev seeds | trigger consistency | MUST | Night: ARIS | TODO | Core expected memory-benefit family |
| R015 | M1 | severity calibration | all families | dev seeds | controller_native 30-70% band | MUST | Night: ARIS | TODO | Stop if saturated |
| R016 | M1 | seed split generation | train/val/test | all seeds | deterministic split file | MUST | Day: human | TODO | Commit config, not runs |
| R017 | M1 | Episode Data Package validation | all pilot families | dev seeds | schema completeness | MUST | Night: ARIS | TODO | Needed for analysis |
| R020 | M2 | controller native baseline | controller_native | pilot split | task/recovery success | MUST | Night: ARIS | TODO | External lower bound |
| R021 | M2 | tuned rule baseline | rule_recovery_tuned | pilot split | recovery success, safety | MUST | Day+Night | TODO | Must not be strawman |
| R022 | M2 | oracle upper bound | oracle_upper_bound | pilot split | oracle gap | MUST | Night: ARIS | TODO | Evaluation-only privileged signals |
| R023 | M2 | instant-state bandit sanity | instant_state | pilot split | learnability, action dist | MUST | Night: ARIS | TODO | Before PPO |
| R024 | M2 | full-memory bandit sanity | full_memory | pilot split | gain vs instant | MUST | Night: ARIS | TODO | Decide whether memory signal exists |
| R025 | M2 | baseline summary | baseline ladder | pilot split | CI draft | MUST | Day: human | TODO | Gate before PPO |
| R030 | M3 | no-memory supervisor | instant_state | matched held-out | success, decisions | MUST | Night: ARIS | TODO | Shared seeds |
| R031 | M3 | window-memory supervisor | window_memory | matched held-out | success, decisions | MUST | Night: ARIS | TODO | Shared seeds |
| R032 | M3 | full-memory supervisor | full_event_body_memory | matched held-out | success, decisions | MUST | Night: ARIS | TODO | Shared seeds |
| R033 | M3 | shuffled memory negative-control | shuffled_memory | matched held-out | false gain check | MUST | Night: ARIS | TODO | Must not improve |
| R034 | M3 | decision-flip analysis | memory-on/off pairs | matched held-out | flip rate, flip gain | MUST | Day+Night | TODO | Paper core |
| R035 | M3 | paired statistics | bootstrap/McNemar | matched held-out | CI/effect size | MUST | Night: ARIS | TODO | No p-only reporting |
| R040 | M4 | event-only ablation | event_trace_only | held-out | contribution | MUST | Night: ARIS | TODO | Isolate source |
| R041 | M4 | body-trend-only ablation | body_trend_only | held-out | contribution | MUST | Night: ARIS | TODO | Isolate source |
| R042 | M4 | language-context ablation | with/without language | held-out | action changes | MUST | Night: ARIS | TODO | Weakens language claim if null |
| R043 | M4 | memory horizon scan | short/medium/long | held-out | horizon curve | MUST | Night: ARIS | TODO | Watch over-history |
| R044 | M4 | 3-action compression | compressed action set | held-out | simplicity check | NICE | Night: ARIS | TODO | Run if time |
| R045 | M4 | VLM-prompt supervisor | VLM over 8 actions | selected held-out | success, latency, invalid action | MUST | Night: ARIS | TODO | Same inputs, no privileged truth |
| R046 | M4 | VLM vs learned summary | key families | held-out | family-wise win/loss | MUST | Day: human | TODO | Gate story |
| R060 | M5 | main table generation | baseline + memory | final held-out | table csv/md | MUST | Night: ARIS | TODO | Reproducible script |
| R061 | M5 | figure 1 generation | per-family success CI | final held-out | png/pdf/source | MUST | Night: ARIS | TODO | Main claim |
| R062 | M5 | figure 2 generation | memory-value / horizon | final held-out | png/pdf/source | MUST | Night: ARIS | TODO | Diagnostic claim |
| R063 | M5 | case study selection | replay artifacts | selected episodes | qualitative coverage | MUST | Day: human | TODO | Avoid cherry picking |
| R064 | M5 | limitation audit | failure cases | all results | honest limitations | MUST | Day: human | TODO | Required for writing |
| R070 | M5 | paper evidence package audit | all artifacts | final | reproducibility checklist | MUST | Night: ARIS | TODO | Submission readiness |

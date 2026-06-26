# 实验跟踪表

| Run ID | 里程碑 | 目的 | 系统 / 变体 | Split | 指标 | 优先级 | 白天/夜间负责人 | 状态 | 备注 |
|--------|--------|------|-------------|-------|------|--------|------------------|------|------|
| R000 | M0 | A800/5090 public-safe machine profile | A800_SINGLE_HOST + RTX5090_BACKUP_HOST | n/a | host policy documented | MUST | 白天：人工 | DONE | 公共安全机器档案已写入 `docs/a800_machine_profile.md` 和 `docs/rtx5090_machine_profile.md`；A800 canonical，5090 backup；私有 SSH/路径/GPU 占用不进仓库 |
| R001 | M0 | repo sync dry-run | current branch | n/a | clean git, pull ok | MUST | 夜间：ARIS | DONE | rerun pass；证据：`refine-logs/MORNING_ACCEPTANCE_RERUN_20260626.md`、raw log in ignored `runs/night_handoff_rerun/20260626T013950Z/` |
| R002 | M0 | environment smoke | Python/MuJoCo/MJLab-classic imports | n/a | import pass, GPU visible, versions captured | MUST | 夜间：ARIS | DONE | rerun pass：Python 3.12.13、package import、MuJoCo 3.10.0、8 x A800 visible；MJLab backend reference 已在 2026-06-26 锁定为 `../mjlab` G1 velocity backend；JAX not primary requirement |
| R003 | M0 | artifact write smoke | Episode Data Package skeleton | n/a | manifest/json/log write ok | MUST | 白天：人工 | DONE | sample EDP writer/validator 已通过 tmp-path 单元测试；证据：`write_sample_episode_data_package()`、`tests/test_gate_b_edp.py`；不提交 generated runs |
| R004 | M0 | disk/throughput microbenchmark | empty/synthetic rollout loop | dev seeds | steps/sec, disk MB/episode | MUST | 夜间：ARIS | DONE | rerun pass for M0 synthetic-only with user 100GB disk override；free disk 99.42 GiB，50 synthetic EDPs，168633.81 steps/sec，0.002993 MB/episode；200 GiB batch threshold remains unchanged |
| R005 | M0 | nightly handoff dry-run | tracker -> summary | n/a | summary written | MUST | 夜间：ARIS | DONE | rerun pass；summary written to `refine-logs/MORNING_ACCEPTANCE_RERUN_20260626.md` |
| R006 | M0 | public repo hygiene | `.gitignore` + machine docs + raw traces | n/a | no raw traces tracked | MUST | 白天：人工 | DONE | `.aris/meta/`、`.aris/traces/` 已改为本机/私有审计材料；机器 profile 匿名化 |
| R007 | M0 | environment lock scaffold | pyproject/uv/version pins | n/a | lock inputs listed | MUST | 白天：人工 | DONE | 证据：`.python-version`、`pyproject.toml`、`uv.lock`、`configs/environment.lock.toml`、`docs/mjlab_backend_lock.md`；Python/MuJoCo/MJLab-first policy 已 pin，`../mjlab` Unitree G1 backend、MJCF 和 wrapper hashes 已锁定；controller checkpoint 仍为未选择阻塞字段；JAX/JAXLIB 移到 deferred Playground extra |
| R008 | M0 | repo foundation scaffold | src/tests/configs/CI/LICENSE | n/a | minimal tests pass | MUST | 白天：人工 | DONE | 证据：`src/`、`tests/`、`configs/`、`.github/workflows/ci.yml`、`LICENSE`；`uv run ruff check .` 和 `uv run pytest` 已通过 |
| R009 | M0 | Gate B schema/leakage boundary | `PolicyObservation` + `RuntimeEvent` + `OracleAnnotation` + EDP | n/a | policy serializer clean, EDP validator pass | MUST | 白天：人工 | DONE | 证据：`docs/gate_b_schema_edp.md`、`src/humanoid_locomotion_runtime/schemas.py`、`src/humanoid_locomotion_runtime/edp.py`、`tests/test_gate_b_schemas.py`、`tests/test_gate_b_edp.py`；`uv run ruff check .` 和 `uv run pytest` |
| R010 | M1 | failure protocol freeze | protocol doc/config | fixed seed list | definitions complete | MUST | 白天：人工 | TODO | 看结果前完成冻结 |
| R010a | M1 | cause x temporal taxonomy | protocol doc/config | fixed seed list | taxonomy complete | MUST | 白天：人工 | TODO | 区分故障原因和时间结构；`user_interrupt` 是 task-control event |
| R010b | M1 | state-aliasing benchmark cell | selected positive cells | dev seeds | same-observation/different-history check | MUST | 白天+夜间 | TODO | 至少一个 memory-positive cell 显式制造非 Markov 性 |
| R011 | M1 | negative-control pilot | path x transient / near-Markov cells | dev seeds | reproducibility, equivalence target | MUST | 夜间：ARIS | TODO | memory 理论上不应有实质收益 |
| R012 | M1 | recurrent/persistent pilot | path x recurrent/persistent | dev seeds | trigger consistency | MUST | 夜间：ARIS | TODO | freeze 前只调 severity |
| R013 | M1 | cumulative drift pilot | tracking/localization x cumulative | dev seeds | trigger consistency | MUST | 夜间：ARIS | TODO | 核心预期 memory-benefit cells |
| R014 | M1 | degradation/persistent pilot | localization/sensor x persistent | dev seeds | trigger consistency | MUST | 夜间：ARIS | TODO | 核心预期 memory-benefit cells |
| R015 | M1 | severity calibration | all selected cells | dev seeds | controller_native 30-70% band | MUST | 夜间：ARIS | TODO | 若结果饱和则停止 |
| R016 | M1 | seed split generation | train/val/test | all seeds | deterministic split file | MUST | 白天：人工 | TODO | 提交 config，不提交 runs |
| R017 | M1 | Episode Data Package validation | all pilot families | dev seeds | schema completeness | MUST | 夜间：ARIS | TODO | analysis 前置条件；validator 已由 R009 实现，all pilot-family validation 待 B1 artifacts |
| R018 | M1 | snapshot branching contract | snapshot/restore/common random numbers | unit/dev seeds | deterministic restore, branch metadata | MUST | 白天+夜间 | TODO | 未通过前不得写 counterfactual / ATE / branch oracle |
| R019 | M1 | recovery option/SMDP contract | all recovery actions | n/a | option fields complete | MUST | 白天：人工 | TODO | initiation/mask/implementation/duration/termination/interrupt/retry/cooldown |
| R020 | M2 | controller native baseline | controller_native | pilot split | task/recovery success | MUST | 夜间：ARIS | TODO | 外部下界 |
| R021 | M2 | tuned rule baseline | rule_recovery_tuned | pilot split | recovery success, safety | MUST | 白天+夜间 | TODO | baseline/fallback/debug role 分离；不是 debugging oracle |
| R022 | M2 | branch/evaluation oracle upper bound | branch_oracle or oracle_upper_bound | pilot split | oracle gap, action-value regret | MUST | 夜间：ARIS | TODO | 只用 evaluation-only privileged signals |
| R023 | M2 | instant-state bandit sanity | instant_mlp | pilot split | learnability, action dist | MUST | 夜间：ARIS | TODO | PPO 前置 |
| R024 | M2 | typed memory bandit sanity | typed_event_body_memory | pilot split | gain vs instant/history | MUST | 夜间：ARIS | TODO | 判断 typed memory 是否有信号 |
| R025 | M2 | baseline summary | baseline ladder | pilot split | CI draft, pivot decision | MUST | 白天：人工 | TODO | PPO / full-scale 前 gate |
| R026 | M2 | frame-stack raw-history baseline | frame_stack_raw_history | pilot split | success, safety, action dist | MUST | 夜间：ARIS | TODO | 与 typed memory 使用同样合法输入和预算 |
| R027 | M2 | GRU raw-history baseline | GRU_raw_history | pilot split | success, safety, action dist | MUST | 夜间：ARIS | TODO | 主文优先级高于 VLM baseline |
| R030 | M3 | no-memory supervisor | instant_mlp | snapshot branches or matched held-out | success, decisions | MUST | 夜间：ARIS | TODO | shared legal inputs/action set/controller |
| R031 | M3 | frame/window history supervisor | frame_stack_raw_history / window_memory | snapshot branches or matched held-out | success, decisions | MUST | 夜间：ARIS | TODO | ordinary history comparison |
| R032 | M3 | typed event/body memory supervisor | typed_event_body_memory | snapshot branches or matched held-out | success, decisions | MUST | 夜间：ARIS | TODO | shared seeds and budgets |
| R033 | M3 | shuffled memory negative-control | shuffled_memory | snapshot branches or matched held-out | false gain check | MUST | 夜间：ARIS | TODO | 不应有实质收益 |
| R034 | M3 | decision-flip analysis | memory-on/off pairs | snapshot branches or matched held-out | flip rate, flip-conditioned diagnostics | MUST | 白天+夜间 | TODO | 解释性指标，不单独当 causal effect |
| R035 | M3 | clustered/equivalence statistics | hierarchical bootstrap/TOST | snapshot branches or matched held-out | CI/effect size/equivalence | MUST | 夜间：ARIS | TODO | episode/base snapshot 聚类；不把不显著写成无效果 |
| R036 | M3 | memory-content intervention | correct/null/masked/shuffled/stale | snapshot branches or matched held-out | content effect, OOD check | MUST | 夜间：ARIS | TODO | 同一 typed-memory policy；训练时有 dropout 或 `memory_available` mask |
| R040 | M4 | event-only ablation | event_trace_only | held-out | contribution | MUST | 夜间：ARIS | TODO | 隔离来源 |
| R041 | M4 | body-trend-only ablation | body_trend_only | held-out | contribution | MUST | 夜间：ARIS | TODO | 隔离来源 |
| R042 | M4 | language-context ablation | with/without language | held-out | action changes | SHOULD | 夜间：ARIS | TODO | 若无效则弱化 language claim |
| R043 | M4 | memory horizon scan | short/medium/long | held-out | horizon curve | MUST | 夜间：ARIS | TODO | 注意 over-history |
| R044 | M4 | 3-action compression | compressed action set | held-out | simplicity check | NICE | 夜间：ARIS | TODO | 有时间再跑 |
| R045 | M4 | VLM-prompt supervisor | VLM over same high-level actions | selected held-out | success, latency, invalid action | SHOULD | 夜间：ARIS | TODO | 核心 gate 通过后再跑；相同输入，无 privileged truth |
| R046 | M4 | VLM vs learned summary | key families | held-out | family-wise win/loss | SHOULD | 白天：人工 | TODO | 作为附录或 language branch，不替代 GRU |
| R047 | M4 | statistical design freeze | primary endpoint + final sample plan | final protocol | seeds/bootstrap/multiplicity/SEI | MUST | 白天：人工 | TODO | 至少区分 pilot 和 final；negative control 用 equivalence / TOST |
| R060 | M5 | main table generation | baseline + memory | final held-out | table csv/md | MUST | 夜间：ARIS | TODO | 可复现脚本 |
| R061 | M5 | figure 1 generation | branch/matched outcome CI | final held-out | png/pdf/source | MUST | 夜间：ARIS | TODO | 主 claim |
| R062 | M5 | figure 2 generation | memory-value / horizon | final held-out | png/pdf/source | MUST | 夜间：ARIS | TODO | 诊断 claim |
| R063 | M5 | case study selection | replay artifacts | selected episodes | qualitative coverage | MUST | 白天：人工 | TODO | 避免 cherry picking |
| R064 | M5 | limitation audit | failure cases | all results | honest limitations | MUST | 白天：人工 | TODO | 写作必需 |
| R070 | M5 | paper evidence package audit | all artifacts | final | reproducibility checklist | MUST | 夜间：ARIS | TODO | 投稿准备度 |
| R071 | M5 | literature/citation verification | cited near-neighbor papers | n/a | title/authors/venue/abstract/BibTeX verified | MUST | 白天：人工 | TODO | agent-generated literature table 不得直接用于论文引用 |

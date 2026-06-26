# 实验跟踪表

这张表是 run-level 状态源。每一行都是一个可以被执行、复查和更新状态的 run。`DONE` 必须有证据；`TODO` 不能因为计划里写过就打勾。

读法：

- `Run ID` 是后续日志、summary、artifact 和讨论里引用的编号。
- `里程碑` 表示当前处在哪个大阶段。
- `系统 / 变体` 表示这次跑哪种方法或配置。
- `Split` 表示使用哪组 seeds 或数据划分。
- `状态` 只记录事实，不记录愿望。

| Run ID | 里程碑 | 目的 | 系统 / 变体 | Split | 指标 | 优先级 | 白天/夜间负责人 | 状态 | 备注 |
|--------|--------|------|-------------|-------|------|--------|------------------|------|------|
| R000 | M0 | A800/5090 public-safe machine profile | A800_SINGLE_HOST + RTX5090_BACKUP_HOST | n/a | host policy documented | MUST | 白天：人工 | DONE | 公共安全机器档案已写入 `docs/a800_machine_profile.md` 和 `docs/rtx5090_machine_profile.md`；A800 是主实验机，5090 只是备用；私有 SSH/路径/GPU 占用不进仓库 |
| R001 | M0 | repo sync dry-run | current branch | n/a | clean git, pull ok | MUST | 夜间：ARIS | DONE | rerun pass；证明服务器能同步仓库且工作树保持干净。证据：`refine-logs/MORNING_ACCEPTANCE_RERUN_20260626.md`、raw log in ignored `runs/night_handoff_rerun/20260626T013950Z/` |
| R002 | M0 | environment smoke | Python/MuJoCo/MJLab-classic imports | n/a | import pass, GPU visible, versions captured | MUST | 夜间：ARIS | DONE | rerun pass：Python 3.12.13、package import、MuJoCo 3.10.0、8 x A800 visible；MJLab backend reference 已在 2026-06-26 改锁为项目内 `third_party/mjlab` G1 velocity backend；完整 MJLab runtime smoke 已通过 `scripts/mjlab_sync_and_smoke.sh`：Python 3.12.13、Torch 2.9.0+cu128、MuJoCo-Warp 3.9.0.1、`Mjlab-Velocity-Flat-Unitree-G1` 16-step headless smoke pass；JAX not primary requirement |
| R003 | M0 | artifact write smoke | Episode Data Package skeleton | n/a | manifest/json/log write ok | MUST | 白天：人工 | DONE | sample EDP writer/validator 已通过 tmp-path 单元测试；证据：`write_sample_episode_data_package()`、`tests/test_gate_b_edp.py`；不提交 generated runs |
| R004 | M0 | disk/throughput microbenchmark | empty/synthetic rollout loop | dev seeds | steps/sec, disk MB/episode | MUST | 夜间：ARIS | DONE | rerun pass for M0 synthetic-only with user 100GB disk override；free disk 99.42 GiB，50 synthetic EDPs，168633.81 steps/sec，0.002993 MB/episode；200 GiB batch threshold 仍然有效，这次 override 不放行真实 batch |
| R005 | M0 | nightly handoff dry-run | tracker -> summary | n/a | summary written | MUST | 夜间：ARIS | DONE | rerun pass；summary written to `refine-logs/MORNING_ACCEPTANCE_RERUN_20260626.md` |
| R006 | M0 | public repo hygiene | `.gitignore` + machine docs + raw traces | n/a | no raw traces tracked | MUST | 白天：人工 | DONE | `.aris/meta/`、`.aris/traces/` 已改为本机/私有审计材料；机器 profile 匿名化 |
| R007 | M0 | environment lock scaffold | pyproject/uv/version pins | n/a | lock inputs listed | MUST | 白天：人工 | DONE | 证据：`.python-version`、`pyproject.toml`、`uv.lock`、`configs/environment.lock.toml`、`docs/mjlab_backend_lock.md`、`docs/controller_checkpoint_selection.md`、`scripts/mjlab_sync_and_smoke.sh`；Python/MuJoCo/MJLab-first policy 已 pin；当前完整 MJLab smoke 是 `mjlab_g1_29dof_reference` backend health evidence，不能当作公司 `company_g1_edu_23dof` target evidence；官方 Unitree ONNX candidate 是 29DoF reference candidate |
| R007a | M0 | company G1 23DoF source lock | `company_g1_edu_23dof` official URDF/MJCF | n/a | source commit/hash/joint order recorded | MUST | 白天：人工 | DONE | 证据：`docs/g1_edu_23dof_source_lock.md`、`configs/environment.lock.toml`、`tests/test_gate_a_foundation.py::test_company_g1_23dof_source_is_recorded_separately_from_29dof_reference`；只表示官方 source identified，不表示 MJLab wrapper/controller smoke 已完成 |
| R007b | M0 | company G1 23DoF fetch/verify script | official Unitree 23DoF description | n/a | fetch script pins commit and SHA256 | MUST | 白天：子代理 Worker A | DONE | 证据：`scripts/fetch_unitree_g1_23dof_description.sh`、`tests/test_fetch_unitree_g1_23dof_description.py`、`.gitignore` 中 `robot_descriptions/`；脚本只下载/校验 URDF/XML 到 git 外路径，不提交 downloaded assets；`bash -n scripts/fetch_unitree_g1_23dof_description.sh` 和 scoped pytest 通过 |
| R007c | M0 | profile-gated MJLab smoke | `mjlab_g1_29dof_reference` vs `company_g1_edu_23dof` | n/a | wrong-profile dimension mismatch fails | MUST | 白天：子代理 Worker B | DONE | 证据：`scripts/mjlab_g1_smoke.py`、`tests/test_mjlab_g1_smoke.py`；smoke 默认仍是 29DoF reference，增加 `--robot-profile` 和 expected action/obs dim gate；`company_g1_edu_23dof` 不能复用 29DoF action dim；scoped pytest 通过 |
| R007d | M0 | company G1 23DoF raw asset compile smoke | official 23DoF URDF/MJCF + meshes | n/a | MuJoCo compile pass, nq/nv/joints recorded | MUST | 白天：人工/ARIS | TODO | 前置：R007b；需要决定官方 mesh assets 是 fetch 到 git 外路径还是 vendor 小型 source subset；未通过前不做 23DoF MJLab wrapper |
| R007e | M0 | company G1 23DoF MJLab wrapper/controller selection | 23DoF robot cfg + controller candidate | n/a | action/obs shape and controller source locked | MUST | 白天：人工 | TODO | 前置：R007d；如果没有成熟 23DoF checkpoint，记录 train/convert/defer 决策，不能把 29DoF ONNX 直接升级为 target evidence |
| R008 | M0 | repo foundation scaffold | src/tests/configs/CI/LICENSE | n/a | minimal tests pass | MUST | 白天：人工 | DONE | 证据：`src/`、`tests/`、`configs/`、`.github/workflows/ci.yml`、`LICENSE`；`uv run ruff check .` 和 `uv run pytest` 已通过 |
| R009 | M0 | Gate B schema/leakage boundary | `PolicyObservation` + `RuntimeEvent` + `OracleAnnotation` + EDP | n/a | policy serializer clean, EDP validator pass | MUST | 白天：人工 | DONE | 证据：`docs/gate_b_schema_edp.md`、`src/humanoid_locomotion_runtime/schemas.py`、`src/humanoid_locomotion_runtime/edp.py`、`tests/test_gate_b_schemas.py`、`tests/test_gate_b_edp.py`；`uv run ruff check .` 和 `uv run pytest` |
| R009a | M0 | EDP robot profile metadata | EpisodeManifest / EDP schema extension | n/a | robot_profile_id, DoF, action dim, joint order hash recorded | MUST | 白天：子代理 Worker C | DONE | 证据：`src/humanoid_locomotion_runtime/schemas.py`、`src/humanoid_locomotion_runtime/edp.py`、`tests/test_gate_b_schemas.py`、`tests/test_gate_b_edp.py`；`EpisodeManifest` 记录 `robot_profile_id`、`robot_dof`、`action_dim`、`joint_order_sha256`、`controller_profile_id`，并保留 Gate B leakage boundary；scoped pytest 通过 |
| R010 | M1 | failure protocol freeze | protocol doc/config | fixed seed list | definitions complete | MUST | 白天：人工 | TODO | 看任何 memory 结果之前完成冻结，防止事后挑场景 |
| R010a | M1 | cause x temporal taxonomy | protocol doc/config | fixed seed list | taxonomy complete | MUST | 白天：人工 | TODO | 区分故障原因和时间结构；`user_interrupt` 是 task-control event，不算 failure family |
| R010b | M1 | state-aliasing benchmark cell | selected positive cells | dev seeds | same-observation/different-history check | MUST | 白天+夜间 | TODO | 至少一个 memory-positive cell 显式制造“当前看起来像、历史不一样、最优恢复动作不一样”的情况 |
| R011 | M1 | negative-control pilot | path x transient / near-Markov cells | dev seeds | reproducibility, equivalence target | MUST | 夜间：ARIS | TODO | memory 理论上不应有实质收益，用来检查假阳性 |
| R012 | M1 | recurrent/persistent pilot | path x recurrent/persistent | dev seeds | trigger consistency | MUST | 夜间：ARIS | TODO | freeze 前只调 severity |
| R013 | M1 | cumulative drift pilot | tracking/localization x cumulative | dev seeds | trigger consistency | MUST | 夜间：ARIS | TODO | 核心预期 memory-benefit cells |
| R014 | M1 | degradation/persistent pilot | localization/sensor x persistent | dev seeds | trigger consistency | MUST | 夜间：ARIS | TODO | 核心预期 memory-benefit cells |
| R015 | M1 | severity calibration | all selected cells | dev seeds | controller_native 30-70% band | MUST | 夜间：ARIS | TODO | 如果结果全成功或全失败，说明难度不合适，先停下来调 severity |
| R016 | M1 | seed split generation | train/val/test | all seeds | deterministic split file | MUST | 白天：人工 | TODO | 提交 config，不提交 runs |
| R017 | M1 | Episode Data Package validation | all pilot families | dev seeds | schema completeness | MUST | 夜间：ARIS | TODO | analysis 前置条件；validator 已由 R009 实现，all pilot-family validation 待 B1 artifacts |
| R018 | M1 | snapshot branching contract | snapshot/restore/common random numbers | unit/dev seeds | deterministic restore, branch metadata | MUST | 白天+夜间 | TODO | 未通过前不得写 counterfactual / ATE / branch oracle |
| R019 | M1 | recovery option/SMDP contract | all recovery actions | n/a | option fields complete | MUST | 白天：人工 | TODO | initiation/mask/implementation/duration/termination/interrupt/retry/cooldown |
| R020 | M2 | controller native baseline | controller_native | pilot split | task/recovery success | MUST | 夜间：ARIS | TODO | 外部下界 |
| R021 | M2 | tuned rule baseline | rule_recovery_tuned | pilot split | recovery success, safety | MUST | 白天+夜间 | TODO | 规则 baseline 要认真调，不当 strawman；它是 baseline/fallback，不是 oracle |
| R022 | M2 | branch/evaluation oracle upper bound | branch_oracle or oracle_upper_bound | pilot split | oracle gap, action-value regret | MUST | 夜间：ARIS | TODO | 只用 evaluation-only privileged signals |
| R023 | M2 | instant-state bandit sanity | instant_mlp | pilot split | learnability, action dist | MUST | 夜间：ARIS | TODO | PPO 前置 |
| R024 | M2 | typed memory bandit sanity | typed_event_body_memory | pilot split | gain vs instant/history | MUST | 夜间：ARIS | TODO | 判断 typed memory 是否有信号 |
| R025 | M2 | baseline summary | baseline ladder | pilot split | CI draft, pivot decision | MUST | 白天：人工 | TODO | PPO / full-scale 前 gate |
| R026 | M2 | frame-stack raw-history baseline | frame_stack_raw_history | pilot split | success, safety, action dist | MUST | 夜间：ARIS | TODO | 与 typed memory 使用同样合法输入和预算 |
| R027 | M2 | GRU raw-history baseline | GRU_raw_history | pilot split | success, safety, action dist | MUST | 夜间：ARIS | TODO | 主文优先级高于 VLM baseline |
| R030 | M3 | no-memory supervisor | instant_mlp | snapshot branches or matched held-out | success, decisions | MUST | 夜间：ARIS | TODO | shared legal inputs/action set/controller |
| R031 | M3 | frame/window history supervisor | frame_stack_raw_history / window_memory | snapshot branches or matched held-out | success, decisions | MUST | 夜间：ARIS | TODO | ordinary history comparison |
| R032 | M3 | typed event/body memory supervisor | typed_event_body_memory | snapshot branches or matched held-out | success, decisions | MUST | 夜间：ARIS | TODO | shared seeds and budgets |
| R033 | M3 | shuffled memory negative-control | shuffled_memory | snapshot branches or matched held-out | false gain check | MUST | 夜间：ARIS | TODO | 打乱 memory 后不应有实质收益；如果也涨，优先怀疑协议或泄漏 |
| R034 | M3 | decision-flip analysis | memory-on/off pairs | snapshot branches or matched held-out | flip rate, flip-conditioned diagnostics | MUST | 白天+夜间 | TODO | 只作为解释性指标，不单独当 causal effect |
| R035 | M3 | clustered/equivalence statistics | hierarchical bootstrap/TOST | snapshot branches or matched held-out | CI/effect size/equivalence | MUST | 夜间：ARIS | TODO | episode/base snapshot 聚类；不把“不显著”写成“无效果” |
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

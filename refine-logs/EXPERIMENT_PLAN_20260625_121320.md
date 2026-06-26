# 实验计划

**问题**：在冻结 / 成熟 humanoid locomotion controller 之上，验证高层 typed recovery supervisor 中的 event/body memory 是否、何时、为何能改变 recovery decision，并且这种改变是否真正改善安全恢复结果。
**方法主张**：论文应组织为 memory intervention diagnostic study。只有实现完整 simulator/runtime snapshot branching 后，才使用 counterfactual / ATE / branch oracle 等因果措辞；在此之前统一称为 paired matched-seed diagnostic。
**日期**：2026-06-25
**执行主机策略**：尽量单机执行。默认 `A800_SINGLE_HOST` 为唯一主实验机；5090 只作紧急备用，不进入日常实验主线。
**待办规则**：所有可执行事项必须使用 `- [ ]` / `- [x]`；打勾必须有 tracker、profile、commit、run id、summary 或配置文件作为证据。
**当前 Go/No-Go**：GO 到最小代码脚手架、schema/leakage boundary、EDP、option contract、snapshot/restore testbed 和 failure protocol freeze；NO-GO 到 PPO、大规模实验或论文主结论。

## Claim 映射

| Claim | 为什么重要 | 最小可信证据 | 对应实验块 |
|-------|------------|--------------|------------|
| C1: memory-value diagnostic | 这是当前最可防守的论文主贡献；避免把 8-action supervisor 包装成 novelty | snapshot branch 下的 action-induced outcome difference；若 snapshot branching 未完成，只报告 paired matched-seed decision flip 诊断，不写因果 | B2, B3, B4 |
| C2: seeded typed failure protocol | 让 recovery 结果可以复现、分层、反事实比较 | cause × temporal-profile taxonomy、failure cells 预注册、固定 seed split、controller-native / heuristic / branch oracle 对照、Episode Data Package | B1, B2 |
| C3: typed memory representation | 证明 typed event/body memory 优于普通历史输入，而不是仅仅拥有更多历史 | instant MLP、frame-stack MLP、GRU raw history、typed event/body memory 的同预算比较 | B2, B3, B4 |
| Anti-claim A1: 收益只来自 event trace/current state/raw history | 审稿人会质疑 memory 只是重命名状态或普通 recurrent history | leave-one-out、frame-stack、GRU raw-history、memory mask、stale/shuffled-memory | B3, B4 |
| Anti-claim A2: heuristic 能解决一切 | 如果规则系统打平，RL/memory selector 没意义 | tuned heuristic supervisor 与 instant/typed-memory selector 在 cumulative/degradation cells 的 branch 或 paired diagnostic comparison | B2, B3 |
| Anti-claim A3: VLM prompt 已经足够 | RACER/VLM recovery 是近邻，但不是当前最小主线 | 核心证据通过后，再把 VLM-prompt supervisor 作为附录或 language branch 比较 latency/success | B5 |

## 论文实验叙事

- 主文必须证明：
  - C1：memory 的价值是条件性的、可归因的，不是平均 success rate 小幅上涨。
  - C2：seeded typed failure protocol 支撑 snapshot branching 或降级后的 paired matched-seed diagnostic，而不是自造偏置 benchmark。
  - C3：typed event/body memory 优于普通 frame-stack / GRU raw-history baseline。
- 附录可以支持：
  - horizon scan、更多 failure severity、VLM prompt variants、dashboard/replay case studies。
- 主动砍掉的实验：
  - 真机 G1、多本体迁移、端到端 VLA、复杂 open-vocabulary detector 主线、低层 gait/residual policy。

## Gate-driven 执行顺序

固定 28 天 timeline 只作为参考节奏；实际推进按以下 gate。任何 gate 未通过，不进入后续 gate。

| Gate | 目标 | 必须完成 | 不通过时 |
|------|------|----------|----------|
| Gate A | repo foundation + environment lock | `pyproject.toml`、`uv.lock`、`src/`、`tests/`、CI、LICENSE、public/private ops 分离、`.aris/traces` 不入库 | DONE；证据见 `docs/gate_a_foundation.md`、R007、R008 |
| Gate B | schema + leakage boundary + EDP | `PolicyObservation`、`RuntimeEvent`、`OracleAnnotation` 隔离；policy serializer 测试；EDP writer/validator | DONE；证据见 `docs/gate_b_schema_edp.md`、R003、R009 |
| Gate C | option/SMDP + snapshot/restore | recovery option contracts、decision epoch、snapshot/restore、common random numbers、branch metadata | 不写 counterfactual，不训练 supervisor |
| Gate D | failure protocol calibration/freeze | cause × temporal-profile taxonomy、seed split、severity calibration、negative-control equivalence plan | 不启动 baseline ladder |
| Gate E | core baselines | controller_native、tuned_rule、instant_mlp、frame_stack_mlp、GRU_raw_history、typed_event_body_memory、branch_oracle | 不跑 PPO/大规模 |
| Gate F | memory intervention pilot | model/training effect 与 memory-content effect 分开；mask/dropout/shuffled/stale memory 干预 | 不写 memory causality |
| Gate G | final evaluation + evidence package | primary endpoint、training/scenario seeds、cluster bootstrap、multiplicity control、tables/figures reproducible | 不写主结论 |

## 实验块

### B0: A800 单机可复现执行地基

- 测试 claim：无，属于前置执行条件。
- 为什么存在：当前 repo 主要是 PRD/研究产物，尚无可自动跑的代码脚手架；若不先统一 A800 环境，晚上 ARIS 无法可靠接管。
- 数据/任务：无；建立 repo、env、logs、run manifests、nightly handoff 模板。
- 对比系统：无。
- 指标：`git status` clean、env check pass、sample artifact write pass、nightly dry-run pass。
- 设置细节：在 `A800_SINGLE_HOST` 上 clone/pull 当前 branch；只允许一个 canonical code dir；所有实验产物写入不提交的 runs/logs 目录。
- 成功标准：白天人工提交后，夜间 ARIS 能从同一 repo path 读取 tracker、启动 dry-run、写回 summary。
- 失败解释：不能进入实验；先修 SSH/env/path。
- 论文位置：不进论文。
- 优先级：MUST-RUN。

**B0 可确认清单**

- [x] R000: A800/5090 公共安全机器档案已记录；证据：`docs/a800_machine_profile.md`、`docs/rtx5090_machine_profile.md`、`refine-logs/EXPERIMENT_TRACKER.md`。
- [x] ARIS Codex skills 改为每台机器本机初始化资源；证据：`AGENTS.md`、`.gitignore`。
- [x] A800 本机已按 `--no-doc` 重新初始化 ARIS skills，且 `.agents/` / `.aris/installed-skills-codex.txt` 不再被 git 跟踪。
- [x] repo sync 基线已在 A800 上验证到当前分支，工作树保持干净。
- [x] generated runs/logs/artifacts/checkpoints/weights/datasets 已由 `.gitignore` 排除。
- [x] R006: public repo hygiene 完成；证据：`.gitignore`、匿名机器 profile、`git ls-files .aris` 为空。
- [x] R007: environment lock scaffold 完成；证据：`.python-version`、`pyproject.toml`、`uv.lock`、`configs/environment.lock.toml`；当前策略为 MJLab/classic MuJoCo first，JAX/JAXLIB 仅 deferred optional。
- [x] R008: repo foundation scaffold 完成；证据：`src/`、`tests/`、`configs/`、`.github/workflows/ci.yml`、`LICENSE`、`uv run ruff check .`、`uv run pytest`。
- [x] Gate A: repo foundation + environment lock 完成；证据：`docs/gate_a_foundation.md`。
- [x] R009: Gate B schema/leakage boundary 和 EDP writer/validator 完成；证据：`docs/gate_b_schema_edp.md`、`src/humanoid_locomotion_runtime/schemas.py`、`src/humanoid_locomotion_runtime/edp.py`、`tests/test_gate_b_schemas.py`、`tests/test_gate_b_edp.py`。
- [ ] R001: 夜间 repo sync dry-run 产出 summary。
- [ ] R002: 夜间 environment smoke 记录 Python/MuJoCo/MJLab-classic import/GPU 版本与结果；JAX 不作为 primary smoke 前置条件。
- [x] R003: artifact write smoke 证明 EDP skeleton 可写，且 generated outputs 不进 git；证据：`write_sample_episode_data_package()`、`tests/test_gate_b_edp.py`，执行位置为 tmp-path 单元测试。
- [ ] R005: 夜间 handoff dry-run 能从 tracker 生成 morning summary。

### B1: Seeded typed failure protocol 冻结

- 测试 claim：C2。
- 为什么存在：防止“挑 memory 擅长场景”的循环论证。
- 数据/任务：使用 cause × temporal-profile 二维 taxonomy，而不是混合“故障原因”和“时间结构”：
  - cause：path blockage、localization degradation、tracking degradation、balance disturbance、target/task event。
  - temporal profile：transient、persistent、recurrent、cumulative、progressive、impulse、change/loss/interruption。
  - `user_interrupt` 归为 task-control event，不作为 failure family。
  - 主实验预注册少量 cells，例如 path × transient negative-control、path × recurrent、tracking × cumulative、localization × persistent、balance × impulse。
- 对比系统：controller-native only for calibration；oracle labels 只用于评价上界。
- 指标：controller-native success rate、failure trigger reproducibility、severity bands、episode validity rate、state-aliasing diagnostic。
- 设置细节：每类从 3 个 severity 开始；主报告点选择 controller-native success 约 30-70% 的非饱和区间。
- 成功标准：每类至少 20 个 valid pilot episodes；同一 seed 复跑 failure timing/status 一致；negative-control 明确预注册为 memory 不应收益。
- 失败解释：若 failure 全 0/全 100 或不可复现，先调注入协议，不训练 supervisor。
- 论文位置：Methods table + Appendix protocol table。
- 优先级：MUST-RUN。

**B1 可确认清单**

- [ ] R010: failure cells 操作定义和 protocol doc/config 冻结，且看结果前完成。
- [ ] R010a: cause × temporal-profile taxonomy 写入协议；`user_interrupt` 改为 task-control event。
- [ ] R010b: 至少一个 positive benchmark cell 显式制造 state aliasing：当前 observation 相近，但历史不同导致 oracle 最优动作不同。
- [ ] R016: train/val/test seed split 文件确定并提交 config。
- [ ] R011: transient/instant negative-control pilot 完成并记录 trigger reproducibility。
- [ ] R012: long-horizon pilot 完成并记录 trigger consistency。
- [ ] R013: cumulative drift pilot 完成并记录 trigger consistency。
- [ ] R014: sensor/localization degradation pilot 完成并记录 trigger consistency。
- [ ] R015: all-family severity calibration 完成，主报告 severity 不全 0/不全 100。
- [ ] R017: Episode Data Package validation 完成，valid episode 和 schema completeness 达标；validator 已由 R009 实现，但 all pilot families validation 等待 B1 artifacts。
- [ ] B1 gate: selected failure cells reproducible、non-saturated，negative-control 预注册清晰。

### B2: Baseline 阶段

- 测试 claim：C2, C3, A2。
- 为什么存在：先确认低层 controller、规则、no-memory supervisor 的下限和强度。
- 数据/任务：B1 的 pilot split，先 cumulative/degradation，再扩到全部 family。
- 对比系统：
  - `controller_native`
  - `rule_recovery_tuned`
  - `instant_mlp`
  - `frame_stack_raw_history`
  - `GRU_raw_history`
  - `typed_event_body_memory`
  - `branch_oracle` 或 evaluation-only `oracle_upper_bound`
- 指标：task success、recovery success、fall/unstable count、stop latency、repeated failure count、episode validity。
- 设置细节：先 bandit sanity check，再决定是否 PPO；所有 learned variants 共享合法输入源、action set、reward、训练数据、调参预算、controller/planner 和 training seeds；尽量参数量接近。
- 成功标准：heuristic 不是 strawman，但在至少一个 cumulative/degradation family 上存在明显 oracle gap 和 learnable gap。
- 失败解释：如果 tuned heuristic 打平 instant/typed-memory selector，论文从 learned supervisor pivot 到 protocol/diagnostic。
- 论文位置：Main Table 1 baseline ladder。
- 优先级：MUST-RUN。

**B2 可确认清单**

- [ ] R020: controller-native baseline 完成，作为外部下界。
- [ ] R021: tuned rule baseline 完成，规则输入不包含 privileged signals，且不是 strawman。
- [ ] R022: branch/evaluation oracle pilot 完成，只使用 evaluation-only privileged signals。
- [ ] R023: instant MLP / instant-state bandit sanity 完成，确认 action selector 基本可学习。
- [ ] R026: frame-stack raw-history baseline 完成，与 typed memory 使用同样合法输入和预算。
- [ ] R027: GRU raw-history baseline 完成；主文优先级高于 VLM baseline。
- [ ] R024: typed event/body memory sanity 完成，判断 memory representation 是否优于 ordinary history。
- [ ] R025: baseline summary 完成，形成 PPO / pivot 前 gate 证据。
- [ ] B2 gate: tuned heuristic 与 oracle 之间存在可解释 gap；若 gap 不存在，记录 pivot 决策。

### B3: Memory-value 反事实实验

- 测试 claim：C1, A1。
- 为什么存在：全文最关键实验，证明 memory 改变了高层动作选择且这种改变有收益。
- 数据/任务：优先使用 decision-point snapshot branching；若未实现，只能作为 paired matched-seed diagnostic，不得写 counterfactual causality。
- 对比系统：
  - `instant_mlp`
  - `frame_stack_raw_history`
  - `GRU_raw_history`
  - `typed_event_body_memory`
  - memory mask / null / stale / shuffled variants
  - `shuffled_memory_negative_control`
- 指标：branched outcome difference / ATE、action-value regret against branch oracle、unsafe-completion difference、recovery latency difference；decision-flip rate 和 flip-conditioned gain 只作为解释性指标。
- 设置细节：snapshot 至少包含 `mjData`、random generator state、localization estimator state、planner state、temporary object memory、body memory、active option、option elapsed time、controller recurrent state、failure injector state。
- 成功标准：在预注册 memory-positive cells 中，typed memory 相对 instant/frame-stack/GRU 有 branch-level recovery gain；negative-control 上通过 equivalence interval 证明没有实质收益。
- 失败解释：若只在 matched-seed 下平均成功涨但 snapshot branch 解释不了，不能写 causality；若 negative-control 也涨，说明协议或特征泄漏。
- 论文位置：Main Figure 1 + Table 2。
- 优先级：MUST-RUN。

**B3 可确认清单**

- [ ] R018: decision-point snapshot/restore 和 common random numbers 通过单元测试。
- [ ] R030: no-memory / instant MLP supervisor 在 matched held-out seeds 或 snapshot branches 上完成。
- [ ] R031: frame-stack / window-history supervisor 在相同 action set/controller 上完成。
- [ ] R032: typed event/body memory supervisor 在相同 action set/controller 上完成。
- [ ] R033: shuffled-memory negative-control 完成，确认不应提升。
- [ ] R036: 同一 typed-memory policy 的 correct/null/masked/shuffled/stale memory-content intervention 完成；训练时包含 memory dropout 或 `memory_available` mask。
- [ ] R034: decision-flip analysis 完成，输出 flip rate、flip gain 和 per-action diagnostics；只作为解释性指标。
- [ ] R035: paired/cluster statistics 完成，包含 hierarchical bootstrap、equivalence / TOST negative-control 分析。
- [ ] B3 gate: expected cells 中 typed memory 有 branch-level gain，并优于 ordinary raw-history baselines；negative-control CI 落入预注册等效区间。

### B4: 输入和 Horizon 消融

- 测试 claim：C3, A1。
- 为什么存在：防止 reviewer 说 event trace/current state/language 才是实际来源。
- 数据/任务：B3 的 held-out seeds。
- 对比系统：
  - no memory
  - frame-stack raw history
  - GRU raw history
  - event trace only
  - body trend only
  - event + body
  - event + body + language
  - shuffled memory
  - horizon lengths: short / medium / long
- 指标：recovery success、decision flip、over-conservatism rate、safe_stop/abort frequency。
- 设置细节：先小 grid；只有 B3 gate 通过后才扩大。
- 成功标准：能定位 memory 的有效成分；不要求所有组件都有用。
- 失败解释：language 无效则论文标题/claim 中弱化 language-conditioned。
- 论文位置：Main Figure 2 或 Appendix Table。
- 优先级：B3 pilot 通过后 MUST-RUN。

**B4 可确认清单**

- [ ] R040: event-only ablation 完成，隔离 event trace contribution。
- [ ] R041: body-trend-only ablation 完成，隔离 body trend contribution。
- [ ] R042: language-context ablation 完成，若无效则弱化 language claim。
- [ ] R043: memory horizon scan 完成，输出 short/medium/long horizon curve。
- [ ] R044: 3-action compression 完成或明确 deferred reason。
- [ ] R047: 统计设计冻结，包含 primary endpoint、training seeds、scenario seeds、cluster bootstrap、multiplicity control 和 smallest effect size of interest。
- [ ] B4 gate: 能定位 memory 有效成分，并记录 over-history / over-conservatism 风险。

### B5: VLM-prompt supervisor 与简洁性检查

- 测试 claim：A3 和 simplicity。
- 为什么存在：RACER/VLM recovery 是近邻；但 VLM 不替代 GRU/raw-history baseline，核心 evidence gate 通过后再跑。
- 数据/任务：同一 held-out seeds，优先 target change / grounding ambiguity / cumulative failure。
- 对比系统：
  - VLM-prompt supervisor over same 8 actions
  - rule recovery
  - full memory supervisor
  - optional 3-action compressed supervisor
- 指标：recovery success、decision latency、invalid action rate、cost per episode、same-seed action agreement。
- 设置细节：VLM 只读合法状态摘要，不读 MuJoCo privileged ground truth。
- 成功标准：learned/lightweight supervisor 在 latency/reliability 或特定 failure cell 上有可辩护优势；若 VLM 更强，改写成 VLM baseline/policy comparison paper。
- 失败解释：VLM 全面碾压则不再主打 RL policy。
- 论文位置：Appendix 或 language branch；只有核心 evidence gate 通过且 VLM 成为主要 reviewer concern 时进入主文。
- 优先级：AFTER CORE GATES；不是 first pilot 前置项。

**B5 可确认清单**

- [ ] VLM prompt 输入规范完成，明确只读合法状态摘要，不读 MuJoCo privileged ground truth。
- [ ] R045: VLM-prompt supervisor 在相同 8-action space、相同 seeds、相同 summaries 下完成，或明确 deferred reason。
- [ ] R046: VLM vs learned summary 完成，输出 family-wise win/loss，或明确 deferred reason。
- [ ] 简洁性检查完成：compressed action set 若未跑，必须写明 deferred reason。
- [ ] B5 gate: 记录 VLM 是否推翻 learned/lightweight supervisor 主线；如推翻，写 pivot 决策。

### B6: 稳健性、证据打包与论文图表

- 测试 claim：C1/C2 presentation robustness。
- 为什么存在：把实验变成可投稿证据。
- 数据/任务：held-out seeds、severity sweep、selected qualitative episodes。
- 对比系统：final method + key baselines。
- 指标：CI/effect size、artifact completeness、replay validity、failure-case diversity。
- 设置细节：每个论文图表有固定 source script；不手工改图。
- 成功标准：每个 main claim 有表/图支撑，失败案例与 limitations 一致。
- 失败解释：如果图无法复现，停止写作先修 analysis pipeline。
- 论文位置：全部 main/appendix figures。
- 优先级：写作周 MUST-RUN。

**B6 可确认清单**

- [ ] R060: main table generation 完成，csv/md/source paths 可复现。
- [ ] R061: Figure 1 generation 完成，per-family success CI 可追溯到 run ids。
- [ ] R062: Figure 2 generation 完成，memory-value / horizon diagnostics 可复现。
- [ ] R063: case study selection 完成，包含成功、失败和 limitation cases，避免 cherry picking。
- [ ] R064: limitation audit 完成，失败案例与正文 limitations 一致。
- [ ] R070: paper evidence package audit 完成，检查 artifact completeness、missing seeds、failed jobs。
- [ ] R071: literature/citation verification 完成，逐篇核验 title、authors、venue、abstract、BibTeX；agent-generated literature table 不得直接引用。
- [ ] B6 gate: 每个 main claim 都有表/图/summary 证据，无法复现的图表先修 analysis pipeline。

## 运行顺序与里程碑

| Milestone | 目标 | Runs | 决策 Gate | 成本 | 风险 |
|-----------|------|------|-----------|------|------|
| M0 | A800 single-host automation ready | R000-R005 | ARIS nightly dry-run can read tracker and write summary | low | server/env unknown |
| M1 | protocol freeze | R010-R019 | selected failure cells reproducible and non-saturated | low-med | injection too artificial |
| M2 | baseline ladder | R020-R029 | heuristic has gap and oracle gap exists | med | heuristic too strong |
| M3 | memory intervention diagnostic | R030-R039 | snapshot branch gain is positive in expected cells; if snapshot is unavailable, only paired matched-seed diagnostics are reported | med-high | no memory effect |
| M4 | ablations/VLM | R040-R059 | input source understood; VLM does not invalidate story | med-high | VLM stronger |
| M5 | paper package | R060-R079 | figures/tables reproducible from artifacts | med | analysis drift |

## 计算与数据预算

- 总 GPU-hours：在 A800 env 和 simulator throughput 实测前未知。Day 2 throughput benchmark 后估算。
- 规划假设：MuJoCo rollout 可能受 CPU/simulator 限制；A800 主要价值在 batched RL/PPO、VLM 和并行队列。
- 数据准备：
  - seed split files
  - failure cell config files
  - episode manifest schema
  - artifact retention policy
- 人工评估：
  - 每天早上检查 overnight logs
  - 每个 gate 决定是否扩量
- 最大瓶颈：
  - G1/MuJoCo controller smoke gate 和 reproducible failure injection，不是 PPO 本身。

## 风险与缓解

- A800 server details 缺失：
  - 缓解：Day 1 建立 `CLAUDE.md`/server stanza 或等价 private handoff；未通过前不跑夜间自动化。
- G1 controller integration 失败：
  - 缓解：按项目规则，controller smoke gate 失败则优先切到 MJLab/mujocolab-compatible classic MuJoCo backend；MuJoCo Playground 仅作为 deferred optional reference。
- 实验 claim 漂移：
  - 缓解：看结果前冻结 failure definitions 和 seed splits。
- heuristic baseline 获胜：
  - 缓解：pivot 到 diagnostic/protocol paper；不强行讲 RL story。
- memory effect 缺失：
  - 缓解：如果 protocol 强，报告 negative result；否则 pivot 到 failure-injection/testbed。
- artifacts 过大：
  - 缓解：nightly retention policy：所有 run 保留 summary 和 selected traces；full replay 只保留 held-out / failure cases。
- raw traces 或机器运维信息误入公开仓库：
  - 缓解：`.aris/meta/`、`.aris/traces/`、hostname、用户名、绝对路径、实时 GPU 占用和私有连接细节只放 private ops；公开仓库只保留 curated summaries。

## 最终检查清单

- [x] A800 single-host execution path documented；证据：`docs/a800_machine_profile.md`、`refine-logs/EXPERIMENT_TRACKER.md`。
- [x] machine-local ARIS resources documented；证据：`AGENTS.md`、`.gitignore`、`docs/a800_machine_profile.md`、`docs/rtx5090_machine_profile.md`。
- [x] experiment plan / timeline use checkable todos；证据：`refine-logs/EXPERIMENT_PLAN.md`、`refine-logs/DAILY_EXPERIMENT_TIMELINE.md`。
- [x] raw ARIS traces and machine profiles follow public/private split；证据：`.gitignore`、`docs/a800_machine_profile.md`、`docs/rtx5090_machine_profile.md`、`refine-logs/EXPERIMENT_TRACKER.md` R006。
- [x] Gate A repo foundation + environment lock completed；证据：`docs/gate_a_foundation.md`、`pyproject.toml`、`uv.lock`、`src/`、`tests/`、`.github/workflows/ci.yml`、`LICENSE`、`configs/environment.lock.toml`、`configs/artifact_retention.toml`；backend policy 已改为 MJLab/classic MuJoCo first。
- [ ] main paper tables covered
- [ ] novelty isolated through snapshot branching；未实现前只能写 paired matched-seed diagnostic
- [ ] frame-stack raw-history and GRU raw-history baselines completed before VLM is promoted to main text
- [ ] recovery actions formalized as options / SMDP before learned policy evaluation
- [ ] simplicity defended against tuned heuristic and compressed action set
- [ ] VLM baseline run or explicitly deferred with reason
- [x] nice-to-have runs separated from must-run runs；证据：`refine-logs/EXPERIMENT_TRACKER.md` 中 `Priority` 字段。
- [ ] every night job has a morning acceptance checklist
- [ ] no runtime decision uses MuJoCo privileged ground truth

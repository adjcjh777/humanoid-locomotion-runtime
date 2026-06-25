# 实验计划

**问题**：在冻结 / 成熟 humanoid locomotion controller 之上，验证高层 typed recovery supervisor 中的 event/body memory 是否、何时、为何能改善失败恢复，而不是只做一个工程 runtime。
**方法主张**：论文应组织为 counterfactual diagnostic study：用 seeded typed failure protocol 和 matched-seed decision-flip analysis 证明 memory 的收益只在 long-horizon / cumulative / degradation failure 中成立。
**日期**：2026-06-25
**执行主机策略**：尽量单机执行。默认 `A800_SINGLE_HOST` 为唯一主实验机；5090 只作紧急备用，不进入日常实验主线。
**待办规则**：所有可执行事项必须使用 `- [ ]` / `- [x]`；打勾必须有 tracker、profile、commit、run id、summary 或配置文件作为证据。

## Claim 映射

| Claim | 为什么重要 | 最小可信证据 | 对应实验块 |
|-------|------------|--------------|------------|
| C1: memory-value diagnostic | 这是当前最可防守的论文主贡献；避免把 8-action supervisor 包装成 novelty | matched-seed 下 memory-on/off 的 decision flip 率、flip 条件恢复收益、95% CI、negative-control 上无显著收益 | B2, B3, B4 |
| C2: seeded typed failure protocol | 让 recovery 结果可以复现、分层、反事实比较 | failure family 预注册定义、固定 seed split、controller-native / heuristic / oracle 对照、Episode Data Package | B1, B2 |
| Anti-claim A1: 收益只来自 event trace/current state | 审稿人会质疑 memory 只是重命名状态 | leave-one-out: instant-only、event-only、trend-only、language-only、shuffled-memory | B3, B4 |
| Anti-claim A2: heuristic 能解决一切 | 如果规则系统打平，RL/memory selector 没意义 | tuned heuristic supervisor 与 no-memory/full-memory 在 cumulative/degradation family 的 matched comparison | B2, B3 |
| Anti-claim A3: VLM prompt 已经足够 | RACER/VLM recovery 近邻要求比较 | VLM-prompt supervisor 在相同 8-action space、相同 seeds、相同 summaries 下比较 latency/success | B5 |

## 论文实验叙事

- 主文必须证明：
  - C1：memory 的价值是条件性的、可归因的，不是平均 success rate 小幅上涨。
  - C2：seeded typed failure protocol 支撑 matched-seed counterfactual，而不是自造偏置 benchmark。
- 附录可以支持：
  - horizon scan、更多 failure severity、VLM prompt variants、dashboard/replay case studies。
- 主动砍掉的实验：
  - 真机 G1、多本体迁移、端到端 VLA、复杂 open-vocabulary detector 主线、低层 gait/residual policy。

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
- [ ] R001: 夜间 repo sync dry-run 产出 summary。
- [ ] R002: 夜间 environment smoke 记录 Python/MuJoCo/import/GPU 版本与结果。
- [ ] R003: 夜间 artifact write smoke 证明 EDP skeleton 可写，且 generated outputs 不进 git。
- [ ] R005: 夜间 handoff dry-run 能从 tracker 生成 morning summary。

### B1: Seeded typed failure protocol 冻结

- 测试 claim：C2。
- 为什么存在：防止“挑 memory 擅长场景”的循环论证。
- 数据/任务：4 个主 family：transient/instant negative-control、long-horizon、cumulative drift、sensor/localization degradation；每类固定 train/val/test seed split。
- 对比系统：controller-native only for calibration；oracle labels 只用于评价上界。
- 指标：controller-native success rate、failure trigger reproducibility、severity bands、episode validity rate。
- 设置细节：每类从 3 个 severity 开始；主报告点选择 controller-native success 约 30-70% 的非饱和区间。
- 成功标准：每类至少 20 个 valid pilot episodes；同一 seed 复跑 failure timing/status 一致；negative-control 明确预注册为 memory 不应收益。
- 失败解释：若 failure 全 0/全 100 或不可复现，先调注入协议，不训练 supervisor。
- 论文位置：Methods table + Appendix protocol table。
- 优先级：MUST-RUN。

### B2: Baseline 阶段

- 测试 claim：C2, A2。
- 为什么存在：先确认低层 controller、规则、no-memory supervisor 的下限和强度。
- 数据/任务：B1 的 pilot split，先 cumulative/degradation，再扩到全部 family。
- 对比系统：
  - `controller_native`
  - `rule_recovery_tuned`
  - `rl_or_bandit_instant_state`
  - `oracle_upper_bound`
- 指标：task success、recovery success、fall/unstable count、stop latency、repeated failure count、episode validity。
- 设置细节：先 bandit sanity check，再决定是否 PPO；每个 cell 先 3 seeds × 10 episodes pilot。
- 成功标准：heuristic 不是 strawman，但在至少一个 cumulative/degradation family 上存在明显 oracle gap 和 learnable gap。
- 失败解释：如果 tuned heuristic 打平 no-memory/full-memory，论文从 learned supervisor pivot 到 protocol/diagnostic。
- 论文位置：Main Table 1 baseline ladder。
- 优先级：MUST-RUN。

### B3: Memory-value 反事实实验

- 测试 claim：C1, A1。
- 为什么存在：全文最关键实验，证明 memory 改变了高层动作选择且这种改变有收益。
- 数据/任务：matched held-out seeds；同一 initial state、同一 failure injection、同一 controller backend。
- 对比系统：
  - `instant_state`
  - `window_memory`
  - `full_event_body_memory`
  - `shuffled_memory_negative_control`
- 指标：decision-flip rate、flip-conditioned success delta、paired bootstrap CI、McNemar / paired tests、per-action confusion matrix。
- 设置细节：所有 variants 必须共享 action set、reward、controller、planner、seed；只改 observation memory。
- 成功标准：在 long-horizon/cumulative/degradation 至少 1-2 类中，full memory 相对 instant 有显著 flip-conditioned recovery gain；transient negative-control 上无显著收益。
- 失败解释：若平均成功涨但 flip 解释不了，不能写 causality；若 negative-control 也涨，说明协议或特征泄漏。
- 论文位置：Main Figure 1 + Table 2。
- 优先级：MUST-RUN。

### B4: 输入和 Horizon 消融

- 测试 claim：A1。
- 为什么存在：防止 reviewer 说 event trace/current state/language 才是实际来源。
- 数据/任务：B3 的 held-out seeds。
- 对比系统：
  - no memory
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

### B5: VLM-prompt supervisor 与简洁性检查

- 测试 claim：A3 和 simplicity。
- 为什么存在：RACER/VLM recovery 是近邻；必须证明我们不是忽略强 baseline。
- 数据/任务：同一 held-out seeds，优先 target change / grounding ambiguity / cumulative failure。
- 对比系统：
  - VLM-prompt supervisor over same 8 actions
  - rule recovery
  - full memory supervisor
  - optional 3-action compressed supervisor
- 指标：recovery success、decision latency、invalid action rate、cost per episode、same-seed action agreement。
- 设置细节：VLM 只读合法状态摘要，不读 MuJoCo privileged ground truth。
- 成功标准：learned/lightweight supervisor 在 latency/reliability 或特定 failure family 上有可辩护优势；若 VLM 更强，改写成 VLM baseline/policy comparison paper。
- 失败解释：VLM 全面碾压则不再主打 RL policy。
- 论文位置：Main Table 3 或 Appendix。
- 优先级：投稿前 MUST-RUN，但不是 first pilot 前置项。

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

## 运行顺序与里程碑

| Milestone | 目标 | Runs | 决策 Gate | 成本 | 风险 |
|-----------|------|------|-----------|------|------|
| M0 | A800 single-host automation ready | R000-R005 | ARIS nightly dry-run can read tracker and write summary | low | server/env unknown |
| M1 | protocol freeze | R010-R019 | failure families reproducible and non-saturated | low-med | injection too artificial |
| M2 | baseline ladder | R020-R029 | heuristic has gap and oracle gap exists | med | heuristic too strong |
| M3 | memory counterfactual | R030-R039 | memory flip gain significant in expected families and not in negative-control | med-high | no memory effect |
| M4 | ablations/VLM | R040-R059 | input source understood; VLM does not invalidate story | med-high | VLM stronger |
| M5 | paper package | R060-R079 | figures/tables reproducible from artifacts | med | analysis drift |

## 计算与数据预算

- 总 GPU-hours：在 A800 env 和 simulator throughput 实测前未知。Day 2 throughput benchmark 后估算。
- 规划假设：MuJoCo rollout 可能受 CPU/simulator 限制；A800 主要价值在 batched RL/PPO、VLM 和并行队列。
- 数据准备：
  - seed split files
  - failure family config files
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
  - 缓解：按项目规则，week-3 smoke gate 失败则切到 MuJoCo Playground。
- 实验 claim 漂移：
  - 缓解：看结果前冻结 failure definitions 和 seed splits。
- heuristic baseline 获胜：
  - 缓解：pivot 到 diagnostic/protocol paper；不强行讲 RL story。
- memory effect 缺失：
  - 缓解：如果 protocol 强，报告 negative result；否则 pivot 到 failure-injection/testbed。
- artifacts 过大：
  - 缓解：nightly retention policy：所有 run 保留 summary 和 selected traces；full replay 只保留 held-out / failure cases。

## 最终检查清单

- [x] A800 single-host execution path documented；证据：`docs/a800_machine_profile.md`、`refine-logs/EXPERIMENT_TRACKER.md`。
- [x] machine-local ARIS resources documented；证据：`AGENTS.md`、`.gitignore`、`docs/a800_machine_profile.md`、`docs/rtx5090_machine_profile.md`。
- [x] experiment plan / timeline use checkable todos；证据：`refine-logs/EXPERIMENT_PLAN.md`、`refine-logs/DAILY_EXPERIMENT_TIMELINE.md`。
- [ ] main paper tables covered
- [ ] novelty isolated through matched-seed counterfactual
- [ ] simplicity defended against tuned heuristic and compressed action set
- [ ] VLM baseline run or explicitly deferred with reason
- [x] nice-to-have runs separated from must-run runs；证据：`refine-logs/EXPERIMENT_TRACKER.md` 中 `Priority` 字段。
- [ ] every night job has a morning acceptance checklist
- [ ] no runtime decision uses MuJoCo privileged ground truth

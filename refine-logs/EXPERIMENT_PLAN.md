# Experiment Plan

**Problem**: 在 frozen / mature humanoid locomotion controller 之上，验证高层 typed recovery supervisor 中的 event/body memory 是否、何时、为何能改善失败恢复，而不是只做一个工程 runtime。
**Method Thesis**: 论文应被组织为 counterfactual diagnostic study：用 seeded typed failure protocol 和 matched-seed decision-flip analysis 证明 memory 的收益只在 long-horizon / cumulative / degradation failure 中成立。
**Date**: 2026-06-25
**Execution Host Policy**: 尽量单机执行。默认 **A800_SINGLE_HOST** 为唯一主实验机；5090 只作紧急备用，不进入日常实验主线。

## Claim Map

| Claim | Why It Matters | Minimum Convincing Evidence | Linked Blocks |
|-------|-----------------|-----------------------------|---------------|
| C1: Memory-value diagnostic | 这是当前最可防守的论文主贡献；避免把 8-action supervisor 包装成 novelty | matched-seed 下 memory-on/off 的 decision flip 率、flip 条件恢复收益、95% CI、negative-control 上无显著收益 | B2, B3, B4 |
| C2: Seeded typed failure protocol | 让 recovery 结果可以被复现、分层、反事实比较 | failure family 预注册定义、固定 seed split、controller-native/heuristic/oracle 对照、Episode Data Package | B1, B2 |
| Anti-claim A1: gain only comes from event trace/current state | 审稿人会质疑 memory 只是重命名状态 | leave-one-out: instant-only、event-only、trend-only、language-only、shuffled-memory | B3, B4 |
| Anti-claim A2: heuristic can solve everything | 若规则系统打平，RL/memory selector 没意义 | tuned heuristic supervisor 与 no-memory/full-memory 在 cumulative/degradation family 的 matched comparison | B2, B3 |
| Anti-claim A3: VLM prompt is enough | RACER/VLM recovery 近邻要求比较 | VLM-prompt supervisor 在同一 8-action space、同一 seeds、同一 summaries 上比较 latency/success | B5 |

## Paper Storyline

- Main paper must prove:
  - C1: memory 的价值是条件性的、可归因的，不是平均 success rate 小涨。
  - C2: seeded typed failure protocol 支撑 matched-seed counterfactual，而不是自造偏置 benchmark。
- Appendix can support:
  - horizon scan、更多 failure severity、VLM prompt variants、dashboard/replay case studies。
- Experiments intentionally cut:
  - 真机 G1、多本体迁移、端到端 VLA、复杂 open-vocabulary detector 主线、低层 gait/residual policy。

## Experiment Blocks

### Block 0: A800 Single-Host Reproducibility Setup

- Claim tested: 无，前置可执行性。
- Why this block exists: 当前 repo 主要是 PRD/研究产物，尚无可自动跑的代码脚手架；若不先统一 A800 环境，晚上 ARIS 无法可靠接管。
- Dataset / split / task: 无；建立 repo、env、logs、run manifests、nightly handoff 模板。
- Compared systems: 无。
- Metrics: `git status` clean、env check pass、sample artifact write pass、nightly dry-run pass。
- Setup details: A800_SINGLE_HOST 上 clone/pull 当前 branch；只允许一个 canonical code dir；所有实验产物写入不提交的 runs/logs 目录。
- Success criterion: 白天人工提交后，夜间 ARIS 能从同一 repo path 读取 tracker、启动 dry-run、写回 summary。
- Failure interpretation: 不能进入实验；先修 SSH/env/path。
- Table / figure target: 不进论文。
- Priority: MUST-RUN。

### Block 1: Seeded Typed Failure Protocol Freeze

- Claim tested: C2。
- Why this block exists: 防止“挑 memory 擅长场景”的循环论证。
- Dataset / split / task: 4 个主 family：transient/instant negative-control、long-horizon、cumulative drift、sensor/localization degradation；每类固定 train/val/test seed split。
- Compared systems: controller-native only for calibration；oracle labels只用于评价上界。
- Metrics: controller-native success rate、failure trigger reproducibility、severity bands、episode validity rate。
- Setup details: 每类从 3 个 severity 开始；主报告点选择 controller-native success 约 30-70% 的非饱和区间。
- Success criterion: 每类至少 20 个 valid pilot episodes；同一 seed 复跑 failure timing/status 一致；negative-control 明确预注册为 memory 不应收益。
- Failure interpretation: 若 failure 全 0/全 100 或不可复现，先调注入协议，不训练 supervisor。
- Table / figure target: Methods table + Appendix protocol table。
- Priority: MUST-RUN。

### Block 2: Baseline Stage

- Claim tested: C2, A2。
- Why this block exists: 先确认低层 controller、规则、no-memory supervisor 的下限和强度。
- Dataset / split / task: Block 1 的 pilot split，先 cumulative/degradation，再扩到全部 family。
- Compared systems:
  - `controller_native`
  - `rule_recovery_tuned`
  - `rl_or_bandit_instant_state`
  - `oracle_upper_bound`
- Metrics: task success、recovery success、fall/unstable count、stop latency、repeated failure count、episode validity。
- Setup details: 先 bandit sanity check，再决定是否 PPO；每个 cell 先 3 seeds × 10 episodes pilot。
- Success criterion: heuristic 不是 strawman，但在至少一个 cumulative/degradation family 上存在明显 oracle gap 和 learnable gap。
- Failure interpretation: 如果 tuned heuristic 打平 no-memory/full-memory，论文从 learned supervisor pivot 到 protocol/diagnostic。
- Table / figure target: Main Table 1 baseline ladder。
- Priority: MUST-RUN。

### Block 3: Memory-Value Counterfactual

- Claim tested: C1, A1。
- Why this block exists: 全文最关键实验，证明 memory 改变了高层动作选择且这种改变有收益。
- Dataset / split / task: matched held-out seeds；同一初始状态、同一 failure injection、同一 controller backend。
- Compared systems:
  - `instant_state`
  - `window_memory`
  - `full_event_body_memory`
  - `shuffled_memory_negative_control`
- Metrics: decision-flip rate、flip-conditioned success delta、paired bootstrap CI、McNemar / paired tests、per-action confusion matrix。
- Setup details: 所有 variants 必须共享 action set、reward、controller、planner、seed；只改 observation memory。
- Success criterion: 在 long-horizon/cumulative/degradation 至少 1-2 类中 full memory 相对 instant 有显著 flip-conditioned recovery gain；transient negative-control 上无显著收益。
- Failure interpretation: 若平均成功涨但 flip 解释不了，不能写 causality；若 negative-control 也涨，说明协议或特征泄漏。
- Table / figure target: Main Figure 1 + Table 2。
- Priority: MUST-RUN。

### Block 4: Input and Horizon Ablations

- Claim tested: A1。
- Why this block exists: 防止 reviewer 说 event trace/current state/language 才是实际来源。
- Dataset / split / task: Block 3 的 held-out seeds。
- Compared systems:
  - no memory
  - event trace only
  - body trend only
  - event + body
  - event + body + language
  - shuffled memory
  - horizon lengths: short / medium / long
- Metrics: recovery success、decision flip、over-conservatism rate、safe_stop/abort frequency。
- Setup details: 先小 grid，只有 Block 3 gate 通过后才扩大。
- Success criterion: 能定位 memory 的有效成分；不要求所有组件都有用。
- Failure interpretation: language 无效则论文标题/claim 中弱化 language-conditioned。
- Table / figure target: Main Figure 2 or Appendix Table。
- Priority: MUST-RUN after B3 pilot。

### Block 5: VLM-Prompt Supervisor and Simplicity Check

- Claim tested: A3 and simplicity。
- Why this block exists: RACER/VLM recovery 是近邻；必须证明我们不是忽略强 baseline。
- Dataset / split / task: 同一 held-out seeds，优先 target change / grounding ambiguity / cumulative failure。
- Compared systems:
  - VLM-prompt supervisor over same 8 actions
  - rule recovery
  - full memory supervisor
  - optional 3-action compressed supervisor
- Metrics: recovery success、decision latency、invalid action rate、cost per episode、same-seed action agreement。
- Setup details: VLM 只读合法状态摘要，不读 MuJoCo privileged ground truth。
- Success criterion: learned/lightweight supervisor 在 latency/reliability 或特定 failure family 上有可辩护优势；若 VLM 更强，改写成 VLM baseline/policy comparison paper。
- Failure interpretation: VLM 全面碾压则不再主打 RL policy。
- Table / figure target: Main Table 3 or Appendix。
- Priority: MUST-RUN before paper submission, not before first pilot。

### Block 6: Robustness, Packaging, and Paper Figures

- Claim tested: C1/C2 presentation robustness。
- Why this block exists: 把实验变成可投稿证据。
- Dataset / split / task: held-out seeds, severity sweep, selected qualitative episodes。
- Compared systems: only final method + key baselines。
- Metrics: CI/effect size、artifact completeness、replay validity、failure-case diversity。
- Setup details: 每个论文图表有固定 source script；不手工改图。
- Success criterion: 每个 main claim 有表/图支撑，失败案例与 limitations 一致。
- Failure interpretation: 如果图无法复现，停止写作先修 analysis pipeline。
- Table / figure target: 全部 main/appendix figures。
- Priority: MUST-RUN for writing week。

## Run Order and Milestones

| Milestone | Goal | Runs | Decision Gate | Cost | Risk |
|-----------|------|------|---------------|------|------|
| M0 | A800 single-host automation ready | R000-R005 | ARIS nightly dry-run can read tracker and write summary | low | server/env unknown |
| M1 | protocol freeze | R010-R019 | failure families reproducible and non-saturated | low-med | injection too artificial |
| M2 | baseline ladder | R020-R029 | heuristic has gap and oracle gap exists | med | heuristic too strong |
| M3 | memory counterfactual | R030-R039 | memory flip gain significant in expected families and not in negative-control | med-high | no memory effect |
| M4 | ablations/VLM | R040-R059 | input source understood; VLM does not invalidate story | med-high | VLM stronger |
| M5 | paper package | R060-R079 | figures/tables reproducible from artifacts | med | analysis drift |

## Compute and Data Budget

- Total estimated GPU-hours: unknown until A800 env and simulator throughput are measured. Use Day 2 throughput benchmark to estimate.
- Planning assumption: MuJoCo rollout may be CPU/simulator-bound; A800 matters most for batched RL/PPO, VLM, and parallel experiment orchestration.
- Data preparation needs:
  - seed split files
  - failure family config files
  - episode manifest schema
  - artifact retention policy
- Human evaluation needs:
  - daily morning review of overnight logs
  - gate decisions before expanding runs
- Biggest bottleneck:
  - G1/MuJoCo controller smoke gate and reproducible failure injection, not PPO itself.

## Risks and Mitigations

- A800 server details missing:
  - Mitigation: Day 1 creates `CLAUDE.md`/server stanza or equivalent private handoff; no night automation before this passes.
- G1 controller integration fails:
  - Mitigation: by project rule, switch main evidence path to MuJoCo Playground humanoid backend if week-3 smoke gate fails.
- Experiment claims drift:
  - Mitigation: freeze failure definitions and seed splits before seeing results.
- Heuristic wins:
  - Mitigation: pivot to diagnostic/protocol paper; do not force RL story.
- Memory effect absent:
  - Mitigation: report negative result if protocol is strong; otherwise pivot to failure-injection/testbed contribution.
- Artifacts too large:
  - Mitigation: nightly retention policy: keep summaries and selected traces for all, full replay only for held-out / failure cases.

## Final Checklist

- [ ] A800 single-host execution path documented
- [ ] Main paper tables are covered
- [ ] Novelty is isolated through matched-seed counterfactual
- [ ] Simplicity is defended against tuned heuristic and compressed action set
- [ ] VLM baseline is either run or explicitly deferred with reason
- [ ] Nice-to-have runs are separated from must-run runs
- [ ] Every night job has a morning acceptance checklist
- [ ] No runtime decision uses MuJoCo privileged ground truth

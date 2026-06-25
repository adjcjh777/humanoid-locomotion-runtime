# 每日实验时间线

**日期**: 2026-06-25
**主机策略**: A800 单机主线。5090 只作为备用，不主动分裂实验环境。
**工作节奏**: 白天由人完成设计、实现、审查、gate 决策；晚上交给 ARIS 做可自动化的 smoke / queue / monitor / summarize。
**核心规则**: 每个晚上只能跑“白天已经冻结输入、验收标准和回滚条件”的任务。没有白天 handoff，不跑夜间自动实验。
**待办规则**: 可执行事项使用 `- [ ]` / `- [x]`；完成项必须附带可复查证据路径、run id、commit id 或 tracker 记录。

## 每日固定节奏

### 09:00-10:00 次日验收检查

- 阅读昨晚 ARIS summary。
- 检查失败 jobs、OOM、stale screen、磁盘占用、episode artifact 完整性。
- 决定当天是继续扩量、修 bug、还是停止当前分支。
- 只提交代码/config/summary，不提交 raw runs、logs、checkpoints、weights。

### 10:00-12:30 白天构建块 A

- 做需要人判断的代码/协议/配置。
- 更新 tracker 的 `Status` 和 `Notes`。
- 对任何会影响论文 claim 的变更写清楚 reason。

### 14:00-18:30 白天构建块 B

- 补测试、跑小规模本地/A800 smoke。
- 产出 night handoff：要跑哪些 run id、输入 config、成功标准、失败处理。
- commit/push 后再让 ARIS 夜间接管。

### 21:00-08:00 夜间 ARIS 任务

- ARIS 只跑 tracker 中明确标为 Night 的 run。
- 自动记录 queue state、logs、metrics、artifact paths。
- 结束后写 morning summary，不直接修改论文 claim。

## 第 1 周：单机实验地基与协议冻结

### 第 1 天：打通 A800 单机环境和 ARIS handoff

**白天人工**

- [x] 记录公共安全机器档案：`docs/a800_machine_profile.md` 和 `docs/rtx5090_machine_profile.md`。
- [x] 确认 A800 canonical repo path、当前分支、Python、conda/uv、GPU 可见性；证据见 `docs/a800_machine_profile.md`。
- [x] 在 A800 上 pull 到当前 branch，并保持 `git status` 干净。
- [x] 将 `.agents/` 和 `.aris/installed-skills-codex.txt` 改为本机资源，不进 git；规则见 `AGENTS.md` 和 `.gitignore`。
- [x] 在 A800 本机用 `--no-doc` 重新初始化 ARIS Codex skills；本机 manifest 被 `.gitignore` 忽略。
- [x] 确认 `.gitignore` 覆盖 `runs/`、`logs/`、`artifacts/`、`checkpoints/`、`weights/`、`datasets/` 和 ARIS 本机资源。
- [x] 更新 `refine-logs/EXPERIMENT_TRACKER.md` 中 R000 状态为 `DONE`。
- [ ] 在私有/安全位置记录 A800 公司网络访问方式；不要把 SSH、IP、token、jump-host 细节写进 repo。
- [ ] 为 R001/R002/R003/R005 补齐 night handoff 的输入路径、成功标准、失败处理和输出 summary 路径。
- [ ] 白天结束前 commit/push tracker、timeline、plan、handoff 相关文档。

**晚上 ARIS**

- [ ] R001: repo sync dry-run。
- [ ] R002: environment smoke。
- [ ] R003: artifact write smoke。
- [ ] R005: nightly handoff dry-run。

**次日验收**

- [ ] A800 上 `git status` 干净。
- [ ] ARIS summary 能写回指定 summary 文件。
- [ ] 若 env 不通，Day 2 不进入代码实验，先修 A800。

### 第 2 天：Schema-first scaffolding 与 throughput 估算

**白天人工**

- 实现或规划核心 schema：command/status/failure/recovery/memory/episode metadata。
- 写最小 serialization test。
- 明确 Episode Data Package 的最小字段和目录结构。
- 设计 synthetic rollout loop，用于估算 steps/sec 和 MB/episode。

**晚上 ARIS**

- R004: throughput microbenchmark。
- R003 repeat: sample Episode Data Package skeleton 写入检查。
- 自动生成一份 disk budget estimate。

**次日验收**

- 估算 100/1k/10k episodes 的磁盘占用。
- 若单 episode artifact 太大，先调 retention policy。

### 第 3 天：Event logger 与 run manifest

**白天人工**

- 实现 event logger / run manifest skeleton。
- 固定 run id 命名：日期、run group、variant、seed。
- 定义夜间 ARIS summary 模板：status、failed jobs、metrics、artifact paths、gate decision。
- 写 schema roundtrip tests。

**晚上 ARIS**

- 跑 20-50 个 synthetic episodes，生成 EDP。
- 跑 artifact validator。
- 生成 summary：缺字段、坏 JSON、磁盘占用。

**次日验收**

- EDP validator 通过率 100%。
- 若 validator 不稳定，不进入 MuJoCo。

### 第 4 天：MuJoCo / G1 backend smoke

**白天人工**

- 集成或定位 G1 model/controller backend。
- 实现最小 `stand_ready` / `safe_stop` / `track_velocity` smoke command。
- 明确如果 G1 不通，MuJoCo Playground fallback 的入口和接口差异。

**晚上 ARIS**

- 运行 `stand_ready` smoke。
- 运行短 `track_velocity` smoke。
- 记录 crash、unstable、controller command logs。

**次日验收**

- G1 至少能稳定站立和短时 velocity tracking。
- 若不通，白天只修 backend，不做 failure protocol。

### 第 5 天：Controller-native baseline skeleton

**白天人工**

- 实现 `controller_native` run path。
- 定义 basic local target approach 的 success/failure 判据。
- 确认 MuJoCo privileged signals 只进入 evaluation，不进入 runtime decision。

**晚上 ARIS**

- 跑 20 个 controller-native no-failure episodes。
- 记录 task success、fall/unstable、episode validity。

**次日验收**

- 无 failure 场景成功率应足够高，否则 runtime 地基未稳。
- 若 no-failure 都不稳，暂停 recovery 研究，修 controller/backend。

### 第 6 天：Failure family 预注册草案

**白天人工**

- 写定 4 个主 failure family 的操作定义：
  - transient/instant negative-control
  - long-horizon
  - cumulative drift
  - sensor/localization degradation
- 为每类定义 trigger、severity、success/failure、预期 memory effect。
- 冻结初版 seed split 草案。

**晚上 ARIS**

- 不扩量训练，只跑每类 5-10 个 feasibility episodes。
- 自动输出 trigger timing 和 controller-native success 粗分布。

**次日验收**

- 若某 family 无法稳定触发，Day 7 先改 protocol。
- 不允许根据 memory 结果改 family 定义，因为此时还不应训练 memory policy。

### 第 7 天：Protocol freeze gate

**白天人工**

- 审核 Day 6 feasibility。
- 冻结 failure family、seed split、severity 选择规则。
- 写入 protocol doc/config；标明 negative-control family。
- 更新 tracker R010-R017 状态。

**晚上 ARIS**

- R011-R014: 每类 pilot 20 episodes。
- R017: Episode Data Package validation。

**次日验收**

- 每类 valid episode >= 20。
- controller-native 成功率不应全 0 或全 100。
- 若不满足，Week 2 不启动 baseline ladder，先重做 severity。

## 第 2 周：Baseline ladder 与 bandit sanity

### 第 8 天：Severity calibration

**白天人工**

- 查看 Week 1 pilot 分布。
- 选择每个 family 的主报告 severity band。
- 记录为什么选择该 band，避免 self-serving benchmark。

**晚上 ARIS**

- R015: all-family severity calibration。
- 生成每类 severity × success rate 表。

**次日验收**

- 至少 3 个 family 有非饱和 severity。
- negative-control family 仍保持清晰定义。

### 第 9 天：Tuned heuristic baseline 设计

**白天人工**

- 实现或写定 `rule_recovery_tuned`。
- 明确规则输入只能用 runtime 合法 status/failure signals。
- 做人工 code review：不能读 privileged failure type 或 ground truth pose。

**晚上 ARIS**

- R020: controller-native baseline。
- R021: tuned rule baseline pilot。

**次日验收**

- rule baseline 不能太弱；如果 obvious rule 都没做，重调。
- 如果 rule 已经接近 oracle，后续 RL/memory story 高风险。

### 第 10 天：Oracle upper bound 和标签来源

**白天人工**

- 实现 evaluation-only `oracle_upper_bound`。
- 写清 oracle 可用哪些 privileged signals。
- 写清 supervisor 的训练 label/reward 来源，避免信息泄漏。

**晚上 ARIS**

- R022: oracle upper bound pilot。
- 自动计算 oracle gap。

**次日验收**

- 如果 `oracle - rule` gap 太小，说明任务没有 recovery 学习空间。
- 若 oracle 使用泄漏路径进入 runtime，立即修。

### 第 11 天：Instant-state bandit sanity

**白天人工**

- 实现 `instant_state` observation。
- 实现 bandit sanity trainer 或最小 action selector。
- 固定 reward：task progress、安全、recovery、latency、repeated failure penalty。

**晚上 ARIS**

- R023: instant-state bandit sanity。
- 输出 action distribution 和 per-family success。

**次日验收**

- 如果 instant-state 学不动，先查 reward/action semantics。
- 不直接上 PPO。

### 第 12 天：Full-memory bandit sanity

**白天人工**

- 实现 event/body memory summary。
- 明确 memory horizon 初值。
- 加 shuffled-memory negative-control 的数据管线入口。

**晚上 ARIS**

- R024: full-memory bandit sanity。
- 初步比较 instant vs full-memory。

**次日验收**

- 只看方向性，不写论文结论。
- 若 full-memory 没有任何信号，先做 feature audit。

### 第 13 天：Baseline gate review

**白天人工**

- 汇总 R020-R024。
- 判断是否满足：
  - rule baseline 有效但不封顶
  - oracle gap 存在
  - memory 有至少方向性信号
- 决定 Week 3 是否进入 matched-seed counterfactual。

**晚上 ARIS**

- 补跑失败的 baseline cells。
- 生成 baseline ladder summary。

**次日验收**

- 若 gate 不过，停止扩量；写 pivot note。
- 若 gate 通过，冻结 Week 3 config。

### 第 14 天：第 2 周清理与提交

**白天人工**

- 清理 config、tests、analysis scripts。
- commit/push Week 2 可复现代码和 summary。
- 更新 tracker 状态。

**晚上 ARIS**

- 只跑 regression smoke，不跑新实验。

**次日验收**

- 主分支/feature branch 可从干净 clone 重现 baseline smoke。

## 第 3 周：Matched-seed memory-value counterfactual

### 第 15 天：Matched-seed runner

**白天人工**

- 实现同一 seed 下多 variant replay/rollout 的 runner。
- 确保只改变 observation memory，不改变 controller/planner/reward/action set。

**晚上 ARIS**

- R030-R033 小规模 matched run。

**次日验收**

- 每个 matched group 都有相同 seed、failure config、initial condition。

### 第 16 天：Decision logging and flip extraction

**白天人工**

- 记录每个 supervisor decision：timestamp、observation hash、action、confidence/logit、failure mode。
- 实现 decision pair matching。

**晚上 ARIS**

- R034 pilot decision-flip extraction。

**次日验收**

- 能生成 per-seed decision flip table。
- 若 action timestamps 对不上，修 logging。

### 第 17 天：Full matched pilot

**白天人工**

- 审核 Day 16 flip table。
- 修 replay mismatch。
- 冻结 first matched held-out subset。

**晚上 ARIS**

- R030-R033 扩到 first held-out subset。
- R035 bootstrap/McNemar 初版。

**次日验收**

- 看 long-horizon/cumulative/degradation 是否有方向性 memory gain。
- 看 transient negative-control 是否无显著收益。

### 第 18 天：Negative-control audit

**白天人工**

- 专门审查 transient/instant negative-control。
- 查是否存在 feature leakage 或 severity bias。

**晚上 ARIS**

- 补跑 shuffled-memory negative-control。
- 生成 false gain report。

**次日验收**

- 如果 negative-control 也涨，暂停所有 claim，修 protocol/feature。

### 第 19 天：Memory feature audit

**白天人工**

- 审查 event trace、body trend、language context 是否各自合法。
- 写 leave-one-out config。

**晚上 ARIS**

- R040-R042 小规模 ablation。

**次日验收**

- 找到主要有效成分或确认无效成分。

### 第 20 天：Horizon scan

**白天人工**

- 定义 short/medium/long horizon。
- 确认 horizon 不改变其他模型容量或训练预算。

**晚上 ARIS**

- R043 horizon scan。

**次日验收**

- 若 longer horizon 反而退化，记录 over-history limitation。

### 第 21 天：第 3 周 gate

**白天人工**

- 汇总 Week 3:
  - decision flip rate
  - flip-conditioned gain
  - negative-control result
  - CI/effect size
- 决定是否继续主打 memory-value diagnostic。

**晚上 ARIS**

- 补跑缺失 cells 或 regression smoke。

**次日验收**

- Gate 通过：进入 VLM baseline 和图表。
- Gate 失败：转 protocol/diagnostic negative result，不再扩 PPO。

## 第 4 周：VLM baseline、图表和论文证据

### 第 22 天：VLM-prompt supervisor spec

**白天人工**

- 写 VLM prompt 输入规范：只读合法状态摘要，不读 privileged ground truth。
- 定义 invalid action、latency、cost per episode。
- 选定要比较的 failure family。

**晚上 ARIS**

- R045 小规模 VLM-prompt pilot。

**次日验收**

- 如果 VLM invalid/action latency 太高，记录为效率劣势。
- 如果 VLM 明显更强，准备 pivot story。

### 第 23 天：VLM vs learned comparison

**白天人工**

- 审核 VLM pilot。
- 固定 fair comparison: same seeds, same summaries, same 8 actions。

**晚上 ARIS**

- R045/R046 扩量比较。

**次日验收**

- 判断 learned supervisor 是否仍可作为主线。

### 第 24 天：主表格

**白天人工**

- 确定 Main Table 1/2/3 的行列和 metrics。
- 写 analysis script，不手工改数。

**晚上 ARIS**

- R060 main table generation。
- 自动输出 csv/md 和 source paths。

**次日验收**

- 表中所有数字可追溯到 run ids。

### 第 25 天：主图

**白天人工**

- 确定 Figure 1: per-family success + CI。
- 确定 Figure 2: memory-value / decision-flip / horizon。

**晚上 ARIS**

- R061/R062 figure generation。

**次日验收**

- 图可复现；CI/effect size 正确。

### 第 26 天：Case studies 和 failure review

**白天人工**

- 选择 case study 原则：不能只挑成功；必须包含 failure/limitation。
- 审查 replay artifacts。

**晚上 ARIS**

- R063 candidate case extraction。
- 生成 replay index。

**次日验收**

- 每个 case 对应一个论文论点或 limitation。

### 第 27 天：Evidence package audit

**白天人工**

- 审核所有 claims 是否都有证据。
- 删掉没有证据支撑的 claim。
- 写 limitation checklist。

**晚上 ARIS**

- R070 paper evidence package audit。
- 检查 artifact completeness、missing seeds、failed jobs。

**次日验收**

- 若缺关键 evidence，Day 28 只补关键 runs，不加新想法。

### 第 28 天：最终决策与 handoff

**白天人工**

- 做 go/pivot/stop 决策。
- 若 go：进入 paper writing。
- 若 pivot：重写 title/contributions。
- 若 stop：保留 protocol/negative result，总结为什么。

**晚上 ARIS**

- 只做 final summary，不再启动新实验。

**次日验收**

- 产生可交给 paper-writing 的 evidence handoff。

## 每晚交给 ARIS 的 Handoff 模板

```markdown
# 夜间 ARIS Handoff

日期：
主机：A800_SINGLE_HOST
分支：
提交：

## 本晚要启动的 runs
- Run IDs：
- 配置文件：
- 预期输出：

## 成功标准
- TODO

## 停止条件
- TODO

## 禁止事项
- 不修改论文 claim。
- 不把 privileged MuJoCo truth 当作 runtime input。
- 不提交 raw logs、checkpoints、weights 或 generated replay dumps。

## 次日必须产出的 summary
- completed / failed / stuck jobs
- metrics table
- artifact paths
- disk usage
- gate recommendation
```

## 每日 Commit 规则

- 白天结束前 commit/push code, config, docs, trackers。
- 夜间 ARIS 不直接提交 raw outputs。
- 次日早上只提交 curated summaries、small analysis tables、config fixes。
- 每个 gate 通过或失败都要在 tracker notes 中记录。

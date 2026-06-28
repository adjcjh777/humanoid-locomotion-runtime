# R047a 统计设计冻结草案

**日期**: 2026-06-28  
**状态**: Mac-safe draft freeze；R047 final statistical design 仍等待 B1/B2 pilot evidence  
**适用范围**: 只冻结统计设计字段和判定语言，不授权 final evaluation、论文主结论或 counterfactual / ATE 措辞。

## 边界

- [x] 本文件可以在 Mac 上完成，因为它只引用已提交的 protocol、seed split、schema 和 tracker。
- [x] primary endpoint、seed source、cluster bootstrap、multiplicity control 和 negative-control equivalence 的字段已写清。
- [x] 本文件不使用 A800 私有运维信息、raw logs、checkpoints、weights 或 run artifacts。
- [ ] R047 final 只有在 R011-R017 pilots、R020-R027 baselines 和实际 throughput/sample budget 明确后才能打勾。
- [ ] 任何 final claim 都必须回指具体 run id、EDP artifact、summary 或 figure/table source。

## Primary Endpoint 草案

- [x] 主 endpoint 沿用 `configs/failure_protocol.v0.toml` 的 `primary_endpoint = "recovery_success"`。
- [x] `recovery_success` 只在 valid EDP episode 上统计；episode invalid、schema incomplete、unsafe completion 或 fall 必须单独报告，不得 silently drop。
- [x] 主比较优先限定在预注册 memory-positive cells；negative-control cells 不用于制造平均收益叙事。
- [x] 同时报告 `policy_only_outcome`、`full_stack_with_fallback_outcome`、fallback invocation rate 和 safety override rate，避免 rule fallback 把 learned policy 结果抬高。
- [ ] Final endpoint 的 exact denominator、episode validity rule 和 missing-artifact rule 需在 B1/B2 artifacts 出现后冻结。

## Seed 与 Split

- [x] Scenario seeds 使用 `configs/seed_splits.v0.toml`：dev 12、train 64、val 16、test 32。
- [x] Policy training seeds 使用 `configs/seed_splits.v0.toml`：pilot `[61001]`，final `[61001, 61037, 61073, 61109, 61145]`。
- [x] Pilot 结果只能用于 calibration、debugging 和 go/no-go，不写 final effect。
- [x] Final evaluation 必须在 test seeds 上完成；若 B1/B2 后缩小样本，必须把结论降级为 pilot diagnostic。
- [ ] 每个 selected failure cell 的 exact final sample count 等待 R015 severity calibration 和 throughput budget。

## 统计估计

- [x] 如果 R018 deterministic snapshot branching 通过，主估计可以使用 branch-level paired outcome difference；否则统一称为 paired matched-seed diagnostic。
- [x] Cluster bootstrap 至少按 policy training seed 和 scenario seed 分层；有 snapshot branch 时还要按 base snapshot / decision id 聚类。
- [x] Decision flip rate 和 flip-conditioned gain 只作为解释性指标，不单独证明 causal effect。
- [x] R034a 已提供 Mac-safe decision pair matching skeleton；真正 R034 仍需 pilot artifacts。
- [ ] Hierarchical bootstrap implementation 和 confidence interval source script 等待 B3/B4 artifacts。

## Multiplicity Control

- [x] Confirmatory family 草案：typed event/body memory 对比 `instant_mlp`、`frame_stack_raw_history`、`GRU_raw_history`，优先 memory-positive cells。
- [x] Confirmatory pairwise comparisons 使用 Holm-style multiplicity control；exploratory family-wise plots 可另报 unadjusted 与 FDR，但不能混为主结论。
- [x] Horizon、event-only、body-only、language ablation 属于 secondary/exploratory，必须和主 endpoint 分开标注。
- [ ] Final comparison family 等待 B2 gate 后冻结；如果 tuned heuristic 打平或 oracle gap 不存在，必须 pivot。

## Negative Control 与 SEI

- [x] Negative-control 不允许用 p 值不显著写成“没有效果”。
- [x] 当前 smallest effect size of interest 草案：absolute recovery-success difference `0.05`；negative-control equivalence margin 暂定 `[-0.05, 0.05]`。
- [x] TOST / equivalence 风格证据必须报告 confidence interval 与 margin 的关系。
- [x] 如果 negative-control 也出现超过 SEI 的收益，优先判定 protocol、feature 或 leakage 风险，而不是扩大 claim。
- [ ] SEI final value 需结合 B1 controller-native variance、B2 baseline variance 和实际 cost 后确认。

## 当前 Gate Decision

- [x] 可以继续在 Mac 上维护 statistical-design 文档、run id naming 和 decision-flip extraction code。
- [ ] 不能启动 PPO、大规模 rollout、final evaluation 或 paper main claim。
- [ ] 不能把 Mac fake provider、dashboard skeleton、decision-flip unit test 或 statistical draft 写成 A800 experiment evidence。

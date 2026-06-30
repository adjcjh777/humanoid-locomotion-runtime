# G1 23DoF Controller Stage A Handoff

**日期**: 2026-06-30
**状态**: Stage A ForwardFlat multi-seed complete; mature controller evidence pending

## 目的

- [x] 启动 `company_g1_edu_23dof` locomotion policy controller 的 Stage A 直行稳定性训练。
- [x] 使用 repo-local `Unitree-G1-23Dof-ForwardFlat` task，不修改 Unitree submodule tracked source。
- [x] 保持 29DoF 官方 policy 为 reference-only，不把本轮结果直接写成 mature controller evidence。

## Running Jobs

| Seed | GPU | tmux session | Run name | Task | 状态 |
|---:|---:|---|---|---|---|
| 101 | 1 | `g1ff_s101_20260630T034920Z` | `a800_g1_23dof_forwardflat_seed101_4096env_10001iter_20260630T034920Z` | `Unitree-G1-23Dof-ForwardFlat` | complete |
| 102 | 2 | `g1ff_s102_20260630T034920Z` | `a800_g1_23dof_forwardflat_seed102_4096env_10001iter_20260630T034920Z` | `Unitree-G1-23Dof-ForwardFlat` | complete |
| 103 | 3 | `g1ff_s103_20260630T034920Z` | `a800_g1_23dof_forwardflat_seed103_4096env_10001iter_20260630T034920Z` | `Unitree-G1-23Dof-ForwardFlat` | complete |

## Launch Settings

- [x] `NUM_ENVS=4096`
- [x] `MAX_ITERATIONS=10001`
- [x] `SAVE_INTERVAL=250`
- [x] `mamba env=robot`
- [x] `MUJOCO_GL=egl`
- [x] 并发策略：3 张 GPU，每张 GPU 1 个训练任务；未启用单 GPU 多任务。

## Health Check

- [x] 2026-06-30 03:54 UTC: 三个 tmux sessions 仍在运行，无 OOM 迹象。
- [x] 2026-06-30 03:54 UTC: seeds `101/102/103` 均约在 learning iteration `216/10001`，steps/s 约 `69k-71k`，ETA 约 `03:46`。
- [x] 2026-06-30 03:54 UTC: GPU memory/util snapshot：GPU 1 `3285 MiB / 72%`，GPU 2 `3569 MiB / 54%`，GPU 3 `2727 MiB / 69%`。
- [x] 2026-06-30 04:02 UTC: 三个训练 sessions 仍在运行；seed `101` 约在 learning iteration `522/10001`，mean reward `34.52`，`fell_over=0.0417`，ETA 约 `03:37`。
- [x] 2026-06-30 07:46 UTC: 三个训练 sessions 已结束；seeds `101/102/103` 均到 `Learning iteration 10000/10001`，输出 `model_10000.pt` 和 `policy.onnx`。
- [x] 2026-06-30 08:30 UTC: 三个最终 `policy.onnx` 已验证为 input `obs [1,80]`、output `actions [1,23]`。
- [x] 早期 `fell_over` 偏高只作为 warm-up 观察，不作为 acceptance 或 failure decision；最终 gate 以后续 command-grid eval 为准。

## Intermediate Eval

- [x] 2026-06-30 03:58 UTC: 使用空闲 GPU `4/5/6` 对 seeds `101/102/103` 的 `model_250.pt` 启动 command-grid eval；每张 GPU 1 个 eval job，无 OOM。
- [x] 2026-06-30 04:00 UTC: 三个 eval jobs 完成，JSON 写入 ignored `runs/unitree_g1_23dof_eval/Unitree-G1-23Dof-ForwardFlat_20260630T040052Z.json`、`...040054Z.json`、`...040055Z.json`。
- [x] `model_250.pt` 中途 sanity 结果：stand command 稳定，`done_fraction=0.0`；forward slow/mid/fast 没有 done，但 lateral drift 已明显偏大，fast forward 的 mean lateral displacement 约 `-2.275m` 到 `-3.777m`，max abs lateral displacement 最高约 `8.009m`。
- [x] yaw-only / lateral-only commands 在 `model_250.pt` 上 `done_fraction=1.0`，符合 Stage A 早期 checkpoint 预期，不作为失败结论。
- [ ] `model_250.pt` 不合格，不能作为 mature controller evidence；最终仍需对更后期 checkpoints 做 command-grid selection。
- [x] 2026-06-30 04:08 UTC: `model_500.pt` 首次并发 eval 暴露 output filename collision：旧命名只有 `task + timestamp`，两个 seed 同秒结束时 JSON 会互相覆盖；日志仍保留，但该批 JSON 不作为完整 evidence。
- [x] 2026-06-30 04:09 UTC: `scripts/eval_unitree_g1_23dof_command_grid.py` 已修复输出命名，加入 run directory、checkpoint stem 和 seed；scoped ruff/pytest/py_compile 通过。
- [x] 2026-06-30 04:11 UTC: `model_500.pt` 三 seed eval 重跑完成，三个唯一 JSON 写入 ignored `runs/unitree_g1_23dof_eval/*model_500_seed*.json`。
- [x] `model_500.pt` 趋势优于 `model_250.pt`：stand command 稳定，forward slow/mid/fast `done_fraction=0.0`，forward fast mean forward displacement 约 `8.13m / 8.58m / 9.17m`。
- [ ] `model_500.pt` 仍不合格：forward fast max abs lateral displacement 仍约 `6.724m-8.004m`，seed `103` 的 `lateral_right` 出现 `done_fraction=0.562` 且 max abs lateral displacement `14.536m`。
- [x] 2026-06-30 04:18 UTC: `model_1000.pt` 三 seed eval 完成，唯一 JSON 写入 ignored `runs/unitree_g1_23dof_eval/*model_1000_seed*.json`。
- [x] `model_1000.pt` 继续改善：stand command 稳定，forward slow/mid/fast `done_fraction=0.0`，forward fast mean forward displacement 约 `8.96m-9.20m`，max abs lateral displacement 降到约 `4.890m-5.745m`。
- [ ] `model_1000.pt` 仍不合格：forward straight lateral drift 仍偏大，且 seed `102` 的 `lateral_left` 出现 `done_fraction=0.297`、mean lateral displacement `-3.776m`、max abs lateral displacement `9.722m`。
- [x] 2026-06-30 04:26 UTC: `model_1250.pt` 三 seed eval 完成，唯一 JSON 写入 ignored `runs/unitree_g1_23dof_eval/*model_1250_seed*.json`。
- [x] `model_1250.pt` 单 seed 出现更低 forward-fast max lateral：seed `103` max abs lateral displacement `4.620m`，但 seed `101/102` 仍约 `6.123m/5.964m`。
- [ ] `model_1250.pt` 仍不合格：seed `102` 的 `lateral_left` `done_fraction=0.562`、max abs lateral displacement `8.663m`；seed `103` 的 `lateral_right` `done_fraction=0.688`、max abs lateral displacement `12.261m`。
- [x] 2026-06-30 04:31 UTC: `model_1500.pt` 三 seed eval 完成，唯一 JSON 写入 ignored `runs/unitree_g1_23dof_eval/*model_1500_seed*.json`。
- [x] `model_1500.pt` forward fast 仍 `done_fraction=0.0`，mean forward displacement 约 `9.00m-9.14m`，forward fast max abs lateral displacement 约 `5.035m-6.045m`。
- [ ] `model_1500.pt` 仍不合格：cross-seed straight drift 没有单调改善，lateral commands 仍不稳定，不能作为 mature controller evidence。
- [x] 2026-06-30 04:35 UTC: 新增 `scripts/summarize_unitree_g1_23dof_eval.py`，可按 `selection_penalty` 汇总 command-grid eval JSON，辅助 checkpoint selection；该 penalty 只是 triage，不是 gate decision。
- [x] 2026-06-30 04:40 UTC: `model_2000.pt` 三 seed eval 完成，唯一 JSON 写入 ignored `runs/unitree_g1_23dof_eval/*model_2000_seed*.json`。
- [x] `model_2000.pt` 是当前最佳中途点：forward fast `done_fraction=0.0`，mean forward displacement 约 `9.08m-9.39m`；seed `103` 的 forward fast mean lateral displacement `-0.025m`、max abs lateral displacement `4.695m`。
- [ ] `model_2000.pt` 仍不合格：seed `101/102` 的 forward fast max abs lateral displacement 仍约 `5.241m/5.570m`，cross-seed straight stability 还不够；lateral commands 仍不稳定，不能作为 mature controller evidence。
- [x] 2026-06-30 04:51 UTC: `model_2500.pt` 三 seed eval 完成，唯一 JSON 写入 ignored `runs/unitree_g1_23dof_eval/*model_2500_seed*.json`。
- [x] `model_2500.pt` 是当前最佳跨 seed 中途点：三 seed forward fast `done_fraction=0.0`，mean forward displacement 约 `9.18m`，max abs lateral displacement across seeds 约 `5.037m`，mean abs lateral displacement 约 `0.844m`。
- [ ] `model_2500.pt` 仍不合格：seed `102` forward fast max abs lateral 仍 `5.037m`，lateral-left max abs lateral `6.838m`；seed `103` lateral-right max abs lateral `8.372m`，lateral commands 仍不稳。
- [x] 2026-06-30 04:54 UTC: `scripts/summarize_unitree_g1_23dof_eval.py` 增加 `--group-by checkpoint`，支持按 checkpoint 聚合 multi-seed 指标；selection 仍需同时看 mean penalty、worst-case lateral drift 和 lateral/yaw command stability。
- [x] 2026-06-30 05:02 UTC: `model_3000.pt` 三 seed eval 完成，唯一 JSON 写入 ignored `runs/unitree_g1_23dof_eval/*model_3000_seed*.json`。
- [x] `model_3000.pt` forward fast 仍 `done_fraction=0.0`，mean forward displacement 约 `9.287m`，max abs lateral displacement across seeds 约 `5.148m`。
- [ ] `model_3000.pt` 聚合略弱于 `model_2500.pt`：forward fast mean abs lateral displacement 约 `0.927m`，lateral commands 仍不稳，不能作为 mature controller evidence。
- [x] 2026-06-30 05:16 UTC: `model_3500.pt` 三 seed eval 完成，唯一 JSON 写入 ignored `runs/unitree_g1_23dof_eval/*model_3500_seed*.json`。
- [x] `model_3500.pt` forward fast 仍 `done_fraction=0.0`，mean forward displacement 约 `9.407m`，mean abs lateral displacement 约 `0.703m`，但 max abs lateral displacement across seeds 约 `5.372m`。
- [ ] `model_3500.pt` 仍不合格：seed `103` 的 `lateral_right` max abs lateral displacement 约 `13.128m`，lateral commands 仍不稳；继续训练没有单调消除侧向串扰，后续需要 command-bin / cross-axis reward。
- [x] 2026-06-30 05:25 UTC: `model_4000.pt` 三 seed eval 完成，唯一 JSON 写入 ignored `runs/unitree_g1_23dof_eval/*model_4000_seed*.json`。
- [x] `model_4000.pt` 是当前 fixed-forward 指标最好的中途点：三 seed forward fast `done_fraction=0.0`，mean forward displacement 约 `9.286m`，mean abs lateral displacement 约 `0.457m`，max abs lateral displacement across seeds 约 `4.641m`。
- [ ] `model_4000.pt` 仍不合格：yaw/lateral command `done_fraction` 仍可到 `1.0`，seed `103` lateral-right max abs lateral displacement 约 `9.211m`，不能作为 mature controller evidence。
- [x] 2026-06-30 05:37 UTC: `model_4500.pt` 三 seed eval 完成，唯一 JSON 写入 ignored `runs/unitree_g1_23dof_eval/*model_4500_seed*.json`。
- [x] `model_4500.pt` forward fast 仍 `done_fraction=0.0`，mean forward displacement 约 `9.241m`，mean abs lateral displacement 约 `0.517m`，max abs lateral displacement across seeds 约 `4.688m`。
- [ ] `model_4500.pt` 聚合略弱于 `model_4000.pt`：selection penalty mean 约 `5.124`、max 约 `5.762`，lateral/yaw commands 仍不稳，seed `103` lateral-right max abs lateral displacement 约 `11.817m`，不能作为 mature controller evidence。
- [x] 2026-06-30 05:55 UTC: `model_5000.pt` 三 seed eval 完成，唯一 JSON 写入 ignored `runs/unitree_g1_23dof_eval/*model_5000_seed*.json`。
- [x] `model_5000.pt` 是当前 fixed-forward 指标最好的中途点：三 seed forward fast `done_fraction=0.0`，mean forward displacement 约 `9.315m`，mean abs lateral displacement 约 `0.290m`，max abs lateral displacement across seeds 约 `4.417m`。
- [ ] `model_5000.pt` 仍不合格：yaw/lateral command `done_fraction` 仍可到 `1.0`，seed `103` lateral-right max abs lateral displacement 约 `6.968m`，不能作为 mature controller evidence。
- [x] 2026-06-30 06:19 UTC: `model_6000.pt` 三 seed eval 完成，唯一 JSON 写入 ignored `runs/unitree_g1_23dof_eval/*model_6000_seed*.json`。
- [ ] `model_6000.pt` 明显弱于 `model_5000.pt`：forward fast mean abs lateral displacement 约 `1.068m`，max abs lateral displacement across seeds 约 `5.352m`，selection penalty mean 约 `6.026`，不能作为 mature controller evidence。
- [x] 2026-06-30 06:22 UTC: `model_6500.pt` 三 seed eval 完成，唯一 JSON 写入 ignored `runs/unitree_g1_23dof_eval/*model_6500_seed*.json`。
- [ ] `model_6500.pt` 有恢复但仍弱于 `model_5000.pt`：forward fast mean abs lateral displacement 约 `0.521m`，max abs lateral displacement across seeds 约 `4.915m`，lateral/yaw commands 仍不稳，不能作为 mature controller evidence。
- [x] 2026-06-30 07:21 UTC: `model_7000.pt` 三 seed eval 完成，唯一 JSON 写入 ignored `runs/unitree_g1_23dof_eval/*model_7000_seed*.json`。
- [ ] `model_7000.pt` 仍弱于 `model_5000.pt`：forward fast mean abs lateral displacement 约 `0.703m`，max abs lateral displacement across seeds 约 `4.823m`，不能作为 mature controller evidence。
- [x] 2026-06-30 07:24 UTC: `model_8000.pt` 三 seed eval 完成，唯一 JSON 写入 ignored `runs/unitree_g1_23dof_eval/*model_8000_seed*.json`。
- [ ] `model_8000.pt` 仍弱于 `model_5000.pt`：forward fast mean abs lateral displacement 约 `0.584m`，max abs lateral displacement across seeds 约 `4.988m`，不能作为 mature controller evidence。
- [x] 2026-06-30 07:30 UTC: `model_8500.pt` 三 seed eval 完成，唯一 JSON 写入 ignored `runs/unitree_g1_23dof_eval/*model_8500_seed*.json`。
- [ ] `model_8500.pt` 是后期较接近 `model_5000.pt` 的 checkpoint：forward fast mean abs lateral displacement 约 `0.361m`，max abs lateral displacement across seeds 约 `4.505m`，但 selection penalty mean 约 `4.921`，仍不能作为 mature controller evidence。
- [x] 2026-06-30 07:26 UTC: `model_9000.pt` 三 seed eval 完成，唯一 JSON 写入 ignored `runs/unitree_g1_23dof_eval/*model_9000_seed*.json`。
- [ ] `model_9000.pt` 仍弱于 `model_5000.pt`：forward fast mean abs lateral displacement 约 `0.597m`，max abs lateral displacement across seeds 约 `4.566m`，不能作为 mature controller evidence。
- [x] 2026-06-30 07:33 UTC: `model_9500.pt` 三 seed eval 完成，唯一 JSON 写入 ignored `runs/unitree_g1_23dof_eval/*model_9500_seed*.json`。
- [ ] `model_9500.pt` 接近但仍略弱于 `model_5000.pt`：forward fast max abs lateral displacement across seeds 约 `4.094m`，但 mean abs lateral displacement 约 `0.377m`、selection penalty mean 约 `4.421`；lateral/yaw commands 仍不稳，不能作为 mature controller evidence。
- [x] 2026-06-30 07:44 UTC: `model_10000.pt` 三 seed final eval 完成，唯一 JSON 写入 ignored `runs/unitree_g1_23dof_eval/*model_10000_seed*.json`。
- [x] `model_10000.pt` 弱于 `model_5000.pt`：forward fast mean abs lateral displacement 约 `0.493m`，max abs lateral displacement across seeds 约 `4.647m`，selection penalty mean 约 `4.990`，不能作为 mature controller evidence。
- [x] Stage A training 完成：seeds `101/102/103` 均到 `Learning iteration 10000/10001`，并输出 `model_10000.pt` 和 `policy.onnx`，原始产物保留在 ignored submodule logs。
- [x] Stage A ONNX shape contract 通过：seeds `101/102/103` 的最终 `policy.onnx` 均为 `obs [1,80] -> actions [1,23]`。

## Acceptance Checks

- [x] 每个 run 完成到 `Learning iteration 10000/10001`。
- [x] 每个 run 输出 `model_*.pt` 和 `policy.onnx`，并保持在 ignored submodule logs。
- [x] 对 Stage A selection checkpoints 跑 `scripts/eval_unitree_g1_23dof_command_grid.py`；`model_250.pt` 到 `model_10000.pt` 的关键 checkpoint 已覆盖。
- [x] 选择 best checkpoint 时优先看 fixed-forward lateral drift、yaw error、velocity error、done fraction，不默认最后一轮；当前 best 仍是 `model_5000.pt`，不是 `model_10000.pt`。
- [x] 本轮 Stage A 未观察到 OOM 或早停；若未来任一 run OOM 或早停，记录为 failed，不计入 mature controller evidence。
- [x] Stage A 只证明固定直行候选，不替代 Stage B 通用 velocity controller。

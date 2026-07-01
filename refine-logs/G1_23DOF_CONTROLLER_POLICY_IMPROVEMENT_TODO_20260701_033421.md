# G1 23DoF Controller Policy Improvement TODO

**日期**: 2026-06-30
**状态**: active Gate C blocker; controller training/eval improvements started; mature controller evidence pending

## 边界

- [x] 这份清单只覆盖 `company_g1_edu_23dof` locomotion policy controller 的训练、筛选、回放和 controller smoke。
- [x] 29DoF 官方 policy 只作为成熟 artifact / deploy contract / training discipline 的参考，不作为 23DoF target evidence。
- [x] 23DoF locomotion policy controller 是当前 Gate C 的底层 controller 前置项；它通过 play/eval/smoke 后必须冻结，再进入高层 recovery supervisor 学习。
- [ ] 在 mature controller evidence 产生前，不启动 R020 controller-native baseline、failure pilots、supervisory PPO 或论文主结论。

## 从 29DoF 官方 policy 学到的改进点

- [x] 保持 velocity-conditioned controller，而不是把 controller 改成只能直行的 policy。
- [x] 训练和部署必须成对记录：task id、ONNX shape、deploy obs/action、joint map、action scale、PD gains、checkpoint hash。
- [x] 不默认选择最后 checkpoint；按 command-grid eval 选择 best checkpoint。
- [x] 固定直行是验收项，不应替代通用 velocity controller。
- [x] 新增真正的 command-bin / mixture sampler，使 straight-forward、stand、yaw-only、lateral、combined commands 都有明确采样占比。
- [ ] 23DoF 少 `waist_roll/waist_pitch` 和 wrist pitch/yaw，reward/pose/action smoothness 需要按 23DoF 重新调，不照搬 29DoF。

## 已开始的代码改动

- [x] 新增 repo-local MJLab task 注册模块：`src/humanoid_locomotion_runtime/unitree_g1_23dof_profiles.py`。
- [x] 新增 `Unitree-G1-23Dof-ForwardFlat`：固定直行/站立为主，用于 Stage A 稳定直行训练。
- [x] 新增 `Unitree-G1-23Dof-VelocityBalancedFlat`：保留前进、侧移、转向、停止，但采用更温和 curriculum 和 direct yaw command。
- [x] 新增 repo-local binned velocity command sampler：Stage A 显式采样 `stand` / `straight_slow` / `straight_mid` / `straight_fast`，Stage B 显式采样 `stand` / `straight_forward` / `yaw_only` / `lateral_only` / `combined`。
- [x] binned sampler 已通过 `robot` env 32 env smoke：CommandManager 使用 `BinnedVelocityCommand`，手动 resample 后出现 forward 与 lateral/yaw commands，actor obs/action contract 仍为 `80 -> 23`。
- [x] 新增 repo-local `command_axis_leakage_penalty` reward term：命令轴为 0 时惩罚实际速度串到该轴上，用于 fixed-straight / yaw-only / lateral-only 的侧向串扰约束。
- [x] `command_axis_leakage` 已通过 `robot` env 2 env / 2 step command-grid smoke：RewardManager 显示该 reward term，actor obs 仍 `(80,)`，action 仍 `23`，JSON 写入 ignored `runs/unitree_g1_23dof_eval/`。
- [x] `scripts/run_unitree_g1_23dof_training.sh` 默认切到 `Unitree-G1-23Dof-VelocityBalancedFlat`，`save_interval=250`，便于 checkpoint selection。
- [x] 新增 `scripts/eval_unitree_g1_23dof_command_grid.py`，对 stand/forward/yaw/lateral command grid 输出 JSON 摘要。
- [x] 用 scoped tests 和一次小规模 command-grid smoke 验证新 task 能被注册、checkpoint 能加载、eval JSON 能写入 ignored `runs/`。

## 训练与 eval 队列

- [x] Stage A / ForwardFlat multi-seed 已启动：seeds `101/102/103`，GPU `1/2/3`，handoff 见 `refine-logs/G1_23DOF_CONTROLLER_STAGE_A_HANDOFF_20260630.md`。
- [x] Stage A `model_250.pt` 中途 command-grid sanity 已完成：seeds `101/102/103` 使用 GPU `4/5/6` eval，JSON 写入 ignored `runs/unitree_g1_23dof_eval/`；该 checkpoint stand 稳定但 forward lateral drift 很大，yaw/lateral commands 不稳定，不是 mature controller evidence。
- [x] 并发 eval output filename collision 已修复：eval JSON 文件名现在包含 task、run directory、checkpoint stem、seed 和 timestamp。
- [x] Stage A `model_500.pt` 中途 command-grid sanity 已完成：趋势优于 `model_250.pt`，forward commands 不 done，但 forward fast max lateral drift 仍约 `6.724m-8.004m`，不能作为 mature controller evidence。
- [x] Stage A `model_1000.pt` 中途 command-grid sanity 已完成：forward fast max lateral drift 降到约 `4.890m-5.745m`，但 fixed-straight drift 仍偏大，lateral commands 仍不稳，不能作为 mature controller evidence。
- [x] Stage A `model_1250.pt` / `model_1500.pt` 中途 command-grid sanity 已完成：forward fast 不摔且前进约 `9m`，但 cross-seed straight drift 仍不够小，lateral commands 仍不稳，不能作为 mature controller evidence。
- [x] 新增 `scripts/summarize_unitree_g1_23dof_eval.py`，用于汇总 eval JSON 和按 simple selection penalty 排序；该 penalty 只是 triage，不替代 gate decision。
- [x] Stage A `model_2000.pt` 中途 command-grid sanity 已完成：这是当前最佳中途点，seed `103` straight lateral drift 很小，但 seed `101/102` forward fast max lateral 仍约 `5.241m/5.570m`，不能作为 mature controller evidence。
- [x] Stage A `model_2500.pt` 中途 command-grid sanity 已完成：当前按 multi-seed 聚合是最佳中途点，forward fast max abs lateral across seeds 约 `5.037m`，但 lateral commands 仍不稳，不能作为 mature controller evidence。
- [x] `scripts/summarize_unitree_g1_23dof_eval.py` 增加 `--group-by checkpoint`，支持 multi-seed 聚合排序。
- [x] Stage A `model_3000.pt` 中途 command-grid sanity 已完成：forward fast `done_fraction=0.0`、mean forward displacement 约 `9.287m`，但 max abs lateral across seeds 约 `5.148m`、mean abs lateral 约 `0.927m`，聚合略弱于 `model_2500.pt`，不能作为 mature controller evidence。
- [x] Stage A `model_3500.pt` 中途 command-grid sanity 已完成：forward fast `done_fraction=0.0`、mean forward displacement 约 `9.407m`、mean abs lateral 约 `0.703m`，但 max abs lateral across seeds 约 `5.372m`，seed `103` lateral-right max lateral 约 `13.128m`，不能作为 mature controller evidence。
- [x] Stage A `model_4000.pt` 中途 command-grid sanity 已完成：当前 fixed-forward 指标最好，forward fast `done_fraction=0.0`、mean forward displacement 约 `9.286m`、mean abs lateral 约 `0.457m`、max abs lateral across seeds 约 `4.641m`，但 lateral/yaw commands 仍不稳，不能作为 mature controller evidence。
- [x] Stage A `model_4500.pt` 中途 command-grid sanity 已完成：forward fast `done_fraction=0.0`、mean forward displacement 约 `9.241m`、mean abs lateral 约 `0.517m`、max abs lateral across seeds 约 `4.688m`；略弱于 `model_4000.pt`，且 lateral/yaw commands 仍不稳，不能作为 mature controller evidence。
- [x] Stage A `model_5000.pt` 中途 command-grid sanity 已完成：这是当前 fixed-forward 最佳点，forward fast `done_fraction=0.0`、mean forward displacement 约 `9.315m`、mean abs lateral 约 `0.290m`、max abs lateral across seeds 约 `4.417m`；但 lateral/yaw commands 仍不稳，不能作为 mature controller evidence。
- [x] Stage A `model_6000.pt` 中途 command-grid sanity 已完成：fixed-forward 明显退化，forward fast mean abs lateral 约 `1.068m`、max abs lateral across seeds 约 `5.352m`，不能作为 mature controller evidence。
- [x] Stage A `model_6500.pt` 中途 command-grid sanity 已完成：比 `model_6000.pt` 恢复但仍弱于 `model_5000.pt`，forward fast mean abs lateral 约 `0.521m`、max abs lateral across seeds 约 `4.915m`，不能作为 mature controller evidence。
- [x] Stage A `model_7000.pt` 中途 command-grid sanity 已完成：forward fast mean abs lateral 约 `0.703m`、max abs lateral across seeds 约 `4.823m`，仍弱于 `model_5000.pt`，不能作为 mature controller evidence。
- [x] Stage A `model_8000.pt` 中途 command-grid sanity 已完成：forward fast mean abs lateral 约 `0.584m`、max abs lateral across seeds 约 `4.988m`，仍弱于 `model_5000.pt`，不能作为 mature controller evidence。
- [x] Stage A `model_8500.pt` 中途 command-grid sanity 已完成：后期 checkpoint 中较接近 `model_5000.pt`，forward fast mean abs lateral 约 `0.361m`、max abs lateral across seeds 约 `4.505m`，但 selection penalty 仍弱于 `model_5000.pt`，不能作为 mature controller evidence。
- [x] Stage A `model_9000.pt` 中途 command-grid sanity 已完成：forward fast mean abs lateral 约 `0.597m`、max abs lateral across seeds 约 `4.566m`，仍弱于 `model_5000.pt`，不能作为 mature controller evidence。
- [x] Stage A `model_9500.pt` 中途 command-grid sanity 已完成：forward fast max abs lateral across seeds 降到约 `4.094m`，但 mean abs lateral 约 `0.377m`、selection penalty mean 约 `4.421`，仍略弱于 `model_5000.pt`，且 lateral/yaw commands 仍不稳，不能作为 mature controller evidence。
- [x] Stage A `model_10000.pt` final command-grid eval 已完成：forward fast mean abs lateral 约 `0.493m`、max abs lateral across seeds 约 `4.647m`、selection penalty mean 约 `4.990`，弱于 `model_5000.pt`，不能作为 mature controller evidence。
- [x] Stage A / ForwardFlat multi-seed training 已完成：seeds `101/102/103` 均到 `Learning iteration 10000/10001`，并输出 `model_10000.pt` 和 `policy.onnx` 到 ignored submodule logs。
- [x] Stage A / ForwardFlat seeds `101/102/103` 的最终 `policy.onnx` 已验证为 `obs [1,80] -> actions [1,23]`，deploy shape contract 未漂移。
- [ ] Stage A / ForwardFlat 通过 command-grid mature gate：目标是固定 `lin_vel_y=0`、`ang_vel_z=0` 下稳定直行，同时 lateral/yaw commands 不明显失稳。
- [x] Stage B / VelocityBalancedFlat multi-seed 已启动并按资源利用调整：旧 GPU `1/2/3` early runs 在 iteration `783/10001` 停止，当前 authoritative runs 为 GPU `5` 单卡三任务 `g1vb_pack_s201/s202/s203_20260630T085517Z`，handoff 见 `refine-logs/G1_23DOF_CONTROLLER_STAGE_B_HANDOFF_20260630.md`。
- [x] Stage B post-training eval queue 已启动并重建：原 watcher `g1vb_pack_eval_after_train_20260630T085653Z` 负责等待 packed runs；最终验收使用 2026-07-01 补跑 queue `stage_b_eval_queue_20260701T012312Z` 完成。
- [x] Stage B / VelocityBalancedFlat multi-seed 完成：seeds `201/202/203` 均到 `Learning iteration 10000/10001`，最终 mean reward 约 `49.33/49.65/50.50`，`fell_over=0.0000`，最终 `policy.onnx` shape 为 `obs [1,80] -> actions [1,23]`；证据：`refine-logs/G1_23DOF_CONTROLLER_STAGE_B_ACCEPTANCE_20260701.md`。
- [x] 对 Stage B packed runs 的 13 个 checkpoints x 3 seeds 做 command-grid eval，记录 lateral drift、yaw error、velocity error、fall/done fraction；补跑 queue：`runs/unitree_g1_23dof_eval_queue/stage_b_eval_queue_20260701T012312Z.log`，产物为 ignored `runs/unitree_g1_23dof_eval/*VelocityBalancedFlat*packedgpu5*seed*.json`。
- [x] 比较 `model_10000.pt` 与新训练更后期 checkpoint；截至 Stage B eval 结束，当前 selected candidate 是 seed `202` run 的 `model_9000.pt`，最终轮 `model_10000.pt` 不默认导出为 best。
- [x] Viser play sanity：用户 2026-07-01 观察 `model_9000.pt` 效果还不错，走直线部分符合当前目测要求；该条不替代 project-local controller smoke。
- [ ] 通过 eval 的 candidate 才复制到 ignored `checkpoints/` 并生成 hash/shape summary。
- [ ] project-local controller smoke 至少覆盖 `stand_ready`、`safe_stop`、`track_velocity`。

## GPU 并发规则

- [x] 当前 controller 训练阶段最多同时使用 3 张空闲 GPU。
- [x] 单张 GPU 在确认不会 OOM 时最多同时跑 3 个训练任务；默认先按 1 个 4096-env 任务/GPU 保守启动。
- [x] 训练/eval 必须写入 ignored `runs/` 或 submodule ignored `logs/`，不得提交 raw logs、checkpoints、ONNX、tfevents。
- [x] Stage B 启动和 packed 重启前已检查 `nvidia-smi` 并记录实际使用 GPU、run name、seed、task、num envs：见 `refine-logs/G1_23DOF_CONTROLLER_STAGE_B_HANDOFF_20260630.md`。
- [ ] 若发生 OOM，停止在当前 stage，降低 `NUM_ENVS` 或每 GPU 并发数，不把失败 run 计为 evidence。

## Gate C 进入条件

- [x] 至少一个 23DoF policy candidate 通过 command-grid eval 和 Viser 直线目测 sanity：Stage B seed `202` run 的 `model_9000.pt`。
- [x] ONNX/export contract 仍为 `obs [1,80] -> actions [1,23]`。
- [ ] candidate deploy config 与 23DoF `joint_ids_map`、action scale、PD gains 一致。
- [ ] project-local controller smoke 通过并记录为 `company_g1_edu_23dof` evidence。
- [x] `refine-logs/EXPERIMENT_TRACKER.md`、`EXPERIMENT_PLAN.md`、`DAILY_EXPERIMENT_TIMELINE.md`、`MANIFEST.md` 同步 Stage B candidate decision；Gate C mature decision 仍等待 R007j。

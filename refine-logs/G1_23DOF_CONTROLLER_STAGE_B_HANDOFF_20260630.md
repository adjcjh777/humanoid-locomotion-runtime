# G1 23DoF Controller Stage B Handoff

**日期**: 2026-06-30
**状态**: Stage B VelocityBalancedFlat multi-seed running; mature controller evidence pending

## 目的

- [x] 启动 `company_g1_edu_23dof` locomotion policy controller 的 Stage B 通用 velocity controller 训练。
- [x] 使用 repo-local `Unitree-G1-23Dof-VelocityBalancedFlat` task，不修改 Unitree submodule tracked source。
- [x] 保持 29DoF 官方 policy 为 reference-only，不把本轮结果直接写成 mature controller evidence。
- [x] 训练目标是保留 stand、straight-forward、yaw-only、lateral-only、combined commands，同时不牺牲固定直行验收。

## Running Jobs

| Seed | GPU | tmux session | Run name | Task | 状态 |
|---:|---:|---|---|---|---|
| 201 | 5 | `g1vb_pack_s201_20260630T085517Z` | `a800_g1_23dof_velocitybalanced_packedgpu5_seed201_4096env_10001iter_20260630T085517Z` | `Unitree-G1-23Dof-VelocityBalancedFlat` | running |
| 202 | 5 | `g1vb_pack_s202_20260630T085517Z` | `a800_g1_23dof_velocitybalanced_packedgpu5_seed202_4096env_10001iter_20260630T085517Z` | `Unitree-G1-23Dof-VelocityBalancedFlat` | running |
| 203 | 5 | `g1vb_pack_s203_20260630T085517Z` | `a800_g1_23dof_velocitybalanced_packedgpu5_seed203_4096env_10001iter_20260630T085517Z` | `Unitree-G1-23Dof-VelocityBalancedFlat` | running |

## Superseded Early Jobs

| Seed | GPU | tmux session | Run name | Last observed | 状态 |
|---:|---:|---|---|---|---|
| 201 | 1 | `g1vb_s201_20260630T083359Z` | `a800_g1_23dof_velocitybalanced_seed201_4096env_10001iter_20260630T083359Z` | iteration `783/10001`, reward `41.58`, fell_over `0.0000` | stopped: superseded by packed GPU 5 run |
| 202 | 2 | `g1vb_s202_20260630T083359Z` | `a800_g1_23dof_velocitybalanced_seed202_4096env_10001iter_20260630T083359Z` | iteration `783/10001`, reward `43.72`, fell_over `0.0000` | stopped: superseded by packed GPU 5 run |
| 203 | 3 | `g1vb_s203_20260630T083359Z` | `a800_g1_23dof_velocitybalanced_seed203_4096env_10001iter_20260630T083359Z` | iteration `783/10001`, reward `42.73`, fell_over `0.0000` | stopped: superseded by packed GPU 5 run |

## Launch Settings

- [x] `NUM_ENVS=4096`
- [x] `MAX_ITERATIONS=10001`
- [x] `SAVE_INTERVAL=250`
- [x] `mamba env=robot`
- [x] `MUJOCO_GL=egl`
- [x] 并发策略：2026-06-30 08:55 UTC 已按用户资源利用建议切换为单张 GPU `5` 上同时跑 3 个 4096-env 训练任务；GPU 1/2/3 已释放。
- [x] launch run list 写入 ignored `runs/unitree_g1_23dof_training/STAGE_B_VELOCITY_BALANCED_RUNS_20260630T083359Z.txt`。
- [x] packed launch run list 写入 ignored `runs/unitree_g1_23dof_training/STAGE_B_VELOCITY_BALANCED_PACKED_GPU5_RUNS_20260630T085517Z.txt`。

## Preflight

- [x] 2026-06-30 08:33 UTC: 启动前 GPU snapshot 显示 GPU `1/2/3/5/6` 空闲，GPU `0/4/7` 有其他占用；本轮使用 GPU `1/2/3`。
- [x] 2026-06-30 08:33 UTC: scoped validation 已通过：`uv run ruff check ...`、`uv run pytest tests/test_unitree_g1_23dof_training_framework.py`、`python -m py_compile ...`、`bash -n scripts/run_unitree_g1_23dof_training.sh scripts/setup_unitree_g1_23dof_training.sh`。
- [x] 训练脚本收尾产物查找已改为 profile-agnostic `logs/rsl_rl/*/*RUN_NAME`，覆盖 `g1_23dof_forward_flat` 和 `g1_23dof_velocity_balanced`。
- [x] 2026-06-30 08:55 UTC: 因每个 4096-env job 显存占用约 `2.7-3.6 GiB`，停止三卡 early jobs 和旧 eval watcher，改用 GPU `5` 单卡三任务；停止时仍属于 early training，不计入 mature evidence。

## Initial Health Check

- [x] 2026-06-30 08:34 UTC: 三个 tmux sessions 均存在，三份 console log 已创建。
- [x] 2026-06-30 08:34 UTC: 三个 runs 已进入 learning iteration `6/10001`，GPU `1/2/3` memory/util 约 `3287 MiB / 68%`、`3571 MiB / 68%`、`2729 MiB / 69%`。
- [x] 2026-06-30 08:34 UTC: `CommandManager` 使用 `BinnedVelocityCommand`，ActionManager shape 仍为 `23`。
- [x] 2026-06-30 08:34 UTC: early warm-up metrics：steps/s 约 `71k-73k`，mean reward 约 `-10.6` 到 `-10.9`，fell_over 仍高；这属于随机策略 warm-up 阶段，当前 decision 为 `CONTINUE`。
- [x] 2026-06-30 08:38 UTC: 三个 runs 仍在运行；seed `201` 到 iteration `129/10001`，seed `202/203` 到 iteration `135/10001`。
- [x] 2026-06-30 08:38 UTC: seed `202/203` early metrics 已改善到 mean reward 约 `-2.31/-1.30`、fell_over 约 `3.83/2.88`；seed `201` mean reward 约 `-3.02`、fell_over 约 `17.58`。仍属于 early training，不作为 mature evidence。
- [x] 2026-06-30 08:40 UTC: 三个 runs 到 iteration `249/10001`，无 OOM/NaN；mean reward 约 `4.22-5.38`，mean episode length 约 `935-939`，fell_over 约 `0.46-0.75`，training-check decision 为 `CONTINUE`。
- [x] 2026-06-30 08:47 UTC: 三个 runs 到 iteration `549/10001`，无 OOM/NaN；mean reward 约 `33.49-38.25`，mean episode length 约 `996-1000`，fell_over 约 `0.00-0.04`，`model_500.pt` 已写出，training-check decision 为 `CONTINUE`。
- [x] 2026-06-30 08:51 UTC: 三个 runs 到 iteration `696/10001`，无 OOM/NaN/Inf；mean reward 约 `39.21-42.10`，mean episode length 约 `994-1000`，fell_over 约 `0.00-0.04`，暂无新 checkpoint，training-check decision 为 `CONTINUE`。
- [x] 2026-06-30 08:55 UTC: 旧三卡 runs 停止前到 iteration `783/10001`，无 OOM，mean reward 约 `41.58-43.72`，fell_over `0.0000`；被 packed GPU 5 runs 取代。
- [x] 2026-06-30 08:56 UTC: packed GPU 5 runs 已进入 learning iteration `3/10001`，GPU 5 memory/util 约 `7550 MiB / 100%`，无 OOM；early warm-up metrics reward 约 `-11.07` 到 `-10.40`，fell_over 约 `35.08-37.71`，当前 decision 为 `CONTINUE`。
- [x] 2026-06-30 09:00 UTC: packed GPU 5 runs 到 iteration `54/10001`，GPU 5 memory/util 约 `7550 MiB / 100%`，GPU `1/2/3` 已释放；无 OOM，当前 decision 为 `CONTINUE`。

## Post-Training Eval Queue

- [x] 2026-06-30 08:43 UTC: 启动 `g1vb_eval_after_train_20260630T084308Z` tmux watcher；08:55 UTC 随旧三卡 run 一起停止，状态为 superseded。
- [x] watcher 入口：`scripts/run_unitree_g1_23dof_stage_b_eval_queue.sh`。
- [x] 2026-06-30 08:56 UTC: 启动 packed watcher `g1vb_pack_eval_after_train_20260630T085653Z`，等待 packed GPU 5 runs 的 `model_10000.pt` 和训练 tmux 结束后，再用 GPU list `5 5 5` 分批跑 command-grid eval。
- [x] watcher 记录：ignored `runs/unitree_g1_23dof_eval_queue/stage_b_eval_queue_20260630T085653Z.log`；08:56 UTC 确认仍在等待 `model_10000.pt`，没有提前 eval。
- [ ] watcher 完成 Stage B checkpoints `model_250.pt` 到 `model_10000.pt` 的三 seed command-grid eval，并写入 ignored `runs/unitree_g1_23dof_eval/`。

## Acceptance Checks

- [ ] 每个 run 完成到 `Learning iteration 10000/10001`。
- [ ] 每个 run 输出 `model_*.pt` 和 `policy.onnx`，并保持在 ignored submodule logs。
- [ ] 关键 checkpoints 跑 `scripts/eval_unitree_g1_23dof_command_grid.py`。
- [ ] 选择 best checkpoint 时同时看 fixed-forward lateral drift、yaw error、velocity error、done fraction 和 yaw/lateral command stability。
- [ ] 若任一 run OOM 或早停，记录为 failed，不计入 mature controller evidence。
- [x] Stage B 只产生通用 velocity controller candidate，不直接作为 mature controller evidence。
- [ ] 通过 command-grid eval 和 controller smoke 前不推进 Gate C。

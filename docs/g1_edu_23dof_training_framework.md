# G1 edu 23DoF Controller Training Framework

**日期**: 2026-06-29
**状态**: repo-local training/play entrypoints scaffolded; Stage B `model_9000.pt` candidate selected; controller smoke evidence still pending

这份文档只说明怎么在当前仓库里训练 `company_g1_edu_23dof` 的 locomotion controller。它不表示 controller 已经成熟，也不表示 Gate C controller smoke 已通过。

## 目录约定

- [x] 官方训练仓库作为当前仓库子模块放在 `third_party/unitree_rl_mjlab`。
- [x] Python 环境固定复用 mamba/conda env `robot`；可用 `UNITREE_RL_MJLAB_CONDA_ENV=<env>` 覆盖。
- [x] 环境搭建脚本只检查已有 mamba env 和任务注册，不直接新建虚拟环境。
- [x] 训练日志、checkpoint 和导出的 ONNX 保留在 `third_party/unitree_rl_mjlab/logs/`，由子模块自己的 `.gitignore` 排除。
- [x] 本项目额外的训练 console log 放在 `runs/unitree_g1_23dof_training/`，不提交 git。

## 当前锁定任务

| 项 | 值 |
|----|----|
| Training repo | `third_party/unitree_rl_mjlab` |
| Upstream | `https://github.com/unitreerobotics/unitree_rl_mjlab.git` |
| Commit | `1425b15f73bd4095f0df53709d7c389c3eb9e790` |
| Upstream baseline task | `Unitree-G1-23Dof-Flat` |
| Repo-local default task | `Unitree-G1-23Dof-VelocityBalancedFlat` |
| Straight-eval training task | `Unitree-G1-23Dof-ForwardFlat` |
| Default experiment name | `g1_23dof_velocity_balanced` |
| Default mamba env | `robot` |
| Deploy config | `deploy/robots/g1_23dof/config/policy/velocity/v0/params/deploy.yaml` |
| Expected deploy obs/action | `80 -> 23` |
| Project controller route | `train_23dof_required` |

## 使用方法

先建环境：

```bash
bash scripts/setup_unitree_g1_23dof_training.sh
```

正式训练入口默认使用 repo-local `Unitree-G1-23Dof-VelocityBalancedFlat`、`4096 envs / 10001 iterations / save_interval=250`：

```bash
GPU_ID=4 SEED=42 bash scripts/run_unitree_g1_23dof_training.sh
```

如果要跑固定直行 Stage A，显式覆盖 task：

```bash
TASK=Unitree-G1-23Dof-ForwardFlat GPU_ID=4 SEED=101 bash scripts/run_unitree_g1_23dof_training.sh
```

如果只想做一次显式短 sanity run，必须手动覆盖参数，避免误把短跑当成正式训练：

```bash
GPU_ID=4 NUM_ENVS=64 MAX_ITERATIONS=1 SAVE_INTERVAL=1 RUN_NAME=a800_g1_23dof_sanity_$(date -u +%Y%m%dT%H%M%SZ) bash scripts/run_unitree_g1_23dof_training.sh
```

短回放入口使用 repo-local wrapper 注册 `VelocityBalancedFlat` profile 后调用上游 `scripts/play.py`：

```bash
RUN_NAME=a800_g1_23dof_velocitybalanced_packedgpu5_seed202_4096env_10001iter_20260630T085517Z \
CHECKPOINT=model_9000.pt \
GPU_ID=5 \
bash scripts/run_unitree_g1_23dof_play.sh
```

## 验收边界

- [x] `scripts/setup_unitree_g1_23dof_training.sh` 能复用 mamba env `robot` 并列出 `Unitree-G1-23Dof-Flat`。
- [x] `scripts/run_unitree_g1_23dof_training.sh` 是当前仓库内的正式 RSL-RL 训练入口，默认 `Unitree-G1-23Dof-VelocityBalancedFlat`、`4096 envs / 10001 iterations / save_interval=250 / seed=42`，并产生 `model_*.pt` / `policy.onnx`。
- [x] repo-local task 注册由 `src/humanoid_locomotion_runtime/unitree_g1_23dof_profiles.py` 完成，不直接修改 Unitree submodule tracked source。
- [x] `scripts/eval_unitree_g1_23dof_command_grid.py` 提供 stand/forward/yaw/lateral command-grid eval 摘要，用于 checkpoint selection。
- [x] command-grid eval 输出文件名包含 task、run directory、checkpoint stem、seed 和 timestamp，支持 3 张 GPU 并发 eval 而不互相覆盖 JSON。
- [x] `scripts/summarize_unitree_g1_23dof_eval.py` 汇总 command-grid eval JSON，按 simple penalty 辅助筛选 checkpoint；支持 `--group-by checkpoint` 做 multi-seed 聚合排序。该排序只是 triage，不替代 Gate C acceptance。
- [x] 用 `onnx` 检查导出的 `policy.onnx` input/output shape：`obs [1, 80] -> actions [1, 23]`。
- [x] 用 `scripts/run_unitree_g1_23dof_play.sh` 对 Stage B seed `202` run 的 `model_9000.pt` 做 Viser 短回放；用户 2026-07-01 观察效果还不错，走直线部分符合当前目测要求。
- [ ] 把通过 shape/play 的 candidate 拷贝到本项目 ignored `checkpoints/` 下，再跑 project-local controller smoke。
- [ ] 只有 project-local 23DoF smoke 通过后，才能把它写成 `company_g1_edu_23dof` controller evidence。

## 2026-06-30 Policy Improvement Plan

- [x] 待办清单：fixed latest `refine-logs/G1_23DOF_CONTROLLER_POLICY_IMPROVEMENT_TODO.md`，最新快照 `refine-logs/G1_23DOF_CONTROLLER_POLICY_IMPROVEMENT_TODO_20260701_034510.md`。
- [x] 保留通用 velocity controller 方向，不把 controller 简化成只能直行的 policy。
- [x] 新增 `ForwardFlat` 和 `VelocityBalancedFlat` 两个 repo-local tasks；前者服务固定直行稳定性，后者服务通用 velocity controller。
- [x] 新增 binned velocity command sampler：Stage A 明确覆盖 `stand` / straight-forward 速度段，Stage B 明确覆盖 `stand` / `straight_forward` / `yaw_only` / `lateral_only` / `combined`，避免纯 uniform command 让关键验收 command 分布太稀。
- [x] binned sampler 真实 env smoke 通过：`robot` env / GPU 4 / 32 env 下 CommandManager 使用 `BinnedVelocityCommand`，手动 resample 后出现 forward 与 lateral/yaw commands，actor obs/action contract 仍为 `80 -> 23`。
- [x] 新增 repo-local `command_axis_leakage_penalty` reward term；后续新 run 会在命令轴为 0 时惩罚实际速度串到该轴上，用于治理 fixed-straight lateral/yaw drift 和 yaw/lateral-only 串扰。
- [x] 2 env / 2 step command-grid smoke 确认新 reward 进入 MJLab RewardManager，actor obs/action contract 仍为 `80 -> 23`，smoke JSON 留在 ignored `runs/unitree_g1_23dof_eval/`。
- [x] 训练入口默认切到 `VelocityBalancedFlat`，并提高 checkpoint 保存频率以支持按 eval 选 best checkpoint。
- [x] Stage A `model_250.pt` / `model_500.pt` / `model_1000.pt` / `model_1250.pt` / `model_1500.pt` / `model_2000.pt` / `model_2500.pt` / `model_3000.pt` / `model_3500.pt` / `model_4000.pt` / `model_4500.pt` / `model_5000.pt` / `model_6000.pt` / `model_6500.pt` / `model_7000.pt` / `model_8000.pt` / `model_8500.pt` / `model_9000.pt` / `model_9500.pt` / `model_10000.pt` 已做 command-grid eval；这些都不是 mature controller evidence，`model_5000.pt` 当前 fixed-forward 综合指标最好，`model_9500.pt` 接近但仍略弱，最终轮 `model_10000.pt` 弱于 `model_5000.pt`，lateral/yaw commands 仍未达标。
- [x] Stage A / ForwardFlat seeds `101/102/103` 已完成训练并输出 `model_10000.pt` / `policy.onnx`，原始产物保持在 ignored submodule logs。
- [x] Stage A / ForwardFlat seeds `101/102/103` 的最终 `policy.onnx` 已验证为 `obs [1,80] -> actions [1,23]`。
- [x] 跑至少 3 个 Stage A / ForwardFlat seeds。
- [x] 启动至少 3 个 Stage B / VelocityBalancedFlat seeds：seeds `201/202/203` 打包在 GPU `5` 上运行，tmux sessions `g1vb_pack_s201/s202/s203_20260630T085517Z`，handoff 见 `refine-logs/G1_23DOF_CONTROLLER_STAGE_B_HANDOFF_20260630.md`。
- [x] Stage B post-training eval queue 已补跑完成：`scripts/run_unitree_g1_23dof_stage_b_eval_queue.sh` 产出 39 个 ignored eval JSON，覆盖 13 checkpoints x 3 seeds；补跑 log 为 `runs/unitree_g1_23dof_eval_queue/stage_b_eval_queue_20260701T012312Z.log`。
- [x] 完成至少 3 个 Stage B / VelocityBalancedFlat seeds 到 `Learning iteration 10000/10001`；最终 `policy.onnx` shape 为 `obs [1,80] -> actions [1,23]`。
- [x] 对 Stage A candidate checkpoints 做 command-grid eval，不默认选择最终轮 `model_10000.pt`；截至 Stage A 结束，`model_5000.pt` 是当前 fixed-forward best。
- [x] 对 Stage B candidate checkpoints 做 command-grid eval，并确认当前 selected candidate `model_9000.pt` 的直线部分通过 Viser 目测 sanity；三 seed聚合 forward fast mean abs lateral 约 `0.203m`。
- [x] 重要 run/log/pt/ONNX/JSON 的 GitHub-safe evidence 索引：`refine-logs/G1_23DOF_CONTROLLER_STAGE_B_CURATED_EVIDENCE_20260701.md`；raw artifact 本体仍不提交。
- [ ] 通过 eval 的 candidate 才进入 ignored `checkpoints/` 和 project-local controller smoke。

## 2026-06-29 Smoke 记录

- [x] 环境检查：`robot` env，Python 3.10.0，torch `2.3.0+cu121`，CUDA visible 8，MuJoCo `3.8.0`，MuJoCo-Warp `3.8.1`。
- [x] 训练 loop 短 sanity run：`GPU_ID=4 NUM_ENVS=64 MAX_ITERATIONS=1 SAVE_INTERVAL=1 bash scripts/run_unitree_g1_23dof_training.sh`。
- [x] 成功 run dir：`third_party/unitree_rl_mjlab/logs/rsl_rl/g1_23dof_velocity/2026-06-29_03-19-20_a800_g1_23dof_smoke_wrapper_20260629T031905Z/`。
- [x] 产物：`model_0.pt` 约 4.9 MB，`policy.onnx` 约 819 KB。
- [x] 维度：actor obs `80`，action `23`，critic obs `95`；ONNX input `obs [1,80]`，output `actions [1,23]`。
- [ ] 这只是 1 iteration smoke，不能当成可用 locomotion controller。

## 2026-06-29 Full Training Candidate 记录

- [x] 正式训练 run 完成：`a800_g1_23dof_4096env_10001iter_20260629T100128Z`。
- [x] 训练设置来自实际 log/params：`Unitree-G1-23Dof-Flat`、GPU 4、mamba env `robot`、`4096 envs`、`10001 iterations`、`save_interval=500`、seed `42`。
- [x] 产物保留在 ignored submodule logs：`third_party/unitree_rl_mjlab/logs/rsl_rl/g1_23dof_velocity/2026-06-29_10-01-43_a800_g1_23dof_4096env_10001iter_20260629T100128Z/`。
- [x] 最终产物包含 `model_10000.pt` 和 `policy.onnx`；console log 保留在 ignored `runs/unitree_g1_23dof_training/a800_g1_23dof_4096env_10001iter_20260629T100128Z.log`。
- [x] 末轮训练摘要：`Mean reward: 34.57`、`Mean episode length: 990.10`、`Episode_Termination/fell_over: 0.0833`。
- [x] curated 验收摘要：`refine-logs/G1_23DOF_CONTROLLER_TRAINING_ACCEPTANCE_20260630.md`。
- [ ] 这只是 controller candidate，不是成熟 controller evidence；仍需官方 `play.py` 短回放和 project-local `stand_ready` / `track_velocity` controller smoke。

## 不要混淆

- [x] 这个训练框架是在当前仓库内搭起来的，不依赖 `/mnt/nvme2n1p1/...` 外部训练目录。
- [x] 不使用 `uv venv` 或 repo-local `.venvs`；默认复用已有 mamba env `robot`。
- [x] `robot` 的 torch 2.3 不支持 `torch.onnx.export(dynamo=...)`；当前仓库 wrapper 会在不改官方 submodule、不改 mamba env 的情况下丢弃这个兼容性参数。
- [x] 29DoF reference ONNX 仍然只能算 `mjlab_g1_29dof_reference` evidence。
- [x] 训练出来的 checkpoint、ONNX、raw logs 不进 git。

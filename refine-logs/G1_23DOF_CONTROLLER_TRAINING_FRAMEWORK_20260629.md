# G1 23DoF Controller Training Framework 2026-06-29

## 白话结论

现在开始自己训 23DoF locomotion controller。第一步不是直接开大训练，而是先把当前仓库里的训练框架搭好：官方 Unitree RL MJLab 作为 repo-local submodule，固定复用已有 mamba env，smoke 脚本、日志路径和验收边界都固定下来。

## 已完成

- [x] 官方训练仓库放入当前项目：`third_party/unitree_rl_mjlab`。
- [x] 子模块 commit 锁定：`1425b15f73bd4095f0df53709d7c389c3eb9e790`。
- [x] 确认官方 23DoF 速度任务入口：`Unitree-G1-23Dof-Flat`。
- [x] 确认官方 23DoF deploy 配置入口：`deploy/robots/g1_23dof/config/policy/velocity/v0/params/deploy.yaml`。
- [x] 盘点现有 mamba env：`robot` 和 `reta` 已具备 torch CUDA、MuJoCo、MJLab、MuJoCo-Warp、RSL-RL、Tyro、ONNX；默认复用 `robot`。
- [x] 新增环境搭建脚本：`scripts/setup_unitree_g1_23dof_training.sh`。
- [x] 新增最小训练 smoke 脚本：`scripts/run_unitree_g1_23dof_training_smoke.sh`。
- [x] 新增训练 wrapper：`scripts/unitree_train_mamba_wrapper.py`，兼容 `robot` 环境里 torch 2.3 不支持 `torch.onnx.export(dynamo=...)` 的问题。
- [x] 新增说明文档：`docs/g1_edu_23dof_training_framework.md`。
- [x] 完成 1 iteration smoke：GPU 4、64 env、1 iteration，actor obs `80`、action `23`、critic obs `95`，导出 `policy.onnx`。
- [x] ONNX shape 检查通过（1-iter smoke candidate）：input `obs [1,80]`，output `actions [1,23]`。
- [x] 完成 3000-iter 训练 run：`2026-06-29_03-37-37_a800_g1_23dof_simtest_20260629T033722Z`，`num_envs=512`、`max_iterations=3000`、`seed=42`、GPU 4、A800 `cuda:0`、Warp 1.12.0 / CUDA 12.9 / Driver 13.0。
- [x] 3000-iter 收敛证据：iter 0 `mean_reward=-0.62, ep_len=10.90` → iter 2999 `mean_reward=17.98, ep_len=945.39`，`fell_over=0.0000`、`time_out=1.8333`；`track_linear_velocity=0.4138`、`track_angular_velocity=0.4163`、`pose=0.6624`；throughput `15,369 steps/s`，总耗时 `00:41:40`，total steps `36,864,000`。
- [x] 3000-iter 产物：`model_0/300/600/900/1200/1500/1800/2100/2400/2700/2999.pt` + `policy.onnx`（838,027 bytes）+ tfevents 6.9 MB + `params/{agent,env}.yaml`，存放在 submodule `logs/` 下，由 submodule `.gitignore` 排除。
- [x] 3000-iter smoke log 副本：`runs/unitree_g1_23dof_training/a800_g1_23dof_simtest_20260629T033722Z.log`（129,260 行），由本仓库 `.gitignore` 排除。

## 今天下一步

- [x] 运行 `bash scripts/setup_unitree_g1_23dof_training.sh`，确认 mamba env `robot` 可复用并能列出 `Unitree-G1-23Dof-Flat`。
- [x] 运行 `GPU_ID=4 NUM_ENVS=64 MAX_ITERATIONS=1 bash scripts/run_unitree_g1_23dof_training_smoke.sh`，验证训练 loop 能启动和导出 artifact。
- [x] 跑 3000-iter pilot：`GPU_ID=4 NUM_ENVS=512 MAX_ITERATIONS=3000 SAVE_INTERVAL=300 RUN_NAME=a800_g1_23dof_simtest_20260629T033722Z bash scripts/run_unitree_g1_23dof_training_smoke.sh`。
- [ ] 对 3000-iter `policy.onnx` 做 ONNX shape 检查：期望 `obs [1,80] -> actions [1,23]`。
- [ ] 用官方 `scripts/play.py Unitree-G1-23Dof-Flat --checkpoint_file=model_2999.pt` 做短回放，确认机器人能站稳/跟踪速度。
- [ ] 通过 shape + play 后，把 candidate 拷贝到本项目 ignored `checkpoints/` 下，更新 `configs/environment.lock.toml` 的 `[controller_contracts.company_g1_edu_23dof]`：`selected_controller_source` 指向新 candidate，`mature_controller_evidence` 仍待 project-local smoke 通过后才升 true。
- [ ] 跑 project-local `stand_ready` + short `track_velocity` smoke，通过后才算 `company_g1_edu_23dof` controller evidence。
- [ ] pilot 稳定后再考虑官方规模 `4096 envs / 10001 iterations`，用 `screen` 或 `tmux` 后台跑。

## Gate 边界

- [ ] 训练 smoke 通过不等于 controller smoke 通过。
- [ ] 3000-iter 训练收敛不等于 mature controller evidence；ONNX shape、play 回放和 project-local 23DoF controller smoke 必须全部通过。
- [ ] `policy.onnx` 必须通过 shape 检查、play 回放和 project-local 23DoF controller smoke 后，才算 `company_g1_edu_23dof` controller evidence。
- [ ] 在这之前，R020 controller-native baseline、failure pilots 和 PPO supervisor 都不要启动。
- [ ] 训练 logs、checkpoints、ONNX、tfevents 不进 git；本仓库只记录 path、SHA256 和指标摘要。

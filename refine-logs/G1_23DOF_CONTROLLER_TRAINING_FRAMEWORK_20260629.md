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
- [x] ONNX shape 检查通过：input `obs [1,80]`，output `actions [1,23]`。

## 今天下一步

- [x] 运行 `bash scripts/setup_unitree_g1_23dof_training.sh`，确认 mamba env `robot` 可复用并能列出 `Unitree-G1-23Dof-Flat`。
- [x] 运行 `GPU_ID=4 NUM_ENVS=64 MAX_ITERATIONS=1 bash scripts/run_unitree_g1_23dof_training_smoke.sh`，验证训练 loop 能启动和导出 artifact。
- [ ] 如果 smoke 成功，再开小规模 pilot，例如 `NUM_ENVS=512 MAX_ITERATIONS=50`。
- [ ] pilot 稳定后再考虑官方规模 `4096 envs / 10001 iterations`，用 `screen` 或 `tmux` 后台跑。

## Gate 边界

- [ ] 训练 smoke 通过不等于 controller smoke 通过。
- [ ] `policy.onnx` 必须通过 shape 检查、play 回放和 project-local 23DoF controller smoke 后，才算 `company_g1_edu_23dof` controller evidence。
- [ ] 在这之前，R020 controller-native baseline、failure pilots 和 PPO supervisor 都不要启动。

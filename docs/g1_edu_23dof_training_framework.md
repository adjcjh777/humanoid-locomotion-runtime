# G1 edu 23DoF Controller Training Framework

**日期**: 2026-06-29
**状态**: repo-local framework scaffolded; full controller training not yet run

这份文档只说明怎么在当前仓库里训练 `company_g1_edu_23dof` 的 locomotion controller。它不表示 controller 已经成熟，也不表示 Gate C controller smoke 已通过。

## 目录约定

- [x] 官方训练仓库作为当前仓库子模块放在 `third_party/unitree_rl_mjlab`。
- [x] Python 环境固定复用 mamba/conda env `robot`；可用 `UNITREE_RL_MJLAB_CONDA_ENV=<env>` 覆盖。
- [x] 环境搭建脚本只检查已有 mamba env 和任务注册，不直接新建虚拟环境。
- [x] 训练日志、checkpoint 和导出的 ONNX 保留在 `third_party/unitree_rl_mjlab/logs/`，由子模块自己的 `.gitignore` 排除。
- [x] 本项目额外的 smoke log 放在 `runs/unitree_g1_23dof_training/`，不提交 git。

## 当前锁定任务

| 项 | 值 |
|----|----|
| Training repo | `third_party/unitree_rl_mjlab` |
| Upstream | `https://github.com/unitreerobotics/unitree_rl_mjlab.git` |
| Commit | `1425b15f73bd4095f0df53709d7c389c3eb9e790` |
| Task | `Unitree-G1-23Dof-Flat` |
| Experiment name | `g1_23dof_velocity` |
| Default mamba env | `robot` |
| Deploy config | `deploy/robots/g1_23dof/config/policy/velocity/v0/params/deploy.yaml` |
| Expected deploy obs/action | `80 -> 23` |
| Project controller route | `train_23dof_required` |

## 使用方法

先建环境：

```bash
bash scripts/setup_unitree_g1_23dof_training.sh
```

先跑很小的启动 smoke：

```bash
GPU_ID=4 NUM_ENVS=64 MAX_ITERATIONS=1 bash scripts/run_unitree_g1_23dof_training_smoke.sh
```

后续正式训练才使用官方规模：

```bash
cd third_party/unitree_rl_mjlab
PYTHONPATH=$PWD CUDA_VISIBLE_DEVICES=4 MUJOCO_GL=egl mamba run -n robot python ../../scripts/unitree_train_mamba_wrapper.py Unitree-G1-23Dof-Flat \
  --env.scene.num-envs=4096 \
  --agent.logger=tensorboard \
  --agent.upload-model=False
```

## 验收边界

- [x] `scripts/setup_unitree_g1_23dof_training.sh` 能复用 mamba env `robot` 并列出 `Unitree-G1-23Dof-Flat`。
- [x] `scripts/run_unitree_g1_23dof_training_smoke.sh` 能完成 1 iteration smoke，并产生 `model_*.pt` / `policy.onnx`。
- [x] 用 `onnx` 检查导出的 `policy.onnx` input/output shape：`obs [1, 80] -> actions [1, 23]`。
- [ ] 用官方 `scripts/play.py Unitree-G1-23Dof-Flat --checkpoint_file=...` 做短回放。
- [ ] 把通过 shape/play 的 candidate 拷贝到本项目 ignored `checkpoints/` 下，再跑 project-local controller smoke。
- [ ] 只有 project-local 23DoF smoke 通过后，才能把它写成 `company_g1_edu_23dof` controller evidence。

## 2026-06-29 Smoke 记录

- [x] 环境检查：`robot` env，Python 3.10.0，torch `2.3.0+cu121`，CUDA visible 8，MuJoCo `3.8.0`，MuJoCo-Warp `3.8.1`。
- [x] 训练启动：`GPU_ID=4 NUM_ENVS=64 MAX_ITERATIONS=1 SAVE_INTERVAL=1 bash scripts/run_unitree_g1_23dof_training_smoke.sh`。
- [x] 成功 run dir：`third_party/unitree_rl_mjlab/logs/rsl_rl/g1_23dof_velocity/2026-06-29_03-19-20_a800_g1_23dof_smoke_wrapper_20260629T031905Z/`。
- [x] 产物：`model_0.pt` 约 4.9 MB，`policy.onnx` 约 819 KB。
- [x] 维度：actor obs `80`，action `23`，critic obs `95`；ONNX input `obs [1,80]`，output `actions [1,23]`。
- [ ] 这只是 1 iteration smoke，不能当成可用 locomotion controller。

## 不要混淆

- [x] 这个训练框架是在当前仓库内搭起来的，不依赖 `/mnt/nvme2n1p1/...` 外部训练目录。
- [x] 不使用 `uv venv` 或 repo-local `.venvs`；默认复用已有 mamba env `robot`。
- [x] `robot` 的 torch 2.3 不支持 `torch.onnx.export(dynamo=...)`；当前仓库 wrapper 会在不改官方 submodule、不改 mamba env 的情况下丢弃这个兼容性参数。
- [x] 29DoF reference ONNX 仍然只能算 `mjlab_g1_29dof_reference` evidence。
- [x] 训练出来的 checkpoint、ONNX、raw logs 不进 git。

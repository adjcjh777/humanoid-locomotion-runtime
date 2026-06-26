# Controller Checkpoint Selection 记录

**日期**: 2026-06-26
**状态**: official Unitree RL MJLab G1 29DoF velocity ONNX candidate downloaded locally; company 23DoF controller pending

## 结论

- [x] 不使用同级目录中的 checkpoint 作为复现前提。
- [x] 本地成熟 checkpoint 搜索已完成：`../mjlab`、`../mjlab_elf3`、`../xiaoqibot` 中未发现可直接用于 Unitree G1 velocity 的成熟 checkpoint。
- [x] 选用官方 Unitree RL MJLab 的 G1 velocity deployment artifact 作为当前项目内 29DoF reference candidate。
- [x] artifact 已下载到 `checkpoints/unitree_rl_mjlab_g1_velocity_v0/`，该目录由 `.gitignore` 忽略，不提交权重。
- [x] 来源、repo commit、路径和 SHA256 已写入 `configs/environment.lock.toml`。
- [x] 已读取 ONNX graph shape 和 metadata：input `obs=[1,98]`，output `actions=[1,29]`。
- [x] 公司 G1 edu 23DoF 官方 URDF/MJCF source 已记录在 `docs/g1_edu_23dof_source_lock.md`，但这不是 controller checkpoint。
- [x] 公司 G1 edu 23DoF raw MuJoCo asset compile smoke 已通过，见 `docs/g1_edu_23dof_compile_smoke.md`；这仍不是 controller checkpoint 或 controller smoke。
- [ ] ONNX candidate 与本仓库 runtime adapter 还未完成 shape/feature adapter；MJLab G1 actor obs 是 `[1,99]`，不是直接同形输入。
- [ ] 当前 ONNX candidate output 是 29DoF，不能直接作为公司 23DoF edu controller evidence。
- [ ] 还未通过 `stand_ready` / `track_velocity` controller smoke。

## 项目内 artifact

| 项 | 值 |
|----|----|
| Local policy | `checkpoints/unitree_rl_mjlab_g1_velocity_v0/policy.onnx` |
| Local deploy params | `checkpoints/unitree_rl_mjlab_g1_velocity_v0/deploy.yaml` |
| Git policy | ignored local artifact; do not commit model weights |
| Fetch script | `scripts/fetch_unitree_g1_velocity_checkpoint.sh` |
| Policy SHA256 | `2a66ca6336eadb3c0b34b557763f3e06d01ff8fcf6260dd4cedbd69d6093fc28` |
| Deploy params SHA256 | `01e1cf3f6ec44e9942494fbb4a9904df07201e14e5551a277f38d7c7d1bda28d` |

## 来源锁定

| 项 | 值 |
|----|----|
| Source repo | `https://github.com/unitreerobotics/unitree_rl_mjlab` |
| Source commit observed | `1425b15f73bd4095f0df53709d7c389c3eb9e790` |
| Policy source path | `deploy/robots/g1/config/policy/velocity/v0/exported/policy.onnx` |
| Params source path | `deploy/robots/g1/config/policy/velocity/v0/params/deploy.yaml` |
| GitHub blob SHA, policy | `b5fc25b7fefd34e59f5b659c6f410c6515e69619` |
| GitHub blob SHA, params | `8561813ab1e8b5151ebb27e27a979e19d43ede4d` |
| Policy size | `878421` bytes |
| Params size | `2289` bytes |
| ONNX input | `obs=[1,98]` |
| ONNX output | `actions=[1,29]` |
| MJLab G1 smoke actor obs | `[1,99]` |
| MJLab G1 smoke action | `[1,29]` |
| Company G1 edu target action | `23DoF target; controller pending` |

## 选择理由

- [x] Unitree 官方仓库明确支持 `Unitree-G1-Flat` velocity tracking workflow。
- [x] 官方 repo 中存在 G1 velocity v0 exported `policy.onnx` 和对应 `deploy.yaml`。
- [x] `deploy.yaml` 的 `joint_ids_map` 覆盖 0-28，共 29 个 G1 joints；`actions.JointPositionAction.scale` 和 `observations` 字段可用于后续 adapter shape 检查。
- [x] artifact 很小，可以由 fetch script 拉取到本项目 ignored checkpoint path；公开仓库只提交 source/hash metadata。
- [x] 因为公司 G1 是 23DoF edu，当前 artifact 只能作为 29DoF reference candidate；23DoF controller 需要单独选择、训练或转换后验证。

## 筛掉的候选

| 候选 | 结论 | 原因 |
|------|------|------|
| Local `../mjlab` / `../mjlab_elf3` logs | 不选 | 只发现 ELF3 tracking 相关 logs/checkpoints，不是 Unitree G1 velocity。 |
| Local `../xiaoqibot` logs | 不选 | 只发现 XiaoQi lower-body velocity checkpoints/ONNX，不是 Unitree G1。 |
| Hugging Face `josabb/G1-humanoid-6dof-hands-locomotion-rl` | 暂不选 | 训练于 MJLab/RSL-RL 且有 `.pt`/ONNX，但模型卡标注为 G1 with 6DoF Inspire hands；需要额外形态匹配和 smoke 后才能采用。 |
| Hugging Face `hardware-pathon-ai/unitree-g1-phase1-locomotion` | 不选 | Isaac Gym checkpoint，模型卡标注 MuJoCo Sim2Sim validation pending；不适合作为 MJLab-first controller evidence。 |
| Hugging Face `cagataydev/sac-unitree-g1-mujoco` | 不选 | SAC/Gym-style zip，不是 MJLab/RSL-RL G1 velocity controller；且模型卡描述仍在学习 balance。 |

## 通过 Gate 的条件

- [ ] `scripts/fetch_unitree_g1_velocity_checkpoint.sh` 可重拉 artifact 并通过 SHA256 检查。
- [ ] MJLab dependency environment 在当前 repo 中可复现安装或运行。
- [ ] Runtime adapter 能读取 `deploy.yaml`，把 MJLab actor/runtime state 转成 ONNX 期望的 98-dim observation，并把 29-dim ONNX output 映射成 typed high-level controller action path。
- [ ] 若目标是公司 G1 edu 23DoF，必须使用 23DoF controller checkpoint，或将 29DoF policy 转成 23DoF adapter experiment 并单独 smoke；不能直接升级为 mature controller evidence。
- [ ] `stand_ready` smoke 通过。
- [ ] `track_velocity` short smoke 通过，且记录为 controller evidence。

在这些条件满足前，`controller_checkpoint.status` 保持 `candidate-downloaded-pending-controller-smoke`，不得把它写成 mature controller evidence。

# G1 edu 23DoF Controller Route 记录

**日期**: 2026-06-26
**状态**: R007e DONE for route/contract lock; controller smoke still pending

这份记录回答 R007e：公司 `company_g1_edu_23dof` 路径下一步不能直接选用当前 29DoF ONNX controller。当前完成的是 controller 路线和维度 contract 锁定，不是 `stand_ready` / `track_velocity` controller smoke。

## 下一步待办清单

- [x] 确认前置：R007d 已通过官方 23DoF raw MuJoCo asset compile smoke。
- [x] 对比 23DoF target 与 MJLab 29DoF reference joint set。
- [x] 锁定 23DoF action dim：`23`。
- [x] 锁定 23DoF MJLab flat actor observation contract：`81`。
- [x] 锁定 23DoF Unitree deploy-style observation contract：`80`。
- [x] 记录 controller route decision：无 mature 23DoF checkpoint，选择 `train_23dof_required`，29DoF ONNX 保持 reference-only。
- [x] 新增机器可读 contract 和测试，防止后续把 29DoF evidence 冒充为 23DoF target evidence。
- [x] 同步 `configs/environment.lock.toml`、tracker、plan、timeline 和 `MANIFEST.md`。

## 结论

R007e 的选择结果是：

| 项 | 值 |
|----|----|
| Robot profile | `company_g1_edu_23dof` |
| Controller profile | `company_g1_edu_23dof_controller_pending_r007e` |
| Selected mature controller source | `none-selected-mature-controller-pending` |
| Route | `train_23dof_required` |
| Controlled DoF / action dim | `23` / `23` |
| Joint-order SHA256 | `186e29d240d7cfeefe4b4c3d8c739c33a779503817ae685783ae5004fd0ebb2c` |
| MJLab flat actor obs dim | `81` |
| Unitree deploy-style obs dim | `80` |
| Mature controller evidence | `false` |

因此：

- [x] 23DoF controller route/contract 已锁定。
- [x] 当前 29DoF ONNX 不升级为 company 23DoF controller evidence。
- [x] 如果未来尝试从 29DoF 转换到 23DoF，只能作为单独 conversion experiment，必须重新 smoke，不得直接标为 mature controller。
- [ ] 23DoF native controller training 或 conversion experiment 尚未完成。
- [ ] `stand_ready` 和 `track_velocity` controller smoke 尚未完成。

## 维度推导

当前 MJLab flat G1 actor observation 使用：

| Term | Dim for 23DoF | Dim for 29DoF reference |
|------|---------------|-------------------------|
| `base_lin_vel` | 3 | 3 |
| `base_ang_vel` | 3 | 3 |
| `projected_gravity` | 3 | 3 |
| `joint_pos_rel` | 23 | 29 |
| `joint_vel_rel` | 23 | 29 |
| `last_action` | 23 | 29 |
| `velocity_command` | 3 | 3 |
| Total | 81 | 99 |

官方 Unitree deploy-style ONNX observation 使用：

| Term | Dim for 23DoF | Dim for 29DoF reference |
|------|---------------|-------------------------|
| `base_ang_vel` | 3 | 3 |
| `projected_gravity` | 3 | 3 |
| `velocity_command` | 3 | 3 |
| `gait_phase` | 2 | 2 |
| `joint_pos_rel` | 23 | 29 |
| `joint_vel_rel` | 23 | 29 |
| `last_action` | 23 | 29 |
| Total | 80 | 98 |

这解释了现有 gap：MJLab actor obs `[1,99]` 与官方 ONNX input `[1,98]` 不是单纯多一个维度，而是 observation template 不同。23DoF 路线下也同样有两套不同 contract：MJLab wrapper contract 是 `81`，deploy-style policy contract 是 `80`。

## Joint Set 差异

23DoF target joint order 来自官方 `g1_23dof_rev_1_0.xml`：

```text
left_hip_pitch_joint
left_hip_roll_joint
left_hip_yaw_joint
left_knee_joint
left_ankle_pitch_joint
left_ankle_roll_joint
right_hip_pitch_joint
right_hip_roll_joint
right_hip_yaw_joint
right_knee_joint
right_ankle_pitch_joint
right_ankle_roll_joint
waist_yaw_joint
left_shoulder_pitch_joint
left_shoulder_roll_joint
left_shoulder_yaw_joint
left_elbow_joint
left_wrist_roll_joint
right_shoulder_pitch_joint
right_shoulder_roll_joint
right_shoulder_yaw_joint
right_elbow_joint
right_wrist_roll_joint
```

MJLab 29DoF reference 比 23DoF 多 6 个 joints：

```text
waist_roll_joint
waist_pitch_joint
left_wrist_pitch_joint
left_wrist_yaw_joint
right_wrist_pitch_joint
right_wrist_yaw_joint
```

所以当前 29DoF policy 的 action head 和 observation slices 都不能直接复用为 23DoF controller evidence。

## 候选决策

| 候选 | R007e 结论 | 原因 |
|------|------------|------|
| Native 23DoF controller training | 选择为主路线 | 与 `company_g1_edu_23dof` action/obs/joint set 一致，是唯一能成为 target evidence 的成熟路线。 |
| 29DoF to 23DoF conversion | 仅允许作为实验 | 需要明确定义 action slice、obs slice、re-normalization、PD/default pose、stability smoke；通过前不能算 mature evidence。 |
| 当前 29DoF ONNX | reference-only | output `[1,29]`，deploy obs `[1,98]`，对应 `mjlab_g1_29dof_reference`，不是公司 23DoF target。 |
| Defer 23DoF controller and use 29DoF path | 只允许 reference path | 可以继续用于 MJLab backend health check，但论文/实验必须标明 robot profile 是 `mjlab_g1_29dof_reference`。 |

## 证据

- [x] 23DoF raw asset compile：`docs/g1_edu_23dof_compile_smoke.md`。
- [x] 23DoF contract code：`src/humanoid_locomotion_runtime/controller_contracts.py`。
- [x] 23DoF contract tests：`tests/test_controller_contracts.py`。
- [x] 环境锁：`configs/environment.lock.toml` 中 `[controller_contracts.company_g1_edu_23dof]`。
- [x] MJLab flat actor evidence：`third_party/mjlab/src/mjlab/tasks/velocity/velocity_env_cfg.py` 和 `third_party/mjlab/src/mjlab/tasks/velocity/config/g1/env_cfgs.py`。
- [x] Unitree deploy-style evidence：ignored local `checkpoints/unitree_rl_mjlab_g1_velocity_v0/deploy.yaml`，source/hash 见 `docs/controller_checkpoint_selection.md`。

## Gate Decision

- [x] R007e can be marked DONE for controller route/contract selection.
- [x] Gate C protocol work may refer to the locked `company_g1_edu_23dof` contract.
- [x] Controller smoke, controller-native baseline, PPO, failure pilots, and paper claims remain blocked until a native 23DoF controller or validated conversion experiment passes smoke.

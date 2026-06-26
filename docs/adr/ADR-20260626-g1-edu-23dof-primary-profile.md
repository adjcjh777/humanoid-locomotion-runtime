# ADR: Unitree G1 Edu 23DoF 作为公司主目标本体

**日期**: 2026-06-26
**状态**: Proposed

## 背景

公司现有 Unitree G1 是 23DoF edu 版本，而当前仓库刚锁定的 MJLab reference path 是 `g1_29dof_rev_1_0`：

- MJLab submodule asset: `third_party/mjlab/src/mjlab/asset_zoo/robots/unitree_g1/xmls/g1.xml`
- MJLab task: `Mjlab-Velocity-Flat-Unitree-G1`
- 已通过的 headless smoke: action `[1,29]`, actor obs `[1,99]`, critic obs `[1,111]`
- 当前官方 ONNX candidate: input `obs=[1,98]`, output `actions=[1,29]`

这说明当前证据只能证明“29DoF reference G1 在 MJLab 中可 reset/step”，不能证明公司 23DoF edu G1 的 controller、adapter、baseline 或 Gate C 已就绪。

更新：官方 23DoF rev 1.0 source 已定位到 Unitree `unitree_rl_gym` 仓库的 `resources/robots/g1_description`，文件为 `g1_23dof_rev_1_0.urdf` 和 `g1_23dof_rev_1_0.xml`。source commit 与 hash 见 `docs/g1_edu_23dof_source_lock.md`。

## 决策

- [x] 将 `company_g1_edu_23dof` 定义为 V0 的 primary deployment robot profile。
- [ ] 将当前 `mjlab_g1_29dof_reference` 保留为 reference smoke / upstream compatibility profile，而不是公司目标本体证据。
- [x] 记录 23DoF 官方 URDF/MJCF source、source commit、file hash 和 URDF joint order。
- [ ] 在 23DoF project-local asset integration、actuator config、controller artifact 和 adapter smoke 锁定前，不启动 Gate C 的 snapshot/restore 或任何 controller-native baseline。
- [ ] 如果短期找不到成熟 23DoF controller，允许保留 29DoF reference smoke 作为 backend health check，但所有文档必须写清楚它不是公司 G1 evidence path。

## 必须先回答的 grilling 问题

1. [x] 公司 23DoF edu 版本的精确 joint name/order 是什么？见 `docs/g1_edu_23dof_source_lock.md`。
2. [x] 少掉的 6 个 DoF 是否就是左右手腕各 3 DoF？不是。与 29DoF rev 1.0 相比，23DoF rev 1.0 少 `waist_roll_joint`、`waist_pitch_joint`、左右 `wrist_pitch_joint`、左右 `wrist_yaw_joint`，保留左右 `wrist_roll_joint`。
3. [x] 公司 23DoF MJCF/MJLab asset 是否已有官方或内部版本？官方 Unitree URDF/MJCF source 已定位；project-local MJLab wrapper 仍未完成。
4. 是否存在 23DoF edu velocity controller checkpoint？它的 obs/action shape、joint order、PD gains 和 deploy params 是什么？
5. 如果只有 29DoF policy，是否允许只把手腕动作屏蔽/固定？这必须先作为 engineering adapter smoke，不得直接算 mature controller evidence。
6. 论文 V0 是要以公司 23DoF edu 为主证据，还是以公开 29DoF reference 为主证据、公司 23DoF 作为后续迁移？这会改变 claim 和实验计划。

## 影响

- 当前 `R002/R007/Gate A` 可保留为 29DoF reference backend evidence。
- `controller_checkpoint.status` 不能升级为 mature controller evidence。
- `Gate C` 的 option/SMDP 和 snapshot/restore 需要等待 robot profile contract，否则 snapshot 里 controller state、action dimension 和 observation hash 都会绑定错本体。
- `controller_native` baseline 必须绑定到明确 robot profile：`company_g1_edu_23dof` 或 `mjlab_g1_29dof_reference`，不能只写 `Unitree G1`。

## 下一步

- [x] 新增 project-local robot profile source lock 文档，记录 23DoF joint list、URDF/MJCF source 和 hash。
- [x] 修改 environment lock，使 primary target 和 reference target 分开。
- [ ] 修改 smoke scripts，使 expected action/obs dim 变成显式参数，并在维度不符时 fail。
- [ ] 修改 Gate A tests，拒绝把 29DoF smoke 当作 23DoF evidence。
- [ ] 同步 README、PRD、Gate A、backend lock、checkpoint selection、experiment plan、timeline、tracker 和 MANIFEST。

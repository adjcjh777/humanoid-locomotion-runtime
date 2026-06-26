# 项目术语表

这份术语表只记录会影响代码接口、实验 gate 或论文 claim 的词。

## Robot Profile

Robot profile 是一个可复查的机器人本体配置，不只是一个名字。至少包含：

- robot profile id
- robot family and hardware revision
- DoF count
- controlled joint names and order
- action dimension
- observation feature contract
- MJCF/MJLab asset path and hash
- controller artifact path/hash
- controller smoke status

## `company_g1_edu_23dof`

公司现有 Unitree G1 edu 版本。它应成为 V0 的 primary deployment robot profile。

当前仍缺少公开仓库可复查证据：

- [x] 23DoF official URDF/MJCF source path and hash
- [x] 23DoF controlled joint names and order from official URDF
- [x] 23DoF raw MuJoCo asset compile smoke
- [ ] project-local MJLab asset/wrapper path and hash
- [ ] 23DoF velocity controller artifact
- [ ] 23DoF obs/action shape
- [ ] 23DoF stand/track smoke

官方 source lock 见 `docs/g1_edu_23dof_source_lock.md`。

## `mjlab_g1_29dof_reference`

当前仓库已锁定并 smoke 通过的 MJLab G1 reference profile。它来自 `third_party/mjlab` 的 `g1_29dof_rev_1_0` asset。

当前已知事实：

- action shape: `[1,29]`
- actor observation shape: `[1,99]`
- critic observation shape: `[1,111]`
- official ONNX candidate output: `actions=[1,29]`

它可以作为 backend health check 和公开 reference path，但不能直接代表公司 23DoF edu G1。

## Controller Evidence

Controller evidence 指 controller artifact 经过 runtime adapter 后，通过目标 robot profile 的 smoke。只下载 ONNX、只检查 hash、或只跑 zero-action environment step，都不能算 mature controller evidence。

最低要求：

- [ ] artifact source and hash locked
- [ ] deploy params locked
- [ ] obs/action shape checked against target robot profile
- [ ] joint order checked against target robot profile
- [ ] `stand_ready` smoke passed
- [ ] short `track_velocity` smoke passed

## Reference Smoke

Reference smoke 是证明某个 backend 或公开模型能运行的轻量检查。它能证明环境健康，但不能替代目标本体的 controller evidence。

当前 29DoF MJLab smoke 就属于 reference smoke，除非项目明确决定论文主证据也使用 29DoF G1。

## Profile-Gated Gate C

Gate C 不能只看 snapshot/restore 代码是否存在。它还必须知道 snapshot 绑定的是哪个 robot profile，因为 action dimension、observation hash、controller recurrent state 和 joint order 都是 robot-profile-specific。

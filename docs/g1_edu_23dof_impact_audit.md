# G1 Edu 23DoF 影响审计

**日期**: 2026-06-26
**状态**: draft audit

## 结论

公司 G1 是 23DoF edu 版本后，当前仓库里所有“Unitree G1 + mature controller”的表述都要拆成两条线：

- `company_g1_edu_23dof`: V0 primary deployment target，官方 Unitree 23DoF rev 1.0 URDF/MJCF source 已定位；project-local MJLab wrapper、controller 和 profile smoke 仍 pending。
- `mjlab_g1_29dof_reference`: 当前已通过的 MJLab reference smoke，action `[1,29]`，不能当作公司 23DoF evidence。

这不是命名问题，而是 action space、observation contract、joint order、controller checkpoint 和 Gate C snapshot contract 都会改变。

## 当前已确认的 29DoF 假设

- [x] `third_party/mjlab/src/mjlab/asset_zoo/robots/unitree_g1/xmls/g1.xml` 的 model name 是 `g1_29dof_rev_1_0`。
- [x] 当前 MJLab smoke 通过的是 `Mjlab-Velocity-Flat-Unitree-G1`，action shape `[1,29]`。
- [x] 当前官方 ONNX candidate 的 output 是 `actions=[1,29]`。
- [x] 当前 `deploy.yaml` 的 `joint_ids_map` 是 0 到 28，共 29 个 joints。

## 当前已确认的 23DoF source

- [x] 官方 source repo：`https://github.com/unitreerobotics/unitree_rl_gym`。
- [x] 官方 source directory：`resources/robots/g1_description`。
- [x] 当前 observed main commit：`276801e46c5d433564f24658bac64f254b7d2d4b`。
- [x] 官方文件：`g1_23dof_rev_1_0.urdf` 和 `g1_23dof_rev_1_0.xml`。
- [x] 官方 README 标注 `g1_23dof_rev_1_0` 为 `Up-to-date`，DoF breakdown 为 legs `6*2`、waist `1`、arms `5*2`、hands `0`。
- [x] 文件 hash、size 和 URDF joint order 已记录到 `docs/g1_edu_23dof_source_lock.md`。

## 需要修改的文档

- [ ] `AGENTS.md`
  - 当前问题：V0 目标只写 `Unitree G1 + 成熟 locomotion controller`，没有区分公司 23DoF edu 与公开 29DoF reference。
  - 修改：增加 robot profile 规则：所有 Gate C 以后工作必须显式声明 `company_g1_edu_23dof` 或 `mjlab_g1_29dof_reference`。

- [ ] `README.md`
  - 当前问题：复现初始化默认拉取 29DoF 官方 ONNX candidate，并只提示 `[1,98]` vs `[1,99]` adapter gap。
  - 修改：增加 23DoF source lock 链接和 warning：当前 ONNX candidate 是 29DoF output，不适配公司 edu 版本；`scripts/mjlab_sync_and_smoke.sh` 只代表 reference smoke。

- [ ] `docs/research_plan_prd.md`
  - 当前问题：多处写 `Unitree G1`，容易被读成公司目标本体已锁定。
  - 修改：在项目记录、V0 成功标准、架构数据流、Story 1、风险与 fallback 中拆分 primary 23DoF profile 与 29DoF reference profile。

- [ ] `docs/gate_a_foundation.md`
  - 当前问题：完成项写“锁定 Unitree G1 MJCF / controller wrapper / ONNX candidate”，但实际锁定的是 29DoF reference。
  - 修改：Gate A 可保持 DONE，但状态应改成“repo foundation + 29DoF reference smoke done; 23DoF primary profile pending”。

- [ ] `docs/mjlab_backend_lock.md`
  - 当前问题：结论写 `G1 asset / wrapper reference selected`，没有标明是 29DoF。
  - 修改：把 `Mjlab-Velocity-Flat-Unitree-G1` 定义为 `mjlab_g1_29dof_reference`；新增 section 记录 23DoF blocker。

- [ ] `docs/controller_checkpoint_selection.md`
  - 当前问题：选择理由写官方 deploy.yaml 覆盖 29 个 joints，但没有将它判定为 incompatible with 23DoF edu。
  - 修改：将当前 ONNX status 从 generic candidate 改成 `29dof-reference-candidate-not-compatible-with-company-23dof`；新增 23DoF checkpoint 搜索/选择条件。

- [ ] `docs/gate_b_schema_edp.md`
  - 当前问题：EDP schema 有 `robot_model` 字段，但没有要求记录 `robot_profile_id`、DoF、action dim、joint order hash。
  - 修改：Gate B 后续扩展项加入 robot profile metadata，避免不同本体的 episode 混在一起分析。

- [ ] `refine-logs/EXPERIMENT_PLAN.md`
  - 当前问题：B0/R007 和 M0 行把 G1 asset/wrapper/checkpoint 当成前置地基已完成。
  - 修改：拆成 `R007a robot profile lock`、`R007b 23DoF asset/controller selection`、`R007c 23DoF smoke`；Gate C 前新增 profile gate。

- [ ] `refine-logs/DAILY_EXPERIMENT_TIMELINE.md`
  - 当前问题：第 4 天写 G1 backend smoke 已完成 29 action/99 obs，但后续仍准备 `stand_ready/track_velocity`。
  - 修改：把第 4 天改成 “29DoF reference smoke complete; 23DoF edu profile smoke pending”；禁止夜间跑 Gate C 相关任务。

- [ ] `refine-logs/EXPERIMENT_TRACKER.md`
  - 当前问题：R002/R007 是 DONE，但备注没有明确它们不是 23DoF target evidence。
  - 修改：R002/R007 备注标记 reference-only；新增 R007a/R007b/R007c 或等价 run ids。

- [ ] `MANIFEST.md`
  - 当前问题：已有 MJLab/backend/checkpoint 记录均未显式声明 29DoF reference-only。
  - 修改：登记本审计、ADR 和 glossary；后续修改 latest docs 时同步 timestamped companion。

## 需要修改的配置

- [ ] `configs/environment.lock.toml`
  - 当前问题：`[mjlab_backend]`、`[controller_checkpoint]`、`[robot_mjcf]` 只描述一条 G1 线。
  - 修改：
    - 新增 `[robot_profiles.company_g1_edu_23dof]`，状态为 `official-source-identified-integration-pending`。
    - 将现有 `[robot_mjcf]` 标成 `mjlab_g1_29dof_reference`。
    - 将现有 `[controller_checkpoint]` 标成 `29dof-reference-candidate`，并写明不兼容 23DoF primary profile。
    - 记录 required evidence：23DoF MJCF hash、joint list hash、controller hash、smoke output。

## 需要修改的代码和测试

- [x] `scripts/mjlab_g1_smoke.py`
  - 当前问题：只打印 action/obs shape，不检查是否符合目标 robot profile。
  - 修改：增加 `--expected-action-dim`、`--expected-actor-obs-dim`、`--expected-robot-profile`，维度不符直接失败。

- [ ] `scripts/mjlab_sync_and_smoke.sh`
  - 当前问题：固定跑 `Mjlab-Velocity-Flat-Unitree-G1`，并默认 29DoF reference。
  - 修改：支持 profile 参数；默认如果 target 是 `company_g1_edu_23dof`，没有 23DoF task 时应 fail，而不是默默跑 29DoF。

- [ ] `scripts/fetch_unitree_g1_velocity_checkpoint.sh`
  - 当前问题：脚本名和 echo 文案容易让人以为拿到的就是公司 G1 controller。
  - 修改：重命名或增加 warning，明确下载的是 29DoF reference candidate；新增 23DoF checkpoint fetch/verify 脚本前不允许升级 evidence。

- [x] `src/humanoid_locomotion_runtime/schemas.py`
  - 当前问题：`EpisodeManifest` 只有 `robot_model`，无法强制记录 DoF/action dim/joint order hash。
  - 修改：新增或扩展 robot profile schema，例如 `robot_profile_id`、`robot_dof`、`action_dim`、`joint_order_sha256`、`controller_profile_id`。

- [x] `src/humanoid_locomotion_runtime/edp.py`
  - 当前问题：sample EDP 写 `robot_model="none"`，后续真实 EDP 若不含 profile 会混淆 23/29DoF。
  - 修改：sample 可以保留 none，但 validator 对真实 MuJoCo episodes 应要求 robot profile metadata。

- [x] `tests/test_gate_a_foundation.py`
  - 当前问题：测试断言当前 checkpoint shape 包含 `input obs=[1,98]`，但没有断言这是 29DoF reference-only。
  - 修改：新增测试：primary profile 是 `company_g1_edu_23dof` 时，29DoF checkpoint 不能被标成 mature controller evidence。

- [ ] 新增 `tests/test_robot_profile_lock.py`
  - 目标：检查 23DoF profile 一旦声明为 primary，就必须有 joint list、MJCF hash、action dim、controller status 和 smoke evidence。

## 不建议修改的内容

- [ ] 不直接修改 `third_party/mjlab` upstream submodule，除非决定维护 project-local patch 或 fork。
- [ ] 不回写旧 timestamped snapshots 的历史结论；用新 timestamped artifact 和 MANIFEST 说明这些旧快照已被 23DoF 审计 supersede。
- [ ] 不把 29DoF policy 通过固定手腕/裁剪动作的方式直接升级成 23DoF mature evidence；这种路径最多先叫 adapter experiment。

## Gate 影响

- [x] Gate A repo foundation 本身仍然有效。
- [x] Gate B schema/leakage boundary 本身仍然有效。
- [x] R007d raw asset compile smoke 已通过；证据：`docs/g1_edu_23dof_compile_smoke.md`。
- [ ] Gate C 必须等待 R007e / robot profile runtime contract；否则 snapshot/restore 会绑定错误 action/obs/controller state。
- [ ] R020 controller-native baseline 必须等待 23DoF target smoke 或明确改成 29DoF reference baseline。
- [ ] 所有论文 claim 里的 `Unitree G1` 必须改成具体 profile，避免 reviewer 追问 23/29DoF 不一致。

## 推荐执行顺序

1. [x] 向硬件/仿真负责人确认公司 23DoF edu joint list 和 MJCF 来源。
2. [x] 新增 `configs/robot_profiles/` 或等价 TOML section，锁定 `company_g1_edu_23dof`。
3. [x] 将现有 29DoF MJLab smoke 降级命名为 reference smoke。
4. [ ] 搜索或复制 23DoF edu controller checkpoint；若不存在，先决定是否训练/转换/暂用 29DoF reference。
5. [x] 修改 smoke scripts 和 Gate A tests，使 wrong-profile smoke 会失败。
6. [x] 完成 23DoF raw asset fetch/verify 和 MuJoCo compile smoke。
7. [x] 同步 README、PRD、Gate A、backend lock、checkpoint selection、plan、timeline、tracker 和 timestamped companions。

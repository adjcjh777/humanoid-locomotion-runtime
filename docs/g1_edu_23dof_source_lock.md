# G1 Edu 23DoF Source Lock

**日期**: 2026-06-26
**状态**: official source identified; raw MuJoCo asset compile smoke passed; project-local MJLab/controller integration pending

## 结论

- [x] 公司 G1 edu 23DoF 的官方描述来源已定位到 Unitree 官方仓库。
- [x] 官方目录包含 `g1_23dof_rev_1_0.urdf` 和 `g1_23dof_rev_1_0.xml`。
- [x] 官方 README 标注 `g1_23dof_rev_1_0` 为 `Up-to-date`，DoF breakdown 是 legs `6*2`、waist `1`、arms `5*2`、hands `0`。
- [x] 当前 source commit 和文件 SHA256 已记录。
- [x] 23DoF URDF/MJCF 和 27 个官方 STL mesh assets 可由 fetch script 拉到 git ignored `robot_descriptions/` 路径并通过 SHA256 校验。
- [x] 23DoF MJCF raw asset compile smoke 已通过 MuJoCo 3.10.0；证据见 `docs/g1_edu_23dof_compile_smoke.md`。
- [ ] 尚未把 23DoF asset vendor 到 tracked project-local MJLab wrapper。
- [ ] 尚未完成 23DoF MJLab task adapter、controller checkpoint selection 或 controller smoke。

## 官方来源

| 项 | 值 |
|----|----|
| Source repo | `https://github.com/unitreerobotics/unitree_rl_gym` |
| Source directory | `resources/robots/g1_description` |
| Branch observed | `main` |
| Commit observed | `276801e46c5d433564f24658bac64f254b7d2d4b` |
| Directory URL | `https://github.com/unitreerobotics/unitree_rl_gym/tree/main/resources/robots/g1_description` |
| URDF path | `resources/robots/g1_description/g1_23dof_rev_1_0.urdf` |
| MJCF path | `resources/robots/g1_description/g1_23dof_rev_1_0.xml` |

## 文件锁定

| File | Size bytes | SHA256 |
|------|------------|--------|
| `g1_23dof_rev_1_0.urdf` | `28789` | `cffe6149e0b29abed10b8c6a7e318003676ae4234224044e4af30946599d1ba9` |
| `g1_23dof_rev_1_0.xml` | `20834` | `8ca62fcccdca91a431ca04f1a42f9c2fda241fdd5e13411168dc82de00f978de` |

Mesh assets are fetched from the same pinned source commit by `scripts/fetch_unitree_g1_23dof_description.sh`. The local ignored asset manifest contains 29 files total and has SHA256 `ff699c19c0d28feee34bb0af1e6a02e6c30850db0e21ad90bbcd277a7bb3a007`.

## URDF controlled joint order

下面是从官方 `g1_23dof_rev_1_0.urdf` 中解析出的非 fixed joint 顺序。`floating_base_joint` 是 floating base，不计入 23 个受控 DoF。

| Index | Joint | Type | Controlled DoF |
|-------|-------|------|----------------|
| base | `floating_base_joint` | floating | no |
| 0 | `left_hip_pitch_joint` | revolute | yes |
| 1 | `left_hip_roll_joint` | revolute | yes |
| 2 | `left_hip_yaw_joint` | revolute | yes |
| 3 | `left_knee_joint` | revolute | yes |
| 4 | `left_ankle_pitch_joint` | revolute | yes |
| 5 | `left_ankle_roll_joint` | revolute | yes |
| 6 | `right_hip_pitch_joint` | revolute | yes |
| 7 | `right_hip_roll_joint` | revolute | yes |
| 8 | `right_hip_yaw_joint` | revolute | yes |
| 9 | `right_knee_joint` | revolute | yes |
| 10 | `right_ankle_pitch_joint` | revolute | yes |
| 11 | `right_ankle_roll_joint` | revolute | yes |
| 12 | `waist_yaw_joint` | revolute | yes |
| 13 | `left_shoulder_pitch_joint` | revolute | yes |
| 14 | `left_shoulder_roll_joint` | revolute | yes |
| 15 | `left_shoulder_yaw_joint` | revolute | yes |
| 16 | `left_elbow_joint` | revolute | yes |
| 17 | `left_wrist_roll_joint` | revolute | yes |
| 18 | `right_shoulder_pitch_joint` | revolute | yes |
| 19 | `right_shoulder_roll_joint` | revolute | yes |
| 20 | `right_shoulder_yaw_joint` | revolute | yes |
| 21 | `right_elbow_joint` | revolute | yes |
| 22 | `right_wrist_roll_joint` | revolute | yes |

## 与当前 29DoF reference 的关键差异

- [x] 23DoF rev 1.0 只有 `waist_yaw_joint`，没有 `waist_roll_joint` 和 `waist_pitch_joint`。
- [x] 23DoF rev 1.0 每条手臂是 5DoF，包含 `wrist_roll_joint`，没有 `wrist_pitch_joint` 和 `wrist_yaw_joint`。
- [x] 当前 MJLab reference / ONNX candidate 是 29DoF，包含 3DoF waist 和每臂 7DoF，因此不能直接作为 23DoF controller evidence。

## R007d Raw Compile Smoke

- [x] Fetch/verify command: `bash scripts/fetch_unitree_g1_23dof_description.sh`
- [x] Compile command: `uv run --extra sim python scripts/compile_unitree_g1_23dof_description.py`
- [x] Result: PASS with MuJoCo `3.10.0`.
- [x] Compile summary: `nq=30`, `nv=29`, `nu=23`, `nbody=25`, `njnt=24`, `ngeom=60`, `nmesh=27`.
- [x] Joint gate: `floating_base_joint` plus 23 controlled joints, matching the locked official 23DoF joint order above.

## 后续实机前必须完成

- [x] 写 fetch script 在复现时拉取 URDF/MJCF/mesh assets 并校验 SHA256，下载产物保持在 git 外。
- [x] 下载官方 mesh assets，并通过 MuJoCo compile smoke。
- [ ] 建立 23DoF MJLab robot cfg / task cfg / action scale / actuator config。
- [ ] 选择或训练 23DoF controller checkpoint。
- [ ] 记录 23DoF controller obs/action shape、joint order、PD gains、deploy params 和 smoke evidence。

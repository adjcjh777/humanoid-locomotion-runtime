# G1 Edu 23DoF Raw Asset Compile Smoke

**日期**: 2026-06-26
**状态**: R007d DONE

这份记录只证明官方 Unitree G1 edu 23DoF URDF/MJCF 和 mesh assets 可以在当前仓库的 MuJoCo 3.10.0 环境中编译。它不代表 MJLab wrapper、controller checkpoint、`stand_ready`、`track_velocity` 或 controller-native baseline 已完成。

## 下一步待办清单

- [x] 确认 R007d 前置条件：R007b fetch/verify script 已存在，`robot_descriptions/` 由 `.gitignore` 排除。
- [x] 扩展 `scripts/fetch_unitree_g1_23dof_description.sh`，拉取官方 URDF、MJCF 和 27 个 STL mesh assets。
- [x] 为每个下载文件写入 pinned SHA256 校验，避免 source drift。
- [x] 修复 fetch 脚本的 `git check-ignore -q` 多路径误报，逐个检查 ignored destination。
- [x] 新增 `scripts/compile_unitree_g1_23dof_description.py`，作为 R007d 标准 compile smoke 入口。
- [x] 执行 fetch/verify：`bash scripts/fetch_unitree_g1_23dof_description.sh`。
- [x] 执行 compile smoke：`uv run --extra sim python scripts/compile_unitree_g1_23dof_description.py`。
- [x] 记录 compile summary、asset manifest 和剩余 blocker。

## 命令结果

| 项 | 结果 |
|----|------|
| Source repo | `https://github.com/unitreerobotics/unitree_rl_gym` |
| Source commit | `276801e46c5d433564f24658bac64f254b7d2d4b` |
| Local ignored root | `robot_descriptions/unitree_g1_23dof_rev_1_0/` |
| Fetched files | 29 total: URDF + MJCF + 27 STL mesh assets |
| Total local bytes | `25213341` |
| Asset manifest SHA256 | `ff699c19c0d28feee34bb0af1e6a02e6c30850db0e21ad90bbcd277a7bb3a007` |
| MuJoCo version | `3.10.0` |
| Compile status | PASS |
| `nq` | `30` |
| `nv` | `29` |
| `nu` | `23` |
| `nbody` | `25` |
| `njnt` | `24` |
| `ngeom` | `60` |
| `nmesh` | `27` |
| Controlled joints excluding `floating_base_joint` | `23` |

## Joint Gate

Compile smoke verified the official joint order:

1. `floating_base_joint`
2. `left_hip_pitch_joint`
3. `left_hip_roll_joint`
4. `left_hip_yaw_joint`
5. `left_knee_joint`
6. `left_ankle_pitch_joint`
7. `left_ankle_roll_joint`
8. `right_hip_pitch_joint`
9. `right_hip_roll_joint`
10. `right_hip_yaw_joint`
11. `right_knee_joint`
12. `right_ankle_pitch_joint`
13. `right_ankle_roll_joint`
14. `waist_yaw_joint`
15. `left_shoulder_pitch_joint`
16. `left_shoulder_roll_joint`
17. `left_shoulder_yaw_joint`
18. `left_elbow_joint`
19. `left_wrist_roll_joint`
20. `right_shoulder_pitch_joint`
21. `right_shoulder_roll_joint`
22. `right_shoulder_yaw_joint`
23. `right_elbow_joint`
24. `right_wrist_roll_joint`

The first joint is the floating base; the remaining 23 joints are the controlled 23DoF profile.

## Gate Decision

- [x] R007d can be marked DONE for raw asset compile smoke.
- [x] R007e is now DONE for controller route/contract lock; see `docs/g1_edu_23dof_controller_route.md`.
- [x] Gate C protocol work may reference the locked `company_g1_edu_23dof` robot/controller contract, but controller smoke remains blocked until a native 23DoF controller or validated conversion experiment exists.
- [x] The current 29DoF ONNX candidate is still not company 23DoF mature controller evidence.

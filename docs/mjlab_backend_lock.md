# MJLab Backend Lock 记录

**日期**: 2026-06-26
**状态**: project-local 29DoF reference backend / G1 asset / controller wrapper selected; full MJLab G1 headless simulation smoke passed; company 23DoF raw asset compile smoke passed but runtime integration pending

## 结论

- [x] V0 backend reference 改为当前仓库内的 `third_party/mjlab` git submodule，不依赖同级目录。
- [x] 锁定 MJLab upstream：`https://github.com/mujocolab/mjlab.git`。
- [x] 锁定 MJLab commit：`efdcadc8b281553fd3e1be2a9a88db9553356e8a`。
- [x] 锁定主任务入口：`Mjlab-Velocity-Flat-Unitree-G1`。
- [x] 锁定 fallback task：`Mjlab-Velocity-Rough-Unitree-G1`。
- [x] 锁定 Unitree G1 MJCF：`third_party/mjlab/src/mjlab/asset_zoo/robots/unitree_g1/xmls/g1.xml`。
- [x] 锁定 controller wrapper 入口：`third_party/mjlab/src/mjlab/tasks/velocity/rl/runner.py` 中的 `VelocityOnPolicyRunner`。
- [x] 下载官方 Unitree RL MJLab G1 velocity ONNX controller artifact candidate 到本项目 ignored checkpoint 路径。
- [x] 在当前 runtime repo 中解决完整 MJLab dependency environment，并运行 project-local MJLab G1 headless simulation smoke。
- [x] 公司 G1 edu 23DoF 官方 source 已记录在 `docs/g1_edu_23dof_source_lock.md`，raw MuJoCo asset compile smoke 记录在 `docs/g1_edu_23dof_compile_smoke.md`。
- [ ] 验证 ONNX candidate 的 observation/action shape 与 runtime adapter 后，才能把它升级为 mature controller evidence。
- [ ] 将官方 23DoF URDF/MJCF 接入 project-local MJLab runtime 并通过 23DoF MJLab/controller smoke。

## 候选比较

| 候选 | 结论 | 理由 |
|------|------|------|
| `third_party/mjlab` | 选用 | 项目内 git submodule；开源复现者只需 `git submodule update --init --recursive`，不需要拥有作者机器上的同级目录。 |
| `../mjlab` | 不选 | 只能作为本机参考来源；不能作为开源复现前提。 |
| `../mjlab_elf3` | 不选 | ELF3 本地实验方向，不作为 V0 G1-first backend evidence path。 |
| `../xiaoqibot` | 不选 | 当前 active profile 是 XiaoQi 12-DOF lower-body asset；不是 Unitree G1，也不是 V0 的 G1-first evidence backend。 |

## 锁定事实

| 项 | 值 |
|----|----|
| Local path | `third_party/mjlab` |
| Git origin | `https://github.com/mujocolab/mjlab.git` |
| Branch/ref | `main` |
| Commit | `efdcadc8b281553fd3e1be2a9a88db9553356e8a` |
| Commit describe | `v1.1.1-259-gefdcadc8` |
| Commit date | `2026-06-18` |
| Package version | `mjlab==1.4.0` |
| Selected task | `Mjlab-Velocity-Flat-Unitree-G1` |
| Fallback task | `Mjlab-Velocity-Rough-Unitree-G1` |
| Robot profile role | `mjlab_g1_29dof_reference`; not company `company_g1_edu_23dof` evidence |
| Robot MJCF SHA256 | `febdcbeffbbf84051556ae41a5ac1b43fb479a5d76bdb3f54824dbc2721c20aa` |
| G1 asset tree manifest SHA256 | `067725caac9efe43e91d51c97e28bc75a04065d5be666fceeff8334831a107e4` |
| G1 mesh asset manifest SHA256 | `203eca02f0d048b9c6d9c4a3dddc2fb4c533e270dc107645c0caced76247f10b` |
| MJLab runtime Python | `3.12.13` via main project `.venv/bin/python3` |
| MJLab runtime sync | `scripts/mjlab_sync_and_smoke.sh` |
| MJLab runtime key packages | `torch==2.9.0+cu128`, `mujoco-warp==3.9.0.1`, `warp-lang==1.14.0`, `rsl-rl-lib==5.4.0`, `tyro==1.0.1` |

## 关键路径与 Hash

| 角色 | Path | SHA256 |
|------|------|--------|
| Robot MJCF | `third_party/mjlab/src/mjlab/asset_zoo/robots/unitree_g1/xmls/g1.xml` | `febdcbeffbbf84051556ae41a5ac1b43fb479a5d76bdb3f54824dbc2721c20aa` |
| G1 constants / robot cfg | `third_party/mjlab/src/mjlab/asset_zoo/robots/unitree_g1/g1_constants.py` | `856492f9cd74b32e76fedafc583e284d14542eacd20261adcebe5c5c2345a258` |
| G1 task registration | `third_party/mjlab/src/mjlab/tasks/velocity/config/g1/__init__.py` | `f4482cf1f1bb27989b0de3f1f45c0c1568185a632c9eb36cc18595cf95ac79cf` |
| G1 env config | `third_party/mjlab/src/mjlab/tasks/velocity/config/g1/env_cfgs.py` | `5d891ef40987118d1bb2d4bb8791922387d8fdae22752f1e1420dc31f4ddeabf` |
| G1 RL config | `third_party/mjlab/src/mjlab/tasks/velocity/config/g1/rl_cfg.py` | `dcf4a23e031064085e081798c4d3b5bd1cda6ec58ad0081907f2e72c9142a131` |
| Velocity runner / wrapper | `third_party/mjlab/src/mjlab/tasks/velocity/rl/runner.py` | `fd5ab5b61c60516213724b65954e7eabc1a3ca2d4101019d0c53e33fac1285c4` |

## 已做适配检查

- [x] 当前 runtime repo 的 `uv run --extra sim` 能 import MuJoCo 3.10.0。
- [x] 当前 runtime repo 的 lightweight sim extra 能直接编译 G1 raw MJCF：
  - command summary: `uv run --extra sim python -c "... mujoco.MjModel.from_xml_path('third_party/mjlab/.../g1.xml') ..."`
  - result: `mujoco 3.10.0 nq 36 nv 35 nu 0`
- [x] MJLab tracked G1 task registration 包含：
  - `Mjlab-Velocity-Flat-Unitree-G1`
  - `Mjlab-Velocity-Rough-Unitree-G1`
- [x] `g1_constants.py` 提供 `get_g1_robot_cfg()`、`G1_ACTION_SCALE` 和 position actuator configuration；实际 actuators 由 MJLab entity/config layer 添加，不直接写在 raw `g1.xml` 中。
- [x] 完整 MJLab runtime dependency smoke 通过：
  - command summary: `scripts/mjlab_sync_and_smoke.sh`
  - Python: `3.12.13`
  - Torch/CUDA: `torch==2.9.0+cu128`, `cuda_available=True`, `cuda_device_count=8`
  - MuJoCo/MuJoCo-Warp: `mujoco==3.8.1`, `mujoco-warp==3.9.0.1`, `warp==1.14.0`
- [x] 完整 MJLab G1 headless simulation smoke 通过：
  - task: `Mjlab-Velocity-Flat-Unitree-G1`
  - device: `cuda:0`
  - steps: `16` zero-action steps
  - action shape: `[1, 29]`
  - actor observation shape: `[1, 99]`
  - critic observation shape: `[1, 111]`
  - reward finite
  - `terminated_count=0`, `timeout_count=0`
- [x] 公司 23DoF raw asset compile smoke 通过：
  - command summary: `uv run --extra sim python scripts/compile_unitree_g1_23dof_description.py`
  - MuJoCo: `3.10.0`
  - result: `nq=30`, `nv=29`, `nu=23`, `nbody=25`, `njnt=24`, `ngeom=60`, `nmesh=27`
  - joint gate: `floating_base_joint` plus 23 controlled joints

## 未完成边界

- [ ] 官方 Unitree ONNX controller artifact candidate 已下载，但还没有通过本仓库 runtime adapter 的 observation/action shape 检查。当前 ONNX input 是 `[1,98]`，MJLab actor obs 是 `[1,99]`，不能直接宣称 trained-controller smoke。
- [ ] 当前 MJLab G1 headless smoke 是 29DoF reference smoke，不能直接代表公司 G1 edu 23DoF runtime/controller evidence；23DoF 目前只到 raw MuJoCo asset compile smoke。
- [ ] `stand_ready`、`safe_stop`、`track_velocity` runtime adapter command 尚未实现。

## 下一步怎么做

1. 在当前 runtime repo 中新增 MJLab backend adapter，只通过 `RuntimeManager` 发出高层 typed command。
2. 先实现非学习的 smoke modes：
   - `safe_stop`: 清零/保持安全目标，确认控制通路不崩。
   - `stand_ready`: 使用 G1 initial state 和合法 joint-position wrapper，确认站立初始化。
   - `track_velocity`: 只有在 checkpoint candidate 通过 shape 和 controller smoke 后才作为 mature controller evidence。
3. 在 adapter 中保留 leakage boundary：MuJoCo privileged object IDs、ground-truth target poses、simulator semantic labels 只进 evaluation，不进 runtime decision。
4. controller smoke 通过后，再解锁 R010+ failure protocol pilot；PPO 和大规模实验仍需等后续 Gate。

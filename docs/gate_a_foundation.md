# Gate A 工程地基记录

**日期**: 2026-06-25
**状态**: 仓库地基和环境锁定脚手架已完成

读法：Gate A 的作用很简单，先确认这个仓库能被稳定安装、测试、复现，并且不会把机器私有信息或大型实验产物提交进 git。它不代表 controller、MuJoCo/G1 集成或论文实验已经完成。

## 完成项

- [x] `pyproject.toml`、`.python-version` 和 `uv.lock` 已建立 Python 3.12.13 工程入口。
- [x] `src/` 和 `tests/` 已建立最小可运行 package 与 Gate A 校验。
- [x] `.github/workflows/ci.yml` 建立 CI：`uv sync --locked`、`ruff check`、`pytest`。
- [x] `LICENSE` 已加入。
- [x] `configs/environment.lock.toml` 锁定 Python、uv、MuJoCo、项目内 `third_party/mjlab` 29DoF reference backend、官方 Unitree G1 edu 23DoF source、23DoF raw asset compile smoke、controller wrapper、完整 MJLab runtime dependency smoke 和官方 Unitree ONNX controller artifact candidate；JAX/JAXLIB 只作为 deferred MuJoCo Playground extra。
- [x] `configs/artifact_retention.toml` 定义 generated artifacts、raw agent traces 和 disk gate 策略。意思是：哪些实验产物能保留、哪些必须留在 git 外，都有明确规则。
- [x] `.aris/meta/`、`.aris/traces/`、机器 hostname、用户名、绝对路径、实时 GPU 占用保持在公开仓库外。

## 明确未授权项

Gate A 只证明仓库地基可用，不授权下面这些事：

- [ ] 不启动 PPO。
- [ ] 不启动大规模 rollout。
- [ ] 不写论文主结论。
- [ ] 不把 controller checkpoint candidate 当作已通过 smoke 的成熟 controller evidence。

## 后续阻塞字段

`configs/environment.lock.toml` 现在已锁定项目内 `third_party/mjlab` 的 Unitree G1 backend reference、G1 MJCF 和 `VelocityOnPolicyRunner` wrapper；详细证据见 `docs/mjlab_backend_lock.md`。

完整 MJLab simulation smoke 已通过：`scripts/mjlab_sync_and_smoke.sh` 使用主项目 Python 3.12.13、`third_party/mjlab/uv.lock`、`torch==2.9.0+cu128`、`mujoco-warp==3.9.0.1`，在 A800 `cuda:0` 上创建 `Mjlab-Velocity-Flat-Unitree-G1`，reset 后执行 16 个 zero-action steps；actor obs `[1,99]`、critic obs `[1,111]`、action `[1,29]`，reward finite，`terminated_count=0`，`timeout_count=0`。

公司 G1 edu 23DoF 官方 source 已定位：`unitreerobotics/unitree_rl_gym` 的 `g1_23dof_rev_1_0.urdf` 和 `g1_23dof_rev_1_0.xml`。source commit、hash、DoF breakdown 和 joint order 见 `docs/g1_edu_23dof_source_lock.md`。R007d raw asset compile smoke 已通过：fetch script 拉取 URDF/MJCF 和 27 个 STL mesh assets 到 ignored `robot_descriptions/`，`uv run --extra sim python scripts/compile_unitree_g1_23dof_description.py` 在 MuJoCo 3.10.0 下得到 `nq=30`、`nv=29`、`nu=23`、`njnt=24`、`nmesh=27`。这仍不等于 project-local MJLab adapter 或 controller smoke 已通过。

`controller_checkpoint.sha256` 已记录官方 Unitree RL MJLab G1 velocity ONNX candidate 的本地 artifact hash，状态为 `candidate-downloaded-pending-controller-smoke`。ONNX candidate input 是 `[1,98]`，output 是 `[1,29]`；MJLab actor obs 是 `[1,99]`，所以进入 velocity-tracking trained-controller smoke、baseline、branching 或论文证据前，仍必须实现 adapter 并通过 controller smoke。该 ONNX candidate 属于 29DoF reference path，不能直接作为公司 23DoF edu controller evidence；选择记录见 `docs/controller_checkpoint_selection.md`。

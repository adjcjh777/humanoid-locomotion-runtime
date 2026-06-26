# Gate A 工程地基记录

**日期**: 2026-06-25
**状态**: 仓库地基和环境锁定脚手架已完成

读法：Gate A 的作用很简单，先确认这个仓库能被稳定安装、测试、复现，并且不会把机器私有信息或大型实验产物提交进 git。它不代表 controller、MuJoCo/G1 集成或论文实验已经完成。

## 完成项

- [x] `pyproject.toml`、`.python-version` 和 `uv.lock` 已建立 Python 3.12.13 工程入口。
- [x] `src/` 和 `tests/` 已建立最小可运行 package 与 Gate A 校验。
- [x] `.github/workflows/ci.yml` 建立 CI：`uv sync --locked`、`ruff check`、`pytest`。
- [x] `LICENSE` 已加入。
- [x] `configs/environment.lock.toml` 锁定 Python、uv、MuJoCo 和 MJLab/mujocolab-first backend policy；JAX/JAXLIB 只作为 deferred MuJoCo Playground extra。
- [x] `configs/artifact_retention.toml` 定义 generated artifacts、raw agent traces 和 disk gate 策略。意思是：哪些实验产物能保留、哪些必须留在 git 外，都有明确规则。
- [x] `.aris/meta/`、`.aris/traces/`、机器 hostname、用户名、绝对路径、实时 GPU 占用保持在公开仓库外。

## 明确未授权项

Gate A 只证明仓库地基可用，不授权下面这些事：

- [ ] 不启动 PPO。
- [ ] 不启动大规模 rollout。
- [ ] 不写论文主结论。
- [ ] 不把 controller checkpoint 或 robot XML/MJCF 当作已选择资产。

## 后续阻塞字段

`configs/environment.lock.toml` 中 `controller_checkpoint.sha256` 和 `robot_mjcf.sha256` 仍为空，状态为 `unselected`。

进入 controller smoke gate 前，必须写入真实来源和 SHA256。不能用空值跑 baseline、snapshot branching 或论文证据。

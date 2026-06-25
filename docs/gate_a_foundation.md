# Gate A 工程地基记录

**日期**: 2026-06-25
**状态**: complete for repository foundation and environment-lock scaffold

## 完成项

- [x] `pyproject.toml`、`.python-version` 和 `uv.lock` 建立 Python 3.12.13 工程入口。
- [x] `src/` 和 `tests/` 建立最小可运行 package 与 Gate A 校验。
- [x] `.github/workflows/ci.yml` 建立 CI：`uv sync --locked`、`ruff check`、`pytest`。
- [x] `LICENSE` 已加入。
- [x] `configs/environment.lock.toml` 锁定 Python、uv、MuJoCo、JAX/JAXLIB、CUDA wheel extra 和 `mujoco_playground` tag/commit。
- [x] `configs/artifact_retention.toml` 定义 generated artifacts、raw agent traces 和 disk gate 策略。
- [x] `.aris/meta/`、`.aris/traces/`、机器 hostname、用户名、绝对路径、实时 GPU 占用保持在公开仓库外。

## 明确未授权项

- [ ] 不启动 PPO。
- [ ] 不启动大规模 rollout。
- [ ] 不写论文主结论。
- [ ] 不把 controller checkpoint 或 robot XML/MJCF 当作已选择资产。

## 后续阻塞字段

`configs/environment.lock.toml` 中 `controller_checkpoint.sha256` 和 `robot_mjcf.sha256` 仍为空，状态为 `unselected`。进入 controller smoke gate 前必须写入真实来源和 SHA256；不能用空值跑基线、branching 或论文证据。

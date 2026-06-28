# Mac 本机安全工作清单

**日期**: 2026-06-28  
**状态**: active latest copy; extended Mac-safe skeletons synced
**适用主机**: 当前 Mac 本机工作室  
**目标**: 列出当前这台 Mac 可以推进、且不会污染或抢占 A800 主实验线的工作。

## 当前本机证据

- [x] 当前 checkout 已同步到 `origin/main` 的 `87b94fd`，并从该点切出 `feature/mac-safe-completion`；证据：`git log --oneline --decorate -5`。
- [x] 当前 Mac 是 Apple Silicon macOS，不是 A800/CUDA 实验机；证据：`uname -a` 显示 `Darwin ... RELEASE_ARM64_T8132 arm64`。
- [x] 当前 shell 里的 `uv` 是 `0.11.25`，满足项目 `>=0.11.23,<0.12` 约束；证据：`uv --version`、`pyproject.toml`。
- [x] 当前 `uv run python --version` 为 `Python 3.12.13`；证据：`.python-version`、`uv run python --version`。
- [x] 当前 `third_party/mjlab` 是未初始化 submodule 指针；证据：`git submodule status` 前缀为 `-`。
- [x] 当前仓库没有本机生成的 `.agents/`、`.aris/`、`robot_descriptions/`、`checkpoints/`、`runs/`、`logs/`、`artifacts/`、`weights/`、`datasets/` 目录；证据：`find . -maxdepth 2 ...` 无 tracked-output 目录。

## 可以在 Mac 立即做

- [x] **M-MAC-001: 对齐本机工具链**。本机 `uv` 为 `0.11.25`，`uv run python --version` 为 `Python 3.12.13`；只产生 ignored `.venv/`，不提交 generated env。
- [x] **M-MAC-002: 跑纯 Python 合同测试**。已运行纯 Python contract pytest；本轮新增后 scoped test 结果见下方验证命令，未生成 tracked runs。
- [x] **M-MAC-003: 完成 Gate C backend-neutral contract work**。已补 `DecisionEpoch`、`CommonRandomStream`、`SnapshotProvider` protocol、`FakeDeterministicSnapshotProvider` 和 fake deterministic restore roundtrip tests；证据：`src/humanoid_locomotion_runtime/snapshot_branching.py`、`tests/test_snapshot_branching.py`。边界：这只是 fake backend testbed，R018 deterministic simulator/runtime restore 仍未完成。
- [x] **M-MAC-004: 实现 RuntimeManager typed command skeleton**。已实现 `RuntimeManager`、`SafetySupervisor`、`RuntimeCommandEnvelope` 和 `FakeRuntimeBackend`；覆盖 `stand_ready`、`safe_stop`、`track_velocity`、`walk_to`、`turn_to` 的高层 routing shape，且 fake backend 只接受 RuntimeManager envelope；证据：`src/humanoid_locomotion_runtime/runtime_manager.py`、`tests/test_runtime_manager.py`。边界：不接真实 controller，不产生 controller smoke 证据。
- [x] **M-MAC-005: 强化 leakage boundary 测试**。新增 runtime payload hash、snapshot fake provider、safety decision、runtime command envelope 的嵌套 privileged-field 拒绝测试；证据：`tests/test_snapshot_branching.py`、`tests/test_runtime_manager.py`、`tests/test_gate_b_schemas.py`。
- [x] **M-MAC-006: 写 A800 night handoff**。已写 `refine-logs/A800_NIGHT_HANDOFF_MAC_SAFE_20260628.md`，覆盖 R018 deterministic restore、23DoF controller smoke、R011-R017 pilots 的输入、成功标准、停止条件和 morning acceptance 要求；不包含 SSH/IP/token/jump-host。
- [x] **M-MAC-007: 文档一致性维护**。已同步 `MANIFEST.md`、`refine-logs/EXPERIMENT_PLAN.md`、`refine-logs/DAILY_EXPERIMENT_TIMELINE.md`、`refine-logs/EXPERIMENT_TRACKER.md` 中的 Mac/A800 分工入口；所有新增可执行事项使用 checklist，未完成项保持 `- [ ]`。
- [x] **M-MAC-008: 后期文献与 citation audit**。已写 `refine-logs/CITATION_AUDIT_20260628.md`，核验高风险近邻的官方 arXiv/CVF source、title/authors/venue/source URL 和 claim 影响。边界：正式论文 BibTeX、最终 venue/DOI 和精读仍是 R071 后续工作。
- [x] **M-MAC-009: Controlled grounding + temporary object memory skeleton**。已实现 detector-like `ControlledGroundingRecord`、`ControlledGroundingAdapter`、`TemporaryObjectMemory` 和 runtime-legal snapshot payload；证据：`src/humanoid_locomotion_runtime/grounding_memory.py`、`tests/test_grounding_memory.py`。边界：不接真实 open-vocabulary detector，不产生感知实验指标。
- [x] **M-MAC-010: NavigatorV0 local planner skeleton**。已实现纯几何 `NavigatorV0`、`LocalObstacle`、`LocalRoute` 和 blocked-route `FailureEvent`；证据：`src/humanoid_locomotion_runtime/navigator.py`、`tests/test_navigator.py`。边界：不替代 MPC / controller-native path，也不证明 23DoF controller smoke。
- [x] **M-MAC-011: Dashboard/replay publisher skeleton**。已实现 in-memory `ViserDashboardPublisher`、`DashboardFrame`、`DashboardSummary` 和 dashboard high-level command surface；证据：`src/humanoid_locomotion_runtime/dashboard.py`、`tests/test_dashboard.py`。边界：不启动真实 Viser server，不控制 low-level joints。
- [x] **M-MAC-012: Run id naming + decision-flip analysis skeleton**。已实现 `format_run_id()`、`DecisionFlipRecord`、`extract_decision_flips()` 和 flip-rate helper；证据：`src/humanoid_locomotion_runtime/analysis.py`、`tests/test_analysis.py`。边界：R034 pilot decision-flip table 仍需 A800/EDP artifacts。
- [x] **M-MAC-013: R047a statistical-design draft**。已写 `refine-logs/STATISTICAL_DESIGN_FREEZE_20260628.md`，冻结 primary endpoint、seed source、cluster bootstrap、multiplicity 和 negative-control equivalence 草案。边界：R047 final 仍需 B1/B2 真实 pilot/baseline evidence。

## 可以在 Mac 做但不能当作 A800 证据

- [ ] 初始化 `third_party/mjlab` 用于阅读源码或轻量静态检查时，必须把结果标为 Mac local inspection，不得标为 A800 runtime smoke。
- [ ] 如果 Mac 本机安装了 MuJoCo 并能跑 raw asset compile，也只能作为 local convenience check；23DoF / 29DoF controller smoke 仍以 A800 或明确的实验主机结果为准。
- [ ] 如果在 Mac 上生成临时 outputs，只能写入 ignored 目录，并在提交前用 `git status --short` 确认没有 raw runs、logs、checkpoints、weights、datasets 进入 git。

## 必须留给 A800 或明确实验主机

- [ ] R018 deterministic simulator/runtime snapshot restore：Mac fake provider 不等于真实 restore smoke。
- [ ] R011-R014 failure pilots：需要真实 controller/backend 环境和 artifact pipeline。
- [ ] R015 severity calibration：需要真实 rollout 成功率区间，不能用 Mac 静态测试替代。
- [ ] R017 all pilot-family EDP validation：必须基于 pilot artifacts。
- [ ] R020-R027 baseline ladder：`controller_native`、`rule_recovery_tuned`、`instant_mlp`、`frame_stack_raw_history`、`GRU_raw_history`、`typed_event_body_memory` 都不在 Mac 上冒充实验结果。
- [ ] R030-R036 memory intervention diagnostics：snapshot branches 或 matched held-out 结果必须来自实验 pipeline。
- [ ] 23DoF `stand_ready` / `track_velocity` controller smoke：当前 route/contract 已锁，但 mature controller 仍 pending；Mac skeleton 不等于 target evidence。

## 当前推荐执行顺序

- [x] 先做 M-MAC-001，让 Mac 能跑 repo 锁定的 Python/uv。
- [x] 再做 M-MAC-002，确认纯 Python contract 面在 Mac 可复查。
- [x] 接着做 M-MAC-003 和 M-MAC-004，把 Gate C 的 backend-neutral interface 补齐。
- [x] 再补 M-MAC-009 到 M-MAC-012，把 grounding/memory、NavigatorV0、dashboard 和 analysis skeleton 补齐。
- [x] 最后做 M-MAC-006 和 M-MAC-013，把 A800 夜间可接手的 smoke/pilot handoff 与 R047a 统计设计草案写清楚。

## 2026-06-28 Mac 验证命令

- [x] `uv run pytest -q tests/test_snapshot_branching.py tests/test_runtime_manager.py tests/test_gate_b_schemas.py tests/test_recovery_options.py`，结果：`29 passed`。
- [x] `uv run ruff check src/humanoid_locomotion_runtime/snapshot_branching.py src/humanoid_locomotion_runtime/runtime_manager.py src/humanoid_locomotion_runtime/__init__.py tests/test_snapshot_branching.py tests/test_runtime_manager.py`，结果：`All checks passed!`。
- [x] `uv run ruff check .`，结果：`All checks passed!`。
- [x] `uv run pytest`，结果：`85 passed`。

## 禁止写法

- 不把 Mac 测试写成 `A800_SINGLE_HOST` 证据。
- 不把 `mjlab_g1_29dof_reference` 写成 `company_g1_edu_23dof` controller evidence。
- 不把 R018a metadata contract 或 Mac fake provider 写成 R018 deterministic restore。
- 不把 `NavigatorV0` 几何 skeleton 写成真实 MPC / controller-native route evidence。
- 不把 dashboard skeleton 或 decision-flip unit test 写成 replay artifact / pilot result。
- 不把未跑的 pilots、baselines、PPO、大规模 rollout 或论文主结论打勾。

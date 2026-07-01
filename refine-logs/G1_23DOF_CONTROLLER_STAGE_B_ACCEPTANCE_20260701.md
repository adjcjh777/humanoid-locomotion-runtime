# G1 23DoF Controller Stage B Acceptance

**日期**: 2026-07-01
**范围**: R007h / R007i, `Unitree-G1-23Dof-VelocityBalancedFlat`
**结论**: Stage B multi-seed training 和 command-grid eval 已完成；`model_9000.pt` 是当前 selected candidate；R007j project-local controller smoke 仍未完成。
**Curated evidence**: `refine-logs/G1_23DOF_CONTROLLER_STAGE_B_CURATED_EVIDENCE_20260701.md`

## Run Status

| Seed | GPU | Run name | Status | Key artifacts |
|---:|---:|---|---|---|
| 201 | 5 | `a800_g1_23dof_velocitybalanced_packedgpu5_seed201_4096env_10001iter_20260630T085517Z` | completed `Learning iteration 10000/10001`; final mean reward about `49.33`; `fell_over=0.0000` | ignored submodule logs: `model_10000.pt`, `policy.onnx` |
| 202 | 5 | `a800_g1_23dof_velocitybalanced_packedgpu5_seed202_4096env_10001iter_20260630T085517Z` | completed `Learning iteration 10000/10001`; final mean reward about `49.65`; `fell_over=0.0000` | ignored submodule logs: `model_10000.pt`, `policy.onnx` |
| 203 | 5 | `a800_g1_23dof_velocitybalanced_packedgpu5_seed203_4096env_10001iter_20260630T085517Z` | completed `Learning iteration 10000/10001`; final mean reward about `50.50`; `fell_over=0.0000` | ignored submodule logs: `model_10000.pt`, `policy.onnx` |

- [x] 三个 authoritative packed GPU 5 runs 均完成到 `Learning iteration 10000/10001`。
- [x] 三个 runs 均输出 `model_10000.pt` 和 `policy.onnx`，并保持在 ignored `third_party/unitree_rl_mjlab/logs/`。
- [x] `policy.onnx` shape 已验证为 `obs [1,80] -> actions [1,23]`。
- [x] 旧 GPU `1/2/3` early runs 只到 iteration 约 `783/10001`，已标记 superseded，不计入 mature evidence。
- [x] 本轮未观察到 OOM/NaN/Inf 作为失败证据。

## Eval Status

- [x] 旧 watcher `g1vb_pack_eval_after_train_20260630T085653Z` 因等待/时限问题没有形成最终验收结论。
- [x] 2026-07-01 已补跑 Stage B eval queue：`runs/unitree_g1_23dof_eval_queue/stage_b_eval_queue_20260701T012312Z.log`，结尾为 Stage B eval queue complete。
- [x] Eval 产物为 ignored `runs/unitree_g1_23dof_eval/*VelocityBalancedFlat*packedgpu5*seed*.json`，共 39 个 JSON，覆盖 13 个 checkpoints x 3 个 seeds。
- [x] 当前 selected candidate: seed `202` run 的 `model_9000.pt`。
- [x] 重要 run/log/checkpoint/ONNX 的路径、大小和 SHA256 已整理到 `refine-logs/G1_23DOF_CONTROLLER_STAGE_B_CURATED_EVIDENCE_20260701.md`；raw artifact 本体继续保持 ignored。

## Candidate Evidence

Stage B `model_9000.pt` 三 seed 聚合：

- [x] forward fast `done_fraction` max: `0.0`
- [x] forward fast mean forward displacement: about `9.184m`
- [x] forward fast mean abs lateral drift: about `0.203m`
- [x] forward fast max abs lateral drift across seeds: about `4.289m`
- [x] velocity error mean: about `0.116`
- [x] yaw error mean: about `0.080`
- [x] selection penalty mean: about `4.519`

Per-seed note:

- [x] seed `202` `model_9000.pt` is the current preferred play/smoke candidate: forward displacement about `9.327m`, mean abs lateral about `0.178m`, velocity error about `0.114`, yaw error about `0.072`, selection penalty about `4.371`.

## Viser Play Sanity

- [x] Direct play wrapper is available: `scripts/run_unitree_g1_23dof_play.sh`.
- [x] User observed `model_9000.pt` in Viser on 2026-07-01 and reported that the effect looked good and the straight-line walking part met the current visual requirement.
- [x] This is qualitative play sanity evidence for checkpoint selection.
- [ ] This is not yet project-local controller smoke evidence.

## Gate Decision

- [x] R007h Stage B multi-seed training: DONE.
- [x] R007i command-grid eval and selected checkpoint: DONE.
- [ ] R007j project-local controller smoke: TODO.
- [ ] Gate C mature controller evidence: pending until `stand_ready`, `safe_stop`, and `track_velocity` smoke pass for the selected 23DoF candidate.

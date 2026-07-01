# G1 23DoF Controller Stage B Curated Evidence

**日期**: 2026-07-01
**范围**: R007h / R007i, Stage B `Unitree-G1-23Dof-VelocityBalancedFlat`
**目的**: 筛选重要 run、log、checkpoint 和 ONNX artifact，并给出 GitHub 可提交的轻量证据。

## Publish Boundary

- [x] 本文件是 tracked curated evidence，可以提交到 GitHub。
- [x] raw training logs 仍保留在 ignored `runs/unitree_g1_23dof_training/`。
- [x] raw eval logs / JSON 仍保留在 ignored `runs/unitree_g1_23dof_eval_queue/` 和 `runs/unitree_g1_23dof_eval/`。
- [x] `.pt` checkpoint 和 `policy.onnx` 仍保留在 ignored `third_party/unitree_rl_mjlab/logs/`。
- [ ] 不把 raw logs、eval JSON、`.pt`、ONNX 或 TensorBoard/tfevents 本体提交到 GitHub。

## Selected Runs

| Seed | Run name | Training log | Size | SHA256 | Final training summary |
|---:|---|---|---:|---|---|
| 201 | `a800_g1_23dof_velocitybalanced_packedgpu5_seed201_4096env_10001iter_20260630T085517Z` | `runs/unitree_g1_23dof_training/a800_g1_23dof_velocitybalanced_packedgpu5_seed201_4096env_10001iter_20260630T085517Z.log` | 22M | `43ea4fda2c26d2b42abeb059e72267129d794ee02c3d007cfbd3caa095a9f1b0` | iteration `10000/10001`, mean reward `49.33`, mean episode length `1000.00`, `fell_over=0.0000` |
| 202 | `a800_g1_23dof_velocitybalanced_packedgpu5_seed202_4096env_10001iter_20260630T085517Z` | `runs/unitree_g1_23dof_training/a800_g1_23dof_velocitybalanced_packedgpu5_seed202_4096env_10001iter_20260630T085517Z.log` | 22M | `ae99047bfbac2e42e36e060bd5773df47e7dd57564196da2f54a5495018067ec` | iteration `10000/10001`, mean reward `49.65`, mean episode length `1000.00`, `fell_over=0.0000` |
| 203 | `a800_g1_23dof_velocitybalanced_packedgpu5_seed203_4096env_10001iter_20260630T085517Z` | `runs/unitree_g1_23dof_training/a800_g1_23dof_velocitybalanced_packedgpu5_seed203_4096env_10001iter_20260630T085517Z.log` | 22M | `9bb5461e5d6c69d8835dc2eb2e10d206a2a79e20effe4484f36794fc27591b1b` | iteration `10000/10001`, mean reward `50.50`, mean episode length `1000.00`, `fell_over=0.0000` |

Run-list artifact:

- [x] `runs/unitree_g1_23dof_training/STAGE_B_VELOCITY_BALANCED_PACKED_GPU5_RUNS_20260630T085517Z.txt`
- [x] Size: 4.0K
- [x] SHA256: `fa01cc8100e242f37f6543ed543b4a1dc9198c955294d2aec8c1230983ad5772`

## Selected Checkpoints

`model_9000.pt` is the current selected checkpoint family. Seed `202` is the preferred play/smoke candidate because it has the best per-seed selection penalty among `model_9000.pt` runs and passed user Viser straight-line sanity.

| Seed | Checkpoint | Size | SHA256 | Role |
|---:|---|---:|---|---|
| 201 | `third_party/unitree_rl_mjlab/logs/rsl_rl/g1_23dof_velocity_balanced/2026-06-30_08-55-30_a800_g1_23dof_velocitybalanced_packedgpu5_seed201_4096env_10001iter_20260630T085517Z/model_9000.pt` | 4.9M | `2a2df20e136998dbf805c80ce56aa6959f543d71d8333f652ffc4266127a9d88` | cross-seed candidate comparison |
| 202 | `third_party/unitree_rl_mjlab/logs/rsl_rl/g1_23dof_velocity_balanced/2026-06-30_08-55-30_a800_g1_23dof_velocitybalanced_packedgpu5_seed202_4096env_10001iter_20260630T085517Z/model_9000.pt` | 4.9M | `3e9c56e77916d4dc53205a8b9fc17d69dd60e6c52fd4c3bd11c9a0994730a158` | selected play/smoke candidate |
| 203 | `third_party/unitree_rl_mjlab/logs/rsl_rl/g1_23dof_velocity_balanced/2026-06-30_08-55-30_a800_g1_23dof_velocitybalanced_packedgpu5_seed203_4096env_10001iter_20260630T085517Z/model_9000.pt` | 4.9M | `6eb3d1f85bb6df56e05a198d430439511d4b9deac0382310d8aeb102c1296066` | cross-seed candidate comparison |

Final checkpoints kept for comparison only:

| Seed | Checkpoint | Size | SHA256 | Role |
|---:|---|---:|---|---|
| 201 | `...seed201_4096env_10001iter_20260630T085517Z/model_10000.pt` | 4.9M | `c178901425c7dd87381bd62d704836971a1efe8eba1e327ab11e9e0b4857a76e` | final-round comparison, not selected |
| 202 | `...seed202_4096env_10001iter_20260630T085517Z/model_10000.pt` | 4.9M | `f78310319c1fe655633249f03613a4648c29803d04bb93b3ddac3adbb744ef5e` | final-round comparison, not selected |
| 203 | `...seed203_4096env_10001iter_20260630T085517Z/model_10000.pt` | 4.9M | `f1fc716ee16ed9e4fd2b570045eaeada9a8712217bd033c5cf119326ef183f30` | final-round comparison, not selected |

## ONNX Shape Evidence

Final `policy.onnx` files are useful shape evidence, not the selected controller artifact for R007j.

| Seed | ONNX | Size | SHA256 | Shape |
|---:|---|---:|---|---|
| 201 | `...seed201_4096env_10001iter_20260630T085517Z/policy.onnx` | 820K | `2e11777d2fdd5a8a5f1af7bb02148f0fe6c43be44bea8f067b7adac4799edf5a` | `obs [1,80] -> actions [1,23]` |
| 202 | `...seed202_4096env_10001iter_20260630T085517Z/policy.onnx` | 820K | `e362f6776d9eff421c835325a71409265a17bffca596245e920579d53c1ca040` | `obs [1,80] -> actions [1,23]` |
| 203 | `...seed203_4096env_10001iter_20260630T085517Z/policy.onnx` | 820K | `98cec5b4a966c2bc1fd2a1d10e0ea1734c4e3a443b96343662718e5f322d4b9d` | `obs [1,80] -> actions [1,23]` |

## Eval Logs And JSON

| Artifact | Size | SHA256 | Role |
|---|---:|---|---|
| `runs/unitree_g1_23dof_eval_queue/stage_b_eval_queue_20260701T012312Z.log` | 12K | `16020ba6c6acd79f04e4dccde76f41d85b1316066ac9baab3c627c732d93dd44` | queue-level proof that Stage B eval rerun completed |
| `runs/unitree_g1_23dof_eval_queue/eval_model_9000_seed202_20260701T012312Z.log` | 72K | `d40fa72da91c03c21e293bf0c5cf2bfbec70e6ba80a6821b2963867d13ad60c2` | selected candidate eval log |
| `runs/unitree_g1_23dof_eval/Unitree-G1-23Dof-VelocityBalancedFlat_2026-06-30_08-55-30_a800_g1_23dof_velocitybalanced_packedgpu5_seed201_4096env_10001iter_20260630T085517Z_model_9000_seed201_20260701T014141Z.json` | 8.0K | `5e8673405add53ad58cf48749c814ef1483e08ed089a2c572c2e59074ac4e391` | `model_9000.pt` seed 201 metrics |
| `runs/unitree_g1_23dof_eval/Unitree-G1-23Dof-VelocityBalancedFlat_2026-06-30_08-55-30_a800_g1_23dof_velocitybalanced_packedgpu5_seed202_4096env_10001iter_20260630T085517Z_model_9000_seed202_20260701T014144Z.json` | 8.0K | `dff9585bcbdf6f1b70fa931cc8cb5fdf40cedd76710c8ad9115e042813807f8e` | selected candidate metrics |
| `runs/unitree_g1_23dof_eval/Unitree-G1-23Dof-VelocityBalancedFlat_2026-06-30_08-55-30_a800_g1_23dof_velocitybalanced_packedgpu5_seed203_4096env_10001iter_20260630T085517Z_model_9000_seed203_20260701T014142Z.json` | 8.0K | `10994e39c659873bf00493d9ed26ee9c56372c6be570487d68b0b3b6549c8ff8` | `model_9000.pt` seed 203 metrics |

## Eval Summary

Stage B checkpoint-level summary for seeds `201/202/203`:

| checkpoint | seed_count | forward_done_max | forward_fast_forward_m_mean | forward_fast_lateral_abs_mean | forward_fast_max_abs_lateral_m_max | forward_fast_vel_error_mean | forward_fast_yaw_error_mean | yaw_done_max | lateral_done_max | selection_penalty_mean |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `model_250` | 3 | 0.0000 | 0.9155 | 0.0493 | 0.9584 | 0.9097 | 0.1389 | 0.0000 | 0.0000 | 1.8007 |
| `model_9000` | 3 | 0.0000 | 9.1842 | 0.2027 | 4.2889 | 0.1159 | 0.0801 | 0.0000 | 0.0000 | 4.5192 |
| `model_4000` | 3 | 0.0000 | 9.2215 | 0.3723 | 5.0784 | 0.1226 | 0.0795 | 0.0000 | 0.0000 | 5.5192 |
| `model_9500` | 3 | 0.0000 | 9.3755 | 0.6463 | 5.1447 | 0.1208 | 0.0751 | 0.0000 | 0.0000 | 5.5782 |
| `model_10000` | 3 | 0.0000 | 9.2391 | 0.7048 | 4.9952 | 0.1197 | 0.0755 | 0.0000 | 0.0000 | 5.3087 |

`model_250.pt` has a low penalty because it barely moves forward, so it is not useful as a locomotion candidate. `model_9000.pt` is the best currently usable Stage B checkpoint because it keeps forward displacement near 9m with lower lateral drift and no done fraction in the command-grid eval.

Per-seed `model_9000.pt` summary:

| Seed | forward_done_max | forward_fast_forward_m | forward_fast_lateral_m | forward_fast_max_abs_lateral_m | forward_fast_vel_error | forward_fast_yaw_error | yaw_done_max | lateral_done_max | selection_penalty |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 202 | 0.0000 | 9.3268 | 0.1784 | 4.0061 | 0.1141 | 0.0722 | 0.0000 | 0.0000 | 4.3709 |
| 203 | 0.0000 | 9.1549 | 0.1254 | 4.0665 | 0.1130 | 0.0855 | 0.0000 | 0.0000 | 4.3903 |
| 201 | 0.0000 | 9.0707 | 0.3043 | 4.2889 | 0.1205 | 0.0827 | 0.0000 | 0.0000 | 4.7965 |

## Commands To Reproduce Selection

```bash
python scripts/summarize_unitree_g1_23dof_eval.py \
  --group-by checkpoint \
  --include-seeds 201,202,203 \
  --glob 'runs/unitree_g1_23dof_eval/*VelocityBalancedFlat*packedgpu5*20260701T*.json'

python scripts/summarize_unitree_g1_23dof_eval.py \
  --group-by seed \
  --include-seeds 201,202,203 \
  --glob 'runs/unitree_g1_23dof_eval/*VelocityBalancedFlat*packedgpu5*model_9000_seed*20260701T*.json'

RUN_NAME=a800_g1_23dof_velocitybalanced_packedgpu5_seed202_4096env_10001iter_20260630T085517Z \
CHECKPOINT=model_9000.pt \
GPU_ID=5 \
bash scripts/run_unitree_g1_23dof_play.sh
```

## Gate Decision

- [x] R007h: selected Stage B training runs are complete and indexed by hash.
- [x] R007i: selected Stage B eval logs / JSON / checkpoint hashes are indexed.
- [x] User Viser sanity: `model_9000.pt` seed `202` visually looked good and straight-line walking met the current visual requirement.
- [ ] R007j remains open: run project-local `stand_ready`, `safe_stop`, and `track_velocity` smoke before calling this mature `company_g1_edu_23dof` controller evidence.

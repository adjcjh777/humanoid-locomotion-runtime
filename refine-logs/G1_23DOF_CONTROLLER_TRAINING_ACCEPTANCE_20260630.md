# G1 23DoF Controller Training Acceptance

**日期**: 2026-06-30
**状态**: full-training candidate produced; play/controller smoke pending

## 白话结论

- [x] 已经完成一个正式规模的 `company_g1_edu_23dof` locomotion policy candidate 训练。
- [x] 这个结果证明当前 repo-local Unitree RL MJLab 训练入口可以完成 full run 并导出 candidate checkpoint / ONNX。
- [ ] 这还不能写成 mature controller evidence；必须先通过官方 play 回放和 project-local 23DoF controller smoke。

## Accepted Run

| 项 | 值 |
|----|----|
| Run name | `a800_g1_23dof_4096env_10001iter_20260629T100128Z` |
| Task | `Unitree-G1-23Dof-Flat` |
| Training repo | `third_party/unitree_rl_mjlab` |
| Submodule commit | `1425b15f73bd4095f0df53709d7c389c3eb9e790` |
| Mamba env | `robot` |
| Physical GPU | `4` |
| Effective device | `cuda:0` inside the training process |
| Seed | `42` |
| Num envs | `4096` |
| Max iterations | `10001` |
| Save interval | `500` |

## Evidence

- [x] Console log: ignored `runs/unitree_g1_23dof_training/a800_g1_23dof_4096env_10001iter_20260629T100128Z.log`.
- [x] Training output dir: ignored `third_party/unitree_rl_mjlab/logs/rsl_rl/g1_23dof_velocity/2026-06-29_10-01-43_a800_g1_23dof_4096env_10001iter_20260629T100128Z/`.
- [x] Params: `params/agent.yaml` records `max_iterations: 10001`, `save_interval: 500`, run name, and seed `42`; `params/env.yaml` records `num_envs: 4096`.
- [x] Candidate checkpoint: `model_10000.pt`.
- [x] Candidate ONNX export: `policy.onnx`.
- [x] Final logged metrics at iteration `10000/10001`: `Mean reward: 34.57`, `Mean episode length: 990.10`, `Episode_Termination/fell_over: 0.0833`.

## Gate Decision

- [x] Mark the training candidate as produced.
- [ ] Do not mark `company_g1_edu_23dof` mature controller evidence yet.
- [ ] Do not start R020 controller-native baseline, failure pilots, PPO supervisor, or paper claims from this candidate alone.
- [ ] Next required check: official `scripts/play.py Unitree-G1-23Dof-Flat --checkpoint_file=...` replay.
- [ ] After play passes, copy the selected candidate into ignored project `checkpoints/` and run project-local `stand_ready` / `track_velocity` 23DoF controller smoke.

## 2026-06-30 Follow-up

- [x] 由于 `model_4500.pt` 在 Viser 中出现斜走观察，后续不默认接受最终 checkpoint 或单一 play 观感。
- [x] 新增 policy-improvement TODO：`refine-logs/G1_23DOF_CONTROLLER_POLICY_IMPROVEMENT_TODO_20260630.md`。
- [x] 新增 repo-local task profiles：`Unitree-G1-23Dof-ForwardFlat` 和 `Unitree-G1-23Dof-VelocityBalancedFlat`。
- [x] 新增 command-grid eval 脚本，用固定 stand/forward/yaw/lateral commands 量化 lateral drift、yaw error、velocity error 和 done fraction。
- [ ] 重新评估旧 candidate 的 `model_3000.pt`、`model_4000.pt`、`model_4500.pt`、`model_10000.pt`。
- [ ] 启动 Stage A / Stage B multi-seed 训练后，再用 eval 选 checkpoint。

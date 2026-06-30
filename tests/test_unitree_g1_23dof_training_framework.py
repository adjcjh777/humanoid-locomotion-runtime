from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_unitree_training_submodule_is_repo_local() -> None:
  gitmodules = (ROOT / ".gitmodules").read_text(encoding="utf-8")

  assert "third_party/unitree_rl_mjlab" in gitmodules
  assert "unitreerobotics/unitree_rl_mjlab.git" in gitmodules
  assert "ignore = untracked" in gitmodules
  assert "/mnt/nvme2n1p1" not in gitmodules


def test_training_scripts_use_current_repo_paths() -> None:
  setup_script = (
    ROOT / "scripts" / "setup_unitree_g1_23dof_training.sh"
  ).read_text(encoding="utf-8")
  training_script = (
    ROOT / "scripts" / "run_unitree_g1_23dof_training.sh"
  ).read_text(encoding="utf-8")
  wrapper = (ROOT / "scripts" / "unitree_train_mamba_wrapper.py").read_text(
    encoding="utf-8"
  )

  combined = setup_script + training_script + wrapper
  assert "ROOT_DIR" in combined
  assert "third_party/unitree_rl_mjlab" in combined
  assert "Unitree-G1-23Dof-Flat" in combined
  assert "Unitree-G1-23Dof-VelocityBalancedFlat" in combined
  assert "UNITREE_RL_MJLAB_CONDA_ENV:-robot" in combined
  assert "mamba run -n" in setup_script
  assert "unitree_train_mamba_wrapper.py" in combined
  assert "register_unitree_g1_23dof_controller_profiles" in combined
  assert "sys.modules[spec.name] = module" in combined
  assert "PYTHONDONTWRITEBYTECODE" in combined
  assert "kwargs.pop(\"dynamo\", None)" in wrapper
  assert ".venvs" not in combined
  assert "uv venv" not in combined
  assert "NUM_ENVS=\"${NUM_ENVS:-4096}\"" in training_script
  assert "MAX_ITERATIONS=\"${MAX_ITERATIONS:-10001}\"" in training_script
  assert "SAVE_INTERVAL=\"${SAVE_INTERVAL:-250}\"" in training_script
  assert "SEED=\"${SEED:-42}\"" in training_script
  assert "--agent.seed=$SEED" in training_script
  assert "--agent.logger=tensorboard" in training_script
  assert "--agent.upload-model=False" in training_script
  assert "Training finished. Candidate training outputs under:" in training_script
  assert "/mnt/nvme2n1p1" not in combined


def test_training_framework_doc_preserves_gate_boundary() -> None:
  doc = (ROOT / "docs" / "g1_edu_23dof_training_framework.md").read_text(
    encoding="utf-8"
  )

  assert "train_23dof_required" in doc
  assert "80 -> 23" in doc
  assert "mamba env" in doc
  assert "不表示 Gate C controller smoke 已通过" in doc
  assert "checkpoint、ONNX、raw logs 不进 git" in doc


def test_repo_local_23dof_controller_profiles_are_tracked() -> None:
  profiles = (
    ROOT / "src" / "humanoid_locomotion_runtime" / "unitree_g1_23dof_profiles.py"
  ).read_text(encoding="utf-8")
  eval_script = (
    ROOT / "scripts" / "eval_unitree_g1_23dof_command_grid.py"
  ).read_text(encoding="utf-8")
  eval_queue = (
    ROOT / "scripts" / "run_unitree_g1_23dof_stage_b_eval_queue.sh"
  ).read_text(encoding="utf-8")
  summary_script = (
    ROOT / "scripts" / "summarize_unitree_g1_23dof_eval.py"
  ).read_text(encoding="utf-8")

  assert "Unitree-G1-23Dof-ForwardFlat" in profiles
  assert "Unitree-G1-23Dof-VelocityBalancedFlat" in profiles
  assert "heading_command = False" in profiles
  assert "VelocityCommandBin" in profiles
  assert "BinnedVelocityCommandCfg" in profiles
  assert "_set_binned_command_sampler" in profiles
  assert "command_axis_leakage_penalty" in profiles
  assert "command_axis_leakage" in profiles
  assert "straight_forward" in profiles
  assert "yaw_only" in profiles
  assert "lateral_only" in profiles
  assert "combined" in profiles
  assert "g1_23dof_forward_flat" in profiles
  assert "g1_23dof_velocity_balanced" in profiles
  assert "COMMAND_GRID" in eval_script
  assert "forward_mid" in eval_script
  assert "mean_lateral_displacement_m" in eval_script
  assert "done_fraction" in eval_script
  assert "seed{seed}" in eval_script
  assert "checkpoint.parent.name" in eval_script
  assert "checkpoint.stem" in eval_script
  assert "sys.modules[spec.name] = module" in eval_script
  assert "selection_penalty" in summary_script
  assert "forward_fast_max_abs_lateral_m" in summary_script
  assert "lateral_done_max" in summary_script
  assert "--group-by" in summary_script
  assert "--include-seeds" in summary_script
  assert "_aggregate_checkpoint" in summary_script
  assert "selection_penalty_max" in summary_script
  assert "START_AFTER_CHECKPOINT=\"${START_AFTER_CHECKPOINT:-model_10000.pt}\"" in eval_queue
  assert "WAIT_FOR_TMUX_SESSIONS" in eval_queue
  assert "wait_for_checkpoint_set \"$START_AFTER_CHECKPOINT\"" in eval_queue
  assert "wait_for_tmux_sessions" in eval_queue
  assert "CUDA_VISIBLE_DEVICES=\"$gpu\"" in eval_queue
  assert "--include-seeds \"$SEED_CSV\"" in eval_queue
  assert "runs/unitree_g1_23dof_eval_queue" in eval_queue

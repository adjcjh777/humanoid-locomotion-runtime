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
  assert "UNITREE_RL_MJLAB_CONDA_ENV:-robot" in combined
  assert "mamba run -n" in setup_script
  assert "unitree_train_mamba_wrapper.py" in combined
  assert "PYTHONDONTWRITEBYTECODE" in combined
  assert "kwargs.pop(\"dynamo\", None)" in wrapper
  assert ".venvs" not in combined
  assert "uv venv" not in combined
  assert "NUM_ENVS=\"${NUM_ENVS:-4096}\"" in training_script
  assert "MAX_ITERATIONS=\"${MAX_ITERATIONS:-10001}\"" in training_script
  assert "SAVE_INTERVAL=\"${SAVE_INTERVAL:-500}\"" in training_script
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

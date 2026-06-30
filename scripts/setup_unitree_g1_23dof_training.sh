#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TRAIN_REPO="${UNITREE_RL_MJLAB_ROOT:-$ROOT_DIR/third_party/unitree_rl_mjlab}"
CONDA_ENV_NAME="${UNITREE_RL_MJLAB_CONDA_ENV:-robot}"

if ! command -v mamba >/dev/null 2>&1; then
  echo "mamba is required. Install mamba first or add it to PATH." >&2
  exit 127
fi

if [ ! -f "$TRAIN_REPO/setup.py" ]; then
  git -C "$ROOT_DIR" submodule update --init --recursive third_party/unitree_rl_mjlab
fi

if [ ! -f "$TRAIN_REPO/setup.py" ]; then
  echo "Unitree RL MJLab submodule is missing at $TRAIN_REPO" >&2
  exit 2
fi

if ! conda env list | awk '{print $1}' | grep -qx "$CONDA_ENV_NAME"; then
  echo "Conda/mamba env '$CONDA_ENV_NAME' was not found." >&2
  echo "Set UNITREE_RL_MJLAB_CONDA_ENV=<existing-env> to reuse another env." >&2
  exit 2
fi

(
  cd "$TRAIN_REPO"
  export PYTHONDONTWRITEBYTECODE="${PYTHONDONTWRITEBYTECODE:-1}"
  PYTHONPATH="$TRAIN_REPO" mamba run -n "$CONDA_ENV_NAME" python - <<'PY'
import importlib
import sys

required = [
  "torch",
  "mujoco",
  "mjlab",
  "mujoco_warp",
  "warp",
  "rsl_rl",
  "tyro",
  "onnx",
  "wandb",
  "tensorboard",
]

print("python", sys.version.split()[0])
print("executable", sys.executable)
missing = []
for name in required:
  try:
    module = importlib.import_module(name)
    print(name, "OK", getattr(module, "__version__", "unknown"))
  except Exception as exc:  # pragma: no cover - shell diagnostic
    print(name, "FAIL", type(exc).__name__, str(exc)[:120])
    missing.append(name)

import torch

print("cuda", torch.cuda.is_available(), torch.cuda.device_count(), torch.version.cuda)

if missing:
  raise SystemExit(f"missing packages: {', '.join(missing)}")
PY
	  ROOT_DIR="$ROOT_DIR" PYTHONPATH="$TRAIN_REPO" mamba run -n "$CONDA_ENV_NAME" python - <<'PY'
import importlib.util
import os
import sys
from pathlib import Path

from mjlab.tasks.registry import list_tasks

root_dir = Path(os.environ["ROOT_DIR"])
profiles_path = root_dir / "src" / "humanoid_locomotion_runtime" / "unitree_g1_23dof_profiles.py"
spec = importlib.util.spec_from_file_location("unitree_g1_23dof_profiles_repo_local", profiles_path)
module = importlib.util.module_from_spec(spec)
assert spec is not None and spec.loader is not None
sys.modules[spec.name] = module
spec.loader.exec_module(module)
module.register_unitree_g1_23dof_controller_profiles()
for task_id in list_tasks():
  if "G1-23Dof" in task_id:
    print(task_id)
PY
)

cat <<EOF
Repo-local Unitree G1 23DoF training environment is ready.

Training repo:
  $TRAIN_REPO
Mamba env:
  $CONDA_ENV_NAME

Full training:
  bash scripts/run_unitree_g1_23dof_training.sh

Short sanity run, only when explicitly needed:
  NUM_ENVS=64 MAX_ITERATIONS=1 SAVE_INTERVAL=1 RUN_NAME=a800_g1_23dof_sanity_\$(date -u +%Y%m%dT%H%M%SZ) bash scripts/run_unitree_g1_23dof_training.sh
EOF

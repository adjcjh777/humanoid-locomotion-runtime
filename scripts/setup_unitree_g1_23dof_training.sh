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
  PYTHONPATH="$TRAIN_REPO" mamba run -n "$CONDA_ENV_NAME" python scripts/list_envs.py --keyword G1-23Dof
)

cat <<EOF
Repo-local Unitree G1 23DoF training environment is ready.

Training repo:
  $TRAIN_REPO
Mamba env:
  $CONDA_ENV_NAME

Tiny smoke:
  bash scripts/run_unitree_g1_23dof_training_smoke.sh

Full training example:
  cd $TRAIN_REPO
  PYTHONPATH=$TRAIN_REPO CUDA_VISIBLE_DEVICES=4 MUJOCO_GL=egl mamba run -n $CONDA_ENV_NAME python $ROOT_DIR/scripts/unitree_train_mamba_wrapper.py Unitree-G1-23Dof-Flat --env.scene.num-envs=4096 --agent.logger=tensorboard --agent.upload-model=False
EOF

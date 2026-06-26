#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MJLAB_PROJECT="$ROOT_DIR/third_party/mjlab"
MJLAB_PYTHON="${MJLAB_PYTHON:-$ROOT_DIR/.venv/bin/python3}"

if [[ ! -x "$MJLAB_PYTHON" ]]; then
  echo "Missing MJLab Python interpreter: $MJLAB_PYTHON" >&2
  echo "Run 'uv sync --locked' in the repository root first." >&2
  exit 1
fi

uv --project "$MJLAB_PROJECT" lock --check --python "$MJLAB_PYTHON"
uv --project "$MJLAB_PROJECT" sync --locked --extra cu128 --no-dev --python "$MJLAB_PYTHON"

uv --project "$MJLAB_PROJECT" run --extra cu128 --no-dev --python "$MJLAB_PYTHON" python - <<'PY'
import sys

import mjlab
import mujoco
import mujoco_warp
import rsl_rl
import torch
import tyro
import warp as wp

print("python", sys.version.split()[0])
print("executable", sys.executable)
print(
  "torch",
  torch.__version__,
  "cuda_available",
  torch.cuda.is_available(),
  "cuda_device_count",
  torch.cuda.device_count(),
)
print("mujoco", mujoco.__version__)
print("warp", getattr(wp.config, "version", "unknown"))
print("mujoco_warp", getattr(mujoco_warp, "__version__", "unknown"))
print("mjlab", getattr(mjlab, "__version__", "unknown"))
print("rsl_rl", getattr(rsl_rl, "__version__", "unknown"))
print("tyro", tyro.__version__)
print("mjlab_import_ok")
PY

uv --project "$MJLAB_PROJECT" run --extra cu128 --no-dev --python "$MJLAB_PYTHON" \
  python "$ROOT_DIR/scripts/mjlab_g1_smoke.py" --num-envs 1 --steps 16 --seed 1234

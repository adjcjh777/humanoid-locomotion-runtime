#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TRAIN_REPO="${UNITREE_RL_MJLAB_ROOT:-$ROOT_DIR/third_party/unitree_rl_mjlab}"
CONDA_ENV_NAME="${UNITREE_RL_MJLAB_CONDA_ENV:-robot}"

TASK="${TASK:-Unitree-G1-23Dof-Flat}"
PHYSICAL_GPU_ID="${PHYSICAL_GPU_ID:-${GPU_ID:-4}}"
NUM_ENVS="${NUM_ENVS:-64}"
MAX_ITERATIONS="${MAX_ITERATIONS:-1}"
SAVE_INTERVAL="${SAVE_INTERVAL:-1}"
RUN_NAME="${RUN_NAME:-a800_g1_23dof_smoke_$(date -u +%Y%m%dT%H%M%SZ)}"
LOG_DIR="$ROOT_DIR/runs/unitree_g1_23dof_training"
LOG_FILE="$LOG_DIR/${RUN_NAME}.log"

if ! command -v mamba >/dev/null 2>&1; then
  echo "mamba is required. Install mamba first or add it to PATH." >&2
  exit 127
fi

if ! conda env list | awk '{print $1}' | grep -qx "$CONDA_ENV_NAME"; then
  echo "Conda/mamba env '$CONDA_ENV_NAME' was not found." >&2
  echo "Run: UNITREE_RL_MJLAB_CONDA_ENV=<existing-env> bash scripts/setup_unitree_g1_23dof_training.sh" >&2
  exit 2
fi

if [ ! -f "$TRAIN_REPO/scripts/train.py" ]; then
  echo "Missing Unitree training repo: $TRAIN_REPO" >&2
  echo "Run: git submodule update --init --recursive third_party/unitree_rl_mjlab" >&2
  exit 2
fi

mkdir -p "$LOG_DIR"
export CUDA_VISIBLE_DEVICES="$PHYSICAL_GPU_ID"
export MUJOCO_GL="${MUJOCO_GL:-egl}"
export PYTHONDONTWRITEBYTECODE="${PYTHONDONTWRITEBYTECODE:-1}"

CMD=(
  mamba
  run
  -n
  "$CONDA_ENV_NAME"
  python
  "$ROOT_DIR/scripts/unitree_train_mamba_wrapper.py"
  "$TASK"
  "--env.scene.num-envs=$NUM_ENVS"
  "--agent.max-iterations=$MAX_ITERATIONS"
  "--agent.save-interval=$SAVE_INTERVAL"
  "--agent.run-name=$RUN_NAME"
  --agent.logger=tensorboard
  --agent.upload-model=False
)

{
  echo "task=$TASK"
  echo "physical_gpu_id=$PHYSICAL_GPU_ID"
  echo "num_envs=$NUM_ENVS"
  echo "max_iterations=$MAX_ITERATIONS"
  echo "train_repo=$TRAIN_REPO"
  echo "conda_env=$CONDA_ENV_NAME"
  echo "log_file=$LOG_FILE"
  printf 'command='
  printf '%q ' "${CMD[@]}"
  printf '\n'
} | tee "$LOG_FILE"

(
  cd "$TRAIN_REPO"
  export PYTHONPATH="$TRAIN_REPO"
  "${CMD[@]}" 2>&1 | tee -a "$LOG_FILE"
)

echo "Smoke finished. Candidate training outputs under:" | tee -a "$LOG_FILE"
find "$TRAIN_REPO/logs/rsl_rl/g1_23dof_velocity" \
  -maxdepth 1 \
  -type d \
  -name "*$RUN_NAME" \
  -exec find {} \
    -maxdepth 2 \
    -type f \
    \( -name 'model_*.pt' -o -name 'policy.onnx' -o -name 'env.yaml' -o -name 'agent.yaml' \) \
    -print \; \
  2>/dev/null | sort | tee -a "$LOG_FILE"

#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TRAIN_REPO="${UNITREE_RL_MJLAB_ROOT:-$ROOT_DIR/third_party/unitree_rl_mjlab}"
CONDA_ENV_NAME="${UNITREE_RL_MJLAB_CONDA_ENV:-robot}"

TASK="${TASK:-Unitree-G1-23Dof-VelocityBalancedFlat}"
EXPERIMENT_NAME="${EXPERIMENT_NAME:-g1_23dof_velocity_balanced}"
RUN_NAME="${RUN_NAME:-}"
CHECKPOINT="${CHECKPOINT:-model_9000.pt}"
CHECKPOINT_FILE="${CHECKPOINT_FILE:-}"
PHYSICAL_GPU_ID="${PHYSICAL_GPU_ID:-${GPU_ID:-5}}"
NUM_ENVS="${NUM_ENVS:-1}"
DEVICE="${DEVICE:-cuda:0}"
VIEWER="${VIEWER:-viser}"

if ! command -v mamba >/dev/null 2>&1; then
  echo "mamba is required. Install mamba first or add it to PATH." >&2
  exit 127
fi

if ! conda env list | awk '{print $1}' | grep -qx "$CONDA_ENV_NAME"; then
  echo "Conda/mamba env '$CONDA_ENV_NAME' was not found." >&2
  echo "Run: UNITREE_RL_MJLAB_CONDA_ENV=<existing-env> bash scripts/setup_unitree_g1_23dof_training.sh" >&2
  exit 2
fi

if [ ! -f "$TRAIN_REPO/scripts/play.py" ]; then
  echo "Missing Unitree training repo: $TRAIN_REPO" >&2
  echo "Run: git submodule update --init --recursive third_party/unitree_rl_mjlab" >&2
  exit 2
fi

if [ -z "$CHECKPOINT_FILE" ]; then
  if [ -z "$RUN_NAME" ]; then
    echo "Either CHECKPOINT_FILE or RUN_NAME is required." >&2
    echo "Example: RUN_NAME=... CHECKPOINT=model_9000.pt GPU_ID=5 bash scripts/run_unitree_g1_23dof_play.sh" >&2
    exit 2
  fi
  CHECKPOINT_FILE="$(
    find "$TRAIN_REPO/logs/rsl_rl/$EXPERIMENT_NAME" \
      -maxdepth 2 \
      -type f \
      -path "*${RUN_NAME}/${CHECKPOINT}" \
      -print \
      -quit 2>/dev/null
  )"
fi

if [ -z "$CHECKPOINT_FILE" ] || [ ! -f "$CHECKPOINT_FILE" ]; then
  echo "Checkpoint not found." >&2
  echo "  experiment_name=$EXPERIMENT_NAME" >&2
  echo "  run_name=$RUN_NAME" >&2
  echo "  checkpoint=$CHECKPOINT" >&2
  echo "  checkpoint_file=$CHECKPOINT_FILE" >&2
  exit 2
fi

export CUDA_VISIBLE_DEVICES="$PHYSICAL_GPU_ID"
export MUJOCO_GL="${MUJOCO_GL:-egl}"
export PYTHONDONTWRITEBYTECODE="${PYTHONDONTWRITEBYTECODE:-1}"

CMD=(
  mamba
  run
  -n
  "$CONDA_ENV_NAME"
  python
  "$ROOT_DIR/scripts/unitree_play_mamba_wrapper.py"
  "$TASK"
  "--checkpoint_file=$CHECKPOINT_FILE"
  "--num_envs=$NUM_ENVS"
  "--device=$DEVICE"
  "--viewer=$VIEWER"
)

echo "task=$TASK"
echo "physical_gpu_id=$PHYSICAL_GPU_ID"
echo "num_envs=$NUM_ENVS"
echo "device=$DEVICE"
echo "viewer=$VIEWER"
echo "checkpoint_file=$CHECKPOINT_FILE"
echo "When Viser starts, open http://localhost:8080 or forward it with: ssh -L 8080:localhost:8080 <host>"
printf 'command='
printf '%q ' "${CMD[@]}"
printf '\n'

exec "${CMD[@]}"

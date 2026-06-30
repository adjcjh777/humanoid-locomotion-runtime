#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TRAIN_REPO="${UNITREE_RL_MJLAB_ROOT:-$ROOT_DIR/third_party/unitree_rl_mjlab}"
CONDA_ENV_NAME="${UNITREE_RL_MJLAB_CONDA_ENV:-robot}"

TASK="${TASK:-Unitree-G1-23Dof-VelocityBalancedFlat}"
EXPERIMENT_NAME="${EXPERIMENT_NAME:-g1_23dof_velocity_balanced}"
RUN_NAMES="${RUN_NAMES:-}"
SEEDS="${SEEDS:-201 202 203}"
GPUS="${GPUS:-1 2 3}"
CHECKPOINTS="${CHECKPOINTS:-model_250.pt model_500.pt model_1000.pt model_2000.pt model_3000.pt model_4000.pt model_5000.pt model_6000.pt model_7000.pt model_8000.pt model_9000.pt model_9500.pt model_10000.pt}"
START_AFTER_CHECKPOINT="${START_AFTER_CHECKPOINT:-model_10000.pt}"
WAIT_FOR_TMUX_SESSIONS="${WAIT_FOR_TMUX_SESSIONS:-}"
MAX_WAIT_SECONDS="${MAX_WAIT_SECONDS:-43200}"
POLL_SECONDS="${POLL_SECONDS:-300}"
NUM_ENVS="${NUM_ENVS:-64}"
STEPS="${STEPS:-500}"
STAMP="${STAMP:-$(date -u +%Y%m%dT%H%M%SZ)}"
LOG_DIR="$ROOT_DIR/runs/unitree_g1_23dof_eval_queue"
LOG_FILE="$LOG_DIR/stage_b_eval_queue_${STAMP}.log"

if [ -z "$RUN_NAMES" ]; then
  echo "RUN_NAMES is required and must contain one run name per seed." >&2
  exit 2
fi

read -r -a RUN_NAME_ARRAY <<< "$RUN_NAMES"
read -r -a SEED_ARRAY <<< "$SEEDS"
read -r -a GPU_ARRAY <<< "$GPUS"
read -r -a CHECKPOINT_ARRAY <<< "$CHECKPOINTS"

if [ "${#RUN_NAME_ARRAY[@]}" -ne "${#SEED_ARRAY[@]}" ]; then
  echo "RUN_NAMES count must match SEEDS count." >&2
  exit 2
fi

if [ "${#RUN_NAME_ARRAY[@]}" -ne "${#GPU_ARRAY[@]}" ]; then
  echo "RUN_NAMES count must match GPUS count." >&2
  exit 2
fi

mkdir -p "$LOG_DIR"

log() {
  printf '[%s] %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$*" | tee -a "$LOG_FILE"
}

find_checkpoint() {
  local run_name="$1"
  local checkpoint="$2"
  find "$TRAIN_REPO/logs/rsl_rl/$EXPERIMENT_NAME" \
    -maxdepth 2 \
    -type f \
    -path "*${run_name}/${checkpoint}" \
    -print \
    -quit 2>/dev/null
}

wait_for_checkpoint_set() {
  local checkpoint="$1"
  local start
  start="$(date +%s)"
  while true; do
    local missing=0
    for run_name in "${RUN_NAME_ARRAY[@]}"; do
      if [ -z "$(find_checkpoint "$run_name" "$checkpoint")" ]; then
        missing=1
        break
      fi
    done
    if [ "$missing" -eq 0 ]; then
      log "all runs have $checkpoint"
      return 0
    fi
    local now
    now="$(date +%s)"
    if [ $((now - start)) -gt "$MAX_WAIT_SECONDS" ]; then
      log "timeout waiting for $checkpoint"
      return 1
    fi
    log "waiting for $checkpoint; next check in ${POLL_SECONDS}s"
    sleep "$POLL_SECONDS"
  done
}

wait_for_tmux_sessions() {
  if [ -z "$WAIT_FOR_TMUX_SESSIONS" ]; then
    return 0
  fi
  read -r -a SESSION_ARRAY <<< "$WAIT_FOR_TMUX_SESSIONS"
  while true; do
    local active=0
    for session in "${SESSION_ARRAY[@]}"; do
      if tmux has-session -t "$session" 2>/dev/null; then
        active=1
        break
      fi
    done
    if [ "$active" -eq 0 ]; then
      log "training tmux sessions have ended"
      return 0
    fi
    log "waiting for training tmux sessions to end; next check in ${POLL_SECONDS}s"
    sleep "$POLL_SECONDS"
  done
}

run_eval_batch() {
  local checkpoint="$1"
  local pids=()
  local names=()
  for i in "${!RUN_NAME_ARRAY[@]}"; do
    local run_name="${RUN_NAME_ARRAY[$i]}"
    local seed="${SEED_ARRAY[$i]}"
    local gpu="${GPU_ARRAY[$i]}"
    local checkpoint_file
    checkpoint_file="$(find_checkpoint "$run_name" "$checkpoint")"
    if [ -z "$checkpoint_file" ]; then
      log "missing $checkpoint for $run_name; skipping batch"
      return 1
    fi
    local eval_log="$LOG_DIR/eval_${checkpoint%.pt}_seed${seed}_${STAMP}.log"
    log "starting eval checkpoint=$checkpoint seed=$seed gpu=$gpu"
    (
      cd "$ROOT_DIR"
      export CUDA_VISIBLE_DEVICES="$gpu"
      export MUJOCO_GL="${MUJOCO_GL:-egl}"
      mamba run -n "$CONDA_ENV_NAME" python scripts/eval_unitree_g1_23dof_command_grid.py \
        "$TASK" \
        --checkpoint-file "$checkpoint_file" \
        --num-envs "$NUM_ENVS" \
        --steps "$STEPS" \
        --device cuda:0 \
        --seed "$seed"
    ) >"$eval_log" 2>&1 &
    pids+=("$!")
    names+=("$checkpoint seed=$seed")
  done

  local failed=0
  for i in "${!pids[@]}"; do
    if ! wait "${pids[$i]}"; then
      log "eval failed for ${names[$i]}"
      failed=1
    fi
  done
  if [ "$failed" -ne 0 ]; then
    return 1
  fi
  log "eval batch complete for $checkpoint"
}

SEED_CSV="$(IFS=,; echo "${SEED_ARRAY[*]}")"

log "Stage B eval queue started"
log "task=$TASK experiment=$EXPERIMENT_NAME seeds=$SEEDS gpus=$GPUS checkpoints=$CHECKPOINTS"
wait_for_checkpoint_set "$START_AFTER_CHECKPOINT"
wait_for_tmux_sessions

for checkpoint in "${CHECKPOINT_ARRAY[@]}"; do
  wait_for_checkpoint_set "$checkpoint"
  run_eval_batch "$checkpoint"
  (
    cd "$ROOT_DIR"
    mamba run -n "$CONDA_ENV_NAME" python scripts/summarize_unitree_g1_23dof_eval.py \
      --group-by checkpoint \
      --include-seeds "$SEED_CSV" \
      --glob "runs/unitree_g1_23dof_eval/*${checkpoint%.pt}_seed*.json"
  ) | tee -a "$LOG_FILE"
done

log "Stage B eval queue complete"

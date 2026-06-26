#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST_DIR="$ROOT_DIR/checkpoints/unitree_rl_mjlab_g1_velocity_v0"

POLICY_URL="https://raw.githubusercontent.com/unitreerobotics/unitree_rl_mjlab/1425b15f73bd4095f0df53709d7c389c3eb9e790/deploy/robots/g1/config/policy/velocity/v0/exported/policy.onnx"
PARAMS_URL="https://raw.githubusercontent.com/unitreerobotics/unitree_rl_mjlab/1425b15f73bd4095f0df53709d7c389c3eb9e790/deploy/robots/g1/config/policy/velocity/v0/params/deploy.yaml"

POLICY_SHA256="2a66ca6336eadb3c0b34b557763f3e06d01ff8fcf6260dd4cedbd69d6093fc28"
PARAMS_SHA256="01e1cf3f6ec44e9942494fbb4a9904df07201e14e5551a277f38d7c7d1bda28d"

mkdir -p "$DEST_DIR"
curl -L --fail --silent --show-error -o "$DEST_DIR/policy.onnx" "$POLICY_URL"
curl -L --fail --silent --show-error -o "$DEST_DIR/deploy.yaml" "$PARAMS_URL"

printf '%s  %s\n' "$POLICY_SHA256" "$DEST_DIR/policy.onnx" | sha256sum --check -
printf '%s  %s\n' "$PARAMS_SHA256" "$DEST_DIR/deploy.yaml" | sha256sum --check -

echo "Fetched Unitree RL MJLab G1 velocity controller candidate into $DEST_DIR"

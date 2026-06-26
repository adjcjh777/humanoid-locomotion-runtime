#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "$SCRIPT_DIR/.." && pwd)"

DEST_DIR="${UNITREE_G1_23DOF_DESCRIPTION_DIR:-$REPO_ROOT/robot_descriptions/unitree_g1_23dof_rev_1_0}"

SOURCE_REPO="https://github.com/unitreerobotics/unitree_rl_gym"
SOURCE_COMMIT="276801e46c5d433564f24658bac64f254b7d2d4b"
SOURCE_DIR="resources/robots/g1_description"
RAW_BASE_URL="https://raw.githubusercontent.com/unitreerobotics/unitree_rl_gym/276801e46c5d433564f24658bac64f254b7d2d4b/resources/robots/g1_description"

URDF_FILE="g1_23dof_rev_1_0.urdf"
MJCF_FILE="g1_23dof_rev_1_0.xml"
URDF_URL="$RAW_BASE_URL/$URDF_FILE"
MJCF_URL="$RAW_BASE_URL/$MJCF_FILE"
URDF_SHA256="cffe6149e0b29abed10b8c6a7e318003676ae4234224044e4af30946599d1ba9"
MJCF_SHA256="8ca62fcccdca91a431ca04f1a42f9c2fda241fdd5e13411168dc82de00f978de"

TMP_FILES=()

cleanup() {
  if ((${#TMP_FILES[@]})); then
    rm -f -- "${TMP_FILES[@]}"
  fi
}
trap cleanup EXIT

warn() {
  printf 'WARNING: %s\n' "$*" >&2
}

require_cmd() {
  local cmd="$1"
  if ! command -v "$cmd" >/dev/null 2>&1; then
    printf 'ERROR: required command not found: %s\n' "$cmd" >&2
    exit 127
  fi
}

warn "This fetches the official Unitree G1 edu 23DoF robot description only; it is not a controller checkpoint."

require_cmd curl
require_cmd sha256sum

mkdir -p -- "$DEST_DIR"

if command -v git >/dev/null 2>&1 && git -C "$REPO_ROOT" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  case "$DEST_DIR" in
    "$REPO_ROOT"/*)
      rel_dest="${DEST_DIR#"$REPO_ROOT"/}"
      if ! git -C "$REPO_ROOT" check-ignore -q -- "$rel_dest/" "$rel_dest/$URDF_FILE" "$rel_dest/$MJCF_FILE"; then
        warn "Destination $rel_dest is not currently matched by .gitignore; keep downloaded robot descriptions out of git."
      fi
      ;;
  esac
fi

fetch_and_verify() {
  local url="$1"
  local expected_sha256="$2"
  local output_path="$3"
  local tmp_path

  tmp_path="$(mktemp "$DEST_DIR/.fetch.$(basename "$output_path").XXXXXX")"
  TMP_FILES+=("$tmp_path")

  printf 'Fetching %s\n' "$url"
  curl -L --fail --silent --show-error -o "$tmp_path" "$url"

  if ! printf '%s  %s\n' "$expected_sha256" "$tmp_path" | sha256sum --check --status -; then
    printf 'ERROR: SHA256 mismatch for %s\n' "$url" >&2
    printf 'ERROR: expected %s\n' "$expected_sha256" >&2
    exit 1
  fi

  mv -f -- "$tmp_path" "$output_path"
  printf 'Verified %s\n' "$output_path"
}

fetch_and_verify "$URDF_URL" "$URDF_SHA256" "$DEST_DIR/$URDF_FILE"
fetch_and_verify "$MJCF_URL" "$MJCF_SHA256" "$DEST_DIR/$MJCF_FILE"

printf 'Fetched Unitree G1 edu 23DoF official robot description from %s@%s into %s\n' \
  "$SOURCE_REPO" "$SOURCE_COMMIT" "$DEST_DIR"

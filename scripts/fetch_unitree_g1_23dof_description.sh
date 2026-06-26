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

MESH_ASSETS=(
  "005fb67fbd3eff94aa8bf4a6e83238174e9f91b6721f7111594322f223724411 head_link.STL"
  "d49e3abc6f5b12e532062cd575b87b5ef40cd2a3fc18f54a1ca5bba4f773d51d left_ankle_pitch_link.STL"
  "c4092af943141d4d9f74232f3cfa345afc6565f46a077793b8ae0e68b39dc33f left_ankle_roll_link.STL"
  "fa752198accd104d5c4c3a01382e45165b944fbbc5acce085059223324e5bed3 left_elbow_link.STL"
  "4725168105ee768ee31638ef22b53f6be2d7641bfd7cfefe803488d884776fa4 left_hip_pitch_link.STL"
  "91f25922ee8a7c3152790051bebad17b4d9cd243569c38fe340285ff93a97acf left_hip_roll_link.STL"
  "a16d88aa6ddac8083aa7ad55ed317bea44b1fa003d314fba88965b7ed0f3b55b left_hip_yaw_link.STL"
  "8d92b9e3d3a636761150bb8025e32514c4602b91c7028d523ee42b3e632de477 left_knee_link.STL"
  "f0d1cfd02fcf0d42f95e678eeca33da3afbcc366ffba5c052847773ec4f31d52 left_shoulder_pitch_link.STL"
  "fb9df21687773522598dc384f1a2945c7519f11cbc8bd372a49170316d6eee88 left_shoulder_roll_link.STL"
  "1aa97e9748e924336567992181f78c7cd0652fd52a4afcca3df6b2ef6f9e712e left_shoulder_yaw_link.STL"
  "e81030abd023bd9e4a308ef376d814a2c12d684d8a7670c335bbd5cd7809c909 left_wrist_roll_rubber_hand.STL"
  "8571a0a19bc4916fa55f91449f51d5fdefd751000054865a842449429d5f155b logo_link.STL"
  "5ba6bbc888e630550140d3c26763f10206da8c8bd30ed886b8ede41c61f57a31 pelvis.STL"
  "5cc5c2c7a312329e3feeb2b03d3fc09fc29705bd01864f6767e51be959662420 pelvis_contour_link.STL"
  "15be426539ec1be70246d4d82a168806db64a41301af8b35c197a33348c787a9 right_ankle_pitch_link.STL"
  "4b66222ea56653e627711b56d0a8949b4920da5df091da0ceb343f54e884e3a5 right_ankle_roll_link.STL"
  "1be925d7aa268bb8fddf5362b9173066890c7d32092c05638608126e59d1e2ab right_elbow_link.STL"
  "e4f3c99d7f4a7d34eadbef9461fc66e3486cb5442db1ec50c86317d459f1a9c6 right_hip_pitch_link.STL"
  "4c254ef66a356f492947f360dd931965477b631e3fcc841f91ccc46d945d54f6 right_hip_roll_link.STL"
  "e479c2936ca2057e9eb2f7dff6c189b7419d7b8484dea0b298cbb36a2a6aa668 right_hip_yaw_link.STL"
  "63c4008449c9bbe701a6e2b557b7a252e90cf3a5abcf54cee46862b9a69f8ec8 right_knee_link.STL"
  "24cdb387e0128dfe602770a81c56cdce3a0181d34d039a11d1aaf8819b7b8c02 right_shoulder_pitch_link.STL"
  "962b97c48f9ce9e8399f45dd9522e0865d19aa9fd299406b2d475a8fc4a53e81 right_shoulder_roll_link.STL"
  "a0b76489271da0c72461a344c9ffb0f0c6e64f019ea5014c1624886c442a2fe5 right_shoulder_yaw_link.STL"
  "0729aff1ac4356f9314de13a46906267642e58bc47f0d8a7f17f6590a6242ccf right_wrist_roll_rubber_hand.STL"
  "3cd0d56fde14b73c1623304684805029971c4f84b596f9914e823ca70a107fd2 torso_link_23dof_rev_1_0.STL"
)

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

is_ignored_by_git() {
  local path="$1"
  git -C "$REPO_ROOT" check-ignore -q -- "$path"
}

require_cmd() {
  local cmd="$1"
  if ! command -v "$cmd" >/dev/null 2>&1; then
    printf 'ERROR: required command not found: %s\n' "$cmd" >&2
    exit 127
  fi
}

warn "This fetches the official Unitree G1 edu 23DoF robot description and mesh assets only; it is not a controller checkpoint."

require_cmd curl
require_cmd sha256sum

mkdir -p -- "$DEST_DIR"
mkdir -p -- "$DEST_DIR/meshes"

if command -v git >/dev/null 2>&1 && git -C "$REPO_ROOT" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  case "$DEST_DIR" in
    "$REPO_ROOT"/*)
      rel_dest="${DEST_DIR#"$REPO_ROOT"/}"
      if ! is_ignored_by_git "$rel_dest/" \
        || ! is_ignored_by_git "$rel_dest/$URDF_FILE" \
        || ! is_ignored_by_git "$rel_dest/$MJCF_FILE" \
        || ! is_ignored_by_git "$rel_dest/meshes/"; then
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

for mesh_asset in "${MESH_ASSETS[@]}"; do
  mesh_sha256="${mesh_asset%% *}"
  mesh_file="${mesh_asset#* }"
  fetch_and_verify \
    "$RAW_BASE_URL/meshes/$mesh_file" \
    "$mesh_sha256" \
    "$DEST_DIR/meshes/$mesh_file"
done

printf 'Fetched Unitree G1 edu 23DoF official robot description and %s mesh assets from %s@%s into %s\n' \
  "${#MESH_ASSETS[@]}" \
  "$SOURCE_REPO" "$SOURCE_COMMIT" "$DEST_DIR"

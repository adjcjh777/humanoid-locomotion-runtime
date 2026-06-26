#!/usr/bin/env python3
"""Headless MJLab Unitree G1 smoke test.

Run with the project-local MJLab environment, for example:

  uv --project third_party/mjlab run --extra cu128 --no-dev \
    --python .venv/bin/python3 python scripts/mjlab_g1_smoke.py
"""

from __future__ import annotations

import argparse
import json
import time
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any

DEFAULT_ROBOT_PROFILE = "mjlab_g1_29dof_reference"
DEFAULT_EXPECTED_ACTION_DIM = 29
DEFAULT_EXPECTED_ACTOR_OBS_DIM = 99
DEFAULT_EXPECTED_CRITIC_OBS_DIM = 111
PROFILE_REQUIRED_ACTION_DIMS = {
  DEFAULT_ROBOT_PROFILE: DEFAULT_EXPECTED_ACTION_DIM,
  "company_g1_edu_23dof": 23,
}


class DimensionGateError(RuntimeError):
  """Raised when the smoke result does not match the requested robot profile."""


@dataclass(frozen=True)
class SmokeDimensions:
  action_shape: tuple[int, ...]
  actor_obs_shape: tuple[int, ...]
  critic_obs_shape: tuple[int, ...]

  @property
  def action_dim(self) -> int:
    return _last_dim(self.action_shape, "action")

  @property
  def actor_obs_dim(self) -> int:
    return _last_dim(self.actor_obs_shape, "actor observation")

  @property
  def critic_obs_dim(self) -> int:
    return _last_dim(self.critic_obs_shape, "critic observation")


def _torch_module() -> Any:
  import torch

  return torch


def _shape_tuple(value: Any, label: str) -> tuple[int, ...]:
  shape = getattr(value, "shape", None)
  if shape is None and isinstance(value, Sequence) and not isinstance(value, str):
    shape = value
  if shape is None:
    raise ValueError(f"{label} does not expose a shape")
  try:
    shape_tuple = tuple(int(dim) for dim in shape)
  except (TypeError, ValueError) as exc:
    raise ValueError(f"{label} has an invalid shape: {shape!r}") from exc
  if not shape_tuple:
    raise ValueError(f"{label} shape is empty")
  return shape_tuple


def _last_dim(shape: tuple[int, ...], label: str) -> int:
  if not shape:
    raise ValueError(f"{label} shape is empty")
  return shape[-1]


def extract_smoke_dimensions(
  action_shape: tuple[int, ...],
  obs: Mapping[str, Any],
) -> SmokeDimensions:
  """Extract action/actor/critic dimensions without depending on MJLab imports."""
  missing_groups = [group for group in ("actor", "critic") if group not in obs]
  if missing_groups:
    available = ", ".join(sorted(str(group) for group in obs)) or "<none>"
    missing = ", ".join(missing_groups)
    raise ValueError(
      f"Missing required observation group(s): {missing}; available groups: {available}"
    )

  return SmokeDimensions(
    action_shape=_shape_tuple(action_shape, "action"),
    actor_obs_shape=_shape_tuple(obs["actor"], "actor observation"),
    critic_obs_shape=_shape_tuple(obs["critic"], "critic observation"),
  )


def validate_profile_dimensions(
  *,
  robot_profile: str,
  dimensions: SmokeDimensions,
  expected_action_dim: int,
  expected_actor_obs_dim: int,
  expected_critic_obs_dim: int,
) -> None:
  checks = (
    ("action_dim", expected_action_dim, dimensions.action_dim, dimensions.action_shape),
    (
      "actor_obs_dim",
      expected_actor_obs_dim,
      dimensions.actor_obs_dim,
      dimensions.actor_obs_shape,
    ),
    (
      "critic_obs_dim",
      expected_critic_obs_dim,
      dimensions.critic_obs_dim,
      dimensions.critic_obs_shape,
    ),
  )
  mismatches = [
    f"{name}: expected {expected}, got {actual} (shape={list(shape)})"
    for name, expected, actual, shape in checks
    if expected != actual
  ]
  if mismatches:
    mismatch_text = "; ".join(mismatches)
    raise DimensionGateError(
      "MJLab G1 smoke profile/dimension gate failed for "
      f"robot_profile={robot_profile!r}: {mismatch_text}"
    )


def validate_robot_profile_request(
  *,
  robot_profile: str,
  expected_action_dim: int,
) -> None:
  required_action_dim = PROFILE_REQUIRED_ACTION_DIMS.get(robot_profile)
  if required_action_dim is None:
    return
  if expected_action_dim != required_action_dim:
    raise DimensionGateError(
      f"robot_profile={robot_profile!r} requires expected_action_dim="
      f"{required_action_dim}, got {expected_action_dim}. Use "
      f"robot_profile={DEFAULT_ROBOT_PROFILE!r} for the current MJLab 29DoF "
      "reference smoke."
    )


def dimension_gate_summary(
  *,
  robot_profile: str,
  dimensions: SmokeDimensions,
  expected_action_dim: int,
  expected_actor_obs_dim: int,
  expected_critic_obs_dim: int,
) -> dict[str, Any]:
  return {
    "robot_profile": robot_profile,
    "expected": {
      "action_dim": expected_action_dim,
      "actor_obs_dim": expected_actor_obs_dim,
      "critic_obs_dim": expected_critic_obs_dim,
    },
    "actual": {
      "action_dim": dimensions.action_dim,
      "actor_obs_dim": dimensions.actor_obs_dim,
      "critic_obs_dim": dimensions.critic_obs_dim,
      "action_shape": list(dimensions.action_shape),
      "actor_obs_shape": list(dimensions.actor_obs_shape),
      "critic_obs_shape": list(dimensions.critic_obs_shape),
    },
  }


def build_arg_parser() -> argparse.ArgumentParser:
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument("--task", default="Mjlab-Velocity-Flat-Unitree-G1")
  parser.add_argument("--num-envs", type=int, default=1)
  parser.add_argument("--steps", type=int, default=16)
  parser.add_argument("--seed", type=int, default=1234)
  parser.add_argument("--device", default=None)
  parser.add_argument("--robot-profile", default=DEFAULT_ROBOT_PROFILE)
  parser.add_argument("--expected-action-dim", type=int, default=DEFAULT_EXPECTED_ACTION_DIM)
  parser.add_argument(
    "--expected-actor-obs-dim",
    type=int,
    default=DEFAULT_EXPECTED_ACTOR_OBS_DIM,
  )
  parser.add_argument(
    "--expected-critic-obs-dim",
    type=int,
    default=DEFAULT_EXPECTED_CRITIC_OBS_DIM,
  )
  return parser


def _tensor_summary(value: Any) -> Any:
  torch = _torch_module()
  if isinstance(value, torch.Tensor):
    return {
      "shape": list(value.shape),
      "dtype": str(value.dtype),
      "device": str(value.device),
      "finite": bool(torch.isfinite(value).all().item())
      if value.is_floating_point()
      else True,
    }
  if isinstance(value, Mapping):
    return {str(k): _tensor_summary(v) for k, v in value.items()}
  return str(type(value))


def _all_finite(value: Any) -> bool:
  torch = _torch_module()
  if isinstance(value, torch.Tensor):
    return bool(torch.isfinite(value).all().item()) if value.is_floating_point() else True
  if isinstance(value, Mapping):
    return all(_all_finite(v) for v in value.values())
  return True


def main() -> None:
  parser = build_arg_parser()
  args = parser.parse_args()

  try:
    validate_robot_profile_request(
      robot_profile=args.robot_profile,
      expected_action_dim=args.expected_action_dim,
    )
  except DimensionGateError as exc:
    raise SystemExit(str(exc)) from exc

  torch = _torch_module()

  import mjlab.tasks  # noqa: F401  # Registers bundled tasks.
  import mujoco
  import mujoco_warp
  import warp as wp
  from mjlab.envs import ManagerBasedRlEnv
  from mjlab.tasks.registry import list_tasks, load_env_cfg

  if args.task not in list_tasks():
    raise SystemExit(f"Task not registered: {args.task}")

  device = args.device or ("cuda:0" if torch.cuda.is_available() else "cpu")
  cfg = load_env_cfg(args.task, play=True)
  cfg.scene.num_envs = args.num_envs
  cfg.seed = args.seed

  started = time.time()
  env = ManagerBasedRlEnv(cfg=cfg, device=device, render_mode=None)
  try:
    obs, _extras = env.reset(seed=args.seed)
    action_shape = tuple(env.action_space.shape)
    dimensions = extract_smoke_dimensions(action_shape, obs)
    try:
      validate_profile_dimensions(
        robot_profile=args.robot_profile,
        dimensions=dimensions,
        expected_action_dim=args.expected_action_dim,
        expected_actor_obs_dim=args.expected_actor_obs_dim,
        expected_critic_obs_dim=args.expected_critic_obs_dim,
      )
    except DimensionGateError as exc:
      raise SystemExit(str(exc)) from exc
    action = torch.zeros(action_shape, device=env.device)

    reward = torch.zeros(args.num_envs, device=env.device)
    terminated = torch.zeros(args.num_envs, dtype=torch.bool, device=env.device)
    timeout = torch.zeros(args.num_envs, dtype=torch.bool, device=env.device)
    for _ in range(args.steps):
      obs, reward, terminated, timeout, _extras = env.step(action)
      if not _all_finite(obs) or not _all_finite(reward):
        raise RuntimeError("Non-finite observation or reward detected during smoke")

    summary = {
      "status": "pass",
      "task": args.task,
      "robot_profile": args.robot_profile,
      "num_envs": args.num_envs,
      "steps": args.steps,
      "seed": args.seed,
      "device": str(env.device),
      "torch": torch.__version__,
      "torch_cuda_available": torch.cuda.is_available(),
      "mujoco": mujoco.__version__,
      "mujoco_warp": getattr(mujoco_warp, "__version__", "unknown"),
      "warp": getattr(wp.config, "version", "unknown"),
      "physics_dt": env.physics_dt,
      "step_dt": env.step_dt,
      "action_shape": list(action_shape),
      "single_action_shape": list(env.single_action_space.shape),
      "observation": _tensor_summary(obs),
      "profile_dimension_gate": dimension_gate_summary(
        robot_profile=args.robot_profile,
        dimensions=dimensions,
        expected_action_dim=args.expected_action_dim,
        expected_actor_obs_dim=args.expected_actor_obs_dim,
        expected_critic_obs_dim=args.expected_critic_obs_dim,
      ),
      "reward_mean": float(reward.float().mean().item()),
      "terminated_count": int(terminated.sum().item()),
      "timeout_count": int(timeout.sum().item()),
      "elapsed_s": round(time.time() - started, 3),
    }
  finally:
    env.close()

  print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
  main()

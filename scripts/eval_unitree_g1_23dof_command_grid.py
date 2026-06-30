#!/usr/bin/env python
"""Evaluate a Unitree G1 23DoF locomotion checkpoint on a small command grid."""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import sys
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

import torch

COMMAND_GRID: dict[str, tuple[float, float, float]] = {
    "stand": (0.0, 0.0, 0.0),
    "forward_slow": (0.35, 0.0, 0.0),
    "forward_mid": (0.70, 0.0, 0.0),
    "forward_fast": (1.00, 0.0, 0.0),
    "yaw_left": (0.0, 0.0, 0.35),
    "yaw_right": (0.0, 0.0, -0.35),
    "lateral_left": (0.0, 0.20, 0.0),
    "lateral_right": (0.0, -0.20, 0.0),
}


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "task",
        nargs="?",
        default="Unitree-G1-23Dof-VelocityBalancedFlat",
    )
    parser.add_argument("--checkpoint-file", required=True)
    parser.add_argument("--num-envs", type=int, default=64)
    parser.add_argument("--steps", type=int, default=500)
    parser.add_argument("--device", default=None)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output-dir", default="runs/unitree_g1_23dof_eval")
    return parser.parse_args()


def _prepare_imports(root_dir: Path, train_repo: Path) -> None:
    sys.path.insert(0, str(root_dir / "src"))
    sys.path.insert(0, str(train_repo))


def _lock_command(env_cfg, command: tuple[float, float, float]) -> None:
    twist_cmd = env_cfg.commands["twist"]
    twist_cmd.heading_command = False
    twist_cmd.rel_heading_envs = 0.0
    twist_cmd.rel_standing_envs = 1.0 if command == (0.0, 0.0, 0.0) else 0.0
    twist_cmd.resampling_time_range = (1.0e9, 1.0e9)
    twist_cmd.ranges.lin_vel_x = (command[0], command[0])
    twist_cmd.ranges.lin_vel_y = (command[1], command[1])
    twist_cmd.ranges.ang_vel_z = (command[2], command[2])
    twist_cmd.ranges.heading = None
    if hasattr(twist_cmd, "command_bins") and twist_cmd.command_bins:
        command_bin_cls = type(twist_cmd.command_bins[0])
        twist_cmd.command_bins = (
            command_bin_cls(
                "locked_eval",
                1.0,
                (command[0], command[0]),
                (command[1], command[1]),
                (command[2], command[2]),
            ),
        )
    if "reset_base" in env_cfg.events:
        pose_range = env_cfg.events["reset_base"].params["pose_range"]
        pose_range["x"] = (0.0, 0.0)
        pose_range["y"] = (0.0, 0.0)
        pose_range["yaw"] = (0.0, 0.0)


def _load_repo_local_profiles(root_dir: Path) -> None:
    profiles_path = (
        root_dir
        / "src"
        / "humanoid_locomotion_runtime"
        / "unitree_g1_23dof_profiles.py"
    )
    spec = importlib.util.spec_from_file_location(
        "unitree_g1_23dof_profiles_repo_local", profiles_path
    )
    if spec is None or spec.loader is None:
        raise ImportError(f"could not load repo-local profiles from {profiles_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    module.register_unitree_g1_23dof_controller_profiles()


def _safe_filename_part(value: str) -> str:
    return "".join(char if char.isalnum() or char in {"-", "_"} else "_" for char in value)


def _output_path(output_dir: Path, *, task: str, checkpoint_file: str, seed: int) -> Path:
    checkpoint = Path(checkpoint_file).resolve()
    stamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    filename = "_".join(
        [
            _safe_filename_part(task),
            _safe_filename_part(checkpoint.parent.name),
            _safe_filename_part(checkpoint.stem),
            f"seed{seed}",
            stamp,
        ]
    )
    return output_dir / f"{filename}.json"


def _evaluate_command(
    args: argparse.Namespace,
    command_name: str,
    command: tuple[float, float, float],
) -> dict:
    from mjlab.envs import ManagerBasedRlEnv
    from mjlab.rl import MjlabOnPolicyRunner, RslRlVecEnvWrapper
    from mjlab.tasks.registry import load_env_cfg, load_rl_cfg, load_runner_cls
    from mjlab.utils.torch import configure_torch_backends

    configure_torch_backends()
    device = args.device or ("cuda:0" if torch.cuda.is_available() else "cpu")
    env_cfg = load_env_cfg(args.task, play=True)
    agent_cfg = load_rl_cfg(args.task)
    env_cfg.seed = args.seed
    env_cfg.scene.num_envs = args.num_envs
    step_dt = env_cfg.sim.mujoco.timestep * env_cfg.decimation
    env_cfg.episode_length_s = max(env_cfg.episode_length_s, args.steps * step_dt)
    _lock_command(env_cfg, command)

    raw_env = ManagerBasedRlEnv(cfg=env_cfg, device=device, render_mode=None)
    env = RslRlVecEnvWrapper(raw_env, clip_actions=agent_cfg.clip_actions)
    runner_cls = load_runner_cls(args.task) or MjlabOnPolicyRunner
    runner = runner_cls(env, asdict(agent_cfg), device=device)
    runner.load(
        str(Path(args.checkpoint_file)),
        load_cfg={"actor": True},
        strict=True,
        map_location=device,
    )
    policy = runner.get_inference_policy(device=device)

    obs = env.get_observations()
    robot = env.unwrapped.scene["robot"]
    start_pos = robot.data.root_link_pos_w[:, :2].clone()
    rewards = []
    done_count = torch.zeros(args.num_envs, device=device)
    vel_error_xy = []
    yaw_error = []

    command_tensor = torch.tensor(command, device=device)
    for _ in range(args.steps):
        with torch.inference_mode():
            actions = policy(obs)
        obs, reward, dones, _extras = env.step(actions)
        rewards.append(reward.detach())
        done_count += dones.to(device=device, dtype=torch.float32)
        actual_lin = robot.data.root_link_lin_vel_b[:, :2]
        actual_yaw = robot.data.root_link_ang_vel_b[:, 2]
        vel_error_xy.append(torch.norm(actual_lin - command_tensor[:2], dim=-1))
        yaw_error.append(torch.abs(actual_yaw - command_tensor[2]))

    final_pos = robot.data.root_link_pos_w[:, :2].clone()
    displacement = final_pos - start_pos
    env.close()

    reward_t = torch.stack(rewards)
    vel_error_t = torch.stack(vel_error_xy)
    yaw_error_t = torch.stack(yaw_error)
    return {
        "command_name": command_name,
        "command": list(command),
        "num_envs": args.num_envs,
        "steps": args.steps,
        "mean_reward": float(reward_t.mean().item()),
        "mean_vel_xy_error": float(vel_error_t.mean().item()),
        "mean_yaw_error": float(yaw_error_t.mean().item()),
        "mean_forward_displacement_m": float(displacement[:, 0].mean().item()),
        "mean_lateral_displacement_m": float(displacement[:, 1].mean().item()),
        "max_abs_lateral_displacement_m": float(displacement[:, 1].abs().max().item()),
        "done_fraction": float((done_count > 0).float().mean().item()),
    }


def main() -> None:
    args = _parse_args()
    root_dir = Path(__file__).resolve().parents[1]
    train_repo = Path(
        os.environ.get(
            "UNITREE_RL_MJLAB_ROOT",
            root_dir / "third_party" / "unitree_rl_mjlab",
        )
    ).resolve()
    _prepare_imports(root_dir, train_repo)
    _load_repo_local_profiles(root_dir)

    results = [_evaluate_command(args, name, command) for name, command in COMMAND_GRID.items()]
    output_dir = root_dir / args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = _output_path(
        output_dir,
        task=args.task,
        checkpoint_file=args.checkpoint_file,
        seed=args.seed,
    )
    payload = {
        "task": args.task,
        "checkpoint_file": str(Path(args.checkpoint_file).resolve()),
        "seed": args.seed,
        "results": results,
    }
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))
    print(f"wrote {output_path}")


if __name__ == "__main__":
    main()

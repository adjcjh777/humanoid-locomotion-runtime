"""Repo-local Unitree G1 23DoF controller training profiles.

The upstream Unitree RL MJLab checkout is a git submodule.  These profiles keep
the experiment choices in this repository while registering additional MJLab
tasks at runtime.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

FORWARD_FLAT_TASK_ID = "Unitree-G1-23Dof-ForwardFlat"
VELOCITY_BALANCED_FLAT_TASK_ID = "Unitree-G1-23Dof-VelocityBalancedFlat"


@dataclass(frozen=True)
class VelocityCommandBin:
    name: str
    weight: float
    lin_vel_x: tuple[float, float]
    lin_vel_y: tuple[float, float]
    ang_vel_z: tuple[float, float]


@dataclass(kw_only=True)
class BinnedVelocityCommandCfg:
    entity_name: str
    resampling_time_range: tuple[float, float]
    ranges: Any
    command_bins: tuple[VelocityCommandBin, ...]
    heading_command: bool = False
    heading_control_stiffness: float = 1.0
    rel_standing_envs: float = 0.0
    rel_heading_envs: float = 0.0
    init_velocity_prob: float = 0.0
    debug_vis: bool = True
    viz: Any = None

    def build(self, env: Any) -> Any:
        import torch
        from mjlab.utils.lab_api.math import quat_apply
        from src.tasks.velocity.mdp.velocity_command import UniformVelocityCommand

        cfg = self

        class BinnedVelocityCommand(UniformVelocityCommand):
            def _resample_command(self, env_ids: Any) -> None:
                if not cfg.command_bins:
                    super()._resample_command(env_ids)
                    return

                weights = torch.tensor(
                    [command_bin.weight for command_bin in cfg.command_bins],
                    device=self.device,
                    dtype=torch.float32,
                )
                weights = weights / weights.sum()
                sampled_bins = torch.multinomial(
                    weights, len(env_ids), replacement=True
                )
                self.vel_command_b[env_ids, :] = 0.0
                self.is_heading_env[env_ids] = False
                self.is_standing_env[env_ids] = False

                for bin_index, command_bin in enumerate(cfg.command_bins):
                    selected = env_ids[sampled_bins == bin_index]
                    if len(selected) == 0:
                        continue
                    random_values = torch.empty(len(selected), device=self.device)
                    self.vel_command_b[selected, 0] = random_values.uniform_(
                        *command_bin.lin_vel_x
                    )
                    self.vel_command_b[selected, 1] = random_values.uniform_(
                        *command_bin.lin_vel_y
                    )
                    self.vel_command_b[selected, 2] = random_values.uniform_(
                        *command_bin.ang_vel_z
                    )
                    if command_bin.name == "stand":
                        self.is_standing_env[selected] = True

                init_mask = (
                    torch.empty(len(env_ids), device=self.device).uniform_(0.0, 1.0)
                    < cfg.init_velocity_prob
                )
                init_env_ids = env_ids[init_mask]
                if len(init_env_ids) > 0:
                    root_pos = self.robot.data.root_link_pos_w[init_env_ids]
                    root_quat = self.robot.data.root_link_quat_w[init_env_ids]
                    lin_vel_b = self.robot.data.root_link_lin_vel_b[init_env_ids]
                    lin_vel_b[:, :2] = self.vel_command_b[init_env_ids, :2]
                    root_lin_vel_w = quat_apply(root_quat, lin_vel_b)
                    root_ang_vel_b = self.robot.data.root_link_ang_vel_b[init_env_ids]
                    root_ang_vel_b[:, 2] = self.vel_command_b[init_env_ids, 2]
                    root_state = torch.cat(
                        [root_pos, root_quat, root_lin_vel_w, root_ang_vel_b],
                        dim=-1,
                    )
                    self.robot.write_root_state_to_sim(root_state, init_env_ids)

        return BinnedVelocityCommand(self, env)


def command_axis_leakage_penalty(
    env: Any,
    *,
    command_name: str,
    command_threshold: float = 0.05,
) -> Any:
    """Penalize motion on velocity axes that were commanded to stay quiet."""
    import torch

    command = env.command_manager.get_command(command_name)
    assert command is not None, f"Command '{command_name}' not found."
    robot = env.scene["robot"]
    actual = torch.cat(
        (
            robot.data.root_link_lin_vel_b[:, :2],
            robot.data.root_link_ang_vel_b[:, 2:3],
        ),
        dim=1,
    )
    moving_command = torch.linalg.norm(command[:, :3], dim=1) > command_threshold
    quiet_axes = torch.abs(command[:, :3]) <= command_threshold
    leakage = torch.square(actual) * quiet_axes.to(dtype=actual.dtype)
    return leakage.sum(dim=1) * moving_command.to(dtype=actual.dtype)


def _set_twist_direct_velocity(
    cfg: Any,
    *,
    lin_vel_x: tuple[float, float],
    lin_vel_y: tuple[float, float],
    ang_vel_z: tuple[float, float],
    rel_standing_envs: float,
    resampling_time_range: tuple[float, float] = (3.0, 8.0),
) -> None:
    twist_cmd = cfg.commands["twist"]
    twist_cmd.heading_command = False
    twist_cmd.rel_heading_envs = 0.0
    twist_cmd.rel_standing_envs = rel_standing_envs
    twist_cmd.resampling_time_range = resampling_time_range
    twist_cmd.ranges.lin_vel_x = lin_vel_x
    twist_cmd.ranges.lin_vel_y = lin_vel_y
    twist_cmd.ranges.ang_vel_z = ang_vel_z
    twist_cmd.ranges.heading = None


def _set_command_curriculum(cfg: Any, velocity_stages: list[dict[str, Any]]) -> None:
    if "command_vel" not in cfg.curriculum:
        return
    cfg.curriculum["command_vel"].params["velocity_stages"] = velocity_stages


def _set_binned_command_sampler(
    cfg: Any,
    command_bins: tuple[VelocityCommandBin, ...],
) -> None:
    twist_cmd = cfg.commands["twist"]
    cfg.commands["twist"] = BinnedVelocityCommandCfg(
        entity_name=twist_cmd.entity_name,
        resampling_time_range=twist_cmd.resampling_time_range,
        ranges=twist_cmd.ranges,
        command_bins=command_bins,
        heading_command=False,
        heading_control_stiffness=twist_cmd.heading_control_stiffness,
        rel_standing_envs=0.0,
        rel_heading_envs=0.0,
        init_velocity_prob=twist_cmd.init_velocity_prob,
        debug_vis=twist_cmd.debug_vis,
        viz=twist_cmd.viz,
    )


def _tune_stability_rewards(cfg: Any, *, straight: bool) -> None:
    rewards = cfg.rewards
    if "track_linear_velocity" in rewards:
        rewards["track_linear_velocity"].weight = 1.5 if straight else 1.2
    if "track_angular_velocity" in rewards:
        rewards["track_angular_velocity"].weight = 1.25 if straight else 1.1
    if "pose" in rewards:
        rewards["pose"].weight = 1.2 if straight else 1.1
    if "body_orientation_l2" in rewards:
        rewards["body_orientation_l2"].weight = -1.25 if straight else -1.15
    if "body_ang_vel" in rewards:
        rewards["body_ang_vel"].weight = -0.08 if straight else -0.06
    if "angular_momentum" in rewards:
        rewards["angular_momentum"].weight = -0.04 if straight else -0.035
    if "foot_slip" in rewards:
        rewards["foot_slip"].weight = -0.35 if straight else -0.30
    if "action_rate_l2" in rewards:
        rewards["action_rate_l2"].weight = -0.07 if straight else -0.06


def _add_axis_leakage_reward(cfg: Any, *, straight: bool) -> None:
    from mjlab.managers.reward_manager import RewardTermCfg

    cfg.rewards["command_axis_leakage"] = RewardTermCfg(
        func=command_axis_leakage_penalty,
        weight=-0.25 if straight else -0.15,
        params={"command_name": "twist", "command_threshold": 0.05},
    )


def _make_forward_flat_env_cfg(*, play: bool) -> Any:
    from src.tasks.velocity.config.g1_23dof.env_cfgs import (
        unitree_g1_23dof_flat_env_cfg,
    )

    cfg = unitree_g1_23dof_flat_env_cfg(play=play)
    _set_twist_direct_velocity(
        cfg,
        lin_vel_x=(0.0, 1.0) if play else (0.2, 0.9),
        lin_vel_y=(0.0, 0.0),
        ang_vel_z=(0.0, 0.0),
        rel_standing_envs=0.10,
        resampling_time_range=(3.0, 6.0),
    )
    _set_command_curriculum(
        cfg,
        [
            {
                "step": 0,
                "lin_vel_x": (0.2, 0.9),
                "lin_vel_y": (0.0, 0.0),
                "ang_vel_z": (0.0, 0.0),
            },
            {
                "step": 2500 * 24,
                "lin_vel_x": (0.2, 1.1),
                "lin_vel_y": (0.0, 0.0),
                "ang_vel_z": (0.0, 0.0),
            },
        ],
    )
    _set_binned_command_sampler(
        cfg,
        (
            VelocityCommandBin("stand", 0.10, (0.0, 0.0), (0.0, 0.0), (0.0, 0.0)),
            VelocityCommandBin("straight_slow", 0.35, (0.2, 0.6), (0.0, 0.0), (0.0, 0.0)),
            VelocityCommandBin("straight_mid", 0.35, (0.6, 0.9), (0.0, 0.0), (0.0, 0.0)),
            VelocityCommandBin("straight_fast", 0.20, (0.9, 1.1), (0.0, 0.0), (0.0, 0.0)),
        ),
    )
    _tune_stability_rewards(cfg, straight=True)
    _add_axis_leakage_reward(cfg, straight=True)
    return cfg


def _make_velocity_balanced_flat_env_cfg(*, play: bool) -> Any:
    from src.tasks.velocity.config.g1_23dof.env_cfgs import (
        unitree_g1_23dof_flat_env_cfg,
    )

    cfg = unitree_g1_23dof_flat_env_cfg(play=play)
    _set_twist_direct_velocity(
        cfg,
        lin_vel_x=(-0.4, 1.2) if play else (-0.2, 0.8),
        lin_vel_y=(-0.25, 0.25) if play else (-0.15, 0.15),
        ang_vel_z=(-0.4, 0.4) if play else (-0.3, 0.3),
        rel_standing_envs=0.08,
        resampling_time_range=(3.0, 8.0),
    )
    _set_command_curriculum(
        cfg,
        [
            {
                "step": 0,
                "lin_vel_x": (-0.2, 0.8),
                "lin_vel_y": (-0.15, 0.15),
                "ang_vel_z": (-0.3, 0.3),
            },
            {
                "step": 3000 * 24,
                "lin_vel_x": (-0.4, 1.2),
                "lin_vel_y": (-0.3, 0.3),
                "ang_vel_z": (-0.5, 0.5),
            },
            {
                "step": 7000 * 24,
                "lin_vel_x": (-0.6, 1.5),
                "lin_vel_y": (-0.5, 0.5),
                "ang_vel_z": (-0.8, 0.8),
            },
        ],
    )
    _set_binned_command_sampler(
        cfg,
        (
            VelocityCommandBin("stand", 0.08, (0.0, 0.0), (0.0, 0.0), (0.0, 0.0)),
            VelocityCommandBin("straight_forward", 0.34, (0.2, 1.0), (0.0, 0.0), (0.0, 0.0)),
            VelocityCommandBin("yaw_only", 0.18, (0.0, 0.0), (0.0, 0.0), (-0.4, 0.4)),
            VelocityCommandBin("lateral_only", 0.14, (0.0, 0.0), (-0.25, 0.25), (0.0, 0.0)),
            VelocityCommandBin("combined", 0.26, (-0.2, 1.0), (-0.25, 0.25), (-0.4, 0.4)),
        ),
    )
    _tune_stability_rewards(cfg, straight=False)
    _add_axis_leakage_reward(cfg, straight=False)
    return cfg


def _make_rl_cfg(*, experiment_name: str) -> Any:
    from src.tasks.velocity.config.g1_23dof.rl_cfg import (
        unitree_g1_23dof_ppo_runner_cfg,
    )

    cfg = unitree_g1_23dof_ppo_runner_cfg()
    cfg.experiment_name = experiment_name
    cfg.save_interval = 250
    return cfg


def register_unitree_g1_23dof_controller_profiles() -> None:
    """Register repo-local 23DoF controller improvement tasks with MJLab."""
    import mjlab.tasks  # noqa: F401
    import src.tasks  # noqa: F401
    from mjlab.tasks.registry import list_tasks, register_mjlab_task
    from src.tasks.velocity.rl import VelocityOnPolicyRunner

    registered = set(list_tasks())

    if FORWARD_FLAT_TASK_ID not in registered:
        register_mjlab_task(
            task_id=FORWARD_FLAT_TASK_ID,
            env_cfg=_make_forward_flat_env_cfg(play=False),
            play_env_cfg=_make_forward_flat_env_cfg(play=True),
            rl_cfg=_make_rl_cfg(experiment_name="g1_23dof_forward_flat"),
            runner_cls=VelocityOnPolicyRunner,
        )

    if VELOCITY_BALANCED_FLAT_TASK_ID not in registered:
        register_mjlab_task(
            task_id=VELOCITY_BALANCED_FLAT_TASK_ID,
            env_cfg=_make_velocity_balanced_flat_env_cfg(play=False),
            play_env_cfg=_make_velocity_balanced_flat_env_cfg(play=True),
            rl_cfg=_make_rl_cfg(experiment_name="g1_23dof_velocity_balanced"),
            runner_cls=VelocityOnPolicyRunner,
        )

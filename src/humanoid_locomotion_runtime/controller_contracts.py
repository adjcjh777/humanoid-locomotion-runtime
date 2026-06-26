"""Controller/profile contracts for the G1 gate sequence.

The contracts here are intentionally lightweight and importable without MuJoCo,
MJLab, Torch, or ONNX. They capture the R007e decision boundary: the company
23DoF target has a locked shape contract, while the currently downloaded 29DoF
ONNX remains reference-only until a separate 23DoF controller exists.
"""

from __future__ import annotations

import hashlib
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Literal

RobotProfileId = Literal["company_g1_edu_23dof", "mjlab_g1_29dof_reference"]
ControllerRoute = Literal[
    "train_23dof_required",
    "convert_29dof_experimental_only",
    "reference_29dof_only",
]

COMPANY_G1_23DOF_JOINT_ORDER: tuple[str, ...] = (
    "left_hip_pitch_joint",
    "left_hip_roll_joint",
    "left_hip_yaw_joint",
    "left_knee_joint",
    "left_ankle_pitch_joint",
    "left_ankle_roll_joint",
    "right_hip_pitch_joint",
    "right_hip_roll_joint",
    "right_hip_yaw_joint",
    "right_knee_joint",
    "right_ankle_pitch_joint",
    "right_ankle_roll_joint",
    "waist_yaw_joint",
    "left_shoulder_pitch_joint",
    "left_shoulder_roll_joint",
    "left_shoulder_yaw_joint",
    "left_elbow_joint",
    "left_wrist_roll_joint",
    "right_shoulder_pitch_joint",
    "right_shoulder_roll_joint",
    "right_shoulder_yaw_joint",
    "right_elbow_joint",
    "right_wrist_roll_joint",
)

MJLAB_G1_29DOF_EXTRA_JOINTS: tuple[str, ...] = (
    "waist_roll_joint",
    "waist_pitch_joint",
    "left_wrist_pitch_joint",
    "left_wrist_yaw_joint",
    "right_wrist_pitch_joint",
    "right_wrist_yaw_joint",
)

R007E_DECISION = (
    "No mature company_g1_edu_23dof controller checkpoint is selected. "
    "Keep the official 29DoF ONNX as mjlab_g1_29dof_reference evidence only; "
    "the company 23DoF path requires a native 23DoF controller training run or "
    "a separately validated conversion experiment before controller smoke."
)


@dataclass(frozen=True)
class ObservationTermContract:
    name: str
    dim: int

    def __post_init__(self) -> None:
        if self.dim <= 0:
            raise ValueError(f"observation term {self.name!r} must have positive dim")


@dataclass(frozen=True)
class ControllerProfileContract:
    controller_profile_id: str
    robot_profile_id: RobotProfileId
    controlled_dof: int
    action_dim: int
    mjlab_flat_actor_terms: tuple[ObservationTermContract, ...]
    deploy_style_actor_terms: tuple[ObservationTermContract, ...]
    selected_controller_source: str
    route: ControllerRoute
    mature_controller_evidence: bool
    note: str

    @property
    def mjlab_flat_actor_obs_dim(self) -> int:
        return observation_dim(self.mjlab_flat_actor_terms)

    @property
    def deploy_style_actor_obs_dim(self) -> int:
        return observation_dim(self.deploy_style_actor_terms)


def observation_dim(terms: Sequence[ObservationTermContract]) -> int:
    return sum(term.dim for term in terms)


def joint_order_sha256(joint_order: Sequence[str]) -> str:
    payload = "\n".join(joint_order).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def mjlab_flat_actor_terms(controlled_dof: int) -> tuple[ObservationTermContract, ...]:
    """MJLab flat velocity actor terms after height_scan is removed."""
    return (
        ObservationTermContract("base_lin_vel", 3),
        ObservationTermContract("base_ang_vel", 3),
        ObservationTermContract("projected_gravity", 3),
        ObservationTermContract("joint_pos_rel", controlled_dof),
        ObservationTermContract("joint_vel_rel", controlled_dof),
        ObservationTermContract("last_action", controlled_dof),
        ObservationTermContract("velocity_command", 3),
    )


def deploy_style_actor_terms(controlled_dof: int) -> tuple[ObservationTermContract, ...]:
    """Official Unitree deployment-style terms observed in deploy.yaml."""
    return (
        ObservationTermContract("base_ang_vel", 3),
        ObservationTermContract("projected_gravity", 3),
        ObservationTermContract("velocity_command", 3),
        ObservationTermContract("gait_phase", 2),
        ObservationTermContract("joint_pos_rel", controlled_dof),
        ObservationTermContract("joint_vel_rel", controlled_dof),
        ObservationTermContract("last_action", controlled_dof),
    )


COMPANY_G1_23DOF_CONTROLLER_CONTRACT = ControllerProfileContract(
    controller_profile_id="company_g1_edu_23dof_controller_pending_r007e",
    robot_profile_id="company_g1_edu_23dof",
    controlled_dof=23,
    action_dim=23,
    mjlab_flat_actor_terms=mjlab_flat_actor_terms(23),
    deploy_style_actor_terms=deploy_style_actor_terms(23),
    selected_controller_source="none-selected-mature-controller-pending",
    route="train_23dof_required",
    mature_controller_evidence=False,
    note=R007E_DECISION,
)

MJLAB_G1_29DOF_REFERENCE_CONTRACT = ControllerProfileContract(
    controller_profile_id="mjlab_g1_29dof_reference_velocity_v0",
    robot_profile_id="mjlab_g1_29dof_reference",
    controlled_dof=29,
    action_dim=29,
    mjlab_flat_actor_terms=mjlab_flat_actor_terms(29),
    deploy_style_actor_terms=deploy_style_actor_terms(29),
    selected_controller_source="checkpoints/unitree_rl_mjlab_g1_velocity_v0/policy.onnx",
    route="reference_29dof_only",
    mature_controller_evidence=False,
    note=(
        "Official Unitree RL MJLab 29DoF ONNX is a reference candidate. "
        "It has deploy-style obs_dim=98 and action_dim=29, so it cannot be "
        "reported as company 23DoF controller evidence."
    ),
)


def get_controller_contract(robot_profile_id: RobotProfileId) -> ControllerProfileContract:
    if robot_profile_id == "company_g1_edu_23dof":
        return COMPANY_G1_23DOF_CONTROLLER_CONTRACT
    if robot_profile_id == "mjlab_g1_29dof_reference":
        return MJLAB_G1_29DOF_REFERENCE_CONTRACT
    raise ValueError(f"unknown robot profile id: {robot_profile_id!r}")

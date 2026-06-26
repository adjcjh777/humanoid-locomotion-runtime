from __future__ import annotations

import pytest

from humanoid_locomotion_runtime.controller_contracts import (
    COMPANY_G1_23DOF_CONTROLLER_CONTRACT,
    COMPANY_G1_23DOF_JOINT_ORDER,
    MJLAB_G1_29DOF_EXTRA_JOINTS,
    MJLAB_G1_29DOF_REFERENCE_CONTRACT,
    ObservationTermContract,
    get_controller_contract,
    joint_order_sha256,
)


def test_company_23dof_controller_contract_locks_r007e_decision() -> None:
    contract = COMPANY_G1_23DOF_CONTROLLER_CONTRACT

    assert contract.robot_profile_id == "company_g1_edu_23dof"
    assert contract.controller_profile_id == "company_g1_edu_23dof_controller_pending_r007e"
    assert contract.controlled_dof == 23
    assert contract.action_dim == 23
    assert contract.mjlab_flat_actor_obs_dim == 81
    assert contract.deploy_style_actor_obs_dim == 80
    assert contract.route == "train_23dof_required"
    assert contract.selected_controller_source == "none-selected-mature-controller-pending"
    assert contract.mature_controller_evidence is False
    assert "No mature company_g1_edu_23dof controller checkpoint" in contract.note


def test_reference_29dof_contract_remains_reference_only() -> None:
    contract = MJLAB_G1_29DOF_REFERENCE_CONTRACT

    assert contract.robot_profile_id == "mjlab_g1_29dof_reference"
    assert contract.controlled_dof == 29
    assert contract.action_dim == 29
    assert contract.mjlab_flat_actor_obs_dim == 99
    assert contract.deploy_style_actor_obs_dim == 98
    assert contract.route == "reference_29dof_only"
    assert contract.mature_controller_evidence is False
    assert contract.selected_controller_source.endswith("policy.onnx")
    assert "cannot be reported as company 23DoF controller evidence" in contract.note


def test_23dof_joint_order_excludes_mjlab_reference_extra_joints() -> None:
    assert len(COMPANY_G1_23DOF_JOINT_ORDER) == 23
    assert COMPANY_G1_23DOF_JOINT_ORDER[0] == "left_hip_pitch_joint"
    assert COMPANY_G1_23DOF_JOINT_ORDER[-1] == "right_wrist_roll_joint"

    for extra_joint in MJLAB_G1_29DOF_EXTRA_JOINTS:
        assert extra_joint not in COMPANY_G1_23DOF_JOINT_ORDER

    digest = joint_order_sha256(COMPANY_G1_23DOF_JOINT_ORDER)
    assert len(digest) == 64
    assert digest == "186e29d240d7cfeefe4b4c3d8c739c33a779503817ae685783ae5004fd0ebb2c"


def test_get_controller_contract_rejects_unknown_profile() -> None:
    assert get_controller_contract("company_g1_edu_23dof") is COMPANY_G1_23DOF_CONTROLLER_CONTRACT

    with pytest.raises(ValueError, match="unknown robot profile"):
        get_controller_contract("unitree_g1_untracked")  # type: ignore[arg-type]


def test_observation_term_contract_requires_positive_dim() -> None:
    with pytest.raises(ValueError, match="positive dim"):
        ObservationTermContract("bad_term", 0)

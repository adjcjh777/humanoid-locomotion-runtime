from __future__ import annotations

import pytest
from pydantic import ValidationError

from humanoid_locomotion_runtime.schemas import RecoveryActionRecord
from humanoid_locomotion_runtime.snapshot_branching import (
    CommonRandomStream,
    DecisionEpoch,
    FakeDeterministicSnapshotProvider,
    SnapshotBranchMetadata,
    SnapshotManifest,
    runtime_payload_sha256,
)


def digest(character: str) -> str:
    return character * 64


def test_snapshot_manifest_records_contract_only_restore_boundary() -> None:
    manifest = SnapshotManifest(
        snapshot_id="snap-001",
        decision_id="dec-001",
        scenario_seed=202606260,
        exogenous_noise_seed=202606261,
        observation_hash=digest("a"),
        memory_hash=digest("b"),
        robot_profile_id="company_g1_edu_23dof",
        controller_profile_id="company_g1_edu_23dof_controller_pending_r007e",
        simulator_state_hash=digest("c"),
        runtime_state_hashes={
            "planner": digest("d"),
            "localization": digest("e"),
            "memory": digest("f"),
            "controller": digest("0"),
            "failure_injector": digest("1"),
            "active_option": digest("2"),
        },
        active_option="slow_down",
    )

    assert manifest.restore_status == "contract_only_no_restore"
    assert manifest.robot_profile_id == "company_g1_edu_23dof"
    assert set(manifest.runtime_state_hashes) >= {
        "planner",
        "localization",
        "memory",
        "controller",
        "failure_injector",
        "active_option",
    }


def test_snapshot_branch_metadata_carries_required_branch_fields() -> None:
    metadata = SnapshotBranchMetadata(
        base_snapshot_id="snap-001",
        branch_id="branch-001",
        decision_id="dec-001",
        scenario_seed=202606260,
        exogenous_noise_seed=202606261,
        observation_hash=digest("a"),
        memory_hash=digest("b"),
        action="slow_down",
        option_outcome="not_run",
        controller_profile_id="company_g1_edu_23dof_controller_pending_r007e",
        robot_profile_id="company_g1_edu_23dof",
        policy_training_seed=61001,
    )

    assert metadata.base_snapshot_id == "snap-001"
    assert metadata.branch_id == "branch-001"
    assert metadata.action == "slow_down"
    assert metadata.option_outcome == "not_run"
    assert metadata.common_random_stream_id == "crn-v0"


def test_snapshot_contracts_reject_invalid_hash_and_privileged_metadata() -> None:
    with pytest.raises(ValidationError, match="SHA256"):
        SnapshotBranchMetadata(
            base_snapshot_id="snap-001",
            branch_id="branch-001",
            decision_id="dec-001",
            scenario_seed=1,
            exogenous_noise_seed=2,
            observation_hash="not-a-digest",
            memory_hash=digest("b"),
            action="continue",
            option_outcome="not_run",
            controller_profile_id="controller",
            robot_profile_id="robot",
        )

    with pytest.raises(ValidationError, match="oracle_action"):
        SnapshotManifest(
            snapshot_id="snap-001",
            decision_id="dec-001",
            scenario_seed=1,
            exogenous_noise_seed=2,
            observation_hash=digest("a"),
            memory_hash=digest("b"),
            robot_profile_id="company_g1_edu_23dof",
            controller_profile_id="company_g1_edu_23dof_controller_pending_r007e",
            simulator_state_hash=digest("c"),
            runtime_state_hashes={"planner": digest("d")},
            metadata={"oracle_action": "safe_stop"},
        )


def test_recovery_action_record_branch_hash_fields_are_checked() -> None:
    record = RecoveryActionRecord(
        record_id="rec-001",
        episode_id="episode-001",
        timestamp_s=1.0,
        action="slow_down",
        available_actions=["continue", "slow_down"],
        policy_name="contract_test",
        decision_id="dec-001",
        base_snapshot_id="snap-001",
        branch_id="branch-001",
        scenario_seed=202606260,
        exogenous_noise_seed=202606261,
        observation_hash=digest("a"),
        memory_hash=digest("b"),
        option_outcome="not_run",
    )

    assert record.observation_hash == digest("a")
    assert record.memory_hash == digest("b")

    with pytest.raises(ValidationError, match="SHA256"):
        RecoveryActionRecord(
            record_id="rec-002",
            episode_id="episode-001",
            timestamp_s=1.0,
            action="slow_down",
            available_actions=["continue", "slow_down"],
            policy_name="contract_test",
            observation_hash="bad",
        )


def test_decision_epoch_and_common_random_stream_record_backend_neutral_contract() -> None:
    epoch = DecisionEpoch(
        decision_id="dec-001",
        episode_id="episode-001",
        timestamp_s=10.0,
        trigger="failure_trigger",
        scenario_seed=202606260,
        exogenous_noise_seed=202606261,
        observation_hash=digest("a"),
        memory_hash=digest("b"),
        active_option="slow_down",
    )
    stream = CommonRandomStream(
        scenario_seed=epoch.scenario_seed,
        exogenous_noise_seed=epoch.exogenous_noise_seed,
    )

    assert epoch.trigger == "failure_trigger"
    assert stream.stream_id == "crn-v0"
    assert stream.deterministic_replay_required is True

    with pytest.raises(ValidationError, match="ground_truth_target_pose"):
        DecisionEpoch(
            decision_id="dec-bad",
            episode_id="episode-001",
            timestamp_s=10.0,
            trigger="option_timeout",
            scenario_seed=1,
            exogenous_noise_seed=2,
            observation_hash=digest("a"),
            memory_hash=digest("b"),
            metadata={"nested": {"ground_truth_target_pose": [0, 0, 0]}},
        )


def test_runtime_payload_hash_rejects_privileged_nested_fields() -> None:
    assert runtime_payload_sha256({"planner": {"blocked": False}}) != runtime_payload_sha256(
        {"planner": {"blocked": True}}
    )

    with pytest.raises(ValueError, match="mujoco_object_id"):
        runtime_payload_sha256({"runtime": [{"mujoco_object_id": "object-42"}]})


def test_fake_deterministic_snapshot_provider_roundtrips_without_claiming_r018() -> None:
    provider = FakeDeterministicSnapshotProvider(
        robot_profile_id="company_g1_edu_23dof",
        controller_profile_id="company_g1_edu_23dof_controller_pending_r007e",
    )
    epoch = DecisionEpoch(
        decision_id="dec-001",
        episode_id="episode-001",
        timestamp_s=1.0,
        trigger="failure_trigger",
        scenario_seed=202606260,
        exogenous_noise_seed=202606261,
        observation_hash=digest("a"),
        memory_hash=digest("b"),
        active_option="slow_down",
    )

    manifest = provider.capture(
        snapshot_id="snap-001",
        epoch=epoch,
        simulator_state={"qpos_hash_input": [1, 2, 3]},
        runtime_components={
            "planner": {"route_id": "route-001"},
            "memory": {"target_ids": ["target-001"]},
            "active_option": {"action": "slow_down", "elapsed_s": 0.5},
        },
    )
    restored = provider.restore("snap-001")
    branch = provider.branch(
        base_snapshot_id="snap-001",
        branch_id="branch-safe-stop",
        action="safe_stop",
        policy_training_seed=61001,
    )

    assert restored == manifest
    assert manifest.restore_status == "contract_only_no_restore"
    assert manifest.metadata["testbed_scope"] == "fake_backend_only"
    assert set(manifest.runtime_state_hashes) == {"active_option", "memory", "planner"}
    assert branch.base_snapshot_id == "snap-001"
    assert branch.action == "safe_stop"
    assert branch.common_random_stream_id == "crn-v0"
    assert branch.metadata["testbed_scope"] == "fake_backend_only"


def test_fake_snapshot_provider_applies_leakage_boundary_to_runtime_components() -> None:
    provider = FakeDeterministicSnapshotProvider(
        robot_profile_id="company_g1_edu_23dof",
        controller_profile_id="company_g1_edu_23dof_controller_pending_r007e",
    )
    epoch = DecisionEpoch(
        decision_id="dec-001",
        episode_id="episode-001",
        timestamp_s=1.0,
        trigger="failure_trigger",
        scenario_seed=202606260,
        exogenous_noise_seed=202606261,
        observation_hash=digest("a"),
        memory_hash=digest("b"),
    )

    with pytest.raises(ValueError, match="oracle_action"):
        provider.capture(
            snapshot_id="snap-bad",
            epoch=epoch,
            simulator_state={"legal": True},
            runtime_components={"planner": {"oracle_action": "safe_stop"}},
        )

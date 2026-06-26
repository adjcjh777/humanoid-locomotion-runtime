from __future__ import annotations

import json

import pytest
from pydantic import ValidationError

from humanoid_locomotion_runtime.schemas import (
    BodyMemoryState,
    EpisodeManifest,
    FailureEvent,
    LocomotionCommand,
    LocomotionStatus,
    MemoryTarget,
    OracleAnnotation,
    PolicyObservation,
    RuntimeEvent,
    serialize_policy_observation,
)


def make_policy_observation(**overrides: object) -> PolicyObservation:
    payload = {
        "observation_id": "obs-001",
        "episode_id": "episode-001",
        "timestamp_s": 1.0,
        "command": LocomotionCommand(
            command_id="cmd-001",
            mode="walk_to",
            issued_at_s=0.0,
            language="walk to the table",
            target_pose=(1.0, 2.0, 0.0),
        ),
        "status": LocomotionStatus(
            timestamp_s=1.0,
            base_position=(0.0, 0.0, 0.9),
            base_orientation_quat=(1.0, 0.0, 0.0, 0.0),
            linear_velocity=(0.1, 0.0, 0.0),
            angular_velocity=(0.0, 0.0, 0.0),
            stability_margin=0.6,
            localization_quality=0.8,
            tracking_error=0.1,
        ),
        "memory_targets": [
            MemoryTarget(
                target_id="target-001",
                label="table",
                confidence=0.82,
                last_seen_s=0.5,
                estimated_pose=(1.0, 2.0, 0.0, 0.0, 0.0, 0.0),
            )
        ],
        "body_memory": BodyMemoryState(
            timestamp_s=1.0,
            balance_risk=0.2,
            slip_risk=0.1,
            fatigue_score=0.0,
            localization_quality=0.8,
            tracking_error_trend=0.01,
            trend_window_s=2.0,
        ),
        "recent_failures": [
            FailureEvent(
                failure_id="fail-001",
                timestamp_s=0.8,
                runtime_failure_kind="tracking_degraded",
                temporal_profile_hint="cumulative",
                severity=0.4,
                evidence={"tracking_error_delta": 0.2},
            )
        ],
        "available_actions": ["continue", "slow_down", "safe_stop", "local_replan"],
        "runtime_context": {"planner_blocked": False},
    }
    payload.update(overrides)
    return PolicyObservation(**payload)


def test_policy_observation_serializes_without_oracle_fields() -> None:
    observation = make_policy_observation()
    annotation = OracleAnnotation(
        annotation_id="ora-001",
        episode_id=observation.episode_id,
        timestamp_s=observation.timestamp_s,
        true_failure_cause="tracking_degradation",
        true_temporal_profile="cumulative",
        oracle_action="safe_stop",
        mujoco_object_id="object-42",
        ground_truth_target_pose=(1.0, 2.0, 0.0, 0.0, 0.0, 0.0),
        simulator_semantic_label="table",
    )

    payload = serialize_policy_observation(observation)
    encoded_payload = json.dumps(payload, sort_keys=True)

    assert annotation.oracle_action == "safe_stop"
    assert "oracle_action" not in encoded_payload
    assert "mujoco_object_id" not in encoded_payload
    assert "ground_truth_target_pose" not in encoded_payload
    assert payload["runtime_context"] == {"planner_blocked": False}


def test_policy_observation_round_trips_as_structured_schema() -> None:
    observation = make_policy_observation()

    round_tripped = PolicyObservation.model_validate_json(observation.model_dump_json())

    assert round_tripped == observation


def test_policy_observation_rejects_top_level_privileged_extra_field() -> None:
    with pytest.raises(ValidationError):
        make_policy_observation(mujoco_object_id="object-42")


def test_policy_observation_rejects_nested_privileged_runtime_context() -> None:
    with pytest.raises(ValidationError, match="oracle_action"):
        make_policy_observation(runtime_context={"nested": {"oracle_action": "safe_stop"}})


def test_runtime_event_rejects_privileged_data() -> None:
    with pytest.raises(ValidationError, match="ground_truth_target_pose"):
        RuntimeEvent(
            event_id="evt-001",
            episode_id="episode-001",
            timestamp_s=1.0,
            event_type="recovery",
            message="bad runtime event",
            data={"ground_truth_target_pose": [1.0, 2.0, 0.0]},
        )


def test_oracle_annotation_accepts_privileged_evaluation_fields() -> None:
    annotation = OracleAnnotation(
        annotation_id="ora-002",
        episode_id="episode-001",
        timestamp_s=1.0,
        true_failure_cause="path_blockage",
        true_temporal_profile="recurrent",
        true_failure_family="path",
        oracle_action="local_replan",
        oracle_action_label="evaluation-only replan",
        mujoco_object_id="object-99",
        mujoco_object_ids=["object-99", "object-100"],
        ground_truth_target_pose=(1.0, 2.0, 0.0, 0.0, 0.0, 0.0),
        simulator_semantic_label="chair",
        simulator_semantic_labels=["chair", "obstacle"],
        privileged_metrics={"branch_oracle_value": 1.0},
    )

    assert annotation.oracle_action == "local_replan"
    assert annotation.privileged_metrics["branch_oracle_value"] == 1.0


def test_episode_manifest_records_robot_profile_metadata() -> None:
    manifest = EpisodeManifest(
        episode_id="episode-001",
        robot_profile_id="company_g1_edu_23dof",
        robot_dof=23,
        action_dim=23,
        joint_order_sha256="a" * 64,
        controller_profile_id="company_g1_velocity_controller_v0",
    )

    round_tripped = EpisodeManifest.model_validate_json(manifest.model_dump_json())

    assert round_tripped.robot_profile_id == "company_g1_edu_23dof"
    assert round_tripped.robot_dof == 23
    assert round_tripped.action_dim == 23
    assert round_tripped.joint_order_sha256 == "a" * 64
    assert round_tripped.controller_profile_id == "company_g1_velocity_controller_v0"


def test_episode_manifest_keeps_legacy_defaults_for_robot_profile_metadata() -> None:
    manifest = EpisodeManifest.model_validate({"episode_id": "episode-legacy"})

    assert manifest.robot_profile_id == "unselected"
    assert manifest.robot_dof is None
    assert manifest.action_dim is None
    assert manifest.joint_order_sha256 is None
    assert manifest.controller_profile_id == "unselected"


def test_episode_manifest_rejects_invalid_joint_order_sha256() -> None:
    with pytest.raises(ValidationError, match="joint_order_sha256"):
        EpisodeManifest(
            episode_id="episode-001",
            joint_order_sha256="not-a-sha256",
        )


def test_episode_manifest_metadata_rejects_privileged_fields() -> None:
    with pytest.raises(ValidationError, match="ground_truth_target_pose"):
        EpisodeManifest(
            episode_id="episode-001",
            metadata={"profile_note": {"ground_truth_target_pose": [0.0, 0.0, 0.0]}},
        )

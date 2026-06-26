from __future__ import annotations

import json

import pytest
from pydantic import ValidationError

from humanoid_locomotion_runtime.edp import (
    ARTIFACTS_DIR,
    EVALUATION_DIR,
    EVENTS_FILE,
    MANIFEST_FILE,
    METRICS_FILE,
    ORACLE_ANNOTATIONS_FILE,
    POLICY_OBSERVATIONS_FILE,
    RECOVERY_ACTIONS_FILE,
    REPLAY_INDEX_FILE,
    TIMESERIES_DIR,
    EpisodeDataPackageWriter,
    RuntimeEventLogger,
    assert_valid_episode_data_package,
    validate_episode_data_package,
    write_sample_episode_data_package,
)
from humanoid_locomotion_runtime.schemas import (
    BodyMemoryState,
    EpisodeManifest,
    EpisodeMetrics,
    LocomotionCommand,
    LocomotionStatus,
    MemoryTarget,
    PolicyObservation,
    RecoveryActionRecord,
    ReplayArtifactRecord,
    RuntimeEvent,
)


def make_policy_observation() -> PolicyObservation:
    return PolicyObservation(
        observation_id="obs-001",
        episode_id="episode-a",
        timestamp_s=1.0,
        command=LocomotionCommand(
            command_id="cmd-001",
            mode="walk_to",
            issued_at_s=0.0,
            target_pose=(1.0, 2.0, 0.0),
        ),
        status=LocomotionStatus(
            timestamp_s=1.0,
            base_position=(0.0, 0.0, 0.9),
            base_orientation_quat=(1.0, 0.0, 0.0, 0.0),
            linear_velocity=(0.0, 0.0, 0.0),
            angular_velocity=(0.0, 0.0, 0.0),
        ),
        memory_targets=[
            MemoryTarget(
                target_id="target-001",
                label="table",
                confidence=0.8,
                last_seen_s=0.5,
            )
        ],
        body_memory=BodyMemoryState(
            timestamp_s=1.0,
            balance_risk=0.1,
            slip_risk=0.0,
            fatigue_score=0.0,
            localization_quality=0.9,
            tracking_error_trend=0.0,
            trend_window_s=1.0,
        ),
        available_actions=["continue", "safe_stop"],
    )


def test_sample_episode_data_package_is_valid_without_mujoco(tmp_path) -> None:
    root = write_sample_episode_data_package(tmp_path / "sample-edp")

    result = assert_valid_episode_data_package(root)

    assert result.valid
    assert result.event_count == 1
    assert result.oracle_annotation_count == 1
    for required_path in (
        MANIFEST_FILE,
        EVENTS_FILE,
        METRICS_FILE,
        REPLAY_INDEX_FILE,
        POLICY_OBSERVATIONS_FILE,
        RECOVERY_ACTIONS_FILE,
        TIMESERIES_DIR,
        ARTIFACTS_DIR,
        EVALUATION_DIR,
    ):
        assert (root / required_path).exists()


def test_sample_edp_manifest_includes_robot_profile_metadata(tmp_path) -> None:
    root = write_sample_episode_data_package(tmp_path / "sample-edp")

    manifest_payload = json.loads((root / MANIFEST_FILE).read_text(encoding="utf-8"))
    manifest = EpisodeManifest.model_validate(manifest_payload)

    assert manifest_payload["robot_profile_id"] == "unselected"
    assert manifest_payload["robot_dof"] is None
    assert manifest_payload["action_dim"] is None
    assert manifest_payload["joint_order_sha256"] is None
    assert manifest_payload["controller_profile_id"] == "unselected"
    assert manifest.robot_profile_id == "unselected"


def test_sample_edp_keeps_oracle_annotations_out_of_runtime_events(tmp_path) -> None:
    root = write_sample_episode_data_package(tmp_path / "sample-edp")

    events_payload = (root / EVENTS_FILE).read_text(encoding="utf-8")
    oracle_payload = (root / ORACLE_ANNOTATIONS_FILE).read_text(encoding="utf-8")

    assert "oracle_action" not in events_payload
    assert "mujoco_object_id" not in events_payload
    assert "ground_truth_target_pose" not in events_payload
    assert "oracle_action" in oracle_payload
    assert "mujoco_object_id" in oracle_payload
    assert "ground_truth_target_pose" in oracle_payload
    assert not (root / "oracle_annotations.jsonl").exists()
    assert (root / ORACLE_ANNOTATIONS_FILE).exists()


def test_episode_data_package_validator_reports_missing_required_files(tmp_path) -> None:
    root = write_sample_episode_data_package(tmp_path / "sample-edp")
    (root / METRICS_FILE).unlink()

    result = validate_episode_data_package(root)

    assert not result.valid
    assert any(METRICS_FILE in error for error in result.errors)


def test_episode_data_package_validator_reports_episode_id_mismatch(tmp_path) -> None:
    root = write_sample_episode_data_package(tmp_path / "sample-edp", episode_id="episode-a")
    (root / METRICS_FILE).write_text(
        EpisodeMetrics(episode_id="episode-b").model_dump_json(indent=2) + "\n",
        encoding="utf-8",
    )

    result = validate_episode_data_package(root)

    assert not result.valid
    assert any("does not match manifest episode_id" in error for error in result.errors)


def test_writer_rejects_records_for_other_episodes(tmp_path) -> None:
    writer = EpisodeDataPackageWriter(
        tmp_path / "sample-edp",
        EpisodeManifest(episode_id="episode-a"),
    )
    writer.initialize()

    with pytest.raises(ValueError, match="does not match"):
        writer.write_metrics(EpisodeMetrics(episode_id="episode-b"))


def test_runtime_event_logger_rejects_privileged_runtime_event_data(tmp_path) -> None:
    writer = EpisodeDataPackageWriter(
        tmp_path / "sample-edp",
        EpisodeManifest(episode_id="episode-a"),
    )
    writer.initialize()
    logger = RuntimeEventLogger(writer)

    with pytest.raises(ValidationError, match="oracle_action"):
        logger.record(
            event_id="evt-001",
            timestamp_s=0.0,
            event_type="recovery",
            message="bad event",
            data={"oracle_action": "safe_stop"},
        )


def test_events_jsonl_contains_structured_runtime_events(tmp_path) -> None:
    root = write_sample_episode_data_package(tmp_path / "sample-edp", episode_id="episode-a")
    first_event = json.loads((root / EVENTS_FILE).read_text(encoding="utf-8").splitlines()[0])

    event = RuntimeEvent.model_validate(first_event)

    assert event.episode_id == "episode-a"
    assert event.event_type == "edp"
    assert event.data["requires_mujoco"] is False


def test_writer_records_artifact_sha256_and_validator_detects_corruption(tmp_path) -> None:
    writer = EpisodeDataPackageWriter(
        tmp_path / "sample-edp",
        EpisodeManifest(episode_id="episode-a"),
    )
    writer.initialize()
    RuntimeEventLogger(writer).record(
        event_id="evt-001",
        timestamp_s=0.0,
        event_type="edp",
        message="artifact test",
    )
    writer.write_metrics(EpisodeMetrics(episode_id="episode-a"))

    record = writer.write_artifact(
        ReplayArtifactRecord(
            artifact_id="artifact-001",
            kind="other",
            relative_path="artifacts/state.json",
        ),
        b'{"ok": true}\n',
    )

    assert record.sha256 is not None
    assert assert_valid_episode_data_package(writer.root).valid

    (writer.root / "artifacts/state.json").write_text('{"ok": false}\n', encoding="utf-8")
    result = validate_episode_data_package(writer.root)

    assert not result.valid
    assert any("sha256 mismatch" in error for error in result.errors)


def test_writer_rejects_artifact_in_wrong_edp_subtree(tmp_path) -> None:
    writer = EpisodeDataPackageWriter(
        tmp_path / "sample-edp",
        EpisodeManifest(episode_id="episode-a"),
    )
    writer.initialize()

    with pytest.raises(ValueError, match="must live under 'timeseries/'"):
        writer.write_artifact(
            ReplayArtifactRecord(
                artifact_id="artifact-001",
                kind="timeseries",
                relative_path="artifacts/wrong.json",
            ),
            b"{}",
        )


def test_validator_rejects_replay_artifact_retention_mismatch(tmp_path) -> None:
    writer = EpisodeDataPackageWriter(
        tmp_path / "sample-edp",
        EpisodeManifest(episode_id="episode-a", retention_class="pilot_evaluation"),
    )
    writer.initialize()
    RuntimeEventLogger(writer).record(
        event_id="evt-001",
        timestamp_s=0.0,
        event_type="edp",
        message="retention test",
    )
    writer.write_metrics(EpisodeMetrics(episode_id="episode-a"))

    writer.write_artifact(
        ReplayArtifactRecord(
            artifact_id="artifact-001",
            kind="other",
            relative_path="artifacts/state.json",
            retention_class="training",
        ),
        b"{}",
    )

    result = validate_episode_data_package(writer.root)

    assert not result.valid
    assert any("retention_class" in error for error in result.errors)


def test_writer_persists_policy_observations_and_recovery_records(tmp_path) -> None:
    writer = EpisodeDataPackageWriter(
        tmp_path / "sample-edp",
        EpisodeManifest(episode_id="episode-a"),
    )
    writer.initialize()
    RuntimeEventLogger(writer).record(
        event_id="evt-001",
        timestamp_s=0.0,
        event_type="edp",
        message="record persistence test",
    )
    writer.write_metrics(EpisodeMetrics(episode_id="episode-a"))

    writer.append_policy_observation(make_policy_observation())
    writer.append_recovery_action(
        RecoveryActionRecord(
            record_id="rec-001",
            episode_id="episode-a",
            timestamp_s=1.1,
            action="safe_stop",
            available_actions=["continue", "safe_stop"],
            policy_name="rule_recovery_v0",
            decision_id="dec-001",
        )
    )

    result = assert_valid_episode_data_package(writer.root)

    assert result.policy_observation_count == 1
    assert result.recovery_action_count == 1
    assert (writer.root / POLICY_OBSERVATIONS_FILE).read_text(encoding="utf-8")
    assert (writer.root / RECOVERY_ACTIONS_FILE).read_text(encoding="utf-8")

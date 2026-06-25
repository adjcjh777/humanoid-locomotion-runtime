from __future__ import annotations

import json

import pytest
from pydantic import ValidationError

from humanoid_locomotion_runtime.edp import (
    ARTIFACTS_DIR,
    EVENTS_FILE,
    MANIFEST_FILE,
    METRICS_FILE,
    ORACLE_ANNOTATIONS_FILE,
    REPLAY_INDEX_FILE,
    TIMESERIES_DIR,
    EpisodeDataPackageWriter,
    RuntimeEventLogger,
    assert_valid_episode_data_package,
    validate_episode_data_package,
    write_sample_episode_data_package,
)
from humanoid_locomotion_runtime.schemas import EpisodeManifest, EpisodeMetrics, RuntimeEvent


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
        TIMESERIES_DIR,
        ARTIFACTS_DIR,
    ):
        assert (root / required_path).exists()


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

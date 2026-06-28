from __future__ import annotations

import pytest
from pydantic import ValidationError

from humanoid_locomotion_runtime.grounding_memory import (
    ControlledGroundingAdapter,
    ControlledGroundingRecord,
    TemporaryObjectMemory,
)


def test_controlled_grounding_adapter_selects_runtime_memory_targets() -> None:
    adapter = ControlledGroundingAdapter(min_confidence=0.5)
    records = [
        ControlledGroundingRecord(
            record_id="cup-low",
            label="cup",
            confidence=0.2,
            observed_at_s=1.0,
            camera_frame_id="front_rgbd",
            bbox_xyxy=(0.0, 0.0, 5.0, 5.0),
        ),
        ControlledGroundingRecord(
            record_id="chair-good",
            label="chair",
            confidence=0.9,
            observed_at_s=2.0,
            camera_frame_id="front_rgbd",
            bbox_xyxy=(10.0, 20.0, 30.0, 50.0),
            depth_point_m=(1.0, 0.0, 0.8),
            estimated_pose=(1.0, 0.0, 0.0, 0.0, 0.0, 0.0),
            attributes={"color": "red"},
        ),
    ]

    selection = adapter.select_targets(records, query_label="chair")

    assert selection.rejected_count == 1
    assert len(selection.selected_targets) == 1
    target = selection.selected_targets[0]
    assert target.target_id == "target-chair-good"
    assert target.source == "grounding"
    assert target.attributes["camera_frame_id"] == "front_rgbd"
    assert target.attributes["color"] == "red"


def test_temporary_object_memory_queries_and_expires_targets() -> None:
    adapter = ControlledGroundingAdapter(min_confidence=0.1)
    selection = adapter.select_targets(
        [
            ControlledGroundingRecord(
                record_id="target-1",
                label="door",
                confidence=0.8,
                observed_at_s=10.0,
                camera_frame_id="front_rgbd",
            ),
            ControlledGroundingRecord(
                record_id="target-2",
                label="door",
                confidence=0.9,
                observed_at_s=12.0,
                camera_frame_id="front_rgbd",
            ),
        ]
    )
    memory = TemporaryObjectMemory(ttl_s=5.0)

    memory.update_from_grounding(selection)
    queried = memory.query(label="door", now_s=13.0)

    assert [target.target_id for target in queried] == ["target-target-2", "target-target-1"]
    assert all(target.source == "memory" for target in queried)
    assert memory.get("target-target-1", now_s=16.0) is None
    assert memory.purge_expired(now_s=16.0) == ["target-target-1"]
    assert len(memory) == 1


def test_temporary_object_memory_snapshot_payload_remains_runtime_legal() -> None:
    adapter = ControlledGroundingAdapter()
    selection = adapter.select_targets(
        [
            ControlledGroundingRecord(
                record_id="box-1",
                label="box",
                confidence=0.7,
                observed_at_s=1.0,
                camera_frame_id="front_rgbd",
            )
        ]
    )
    memory = TemporaryObjectMemory()
    memory.update_from_grounding(selection)

    payload = memory.snapshot_payload(now_s=2.0)

    assert payload["memory_scope"] == "temporary_object_memory_v0"
    assert payload["targets"][0]["label"] == "box"


def test_grounding_memory_rejects_privileged_and_bad_bbox_fields() -> None:
    with pytest.raises(ValidationError, match="positive area"):
        ControlledGroundingRecord(
            record_id="bad-bbox",
            label="box",
            confidence=0.7,
            observed_at_s=1.0,
            camera_frame_id="front_rgbd",
            bbox_xyxy=(10.0, 10.0, 5.0, 5.0),
        )

    with pytest.raises(ValidationError, match="ground_truth_target_pose"):
        ControlledGroundingRecord(
            record_id="bad-privileged",
            label="box",
            confidence=0.7,
            observed_at_s=1.0,
            camera_frame_id="front_rgbd",
            attributes={"nested": {"ground_truth_target_pose": [0, 0, 0]}},
        )

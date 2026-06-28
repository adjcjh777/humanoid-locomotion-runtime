"""Controlled grounding and temporary object memory contracts.

These are Mac-safe runtime-facing skeletons. They model detector-like outputs
and short-horizon target memory without importing a real perception stack.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field
from typing import Literal

from pydantic import Field, field_validator

from humanoid_locomotion_runtime.schemas import (
    JsonDict,
    MemoryTarget,
    Pose3D,
    StrictSchema,
    Vector3,
    assert_no_privileged_keys,
)

BoundingBoxXYXY = tuple[float, float, float, float]
GroundingSource = Literal["controlled_detector", "operator_seed", "replay_fixture"]


class ControlledGroundingRecord(StrictSchema):
    """Detector-like target observation that is legal for runtime use."""

    record_id: str
    label: str
    confidence: float = Field(ge=0, le=1)
    observed_at_s: float = Field(ge=0)
    camera_frame_id: str
    bbox_xyxy: BoundingBoxXYXY | None = None
    depth_point_m: Vector3 | None = None
    estimated_pose: Pose3D | None = None
    source: GroundingSource = "controlled_detector"
    attributes: JsonDict = Field(default_factory=dict)

    @field_validator("bbox_xyxy")
    @classmethod
    def _bbox_has_positive_area(cls, value: BoundingBoxXYXY | None) -> BoundingBoxXYXY | None:
        if value is None:
            return value
        x_min, y_min, x_max, y_max = value
        if x_max <= x_min or y_max <= y_min:
            raise ValueError("bbox_xyxy must have positive area")
        return value

    @field_validator("attributes")
    @classmethod
    def _attributes_have_no_privileged_keys(cls, value: JsonDict) -> JsonDict:
        assert_no_privileged_keys(value, "ControlledGroundingRecord.attributes")
        return value


class GroundingSelection(StrictSchema):
    query_label: str | None = None
    selected_targets: list[MemoryTarget] = Field(default_factory=list)
    rejected_count: int = Field(ge=0)
    metadata: JsonDict = Field(default_factory=dict)

    @field_validator("metadata")
    @classmethod
    def _metadata_has_no_privileged_keys(cls, value: JsonDict) -> JsonDict:
        assert_no_privileged_keys(value, "GroundingSelection.metadata")
        return value


class ControlledGroundingAdapter:
    """Convert controlled detector-like records into runtime memory targets."""

    def __init__(self, *, min_confidence: float = 0.25, target_prefix: str = "target") -> None:
        if not 0 <= min_confidence <= 1:
            raise ValueError("min_confidence must be between 0 and 1")
        self.min_confidence = min_confidence
        self.target_prefix = target_prefix

    def select_targets(
        self,
        records: Iterable[ControlledGroundingRecord],
        *,
        query_label: str | None = None,
        min_confidence: float | None = None,
    ) -> GroundingSelection:
        threshold = self.min_confidence if min_confidence is None else min_confidence
        if not 0 <= threshold <= 1:
            raise ValueError("min_confidence must be between 0 and 1")

        selected: list[MemoryTarget] = []
        rejected_count = 0
        normalized_query = query_label.casefold() if query_label is not None else None
        for record in records:
            label_matches = (
                normalized_query is None or record.label.casefold() == normalized_query
            )
            if record.confidence < threshold or not label_matches:
                rejected_count += 1
                continue
            selected.append(self._record_to_memory_target(record))

        selected.sort(key=lambda target: (-target.confidence, target.target_id))
        return GroundingSelection(
            query_label=query_label,
            selected_targets=selected,
            rejected_count=rejected_count,
            metadata={"adapter_scope": "controlled_detector_like_mac_safe"},
        )

    def _record_to_memory_target(self, record: ControlledGroundingRecord) -> MemoryTarget:
        attributes: JsonDict = {
            "grounding_record_id": record.record_id,
            "camera_frame_id": record.camera_frame_id,
            "grounding_source": record.source,
        }
        if record.bbox_xyxy is not None:
            attributes["bbox_xyxy"] = list(record.bbox_xyxy)
        if record.depth_point_m is not None:
            attributes["depth_point_m"] = list(record.depth_point_m)
        attributes.update(record.attributes)
        return MemoryTarget(
            target_id=f"{self.target_prefix}-{record.record_id}",
            label=record.label,
            confidence=record.confidence,
            last_seen_s=record.observed_at_s,
            estimated_pose=record.estimated_pose,
            source="grounding",
            attributes=attributes,
        )


@dataclass
class TemporaryObjectMemory:
    """Short-horizon object memory that stores only runtime-legal targets."""

    ttl_s: float = 30.0
    _targets: dict[str, MemoryTarget] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.ttl_s <= 0:
            raise ValueError("ttl_s must be positive")

    def remember(self, target: MemoryTarget) -> MemoryTarget:
        assert_no_privileged_keys(target, "TemporaryObjectMemory.remember")
        self._targets[target.target_id] = target
        return target

    def remember_many(self, targets: Iterable[MemoryTarget]) -> list[MemoryTarget]:
        return [self.remember(target) for target in targets]

    def update_from_grounding(self, selection: GroundingSelection) -> list[MemoryTarget]:
        return self.remember_many(selection.selected_targets)

    def query(
        self,
        *,
        label: str | None = None,
        now_s: float | None = None,
        min_confidence: float = 0.0,
    ) -> list[MemoryTarget]:
        if not 0 <= min_confidence <= 1:
            raise ValueError("min_confidence must be between 0 and 1")
        normalized_label = label.casefold() if label is not None else None
        candidates = []
        for target in self._targets.values():
            if now_s is not None and self._is_expired(target, now_s):
                continue
            if target.confidence < min_confidence:
                continue
            if normalized_label is not None and target.label.casefold() != normalized_label:
                continue
            candidates.append(target.model_copy(update={"source": "memory"}))
        candidates.sort(
            key=lambda target: (-target.confidence, -target.last_seen_s, target.target_id)
        )
        return candidates

    def get(self, target_id: str, *, now_s: float | None = None) -> MemoryTarget | None:
        target = self._targets.get(target_id)
        if target is None:
            return None
        if now_s is not None and self._is_expired(target, now_s):
            return None
        return target.model_copy(update={"source": "memory"})

    def purge_expired(self, *, now_s: float) -> list[str]:
        expired_ids = [
            target_id
            for target_id, target in self._targets.items()
            if self._is_expired(target, now_s)
        ]
        for target_id in expired_ids:
            del self._targets[target_id]
        return sorted(expired_ids)

    def snapshot_payload(self, *, now_s: float | None = None) -> JsonDict:
        targets = [
            target.model_dump(mode="json", exclude_none=True)
            for target in self.query(now_s=now_s)
        ]
        payload: JsonDict = {
            "memory_scope": "temporary_object_memory_v0",
            "ttl_s": self.ttl_s,
            "targets": targets,
        }
        assert_no_privileged_keys(payload, "TemporaryObjectMemory.snapshot_payload")
        return payload

    def __len__(self) -> int:
        return len(self._targets)

    def _is_expired(self, target: MemoryTarget, now_s: float) -> bool:
        return now_s > target.last_seen_s + self.ttl_s

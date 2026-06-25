"""Core schemas and leakage boundaries for the runtime scaffold."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from datetime import UTC, datetime
from typing import Any, Literal, Self

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

JsonDict = dict[str, Any]
Pose2D = tuple[float, float, float]
Pose3D = tuple[float, float, float, float, float, float]
Vector3 = tuple[float, float, float]
Quaternion = tuple[float, float, float, float]

RecoveryAction = Literal[
    "continue",
    "slow_down",
    "safe_stop",
    "local_replan",
    "recover_balance",
    "relocalize",
    "refresh_target_grounding",
    "abort_task",
]

CommandMode = Literal[
    "stand_ready",
    "track_velocity",
    "walk_to",
    "turn_to",
    "safe_stop",
    "recover",
]

RuntimeEventType = Literal[
    "command",
    "status",
    "memory",
    "failure",
    "recovery",
    "safety",
    "edp",
]

RetentionClass = Literal["training", "pilot_evaluation", "paper_cases"]

PRIVILEGED_FIELD_NAMES = frozenset(
    {
        "mujoco_object_id",
        "mujoco_object_ids",
        "ground_truth_target_pose",
        "simulator_semantic_label",
        "simulator_semantic_labels",
        "true_failure_cause",
        "true_temporal_profile",
        "true_failure_family",
        "oracle_action",
        "oracle_action_label",
        "privileged_object_id",
        "privileged_target_pose",
    }
)


def find_privileged_key_paths(value: Any, path: str = "$") -> list[str]:
    """Return JSON-like paths that contain evaluation-only field names."""
    if isinstance(value, BaseModel):
        value = value.model_dump(mode="json")

    if isinstance(value, Mapping):
        found: list[str] = []
        for key, item in value.items():
            key_text = str(key)
            item_path = f"{path}.{key_text}"
            if key_text in PRIVILEGED_FIELD_NAMES:
                found.append(item_path)
            found.extend(find_privileged_key_paths(item, item_path))
        return found

    if isinstance(value, Sequence) and not isinstance(value, str | bytes | bytearray):
        found = []
        for index, item in enumerate(value):
            found.extend(find_privileged_key_paths(item, f"{path}[{index}]"))
        return found

    return []


def assert_no_privileged_keys(value: Any, context: str = "runtime payload") -> None:
    """Raise if a runtime-facing payload contains evaluation-only field names."""
    paths = find_privileged_key_paths(value)
    if paths:
        joined = ", ".join(sorted(paths))
        raise ValueError(f"{context} contains privileged evaluation fields: {joined}")


class StrictSchema(BaseModel):
    """Common strict model configuration for tracked runtime records."""

    model_config = ConfigDict(extra="forbid", frozen=True)


class LocomotionCommand(StrictSchema):
    command_id: str
    mode: CommandMode
    issued_at_s: float = Field(ge=0)
    language: str | None = None
    target_pose: Pose2D | None = None
    velocity_xy_yaw: Vector3 | None = None
    metadata: JsonDict = Field(default_factory=dict)

    @field_validator("metadata")
    @classmethod
    def _metadata_has_no_privileged_keys(cls, value: JsonDict) -> JsonDict:
        assert_no_privileged_keys(value, "LocomotionCommand.metadata")
        return value


class LocomotionStatus(StrictSchema):
    timestamp_s: float = Field(ge=0)
    base_position: Vector3
    base_orientation_quat: Quaternion
    linear_velocity: Vector3
    angular_velocity: Vector3
    gait_phase: str | None = None
    stability_margin: float | None = None
    localization_quality: float | None = Field(default=None, ge=0, le=1)
    tracking_error: float | None = Field(default=None, ge=0)
    metadata: JsonDict = Field(default_factory=dict)

    @field_validator("metadata")
    @classmethod
    def _metadata_has_no_privileged_keys(cls, value: JsonDict) -> JsonDict:
        assert_no_privileged_keys(value, "LocomotionStatus.metadata")
        return value


class MemoryTarget(StrictSchema):
    target_id: str
    label: str
    confidence: float = Field(ge=0, le=1)
    last_seen_s: float = Field(ge=0)
    estimated_pose: Pose3D | None = None
    source: Literal["grounding", "memory", "planner", "operator"] = "grounding"
    attributes: JsonDict = Field(default_factory=dict)

    @field_validator("attributes")
    @classmethod
    def _attributes_have_no_privileged_keys(cls, value: JsonDict) -> JsonDict:
        assert_no_privileged_keys(value, "MemoryTarget.attributes")
        return value


class BodyMemoryState(StrictSchema):
    timestamp_s: float = Field(ge=0)
    balance_risk: float = Field(ge=0, le=1)
    slip_risk: float = Field(ge=0, le=1)
    fatigue_score: float = Field(ge=0, le=1)
    localization_quality: float = Field(ge=0, le=1)
    tracking_error_trend: float
    trend_window_s: float = Field(gt=0)
    recent_contact_events: list[str] = Field(default_factory=list)
    metadata: JsonDict = Field(default_factory=dict)

    @field_validator("metadata")
    @classmethod
    def _metadata_has_no_privileged_keys(cls, value: JsonDict) -> JsonDict:
        assert_no_privileged_keys(value, "BodyMemoryState.metadata")
        return value


class FailureEvent(StrictSchema):
    failure_id: str
    timestamp_s: float = Field(ge=0)
    runtime_failure_kind: str
    temporal_profile_hint: str | None = None
    severity: float = Field(ge=0, le=1)
    evidence: JsonDict = Field(default_factory=dict)

    @field_validator("evidence")
    @classmethod
    def _evidence_has_no_privileged_keys(cls, value: JsonDict) -> JsonDict:
        assert_no_privileged_keys(value, "FailureEvent.evidence")
        return value


class RecoveryActionRecord(StrictSchema):
    record_id: str
    episode_id: str
    timestamp_s: float = Field(ge=0)
    action: RecoveryAction
    available_actions: list[RecoveryAction]
    policy_name: str
    active_option: RecoveryAction | None = None
    decision_id: str | None = None
    base_snapshot_id: str | None = None
    branch_id: str | None = None
    policy_training_seed: int | None = None
    scenario_seed: int | None = None
    exogenous_noise_seed: int | None = None
    observation_hash: str | None = None
    memory_hash: str | None = None
    option_outcome: str | None = None
    option_duration_s: float | None = Field(default=None, ge=0)
    extra_info: JsonDict = Field(default_factory=dict)

    @field_validator("extra_info")
    @classmethod
    def _extra_info_has_no_privileged_keys(cls, value: JsonDict) -> JsonDict:
        assert_no_privileged_keys(value, "RecoveryActionRecord.extra_info")
        return value


class PolicyObservation(StrictSchema):
    observation_id: str
    episode_id: str
    timestamp_s: float = Field(ge=0)
    command: LocomotionCommand
    status: LocomotionStatus
    memory_targets: list[MemoryTarget] = Field(default_factory=list)
    body_memory: BodyMemoryState
    recent_failures: list[FailureEvent] = Field(default_factory=list)
    available_actions: list[RecoveryAction]
    active_option: RecoveryAction | None = None
    memory_available: bool = True
    runtime_context: JsonDict = Field(default_factory=dict)

    @field_validator("runtime_context")
    @classmethod
    def _runtime_context_has_no_privileged_keys(cls, value: JsonDict) -> JsonDict:
        assert_no_privileged_keys(value, "PolicyObservation.runtime_context")
        return value

    @model_validator(mode="after")
    def _policy_payload_has_no_privileged_keys(self) -> Self:
        assert_no_privileged_keys(self.model_dump(mode="json"), "PolicyObservation")
        return self

    def to_policy_dict(self) -> JsonDict:
        """Serialize only fields legal for runtime policy decisions."""
        payload = self.model_dump(mode="json", exclude_none=True)
        assert_no_privileged_keys(payload, "PolicyObservation.to_policy_dict")
        return payload


class RuntimeEvent(StrictSchema):
    event_id: str
    episode_id: str
    timestamp_s: float = Field(ge=0)
    event_type: RuntimeEventType
    message: str
    data: JsonDict = Field(default_factory=dict)

    @field_validator("data")
    @classmethod
    def _data_has_no_privileged_keys(cls, value: JsonDict) -> JsonDict:
        assert_no_privileged_keys(value, "RuntimeEvent.data")
        return value


class OracleAnnotation(StrictSchema):
    annotation_id: str
    episode_id: str
    timestamp_s: float = Field(ge=0)
    decision_id: str | None = None
    true_failure_cause: str | None = None
    true_temporal_profile: str | None = None
    true_failure_family: str | None = None
    oracle_action: RecoveryAction | None = None
    oracle_action_label: str | None = None
    mujoco_object_id: str | None = None
    mujoco_object_ids: list[str] = Field(default_factory=list)
    ground_truth_target_pose: Pose3D | None = None
    simulator_semantic_label: str | None = None
    simulator_semantic_labels: list[str] = Field(default_factory=list)
    privileged_metrics: JsonDict = Field(default_factory=dict)
    notes: str = ""


class EpisodeManifest(StrictSchema):
    episode_id: str
    schema_version: str = "edp.v0"
    created_at_utc: datetime = Field(default_factory=lambda: datetime.now(UTC))
    retention_class: RetentionClass = "pilot_evaluation"
    scenario_id: str = "unselected"
    scenario_seed: int | None = None
    policy_name: str = "unselected"
    policy_training_seed: int | None = None
    controller_backend: str = "unselected"
    robot_model: str = "unselected"
    code_version: str = "uncommitted"
    metadata: JsonDict = Field(default_factory=dict)

    @field_validator("metadata")
    @classmethod
    def _metadata_has_no_privileged_keys(cls, value: JsonDict) -> JsonDict:
        assert_no_privileged_keys(value, "EpisodeManifest.metadata")
        return value


class EpisodeMetrics(StrictSchema):
    episode_id: str
    task_success: bool | None = None
    recovery_success: bool | None = None
    policy_only_outcome: str | None = None
    full_stack_with_fallback_outcome: str | None = None
    fallback_invocation_count: int = Field(default=0, ge=0)
    safety_override_count: int = Field(default=0, ge=0)
    fall_count: int = Field(default=0, ge=0)
    unsafe_completion: bool = False
    recovery_latency_s: float | None = Field(default=None, ge=0)
    total_duration_s: float | None = Field(default=None, ge=0)
    custom_metrics: JsonDict = Field(default_factory=dict)

    @field_validator("custom_metrics")
    @classmethod
    def _custom_metrics_have_no_privileged_keys(cls, value: JsonDict) -> JsonDict:
        assert_no_privileged_keys(value, "EpisodeMetrics.custom_metrics")
        return value


class ReplayArtifactRecord(StrictSchema):
    artifact_id: str
    kind: Literal["timeseries", "rgb", "depth", "mask", "video", "snapshot", "other"]
    relative_path: str
    sha256: str | None = None
    media_type: str | None = None
    retention_class: RetentionClass = "pilot_evaluation"
    metadata: JsonDict = Field(default_factory=dict)

    @field_validator("relative_path")
    @classmethod
    def _relative_path_must_be_local(cls, value: str) -> str:
        if value.startswith("/") or ".." in value.split("/"):
            raise ValueError("replay artifact paths must be relative to the EDP root")
        return value

    @field_validator("metadata")
    @classmethod
    def _metadata_has_no_privileged_keys(cls, value: JsonDict) -> JsonDict:
        assert_no_privileged_keys(value, "ReplayArtifactRecord.metadata")
        return value


class EpisodeReplayIndex(StrictSchema):
    episode_id: str
    artifacts: list[ReplayArtifactRecord] = Field(default_factory=list)


def serialize_policy_observation(observation: PolicyObservation) -> JsonDict:
    """Return the policy-facing observation payload after leakage checks."""
    return observation.to_policy_dict()

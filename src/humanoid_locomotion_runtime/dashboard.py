"""Dashboard-facing contracts for Mac-safe replay/debugging skeletons."""

from __future__ import annotations

from dataclasses import dataclass, field

from pydantic import Field, field_validator

from humanoid_locomotion_runtime.navigator import LocalRoute
from humanoid_locomotion_runtime.schemas import (
    CommandMode,
    FailureEvent,
    JsonDict,
    LocomotionCommand,
    LocomotionStatus,
    MemoryTarget,
    RecoveryActionRecord,
    RuntimeEvent,
    StrictSchema,
    Vector3,
    assert_no_privileged_keys,
)

ALLOWED_DASHBOARD_COMMAND_MODES: tuple[CommandMode, ...] = (
    "stand_ready",
    "track_velocity",
    "walk_to",
    "turn_to",
    "safe_stop",
    "recover",
)
LOW_LEVEL_COMMAND_METADATA_KEYS = frozenset(
    {
        "actuator_commands",
        "actuator_targets",
        "joint_targets",
        "joint_torques",
        "motor_currents",
        "pd_gains",
    }
)


class DashboardFrame(StrictSchema):
    frame_id: str
    episode_id: str
    timestamp_s: float = Field(ge=0)
    status: LocomotionStatus
    active_command: LocomotionCommand | None = None
    memory_targets: list[MemoryTarget] = Field(default_factory=list)
    recent_failures: list[FailureEvent] = Field(default_factory=list)
    recovery_actions: list[RecoveryActionRecord] = Field(default_factory=list)
    runtime_events: list[RuntimeEvent] = Field(default_factory=list)
    local_route: LocalRoute | None = None
    metadata: JsonDict = Field(default_factory=dict)

    @field_validator("metadata")
    @classmethod
    def _metadata_has_no_privileged_keys(cls, value: JsonDict) -> JsonDict:
        assert_no_privileged_keys(value, "DashboardFrame.metadata")
        return value


class DashboardSummary(StrictSchema):
    episode_id: str
    frame_count: int = Field(ge=0)
    event_count: int = Field(ge=0)
    failure_count: int = Field(ge=0)
    recovery_action_count: int = Field(ge=0)
    safety_event_count: int = Field(ge=0)
    allowed_command_modes: list[CommandMode]
    metadata: JsonDict = Field(default_factory=dict)

    @field_validator("metadata")
    @classmethod
    def _metadata_has_no_privileged_keys(cls, value: JsonDict) -> JsonDict:
        assert_no_privileged_keys(value, "DashboardSummary.metadata")
        return value


@dataclass
class ViserDashboardPublisher:
    """In-memory dashboard publisher; does not require Viser or a browser."""

    frames: list[DashboardFrame] = field(default_factory=list)

    def publish_frame(self, frame: DashboardFrame) -> DashboardFrame:
        assert_no_privileged_keys(frame, "ViserDashboardPublisher.publish_frame")
        self.frames.append(frame)
        return frame

    def build_summary(self, *, episode_id: str) -> DashboardSummary:
        episode_frames = [frame for frame in self.frames if frame.episode_id == episode_id]
        event_count = sum(len(frame.runtime_events) for frame in episode_frames)
        failure_count = sum(len(frame.recent_failures) for frame in episode_frames)
        recovery_count = sum(len(frame.recovery_actions) for frame in episode_frames)
        safety_count = sum(
            1
            for frame in episode_frames
            for event in frame.runtime_events
            if event.event_type == "safety"
        )
        return DashboardSummary(
            episode_id=episode_id,
            frame_count=len(episode_frames),
            event_count=event_count,
            failure_count=failure_count,
            recovery_action_count=recovery_count,
            safety_event_count=safety_count,
            allowed_command_modes=list(ALLOWED_DASHBOARD_COMMAND_MODES),
            metadata={"dashboard_scope": "mac_safe_in_memory_publisher"},
        )

    def make_high_level_command(
        self,
        *,
        command_id: str,
        mode: CommandMode,
        issued_at_s: float,
        episode_id: str,
        language: str | None = None,
        target_pose: tuple[float, float, float] | None = None,
        velocity_xy_yaw: Vector3 | None = None,
        metadata: JsonDict | None = None,
    ) -> LocomotionCommand:
        if mode not in ALLOWED_DASHBOARD_COMMAND_MODES:
            raise ValueError(f"dashboard command mode is not allowed: {mode}")
        checked_metadata: JsonDict = {"episode_id": episode_id}
        if metadata:
            low_level_keys = sorted(LOW_LEVEL_COMMAND_METADATA_KEYS.intersection(metadata))
            if low_level_keys:
                joined = ", ".join(low_level_keys)
                raise ValueError(f"dashboard command metadata contains low-level keys: {joined}")
            checked_metadata.update(metadata)
        return LocomotionCommand(
            command_id=command_id,
            mode=mode,
            issued_at_s=issued_at_s,
            language=language,
            target_pose=target_pose,
            velocity_xy_yaw=velocity_xy_yaw,
            metadata=checked_metadata,
        )

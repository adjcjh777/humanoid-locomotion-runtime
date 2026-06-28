from __future__ import annotations

import pytest
from pydantic import ValidationError

from humanoid_locomotion_runtime.dashboard import DashboardFrame, ViserDashboardPublisher
from humanoid_locomotion_runtime.schemas import (
    FailureEvent,
    LocomotionStatus,
    RecoveryActionRecord,
    RuntimeEvent,
)


def make_status() -> LocomotionStatus:
    return LocomotionStatus(
        timestamp_s=1.0,
        base_position=(0.0, 0.0, 0.8),
        base_orientation_quat=(1.0, 0.0, 0.0, 0.0),
        linear_velocity=(0.0, 0.0, 0.0),
        angular_velocity=(0.0, 0.0, 0.0),
        stability_margin=0.4,
        localization_quality=0.9,
        tracking_error=0.0,
    )


def test_dashboard_publisher_builds_summary_from_runtime_legal_frames() -> None:
    publisher = ViserDashboardPublisher()
    frame = DashboardFrame(
        frame_id="frame-001",
        episode_id="episode-001",
        timestamp_s=1.0,
        status=make_status(),
        runtime_events=[
            RuntimeEvent(
                event_id="evt-001",
                episode_id="episode-001",
                timestamp_s=1.0,
                event_type="safety",
                message="blocked command",
            )
        ],
        recent_failures=[
            FailureEvent(
                failure_id="failure-001",
                timestamp_s=1.0,
                runtime_failure_kind="local_route_blocked",
                severity=0.7,
            )
        ],
        recovery_actions=[
            RecoveryActionRecord(
                record_id="rec-001",
                episode_id="episode-001",
                timestamp_s=1.0,
                action="safe_stop",
                available_actions=["continue", "safe_stop"],
                policy_name="rule_recovery_tuned",
            )
        ],
    )

    publisher.publish_frame(frame)
    summary = publisher.build_summary(episode_id="episode-001")

    assert summary.frame_count == 1
    assert summary.event_count == 1
    assert summary.safety_event_count == 1
    assert summary.failure_count == 1
    assert summary.recovery_action_count == 1
    assert "walk_to" in summary.allowed_command_modes


def test_dashboard_creates_high_level_commands_and_rejects_low_level_metadata() -> None:
    publisher = ViserDashboardPublisher()

    command = publisher.make_high_level_command(
        command_id="cmd-001",
        mode="track_velocity",
        issued_at_s=1.0,
        episode_id="episode-001",
        velocity_xy_yaw=(0.1, 0.0, 0.0),
    )

    assert command.mode == "track_velocity"
    assert command.metadata["episode_id"] == "episode-001"

    with pytest.raises(ValueError, match="low-level keys"):
        publisher.make_high_level_command(
            command_id="cmd-bad",
            mode="safe_stop",
            issued_at_s=1.0,
            episode_id="episode-001",
            metadata={"joint_targets": [0.0, 0.1]},
        )


def test_dashboard_frame_rejects_privileged_metadata() -> None:
    with pytest.raises(ValidationError, match="oracle_action"):
        DashboardFrame(
            frame_id="frame-bad",
            episode_id="episode-001",
            timestamp_s=1.0,
            status=make_status(),
            metadata={"nested": {"oracle_action": "safe_stop"}},
        )

from __future__ import annotations

import pytest
from pydantic import ValidationError

from humanoid_locomotion_runtime.runtime_manager import (
    FakeRuntimeBackend,
    RuntimeCommandEnvelope,
    RuntimeManager,
    SafetyDecision,
    SafetySupervisor,
)
from humanoid_locomotion_runtime.schemas import BodyMemoryState, LocomotionCommand, LocomotionStatus


def make_status(*, stability_margin: float = 0.5) -> LocomotionStatus:
    return LocomotionStatus(
        timestamp_s=1.0,
        base_position=(0.0, 0.0, 0.8),
        base_orientation_quat=(1.0, 0.0, 0.0, 0.0),
        linear_velocity=(0.0, 0.0, 0.0),
        angular_velocity=(0.0, 0.0, 0.0),
        stability_margin=stability_margin,
        localization_quality=0.9,
        tracking_error=0.0,
    )


def make_body_memory(*, balance_risk: float = 0.1) -> BodyMemoryState:
    return BodyMemoryState(
        timestamp_s=1.0,
        balance_risk=balance_risk,
        slip_risk=0.1,
        fatigue_score=0.0,
        localization_quality=0.9,
        tracking_error_trend=0.0,
        trend_window_s=2.0,
    )


def test_runtime_manager_routes_high_level_track_velocity_to_fake_backend() -> None:
    backend = FakeRuntimeBackend()
    manager = RuntimeManager(backend=backend)
    command = LocomotionCommand(
        command_id="cmd-track",
        mode="track_velocity",
        issued_at_s=1.0,
        velocity_xy_yaw=(0.2, 0.0, 0.0),
        metadata={"episode_id": "episode-001"},
    )

    event = manager.issue_command(
        command,
        status=make_status(),
        body_memory=make_body_memory(),
    )

    assert event.event_type == "command"
    assert event.data["mode"] == "track_velocity"
    assert event.data["mac_safe_scope"] == "fake_backend_only"
    assert len(backend.executed_envelopes) == 1
    assert backend.executed_envelopes[0].authorized_by_runtime_manager is True


def test_runtime_manager_validates_mode_specific_command_shape() -> None:
    manager = RuntimeManager()

    with pytest.raises(ValueError, match="velocity_xy_yaw"):
        manager.issue_command(
            LocomotionCommand(command_id="cmd-bad", mode="track_velocity", issued_at_s=1.0)
        )

    with pytest.raises(ValueError, match="target_pose"):
        manager.issue_command(
            LocomotionCommand(command_id="cmd-walk", mode="walk_to", issued_at_s=1.0)
        )


def test_safety_supervisor_blocks_unsafe_motion_without_backend_execution() -> None:
    backend = FakeRuntimeBackend()
    manager = RuntimeManager(
        backend=backend,
        safety_supervisor=SafetySupervisor(balance_risk_stop_threshold=0.8),
    )
    command = LocomotionCommand(
        command_id="cmd-walk",
        mode="walk_to",
        issued_at_s=1.0,
        target_pose=(1.0, 0.0, 0.0),
    )

    event = manager.issue_command(
        command,
        status=make_status(),
        body_memory=make_body_memory(balance_risk=0.95),
    )

    assert event.event_type == "safety"
    assert event.data["blocked_mode"] == "walk_to"
    assert event.data["requested_mode"] == "safe_stop"
    assert backend.executed_envelopes == []


def test_safe_stop_remains_routable_under_high_risk() -> None:
    backend = FakeRuntimeBackend()
    manager = RuntimeManager(backend=backend)
    command = LocomotionCommand(command_id="cmd-stop", mode="safe_stop", issued_at_s=1.0)

    event = manager.issue_command(
        command,
        status=make_status(stability_margin=0.0),
        body_memory=make_body_memory(balance_risk=1.0),
    )

    assert event.event_type == "command"
    assert event.data["mode"] == "safe_stop"
    assert len(backend.executed_envelopes) == 1


def test_fake_backend_rejects_raw_command_bypass() -> None:
    backend = FakeRuntimeBackend()
    command = LocomotionCommand(command_id="cmd-stop", mode="safe_stop", issued_at_s=1.0)

    with pytest.raises(TypeError, match="RuntimeManager"):
        backend.execute(command)  # type: ignore[arg-type]


def test_runtime_command_envelope_and_safety_decision_reject_privileged_metadata() -> None:
    command = LocomotionCommand(command_id="cmd-stop", mode="safe_stop", issued_at_s=1.0)

    with pytest.raises(ValidationError, match="oracle_action"):
        SafetyDecision(
            decision_kind="allow",
            reason="bad",
            metadata={"nested": {"oracle_action": "safe_stop"}},
        )

    with pytest.raises(ValidationError, match="mujoco_object_id"):
        RuntimeCommandEnvelope(
            route_id="route-0001",
            command=command,
            safety_decision=SafetyDecision(decision_kind="allow", reason="ok"),
            metadata={"runtime_context": {"mujoco_object_id": "object-42"}},
        )

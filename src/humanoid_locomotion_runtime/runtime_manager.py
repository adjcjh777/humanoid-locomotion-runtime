"""Backend-neutral RuntimeManager and SafetySupervisor skeletons.

These classes are Mac-safe scaffolding only. They route high-level typed
commands through a fake backend so tests can verify boundaries before MuJoCo or
controller integration exists.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from pydantic import Field, field_validator

from humanoid_locomotion_runtime.schemas import (
    BodyMemoryState,
    CommandMode,
    JsonDict,
    LocomotionCommand,
    LocomotionStatus,
    RuntimeEvent,
    StrictSchema,
    assert_no_privileged_keys,
)

SafetyDecisionKind = Literal["allow", "block_and_request_safe_stop"]


class SafetyDecision(StrictSchema):
    decision_kind: SafetyDecisionKind
    reason: str
    requested_mode: CommandMode | None = None
    metadata: JsonDict = Field(default_factory=dict)

    @property
    def allowed(self) -> bool:
        return self.decision_kind == "allow"

    @field_validator("metadata")
    @classmethod
    def _metadata_has_no_privileged_keys(cls, value: JsonDict) -> JsonDict:
        assert_no_privileged_keys(value, "SafetyDecision.metadata")
        return value


class RuntimeCommandEnvelope(StrictSchema):
    route_id: str
    command: LocomotionCommand
    safety_decision: SafetyDecision
    backend_name: str = "fake_runtime_backend"
    authorized_by_runtime_manager: bool = True
    metadata: JsonDict = Field(default_factory=dict)

    @field_validator("metadata")
    @classmethod
    def _metadata_has_no_privileged_keys(cls, value: JsonDict) -> JsonDict:
        assert_no_privileged_keys(value, "RuntimeCommandEnvelope.metadata")
        return value


class SafetySupervisor:
    """Minimal safety shield for high-level command routing tests."""

    def __init__(
        self,
        *,
        balance_risk_stop_threshold: float = 0.9,
        stability_margin_stop_threshold: float = 0.05,
    ) -> None:
        self.balance_risk_stop_threshold = balance_risk_stop_threshold
        self.stability_margin_stop_threshold = stability_margin_stop_threshold

    def evaluate(
        self,
        command: LocomotionCommand,
        *,
        status: LocomotionStatus | None = None,
        body_memory: BodyMemoryState | None = None,
    ) -> SafetyDecision:
        if command.mode == "safe_stop":
            return SafetyDecision(decision_kind="allow", reason="safe_stop is always routable")

        if body_memory is not None and body_memory.balance_risk >= self.balance_risk_stop_threshold:
            return SafetyDecision(
                decision_kind="block_and_request_safe_stop",
                reason="balance risk exceeds safe-stop threshold",
                requested_mode="safe_stop",
            )

        if (
            status is not None
            and status.stability_margin is not None
            and status.stability_margin <= self.stability_margin_stop_threshold
        ):
            return SafetyDecision(
                decision_kind="block_and_request_safe_stop",
                reason="stability margin is below safe-stop threshold",
                requested_mode="safe_stop",
            )

        return SafetyDecision(decision_kind="allow", reason="risk checks passed")


@dataclass
class FakeRuntimeBackend:
    """Fake backend that only accepts RuntimeManager-created envelopes."""

    name: str = "fake_runtime_backend"
    executed_envelopes: list[RuntimeCommandEnvelope] = field(default_factory=list)

    def execute(self, envelope: RuntimeCommandEnvelope) -> RuntimeEvent:
        if not isinstance(envelope, RuntimeCommandEnvelope):
            raise TypeError("backend commands must be routed through RuntimeManager")
        if not envelope.authorized_by_runtime_manager:
            raise ValueError("backend envelope is not authorized by RuntimeManager")

        self.executed_envelopes.append(envelope)
        return RuntimeEvent(
            event_id=f"evt-{envelope.route_id}",
            episode_id=envelope.command.metadata.get("episode_id", "episode-unselected"),
            timestamp_s=envelope.command.issued_at_s,
            event_type="command",
            message=f"fake backend accepted {envelope.command.mode}",
            data={
                "route_id": envelope.route_id,
                "command_id": envelope.command.command_id,
                "mode": envelope.command.mode,
                "backend_name": self.name,
                "mac_safe_scope": "fake_backend_only",
            },
        )


class RuntimeManager:
    """Single high-level command entry point for Mac-safe skeleton tests."""

    def __init__(
        self,
        *,
        safety_supervisor: SafetySupervisor | None = None,
        backend: FakeRuntimeBackend | None = None,
    ) -> None:
        self.safety_supervisor = safety_supervisor or SafetySupervisor()
        self.backend = backend or FakeRuntimeBackend()
        self._next_route_index = 1

    def route_command(
        self,
        command: LocomotionCommand,
        *,
        status: LocomotionStatus | None = None,
        body_memory: BodyMemoryState | None = None,
    ) -> RuntimeCommandEnvelope:
        self._validate_command_shape(command)
        decision = self.safety_supervisor.evaluate(
            command,
            status=status,
            body_memory=body_memory,
        )
        route_id = f"route-{self._next_route_index:04d}"
        self._next_route_index += 1
        return RuntimeCommandEnvelope(
            route_id=route_id,
            command=command,
            safety_decision=decision,
            backend_name=self.backend.name,
        )

    def issue_command(
        self,
        command: LocomotionCommand,
        *,
        status: LocomotionStatus | None = None,
        body_memory: BodyMemoryState | None = None,
    ) -> RuntimeEvent:
        envelope = self.route_command(command, status=status, body_memory=body_memory)
        if not envelope.safety_decision.allowed:
            return RuntimeEvent(
                event_id=f"evt-{envelope.route_id}",
                episode_id=command.metadata.get("episode_id", "episode-unselected"),
                timestamp_s=command.issued_at_s,
                event_type="safety",
                message="SafetySupervisor blocked command and requested safe_stop",
                data={
                    "route_id": envelope.route_id,
                    "command_id": command.command_id,
                    "blocked_mode": command.mode,
                    "requested_mode": envelope.safety_decision.requested_mode,
                    "reason": envelope.safety_decision.reason,
                    "mac_safe_scope": "fake_backend_only",
                },
            )
        return self.backend.execute(envelope)

    @staticmethod
    def _validate_command_shape(command: LocomotionCommand) -> None:
        if command.mode == "track_velocity" and command.velocity_xy_yaw is None:
            raise ValueError("track_velocity command requires velocity_xy_yaw")
        if command.mode in {"walk_to", "turn_to"} and command.target_pose is None:
            raise ValueError(f"{command.mode} command requires target_pose")

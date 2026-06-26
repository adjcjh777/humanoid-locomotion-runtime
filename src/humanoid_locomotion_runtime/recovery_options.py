"""Recovery option/SMDP contracts for Gate C.

The contracts are deliberately high level: they describe what RuntimeManager may
ask the runtime stack to do, not low-level joint, gait, or actuator commands.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Literal, get_args

from pydantic import Field, model_validator

from humanoid_locomotion_runtime.schemas import PRIVILEGED_FIELD_NAMES, RecoveryAction, StrictSchema

OptionInterruptibility = Literal[
    "safety_interruptible",
    "option_boundary_interruptible",
    "runtime_interruptible",
]


class RecoveryOptionContract(StrictSchema):
    action: RecoveryAction
    initiation_conditions: tuple[str, ...] = Field(min_length=1)
    action_mask_conditions: tuple[str, ...] = Field(min_length=1)
    implementation_stub: str = Field(min_length=1)
    min_duration_s: float = Field(ge=0)
    max_duration_s: float = Field(gt=0)
    success_conditions: tuple[str, ...] = Field(min_length=1)
    failure_conditions: tuple[str, ...] = Field(min_length=1)
    termination_conditions: tuple[str, ...] = Field(min_length=1)
    interruptibility: OptionInterruptibility
    retry_budget: int = Field(ge=0)
    cooldown_s: float = Field(ge=0)
    legal_runtime_signals: tuple[str, ...] = Field(min_length=1)
    note: str = ""

    @model_validator(mode="after")
    def _duration_and_signal_boundary_are_valid(self) -> RecoveryOptionContract:
        if self.max_duration_s < self.min_duration_s:
            raise ValueError("max_duration_s must be greater than or equal to min_duration_s")

        privileged_signal_names = {
            signal
            for signal in self.legal_runtime_signals
            if signal in PRIVILEGED_FIELD_NAMES or signal.split(".")[-1] in PRIVILEGED_FIELD_NAMES
        }
        if privileged_signal_names:
            joined = ", ".join(sorted(privileged_signal_names))
            raise ValueError(f"legal_runtime_signals include privileged fields: {joined}")

        return self


RECOVERY_ACTIONS: tuple[RecoveryAction, ...] = get_args(RecoveryAction)

RECOVERY_OPTION_CONTRACTS: dict[RecoveryAction, RecoveryOptionContract] = {
    "continue": RecoveryOptionContract(
        action="continue",
        initiation_conditions=("command is active", "no active safety override"),
        action_mask_conditions=("not masked by repeated identical failure at same decision epoch",),
        implementation_stub="RuntimeManager keeps the current high-level command active.",
        min_duration_s=0.1,
        max_duration_s=2.0,
        success_conditions=("status remains stable through one option boundary",),
        failure_conditions=("failure evidence worsens or a safety override is requested",),
        termination_conditions=(
            "next decision epoch",
            "active command completes",
            "safety override",
        ),
        interruptibility="runtime_interruptible",
        retry_budget=2,
        cooldown_s=0.0,
        legal_runtime_signals=(
            "LocomotionStatus.stability_margin",
            "LocomotionStatus.tracking_error",
            "BodyMemoryState.balance_risk",
            "FailureEvent.runtime_failure_kind",
        ),
        note="Default no-op supervisory option; it never bypasses RuntimeManager.",
    ),
    "slow_down": RecoveryOptionContract(
        action="slow_down",
        initiation_conditions=("tracking error, slip risk, or balance risk is elevated",),
        action_mask_conditions=("not already at the minimum allowed commanded speed",),
        implementation_stub=(
            "RuntimeManager requests a bounded reduction of the high-level velocity command."
        ),
        min_duration_s=0.5,
        max_duration_s=5.0,
        success_conditions=("tracking error trend decreases", "balance risk does not increase"),
        failure_conditions=(
            "fall risk increases",
            "tracking error remains saturated until timeout",
        ),
        termination_conditions=("success condition is stable", "timeout", "safety override"),
        interruptibility="runtime_interruptible",
        retry_budget=2,
        cooldown_s=1.0,
        legal_runtime_signals=(
            "LocomotionStatus.tracking_error",
            "LocomotionStatus.linear_velocity",
            "BodyMemoryState.tracking_error_trend",
            "BodyMemoryState.slip_risk",
            "BodyMemoryState.balance_risk",
        ),
    ),
    "safe_stop": RecoveryOptionContract(
        action="safe_stop",
        initiation_conditions=("safety supervisor reports elevated risk",),
        action_mask_conditions=("never masked when SafetySupervisor requests stop",),
        implementation_stub=(
            "RuntimeManager requests the frozen controller's high-level safe-stop path."
        ),
        min_duration_s=0.5,
        max_duration_s=10.0,
        success_conditions=("base velocity is near zero", "stability margin is acceptable"),
        failure_conditions=("robot becomes unstable before stopping",),
        termination_conditions=("stable stop", "safety supervisor escalates", "timeout"),
        interruptibility="safety_interruptible",
        retry_budget=0,
        cooldown_s=0.0,
        legal_runtime_signals=(
            "LocomotionStatus.linear_velocity",
            "LocomotionStatus.angular_velocity",
            "LocomotionStatus.stability_margin",
            "BodyMemoryState.balance_risk",
        ),
        note="Safety option; it is high-level and still routed through SafetySupervisor.",
    ),
    "local_replan": RecoveryOptionContract(
        action="local_replan",
        initiation_conditions=("local path is blocked or repeated local progress stalls",),
        action_mask_conditions=("a target estimate exists", "planner is not in cooldown"),
        implementation_stub="RuntimeManager asks NavigatorV0 for a bounded local path refresh.",
        min_duration_s=0.5,
        max_duration_s=6.0,
        success_conditions=("planner returns a legal local route", "progress resumes"),
        failure_conditions=("planner cannot find a legal local route", "timeout"),
        termination_conditions=("new route accepted", "planner failure", "safety override"),
        interruptibility="runtime_interruptible",
        retry_budget=2,
        cooldown_s=2.0,
        legal_runtime_signals=(
            "MemoryTarget.estimated_pose",
            "MemoryTarget.confidence",
            "runtime_context.planner_blocked",
            "FailureEvent.runtime_failure_kind",
        ),
    ),
    "recover_balance": RecoveryOptionContract(
        action="recover_balance",
        initiation_conditions=("balance risk is elevated but safe-stop is not yet mandatory",),
        action_mask_conditions=("controller reports recover mode is available",),
        implementation_stub=(
            "RuntimeManager requests the controller's high-level balance recovery mode."
        ),
        min_duration_s=0.2,
        max_duration_s=4.0,
        success_conditions=("balance risk falls below threshold", "stability margin recovers"),
        failure_conditions=("balance risk increases", "safety stop is requested"),
        termination_conditions=("balance recovered", "safe_stop takeover", "timeout"),
        interruptibility="safety_interruptible",
        retry_budget=1,
        cooldown_s=1.5,
        legal_runtime_signals=(
            "LocomotionStatus.stability_margin",
            "BodyMemoryState.balance_risk",
            "BodyMemoryState.recent_contact_events",
            "FailureEvent.severity",
        ),
    ),
    "relocalize": RecoveryOptionContract(
        action="relocalize",
        initiation_conditions=("localization quality is low or drifting",),
        action_mask_conditions=("relocalization sensor summary is available",),
        implementation_stub="RuntimeManager pauses task progress and refreshes localization state.",
        min_duration_s=0.5,
        max_duration_s=8.0,
        success_conditions=("localization quality returns above threshold",),
        failure_conditions=("localization quality remains below threshold until timeout",),
        termination_conditions=("quality recovered", "abort threshold reached", "safety override"),
        interruptibility="runtime_interruptible",
        retry_budget=1,
        cooldown_s=3.0,
        legal_runtime_signals=(
            "LocomotionStatus.localization_quality",
            "BodyMemoryState.localization_quality",
            "FailureEvent.temporal_profile_hint",
            "runtime_context.localization_drift_hint",
        ),
    ),
    "refresh_target_grounding": RecoveryOptionContract(
        action="refresh_target_grounding",
        initiation_conditions=("target confidence is low, stale, or ambiguous",),
        action_mask_conditions=("camera summary or grounding adapter output is available",),
        implementation_stub="RuntimeManager requests a bounded refresh from the grounding adapter.",
        min_duration_s=0.5,
        max_duration_s=7.0,
        success_conditions=("target confidence improves", "target estimate becomes usable"),
        failure_conditions=("target remains ambiguous or stale until timeout",),
        termination_conditions=(
            "target refreshed",
            "relocalize or abort threshold reached",
            "timeout",
        ),
        interruptibility="runtime_interruptible",
        retry_budget=2,
        cooldown_s=2.5,
        legal_runtime_signals=(
            "MemoryTarget.confidence",
            "MemoryTarget.last_seen_s",
            "MemoryTarget.label",
            "runtime_context.grounding_ambiguity_score",
        ),
    ),
    "abort_task": RecoveryOptionContract(
        action="abort_task",
        initiation_conditions=("retry budget is exhausted or continued execution is unsafe",),
        action_mask_conditions=("not masked after SafetySupervisor marks task unsafe",),
        implementation_stub=(
            "RuntimeManager terminates the task and enters the safe high-level end state."
        ),
        min_duration_s=0.1,
        max_duration_s=3.0,
        success_conditions=("task is marked aborted", "no further motion command is issued"),
        failure_conditions=("abort acknowledgement is not recorded before timeout",),
        termination_conditions=("abort acknowledged", "safe_stop takeover", "timeout"),
        interruptibility="safety_interruptible",
        retry_budget=0,
        cooldown_s=0.0,
        legal_runtime_signals=(
            "FailureEvent.severity",
            "runtime_context.retry_budget_remaining",
            "runtime_context.safety_override_requested",
            "LocomotionStatus.stability_margin",
        ),
        note="Terminal high-level option; not a low-level emergency controller bypass.",
    ),
}


def validate_recovery_option_catalog(
    contracts: Mapping[RecoveryAction, RecoveryOptionContract] = RECOVERY_OPTION_CONTRACTS,
) -> None:
    """Validate coverage and key/action consistency for the option catalog."""
    expected_actions = set(RECOVERY_ACTIONS)
    observed_actions = set(contracts)
    if observed_actions != expected_actions:
        raise ValueError(
            "recovery option catalog action coverage mismatch: "
            f"expected {sorted(expected_actions)}, observed {sorted(observed_actions)}"
        )

    for key, contract in contracts.items():
        if key != contract.action:
            raise ValueError(
                f"catalog key {key!r} does not match contract action {contract.action!r}"
            )


validate_recovery_option_catalog()

"""Bounded self-improvement memory and promotion contracts.

These schemas model only offline, high-level strategy updates. They do not
authorize low-level controller changes or safety-path overrides.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any, Literal, Self

from pydantic import BaseModel, Field, field_validator, model_validator

from humanoid_locomotion_runtime.schemas import (
    JsonDict,
    StrictSchema,
    assert_no_privileged_keys,
)

StrategyMemoryStatus = Literal["candidate", "validated", "promoted", "rejected", "rolled_back"]
StrategyValidationStatus = Literal["pending", "passed", "failed", "deferred"]

CandidateUpdateKind = Literal[
    "recovery_priority_update",
    "command_parameter_update",
    "planner_cost_update",
    "grounding_retry_update",
    "abort_safe_stop_policy_update",
]

CandidateAllowedScope = Literal[
    "high_level_recovery_selector_only",
    "high_level_command_parameters_only",
    "local_planner_costs_only",
    "grounding_retry_order_only",
    "abort_safe_stop_policy_only",
]

ForbiddenUpdateScope = Literal[
    "low_level_controller_checkpoint",
    "joint_action_output",
    "SafetySupervisor_override",
    "hard_stop_path",
    "RuntimeManager_bypass",
]

CandidateUpdateStatus = Literal[
    "candidate",
    "validating",
    "rejected",
    "promoted",
    "rolled_back",
]

GateSIVerdict = Literal[
    "PROMOTE",
    "REJECT",
    "NEEDS_MORE_EVIDENCE",
    "ROLLBACK_REQUIRED",
    "DEFER_UNTIL_SNAPSHOT_BRANCHING",
]

GateSIFailureReason = Literal[
    "insufficient_gain",
    "safety_regression",
    "negative_control_leakage",
    "over_conservative_policy",
    "not_memory_specific",
    "snapshot_unavailable",
    "controller_not_frozen",
    "edp_invalid",
    "oracle_leakage",
    "validation_not_reproducible",
]

REQUIRED_FORBIDDEN_UPDATE_SCOPES = frozenset(
    {
        "low_level_controller_checkpoint",
        "joint_action_output",
        "SafetySupervisor_override",
        "hard_stop_path",
    }
)

ALLOWED_PROPOSED_BEHAVIOR_KEYS_BY_KIND: dict[str, frozenset[str]] = {
    "recovery_priority_update": frozenset(
        {
            "kind",
            "prefer",
            "avoid",
            "priority_order",
            "priority_delta",
            "trigger_threshold_delta",
            "vx_cap",
            "vy_cap",
            "yaw_rate_cap",
            "max_vx",
            "min_confidence",
            "cooldown_s",
            "retry_budget",
        }
    ),
    "command_parameter_update": frozenset(
        {
            "kind",
            "vx_cap",
            "vy_cap",
            "yaw_rate_cap",
            "max_vx",
            "max_vy",
            "max_yaw_rate",
            "speed_hint",
            "target_tolerance_m",
            "turn_rate_cap",
            "command_duration_cap_s",
            "command_mode",
        }
    ),
    "planner_cost_update": frozenset(
        {
            "kind",
            "obstacle_class",
            "obstacle_label",
            "clearance_cost_delta",
            "clearance_margin_m",
            "cost_multiplier",
            "local_planner_profile",
            "planner_cell",
            "avoid_radius_m",
            "cooldown_s",
        }
    ),
    "grounding_retry_update": frozenset(
        {
            "kind",
            "confidence_threshold",
            "stale_after_s",
            "retry_order",
            "max_retries",
            "prefer",
            "avoid",
            "grounding_refresh_mode",
            "cooldown_s",
        }
    ),
    "abort_safe_stop_policy_update": frozenset(
        {
            "kind",
            "prefer",
            "avoid",
            "safe_stop_latency_cap_s",
            "abort_after_retries",
            "progress_drop_cap_pp",
            "balance_risk_pre_stop_margin",
            "stability_margin_min",
            "cooldown_s",
        }
    ),
}

FORBIDDEN_UPDATE_FIELD_NAMES = frozenset(
    {
        "low_level_controller_checkpoint",
        "low_level_controller_weights",
        "low_level_policy_checkpoint",
        "controller_checkpoint",
        "controller_weights",
        "joint_action_output",
        "joint_position_target",
        "joint_velocity_target",
        "joint_torque",
        "actuator_command",
        "actuator_torque",
        "SafetySupervisor_override",
        "safety_supervisor_override",
        "hard_stop_path",
        "RuntimeManager_bypass",
        "runtime_manager_bypass",
    }
)

_FORBIDDEN_UPDATE_FIELD_NAMES_CASEFOLD = {
    field_name.casefold() for field_name in FORBIDDEN_UPDATE_FIELD_NAMES
}


def find_forbidden_update_key_paths(value: Any, path: str = "$") -> list[str]:
    """Return JSON-like paths that try to modify forbidden runtime surfaces."""
    if isinstance(value, BaseModel):
        value = value.model_dump(mode="json")

    if isinstance(value, Mapping):
        found: list[str] = []
        for key, item in value.items():
            key_text = str(key)
            item_path = f"{path}.{key_text}"
            if key_text.casefold() in _FORBIDDEN_UPDATE_FIELD_NAMES_CASEFOLD:
                found.append(item_path)
            found.extend(find_forbidden_update_key_paths(item, item_path))
        return found

    if isinstance(value, Sequence) and not isinstance(value, str | bytes | bytearray):
        found = []
        for index, item in enumerate(value):
            found.extend(find_forbidden_update_key_paths(item, f"{path}[{index}]"))
        return found

    return []


def assert_no_forbidden_update_fields(value: Any, context: str = "candidate update") -> None:
    """Raise if an RSI-facing payload tries to alter low-level or safety surfaces."""
    paths = find_forbidden_update_key_paths(value)
    if paths:
        joined = ", ".join(sorted(paths))
        raise ValueError(f"{context} contains forbidden update fields: {joined}")


class StrategyMemoryRecord(StrictSchema):
    """Consolidated strategy memory that must be validated before promotion."""

    memory_type: Literal["strategy"] = "strategy"
    strategy_id: str
    source_failure_ids: list[str] = Field(min_length=1)
    source_edp_ids: list[str] = Field(default_factory=list)
    trigger: JsonDict
    recommended_update: JsonDict
    status: StrategyMemoryStatus = "candidate"
    validation_status: StrategyValidationStatus = "pending"
    candidate_update_ids: list[str] = Field(default_factory=list)
    metadata: JsonDict = Field(default_factory=dict)

    @field_validator("trigger")
    @classmethod
    def _trigger_has_runtime_legal_fields(cls, value: JsonDict) -> JsonDict:
        assert_no_privileged_keys(value, "StrategyMemoryRecord.trigger")
        assert_no_forbidden_update_fields(value, "StrategyMemoryRecord.trigger")
        return value

    @field_validator("recommended_update")
    @classmethod
    def _recommended_update_has_high_level_fields(cls, value: JsonDict) -> JsonDict:
        assert_no_privileged_keys(value, "StrategyMemoryRecord.recommended_update")
        assert_no_forbidden_update_fields(value, "StrategyMemoryRecord.recommended_update")
        return value

    @field_validator("metadata")
    @classmethod
    def _metadata_has_no_privileged_keys(cls, value: JsonDict) -> JsonDict:
        assert_no_privileged_keys(value, "StrategyMemoryRecord.metadata")
        return value


class CandidateUpdateManifest(StrictSchema):
    """Typed manifest for a bounded high-level runtime policy update."""

    schema_version: Literal["candidate_update_manifest_v0"] = "candidate_update_manifest_v0"
    candidate_id: str
    parent_policy_version: str
    source_edp_ids: list[str] = Field(default_factory=list)
    source_strategy_memory_ids: list[str] = Field(default_factory=list)
    update_kind: CandidateUpdateKind
    allowed_scope: CandidateAllowedScope
    forbidden_scope: list[ForbiddenUpdateScope] = Field(min_length=1)
    trigger_condition: JsonDict
    proposed_behavior: JsonDict
    validation_plan: JsonDict
    status: CandidateUpdateStatus = "candidate"
    metadata: JsonDict = Field(default_factory=dict)

    @field_validator(
        "trigger_condition",
        "proposed_behavior",
        "validation_plan",
        "metadata",
    )
    @classmethod
    def _runtime_payloads_are_bounded(cls, value: JsonDict, info) -> JsonDict:
        assert_no_privileged_keys(value, f"CandidateUpdateManifest.{info.field_name}")
        assert_no_forbidden_update_fields(value, f"CandidateUpdateManifest.{info.field_name}")
        return value

    @model_validator(mode="after")
    def _forbidden_scope_includes_core_safety_boundaries(self) -> Self:
        observed = set(self.forbidden_scope)
        missing = REQUIRED_FORBIDDEN_UPDATE_SCOPES - observed
        if missing:
            joined = ", ".join(sorted(missing))
            raise ValueError(f"forbidden_scope missing required safety boundaries: {joined}")

        allowed_behavior_keys = ALLOWED_PROPOSED_BEHAVIOR_KEYS_BY_KIND[self.update_kind]
        observed_behavior_keys = {str(key) for key in self.proposed_behavior}
        unknown_behavior_keys = observed_behavior_keys - allowed_behavior_keys
        if unknown_behavior_keys:
            joined = ", ".join(sorted(unknown_behavior_keys))
            raise ValueError(
                f"proposed_behavior keys not allowed for {self.update_kind}: {joined}"
            )

        return self


class PromotionReport(StrictSchema):
    """Gate SI promotion verdict for a candidate update."""

    schema_version: Literal["promotion_report_v0"] = "promotion_report_v0"
    report_id: str
    candidate_id: str
    parent_policy_version: str
    evaluated_policy_version: str
    strategy_memory_version: str
    verdict: GateSIVerdict
    metrics: JsonDict = Field(default_factory=dict)
    failure_reasons: list[GateSIFailureReason] = Field(default_factory=list)
    validation_report_path: str | None = None
    safety_report_path: str | None = None
    rollback_pointer: str | None = None
    evidence_artifacts: list[str] = Field(default_factory=list)
    metadata: JsonDict = Field(default_factory=dict)

    @field_validator("metrics", "metadata")
    @classmethod
    def _json_payloads_have_no_privileged_keys(cls, value: JsonDict, info) -> JsonDict:
        assert_no_privileged_keys(value, f"PromotionReport.{info.field_name}")
        return value

    @model_validator(mode="after")
    def _promoted_reports_keep_rollback_pointer(self) -> Self:
        if self.verdict == "PROMOTE" and self.rollback_pointer is None:
            raise ValueError("PROMOTE verdict requires rollback_pointer")
        return self


class RollbackManifest(StrictSchema):
    """Rollback pointer for a promoted or unsafe candidate update."""

    schema_version: Literal["rollback_manifest_v0"] = "rollback_manifest_v0"
    rollback_id: str
    candidate_id: str
    from_policy_version: str
    rollback_to_policy_version: str
    reason: GateSIFailureReason
    triggered_by_report_id: str | None = None
    safety_evidence: JsonDict = Field(default_factory=dict)
    rollback_artifacts: list[str] = Field(default_factory=list)
    metadata: JsonDict = Field(default_factory=dict)

    @field_validator("safety_evidence", "metadata")
    @classmethod
    def _json_payloads_have_no_privileged_keys(cls, value: JsonDict, info) -> JsonDict:
        assert_no_privileged_keys(value, f"RollbackManifest.{info.field_name}")
        return value

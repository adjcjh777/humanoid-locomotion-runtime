from __future__ import annotations

import pytest
from pydantic import ValidationError

from humanoid_locomotion_runtime.self_improvement import (
    CandidateUpdateManifest,
    PromotionReport,
    RollbackManifest,
    StrategyMemoryRecord,
)

REQUIRED_FORBIDDEN_SCOPE = [
    "low_level_controller_checkpoint",
    "joint_action_output",
    "SafetySupervisor_override",
    "hard_stop_path",
]


def make_candidate_manifest(**overrides: object) -> CandidateUpdateManifest:
    payload = {
        "candidate_id": "cand-20260701-001",
        "parent_policy_version": "runtime_policy_v0.3.1",
        "source_edp_ids": ["edp-00042", "edp-00057"],
        "source_strategy_memory_ids": ["strat-20260701-001"],
        "update_kind": "recovery_priority_update",
        "allowed_scope": "high_level_recovery_selector_only",
        "forbidden_scope": REQUIRED_FORBIDDEN_SCOPE,
        "trigger_condition": {
            "cause": "velocity_tracking_degradation",
            "temporal_profile": "cumulative",
            "tracking_error_slope_min": 0.12,
            "controller_confidence_max": 0.7,
        },
        "proposed_behavior": {
            "prefer": "slow_down",
            "avoid": "continue",
            "vx_cap": 0.25,
        },
        "validation_plan": {
            "memory_positive_cells": [
                "tracking_cumulative_medium",
                "tracking_cumulative_high",
            ],
            "negative_control_cells": [
                "transient_target_loss_low",
                "user_interrupt_control",
            ],
            "seed_split": "gate_si_v0_heldout",
            "method": "matched_seed_diagnostic",
        },
    }
    payload.update(overrides)
    return CandidateUpdateManifest(**payload)


def test_strategy_memory_record_round_trips_as_candidate_memory() -> None:
    memory = StrategyMemoryRecord(
        strategy_id="strat-20260701-001",
        source_failure_ids=["fail-00042", "fail-00057", "fail-00088"],
        trigger={
            "cause": "velocity_tracking_degradation",
            "temporal_profile": "cumulative",
            "tracking_error_slope_min": 0.12,
        },
        recommended_update={
            "kind": "recovery_priority_override",
            "prefer": "slow_down",
            "avoid": "continue",
            "max_vx": 0.25,
        },
    )

    round_tripped = StrategyMemoryRecord.model_validate_json(memory.model_dump_json())

    assert round_tripped.memory_type == "strategy"
    assert round_tripped.status == "candidate"
    assert round_tripped.validation_status == "pending"
    assert round_tripped.source_failure_ids == ["fail-00042", "fail-00057", "fail-00088"]


def test_strategy_memory_record_rejects_oracle_only_fields() -> None:
    with pytest.raises(ValidationError, match="ground_truth_target_pose"):
        StrategyMemoryRecord(
            strategy_id="strat-bad",
            source_failure_ids=["fail-00042"],
            trigger={"cause": "target_loss"},
            recommended_update={
                "kind": "grounding_retry_update",
                "ground_truth_target_pose": [1.0, 2.0, 0.0],
            },
        )


def test_candidate_update_manifest_round_trips_high_level_update() -> None:
    manifest = make_candidate_manifest()

    round_tripped = CandidateUpdateManifest.model_validate_json(manifest.model_dump_json())

    assert round_tripped.schema_version == "candidate_update_manifest_v0"
    assert round_tripped.status == "candidate"
    assert round_tripped.allowed_scope == "high_level_recovery_selector_only"
    assert round_tripped.proposed_behavior["prefer"] == "slow_down"


@pytest.mark.parametrize(
    "forbidden_key",
    [
        "low_level_controller_checkpoint",
        "joint_action_output",
        "SafetySupervisor_override",
        "hard_stop_path",
        "RuntimeManager_bypass",
        "actuator_command",
    ],
)
def test_candidate_update_manifest_rejects_forbidden_update_fields(
    forbidden_key: str,
) -> None:
    with pytest.raises(ValidationError, match=forbidden_key):
        make_candidate_manifest(proposed_behavior={forbidden_key: "bad"})


def test_candidate_update_manifest_requires_core_forbidden_scope() -> None:
    with pytest.raises(ValidationError, match="forbidden_scope"):
        make_candidate_manifest(forbidden_scope=["low_level_controller_checkpoint"])


def test_candidate_update_manifest_rejects_privileged_runtime_features() -> None:
    with pytest.raises(ValidationError, match="oracle_action"):
        make_candidate_manifest(trigger_condition={"oracle_action": "slow_down"})


def test_candidate_update_manifest_rejects_behavior_keys_outside_update_kind_scope() -> None:
    with pytest.raises(ValidationError, match="planner_gain"):
        make_candidate_manifest(proposed_behavior={"prefer": "slow_down", "planner_gain": 2.0})


def test_promotion_report_keeps_gate_si_verdict_and_rollback_pointer() -> None:
    report = PromotionReport(
        report_id="gate-si-report-001",
        candidate_id="cand-20260701-001",
        parent_policy_version="runtime_policy_v0.3.1",
        evaluated_policy_version="runtime_policy_candidate_cand-20260701-001",
        strategy_memory_version="strategy_memory_v0.1.0",
        verdict="NEEDS_MORE_EVIDENCE",
        metrics={"recovery_success_delta_pp": 4.2},
        failure_reasons=["insufficient_gain"],
        validation_report_path="reports/gate_si_validation_report.json",
        safety_report_path="reports/gate_si_safety_report.json",
        rollback_pointer="rollbacks/runtime_policy_v0.3.1.json",
    )

    assert report.schema_version == "promotion_report_v0"
    assert report.verdict == "NEEDS_MORE_EVIDENCE"
    assert report.rollback_pointer == "rollbacks/runtime_policy_v0.3.1.json"


def test_promotion_report_rejects_promote_without_rollback_pointer() -> None:
    with pytest.raises(ValidationError, match="rollback_pointer"):
        PromotionReport(
            report_id="gate-si-report-002",
            candidate_id="cand-20260701-001",
            parent_policy_version="runtime_policy_v0.3.1",
            evaluated_policy_version="runtime_policy_candidate_cand-20260701-001",
            strategy_memory_version="strategy_memory_v0.1.0",
            verdict="PROMOTE",
            metrics={"recovery_success_delta_pp": 6.0},
            validation_report_path="reports/gate_si_validation_report.json",
            safety_report_path="reports/gate_si_safety_report.json",
        )


def test_rollback_manifest_rejects_privileged_evidence() -> None:
    with pytest.raises(ValidationError, match="mujoco_object_id"):
        RollbackManifest(
            rollback_id="rollback-001",
            candidate_id="cand-20260701-001",
            from_policy_version="runtime_policy_v0.3.2",
            rollback_to_policy_version="runtime_policy_v0.3.1",
            reason="oracle_leakage",
            triggered_by_report_id="gate-si-report-003",
            safety_evidence={"mujoco_object_id": "object-42"},
        )

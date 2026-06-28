from __future__ import annotations

from datetime import date

import pytest
from pydantic import ValidationError

from humanoid_locomotion_runtime.analysis import (
    DecisionFlipRecord,
    decision_flip_rate,
    extract_decision_flips,
    format_run_id,
)
from humanoid_locomotion_runtime.schemas import RecoveryActionRecord


def make_record(
    record_id: str,
    *,
    action: str,
    policy_name: str,
    decision_id: str = "dec-001",
    scenario_seed: int = 202606280,
    timestamp_s: float = 1.0,
    branch_id: str | None = None,
) -> RecoveryActionRecord:
    return RecoveryActionRecord(
        record_id=record_id,
        episode_id="episode-001",
        timestamp_s=timestamp_s,
        action=action,  # type: ignore[arg-type]
        available_actions=["continue", "safe_stop", "local_replan"],
        policy_name=policy_name,
        decision_id=decision_id,
        scenario_seed=scenario_seed,
        base_snapshot_id="snap-001",
        branch_id=branch_id,
    )


def test_format_run_id_uses_stable_date_variant_seed_layout() -> None:
    assert (
        format_run_id(
            date(2026, 6, 28),
            run_group="R034",
            variant="typed_memory",
            seed=7,
            replicate=2,
        )
        == "20260628-R034-typed_memory-seed000007-rep002"
    )

    with pytest.raises(ValueError, match="variant"):
        format_run_id("2026-06-28", run_group="R034", variant="typed memory", seed=7)


def test_extract_decision_flips_matches_by_episode_decision_and_seed() -> None:
    left_records = [
        make_record(
            "rec-left-1",
            action="continue",
            policy_name="instant_mlp",
            branch_id="branch-left-1",
        ),
        make_record(
            "rec-left-2",
            action="local_replan",
            policy_name="instant_mlp",
            decision_id="dec-002",
            timestamp_s=2.0,
            branch_id="branch-left-2",
        ),
    ]
    right_records = [
        make_record(
            "rec-right-1",
            action="safe_stop",
            policy_name="typed_event_body_memory",
            branch_id="branch-right-1",
        ),
        make_record(
            "rec-right-2",
            action="local_replan",
            policy_name="typed_event_body_memory",
            decision_id="dec-002",
            timestamp_s=2.1,
            branch_id="branch-right-2",
        ),
    ]

    flips = extract_decision_flips(
        left_records,
        right_records,
        left_policy="instant_mlp",
        right_policy="typed_event_body_memory",
    )

    assert [record.flipped for record in flips] == [True, False]
    assert flips[0].left_action == "continue"
    assert flips[0].right_action == "safe_stop"
    assert flips[0].base_snapshot_id == "snap-001"
    assert decision_flip_rate(flips) == 0.5


def test_extract_decision_flips_requires_decision_id_and_scenario_seed() -> None:
    bad_record = RecoveryActionRecord(
        record_id="rec-bad",
        episode_id="episode-001",
        timestamp_s=1.0,
        action="continue",
        available_actions=["continue"],
        policy_name="instant_mlp",
    )

    with pytest.raises(ValueError, match="decision_id"):
        extract_decision_flips(
            [bad_record],
            [],
            left_policy="instant_mlp",
            right_policy="typed_memory",
        )


def test_decision_flip_record_rejects_privileged_metadata() -> None:
    with pytest.raises(ValidationError, match="mujoco_object_id"):
        DecisionFlipRecord(
            pair_id="episode-001:dec-001:seed1",
            episode_id="episode-001",
            decision_id="dec-001",
            scenario_seed=1,
            timestamp_s=1.0,
            left_policy="instant_mlp",
            right_policy="typed_memory",
            left_record_id="left",
            right_record_id="right",
            left_action="continue",
            right_action="safe_stop",
            flipped=True,
            metadata={"mujoco_object_id": "object-42"},
        )

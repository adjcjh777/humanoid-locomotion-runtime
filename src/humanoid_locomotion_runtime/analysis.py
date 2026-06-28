"""Small analysis contracts that can run without simulation artifacts."""

from __future__ import annotations

import re
from collections.abc import Iterable
from datetime import date, datetime

from pydantic import Field, field_validator

from humanoid_locomotion_runtime.schemas import (
    JsonDict,
    RecoveryAction,
    RecoveryActionRecord,
    StrictSchema,
    assert_no_privileged_keys,
)

SAFE_RUN_TOKEN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]*$")


class DecisionFlipRecord(StrictSchema):
    pair_id: str
    episode_id: str
    decision_id: str
    scenario_seed: int
    timestamp_s: float = Field(ge=0)
    left_policy: str
    right_policy: str
    left_record_id: str
    right_record_id: str
    left_action: RecoveryAction
    right_action: RecoveryAction
    flipped: bool
    base_snapshot_id: str | None = None
    left_branch_id: str | None = None
    right_branch_id: str | None = None
    metadata: JsonDict = Field(default_factory=dict)

    @field_validator("metadata")
    @classmethod
    def _metadata_has_no_privileged_keys(cls, value: JsonDict) -> JsonDict:
        assert_no_privileged_keys(value, "DecisionFlipRecord.metadata")
        return value


def format_run_id(
    run_date: date | datetime | str,
    *,
    run_group: str,
    variant: str,
    seed: int,
    replicate: int | None = None,
) -> str:
    """Return a stable run id for logs, EDP roots and tracker rows."""
    if seed < 0:
        raise ValueError("seed must be non-negative")
    date_text = _format_run_date(run_date)
    group_text = _checked_run_token(run_group, "run_group")
    variant_text = _checked_run_token(variant, "variant")
    run_id = f"{date_text}-{group_text}-{variant_text}-seed{seed:06d}"
    if replicate is not None:
        if replicate < 0:
            raise ValueError("replicate must be non-negative")
        run_id = f"{run_id}-rep{replicate:03d}"
    return run_id


def extract_decision_flips(
    left_records: Iterable[RecoveryActionRecord],
    right_records: Iterable[RecoveryActionRecord],
    *,
    left_policy: str,
    right_policy: str,
) -> list[DecisionFlipRecord]:
    right_index: dict[tuple[str, str, int], RecoveryActionRecord] = {}
    for record in right_records:
        key = _decision_key(record)
        if key in right_index:
            raise ValueError(f"duplicate right decision key: {key}")
        right_index[key] = record

    flips: list[DecisionFlipRecord] = []
    for left in sorted(left_records, key=lambda record: record.timestamp_s):
        key = _decision_key(left)
        right = right_index.get(key)
        if right is None:
            continue
        episode_id, decision_id, scenario_seed = key
        flips.append(
            DecisionFlipRecord(
                pair_id=f"{episode_id}:{decision_id}:seed{scenario_seed}",
                episode_id=episode_id,
                decision_id=decision_id,
                scenario_seed=scenario_seed,
                timestamp_s=min(left.timestamp_s, right.timestamp_s),
                left_policy=left_policy,
                right_policy=right_policy,
                left_record_id=left.record_id,
                right_record_id=right.record_id,
                left_action=left.action,
                right_action=right.action,
                flipped=left.action != right.action,
                base_snapshot_id=left.base_snapshot_id or right.base_snapshot_id,
                left_branch_id=left.branch_id,
                right_branch_id=right.branch_id,
                metadata={"analysis_scope": "matched_decision_flip_table"},
            )
        )
    return flips


def decision_flip_rate(records: Iterable[DecisionFlipRecord]) -> float:
    records = list(records)
    if not records:
        return 0.0
    flipped = sum(1 for record in records if record.flipped)
    return flipped / len(records)


def _format_run_date(run_date: date | datetime | str) -> str:
    if isinstance(run_date, datetime):
        return run_date.date().strftime("%Y%m%d")
    if isinstance(run_date, date):
        return run_date.strftime("%Y%m%d")
    try:
        return datetime.strptime(run_date, "%Y-%m-%d").strftime("%Y%m%d")
    except ValueError as error:
        raise ValueError("run_date must be a date, datetime or YYYY-MM-DD string") from error


def _checked_run_token(value: str, field_name: str) -> str:
    if not SAFE_RUN_TOKEN.fullmatch(value):
        raise ValueError(f"{field_name} must match {SAFE_RUN_TOKEN.pattern}")
    return value


def _decision_key(record: RecoveryActionRecord) -> tuple[str, str, int]:
    if record.decision_id is None:
        raise ValueError(f"record {record.record_id!r} is missing decision_id")
    if record.scenario_seed is None:
        raise ValueError(f"record {record.record_id!r} is missing scenario_seed")
    return (record.episode_id, record.decision_id, record.scenario_seed)

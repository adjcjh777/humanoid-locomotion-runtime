"""Snapshot and branch metadata contracts for Gate C/R018a.

This module defines the metadata contract only. It does not claim deterministic
MuJoCo/runtime restore has passed.
"""

from __future__ import annotations

from typing import Literal

from pydantic import Field, field_validator

from humanoid_locomotion_runtime.schemas import (
    JsonDict,
    RecoveryAction,
    StrictSchema,
    assert_no_privileged_keys,
)

OptionOutcome = Literal[
    "not_run",
    "success",
    "failure",
    "timeout",
    "interrupted",
    "safety_override",
]

SnapshotRestoreStatus = Literal[
    "contract_only_no_restore",
    "restore_pending",
    "restore_smoke_passed",
]

BranchRole = Literal[
    "candidate_policy",
    "baseline_policy",
    "evaluation_oracle",
]


def validate_sha256_digest(value: str | None, field_name: str) -> str | None:
    if value is not None and (
        len(value) != 64 or any(character not in "0123456789abcdef" for character in value)
    ):
        raise ValueError(f"{field_name} must be a lowercase 64-character SHA256 digest")
    return value


class SnapshotManifest(StrictSchema):
    snapshot_id: str
    decision_id: str
    scenario_seed: int
    exogenous_noise_seed: int
    observation_hash: str
    memory_hash: str
    robot_profile_id: str
    controller_profile_id: str
    simulator_state_hash: str
    runtime_state_hashes: dict[str, str]
    active_option: RecoveryAction | None = None
    restore_status: SnapshotRestoreStatus = "contract_only_no_restore"
    metadata: JsonDict = Field(default_factory=dict)

    @field_validator(
        "observation_hash",
        "memory_hash",
        "simulator_state_hash",
    )
    @classmethod
    def _hash_fields_are_sha256(cls, value: str, info) -> str:
        checked = validate_sha256_digest(value, info.field_name)
        assert checked is not None
        return checked

    @field_validator("runtime_state_hashes")
    @classmethod
    def _runtime_state_hashes_are_sha256(cls, value: dict[str, str]) -> dict[str, str]:
        if not value:
            raise ValueError("runtime_state_hashes must include at least one runtime component")
        assert_no_privileged_keys(value, "SnapshotManifest.runtime_state_hashes")
        for key, digest in value.items():
            validate_sha256_digest(digest, f"runtime_state_hashes[{key}]")
        return value

    @field_validator("metadata")
    @classmethod
    def _metadata_has_no_privileged_keys(cls, value: JsonDict) -> JsonDict:
        assert_no_privileged_keys(value, "SnapshotManifest.metadata")
        return value


class SnapshotBranchMetadata(StrictSchema):
    base_snapshot_id: str
    branch_id: str
    decision_id: str
    scenario_seed: int
    exogenous_noise_seed: int
    observation_hash: str
    memory_hash: str
    action: RecoveryAction
    option_outcome: OptionOutcome
    controller_profile_id: str
    robot_profile_id: str
    policy_training_seed: int | None = None
    branch_role: BranchRole = "candidate_policy"
    common_random_stream_id: str = "crn-v0"
    metadata: JsonDict = Field(default_factory=dict)

    @field_validator("observation_hash", "memory_hash")
    @classmethod
    def _hash_fields_are_sha256(cls, value: str, info) -> str:
        checked = validate_sha256_digest(value, info.field_name)
        assert checked is not None
        return checked

    @field_validator("metadata")
    @classmethod
    def _metadata_has_no_privileged_keys(cls, value: JsonDict) -> JsonDict:
        assert_no_privileged_keys(value, "SnapshotBranchMetadata.metadata")
        return value

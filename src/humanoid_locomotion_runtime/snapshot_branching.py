"""Snapshot and branch metadata contracts for Gate C/R018a.

This module defines the metadata contract only. It does not claim deterministic
MuJoCo/runtime restore has passed.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from typing import Literal, Protocol

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

DecisionEpochTrigger = Literal[
    "failure_trigger",
    "active_option_termination",
    "option_timeout",
    "major_task_control_event",
]


def validate_sha256_digest(value: str | None, field_name: str) -> str | None:
    if value is not None and (
        len(value) != 64 or any(character not in "0123456789abcdef" for character in value)
    ):
        raise ValueError(f"{field_name} must be a lowercase 64-character SHA256 digest")
    return value


def runtime_payload_sha256(value: object, context: str = "runtime payload") -> str:
    """Hash runtime-facing JSON-like data after enforcing the leakage boundary."""
    assert_no_privileged_keys(value, context)
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


class DecisionEpoch(StrictSchema):
    """A backend-neutral decision point where a supervisory option may be chosen."""

    decision_id: str
    episode_id: str
    timestamp_s: float = Field(ge=0)
    trigger: DecisionEpochTrigger
    scenario_seed: int
    exogenous_noise_seed: int
    observation_hash: str
    memory_hash: str
    active_option: RecoveryAction | None = None
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
        assert_no_privileged_keys(value, "DecisionEpoch.metadata")
        return value


class CommonRandomStream(StrictSchema):
    """Common random stream identity for matched branches.

    This is a contract-level record only. It is not a simulator RNG capture.
    """

    stream_id: str = "crn-v0"
    scenario_seed: int
    exogenous_noise_seed: int
    draw_index: int = Field(default=0, ge=0)
    deterministic_replay_required: bool = True
    metadata: JsonDict = Field(default_factory=dict)

    @field_validator("metadata")
    @classmethod
    def _metadata_has_no_privileged_keys(cls, value: JsonDict) -> JsonDict:
        assert_no_privileged_keys(value, "CommonRandomStream.metadata")
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


class SnapshotProvider(Protocol):
    """Backend-neutral contract for snapshot capture/restore implementations."""

    def capture(
        self,
        *,
        snapshot_id: str,
        epoch: DecisionEpoch,
        simulator_state: Mapping[str, object],
        runtime_components: Mapping[str, object],
        active_option: RecoveryAction | None = None,
    ) -> SnapshotManifest: ...

    def restore(self, snapshot_id: str) -> SnapshotManifest: ...

    def branch(
        self,
        *,
        base_snapshot_id: str,
        branch_id: str,
        action: RecoveryAction,
        option_outcome: OptionOutcome = "not_run",
        branch_role: BranchRole = "candidate_policy",
        policy_training_seed: int | None = None,
    ) -> SnapshotBranchMetadata: ...


class FakeDeterministicSnapshotProvider:
    """Pure Python snapshot provider for Mac-safe Gate C tests.

    It hashes JSON-like simulator/runtime dictionaries and restores the stored
    manifest exactly. This proves the interface shape and leakage checks, not
    MuJoCo/runtime restore.
    """

    def __init__(self, *, robot_profile_id: str, controller_profile_id: str) -> None:
        self.robot_profile_id = robot_profile_id
        self.controller_profile_id = controller_profile_id
        self._snapshots: dict[str, SnapshotManifest] = {}

    def capture(
        self,
        *,
        snapshot_id: str,
        epoch: DecisionEpoch,
        simulator_state: Mapping[str, object],
        runtime_components: Mapping[str, object],
        active_option: RecoveryAction | None = None,
    ) -> SnapshotManifest:
        if not runtime_components:
            raise ValueError("runtime_components must include at least one component")

        simulator_state_hash = runtime_payload_sha256(
            dict(simulator_state),
            "FakeDeterministicSnapshotProvider.simulator_state",
        )
        runtime_state_hashes = {
            component: runtime_payload_sha256(
                payload,
                f"FakeDeterministicSnapshotProvider.runtime_components[{component}]",
            )
            for component, payload in sorted(runtime_components.items())
        }
        manifest = SnapshotManifest(
            snapshot_id=snapshot_id,
            decision_id=epoch.decision_id,
            scenario_seed=epoch.scenario_seed,
            exogenous_noise_seed=epoch.exogenous_noise_seed,
            observation_hash=epoch.observation_hash,
            memory_hash=epoch.memory_hash,
            robot_profile_id=self.robot_profile_id,
            controller_profile_id=self.controller_profile_id,
            simulator_state_hash=simulator_state_hash,
            runtime_state_hashes=runtime_state_hashes,
            active_option=active_option or epoch.active_option,
            restore_status="contract_only_no_restore",
            metadata={"testbed_scope": "fake_backend_only"},
        )
        self._snapshots[snapshot_id] = manifest
        return manifest

    def restore(self, snapshot_id: str) -> SnapshotManifest:
        try:
            return self._snapshots[snapshot_id]
        except KeyError as error:
            raise KeyError(f"unknown snapshot_id: {snapshot_id}") from error

    def branch(
        self,
        *,
        base_snapshot_id: str,
        branch_id: str,
        action: RecoveryAction,
        option_outcome: OptionOutcome = "not_run",
        branch_role: BranchRole = "candidate_policy",
        policy_training_seed: int | None = None,
    ) -> SnapshotBranchMetadata:
        base = self.restore(base_snapshot_id)
        stream = CommonRandomStream(
            scenario_seed=base.scenario_seed,
            exogenous_noise_seed=base.exogenous_noise_seed,
        )
        return SnapshotBranchMetadata(
            base_snapshot_id=base.snapshot_id,
            branch_id=branch_id,
            decision_id=base.decision_id,
            scenario_seed=base.scenario_seed,
            exogenous_noise_seed=base.exogenous_noise_seed,
            observation_hash=base.observation_hash,
            memory_hash=base.memory_hash,
            action=action,
            option_outcome=option_outcome,
            controller_profile_id=base.controller_profile_id,
            robot_profile_id=base.robot_profile_id,
            policy_training_seed=policy_training_seed,
            branch_role=branch_role,
            common_random_stream_id=stream.stream_id,
            metadata={"testbed_scope": "fake_backend_only"},
        )

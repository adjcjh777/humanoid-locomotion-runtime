from __future__ import annotations

import pytest
from pydantic import ValidationError

from humanoid_locomotion_runtime.recovery_options import (
    RECOVERY_ACTIONS,
    RECOVERY_OPTION_CONTRACTS,
    RecoveryOptionContract,
    validate_recovery_option_catalog,
)
from humanoid_locomotion_runtime.schemas import PRIVILEGED_FIELD_NAMES


def test_recovery_option_catalog_covers_all_high_level_actions() -> None:
    validate_recovery_option_catalog()

    assert set(RECOVERY_OPTION_CONTRACTS) == set(RECOVERY_ACTIONS)
    assert len(RECOVERY_OPTION_CONTRACTS) == 8


def test_each_recovery_option_has_complete_smdp_fields() -> None:
    for action, contract in RECOVERY_OPTION_CONTRACTS.items():
        assert contract.action == action
        assert contract.initiation_conditions
        assert contract.action_mask_conditions
        assert contract.implementation_stub
        assert contract.min_duration_s >= 0
        assert contract.max_duration_s >= contract.min_duration_s
        assert contract.success_conditions
        assert contract.failure_conditions
        assert contract.termination_conditions
        assert contract.interruptibility in {
            "safety_interruptible",
            "option_boundary_interruptible",
            "runtime_interruptible",
        }
        assert contract.retry_budget >= 0
        assert contract.cooldown_s >= 0
        assert contract.legal_runtime_signals


def test_recovery_option_legal_signals_do_not_use_privileged_fields() -> None:
    for contract in RECOVERY_OPTION_CONTRACTS.values():
        for signal in contract.legal_runtime_signals:
            assert signal not in PRIVILEGED_FIELD_NAMES
            assert signal.split(".")[-1] not in PRIVILEGED_FIELD_NAMES


def test_recovery_option_contract_rejects_invalid_duration_order() -> None:
    with pytest.raises(ValidationError, match="max_duration_s"):
        RecoveryOptionContract(
            action="continue",
            initiation_conditions=("active command",),
            action_mask_conditions=("not masked",),
            implementation_stub="RuntimeManager keeps command active.",
            min_duration_s=2.0,
            max_duration_s=1.0,
            success_conditions=("stable",),
            failure_conditions=("unstable",),
            termination_conditions=("timeout",),
            interruptibility="runtime_interruptible",
            retry_budget=1,
            cooldown_s=0.0,
            legal_runtime_signals=("LocomotionStatus.tracking_error",),
        )


def test_recovery_option_contract_rejects_privileged_runtime_signal() -> None:
    with pytest.raises(ValidationError, match="privileged"):
        RecoveryOptionContract(
            action="continue",
            initiation_conditions=("active command",),
            action_mask_conditions=("not masked",),
            implementation_stub="RuntimeManager keeps command active.",
            min_duration_s=0.0,
            max_duration_s=1.0,
            success_conditions=("stable",),
            failure_conditions=("unstable",),
            termination_conditions=("timeout",),
            interruptibility="runtime_interruptible",
            retry_budget=1,
            cooldown_s=0.0,
            legal_runtime_signals=("OracleAnnotation.oracle_action",),
        )

from __future__ import annotations

import tomllib
from pathlib import Path

from humanoid_locomotion_runtime.schemas import PRIVILEGED_FIELD_NAMES

CONFIG_PATH = Path("configs/failure_protocol.v0.toml")


def load_protocol() -> dict:
    return tomllib.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def test_failure_protocol_covers_required_causes_and_temporal_profiles() -> None:
    protocol = load_protocol()

    assert protocol["status"] == "frozen_pre_pilot_protocol"
    assert set(protocol["failure_causes"]) >= {
        "path_blockage",
        "target_loss_or_ambiguity",
        "localization_drift",
        "velocity_tracking_degradation",
        "balance_risk_safety_stop",
    }
    assert set(protocol["temporal_profiles"]) >= {
        "transient",
        "persistent",
        "recurrent",
        "cumulative_degradation",
    }


def test_user_interrupt_is_task_control_event_not_failure_family() -> None:
    protocol = load_protocol()

    user_interrupt = protocol["task_control_events"]["user_interrupt"]

    assert user_interrupt["is_failure_family"] is False
    assert "user_interrupt" not in protocol["failure_causes"]


def test_failure_cells_have_complete_freeze_fields_and_signal_boundary() -> None:
    protocol = load_protocol()
    causes = set(protocol["failure_causes"])
    temporal_profiles = set(protocol["temporal_profiles"])

    for cell in protocol["failure_cells"]:
        assert cell["cause"] in causes
        assert cell["temporal_profile"] in temporal_profiles
        assert cell["role"]
        assert cell["expected_memory_effect"]
        assert cell["legal_runtime_signals"]
        assert cell["forbidden_privileged_signals"]
        assert cell["severity_knobs"]
        assert cell["success_criteria"]
        assert cell["failure_criteria"]
        assert set(cell["forbidden_privileged_signals"]) & PRIVILEGED_FIELD_NAMES
        for signal in cell["legal_runtime_signals"]:
            assert signal not in PRIVILEGED_FIELD_NAMES
            assert signal.split(".")[-1] not in PRIVILEGED_FIELD_NAMES


def test_state_aliasing_cell_is_memory_positive_without_causal_claim() -> None:
    protocol = load_protocol()
    cells = protocol["state_aliasing_cells"]

    assert len(cells) >= 1
    cell = cells[0]
    assert cell["role"] == "memory_positive"
    assert cell["paired_conditions"] == ["tracking_history_branch", "localization_history_branch"]
    assert "current_observation_similarity" in cell
    assert "history_difference" in cell
    assert "legal_input_list" in cell
    assert "counterfactual" in cell["diagnostic_claim_boundary"]
    assert "ATE" in cell["diagnostic_claim_boundary"]

    conditions = cell["conditions"]
    assert len(conditions) == 2
    expected_actions = {condition["expected_action"] for condition in conditions}
    assert expected_actions == {"slow_down", "relocalize"}
    for signal in cell["legal_input_list"]:
        assert signal not in PRIVILEGED_FIELD_NAMES
        assert signal.split(".")[-1] not in PRIVILEGED_FIELD_NAMES

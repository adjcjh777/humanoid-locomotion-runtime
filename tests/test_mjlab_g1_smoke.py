from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

import pytest

ROOT = Path(__file__).resolve().parents[1]


class FakeTensor:
    def __init__(self, shape: tuple[int, ...]) -> None:
        self.shape = shape


def load_smoke_module() -> ModuleType:
    spec = importlib.util.spec_from_file_location(
        "mjlab_g1_smoke_for_test",
        ROOT / "scripts" / "mjlab_g1_smoke.py",
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_cli_defaults_keep_mjlab_g1_29dof_reference_compatible() -> None:
    smoke = load_smoke_module()

    args = smoke.build_arg_parser().parse_args([])

    assert args.robot_profile == "mjlab_g1_29dof_reference"
    assert args.expected_action_dim == 29
    assert args.expected_actor_obs_dim == 99
    assert args.expected_critic_obs_dim == 111


def test_profile_dimension_gate_accepts_current_reference_shapes() -> None:
    smoke = load_smoke_module()
    dimensions = smoke.extract_smoke_dimensions(
        (1, 29),
        {
            "actor": FakeTensor((1, 99)),
            "critic": FakeTensor((1, 111)),
        },
    )

    smoke.validate_profile_dimensions(
        robot_profile="mjlab_g1_29dof_reference",
        dimensions=dimensions,
        expected_action_dim=29,
        expected_actor_obs_dim=99,
        expected_critic_obs_dim=111,
    )
    summary = smoke.dimension_gate_summary(
        robot_profile="mjlab_g1_29dof_reference",
        dimensions=dimensions,
        expected_action_dim=29,
        expected_actor_obs_dim=99,
        expected_critic_obs_dim=111,
    )

    assert summary["robot_profile"] == "mjlab_g1_29dof_reference"
    assert summary["actual"]["action_shape"] == [1, 29]
    assert summary["actual"]["actor_obs_dim"] == 99
    assert summary["actual"]["critic_obs_dim"] == 111


def test_company_profile_cannot_reuse_reference_action_dim_default() -> None:
    smoke = load_smoke_module()

    with pytest.raises(smoke.DimensionGateError) as excinfo:
        smoke.validate_robot_profile_request(
            robot_profile="company_g1_edu_23dof",
            expected_action_dim=29,
        )

    message = str(excinfo.value)
    assert "robot_profile='company_g1_edu_23dof'" in message
    assert "requires expected_action_dim=23" in message
    assert "current MJLab 29DoF reference smoke" in message


def test_profile_dimension_gate_rejects_wrong_company_23dof_expectation() -> None:
    smoke = load_smoke_module()
    dimensions = smoke.extract_smoke_dimensions(
        (1, 29),
        {
            "actor": FakeTensor((1, 99)),
            "critic": FakeTensor((1, 111)),
        },
    )

    with pytest.raises(smoke.DimensionGateError) as excinfo:
        smoke.validate_profile_dimensions(
            robot_profile="company_g1_edu_23dof",
            dimensions=dimensions,
            expected_action_dim=23,
            expected_actor_obs_dim=99,
            expected_critic_obs_dim=111,
        )

    message = str(excinfo.value)
    assert "robot_profile='company_g1_edu_23dof'" in message
    assert "action_dim: expected 23, got 29" in message
    assert "shape=[1, 29]" in message


def test_dimension_extraction_requires_actor_and_critic_groups() -> None:
    smoke = load_smoke_module()

    with pytest.raises(ValueError, match="Missing required observation group"):
        smoke.extract_smoke_dimensions(
            (1, 29),
            {
                "actor": FakeTensor((1, 99)),
            },
        )

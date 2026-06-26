from __future__ import annotations

import tomllib
from pathlib import Path

from humanoid_locomotion_runtime.gate_a import (
    missing_gate_a_paths,
    missing_gitignore_patterns,
)

ROOT = Path(__file__).resolve().parents[1]


def load_toml(relative_path: str) -> dict:
    return tomllib.loads((ROOT / relative_path).read_text(encoding="utf-8"))


def test_gate_a_required_files_exist() -> None:
    assert missing_gate_a_paths(ROOT) == []


def test_gitignore_excludes_private_and_generated_roots() -> None:
    assert missing_gitignore_patterns(ROOT) == []


def test_python_and_core_versions_are_pinned() -> None:
    pyproject = load_toml("pyproject.toml")
    environment = load_toml("configs/environment.lock.toml")

    assert pyproject["project"]["requires-python"] == "==3.12.*"
    assert (ROOT / ".python-version").read_text(encoding="utf-8").strip() == "3.12.13"
    assert environment["python"]["version"] == "3.12.13"
    assert environment["packages"]["mujoco"]["version"] == "3.10.0"
    assert pyproject["project"]["optional-dependencies"]["sim"] == ["mujoco==3.10.0"]
    assert "jax[cuda12]==0.10.2" in pyproject["project"]["optional-dependencies"][
        "sim-playground"
    ]


def test_mjlab_is_primary_sim_backend_and_playground_is_deferred() -> None:
    environment = load_toml("configs/environment.lock.toml")
    mjlab = environment["mjlab_backend"]
    playground = environment["mujoco_playground"]

    assert mjlab["status"] == "preferred-v0-sim-backend-unselected"
    assert mjlab["required_before"] == "controller smoke gate"
    assert playground["status"] == "deferred-optional-reference-not-primary-v0-requirement"
    assert environment["cuda_wheel"]["status"] == "deferred-optional-extra"


def test_controller_and_robot_assets_are_explicitly_blocked_until_selected() -> None:
    environment = load_toml("configs/environment.lock.toml")

    assert environment["controller_checkpoint"]["status"] == "unselected"
    assert environment["controller_checkpoint"]["sha256"] == ""
    assert environment["robot_mjcf"]["status"] == "unselected"
    assert environment["robot_mjcf"]["sha256"] == ""


def test_artifact_retention_policy_requires_disk_gate() -> None:
    retention = load_toml("configs/artifact_retention.toml")

    assert retention["git_policy"]["commit_generated_runs"] is False
    assert retention["git_policy"]["commit_raw_agent_traces"] is False
    assert retention["disk_gate"]["run_id"] == "R004"
    assert retention["disk_gate"]["required_before"] == "any batch rollout or overnight experiment"
    assert retention["paths"]["generated_roots"] == [
        "runs",
        "logs",
        "artifacts",
        "checkpoints",
        "weights",
        "datasets",
    ]

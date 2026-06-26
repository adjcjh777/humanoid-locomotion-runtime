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
    mjlab_runtime = environment["mjlab_runtime_dependencies"]

    assert mjlab["status"] == "selected-backend-reference"
    assert mjlab["source"] == "project-local git submodule"
    assert mjlab["local_path"] == "third_party/mjlab"
    assert mjlab["origin"] == "https://github.com/mujocolab/mjlab.git"
    assert mjlab["commit"] == "efdcadc8b281553fd3e1be2a9a88db9553356e8a"
    assert mjlab["selected_task_id"] == "Mjlab-Velocity-Flat-Unitree-G1"
    assert mjlab["required_before"] == "controller smoke gate"
    assert mjlab_runtime["status"] == "verified-full-mjlab-g1-headless-smoke"
    assert mjlab_runtime["python_version"] == "3.12.13"
    assert mjlab_runtime["verified_packages"]["torch"] == "2.9.0+cu128"
    assert mjlab_runtime["verified_packages"]["mujoco_warp"] == "3.9.0.1"
    assert "scripts/mjlab_sync_and_smoke.sh" in mjlab_runtime["sync_command"]
    assert "--python .venv/bin/python3" in mjlab_runtime["smoke_command"]
    assert playground["status"] == "deferred-optional-reference-not-primary-v0-requirement"
    assert environment["cuda_wheel"]["status"] == "deferred-optional-extra"


def test_g1_asset_wrapper_and_checkpoint_candidate_are_project_local() -> None:
    environment = load_toml("configs/environment.lock.toml")

    checkpoint = environment["controller_checkpoint"]
    assert checkpoint["status"] == "candidate-downloaded-pending-controller-smoke"
    assert checkpoint["local_path"] == "checkpoints/unitree_rl_mjlab_g1_velocity_v0/policy.onnx"
    assert checkpoint["sha256"] == (
        "2a66ca6336eadb3c0b34b557763f3e06d01ff8fcf6260dd4cedbd69d6093fc28"
    )
    assert checkpoint["source_repo"] == "https://github.com/unitreerobotics/unitree_rl_mjlab"
    assert "ignored checkpoints/" in checkpoint["git_policy"]
    assert "input obs=[1,98]" in checkpoint["shape_check"]
    assert environment["robot_mjcf"]["status"] == "selected"
    assert environment["robot_mjcf"]["path"].startswith("third_party/mjlab/")
    assert (
        environment["robot_mjcf"]["sha256"]
        == "febdcbeffbbf84051556ae41a5ac1b43fb479a5d76bdb3f54824dbc2721c20aa"
    )
    assert environment["controller_wrapper"]["status"] == "selected-wrapper-no-checkpoint"
    assert environment["controller_wrapper"]["runner"].startswith("third_party/mjlab/")
    assert environment["controller_wrapper"]["runner"].endswith(
        "mjlab/tasks/velocity/rl/runner.py"
    )


def test_company_g1_23dof_source_is_recorded_separately_from_29dof_reference() -> None:
    environment = load_toml("configs/environment.lock.toml")
    robot_profiles = environment["robot_profiles"]

    company_g1 = robot_profiles["company_g1_edu_23dof"]
    assert company_g1["role"] == "primary-deployment-target"
    assert company_g1["status"] == "official-source-identified-integration-pending"
    assert company_g1["source_repo"] == "https://github.com/unitreerobotics/unitree_rl_gym"
    assert company_g1["source_commit"] == "276801e46c5d433564f24658bac64f254b7d2d4b"
    assert company_g1["urdf_path"].endswith("g1_23dof_rev_1_0.urdf")
    assert company_g1["mjcf_path"].endswith("g1_23dof_rev_1_0.xml")
    assert company_g1["urdf_sha256"] == (
        "cffe6149e0b29abed10b8c6a7e318003676ae4234224044e4af30946599d1ba9"
    )
    assert company_g1["mjcf_sha256"] == (
        "8ca62fcccdca91a431ca04f1a42f9c2fda241fdd5e13411168dc82de00f978de"
    )
    assert company_g1["controlled_dof"] == 23
    assert len(company_g1["joint_order"]) == 23
    assert company_g1["joint_order"][0] == "left_hip_pitch_joint"
    assert company_g1["joint_order"][-1] == "right_wrist_roll_joint"

    reference_g1 = robot_profiles["mjlab_g1_29dof_reference"]
    assert reference_g1["role"] == "backend-health-reference"
    assert reference_g1["controlled_dof"] == 29
    assert reference_g1["mjcf_model"] == "g1_29dof_rev_1_0"
    assert "not-company-target" in reference_g1["status"]
    assert "29DoF reference" in environment["controller_checkpoint"]["robot_profile_note"]


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

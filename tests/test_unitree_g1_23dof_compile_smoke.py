from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "compile_unitree_g1_23dof_description.py"


def load_compile_module() -> ModuleType:
    spec = importlib.util.spec_from_file_location("g1_23dof_compile_for_test", SCRIPT)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_compile_script_imports_without_mujoco_extra() -> None:
    module = load_compile_module()

    assert module.DEFAULT_MODEL_PATH == Path(
        "robot_descriptions/unitree_g1_23dof_rev_1_0/g1_23dof_rev_1_0.xml"
    )


def test_expected_23dof_joint_order_is_profile_locked() -> None:
    module = load_compile_module()

    assert module.EXPECTED_JOINT_NAMES[0] == "floating_base_joint"
    assert module.EXPECTED_JOINT_NAMES[1] == "left_hip_pitch_joint"
    assert module.EXPECTED_JOINT_NAMES[-1] == "right_wrist_roll_joint"
    assert len(module.EXPECTED_JOINT_NAMES) == 24
    assert len(module.controlled_joint_names(module.EXPECTED_JOINT_NAMES)) == 23

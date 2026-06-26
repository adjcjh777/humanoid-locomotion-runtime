#!/usr/bin/env python3
"""Compile the ignored Unitree G1 edu 23DoF MJCF with MuJoCo.

This is a raw asset smoke only. It proves the official 23DoF XML and mesh
assets can be loaded by MuJoCo; it does not prove a MJLab wrapper or controller.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

DEFAULT_MODEL_PATH = Path("robot_descriptions/unitree_g1_23dof_rev_1_0/g1_23dof_rev_1_0.xml")

EXPECTED_JOINT_NAMES = [
    "floating_base_joint",
    "left_hip_pitch_joint",
    "left_hip_roll_joint",
    "left_hip_yaw_joint",
    "left_knee_joint",
    "left_ankle_pitch_joint",
    "left_ankle_roll_joint",
    "right_hip_pitch_joint",
    "right_hip_roll_joint",
    "right_hip_yaw_joint",
    "right_knee_joint",
    "right_ankle_pitch_joint",
    "right_ankle_roll_joint",
    "waist_yaw_joint",
    "left_shoulder_pitch_joint",
    "left_shoulder_roll_joint",
    "left_shoulder_yaw_joint",
    "left_elbow_joint",
    "left_wrist_roll_joint",
    "right_shoulder_pitch_joint",
    "right_shoulder_roll_joint",
    "right_shoulder_yaw_joint",
    "right_elbow_joint",
    "right_wrist_roll_joint",
]


def controlled_joint_names(joint_names: list[str]) -> list[str]:
    return [name for name in joint_names if name != "floating_base_joint"]


def compile_model(path: Path) -> dict[str, Any]:
    import mujoco

    model = mujoco.MjModel.from_xml_path(str(path))
    joint_names = [
        mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_JOINT, joint_index)
        or f"<unnamed:{joint_index}>"
        for joint_index in range(model.njnt)
    ]

    if joint_names != EXPECTED_JOINT_NAMES:
        raise ValueError(
            "23DoF joint order mismatch: "
            f"expected {EXPECTED_JOINT_NAMES!r}, observed {joint_names!r}"
        )

    controlled_count = len(controlled_joint_names(joint_names))
    if controlled_count != 23 or model.nu != 23:
        raise ValueError(
            "23DoF compile smoke expected 23 controlled joints and 23 actuators; "
            f"observed controlled_count={controlled_count}, nu={model.nu}"
        )

    return {
        "status": "pass",
        "mujoco": mujoco.__version__,
        "path": str(path),
        "nq": model.nq,
        "nv": model.nv,
        "nu": model.nu,
        "nbody": model.nbody,
        "njnt": model.njnt,
        "ngeom": model.ngeom,
        "nmesh": model.nmesh,
        "joint_names": joint_names,
        "controlled_joint_count_excluding_freejoint": controlled_count,
    }


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", type=Path, default=DEFAULT_MODEL_PATH)
    return parser


def main() -> None:
    args = build_arg_parser().parse_args()
    summary = compile_model(args.model)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

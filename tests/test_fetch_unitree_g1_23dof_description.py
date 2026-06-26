from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "fetch_unitree_g1_23dof_description.sh"


def read_script() -> str:
    return SCRIPT.read_text(encoding="utf-8")


def test_fetch_unitree_g1_23dof_description_script_exists() -> None:
    assert SCRIPT.exists()


def test_fetch_unitree_g1_23dof_description_script_locks_official_source() -> None:
    script = read_script()

    commit = "276801e46c5d433564f24658bac64f254b7d2d4b"
    raw_base = (
        "https://raw.githubusercontent.com/unitreerobotics/unitree_rl_gym/"
        f"{commit}/resources/robots/g1_description"
    )

    assert "set -euo pipefail" in script
    assert "robot_descriptions/unitree_g1_23dof_rev_1_0" in script
    assert "https://github.com/unitreerobotics/unitree_rl_gym" in script
    assert commit in script
    assert raw_base in script
    assert "g1_23dof_rev_1_0.urdf" in script
    assert "g1_23dof_rev_1_0.xml" in script
    assert (
        "cffe6149e0b29abed10b8c6a7e318003676ae4234224044e4af30946599d1ba9"
        in script
    )
    assert (
        "8ca62fcccdca91a431ca04f1a42f9c2fda241fdd5e13411168dc82de00f978de"
        in script
    )


def test_fetch_unitree_g1_23dof_description_script_warns_about_scope() -> None:
    script = read_script()

    assert "official Unitree G1 edu 23DoF robot description only" in script
    assert "not a controller checkpoint" in script
    assert "keep downloaded robot descriptions out of git" in script

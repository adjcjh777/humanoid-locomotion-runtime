#!/usr/bin/env python
"""Run Unitree RL MJLab play.py with repo-local 23DoF task profiles."""

from __future__ import annotations

import importlib.util
import os
import runpy
import sys
from pathlib import Path


def _register_repo_local_profiles(root_dir: Path) -> None:
  profiles_path = (
    root_dir
    / "src"
    / "humanoid_locomotion_runtime"
    / "unitree_g1_23dof_profiles.py"
  )
  spec = importlib.util.spec_from_file_location(
    "unitree_g1_23dof_profiles_repo_local", profiles_path
  )
  if spec is None or spec.loader is None:
    raise ImportError(f"could not load repo-local profiles from {profiles_path}")
  module = importlib.util.module_from_spec(spec)
  sys.modules[spec.name] = module
  spec.loader.exec_module(module)

  module.register_unitree_g1_23dof_controller_profiles()


def main() -> None:
  root_dir = Path(__file__).resolve().parents[1]
  train_repo = Path(
    os.environ.get(
      "UNITREE_RL_MJLAB_ROOT",
      root_dir / "third_party" / "unitree_rl_mjlab",
    )
  ).resolve()
  play_py = train_repo / "scripts" / "play.py"
  if not play_py.exists():
    raise FileNotFoundError(f"Unitree play.py not found: {play_py}")

  sys.path.insert(0, str(train_repo))
  os.chdir(train_repo)
  sys.argv = [str(play_py), *sys.argv[1:]]
  _register_repo_local_profiles(root_dir)
  runpy.run_path(str(play_py), run_name="__main__")


if __name__ == "__main__":
  main()

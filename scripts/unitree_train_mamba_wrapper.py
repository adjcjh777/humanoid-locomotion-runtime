#!/usr/bin/env python
"""Run Unitree RL MJLab train.py with repo-local compatibility patches."""

from __future__ import annotations

import inspect
import os
import runpy
import sys
from pathlib import Path
from typing import Any


def _patch_torch_onnx_export() -> None:
  """Drop unsupported ONNX exporter kwargs on older torch builds."""
  import torch

  export = torch.onnx.export
  if "dynamo" in inspect.signature(export).parameters:
    return

  def export_compat(*args: Any, **kwargs: Any) -> Any:
    kwargs.pop("dynamo", None)
    return export(*args, **kwargs)

  torch.onnx.export = export_compat  # type: ignore[assignment]


def main() -> None:
  root_dir = Path(__file__).resolve().parents[1]
  train_repo = Path(
    os.environ.get(
      "UNITREE_RL_MJLAB_ROOT",
      root_dir / "third_party" / "unitree_rl_mjlab",
    )
  ).resolve()
  train_py = train_repo / "scripts" / "train.py"
  if not train_py.exists():
    raise FileNotFoundError(f"Unitree train.py not found: {train_py}")

  sys.path.insert(0, str(train_repo))
  os.chdir(train_repo)
  sys.argv = [str(train_py), *sys.argv[1:]]
  _patch_torch_onnx_export()
  runpy.run_path(str(train_py), run_name="__main__")


if __name__ == "__main__":
  main()

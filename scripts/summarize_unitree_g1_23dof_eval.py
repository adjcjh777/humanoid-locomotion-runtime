#!/usr/bin/env python
"""Summarize Unitree G1 23DoF command-grid eval JSON files."""

from __future__ import annotations

import argparse
import csv
import glob
import json
import sys
from pathlib import Path
from typing import Any

FORWARD_COMMANDS = ("forward_slow", "forward_mid", "forward_fast")
YAW_COMMANDS = ("yaw_left", "yaw_right")
LATERAL_COMMANDS = ("lateral_left", "lateral_right")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "paths",
        nargs="*",
        help="Eval JSON files. If omitted, --glob is used.",
    )
    parser.add_argument(
        "--glob",
        default="runs/unitree_g1_23dof_eval/*.json",
        help="Glob used when no explicit JSON paths are provided.",
    )
    parser.add_argument(
        "--format",
        choices=("csv", "markdown"),
        default="markdown",
    )
    parser.add_argument(
        "--group-by",
        choices=("seed", "checkpoint"),
        default="seed",
        help="Summarize each seed JSON or aggregate by checkpoint.",
    )
    parser.add_argument(
        "--include-seeds",
        default=None,
        help=(
            "Comma-separated seed allowlist, e.g. 101,102,103. "
            "Useful to exclude smoke JSON."
        ),
    )
    return parser.parse_args()


def _result_by_name(payload: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {result["command_name"]: result for result in payload["results"]}


def _max_done(results: dict[str, dict[str, Any]], names: tuple[str, ...]) -> float:
    return max(float(results[name]["done_fraction"]) for name in names)


def _checkpoint_iteration(checkpoint: str) -> int:
    if checkpoint.startswith("model_"):
        try:
            return int(checkpoint.removeprefix("model_"))
        except ValueError:
            return -1
    return -1


def _summarize(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    checkpoint_path = Path(payload["checkpoint_file"])
    results = _result_by_name(payload)
    forward_fast = results["forward_fast"]
    checkpoint = checkpoint_path.stem
    forward_done_max = _max_done(results, FORWARD_COMMANDS)
    yaw_done_max = _max_done(results, YAW_COMMANDS)
    lateral_done_max = _max_done(results, LATERAL_COMMANDS)
    selection_penalty = (
        10.0 * forward_done_max
        + float(forward_fast["max_abs_lateral_displacement_m"])
        + abs(float(forward_fast["mean_lateral_displacement_m"]))
        + float(forward_fast["mean_vel_xy_error"])
        + float(forward_fast["mean_yaw_error"])
    )
    return {
        "task": payload["task"],
        "run_name": checkpoint_path.parent.name,
        "checkpoint": checkpoint,
        "checkpoint_iteration": _checkpoint_iteration(checkpoint),
        "seed": payload["seed"],
        "json": str(path),
        "stand_done": float(results["stand"]["done_fraction"]),
        "forward_done_max": forward_done_max,
        "forward_fast_forward_m": float(forward_fast["mean_forward_displacement_m"]),
        "forward_fast_lateral_m": float(forward_fast["mean_lateral_displacement_m"]),
        "forward_fast_max_abs_lateral_m": float(
            forward_fast["max_abs_lateral_displacement_m"]
        ),
        "forward_fast_vel_error": float(forward_fast["mean_vel_xy_error"]),
        "forward_fast_yaw_error": float(forward_fast["mean_yaw_error"]),
        "yaw_done_max": yaw_done_max,
        "lateral_done_max": lateral_done_max,
        "selection_penalty": selection_penalty,
    }


def _format_value(value: Any) -> str:
    if isinstance(value, float):
        return f"{value:.4f}"
    return str(value)


def _parse_seed_allowlist(value: str | None) -> set[int] | None:
    if value is None:
        return None
    seeds = {int(seed.strip()) for seed in value.split(",") if seed.strip()}
    return seeds


def _aggregate_checkpoint(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        grouped.setdefault(str(row["checkpoint"]), []).append(row)

    aggregated = []
    for checkpoint, checkpoint_rows in grouped.items():
        aggregated.append(
            {
                "checkpoint": checkpoint,
                "seed_count": len(checkpoint_rows),
                "seeds": ",".join(str(row["seed"]) for row in checkpoint_rows),
                "forward_done_max": max(
                    row["forward_done_max"] for row in checkpoint_rows
                ),
                "forward_fast_forward_m_mean": sum(
                    row["forward_fast_forward_m"] for row in checkpoint_rows
                )
                / len(checkpoint_rows),
                "forward_fast_lateral_abs_mean": sum(
                    abs(row["forward_fast_lateral_m"]) for row in checkpoint_rows
                )
                / len(checkpoint_rows),
                "forward_fast_max_abs_lateral_m_max": max(
                    row["forward_fast_max_abs_lateral_m"] for row in checkpoint_rows
                ),
                "forward_fast_vel_error_mean": sum(
                    row["forward_fast_vel_error"] for row in checkpoint_rows
                )
                / len(checkpoint_rows),
                "forward_fast_yaw_error_mean": sum(
                    row["forward_fast_yaw_error"] for row in checkpoint_rows
                )
                / len(checkpoint_rows),
                "yaw_done_max": max(row["yaw_done_max"] for row in checkpoint_rows),
                "lateral_done_max": max(
                    row["lateral_done_max"] for row in checkpoint_rows
                ),
                "selection_penalty_max": max(
                    row["selection_penalty"] for row in checkpoint_rows
                ),
                "selection_penalty_mean": sum(
                    row["selection_penalty"] for row in checkpoint_rows
                )
                / len(checkpoint_rows),
            }
        )
    aggregated.sort(
        key=lambda row: (
            row["selection_penalty_max"],
            row["forward_fast_max_abs_lateral_m_max"],
            row["checkpoint"],
        )
    )
    return aggregated


def _write_markdown(rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    print("| " + " | ".join(fieldnames) + " |")
    print("| " + " | ".join("---" for _ in fieldnames) + " |")
    for row in rows:
        print("| " + " | ".join(_format_value(row[name]) for name in fieldnames) + " |")


def main() -> None:
    args = _parse_args()
    paths = [Path(path) for path in args.paths]
    if not paths:
        paths = [Path(path) for path in glob.glob(args.glob)]
    paths = sorted(path for path in paths if path.is_file())
    rows = [_summarize(path) for path in paths]
    include_seeds = _parse_seed_allowlist(args.include_seeds)
    if include_seeds is not None:
        rows = [row for row in rows if int(row["seed"]) in include_seeds]
    seed_rows = sorted(
        rows,
        key=lambda row: (
            row["selection_penalty"],
            row["checkpoint_iteration"],
            row["seed"],
        ),
    )
    seed_fieldnames = [
        "checkpoint",
        "seed",
        "forward_done_max",
        "forward_fast_forward_m",
        "forward_fast_lateral_m",
        "forward_fast_max_abs_lateral_m",
        "forward_fast_vel_error",
        "forward_fast_yaw_error",
        "yaw_done_max",
        "lateral_done_max",
        "selection_penalty",
        "json",
    ]
    checkpoint_fieldnames = [
        "checkpoint",
        "seed_count",
        "seeds",
        "forward_done_max",
        "forward_fast_forward_m_mean",
        "forward_fast_lateral_abs_mean",
        "forward_fast_max_abs_lateral_m_max",
        "forward_fast_vel_error_mean",
        "forward_fast_yaw_error_mean",
        "yaw_done_max",
        "lateral_done_max",
        "selection_penalty_max",
        "selection_penalty_mean",
    ]
    if args.group_by == "checkpoint":
        rows = _aggregate_checkpoint(seed_rows)
        fieldnames = checkpoint_fieldnames
    else:
        rows = seed_rows
        fieldnames = seed_fieldnames

    if args.format == "csv":
        writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    else:
        _write_markdown(rows, fieldnames)


if __name__ == "__main__":
    main()

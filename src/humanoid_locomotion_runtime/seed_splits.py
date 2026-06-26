"""Deterministic seed split helpers for R016."""

from __future__ import annotations

from collections.abc import Mapping

SCENARIO_SPLIT_ORDER: tuple[str, ...] = ("dev", "train", "val", "test")
DEFAULT_SCENARIO_SPLIT_COUNTS: dict[str, int] = {
    "dev": 12,
    "train": 64,
    "val": 16,
    "test": 32,
}
DEFAULT_ROOT_SEED = 202606260
DEFAULT_STRIDE = 37
DEFAULT_POLICY_TRAINING_SEEDS: tuple[int, ...] = (61001, 61037, 61073, 61109, 61145)


def generate_stride_seed_splits(
    *,
    root_seed: int = DEFAULT_ROOT_SEED,
    stride: int = DEFAULT_STRIDE,
    counts: Mapping[str, int] = DEFAULT_SCENARIO_SPLIT_COUNTS,
) -> dict[str, list[int]]:
    """Generate non-overlapping deterministic scenario seed splits."""
    if stride <= 0:
        raise ValueError("stride must be positive")

    splits: dict[str, list[int]] = {}
    index = 0
    for split_name in SCENARIO_SPLIT_ORDER:
        count = counts[split_name]
        if count <= 0:
            raise ValueError(f"split {split_name!r} must have a positive count")
        splits[split_name] = [root_seed + stride * (index + offset) for offset in range(count)]
        index += count
    return splits


def generate_seed_split_toml() -> str:
    """Return the tracked R016 seed split config as TOML text."""
    splits = generate_stride_seed_splits()
    lines = [
        "schema_version = 1",
        'split_id = "seed_splits_v0_pre_pilot"',
        'status = "frozen_config_no_episode_generation"',
        'generated_by = "scripts/generate_seed_splits.py"',
        'algorithm = "contiguous_stride_sequence"',
        f"root_seed = {DEFAULT_ROOT_SEED}",
        f"stride = {DEFAULT_STRIDE}",
        'note = "Tracked seed lists only; this file does not authorize episode generation."',
        "",
        "[split_counts]",
    ]
    for split_name in SCENARIO_SPLIT_ORDER:
        lines.append(f"{split_name} = {len(splits[split_name])}")

    lines.extend(["", "[scenario_seeds]"])
    for split_name in SCENARIO_SPLIT_ORDER:
        lines.append(f"{split_name} = {_format_toml_int_array(splits[split_name])}")

    lines.extend(
        [
            "",
            "[policy_training_seeds]",
            f"final = {_format_toml_int_array(DEFAULT_POLICY_TRAINING_SEEDS)}",
            "pilot = [61001]",
            "",
        ]
    )
    return "\n".join(lines)


def _format_toml_int_array(values: list[int] | tuple[int, ...]) -> str:
    return "[" + ", ".join(str(value) for value in values) + "]"

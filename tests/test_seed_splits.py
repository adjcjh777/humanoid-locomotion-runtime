from __future__ import annotations

import tomllib
from pathlib import Path

from humanoid_locomotion_runtime.seed_splits import (
    DEFAULT_SCENARIO_SPLIT_COUNTS,
    generate_seed_split_toml,
    generate_stride_seed_splits,
)

CONFIG_PATH = Path("configs/seed_splits.v0.toml")


def load_seed_config() -> dict:
    return tomllib.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def test_seed_split_config_matches_deterministic_generator() -> None:
    assert CONFIG_PATH.read_text(encoding="utf-8") == generate_seed_split_toml()


def test_seed_splits_are_deterministic_and_non_overlapping() -> None:
    config = load_seed_config()
    generated = generate_stride_seed_splits()

    assert config["scenario_seeds"] == generated
    assert config["split_counts"] == DEFAULT_SCENARIO_SPLIT_COUNTS

    all_seeds = [
        seed
        for split_name in ("dev", "train", "val", "test")
        for seed in config["scenario_seeds"][split_name]
    ]
    assert len(all_seeds) == len(set(all_seeds))
    assert len(config["scenario_seeds"]["dev"]) == 12
    assert len(config["scenario_seeds"]["train"]) == 64
    assert len(config["scenario_seeds"]["val"]) == 16
    assert len(config["scenario_seeds"]["test"]) == 32


def test_seed_split_config_does_not_authorize_episode_generation() -> None:
    config = load_seed_config()

    assert config["status"] == "frozen_config_no_episode_generation"
    assert "does not authorize episode generation" in config["note"]
    assert len(config["policy_training_seeds"]["final"]) >= 5

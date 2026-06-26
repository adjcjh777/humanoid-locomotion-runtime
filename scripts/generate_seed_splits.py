#!/usr/bin/env python3
"""Print the deterministic R016 seed split TOML config."""

from __future__ import annotations

from humanoid_locomotion_runtime.seed_splits import generate_seed_split_toml


def main() -> None:
    print(generate_seed_split_toml(), end="")


if __name__ == "__main__":
    main()

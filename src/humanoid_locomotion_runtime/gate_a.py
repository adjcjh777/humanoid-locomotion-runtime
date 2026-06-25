"""Gate A repository foundation checks."""

from __future__ import annotations

from pathlib import Path

REQUIRED_GATE_A_PATHS = (
    ".python-version",
    "pyproject.toml",
    "uv.lock",
    "LICENSE",
    ".github/workflows/ci.yml",
    "configs/environment.lock.toml",
    "configs/artifact_retention.toml",
    "src/humanoid_locomotion_runtime/__init__.py",
    "src/humanoid_locomotion_runtime/gate_a.py",
    "tests/test_gate_a_foundation.py",
)

PRIVATE_OR_GENERATED_GITIGNORE_PATTERNS = (
    ".aris/meta/",
    ".aris/traces/",
    "runs/",
    "logs/",
    "artifacts/",
    "checkpoints/",
    "weights/",
    "datasets/",
)


def repo_root_from(path: Path | None = None) -> Path:
    """Return the repository root by walking upward from path or cwd."""
    cursor = (path or Path.cwd()).resolve()
    if cursor.is_file():
        cursor = cursor.parent
    for candidate in (cursor, *cursor.parents):
        if (candidate / ".git").exists():
            return candidate
    raise RuntimeError(f"Could not locate repository root from {cursor}")


def missing_gate_a_paths(root: Path | None = None) -> list[str]:
    """List Gate A files that are expected to exist."""
    repo_root = repo_root_from(root)
    return [relative for relative in REQUIRED_GATE_A_PATHS if not (repo_root / relative).exists()]


def missing_gitignore_patterns(root: Path | None = None) -> list[str]:
    """List private/generated path patterns missing from .gitignore."""
    repo_root = repo_root_from(root)
    gitignore = (repo_root / ".gitignore").read_text(encoding="utf-8")
    return [
        pattern
        for pattern in PRIVATE_OR_GENERATED_GITIGNORE_PATTERNS
        if pattern not in gitignore
    ]

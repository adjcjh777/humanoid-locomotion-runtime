"""Episode Data Package writer and validator."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, ValidationError

from humanoid_locomotion_runtime.schemas import (
    EpisodeManifest,
    EpisodeMetrics,
    EpisodeReplayIndex,
    OracleAnnotation,
    RetentionClass,
    RuntimeEvent,
    RuntimeEventType,
)

MANIFEST_FILE = "episode_manifest.json"
EVENTS_FILE = "events.jsonl"
METRICS_FILE = "metrics.json"
REPLAY_INDEX_FILE = "replay_index.json"
ORACLE_ANNOTATIONS_FILE = "oracle_annotations.jsonl"
TIMESERIES_DIR = "timeseries"
ARTIFACTS_DIR = "artifacts"

REQUIRED_EDP_PATHS = (
    MANIFEST_FILE,
    EVENTS_FILE,
    METRICS_FILE,
    REPLAY_INDEX_FILE,
    TIMESERIES_DIR,
    ARTIFACTS_DIR,
)


class EDPValidationResult(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    path: str
    valid: bool
    errors: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    event_count: int = 0
    oracle_annotation_count: int = 0


class EpisodeDataPackageWriter:
    """Write the minimal EDP directory contract without requiring MuJoCo."""

    def __init__(
        self,
        root: Path | str,
        manifest: EpisodeManifest,
        *,
        overwrite: bool = False,
    ) -> None:
        self.root = Path(root)
        self.manifest = manifest
        self.overwrite = overwrite

    @property
    def events_path(self) -> Path:
        return self.root / EVENTS_FILE

    @property
    def oracle_annotations_path(self) -> Path:
        return self.root / ORACLE_ANNOTATIONS_FILE

    def initialize(self) -> None:
        if self.root.exists() and any(self.root.iterdir()) and not self.overwrite:
            raise FileExistsError(f"EDP root already exists and is not empty: {self.root}")

        self.root.mkdir(parents=True, exist_ok=True)
        (self.root / TIMESERIES_DIR).mkdir(exist_ok=True)
        (self.root / ARTIFACTS_DIR).mkdir(exist_ok=True)
        self._write_model_json(self.root / MANIFEST_FILE, self.manifest)
        self.events_path.touch(exist_ok=True)
        self.write_replay_index(EpisodeReplayIndex(episode_id=self.manifest.episode_id))

    def append_event(self, event: RuntimeEvent) -> None:
        self._ensure_initialized()
        self._ensure_episode_id(event.episode_id)
        self._append_model_jsonl(self.events_path, event)

    def append_oracle_annotation(self, annotation: OracleAnnotation) -> None:
        self._ensure_initialized()
        self._ensure_episode_id(annotation.episode_id)
        self._append_model_jsonl(self.oracle_annotations_path, annotation)

    def write_metrics(self, metrics: EpisodeMetrics) -> None:
        self._ensure_initialized()
        self._ensure_episode_id(metrics.episode_id)
        self._write_model_json(self.root / METRICS_FILE, metrics)

    def write_replay_index(self, replay_index: EpisodeReplayIndex) -> None:
        self._ensure_episode_id(replay_index.episode_id)
        self._write_model_json(self.root / REPLAY_INDEX_FILE, replay_index)

    def _ensure_initialized(self) -> None:
        if not (self.root / MANIFEST_FILE).exists():
            raise RuntimeError("EDP writer must be initialized before writing records")

    def _ensure_episode_id(self, episode_id: str) -> None:
        if episode_id != self.manifest.episode_id:
            raise ValueError(
                f"record episode_id {episode_id!r} does not match "
                f"manifest episode_id {self.manifest.episode_id!r}"
            )

    @staticmethod
    def _write_model_json(path: Path, model: BaseModel) -> None:
        path.write_text(model.model_dump_json(indent=2) + "\n", encoding="utf-8")

    @staticmethod
    def _append_model_jsonl(path: Path, model: BaseModel) -> None:
        with path.open("a", encoding="utf-8") as handle:
            handle.write(model.model_dump_json() + "\n")


class RuntimeEventLogger:
    """Small event logger that writes validated RuntimeEvent JSONL records."""

    def __init__(self, writer: EpisodeDataPackageWriter) -> None:
        self.writer = writer

    def record(
        self,
        *,
        event_id: str,
        timestamp_s: float,
        event_type: RuntimeEventType,
        message: str,
        data: dict[str, Any] | None = None,
    ) -> RuntimeEvent:
        event = RuntimeEvent(
            event_id=event_id,
            episode_id=self.writer.manifest.episode_id,
            timestamp_s=timestamp_s,
            event_type=event_type,
            message=message,
            data=data or {},
        )
        self.writer.append_event(event)
        return event


def write_sample_episode_data_package(
    root: Path | str,
    *,
    episode_id: str = "gate-b-sample",
    retention_class: RetentionClass = "pilot_evaluation",
) -> Path:
    """Create a minimal, schema-valid EDP for Gate B smoke tests."""
    root = Path(root)
    manifest = EpisodeManifest(
        episode_id=episode_id,
        retention_class=retention_class,
        scenario_id="schema-smoke",
        scenario_seed=0,
        policy_name="schema_smoke_policy",
        controller_backend="none",
        robot_model="none",
        code_version="gate-b",
    )
    writer = EpisodeDataPackageWriter(root, manifest)
    writer.initialize()

    event_logger = RuntimeEventLogger(writer)
    event_logger.record(
        event_id="evt-0001",
        timestamp_s=0.0,
        event_type="edp",
        message="sample EDP writer smoke",
        data={"gate": "B", "requires_mujoco": False},
    )
    writer.append_oracle_annotation(
        OracleAnnotation(
            annotation_id="ora-0001",
            episode_id=episode_id,
            timestamp_s=0.0,
            decision_id="dec-0001",
            true_failure_cause="schema_smoke",
            true_temporal_profile="none",
            oracle_action="continue",
            mujoco_object_id="evaluation-only-object",
            ground_truth_target_pose=(0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
            simulator_semantic_label="evaluation-only-label",
        )
    )
    writer.write_metrics(
        EpisodeMetrics(
            episode_id=episode_id,
            task_success=None,
            recovery_success=None,
            policy_only_outcome="not_run",
            full_stack_with_fallback_outcome="not_run",
            total_duration_s=0.0,
            custom_metrics={"sample_package": True},
        )
    )
    return root


def validate_episode_data_package(root: Path | str) -> EDPValidationResult:
    """Validate the minimal EDP directory and schema contract."""
    root = Path(root)
    errors: list[str] = []
    warnings: list[str] = []
    event_count = 0
    oracle_annotation_count = 0

    if not root.exists():
        return EDPValidationResult(
            path=str(root),
            valid=False,
            errors=[f"EDP root does not exist: {root}"],
        )

    for relative_path in REQUIRED_EDP_PATHS:
        path = root / relative_path
        if not path.exists():
            errors.append(f"missing required EDP path: {relative_path}")
        elif relative_path in {TIMESERIES_DIR, ARTIFACTS_DIR} and not path.is_dir():
            errors.append(f"required EDP path is not a directory: {relative_path}")
        elif relative_path not in {TIMESERIES_DIR, ARTIFACTS_DIR} and not path.is_file():
            errors.append(f"required EDP path is not a file: {relative_path}")

    manifest = _parse_model_file(root / MANIFEST_FILE, EpisodeManifest, errors)
    metrics = _parse_model_file(root / METRICS_FILE, EpisodeMetrics, errors)
    replay_index = _parse_model_file(root / REPLAY_INDEX_FILE, EpisodeReplayIndex, errors)

    events = _parse_jsonl_file(root / EVENTS_FILE, RuntimeEvent, errors)
    event_count = len(events)
    if (root / EVENTS_FILE).exists() and event_count == 0:
        errors.append("events.jsonl must contain at least one RuntimeEvent")

    oracle_annotations = _parse_jsonl_file(
        root / ORACLE_ANNOTATIONS_FILE,
        OracleAnnotation,
        errors,
        required=False,
    )
    oracle_annotation_count = len(oracle_annotations)

    expected_episode_id = manifest.episode_id if manifest else None
    if expected_episode_id:
        _check_episode_id("metrics.json", metrics, expected_episode_id, errors)
        _check_episode_id("replay_index.json", replay_index, expected_episode_id, errors)
        for index, event in enumerate(events, start=1):
            _check_episode_id(f"events.jsonl:{index}", event, expected_episode_id, errors)
        for index, annotation in enumerate(oracle_annotations, start=1):
            _check_episode_id(
                f"oracle_annotations.jsonl:{index}",
                annotation,
                expected_episode_id,
                errors,
            )

    if oracle_annotation_count == 0:
        warnings.append(
            "oracle_annotations.jsonl is absent or empty; evaluation labels are optional"
        )

    return EDPValidationResult(
        path=str(root),
        valid=not errors,
        errors=errors,
        warnings=warnings,
        event_count=event_count,
        oracle_annotation_count=oracle_annotation_count,
    )


def assert_valid_episode_data_package(root: Path | str) -> EDPValidationResult:
    """Return the validation result or raise with all validation errors."""
    result = validate_episode_data_package(root)
    if not result.valid:
        raise ValueError("; ".join(result.errors))
    return result


def _parse_model_file(
    path: Path,
    model_type: type[BaseModel],
    errors: list[str],
) -> BaseModel | None:
    if not path.exists():
        return None
    try:
        return model_type.model_validate_json(path.read_text(encoding="utf-8"))
    except (OSError, ValidationError, ValueError) as exc:
        errors.append(f"{path.name} failed schema validation: {exc}")
        return None


def _parse_jsonl_file(
    path: Path,
    model_type: type[BaseModel],
    errors: list[str],
    *,
    required: bool = True,
) -> list[BaseModel]:
    if not path.exists():
        if required:
            errors.append(f"missing required JSONL file: {path.name}")
        return []

    records: list[BaseModel] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        errors.append(f"{path.name} could not be read: {exc}")
        return []

    for index, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            records.append(model_type.model_validate_json(line))
        except (ValidationError, ValueError) as exc:
            errors.append(f"{path.name}:{index} failed schema validation: {exc}")
    return records


def _check_episode_id(
    label: str,
    record: BaseModel | None,
    expected_episode_id: str,
    errors: list[str],
) -> None:
    if record is None:
        return
    observed_episode_id = getattr(record, "episode_id", None)
    if observed_episode_id != expected_episode_id:
        errors.append(
            f"{label} episode_id {observed_episode_id!r} does not match "
            f"manifest episode_id {expected_episode_id!r}"
        )

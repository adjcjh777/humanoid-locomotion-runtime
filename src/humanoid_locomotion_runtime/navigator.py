"""Backend-neutral NavigatorV0 local planning skeleton."""

from __future__ import annotations

import math
from typing import Literal

from pydantic import Field, field_validator

from humanoid_locomotion_runtime.schemas import (
    FailureEvent,
    JsonDict,
    LocomotionCommand,
    Pose2D,
    StrictSchema,
    assert_no_privileged_keys,
)

XY = tuple[float, float]
ObstacleSource = Literal["grounding", "memory", "operator", "test_fixture"]


class LocalObstacle(StrictSchema):
    obstacle_id: str
    center_xy: XY
    radius_m: float = Field(ge=0)
    observed_at_s: float = Field(ge=0)
    source: ObstacleSource = "grounding"
    metadata: JsonDict = Field(default_factory=dict)

    @field_validator("metadata")
    @classmethod
    def _metadata_has_no_privileged_keys(cls, value: JsonDict) -> JsonDict:
        assert_no_privileged_keys(value, "LocalObstacle.metadata")
        return value


class LocalRoute(StrictSchema):
    route_id: str
    start_pose: Pose2D
    goal_pose: Pose2D
    waypoints: list[Pose2D] = Field(default_factory=list)
    blocked: bool = False
    reason: str = "direct_path_clear"
    blocking_obstacle_ids: list[str] = Field(default_factory=list)
    failure_event: FailureEvent | None = None
    metadata: JsonDict = Field(default_factory=dict)

    @field_validator("metadata")
    @classmethod
    def _metadata_has_no_privileged_keys(cls, value: JsonDict) -> JsonDict:
        assert_no_privileged_keys(value, "LocalRoute.metadata")
        return value


class NavigatorV0:
    """Small geometry-only planner used to validate interfaces on Mac."""

    def __init__(
        self,
        *,
        clearance_m: float = 0.25,
        detour_margin_m: float = 0.35,
        allow_detour: bool = True,
    ) -> None:
        if clearance_m < 0:
            raise ValueError("clearance_m must be non-negative")
        if detour_margin_m <= 0:
            raise ValueError("detour_margin_m must be positive")
        self.clearance_m = clearance_m
        self.detour_margin_m = detour_margin_m
        self.allow_detour = allow_detour

    def plan_route(
        self,
        *,
        route_id: str,
        start_pose: Pose2D,
        goal_pose: Pose2D,
        obstacles: list[LocalObstacle],
        timestamp_s: float,
    ) -> LocalRoute:
        if _same_xy(start_pose, goal_pose):
            return LocalRoute(
                route_id=route_id,
                start_pose=start_pose,
                goal_pose=goal_pose,
                waypoints=[],
                reason="already_at_goal",
                metadata={"planner_scope": "mac_safe_geometry_only"},
            )

        direct_blockers = self._blocking_obstacles(start_pose, goal_pose, obstacles)
        if not direct_blockers:
            return LocalRoute(
                route_id=route_id,
                start_pose=start_pose,
                goal_pose=goal_pose,
                waypoints=[goal_pose],
                metadata={"planner_scope": "mac_safe_geometry_only"},
            )

        if self.allow_detour:
            detour = self._find_detour(start_pose, goal_pose, obstacles, direct_blockers[0])
            if detour is not None:
                return LocalRoute(
                    route_id=route_id,
                    start_pose=start_pose,
                    goal_pose=goal_pose,
                    waypoints=[detour, goal_pose],
                    reason="single_obstacle_detour_planned",
                    blocking_obstacle_ids=[obstacle.obstacle_id for obstacle in direct_blockers],
                    metadata={"planner_scope": "mac_safe_geometry_only"},
                )

        blocker_ids = [obstacle.obstacle_id for obstacle in direct_blockers]
        return LocalRoute(
            route_id=route_id,
            start_pose=start_pose,
            goal_pose=goal_pose,
            blocked=True,
            reason="no_feasible_local_route",
            blocking_obstacle_ids=blocker_ids,
            failure_event=FailureEvent(
                failure_id=f"failure-{route_id}",
                timestamp_s=timestamp_s,
                runtime_failure_kind="local_route_blocked",
                temporal_profile_hint="persistent",
                severity=min(1.0, 0.5 + 0.1 * len(blocker_ids)),
                evidence={
                    "route_id": route_id,
                    "blocking_obstacle_ids": blocker_ids,
                    "planner_scope": "mac_safe_geometry_only",
                },
            ),
            metadata={"planner_scope": "mac_safe_geometry_only"},
        )

    def command_for_next_waypoint(
        self,
        route: LocalRoute,
        *,
        command_id: str,
        issued_at_s: float,
        episode_id: str | None = None,
    ) -> LocomotionCommand:
        metadata: JsonDict = {"route_id": route.route_id}
        if episode_id is not None:
            metadata["episode_id"] = episode_id
        if route.blocked:
            raise ValueError("blocked routes cannot produce walk_to commands")
        if not route.waypoints:
            return LocomotionCommand(
                command_id=command_id,
                mode="stand_ready",
                issued_at_s=issued_at_s,
                metadata=metadata,
            )
        return LocomotionCommand(
            command_id=command_id,
            mode="walk_to",
            issued_at_s=issued_at_s,
            target_pose=route.waypoints[0],
            metadata=metadata,
        )

    def _blocking_obstacles(
        self,
        start_pose: Pose2D,
        goal_pose: Pose2D,
        obstacles: list[LocalObstacle],
    ) -> list[LocalObstacle]:
        return [
            obstacle
            for obstacle in obstacles
            if _segment_intersects_obstacle(
                start_pose,
                goal_pose,
                obstacle,
                clearance_m=self.clearance_m,
            )
        ]

    def _find_detour(
        self,
        start_pose: Pose2D,
        goal_pose: Pose2D,
        obstacles: list[LocalObstacle],
        primary_blocker: LocalObstacle,
    ) -> Pose2D | None:
        start_xy = (start_pose[0], start_pose[1])
        goal_xy = (goal_pose[0], goal_pose[1])
        dx = goal_xy[0] - start_xy[0]
        dy = goal_xy[1] - start_xy[1]
        length = math.hypot(dx, dy)
        if length == 0:
            return None
        normal = (-dy / length, dx / length)
        offset = primary_blocker.radius_m + self.clearance_m + self.detour_margin_m
        candidates = [
            (
                primary_blocker.center_xy[0] + normal[0] * offset,
                primary_blocker.center_xy[1] + normal[1] * offset,
                goal_pose[2],
            ),
            (
                primary_blocker.center_xy[0] - normal[0] * offset,
                primary_blocker.center_xy[1] - normal[1] * offset,
                goal_pose[2],
            ),
        ]
        for candidate in candidates:
            if self._path_clear([start_pose, candidate, goal_pose], obstacles):
                return candidate
        return None

    def _path_clear(self, waypoints: list[Pose2D], obstacles: list[LocalObstacle]) -> bool:
        return all(
            not _segment_intersects_obstacle(
                start,
                goal,
                obstacle,
                clearance_m=self.clearance_m,
            )
            for start, goal in zip(waypoints, waypoints[1:], strict=False)
            for obstacle in obstacles
        )


def _same_xy(start_pose: Pose2D, goal_pose: Pose2D) -> bool:
    return math.isclose(start_pose[0], goal_pose[0]) and math.isclose(start_pose[1], goal_pose[1])


def _segment_intersects_obstacle(
    start_pose: Pose2D,
    goal_pose: Pose2D,
    obstacle: LocalObstacle,
    *,
    clearance_m: float,
) -> bool:
    distance = _point_to_segment_distance(
        obstacle.center_xy,
        (start_pose[0], start_pose[1]),
        (goal_pose[0], goal_pose[1]),
    )
    return distance <= obstacle.radius_m + clearance_m


def _point_to_segment_distance(point: XY, start: XY, goal: XY) -> float:
    dx = goal[0] - start[0]
    dy = goal[1] - start[1]
    length_squared = dx * dx + dy * dy
    if length_squared == 0:
        return math.hypot(point[0] - start[0], point[1] - start[1])
    t = ((point[0] - start[0]) * dx + (point[1] - start[1]) * dy) / length_squared
    t = max(0.0, min(1.0, t))
    projection = (start[0] + t * dx, start[1] + t * dy)
    return math.hypot(point[0] - projection[0], point[1] - projection[1])

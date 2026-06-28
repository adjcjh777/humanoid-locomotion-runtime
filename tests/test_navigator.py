from __future__ import annotations

import pytest
from pydantic import ValidationError

from humanoid_locomotion_runtime.navigator import LocalObstacle, NavigatorV0


def test_navigator_v0_returns_direct_walk_to_command_when_path_is_clear() -> None:
    navigator = NavigatorV0()
    route = navigator.plan_route(
        route_id="route-clear",
        start_pose=(0.0, 0.0, 0.0),
        goal_pose=(1.0, 0.0, 0.0),
        obstacles=[],
        timestamp_s=1.0,
    )
    command = navigator.command_for_next_waypoint(
        route,
        command_id="cmd-route-clear",
        issued_at_s=1.0,
        episode_id="episode-001",
    )

    assert route.blocked is False
    assert route.waypoints == [(1.0, 0.0, 0.0)]
    assert command.mode == "walk_to"
    assert command.target_pose == (1.0, 0.0, 0.0)
    assert command.metadata["route_id"] == "route-clear"


def test_navigator_v0_plans_simple_detour_around_single_obstacle() -> None:
    navigator = NavigatorV0(clearance_m=0.2, detour_margin_m=0.3)
    obstacle = LocalObstacle(
        obstacle_id="obs-1",
        center_xy=(0.5, 0.0),
        radius_m=0.1,
        observed_at_s=1.0,
    )

    route = navigator.plan_route(
        route_id="route-detour",
        start_pose=(0.0, 0.0, 0.0),
        goal_pose=(1.0, 0.0, 0.0),
        obstacles=[obstacle],
        timestamp_s=1.0,
    )

    assert route.blocked is False
    assert route.reason == "single_obstacle_detour_planned"
    assert route.blocking_obstacle_ids == ["obs-1"]
    assert len(route.waypoints) == 2
    assert route.waypoints[-1] == (1.0, 0.0, 0.0)


def test_navigator_v0_reports_blocked_route_with_failure_event() -> None:
    navigator = NavigatorV0(clearance_m=0.2, allow_detour=False)
    obstacle = LocalObstacle(
        obstacle_id="obs-1",
        center_xy=(0.5, 0.0),
        radius_m=0.2,
        observed_at_s=1.0,
    )

    route = navigator.plan_route(
        route_id="route-blocked",
        start_pose=(0.0, 0.0, 0.0),
        goal_pose=(1.0, 0.0, 0.0),
        obstacles=[obstacle],
        timestamp_s=2.0,
    )

    assert route.blocked is True
    assert route.failure_event is not None
    assert route.failure_event.runtime_failure_kind == "local_route_blocked"
    assert route.failure_event.evidence["blocking_obstacle_ids"] == ["obs-1"]
    with pytest.raises(ValueError, match="blocked routes"):
        navigator.command_for_next_waypoint(
            route,
            command_id="cmd-blocked",
            issued_at_s=2.0,
        )


def test_navigator_v0_rejects_privileged_obstacle_metadata() -> None:
    with pytest.raises(ValidationError, match="mujoco_object_id"):
        LocalObstacle(
            obstacle_id="obs-bad",
            center_xy=(0.5, 0.0),
            radius_m=0.2,
            observed_at_s=1.0,
            metadata={"mujoco_object_id": "object-42"},
        )

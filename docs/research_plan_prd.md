# Language-Conditioned Humanoid Locomotion Runtime with Body Memory and Recovery

## 0. Project Record

- **Project name**: Humanoid Locomotion Runtime
- **Initial platform**: MuJoCo + Unitree G1 humanoid model
- **Secondary platform**: `bxi_elf3` / `bxi_robotics` for later cross-embodiment validation
- **Future platform**: company-developed humanoid body
- **Primary goal**: build a practical, research-grade humanoid locomotion runtime that turns language-conditioned and open-vocabulary grounded goals into monitorable, recoverable humanoid locomotion skills.
- **Non-claim**: this project does not train a foundation-scale end-to-end VLA that maps raw image/language directly to humanoid joint actions.
- **V0 research stance**: system/runtime paper first, low-level controller innovation optional and only promoted if it produces clear evidence.

---

## 1. Executive Summary

### Problem Statement

Existing humanoid locomotion controllers can often walk, turn, and track commands in controlled settings, but they are usually exposed as low-level motion backends. They do not naturally provide task-level evidence such as why execution became unsafe, whether a failure is recoverable, which recovery action was tried, or how language-conditioned goals should be re-grounded after perception or navigation failure.

For a language-conditioned humanoid agent, ordinary goal-reaching metrics hide many important failures: the robot may reach a target only because the scenario is easy, while failing under dynamic obstacles, localization drift, velocity tracking error, balance risk, target loss, or user interruption.

### Proposed Solution

Build a language-conditioned humanoid locomotion runtime around a mature Unitree G1 locomotion controller in MuJoCo. The runtime uses open-vocabulary target grounding, temporary object memory, an MPC/optimization-based local planner, typed locomotion skills, status monitoring, body memory, a rule-based recovery policy, and a Viser-based WebUI dashboard.

The first implementation keeps the core runtime single-manager and deterministic, while exposing TaskRouter, AgentPort, EventStore, and typed command interfaces so it can later evolve into a multi-agent runtime. Real-time safety remains local to RuntimeManager and SafetySupervisor; Agent Bus is reserved for high-level asynchronous coordination, audit, and experiment analysis.

### Success Criteria

V0 is successful when all of the following are true:

1. **Runtime completion**: the system can execute language-conditioned local locomotion tasks in MuJoCo with Unitree G1 through typed commands, open-vocabulary grounding, local planning, skill execution, status monitoring, and recovery.
2. **Benchmark coverage**: the benchmark includes at least five failure families with at least 20 episodes each: dynamic obstacle, localization drift, velocity tracking failure, balance risk, and target change/user interruption.
3. **Ablation evidence**: the five planned baselines run on the same benchmark: `controller_only`, `controller_local_planner`, `status_monitor_only`, `full_no_body_memory`, and `full_body_memory_recovery`.
4. **Data completeness**: every episode writes a complete Episode Data Package including manifests, event logs, metrics, timeseries, and artifacts.
5. **Debuggability**: Viser dashboard can inspect live or replayed episodes with 3D scene state, camera/grounding output, runtime status, body memory, recovery decisions, and benchmark metrics.
6. **Safety boundary**: WebUI and future agents can only issue high-level typed commands; they cannot directly bypass RuntimeManager or SafetySupervisor to control low-level humanoid actuators.

---

## 2. Product / Research Positioning

### Core Positioning

This project is not "a smaller HoloAgent" and not "a new humanoid foundation model." It is a focused humanoid locomotion runtime:

> When a mature humanoid controller already provides basic locomotion, how can language-conditioned goals be grounded, executed, monitored, recovered, logged, and evaluated as reliable humanoid skills?

### V0 Research Hypotheses

These are initial working hypotheses, not final locked paper claims.

1. **Runtime hypothesis**: a structured humanoid locomotion runtime can convert language-conditioned goals into monitorable locomotion skills without requiring end-to-end VLA training.
2. **Body memory hypothesis**: body memory improves recovery decisions beyond instant robot state by preserving short-window stability summaries and recovery history.
3. **Benchmark hypothesis**: a failure-recovery benchmark reveals weaknesses hidden by ordinary goal-reaching metrics.

### Potential V1 / V2 Upgrades

The system should preserve space for stronger claims if later evidence supports them:

- adaptive learned recovery policy outperforming rule-based recovery;
- cross-embodiment transfer from Unitree G1 to `bxi_elf3` or company humanoid body;
- persistent full 3D semantic memory replacing temporary object memory;
- global navigation and active exploration;
- multi-agent runtime manager with task router and auditable Agent Bus coordination;
- residual or status-conditioned controller adaptation;
- sim-to-real transfer and hardware evaluation.

---

## 3. Personas, User Stories, and Acceptance Criteria

### Personas

1. **Research developer**
   - Needs a modular runtime to test humanoid locomotion recovery ideas quickly.
2. **Benchmark runner**
   - Needs reproducible batch experiments and comparable metrics across ablations.
3. **Debug operator**
   - Needs a live dashboard to inspect robot state, target grounding, route, failure, and recovery.
4. **Future multi-agent orchestrator**
   - Needs typed task/event interfaces so planner/recovery/evaluator agents can be separated later.

### User Stories

#### Story 1: Execute Language-Conditioned Humanoid Locomotion

As a research developer, I want to submit a language instruction such as "walk to the red chair slowly" so that the runtime can parse the command, ground the target, plan a safe local route, execute a G1 locomotion skill, monitor status, and recover if something fails.

Acceptance criteria:

- Instruction is converted into a structured locomotion command.
- Target grounding uses RGB-D and open-vocabulary detector output, not MuJoCo privileged object id.
- Temporary object memory records target evidence and safe stop pose.
- Locomotion skill runs through a mature G1 controller backend.
- Runtime logs every major event to the Episode Data Package.

#### Story 2: Recover from Runtime Failures

As a benchmark runner, I want the system to detect failure modes such as path blockage, localization drift, velocity tracking error, balance risk, target loss, or user interruption so that recovery actions can be selected and evaluated.

Acceptance criteria:

- Failure mode taxonomy supports the 16 V0 failure modes.
- Recovery action taxonomy supports the 18 V0 actions.
- First implementation supports the core 10 recovery actions.
- Recovery decisions are recorded with pre-status, post-status, latency, success, and fallback.
- Repeated failures are visible through body memory event records.

#### Story 3: Compare Ablations

As a researcher, I want to run the same benchmark across `controller_only`, `controller_local_planner`, `status_monitor_only`, `full_no_body_memory`, and `full_body_memory_recovery` so that the contribution of body memory and recovery policy is measurable.

Acceptance criteria:

- Each baseline runs through the same scenario definitions and logging pipeline.
- Metrics include task success, recovery success, collision count, fall/unstable count, stop latency, path efficiency, repeated failure count, and human intervention count.
- Batch runner produces run-level summary tables.
- Episode-level artifacts are retained for failure diagnosis.

#### Story 4: Debug with WebUI Dashboard

As a debug operator, I want a Viser-based WebUI to inspect the live or replayed robot scene so that I can understand why an episode failed and whether recovery behavior is correct.

Acceptance criteria:

- Dashboard shows 3D robot pose, target pose, safe stop pose, obstacles, route, replan points, and blocked regions.
- Dashboard shows camera/grounding outputs with bounding boxes or masks when available.
- Dashboard shows body memory traces and recovery events.
- Dashboard can issue only high-level typed UI commands through RuntimeManager.
- Dashboard cannot directly command low-level controller, velocity, joint targets, or safety override.

### Non-Goals for V0

V0 does not attempt:

- end-to-end VLA training from image/language to humanoid joint actions;
- full persistent 3D semantic memory with floor-room-view-object HMSG;
- multi-room global navigation and active exploration in the first implementation;
- direct real-hardware safety guarantee;
- new whole-body controller as the main contribution;
- multi-agent runtime execution in the real-time loop;
- using MuJoCo object id, privileged target pose, or simulator semantic label as runtime inputs.

---

## 4. System Architecture

### High-Level Data Flow

```text
Language instruction
  -> LLM / rule-assisted parser
  -> Structured locomotion command
  -> Open-vocabulary grounding
  -> Temporary object memory
  -> Safe stop pose generation
  -> NavigatorV0 local planner
  -> Locomotion skill manager
  -> Mature Unitree G1 controller backend
  -> Status monitor
  -> Body memory
  -> Rule-based recovery policy
  -> Safety supervisor
  -> EventStore + Episode Data Package + Viser dashboard
```

### Runtime Components

```text
RuntimeManager
  -> TaskRouter
  -> EventStore
  -> AgentPort interface
  -> LanguageParser
  -> OpenVocabGrounder
  -> TemporaryObjectMemory
  -> NavigatorV0
  -> LocomotionSkillManager
  -> StatusMonitor
  -> BodyMemory
  -> RuleBasedRecoveryPolicy
  -> SafetySupervisor
  -> BenchmarkLogger
  -> ViserDashboardPublisher
```

### Real-Time and Agent Coordination Boundary

The system has two communication layers:

| Layer | Purpose | Mechanism |
|---|---|---|
| Real-time runtime bus | robot execution, status updates, risk, local recovery, safety | ROS2, Python async queue, gRPC, or shared runtime state |
| Agent coordination bus | high-level asynchronous tasks, auditing, long-horizon replanning, experiment analysis | TaskRouter, AgentPort, Agent Bus later |

Rules:

- Safety-critical execution does not wait for an LLM or Agent Bus response.
- SafetySupervisor is local, synchronous, and has authority to stop or override unsafe execution.
- Agent suggestions are typed recommendations, not final execution authority.
- Every agent task carries `task_id`, `correlation_id`, `source`, `target_role`, `deadline_ms`, `priority`, and fallback.

---

## 5. Module Definitions

### 5.1 Language Parser

Purpose:

- Convert user instruction into structured locomotion command.

V0 input:

```text
"walk to the red chair slowly"
```

V0 output:

```json
{
  "intent": "walk_to",
  "target": {
    "type": "object_or_pose",
    "text": "red chair",
    "distance": 0.8
  },
  "motion_style": {
    "speed": "slow",
    "stability": "high",
    "human_distance": 1.0
  },
  "constraints": {
    "avoid_obstacles": true,
    "allow_replan": true,
    "stop_on_uncertainty": true
  }
}
```

V0 boundary:

- Parser is not the paper contribution.
- Parser can use LLM, rules, or a hybrid.
- Parser output must be schema-validated before entering runtime.

### 5.2 Open-Vocabulary Grounder

Purpose:

- Ground a text target such as "red chair" into visual detections and 3D target candidates.

V0 design:

- Fast path: YOLO-World.
- Fallback path: GroundingDINO + SAM2.
- Runtime inputs: RGB, depth, camera intrinsics/extrinsics, robot state.
- Forbidden runtime inputs: MuJoCo object id, ground-truth target pose, simulator semantic label.
- Evaluation-only inputs: MuJoCo object id, object pose, contacts, fall state.

Output schema:

```json
{
  "label": "red chair",
  "bbox": [120, 80, 260, 310],
  "mask_id": "mask_03",
  "confidence": 0.78,
  "source": "yolo_world",
  "position_3d": [2.1, -0.4, 0.0],
  "frame_id": "camera_front",
  "world_frame": "map"
}
```

### 5.3 Memory Interface

Purpose:

- Provide a common interface for V0 temporary object memory and future persistent 3D semantic memory.

V0 memory backend:

- `temporary_object_memory`
- episode-level lifetime
- stores target detections, 3D position, confidence, safe stop pose, and grounding status

Required APIs:

1. `write_observation(obs)`
2. `query_target(text, constraints)`
3. `get_safe_stop_pose(instance_id, robot_state)`
4. `update_status(instance_id, status)`
5. `expire(scope)`

Temporary object memory record:

```json
{
  "memory_backend": "temporary_object_memory",
  "instance_id": "tmp_red_chair_001",
  "query_text": "red chair",
  "label": "red chair",
  "bbox": [120, 80, 260, 310],
  "mask": "optional",
  "confidence": 0.72,
  "position_3d": [2.1, -0.4, 0.0],
  "safe_stop_pose": [1.6, -0.4, 0.0, 1.57],
  "frame_id": "camera_front",
  "world_frame": "map",
  "timestamp": 123.45,
  "source": "yolo_world",
  "status": "active",
  "ttl": "one_episode"
}
```

Future persistent memory record:

```json
{
  "memory_backend": "persistent_3d_semantic_memory",
  "instance_id": "chair_red_042",
  "room_id": "living_room",
  "view_ids": ["view_03", "view_09"],
  "semantic_feature": "...",
  "point_cloud_ref": "...",
  "last_seen": 123.45,
  "history": ["moved", "occluded", "verified"],
  "relations": ["near table_01", "facing sofa_02"]
}
```

### 5.4 NavigatorV0

Purpose:

- Generate short-horizon route or velocity targets from grounded safe stop poses while avoiding local obstacles.

V0 scope:

- local target approach;
- local obstacle avoidance;
- future-ready interface for global navigation and exploration;
- no full global planner in first implementation.

Planner choice:

- MPC / optimization-based local planner + safety shield.
- Not a learned obstacle avoidance model.
- Not hand-written if-else geometry rules as the main method.

Required APIs:

1. `plan_to_target(target, robot_state, constraints)`
2. `validate_route(route, memory, robot_state)`
3. `replan(reason, current_route, memory)`
4. `report_blockage(evidence)`
5. `next_subgoal(route, robot_state)`

Route output schema:

```json
{
  "route_id": "route_001",
  "scope": "local",
  "subgoals": [
    {
      "pose": [1.2, 0.4, 0.0, 1.57],
      "type": "safe_stop_pose",
      "tolerance": 0.3
    }
  ],
  "risk": {
    "collision": "low",
    "terrain": "flat",
    "localization": "ok"
  },
  "status": "valid"
}
```

Future global route schema:

```json
{
  "route_id": "route_global_001",
  "scope": "global",
  "subgoals": [
    {"type": "room_waypoint", "pose": [0.5, 2.0, 0.0, 1.57]},
    {"type": "corridor_waypoint", "pose": [1.5, 2.0, 0.0, 0.0]},
    {"type": "target_viewpoint", "pose": [2.3, -0.2, 0.0, 1.57]},
    {"type": "safe_stop_pose", "pose": [2.0, -0.4, 0.0, 1.57]}
  ],
  "status": "valid"
}
```

### 5.5 Locomotion Skill Manager

Purpose:

- Expose humanoid locomotion as typed, monitorable skills.

Initial backend:

- Unitree official or community mature G1 controller through MuJoCo.

V0 core skills:

- `stand_ready`
- `track_velocity`
- `turn_to`
- `walk_to`
- `safe_stop`
- `recover_balance`

The controller backend is not the primary V0 novelty. It is a stable execution backend to be wrapped by the runtime.

### 5.6 Status Monitor

Purpose:

- Convert raw robot state, controller feedback, planner state, perception confidence, and safety signals into typed runtime status.

Locomotion status schema:

```json
{
  "skill_id": "walk_to_0001",
  "phase": "executing",
  "progress": 0.42,
  "pose_error": 0.18,
  "velocity_error": 0.07,
  "orientation_error": 0.05,
  "balance_margin": 0.63,
  "contact_state": {
    "left_foot": "stance",
    "right_foot": "swing"
  },
  "slip_score": 0.0,
  "collision_risk": "medium",
  "localization_confidence": 0.81,
  "controller_confidence": 0.76,
  "failure_mode": null,
  "recoverability": "recoverable",
  "recommended_action": "slow_down"
}
```

### 5.7 Body Memory

Purpose:

- Store task-level body execution evidence for recovery and evaluation. It is not merely the previous locomotion observation.

Body memory has three layers:

1. **Instant state**
2. **Windowed summary**
3. **Event / recovery memory**

Body memory schema:

```json
{
  "instant": {
    "base_pose": [0.0, 0.0, 0.0, 0.0],
    "base_velocity": [0.0, 0.0, 0.0],
    "commanded_velocity": [0.0, 0.0, 0.0],
    "contact_state": {
      "left_foot": "stance",
      "right_foot": "swing"
    },
    "joint_limit_margin": 0.42
  },
  "window_summary": {
    "velocity_error_mean_2s": 0.12,
    "velocity_error_max_2s": 0.31,
    "orientation_error_mean_2s": 0.08,
    "balance_margin_min_2s": 0.18,
    "slip_events_5s": 2,
    "collision_risk_max_2s": "medium",
    "controller_confidence_mean_2s": 0.74
  },
  "event_memory": {
    "recent_failure_count": {
      "path_blocked": 1,
      "balance_unstable": 2,
      "localization_lost": 0,
      "target_lost": 0
    },
    "last_recovery_action": "recover_balance",
    "last_recovery_success": true,
    "last_recovery_latency": 1.3,
    "blocked_regions": ["front_left_zone"]
  }
}
```

### 5.8 Recovery Policy

Purpose:

- Select recovery actions from typed failure and body-memory evidence.

V0 recovery policy:

- rule-based first;
- complete action taxonomy from day one;
- learned adaptive recovery policy later.

Recovery action record:

```json
{
  "timestamp": 12.4,
  "trigger": "balance_margin_low",
  "failure_mode": "balance_unstable",
  "action": "recover_balance",
  "implementation_status": "implemented",
  "pre_status": {},
  "post_status": {},
  "success": true,
  "latency": 1.2,
  "fallback_used": null
}
```

### 5.9 Safety Supervisor

Purpose:

- Enforce hard runtime safety boundaries independent of LLM, dashboard, or future agent suggestions.

Rules:

- SafetySupervisor can override planned action.
- It can force `safe_stop` or `emergency_stop`.
- It never depends on Agent Bus or browser UI for critical decisions.
- It logs all overrides as `safety_override` events.

### 5.10 Viser Dashboard

Purpose:

- Provide integrated WebUI for live debugging, benchmark inspection, and demonstration.

Panels:

1. 3D scene panel
2. Camera / grounding panel
3. Runtime state panel
4. Body memory panel
5. Recovery panel
6. Benchmark panel

Allowed UI commands:

- start episode
- pause episode
- resume episode
- reset episode
- choose scenario
- inject dynamic obstacle
- inject localization drift
- trigger user interrupt
- submit language instruction
- export episode data

Forbidden UI commands:

- direct joint command;
- direct low-level velocity command bypassing RuntimeManager;
- direct safety override disable;
- direct controller mutation during episode except through approved typed command.

UI command schema:

```json
{
  "command_id": "ui_cmd_0001",
  "source": "viser_dashboard",
  "type": "submit_instruction",
  "payload": {
    "instruction": "walk to the red chair slowly"
  },
  "requires_safety_approval": true
}
```

---

## 6. Failure Modes and Recovery Actions

### 6.1 Failure Mode Taxonomy v0

| Category | Failure mode |
|---|---|
| Target | `target_not_found` |
| Target | `target_ambiguous` |
| Target | `target_lost` |
| Perception / localization | `low_detection_confidence` |
| Perception / localization | `localization_lost` |
| Perception / localization | `depth_projection_invalid` |
| Path | `path_blocked` |
| Path | `no_feasible_local_plan` |
| Path | `dynamic_obstacle` |
| Motion control | `velocity_tracking_error` |
| Motion control | `orientation_tracking_error` |
| Motion control | `controller_unstable` |
| Body safety | `balance_unstable` |
| Body safety | `slip_detected` |
| Body safety | `collision_risk_high` |
| Task control | `user_interrupt` |

Failure event schema:

```json
{
  "failure_mode": "path_blocked",
  "severity": "medium",
  "recoverability": "recoverable",
  "evidence": {
    "collision_risk": "high",
    "blocked_region": "front_left",
    "local_planner_status": "no_feasible_local_plan"
  },
  "suggested_actions": ["safe_stop", "mark_blocked_region", "local_replan"]
}
```

### 6.2 Recovery Action Taxonomy v0

| Category | Action | V0 status |
|---|---|---|
| Normal control | `continue` | implemented |
| Normal control | `slow_down` | implemented |
| Normal control | `adjust_heading` | reserved |
| Normal control | `adjust_posture` | reserved |
| Stop / protection | `safe_stop` | implemented |
| Stop / protection | `emergency_stop` | implemented |
| Stop / protection | `wait_and_observe` | reserved |
| Balance recovery | `recover_balance` | implemented |
| Balance recovery | `reset_stance` | reserved |
| Balance recovery | `switch_gait` | reserved |
| Localization / target | `relocalize` | implemented |
| Localization / target | `refresh_target_grounding` | implemented |
| Localization / target | `confirm_with_user` | reserved |
| Planning | `local_replan` | implemented |
| Planning | `ask_agent_replan` | implemented |
| Planning | `mark_blocked_region` | implemented |
| Task control | `pause_task` | reserved |
| Task control | `abort_task` | reserved |

Reserved action schema:

```json
{
  "action": "switch_gait",
  "implementation_status": "reserved",
  "fallback": "slow_down"
}
```

---

## 7. Benchmark Design

### V0 Scenario Families

V0 benchmark has five failure-recovery task families.

1. **Dynamic obstacle**
   - A moving or newly inserted obstacle blocks the route.
   - Tests stopping, local replanning, blocked-region marking, and collision avoidance.

2. **Localization drift**
   - Pose estimate receives noise or temporary loss.
   - Tests stop-and-relocalize behavior.

3. **Velocity tracking failure**
   - Controller cannot track commanded speed or turn rate.
   - Tests slowing down and controller instability detection.

4. **Balance risk**
   - External force, terrain perturbation, slip, or stability-margin drop.
   - Tests balance recovery and emergency stop boundaries.

5. **Target change / user interruption**
   - Target disappears, target changes, or user issues stop/change command.
   - Tests refresh grounding, safe stop, and high-level replanning.

Initial size:

- 20 episodes per scenario family.
- 100 total V0 episodes per baseline.

### Metrics

Episode metrics:

- task success rate;
- recovery success rate;
- collision count;
- fall / unstable count;
- stop latency;
- path efficiency;
- repeated failure count;
- human intervention count;
- grounding success rate;
- route validity rate;
- final failure mode.

Per-episode metrics schema:

```json
{
  "episode_id": "ep_0007",
  "scenario": "dynamic_obstacle",
  "task_success": true,
  "recovery_success": true,
  "num_failures": 2,
  "num_recoveries": 2,
  "collision_count": 0,
  "fall_count": 0,
  "stop_latency_mean": 0.31,
  "path_efficiency": 0.82,
  "human_intervention": false,
  "final_failure_mode": null
}
```

### Baselines

V0 baselines:

1. `controller_only`
   - mature G1 controller tracks target velocity or pose; no memory and no recovery.

2. `controller_local_planner`
   - controller plus MPC/optimization local planner; no body memory and no recovery policy.

3. `status_monitor_only`
   - local planner plus status monitor; detects issues but does not execute recovery policy.

4. `full_no_body_memory`
   - recovery policy exists but only sees instant robot state, not window summaries or event memory.

5. `full_body_memory_recovery`
   - full V0 system with body memory and rule-based recovery policy.

Main comparison:

- `full_no_body_memory` vs `full_body_memory_recovery` isolates the value of body memory.
- `status_monitor_only` vs `full_body_memory_recovery` isolates the value of recovery action selection.
- `controller_local_planner` vs `full_body_memory_recovery` isolates the value of failure-aware runtime beyond ordinary local planning.

---

## 8. Episode Data Package

### Principle

Every episode must produce a complete data package from the start. JSONL + metrics alone are not enough because future learning, replay, audit, and debugging require high-frequency timeseries and artifacts.

### Directory Structure

```text
runs/
  run_YYYYMMDD_HHMMSS/
    run_manifest.json
    config_snapshot/
      g1_mujoco.yaml
      recovery_rules.yaml
      benchmark_v0.yaml
      perception.yaml
      logging.yaml

    episodes/
      ep_000001/
        episode_manifest.json
        events.jsonl
        metrics.json

        timeseries/
          robot_state.npz
          body_memory.npz
          controller_command.npz
          contact_state.npz
          planner_state.npz

        artifacts/
          rgb_front.mp4
          depth_front.npz
          detection_debug.mp4
          segmentation_masks.npz
          route_trace.json
          recovery_trace.jsonl
          body_memory_trace.jsonl
          mujoco_state_final.npz
```

### Required Event Types

1. `instruction_received`
2. `command_parsed`
3. `target_detected`
4. `memory_written`
5. `route_planned`
6. `skill_started`
7. `status_update`
8. `failure_detected`
9. `recovery_selected`
10. `recovery_executed`
11. `memory_updated`
12. `skill_completed`
13. `task_completed`
14. `task_failed`
15. `safety_override`

Event schema:

```json
{
  "timestamp": 12.34,
  "episode_id": "ep_0007",
  "task_id": "task_0007",
  "event_type": "failure_detected",
  "source": "status_monitor",
  "correlation_id": "ep_0007_step_012",
  "payload": {
    "failure_mode": "path_blocked",
    "severity": "medium",
    "recoverability": "recoverable",
    "evidence": {
      "collision_risk": "high",
      "local_planner_status": "no_feasible_local_plan"
    }
  }
}
```

### Logging Frequencies

| Data | V0 frequency |
|---|---|
| robot state | 50 Hz |
| controller command | 50 Hz |
| contact state | 50 Hz |
| body memory | 10 Hz |
| planner state | 5-10 Hz or planning event |
| RGB video | 10 Hz |
| depth | 5 Hz |
| detection debug | 5 Hz or detection event |
| segmentation mask | detection event |
| events | event-triggered |
| recovery trace | recovery event |
| route trace | plan/replan event |

### Logging Config

```yaml
logging:
  enabled: true
  save_rgb_video: true
  save_depth: true
  save_detection_debug: true
  save_segmentation_masks: true
  save_mujoco_state: true

  rates:
    robot_state_hz: 50
    controller_command_hz: 50
    body_memory_hz: 10
    planner_state_hz: 10
    rgb_hz: 10
    depth_hz: 5
    detection_debug_hz: 5

  compression:
    video_codec: "mp4v"
    npz_compressed: true

  retention:
    keep_success_artifacts: true
    keep_failure_artifacts: true
```

---

## 9. WebUI Requirements

### Dashboard Type

Use a Viser-based integrated WebUI dashboard.

### Dashboard Purposes

- live debugging;
- benchmark scenario control;
- episode inspection;
- failure/recovery visualization;
- demonstration and video recording;
- future multi-agent audit display.

### Dashboard Panels

1. **3D Scene Panel**
   - G1 robot pose;
   - target point;
   - safe stop pose;
   - obstacles;
   - local route;
   - replan points;
   - blocked regions.

2. **Camera / Grounding Panel**
   - RGB frame;
   - YOLO-World bbox;
   - GroundingDINO/SAM2 fallback result;
   - target confidence;
   - depth projection result.

3. **Runtime State Panel**
   - current skill;
   - phase;
   - progress;
   - failure mode;
   - recoverability;
   - recommended action.

4. **Body Memory Panel**
   - balance margin;
   - velocity error;
   - slip events;
   - contact state;
   - controller confidence;
   - recent failure count.

5. **Recovery Panel**
   - active failure mode;
   - recovery action selected;
   - trigger rule;
   - pre/post status;
   - success/failure;
   - latency.

6. **Benchmark Panel**
   - episode id;
   - scenario;
   - success;
   - collision count;
   - fall count;
   - stop latency;
   - path efficiency.

### Runtime Frequency for Dashboard

| Signal | Dashboard rate |
|---|---|
| robot pose / route | 10-20 Hz |
| body memory summary | 5-10 Hz |
| RGB / detection overlay | 5-10 Hz |
| high-frequency qpos/qvel | not directly rendered; saved to timeseries |
| events / recovery | event-triggered |

### Dashboard Command Boundary

Allowed:

- submit language instruction;
- start/reset/pause/resume episode;
- choose scenario;
- inject dynamic obstacle;
- inject localization drift;
- trigger user interrupt;
- export episode data.

Forbidden:

- direct joint command;
- direct controller command;
- direct velocity command bypassing RuntimeManager;
- disabling SafetySupervisor from dashboard.

---

## 10. Batch Runner and Dashboard Runner

### Batch Runner

Primary path for paper metrics:

```bash
python -m benchmark.runner --config configs/benchmark_v0.yaml
```

Requirements:

- run all selected scenarios;
- run all selected baselines;
- write complete Episode Data Packages;
- aggregate metrics at run level;
- support random seeds and config snapshots.

### Dashboard Debug Mode

Primary path for development and demonstration:

```bash
python -m dashboard.viser_app --episode-config configs/debug_episode.yaml
```

Requirements:

- run one scenario interactively;
- display 3D scene and runtime state;
- allow high-level UI commands;
- write the same Episode Data Package as batch mode.

---

## 11. Multi-Agent Expansion Plan

### V0

Single RuntimeManager with modular backends.

### V1

TaskRouter and AgentPort become real process boundaries.

Possible services:

- PerceptionService
- MemoryService
- NavigatorService
- RecoveryService
- EvaluatorService

### V2

Multi-agent runtime manager for high-level, non-real-time tasks.

Agent roles:

- PlannerAgent
- RecoveryAgent
- ExperimentAuditor
- BenchmarkAnalyst
- FailureCaseReviewer

Agent Bus usage:

- high-level task delegation;
- asynchronous replanning;
- experiment audit;
- failure-case review;
- result handoff;
- multi-agent traceability.

Hard rule:

- Agent Bus is not part of real-time safety or high-frequency control.
- Durable bus delivery is not equivalent to physical execution.
- All agent outputs are recommendations until RuntimeManager and SafetySupervisor approve them.

---

## 12. Technical Specifications

### Suggested Repo Skeleton

```text
humanoid_loco_runtime/
  runtime/
    manager.py
    task_router.py
    event_store.py
    agent_ports.py
    safety_supervisor.py

  language/
    parser.py
    schemas.py

  perception/
    open_vocab_grounder.py
    yolo_world_backend.py
    grounding_sam_backend.py
    depth_projector.py

  memory/
    object_memory.py
    body_memory.py
    interfaces.py

  navigation/
    navigator_base.py
    navigator_v0_local.py
    mpc_local_planner.py
    route_schema.py

  locomotion/
    skill_manager.py
    g1_controller_backend.py
    skill_schema.py

  recovery/
    failure_modes.py
    recovery_actions.py
    rule_policy.py
    recovery_schema.py

  benchmark/
    scenarios/
      dynamic_obstacle.py
      localization_drift.py
      velocity_tracking_failure.py
      balance_risk.py
      user_interrupt.py
    runner.py
    metrics.py
    logger.py

  sim/
    mujoco_env.py
    g1_model_loader.py
    cameras.py
    perturbations.py

  dashboard/
    viser_app.py
    scene_builder.py
    panels.py

  configs/
    g1_mujoco.yaml
    recovery_rules.yaml
    benchmark_v0.yaml
    perception.yaml
    logging.yaml
```

### First Six Schemas to Implement

1. `LocomotionCommand`
2. `LocomotionStatus`
3. `MemoryTarget`
4. `BodyMemoryState`
5. `FailureEvent`
6. `RecoveryActionRecord`

### Integration Points

- MuJoCo simulation environment;
- Unitree G1 model/controller backend;
- YOLO-World or GroundingDINO/SAM2 perception backend;
- Viser dashboard;
- local filesystem run store;
- future ROS2 runtime bus;
- future Agent Bus high-level coordination.

### Security and Safety

- No direct low-level control from dashboard or LLM.
- SafetySupervisor can always override.
- Privileged MuJoCo ground truth is evaluation-only.
- Episode logs should not contain credentials or private company robot details.
- When using company body later, separate public artifact logs from internal hardware-sensitive logs.

---

## 13. Rollout Plan

### Milestone 0: Project Skeleton and Schemas

Deliverables:

- repo skeleton;
- six core schemas;
- config files;
- event logger;
- minimal tests for schema validation.

Exit criteria:

- structured command, status, failure, and recovery records can be serialized/deserialized;
- sample Episode Data Package can be generated without running MuJoCo.

### Milestone 1: MuJoCo + G1 Backend

Deliverables:

- G1 model loading;
- mature controller backend wrapper;
- `stand_ready`, `track_velocity`, `turn_to`, `walk_to`, `safe_stop`;
- robot state and controller command logging.

Exit criteria:

- G1 can execute basic local target approach in MuJoCo;
- logs include robot state, controller command, and metrics.

### Milestone 2: Open-Vocabulary Grounding and Temporary Memory

Deliverables:

- YOLO-World fast path;
- GroundingDINO/SAM2 fallback interface;
- depth projection;
- temporary object memory;
- safe stop pose generation.

Exit criteria:

- runtime grounds a language target from RGB-D without MuJoCo object id;
- evaluation oracle can score grounding accuracy separately.

### Milestone 3: NavigatorV0 and Safety Shield

Deliverables:

- MPC / optimization local planner;
- local obstacle representation;
- route validation;
- local replan;
- safety shield integration.

Exit criteria:

- system can approach target while avoiding local obstacles;
- planner returns typed blocked/no-feasible-plan failures.

### Milestone 4: Body Memory and Rule Recovery

Deliverables:

- instant state;
- windowed summary;
- event/recovery memory;
- 16 failure modes;
- 18 recovery actions;
- 10 implemented core actions.

Exit criteria:

- recovery policy responds to each V0 benchmark failure family;
- recovery traces are written per episode.

### Milestone 5: Benchmark and Baselines

Deliverables:

- five scenario families;
- five baselines;
- batch runner;
- metrics aggregation.

Exit criteria:

- 100 episodes per baseline can run automatically;
- run-level summary compares all baselines.

### Milestone 6: Viser Dashboard

Deliverables:

- integrated WebUI dashboard;
- 3D scene;
- grounding panel;
- body memory panel;
- recovery panel;
- benchmark panel;
- high-level typed UI commands.

Exit criteria:

- dashboard can debug a selected episode live;
- dashboard cannot bypass RuntimeManager or SafetySupervisor.

### Milestone 7: Research Report

Deliverables:

- experiment tables;
- failure case studies;
- ablation analysis;
- limitations and V1 plan.

Exit criteria:

- V0 hypotheses are either supported or explicitly falsified by benchmark evidence.

---

## 14. Risks and Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Mature G1 controller is hard to integrate | blocks whole runtime | start with simplest velocity tracking backend; keep controller wrapper replaceable |
| Open-vocabulary detector is too slow | benchmark becomes impractical | use YOLO-World fast path and fallback only on low confidence |
| Grounding in MuJoCo visuals is brittle | target approach fails for perception reasons | log grounding accuracy separately; use evaluation oracle only for scoring |
| Logging is too heavy | slows benchmark and fills disk | configurable rates, compression, retention policy |
| MPC local planner becomes too complex | delays recovery work | implement minimal optimization planner first; keep API compatible with stronger planner |
| Body memory seems like renamed state | weak novelty | emphasize window summaries, failure events, and recovery outcomes rather than instant state alone |
| Rule recovery looks too simple | reviewer may see it as engineering | position as deterministic safety baseline and data generator for learned recovery |
| Dashboard consumes too much time | delays benchmark | build only Viser panels necessary for debugging and data validation |
| Multi-agent extension distracts V0 | scope creep | keep multi-agent behind AgentPort and TaskRouter interfaces only |
| No real-hardware result | limits venue strength | target workshop/early conference first; plan bxi_elf3/company body as V1/V2 |

---

## 15. Open Questions

These are intentionally left open for implementation-time validation:

1. Which exact G1 MuJoCo model and controller backend will be the first stable baseline?
2. Is YOLO-World sufficient for MuJoCo RGB textures, or is GroundingDINO fallback needed frequently?
3. Which MPC / optimization library should be used for NavigatorV0?
4. What numerical formula should define `balance_margin` for the first G1 implementation?
5. How should `controller_confidence` be estimated if the backend does not expose confidence?
6. What disk budget per 100-episode run is acceptable with all artifacts enabled?
7. Which parts of `bxi_elf3` can be safely described in public artifacts?

---

## 16. Summary of Locked Decisions

- Use MuJoCo + Unitree G1 first.
- Keep `bxi_elf3` and company body as later transfer targets.
- Use mature G1 controller backend first.
- Do not train end-to-end VLA in V0.
- Use language parser to produce structured locomotion commands.
- Use open-vocabulary grounding in V0.
- Use YOLO-World fast path and GroundingDINO/SAM2 fallback.
- Use RGB-D and camera parameters as runtime perception input.
- Use MuJoCo privileged ground truth only for evaluation.
- Use temporary object memory in V0, but expose memory interface compatible with persistent 3D semantic memory.
- Use five memory APIs: `write_observation`, `query_target`, `get_safe_stop_pose`, `update_status`, `expire`.
- Use local target approach and local avoidance in V0; keep global navigation/exploration extension interface.
- Use MPC / optimization-based local planner plus safety shield.
- Use body memory with instant state, windowed summary, and event/recovery memory.
- Use complete recovery action taxonomy from day one.
- Implement 10 core recovery actions in V0 and reserve 8 for later.
- Use 16 failure modes in V0.
- Use single RuntimeManager in V0, not multi-agent real-time execution.
- Keep Agent Bus for high-level async coordination and audit, not real-time safety.
- Use Episode Data Package from the start, including timeseries and artifacts.
- Use Viser integrated WebUI dashboard from the start.
- Support both batch benchmark runner and dashboard debug mode.
- Use five baselines for V0 evaluation.
- Treat the three claims as V0 hypotheses, not final fixed paper claims.


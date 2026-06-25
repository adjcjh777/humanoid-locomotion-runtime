# Language-Conditioned Humanoid Locomotion Runtime with Supervisory RL Recovery

## 0. Project Record

- **Project name**: Humanoid Locomotion Runtime
- **Initial platform**: MuJoCo + Unitree G1 humanoid model
- **Fallback platform**: MuJoCo Playground humanoid locomotion backend if the G1 controller path cannot pass the early smoke gate.
- **Secondary compatibility targets**: `bxi_elf3` / `bxi_robotics` and company-developed humanoid body for later validation, not V0 evidence.
- **Primary goal**: build a practical, research-grade humanoid locomotion runtime that turns language-conditioned and open-vocabulary grounded goals into monitorable, recoverable humanoid locomotion skills, with a high-level learned recovery selector above a self-stabilizing controller.
- **Non-claim**: this project does not train a foundation-scale end-to-end VLA that maps raw image/language directly to humanoid joint actions.
- **Non-claim**: V0 does not claim cross-embodiment generalization; backend-replaceable interfaces are a design constraint, not an experimental result.
- **V0 research stance**: system/runtime paper with one methods core: body-memory-conditioned supervisory RL recovery. Low-level controller innovation is out of scope.

---

## 1. Executive Summary

### Problem Statement

Existing humanoid locomotion controllers can often walk, turn, and track commands in controlled settings, but they are usually exposed as low-level motion backends. They do not naturally provide task-level evidence such as why execution became unsafe, whether a failure is recoverable, which recovery action was tried, or how language-conditioned goals should be re-grounded after perception or navigation failure.

For a language-conditioned humanoid agent, ordinary goal-reaching metrics hide many important failures: the robot may reach a target only because the scenario is easy, while failing under dynamic obstacles, localization drift, velocity tracking error, balance risk, target loss, or user interruption.

### Proposed Solution

Build a language-conditioned humanoid locomotion runtime around a mature Unitree G1 locomotion controller in MuJoCo, with MuJoCo Playground as the fallback humanoid backend. The runtime uses controlled open-vocabulary-style grounding in V0, temporary object memory, an MPC/optimization-based local planner, typed locomotion skills, status monitoring, body memory, a high-level RL recovery selector, deterministic safety fallback, and a Viser-based WebUI dashboard.

The first implementation keeps the core runtime single-manager and keeps the locomotion controller frozen. RL is only used as a low-frequency supervisory recovery selector over typed failure/status/body-memory observations; it never outputs joint commands or replaces the self-stabilizing locomotion controller. Real-time safety remains local to RuntimeManager and SafetySupervisor; Agent Bus is reserved for high-level asynchronous coordination, audit, and experiment analysis.

### Success Criteria

V0 is successful when all of the following are true:

1. **Runtime completion**: the system can execute language-conditioned local locomotion tasks in MuJoCo with Unitree G1 or the fallback humanoid backend through typed commands, controlled grounding, local planning, skill execution, status monitoring, supervisory recovery, and safety fallback.
2. **Benchmark coverage**: the benchmark includes five seeded failure families: dynamic obstacle, localization drift, velocity tracking failure, balance risk, and target change/user interruption.
3. **External baseline and ablations**: V0 reports a controller-native external baseline, a deterministic recovery baseline, and RL ablations over instant state, window memory, and full body memory.
4. **Data completeness**: every episode writes a complete Episode Data Package including manifests, event logs, metrics, timeseries, and artifacts.
5. **Debuggability**: Viser dashboard can inspect live or replayed episodes with 3D scene state, camera/grounding output, runtime status, body memory, recovery decisions, and benchmark metrics.
6. **Safety boundary**: WebUI and future agents can only issue high-level typed commands; they cannot directly bypass RuntimeManager or SafetySupervisor to control low-level humanoid actuators.
7. **RL boundary**: learned recovery is low-frequency and task-level only; the locomotion controller, safety supervisor, and hard stop paths remain non-learned V0 components.

---

## 2. Product / Research Positioning

### Core Positioning

This project is not "a smaller HoloAgent" and not "a new humanoid foundation model." It is a focused humanoid locomotion runtime:

> When a mature humanoid controller already provides self-stabilizing locomotion, how can a runtime learn task-level recovery decisions from body memory while preserving typed safety, logging, replay, and benchmark comparability?

V0 is a single-embodiment evidence project. It uses Unitree G1 first, may fall back to MuJoCo Playground humanoids if G1 integration fails the early gate, and preserves replaceable backend interfaces for later `bxi_elf3` or company-body validation. It does not claim that the learned selector generalizes across humanoid bodies in V0.

Humanoid specificity comes from the coupling between task progress and body dynamics: balance margin, contact state, slip, fall risk, velocity/orientation tracking error, controller confidence, and recovery latency. Unlike wheeled navigation, the runtime must decide when the body can continue, slow down, stop, recover balance, re-ground, re-localize, replan, or abort.

### V0 Research Hypotheses

These are initial working hypotheses, not final locked paper claims.

1. **Supervisory recovery hypothesis**: a high-level RL recovery selector can improve task-level recovery above a self-stabilizing locomotion controller without learning low-level gait or joint control.
2. **Body memory hypothesis**: recovery selectors conditioned on window summaries and event/recovery memory outperform selectors that only observe instant state.
3. **Benchmark hypothesis**: seeded failure-recovery evaluation with external controller-native comparison reveals weaknesses hidden by ordinary goal-reaching metrics.

### Potential V1 / V2 Upgrades

The system should preserve space for stronger claims if later evidence supports them:

- parameterized recovery actions beyond discrete action selection;
- residual or status-conditioned controller adaptation after a stable supervisory layer exists;
- cross-embodiment transfer from Unitree G1 to `bxi_elf3` or company humanoid body;
- persistent full 3D semantic memory replacing temporary object memory;
- global navigation and active exploration;
- multi-agent runtime manager with task router and auditable Agent Bus coordination;
- real open-vocabulary detector stack as the main perception path;
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

As a benchmark runner, I want the system to detect failure modes such as path blockage, localization drift, velocity tracking error, balance risk, target loss, or user interruption so that a high-level recovery selector can choose typed recovery actions and be evaluated against controller-native and deterministic recovery baselines.

Acceptance criteria:

- Failure mode taxonomy supports the 16 V0 failure modes.
- Recovery action taxonomy supports the 18 V0 actions.
- First implementation exposes 8 discrete RL recovery actions: `continue`, `slow_down`, `safe_stop`, `local_replan`, `recover_balance`, `refresh_target_grounding`, `relocalize`, and `abort_task`.
- Rule-based recovery exists as baseline, fallback, and debugging oracle, not as the main claimed method.
- Recovery decisions are recorded with pre-status, post-status, latency, success, and fallback.
- Repeated failures are visible through body memory event records.

#### Story 3: Compare Ablations

As a researcher, I want to run the same benchmark across `controller_native`, `rule_recovery`, `rl_instant_state`, `rl_window_memory`, `rl_full_body_memory`, and an optional `oracle_upper_bound` so that the contribution of supervisory recovery and body memory is measurable.

Acceptance criteria:

- Each method runs through the same scenario definitions, fixed held-out seeds, and logging pipeline.
- Metrics include task success, recovery success, collision count, fall/unstable count, stop latency, path efficiency, repeated failure count, and human intervention count.
- Batch runner produces run-level summary tables.
- Episode-level artifacts are retained for failure diagnosis.
- Reports include per-family breakdowns and confidence intervals, not only aggregate success rates.

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
  -> Supervisory RL recovery selector
  -> Rule/safety fallback
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
  -> SupervisoryRecoverySelector
  -> RuleRecoveryFallback
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
- The learned recovery selector only chooses typed high-level recovery actions. It cannot issue joint commands, direct actuator commands, or direct low-level velocity commands that bypass RuntimeManager.
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

- Main experimental path: controlled detector-like grounding adapter that emits realistic `label`, `bbox`, `mask`, `confidence`, and depth-projected `position_3d` records from scene configuration and offline annotations.
- Adapter failures are first-class benchmark events: low confidence, target ambiguity, target loss, and invalid depth projection.
- Optional demo path: YOLO-World fast path and GroundingDINO + SAM2 fallback.
- V1+ path: real open-vocabulary detectors become the primary runtime perception source.
- Runtime inputs: RGB, depth, camera intrinsics/extrinsics, robot state.
- Forbidden runtime inputs: MuJoCo object id, ground-truth target pose, simulator semantic label.
- Evaluation-only inputs: MuJoCo object id, object pose, contacts, fall state.
- The controlled adapter may be built from privileged simulator metadata offline, but the runtime only receives detector-like outputs and never receives object IDs or ground-truth target poses.

Output schema:

```json
{
  "label": "red chair",
  "bbox": [120, 80, 260, 310],
  "mask_id": "mask_03",
  "confidence": 0.78,
  "source": "controlled_grounding_adapter",
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

### 5.8 Supervisory Recovery Policy

Purpose:

- Select task-level recovery actions from typed failure, locomotion status, and body-memory evidence while leaving low-level gait and stabilization to the frozen locomotion controller.

V0 recovery policy:

- main method: body-memory-conditioned supervisory RL recovery selector;
- action level: low-frequency discrete task-level action selection, not joint control or 50 Hz velocity control;
- controller and local planner are frozen during recovery-selector training;
- rule-based policy remains as deterministic baseline, debugging oracle, and safety fallback;
- bandit sanity check is used before PPO to verify that body-memory observations contain useful recovery signal;
- PPO is the V0 main RL algorithm for multi-step recovery chains if the bandit check passes.

V0 RL action space:

1. `continue`
2. `slow_down`
3. `safe_stop`
4. `local_replan`
5. `recover_balance`
6. `refresh_target_grounding`
7. `relocalize`
8. `abort_task`

Reserved recovery actions remain in the taxonomy for V1+, but they are not part of the V0 RL action space unless explicitly promoted.

Reward priority:

1. Strongly penalize fall, collision, unsafe state, and emergency stop.
2. Reward final task success.
3. Reward successful recovery from detected failure.
4. Penalize recovery latency and path inefficiency.
5. Penalize unnecessary recovery and overly conservative stopping.

Canonical reward shape:

```text
+ task_success
+ recovery_success_bonus
- large_collision_penalty
- large_fall_penalty
- emergency_stop_penalty
- repeated_failure_penalty
- latency_penalty
- path_inefficiency_penalty
- unnecessary_recovery_penalty
```

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
| Stop / protection | `emergency_stop` | safety-only |
| Stop / protection | `wait_and_observe` | reserved |
| Balance recovery | `recover_balance` | implemented |
| Balance recovery | `reset_stance` | reserved |
| Balance recovery | `switch_gait` | reserved |
| Localization / target | `relocalize` | implemented |
| Localization / target | `refresh_target_grounding` | implemented |
| Localization / target | `confirm_with_user` | reserved |
| Planning | `local_replan` | implemented |
| Planning | `ask_agent_replan` | reserved |
| Planning | `mark_blocked_region` | side_effect |
| Task control | `pause_task` | reserved |
| Task control | `abort_task` | implemented |

V0 RL selector action set:

```text
continue
slow_down
safe_stop
local_replan
recover_balance
refresh_target_grounding
relocalize
abort_task
```

`emergency_stop` is a SafetySupervisor override, not an action that RL is allowed to select. `mark_blocked_region` is produced by planner/memory side effects after blockage evidence, not a standalone V0 RL action. `ask_agent_replan` remains reserved until high-level agent coordination is introduced outside the real-time loop.

Reserved action schema:

```json
{
  "action": "switch_gait",
  "implementation_status": "reserved",
  "fallback": "slow_down"
}
```

---

## 7. Benchmark and Evaluation Design

### External Anchors

No existing benchmark exactly covers language-conditioned humanoid locomotion, task-level failure recovery, body-memory-conditioned supervisory RL, and complete runtime logging. V0 therefore uses a seeded internal failure-recovery benchmark, but anchors its design and comparisons to external sources:

1. **MuJoCo Playground**
   - Used as the primary external controller-native reference and fallback humanoid locomotion backend.
   - Rationale: MuJoCo Playground provides open-source MJX robot-learning environments, includes humanoids such as Unitree G1, and demonstrates joystick-style humanoid locomotion and fall recovery examples.
   - Reference: <https://playground.mujoco.org/> and <https://arxiv.org/abs/2502.08844>

2. **LocoMuJoCo**
   - Used as a locomotion robustness and evaluation-protocol reference, not necessarily as a direct runtime dependency in V0.
   - Rationale: LocoMuJoCo is a MuJoCo-based locomotion benchmark for imitation and reinforcement learning with humanoids/bipeds, datasets, dynamics randomization, and task metrics.
   - Reference: <https://loco-mujoco.readthedocs.io/en/v0.3.0/> and <https://arxiv.org/abs/2311.02496>

3. **HumanoidBench**
   - Used for related benchmark positioning and optional sanity-check tasks, not as the V0 main benchmark.
   - Rationale: HumanoidBench is a MuJoCo humanoid benchmark with 27 whole-body tasks, including 12 locomotion tasks, but it does not directly target language-conditioned failure-recovery runtime evaluation.
   - Reference: <https://humanoid-bench.github.io/> and <https://arxiv.org/abs/2403.10506>

### V0 Scenario Families

V0 benchmark has five seeded failure-recovery task families. Each family starts with a minimal controlled version and may add stronger variants after the runtime is stable.

1. **Dynamic obstacle**
   - A single moving or newly inserted obstacle blocks or crosses the route.
   - Randomized variables: obstacle spawn time, crossing angle, speed, size, and distance to robot.
   - Tests stopping, slowing, local replanning, blocked-region side effects, and collision avoidance.

2. **Localization drift**
   - Pose estimate receives bounded noise, confidence drop, or temporary loss.
   - Randomized variables: noise amplitude, drift duration, onset phase, and recovery latency.
   - Tests safe stop, relocalization, and whether continuing is unsafe.

3. **Velocity tracking failure**
   - Controller cannot track commanded speed or turn rate due to delay, saturation, or degraded tracking.
   - Randomized variables: target speed, turn rate, delay, tracking degradation, and duration.
   - Tests slowing down, safe stop, controller-confidence estimation, and recovery latency.

4. **Balance risk**
   - External impulse, terrain perturbation, slip zone, or stability-margin drop creates humanoid-specific risk.
   - Randomized variables: impulse direction, impulse magnitude, contact timing, slip coefficient, and terrain patch.
   - Tests safe stop, recover balance, abort boundaries, and fall/collision avoidance.

5. **Target change / user interruption**
   - Target disappears, target changes, or user issues stop/change command.
   - Randomized variables: interruption time, target ambiguity, new target distance, and grounding confidence.
   - Tests refresh grounding, safe stop, local replan, and abort behavior.

### Seed Protocol

Training and evaluation use different seed pools.

- Training seeds: large randomly generated pool per family, scaled to compute budget.
- Validation seeds: 30 fixed seeds per family for tuning and early stopping.
- Test seeds: 30 held-out fixed seeds per family for final reporting.
- All compared methods run exactly the same validation and test seeds.
- Scenario generator distributions and severity ranges must be committed before final test runs.
- Failed episodes are retained and reported; no hand-picked success-only evaluation.

### Methods and Ablations

V0 distinguishes external baseline, deterministic baseline, RL methods, and ablations.

1. `controller_native`
   - External reference: selected locomotion backend driven through its native command interface.
   - No typed failure-recovery runtime, no body memory, and no learned recovery selector.

2. `rule_recovery`
   - Deterministic pre-registered recovery policy over typed status/failure signals.
   - Serves as baseline, fallback, and debugging oracle.

3. `rl_instant_state`
   - Supervisory RL recovery selector observing only current locomotion status and instant robot state.

4. `rl_window_memory`
   - Supervisory RL recovery selector observing instant state plus short-window summaries.

5. `rl_full_body_memory`
   - Main V0 method: supervisory RL recovery selector observing instant state, window summaries, and event/recovery memory.

6. `oracle_upper_bound` optional
   - Privileged evaluation-only upper bound that may use MuJoCo ground-truth signals.
   - It is not a fair runtime method and must never be compared as a deployable system.

Primary comparisons:

- `controller_native` vs `rl_full_body_memory` estimates the value of controller-to-task recovery runtime.
- `rule_recovery` vs `rl_full_body_memory` estimates the value of learned supervisory selection.
- `rl_instant_state` vs `rl_full_body_memory` estimates the value of body memory.
- `rl_window_memory` vs `rl_full_body_memory` estimates the additional value of event/recovery history.

### RL Training Protocol

V0 uses a staged training path:

1. **Bandit sanity check**
   - Treat a failure event as a one-step recovery-action selection problem.
   - Verify that body-memory observations improve short-horizon recovery outcomes before spending effort on full PPO.

2. **PPO supervisory recovery**
   - Train a low-frequency discrete recovery selector for multi-step recovery chains.
   - The frozen locomotion controller handles balance and gait; PPO only selects typed recovery actions.

If the bandit sanity check shows no body-memory advantage over instant state, the project must pause RL scaling and inspect observation design, action taxonomy, and scenario distributions before running long PPO jobs.

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
      mujoco_playground.yaml
      recovery_rules.yaml
      recovery_rl.yaml
      benchmark_v0.yaml
      seed_protocol.yaml
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
   - humanoid robot pose;
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
- run all selected methods and ablations;
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
    rl_selector.py
    bandit_sanity.py
    reward.py
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
    seed_protocol.py

  sim/
    mujoco_env.py
    g1_model_loader.py
    mujoco_playground_backend.py
    cameras.py
    perturbations.py

  dashboard/
    viser_app.py
    scene_builder.py
    panels.py

  configs/
    g1_mujoco.yaml
    mujoco_playground.yaml
    recovery_rules.yaml
    recovery_rl.yaml
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
- MuJoCo Playground humanoid locomotion backend as fallback and external controller-native reference;
- YOLO-World or GroundingDINO/SAM2 perception backend;
- controlled grounding adapter for V0 benchmark stability;
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
- robot state and controller command logging;
- MuJoCo Playground humanoid backend smoke path.

Exit criteria:

- G1 can execute basic local target approach in MuJoCo;
- logs include robot state, controller command, and metrics.
- if G1 cannot reliably execute `stand_ready`, `track_velocity`, `safe_stop`, and short `walk_to` by the end of week 3, switch the main V0 evidence path to MuJoCo Playground while keeping G1 as target backend.

### Milestone 2: Open-Vocabulary Grounding and Temporary Memory

Deliverables:

- controlled detector-like grounding adapter;
- target ambiguity, target loss, low-confidence, and invalid-depth failure injection;
- optional YOLO-World fast path;
- optional GroundingDINO/SAM2 fallback interface;
- depth projection;
- temporary object memory;
- safe stop pose generation.

Exit criteria:

- runtime receives detector-like target records from RGB-D-style interfaces without MuJoCo object id or ground-truth target pose;
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

### Milestone 4: Body Memory and Supervisory Recovery

Deliverables:

- instant state;
- windowed summary;
- event/recovery memory;
- 16 failure modes;
- 18 recovery actions;
- 8 implemented V0 RL actions;
- rule-based recovery baseline and safety fallback;
- bandit sanity-check trainer;
- PPO supervisory recovery selector.

Exit criteria:

- rule baseline and RL selectors respond to each V0 benchmark failure family;
- bandit sanity check demonstrates whether body-memory observations contain useful recovery signal before long PPO runs;
- recovery traces are written per episode.

### Milestone 5: Seeded Benchmark, External Baseline, and Ablations

Deliverables:

- five scenario families;
- scenario generator distributions and severity ranges;
- train/validation/test seed protocol;
- controller-native external baseline;
- rule recovery baseline;
- RL instant/window/full-body-memory ablations;
- batch runner;
- metrics aggregation.

Exit criteria:

- validation seeds include 30 fixed seeds per family;
- final test seeds include 30 held-out fixed seeds per family;
- all methods run the same held-out seeds;
- reports include confidence intervals and per-family breakdowns.

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
- external benchmark positioning;
- limitations and V1 plan.

Exit criteria:

- V0 hypotheses are either supported or explicitly falsified by benchmark evidence.

---

## 14. Risks and Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Mature G1 controller is hard to integrate | blocks whole runtime | set a week-3 smoke gate and switch V0 evidence to MuJoCo Playground humanoid backend if needed |
| Open-vocabulary detector is too slow or brittle in MuJoCo visuals | benchmark becomes impractical or perception dominates the study | use controlled detector-like grounding adapter for V0 main experiments; keep real detectors as optional demo and V1+ target |
| Controlled grounding looks too artificial | weak language/open-vocabulary claim | expose detector-like outputs, inject grounding failures, keep oracle evaluation separate, and state that real open-vocabulary detectors are V1+ |
| Logging is too heavy | slows benchmark and fills disk | configurable rates, compression, retention policy |
| MPC local planner becomes too complex | delays recovery work | implement minimal optimization planner first; keep API compatible with stronger planner |
| Body memory seems like renamed state | weak novelty | make body memory the observation representation for learned recovery and test instant/window/full-memory ablations |
| PPO training is unstable or expensive | delays core results | run bandit sanity check first, freeze controller/planner, keep action space discrete and low-frequency, and retain rule fallback |
| Rule recovery looks too simple | reviewer may see it as engineering | position rule recovery as deterministic baseline, fallback, and debugging oracle, not the main method |
| Benchmark is seen as self-serving | weak external validity | pre-register seeded scenario distributions, report held-out seeds, compare against controller-native external baseline, and position against MuJoCo Playground, LocoMuJoCo, and HumanoidBench |
| Dashboard consumes too much time | delays benchmark | build only Viser panels necessary for debugging and data validation |
| Multi-agent extension distracts V0 | scope creep | keep multi-agent behind AgentPort and TaskRouter interfaces only |
| No real-hardware result | limits venue strength | target workshop/early conference first; plan bxi_elf3/company body as V1/V2 |

---

## 15. Open Questions

These are intentionally left open for implementation-time validation:

1. Which exact Unitree G1 controller backend can pass the week-3 smoke gate?
2. If G1 integration misses the smoke gate, which MuJoCo Playground humanoid environment becomes the V0 evidence backend?
3. Which MPC / optimization library should be used for NavigatorV0?
4. What numerical formula should define `balance_margin` for the first humanoid implementation?
5. How should `controller_confidence` be estimated if the backend does not expose confidence?
6. Which observation features should be included in `rl_instant_state`, `rl_window_memory`, and `rl_full_body_memory`?
7. How many training seeds are feasible for bandit and PPO under the available compute budget?
8. What disk budget per held-out evaluation run is acceptable with all artifacts enabled?
9. Which parts of `bxi_elf3` can be safely described in public artifacts?

---

## 16. Summary of Locked Decisions

- Use MuJoCo + Unitree G1 first.
- Use MuJoCo Playground humanoid backend as the fallback and external controller-native reference if G1 integration misses the early smoke gate.
- Keep `bxi_elf3` and company body as later compatibility targets, not V0 evidence.
- Use mature G1 controller backend first, but do not let it become a single point of failure.
- Do not train end-to-end VLA in V0.
- Do not train low-level locomotion, gait, joint, or residual controller policies in V0.
- Train only a high-level supervisory recovery selector over a self-stabilizing controller.
- Use language parser to produce structured locomotion commands.
- Use controlled detector-like grounding adapter for V0 main experiments.
- Use YOLO-World fast path and GroundingDINO/SAM2 fallback only as optional V0 demos and V1+ primary perception targets.
- Use RGB-D and camera parameters as runtime perception input.
- Use MuJoCo privileged ground truth only for evaluation.
- Use temporary object memory in V0, but expose memory interface compatible with persistent 3D semantic memory.
- Use five memory APIs: `write_observation`, `query_target`, `get_safe_stop_pose`, `update_status`, `expire`.
- Use local target approach and local avoidance in V0; keep global navigation/exploration extension interface.
- Use MPC / optimization-based local planner plus safety shield.
- Use body memory with instant state, windowed summary, and event/recovery memory.
- Use complete recovery action taxonomy from day one.
- Implement 8 V0 RL recovery actions: `continue`, `slow_down`, `safe_stop`, `local_replan`, `recover_balance`, `refresh_target_grounding`, `relocalize`, and `abort_task`.
- Treat `emergency_stop` as SafetySupervisor-only, not RL-selectable.
- Treat `ask_agent_replan` as reserved until future high-level agent coordination.
- Use 16 failure modes in V0.
- Use single RuntimeManager in V0, not multi-agent real-time execution.
- Keep Agent Bus for high-level async coordination and audit, not real-time safety.
- Use Episode Data Package from the start, including timeseries and artifacts.
- Use Viser integrated WebUI dashboard from the start.
- Support both batch benchmark runner and dashboard debug mode.
- Use seeded five-family failure-recovery benchmark with train/validation/test split.
- Use `controller_native` as the required external baseline.
- Use `rule_recovery`, `rl_instant_state`, `rl_window_memory`, `rl_full_body_memory`, and optional `oracle_upper_bound` for V0 evaluation.
- Run a bandit sanity check before long PPO training.
- Treat supervisory recovery, body memory, and benchmark claims as V0 hypotheses, not final fixed paper claims.

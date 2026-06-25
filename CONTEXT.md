# Humanoid Locomotion Runtime

This context defines the project language for the humanoid locomotion runtime research repo. It captures domain terms only, not implementation decisions or task plans.

## Language

**A800 Single-Host Experiment Path**:
The default research execution path where one A800 server is treated as the canonical host for experiment code, queued runs, logs, and summaries.
_Avoid_: Split-server experiment path, ad-hoc dual-server workflow

**Local Studio Workspace**:
The local macOS working environment used for planning, code review, documentation, and local ARIS research runs.
_Avoid_: Local server, company server

**Company Experiment Server**:
A remote GPU server used for actual experiment execution, including A800 or 5090 machines.
_Avoid_: Local studio, laptop

**Nightly ARIS Run**:
An unattended ARIS-managed run started after the daytime handoff, usually for smoke tests, queued pilots, multi-seed experiments, monitoring, or result summaries.
_Avoid_: Manual run, daytime inspection

**Morning Acceptance Check**:
The human review step after a Nightly ARIS Run that decides whether the produced logs, metrics, and artifacts are valid enough to unlock the next run group.
_Avoid_: Casual log skim, informal check

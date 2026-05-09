---
name: ptq-resolution-engine
description: >-
  Maxine - Qualification engine for Pending Action Candidates. Resolves Project
  / Task Qualifications and converts qualified PACs into a task packet or a
  project-initiation handoff while closing non-work cleanly.
version: 1.0.0
author: FlavorOS
license: MIT
---

# Maxine | PTQ Resolution Engine

You decide when possible work becomes real work and when it should die quietly.

## When to invoke

- A new PAC is logged.
- A PTQ condition is met.
- A waiting PAC needs reevaluation.
- Khadijah asks whether a candidate should now become committed work.

## Protocol

This skill executes `WorkIntake.ptq-resolution-engine.protocol`.

### 1. PTQ Dispatch

- Route the qualification to the right lane: owner confirmation, client reply, budget, time passage, or dependency completion.

### 2. Condition Monitoring

- Track whether the PTQ is still open, waiting, met, failed, or stale.

### 3. Resolution Assessment

- Decide whether the outcome is yes, no, or redirect.

### 4. Conversion Or Closure

- Create a standalone task packet for bounded work.
- Invoke `project-initiation-milestone-mapping` for structured or multi-milestone work.
- Close and archive the PAC when no work should exist.

## SIGMA and Readiness Contract

- PTQ lifecycle state belongs in durable runtime storage first.
- Render human-readable PTQ state into the PAC master list and related readiness notes.
- Create project-state SIGMAs only when the qualified work becomes an active operating object.

## Boundaries

- Do not create external obligations without approval.
- Do not force every qualified PAC into a full project shell.
- Do not leave stale PACs unresolved without surfacing the blocker.

## Inputs

- PAC records
- PTQ records
- service templates
- existing tasks and project context
- vault: `15-Readiness/**`, `30-Projects/**`, `35-Reports/**`

## Outputs

- PAC master list update
- task packet or project-initiation handoff
- closure note when relevant
- `report.maxine.ptq-resolved`

## Related Skills

- `pac-triage-and-logging`
- `project-initiation-milestone-mapping`
- `task-execution-status-monitoring`
- `workflow-approval-control`

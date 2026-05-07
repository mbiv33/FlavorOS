---
id: FOS-OBS-DASHBOARD
title: FlavorOS MVP Dashboard
type: dashboard
status: active
priority: P0
owner_agent: maxine
created: 2026-05-07
updated: 2026-05-07
tags:
  - flavoros
  - dashboard
  - mvp
---

# FlavorOS MVP Dashboard

## Visual Map

Open [[FlavorOS MVP Delivery.canvas]].

## Current Focus

Agents first:

- FOS-MVP-005: temporary VPS dev-agent report paths
- FOS-MVP-006: normalized work orders
- FOS-MVP-007: normalized specialist reports
- FOS-MVP-009: Hermes-aware voice response path
- FOS-MVP-016: operator console IA

## MVP Tasks By Status

Requires Dataview.

```dataview
TASK
FROM "30-Projects/FlavorOS"
WHERE flavoros_id
GROUP BY task_status
SORT priority ASC, due ASC
```

## Agent-Owned Work

Requires Dataview.

```dataview
TASK
FROM "30-Projects/FlavorOS"
WHERE flavoros_id
GROUP BY owner_agent
SORT owner_agent ASC
```

## UI/UX Surface Work

Requires Dataview.

```dataview
TASK
FROM "30-Projects/FlavorOS"
WHERE flavoros_id AND system_area = "ui-ux"
SORT due ASC
```

## External Approval Risk

Requires Dataview.

```dataview
TASK
FROM "30-Projects/FlavorOS"
WHERE flavoros_id AND external_action_risk = true
SORT due ASC
```

## Links

- [[FlavorOS MVP Kanban]]
- [[FlavorOS MVP Tasks]]
- [[Obsidian Setup]]


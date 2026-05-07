---
flavoros_id: FOS-DASH-001
type: dashboard
status: active
workstream: Delivery Control Plane
owner_agent: maxine
created: 2026-05-07
tags:
  - flavoros
  - dashboard
  - mvp
---

# FlavorOS MVP Dashboard

Use this note inside Obsidian. It is compatible with Dataview-style project tracking and can coexist with TaskNotes, Kanban, Cards View, Meta Bind, and Bases.

## Current Priority

Agents first. Get the dev-agent crew and product-agent work-order loop running so background work can continue while the full system map is refined.

## Views

### MVP Tasks By Status

```dataview
TASK
FROM "planning/00-flavoros-mvp-delivery-system"
WHERE flavoros_id
GROUP BY task_status
SORT priority ASC, due ASC
```

### Blocked Work

```dataview
TASK
FROM "planning/00-flavoros-mvp-delivery-system"
WHERE flavoros_id AND task_status = "blocked"
SORT due ASC
```

### Agent-Owned Work

```dataview
TASK
FROM "planning/00-flavoros-mvp-delivery-system"
WHERE flavoros_id
GROUP BY owner_agent
SORT owner_agent ASC
```

### UI/UX Surface Work

```dataview
TASK
FROM "planning/00-flavoros-mvp-delivery-system"
WHERE flavoros_id AND system_area = "ui-ux"
SORT due ASC
```

## Bases/TaskNotes Properties

Recommended fields:

- `flavoros_id`
- `type`
- `task_status`
- `priority`
- `workstream`
- `owner_agent`
- `phase`
- `system_area`
- `due`
- `dependency_ids`
- `clickup_status`
- `external_action_risk`

## Manual Sync Rule

Until automated sync exists:

1. Update `task_map.yaml` first.
2. Update ClickUp from `clickup_import.csv` or manual mapping.
3. Update this dashboard and Kanban board only as projections.
4. Do not let ClickUp become the hidden source of truth.

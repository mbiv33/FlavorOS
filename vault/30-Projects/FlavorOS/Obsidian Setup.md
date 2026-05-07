---
id: FOS-OBS-SETUP
title: Obsidian Setup
type: setup
status: active
owner_agent: scooter
created: 2026-05-07
updated: 2026-05-07
tags:
  - flavoros
  - obsidian
  - setup
---

# Obsidian Setup

## Works Immediately

[[FlavorOS MVP Delivery.canvas]] should open as a visual map using Obsidian Canvas, which is a core Obsidian feature.

If it opens as raw JSON, enable the core Canvas plugin:

```text
Settings -> Core plugins -> Canvas
```

## Plugin-Enhanced Views

Run this repo script from macOS to install the community plugins into this vault and open the Canvas:

```bash
scripts/open-flavoros-obsidian.command
```

The installer writes plugins into:

```text
vault/.obsidian/plugins/
```

It also enables installed plugins through:

```text
vault/.obsidian/community-plugins.json
```

If Obsidian still shows Restricted Mode, open Settings -> Community plugins and allow community plugins for this vault.

These community plugins power the richer project views:

| View | Plugin | Purpose |
|---|---|---|
| [[FlavorOS MVP Dashboard]] | Dataview | Query tasks by status, owner, workstream, and risk |
| [[FlavorOS MVP Kanban]] | Kanban | Render the Markdown board as a drag-and-drop board |
| [[FlavorOS MVP Tasks]] | Dataview or TaskNotes | Query task metadata and build task views |

Recommended plugin stack:

- Dataview
- Kanban
- TaskNotes
- Meta Bind
- Cards View
- Mind Map
- Heatmap Calendar
- Tasks Calendar Wrapper
- Templater
- Tasks

## Important

Open the `vault/` folder as the Obsidian vault if you want these notes to appear exactly as linked.

The canonical task source is still:

```text
planning/00-flavoros-mvp-delivery-system/task_map.yaml
```

These Obsidian files are a visual projection for working the plan.

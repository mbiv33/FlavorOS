# Project Management, ClickUp, and Obsidian Expertise

Generated for FlavorOS on 2026-05-07.

This file is the project-delivery companion to `PROVIDER_EXPERTISE.md`. Use it when planning, executing, visualizing, or delegating FlavorOS work. It exists because FlavorOS must be managed as a deployable product, not as a stream of isolated prompts.

## Source Map

Primary sources and reference repositories reviewed:

- ClickUp API task creation: https://developer.clickup.com/reference/createtask
- ClickUp task custom fields: https://developer.clickup.com/reference/setcustomfieldvalue
- ClickUp hierarchy: https://help.clickup.com/hc/en-us/articles/13856392825367-Intro-to-the-Hierarchy
- ClickUp spreadsheet import guidance: https://help.clickup.com/hc/en-us/articles/6310834724247-Use-the-Spreadsheets-Importer
- ClickUp spreadsheet field support: https://help.clickup.com/hc/en-us/articles/6310876671255-Fields-supported-by-the-Spreadsheets-importer
- Obsidian properties: https://help.obsidian.md/properties
- Obsidian Bases: https://help.obsidian.md/bases
- Obsidian Dataview: https://github.com/blacksmithgu/obsidian-dataview
- Obsidian Kanban: https://github.com/mgmeyers/obsidian-kanban
- TaskNotes: https://github.com/callumalpass/tasknotes
- Obsidian Meta Bind: https://github.com/mProjectsCode/obsidian-meta-bind-plugin
- Obsidian Cards View: https://github.com/jillro/obsidian-cards-view-plugin
- Obsidian Mind Map: https://github.com/lynchjames/obsidian-mind-map
- Heatmap Calendar: https://github.com/Richardsl/heatmap-calendar-obsidian
- Obsidian Tasks Calendar Wrapper: https://github.com/Leonezz/obsidian-tasks-calendar-wrapper
- Obsidian Canvas Presentation: https://github.com/Quorafind/Obsidian-Canvas-Presentation
- Obsidian Startpage: https://github.com/kuzzh/obsidian-startpage
- Obsidian Metatable: https://github.com/arnau/obsidian-metatable
- Vega: https://github.com/iCarlosVega/Vega
- DeepResearchAgent: https://github.com/SkyworkAI/DeepResearchAgent
- Agent-MCP: https://github.com/rinadelph/Agent-MCP

## Working Conclusions

### Canonical Source

FlavorOS should keep the canonical delivery plan in git, with Markdown for humans and YAML for agents. ClickUp and Obsidian should be projections of that source, not competing sources of truth.

Canonical files:

- `planning/00-flavoros-mvp-delivery-system/FLAVOROS_MVP_PROJECT_PLAN.md`
- `planning/00-flavoros-mvp-delivery-system/task_map.yaml`
- `planning/00-flavoros-mvp-delivery-system/clickup_import.csv`
- `planning/00-flavoros-mvp-delivery-system/OBSIDIAN_DASHBOARD.md`
- `planning/00-flavoros-mvp-delivery-system/OBSIDIAN_KANBAN.md`

### Industry Delivery Rules

- Keep one product goal visible before choosing tasks.
- Define work as outcomes, not activity.
- Use a delivery hierarchy: initiative -> phase -> epic -> task -> acceptance criteria.
- Every task needs an owner, dependency state, acceptance criteria, and a verification method.
- Track UI/UX as a product surface, not a polish phase.
- Make agents useful early with bounded, report-producing work.
- Use tests to protect shipping risk, not as the center of the project.
- Keep approval gates explicit for money, external sends, bookings, public statements, and client commitments.
- Prefer weekly or shorter milestones during the MVP recovery period.

### ClickUp Mapping

Recommended ClickUp hierarchy:

- Space: `FlavorOS`
- Folder: `MVP Delivery`
- Lists:
  - `00 Control Plane`
  - `01 Agent Runtime`
  - `02 Voice Demo`
  - `03 Email Calendar`
  - `04 UI UX`
  - `05 Deployment`
  - `06 Beta and Beyond`

Recommended ClickUp statuses:

- `backlog`
- `ready`
- `in progress`
- `blocked`
- `review`
- `done`

Recommended custom fields:

- `FlavorOS ID`
- `Workstream`
- `Owner Agent`
- `System Area`
- `MVP Phase`
- `Dependency IDs`
- `Obsidian Note`
- `Acceptance Criteria`
- `Verification`
- `External Action Risk`

### Obsidian Mapping

Recommended Obsidian stack for FlavorOS:

- Dataview: dashboards over frontmatter and task metadata.
- Kanban: sprint and workflow board.
- TaskNotes: one note per high-value task when work becomes active.
- Meta Bind: dashboard controls and status update affordances.
- Cards View: CRM, client, SIGMA, and readiness review surfaces.
- Mind Map: system map and workstream decomposition.
- Heatmap Calendar: shipping streaks and agent heartbeat visibility.
- Tasks Calendar Wrapper: due-date and agenda view.

Obsidian note properties should stay plain and queryable:

```yaml
flavoros_id: FOS-MVP-001
type: task
status: ready
priority: P0
workstream: Agent Runtime
owner_agent: Scooter
phase: MVP Recovery
system_area: agent-runtime
due: 2026-05-08
clickup_status: ready
```

### Agent-Orchestration Pattern Extraction

Useful from Vega:

- Principal Engineer style orchestrator.
- Central state machine.
- Scoped agents.
- Explicit human approval gates.
- Agent handoffs as artifacts.
- QA rollback as targeted rework, not endless testing.
- Dashboard visibility for agent status.

Useful from DeepResearchAgent:

- Act, observe, optimize, remember loop.
- Versioned resources.
- Separate prompts, tools, environments, memory, traces, and config.
- Persistent workdir and trace artifacts.

Useful from Agent-MCP:

- Persistent project context.
- Task dependencies.
- Agent status dashboard.
- Admin-only root task creation.
- Agents should be created with assigned work, not vague availability.
- Shared memory and structured task tools are helpful, but should not replace the existing NATS/vault architecture during MVP.

## FlavorOS Adaptation

FlavorOS should not adopt any external framework wholesale before MVP. The immediate adaptation is:

- Khadijah is the product orchestrator.
- Maxine owns project management and task state.
- Scooter owns provider research, endpoint testing, and technical readiness.
- Sinclair owns the live voice and email/calendar UX paths.
- Kyle joins when CRM, follow-up, or relationship intelligence is needed.
- Temporary VPS dev agents handle logwatch, provider research, and endpoint testing as described in `docs/dev_context/VPS_DEV_AGENTS_RETASKING.md`.
- The canonical task state remains in git until ClickUp sync is intentionally added.

## Planning Quality Gate

Before any implementation session:

1. Read the latest project plan and task map.
2. Name the current product objective.
3. Identify the workstream being advanced.
4. Confirm whether UI/UX, deployment, agent runtime, and data/artifact impacts are affected.
5. Decide whether the task belongs to local Codex, a product agent, or a VPS dev agent.
6. Do only the smallest useful verification that proves the task moved toward shipping.

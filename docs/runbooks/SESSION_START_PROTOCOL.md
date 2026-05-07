# Session Start Protocol

## Purpose

Spin up project context at the beginning of a Codex, Claude Code, or agent development session. This is the lightweight startup companion to `/itc` and the opening counterpart to `/ctl`.

The goal is to get the worker oriented in under five minutes without re-reading the entire repository.

## Manual Trigger

```text
/ctx
```

`/ctx` means "load current context": read the latest handoff docs, inspect current workspace status, and report the active module, blockers, and next actions.

## IDE Interaction Markers

These markers are part of Dee's IDE operating context:

- `/pn`: "please note." Treat as durable operational context for the current IDE/project workflow when it affects future behavior.
- `/qq`: "quick question." Answer without losing the active train of thought or session direction.
- `/qr`: "quick response." Answer subsequent questions with a focused response, defaulting to fewer than 30 words, leading with yes/no when applicable, and without extra context.
- `/qrN`: quick response with an explicit word limit, where `N` is the number immediately after `/qr`.

When the user uses `/qq`, record the question and answer summary in `planning/QQ_AUDIT_LOG.md` during the next permitted file-edit pass.

## When To Run

Run `/ctx`:

- at the beginning of a fresh chat/session,
- after restarting the computer,
- before starting a new module,
- when switching between Codex and Claude Code,
- when the worker is unsure whether current memory matches repo state.

## Required Reads

Read these first:

- `docs/dev/LATEST_CONTEXT_SNAPSHOT.md`
- `docs/dev/NEXT_ACTIONS.md`
- `docs/dev/DECISIONS.md`
- `docs/dev/SESSION_LOG.md`
- `docs/pm/MODULE_BACKLOG.md`

If the session needs Product IT Director mode, also read:

- `docs/runbooks/IT_DIRECTOR_COMMAND_PROTOCOL.md`
- `docs/dev_context/PROVIDER_EXPERTISE.md`
- `docs/dev_context/PROJECT_MANAGEMENT_CLICKUP_OBSIDIAN_EXPERTISE.md`
- `docs/dev_context/AGENT_OPS_INTEGRATION.md`
- `docs/dev_context/VPS_DEV_AGENTS_RETASKING.md`
- `FLAVOROS_CONTEXT.md`

If the task touches MVP delivery, planning, agent assignment, ClickUp, Obsidian, UI/UX, or deployment sequencing, also read:

- `planning/00-flavoros-mvp-delivery-system/FLAVOROS_MVP_PROJECT_PLAN.md`
- `planning/00-flavoros-mvp-delivery-system/task_map.yaml`
- `planning/00-flavoros-mvp-delivery-system/AGENT_WORKSTREAMS.md`

Then inspect current status:

```bash
git status --short
```

If the task touches deployment or services, also run:

```bash
docker compose config --services
```

If the task touches config, validate relevant YAML before editing when practical.

## Response Shape

When `/ctx` is requested, respond with:

```text
Context loaded:
- Active canon:
- Current module:
- Current branch/status:
- Known blockers:
- Next 3 actions:
- Do-not-touch notes:
```

## Rules

- Do not regenerate `LATEST_CONTEXT_SNAPSHOT.md` during `/ctx` unless the user asks or the snapshot is obviously stale.
- Do not run VPS commands during `/ctx` unless explicitly requested.
- Do not print secret values.
- Do not start implementation until the context report is complete.
- If repo state conflicts with the latest snapshot, say so clearly and trust the repo over the snapshot.

## Relationship To Commands

- `/ctx` opens context at session start.
- `/itc` opens the same context in Product IT Director mode and builds the current project task list.
- `/ctl` closes the loop at session end or handoff.

# IT Director Command Protocol

## Purpose

Activate FlavorOS Product IT Director mode at the beginning of a working session.

`/itc` is the command that brings the session to life as an execution console: it resumes from the last stopping point, loads the active canon, and produces a project task list with completed work and next todos.

## Manual Trigger

```text
/itc
```

`/itc` means:

- load the latest project control context
- determine where the last session stopped
- identify the active module and blockers
- generate the current completed-task list
- generate the current next-todo list
- surface any canon drift that should be corrected before implementation

## Required Reads

Read these first:

- `docs/dev/LATEST_CONTEXT_SNAPSHOT.md`
- `docs/dev/NEXT_ACTIONS.md`
- `docs/dev/DECISIONS.md`
- `docs/dev/SESSION_LOG.md`
- `docs/pm/MODULE_BACKLOG.md`
- `docs/prd/FLAVOROS_12_HOUR_MVP.md`
- `docs/runbooks/SESSION_START_PROTOCOL.md`
- `docs/runbooks/SESSION_SUMMARY_PROTOCOL.md`
- `docs/dev_context/PROVIDER_EXPERTISE.md`
- `docs/dev_context/AGENT_OPS_INTEGRATION.md`
- `docs/dev_context/VPS_DEV_AGENTS_RETASKING.md`
- `FLAVOROS_CONTEXT.md`

Then inspect current state:

```bash
git status --short
```

If the session touches deployment or live services, also run:

```bash
docker compose config --services
```

## Director Output

When `/itc` is requested, respond with:

```text
IT Director activated:
- Last session ended at:
- Active canon:
- Current module:
- Current branch/status:
- Completed since last major checkpoint:
- Next todo list:
- Known blockers:
- Directive drift to fix now:
```

## Task List Rules

- The completed list should only include meaningful shipped steps, not noise.
- The next todo list should be ruthless and MVP-first.
- Separate "already proven" from "still only scaffolded or tested."
- If the docs over-index on testing, compress them into ship-critical tasks.
- If active docs disagree, trust the repo and flag the inconsistency immediately.

## Scope Boundary

- `/itc` does not itself regenerate `docs/dev/LATEST_CONTEXT_SNAPSHOT.md`.
- `/itc` does not perform VPS commands unless the user asks or the current task requires them.
- `/itc` does not print secret values.
- `/itc` is a startup command, not a close-loop command.

## Relationship To Commands

- `/ctx` is the lighter startup context check.
- `/itc` is the Product IT Director startup mode.
- `/ctl` is the close-loop handoff command.

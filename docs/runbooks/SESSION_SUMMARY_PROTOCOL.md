# Session Summary Protocol

## Purpose

Make every Codex, Claude Code, and agent development session resumable. The goal is that the next worker can read the current context in under five minutes and continue without rebuilding the mental model.

Counterpart protocol:

- Use `/ctx` at session start to spin up context.
- Use `/ctl` at session end to close the loop.

## When To Run

Run this protocol at the end of every meaningful development session, and any time one agent hands work to another.

Manual trigger:

```text
/ctl
```

`/ctl` means "close the loop": update the handoff docs, regenerate the latest context snapshot, and report the next three actions.

Automatic habit:

- If a live LLM/user development session has been active for more than 2.5 hours since the last close-loop run, run this protocol before continuing into another module.
- If a worker cannot verify the last close-loop time, run the protocol before major deployment, secrets, or architecture work.

## Required Updates

Update these files:

- `docs/dev/SESSION_LOG.md`
- `docs/dev/NEXT_ACTIONS.md`
- `docs/dev/DECISIONS.md`
- `docs/pm/MODULE_BACKLOG.md`

Update these when relevant:

- `docs/dev/VPS_INVENTORY.md`
- `docs/runbooks/STACK_API_PROTOCOL.md`
- `docs/prd/FLAVOROS_12_HOUR_MVP.md`
- `docs/architecture/SIGMA_READINESS_CONTRACT.md`
- module-specific docs under `docs/build/`, `docs/runbooks/`, or `docs/architecture/`

## Summary Shape

Every session summary should include:

```text
Date/time:
Worker/tool:
Goal:
Files changed:
Decisions made:
What now works:
What remains broken or unknown:
Secrets touched: yes/no, names only
VPS touched: yes/no
Tests/checks run:
Next 3 actions:
Risks:
```

## Rules

- Do not include secret values.
- Do not include raw OAuth tokens, API keys, passwords, SSH private keys, or unredacted provider tokens.
- Do not include full VPS logs unless they have been reviewed for secrets.
- Prefer concrete file paths and checkboxes over vague narration.
- If a task fails because of permissions or missing access, record the exact blocker and the next required human action.

## Handoff Standard

The next worker should know:

- current architecture canon,
- active module,
- exact next command or file edit,
- where the prior worker stopped,
- what must not be changed yet.

## Suggested Closing Command

Run the local snapshot script:

```bash
scripts/session-snapshot.sh > docs/dev/LATEST_CONTEXT_SNAPSHOT.md
```

Review the output before committing.

## Close-Loop Response

When `/ctl` is requested, the worker should finish with:

```text
Closed loop:
- Snapshot updated: yes/no
- Docs updated: yes/no
- Tests/checks run:
- Next 3 actions:
- Blockers:
```

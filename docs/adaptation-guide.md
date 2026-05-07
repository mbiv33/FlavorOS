# Adaptation Guide

How to customize the Chief of Staff OS for your workflow.

---

## Start with the Context File

`FLAVOROS_CONTEXT.md` now holds system-level FlavorOS rules, not personal profile data. Before tweaking skills, make sure:
- `FLAVOROS_CONTEXT.md` reflects the operating model and authority boundaries
- client-specific account mappings and preferences live in client envelopes, workspace files, or vault artifacts
- approval rules are clear in the active client workflow

Most product-level customization happens in `FLAVOROS_CONTEXT.md`. Most client-level customization should happen outside it.

## Adjusting Authority Levels

The default authority framework is conservative — the assistant drafts most replies for your review. To expand what it handles autonomously:

1. Open `FLAVOROS_CONTEXT.md` for system-level authority defaults
2. Open the active client envelope or workflow artifact for client-specific overrides
3. Move items from "Draft for review" to "Act autonomously"
4. Be specific: "Reply to scheduling confirmations" is better than "handle routine emails"

Start conservative. Expand as you build trust.

## Changing the Follow-up Cadence

The default cadence is 2 → 5 → 7 days. To change it:

1. Update the active client envelope, relationship workflow, or vault note with the preferred cadence
2. The relationship-manager workflow should read that client-specific source on every run

For different cadences per contact type, add notes in the Business Context section.

## Modifying the Daily Rhythm

### Change sweep frequency
Edit the cron schedule. For less frequent sweeps:
```bash
hermes cron add "0 9,12,15,18 * * 1-5" "Run executive-assistant in heartbeat mode..."
```

### Change task prep time
If you're a night owl and 2 AM prep is too early:
```bash
hermes cron add "0 5 * * *" "Run daily-task-prep..."
```

### Skip the morning briefing
Simply don't set up the morning briefing cron job. The other skills work independently.

## Adding Task Sections

The task file format is flexible. To add custom sections:

1. Open `workspace/tasks/current.md`
2. Add a new `##` section wherever it makes sense
3. Update the "Rules" section to explain the new section
4. If the section should be checked by daily-task-prep, note that in the skill's procedure

## Adding New Email Accounts

1. Add the account to the active client envelope or connector inventory
2. Add the corresponding calendar alias to the approved workflow/tool config
3. Configure the MCP server for the new account in `~/.hermes/config.yaml`

## Integrating External Tools

The CoS skills are tool-agnostic — they describe what to do, not which specific tool to use. To add integrations:

1. Set up the MCP server in `~/.hermes/config.yaml`
2. Record the tool in the relevant client or workspace ops doc
3. Add notes in `workspace/TOOLS.md` about any quirks

## Building Custom Skills

The five included skills cover the core operating model. To add your own:

1. Create a new directory under `skills/` with a `SKILL.md`
2. Use the same YAML frontmatter pattern (name, description, version, author, license)
3. Reference `FLAVOROS_CONTEXT.md` for system rules and the client envelope for client-specific configuration
4. Add a cron schedule if it should run automatically

Examples of skills you might add:
- **meeting-prep**: Generate briefing docs before important meetings
- **weekly-digest**: Produce a weekly summary of activity
- **content-calendar**: Track publishing schedules
- **business-development**: Pipeline tracking with Google Sheets

## Removing Skills You Don't Need

Each skill is independent. To run a lighter setup:

- **Minimal (EA only)**: Keep just `executive-assistant` and `daily-task-manager`
- **Standard (3 pillars)**: Add `relationship-manager` and `daily-task-prep`
- **Full CoS**: Add `chief-of-staff` orchestrator

Remove the cron jobs for skills you're not using.

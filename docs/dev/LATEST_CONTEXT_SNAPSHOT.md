
## FlavorOS Context Snapshot

- Generated at: 2026-05-07T18:05:31Z
- Working directory: /Users/marcusbivines/Library/CloudStorage/Dropbox/My Mac (Marcuss-MacBook-Pro.local)/Documents/FlavorOS

## Git

### status short

```text
 D .DS_Store
 M .env.example
 M .gitignore
 M ARCHITECTURE.md
 D CHIEF_OF_STAFF_CONTEXT.md
 M DEPLOYMENT.md
 M INSTALL.md
 M PHILOSOPHY.md
 M README.md
 M SKILLS_INVENTORY.md
 D agents/.DS_Store
 M agents/khadijah/agent.yaml
 M agents/khadijah/skills/chief-of-staff/SKILL.md
 M agents/kyle/agent.yaml
 M agents/kyle/skills/relationship-manager/SKILL.md
 M agents/kyle/skills/relationship-manager/references/follow-up-cadence.md
 M agents/maxine/agent.yaml
 M agents/maxine/skills/daily-task-prep/SKILL.md
 M agents/scooter/agent.yaml
 M agents/sinclair/agent.yaml
 M agents/sinclair/skills/executive-assistant/references/authority-framework.md
 M agents/sinclair/skills/executive-assistant/references/calendar-rules.md
 M agents/sinclair/skills/executive-assistant/references/email-templates.md
 M cron/schedules.yaml
 M docker-compose.yml
 M docs/adaptation-guide.md
 M docs/maturity-levels.md
 M docs/operating-model.md
 M docs/recommended-founder-setup.md
 D infra/.DS_Store
 M infra/obsidian.yaml
 M infra/secrets/.sops.yaml
 M infra/secrets/secrets.example.yaml
 M skills/.DS_Store
 M skills/brand-social/SKILL.md
 M skills/chief-of-staff/SKILL.md
 M skills/daily-task-manager/SKILL.md
 M skills/daily-task-prep/SKILL.md
 M skills/executive-assistant/SKILL.md
 M skills/executive-assistant/references/authority-framework.md
 M skills/executive-assistant/references/calendar-rules.md
 M skills/executive-assistant/references/email-templates.md
 M skills/infrastructure-ops/SKILL.md
 M skills/relationship-manager/SKILL.md
 M skills/relationship-manager/references/follow-up-cadence.md
 M skills/travel-logistics/SKILL.md
 M skills/wellness/SKILL.md
 D vault/.DS_Store
 D workspace/.DS_Store
 M workspace/HEARTBEAT.md
 M workspace/relationships/current.md
?? .claude/
?? CLAUDE_DESIGN_PROMPT.md
?? DESIGN_BRIEF.md
?? FLAVOROS_CONTEXT.md
?? agents/khadijah/skills/project-management-control/
?? agents/kyle/personas/
?? agents/maxine/personas/
?? agents/maxine/skills/clickup-obsidian-project-management/
?? agents/scooter/personas/
?? agents/sinclair/personas/
?? clients/
?? docs/.obsidian/
?? docs/architecture/
?? docs/archive/
?? docs/build/
?? docs/dev/
?? docs/dev_context/
?? docs/pm/
?? docs/prd/
?? docs/runbooks/
?? infra/secrets/secrets.enc.yaml
?? infra/voice-gateway/
?? planning/
?? relationship-file-format.md
?? scripts/
?? skills/project-management-control/
?? vault/.obsidian/
?? vault/05-SIGMA/
?? vault/15-Readiness/
?? vault/30-Projects/FlavorOS/
?? vault/TaskNotes/
```

### branch

```text
main
```


## Compose

### compose services

```text
redis
postgres
secrets-loader
openrouter-proxy
nats
khadijah
kyle
maxine
scheduler
scooter
sinclair
vault-sync
voice-gateway
```


## Active Agents

### agent configs

```text
agents/khadijah/agent.yaml
agents/kyle/agent.yaml
agents/maxine/agent.yaml
agents/sinclair/agent.yaml
agents/scooter/agent.yaml
```

### persona packs

```text
agents/kyle/personas/regine/PERSONA.md
agents/maxine/personas/overton-ops/PERSONA.md
agents/sinclair/personas/watson/PERSONA.md
agents/scooter/personas/overton-tech/PERSONA.md
```


## Project Control Docs

### dev docs

```text
docs/dev/VPS_INVENTORY.md
docs/dev/SESSION_LOG.md
docs/dev/LATEST_CONTEXT_SNAPSHOT.md
docs/dev/NEXT_ACTIONS.md
docs/dev/DECISIONS.md
docs/pm/MODULE_BACKLOG.md
docs/prd/FLAVOROS_12_HOUR_MVP.md
docs/runbooks/VPS_INVENTORY_RUNBOOK.md
docs/runbooks/SESSION_START_PROTOCOL.md
docs/runbooks/IT_DIRECTOR_COMMAND_PROTOCOL.md
docs/runbooks/SESSION_SUMMARY_PROTOCOL.md
docs/runbooks/STACK_API_PROTOCOL.md
docs/runbooks/RELATIONSHIP_DISCOVERY_ONBOARDING.md
docs/architecture/SIGMA_READINESS_CONTRACT.md
docs/architecture/PERSONA_PACKS.md
docs/architecture/CLIENT_ENVELOPE.md
```


## Important Reminders

- Five active agents only: khadijah, sinclair, maxine, scooter, kyle.
- Retired identities are persona/capability packs, not deployable agents.
- SIGMAs are created intelligence artifacts, not triggers.
- Do not rotate secrets until the full stack API protocol.
- Do not print secret values in summaries, logs, or chat.

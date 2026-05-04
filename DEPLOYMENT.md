# FlavorOS Deployment

## Agent Footprint

Active staff:

- `khadijah` (Hermes)
- `sinclair` (Hermes)
- `maxine` (OpenClaw)
- `scooter` (OpenClaw)
- `kyle` (OpenClaw)

## Bring Up

```bash
docker compose up -d nats redis postgres openrouter-proxy secrets-loader scheduler vault-sync
docker compose up -d khadijah maxine sinclair scooter kyle
```

## What Changed

- retired containers `regine`, `watson`, and `overton` were removed
- active agents now mount local skill bundles from `agents/<name>/skills`
- each agent mounts its own `SOUL.md`
- Khadijah and Sinclair now each have their own voice/interface lane
- Obsidian access is role-scoped in `infra/obsidian.yaml`

## Obsidian

CRM, PM, reports, travel notes, wellness notes, and ops logs are all expected to live in the shared vault.

Each active agent now has:

- a role-specific Obsidian skill
- Obsidian plugin metadata in `agent.yaml`
- explicit folder scope in `infra/obsidian.yaml`

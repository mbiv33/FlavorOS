# Stack API and Secrets Protocol

## Purpose

Load and rotate all required provider credentials in one controlled ceremony. Avoid piecemeal updates that leave containers, docs, encrypted blobs, and provider dashboards out of sync.

## Never Do

- Never paste secret values into chat.
- Never commit plaintext secrets.
- Never print secret values in scripts or logs.
- Never rotate only one key unless responding to an urgent compromise.

## Protocol Phases

### Phase 1: Provider Inventory

List required providers and whether they are needed for demo, MVP, or later.

Initial provider classes:

- OpenRouter
- Hermes
- OpenClaw
- ElevenLabs
- Twilio
- Google Gmail
- Google Calendar
- Google Drive
- Composio or direct OAuth broker
- Obsidian vault Git remote
- Cloudflare DNS
- Hostinger VPS

### Phase 2: Schema Update

Update templates with names only:

- `.env.example` for public/non-secret config.
- `infra/secrets/secrets.example.yaml` for secret names and shape.
- `docs/runbooks/STACK_API_PROTOCOL.md` if provider classes change.

### Phase 3: Local Plaintext Fill

Create or update local plaintext only in gitignored files:

```text
.env
infra/secrets/secrets.yaml
infra/secrets/secrets.local.yaml
```

### Phase 4: Validation Without Values

Run validators that print:

- key present/missing
- expected file path present/missing
- provider health yes/no
- token scopes names where safe

Validators must not print values.

### Phase 5: Encrypt

Use SOPS/age to encrypt:

```bash
bash scripts/encrypt-secrets.sh
```

Notes:

- The helper refuses to run if `infra/secrets/.sops.yaml` still has the placeholder age public key.
- By default it creates `infra/secrets/secrets.enc.yaml` and keeps the local plaintext file.
- To remove the plaintext after verification:

```bash
REMOVE_PLAINTEXT=1 bash scripts/encrypt-secrets.sh
```

### Phase 6: Commit Safe Files

Commit only:

- encrypted secrets blob if intended for repo deploy,
- templates,
- docs,
- code changes.

Do not commit plaintext `.env` or `secrets.yaml`.

If a file named `secrets.enc.yaml` is discovered without SOPS metadata, treat it as plaintext/misnamed and quarantine it as `infra/secrets/secrets.local.yaml` until the protocol creates a real encrypted blob.

### Phase 7: Deploy

On VPS:

```bash
git pull
docker compose restart secrets-loader
docker compose ps
```

### Phase 8: Verify Distribution

Check only presence and health:

```bash
docker compose exec secrets-loader find /run/flavor/secrets -type f -maxdepth 3 -print
docker compose logs --tail=50 secrets-loader
```

Expected: file paths and success messages only, no values.

## Approval Boundary

All external sends, bookings, money movement, legal/contract actions, and sensitive relationship moves remain approval-gated until explicitly changed in client HITL policy.

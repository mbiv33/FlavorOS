# VPS Dev Agents Retasking

Generated for the FlavorOS 12-hour MVP on 2026-05-07.

This runbook defines how to temporarily repurpose the three idling VPS agents for launch acceleration, then reset them before official Marcus/Christy onboarding.

Scope:

- Use temporary dev-agent work only.
- Do not contaminate the canonical five-agent product identity.
- Do not print, request, or log raw secrets.
- Do not write dev scratch into client onboarding canon.
- Do not let temporary dev agents take external actions.

## Retasking Objective

Use three idling VPS agents as a temporary development crew:

| Temp agent | Mission | Output |
| --- | --- | --- |
| Agent 1 | CI/CD log monitoring and syntax checking | `docs/dev_context/runtime/agent1-logwatch.md` and NATS/audit notes |
| Agent 2 | Continuous provider/API documentation research | `docs/dev_context/runtime/agent2-provider-research.md` |
| Agent 3 | Automated testing client for Hermes voice/text endpoints | `docs/dev_context/runtime/agent3-endpoint-tests.md` |

These are temporary operator roles, not product agents.

## Boundaries

Allowed:

- Read logs that do not contain secrets.
- Run syntax checks.
- Run no-value health checks.
- Research official docs.
- Ping local/internal endpoints.
- Publish test work orders to NATS with fake data.
- Write reports into `docs/dev_context/runtime/`.

Blocked:

- Reading or printing plaintext secret files.
- Sending email, SMS, calendar invites, or public posts.
- Booking travel or spending money.
- Modifying production client vault files.
- Editing provider dashboards.
- Rotating credentials outside `STACK_API_PROTOCOL.md`.
- Running destructive cleanup without explicit operator approval.

## Directory Layout

Create these scratch paths on the VPS:

```bash
cd /home/deploy/apps/flavoros
mkdir -p docs/dev_context/runtime
mkdir -p runtime/dev-agents/agent1-logwatch
mkdir -p runtime/dev-agents/agent2-provider-research
mkdir -p runtime/dev-agents/agent3-endpoint-tests
```

Do not place scratch data under:

```text
vault/05-SIGMA/
vault/15-Readiness/
clients/
infra/secrets/
```

unless the work is intentionally promoted by Khadijah or the human operator.

## Agent 1: CI/CD Logwatch And Syntax Check

Mission:

- Keep the launch path honest.
- Watch compose state and logs.
- Run syntax/config checks after each code change.
- Report blockers quickly and without leaking values.

Standing prompt:

```text
You are FlavorOS Dev Agent 1: Logwatch and Syntax.

Mission:
- Monitor Docker Compose service state, voice-gateway logs, scheduler logs, NATS connectivity, and syntax/config checks.
- Report only service names, statuses, error classes, file paths, and line numbers.
- Never print secret values, tokens, raw env files, or decrypted secret content.
- Do not edit files unless explicitly instructed by the Product IT Director.

Every report must include:
- Timestamp
- Commands run
- Pass/fail status
- Failing service or file path
- Short recommended fix
```

Safe checks:

```bash
cd /home/deploy/apps/flavoros
docker compose config >/tmp/flavoros-compose-check.yml
docker compose ps
python -m py_compile infra/voice-gateway/app/main.py infra/voice-gateway/app/elevenlabs_tts.py infra/voice-gateway/app/openai_stt.py infra/voice-gateway/app/policy.py
bash scripts/validate-secrets-readiness.sh
```

Safe log monitor:

```bash
cd /home/deploy/apps/flavoros
docker compose logs --tail=80 voice-gateway scheduler openrouter-proxy secrets-loader
```

NATS smoke check:

```bash
cd /home/deploy/apps/flavoros
docker compose exec nats nats --server nats://localhost:4222 server check connection
```

If the `nats` CLI is unavailable in the container, skip the command and report `nats_cli_missing`; do not install packages during launch unless assigned.

Report path:

```text
docs/dev_context/runtime/agent1-logwatch.md
```

Report template:

```markdown
# Agent 1 Logwatch

## Latest Status

- Time:
- Compose config:
- Compose ps:
- Python syntax:
- Secrets readiness:
- NATS check:

## Findings

## Recommended Fixes
```

## Agent 2: Provider Documentation Research

Mission:

- Keep provider implementation docs current.
- Research only official/provider-primary docs unless explicitly told otherwise.
- Produce implementation-ready notes, not broad essays.

Standing prompt:

```text
You are FlavorOS Dev Agent 2: Provider Research.

Mission:
- Track missing implementation details for OpenRouter, Hermes, OpenClaw, ElevenLabs, Twilio, Google Gmail/Calendar/Drive, NATS, Redis, Postgres, and Obsidian Git sync.
- Prefer official docs and primary repositories.
- Summarize exact endpoint shapes, auth requirements, rate limits, retry behavior, webhook formats, and code-impact notes.
- Never ask for or expose secrets.

Every report must include:
- Provider
- Question answered
- Source links
- Implementation note
- Risk or rate-limit note
- Recommended code location in this repo
```

Research queue:

```text
1. Twilio barge-in: clear/mark handling and interruption behavior.
2. ElevenLabs lowest-latency TTS path for Twilio ulaw 8000.
3. OpenRouter retry behavior, model fallback, and request metadata.
4. Google Gmail minimal scopes for read + draft + label without send.
5. Google Calendar proposal/hold strategy without external notifications.
6. Obsidian Git or raw Git sync conflict strategy for vault artifacts.
```

Report path:

```text
docs/dev_context/runtime/agent2-provider-research.md
```

Report template:

```markdown
# Agent 2 Provider Research

## Latest Research

### Provider

- Question:
- Official source:
- API shape:
- Rate-limit/retry note:
- FlavorOS code impact:
- Launch recommendation:
```

## Agent 3: Endpoint Testing Client

Mission:

- Act as a synthetic test client for local/internal Hermes and voice/text endpoints.
- Validate health, TwiML shape, WebSocket path, and NATS report loop with fake data.
- Never use real client data.

Standing prompt:

```text
You are FlavorOS Dev Agent 3: Endpoint Test Client.

Mission:
- Ping health endpoints.
- Verify Twilio webhook returns TwiML with the expected WSS stream URL.
- Send synthetic work orders to NATS only with fake data.
- Confirm reports return on expected subjects.
- Test Hermes/OpenRouter text path through internal endpoints when available.
- Never use real phone numbers, real emails, real calendar data, or real secrets.

Every report must include:
- Endpoint or subject tested
- Fake input used
- Expected result
- Actual result
- Pass/fail
- Next fix
```

Safe endpoint checks:

```bash
cd /home/deploy/apps/flavoros
curl -fsS https://voice.flavoros.bairyos.com/health
curl -fsS -X POST https://voice.flavoros.bairyos.com/voice | sed -n '1,20p'
```

Expected `/voice` signals:

```text
<Response>
  <Connect>
    <Stream url="wss://voice.flavoros.bairyos.com/twilio-stream" />
  </Connect>
</Response>
```

Synthetic NATS work order:

```bash
cd /home/deploy/apps/flavoros
docker compose exec nats nats --server nats://localhost:4222 pub work_order.scooter '{
  "id":"wo_dev_endpoint_test_001",
  "agent":"scooter",
  "skill":"web-research",
  "args":{
    "task_type":"synthetic_test",
    "user_request":"Confirm this fake work order can move through NATS.",
    "deliverable":"One short fake report.",
    "vault_path":"docs/dev_context/runtime/",
    "requires_approval":false
  },
  "fired_at":"2026-05-07T16:00:00Z"
}'
```

Report subscription:

```bash
cd /home/deploy/apps/flavoros
docker compose exec nats nats --server nats://localhost:4222 sub 'report.*' --count 1
```

If the `nats` CLI is unavailable, use service logs:

```bash
cd /home/deploy/apps/flavoros
docker compose logs --tail=120 scooter khadijah sinclair
```

Report path:

```text
docs/dev_context/runtime/agent3-endpoint-tests.md
```

Report template:

```markdown
# Agent 3 Endpoint Tests

## Latest Run

- Time:
- Voice health:
- Voice TwiML:
- NATS work order:
- Report observed:

## Failures

## Next Fix
```

## Retasking Methods

Use whichever method matches the currently idling VPS agents.

### Hermes Agent Method

If the idle agent is a Hermes instance:

1. Put the standing prompt into that agent's temporary session message.
2. If persistent behavior is needed, place task-specific instructions in a temporary `AGENTS.md` inside `runtime/dev-agents/<agent>/`.
3. Keep `SOUL.md` untouched unless the agent is dedicated to dev only.
4. Use explicit allowlists for any messaging channel.
5. Disable external send tools.

Suggested launch command shape:

```bash
cd /home/deploy/apps/flavoros/runtime/dev-agents/agent1-logwatch
hermes -c
```

### OpenClaw Agent Method

If the idle agent is an OpenClaw instance:

1. Use a temporary workspace under `runtime/dev-agents/<agent>/`.
2. Seed:
   - `AGENTS.md`
   - `SOUL.md`
   - `TOOLS.md`
   - `IDENTITY.md`
   - `USER.md`
3. Set the agent workspace to that temp path.
4. Keep queue mode conservative; avoid steering while tests mutate state.
5. Keep sessions isolated from official agents.

Suggested workspace files:

```text
runtime/dev-agents/agent1-logwatch/AGENTS.md
runtime/dev-agents/agent1-logwatch/SOUL.md
runtime/dev-agents/agent1-logwatch/TOOLS.md
runtime/dev-agents/agent1-logwatch/IDENTITY.md
runtime/dev-agents/agent1-logwatch/USER.md
```

Do not reuse:

```text
agents/khadijah/
agents/sinclair/
agents/maxine/
agents/scooter/
agents/kyle/
vault/
clients/
```

as temp dev-agent workspaces.

## Promotion Rules

A dev-agent finding can be promoted into product canon only if:

- It directly supports the 12-hour MVP.
- It contains no secret values.
- It has source links or reproducible command output.
- It maps to a repo file path or launch checklist item.
- Khadijah or the Product IT Director accepts it.

Promotion targets:

- Provider knowledge -> `docs/dev_context/PROVIDER_EXPERTISE.md`
- Agent routing knowledge -> `docs/dev_context/AGENT_OPS_INTEGRATION.md`
- Launch status -> `docs/dev/NEXT_ACTIONS.md`
- Durable demo output -> `vault/05-SIGMA/` or `vault/15-Readiness/`

## Reset Before Marcus/Christy Onboarding

Goal:

- Remove temporary dev-agent state.
- Preserve useful docs.
- Start onboarding with clean client memory and no testing residue.

Reset checklist:

```text
[ ] Stop temporary dev-agent sessions.
[ ] Archive useful runtime reports into docs/archive/dev-agent-reports/.
[ ] Delete or quarantine runtime/dev-agents scratch workspaces.
[ ] Remove temporary NATS subjects/subscriptions if any were added.
[ ] Clear Redis dev/test keys only.
[ ] Keep production call/work-order audit records.
[ ] Remove fake vault artifacts from client-facing folders.
[ ] Re-run no-secret grep for provider keys and tokens.
[ ] Run /ctl to regenerate the latest context snapshot.
```

Operator-approved cleanup commands:

```bash
cd /home/deploy/apps/flavoros
mkdir -p docs/archive/dev-agent-reports
cp -a docs/dev_context/runtime/. docs/archive/dev-agent-reports/ 2>/dev/null || true
```

Destructive cleanup requires explicit operator approval before execution:

```bash
cd /home/deploy/apps/flavoros
rm -rf runtime/dev-agents
rm -rf docs/dev_context/runtime
```

Redis cleanup must target only dev keys:

```bash
cd /home/deploy/apps/flavoros
docker compose exec redis redis-cli --scan --pattern 'dev:*'
```

After reviewing matched keys, delete only approved dev/test keys. Do not use broad `FLUSHALL`.

## Launch Reporting Cadence

During active MVP build:

- Agent 1 reports after every deploy or code edit.
- Agent 2 reports whenever provider research closes an implementation question.
- Agent 3 reports after each endpoint change.
- Product IT Director consolidates findings into `docs/dev/NEXT_ACTIONS.md` or the active implementation plan.

Report format:

```text
Status:
- Agent:
- Mission:
- Result:
- Blocker:
- Next action:
```

## Stop Conditions

Immediately stop or pause a dev agent if:

- It attempts to print secrets.
- It tries to send external messages.
- It writes into client onboarding canon without approval.
- It runs destructive commands.
- It floods provider APIs or NATS subjects.
- It produces reports without sources or reproducible checks.

Escalate to Khadijah/Product IT Director with:

```text
flag.high
reason=<short reason>
agent=<temp agent>
last_safe_action=<command or report>
```

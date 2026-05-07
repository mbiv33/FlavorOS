# Provider Expertise

Generated for the FlavorOS 12-hour MVP on 2026-05-07.

This file is the launch-stage provider playbook. It captures the API shapes, runtime integration patterns, and rate-limit behavior needed to build FlavorOS without re-researching the same surface every session.

Hard rules:

- Never print, paste, or commit raw provider secrets.
- Follow `docs/runbooks/STACK_API_PROTOCOL.md` for all credential changes.
- Use providers only to ship the MVP: live voice, context-aware responses, durable SIGMA/readiness artifacts, and one email/calendar demo flow.
- External sends, bookings, money movement, legal/contract actions, public posts, and sensitive relationship moves stay approval-gated.

## Source Map

Primary sources used:

- OpenRouter chat completions: https://openrouter.ai/docs/api-reference/chat-completion
- OpenRouter rate limits and key status: https://openrouter.ai/docs/api/reference/limits
- Hermes context and skills guidance: https://hermes-agent.nousresearch.com/docs/guides/tips/
- Hermes configuration layout: https://hermes-agent.nousresearch.com/docs/user-guide/configuration/
- OpenClaw agent runtime: https://docs.openclaw.ai/concepts/agent
- OpenClaw runtime layers: https://docs.openclaw.ai/concepts/agent-runtimes
- Twilio Media Streams overview and messages: https://www.twilio.com/docs/voice/media-streams and https://www.twilio.com/docs/voice/media-streams/websocket-messages
- ElevenLabs streaming TTS: https://elevenlabs.io/docs/api-reference/text-to-speech/stream
- ElevenLabs latency guidance: https://elevenlabs.io/docs/developer-guides/specifying-server-location
- Gmail push notifications: https://developers.google.com/workspace/gmail/api/guides/push
- Gmail usage limits: https://developers.google.com/workspace/gmail/api/reference/quota
- Gmail message resource: https://developers.google.com/workspace/gmail/api/reference/rest/v1/users.messages
- Google Calendar event insert: https://developers.google.com/workspace/calendar/api/v3/reference/events/insert
- Google Calendar push notifications: https://developers.google.com/workspace/calendar/api/guides/push
- Google Calendar quota guidance: https://developers.google.com/workspace/calendar/api/guides/quota
- Google Drive change watches: https://developers.google.com/workspace/drive/api/reference/rest/v3/changes/watch
- Google Drive usage limits: https://developers.google.com/workspace/drive/api/guides/limits
- Google OAuth web-server flow: https://developers.google.com/identity/protocols/oauth2/web-server
- Gmail scopes: https://developers.google.com/workspace/gmail/api/auth/scopes
- Calendar scopes: https://developers.google.com/workspace/calendar/api/auth
- NATS request-reply: https://docs.nats.io/nats-concepts/core-nats/reqreply
- NATS queue groups: https://docs.nats.io/nats-concepts/core-nats/queue
- NATS JetStream: https://docs.nats.io/nats-concepts/jetstream
- Obsidian Git plugin: https://github.com/Vinzent03/obsidian-git
- Obsidian sync guidance: https://obsidian.md/help/sync-notes

## Runtime Topology

FlavorOS runs as a containerized hub-and-spoke system:

- Voice edge: `voice-gateway`
- LLM router: `openrouter-proxy`
- Human-facing agents: `khadijah`, `sinclair`
- Dark specialists: `maxine`, `scooter`, `kyle`
- Bus: `nats`
- Hot state and rate control: `redis`
- Durable state and audit: `postgres`
- Vault files: bind-mounted `vault/`
- Vault sync: `vault-sync`, currently parked until Git remote/deploy key are configured
- Secret distribution: `secrets-loader` writes file-based secrets under `/run/flavor/secrets`

Provider calls must enter through a small number of internal adapters:

- OpenRouter: call only through `openrouter-proxy`.
- Twilio: terminate at `voice-gateway` `/voice` and `/twilio-stream`.
- ElevenLabs: call only from voice rendering adapters with secret files.
- Google: call through OAuth broker or Composio-equivalent account grants; never give every agent every scope.
- Obsidian Git: sync vault files as durable artifacts, not as chat memory.

## OpenRouter

Purpose:

- Unified model router for Hermes and OpenClaw reasoning.
- Current repo adapter is `infra/openrouter-proxy/proxy.py`.

Current local implementation:

- Internal endpoint: `http://openrouter-proxy:8080/v1/chat/completions`
- Upstream endpoint: `https://openrouter.ai/api/v1/chat/completions`
- Secret file: `/run/flavor/secrets/_shared/openrouter.key`
- Routing config: `infra/openrouter.yaml`
- Request headers set by proxy:
  - `Authorization: Bearer <secret>`
  - `HTTP-Referer: https://flavoros.local`
  - `X-Title: FlavorOS/<agent>`
  - `Content-Type: application/json`
- Agent selector headers:
  - `X-Agent-Name`
  - `X-Agent-Profile`

API shape:

```http
POST https://openrouter.ai/api/v1/chat/completions
Authorization: Bearer <OPENROUTER_API_KEY>
Content-Type: application/json
HTTP-Referer: https://flavoros.local
X-Title: FlavorOS/sinclair

{
  "model": "anthropic/claude-sonnet-4.6",
  "messages": [
    {"role": "system", "content": "..."},
    {"role": "user", "content": "..."}
  ],
  "max_tokens": 4096,
  "temperature": 0.4,
  "stream": false,
  "metadata": {
    "work_order_id": "wo_...",
    "agent": "sinclair"
  }
}
```

Response shape to normalize:

```json
{
  "id": "chatcmpl-...",
  "object": "chat.completion",
  "model": "provider/model",
  "choices": [
    {
      "index": 0,
      "finish_reason": "stop",
      "message": {
        "role": "assistant",
        "content": "..."
      }
    }
  ],
  "usage": {
    "prompt_tokens": 0,
    "completion_tokens": 0,
    "total_tokens": 0
  }
}
```

MVP pattern:

- Human-facing live voice should use fast, short responses.
- Deep synthesis and high-stakes drafts use `thinking`.
- Do not let the voice loop generate long multi-step analysis live. If the answer needs work, create a readiness artifact and publish a work order.
- Use `session_id`, `metadata`, or trace fields once added to the proxy so cost and errors can be tied to `call_sid`, `work_order_id`, and `agent`.

Rate limit and failure strategy:

- OpenRouter key status can be checked with `GET https://openrouter.ai/api/v1/key`.
- Free model variants have specific request caps; avoid `:free` models for the live demo path.
- Treat 402 as credit/billing failure, 429 as rate limiting, 5xx as provider instability.
- Redis limiter key pattern:
  - `rl:openrouter:<agent>:<model>`
  - `rl:openrouter:global`
- Retry only idempotent generations.
- For live voice, use one retry max with short timeout; if it fails, speak a graceful deferral and create the artifact.
- For background specialists, use exponential backoff with jitter and durable status in Postgres.

NATS integration:

- Front agent publishes `work_order.<agent>`.
- Specialist calls OpenRouter through proxy and publishes `report.<agent>`.
- Audit fanout should capture model id, status code, token usage, latency, and artifact path, never prompt text that contains secrets.

## Hermes

Purpose:

- Human-facing runtime class for Khadijah and Sinclair.
- Used for natural interaction, approvals, voice identity, and synthesis.

Relevant upstream runtime knowledge:

- Hermes uses durable context files such as `SOUL.md` for identity and `AGENTS.md` for project instructions.
- Skills are reusable workflows; memory is for facts, skills are for procedures.
- Hermes configuration and secrets normally live under `~/.hermes/`, including `config.yaml`, `.env`, `SOUL.md`, memories, skills, cron, sessions, and logs.

FlavorOS repo contract:

- Khadijah and Sinclair are configured with `runtime: hermes-agent`.
- The local lightweight runtime loads:
  - `/etc/flavoros/SOUL.md`
  - `/etc/flavoros/FLAVOROS_CONTEXT.md`
  - `/skills/*/SKILL.md`
  - vault/HITL rules from `agent.yaml`
- Runtime subscribes to configured NATS subjects and sends completions through `openrouter-proxy`.

MVP integration pattern:

- Khadijah owns executive framing, approvals, decisions, and briefings.
- Sinclair owns inbox, calendar, meeting prep, wellness, notes, and most impromptu voice.
- Hermes agents may speak to the user. OpenClaw specialists do not.
- Voice gateway should call a Hermes-facing policy/router, not hardcode canned answers.
- Every meaningful Hermes outcome should either:
  - answer from prepared context,
  - ask one clarifying question,
  - or defer into a work order plus readiness artifact.

Session and memory strategy:

- Use Redis for short-lived live-call state:
  - `call:<call_sid>:active_agent`
  - `call:<call_sid>:last_transcript`
  - `call:<call_sid>:open_work_orders`
- Use Postgres for durable call events and audit.
- Use vault files for user-facing artifacts and context snapshots.
- Keep Hermes memory small and curated; do not dump raw Gmail/Calendar payloads into identity memory.

Risk controls:

- Hermes may draft external messages but must not send without approval.
- Do not enable unrestricted messaging bot access.
- Do not give Hermes raw broad OAuth credentials; provide scoped broker actions or per-agent grants.

## OpenClaw

Purpose:

- Dark specialist runtime class for Maxine, Scooter, and Kyle.
- Used for execution work, research, logistics, operations, CRM, and structured follow-up.

Relevant upstream runtime knowledge:

- OpenClaw runs an embedded agent runtime with a workspace as cwd.
- It injects bootstrap/context files such as `AGENTS.md`, `SOUL.md`, `TOOLS.md`, `IDENTITY.md`, and `USER.md`.
- Skills are loaded from workspace, project, personal, managed, bundled, and extra directories.
- Sessions are stored under `~/.openclaw/agents/<agentId>/sessions/<SessionId>.jsonl`.
- OpenClaw has runtime, provider, model, and channel as separate layers.

FlavorOS repo contract:

- Maxine, Scooter, and Kyle are configured with `runtime: openclaw`.
- In the current lightweight container, the same Python base runtime processes work orders for all agents.
- OpenClaw specialists receive only `work_order.<agent>` and publish `report.<agent>`.
- They never speak directly to the user.

MVP integration pattern:

- Use OpenClaw for background work that can survive live-call latency.
- Inputs must be structured work orders, not vague chat transcripts.
- Outputs must be structured reports plus vault file paths.
- Every specialist report should contain:
  - `work_order_id`
  - `agent`
  - `status`
  - `summary`
  - `vault_file`
  - `user_facing_response`
  - `requires_approval`

State strategy:

- Redis: in-progress locks and de-dupe keys.
- Postgres: `work_orders`, `agent_reports`, `provider_events`, `artifact_index`.
- Vault: final human-readable artifacts.
- NATS: command and event transport.

Guardrails:

- Maxine escalates money movement, invoice disputes, contract terms, and subscriptions.
- Scooter escalates bookings and external commitments.
- Kyle escalates public statements, partnership terms, contract terms, and sensitive relationship moves.

## ElevenLabs

Purpose:

- Spoken voice rendering for Khadijah and Sinclair.
- Current repo adapter is `infra/voice-gateway/app/elevenlabs_tts.py`.

Current implementation:

- API base: `https://api.elevenlabs.io/v1`
- Endpoint: `/text-to-speech/{voice_id}/stream`
- Secret files:
  - `ELEVENLABS_API_KEY_FILE`
  - `ELEVENLABS_VOICE_ID_FILE`
- Default model: `eleven_flash_v2_5`
- Current output format: `ulaw_8000`, which fits Twilio media playback.

API shape:

```http
POST https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream?output_format=ulaw_8000
xi-api-key: <ELEVENLABS_API_KEY>
Content-Type: application/json

{
  "text": "Sinclair here. I have that.",
  "model_id": "eleven_flash_v2_5",
  "voice_settings": {
    "stability": 0.45,
    "similarity_boost": 0.85,
    "style": 0.25,
    "use_speaker_boost": true
  }
}
```

Latency strategy:

- Use Flash for live phone interactions.
- Use streaming endpoint when response text is ready up front.
- Consider WebSocket TTS later when streaming LLM text directly into audio.
- Keep live utterances short. Generate one spoken response, then defer background work.
- Log request id, model, voice alias, character count, latency, and status. Do not log generated text if it contains private material.

Twilio compatibility:

- Prefer `ulaw_8000` output when available.
- Send audio frames over Twilio media messages as base64 payloads.
- Send a Twilio `mark` after media so playback completion can be tracked.
- Use Twilio `clear` to interrupt buffered audio on DTMF or future barge-in.

Rate and quota strategy:

- Track character usage by agent and call.
- Redis limiter keys:
  - `rl:elevenlabs:sinclair`
  - `rl:elevenlabs:khadijah`
  - `rl:elevenlabs:global`
- On 429, stop retrying live audio and send a short fallback tone or text-path update if available.
- For non-live briefings, queue TTS rendering as background work.

## Twilio

Purpose:

- Phone transport and bidirectional media stream for live voice.
- Current repo adapter is `infra/voice-gateway/app/main.py`.

Current implementation:

- `GET /health`: public health check.
- `POST /voice`: returns TwiML with `<Connect><Stream>`.
- `WebSocket /twilio-stream`: receives and sends Twilio Media Stream events.
- Stream URL comes from `TWILIO_STREAM_URL`.

TwiML shape:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Connect>
    <Stream url="wss://voice.flavoros.bairyos.com/twilio-stream" />
  </Connect>
</Response>
```

Inbound WebSocket events to handle:

- `connected`: protocol open.
- `start`: stream metadata, including `streamSid`, `callSid`, media format, and custom parameters.
- `media`: base64 G.711 mu-law audio payload.
- `dtmf`: inbound touch-tone input for bidirectional streams.
- `mark`: Twilio acknowledgement for completed or cleared playback.
- `stop`: call or stream ended.

Outbound WebSocket events to send:

```json
{
  "event": "media",
  "streamSid": "MZ...",
  "media": {
    "payload": "<base64-ulaw-8000-no-container-header>"
  }
}
```

```json
{
  "event": "mark",
  "streamSid": "MZ...",
  "mark": {
    "name": "sinclair-policy-response"
  }
}
```

```json
{
  "event": "clear",
  "streamSid": "MZ..."
}
```

MVP voice policy:

- Accept call.
- Capture short utterance.
- Transcribe.
- Route to Sinclair by default, Khadijah for briefing mode.
- If answer is present in prepared context, answer.
- If not, create readiness artifact and publish a work order.
- Speak one short acknowledgement.

Security and reliability:

- Twilio requires HTTPS/WSS for production webhooks.
- Validate `X-Twilio-Signature` before real users.
- Allow WebSocket traffic from Twilio over 443.
- For bidirectional streams, Twilio supports one stream per call.
- Use `clear` for interruption and `mark` to track buffered audio.
- Do not log full phone numbers in broad logs; log `from_present=true` or a hashed/last-4 value.

Rate and failure strategy:

- Protect `/voice` with signature validation and optional allowlist during demo.
- Bound call duration and max utterances per call.
- Redis keys:
  - `call:<call_sid>:started_at`
  - `call:<call_sid>:utterance_count`
  - `call:<call_sid>:last_mark`
- Postgres audit:
  - call started/stopped
  - transcript chars
  - provider status
  - artifact paths

## Google APIs

Purpose:

- Prove FlavorOS is an operating system by processing one email/calendar flow.
- MVP should support multiple accounts by design but only needs a safe test flow.

Credential strategy:

- Prefer an OAuth broker abstraction so agents request actions by account alias, not raw tokens.
- Use least-privilege scopes and incremental authorization.
- Use offline access for server-side background work, storing refresh tokens only through the secrets protocol.
- Never mount all Google credentials into all agents.

Recommended account alias pattern:

```yaml
email_biz_a:
  provider: google_gmail
  client: marcus_test
  access: read_draft_label

cal_biz_a:
  provider: google_calendar
  client: marcus_test
  access: read_propose

drive_biz_a:
  provider: google_drive
  client: marcus_test
  access: artifact_read_write
```

### Gmail

API shapes:

```http
GET https://gmail.googleapis.com/gmail/v1/users/me/messages?q=newer_than:7d
Authorization: Bearer <access_token>
```

```http
GET https://gmail.googleapis.com/gmail/v1/users/me/messages/{id}?format=metadata&metadataHeaders=From&metadataHeaders=To&metadataHeaders=Subject&metadataHeaders=Date
Authorization: Bearer <access_token>
```

```http
POST https://gmail.googleapis.com/gmail/v1/users/me/drafts
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "message": {
    "raw": "<base64url-rfc2822-message>"
  }
}
```

Push notification pattern:

- Gmail uses Cloud Pub/Sub for mailbox push notifications.
- `watch` returns a `historyId` and expiration.
- Call `watch` at least every 7 days; daily renewal is recommended.
- Notifications indicate that something changed; process actual deltas with `users.history.list`.

MVP strategy:

- For the 12-hour demo, polling one test inbox is acceptable if push setup is too slow.
- Store `last_history_id` per account alias in Postgres.
- Read metadata first, fetch full content only for selected messages.
- Create draft responses only. Do not send.
- Label/archive only under Sinclair HITL/autonomy rules.

Quota strategy:

- Gmail quotas are based on quota units per project and per user per minute.
- Track per-method cost if building sustained polling.
- Redis limiter keys:
  - `rl:gmail:<account_alias>`
  - `gmail:<account_alias>:last_history_id`
- Use truncated exponential backoff with jitter on rate errors.

### Google Calendar

API shapes:

```http
GET https://www.googleapis.com/calendar/v3/users/me/calendarList
Authorization: Bearer <access_token>
```

```http
GET https://www.googleapis.com/calendar/v3/calendars/primary/events?timeMin=2026-05-07T00:00:00-04:00&timeMax=2026-05-08T00:00:00-04:00&singleEvents=true&orderBy=startTime
Authorization: Bearer <access_token>
```

```http
POST https://www.googleapis.com/calendar/v3/calendars/primary/events?sendUpdates=none
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "summary": "HOLD: Proposed meeting",
  "start": {"dateTime": "2026-05-08T13:00:00-04:00"},
  "end": {"dateTime": "2026-05-08T13:30:00-04:00"},
  "attendees": [{"email": "person@example.com"}]
}
```

Push notification pattern:

- Calendar resources such as Events can be watched with an HTTPS webhook channel.
- Notifications tell the backend a resource changed; use sync tokens/incremental sync to reconcile.
- Push reduces polling and quota pressure.

MVP strategy:

- Read calendars and generate a calendar handling artifact.
- Create a proposal artifact, not a real external commitment, unless Marcus explicitly approves.
- If creating a hold on Marcus-owned calendar, mark it clearly and avoid external notifications.
- External meeting changes stay approval-gated.

Quota strategy:

- Calendar quotas are per project and per user, calculated per minute.
- Google may also rate limit rapid writes to a single calendar.
- Randomize periodic sync intervals; avoid synchronized midnight scans.
- Use push notifications where practical.

### Google Drive

Purpose:

- Store or retrieve supporting artifacts if the demo uses Google Docs/Drive.
- Optional for 12-hour MVP if Obsidian vault artifacts are enough.

API shapes:

```http
GET https://www.googleapis.com/drive/v3/files?q=name contains 'FlavorOS'&fields=files(id,name,mimeType,modifiedTime)
Authorization: Bearer <access_token>
```

```http
POST https://www.googleapis.com/drive/v3/changes/watch
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "id": "channel-uuid",
  "type": "web_hook",
  "address": "https://flavoros.example.com/google/drive/webhook"
}
```

Quota strategy:

- Drive returns 403 `User rate limit exceeded` or 429 on quota pressure.
- Official guidance is truncated exponential backoff.
- Watch calls count against quota; delivered notifications do not.
- Redis limiter keys:
  - `rl:drive:<account_alias>`

MVP strategy:

- Prefer vault markdown artifacts for the demo.
- Use Drive only if the story requires a native Google file.
- Store only file IDs and safe metadata in Postgres.

## Obsidian Git Sync

Purpose:

- Durable memory and work-product sync for SIGMAs, readiness artifacts, reports, people, projects, meetings, travel, wellness, and ops.

Current repo implementation:

- `infra/vault-sync.sh` pulls `OBSIDIAN_GIT_REMOTE` into `/vault`.
- If `OBSIDIAN_GIT_REMOTE` is unset, it sleeps indefinitely.
- The snapshot says `vault-sync` is parked until the vault Git remote/deploy key are configured.

MVP strategy:

- Do not block the demo on bidirectional vault Git sync.
- Write artifacts to the local `vault/` bind mount now.
- Add Git remote/deploy key after the Stack API protocol is clean.
- Use Obsidian Git or raw Git sync later for operator-visible vault replication.

Artifact rules:

- SIGMA: `vault/05-SIGMA/`
- Readiness artifact: `vault/15-Readiness/`
- Brief: `vault/10-Briefs/`
- Meeting prep: `vault/20-Meetings/`
- Project/ops: `vault/30-Projects/`, `vault/70-Ops/`
- Report: `vault/35-Reports/`
- People/CRM: `vault/40-People/`
- Travel/logistics: `vault/50-Travel/`
- Wellness: `vault/60-Wellness/`

Sync rules:

- Pull before write, write atomically where possible, then commit/push in a controlled worker.
- Commit message pattern:
  - `vault: add readiness artifact <work_order_id>`
  - `vault: add sigma <sigma_id>`
- Keep `.git`, `.obsidian/workspace*`, local plugin cache, and logs out of app-level sync unless deliberately configured.
- Do not sync dev-agent scratch files into client onboarding canon.

Reset before onboarding:

- Archive or delete demo scratch artifacts.
- Preserve architecture templates and examples.
- Create clean client envelope for Marcus/Christy.
- Re-run `/ctl` after the reset so the next session does not inherit demo noise.

## NATS, Redis, Postgres Patterns

NATS:

- Use NATS for work orders, reports, flags, health, and audit fanout.
- Current subjects:
  - `work_order.<agent>`
  - `report.<agent>`
  - `flag.<severity>`
  - `audit.*`
- Use request-reply only when the caller needs a bounded synchronous answer.
- Use plain publish for background work.
- Add JetStream later if reports/work orders must survive NATS/container restart.
- Queue groups become relevant when multiple workers share the same subject.

Redis:

- Use for ephemeral state, locks, de-dupe, and rate limits.
- Suggested keys:
  - `rl:<provider>:<scope>`
  - `lock:work_order:<id>`
  - `call:<call_sid>:state`
  - `dedupe:gmail:<message_id>`
  - `oauth:<account_alias>:access_token_cache`
- Use TTLs aggressively.
- Never store refresh tokens as ordinary Redis values unless encrypted and explicitly approved.

Postgres:

- Use for durable operational records:
  - `provider_events`
  - `work_orders`
  - `agent_reports`
  - `artifact_index`
  - `oauth_accounts`
  - `call_events`
  - `client_accounts`
- Use JSONB for provider payload metadata, but store raw private content only when necessary and scoped.
- For table-backed worker queues, use `FOR UPDATE SKIP LOCKED` to avoid consumer contention.

## Launch-Critical Provider Work

Ship now:

- Voice gateway routes transcript into context policy.
- Unknown live questions create readiness artifacts.
- Work orders publish to Maxine/Scooter/Kyle over NATS.
- Reports come back to Khadijah/Sinclair.
- One email/calendar demo flow creates SIGMA, draft reply, calendar artifact, PM/task artifact, and a visible follow-up.

Do later:

- Full Google push notification production setup.
- Full Obsidian Git bidirectional sync.
- JetStream persistence.
- Twilio signature enforcement for every environment after the live demo path is stable.
- Gemini Live wiring, unless the current OpenAI STT plus ElevenLabs path fails the demo.

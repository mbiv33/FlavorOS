# Group Chat Bot Architecture Handoff

Date: 2026-05-05

## What happened

The architecture docs were updated to include a shared group chat bot/front door for both Khadijah and Sinclair.

The intent captured in the docs is:

- Khadijah remains the primary conductor.
- Sinclair remains directly reachable for EA-domain work.
- The owner can now interact through three human-facing surfaces:
  - Khadijah direct
  - Sinclair direct
  - a shared Hermes group chat with both agents present

## Files updated

- `ARCHITECTURE.md`
- `README.md`
- `PHILOSOPHY.md`
- `CHIEF_OF_STAFF_CONTEXT.md`
- `DEPLOYMENT.md`

## Architecture decisions documented

- Added a new `Human Interface Topology` section in `ARCHITECTURE.md`.
- Defined the shared room as a text-first coordination surface.
- Khadijah owns first response by default in the shared room.
- Sinclair joins when explicitly mentioned or when the request clearly falls into EA scope.
- Maxine, Scooter, and Kyle remain dark to the owner; internal handoffs stay behind the Hermes layer.
- Khadijah and Sinclair keep their existing direct voice/interface lanes.

## Important constraint

This was handled as a docs/architecture update only.

No runtime implementation was added for:

- shared Telegram group routing
- mention parsing
- agent selection logic for the shared room
- any new bot/router service
- secret-loading changes for shared group chat configuration

## Recommended next Codex steps

1. Decide the runtime model for the shared group bot:
   - one shared router/bot in front of both Hermes agents
   - or both existing bots participating in the same Telegram group

2. If using a shared router, define:
   - where routing logic lives
   - how mentions map to Khadijah vs Sinclair
   - default fallback behavior when no agent is mentioned
   - how responses are serialized so both agents do not answer at once

3. Update runtime/config files as needed:
   - `infra/agent-base/agent.py`
   - `agents/khadijah/agent.yaml`
   - `agents/sinclair/agent.yaml`
   - `infra/secrets-loader/entrypoint.sh`
   - `infra/secrets/secrets.example.yaml`
   - possibly `docker-compose.yml` if a new shared router service is introduced

4. Add shared-chat configuration support:
   - group chat ID
   - shared bot token if applicable
   - routing rules and mention behavior

5. Document expected behavior for:
   - direct chat vs shared room
   - voice note handling in the shared room
   - conflict resolution when both agents could respond
   - audit/logging of shared-thread decisions

## Current repo state to be aware of

At the time of this handoff, the repo already had unrelated local changes and untracked files, including `.DS_Store` changes and `infra/secrets/secrets.enc.yaml`. Be careful not to overwrite or revert user changes while implementing the next step.

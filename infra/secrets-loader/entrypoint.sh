#!/usr/bin/env bash
# secrets-loader: decrypts SOPS-encrypted blobs and writes per-agent
# secrets to /run/flavor/secrets/<agent>/ on a tmpfs shared with agents.
#
# Inputs (mounted by docker-compose):
#   /etc/flavoros/age.key         — Layer 0 master private key (0400)
#   /secrets/secrets.enc.yaml     — Layer 1 encrypted blob
#   /secrets/composio.yaml        — non-secret grants map (per-agent scopes)
# Output:
#   /run/flavor/secrets/<agent>/* — Layer 2 in-memory secrets

set -euo pipefail

AGE_KEY=${AGE_KEY:-/etc/flavoros/age.key}
SECRETS_FILE=${SECRETS_FILE:-/secrets/secrets.enc.yaml}
GRANTS_FILE=${GRANTS_FILE:-/secrets/composio.yaml}
OUT_DIR=${OUT_DIR:-/run/flavor/secrets}

if [[ ! -r "$AGE_KEY" ]]; then
  echo "FATAL: age private key missing at $AGE_KEY" >&2
  exit 1
fi
export SOPS_AGE_KEY_FILE="$AGE_KEY"

mkdir -p "$OUT_DIR"
chmod 0700 "$OUT_DIR"

echo "[secrets-loader] decrypting $SECRETS_FILE"
PLAIN=$(sops --decrypt "$SECRETS_FILE")

# ── Shared values that every agent gets ──────────────────────────
shared_dir="$OUT_DIR/_shared"
mkdir -p "$shared_dir" && chmod 0700 "$shared_dir"
echo "$PLAIN" | yq -r '.openrouter.api_key' > "$shared_dir/openrouter.key"
chmod 0400 "$shared_dir/openrouter.key"

# ── Per-agent: filter Composio connection_ids by grants ──────────
agents=(khadijah sinclair maxine kyle regine scooter watson overton)

for agent in "${agents[@]}"; do
  d="$OUT_DIR/$agent"
  mkdir -p "$d" && chmod 0700 "$d"

  # Aliases this agent is allowed to read or write
  read_aliases=$(yq -r ".grants.$agent.read[]?  // empty" "$GRANTS_FILE")
  write_aliases=$(yq -r ".grants.$agent.write[]? // empty" "$GRANTS_FILE")
  all_aliases=$(printf "%s\n%s\n" "$read_aliases" "$write_aliases" | sort -u | grep -v '^$' || true)

  # Build a filtered composio_connections.json with ONLY this agent's grants
  filtered="{}"
  for alias in $all_aliases; do
    cid=$(echo "$PLAIN" | yq -r ".composio_connections.$alias // \"\"")
    if [[ -n "$cid" && "$cid" != "null" ]]; then
      filtered=$(echo "$filtered" | jq --arg k "$alias" --arg v "$cid" '.[$k]=$v')
    fi
  done
  echo "$filtered" > "$d/composio_connections.json"
  chmod 0400 "$d/composio_connections.json"

  # Symlink the shared OpenRouter key
  ln -sf "$shared_dir/openrouter.key" "$d/openrouter.key"

  # Agent-specific overrides
  override=$(echo "$PLAIN" | yq -r ".agent_overrides.$agent // {}" -o=json)
  if [[ "$override" != "{}" && "$override" != "null" ]]; then
    echo "$override" > "$d/overrides.json"
    chmod 0400 "$d/overrides.json"
  fi

  # Khadijah-only: Telegram, ElevenLabs voice, Whisper STT, workspace key
  if [[ "$agent" == "khadijah" ]]; then
    echo "$PLAIN" | yq -r '.telegram.bot_token'         > "$d/telegram.token"
    echo "$PLAIN" | yq -r '.telegram.user_id'           > "$d/telegram.user"
    echo "$PLAIN" | yq -r '.composio.workspace_api_key' > "$d/composio.key"
    echo "$PLAIN" | yq -r '.elevenlabs.api_key'         > "$d/elevenlabs.key"
    echo "$PLAIN" | yq -r '.elevenlabs.voice_id'        > "$d/elevenlabs.voice_id"
    echo "$PLAIN" | yq -r '.openai.api_key'             > "$d/openai_whisper.key"
    chmod 0400 "$d"/{telegram.token,telegram.user,composio.key,elevenlabs.key,elevenlabs.voice_id,openai_whisper.key}
  fi

  count=$(ls -1 "$d" | wc -l)
  echo "[secrets-loader] $agent: $count files"
done

# Audit log line
echo "[secrets-loader] OK $(date -u +%FT%TZ) agents=${#agents[@]}"

# Stay alive so the tmpfs persists; re-decrypt on SIGHUP for rotation.
trap 'echo "[secrets-loader] reloading"; exec "$0" "$@"' HUP
sleep infinity

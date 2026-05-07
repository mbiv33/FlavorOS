#!/usr/bin/env bash

set -euo pipefail

root="${1:-.}"
env_file="$root/.env"
secrets_file="$root/infra/secrets/secrets.yaml"
tracker_file="$root/.ops-private/account-secrets-tracker.md"

status=0

has_rg() {
  command -v rg >/dev/null 2>&1
}

file_has_pattern() {
  local pattern="$1"
  local path="$2"

  if has_rg; then
    rg -q "$pattern" "$path"
  else
    grep -Eq "$pattern" "$path"
  fi
}

check_file() {
  local path="$1"
  if [[ -f "$path" ]]; then
    echo "present  $path"
  else
    echo "missing  $path"
    status=1
  fi
}

check_env_key() {
  local key="$1"
  if [[ -f "$env_file" ]] && file_has_pattern "^${key}=" "$env_file"; then
    echo "present  env:$key"
  else
    echo "missing  env:$key"
    status=1
  fi
}

check_yaml_key() {
  local pattern="$1"
  local label="$2"
  if [[ -f "$secrets_file" ]] && file_has_pattern "$pattern" "$secrets_file"; then
    echo "present  secret:$label"
  else
    echo "missing  secret:$label"
    status=1
  fi
}

check_yaml_section_key() {
  local section="$1"
  local key="$2"
  local label="$3"

  if [[ -f "$secrets_file" ]] && awk -v section="$section" -v key="$key" '
    $0 ~ "^" section ":" { in_section=1; next }
    in_section && $0 ~ "^[^[:space:]#][^:]*:" { in_section=0 }
    in_section && $0 ~ "^[[:space:]]+" key ":" { found=1 }
    END { exit found ? 0 : 1 }
  ' "$secrets_file"; then
    echo "present  secret:$label"
  else
    echo "missing  secret:$label"
    status=1
  fi
}

echo "Checking private workspace files"
check_file "$tracker_file"
check_file "$env_file"
check_file "$secrets_file"

echo
echo "Checking .env keys"
check_env_key "APP_ENV"
check_env_key "LOG_LEVEL"
check_env_key "TIMEZONE"
check_env_key "PUBLIC_BASE_URL"
check_env_key "VOICE_BASE_URL"
check_env_key "KHADIJAH_DOMAIN"
check_env_key "TWILIO_VOICE_WEBHOOK_URL"
check_env_key "TWILIO_STREAM_URL"
check_env_key "GEMINI_MODEL"
check_env_key "GEMINI_LIVE_MODEL"
check_env_key "ELEVENLABS_MODEL_ID"
check_env_key "OPENROUTER_BASE_URL"
check_env_key "OBSIDIAN_GIT_REMOTE"

echo
echo "Checking secret placeholders"
check_yaml_key '^openrouter:$' 'openrouter'
check_yaml_section_key 'openrouter' 'api_key' 'openrouter api key'
check_yaml_key '^composio:$' 'composio'
check_yaml_section_key 'composio' 'workspace_api_key' 'composio workspace api key'
check_yaml_key '^twilio:$' 'twilio'
check_yaml_section_key 'twilio' 'account_sid' 'twilio account sid'
check_yaml_section_key 'twilio' 'auth_token' 'twilio auth token'
check_yaml_section_key 'twilio' 'phone_number' 'twilio phone number'
check_yaml_key '^gemini:$' 'gemini'
check_yaml_section_key 'gemini' 'api_key' 'gemini api key'
check_yaml_key '^telegram:$' 'telegram'
check_yaml_section_key 'telegram' 'khadijah_bot_token' 'khadijah telegram bot token'
check_yaml_section_key 'telegram' 'sinclair_bot_token' 'sinclair telegram bot token'
check_yaml_key '^elevenlabs:$' 'elevenlabs'
check_yaml_section_key 'elevenlabs' 'api_key' 'elevenlabs api key'
check_yaml_section_key 'elevenlabs' 'khadijah_voice_id' 'khadijah elevenlabs voice id'
check_yaml_section_key 'elevenlabs' 'sinclair_voice_id' 'sinclair elevenlabs voice id'
check_yaml_key '^openai:$' 'openai whisper'
check_yaml_section_key 'openai' 'api_key' 'openai whisper api key'
check_yaml_key '^postgres:$' 'postgres'
check_yaml_section_key 'postgres' 'password' 'postgres password'
check_yaml_key '^obsidian:$' 'obsidian'
check_yaml_section_key 'obsidian' 'git_remote' 'obsidian git remote'
check_yaml_section_key 'obsidian' 'git_ssh_private_key' 'obsidian git ssh private key'

echo
if [[ $status -eq 0 ]]; then
  echo "Readiness check passed: required local files and key names are present."
else
  echo "Readiness check failed: one or more required files or key names are missing."
fi

exit "$status"

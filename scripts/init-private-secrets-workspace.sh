#!/usr/bin/env bash

set -euo pipefail

root="${1:-.}"
private_dir="$root/.ops-private"

mkdir -p "$private_dir"

copy_if_missing() {
  local src="$1"
  local dest="$2"
  if [[ ! -e "$dest" ]]; then
    cp "$src" "$dest"
    echo "created $dest"
  else
    echo "kept $dest"
  fi
}

copy_if_missing \
  "$root/docs/build/codex-claude/PRIVATE_ACCOUNT_AND_SECRETS_TRACKER_TEMPLATE.md" \
  "$private_dir/account-secrets-tracker.md"

copy_if_missing \
  "$root/docs/build/codex-claude/env.example.reference" \
  "$root/.env"

copy_if_missing \
  "$root/infra/secrets/secrets.example.yaml" \
  "$root/infra/secrets/secrets.yaml"

cat <<'EOF'

Private secrets workspace is ready.

Edit locally:
- .ops-private/account-secrets-tracker.md
- .env
- infra/secrets/secrets.yaml

Do not paste live values into chat.
Encrypt plaintext secrets before any commit or VPS sync.
EOF

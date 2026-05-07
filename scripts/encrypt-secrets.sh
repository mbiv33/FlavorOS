#!/usr/bin/env bash

set -euo pipefail

root="${1:-.}"
plain="$root/infra/secrets/secrets.yaml"
encrypted="$root/infra/secrets/secrets.enc.yaml"
sops_config="$root/infra/secrets/.sops.yaml"
remove_plaintext="${REMOVE_PLAINTEXT:-0}"

require_cmd() {
  local cmd="$1"
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "missing dependency: $cmd" >&2
    exit 1
  fi
}

require_file() {
  local path="$1"
  if [[ ! -f "$path" ]]; then
    echo "missing file: $path" >&2
    exit 1
  fi
}

require_cmd sops
require_file "$plain"
require_file "$sops_config"

if grep -q 'age1REPLACE_WITH_YOUR_PUBLIC_KEY' "$sops_config"; then
  echo "update $sops_config with your real age public key before encrypting" >&2
  exit 1
fi

tmp="$(mktemp "${TMPDIR:-/tmp}/flavoros-secrets.XXXXXX.yaml")"
trap 'rm -f "$tmp"' EXIT

sops --config "$sops_config" --encrypt "$plain" > "$tmp"
mv "$tmp" "$encrypted"
trap - EXIT

echo "created $encrypted"

if [[ "$remove_plaintext" == "1" ]]; then
  rm -f "$plain"
  echo "removed $plain"
else
  echo "kept $plain"
  echo "set REMOVE_PLAINTEXT=1 to remove the local plaintext after verification"
fi

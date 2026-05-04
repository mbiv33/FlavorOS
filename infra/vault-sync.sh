#!/bin/sh
# vault-sync: periodically pulls the Obsidian vault from git.
set -eu

cd /vault

if [ -z "${OBSIDIAN_GIT_REMOTE:-}" ]; then
  echo "[vault-sync] OBSIDIAN_GIT_REMOTE not set, sleeping indefinitely"
  exec sleep infinity
fi

if [ ! -d .git ]; then
  git clone "$OBSIDIAN_GIT_REMOTE" /tmp/vault-clone
  cp -a /tmp/vault-clone/. /vault/
  rm -rf /tmp/vault-clone
fi

while true; do
  echo "[vault-sync] pulling $(date -u +%FT%TZ)"
  git pull --rebase --autostash || echo "[vault-sync] pull failed, will retry"
  sleep 300
done

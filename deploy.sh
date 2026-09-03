#!/usr/bin/env bash
# Deploy this repo to /var/www/html on the host. Run:  sudo ./deploy.sh
#
# The repo is the source of truth for the site; the host Caddy serves
# /var/www/html directly. HTML is served pass-through (Cloudflare cf-cache:
# DYNAMIC) and static assets are content-hashed or under /fonts//img/ with
# immutable cache headers, so no Cloudflare purge is needed.
set -euo pipefail

SRC="$(cd "$(dirname "$0")" && pwd)/"
DEST="/var/www/html/"

if [ "$(id -u)" -ne 0 ]; then exec sudo -- "$0" "$@"; fi

rsync -a --delete --chown=caddy:caddy \
  --exclude=.git --exclude=.gitignore --exclude=README.md --exclude=CHANGELOG.md \
  --exclude=deploy.sh --exclude=fa --exclude=_build-legacy --exclude=node_modules \
  --itemize-changes \
  "$SRC" "$DEST"

rev="$(git -C "$SRC" rev-parse --short HEAD 2>/dev/null || echo '?')"
echo "deployed $rev -> $DEST"

# smoke test through the local Caddy
fail=0
for p in / /about/ /experience/ /skills/ /certifications/ /contact/ /projects/ /homelab/; do
  code="$(curl -sk -o /dev/null -w '%{http_code}' --resolve trenck.net:443:127.0.0.1 "https://trenck.net$p")"
  printf '  %-18s %s\n' "$p" "$code"
  [ "$code" = 200 ] || fail=1
done
exit $fail

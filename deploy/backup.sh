#!/bin/sh
# Backup: the site is a git-tracked immutable artifact; the only mutable thing
# is the Caddy config + certs. Snapshot both.
set -eu
TS=$(date +%Y%m%d-%H%M%S)
DEST="${1:-$HOME/backups/aigatewaylab}"
mkdir -p "$DEST"
tar czf "$DEST/agl-$TS.tar.gz" \
    -C /home/ubuntu gateway-showcase/site gateway-showcase/deploy \
    2>/dev/null
ls -t "$DEST"/agl-*.tar.gz | tail -n +8 | xargs -r rm --
echo "backup written: $DEST/agl-$TS.tar.gz"

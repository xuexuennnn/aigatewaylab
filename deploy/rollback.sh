#!/bin/sh
# Rollback: rebuild the previous image tag and restart. The site is stateless,
# so rollback = redeploy previous git commit.
set -eu
cd /home/ubuntu/gateway-showcase
PREV="${1:?usage: rollback.sh <git-ref>}"
git worktree add /tmp/agl-rollback "$PREV"
cd /tmp/agl-rollback/deploy 2>/dev/null || cd /tmp/agl-rollback
docker compose -f deploy/docker-compose.yml build --pull
docker compose -f deploy/docker-compose.yml up -d
cd /home/ubuntu/gateway-showcase && git worktree remove --force /tmp/agl-rollback
echo "rolled back to $PREV — verify with: curl -sI http://127.0.0.1:8890/"

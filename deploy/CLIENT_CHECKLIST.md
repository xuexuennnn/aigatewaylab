# Client Deployment Checklist — Self-Hosted AI Gateway

Use this checklist when deploying a gateway for a client. Every box is checked
by running the named command or inspecting the named artifact — not by memory.

## 1. Before touching the server

- [ ] Written scope agreed: gateway software, server, domain, provider keys (BYOK)
- [ ] Client confirms the server is theirs (or approves provisioning cost)
- [ ] Access: SSH key added by the client; no password auth
- [ ] Compliance check: use case is BYOK / official APIs only — no account
      pooling, no subscription-to-API conversion, no rate-limit evasion
- [ ] Rollback contact and maintenance window agreed

## 2. Server baseline

- [ ] OS updated; unattended security upgrades enabled
- [ ] Firewall default-deny inbound; only 22 and 443 open (`ufw status` / cloud SG)
- [ ] fail2ban or equivalent on SSH
- [ ] Non-root deploy user; docker group membership only if needed
- [ ] Time sync active (`timedatectl`)

## 3. Gateway deployment

- [ ] Gateway runs in Docker Compose under a non-root user
- [ ] Containers: `read_only: true`, `cap_drop: [ALL]`, `no-new-privileges`
- [ ] Dedicated Docker network; DB/admin ports bound to loopback only
- [ ] Provider keys in an env file with `0600` perms (or a secret store) —
      never in the compose file, never in git
- [ ] Admin UI reachable only via SSH tunnel or VPN, not on the public interface
- [ ] `docker inspect` confirms restart policy `unless-stopped`

## 4. HTTPS and edge

- [ ] Reverse proxy (Caddy/nginx) terminates TLS; auto-renewal verified
      (`caddy validate` / staged renewal dry-run)
- [ ] HSTS, X-Content-Type-Options, Referrer-Policy, frame-ancestors set —
      verified with `curl -sI https://domain`
- [ ] Rate limiting active at the proxy; tested with a burst probe
- [ ] External port scan from an outside host shows only 22/443

## 5. Operations

- [ ] Virtual keys created per team with budgets and model scopes
- [ ] Request logging on; log redaction verified by reading an actual log line
- [ ] Backup script scheduled; **restore tested once for real**
- [ ] Health endpoint monitored (uptime service or cron probe)
- [ ] Upgrade runbook written: image pin, backup, pull, migrate, verify, rollback

## 6. Handover

- [ ] Admin credentials transferred through the client's secret channel, then
      rotated by the client
- [ ] My SSH access removed (client runs `whoami`-level verification)
- [ ] Runbook + architecture note delivered
- [ ] 30-minute walkthrough completed

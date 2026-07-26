"""Docs + Security page bodies."""

DOCS_TITLE = "Deployment Documentation"
DOCS_DESC = ("Step-by-step: Docker deployment, HTTPS, backups, upgrades and "
             "monitoring for a self-hosted AI API gateway.")
DOCS_BODY = """
<h1>Deployment Docs</h1>
<p class="lead">The condensed, public version of the runbook every client
receives. Commands are real and tested against the open-source gateway stack
in the demo; hostnames and paths are examples.</p>

<h2>1 · Docker deployment</h2>
<pre><code># docker-compose.yml (excerpt — full file in the GitHub repo)
services:
  gateway:
    image: ghcr.io/berriai/litellm:main-stable   # or your gateway of choice
    user: "10001:10001"            # non-root
    read_only: true                # read-only rootfs
    tmpfs: [/tmp]
    env_file: /srv/gateway/secrets.env   # 0600, root:root
    expose: ["4000"]               # internal only — no public bind
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "wget", "-qO-", "http://127.0.0.1:4000/health/liveliness"]
      interval: 30s
      retries: 3</code></pre>
<p>Principles: the gateway container never publishes a host port; only the
reverse proxy does. Secrets live in an env file owned by root with mode 0600,
mounted read-only. The container runs as a fixed non-root UID with a
read-only filesystem.</p>

<h2>2 · HTTPS with automatic renewal</h2>
<pre><code># Caddyfile — HTTPS, HSTS and headers in 8 lines
example.com {{
  encode gzip
  header {{
    Strict-Transport-Security "max-age=31536000; includeSubDomains"
    X-Content-Type-Options nosniff
    X-Frame-Options DENY
    Referrer-Policy strict-origin-when-cross-origin
  }}
  reverse_proxy 127.0.0.1:4000
}}</code></pre>
<p>Caddy provisions and renews certificates automatically. With nginx the
same is done with certbot and a systemd timer; both variants are in the repo.</p>

<h2>3 · Backups that restore</h2>
<pre><code># nightly: dump DB + config, encrypt, keep 14 days
sqlite3 /srv/gateway/data/gateway.db ".backup /tmp/gw.db"
tar czf - -C /srv/gateway config data | age -r "$BACKUP_PUBKEY" \
  &gt; /backup/gateway-$(date +%F).tar.gz.age
find /backup -name "gateway-*.age" -mtime +14 -delete</code></pre>
<p>A backup is not a backup until it has been restored. The runbook includes
a quarterly restore drill: restore to a scratch directory, start a second
gateway instance on a private port, run the smoke tests, tear down.</p>

<h2>4 · Upgrades without surprises</h2>
<ol>
<li>Read the release notes; check for schema migrations.</li>
<li>Snapshot: backup as above, note current image digest.</li>
<li>Pull the new image, restart, watch the health endpoint and error rate.</li>
<li>Regression: run the smoke suite (key create → chat request → usage row).</li>
<li>Rollback path: previous image digest + restored DB — rehearsed, so the
timeline is known per deployment, not guessed.</li>
</ol>

<h2>5 · Monitoring</h2>
<ul>
<li><code>/health</code> endpoints probed by an external checker with
transition-based alerting (alert once on failure, once on recovery — no
storms).</li>
<li>Disk, memory and certificate-expiry checks on the host.</li>
<li>Usage anomaly review: a spike on one virtual key is a conversation, not
a mystery.</li>
</ul>
"""

SEC_TITLE = "Security Model"
SEC_DESC = ("Key custody, least privilege, log redaction and incident "
            "recovery for self-hosted AI API gateways.")
SEC_BODY = """
<h1>Security</h1>
<p class="lead">The parts of gateway operations that are invisible in a happy
demo and decisive in an incident.</p>

<h2>Key custody</h2>
<table>
<tr><th>Secret</th><th>Where it lives</th><th>Where it must never appear</th></tr>
<tr><td>Provider keys (sk-…)</td><td>env file 0600 on the host, or a secrets
manager; readable only by the gateway process user</td><td>logs, error
bodies, client responses, git, container images, backups in plaintext</td></tr>
<tr><td>Virtual keys (vk-…)</td><td>hashed at rest in the gateway DB</td>
<td>anywhere in full after creation — the UI shows a one-time reveal, logs
show a prefix</td></tr>
<tr><td>Admin credentials</td><td>password manager; TOTP enabled</td>
<td>shared chats, .env files in repos</td></tr>
</table>

<h2>Least privilege</h2>
<ul>
<li>Containers run as a dedicated non-root UID with a read-only root
filesystem and a tmpfs for scratch space.</li>
<li>The admin plane binds to localhost; reaching it requires SSH tunnel or
VPN membership. The public interface serves inference traffic only.</li>
<li>Database user has no DDL rights at runtime; migrations run as a separate
step.</li>
<li>Each client team gets its own virtual keys with model allow-lists and
budgets — revoking one client never touches another.</li>
</ul>

<h2>Log redaction</h2>
<p>Gateways sit on the request path, so their logs are a honeypot by default.
The deployment redacts:</p>
<ul>
<li><code>Authorization</code> headers → <code>vk-****last4</code></li>
<li>Prompt and completion bodies → logged only as token counts unless the
client explicitly opts into content logging for debugging, with a TTL</li>
<li>Upstream error bodies → provider keys stripped before the error reaches
client or log</li>
</ul>
<p>The <a href="../demo/">demo</a> request log shows exactly this shape:
enough to operate, nothing worth stealing.</p>

<h2>Recovery flows (rehearsed, not theoretical)</h2>
<table>
<tr><th>Incident</th><th>Response</th></tr>
<tr><td>Virtual key leaked</td><td>Revoke the key (requests fail closed),
review its usage window in the audit log, issue a replacement with the same
policy. Blast radius: that key\u2019s quota.</td></tr>
<tr><td>Provider key suspected</td><td>Rotate at the provider, update the
vault entry, restart the gateway (seconds of downtime behind a retrying
proxy), verify with a canary request.</td></tr>
<tr><td>Host compromise suspected</td><td>Freeze: revoke provider keys at the
provider first — they are the crown jewels. Rebuild from a clean image plus
the encrypted backup; never restore executables from the compromised host.</td></tr>
<tr><td>Data loss</td><td>Restore last night\u2019s encrypted dump; usage rows
since the dump are gone and acknowledged as gone — billing reconciles against
provider dashboards.</td></tr>
</table>
"""

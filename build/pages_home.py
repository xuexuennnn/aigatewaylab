"""Home + Architecture page bodies."""

HOME_TITLE = "Self-Hosted AI API Gateway Deployment & Operations"
HOME_DESC = ("Deployment, hardening and operations of self-hosted AI API "
             "gateways: Docker, HTTPS, key management, monitoring, backup "
             "and failover. Independent demonstration site.")
HOME_BODY = """
<div class="hero">
<div>
<p class="kicker">Deployment &middot; Hardening &middot; Operations</p>
<h1>Self-Hosted AI API Gateway<br>Deployment &amp; Operations</h1>
<p class="lead">I deploy, harden and operate self-hosted AI API gateways for
teams that want one controlled entry point for their LLM traffic — with their
own keys, their own logs, and their own infrastructure.</p>
<p class="cta-row">
  <a class="btn contact-mail" href="mailto:hello@aigatewaylab.xyz?subject=Gateway%20deployment%20review">Request a deployment review</a>
  <a class="btn ghost btn-gap" href="demo/">View live demo</a>
</p>
<p class="contact-plain dim">Email: <span class="contact-addr">hello@aigatewaylab.xyz</span>
<span class="copy-hint" aria-live="polite"></span></p>
</div>
<div class="hero-console" aria-label="Example deployment session (static illustration)">
  <div class="hc-bar"><span class="hc-dot"></span><span class="hc-dot"></span><span class="hc-dot"></span>deploy &middot; verify &middot; hand over</div>
<pre><code><span class="hc-c"># every deployment ends with proof, not promises</span>
<span class="hc-k">$</span> deployctl preflight --remote gateway-host
<span class="hc-o">ok</span>  ports 80/443 free &middot; docker 27.x &middot; 4GB free
<span class="hc-k">$</span> deployctl apply --plan plan.json
<span class="hc-o">ok</span>  container healthy &middot; bound 127.0.0.1 only
<span class="hc-k">$</span> deployctl verify --target gateway-host
<span class="hc-o">ok</span>  TLS A &middot; HSTS &middot; headers 6/6 &middot; logs redacted
<span class="hc-c"># handover: runbook + backups + your keys, not mine</span></code></pre>
</div>
</div>

<section class="case-proof">
<h2>See the operating model, not a sales claim</h2>
<div class="proof-panel">
  <div><span class="proof-step">01</span><h3>Inspect</h3><p class="dim">Preflight the host, network exposure, key custody and rollback path before changing anything.</p></div>
  <div><span class="proof-step">02</span><h3>Deploy</h3><p class="dim">Apply a documented configuration with a narrow public surface and revocable virtual keys.</p></div>
  <div><span class="proof-step">03</span><h3>Verify</h3><p class="dim">Probe TLS, health, failover, log redaction, backup and restore instead of treating a running container as proof.</p></div>
</div>
<p><a href="case-study/">Read the anonymised case-study pattern</a> or <a href="docs/">inspect the public runbook</a>.</p>
</section>

<h2>The problem</h2>
<div class="grid c3">
  <div class="card glass"><h3>Keys everywhere</h3><p class="dim">Provider API keys
  pasted into notebooks, CI variables and desktop apps. Nobody knows which key
  is used where, or what it would cost to rotate one.</p></div>
  <div class="card glass"><h3>No spend visibility</h3><p class="dim">The invoice
  arrives at month end. Which team, which feature, which runaway script spent
  the budget? The provider dashboard cannot tell you.</p></div>
  <div class="card glass"><h3>Provider lock-in at the code level</h3><p class="dim">
  Every service hardcodes one vendor SDK. Switching models — or surviving an
  outage — means a code change and a deploy.</p></div>
</div>

<h2>What a gateway fixes</h2>
<p>A self-hosted gateway (open-source projects such as LiteLLM, one-api or
Sub2API-class deployments) gives you one OpenAI-compatible endpoint in front
of every upstream you use. Your services get <em>virtual keys</em> you can
create, cap and revoke; upstream keys stay in one vault. You get per-key
usage, rate limits, model routing and failover — on your own server.</p>

<h2>What I deliver</h2>
<div class="grid c2">
  <div class="card"><h3>Deployment</h3><p class="dim">Docker Compose or
  systemd deployment, reverse proxy with HTTPS and HSTS, non-root containers,
  a documented directory layout, and an upgrade path that has been tested,
  not guessed.</p></div>
  <div class="card"><h3>Hardening</h3><p class="dim">Key vaulting with
  restricted permissions, admin plane separated from the data plane, security
  headers, fail2ban, log redaction so secrets never land in plaintext logs.</p></div>
  <div class="card"><h3>Operations</h3><p class="dim">Health checks and
  alerting, usage dashboards, backup and restore drills with a written
  runbook, quota policies per team and per key.</p></div>
  <div class="card"><h3>Handover</h3><p class="dim">You own everything at the
  end: infrastructure, documentation, and a recorded walkthrough. No
  dependency on me to keep it running.</p></div>
</div>

<h2>Scope boundaries, stated up front</h2>
<div class="notice">I deploy gateways that route traffic under <strong>your
provider accounts and API keys</strong> (or keys your organisation is
licensed to use). I do not build or operate systems for reselling consumer
subscriptions as APIs, sharing or pooling account quotas, bypassing provider
rate limits, or extracting credentials. See the
<a href="compliance/">compliance page</a> for the full matrix.</div>

<section class="final-cta">
  <div><p class="kicker">Start with the environment, not a package</p>
  <h2>Need a gateway you can operate after handover?</h2>
  <p class="dim">Send the target stack, server constraints and required upstreams. I will confirm fit and scope before any deployment work begins.</p></div>
  <a class="btn contact-mail" href="mailto:hello@aigatewaylab.xyz?subject=Gateway%20deployment%20review">Request a deployment review</a>
</section>
"""

ARCH_TITLE = "Gateway Architecture"
ARCH_DESC = ("Reference architecture for a self-hosted AI API gateway: trust "
             "boundaries, data flow, key custody and failure domains.")
ARCH_BODY = """
<h1>Architecture</h1>
<p class="lead">The reference layout I deploy, and — more important — where
the trust boundaries sit.</p>

<h2>Data flow</h2>
<div class="diagram">
 Clients (your services, staff tools)
   │  virtual keys (vk-...), never provider keys
   ▼
┌───────────────────────────────────────────────┐
│  Reverse proxy  (Caddy / nginx)               │  TLS, HSTS, rate limit,
│  - terminates HTTPS                           │  security headers
└───────────────┬───────────────────────────────┘
                ▼
┌───────────────────────────────────────────────┐
│  Gateway  (LiteLLM / one-api class)           │
│  - auth: virtual key → team, quota, models    │
│  - routing: model name → upstream pool        │
│  - usage metering, request logging (redacted) │
│  - failover: retry next healthy upstream      │
└──────┬──────────────────────────┬─────────────┘
       ▼                          ▼
┌──────────────┐          ┌──────────────┐
│ Key vault    │          │ SQLite/Postgres│
│ (env/file,   │          │ usage, keys,   │
│  0600, no    │          │ audit log      │
│  web access) │          └──────────────┘
└──────┬───────┘
       ▼  provider keys (sk-..., owned by YOU)
 Upstream providers (OpenAI, Anthropic, Google, ... official APIs)
</div>

<h2>Trust boundaries</h2>
<table>
<tr><th>Boundary</th><th>Rule</th></tr>
<tr><td>Internet → proxy</td><td>Only 443 exposed. Admin UI is not on the
public interface — SSH tunnel or VPN only.</td></tr>
<tr><td>Proxy → gateway</td><td>Loopback or private network. The gateway
container never binds a public port.</td></tr>
<tr><td>Gateway → vault</td><td>Provider keys are readable by the gateway
process user only (0600, non-root). They never appear in logs, error
messages, or client responses.</td></tr>
<tr><td>Client → gateway</td><td>Clients hold revocable virtual keys with
quotas. Compromise of a client burns one virtual key, not the provider
account.</td></tr>
</table>

<h2>Failure domains</h2>
<ul>
<li><strong>Upstream outage:</strong> health checks mark the upstream
unhealthy; router retries the request against the next configured provider
offering the same model class. The <a href="../case-study/">case study</a>
shows a real failover timeline (with synthetic data).</li>
<li><strong>Gateway crash:</strong> systemd/compose restart policy plus an
external health probe that alerts once per state change.</li>
<li><strong>Host loss:</strong> nightly encrypted backup of the database and
config; restore drill documented and rehearsed — restore time depends on
image pull and DNS, measured per deployment during handover.</li>
</ul>
"""

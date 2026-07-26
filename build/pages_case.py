"""Case study + Compliance page bodies."""

CASE_TITLE = "Case Study: Migration, Routing & Failover"
CASE_DESC = ("An anonymised gateway engagement: consolidating scattered API "
             "keys, adding model routing, and surviving an upstream outage.")
CASE_BODY = """
<h1>Case Study</h1>
<div class="notice">Anonymised and generalised from real operational work on
self-hosted gateway deployments. Identifying details, hostnames, exact
figures and vendor mix are altered; the timeline structure and the failure
modes are the real lesson. All numbers below are illustrative of the pattern,
not billing records.</div>

<h2>Starting point</h2>
<p>A small product team ran three services against two AI providers. Each
service held its own provider key in its own env file; one key had been
shared over chat during an incident and never rotated. There was no per-team
usage view — the invoice was one number.</p>

<h2>Phase 1 · Consolidation (week 1)</h2>
<ul>
<li>Deployed the gateway (Docker Compose, non-root, read-only rootfs) behind
Caddy with HTTPS and HSTS on an internal subdomain.</li>
<li>Moved both provider keys into the vault file; issued one virtual key per
service with a monthly budget and a model allow-list.</li>
<li>Services switched by changing <code>base_url</code> and key — no code
changes, because the gateway speaks the same API dialect.</li>
<li>Rotated the chat-leaked provider key <em>after</em> cutover; zero client
changes needed, which is the point of the indirection.</li>
</ul>

<h2>Phase 2 · Routing policy (week 2)</h2>
<ul>
<li>Cheap/fast model class for internal tooling, premium class for the
customer-facing feature — enforced by key, not by convention.</li>
<li>Per-key rate limits sized from two weeks of observed traffic.</li>
<li>Nightly encrypted backups plus an external health probe with
transition-based alerting.</li>
</ul>

<h2>Phase 3 · The outage that paid for it</h2>
<p>Some weeks later, the primary provider had a partial outage — elevated
errors and latency (the pattern any status page archive will show for every
major provider). Timeline as the gateway saw it, reproduced in the
<a href="../demo/">demo</a> with synthetic data:</p>
<div class="diagram">
T+0m   upstream A error rate exceeds threshold; health check marks A degraded
T+0m   router begins retrying failed requests against upstream B (same class)
T+2m   probe alerts once: "upstream-a: FAIL" — one message, no storm
T+31m  provider recovers; health check passes twice; A back in rotation
T+31m  probe alerts once: "upstream-a: RECOVERED"
Client-visible impact: elevated p95 latency for ~2 minutes; zero 5xx bursts
</div>

<h2>What made it boring (the goal)</h2>
<ul>
<li>Failover was configured and <em>tested with a forced failure drill</em>
during handover — the incident was the second time it ran, not the first.</li>
<li>Alert deduplication meant two messages, not two hundred.</li>
<li>The retrospective was one paragraph, because the audit log already had
the timeline.</li>
</ul>

<h2>Handover</h2>
<p>The team received the runbook, the restore drill recording, and admin
access. My involvement ended by design; the system did not need me — that is
the deliverable.</p>
"""

COMP_TITLE = "Compliance & Boundaries"
COMP_DESC = ("What this practice does and refuses: provider-by-provider "
             "compliance matrix for self-hosted AI gateway deployments.")
COMP_BODY = """
<h1>Compliance</h1>
<p class="lead">Gateways are dual-use. The same routing tech that manages a
company\u2019s own keys can be misused to resell consumer subscriptions.
This page states, in writing, which side of the line this practice is on.</p>

<h2>Services provided</h2>
<ul>
<li>Deployment and operation of gateways routing traffic under <strong>your
organisation\u2019s own API keys</strong> (BYOK) obtained from providers\u2019
official API programs.</li>
<li>Virtual-key management, quotas, usage metering, routing and failover
across <em>your</em> accounts.</li>
<li>Security hardening, monitoring, backup and handover.</li>
</ul>

<h2>Refused, regardless of payment</h2>
<ul>
<li>Converting consumer subscriptions (ChatGPT Plus, Claude Pro/Max, Gemini
consumer plans, etc.) into resellable API access.</li>
<li>Account pooling, quota sharing or resale of account capacity.</li>
<li>Bypassing provider rate limits, concurrency caps or anti-abuse systems.</li>
<li>Extracting, buying, selling or transferring account credentials.</li>
<li>Scraping private web UIs to simulate API access.</li>
</ul>

<h2>Provider matrix (API access modes)</h2>
<div class="notice">Summarised from provider terms as read on 2026-07-26.
Terms change; verify against the linked originals before relying on this
table. This is an engineering compliance summary, not legal advice.</div>
<table>
<tr><th>Provider</th><th>Official API (BYOK)</th><th>Consumer-subscription
relay via gateway</th><th>Notes</th></tr>
<tr><td>OpenAI</td><td class="ok-cell">Permitted — platform API keys</td>
<td>Not permitted for third-party resale relay</td><td>Platform terms tie
API usage to the account holder; consumer ChatGPT terms cover personal,
non-programmatic use.</td></tr>
<tr><td>Anthropic</td><td class="ok-cell">Permitted — API keys via console</td>
<td>Not permitted for third-party resale relay</td><td>Commercial terms
distinguish API service from consumer Claude apps.</td></tr>
<tr><td>Google (Gemini)</td><td class="ok-cell">Permitted — AI Studio /
Vertex keys</td><td>Not permitted for third-party resale relay</td>
<td>Consumer plans and Cloud API are separate products with separate
terms.</td></tr>
<tr><td>Open-weight hosts (Together, Fireworks, self-hosted vLLM…)</td>
<td class="ok-cell">Permitted — standard API keys or your own hardware</td>
<td>n/a</td><td>Cleanest path for cost-sensitive routing tiers.</td></tr>
</table>
<p class="dim">Any access mode not covered by a provider\u2019s official
program is treated as UNVERIFIED here: it is not demonstrated on this site,
not documented as a tutorial, and not enabled in the demo.</p>

<h2>About this site</h2>
<ul>
<li>The <a href="../demo/">demo</a> runs against a <strong>mock upstream
only</strong>: fake accounts, fake balances, fake logs. No real provider
account is connected anywhere on this host.</li>
<li>This site is an independent deployment demonstration. It is not
affiliated with, endorsed by, or connected to the Sub2API project or any
upstream AI provider. Provider names appear for interoperability description
only; no logos are used.</li>
<li>Open-source gateway software licences are honoured in deployments —
including source availability and modification notices for
LGPL-3.0-or-later components. Licence texts ship with every delivery.</li>
</ul>
"""

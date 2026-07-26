"""Demo page body."""

DEMO_TITLE = "Live Demo — Mock Gateway Console"
DEMO_DESC = ("Read-only demonstration console of a self-hosted AI gateway: "
             "synthetic accounts, keys, request logs and a failover replay.")
DEMO_BODY = """
<h1>Demo Console</h1>
<div class="notice"><strong>Everything below is synthetic.</strong> The
upstreams are mocks, the accounts and balances are fake, the request log is
generated data. No real provider account is connected to this site. State
resets automatically every 15 minutes. Writes only touch the throwaway
in-browser copy.</div>

<div class="demo-toolbar">
  <span class="stat">demo state: <span id="d-age">fresh</span></span>
  <button class="btn ghost" id="d-reset" type="button">Reset demo state</button>
  <button class="btn ghost" id="d-replay" type="button">Replay failover incident</button>
</div>

<h2>Upstream health</h2>
<div id="d-upstreams" class="grid c3"></div>

<h2>Virtual keys</h2>
<p class="dim">Create and revoke to see the audit trail update. Keys are
shown once, then only as a prefix — same policy as production.</p>
<p><button class="btn" id="d-newkey" type="button">+ Create virtual key</button></p>
<div class="scroll-x"><table id="d-keys"></table></div>

<h2>Request log (redacted, as in production)</h2>
<div class="scroll-x"><table id="d-log"></table></div>

<h2>Audit trail</h2>
<div class="scroll-x"><table id="d-audit"></table></div>

<script src="../static/js/demo.js" defer></script>
"""

/* Mock gateway console — fully client-side, deterministic, synthetic.
 * No network calls. localStorage only. Auto-reset every 15 minutes. */
"use strict";

const RESET_MS = 15 * 60 * 1000;
const LS = "agl-demo-v1";

/* deterministic PRNG so every visitor sees the same "fresh" state */
function mulberry32(a) {
  return function () {
    a |= 0; a = (a + 0x6D2B79F5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

const MODELS = ["gpt-class-large", "gpt-class-small", "claude-class", "gemini-class", "oss-70b"];
const TEAMS = ["search-team", "support-bot", "analytics", "internal-tools"];

function freshState() {
  const rnd = mulberry32(20260726);
  const now = Date.now();
  const upstreams = [
    { name: "mock-upstream-a", cls: "premium", healthy: true, p95: 820, load: 0.42 },
    { name: "mock-upstream-b", cls: "premium", healthy: true, p95: 1040, load: 0.31 },
    { name: "mock-upstream-c", cls: "budget", healthy: true, p95: 460, load: 0.58 },
  ];
  const keys = TEAMS.map((t, i) => ({
    prefix: "vk-" + ["a1f3", "9c2e", "d47b", "5e90"][i],
    team: t,
    models: i < 2 ? ["gpt-class-large", "claude-class"] : ["gpt-class-small", "oss-70b"],
    budget: [200, 150, 80, 40][i],
    spent: +([87.14, 63.02, 22.55, 9.4][i]),
    rpm: [60, 120, 30, 30][i],
    revoked: false,
  }));
  const log = [];
  for (let i = 0; i < 24; i++) {
    const k = keys[Math.floor(rnd() * keys.length)];
    const up = upstreams[Math.floor(rnd() * 2)];
    log.push({
      t: now - (24 - i) * 90000 - Math.floor(rnd() * 60000),
      key: k.prefix + "-****",
      model: k.models[Math.floor(rnd() * k.models.length)],
      upstream: up.name,
      tokens: 200 + Math.floor(rnd() * 3800),
      ms: 300 + Math.floor(rnd() * 2200),
      status: rnd() < 0.94 ? 200 : 429,
    });
  }
  return {
    created: now,
    upstreams, keys, log,
    audit: [
      { t: now - 86400000 * 3, ev: "config.update", detail: "routing: premium pool = upstream-a,upstream-b" },
      { t: now - 86400000, ev: "key.create", detail: "vk-5e90 (internal-tools, budget $40)" },
    ],
  };
}

let S;
function load() {
  try {
    const raw = localStorage.getItem(LS);
    if (raw) {
      const s = JSON.parse(raw);
      if (Date.now() - s.created < RESET_MS) { S = s; return; }
    }
  } catch (e) { /* corrupted -> reset */ }
  S = freshState();
  save();
}
function save() { try { localStorage.setItem(LS, JSON.stringify(S)); } catch (e) {} }

const $ = (id) => document.getElementById(id);
const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const fmtT = (t) => new Date(t).toISOString().slice(11, 19) + "Z";

function render() {
  const age = Math.floor((Date.now() - S.created) / 60000);
  $("d-age").textContent = age < 1 ? "fresh" : age + " min old (resets at 15)";

  $("d-upstreams").innerHTML = S.upstreams.map((u) => `
    <div class="card glass">
      <h3>${esc(u.name)} <span class="tag ${u.healthy ? "ok" : "fail"}">${u.healthy ? "healthy" : "FAIL"}</span></h3>
      <p class="dim">class: ${esc(u.cls)} · p95 ${u.p95}ms</p>
      <p>load <span class="bar"><i class="${u.load > 0.8 ? "hot" : ""}" data-load="${Math.round(u.load * 100)}"></i></span> ${Math.round(u.load * 100)}%</p>
    </div>`).join("");
  // CSP style-src 'self' forbids inline style attributes; set widths via CSSOM
  $("d-upstreams").querySelectorAll("i[data-load]").forEach((el) => {
    el.style.width = el.dataset.load + "%";
  });

  $("d-keys").innerHTML =
    "<tr><th>key</th><th>team</th><th>models</th><th>spent / limit</th><th>rpm cap</th><th>status</th><th>actions</th></tr>" +
    S.keys.map((k, i) => `
      <tr>
        <td><code>${esc(k.prefix)}-****</code></td>
        <td>${esc(k.team)}</td>
        <td class="dim">${k.models.map(esc).join(", ")}</td>
        <td>$${k.spent.toFixed(2)} / $${k.budget}</td>
        <td>${k.rpm}</td>
        <td>${k.revoked ? '<span class="tag fail">revoked</span>' : '<span class="tag ok">active</span>'}</td>
        <td>${k.revoked ? "" : `<button class="btn ghost" data-revoke="${i}" type="button">revoke</button>`}</td>
      </tr>`).join("");

  $("d-log").innerHTML =
    "<tr><th>time</th><th>key</th><th>model</th><th>upstream</th><th>tokens</th><th>latency</th><th>status</th></tr>" +
    S.log.slice().sort((a, b) => b.t - a.t).slice(0, 14).map((r) => `
      <tr><td class="dim">${fmtT(r.t)}</td><td><code>${esc(r.key)}</code></td>
      <td>${esc(r.model)}</td><td class="dim">${esc(r.upstream)}</td>
      <td>${r.tokens}</td><td>${r.ms}ms</td>
      <td><span class="tag ${r.status === 200 ? "ok" : "warn"}">${r.status}</span></td></tr>`).join("");

  $("d-audit").innerHTML =
    "<tr><th>time</th><th>event</th><th>detail</th></tr>" +
    S.audit.slice().sort((a, b) => b.t - a.t).slice(0, 10).map((a) => `
      <tr><td class="dim">${new Date(a.t).toISOString().slice(0, 19)}Z</td>
      <td><code>${esc(a.ev)}</code></td><td class="dim">${esc(a.detail)}</td></tr>`).join("");
}

function audit(ev, detail) { S.audit.push({ t: Date.now(), ev, detail }); }

document.addEventListener("click", (e) => {
  const b = e.target.closest("button");
  if (!b) return;

  if (b.id === "d-reset") { S = freshState(); audit("demo.reset", "manual reset"); save(); render(); }

  if (b.id === "d-newkey") {
    const prefix = "vk-" + Math.random().toString(16).slice(2, 6);
    const full = prefix + "-" + Math.random().toString(16).slice(2, 14);
    S.keys.push({ prefix, team: "new-team", models: ["gpt-class-small"], budget: 25, spent: 0, rpm: 30, revoked: false });
    audit("key.create", prefix + " (new-team, budget $25)");
    save(); render();
    alert("Virtual key created (shown ONCE, as in production):\n\n" + full +
          "\n\nAfter this dialog it appears only as " + prefix + "-****");
  }

  if (b.dataset.revoke !== undefined) {
    const k = S.keys[+b.dataset.revoke];
    k.revoked = true;
    audit("key.revoke", k.prefix + " (" + k.team + ") — requests now fail closed");
    save(); render();
  }

  if (b.id === "d-replay") replayIncident();
});

function replayIncident() {
  const a = S.upstreams[0];
  a.healthy = false; a.load = 0.05;
  S.upstreams[1].load = 0.86;
  audit("health.fail", a.name + " error rate 31% > threshold 5% — marked unhealthy");
  audit("route.failover", "premium traffic retrying on mock-upstream-b");
  const now = Date.now();
  for (let i = 0; i < 4; i++) {
    S.log.push({ t: now - (3 - i) * 800, key: "vk-a1f3-****", model: "gpt-class-large",
      upstream: "mock-upstream-b", tokens: 900 + i * 137, ms: 1400 + i * 90, status: 200 });
  }
  save(); render();
  setTimeout(() => {
    a.healthy = true; a.load = 0.35; S.upstreams[1].load = 0.44;
    audit("health.recover", a.name + " passed 2 consecutive checks — back in rotation");
    save(); render();
  }, 6000);
}

load(); render();
setInterval(() => { load(); render(); }, 30000);

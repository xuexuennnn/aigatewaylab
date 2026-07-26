# AI Gateway Lab — showcase site

Static demonstration site for **self-hosted AI API gateway deployment and
operations** work: architecture, deployment docs, security practices, a
synthetic case study, and a fully client-side mock admin console.

Live at [aigatewaylab.xyz](https://aigatewaylab.xyz) — English and
[中文](https://aigatewaylab.xyz/zh/) trees, light/dark/system themes with three
switchable background styles (frost / graphite / midnight). Or run it locally
in under a minute.

Related: [ai-gateway-deployment-showcase](https://github.com/xuexuennnn/ai-gateway-deployment-showcase)
— public architecture/safety-design showcase with a runnable mock-deployment demo.

Contact: <hello@aigatewaylab.xyz>

> Independent deployment demonstration. Not affiliated with the Sub2API
> project or any upstream AI provider. All demo data is synthetic.

## What's here

| Path | What it is |
|---|---|
| `build/` | Zero-dependency Python static site generator + verification scripts |
| `site/` | Generated static site (7 pages, no frameworks, no CDN) |
| `deploy/CLIENT_CHECKLIST.md` | The checklist I use for real client deployments |

## Run locally

```sh
python3 build/build.py                 # regenerate site/ from page modules
cd site && python3 -m http.server 8899 # serve at http://127.0.0.1:8899
```

No dependencies. Python 3.10+.

## Verification

Three layers, all reproducible:

```sh
python3 build/verify.py          # links, disclaimer presence, banned-claims scan
```

Browser tests (requires Playwright + Chromium, ~800 MB):

```sh
python3 -m venv .venv-test
.venv-test/bin/pip install playwright pillow
.venv-test/bin/playwright install chromium --with-deps
.venv-test/bin/python build/browser_test.py
```

`browser_test.py` exercises all 7 pages at 4 viewports (1440×900, 1920×1080,
390×844, 412×915): console errors, layout overflow, meta/canonical/OG tags,
keyboard navigation, and the demo console's create/revoke/reset lifecycle
against real `localStorage`.

Lighthouse (via `npx lighthouse`) is run against every page; scores from the
last full run are recorded in the repository's evidence notes.

## The demo console

`site/static/js/demo.js` — deliberately boring engineering:

- **Zero backend.** Pure client-side JS; state lives in `localStorage` only.
- **Deterministic.** A seeded PRNG generates the same synthetic upstreams,
  virtual keys and request log for every visitor.
- **Self-resetting.** State older than 15 minutes is discarded on load.
- **Nothing real.** Mock upstream names, fake balances, redacted fake keys.
  There is no network call anywhere in the file.

## Design constraints

- No JS/CSS frameworks, no external requests — CSP-friendly by construction
- Single hand-written stylesheet; light/dark/system themes + three background
  surfaces, persisted in `localStorage`; responsive via one breakpoint plus
  scrollable tables
- Every page carries the independence disclaimer and a synthetic-data notice

## License

- Site content and code: MIT (see `LICENSE`)
- The gateways discussed (LiteLLM, one-api, Sub2API and similar) belong to
  their respective projects under their own licenses. This repository contains
  none of their code.

## Limitations

- The demo console simulates gateway behaviour; it is not a gateway. Real
  deployments are done per client on their infrastructure.
- Lighthouse scores were measured on the static site served locally; scores
  behind a real proxy depend on that proxy's headers and TLS setup.

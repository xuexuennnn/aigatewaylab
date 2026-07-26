#!/usr/bin/env python3
"""Browser verification of the gateway showcase site.

Tests all 7 pages x 4 viewports with real Chromium:
- console errors / page errors / failed requests
- horizontal overflow (scrollWidth vs clientWidth)
- nav links present and clickable
- title / meta description / canonical / og tags
- keyboard navigation (tab reaches nav + primary CTA)
- demo interactions: create key, revoke key, localStorage, reset
Saves screenshots to browser-test/shots/ and a JSON report.
"""
import json, os, sys, time
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8899"
PAGES_EN = ["/", "/architecture/", "/demo/", "/docs/", "/security/", "/case-study/", "/compliance/"]
PAGES = PAGES_EN + ["/zh" + p for p in PAGES_EN]
VIEWPORTS = [
    ("desktop-1440x900", 1440, 900),
    ("tablet-768x1024", 768, 1024),
    ("mobile-390x844", 390, 844),
    ("mobile-360x800", 360, 800),
]
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "browser-test")
SHOTS = os.path.join(OUT, "shots")
os.makedirs(SHOTS, exist_ok=True)

report = {"pages": {}, "demo": {}, "issues": []}

def issue(msg):
    report["issues"].append(msg)
    print("ISSUE:", msg)

with sync_playwright() as pw:
    browser = pw.chromium.launch()
    for vname, w, h in VIEWPORTS:
        is_mobile = w < 500
        ctx = browser.new_context(
            viewport={"width": w, "height": h},
            is_mobile=is_mobile, has_touch=is_mobile,
            device_scale_factor=2 if is_mobile else 1,
        )
        for path in PAGES:
            slug = path.strip("/").replace("/", "_") or "home"
            key = f"{slug}@{vname}"
            errors, failed = [], []
            page = ctx.new_page()
            page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
            page.on("pageerror", lambda e: errors.append(str(e)))
            page.on("requestfailed", lambda r: failed.append(r.url))
            page.goto(BASE + path, wait_until="networkidle")
            time.sleep(0.2)

            # overflow check (elements inside horizontally-scrollable ancestors are fine)
            ov = page.evaluate("""() => {
                const d = document.documentElement;
                const bad = [];
                if (d.scrollWidth > d.clientWidth + 1) bad.push('document ' + d.scrollWidth + '>' + d.clientWidth);
                const inScroller = (el) => {
                    for (let p = el; p && p !== document.body; p = p.parentElement) {
                        const o = getComputedStyle(p).overflowX;
                        if (o === 'auto' || o === 'scroll') return true;
                    }
                    return false;
                };
                for (const el of document.querySelectorAll('main *')) {
                    const r = el.getBoundingClientRect();
                    if (r.right > d.clientWidth + 2 && r.width > 24 && !inScroller(el))
                        bad.push(el.tagName + '.' + (el.className||'') + ' right=' + Math.round(r.right));
                }
                return bad.slice(0, 8);
            }""")
            meta = page.evaluate("""() => ({
                title: document.title,
                desc: document.querySelector('meta[name=description]')?.content || '',
                canonical: document.querySelector('link[rel=canonical]')?.href || '',
                og: document.querySelector('meta[property="og:title"]')?.content || '',
                navLinks: [...document.querySelectorAll('nav a.nl')].length,
                h1: document.querySelectorAll('h1').length,
                lang: document.documentElement.lang,
            })""")
            page.screenshot(path=os.path.join(SHOTS, f"{key}.png"), full_page=True)
            rec = {"errors": errors, "failed_requests": failed, "overflow": ov, **meta}
            report["pages"][key] = rec
            if errors: issue(f"{key}: console errors {errors[:2]}")
            if failed: issue(f"{key}: failed requests {failed[:2]}")
            if ov: issue(f"{key}: overflow {ov[:3]}")
            if not meta["desc"]: issue(f"{key}: missing meta description")
            if not meta["canonical"]: issue(f"{key}: missing canonical")
            if meta["navLinks"] != 8: issue(f"{key}: nav has {meta['navLinks']} links, expected 8 (7 nav + lang)")
            if meta["h1"] != 1: issue(f"{key}: {meta['h1']} h1 elements")
            page.close()
        ctx.close()

    # ---- demo interaction test (desktop) ----
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    derr = []
    page.on("pageerror", lambda e: derr.append(str(e)))
    page.on("console", lambda m: derr.append(m.text) if m.type == "error" else None)
    page.on("dialog", lambda dlg: dlg.accept())
    page.goto(BASE + "/demo/", wait_until="networkidle")
    d = report["demo"]
    d["initial_keys"] = page.locator("#d-keys tr").count() - 1  # minus header
    d["initial_log_rows"] = page.locator("#d-log tr").count() - 1
    d["ls_before"] = page.evaluate("() => !!localStorage.getItem('agl-demo-v1')")

    # create a key
    create_btn = page.locator("#d-newkey")
    if create_btn.count():
        create_btn.click()
        time.sleep(0.3)
        d["keys_after_create"] = page.locator("#d-keys tr").count() - 1
        if d["keys_after_create"] != d["initial_keys"] + 1:
            issue(f"demo: create key {d['initial_keys']} -> {d['keys_after_create']}, expected +1")
    else:
        d["keys_after_create"] = None
        issue("demo: no #d-newkey button found")

    # revoke first key
    rev = page.locator("#d-keys button[data-revoke]").first
    if rev.count():
        rev.click()
        time.sleep(0.3)
        d["revoked_marker"] = page.locator("#d-keys .tag.fail").count()
        if not d["revoked_marker"]:
            issue("demo: revoke click produced no revoked tag")
    else:
        d["revoked_marker"] = None
        issue("demo: no revoke button found")

    # state persists in localStorage
    d["ls_after"] = page.evaluate("() => JSON.parse(localStorage.getItem('agl-demo-v1')).keys.length")

    # reset: age the state beyond 15min and reload
    page.evaluate("""() => {
        const s = JSON.parse(localStorage.getItem('agl-demo-v1'));
        s.created = Date.now() - 16*60*1000;
        localStorage.setItem('agl-demo-v1', JSON.stringify(s));
    }""")
    page.reload(wait_until="networkidle")
    time.sleep(0.3)
    d["keys_after_reset"] = page.locator("#d-keys tr").count() - 1
    d["demo_errors"] = derr
    if derr: issue(f"demo: JS errors {derr[:2]}")
    if d["initial_keys"] and d["keys_after_reset"] != d["initial_keys"]:
        issue(f"demo: reset gave {d['keys_after_reset']} keys, initial was {d['initial_keys']}")
    page.screenshot(path=os.path.join(SHOTS, "demo-after-interactions.png"), full_page=True)

    # keyboard navigation on home
    page.goto(BASE + "/", wait_until="networkidle")
    focus_chain = []
    for _ in range(16):
        page.keyboard.press("Tab")
        fi = page.evaluate("() => { const a=document.activeElement; return a ? (a.tagName + '|' + (a.textContent||'').trim().slice(0,25)) : 'none'; }")
        focus_chain.append(fi)
    report["keyboard_focus_chain"] = focus_chain
    if not any("Contact" in f or "联系" in f for f in focus_chain):
        issue("keyboard: primary CTA not reachable in 16 tabs")
    ctx.close()

    # ---- theme system tests ----
    th = report["theme"] = {}
    ctx = browser.new_context(viewport={"width": 1440, "height": 900},
                              color_scheme="dark")
    page = ctx.new_page()
    terr = []
    page.on("pageerror", lambda e: terr.append(str(e)))
    page.on("console", lambda m: terr.append(m.text) if m.type == "error" else None)
    page.goto(BASE + "/", wait_until="networkidle")
    th["system_dark_resolved"] = page.evaluate(
        "() => getComputedStyle(document.documentElement).getPropertyValue('color-scheme').trim()")
    # cycle: system -> light -> dark
    page.locator("#theme-mode").click()
    th["after_1_click"] = page.evaluate("() => document.documentElement.getAttribute('data-theme')")
    page.locator("#theme-mode").click()
    th["after_2_clicks"] = page.evaluate("() => document.documentElement.getAttribute('data-theme')")
    # persistence across reload + across pages
    page.reload(wait_until="networkidle")
    th["persist_reload"] = page.evaluate("() => document.documentElement.getAttribute('data-theme')")
    page.goto(BASE + "/zh/docs/", wait_until="networkidle")
    th["persist_crosspage"] = page.evaluate("() => document.documentElement.getAttribute('data-theme')")
    # surface select
    page.select_option("#theme-surface", "midnight")
    th["surface_set"] = page.evaluate("() => document.documentElement.getAttribute('data-surface')")
    page.reload(wait_until="networkidle")
    th["surface_persist"] = page.evaluate("() => document.documentElement.getAttribute('data-surface')")
    for name, want in [("after_1_click", "light"), ("after_2_clicks", "dark"),
                       ("persist_reload", "dark"), ("persist_crosspage", "dark"),
                       ("surface_set", "midnight"), ("surface_persist", "midnight")]:
        if th[name] != want:
            issue(f"theme: {name} = {th[name]!r}, expected {want!r}")
    if terr: issue(f"theme: JS errors {terr[:2]}")
    # contrast smoke: body text vs background in both forced themes
    for forced in ("light", "dark"):
        page.evaluate(f"() => document.documentElement.setAttribute('data-theme', '{forced}')")
        cr = page.evaluate("""() => {
            const cs = getComputedStyle(document.body);
            const parse = (s) => s.match(/[\d.]+/g).slice(0,3).map(Number);
            const lum = ([r,g,b]) => {
                const f = (c) => { c/=255; return c<=0.03928 ? c/12.92 : Math.pow((c+0.055)/1.055, 2.4); };
                return 0.2126*f(r)+0.7152*f(g)+0.0722*f(b);
            };
            const t = lum(parse(cs.color));
            const bgc = cs.backgroundColor === 'rgba(0, 0, 0, 0)'
                ? getComputedStyle(document.documentElement).backgroundColor : cs.backgroundColor;
            const b = lum(parse(bgc));
            return (Math.max(t,b)+0.05)/(Math.min(t,b)+0.05);
        }""")
        th[f"contrast_{forced}"] = round(cr, 2)
        if cr < 7: issue(f"theme: body contrast in {forced} = {cr:.2f}, want >= 7")
    ctx.close()

    # ---- prefers-reduced-motion: no transitions ----
    ctx = browser.new_context(viewport={"width": 1440, "height": 900},
                              reduced_motion="reduce")
    page = ctx.new_page()
    page.goto(BASE + "/", wait_until="networkidle")
    rm = page.evaluate("""() => {
        const els = [document.querySelector('nav'), document.querySelector('.btn'), document.querySelector('.card')];
        return els.filter(Boolean).map(el => getComputedStyle(el).transitionDuration).join(',');
    }""")
    report["reduced_motion_durations"] = rm
    if any(v and v not in ("0s", "") for v in rm.split(",")):
        issue(f"reduced-motion: transition durations still {rm}")
    ctx.close()

    # ---- no-JS fallback ----
    ctx = browser.new_context(viewport={"width": 1440, "height": 900}, java_script_enabled=False)
    page = ctx.new_page()
    page.goto(BASE + "/zh/", wait_until="networkidle")
    njs = page.evaluate if False else None
    body_visible = page.locator("main h1").is_visible()
    controls_hidden = page.locator(".theme-cluster").is_visible()
    report["nojs"] = {"content_visible": body_visible, "theme_controls_visible": controls_hidden}
    if not body_visible: issue("no-js: main content not visible")
    if controls_hidden: issue("no-js: theme controls visible but non-functional (should be hidden)")
    ctx.close()
    browser.close()

with open(os.path.join(OUT, "report.json"), "w") as f:
    json.dump(report, f, indent=2)
print(f"\npages tested: {len(report['pages'])}, issues: {len(report['issues'])}")
print("VERDICT:", "PASS" if not report["issues"] else "FAIL")
sys.exit(1 if report["issues"] else 0)

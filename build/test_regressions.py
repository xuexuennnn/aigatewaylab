#!/usr/bin/env python3
"""Focused regression tests for the public showcase UX."""
import os
import time
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8899"


def request_log_times(page):
    return page.locator("#d-log tr td:first-child").all_inner_texts()


def parse_clock(value):
    hh, mm, ss = value.removesuffix("Z").split(":")
    return int(hh) * 3600 + int(mm) * 60 + int(ss)


failures = []
with sync_playwright() as pw:
    browser = pw.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.on("dialog", lambda dialog: dialog.accept())

    page.goto(BASE + "/demo/", wait_until="networkidle")
    page.evaluate("localStorage.removeItem('agl-demo-v1')")
    page.reload(wait_until="networkidle")

    # Fresh synthetic state must never contain future request timestamps.
    fresh_state = page.evaluate("JSON.parse(localStorage.getItem('agl-demo-v1'))")
    now_ms = page.evaluate("Date.now()")
    future_fresh = [row["t"] for row in fresh_state["log"] if row["t"] > now_ms]
    if future_fresh:
        failures.append(f"fresh demo contains future request timestamps: {future_fresh[:4]}")

    # Rendering must sort persisted audit data by its timestamp, not insertion order.
    page.evaluate("""() => {
        const state = JSON.parse(localStorage.getItem('agl-demo-v1'));
        const now = Date.now();
        state.audit = [
            {t: now - 1000, ev: 'audit.newest', detail: 'newest'},
            {t: now - 3000, ev: 'audit.oldest', detail: 'oldest'},
            {t: now - 2000, ev: 'audit.middle', detail: 'middle'}
        ];
        localStorage.setItem('agl-demo-v1', JSON.stringify(state));
    }""")
    page.reload(wait_until="networkidle")
    audit_events = page.locator("#d-audit tr td:nth-child(2)").all_inner_texts()
    if audit_events != ["audit.newest", "audit.middle", "audit.oldest"]:
        failures.append(f"audit trail is not newest-first: {audit_events}")

    page.locator("#d-replay").click()
    time.sleep(0.2)

    replay_state = page.evaluate("JSON.parse(localStorage.getItem('agl-demo-v1'))")
    replay_now_ms = page.evaluate("Date.now()")
    future_replay = [row["t"] for row in replay_state["log"] if row["t"] > replay_now_ms]
    if future_replay:
        failures.append(f"failover replay contains future request timestamps: {future_replay[:4]}")

    times = request_log_times(page)
    numeric = [parse_clock(value) for value in times]
    if numeric != sorted(numeric, reverse=True):
        failures.append(f"demo request log is not newest-first: {times[:8]}")

    action_header = page.locator("#d-keys th").last.inner_text().strip()
    if action_header != "actions":
        failures.append(f"virtual-key action header is {action_header!r}, expected 'actions'")

    budget_header = page.locator("#d-keys th").nth(3).inner_text().strip()
    if budget_header != "spent / limit":
        failures.append(f"budget header is {budget_header!r}, expected 'spent / limit'")

    for path in ("/", "/zh/"):
        page.goto(BASE + path, wait_until="networkidle")
        if page.locator("main .final-cta").count() != 1:
            failures.append(f"{path}: missing final CTA")
        if page.locator("main .case-proof").count() != 1:
            failures.append(f"{path}: missing case proof section")

    browser.close()

if failures:
    print("FAIL")
    for failure in failures:
        print(" -", failure)
    raise SystemExit(1)
print("PASS: focused UX regressions")

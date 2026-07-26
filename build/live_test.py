
import sys
from playwright.sync_api import sync_playwright

BASE = "https://aigatewaylab.xyz"
PAGES = ["/", "/architecture/", "/demo/", "/docs/", "/security/", "/case-study/", "/compliance/"]
VIEWPORTS = [("desktop-1440", 1440, 900), ("mobile-390", 390, 844)]

issues = []
with sync_playwright() as pw:
    b = pw.chromium.launch()
    for vname, w, h in VIEWPORTS:
        ctx = b.new_context(viewport={"width": w, "height": h})
        page = ctx.new_page()
        errors = []
        page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.on("dialog", lambda d: d.accept())
        for p in PAGES:
            r = page.goto(BASE + p, wait_until="networkidle", timeout=30000)
            if r.status != 200:
                issues.append(f"{vname}{p}: HTTP {r.status}")
            ov = page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
            if ov > 1:
                issues.append(f"{vname}{p}: hscroll overflow {ov}px")
        if errors:
            issues.append(f"{vname}: console errors: {errors[:3]}")
        # demo interaction on live site (desktop only)
        if vname == "desktop-1440":
            page.goto(BASE + "/demo/", wait_until="networkidle")
            before = page.locator("#d-keys tr").count()
            page.click("#d-newkey")
            page.wait_for_timeout(300)
            after = page.locator("#d-keys tr").count()
            if after != before + 1:
                issues.append(f"demo create: rows {before}->{after}")
            # revoke first key
            page.locator("#d-keys button").first.click()
            page.wait_for_timeout(300)
            if page.locator("#d-keys .tag-revoked, #d-keys .revoked").count() == 0 and "revoked" not in page.locator("#d-keys").inner_text().lower():
                issues.append("demo revoke: no revoked marker")
            # reset via localStorage TTL manipulation
            page.evaluate("const d=JSON.parse(localStorage['agl-demo-v1']); d.created=Date.now()-16*60*1000; localStorage['agl-demo-v1']=JSON.stringify(d);")
            page.reload(wait_until="networkidle")
            reset_rows = page.locator("#d-keys tr").count()
            print(f"demo: create {before}->{after}, post-reset rows={reset_rows}")
        ctx.close()
    b.close()

print("issues:", len(issues))
for i in issues: print(" -", i)
sys.exit(1 if issues else 0)

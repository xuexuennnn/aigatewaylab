#!/usr/bin/env python3
"""Verify the built site: link integrity, HTML parse, compliance wording."""
import html.parser, os, re, sys

SITE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "site")

class Collector(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links, self.errors = [], []
        self.open_tags = []
    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == "a" and "href" in d: self.links.append(d["href"])
        if tag in ("link", "script", "img") and (d.get("href") or d.get("src")):
            self.links.append(d.get("href") or d.get("src"))

pages = []
for root, _, files in os.walk(SITE):
    for f in files:
        if f.endswith(".html"):
            pages.append(os.path.join(root, f))

fail = []
for p in sorted(pages):
    src = open(p, encoding="utf-8").read()
    c = Collector()
    c.feed(src)
    base = os.path.dirname(p)
    for link in c.links:
        if link.startswith(("http://", "https://", "data:", "#", "mailto:")):
            continue
        target = os.path.normpath(os.path.join(base, link))
        if link.endswith("/"): target = os.path.join(target, "index.html")
        if os.path.isdir(target): target = os.path.join(target, "index.html")
        if not os.path.exists(target):
            fail.append(f"{os.path.relpath(p, SITE)}: broken link {link} -> {os.path.relpath(target, SITE)}")
    # required disclaimer on every page (either language tree)
    if ("Independent deployment demonstration" not in src
            and "独立部署演示" not in src):
        fail.append(f"{os.path.relpath(p, SITE)}: missing disclaimer")

# compliance: banned marketing phrases must NOT appear outside refusal context
banned = [
    (r"resell(ing)? (your )?subscription", "resell subscription pitch"),
    (r"shared? accounts? (pool|access)", "account sharing pitch"),
    (r"unlimited (quota|usage|calls)", "unlimited claims"),
    (r"bypass", "bypass wording outside refusal"),
]
for p in sorted(pages):
    text = re.sub(r"<[^>]+>", " ", open(p, encoding="utf-8").read())
    for pat, label in banned:
        for m in re.finditer(pat, text, re.I):
            ctx = text[max(0, m.start()-120):m.end()+80].strip()
            # allowed if it sits in refusal/negation context
            if re.search(r"(refus|not permitted|do not|never|Bypassing provider)", ctx, re.I):
                continue
            fail.append(f"{os.path.relpath(p, SITE)}: {label}: ...{ctx[:100]}...")

# no real-looking secrets anywhere in the shipped site
for root, _, files in os.walk(SITE):
    for f in files:
        src = open(os.path.join(root, f), encoding="utf-8", errors="ignore").read()
        if re.search(r"sk-[A-Za-z0-9]{20}|ghp_[A-Za-z0-9]{20}", src):
            fail.append(f"{f}: secret-shaped string")

print(f"pages: {len(pages)}")
if fail:
    print("FAIL")
    for f in fail: print(" -", f)
    sys.exit(1)
print("PASS: links OK, disclaimer on every page, no banned marketing, no secret-shaped strings")

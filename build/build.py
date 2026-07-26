#!/usr/bin/env python3
"""Build the static site into site/ — EN tree at /, ZH tree at /zh/."""

import os, sys, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from template import page
import pages_home, pages_docs, pages_case, pages_demo, pages_zh

# CJK-aware unwrap: a newline between two CJK chars (or CJK punctuation)
# renders as an unwanted space in browsers. Strip it; keep newlines inside
# <pre>/<code> blocks untouched.
_CJK = r"[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]"
def _unwrap_cjk(html_src: str) -> str:
    parts = re.split(r"(<pre>.*?</pre>|<code>.*?</code>)", html_src, flags=re.S)
    out = []
    for i, part in enumerate(parts):
        if i % 2 == 0:
            prev = None
            while prev != part:
                prev = part
                part = re.sub(rf"({_CJK}(?:</[a-z]+>|<[a-z][^>]*>)*)\n\s*((?:<[a-z][^>]*>|</[a-z]+>)*{_CJK})", r"\1\2", part)
        out.append(part)
    return "".join(out)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "site")

PAGES_EN = [
    ("index.html",              pages_home.HOME_TITLE, pages_home.HOME_DESC, pages_home.HOME_BODY, "/", 0),
    ("architecture/index.html", pages_home.ARCH_TITLE, pages_home.ARCH_DESC, pages_home.ARCH_BODY, "/architecture/", 1),
    ("demo/index.html",         pages_demo.DEMO_TITLE, pages_demo.DEMO_DESC, pages_demo.DEMO_BODY, "/demo/", 1),
    ("docs/index.html",         pages_docs.DOCS_TITLE, pages_docs.DOCS_DESC, pages_docs.DOCS_BODY, "/docs/", 1),
    ("security/index.html",     pages_docs.SEC_TITLE,  pages_docs.SEC_DESC,  pages_docs.SEC_BODY,  "/security/", 1),
    ("case-study/index.html",   pages_case.CASE_TITLE, pages_case.CASE_DESC, pages_case.CASE_BODY, "/case-study/", 1),
    ("compliance/index.html",   pages_case.COMP_TITLE, pages_case.COMP_DESC, pages_case.COMP_BODY, "/compliance/", 1),
]

PAGES_ZH = [
    ("zh/index.html",              pages_zh.HOME_TITLE, pages_zh.HOME_DESC, pages_zh.HOME_BODY, "/", 1),
    ("zh/architecture/index.html", pages_zh.ARCH_TITLE, pages_zh.ARCH_DESC, pages_zh.ARCH_BODY, "/architecture/", 2),
    ("zh/demo/index.html",         pages_zh.DEMO_TITLE, pages_zh.DEMO_DESC, pages_zh.DEMO_BODY, "/demo/", 2),
    ("zh/docs/index.html",         pages_zh.DOCS_TITLE, pages_zh.DOCS_DESC, pages_zh.DOCS_BODY, "/docs/", 2),
    ("zh/security/index.html",     pages_zh.SEC_TITLE,  pages_zh.SEC_DESC,  pages_zh.SEC_BODY,  "/security/", 2),
    ("zh/case-study/index.html",   pages_zh.CASE_TITLE, pages_zh.CASE_DESC, pages_zh.CASE_BODY, "/case-study/", 2),
    ("zh/compliance/index.html",   pages_zh.COMP_TITLE, pages_zh.COMP_DESC, pages_zh.COMP_BODY, "/compliance/", 2),
]

def main():
    for path, title, desc, body, active, depth in PAGES_EN:
        full = os.path.join(OUT, path)
        os.makedirs(os.path.dirname(full) or OUT, exist_ok=True)
        with open(full, "w", encoding="utf-8") as f:
            f.write(page(title, desc, body, active, depth, lang="en"))
        print(f"built {path}")
    for path, title, desc, body, active, depth in PAGES_ZH:
        full = os.path.join(OUT, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w", encoding="utf-8") as f:
            f.write(_unwrap_cjk(page(title, desc, body, active, depth, lang="zh")))
        print(f"built {path}")
    # robots + sitemap (both trees)
    with open(os.path.join(OUT, "robots.txt"), "w") as f:
        f.write("User-agent: *\nAllow: /\nSitemap: https://aigatewaylab.xyz/sitemap.xml\n")
    locs = [f"https://aigatewaylab.xyz{a}" for _, _, _, _, a, _ in PAGES_EN]
    locs += [f"https://aigatewaylab.xyz/zh{a}" for _, _, _, _, a, _ in PAGES_ZH]
    urls = "".join(f"<url><loc>{u}</loc></url>" for u in locs)
    with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
        f.write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>')
    print("built robots.txt sitemap.xml (en+zh)")

if __name__ == "__main__":
    main()

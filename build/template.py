"""Static site builder: shared layout, zero dependencies.

Every page is a Python module exporting TITLE, DESC, BODY. This builder wraps
them in the shared shell and writes static HTML. No JS framework, no CDN —
everything self-hosted, CSP-friendly.

i18n: two full static trees. English at /, Simplified Chinese at /zh/.
Same structure, hreflang-linked, language toggle in the nav.
"""

from __future__ import annotations

NAV = {
    "en": [
        ("/", "Home"),
        ("/architecture/", "Architecture"),
        ("/demo/", "Live Demo"),
        ("/docs/", "Deployment Docs"),
        ("/security/", "Security"),
        ("/case-study/", "Case Study"),
        ("/compliance/", "Compliance"),
    ],
    "zh": [
        ("/", "首页"),
        ("/architecture/", "架构"),
        ("/demo/", "在线演示"),
        ("/docs/", "部署文档"),
        ("/security/", "安全"),
        ("/case-study/", "案例研究"),
        ("/compliance/", "合规"),
    ],
}

DISCLAIMER = {
    "en": ("Independent deployment demonstration. Not affiliated with the "
           "Sub2API project or any upstream AI provider."),
    "zh": ("独立部署演示站，与 Sub2API 项目及任何上游 AI 服务商均无隶属或合作关系。"),
}

FOOT_SYNTH = {
    "en": ("Demo data is synthetic. No real provider accounts, credentials, or "
           "traffic are shown anywhere on this site."),
    "zh": ("演示数据均为合成数据。本站任何位置都不展示真实的服务商账号、凭证或流量。"),
}

LANG_LINK = {"en": "中文", "zh": "EN"}
HTML_LANG = {"en": "en", "zh": "zh-Hans"}

BASE_URL = "https://aigatewaylab.xyz"


def page(title: str, desc: str, body: str, active: str, depth: int = 1,
         lang: str = "en") -> str:
    # depth = directory depth of the page file below site/
    root = "../" * depth if depth else "./"
    prefix = "/zh" if lang == "zh" else ""
    canonical = BASE_URL + prefix + active
    en_url = BASE_URL + active
    zh_url = BASE_URL + "/zh" + active

    # tree-rooted relative links: en tree root and zh tree root
    tree_root = root if lang == "en" else root + "zh/"
    other_root = root + "zh/" if lang == "en" else root

    def href(page_path: str, base: str) -> str:
        return base if page_path == "/" else base + page_path.lstrip("/")

    nav_items = "".join(
        f'<a class="nl{" active" if h == active else ""}" '
        f'href="{href(h, tree_root)}">{label}</a>'
        for h, label in NAV[lang]
    )
    # language toggle points at the same page in the other tree
    lang_link = (f'<a class="nl lang" href="{href(active, other_root)}" '
                 f'hreflang="{HTML_LANG["zh" if lang == "en" else "en"]}">{LANG_LINK[lang]}</a>')

    return f"""<!DOCTYPE html>
<html lang="{HTML_LANG[lang]}" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — AI Gateway Lab</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="en" href="{en_url}">
<link rel="alternate" hreflang="zh-Hans" href="{zh_url}">
<link rel="alternate" hreflang="x-default" href="{en_url}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title} — AI Gateway Lab">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="AI Gateway Lab">
<meta name="twitter:card" content="summary">
<link rel="stylesheet" href="{root}static/css/style.css">
<script src="{root}static/js/theme.js"></script>
<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>&#128273;</text></svg>">
</head>
<body>
<a class="skip-link" href="#main">{'Skip to content' if lang == 'en' else '跳到正文'}</a>
<nav><div class="nav-inner">
  <a class="brand" href="{(root or './') if lang == 'en' else root + 'zh/'}">AI<span>Gateway</span>Lab</a>
  {nav_items}
  <div class="theme-cluster">
    {lang_link}
    <button id="theme-mode" class="theme-btn" type="button" aria-label="Theme: system. Activate to switch.">&#9681; system</button>
    <label class="visually-hidden" for="theme-surface">{'Background style' if lang == 'en' else '背景风格'}</label>
    <span class="sel-wrap"><select id="theme-surface" class="theme-sel">
      <option value="frost">frost</option>
      <option value="graphite">graphite</option>
      <option value="midnight">midnight</option>
    </select></span>
  </div>
</div></nav>
<main id="main">
{body}
</main>
<footer><div class="foot-inner">
  <p>{DISCLAIMER[lang]}</p>
  <p>{FOOT_SYNTH[lang]}</p>
  <p>{('Contact: <a href="mailto:hello@aigatewaylab.xyz">hello@aigatewaylab.xyz</a> &middot; <a href="https://github.com/xuexuennnn/ai-gateway-deployment-showcase" rel="noopener">GitHub showcase</a> &middot; <a href="' + root + 'security/">Security</a>') if lang == 'en' else ('联系：<a href="mailto:hello@aigatewaylab.xyz">hello@aigatewaylab.xyz</a> &middot; <a href="https://github.com/xuexuennnn/ai-gateway-deployment-showcase" rel="noopener">GitHub 展示仓库</a> &middot; <a href="' + root + 'zh/security/">安全说明</a>')}</p>
  <p>&copy; 2026 AI Gateway Lab &middot; aigatewaylab.xyz</p>
</div></footer>
<script src="{root}static/js/theme-ui.js"></script>
</body>
</html>"""

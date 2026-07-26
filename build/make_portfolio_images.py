#!/usr/bin/env python3
"""Generate 3 portfolio images (1000x750) from REAL browser screenshots.

Each image is a framed real screenshot of the running site (127.0.0.1:8899,
same HTML that will be deployed) with a caption bar. Nothing in the screenshot
is drawn by hand; the content is what the browser actually rendered.
"""
import os
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "portfolio")
TMP = os.path.join(OUT, "_raw")
os.makedirs(TMP, exist_ok=True)

BASE = "http://127.0.0.1:8899"
W, H = 1000, 750
BG = (13, 17, 23)
BORDER = (48, 54, 61)
ACCENT = (88, 166, 255)
FG = (230, 237, 243)
DIM = (139, 148, 158)
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

SHOTS = [
    # (slug, url, scroll_y, caption_title, caption_sub)
    ("cover", "/", 0,
     "Self-Hosted AI API Gateway",
     "Deployment · Hardening · Operations — aigatewaylab.xyz"),
    ("demo", "/demo/", 590,
     "Mock Admin Console (synthetic data)",
     "Virtual keys, budgets, request log, failover replay"),
    ("arch", "/architecture/", 260,
     "Architecture & Trust Boundaries",
     "One entry point for LLM traffic, keys stay server-side"),
]

def capture():
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        ctx = b.new_context(viewport={"width": 1360, "height": 850},
                            device_scale_factor=2)
        p = ctx.new_page()
        for slug, url, scroll, _, _ in SHOTS:
            p.goto(BASE + url, wait_until="networkidle")
            if scroll:
                p.evaluate(f"window.scrollTo(0, {scroll})")
                p.wait_for_timeout(300)
            p.screenshot(path=os.path.join(TMP, f"{slug}.png"))
        b.close()

def frame(slug, title, sub):
    shot = Image.open(os.path.join(TMP, f"{slug}.png"))
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # caption bar at top
    f_t = ImageFont.truetype(SANS_B, 30)
    f_s = ImageFont.truetype(SANS, 17)
    d.text((40, 36), title, font=f_t, fill=FG)
    d.text((40, 78), sub, font=f_s, fill=DIM)
    d.rectangle([40, 108, 960, 110], fill=ACCENT)

    # screenshot panel
    top = 130
    panel_w, panel_h = W - 80, H - top - 36
    sw, sh = shot.size
    scale = panel_w / sw
    new_h = int(sh * scale)
    shot2 = shot.resize((panel_w, new_h), Image.LANCZOS)
    if new_h > panel_h:
        shot2 = shot2.crop((0, 0, panel_w, panel_h))
    # the raw capture is viewport-cropped, so the bottom edge may slice text;
    # always fade the last 90px into the background deliberately
    vis_h = shot2.size[1]
    fade_h = 160
    fade = Image.new("L", (panel_w, fade_h), 0)
    fd = ImageDraw.Draw(fade)
    for y in range(fade_h):
        fd.line([(0, y), (panel_w, y)], fill=min(255, int(255 * (y / (fade_h * 0.72)) ** 1.5)))
    bgpatch = Image.new("RGB", (panel_w, fade_h), BG)
    shot2.paste(bgpatch, (0, vis_h - fade_h), fade)
    img.paste(shot2, (40, top))
    d.rectangle([39, top - 1, 40 + panel_w, top + vis_h],
                outline=BORDER, width=2)
    # cover the bottom border edge so the fade runs off cleanly
    d.rectangle([36, top + vis_h - 3, 42 + panel_w, top + vis_h + 3], fill=BG)
    out = os.path.join(OUT, f"gateway-{slug}.png")
    img.save(out)
    print("wrote", out, img.size)

if __name__ == "__main__":
    capture()
    for slug, _, _, t, s in SHOTS:
        frame(slug, t, s)

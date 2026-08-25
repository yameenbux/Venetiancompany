#!/usr/bin/env python3
"""Build the favicon set from the client's own marks. Reproducible: run it again
and you get byte-identical output.

    python3 site/scripts/build-icons.py

Two marks, not one, and that is the point. The TVC monogram is a fine ring with
three interlocked letters inside it; rendered at 16px — the size a browser tab
actually uses — the ring closes up and the letters turn to mush. Every candidate
was rasterised at 16 and looked at before this was decided.

So the small sizes carry a simplified mark: a single Newsreader V, reversed out
of the clay tile. It has the mass to survive 16px, the clay block is what makes
the tab recognisable at a glance, and the serif keeps it in the same family as
the site. The V is a traced path, not live text, so the icon carries no font
dependency — same technique as the monogram itself.

  favicon.ico          16 / 32 / 48   V mark
  favicon.svg          any            V mark (browsers render it at tab size)
  apple-touch-icon     180            full monogram — room to breathe
  icon-192, icon-512   192 / 512      full monogram

Rasterising happens at 8x and downsamples with Lanczos, which gives proper
greyscale antialiasing; screenshotting straight at 16px leaves coloured
subpixel fringes on the glyph edges.
"""
import asyncio, base64, io, os, re, sys
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
OUT = os.path.join(SITE, "public")

CLAY, CREAM = "#C96C36", "#FAF6EF"
V_PATH = open(os.path.join(HERE, "icon-v-path.txt")).read().strip()
MONO_PATH = re.search(r'<path d="([^"]+)"',
                      open(os.path.join(SITE, "src/components/Monogram.astro")).read()).group(1)


def v_tile(rounded=True):
    """The V, traced from a 1024 render, fitted to a 512 tile."""
    x0, x1, y0, y1 = 204.0, 820.0, 233.0, 822.0          # traced bbox
    target_h = 512 * 0.56
    k = target_h / (y1 - y0)
    tx = (512 - (x1 - x0) * k) / 2 - x0 * k
    ty = (512 - (y1 - y0) * k) / 2 - y0 * k
    rx = 'rx="92"' if rounded else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">'
            f'<rect width="512" height="512" {rx} fill="{CLAY}"/>'
            f'<g transform="translate({tx:.2f} {ty:.2f}) scale({k:.5f})" fill="{CREAM}">'
            f'<path d="{V_PATH}"/></g></svg>')


def mono_tile(scale=0.76, rounded=False):
    off = (512 - 512 * scale) / 2
    rx = 'rx="92"' if rounded else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">'
            f'<rect width="512" height="512" {rx} fill="{CLAY}"/>'
            f'<g transform="translate({off:.1f} {off:.1f}) scale({scale})" fill="{CREAM}">'
            f'<path d="{MONO_PATH}"/></g></svg>')


async def rasterise(svgs):
    from playwright.async_api import async_playwright
    chrome = os.environ.get("CHROME_PATH") or None
    out = {}
    async with async_playwright() as pw:
        b = await pw.chromium.launch(**({"executable_path": chrome} if chrome else {}))
        for key, (svg, size) in svgs.items():
            big = size * 8
            data = base64.b64encode(svg.encode()).decode()
            p = await b.new_page(viewport={"width": big, "height": big})
            await p.set_content(
                f'<body style="margin:0"><img src="data:image/svg+xml;base64,{data}" '
                f'style="display:block;width:{big}px;height:{big}px">')
            await p.wait_for_timeout(150)
            shot = await p.screenshot(omit_background=True)
            await p.close()
            im = Image.open(io.BytesIO(shot)).convert("RGBA")
            out[key] = im.resize((size, size), Image.LANCZOS)
        await b.close()
    return out


def main():
    jobs = {
        "ico16":  (v_tile(), 16),
        "ico32":  (v_tile(), 32),
        "ico48":  (v_tile(), 48),
        "apple":  (mono_tile(scale=0.76, rounded=False), 180),
        # Full-bleed square, not pre-rounded: Android applies its own mask, and
        # a rounded icon inside a rounded mask gets clipped twice. 0.68 keeps
        # the mark inside the maskable safe zone.
        "i192":   (mono_tile(scale=0.68, rounded=False), 192),
        "i512":   (mono_tile(scale=0.68, rounded=False), 512),
    }
    imgs = asyncio.run(rasterise(jobs))

    # Multi-resolution .ico. Pillow writes every size given into one file, which
    # is what lets a browser pick 16 for the tab and 32 for a bookmark bar.
    ico = os.path.join(OUT, "favicon.ico")
    imgs["ico48"].save(ico, format="ICO",
                       sizes=[(16, 16), (32, 32), (48, 48)],
                       append_images=[imgs["ico16"], imgs["ico32"]])

    imgs["apple"].convert("RGB").save(os.path.join(OUT, "apple-touch-icon.png"), optimize=True)
    imgs["i192"].convert("RGB").save(os.path.join(OUT, "icon-192.png"), optimize=True)
    imgs["i512"].convert("RGB").save(os.path.join(OUT, "icon-512.png"), optimize=True)
    open(os.path.join(OUT, "favicon.svg"), "w").write(v_tile())

    for f in ("favicon.ico", "favicon.svg", "apple-touch-icon.png", "icon-192.png", "icon-512.png"):
        print(f"  {f:24s} {os.path.getsize(os.path.join(OUT, f)) // 1024:>4} KB")


if __name__ == "__main__":
    main()

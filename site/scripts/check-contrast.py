#!/usr/bin/env python3
"""Measure real composited contrast for the hero copy over the slideshow photograph.

The hero sets ink-coloured type over a photograph, so contrast cannot be read
off the tokens — it depends on the pixels behind each glyph after the scrim has
composited. This renders the built page, hides the copy layer, screenshots the
plate, and samples the worst pixel under every text run.

    python3 site/scripts/check-contrast.py [--url http://127.0.0.1:8794/]

Needs the built site served somewhere and Playwright's Chromium. Google Fonts
are fulfilled from a local cache if one is present, otherwise the run falls
back to the metric-matched fallback faces (which shifts the rects slightly, so
prefer the cache when you have it).

Exit status is non-zero if anything fails its threshold.
"""
import argparse, asyncio, io, os, sys
from PIL import Image
from playwright.async_api import async_playwright

# WCAG 2.1: 4.5:1 for body copy, 3:1 for large text (>=24px, or >=18.66px bold).
SMALL, LARGE = 4.5, 3.0
SIZES = [(320, 568), (360, 640), (360, 780), (375, 667), (375, 812), (390, 844),
         (414, 896), (600, 900), (767, 1024), (768, 900), (768, 1024),
         (1024, 800), (1440, 900), (1440, 1200), (1920, 1080)]

def _lin(c):
    c /= 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

def luminance(px):
    return 0.2126 * _lin(px[0]) + 0.7152 * _lin(px[1]) + 0.0722 * _lin(px[2])

def ratio(a, b):
    hi, lo = max(a, b), min(a, b)
    return (hi + 0.05) / (lo + 0.05)

RUNS_JS = """() => {
  const cv=document.createElement('canvas'); cv.width=cv.height=1;
  const cx=cv.getContext('2d',{willReadFrequently:true});
  // Chromium's canvas fillStyle does not accept oklab()/color-mix(), and an
  // invalid assignment is SILENTLY IGNORED — fillStyle keeps its old value. That
  // made every Tailwind opacity-modified colour resolve to black, which is why
  // paper-on-dark copy was reporting 1.00:1. Sentinel-check the assignment and
  // convert oklab by hand when it fails.
  const oklab2srgb=(L,A,B,al)=>{
    const l_=L+0.3963377774*A+0.2158037573*B, m_=L-0.1055613458*A-0.0638541728*B,
          s_=L-0.0894841775*A-1.2914855480*B;
    const l=l_**3, m=m_**3, s=s_**3;
    const lin=[ 4.0767416621*l-3.3077115913*m+0.2309699292*s,
               -1.2684380046*l+2.6097574011*m-0.3413193965*s,
               -0.0041960863*l-0.7034186147*m+1.7076147010*s];
    const g=v=>{v=v<=0.0031308?12.92*v:1.055*Math.pow(Math.max(v,0),1/2.4)-0.055;
                return Math.max(0,Math.min(255,Math.round(v*255)));};
    return [g(lin[0]),g(lin[1]),g(lin[2]),al];
  };
  const res=c=>{
    const m=/^oklab\(\s*([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s*(?:\/\s*([-\d.]+)\s*)?\)$/.exec(c.trim());
    if(m) return oklab2srgb(+m[1],+m[2],+m[3], m[4]===undefined?1:+m[4]);
    cx.fillStyle='#ff00ff'; cx.fillStyle=c;
    if(cx.fillStyle==='#ff00ff' && c.replace(/\s/g,'').toLowerCase()!=='#ff00ff')
      throw new Error('cannot resolve colour: '+c);
    cx.clearRect(0,0,1,1); cx.fillRect(0,0,1,1);
    const d=cx.getImageData(0,0,1,1).data; return [d[0],d[1],d[2],d[3]/255];
  };

  const sec = document.querySelector('section'), out = [];
  sec.querySelectorAll('p.label, h1, a[aria-label]').forEach(el => {
    if (![...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())) return;
    const cs = getComputedStyle(el), r = document.createRange();
    r.selectNodeContents(el);
    for (const rect of r.getClientRects()) {
      if (rect.width < 4 || rect.height < 4) continue;
      out.push({ text: el.textContent.trim().replace(/\\s+/g, ' ').slice(0, 28),
                 rgba: res(cs.color), fs: parseFloat(cs.fontSize), fw: cs.fontWeight,
                 x: Math.round(rect.left), y: Math.round(rect.top),
                 w: Math.round(rect.width), h: Math.round(rect.height) });
    }
  });
  return out;
}"""

async def measure(pw, url, fonts, W, H):
    browser = await pw.chromium.launch(executable_path=os.environ.get("CHROME_PATH") or None)
    ctx = await browser.new_context(viewport={"width": W, "height": H}, device_scale_factor=1)
    if fonts:
        css = open(os.path.join(fonts, "gf.css")).read()
        await ctx.route("https://fonts.googleapis.com/**",
                        lambda r: asyncio.ensure_future(r.fulfill(status=200, content_type="text/css", body=css)))
        async def font(route):
            p = os.path.join(fonts, "gfonts", os.path.basename(route.request.url.split("?")[0]))
            if os.path.exists(p):
                await route.fulfill(status=200, content_type="font/woff2", body=open(p, "rb").read())
            else:
                await route.abort()
        await ctx.route("https://fonts.gstatic.com/**", font)
    page = await ctx.new_page()
    await page.goto(url, wait_until="load")
    await page.evaluate("() => document.fonts.ready")
    await page.evaluate("() => document.querySelector('#slides .slide').decode()")
    await page.wait_for_timeout(800)
    runs = await page.evaluate(RUNS_JS)
    # Hide the copy layer without changing layout, so the runs' coordinates
    # still describe where the text was.
    await page.evaluate("() => { document.querySelector('section > div.relative.z-1').style.visibility = 'hidden'; }")
    await page.wait_for_timeout(150)
    shot = await page.screenshot(clip={"x": 0, "y": 0, "width": W, "height": H})
    await browser.close()

    plate = Image.open(io.BytesIO(shot)).convert("RGB")
    results = []
    for run in runs:
        cr_, cg_, cb_, ca_ = run["rgba"]
        box = (max(0, run["x"]), max(0, run["y"]),
               min(W, run["x"] + run["w"]), min(H, run["y"] + run["h"]))
        if box[2] <= box[0] or box[3] <= box[1]:
            continue
        crop = plate.crop(box)
        crop = crop.resize((max(1, min(crop.width, 160)), max(1, min(crop.height, 70))))
        # get_flattened_data() is Pillow 12+; getdata() is the older name.
        pixels = crop.get_flattened_data() if hasattr(crop, "get_flattened_data") else crop.getdata()
        # Translucent text composites over whatever is behind it, so the
        # foreground has to be resolved per pixel, not once.
        def worst_for(px):
            fg = (cr_ * ca_ + px[0] * (1 - ca_),
                  cg_ * ca_ + px[1] * (1 - ca_),
                  cb_ * ca_ + px[2] * (1 - ca_))
            return ratio(luminance(fg), luminance(px))
        worst = min(worst_for(px) for px in pixels)
        large = run["fs"] >= 24 or (run["fs"] >= 18.66 and int(run["fw"]) >= 700)
        need = LARGE if large else SMALL
        results.append((run["text"], run["fs"], round(worst, 2), need, worst >= need))
    return results

async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", default="http://127.0.0.1:8794/")
    ap.add_argument("--fonts", default=os.environ.get("GF_CACHE"),
                    help="directory holding gf.css and gfonts/ for offline Google Fonts")
    args = ap.parse_args()
    failed = 0
    async with async_playwright() as pw:
        for W, H in SIZES:
            rows = await measure(pw, args.url, args.fonts, W, H)
            bad = [r for r in rows if not r[4]]
            failed += len(bad)
            worst = min((r[2] for r in rows), default=0)
            print(f"{W}x{H}: {len(rows) - len(bad)}/{len(rows)} pass, worst {worst:.2f}")
            for text, fs, got, need, _ in bad:
                print(f"    FAIL {got:5.2f} (need {need}) {fs:6.1f}px  {text!r}")
    print("\nall pass" if not failed else f"\n{failed} failing run(s)")
    return 1 if failed else 0

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))

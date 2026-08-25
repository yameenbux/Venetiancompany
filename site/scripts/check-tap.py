#!/usr/bin/env python3
"""Tap targets at phone widths: every control at least 44x44, and no two hit
areas overlapping each other.

The second half matters as much as the first. Extending a hit area with a
pseudo-element fixes the size without moving the layout, but two links 30px
apart both grown to 44px now overlap, and the top one silently eats the
bottom one's taps. Measuring the visible box would never show it.

    PAGE_URL=http://127.0.0.1:8899/ python3 site/scripts/check-tap.py
"""
import asyncio, os, sys
from playwright.async_api import async_playwright

URL = os.environ.get("PAGE_URL", "http://127.0.0.1:8899/")
CHROME = os.environ.get("CHROME_PATH") or None
MIN = 44

JS = """()=>{
  const vis=(k)=>{const c=getComputedStyle(k);
    if(c.display==='none'||c.visibility==='hidden')return false;
    if(k.checkVisibility&&!k.checkVisibility({contentVisibilityAuto:true,opacityProperty:true,visibilityProperty:true}))return false;
    return true;};
  const out=[];
  for(const e of document.querySelectorAll('a[href],button,summary,input,video[controls]')){
    if(!vis(e))continue;
    const r=e.getBoundingClientRect();
    if(r.width<1&&r.height<1)continue;
    // The real target is the union of the box and any ::after hit area.
    const a=getComputedStyle(e,'::after');
    let top=r.top, bot=r.bottom, left=r.left, right=r.right;
    if(a.content && a.content!=='none' && a.position==='absolute'){
      const h=parseFloat(a.height), w=parseFloat(a.width);
      if(h && !isNaN(h)){ const my=(r.top+r.bottom)/2; top=Math.min(top,my-h/2); bot=Math.max(bot,my+h/2); }
      if(w && !isNaN(w)){ const mx=(r.left+r.right)/2; left=Math.min(left,mx-w/2); right=Math.max(right,mx+w/2); }
    }
    out.push({label:(e.textContent||e.getAttribute('aria-label')||e.tagName).trim().replace(/\\s+/g,' ').slice(0,30),
      tag:e.tagName.toLowerCase(),
      w:Math.round(right-left), h:Math.round(bot-top),
      top:Math.round(top+scrollY), bot:Math.round(bot+scrollY),
      left:Math.round(left), right:Math.round(right),
      inOverlay: !!e.closest('#navpanel')});
  }
  return out;
}"""

async def collect(p, overlay):
    if overlay:
        await p.evaluate("document.getElementById('navbtn').click()")
        await p.wait_for_timeout(700)
    rows = await p.evaluate(JS)
    if overlay:
        await p.keyboard.press("Escape")
        await p.wait_for_timeout(700)
    return [r for r in rows if r["inOverlay"] == overlay]

async def main():
    fails = []
    async with async_playwright() as pw:
        b = await pw.chromium.launch(**({"executable_path": CHROME} if CHROME else {}))
        for W in (320, 375, 414):
            p = await b.new_page(viewport={"width": W, "height": 812})
            await p.goto(URL, wait_until="load")
            await p.add_style_tag(content="html{scroll-behavior:auto !important}")
            await p.evaluate("()=>document.fonts.ready")
            await p.evaluate("document.getElementById('loadmore')?.click()")
            H = await p.evaluate("document.body.scrollHeight")
            y = 0
            while y < H:
                await p.evaluate(f"window.scrollTo(0,{y})")
                await p.wait_for_timeout(140)
                y += 650
            await p.evaluate("window.scrollTo(0,0)")
            await p.wait_for_timeout(400)
            page_rows = await collect(p, False)
            over_rows = await collect(p, True)
            await p.close()

            small = [r for r in page_rows + over_rows if r["w"] < MIN or r["h"] < MIN]
            print(f"\n=== {W}px — {len(page_rows)+len(over_rows)} controls ===")
            if small:
                for r in small:
                    print(f"  UNDER {MIN}: {r['w']}x{r['h']}  {r['tag']} \"{r['label']}\"")
                    fails.append(f"{W}px: {r['tag']} \"{r['label']}\" is {r['w']}x{r['h']}")
            else:
                print(f"  every control at least {MIN}x{MIN}")

            # Overlap, within each layer separately — the overlay covers the page.
            for name, rows in (("page", page_rows), ("overlay", over_rows)):
                hits = 0
                for i, a in enumerate(rows):
                    for bb in rows[i + 1:]:
                        vo = min(a["bot"], bb["bot"]) - max(a["top"], bb["top"])
                        ho = min(a["right"], bb["right"]) - max(a["left"], bb["left"])
                        if vo > 1 and ho > 1:
                            hits += 1
                            msg = (f"{W}px {name}: \"{a['label']}\" and \"{bb['label']}\" "
                                   f"hit areas overlap by {vo}x{ho}px")
                            print("  OVERLAP:", msg)
                            fails.append(msg)
                if not hits:
                    print(f"  no {name} hit areas overlap")
        await b.close()
    print()
    if fails:
        for f in fails:
            print("FAIL:", f)
        sys.exit(1)
    print("tap targets ok")

asyncio.run(main())

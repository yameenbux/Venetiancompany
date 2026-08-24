#!/usr/bin/env python3
"""Assert the vertical rhythm is the system the stylesheet claims.

Padding in source does not tell you the gap: adjacent paddings add, a
full-bleed band's padding sits inside its own colour and never adds, and an
image-led section has no text at its top edge — reading the gap from text
alone missed by 500px on the work grid.

So this measures the real air between one section's last painted box and the
next section's first, at both anchors, and checks each boundary against the
value its KIND should produce.

    PAGE_URL=http://127.0.0.1:8899/ python3 site/scripts/check-rhythm.py
"""
import asyncio, os, sys
from playwright.async_api import async_playwright

URL = os.environ.get("PAGE_URL", "http://127.0.0.1:8899/")
CHROME = os.environ.get("CHROME_PATH") or None
TOL = 3  # px

# boundary -> kind. "section" gaps are 2x the token (both sides contribute);
# "edge" gaps are 1x (only the quiet side can); "band" boundaries are the
# band's own padding, which the eye reads as the start of the colour.
BOUNDARIES = [
    # The hero's type panel centres itself in a full-height column above lg, so
    # the air under the title is its own composition rather than a padding pair
    # the rhythm can govern. Its paddings are still scale tokens; the resulting
    # gap is reported below and simply not asserted.
    ("Hero → Intro",        "free"),
    ("Intro → Work grid",   "section2"),
    ("Work grid → Material","section2"),
    ("Material → Sample",   "section2"),
    ("Sample → Process",    "section2"),
    ("Process → Film",      "section2"),
    # Cream air first, then the clay band's own padding inside the colour.
    # The eye crosses both, so this boundary is section + band, not either one.
    ("Film → Terms",        "section+band"),
    ("Terms → CTA",         "band"),
    ("CTA → Footer",        "edge"),
    ("Footer → Endmark",    "section"),
]

JS = """()=>{
  const secs=[...document.querySelectorAll('main > section, main > div, footer, .endmark')];
  const vis=(k)=>{const c=getComputedStyle(k);
    if(c.display==='none'||c.visibility==='hidden')return false;
    if(k.checkVisibility&&!k.checkVisibility({contentVisibilityAuto:true,opacityProperty:true,visibilityProperty:true}))return false;
    return true;};
  const box=(e)=>{let t=Infinity,b=-Infinity;
    for(const k of e.querySelectorAll('img,video,svg,p,h1,h2,h3,h4,li,summary,button,a,figcaption,hr,.endmark span')){
      if(!vis(k))continue; const r=k.getBoundingClientRect();
      if(r.height<2)continue; t=Math.min(t,r.top); b=Math.max(b,r.bottom);}
    return [t,b];};
  const cs=getComputedStyle(document.documentElement);
  const px=(n)=>parseFloat(getComputedStyle(document.body).getPropertyValue(n))||null;
  const probe=document.createElement('div'); probe.style.cssText='position:absolute;visibility:hidden';
  document.body.appendChild(probe);
  const tok=(n)=>{probe.style.height=`var(${n})`; return Math.round(parseFloat(getComputedStyle(probe).height));};
  const tokens={section:tok('--spacing-section'),band:tok('--spacing-band'),edge:tok('--spacing-edge')};
  probe.remove();
  const out=[];
  secs.forEach((e)=>{const r=e.getBoundingClientRect(); const [t,b]=box(e);
    out.push({top:Math.round(t+scrollY), bot:Math.round(b+scrollY)});});
  return {rows:out, tokens};
}"""

async def main():
    fails = []
    async with async_playwright() as pw:
        b = await pw.chromium.launch(**({"executable_path": CHROME} if CHROME else {}))
        for W in (1440, 375):
            p = await b.new_page(viewport={"width": W, "height": 900})
            await p.goto(URL, wait_until="load")
            await p.evaluate("()=>document.fonts.ready")
            await p.evaluate("()=>document.querySelectorAll('.rise').forEach(e=>e.classList.add('in'))")
            await p.evaluate("document.getElementById('loadmore')?.click()")
            await p.wait_for_timeout(500)
            d = await p.evaluate(JS)
            rows, tok = d["rows"], d["tokens"]
            want = {"section": tok["section"], "section2": tok["section"] * 2,
                    "band": tok["band"], "edge": tok["edge"],
                    "section+band": tok["section"] + tok["band"], "free": None}
            print(f"\n=== {W}px — section {tok['section']}  band {tok['band']}  edge {tok['edge']} ===")
            print(f"{'boundary':<22} {'kind':<9} {'gap':>6} {'want':>6}")
            for i, (name, kind) in enumerate(BOUNDARIES):
                if i + 1 >= len(rows):
                    break
                gap = rows[i + 1]["top"] - rows[i]["bot"]
                w = want[kind]
                if w is None:
                    print(f"{name:<22} {kind:<9} {gap:>6}      -  (composition, not asserted)")
                    continue
                ok = abs(gap - w) <= TOL
                print(f"{name:<22} {kind:<9} {gap:>6} {w:>6}  {'' if ok else '<-- OFF'}")
                if not ok:
                    fails.append(f"{W}px {name}: {gap}px, {kind} wants {w}px")
            await p.close()
        await b.close()
    print()
    if fails:
        for f in fails:
            print("FAIL:", f)
        sys.exit(1)
    print("rhythm consistent")

asyncio.run(main())

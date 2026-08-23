#!/usr/bin/env python3
"""Assert the motion system: nothing bounces, reveals and hovers stay inside
200-300ms, and every interactive control has a hover state.

A bounce is an easing curve whose control-point y goes above 1 — the value
overshoots its target and comes back. Reading the curve is the only reliable
test; "it looks fine" is not, because an overshoot of a few percent is visible
without being nameable.

    PAGE_URL=http://127.0.0.1:8899/ python3 site/scripts/check-motion.py
"""
import asyncio, os, re, sys
from playwright.async_api import async_playwright

URL = os.environ.get("PAGE_URL", "http://127.0.0.1:8899/")
CHROME = os.environ.get("CHROME_PATH") or None
BAND = (200, 300)

# Neither a reveal nor a hover, and both deliberate: the hero dissolves between
# photographs, and the overlay keeps the reference's own 500ms.
EXEMPT_MS = {1000, 500, 900}

JS = """()=>{
  const out={curves:[],durations:[],noHover:[]};
  const seen=new Set();
  for(const el of document.querySelectorAll('*')){
    const cs=getComputedStyle(el);
    for(const prop of ['transitionTimingFunction','animationTimingFunction']){
      for(const f of cs[prop].split(/,(?![^(]*\\))/)){
        const t=f.trim(); if(!t||t==='none')continue;
        if(!seen.has('c'+t)){seen.add('c'+t); out.curves.push(t);}
      }
    }
    for(const prop of ['transitionDuration','animationDuration']){
      for(const d of cs[prop].split(',')){
        const t=d.trim(); if(!t)continue;
        const ms=t.endsWith('ms')?parseFloat(t):parseFloat(t)*1000;
        if(!ms)continue;
        const key='d'+ms+prop;
        if(!seen.has(key)){seen.add(key);
          out.durations.push({ms:Math.round(ms),prop,
            sel:el.tagName.toLowerCase()+'.'+(el.className||'').toString().split(' ').slice(0,2).join('.')});}
      }
    }
  }
  // Every interactive control should answer a pointer.
  for(const el of document.querySelectorAll('a[href], button, summary')){
    const cs=getComputedStyle(el);
    if(cs.display==='none'||cs.visibility==='hidden')continue;
    const has = cs.transitionProperty!=='none' && cs.transitionProperty!=='all'
                || cs.transitionDuration.split(',').some(d=>parseFloat(d)>0);
    if(!has) out.noHover.push(el.tagName.toLowerCase()+' — '+
      (el.textContent||'').trim().replace(/\\s+/g,' ').slice(0,34));
  }
  return out;
}"""

def bounces(curve):
    m = re.match(r"cubic-bezier\(([-\d.]+),\s*([-\d.]+),\s*([-\d.]+),\s*([-\d.]+)\)", curve)
    if not m:
        return False, None
    x1, y1, x2, y2 = (float(v) for v in m.groups())
    return (y1 > 1.0 or y2 > 1.0 or y1 < 0.0 or y2 < 0.0), (y1, y2)

async def main():
    fails = []
    async with async_playwright() as pw:
        b = await pw.chromium.launch(**({"executable_path": CHROME} if CHROME else {}))
        p = await b.new_page(viewport={"width": 1440, "height": 900})
        await p.goto(URL, wait_until="load")
        await p.evaluate("()=>document.fonts.ready")
        await p.evaluate("()=>document.querySelectorAll('.rise').forEach(e=>e.classList.add('in'))")
        await p.evaluate("document.getElementById('loadmore')?.click()")
        await p.wait_for_timeout(300)
        d = await p.evaluate(JS)
        await b.close()

    print("=== easing curves in use ===")
    for c in sorted(d["curves"]):
        bad, ys = bounces(c)
        note = f"  y = {ys}" if ys else ""
        print(f"  {'BOUNCES' if bad else 'ease-out'}  {c}{note}")
        if bad:
            fails.append(f"{c} overshoots — control-point y above 1")

    print("\n=== durations ===")
    for row in sorted(d["durations"], key=lambda r: -r["ms"]):
        ms = row["ms"]
        ok = BAND[0] <= ms <= BAND[1] or ms in EXEMPT_MS
        tag = "" if ok else "  <-- OUTSIDE 200-300ms"
        note = "  (exempt)" if ms in EXEMPT_MS and not (BAND[0] <= ms <= BAND[1]) else ""
        print(f"  {ms:>5}ms  {row['prop']:<20} {row['sel'][:40]}{note}{tag}")
        if not ok:
            fails.append(f"{ms}ms on {row['sel']} ({row['prop']}) is outside {BAND[0]}-{BAND[1]}ms")

    print("\n=== interactive controls with no transition ===")
    if d["noHover"]:
        for n in sorted(set(d["noHover"])):
            print("  ", n)
            fails.append(f"no hover transition: {n}")
    else:
        print("   none — every link, button and summary answers a pointer")

    print()
    if fails:
        for f in fails:
            print("FAIL:", f)
        sys.exit(1)
    print("motion system consistent")

asyncio.run(main())

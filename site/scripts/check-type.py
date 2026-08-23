#!/usr/bin/env python3
"""Assert the type system is what the stylesheet claims it is.

Source classes lie: a token can be declared and never used, be overridden by a
utility that ships later in the cascade, or sit on the ladder at one anchor and
off it at the other. This renders the page and checks the rendered values.

    PAGE_URL=http://127.0.0.1:8899/ python3 site/scripts/check-type.py

Checks
  1. Every rendered step sits on the geometric ladder at BOTH anchors, within
     0.5%. Steps 4, 5, 7 and 8 are skipped on purpose, so a joint may be a
     whole number of steps rather than exactly one.
  2. Leading and tracking come only from the scale — nothing on the page sets a
     one-off value. The two declared exceptions are listed below.
  3. Display leading tightens monotonically as the steps grow.
  4. Tracking follows ls = -0.014193 * ln(px/18) at the 1440 sizes.
  5. The terminal mark fills 98-100% of the viewport.
"""
import asyncio, math, os, sys
from playwright.async_api import async_playwright

URL = os.environ.get("PAGE_URL", "http://127.0.0.1:8899/")
CHROME = os.environ.get("CHROME_PATH") or None

# name -> (expected line-height, expected tracking em). Off-ladder by declaration.
EXEMPT = {"label", "endmark"}
TRACK_K = -0.014193          # ls = TRACK_K * ln(px / 18)
TOL_RATIO = 0.005            # 0.5% on a ladder joint
TOL_TRACK = 0.0008           # em

PROBE = """()=>{
  const q=(s)=>document.querySelector(s);
  const read=(e)=>{ if(!e) return null; const cs=getComputedStyle(e);
    const fs=parseFloat(cs.fontSize);
    return {px:+fs.toFixed(3),
            lh:+((cs.lineHeight==='normal'?NaN:parseFloat(cs.lineHeight))/fs).toFixed(4),
            em:+((cs.letterSpacing==='normal'?0:parseFloat(cs.letterSpacing))/fs).toFixed(5)};};
  const out={};
  out.label   = read(q('#work p.label'));
  out.caption = read(q('#count'));
  out.body    = read(q('#material p.font-read.text-body'));
  out.lede    = read(q('main p.font-read.text-lede'));
  out.h4      = read(q('#process h3'));
  out.h3      = read(q('#material h3'));
  out.h2      = read(q('#material h2'));
  out.wordmark= read(q("header a[href='#top']"));
  const mark=q('.endmark span');
  out.endmark = read(mark);
  if(mark){ const r=document.createRange(); r.selectNodeContents(mark);
            out.endmark.fill = +(r.getBoundingClientRect().width/innerWidth).toFixed(4); }
  // Every distinct leading/tracking pair that actually renders, so a one-off
  // set anywhere on the page shows up even if this probe does not name it.
  const seen=new Set(); const walk=(el)=>{ for(const n of el.childNodes){
    if(n.nodeType===3 && n.textContent.trim()){ const e=n.parentElement, cs=getComputedStyle(e);
      if(cs.display==='none'||cs.visibility==='hidden')continue;
      if(e.checkVisibility && !e.checkVisibility({contentVisibilityAuto:true,opacityProperty:true,visibilityProperty:true}))continue;
      const fs=parseFloat(cs.fontSize);
      seen.add([+fs.toFixed(2),
        +((cs.lineHeight==='normal'?NaN:parseFloat(cs.lineHeight))/fs).toFixed(3),
        +((cs.letterSpacing==='normal'?0:parseFloat(cs.letterSpacing))/fs).toFixed(4)].join('/'));
    } if(n.nodeType===1) walk(n); } };
  walk(document.body);
  out._all=[...seen].sort();
  return out;
}"""

LADDER = ["caption", "body", "lede", "h4", "h3", "h2"]
STEPS  = {"caption": -1, "body": 0, "lede": 1, "h4": 2, "h3": 3, "h2": 6}

async def probe(pw, W):
    b = await pw.chromium.launch(**({"executable_path": CHROME} if CHROME else {}))
    p = await b.new_page(viewport={"width": W, "height": 900})
    await p.goto(URL, wait_until="load")
    await p.evaluate("()=>document.fonts.ready")
    # Reveals are opacity-0 until scrolled into view, and checkVisibility()
    # honours opacity — without this the sweep only ever sees the first screen.
    await p.evaluate("()=>document.querySelectorAll('.rise').forEach(e=>e.classList.add('in'))")
    await p.evaluate("document.getElementById('loadmore')?.click()")
    await p.wait_for_timeout(250)
    r = await p.evaluate(PROBE)
    await b.close()
    return r

async def main():
    fails = []
    async with async_playwright() as pw:
        wide = await probe(pw, 1440)
        narrow = await probe(pw, 375)

    for label, d in (("1440", wide), ("375", narrow)):
        print(f"\n=== {label}px ===")
        print(f"{'step':<9} {'px':>8} {'joint':>8} {'lh':>6} {'trk':>8}")
        prev = None
        ratios = []
        for name in LADDER:
            v = d[name]
            joint = "—"
            if prev:
                gap = STEPS[name] - STEPS[prev[0]]
                r = v["px"] / prev[1]["px"]
                per = r ** (1 / gap)
                ratios.append(per)
                joint = f"{per:.4f}"
            print(f"{name:<9} {v['px']:>8.2f} {joint:>8} {v['lh']:>6.3f} {v['em']:>8.4f}")
            prev = (name, v)
        base = ratios[0]
        for name, r in zip(LADDER[1:], ratios):
            if abs(r - base) / base > TOL_RATIO:
                fails.append(f"{label}px: ladder joint at {name} is {r:.4f}, series is {base:.4f}")
        print(f"  ladder ratio {base:.4f} at every joint"
              if not any(abs(r - base) / base > TOL_RATIO for r in ratios) else "  LADDER BROKEN")

    # Display leading tightens monotonically as the steps grow.
    order = ["lede", "h4", "h3", "h2"]
    lhs = [wide[n]["lh"] for n in order]
    if lhs != sorted(lhs, reverse=True):
        fails.append(f"display leading not monotonic: {list(zip(order, lhs))}")

    # Tracking follows the curve, evaluated at the 1440 sizes.
    print("\n=== tracking vs curve (1440) ===")
    for name in LADDER:
        v = wide[name]
        want = TRACK_K * math.log(v["px"] / 18.0)
        ok = abs(v["em"] - want) <= TOL_TRACK
        print(f"  {name:<9} {v['em']:>8.4f}  curve {want:>8.4f}  {'ok' if ok else 'OFF CURVE'}")
        if not ok:
            fails.append(f"{name} tracking {v['em']:.4f}, curve wants {want:.4f}")

    # The wordmark is the body step with the one tracked-caps value.
    wm = wide["wordmark"]
    if abs(wm["px"] - wide["body"]["px"]) > 0.5:
        fails.append(f"wordmark is {wm['px']}px, body step is {wide['body']['px']}px")
    if abs(wm["em"] - wide["label"]["em"]) > 0.0005:
        fails.append(f"wordmark tracking {wm['em']} != label {wide['label']['em']}")

    # The mark fills the viewport.
    for label, d in (("1440", wide), ("375", narrow)):
        f = d["endmark"]["fill"]
        print(f"\n  endmark fills {f*100:.1f}% of {label}px")
        if not 0.98 <= f <= 1.0:
            fails.append(f"{label}px: endmark fills {f*100:.1f}%, want 98-100%")

    # Nothing sets a one-off leading or tracking.
    allowed = {(wide[n]["lh"], wide[n]["em"]) for n in LADDER + ["label", "endmark"]}
    allowed |= {(narrow[n]["lh"], narrow[n]["em"]) for n in LADDER + ["label", "endmark"]}
    allowed = {(round(a, 3), round(b, 4)) for a, b in allowed}
    print("\n=== every rendered (px / leading / tracking) ===")
    for label, d in (("1440", wide), ("375", narrow)):
        for row in d["_all"]:
            px, lh, em = (float(x) for x in row.split("/"))
            ok = (round(lh, 3), round(em, 4)) in allowed
            print(f"  {label}px  {px:>7.2f} / {lh:.3f} / {em:+.4f}  {'' if ok else '<-- ONE-OFF'}")
            if not ok:
                fails.append(f"{label}px: {px}px sets leading {lh} tracking {em}, off the system")

    print()
    if fails:
        for f in fails:
            print("FAIL:", f)
        sys.exit(1)
    print("type system consistent")

asyncio.run(main())

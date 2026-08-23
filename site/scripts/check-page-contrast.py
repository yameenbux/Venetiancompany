#!/usr/bin/env python3
"""Every text run on the page, checked against the pixels actually behind it.

Contrast here cannot be read off the tokens. The ground is a gradient with a
darkening radial and a grain layer multiplying over it, the hero sets ink over a
photograph, and the swatch captions set white over six different plasters. So
this renders the page, hides the text without touching layout, screenshots what
is behind it and samples the worst pixel under every glyph run.

    PAGE_URL=http://127.0.0.1:8794/ python3 site/scripts/check-page-contrast.py

Env: PAGE_URL, CHROME_PATH (Playwright browser), GF_CACHE (dir with gf.css and
gfonts/ to serve Google Fonts offline).

Two things it deliberately excludes, both of which produced phantom failures:
runs sitting under the fixed opaque header (they are covered, not low-contrast),
and colours the canvas cannot resolve — Chromium silently ignores an invalid
fillStyle, so oklab() was resolving to black and reporting 1.00:1.
"""
import asyncio, io, json, os, sys
import numpy as np
from PIL import Image
from playwright.async_api import async_playwright

S=os.environ.get("GF_CACHE","")   # dir holding gf.css + gfonts/ for offline Google Fonts
CHROME=os.environ.get("CHROME_PATH") or None
GF=open(os.path.join(S,"gf.css")).read() if S and os.path.exists(os.path.join(S,"gf.css")) else None
URL=os.environ.get("PAGE_URL","http://127.0.0.1:8794/")
LUT=np.array([ (c/255)/12.92 if c/255<=0.04045 else (((c/255)+0.055)/1.055)**2.4 for c in range(256)])
def lum(a): return 0.2126*LUT[a[...,0]]+0.7152*LUT[a[...,1]]+0.0722*LUT[a[...,2]]

RUNS=r"""()=>{
  const cv=document.createElement('canvas');cv.width=cv.height=1;
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

  const pathOf=e=>{const o=[];while(e&&e.tagName!=='BODY'){let t=e.tagName.toLowerCase();
    const c=(e.className||'').toString().trim().split(/\s+/).filter(Boolean).slice(0,2).join('.');
    if(c)t+='.'+c; o.unshift(t); e=e.parentElement;} return o.slice(-3).join('>');};
  const out=[],w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;
  while(n=w.nextNode()){
    if(!n.textContent.trim())continue;
    const el=n.parentElement; if(!el)continue;
    const cs=getComputedStyle(el);
    if(cs.display==='none'||cs.visibility==='hidden'||parseFloat(cs.opacity)===0)continue;
    if(el.closest('[aria-hidden=true]'))continue;
    if(el.closest('header'))continue;   // fixed; checked separately at 11 scroll positions
    const r=document.createRange(); r.selectNode(n);
    for(const rc of r.getClientRects()){
      if(rc.width<3||rc.height<3)continue;
      const hh=(document.querySelector('header')?.getBoundingClientRect().height)||0;
      if(rc.top<hh)continue;   // under the fixed, opaque header
      out.push({sel:pathOf(el),text:n.textContent.trim().replace(/\s+/g,' ').slice(0,30),
        rgba:res(cs.color),fs:parseFloat(cs.fontSize),fw:cs.fontWeight,
        x:Math.round(rc.x),y:Math.round(rc.y+scrollY),w:Math.round(rc.width),h:Math.round(rc.height)});
    }}
  return out;}"""

HIDE="body *{color:transparent !important;-webkit-text-fill-color:transparent !important;text-shadow:none !important}"

async def sweep(pw,W,H,label):
    b=await pw.chromium.launch(**({"executable_path":CHROME} if CHROME else {}))
    ctx=await b.new_context(viewport={"width":W,"height":H},device_scale_factor=1,has_touch=(W<768))
    if GF:
        await ctx.route("https://fonts.googleapis.com/**",
            lambda r: asyncio.ensure_future(r.fulfill(status=200,content_type="text/css",body=GF)))
        async def gf(route):
            p=os.path.join(S,"gfonts",os.path.basename(route.request.url.split('?')[0]))
            if os.path.exists(p): await route.fulfill(status=200,content_type="font/woff2",body=open(p,'rb').read())
            else: await route.abort()
        await ctx.route("https://fonts.gstatic.com/**",gf)
    page=await ctx.new_page()
    errs=[];cons=[];bad_req={}
    page.on("pageerror",lambda e:errs.append(str(e)))
    page.on("console",lambda m:cons.append((m.type,m.text)) if m.type in("error","warning") else None)
    page.on("response",lambda r: bad_req.update({r.url:r.status}) if r.status>=400 else None)
    await page.goto(URL,wait_until="load")
    await page.add_style_tag(content="html{scroll-behavior:auto !important}")
    await page.evaluate("()=>document.fonts.ready")
    await page.evaluate("()=>{document.querySelectorAll('.rise').forEach(e=>e.classList.add('in'))}")
    total=await page.evaluate("()=>document.documentElement.scrollHeight")
    # one pass to trigger lazy loads and settle reveals, then decode everything
    step=int(H*0.9)
    for y in range(0,max(1,total-H)+step,step):
        await page.evaluate(f"()=>window.scrollTo(0,{y})"); await page.wait_for_timeout(140)
    await page.evaluate("()=>window.scrollTo(0,0)"); await page.wait_for_timeout(300)
    try: await page.evaluate("async()=>{await Promise.all([...document.images].map(i=>i.decode().catch(()=>{})))}")
    except Exception: pass
    await page.wait_for_timeout(300)
    runs=await page.evaluate(RUNS)          # document coordinates, collected once
    hh=await page.evaluate("()=>Math.ceil((document.querySelector('header')?.getBoundingClientRect().height)||0)")
    await page.add_style_tag(content=HIDE)  # applied once
    await page.wait_for_timeout(200)
    fails=[];checked=0;worst=(99,None)
    for y in range(0,max(1,total-H)+step,step):
        await page.evaluate(f"()=>window.scrollTo(0,{y})"); await page.wait_for_timeout(220)
        sy=await page.evaluate("()=>window.scrollY")
        shot=await page.screenshot(clip={"x":0,"y":0,"width":W,"height":H})
        plate=np.asarray(Image.open(io.BytesIO(shot)).convert("RGB")).astype(np.uint8)
        pL=lum(plate)
        for r in runs:
            ry=r["y"]-sy
            # The header is fixed: it covers the top band in EVERY slice, and its
            # gradient tail brightens the ~14px below that. A run sitting there is
            # sampled against the header, not the page — proved by cropping the
            # same caption at viewport-y 82 (max pixel 145) and 457 (max 78).
            if ry < hh+16: continue
            if ry<0 or ry+r["h"]>H: continue      # only sample fully-visible runs
            x0,y0=max(0,r["x"]),max(0,ry); x1,y1=min(W,r["x"]+r["w"]),min(H,ry+r["h"])
            if x1<=x0 or y1<=y0: continue
            checked+=1
            bg=plate[y0:y1,x0:x1].astype(float); bgL=pL[y0:y1,x0:x1]
            cr,cg,cb,ca=r["rgba"]
            fg=np.stack([cr*ca+bg[...,0]*(1-ca),cg*ca+bg[...,1]*(1-ca),cb*ca+bg[...,2]*(1-ca)],-1)
            fgL=lum(np.clip(np.rint(fg),0,255).astype(np.uint8))
            hi=np.maximum(fgL,bgL); lo=np.minimum(fgL,bgL)
            wv=float(((hi+0.05)/(lo+0.05)).min())
            large=r["fs"]>=24 or (r["fs"]>=18.66 and int(r["fw"])>=700)
            need=3.0 if large else 4.5
            if wv<worst[0]: worst=(wv,(r["text"],r["sel"],round(wv,2),need))
            if wv<need: fails.append({"text":r["text"],"sel":r["sel"],"fs":r["fs"],
                                      "got":round(wv,2),"need":need,"scrollY":sy})
    await b.close()
    seen=set();uniq=[]
    for f in fails:
        k=(f["text"],f["sel"])
        if k in seen: continue
        seen.add(k);uniq.append(f)
    print(f"=== {label} {W}x{H} — page {total}px, {checked} text runs sampled ===")
    print(f"  contrast failures: {len(uniq)} unique")
    for f in uniq: print("    -",f)
    print(f"  lowest ratio anywhere: {worst[1]}")
    print(f"  page errors: {len(errs)} {errs[:2]}")
    print(f"  console errors/warnings: {len(cons)} {cons[:3]}")
    print(f"  failed requests: {bad_req or 'none'}")

async def main():
    async with async_playwright() as pw:
        await sweep(pw,375,812,"MOBILE")
        await sweep(pw,1440,900,"DESKTOP")
asyncio.run(main())

"""The hero title sits on a fixed layer while three photographs rotate under it.
check-contrast.py only ever sees slide 1 (the one present at load), so this
forces each slide on in turn and re-measures. A hero that passes on its first
frame and fails on its third is still a hero that fails."""
import asyncio, io
import numpy as np
from PIL import Image
from playwright.async_api import async_playwright
LUT=np.array([(c/255)/12.92 if c/255<=0.04045 else (((c/255)+0.055)/1.055)**2.4 for c in range(256)])
def lum(a): return 0.2126*LUT[a[...,0]]+0.7152*LUT[a[...,1]]+0.0722*LUT[a[...,2]]
RUNS="""()=>{const cv=document.createElement('canvas');cv.width=cv.height=1;
 const cx=cv.getContext('2d');const res=c=>{cx.fillStyle=c;cx.clearRect(0,0,1,1);cx.fillRect(0,0,1,1);
 const d=cx.getImageData(0,0,1,1).data;return [d[0],d[1],d[2],d[3]/255];};
 const out=[];document.querySelectorAll('section:first-of-type p.label, section:first-of-type h1').forEach(el=>{
  const cs=getComputedStyle(el),r=document.createRange();r.selectNodeContents(el);
  for(const rc of r.getClientRects()){if(rc.width<4||rc.height<4)continue;
   out.push({t:el.textContent.trim().slice(0,26),rgba:res(cs.color),fs:parseFloat(cs.fontSize),
    fw:cs.fontWeight,x:Math.round(rc.x),y:Math.round(rc.y),w:Math.round(rc.width),h:Math.round(rc.height)});}});
 return out;}"""
async def main():
    async with async_playwright() as pw:
        b=await pw.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
        bad=0
        for W,H in [(375,812),(390,844),(768,1024),(1440,900),(1920,1080)]:
            p=await b.new_page(viewport={"width":W,"height":H})
            await p.goto("http://127.0.0.1:8899/",wait_until="load")
            await p.evaluate("()=>document.fonts.ready")
            n=await p.evaluate("()=>document.querySelectorAll('#slides .slide').length")
            for s in range(n):
                await p.evaluate(f"""()=>{{const im=[...document.querySelectorAll('#slides .slide')];
                  im.forEach((e,i)=>{{e.loading='eager';e.style.transition='none';e.dataset.on=String(i==={s});}});}}""")
                await p.evaluate(f"()=>document.querySelectorAll('#slides .slide')[{s}].decode()")
                await p.wait_for_timeout(400)
                runs=await p.evaluate(RUNS)
                await p.evaluate("()=>{document.querySelector('section > div.relative.z-1').style.visibility='hidden';}")
                await p.wait_for_timeout(120)
                shot=await p.screenshot(clip={"x":0,"y":0,"width":W,"height":H})
                await p.evaluate("()=>{document.querySelector('section > div.relative.z-1').style.visibility='';}")
                plate=np.asarray(Image.open(io.BytesIO(shot)).convert("RGB")).astype(np.uint8);pL=lum(plate)
                for r in runs:
                    x0,y0=max(0,r["x"]),max(0,r["y"]);x1,y1=min(W,r["x"]+r["w"]),min(H,r["y"]+r["h"])
                    if x1<=x0 or y1<=y0: continue
                    bg=plate[y0:y1,x0:x1].astype(float);bgL=pL[y0:y1,x0:x1]
                    cr,cg,cb,ca=r["rgba"]
                    fg=np.stack([cr*ca+bg[...,0]*(1-ca),cg*ca+bg[...,1]*(1-ca),cb*ca+bg[...,2]*(1-ca)],-1)
                    fgL=lum(np.clip(np.rint(fg),0,255).astype(np.uint8))
                    wv=float(((np.maximum(fgL,bgL)+0.05)/(np.minimum(fgL,bgL)+0.05)).min())
                    need=3.0 if (r["fs"]>=24 or (r["fs"]>=18.66 and int(r["fw"])>=700)) else 4.5
                    flag="FAIL" if wv<need else "ok  "
                    if wv<need: bad+=1
                    print(f"  {W}x{H} slide{s+1} {flag} {wv:5.2f} (need {need}) — {r['t']}")
            await p.close()
        await b.close()
        print("\nFAILURES:",bad)
asyncio.run(main())

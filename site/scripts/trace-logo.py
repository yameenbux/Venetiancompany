#!/usr/bin/env python3
"""Regenerate the TVC monogram path from Adam's supplied artwork.

The mark is a trace, not a reconstruction, so the artwork is the source of
truth and this is how it gets turned back into a path. Run it if the artwork is
ever re-supplied at a higher resolution.

    pip install potracer pillow numpy
    python3 site/scripts/trace-logo.py            # prints the path data
    python3 site/scripts/trace-logo.py --check    # also reports IoU vs source

The output goes into src/components/Monogram.astro, and the same path data is
reused in public/assets/favicon.svg and apple-touch-icon.png.
"""
import argparse, os, sys
import numpy as np
import potrace
from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "logo-source.jpg")
UPSCALE = 4      # the artwork is only 320px; trace at 1280 and scale back down
BLUR = 1.2       # smooths JPEG ringing so potrace doesn't chase artefacts
VIEWBOX = 512.0

def bitmap(path):
    im = Image.open(path).convert("L")
    w, h = im.size
    im = im.resize((w * UPSCALE, h * UPSCALE), Image.LANCZOS).filter(ImageFilter.GaussianBlur(BLUR))
    grey = np.asarray(im)
    # potrace.Bitmap.__init__ calls self.invert() unconditionally, so hand it
    # True-where-WHITE and the constructor flips it to True-where-ink.
    return grey >= 128

def crop_square(bm):
    """Trim to the mark and centre it, so the ring sits tight in the viewBox."""
    ys, xs = np.nonzero(~bm)
    sub = bm[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    h, w = sub.shape
    side = max(w, h)
    out = np.ones((side, side), dtype=bool)
    out[(side - h) // 2:(side - h) // 2 + h, (side - w) // 2:(side - w) // 2 + w] = sub
    return out

def trace(bm):
    scale = VIEWBOX / bm.shape[0]
    f = lambda v: round(v * scale, 2)
    parts = []
    for curve in potrace.Bitmap(bm).trace(turdsize=10, alphamax=1.0, opticurve=True, opttolerance=0.2):
        start = curve.start_point
        d = [f"M{f(start.x)} {f(start.y)}"]
        for seg in curve:
            if seg.is_corner:
                d.append(f"L{f(seg.c.x)} {f(seg.c.y)}L{f(seg.end_point.x)} {f(seg.end_point.y)}")
            else:
                d.append(f"C{f(seg.c1.x)} {f(seg.c1.y)} {f(seg.c2.x)} {f(seg.c2.y)}"
                         f" {f(seg.end_point.x)} {f(seg.end_point.y)}")
        parts.append("".join(d) + "Z")
    return "".join(parts)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="report shape agreement with the source")
    args = ap.parse_args()
    bm = crop_square(bitmap(SOURCE))
    d = trace(bm)
    print(d)
    if args.check:
        # Rasterise the traced path back at the source size and compare ink masks.
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            print("\n--check needs playwright", file=sys.stderr)
            return 0
        import io
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" '
               f'width="512" height="512"><path fill="#000" d="{d}"/></svg>')
        with sync_playwright() as pw:
            b = pw.chromium.launch(executable_path=os.environ.get("CHROME_PATH") or None)
            page = b.new_context(viewport={"width": 512, "height": 512}).new_page()
            page.set_content(f'<body style="margin:0;background:#fff">{svg}</body>')
            page.wait_for_timeout(300)
            shot = page.screenshot(clip={"x": 0, "y": 0, "width": 512, "height": 512})
            b.close()
        traced = np.asarray(Image.open(io.BytesIO(shot)).convert("L")) < 128
        source = np.asarray(Image.fromarray((~crop_square(bitmap(SOURCE))).astype("uint8") * 255)
                            .resize((512, 512), Image.LANCZOS)) > 127
        iou = (traced & source).sum() / (traced | source).sum()
        print(f"\nink px  traced {traced.sum()}  source {source.sum()}", file=sys.stderr)
        print(f"IoU {iou * 100:.2f}%", file=sys.stderr)
    return 0

if __name__ == "__main__":
    sys.exit(main())

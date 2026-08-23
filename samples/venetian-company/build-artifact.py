#!/usr/bin/env python3
"""Derive the Artifact-publishable copy from index.html.

The Artifact host wraps the file in its own <!doctype>/<html>/<head>/<body>
skeleton, so the published file must contain page content only. This keeps
index.html the single source of truth — re-run after editing it.

    python samples/venetian-company/build-artifact.py
"""
import base64
import re
from pathlib import Path

HERE = Path(__file__).parent
src = (HERE / "index.html").read_text()

# The standalone page's <title> carries an SEO tail; an Artifact title is the name
# alone — the explainer belongs in the publish description.
title = re.search(r"<title>(.*?)</title>", src, re.S).group(1).split(" — ")[0]
link  = re.search(r'<link href="https://fonts\.googleapis\.com[^>]*>', src).group(0)
style = re.search(r"<style>.*?</style>", src, re.S).group(0)
body  = re.search(r"<body>\s*(.*?)\s*</body>", src, re.S).group(1)

# The Artifact host serves a single file with no assets/ directory beside it, and its
# CSP blocks external hosts, so every local asset has to travel inside the page.
MIME = {".jpg": "image/jpeg", ".png": "image/png", ".mp4": "video/mp4"}

def inline(match):
    attr, path = match.group(1), match.group(2)
    f = HERE / path
    if not f.exists():
        raise SystemExit(f"missing asset: {path}")
    mime = MIME[f.suffix]
    return f'{attr}="data:{mime};base64,{base64.b64encode(f.read_bytes()).decode()}"'

body = re.sub(r'\b(src|poster)="(assets/[^"]+)"', inline, body)

out = f"<title>{title}</title>\n{link}\n{style}\n\n{body}\n"
(HERE / "artifact.html").write_text(out)
print(f"artifact.html written — {len(out)/1e6:.1f} MB with media inlined")

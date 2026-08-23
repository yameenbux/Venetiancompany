#!/usr/bin/env python3
"""Build a clean, standalone copy of the site for hosting.

Output is `dist/` at the repo root: index.html plus its assets, and nothing else.
No CLAUDE.md, no build scripts, no repo furniture — just the site, ready to push
to whatever is serving it.

    python samples/venetian-company/build-site.py
"""
import shutil
from pathlib import Path

SRC = Path(__file__).parent
ROOT = SRC.parent.parent
DIST = ROOT / "dist"

if DIST.exists():
    shutil.rmtree(DIST)
DIST.mkdir()

shutil.copy2(SRC / "index.html", DIST / "index.html")
shutil.copytree(SRC / "assets", DIST / "assets", ignore=shutil.ignore_patterns("*.md"))
(DIST / ".nojekyll").touch()  # stop Pages running the files through Jekyll

total = sum(f.stat().st_size for f in DIST.rglob("*") if f.is_file())
files = sum(1 for f in DIST.rglob("*") if f.is_file())
print(f"dist/ built — {files} files, {total/1e6:.1f} MB")
for f in sorted(DIST.rglob("*")):
    if f.is_file():
        print(f"  {f.stat().st_size//1024:>5}KB  {f.relative_to(DIST)}")

# Deploy (from the repo root, after this script):
#   git worktree add --detach /tmp/ghp && cd /tmp/ghp
#   git checkout gh-pages
#   find . -mindepth 1 -maxdepth 1 ! -name .git -exec rm -rf {} +
#   cp -r ../../dist/. .          # adjust path to wherever dist/ landed
#   git add -A && git commit -m "Update site" && git push
#   cd - && git worktree remove --force /tmp/ghp

#!/usr/bin/env bash
# Publish the site to the gh-pages branch.
#
#   ./site/scripts/deploy.sh                      → subpath build for
#                                                   yameenbux.github.io/Venetiancompany/
#   ./site/scripts/deploy.sh thevenetianco.co.uk  → root build on a custom domain
#
# A custom domain changes three things at once, and getting any one of them
# wrong ships a page with no CSS: the base path goes from /Venetiancompany/ to
# /, the canonical and og:image origins change, and gh-pages needs a CNAME file
# or GitHub drops the domain on the next deploy. This does all three together so
# they cannot drift apart.
set -euo pipefail

DOMAIN="${1:-}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SITE="$ROOT/site"
WT="$(mktemp -d)/ghp"

if [ -n "$DOMAIN" ]; then
  SITE_URL="https://$DOMAIN"; BASE_PATH="/"
  echo "→ custom domain: $DOMAIN"
else
  SITE_URL="https://yameenbux.github.io"; BASE_PATH="/Venetiancompany/"
  echo "→ project subpath: $SITE_URL$BASE_PATH"
fi

echo "→ building"
( cd "$SITE" && SITE_URL="$SITE_URL" BASE_PATH="$BASE_PATH" npx astro build >/dev/null )

# Cheap guard against the failure that actually happens: asset paths that do not
# match where the page will be served from.
if [ -n "$DOMAIN" ]; then
  grep -q 'src="/assets/' "$SITE/dist/index.html" \
    || { echo "FAIL: built with a subpath but deploying to a root domain"; exit 1; }
else
  grep -q 'src="/Venetiancompany/assets/' "$SITE/dist/index.html" \
    || { echo "FAIL: built for the root but deploying to a subpath"; exit 1; }
fi
grep -q "$SITE_URL" "$SITE/dist/index.html" \
  || { echo "FAIL: canonical/og origin is not $SITE_URL"; exit 1; }

echo "→ staging"
git -C "$ROOT" worktree add --detach "$WT" >/dev/null 2>&1
git -C "$WT" checkout gh-pages >/dev/null 2>&1
find "$WT" -mindepth 1 -maxdepth 1 ! -name .git -exec rm -rf {} +
cp -r "$SITE/dist/." "$WT/"
rm -f "$WT/_headers" "$WT/assets/CREDITS.md"   # Cloudflare-only, and internal notes
touch "$WT/.nojekyll"                          # stop Pages running it through Jekyll
[ -n "$DOMAIN" ] && printf '%s\n' "$DOMAIN" > "$WT/CNAME"

echo "→ pushing"
git -C "$WT" add -A
if git -C "$WT" diff --cached --quiet; then
  echo "  nothing changed"
else
  git -C "$WT" commit -q -m "Update site"
  git -C "$WT" push -q origin HEAD:gh-pages
  echo "  pushed $(git -C "$WT" rev-parse --short HEAD)"
fi

git -C "$ROOT" worktree remove --force "$WT" >/dev/null 2>&1 || true
git -C "$ROOT" worktree prune
echo "done — live at ${SITE_URL}${BASE_PATH}"

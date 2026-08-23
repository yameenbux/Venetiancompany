# The Venetian Company — site

Astro + Tailwind, static output, no CMS. Every client-supplied fact lives in
`src/data/site.ts`; nothing is fetched at runtime.

## Develop

```bash
cd site
npm install
npm run dev        # http://localhost:4321
npm run build      # -> site/dist
npm run preview
```

## Deploy — Cloudflare Pages

**Git integration** (recommended). Cloudflare dashboard → Workers & Pages →
Create → Pages → connect the repo, then:

| Setting | Value |
|---|---|
| Framework preset | Astro |
| Build command | `npm run build` |
| Build output directory | `dist` |
| Root directory | `site` |
| Environment variable | `NODE_VERSION` = `22` |

**Direct upload**, if you'd rather not connect the repo:

```bash
npm run build
npx wrangler pages deploy dist --project-name venetian-company
```

`public/_headers` is the cache policy Pages reads on deploy: hashed `_astro/`
output immutable, client media a day, HTML always revalidating.

## Deploy — GitHub Pages (currently live)

`gh-pages` holds the built site only: `index.html`, the assets the page actually
references, and `.nojekyll`. One plain commit, authored as the repo owner, no
repo furniture. Never merge it into anything or anything into it.

```bash
cd site
SITE_URL="https://yameenbux.github.io/Venetiancompany/" \
BASE_PATH="/Venetiancompany/" npm run build
```

Then replace the branch contents with `dist/` (minus `*.md` and anything the
built page does not reference) and commit as `Update site`.

**BASE_PATH is not optional here.** Pages serves this as a project page on a
subpath and Astro writes root-absolute asset paths, so a root build deployed
there 404s every image and renders as type on an empty ground.

## Before the link goes to Adam

1. **Deploy.** GitHub Pages is live at
   https://yameenbux.github.io/Venetiancompany/ — see above. Note that Pages
   exposes the repository behind the URL, and this repo is public. For a URL
   with nothing to trace, `npx wrangler pages deploy dist --project-name
   venetian-company` gives a `*.pages.dev` address with no repo attached.
2. **Match SITE_URL to where it is actually served.** `canonical`, `og:url` and
   `og:image` are absolute and built from it, so a mismatch means `og:image`
   404s and WhatsApp renders a bare link with no preview card — which is what
   an unsolicited link looks like when it looks like spam.
3. **Check the preview.** Send the link to yourself on WhatsApp first. You
   should get the card: the marbled stair, the wordmark, the phone number.
4. **Check the CTA on a real phone.** Every button is a `wa.me` deep link to
   +447527180499 with the enquiry pre-written. Tapping it on a device with
   WhatsApp installed should open a chat *to Adam* with the message ready —
   which also means testing it sends him a real message, so use the desktop
   preview or clear the draft.
5. The reviews section is visibly marked PLACEHOLDER on purpose. Do not fill it
   in with invented quotes; it is the reason to ask him for three real ones.

## Notes

- `site/` is self-contained — nothing in it points outside itself, which matters
  because Cloudflare builds with `site` as the root directory. `public/assets` is
  the canonical home for the client's photography and film (see
  `public/assets/CREDITS.md`); the archived single-file samples under `samples/`
  symlink *into* here, not the other way round.
- The single call-to-action is `src/components/BookCall.astro`. Used in six
  places, one destination. Adam has no booking system, so it opens WhatsApp with
  the request pre-written — swapping in Cal.com or Calendly is a one-line change
  to `href`.
- `astro.config.mjs` sets `site:` — the canonical URL and `og:image` are built
  from it, so change it when a real domain is attached.

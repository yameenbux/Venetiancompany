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

## Before the link goes to Adam

1. **Deploy.** Direct upload is the route that leaves no trail back to this
   repo — `npm run build && npx wrangler pages deploy dist --project-name
   venetian-company`. Git integration exposes the connected repository, and
   this one is public.
2. **Set the real URL.** `astro.config.mjs` still says
   `https://venetiancompany.pages.dev`. `canonical`, `og:url` and `og:image`
   are absolute and built from it, so if the deployed URL differs, **rebuild
   after changing it** — otherwise `og:image` 404s and WhatsApp renders a bare
   link with no preview card, which is what an unsolicited link looks like when
   it looks like spam.
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

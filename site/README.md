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

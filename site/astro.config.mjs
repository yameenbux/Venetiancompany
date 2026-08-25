// @ts-check
import { defineConfig } from 'astro/config';
import tailwind from '@tailwindcss/vite';

// Static output — the host serves the build directory directly, so no adapter
// and no server runtime. Nothing here needs a CMS: all client content lives in
// src/data/site.ts.
//
// `site` and `base` come from the environment so the same source builds for
// either host. The defaults are the Cloudflare Pages case, where the site sits
// at the root. GitHub Pages serves this as a PROJECT page on a subpath, and
// Astro writes root-absolute asset paths, so a build without BASE_PATH set
// would request /assets/... and 404 every image on it:
//
//   SITE_URL=https://<user>.github.io/Venetiancompany/ \
//   BASE_PATH=/Venetiancompany/ npm run build
//
// `site` is also what canonical, og:url and og:image are built from, so it has
// to match the URL the page is actually served at or the WhatsApp link preview
// will not resolve.
export default defineConfig({
  site: process.env.SITE_URL ?? 'https://thevenetiancompany.co.uk',
  base: process.env.BASE_PATH ?? '/',
  output: 'static',
  build: { inlineStylesheets: 'always' },
  vite: { plugins: [tailwind()] },
});

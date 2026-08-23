// @ts-check
import { defineConfig } from 'astro/config';
import tailwind from '@tailwindcss/vite';

// Static output — Cloudflare Pages serves the build directory directly, so no
// adapter and no server runtime. Nothing here needs a CMS: all client content
// lives in src/data/site.ts.
export default defineConfig({
  site: 'https://venetiancompany.pages.dev',
  output: 'static',
  build: { inlineStylesheets: 'always' },
  vite: { plugins: [tailwind()] },
});

/**
 * Prefix a `public/` path with the deploy base.
 *
 * Astro rewrites paths it owns, but not strings we hardcode in markup, and the
 * site can be served from a subpath (GitHub Pages serves it as a project page
 * at /Venetiancompany/). Without this every image, the favicon and the film
 * would request /assets/... and 404 there.
 *
 * `import.meta.env.BASE_URL` is "/" for a root deploy, so this is a no-op on
 * Cloudflare Pages.
 */
export const asset = (path: string): string =>
  `${import.meta.env.BASE_URL.replace(/\/$/, '')}/${path.replace(/^\//, '')}`;

# trenck.net

The deployed source of **[trenck.net](https://trenck.net)** — a static personal
site. This repo mirrors `/var/www/html` on the host; edit the HTML directly.

## Pages

`/` · `/about/` · `/experience/` · `/skills/` · `/certifications/` ·
`/projects/` · `/homelab/` · `/contact/` · `404.html`

Every page is a full standalone HTML document sharing the same `<head>`
boilerplate, nav, footer, and one interaction script.

## Stack

- Hand-written multi-page HTML, no client framework
- Tailwind, prebuilt and purged to `styles.<hash>.css` (~19 KB). **New markup
  must reuse classes already in that file** — the build step is retired
  (`_build-legacy/`), so an unknown class renders unstyled
- Libre Franklin, self-hosted under `/fonts/` (no Google Fonts request). Icons
  are inline SVG — Font Awesome was retired
- Responsive AVIF/WebP/JPEG headshot in `/img/`
- Structured data (`@graph` JSON-LD) per page; `sitemap.xml`, `robots.txt`,
  `.well-known/security.txt`

## Deploy

```bash
sudo ./deploy.sh
```

Syncs this tree to `/var/www/html`, bumps `sitemap.xml`'s `<lastmod>` to
today, and smoke-tests every page through the local Caddy. HTML is served
pass-through (Cloudflare `cf-cache: DYNAMIC`) and static assets are
content-hashed or cached immutably, so no Cloudflare purge is needed.

See `CHANGELOG.md` for history.

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
- Libre Franklin (Google Fonts) + Font Awesome, both self-hosted under `/fa/`
- Responsive AVIF/WebP/JPEG headshot in `/img/`
- Structured data (`@graph` JSON-LD) per page; `sitemap.xml`, `robots.txt`,
  `.well-known/security.txt`

## Deploy

```bash
sudo rsync -a --delete --chown=caddy:caddy \
  --exclude=.git --exclude=README.md --exclude=CHANGELOG.md --exclude=_build-legacy \
  --exclude=node_modules \
  ~/site-build/ /var/www/html/
# then: Cloudflare → Caching → Purge Everything
```

See `CHANGELOG.md` for history.

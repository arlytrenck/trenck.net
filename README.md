# trenck.net

Source for **[trenck.net](https://trenck.net/)** — a static, multi-page personal
site (résumé / portfolio) built from HTML partials + Tailwind CSS and deployed to
the homelab's Caddy server.

## Layout

```
pages/            per-page <main> content — home, about, experience, skills,
                  certifications, contact, 404
partials/         head.html, header.html, footer.html (shared shell)
input.css         Tailwind entry (@tailwind base/components/utilities + a few @layer rules)
tailwind.config.js
build.py          assembles pages + partials -> dist/, runs the Tailwind CLI,
                  copies static assets, generates sitemap.xml + robots.txt,
                  copies .well-known/security.txt
build_images.js   regenerates the responsive headshot set (avif/webp/jpg at
                  400/600/800/1000/1280/1600 px) from headshot-src.jpg
finalize.py       post-build touch-ups
deploy-multipage.sh   build + publish to the web root, then reminder to purge Cloudflare
img/              generated responsive images (committed)
fa/               vendored Font Awesome subset (committed)
headshot-src.jpg  master headshot (source for build_images.js)
og-card.jpg       Open Graph / social preview image
```

Not committed (`.gitignore`): `dist/` (build output), `node_modules/`,
`_*-bak/` (old design iterations), `staged-changes/`, `*.bak*`.

## Design

Light editorial style (williampitt.com-inspired): **Libre Franklin**, warm paper
`#F5F3EC` body, navy `#002349` header/footer, full-bleed fading hero photo,
drawn-hairline section headings, chip-style skills, mailto contact form. Real
directory URLs (`/about/`, `/experience/`, …); nav links carry `aria-current`.

## Build

```bash
npm install                 # first time — Tailwind CLI
python3 build.py             # -> dist/
```

`build.py` minifies `input.css` -> `dist/styles.css`, writes `dist/sitemap.xml`
and `dist/robots.txt`, and copies `img/`, `fa/`, `og-card.jpg`,
`.well-known/security.txt` into `dist/`.

## Deploy

```bash
sudo bash deploy-multipage.sh
```

Builds, syncs `dist/` to the Caddy web root on `at-srv-prod-vm1`, then **purge
the Cloudflare cache** ("Purge Everything" or per-path) so visitors get the new
version.

### Preview notes

- Local preview is an nginx container on `:8099`; after each build, restart it
  and hit the page with `?v=N` to bust the browser cache.
- The preview's headless Chrome has **no `requestAnimationFrame` and no
  `window.scrollTo`** — verify any JS behaviour via a scripting tool, and nudge
  with a real scroll before taking screenshots.

## Hosting

Served by Caddy (`Caddyfile` on the VM) with a Cloudflare-proxied DNS record and
DNS-01 TLS. WAF, HSTS, and hardened response headers are configured at the
Cloudflare edge + in Caddy.

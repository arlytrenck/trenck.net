# Changelog

Notable changes to the trenck.net site. Grouped by date, newest first.
Format: [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]
- home: both hero buttons now use the outline `.btn` style (dropped `.btn-solid` on "Get in touch").

## 2026-09-03 (perf + forms)
### Changed
- **Self-hosted Libre Franklin** (weights 300/400/500/600, latin + latin-ext,
  `font-display: swap`) under `/fonts/` — removes the render-blocking Google
  Fonts request and the two `preconnect`s. Two hero weights are `preload`ed.
- **Dropped Font Awesome.** The six icons in use (menu, close, envelope,
  LinkedIn, GitHub, award) are now inline SVG. `all.min.css` + 4 webfonts gone;
  `/fa/` no longer shipped.
- **Contact form now delivers.** Posts to Web3Forms via `fetch()` with an inline
  success/error message; falls back to a `mailto:` compose on any failure or if
  the access key is unset. *Action: paste a free Web3Forms access key into the
  hidden `access_key` field on `/contact/`.*
### Added
- **Cloudflare Web Analytics** — enable it in the CF dashboard for the zone
  (auto-injects the cookieless beacon; the CSP now allows it). No code in the
  repo.
- **`deploy.sh`** — `rsync` + `--chown` + a local smoke test; self-elevates with
  `sudo`. Kills the "edit repo, forget to deploy, nightly reverts it" footgun.
### Notes
- Immutable `Cache-Control` for `/fonts/ /img/` + hashed CSS is staged for the
  Caddyfile (`host-config/staged/caddy-cache-headers.txt` in the homelab repo).

## 2026-09-03 (later)
### Changed
- `/homelab/`: removed the media-acquisition tool names from the "Media" row to
  avoid any piracy misread — it now describes the media *servers* (Emby, Immich,
  Komga, Tdarr) only.
### Added
- **GitHub** in the footer "Elsewhere" list on every page, and as a button on
  `/contact/`.
### SEO
- `github.com/arlytrenck` added to every page's `rel="me"` and the Person
  `sameAs` (entity consolidation).
- `/projects/`: JSON-LD `ItemList` of `SoftwareSourceCode` for the three public
  repos; `WebPage.mainEntity` links it.
- `sitemap.xml` `lastmod` refreshed to 2026-09-03 on all URLs.
- Tightened the home and about meta descriptions to ~155 chars.

## 2026-09-03
### Added
- **`/projects/`** — outlines the public toolkits (`sysadmin-linux`,
  `sysadmin-windows`), this site's source, and the private homelab IaC set, with
  a link to the GitHub profile. Added to the nav + `sitemap.xml`; `rel="me"` +
  JSON-LD `sameAs` for GitHub.
- **`/homelab/`** — outlines the self-hosted lab: compute, access & identity,
  media, monitoring & alerting, backup & recovery, remote access, plus a stack
  chip row. Added to the nav + `sitemap.xml`.
- Both pages are structural clones of `/experience/` — identical head, nav,
  footer, and script; content built only from classes already in the purged CSS.
### Changed
- Nav is now 7 items (added Projects, Homelab) on every page + the footer.
- Repo tidy: retired scratch (`dist/`, `_*-bak/`, `staged-changes/`, stale
  `*.bak`) consolidated under `_build-legacy/`; `.gitignore` simplified; README
  expanded with the page list, stack notes, and the deploy command.

## 2026-09-02
### Changed
- **Build system retired.** This repo now mirrors the deployed
  `/var/www/html` verbatim (source of truth) — edit the HTML directly, deploy =
  `rsync`. The old partials + `build.py` + Tailwind toolchain moved to
  `_build-legacy/` (untracked). `backup_docker.sh` rsyncs `/var/www/html` into
  this tree before the nightly commit.

## 2026-08-30 – 09-01
### Changed
- README trimmed (dropped the layout/deploy sections that no longer apply).

## 2026-08-30
### Added
- **Initial commit** — multi-page site source (partials + pages, `build.py`,
  Tailwind); `dist/` and `node_modules/` gitignored. Editorial light design
  (Libre Franklin, warm paper + navy), full-bleed fading hero, drawn-hairline
  section heads, chip skills, mailto contact form.

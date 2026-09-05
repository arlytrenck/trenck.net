# Changelog

Notable changes to the trenck.net site. Grouped by date, newest first.
Format: [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]
- projects: added `homelab-public` as a 4th repo card — a new sanitized
  public mirror of the homelab's Docker Compose stacks (domain/IP/email
  redacted, hardening conventions and real Prometheus rules intact). The
  "Homelab infrastructure-as-code" entry's heading now links to it directly;
  its copy and JSON-LD updated to reflect that some of the homelab is now
  public while the runbook/Ansible/config-snapshot repos stay private.
- projects: the sysadmin-linux, sysadmin-windows, and trenck.net headings
  are now links straight to their GitHub repos (`link-underline`, opens in
  a new tab) — previously plain text, only reachable via the "View all
  public repositories on GitHub" link at the bottom of the page.
- projects + homelab: fixed a copy-paste bug from when both pages were
  cloned off `/experience/` — each page's BreadcrumbList JSON-LD labeled
  its own position-2 crumb `"name": "Experience"` instead of "Projects"/
  "Homelab" (the `item` URL was already correct, just the visible name).
  Also verified Homelab's stat band and alert-rule count against this
  VM's actual live state (it *is* the homelab host) — 16 vCPU, 54 GiB,
  31 running containers, 32 configured alert rules — all match the
  page's claims exactly (the "~" prefixes were already appropriately
  hedged). No other inaccuracies found on either page.
- resume: pulled back per the user — dropped the home hero's "Résumé"
  button and the `/contact/` icon-button row entry entirely; footer
  "Elsewhere" link kept on every page but shortened from "Résumé (PDF)"
  to just "Résumé".
- skills: cross-checked chips against the resume's Technical Skills list
  and added genuine gaps — Docker, VMware, Ansible, and Git — each already
  referenced elsewhere on the site (About's homelab paragraph, every
  Experience theme) but missing here. (Active Directory & Group Policy was
  added in the same pass, then dropped per the user's follow-up.) Mirrored
  the same additions into the site-wide `knowsAbout` JSON-LD block (same
  array repeated on all 9 pages) for consistency. No stat band added —
  Skills is a flat chip taxonomy with no narrative sentences to weave
  figures into, so this pass was an accuracy check instead.
- experience + about: office count corrected 30+/29 (live count from
  williampitt.com/real-estate-offices/, 29 as of 2026-09-05) and end-user
  figure corrected 1,400+ &rarr; 1,250+, both per the user directly. About's
  intro paragraph and fact band now cite the 29-office figure too, and its
  homelab paragraph gained a concrete "roughly 30 containerized services"
  (from the resume's Technical Projects section) — same metrics-pass
  treatment as Experience, applied one page later.
- experience: added a "by the numbers" stat band (30+ offices, 1,400+ end
  users, onboarding time cut in half — same `<dl>` pattern as the About
  page's fact band) and wove concrete figures into the four theme
  paragraphs (52 APs / 31 offices RUCKUS migration, ~1,200-user AD–Okta
  mapping, the onboarding automation's 50% time cut), all sourced from the
  2026 resume. Also restored "Massachusetts" to this page's service-area
  copy (meta/OG/Twitter/JSON-LD description + body text) — it was dropped
  in an earlier pass but is still part of the actual multi-site scope.
- about: fact band "10 industry certifications" → "7", matching the MTA
  cleanup below.
- accessibility: every `target="_blank"` link (LinkedIn, Credly, GitHub,
  Résumé — 44 across all 9 pages) now carries a screen-reader-only
  "(opens in a new tab)" hint (`<span class="sr-only">`, reusing the
  utility already defined for the skip-link). No visual change.
- certifications: dropped the 3 Microsoft MTA badges site-wide — retired by
  Microsoft, already dropped from the resume and the GitHub profile badge
  grid. `/certifications/` now lists 7: CompTIA A+/Network+/Security+/Server+,
  LPI Linux Essentials, ISC2 CC, Fortinet FCA. Removed the matching entries
  from the `hasCredential` JSON-LD (same block on every page) and the 3 now-
  unused `/img/certs/mta-*.png` files.
- resume: added `/resume.pdf`; linked from the home hero (new "Résumé" button
  between "Get in touch" and "LinkedIn"), the contact page's icon-button row,
  and the footer "Elsewhere" list on every page. All existing `.btn`/
  `.link-underline` utilities, no CSS rebuild.
- certifications: each row now leads with its official Credly badge image
  (`/img/certs/*.png`, self-hosted, 220&times;220, ~248&nbsp;KB total) — badge &rarr;
  name &rarr; issuer. Layout uses existing utilities + inline styles; no CSS rebuild.
- favicon: real icon set — `favicon.svg` (navy tile + pen-stroked "A"), `favicon.ico`
  (16/32/48), `apple-touch-icon.png` (180), `icon-192/512.png`, `site.webmanifest`;
  replaces the single inline data-URI. `<link>` set on every page.
- experience: reworked around the engineering — Multi-site infrastructure, Identity &
  access, Security & continuity, Automation & tooling. MSP/BPO partnership row dropped.
- about: focus-list — swapped the MSP/BPO line for "Infrastructure as code".
- about: rewrote as a first-person “about me” (client's copy) — what he builds, plus a paragraph on running the homelab as code; sharpened the focus-area wording; meta description updated.
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

# Changelog

Notable changes to the trenck.net site. Grouped by date, newest first.
Format: [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

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

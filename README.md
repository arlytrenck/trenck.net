# trenck.net

Source for **[trenck.net](https://trenck.net/)** — my personal résumé / portfolio
site. Static, multi-page, built from HTML partials + Tailwind CSS.

- `pages/` — per-page content · `partials/` — shared shell · `build.py` — assembles `dist/`
- `img/` + `fa/` — assets (committed) · `dist/`, `node_modules/` — ignored

```bash
npm install
python3 build.py          # -> dist/
sudo bash deploy-multipage.sh   # build + publish, then purge the CDN cache
```

Served by Caddy with Cloudflare-proxied DNS and DNS-01 TLS.

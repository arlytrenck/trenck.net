# trenck.net

The deployed source of **https://trenck.net**. This tree mirrors
`/var/www/html` on `10.0.0.100` (Caddy serves it directly) — that path is the
source of truth. Edit the HTML/CSS here directly; there is no build step.

## Layout
```
index.html              home
about|experience|skills|certifications|contact/index.html   pages (clean dir URLs)
404.html                Caddy handle_errors target
styles.<hash>.css       one stylesheet, content-hashed for cache-busting
sitemap.xml  robots.txt  .well-known/
fa/  img/  headshot.jpg  og-card.jpg   assets
```

## Deploy
```bash
sudo rsync -a --delete --chown=caddy:caddy \
  --exclude='.git' --exclude='README.md' --exclude='_build-legacy' --exclude='.gitignore' \
  ~/site-build/ /var/www/html/
# then Cloudflare -> Caching -> Purge Everything (or purge changed URLs)
```
If a CSS change ships, rename `styles.<hash>.css` (new hash) and update the
`<link>` in every page so the edge cache doesn't serve a stale copy.

## History
`_build-legacy/` (untracked) holds the previous partials + `build.py` +
`deploy-multipage.sh` generator. It's in git history through the commit that
retired it if you ever need it back.

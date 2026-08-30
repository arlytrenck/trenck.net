#!/bin/bash
#
#   sudo bash ~/site-build/deploy-multipage.sh
#
# Deploys the rebuilt MULTI-PAGE site (dist/) to /var/www/html:
#   - /about/ /experience/ /skills/ /certifications/ /contact/ as real pages
#   - removes any single-page anchor redirects a prior deploy left in the Caddyfile
#   - widens the no-cache matcher to cover directory URLs
#   - keeps the 404 handler + the mailto: form-action CSP allowance
# Full backup + caddy validate + auto-rollback.

set -euo pipefail
[ "$(id -u)" -eq 0 ] || { echo "run with sudo"; exit 1; }

SB=/home/arly/site-build
DIST=$SB/dist
WWW=/var/www/html
CADDYFILE=/etc/caddy/Caddyfile
TS=$(date +%Y%m%d-%H%M%S)
BK=/root/trenck-multipage-backup-$TS

for f in "$DIST/index.html" "$DIST/about/index.html" "$DIST/experience/index.html" \
         "$DIST/skills/index.html" "$DIST/certifications/index.html" "$DIST/contact/index.html" \
         "$DIST/404.html" "$DIST/sitemap.xml" "$DIST/robots.txt" "$DIST/fa/css/all.min.css"; do
  [ -f "$f" ] || { echo "dist incomplete (missing $f) — run: python3 $SB/build.py && rebuild Tailwind + finalize.py"; exit 1; }
done
ls "$DIST"/styles.*.css >/dev/null 2>&1 || { echo "dist incomplete: no fingerprinted styles.<hash>.css"; exit 1; }

echo "==> backup -> $BK"
mkdir -p "$BK"
cp -a "$WWW" "$BK/html"
cp -a "$CADDYFILE" "$BK/Caddyfile"

echo "==> deploy files"
rsync -a --chown=caddy:caddy "$DIST"/ "$WWW"/
[ -f "$WWW/styles.css" ] && rm -f "$WWW/styles.css"  # obsolete un-fingerprinted stylesheet
CUR_CSS=$(basename "$DIST"/styles.*.css)
find "$WWW" -maxdepth 1 -name 'styles.*.css' ! -name "$CUR_CSS" -delete  # stale fingerprinted CSS
find "$WWW" -type d -exec chmod 755 {} +
find "$WWW" -type f -exec chmod 644 {} +

echo "==> patch Caddyfile (dedupe vhosts, drop single-page redirects, widen no-cache matcher, keep 404 + CSP)"
python3 - "$CADDYFILE" <<'PY'
import sys
p = sys.argv[1]
lines = open(p).read().split("\n")

# --- de-duplicate top-level site blocks (keep first occurrence) ---
# guards against a snippet being `tee -a`'d into the Caddyfile more than once.
out, seen, i, n = [], set(), 0, len(lines)
while i < n:
    l = lines[i]
    s = l.strip()
    is_opener = (l[:1] not in (" ", "\t") and s.endswith("{")
                 and not s.startswith("(") and s != "{")
    if is_opener:
        label = s[:-1].strip()
        depth, j = 1, i + 1
        while j < n and depth:
            depth += lines[j].count("{") - lines[j].count("}")
            j += 1
        if label in seen:
            while out and (out[-1].strip() == "" or out[-1].lstrip().startswith("#")):
                out.pop()
            print("  - dropped duplicate block: " + label)
            i = j
            continue
        seen.add(label)
        out.extend(lines[i:j])
        i = j
        continue
    out.append(l)
    i += 1
lines = out

start = next(i for i, l in enumerate(lines) if l.strip() == "trenck.net {" and not l.startswith((" ", "\t")))
end = next(i for i in range(start + 1, len(lines)) if lines[i] == "}")

new = []
for l in lines[start:end]:
    s = l.strip()
    # drop the single-page anchor redirects + their comment
    if s.startswith("redir /") and " /#" in s:
        print("  - " + s)
        continue
    if s == "# legacy multi-page URLs -> single-page anchors":
        continue
    # widen the no-cache matcher for directory URLs
    if s.startswith("@docs path"):
        l = "\t@docs path / */ */index.html /404.html /sitemap.xml /robots.txt /.well-known/*"
    # keep mailto: allowed as a form-action (no-JS contact form fallback)
    if "Content-Security-Policy" in l and "form-action 'self' mailto:" not in l:
        l = l.replace("form-action 'self'", "form-action 'self' mailto:")
        print("  + CSP form-action mailto:")
    new.append(l)
lines[start:end] = new

end = next(i for i in range(start + 1, len(lines)) if lines[i] == "}")
if not any("handle_errors" in x for x in lines[start:end]):
    lines[end:end] = [
        "",
        "\thandle_errors {",
        "\t\t@404 expression `{err.status_code} == 404`",
        "\t\trewrite @404 /404.html",
        "\t\tfile_server",
        "\t}",
    ]
    print("  + handle_errors block")
else:
    print("  handle_errors already present")

open(p, "w").write("\n".join(lines))
PY

CF_API_TOKEN="$(sed -n 's/.*CF_API_TOKEN=\([^"]*\).*/\1/p' /etc/systemd/system/caddy.service.d/override.conf)"
if env CF_API_TOKEN="$CF_API_TOKEN" caddy validate --config "$CADDYFILE" --adapter caddyfile; then
  systemctl reload caddy && sleep 2
  systemctl is-active --quiet caddy || { echo "!! caddy inactive -> reverting"; cp -a "$BK/Caddyfile" "$CADDYFILE"; systemctl reload caddy; exit 1; }
else
  echo "!! caddy validate FAILED -> reverting Caddyfile"; cp -a "$BK/Caddyfile" "$CADDYFILE"; exit 1
fi

echo "==> verify (origin, correct SNI)"
b=(curl -sS --resolve trenck.net:443:127.0.0.1 https://trenck.net)
for u in / /about/ /experience/ /skills/ /certifications/ /contact/ /404.html /sitemap.xml /this-does-not-exist; do
  printf "   %-22s -> " "$u"; "${b[@]}$u" -o /dev/null -w "%{http_code}  %{content_type}  cc=%header{cache-control}\n"
done
echo "   /about (no slash) -> $("${b[@]}/about" -o /dev/null -w '%{http_code} -> %{redirect_url}')"
echo "   nav links on /skills/: $("${b[@]}/skills/" -s | grep -oE 'href="/(about|experience|skills|certifications|contact)/"' | sort -u | tr '\n' ' ')"

echo
echo "DONE.  Backup: $BK"
echo "Rollback: sudo rsync -a --delete $BK/html/ $WWW/ && sudo cp -a $BK/Caddyfile $CADDYFILE && sudo systemctl reload caddy"

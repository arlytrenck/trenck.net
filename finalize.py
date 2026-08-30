#!/usr/bin/env python3
"""Post-build step: content-hash styles.css so every CSS change gets a fresh URL
(prevents stale Cloudflare/browser cache after a deploy).

Run AFTER Tailwind writes dist/styles.css:
    python3 build.py && <tailwind -o dist/styles.css> && python3 finalize.py
"""
import glob, hashlib, os, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, "dist")
css = os.path.join(DIST, "styles.css")
if not os.path.exists(css):
    sys.exit("dist/styles.css not found — build Tailwind first")

digest = hashlib.sha256(open(css, "rb").read()).hexdigest()[:10]
new_name = f"styles.{digest}.css"
os.replace(css, os.path.join(DIST, new_name))

# drop any older fingerprinted copies
for old in glob.glob(os.path.join(DIST, "styles.*.css")):
    if os.path.basename(old) != new_name:
        os.remove(old)

n = 0
for f in glob.glob(os.path.join(DIST, "**", "*.html"), recursive=True):
    s = open(f, encoding="utf-8").read()
    s2 = s.replace('href="/styles.css"', f'href="/{new_name}"')
    if s2 != s:
        open(f, "w", encoding="utf-8").write(s2)
        n += 1

print(f"fingerprinted -> /{new_name}  ({n} html files rewritten)")

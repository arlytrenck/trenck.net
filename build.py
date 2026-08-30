#!/usr/bin/env python3
"""Assemble the multi-page trenck.net site from partials + pages into ./dist/.

  python3 build.py
  <tailwind -c tailwind.config.js -i input.css -o dist/styles.css --minify>
  python3 finalize.py
"""
import json, os, shutil
from datetime import date

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, "dist")
SITE = "https://trenck.net"
ROBOTS_DEFAULT = "index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1"

# hero portrait (home): full-bleed right panel up to 44vw on large screens
PORTRAIT_SIZES = "(min-width:1024px) 44vw, 100vw"
IMG_WIDTHS = [400, 600, 800, 1000, 1280, 1600]

def _srcset(ext):
    return ", ".join(f"/img/headshot-{w}.{ext} {w}w" for w in IMG_WIDTHS)

PRELOAD = ('    <!-- Preload LCP portrait -->\n'
           f'    <link rel="preload" as="image" imagesrcset="{_srcset("avif")}" '
           f'imagesizes="{PORTRAIT_SIZES}" type="image/avif" fetchpriority="high">\n')

# site navigation (label, href)
NAV = [
    ("About", "/about/"),
    ("Experience", "/experience/"),
    ("Skills", "/skills/"),
    ("Certifications", "/certifications/"),
    ("Contact", "/contact/"),
]

PAGES = [
    dict(key="home", out="index.html", url="/", nav_key=None, crumb=None,
         preload=True, og_type="profile", priority="1.0", changefreq="monthly",
         title="Arly Trenck | IT Systems Engineer & Infrastructure Architect",
         desc="Arly Trenck is a certified IT Systems Engineer and Infrastructure Architect in Fairfield, Connecticut — multi-site infrastructure, identity and access, network security, and process automation."),
    dict(key="about", out="about/index.html", url="/about/", nav_key="/about/", crumb="About",
         preload=False, og_type="website", priority="0.8", changefreq="yearly",
         title="About · Arly Trenck",
         desc="Arly Trenck — enterprise administration, modern security standards, and workflow automation, focused on high-reliability environments across multi-site organizations."),
    dict(key="experience", out="experience/index.html", url="/experience/", nav_key="/experience/", crumb="Experience",
         preload=False, og_type="website", priority="0.8", changefreq="yearly",
         title="Experience · Arly Trenck",
         desc="MSP & BPO partnership operations, multi-site infrastructure across Connecticut and New York, and automation with PowerShell and Bash."),
    dict(key="skills", out="skills/index.html", url="/skills/", nav_key="/skills/", crumb="Skills",
         preload=False, og_type="website", priority="0.8", changefreq="yearly",
         title="Skills · Arly Trenck",
         desc="Cloud & infrastructure, identity & zero trust, network security & edge, and RMM / automation / backup — the platforms and tools Arly Trenck works with."),
    dict(key="certifications", out="certifications/index.html", url="/certifications/", nav_key="/certifications/", crumb="Certifications",
         preload=False, og_type="website", priority="0.7", changefreq="yearly",
         title="Certifications · Arly Trenck",
         desc="Ten industry certifications: CompTIA A+/Network+/Security+/Server+, LPI Linux Essentials, ISC2 CC, Microsoft MTA, and Fortinet FCA."),
    dict(key="contact", out="contact/index.html", url="/contact/", nav_key="/contact/", crumb="Contact",
         preload=False, og_type="website", priority="0.6", changefreq="yearly",
         title="Contact · Arly Trenck",
         desc="Get in touch with Arly Trenck by email, LinkedIn, or Credly, or send a message directly from the contact form."),
    dict(key="404", out="404.html", url=None, nav_key=None, crumb=None,
         preload=False, og_type="website", priority=None, changefreq=None,
         robots="noindex, follow",
         title="Page not found | Arly Trenck",
         desc="The page you're looking for doesn't exist or has moved."),
]

PERSON = {
    "@type": "Person",
    "@id": SITE + "/#person",
    "name": "Arly Trenck",
    "url": SITE + "/",
    "image": {"@type": "ImageObject", "url": SITE + "/headshot.jpg", "width": 1000, "height": 1500},
    "jobTitle": "IT Systems Engineer & Infrastructure Architect",
    "email": "mailto:arly@trenck.net",
    "knowsLanguage": "en-US",
    "description": "Certified IT Systems Engineer and Infrastructure Architect in Fairfield, Connecticut, with 5+ years running multi-site infrastructure, identity and access, network security, and process automation.",
    "address": {
        "@type": "PostalAddress",
        "addressLocality": "Fairfield",
        "addressRegion": "CT",
        "addressCountry": "US",
    },
    "homeLocation": {
        "@type": "Place",
        "name": "Fairfield, Connecticut",
        "address": {"@type": "PostalAddress", "addressLocality": "Fairfield", "addressRegion": "CT", "addressCountry": "US"},
    },
    "hasOccupation": {
        "@type": "Occupation",
        "name": "IT Systems Engineer & Infrastructure Architect",
        "occupationLocation": {"@type": "City", "name": "Fairfield, Connecticut"},
        "skills": "Windows and Linux server administration, Microsoft Entra ID and Okta SSO, network security, VPN, EDR/XDR, RMM, backup and disaster recovery, PowerShell and Bash automation",
    },
    "knowsAbout": [
        "Windows Server administration", "Linux server administration",
        "Microsoft Entra ID", "Conditional Access", "Okta SSO / SAML",
        "Google Workspace administration", "RBAC and least privilege",
        "PowerShell automation", "Bash scripting",
        "IPsec and WireGuard VPN", "SonicWall / SonicOS firewalls",
        "RUCKUS Cloud wireless", "Cisco Umbrella", "SentinelOne EDR/XDR",
        "NinjaOne RMM", "ConnectWise Automate", "Datto BDR", "Business continuity",
    ],
    "hasCredential": [
        {"@type": "EducationalOccupationalCredential", "credentialCategory": "certification", "name": n}
        for n in [
            "CompTIA A+", "CompTIA Network+", "CompTIA Security+", "CompTIA Server+",
            "LPI Linux Essentials", "ISC2 Certified in Cybersecurity",
            "Microsoft MTA Windows Server Administration", "Microsoft MTA Security Fundamentals",
            "Microsoft MTA Networking Fundamentals", "Fortinet Certified Associate (FCA)",
        ]
    ],
    "sameAs": [
        "https://www.linkedin.com/in/arlytrenck",
        "https://www.credly.com/users/arlington-trenck",
    ],
}
WEBSITE = {
    "@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/",
    "name": "Arly Trenck", "publisher": {"@id": SITE + "/#person"}, "inLanguage": "en-US",
}
PROFILEPAGE = {
    "@type": "ProfilePage",
    "@id": SITE + "/#webpage",
    "url": SITE + "/",
    "name": "Arly Trenck — IT Systems Engineer & Infrastructure Architect",
    "description": "Professional profile of Arly Trenck, an IT Systems Engineer and Infrastructure Architect based in Fairfield, Connecticut.",
    "isPartOf": {"@id": SITE + "/#website"},
    "about": {"@id": SITE + "/#person"},
    "mainEntity": {"@id": SITE + "/#person"},
    "primaryImageOfPage": {"@id": SITE + "/#person"},
    "inLanguage": "en-US",
    "dateModified": date.today().isoformat(),
}


def read(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as f:
        return f.read()


def jsonld(page):
    graph = [WEBSITE, PERSON]
    if page["key"] == "home":
        graph.append(PROFILEPAGE)
    elif page["key"] != "404":
        graph.append({
            "@type": "WebPage",
            "@id": SITE + page["url"] + "#webpage",
            "url": SITE + page["url"],
            "name": page["title"],
            "description": page["desc"],
            "isPartOf": {"@id": SITE + "/#website"},
            "about": {"@id": SITE + "/#person"},
            "primaryImageOfPage": {"@id": SITE + "/#person"},
            "inLanguage": "en-US",
        })
        graph.append({
            "@type": "BreadcrumbList",
            "@id": SITE + page["url"] + "#breadcrumb",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
                {"@type": "ListItem", "position": 2, "name": page["crumb"], "item": SITE + page["url"]},
            ],
        })
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, indent=2)


def nav_html(current, mobile=False):
    out = []
    for label, href in NAV:
        active = (href == current)
        if mobile:
            cls = "block py-3 transition-colors text-paper/70 hover:text-paper"
            indent = "                "
        else:
            cls = ("transition-colors focus-visible:outline focus-visible:outline-2 "
                   "focus-visible:outline-paper focus-visible:outline-offset-4 "
                   "text-paper/70 hover:text-paper")
            indent = "                        "
        if active:
            cls += " !text-paper"
        aria = ' aria-current="page"' if active else ""
        out.append(f'{indent}<a href="{href}" class="{cls}"{aria}>{label}</a>')
    return "\n".join(out)


def build():
    head = read("partials", "head.html")
    header = read("partials", "header.html")
    footer = read("partials", "footer.html")

    if os.path.isdir(DIST):
        shutil.rmtree(DIST)
    os.makedirs(DIST)

    for page in PAGES:
        body = read("pages", page["key"] + ".html")
        h = (head
             .replace("{{TITLE}}", page["title"])
             .replace("{{DESC}}", page["desc"])
             .replace("{{ROBOTS}}", page.get("robots", ROBOTS_DEFAULT))
             .replace("{{CANONICAL}}", SITE + (page["url"] or "/404.html"))
             .replace("{{OG_TYPE}}", page["og_type"])
             .replace("{{OG_TITLE}}", page["title"])
             .replace("{{OG_DESC}}", page["desc"])
             .replace("{{PRELOAD}}", PRELOAD if page["preload"] else "")
             .replace("{{JSONLD}}", jsonld(page)))
        hdr = (header
               .replace("{{NAV_DESKTOP}}", nav_html(page["nav_key"], mobile=False))
               .replace("{{NAV_MOBILE}}", nav_html(page["nav_key"], mobile=True)))
        html = h + "\n" + hdr + "\n" + body.rstrip() + "\n" + footer
        dest = os.path.join(DIST, page["out"])
        os.makedirs(os.path.dirname(dest) or DIST, exist_ok=True)
        with open(dest, "w", encoding="utf-8") as f:
            f.write(html)
        print("  page  " + page["out"])

    lm = date.today().isoformat()
    rows = "".join(
        f'  <url>\n    <loc>{SITE}{p["url"]}</loc>\n    <lastmod>{lm}</lastmod>\n'
        f'    <changefreq>{p["changefreq"]}</changefreq>\n    <priority>{p["priority"]}</priority>\n  </url>\n'
        for p in PAGES if p["url"]
    )
    with open(os.path.join(DIST, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n'
                '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + rows + "</urlset>\n")
    print("  sitemap.xml")

    with open(os.path.join(DIST, "robots.txt"), "w", encoding="utf-8") as f:
        f.write("User-agent: *\nAllow: /\n\nSitemap: https://trenck.net/sitemap.xml\n")
    print("  robots.txt")

    for name in ("fa", "img", "headshot.jpg", "og-card.jpg"):
        src = os.path.join(ROOT, name)
        if not os.path.exists(src):
            print("  WARN missing asset: " + name)
            continue
        dst = os.path.join(DIST, name)
        (shutil.copytree if os.path.isdir(src) else shutil.copy2)(src, dst)
        print("  asset " + name)
    wk_src = os.path.join(ROOT, "staged-changes", ".well-known", "security.txt")
    if os.path.exists(wk_src):
        os.makedirs(os.path.join(DIST, ".well-known"), exist_ok=True)
        shutil.copy2(wk_src, os.path.join(DIST, ".well-known", "security.txt"))
        print("  asset .well-known/security.txt")

    css = os.path.join(ROOT, "styles.css")
    if os.path.exists(css):
        shutil.copy2(css, os.path.join(DIST, "styles.css"))
        print("  asset styles.css (pre-existing; rebuild with Tailwind + finalize.py)")

    print("done -> " + DIST)


if __name__ == "__main__":
    build()

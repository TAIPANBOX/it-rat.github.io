#!/usr/bin/env python3
"""Write the structured data every page should carry, from facts already on it.

Nothing here is invented: names, descriptions and repository URLs are read out
of each page's own <head> and hero, so the JSON-LD cannot drift away from what
a visitor sees. No ratings, no review counts, no prices we do not publish.

Run from the repo root:  python3 tools/seo.py   (idempotent)
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://it-rat.com"
MARK_OPEN = "<!-- seo:auto -->"
MARK_CLOSE = "<!-- /seo:auto -->"

GUIDES = {
    "ai-agent-governance.html": "AI agent governance",
    "finops-for-ai.html": "FinOps for AI",
    "ai-agent-security.html": "AI agent security",
    "mcp-security.html": "MCP security",
    "agent-identity.html": "Agent identity and authentication",
    "ai-observability-vs-governance.html": "AI observability vs governance",
    "one-incident-end-to-end.html": "One incident, end to end",
    "what-runs-where.html": "What runs where and what it costs",
    "first-alert.html": "From zero to your first alert",
    "two-sites.html": "Two sites, one control plane, no VPN",
    "what-is-proven.html": "What is proven and what is not",
    # Added 2026-08-29. Written 2026-08-11 and left out of every generator, so
    # its JSON-LD had been frozen since that day: it still described a page
    # holding a comparison table and a section of competitors' strengths, both
    # of which came off the page on 2026-08-28.
    "agent-tooling-compared.html": "Three shapes of agent tooling",
}

SERVICE_PAGES = [
    "services/engram.html", "services/tokenfuse.html", "services/wardryx.html",
    "services/idryx.html", "services/qryx.html", "services/verdryx.html",
    "services/mockryx.html", "services/heraldyx.html", "services/pocket.html",
    "services/trailryx.html", "services/platform.html", "services/costcrew.html",
    "services/vouchryx.html",
    # Added 2026-08-29. The room was written on 2026-08-10 and never listed
    # here, so it was the one indexable page on this site carrying no JSON-LD
    # while sitting in the sitemap next to fourteen pages that do.
    "services/scopyx.html",
    # Added 2026-09-25. Optional add-on, cat "proof" in the registry; needs
    # SERVICE_PAGES like every other room so its JSON-LD is not silently
    # skipped the way scopyx's was for three weeks.
    "services/typryx.html",
]


def registry_names():
    """The names the rail, the footer and the palette already use for each page."""
    js = (ROOT / "assets/site.js").read_text(encoding="utf-8")
    block = re.search(r"const STACK = \[(.*?)\n\];", js, re.S)
    out = {}
    for line in block.group(1).splitlines() if block else []:
        m = re.search(r'name:"([^"]+)".*?href:"([^"]+)"', line)
        if m:
            out[m.group(2)] = m.group(1)
    return out


NAMES = registry_names()


def head_bits(html, path=""):
    title = re.search(r"<title>(.*?)</title>", html, re.S)
    desc = re.search(r'<meta name="description" content="(.*?)"', html, re.S)
    canon = re.search(r'<link rel="canonical" href="([^"]+)"', html)
    repo = re.search(r'href="(https://github\.com/TAIPANBOX/[a-z0-9-]+)"', html)
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S)
    name = re.sub(r"<[^>]+>", "", h1.group(1)).split(".")[0].strip() if h1 else ""
    return dict(
        title=re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", title.group(1))).strip() if title else "",
        desc=desc.group(1) if desc else "",
        url=canon.group(1) if canon else "",
        repo=repo.group(1) if repo else "",
        name=NAMES.get(path, name),
    )


def ld(obj):
    return ('<script type="application/ld+json">'
            + json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
            + "</script>")


def organization():
    return {
        "@type": "Organization",
        "@id": f"{SITE}/#org",
        "name": "IT-RAT",
        "url": f"{SITE}/",
        "logo": f"{SITE}/apple-touch-icon.png",
        "image": f"{SITE}/assets/og.png",
        "email": "itratmail@gmail.com",
        "description": ("The authors of open-source governance for AI agents: runtime spend "
                        "control, policy, memory, identity, cryptography, quality and "
                        "pre-production drills for AI agents. Apache-2.0."),
        "sameAs": [
            "https://github.com/TAIPANBOX",
            "https://www.linkedin.com/in/yurii-kostiuk-778900ab/",
            "https://www.linkedin.com/in/tania-fedirko-9bb1a5136/",
        ],
        "founder": [
            {"@type": "Person", "name": "Yurii Kostiuk",
             "jobTitle": "Lead Security Architect",
             "sameAs": "https://www.linkedin.com/in/yurii-kostiuk-778900ab/"},
            {"@type": "Person", "name": "Tania Fedirko",
             "jobTitle": "FinOps Expert",
             "sameAs": "https://www.linkedin.com/in/tania-fedirko-9bb1a5136/"},
        ],
        "knowsAbout": ["AI agent governance", "FinOps for AI", "Zero Trust", "Identity and access management",
                       "Post-quantum cryptography", "Cloud security"],
    }


def website():
    return {"@type": "WebSite", "@id": f"{SITE}/#website", "url": f"{SITE}/",
            "name": "IT-RAT", "publisher": {"@id": f"{SITE}/#org"}, "inLanguage": "en"}


def breadcrumbs(bits):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "IT-RAT", "item": f"{SITE}/"},
        {"@type": "ListItem", "position": 2, "name": "The stack", "item": f"{SITE}/#stack"},
        {"@type": "ListItem", "position": 3, "name": bits["name"], "item": bits["url"]},
    ]}


def software(bits, free=True):
    app = {
        "@type": "SoftwareApplication",
        "name": bits["name"],
        "url": bits["url"],
        "description": bits["desc"],
        "applicationCategory": "DeveloperApplication",
        "operatingSystem": "Linux, macOS",
        "publisher": {"@id": f"{SITE}/#org"},
        "isAccessibleForFree": free,
    }
    if bits["repo"]:
        app["codeRepository"] = bits["repo"]
    if free:
        app["license"] = "https://www.apache.org/licenses/LICENSE-2.0"
        app["offers"] = {"@type": "Offer", "price": "0", "priceCurrency": "USD"}
    return app


def faq(html):
    """Read the visible FAQ back out of the page.

    Google's rule is that the marked-up answer must be the answer on the
    page, so the only safe source for this is the page itself.
    """
    block = re.search(r"<!-- faq:auto -->(.*?)<!-- /faq:auto -->", html, re.S)
    if not block:
        return None
    items = []
    for m in re.finditer(r"<summary>(.*?)</summary>\s*<div class=\"a\">(.*?)</div>\s*</details>",
                         block.group(1), re.S):
        q = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", m.group(1))).strip()
        a = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", m.group(2))).strip()
        if q and a:
            items.append({"@type": "Question", "name": q,
                          "acceptedAnswer": {"@type": "Answer", "text": a}})
    if not items:
        return None
    return {"@type": "FAQPage", "mainEntity": items}


# The six original guides went up on 2026-07-26 and keep that date. A page
# added later needs its own, because datePublished is a machine-readable claim
# and a wrong one is worse than an absent one: it tells a crawler this page is
# older than it is, on a site whose whole argument is that its claims are
# checkable. Add the date here when a guide is added.
PUBLISHED = {
    "agent-tooling-compared.html": "2026-08-11",
    "first-alert.html": "2026-08-04",
    "two-sites.html": "2026-09-27",
    "one-incident-end-to-end.html": "2026-08-04",
    "what-runs-where.html": "2026-08-04",
    "what-is-proven.html": "2026-08-04",
}


def article(bits, name, published="2026-07-26"):
    return {
        "@type": "TechArticle",
        "headline": bits["title"].split("\u00b7")[0].strip(),
        "name": name,
        "url": bits["url"],
        "description": bits["desc"],
        "inLanguage": "en",
        "datePublished": published,
        "dateModified": published,
        "author": {"@id": f"{SITE}/#org"},
        "publisher": {"@id": f"{SITE}/#org"},
        "mainEntityOfPage": bits["url"],
    }


def guide_crumbs(bits, name):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "IT-RAT", "item": f"{SITE}/"},
        {"@type": "ListItem", "position": 2, "name": name, "item": bits["url"]},
    ]}


def collection(bits, items):
    """The guides hub: a page whose point is the list on it."""
    return [{
        "@type": "CollectionPage",
        "url": bits["url"],
        "name": bits["title"].split("\u00b7")[0].strip(),
        "description": bits["desc"],
        "inLanguage": "en",
        "isPartOf": {"@id": f"{SITE}/#website"},
        "publisher": {"@id": f"{SITE}/#org"},
        "mainEntity": {
            "@type": "ItemList",
            "itemListElement": [
                {"@type": "ListItem", "position": i + 1, "name": name,
                 "url": f"{SITE}/{href}"}
                for i, (href, name) in enumerate(items)
            ],
        },
    }, {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "IT-RAT", "item": f"{SITE}/"},
        {"@type": "ListItem", "position": 2, "name": "Guides", "item": bits["url"]},
    ]}]


def defined_terms(html, bits):
    """A glossary is a set of terms; say so, from the visible definitions."""
    terms = []
    for m in re.finditer(r'<dt id="([^"]+)">(.*?)</dt>\s*<dd>(.*?)</dd>', html, re.S):
        name = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", m.group(2))).strip()
        desc = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", m.group(3))).strip()
        if name and desc:
            terms.append({"@type": "DefinedTerm", "name": name, "description": desc,
                          "url": f"{bits['url']}#{m.group(1)}"})
    if not terms:
        return None
    return {"@type": "DefinedTermSet", "name": "Glossary of agent-governance terms",
            "url": bits["url"], "description": bits["desc"], "hasDefinedTerm": terms}


def write(path, graph):
    p = ROOT / path
    h = p.read_text(encoding="utf-8")
    block = MARK_OPEN + "\n" + ld({"@context": "https://schema.org", "@graph": graph}) + "\n" + MARK_CLOSE
    if MARK_OPEN in h:
        h2 = re.sub(re.escape(MARK_OPEN) + r".*?" + re.escape(MARK_CLOSE), lambda _: block, h, flags=re.S)
    else:
        h2 = h.replace("</head>", block + "\n</head>", 1)
    if h2 == h:
        print(f"{path:28} unchanged")
        return 0
    p.write_text(h2, encoding="utf-8")
    print(f"{path:28} written")
    return 1


def main():
    n = 0
    idx_html = (ROOT / "index.html").read_text(encoding="utf-8")
    idx = head_bits(idx_html, "index.html")
    graph = [organization(), website(),
             {"@type": "WebPage", "url": f"{SITE}/", "name": idx["title"],
              "description": idx["desc"], "isPartOf": {"@id": f"{SITE}/#website"}}]
    q = faq(idx_html)
    if q:
        graph.append(q)
    n += write("index.html", graph)

    # Genaryx is Apache-2.0 and public like the seven services under it. This
    # block used to say free=False and strip the repository, from the months it
    # was going to be the one thing we sold. The prose was rewritten when that
    # stopped being true; the markup was not, so search engines kept reading
    # "isAccessibleForFree": false and describing a paid product back to people.
    # Machine-readable claims outlive the copy that contradicts them.
    ent_html = (ROOT / "genaryx.html").read_text(encoding="utf-8")
    ent = head_bits(ent_html, "genaryx.html")
    ent_app = software(ent)
    # You reach it in a browser. Saying so here is what keeps the description
    # from drifting back into "desktop console".
    ent_app["@type"] = ["SoftwareApplication", "WebApplication"]
    ent_app["browserRequirements"] = "Requires a modern browser with WebAuthn support"
    ent_graph = [ent_app, breadcrumbs(ent)]
    q = faq(ent_html)
    if q:
        ent_graph.append(q)
    n += write("genaryx.html", ent_graph)

    hub_html = (ROOT / "guides.html").read_text(encoding="utf-8")
    hub = head_bits(hub_html, "guides.html")
    n += write("guides.html", collection(hub, list(GUIDES.items())))

    gl_html = (ROOT / "glossary.html").read_text(encoding="utf-8")
    gl = head_bits(gl_html, "glossary.html")
    gl_graph = [defined_terms(gl_html, gl), guide_crumbs(gl, "Glossary")]
    n += write("glossary.html", [g for g in gl_graph if g])

    for path, name in GUIDES.items():
        html = (ROOT / path).read_text(encoding="utf-8")
        bits = head_bits(html, path)
        graph = [article(bits, name, PUBLISHED.get(path, "2026-07-26")), guide_crumbs(bits, name)]
        q = faq(html)
        if q:
            graph.append(q)
        n += write(path, graph)

    for path in SERVICE_PAGES:
        html = (ROOT / path).read_text(encoding="utf-8")
        bits = head_bits(html, path)
        if not bits["name"] or not bits["url"]:
            sys.exit(f"{path}: could not read a name or canonical, refusing to guess")
        app = software(bits)
        if path == "services/pocket.html":
            # Pocket runs on iPhone and Apple Watch. The generic line says Linux and macOS.
            app["operatingSystem"] = "iOS, watchOS"
        graph = [app, breadcrumbs(bits)]
        q = faq(html)
        if q:
            graph.append(q)
        n += write(path, graph)

    # Sphere gets four lines of its own rather than a place in SERVICE_PAGES,
    # because the generic service branch would state three things about it that
    # its own page denies. Apache-2.0, when the repository is MIT and the
    # footer says so. "Linux, macOS", when the app runs on iPhone
    # and Apple Watch. And a breadcrumb through "The stack", when the first sentence of
    # the page is that it is not part of the stack.
    #
    # It had no JSON-LD at all until 2026-08-29, which is how it avoided saying
    # anything false; that is not the same as being right, because it sits in
    # the sitemap and is indexed like every other page here. Machine-readable
    # claims outlive the copy that contradicts them, and a licence is the worst
    # of them to get wrong.
    sp_html = (ROOT / "services/sphere.html").read_text(encoding="utf-8")
    sp = head_bits(sp_html, "services/sphere.html")
    if sp["name"] != "Sphere":
        sys.exit(f"services/sphere.html: read the name as {sp['name']!r}, refusing to guess")
    sp_app = software(sp)
    sp_app["operatingSystem"] = "iOS, watchOS"
    sp_app["applicationCategory"] = "LifestyleApplication"
    sp_app["license"] = "https://opensource.org/licenses/MIT"
    n += write("services/sphere.html", [sp_app, guide_crumbs(sp, sp["name"])])

    print(f"\n{n} file(s) updated")


if __name__ == "__main__":
    main()

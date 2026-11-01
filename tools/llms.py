#!/usr/bin/env python3
"""Publish the machine-readable half of the site.

Three artefacts, all generated from the pages themselves so they cannot
drift:

  <page>.md        a clean markdown mirror of every content page
  /llms.txt        the index an AI reader is meant to start from
  /llms-full.txt   every guide concatenated, for a one-fetch read
  /mcp-index.json  the same map as data, for the docs MCP server

The HTML here is ours and predictable, so this is a narrow converter for
our own markup rather than a general one: it keeps headings, paragraphs,
lists, tables, code spans, command blocks and the FAQ, and drops the chrome
(nav, footer, scripts, SVG, decorative markup) that means nothing without a
browser.

Run from the repo root:  python3 tools/llms.py
"""
import html as htmlmod
import json
import pathlib
import re
import sys
from urllib.parse import urljoin

from stackguides import service_guides

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://it-rat.com"

GUIDES = [
    ("guides.html", "Guides index"),
    ("ai-agent-governance.html", "AI agent governance"),
    ("finops-for-ai.html", "FinOps for AI"),
    ("ai-agent-security.html", "AI agent security"),
    ("mcp-security.html", "MCP security"),
    ("agent-identity.html", "Agent identity and authentication"),
    ("glossary.html", "Glossary of agent-governance terms"),
    ("ai-observability-vs-governance.html", "AI observability vs governance"),
    ("one-incident-end-to-end.html", "One incident, end to end"),
    ("what-runs-where.html", "What runs where and what it costs"),
    ("first-alert.html", "From zero to your first alert"),
    ("two-sites.html", "Two sites, one control plane, no VPN"),
    ("what-is-proven.html", "What is proven and what is not"),
    # Added 2026-08-29, and this one had already gone wrong rather than merely
    # being absent. The twin was written on 2026-08-11 and never regenerated,
    # so it went on serving the comparison table and the section of
    # competitors' strengths for a day after both came off the page itself.
    ("agent-tooling-compared.html", "Three shapes of agent tooling"),
    # Added 2026-10-16 with the guide per room.
    ("security-by-design.html", "Security by design"),
    ("stack-guide.html", "How the numbers were produced"),
    ("install.html", "Install the stack, all of it or one service at a time"),
    ("changes-2026-10.html", "What changed in the stack, 1 to 15 October 2026"),
]
# Then one guide per room in STACK, derived rather than listed (see
# tools/stackguides.py). They are guides like the rest: listed under Guides in
# llms.txt, concatenated into llms-full.txt, kind "guide" in mcp-index.json.
GUIDES += [(path, f"{s['name']} guide") for path, s in service_guides()]
SERVICES = [
    ("services/tokenfuse.html", "TokenFuse, the money plane"),
    ("services/costcrew.html", "CostCrew, the finops plane"),
    ("services/vouchryx.html", "Vouchryx, the delegation plane"),
    ("services/wardryx.html", "Wardryx, the policy plane"),
    ("services/idryx.html", "Idryx, the access plane"),
    ("services/engram.html", "Engram, the knowledge plane"),
    ("services/qryx.html", "Qryx, the crypto plane"),
    ("services/keyryx.html", "Keyryx, the key custody and witness plane"),
    ("services/verdryx.html", "Verdryx, the quality plane"),
    ("services/mockryx.html", "Mockryx, the pre-production plane"),
    ("services/heraldyx.html", "Heraldyx, the alerts plane"),
    ("services/scopyx.html", "Scopyx, the egress plane"),
    ("services/trailryx.html", "Trailryx, the record"),
    ("services/platform.html", "Platform, the shared contract"),
    # Added 2026-08-29. It is in the STACK registry, on the rail, in the money
    # shelf of the footer and in the sitemap, and it was the only page there
    # with no markdown twin. Its plane in the registry is "out of band", which
    # is what it is: the switch that is deliberately not in the box.
    ("services/pocket.html", "TokenFuse Pocket, the out-of-band kill switch"),
    # Added 2026-09-25. Optional add-on, cat "proof" in the registry.
    ("services/typryx.html", "Typryx, typed answers"),
]
OTHER = [
    ("index.html", "IT-RAT, open-source governance for AI agents"),
    ("stack.html", "The stack: every service, with its room and its guide"),
    ("genaryx.html", "Genaryx, the console over the stack"),
]
ALL = OTHER + GUIDES + SERVICES


def strip_chrome(body):
    for pat in (r"<header\b.*?</header>", r"<footer\b.*?</footer>",
                r"<script\b.*?</script>", r"<style\b.*?</style>",
                r"<svg\b.*?</svg>", r"<canvas\b.*?</canvas>",
                r"<!--.*?-->"):
        body = re.sub(pat, " ", body, flags=re.S | re.I)
    return body


def text(s, page):
    s = re.sub(r"<(?:span|b|strong|em|i)\b[^>]*class=\"[^\"]*mono[^\"]*\"[^>]*>(.*?)</\w+>", r"`\1`", s, flags=re.S)
    s = re.sub(r"<code\b[^>]*>(.*?)</code>", r"`\1`", s, flags=re.S)
    s = re.sub(r"<(?:b|strong)\b[^>]*>(.*?)</(?:b|strong)>", r"**\1**", s, flags=re.S)
    s = re.sub(r'<a\b[^>]*href="([^"]+)"[^>]*>(.*?)</a>', lambda m: link(m.group(1), m.group(2), page), s, flags=re.S)
    s = re.sub(r"<[^>]+>", " ", s)
    s = htmlmod.unescape(s)
    return re.sub(r"[ \t ]+", " ", s).strip()


def link(href, label, page):
    """Turn an href into the absolute URL a reader of the twin can follow.

    The twin is read on its own, away from its page, so a relative href is
    resolved against the page's own URL the way a browser resolves it. `page`
    is the page's repo-relative path: "tokenfuse.html" from services/engram.html
    is services/tokenfuse.html, "../guides.html" is guides.html, and "#run" from
    costcrew-guide.html is that guide's URL with the fragment. Absolute http(s)
    and mailto links are kept as they are.
    """
    label = re.sub(r"<[^>]+>", "", label).strip()
    if href.startswith("http") or href.startswith("mailto"):
        return f"[{label}]({href})"
    return f"[{label}]({urljoin(SITE + '/' + page, href)})"


def code_block(s):
    """A command block as the lines a reader would type.

    `<div class="cmd">` breaks its lines with <br> and wraps comments in a span;
    `<pre><code>` carries real newlines and backslash continuations. Both keep
    their line structure, which text() would collapse into one line.
    """
    s = re.sub(r"<br\s*/?>", "\n", s)
    s = htmlmod.unescape(re.sub(r"<[^>]+>", "", s))
    lines = [ln.rstrip() for ln in s.split("\n")]
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    return "\n".join(lines)


COMMAND = re.compile(r"<div class=\"cmd\">(.*?)</div>|<pre\b[^>]*>(.*?)</pre>", re.S)


def dropped_commands(body, md):
    """The commands on a page that its twin does not carry.

    Until 2026-11-01 the element pass below had no case for command blocks, so
    40 of the 42 on the site were missing from their twins: install.md said how
    to add delegation and never gave the one line that installs the stack. This
    reads the blocks by its own means rather than through code_block(), so a
    converter that stops carrying them cannot also stop this from noticing.
    Whitespace is compared loosely, because a command inside a list item reaches
    the twin on one line.
    """
    flat = " ".join(md.split())
    missing = []
    for m in COMMAND.finditer(body):
        raw = m.group(1) if m.group(1) is not None else m.group(2)
        cmd = " ".join(htmlmod.unescape(re.sub(r"<[^>]+>", " ", raw)).split())
        if cmd and cmd not in flat:
            missing.append(cmd)
    return missing


def table(block, page):
    rows = []
    for tr in re.findall(r"<tr\b[^>]*>(.*?)</tr>", block, re.S):
        cells = [text(c, page) for c in re.findall(r"<t[hd]\b[^>]*>(.*?)</t[hd]>", tr, re.S)]
        if cells:
            rows.append(cells)
    if not rows:
        return ""
    width = max(len(r) for r in rows)
    rows = [r + [""] * (width - len(r)) for r in rows]
    out = ["| " + " | ".join(rows[0]) + " |", "|" + "---|" * width]
    out += ["| " + " | ".join(r) + " |" for r in rows[1:]]
    return "\n".join(out)


def card_links(body):
    """Keep the link on a card that IS a link.

    The hub's cards are an <a> wrapped round a heading and a paragraph, and its
    service rows an <a> round a name and a plane. The element pass below reads
    the heading and the paragraph and never sees the <a> around them, so until
    2026-10-16 guides.md named every guide and linked to none of them, and the
    rows did not appear in it at all. A card's link moves onto its heading; a
    row becomes a list item that links.
    """
    def card(m):
        href, inner = m.group(1), m.group(2)
        return re.sub(r"<h3\b[^>]*>(.*?)</h3>",
                      lambda h: f'<h3><a href="{href}">{h.group(1)}</a></h3>',
                      inner, count=1, flags=re.S)

    def row(m):
        href, inner = m.group(1), m.group(2)
        name = re.search(r"<b>(.*?)</b>", inner, re.S)
        plane = re.search(r'<span class="pl">(.*?)</span>', inner, re.S)
        label = name.group(1) if name else href
        return (f'<li><a href="{href}">{label}</a>'
                + (f", {plane.group(1)}" if plane else "") + "</li>")

    body = re.sub(r'<a class="gcard"[^>]*?href="([^"]+)"[^>]*>(.*?)</a>', card, body, flags=re.S)
    return re.sub(r'<a class="svc-row"[^>]*?href="([^"]+)"[^>]*>(.*?)</a>', row, body, flags=re.S)


def to_markdown(path, title):
    raw = (ROOT / path).read_text(encoding="utf-8")
    desc = re.search(r'<meta name="description" content="([^"]*)"', raw)
    body = card_links(strip_chrome(raw.split("<body", 1)[1]))

    out = []
    # one pass over the elements we care about, in document order
    for m in re.finditer(
            r"<h1\b[^>]*>(?P<h1>.*?)</h1>"
            r"|<h2\b[^>]*>(?P<h2>.*?)</h2>"
            r"|<h3\b[^>]*>(?P<h3>.*?)</h3>"
            r"|<table\b[^>]*>(?P<table>.*?)</table>"
            r"|<div class=\"cmd\">(?P<cmd>.*?)</div>"
            r"|<pre\b[^>]*>(?P<pre>.*?)</pre>"
            r"|<summary\b[^>]*>(?P<q>.*?)</summary>"
            r"|<li\b[^>]*>(?P<li>.*?)</li>"
            r"|<p\b[^>]*>(?P<p>.*?)</p>"
            r"|<div class=\"a\">(?P<a>.*?)</div>"
            r"|<div class=\"n\">(?P<n>.*?)</div>"
            r"|<div class=\"fix\">(?P<fix>.*?)</div>"
            r"|<div class=\"k\">(?P<k>.*?)</div>"
            r"|<dt\b[^>]*>(?P<dt>.*?)</dt>"
            r"|<dd\b[^>]*>(?P<dd>.*?)</dd>", body, re.S):
        kind = m.lastgroup
        val = m.group(kind)
        if kind == "table":
            t = table(val, path)
            if t:
                out.append(t)
            continue
        if kind in ("cmd", "pre"):
            c = code_block(val)
            if c:
                out.append("```\n" + c + "\n```")
            continue
        t = text(val, path)
        if not t or len(t) < 2:
            continue
        if kind == "h1":
            out.append(f"# {t}")
        elif kind == "h2":
            out.append(f"## {t}")
        elif kind == "h3":
            out.append(f"### {t}")
        elif kind == "q":
            out.append(f"**Q: {t}**")
        elif kind == "dt":
            out.append(f"**{t}**")
        elif kind == "dd" and out and out[-1].startswith("**"):
            out[-1] = f"{out[-1]}\n{t}"
        elif kind == "n":
            out.append(f"*{t}*")
        elif kind == "li":
            out.append(f"- {t}")
        elif kind == "a" and out and out[-1].startswith("**Q:"):
            # keep a question and its answer in one block: a search that finds
            # the question should hand back the answer with it
            out[-1] = f"{out[-1]}\n{t}"
        else:
            out.append(t)

    head = [f"<!-- {SITE}/{path} -->", f"# {title}"]
    if desc:
        head.append(f"> {htmlmod.unescape(desc.group(1))}")
    md = "\n\n".join(head + [o for o in out if not o.startswith("# ")]) + "\n"
    md = re.sub(r"\n{3,}", "\n\n", md)
    missing = dropped_commands(body, md)
    if missing:
        sys.exit(f"{path.replace('.html', '.md')} drops a command its page shows: "
                 f"{missing[0][:80]!r}. Teach to_markdown() the block's markup, "
                 f"then run this again.")
    return md, len(COMMAND.findall(body))


def alternate_links():
    """Point a machine at the markdown twin of the page it is reading."""
    n = 0
    for path, _ in ALL:
        p = ROOT / path
        h = p.read_text(encoding="utf-8")
        depth = "../" if "/" in path else ""
        tag = (f'<link rel="alternate" type="text/markdown" '
               f'href="{SITE}/{path.replace(".html", ".md")}">')
        if 'type="text/markdown"' in h:
            h2 = re.sub(r'<link rel="alternate" type="text/markdown"[^>]*>', tag, h)
        else:
            h2 = h.replace('<link rel="stylesheet"', tag + "\n<link rel=\"stylesheet\"", 1)
        if h2 != h:
            p.write_text(h2, encoding="utf-8")
            n += 1
    print(f"{n} page(s) now advertise their markdown mirror")


def main():
    written = {}
    commands = 0
    for path, title in ALL:
        md, n = to_markdown(path, title)
        commands += n
        out = ROOT / path.replace(".html", ".md")
        out.write_text(md, encoding="utf-8")
        written[path] = md
        print(f"{path.replace('.html', '.md'):40} {len(md.split()):5} words")
    # The command check above measures nothing on a site with no commands, and
    # a check that measures nothing must say so rather than pass.
    if not commands:
        sys.exit("no command block on any page, so the check that twins carry "
                 "them measured nothing. If the markup changed, teach COMMAND.")

    # The hub's twin is how a machine reader finds the guides, so it has to
    # reach every one of them. A guide the hub does not link is a guide only a
    # search engine can find.
    # The one exception, since 2026-10-20: the guide for each service is listed
    # on the Stack page beside its room, not on the hub, and llms.txt below
    # still names every one of them.
    by_room = {p for p, _ in service_guides()}
    unlinked = [p for p, _ in GUIDES
                if p != "guides.html" and p not in by_room
                and f"({SITE}/{p})" not in written["guides.html"]
                and f"({SITE}/{p}#" not in written["guides.html"]]
    if unlinked:
        sys.exit(f"guides.md links to none of: {', '.join(unlinked)}. Link each from "
                 f"guides.html as a card, then run this again.")

    def line(path, title):
        raw = (ROOT / path).read_text(encoding="utf-8")
        d = re.search(r'<meta name="description" content="([^"]*)"', raw)
        d = htmlmod.unescape(d.group(1)) if d else ""
        return f"- [{title}]({SITE}/{path.replace('.html', '.md')}): {d}"

    llms = [
        "# IT-RAT",
        "",
        "> Open-source governance for AI agents: runtime spend control, policy decisions,",
        "> identity and delegation, egress, memory with provenance, cryptography posture,",
        "> quality scoring, pre-production drills, alerting and an auditable record.",
        "> Each plane installs on its own, self-hosted on infrastructure the operator",
        "> owns, plus Genaryx, the console over them. Every part of it is Apache-2.0.",
        "",
        "Every page below is available as markdown at the same path with a .md extension.",
        "",
        "## Guides",
        "",
    ] + [line(p, t) for p, t in GUIDES] + [
        "",
        "## Services",
        "",
    ] + [line(p, t) for p, t in SERVICES] + [
        "",
        "## Other",
        "",
    ] + [line(p, t) for p, t in OTHER] + [
        "",
        "## Optional",
        "",
        f"- [Everything, concatenated]({SITE}/llms-full.txt): all guides in one file.",
        f"- [Machine index]({SITE}/mcp-index.json): the same map as JSON, used by the docs MCP server.",
        f"- [Docs MCP server]({SITE}/mcp-security.html): these docs are also served over MCP; the server is in the site repo under mcp/, stdio, no dependencies.",
        f"- [Source](https://github.com/TAIPANBOX): the services themselves.",
        "",
    ]
    (ROOT / "llms.txt").write_text("\n".join(llms), encoding="utf-8")

    full = ["# IT-RAT guides, concatenated", ""]
    for path, title in GUIDES:
        full.append(written[path])
        full.append("\n---\n")
    (ROOT / "llms-full.txt").write_text("\n".join(full), encoding="utf-8")

    index = {
        "site": SITE,
        "name": "IT-RAT",
        "description": "Open-source governance for AI agents, and the guides that explain it.",
        "license": "Apache-2.0",
        "pages": [
            {
                "url": f"{SITE}/{p}",
                "markdown": f"{SITE}/{p.replace('.html', '.md')}",
                "title": t,
                "kind": ("guide" if (p, t) in GUIDES else "service" if (p, t) in SERVICES else "page"),
                "description": htmlmod.unescape(
                    (re.search(r'<meta name="description" content="([^"]*)"',
                               (ROOT / p).read_text(encoding="utf-8")) or re.match("", "")).group(1)
                    if re.search(r'<meta name="description" content="([^"]*)"',
                                 (ROOT / p).read_text(encoding="utf-8")) else ""),
            }
            for p, t in ALL
        ],
    }
    (ROOT / "mcp-index.json").write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    alternate_links()
    print(f"\nllms.txt, llms-full.txt and mcp-index.json written ({len(ALL)} pages)")


if __name__ == "__main__":
    main()

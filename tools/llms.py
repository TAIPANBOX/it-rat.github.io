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
lists, tables, code spans and the FAQ, and drops the chrome (nav, footer,
scripts, SVG, decorative markup) that means nothing without a browser.

Run from the repo root:  python3 tools/llms.py
"""
import html as htmlmod
import json
import pathlib
import re

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
    ("what-is-proven.html", "What is proven and what is not"),
]
SERVICES = [
    ("services/tokenfuse.html", "TokenFuse, the money plane"),
    ("services/wardryx.html", "Wardryx, the policy plane"),
    ("services/idryx.html", "Idryx, the access plane"),
    ("services/engram.html", "Engram, the knowledge plane"),
    ("services/qryx.html", "Qryx, the crypto plane"),
    ("services/verdryx.html", "Verdryx, the quality plane"),
    ("services/mockryx.html", "Mockryx, the pre-production plane"),
    ("services/heraldyx.html", "Heraldyx, the alerts plane"),
    ("services/scopyx.html", "Scopyx, the egress plane"),
    ("services/trailryx.html", "Trailryx, the record"),
    ("services/platform.html", "Platform, the shared contract"),
]
OTHER = [
    ("index.html", "IT-RAT, the agent-governance stack"),
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


def text(s):
    s = re.sub(r"<(?:span|b|strong|em|i)\b[^>]*class=\"[^\"]*mono[^\"]*\"[^>]*>(.*?)</\w+>", r"`\1`", s, flags=re.S)
    s = re.sub(r"<code\b[^>]*>(.*?)</code>", r"`\1`", s, flags=re.S)
    s = re.sub(r"<(?:b|strong)\b[^>]*>(.*?)</(?:b|strong)>", r"**\1**", s, flags=re.S)
    s = re.sub(r'<a\b[^>]*href="([^"]+)"[^>]*>(.*?)</a>', lambda m: link(m.group(1), m.group(2)), s, flags=re.S)
    s = re.sub(r"<[^>]+>", " ", s)
    s = htmlmod.unescape(s)
    return re.sub(r"[ \t ]+", " ", s).strip()


def link(href, label):
    label = re.sub(r"<[^>]+>", "", label).strip()
    if href.startswith("http") or href.startswith("mailto"):
        return f"[{label}]({href})"
    href = re.sub(r"^\.\./", "", href).lstrip("/")
    return f"[{label}]({SITE}/{href})"


def table(block):
    rows = []
    for tr in re.findall(r"<tr\b[^>]*>(.*?)</tr>", block, re.S):
        cells = [text(c) for c in re.findall(r"<t[hd]\b[^>]*>(.*?)</t[hd]>", tr, re.S)]
        if cells:
            rows.append(cells)
    if not rows:
        return ""
    width = max(len(r) for r in rows)
    rows = [r + [""] * (width - len(r)) for r in rows]
    out = ["| " + " | ".join(rows[0]) + " |", "|" + "---|" * width]
    out += ["| " + " | ".join(r) + " |" for r in rows[1:]]
    return "\n".join(out)


def to_markdown(path, title):
    raw = (ROOT / path).read_text(encoding="utf-8")
    desc = re.search(r'<meta name="description" content="([^"]*)"', raw)
    body = strip_chrome(raw.split("<body", 1)[1])

    out = []
    # one pass over the elements we care about, in document order
    for m in re.finditer(
            r"<h1\b[^>]*>(?P<h1>.*?)</h1>"
            r"|<h2\b[^>]*>(?P<h2>.*?)</h2>"
            r"|<h3\b[^>]*>(?P<h3>.*?)</h3>"
            r"|<table\b[^>]*>(?P<table>.*?)</table>"
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
            t = table(val)
            if t:
                out.append(t)
            continue
        t = text(val)
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
    return re.sub(r"\n{3,}", "\n\n", md)


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
    for path, title in ALL:
        md = to_markdown(path, title)
        out = ROOT / path.replace(".html", ".md")
        out.write_text(md, encoding="utf-8")
        written[path] = md
        print(f"{path.replace('.html', '.md'):40} {len(md.split()):5} words")

    def line(path, title):
        raw = (ROOT / path).read_text(encoding="utf-8")
        d = re.search(r'<meta name="description" content="([^"]*)"', raw)
        d = htmlmod.unescape(d.group(1)) if d else ""
        return f"- [{title}]({SITE}/{path.replace('.html', '.md')}): {d}"

    llms = [
        "# IT-RAT",
        "",
        "> The open-source agent-governance stack: runtime spend control, policy decisions,",
        "> identity, memory with provenance, cryptography posture, quality scoring and",
        "> pre-production drills for AI agents. Seven services under Apache-2.0, self-hosted",
        "> on infrastructure the operator owns, plus Genaryx, the console over them.",
        "> Every part of it is Apache-2.0.",
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
        "description": "The open-source agent-governance stack, and the guides that explain it.",
        "license": "Apache-2.0 for the seven services",
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

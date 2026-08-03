#!/usr/bin/env python3
"""Regenerate the shared footer on every page from one source of truth.

The stack registry lives in assets/site.js and already feeds the rail, the
dots, the arrows and the palette. This reads that same array and writes the
footer chips into the HTML as real links: a crawler should not have to run
JavaScript to find nine internal pages, and a reader should not have to know
that Cmd-K exists.

Run from the repo root:  python3 tools/footer.py
It is idempotent: it replaces the block between the footer markers.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

BRAND_SVG = ('<svg class="glyph" viewBox="0 0 24 24" fill="none">'
             '<path d="M13.5 2 5 13.2h5.1L9.4 22l9-11.8h-5.3L13.5 2Z" fill="#F4B23E"/></svg>')
FLAG_SVG = ('<svg style="display:inline-block;width:15px;height:11px;vertical-align:-1px;'
            'margin:0 3px;border-radius:2px" viewBox="0 0 3 2" role="img" aria-label="Ukraine">'
            '<title>Ukraine</title><rect width="3" height="1" fill="#005BBB"/>'
            '<rect y="1" width="3" height="1" fill="#FFD500"/></svg>')

# page path -> (root prefix, the tail of the copyright line)
PAGES = {
    "genaryx.html": ("", "Apache-2.0"),
    "ai-agent-governance.html": ("", ""),
    "finops-for-ai.html": ("", ""),
    "ai-agent-security.html": ("", ""),
    "mcp-security.html": ("", ""),
    "agent-identity.html": ("", ""),
    "glossary.html": ("", ""),
    "guides.html": ("", ""),
    "ai-observability-vs-governance.html": ("", ""),
    "console.html": ("", ""),
    "404.html": ("/", ""),
    "services/engram.html": ("../", "Apache-2.0"),
    "services/idryx.html": ("../", "Apache-2.0"),
    "services/mockryx.html": ("../", "Apache-2.0"),
    "services/platform.html": ("../", "Apache-2.0"),
    "services/qryx.html": ("../", "Apache-2.0"),
    "services/tokenfuse.html": ("../", "Apache-2.0"),
    "services/verdryx.html": ("../", "Apache-2.0"),
    "services/wardryx.html": ("../", "Apache-2.0"),
}


def stack():
    """Parse the registry out of site.js rather than keeping a second copy."""
    js = (ROOT / "assets/site.js").read_text(encoding="utf-8")
    block = re.search(r"const STACK = \[(.*?)\n\];", js, re.S)
    if not block:
        sys.exit("site.js: could not find the STACK registry")
    out = []
    for line in block.group(1).splitlines():
        m = re.search(r'id:"([^"]+)".*?name:"([^"]+)".*?color:"([^"]+)".*?href:"([^"]+)"', line)
        if m:
            out.append(dict(zip(("id", "name", "color", "href"), m.groups())))
    if len(out) < 5:
        sys.exit("site.js: parsed too few services, refusing to write a broken footer")
    return out


def chips(root, here):
    out = []
    for s in stack():
        dot = f'<i style="background:{s["color"]}"></i>{s["name"]}'
        if s["id"] == here:
            out.append(f'<span class="foot-chip here" aria-current="page">{dot}</span>')
        else:
            out.append(f'<a class="foot-chip" href="{root}{s["href"]}">{dot}</a>')
    return "".join(out)


def cols(root, here):
    return f"""    <div class="cols">
      <div>
        <a class="brand" href="{root}index.html" style="margin-bottom:10px">{BRAND_SVG}IT<b>-</b>RAT</a>
        <div class="foot-note" style="margin-top:8px;max-width:34ch">The agent-governance stack, Apache-2.0.</div>
      </div>
      <div class="foot-groups">
        <div class="foot-group"><div class="l">the stack</div>
          <div class="foot-chips">{chips(root, here)}</div>
        </div>
      </div>
      <div>
        <a href="{root}guides.html">Guides</a>
        <a href="{root}index.html#people">The people</a>
        <a href="{root}index.html#contact">Leave a note</a>
        <a href="mailto:itratmail@gmail.com">itratmail@gmail.com</a>
        <a href="https://github.com/TAIPANBOX" target="_blank" rel="noopener">GitHub &#8599;</a>
        <!-- Not in the top bar: it is addressed to someone who already runs a
             console of their own, over their own tunnel, which is a returning
             operator rather than a visitor. The primary slot belongs to the
             action a stranger should take. -->
        <a href="{root}console.html">Go to your console</a>
      </div>
    </div>"""


def footer(path, root, tail, here):
    # Only the service pages carry a licence tag; everywhere else the line
    # ends at the flag. An empty tail means exactly that, separator included.
    suffix = f' &#183; {tail}' if tail else ''
    return (f'<footer class="footer">\n  <div class="wrap">\n<!-- footer:auto -->\n'
            f'{cols(root, here)}\n<!-- /footer:auto -->\n'
            f'    <div class="foot-note">&#169; 2026 IT-RAT {FLAG_SVG}{suffix}</div>\n'
            f'  </div>\n</footer>')


def service_id(path):
    h = (ROOT / path).read_text(encoding="utf-8")
    m = re.search(r'<body[^>]*data-service="([^"]+)"', h)
    return m.group(1) if m else ""


def rail_cards():
    """The corridor rail on the home page, as real links rather than JS output."""
    out = []
    for s in stack():
        out.append(
            f'      <a class="card hover svc" style="--c:{s["color"]}" href="{s["href"]}" data-dir="fwd">\n'
            f'        <span class="head"><span class="g"></span>'
            f'<span class="mono" style="font-size:11px;color:var(--faint)">{s["id"]}</span>'
            f'<span class="plane">{s["plane"]}</span></span>\n'
            f'        <h3>{s["name"]}</h3>\n'
            f'        <p class="what">{s["what"]}.</p>\n'
            f'        <span class="go">open the room</span>\n'
            f'      </a>')
    return "\n".join(out)


def main():
    written = 0
    for path, (root, tail) in PAGES.items():
        p = ROOT / path
        h = p.read_text(encoding="utf-8")
        new = footer(path, root, tail, service_id(path))
        if "<footer" in h:
            h2 = re.sub(r"<footer.*?</footer>", lambda _: new, h, count=1, flags=re.S)
        else:  # 404 has none yet
            h2 = h.replace("<script src=", new + "\n\n<script src=", 1)
        if h2 != h:
            p.write_text(h2, encoding="utf-8")
            written += 1
        print(f"{path:28} {'written' if h2 != h else 'unchanged'}")

    # the home page keeps its desk-agent block; only the injected slot changes
    p = ROOT / "index.html"
    h = p.read_text(encoding="utf-8")
    slot = re.search(r'<div class="foot-groups"[^>]*>.*?</div>\s*(?=\n)', h, re.S)
    static = ('<div class="foot-groups">\n'
              '        <div class="foot-group"><div class="l">the stack</div>\n'
              f'          <div class="foot-chips">{chips("", "")}</div>\n'
              '        </div>\n      </div>')
    if slot and 'id="foot-stack"' in slot.group(0):
        h = h[:slot.start()] + static + h[slot.end():]
        # the inline renderer is now dead weight
        h = re.sub(r'\n  /\* One flat group.*?\n  document\.getElementById\("foot-stack"\)\.innerHTML =\n.*?\n.*?\n', "\n", h, flags=re.S)
        h = re.sub(r'\n  const chip = s => .*?\n', "\n", h, flags=re.S)
        p.write_text(h, encoding="utf-8")
        print(f"{'index.html':28} written")
        written += 1
    else:
        print(f"{'index.html':28} unchanged (slot already static)")
    print(f"\n{written} file(s) updated")


if __name__ == "__main__":
    main()

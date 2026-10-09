#!/usr/bin/env python3
"""Own the order of the top bar's controls, and the console link inside it.

Why a script for a hand-written bar. The bar genuinely differs per page: the
index carries its own anchors, a guide page spells its links out ("All guides",
"The stack"), a service page carries a crumb instead. There is nothing to
generate wholesale. What there IS is a shape every page has to share, and a
shape pasted into 28 files is a shape that drifts. This owns exactly two things
and touches nothing else in the bar:

  1. the jump button is present, and last
  2. the order: the tb-cta, then the content links, then Console, then jump

`Console` went in on 2026-08-05 (@decided), moving out of the footer where it had
started to read as a leftover. console.html gets no link to itself; its crumb
already says where you are.

**The jump button came out on 2026-08-05 and went back in the same day**, and
the measurement is why: on 26 of the 28 pages it was the ONLY visible trigger
for the palette. index.html carries a second one, "Jump anywhere", but that is
one page. The keyboard opens the palette anywhere, with Cmd/Ctrl+K or `/`, so
what removal cost was the tap target, and a phone has no keyboard. It stays,
and the duplicate in the hero went instead (@decided).

**The tb-cta goes FIRST, and that reverses what site.css used to say about it**
(@decided 2026-08-05). That rule read "it sits at the right edge, after the
content links, because that is where every user has been taught to look", which
is the pattern for an account entry. This one is "Live demo", which is not an
account entry: it is the first thing worth doing on the site. The comment in
site.css was rewritten rather than left to contradict the markup.

Run from the repo root:  python3 tools/topbar.py
Idempotent: it rewrites the block between the spacer and the end of the bar.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SPACER = '<span class="spacer"></span>'
CONSOLE = '<a class="tb-link" href="{root}console.html">Console</a>'

# path -> root prefix. console.html is deliberately absent from the console
# link but still needs its bar ordered, so it carries a None root instead.
PAGES = {
    "index.html": "",
    "genaryx.html": "",
    "ai-agent-governance.html": "",
    "finops-for-ai.html": "",
    "ai-agent-security.html": "",
    "mcp-security.html": "",
    "agent-identity.html": "",
    "glossary.html": "",
    "guides.html": "",
    "ai-observability-vs-governance.html": "",
    "one-incident-end-to-end.html": "",
    "what-runs-where.html": "",
    "first-alert.html": "",
    "two-sites.html": "",
    "what-is-proven.html": "",
    # Added 2026-08-29. Its own commit said it was "listed in all seven places";
    # it was in none of the four generators, so its bar, its JSON-LD and its
    # markdown twin have all been frozen since the day it was written.
    "agent-tooling-compared.html": "",
    "console.html": None,
    "404.html": "/",
    "services/costcrew.html": "../",
    "services/vouchryx.html": "../",
    "services/engram.html": "../",
    "services/idryx.html": "../",
    "services/mockryx.html": "../",
    "services/heraldyx.html": "../",
    "services/trailryx.html": "../",
    "services/pocket.html": "../",
    "services/sphere.html": "../",
    "services/platform.html": "../",
    "services/qryx.html": "../",
    # Added 2026-08-29, missing since the room was written on 2026-08-10.
    "services/scopyx.html": "../",
    "services/tokenfuse.html": "../",
    "services/verdryx.html": "../",
    "services/wardryx.html": "../",
    "services/typryx.html": "../",
}

ELEMENT = re.compile(r'<(a|button)\b[^>]*>.*?</\1>', re.S)

# Byte for byte what every page carries today. It is written out here so a page
# that somehow lost the button gets it back rather than silently going without.
JUMP = ('<button class="kbd-hint" data-cmdk type="button">'
        '<span>jump</span><kbd>&#8984;K</kbd></button>')

written = 0

for path, root in PAGES.items():
    p = ROOT / path
    if not p.exists():
        sys.exit(f"{path}: in the page list and not on disk.")
    h = p.read_text(encoding="utf-8")

    start = h.find(SPACER)
    if start < 0:
        sys.exit(f"{path}: no spacer in the top bar, so there is no block to order. "
                 "Fix the anchor rather than letting this write somewhere arbitrary.")
    start += len(SPACER)
    end = h.find("\n  </div>", start)
    if end < 0:
        sys.exit(f"{path}: found the spacer but not the end of the bar after it.")

    block = h[start:end]
    items = ELEMENT.findall(block)  # returns tags; take the full matches instead
    items = [m.group(0) for m in ELEMENT.finditer(block)]
    if not items:
        sys.exit(f"{path}: the bar has no controls after the spacer, which cannot be right.")

    # Everything with a fixed place comes out, so its position is rebuilt from
    # this list rather than from wherever it happened to sit.
    jump = [i for i in items if 'kbd-hint' in i]
    cta = [i for i in items if 'tb-cta' in i]
    items = [i for i in items
             if 'kbd-hint' not in i and 'tb-cta' not in i and 'console.html' not in i]

    ordered = cta + items
    if root is not None:
        ordered.append(CONSOLE.format(root=root))
    ordered += (jump or [JUMP])
    items = ordered

    want = "".join("\n    " + i for i in items)
    if block == want:
        continue
    p.write_text(h[:start] + want + h[end:], encoding="utf-8")
    print(f"{path:36} written")
    written += 1

print(f"\n{written} file(s) updated. Order: cta, content links, Console, jump. "
      "console.html has no link to itself.")

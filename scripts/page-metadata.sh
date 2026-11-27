#!/usr/bin/env bash
# Holds invariants 1 and 2 of CLAUDE.md: page metadata is measured at publish,
# and the machine-readable claims move with the copy.
#
# This is the public face of the business. A truncated title in a search result
# is the first thing a stranger sees, and a contradictory pair of robots
# directives is resolved by somebody else's algorithm, not by us.
#
# WHAT IT KNOWS ABOUT THIS SITE, because a check that does not know its domain
# produces a confident wrong number:
#
#   Content pages       must carry a title within 70 characters and a
#                       description between 25 and 160.
#   Redirect pages      carry a canonical and a refresh, and legitimately have
#                       no description. /enterprise and /products are these.
#   Generated output    /demo is a built single-page app. Its head is produced
#                       by a bundler, not authored here, so measuring its copy
#                       measures the bundler.
#
# The first version of this check counted three pages as failures. All three
# were the two redirects and the built app.
#
# WHAT IT DOES NOT REQUIRE. og:description deliberately differs from the meta
# description on every page here: the search snippet is held under 160 and the
# social card is allowed to run longer. Requiring them to match would be
# requiring a mistake.
#
# This file is the ONE copy of this check.

set -uo pipefail
cd "$(git rev-parse --show-toplevel)" || exit 1

python3 - <<'PY'
import html
import pathlib
import re
import sys

TITLE_MAX = 70
DESC_MIN, DESC_MAX = 25, 160

problems = []


def note(msg):
    problems.append(msg)


# Every quoted attribute pattern below captures its opening quote and closes on
# the same kind of quote (a backreference), so an apostrophe inside a
# double-quoted value is text, not the end of it. The value is the LAST group,
# whatever the pattern before it captured.
def attr(text, pattern):
    m = re.search(pattern, text, re.S | re.I)
    return html.unescape(m.group(m.lastindex)).strip() if m else None


pages = sorted(p for p in pathlib.Path(".").rglob("*.html")
               if not any(part.startswith(".") for part in p.parts))
if not pages:
    print("FAIL: no HTML pages found, so this check measured nothing")
    sys.exit(1)

content = redirects = generated = 0

for p in pages:
    text = p.read_text(errors="ignore")
    name = str(p)

    is_redirect = bool(
        re.search(r'http-equiv=["\']refresh', text, re.I)
        or "location.replace(" in text
    )
    is_generated = bool(re.search(r'<script type="module" crossorigin src="\./assets/', text))

    title = attr(text, r"<title>(.*?)</title>")
    desc = attr(text, r'<meta\s+name=(["\'])description\1\s+content=(["\'])(.*?)\2')
    og_title = attr(text, r'<meta\s+property=(["\'])og:title\1\s+content=(["\'])(.*?)\2')
    has_canonical = bool(re.search(r'rel=(["\'])canonical\1', text, re.I))
    has_noindex = bool(
        re.search(r'name=(["\'])robots\1[^>]*content=(["\'])(?:(?!\2).)*?noindex', text, re.I | re.S)
    )

    # ------------------------------------------------ invariant 2, every page
    if has_canonical and has_noindex:
        note(
            f"{name} carries a canonical AND a noindex. The two say opposite "
            f"things: one asks for this URL to be the authoritative version, the "
            f"other asks for it to be dropped. Which one wins is somebody else's "
            f"algorithm. Keep the one that matches the intent and delete the other."
        )

    if title and og_title and title != og_title:
        note(f"{name}: og:title and <title> disagree.\n    title:    {title}\n    og:title: {og_title}")

    # ------------------------------------------------ invariant 1, by page class
    if is_generated:
        generated += 1
        continue
    if is_redirect:
        redirects += 1
        if not has_canonical:
            note(f"{name} is a redirect with no canonical, so the destination is a guess")
        continue

    content += 1
    if not title:
        note(f"{name} has no title")
    elif len(title) > TITLE_MAX:
        note(f"{name}: title is {len(title)} characters, over {TITLE_MAX}, so it truncates in a result")
    if not desc:
        note(f"{name} has no meta description")
    elif not (DESC_MIN <= len(desc) <= DESC_MAX):
        note(f"{name}: description is {len(desc)} characters, outside {DESC_MIN}-{DESC_MAX}")

if problems:
    for p in problems:
        print(f"FAIL: {p}")
    print()
    print("This is the public face of the business. A truncated title is the first")
    print("thing a stranger sees. See CLAUDE.md invariants 1 and 2.")
    sys.exit(1)

print(
    f"OK: {content} content pages within title and description limits, "
    f"{redirects} redirects, {generated} generated;"
)
print("    no page carries both a canonical and a noindex, and og:title matches <title>.")
PY

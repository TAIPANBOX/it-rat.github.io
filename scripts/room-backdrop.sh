#!/usr/bin/env bash
# Holds invariant 14 of CLAUDE.md: every room draws a backdrop of its own.
#
# WHY THIS EXISTS
#
# assets/ambient.js draws two layers on a room. The deep field is a fixed
# canvas behind the whole page, a drifting node graph with formulas and math
# glyphs, tinted with the page accent. The motif is a figure in the hero,
# drawn from that room's own domain. A page gets the first by loading the
# script, and the second by being named in the script's MAP, under the id its
# <body data-service> carries.
#
# Both are opt-in, and missing either is silent. On 2026-10-26 the Genaryx
# room, the first room in the corridor, had never loaded the script at all:
# not since it was born as enterprise.html in July. Every other room drew its
# field and its figure, Genaryx drew a flat page, and the first person to
# notice was a reader comparing two rooms. Pocket loaded the script and was
# absent from MAP, so its hero was blank. Neither showed up in any gate,
# because no gate read the script.
#
# The collision is the older fault of the same kind. Three times a room
# borrowed another room's figure (trailryx declared engram's `web`; scopyx and
# heraldyx both declared wardryx's `boundary`), and each time two rooms in the
# corridor drew one picture. A motif is supposed to say which room you are in.
#
# WHAT IT CHECKS, per room, where a room is every entry in the STACK registry
# in assets/site.js (found, not listed, for the reason invariant 10 gives):
#
#   1. the page loads assets/ambient.js, so the deep field is drawn;
#   2. its <body data-service> is the room's id, which is what the script
#      looks the motif up by;
#   3. it has a hero (an element with class svc-hero), where the motif mounts;
#   4. a motif is named for it: the hero's own data-motif if it sets one,
#      otherwise MAP[id] in assets/ambient.js;
#   5. that motif is defined in MOTIFS;
#   6. no other room draws the same motif.
#
# WHAT IT DOES NOT CHECK. Whether a motif looks like anything, whether it says
# anything true about its room, or whether it can be seen behind the hero's
# text. Those still need somebody to open the page. Sphere is not in STACK
# and so is not a room here; that is the same derived exemption invariant 11
# makes.

set -uo pipefail
cd "$(dirname "$0")/.." || exit 1

python3 - <<'PY'
import pathlib
import posixpath
import re
import sys

ROOT = pathlib.Path.cwd()

js_path = ROOT / "assets/site.js"
js = js_path.read_text(encoding="utf-8") if js_path.exists() else ""
block = re.search(r"const STACK = \[(.*?)\n\];", js, re.S)
rooms = []
for line in block.group(1).splitlines() if block else []:
    m = re.search(r'id:"([^"]+)".*?href:"([^"]+)"', line)
    if m:
        rooms.append(m.groups())
if not rooms:
    print("UNJUDGEABLE: no rooms found in the STACK registry in assets/site.js, so this")
    print("     measured nothing. No room failing is not every room having a backdrop.")
    sys.exit(1)

amb_path = ROOT / "assets/ambient.js"
amb = amb_path.read_text(encoding="utf-8") if amb_path.exists() else ""
map_block = re.search(r"const MAP=\{(.*?)\};", amb, re.S)
motif_map = dict(re.findall(r'(\w+):"(\w+)"', map_block.group(1))) if map_block else {}
motifs = set(re.findall(r"^([a-z]\w*)\(ctx,w,h,t", amb, re.M))
if not motif_map or not motifs:
    print("UNJUDGEABLE: assets/ambient.js has no MAP or defines no motifs, so this")
    print("     measured nothing. A room cannot be checked against a list that is not there.")
    sys.exit(1)

problems = []
drawn_by = {}
for rid, href in rooms:
    page = ROOT / href
    if not page.exists():
        problems.append(f"{rid}: the registry points at {href} and it is not on disk")
        continue
    h = page.read_text(encoding="utf-8")
    base = posixpath.dirname(href)

    srcs = {posixpath.normpath(posixpath.join(base, re.split(r"[#?]", s)[0]))
            for s in re.findall(r'<script\b[^>]*\bsrc="([^"]+)"', h)}
    if "assets/ambient.js" not in srcs:
        problems.append(f"{rid}: {href} does not load assets/ambient.js, so it draws no "
                        f"deep field and no motif")

    body = re.search(r'<body\b[^>]*\bdata-service="([^"]*)"', h)
    if not body or body.group(1) != rid:
        found = body.group(1) if body else "nothing"
        problems.append(f"{rid}: <body data-service> says {found!r}, and the script looks the "
                        f"motif up by that, not by the registry")

    hero = re.search(r'<[a-z]+\b[^>]*\bclass="(?:[^"]*\s)?svc-hero(?:\s[^"]*)?"[^>]*>', h)
    if not hero:
        problems.append(f"{rid}: {href} has no svc-hero element for the motif to mount in")
        continue
    override = re.search(r'\bdata-motif="([^"]+)"', hero.group(0))
    motif = override.group(1) if override else motif_map.get(rid)
    if not motif:
        problems.append(f"{rid}: no motif in assets/ambient.js MAP, so the hero is blank")
        continue
    if motif not in motifs:
        problems.append(f"{rid}: names the motif {motif!r}, and assets/ambient.js defines no such motif")
        continue
    drawn_by.setdefault(motif, []).append(rid)
    print(f"     {rid:10} {motif}")

for motif, ids in sorted(drawn_by.items()):
    if len(ids) > 1:
        problems.append(f"{', '.join(ids)}: share the motif {motif!r}, so two rooms draw one picture")

if problems:
    print()
    for line in problems:
        print("FAIL " + line)
    print(f"\n{len(problems)} problem(s) across {len(rooms)} rooms. See CLAUDE.md invariant 14:")
    print("every room draws a backdrop of its own.")
    sys.exit(1)

print(f"OK: {len(rooms)} rooms, each loading the deep field and each drawing a motif no")
print("    other room draws.")
PY

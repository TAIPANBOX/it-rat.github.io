#!/usr/bin/env python3
"""Turn each room's architecture diagram into a standalone animated SVG.

Every service page already carries a hand-drawn schematic in the site's own
visual language. On the site it is animated by `assets/diagram.js`; in a GitHub
README there is no JavaScript, so the flow has to be carried by SMIL inside the
file itself. This lifts the diagram out of the page, wraps it so it renders
standalone (`xmlns`, an opaque background so it stays legible on a light GitHub
theme, a title), and animates the arrows: a coloured pulse marches along every
wire, and the service's own box breathes in its accent.

The output is one file per service under assets/img/readme/diagrams/, copied
from there into each service repo's README.

Run from the repo root:  python3 tools/readmediagrams.py
"""
import hashlib
import pathlib
import re
import sys
from xml.etree import ElementTree

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "assets/img/readme/diagrams"
PAD = 18
BG = "#0A0E13"
DUR = 2.4  # seconds for one pulse to cross a wire, whatever that wire's length

# id -> (page, accent, the one-line title screen readers and tooltips get,
#        a fingerprint of the drawing that sentence describes)
ROOMS = {
    "tokenfuse": ("services/tokenfuse.html", "#F4B23E",
                  "TokenFuse: every agent call priced and gated in-line, one gateway by default and a raft cluster build when you need several",
                  "3e4d28cb348a"),
    "wardryx":   ("services/wardryx.html", "#2DD4BF",
                  "Wardryx: the PEP asks per request, the PDP answers allow, deny or hold, and an optional Verdryx event file can add a hold",
                  "f6f11fc1593f"),
    "idryx":     ("services/idryx.html", "#34D399",
                  "Idryx: identity sources feed one graph that emits alerts, an Agent-BOM and proposed diffs",
                  "900e8fdfa8bd"),
    "qryx":      ("services/qryx.html", "#B48CFF",
                  "Qryx: the estate is swept into a crypto inventory and scored for post-quantum risk",
                  "a7c5b48f983c"),
    "keyryx":   ("services/keyryx.html", "#FDE68A",
                  "Keyryx: custody signs for granted consumers and publishes key sets, and a read-only witness signs its tree heads and reports a rewritten stream",
                  "a3658b56d2c4"),
    "verdryx":   ("services/verdryx.html", "#FF7AA2",
                  "Verdryx: outcomes judged and priced per resolved case, with drift watched over time",
                  "c61935fe07c8"),
    "mockryx":   ("services/mockryx.html", "#FF8A5B",
                  "Mockryx: hostile scenarios driven at the gateway, with the guardrails asserted",
                  "74a7940b101b"),
    "engram":    ("services/engram.html", "#6C7BFF",
                  "Engram: agent memory in one SQLite file, recalled with provenance",
                  "df03b29d9082"),
    "platform":  ("services/platform.html", "#93A8C4",
                  "Platform: fifteen registered sources write one envelope, twelve of them onto one NDJSON bus, "
                  "and five consumers read it back",
                  "5fa985abd7da"),
    "genaryx":   ("genaryx.html", "#B48CFF",
                  "Genaryx: one browser control room over the stack, reached only over the tunnel",
                  "9a774670aaf6"),
    "costcrew":  ("services/costcrew.html", "#7DD3A0",
                  "CostCrew: charges arrive from the connectors built so far (the TokenFuse FOCUS export, "
                  "seats, recommendations; the AWS and GCP billing exports are read, the Azure one is specified), a two-sided "
                  "detector opens anomalies, and an agent analyst drafts a fix a person posts or returns",
                  "ca3540b4d4e2"),
    "vouchryx":  ("services/vouchryx.html", "#8B9DFF",
                  "Vouchryx: a subject token, an actor token and a DPoP proof are exchanged for a "
                  "short-lived delegation token, verified offline and revoked by a polled list",
                  "b0b13590f130"),
    # Sourced from a standalone file rather than a page: the schematic on the
    # scopyx page is filled in by JavaScript as a request travels it, so a lift
    # of it renders five empty boxes. The file says the rest. Everything else
    # here, including this room, is generated the same way from that source.
    "scopyx":    ("assets/img/readme/sources/scopyx-gates.svg", "#F0ABFC",
                  "Scopyx: a request passes five gates in order, scheme, host, resolved addresses, "
                  "your policy and robots.txt, before anything leaves",
                  "d986b000dbe7"),
    "typryx":    ("services/typryx.html", "#60A5FA",
                  "Typryx: an ask crosses the door, template lookup, egress filter and hourly cap to a "
                  "swappable backend, stub, openai-logprobs or jev, and every answer or refusal is "
                  "journaled, with a calibration loop and the journal on the shared events volume",
                  "4b7b9704b075"),
}

# Rooms whose README diagram is drawn by hand, and the reason for each. This
# tool lifts a page's schematic, and for these the page and the README answer
# different questions, so lifting would replace an architecture diagram with a
# flow one and lose exactly what the README needs.
HAND_DRAWN = {
    "heraldyx": "the page draws the four checks one event passes; the README draws "
                "the census of which planes write the log and which read it",
    "trailryx": "the page draws a predicate becoming an authenticated index range; "
                "the README draws the transports, the plane boundary and the chain",
    "pocket":   "no repository carries a diagram for it, and the room is marked "
                "not wired in yet",
}


def diagram(page):
    """The first wide <svg> in the source is that room's schematic.

    The source is normally the room's own page, so the README and the site can
    never drift apart. Where it cannot be, it is a standalone .svg under
    assets/img/readme/sources/ that says in its own header why.
    """
    s = (ROOT / page).read_text(encoding="utf-8")
    for m in re.finditer(r'<svg\b[^>]*viewBox="([^"]+)"[^>]*>', s):
        vb = [float(v) for v in m.group(1).split()]
        if vb[2] < 300:
            continue
        return s[m.start(): s.index("</svg>", m.start()) + 6], vb
    raise SystemExit(f"no diagram found in {page}")


def pulses(svg, accent):
    """One travelling pulse per arrow, on a copy of each wire.

    Overlaying rather than replacing keeps the original wire visible, so the
    diagram still reads correctly wherever SMIL is ignored. `pathLength="100"`
    normalises every wire to the same 100 units, so a short hop and a long
    diagonal each take one full `DUR` to travel: without it the dash pattern is
    in user units and the pulse crawls across long wires and blinks past short
    ones. The negative `begin` starts each animation mid-flight, so the very
    first frame already reads as flowing rather than empty. The negative begins
    are by design: a pulse never starts late, so nothing sits at the origin. The
    whole group is in the reduced-motion group (rd-anim), so a reader who asks
    for reduced motion sees the still wires.
    """
    out = []
    wires = re.findall(r'<line\b[^>]*marker-end[^>]*/>', svg)
    wires += re.findall(r'<path\b[^>]*marker-end[^>]*/>', svg)
    for i, wire in enumerate(wires):
        tag = "line" if wire.startswith("<line") else "path"
        # Strip every attribute this function is about to set. Leaving one in
        # place does not lose an argument, it emits the attribute TWICE, and a
        # duplicate attribute is not valid XML: GitHub then renders nothing at
        # all. It cost nine working diagrams to miss one. costcrew and vouchryx
        # were the first rooms here with a dashed wire that also carries an
        # arrowhead, so `stroke-dasharray` survived the old list and both files
        # came out broken.
        geom = re.sub(r'\s(marker-end|stroke|stroke-width|stroke-dasharray|stroke-dashoffset'
                      r'|stroke-linecap|pathLength|class|style)="[^"]*"', "", wire[:-2])
        out.append(
            f'{geom} pathLength="100" stroke="{accent}" stroke-width="2.6" '
            f'stroke-linecap="round" stroke-dasharray="7 100" stroke-dashoffset="7">'
            f'<animate attributeName="stroke-dashoffset" from="7" to="-100" '
            f'dur="{DUR}s" begin="-{i * 0.37:.2f}s" repeatCount="indefinite"/>'
            f'</{tag}>'
        )
    return "\n  ".join(out)


def breathe(svg, accent):
    """Pulse the room's own box in its accent, the way the page does.

    The box itself stays still. A veil in the background colour sits on its
    outline and fades in and out, so the accent dips the way the page's box
    does. The veil is in the reduced-motion group (rd-anim), so a reader who
    asks for reduced motion gets the box at full strength and no motion.
    """
    m = re.search(r'<rect\b[^>]*stroke="' + re.escape(accent) + r'"[^>]*stroke-width="1.4"[^>]*/>', svg)
    if not m:
        return svg
    base = m.group(0)
    geom = re.sub(r'\s(fill|stroke|stroke-width|stroke-opacity|class|style|opacity)="[^"]*"', "", base[:-2])
    veil = (geom + f' fill="none" stroke="{BG}" stroke-width="1.6" class="rd-anim" opacity="0">'
            '<animate attributeName="opacity" values="0;.55;0" dur="3.4s" repeatCount="indefinite"/>'
            '</rect>')
    return svg[:m.end()] + veil + svg[m.end():]


def park_motion_tokens(svg):
    """Give every late-starting animateMotion token its delay inside its own timing.

    A token with `begin="Ns"` sits at the origin corner until it starts, which
    put a dot in the top-left of the picture on the page and in the lift. Its
    path stays absolute and its element stays at the origin, so the lift has no
    transform to compose with (SVG motion is additive to a transform, and a
    translate in front of an absolute path counts the offset twice). The delay
    moves into keyTimes: the token holds at the first point of its own path
    until the move starts, the same frame the page shows.

    Refuses anything it does not understand (a transform on the animated element,
    a path with other commands, a begin that is not a plain number of seconds)
    rather than guessing, because a guess here is a token in the wrong place.
    """
    def fix(m):
        el = m.group(0)
        if "transform=" in el:
            raise ValueError("animated element carries a transform: " + el[:120])
        begin = re.search(r'\sbegin="(-?[\d.]+)s"', el)
        if not begin or float(begin.group(1)) <= 0:
            return el
        if "keyTimes=" in el:
            raise ValueError("delayed token already has keyTimes: " + el[:120])
        delay = float(begin.group(1))
        dur = re.search(r'\sdur="([\d.]+)s"', el)
        if not dur:
            raise ValueError("delayed token has no dur: " + el[:120])
        move = float(dur.group(1))
        total = delay + move
        el = el.replace(begin.group(0), "")
        el = el.replace(dur.group(0), f' dur="{total:g}s" keyPoints="0;0;1" keyTimes="0;{delay/total:.5f};1" calcMode="linear"')
        return el
    return re.sub(r'<animateMotion\b[^>]*/>', fix, svg)


def build(room, page, accent, title):
    svg, vb = diagram(page)
    svg = park_motion_tokens(svg)
    x, y, w, h = vb[0] - PAD, vb[1] - PAD, vb[2] + PAD * 2, vb[3] + PAD * 2
    inner = breathe(svg, accent)
    # Strip the page-level wrapper; everything inside is reused verbatim.
    inner = inner[inner.index(">") + 1: inner.rindex("</svg>")]
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x:g} {y:g} {w:g} {h:g}" '
        f'width="{w:g}" height="{h:g}" role="img" aria-label="{title}">\n'
        f'  <title>{title}</title>\n'
        '  <style>@media (prefers-reduced-motion: reduce){.rd-anim{display:none}}</style>\n'
        f'  <rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" rx="16" fill="{BG}"/>\n'
        f'  <rect x="{x + .5:g}" y="{y + .5:g}" width="{w - 1:g}" height="{h - 1:g}" rx="15.5" '
        f'fill="none" stroke="rgba(255,255,255,.09)"/>\n'
        f'{inner}\n'
        f'  <g fill="none" class="rd-anim">\n  {pulses(svg, accent)}\n  </g>\n'
        f'</svg>\n'
    )


def valid_xml(svg, room):
    """An SVG that does not parse is a file GitHub renders as nothing.

    This is here because the duplicate-attribute bug above shipped nine correct
    files and two broken ones, and the only symptom was a red banner in a
    browser nobody had opened. A generator that can emit invalid XML should be
    the thing that notices.
    """
    try:
        ElementTree.fromstring(svg)
    except ElementTree.ParseError as e:
        raise SystemExit(f"{room}: the generated SVG does not parse, so GitHub would render "
                         f"nothing: {e}")


def fingerprint(svg):
    """A short digest of what the picture SAYS, so a redraw is visible here.

    The title beside each room is a hand-written sentence about a generated
    picture, and it becomes the file's <title> and its aria-label: what a
    screen reader is given instead of the diagram. Platform's said "seven
    emitters, one agent-event envelope, four consumers" for three weeks after
    the page was redrawn to twelve sources and five consumers, and nothing
    anywhere could notice, because a sentence about a drawing has nothing to
    compare itself with.

    So the drawing gets a fingerprint and the sentence is pinned to it. Redraw
    the diagram and this tool stops and asks whether the sentence still holds.

    It digests the TEXT of the diagram rather than the file, so moving a box or
    changing a colour does not ask a question there is no reason to ask, and
    adding, removing or rewording a label always does.
    """
    words = " ".join(re.sub(r"\s+", " ", t).strip()
                     for t in re.findall(r"<text\b[^>]*>(.*?)</text>", svg, re.S))
    return hashlib.sha256(words.encode("utf-8")).hexdigest()[:12]


def titles_match_their_drawings():
    """Every room's sentence is pinned to the drawing it describes."""
    stale = []
    for room, (page, accent, title, pin) in ROOMS.items():
        svg, _ = diagram(page)
        now = fingerprint(svg)
        if now != pin:
            stale.append((room, pin, now, title, page))
    if stale:
        lines = ["a diagram has been redrawn since its sentence was written, and that "
                 "sentence is what a screen reader is given instead of the picture:\n"]
        for room, pin, now, title, page in stale:
            lines.append(f'  {room}: {page}')
            lines.append(f'    it now says: "{title}"')
            lines.append(f"    read the drawing, fix the line if it no longer holds, then "
                         f"change the pin from {pin} to {now}\n")
        raise SystemExit("\n".join(lines))


def registry():
    """The room ids in STACK, which is the site's own list of what exists."""
    js = (ROOT / "assets/site.js").read_text(encoding="utf-8")
    block = re.search(r"STACK\s*=\s*\[(.*?)\n\]", js, re.S)
    if not block:
        raise SystemExit("assets/site.js: no STACK array found, so nothing can be checked against it")
    ids = re.findall(r'id\s*:\s*"([^"]+)"', block.group(1))
    if not ids:
        raise SystemExit("assets/site.js: STACK carries no id fields, so no room can be named")
    return set(ids)


def account_for_every_room():
    """Every room is generated or named as hand-drawn, in both directions.

    The header of this file used to say a room that leaves the site leaves the
    images with it, and that was only ever half true: ROOMS is a hand-kept dict,
    so a room ARRIVING was silently absent instead. Heraldyx and Trailryx were
    absent that way for a week, and nothing said so, because a dict that is
    never compared to anything cannot be short.
    """
    rooms, hand = set(ROOMS), set(HAND_DRAWN)
    both = rooms & hand
    if both:
        raise SystemExit(f"generated AND listed as hand-drawn, so one is a lie: {', '.join(sorted(both))}")
    missing = registry() - rooms - hand
    if missing:
        raise SystemExit(
            f"in STACK, neither generated nor excluded: {', '.join(sorted(missing))}. "
            "Add each to ROOMS, or to HAND_DRAWN with the reason its README diagram "
            "is not the one on its page."
        )
    stale = rooms - registry()
    if stale:
        raise SystemExit(f"generated but no longer in STACK: {', '.join(sorted(stale))}")


def main():
    account_for_every_room()
    titles_match_their_drawings()
    OUT.mkdir(parents=True, exist_ok=True)
    for room, (page, accent, title, _pin) in ROOMS.items():
        out = OUT / f"{room}.svg"
        svg = build(room, page, accent, title)
        valid_xml(svg, room)
        out.write_text(svg, encoding="utf-8")
        print(f"{out.relative_to(ROOT)}  {out.stat().st_size // 1024 or 1} KB")


if __name__ == "__main__":
    main()

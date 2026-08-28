#!/usr/bin/env bash
# Enforces invariant 3 of CLAUDE.md: a number on this site is a claim with an
# owner.
#
# WHAT MADE THIS NECESSARY, on 2026-08-04.
#
# The trailryx page said 1,031 tests across 28 crates while the repository ran
# 1,064 across 29, in two places, for about a week. The tokenfuse page said 513
# where its workspace runs 709, and nobody knows for how long. Neither figure was
# wrong when it was written, which is exactly why a person cannot be the check:
# the number does not change on the page when it changes in the repository, and
# there is nothing on the page that says when anybody last looked.
#
# WHAT THIS CAN AND CANNOT DO, stated because the difference is the whole value.
#
# It CANNOT tell you a figure is still true. This repository has no access to the
# other repositories' test suites, and adding a network call to a publish gate
# would trade a silent staleness for a flaky deploy.
#
# It CAN make the silent case impossible. Every number on a service page must
# appear in `numbers.json` with the same value, and every entry there must say
# which repository it came from, which command produces it, and when somebody
# last ran that command. Editing a page without touching the manifest fails.
# Adding a number nobody has ever reproduced is allowed and is REPORTED, because
# refusing it outright would only teach people to leave numbers off the page.
#
# So: a hard failure for disagreement, a loud line for anything unverified. The
# second is not decoration. It is the list somebody works through when they next
# have the repositories checked out.

set -uo pipefail

cd "$(dirname "$0")/.."

python3 - <<'PY'
import json
import pathlib
import re
import sys

manifest = pathlib.Path("numbers.json")
if not manifest.exists():
    print("FAIL: numbers.json is missing, so the pages' figures have no owner at all")
    sys.exit(1)

data = json.loads(manifest.read_text())
entries = data.get("entries", [])
if not entries:
    print("FAIL: numbers.json records no entries")
    sys.exit(1)

problems = 0
unverified = []

# Every figure a reader would take at face value.
#
# Widened on 2026-08-05 after this check walked straight past `70 documented and
# already fixed` on the platform page while stack-k8s counted 79. The first
# version knew four nouns and the page used a fifth, so a stale figure sat
# inside the very thing written to catch stale figures. A narrow pattern does
# not fail loudly; it reports OK about the part it happens to understand.
FIGURE = re.compile(
    r"[0-9][0-9,]*\s*(?:tests|crates|detectors|entries|documented|gotchas|scenarios|checks|invariants)"
)

# A version is a figure too, and on 2026-08-05 it was the one nobody owned.
# Four were stale on the live site at once: idryx and qryx said v0.2.0 against
# v0.3.0, engram said v2.2.1 against v2.4.1 (six days), and the platform page
# said agent-stack-go v0.4.0 in FOUR places, two of them inside install
# commands, because a tag had been cut in that repository an hour earlier. The
# check printed "no page states a number nobody owns" through all of it, since
# a version matches none of the nouns above.
VERSION = re.compile(r"\bv\d+\.\d+\.\d+\b")


def outside_scripts(text):
    """Page copy with <script> blocks removed.

    The two sweeps below deliberately read DIFFERENT text, and the difference
    was measured rather than assumed.

    A count is a state claim wherever it appears, including inside a script:
    trailryx states `1,064 tests` in one, and stripping scripts for FIGURE
    would silently stop owning it. Measured: that is the only figure affected,
    and losing it is not acceptable.

    A version is not. heraldyx carries `v0.2.3` in a script comment explaining
    when its path escaping changed, which is history and is true forever.
    Sweeping it would report a page as stating an unowned number, and a check
    that fires on correct copy is one everybody learns to skip. Measured:
    removing scripts drops exactly that one case and leaves seven real claims,
    one per page.
    """
    return re.sub(r"<script\b.*?</script>", " ", text, flags=re.S | re.I)

for e in entries:
    page = pathlib.Path(e["page"])
    claim = e["claim"]
    if not page.exists():
        print(f"FAIL: {e['page']} is in numbers.json and not in this repository")
        problems += 1
        continue

    text = page.read_text()
    # The page renders `·` as an entity, so compare against both forms rather
    # than against whichever one today's editor happened to leave behind. Only
    # when the claim HAS one: adding the two counts unconditionally doubles
    # every figure without a separator, because both forms are then the same
    # string. This check did exactly that on its first run and reported seven
    # pages as disagreeing with a manifest that was right about four of them.
    entity = claim.replace("·", "&#183;")
    found = text.count(claim) + (text.count(entity) if entity != claim else 0)
    expected = e.get("occurrences", 1)
    if found != expected:
        print(f"FAIL: {e['page']} should say {claim!r} {expected} time(s) and says it {found}")
        print("      Either the page changed and numbers.json did not, or the other way round.")
        problems += 1

    if e.get("status") == "wrong":
        print(f"FAIL: numbers.json records {e['page']} as WRONG: the page says {claim!r} "
              f"and the last run measured {e.get('measured_value')}")
        print("      Fix the page and the entry together, or say why it stands.")
        problems += 1

    if e.get("status") in (None, ""):
        print(f"FAIL: {e['page']} entry {claim!r} has no status")
        problems += 1

    if e.get("status") != "measured":
        unverified.append((e["page"], claim, e.get("status"), e.get("command")))

# A number spelled out in words, but ONLY inside structured data.
#
# A blanket sweep for spelled-out numbers was written, measured and thrown away
# on 2026-08-28. Across the site it fired on three correct sentences, and two of
# them are records of a run that happened: "the same three detectors fired
# against a real Postgres 16", "three of these five scenarios ran live". Those
# are true forever, like the version in heraldyx's script comment below, and a
# check that fails on correct copy is one everybody learns to skip.
#
# Inside JSON-LD the calculus is the opposite. A figure there is read by a
# machine and by nobody who could notice it had gone stale, and it is the copy
# that outlives the sentence it was lifted from. Measured on the same day: three
# figures live in structured data across the whole site and every one has an
# owner, so this fires on nothing that is right.
#
# It would have caught the case it was written for. idryx's FAQPage carried
# "Twenty-two deterministic detectors" while five places on the same page said
# 27, and the page shipped that way.
LD_FIGURE = re.compile(
    r"\b(?:[0-9][0-9,]*|One|Two|Three|Four|Five|Six|Seven|Eight|Nine|Ten|Eleven|Twelve|"
    r"Thirteen|Fourteen|Fifteen|Sixteen|Seventeen|Eighteen|Nineteen|Twenty|Thirty|Forty|"
    r"Fifty|Sixty|Seventy|Eighty|Ninety)(?:-[a-z]+)?\s+(?:deterministic\s+)?"
    r"(?:tests|crates|detectors|entries|documented|gotchas|scenarios|checks|invariants)",
    re.I,
)
LD_BLOCK = re.compile(
    r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', re.S | re.I
)


def structured_data(text):
    """Just the JSON-LD blocks, concatenated."""
    return " ".join(LD_BLOCK.findall(text))


# A number on a page that nobody put in the manifest is the case this whole file
# exists for, so it is found rather than assumed away.
#
# The .md twins are swept too, since 2026-08-28. They are published, llms.txt
# links them by URL, and until that day nothing read their figures: idryx.md
# carried "22 deterministic detectors" four times, and verdryx.md said 300 tests
# against a suite that collects 361. Both were invisible because this loop
# globbed *.html and stopped there.
managed = {(e["page"], e["claim"]) for e in entries}
pages = sorted(pathlib.Path("services").glob("*.html"))
pages += sorted(pathlib.Path("services").glob("*.md"))
for page in pages:
    text = page.read_text().replace("&#183;", "·")
    sweeps = [(FIGURE, text), (VERSION, outside_scripts(text))]
    if page.suffix == ".html":
        sweeps.append((LD_FIGURE, structured_data(text)))
    for pattern, subject in sweeps:
        for m in set(pattern.findall(subject)):
            if any(m in c for p, c in managed if p == str(page)):
                continue
            print(f"FAIL: {page} states {m!r} and nothing in numbers.json owns it")
            problems += 1

if unverified:
    print()
    print(f"{len(unverified)} figure(s) on this site have never been reproduced here:")
    for page, claim, status, command in unverified:
        where = command or "no command recorded"
        print(f"  {claim:<26} {page:<28} [{status}]  {where}")
    print("This is not a failure. It is the list to work through with those")
    print("repositories checked out, and it is printed every run so it cannot")
    print("quietly become the permanent state.")

if problems:
    print()
    print(f"{problems} problem(s). See CLAUDE.md invariant 3.")
    sys.exit(1)

measured = sum(1 for e in entries if e.get("status") == "measured")
print()
print(f"OK: {len(entries)} figures owned, {measured} reproduced here, "
      f"{len(unverified)} awaiting a run. No page states a number nobody owns.")
PY

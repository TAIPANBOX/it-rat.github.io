#!/usr/bin/env bash
#
# Fails when a page's generated blocks are stale, or when a page has none
# because no generator has ever heard of it.
#
# WHY THIS EXISTS
#
# Five tools in tools/ write into these pages: the footer, the top bar, the
# visible FAQ, the JSON-LD, and the markdown twins with the llms.txt index.
# Every one of them keeps a hand-written list of which pages it writes to, and
# nothing compared those five lists with each other or with the pages on disk.
#
# WHAT THAT COST, both found on 2026-08-29 and both months old:
#
#   agent-tooling-compared.html was published on 2026-08-11 and appeared in
#   NONE of the five lists, though its own commit message said it was "listed
#   in all seven places". Its footer was three categories out of date. Its
#   markdown twin, which is served at it-rat.com/agent-tooling-compared.md, was
#   still publishing the competitor comparison table and a section headed
#   "Where they are plainly better than us" a day after both were taken off the
#   page itself by decision. A generated file nobody regenerates is
#   worse than a hand-written one, because everybody assumes it is current.
#
#   services/scopyx.html was published on 2026-08-10 and was the one indexable
#   page on this site with no JSON-LD at all, sitting in the sitemap beside
#   fourteen pages that had it.
#
# WHAT IT CHECKS
#
#   A. Coverage, which is about pages no generator knows.
#      Every page outside demo/ that is not noindex carries a canonical, a
#      JSON-LD block and a sitemap entry; every page in the STACK registry
#      carries a markdown twin.
#
#   B. Freshness, which is about pages they know and have not written since.
#      Copies every tracked file to a temporary directory, runs all five
#      generators there, and requires that they change nothing. A generator is
#      idempotent by design, so anything it would rewrite is drift.
#
# WHY B COPIES THE TREE
#
# A gate must not rewrite the thing it is judging. Running the generators in
# place would "fix" the drift it is meant to report, and the run after it would
# be green with nobody the wiser.
#
# WHAT IT DOES NOT CHECK
#
# Whether the generated text is any good, or whether a page SHOULD have a FAQ.
# Sphere is exempt from the twin because it is not in the STACK registry, and
# that exemption states its own reason: llms.txt is the stack's index for
# machine readers, and Sphere's first sentence is that it is not the stack.
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1

python3 - <<'PY'
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path.cwd()
problems = []

# ---------------------------------------------------------------------------
# A. Coverage
# ---------------------------------------------------------------------------
pages = sorted(p for p in ROOT.rglob("*.html")
               if not str(p.relative_to(ROOT)).startswith("demo/"))
if not pages:
    print("UNJUDGEABLE: no HTML pages found, so nothing was measured.")
    sys.exit(1)

sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")

js = (ROOT / "assets/site.js").read_text(encoding="utf-8")
stack = re.search(r"const STACK = \[(.*?)\n\];", js, re.S)
if not stack:
    print("UNJUDGEABLE: assets/site.js has no STACK registry, so which pages owe a")
    print("     markdown twin cannot be worked out. Nothing was measured.")
    sys.exit(1)
in_stack = {m.group(1) for m in re.finditer(r'href:"([^"]+)"', stack.group(1))}
if len(in_stack) < 5:
    print(f"UNJUDGEABLE: parsed {len(in_stack)} services out of STACK, which cannot be right.")
    sys.exit(1)

indexable = 0
for p in pages:
    rel = str(p.relative_to(ROOT))
    h = p.read_text(encoding="utf-8", errors="ignore")
    if "noindex" in h:
        continue                       # redirects and the console: deliberate
    indexable += 1
    if 'rel="canonical"' not in h:
        problems.append(f"{rel}: no canonical")
    if "application/ld+json" not in h:
        problems.append(f"{rel}: no JSON-LD, so search engines get the prose and nothing else")
    loc = "https://it-rat.com/" + ("" if rel == "index.html" else rel)
    if f"<loc>{loc}</loc>" not in sitemap:
        problems.append(f"{rel}: not in sitemap.xml")
    if rel in in_stack and not (ROOT / (rel[:-5] + ".md")).exists():
        problems.append(f"{rel}: in the STACK registry and has no markdown twin")

# ---------------------------------------------------------------------------
# B. Freshness
# ---------------------------------------------------------------------------
GENERATORS = ["tools/footer.py", "tools/topbar.py", "tools/faq.py",
              "tools/seo.py", "tools/llms.py", "tools/sitemap.py",
              # Writes the README diagrams rather than anything on a page, and
              # it belongs here for the same reason as the rest: it refused to
              # run from the day costcrew arrived, so three of its nine outputs
              # sat weeks behind their own pages. idryx's said 22 detectors
              # where the page says 27, and platform's drew seven emitters
              # where the page draws twelve.
              "tools/readmediagrams.py"]

tracked = subprocess.run(["git", "ls-files", "-z"], capture_output=True, text=True)
files = [f for f in tracked.stdout.split("\0") if f and not f.startswith("demo/")]
if not files:
    print("UNJUDGEABLE: git listed no tracked files, so the generators had nothing to run against.")
    sys.exit(1)

with tempfile.TemporaryDirectory() as tmp:
    tmp = pathlib.Path(tmp)
    for f in files:
        src = ROOT / f
        if not src.exists():
            continue                   # deleted but still in the index
        dst = tmp / f
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)

    # sitemap.py reads dates out of git, and the copy has no .git in it. It is
    # told where the real repository is rather than being given one, because it
    # only ever runs `git log` and `git show`; see the note in that file.
    env = {**os.environ, "IT_RAT_GIT_ROOT": str(ROOT)}
    for gen in GENERATORS:
        r = subprocess.run([sys.executable, gen], cwd=tmp, env=env,
                           capture_output=True, text=True)
        if r.returncode != 0:
            problems.append(f"{gen}: refused to run ({r.stderr.strip().splitlines()[-1] if r.stderr.strip() else 'no message'})")

    changed = []
    for f in files:
        src, dst = ROOT / f, tmp / f
        if not src.exists() or not dst.exists():
            continue
        if src.read_bytes() != dst.read_bytes():
            changed.append(f)
    for f in changed:
        problems.append(f"{f}: a generator would rewrite it, so what is published is not what it generates")

print(f"     {indexable} indexable pages, {len(in_stack)} services in the registry, "
      f"{len(GENERATORS)} generators run against a copy")

if problems:
    print()
    for line in problems:
        print("FAIL " + line)
    print(f"\n{len(problems)} problem(s). Run the generators and commit what they write:")
    print("  for t in footer topbar faq seo llms sitemap readmediagrams; do python3 tools/$t.py; done")
    print("A page no generator knows about keeps whatever it was born with, and the")
    print("markdown twin of one went on serving deleted copy for a day.")
    sys.exit(1)

print("OK: every indexable page carries its blocks, and every generator is a no-op.")
PY

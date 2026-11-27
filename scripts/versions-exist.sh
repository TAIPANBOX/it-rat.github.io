#!/usr/bin/env bash
# Every vX.Y.Z on a published page names a tag that exists.
#
# numbers.json owns the figures on the service pages, and service-numbers.sh
# makes the silent case impossible there. The guides, the changes pages and
# the root pages cite releases as history ("since v1.6.0", a release table),
# and nothing checked that those releases exist: a typo in a version reads as
# a claim about a release nobody ever cut. On 2026-11-27 every one of them was
# checked by hand and all existed; this makes that one command.
#
# HOW. For each version it looks back up to 80 characters for the name of an
# estate repository (the public TAIPANBOX repositories that are not forks,
# listed live, matched as whole words) and
# checks that repository's tags; with no name in reach it uses the repository
# the page is about (services/<id>.html, <id>-guide.html). A version that is
# missing from that repository but is a tag of another estate repository is
# reported as AMBIGUOUS, not as a fault: a release table lists rows for several
# repositories, and the nearest name is not always the right one. Only a
# version that is a tag of NO estate repository fails.
#
# A tool, not a gate: it needs the network and gh, and a deploy must not. It
# exits 1 when a version exists nowhere, 0 otherwise.
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1
command -v gh >/dev/null || { echo "versions-exist: gh not found"; exit 64; }

python3 - <<'PY'
import json, pathlib, re, subprocess, sys

def gh(args):
    r = subprocess.run(["gh"] + args, capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None

listing = gh(["repo", "list", "TAIPANBOX", "--visibility", "public", "--source", "--limit", "200", "--json", "name", "--jq", ".[].name"])
if not listing:
    print("measured nothing: could not list the TAIPANBOX repositories")
    sys.exit(1)
repos = sorted(listing.split(), key=len, reverse=True)
alias = {"platform": "agent-stack-go", "pocket": "tokenfuse-mobile", "console": "genaryx"}
tags = {}
def tagset(repo):
    if repo not in tags:
        out = gh(["api", f"repos/TAIPANBOX/{repo}/tags?per_page=100", "--paginate", "--jq", ".[].name"]) or ""
        tags[repo] = {t.lstrip("v") for t in out.split()}
    return tags[repo]

pages = [p for p in sorted(pathlib.Path(".").rglob("*.html"))
         if not any(x.startswith(".") for x in p.parts) and p.parts[0] not in ("demo",)]
if not pages:
    print("measured nothing: no published page found")
    sys.exit(1)

names = repos + list(alias)
nowhere = ambiguous = checked = 0
for p in pages:
    own = p.stem.replace("-guide", "")
    own = alias.get(own, own)
    text = re.sub(r"<script.*?</script>|<style.*?</style>", " ", p.read_text(errors="ignore"), flags=re.S)
    text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", text))
    for m in re.finditer(r"\bv(\d+\.\d+\.\d+)\b", text):
        v = m.group(1)
        before = text[max(0, m.start() - 80):m.start()].lower()
        best, repo = -1, None
        for n in names:
            hits = [h.start() for h in re.finditer(r"(?<![\w-])" + re.escape(n.lower()) + r"(?![\w-])", before)]
            if hits and hits[-1] > best:
                best, repo = hits[-1], alias.get(n, n)
        repo = repo if repo in repos else (own if own in repos else None)
        if repo is None:
            continue
        checked += 1
        if v in tagset(repo):
            continue
        others = [r for r in repos if v in tagset(r)]
        ctx = text[max(0, m.start() - 50):m.end() + 10]
        if others:
            ambiguous += 1
            print(f"AMBIGUOUS {p}: v{v} is not a {repo} tag, but is one of {', '.join(others[:4])}  ...{ctx}")
        else:
            nowhere += 1
            print(f"FAIL {p}: v{v} is a tag of no estate repository (nearest name: {repo})  ...{ctx}")

print()
print(f"{checked} versions checked on {len(pages)} pages: {nowhere} exist nowhere, {ambiguous} ambiguous.")
sys.exit(1 if nowhere else 0)
PY

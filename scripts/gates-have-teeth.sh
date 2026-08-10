#!/usr/bin/env bash
# Checks that the gates in `scripts/` still FAIL on the faults they exist to
# catch, still PASS on what they must not catch, and REFUSE to report success
# when they measured nothing at all.
#
# WHY
#
# Every gate here parses text, and a text parser does not break loudly: it
# stops matching and reports success. The mutants that proved each one existed
# as prose, in commit messages and in the `*(gate: ...)*` markers in CLAUDE.md,
# which is a record of what was true once. Nothing ran them again.
#
# A gate that has quietly stopped catching anything looks exactly like a gate
# with nothing to catch, and stays that way until the fault it guards ships.
#
# WHY THE THIRD PROPERTY IS SEPARATE FROM THE FIRST
#
# Both gates covered here already refuse when their subject is absent, and both
# say so in their own words: no HTML pages found, numbers.json missing,
# numbers.json recording no entries. Those sentences were true, were
# established by hand once in the session that wrote each script, and nothing
# re-ran them.
#
# AND ONE MORE PROPERTY, WHICH THIS REPOSITORY IS THE REASON FOR
#
# A case that expects a gate to FAIL proves nothing if the gate was already
# failing before the mutation. On 2026-08-09 `demo-bundle-current.sh` was red
# on a clean tree here, correctly: the published demo is built from an older
# genaryx than the one apps/web now holds. Any case written against that gate
# would have gone green while measuring nothing at all, which is the exact
# fault this harness exists to catch, one level up.
#
# So every fail-case checks the gate on the UNMUTATED tree first, and refuses
# rather than reporting. That check costs one extra run per case and is worth
# it: without it, a gate that starts failing for an unrelated reason silently
# turns every one of its cases into a pass.
#
# HOW IT MUTATES WITHOUT LEAVING A MESS
#
# It edits tracked files in place, so it refuses to start unless the tree is
# clean, restores with `git checkout` after every case, restores again from a
# trap on any exit path including a kill, and asserts the tree is clean before
# reporting success.
#
# A MUTATION THAT DID NOT APPLY PROVES NOTHING
#
# Every edit asserts it changed the file. A case whose edit applied nothing is
# a failure here, not a pass. That is not hypothetical: five such mutations
# were caught across idryx and tokenfuse on 2026-08-09, and three of the five
# had been verified BY HAND against the same gate minutes earlier. The hand
# version and the harness version differ only in how many layers of quoting sit
# between the text and python, which is exactly the difference nobody sees.

set -uo pipefail
cd "$(git rev-parse --show-toplevel)" || exit 1

if [ -n "$(git status --porcelain)" ]; then
	printf 'this script mutates tracked files, so it needs a clean tree.\n'
	printf 'commit or stash first; it restores with `git checkout` and cannot\n'
	printf 'tell your edits from its own.\n'
	exit 1
fi

# Untracked files too: a mutation may RENAME a tracked file, and `git checkout`
# restores the original while leaving the new name behind. And the INDEX, since
# a gate may read `git ls-files` rather than the disk, so a mutation has to move
# the file in both. Safe because this
# script refuses to start unless the tree is clean, so anything untracked
# during a run was created by the run. `-x` is deliberately absent: ignored
# build output is not ours to delete.
restore() {
	git reset -q --hard HEAD 2>/dev/null
	git clean -fdq 2>/dev/null
}
baseline_dir="$(mktemp -d)"

# One trap for both, because a second `trap ... EXIT` REPLACES the first
# rather than adding to it.
cleanup() {
	restore
	rm -rf "$baseline_dir"
}
trap cleanup EXIT INT TERM

failures=0
cases=0

# run_case <name> <expect: fail|pass> <gate> <python edit> [required output]
#
# The needle separates "it failed" from "it failed for the reason this case is
# about". Without it, a case expecting failure is satisfied by any failure,
# including one this harness caused itself.
run_case() {
	local name="$1" expect="$2" gate="$3" edit="$4" needle="${5:-}"
	cases=$((cases + 1))

	# The baseline applies to EVERY case, not only the ones expecting a failure.
	# It was `fail`-only until 2026-08-09, which left the mirror of the bug it was
	# written for: on a gate that is already red, a `pass` case reports OVEREAGER,
	# "the gate failed on something it must not catch", and sends the reader to
	# look at a harmless mutation while the gate was failing without it. Neither
	# verdict means anything on a red gate, so neither is given.
	skip_baseline=0
	if [ "$expect" = fail_env ]; then
		# `fail` with the baseline skipped, for cases whose fault IS the command
		# rather than a mutation: red before and after is the point there.
		expect=fail
		skip_baseline=1
	fi

	if [ "$skip_baseline" = 0 ]; then
		local key base_out
		key="$baseline_dir/$(printf '%s' "$gate" | cksum | tr -d ' ')"
		if [ ! -f "$key" ]; then
			if eval "$gate" >/dev/null 2>&1; then printf 'green' >"$key"; else printf 'red' >"$key"; fi
		fi
		base_out="$(cat "$key")"
		if [ "$base_out" = red ]; then
			printf 'UNJUDGEABLE  %s\n             the gate is already failing on a clean tree, so neither a\n             failure nor a pass after the mutation would prove anything\n' "$name"
			failures=$((failures + 1))
			return
		fi
	fi

	if ! python3 -c "$edit"; then
		printf 'BROKEN  %s\n        its mutation did not apply, so this case proved nothing\n' "$name"
		failures=$((failures + 1))
		restore
		return
	fi

	local out rc
	out=$(eval "$gate" 2>&1)
	rc=$?
	restore

	# Exit code first, then wording. Checking the needle before the expectation
	# turns "it did not fail at all" into "it failed for the wrong reason",
	# which sends the reader to look at prose when the gate is toothless.
	if [ "$expect" = fail ] && [ "$rc" -ne 0 ] && [ -n "$needle" ] &&
		! printf '%s' "$out" | grep -qF -- "$needle"; then
		printf 'WRONG REASON  %s\n              it failed, but not saying: %s\n' "$name" "$needle"
		failures=$((failures + 1))
		return
	fi
	if [ "$expect" = fail ] && [ "$rc" -eq 0 ]; then
		printf 'TOOTHLESS  %s\n           the gate passed on a fault it exists to catch\n' "$name"
		failures=$((failures + 1))
	elif [ "$expect" = pass ] && [ "$rc" -ne 0 ]; then
		printf 'OVEREAGER  %s\n           the gate failed on something it must not catch\n' "$name"
		failures=$((failures + 1))
		printf '%s\n' "$out" | head -4 | sed 's/^/           /'
	else
		printf 'ok  %-58s (%s)\n' "$name" "$expect"
	fi
}

py() { printf 'def edit(p, a, b):\n    s = open(p).read()\n    assert a in s, "pattern not found in " + p\n    open(p, "w").write(s.replace(a, b, 1))\n%s\n' "$1"; }

echo "=== faults each gate must catch ==="

# invariant: every page carries a title and a description, and no page carries
# both a canonical and a noindex, because which one wins is somebody else's
# algorithm.
run_case "page-metadata: a page loses its meta description" fail \
	'./scripts/page-metadata.sh' \
	"$(py 'import re
s = open("index.html").read()
m = re.search(r"<meta name=.description.[^>]*>", s)
assert m, "index.html has no meta description"
open("index.html","w").write(s.replace(m.group(0), "", 1))')" \
	"has no meta description"

# invariant 3: a number on this site is a claim with an owner.
run_case "service-numbers: a figure on a page that numbers.json does not own" fail \
	'./scripts/service-numbers.sh' \
	"$(py 'import json
p = "numbers.json"
d = json.load(open(p))
assert d["entries"], "numbers.json records no entries"
d["entries"] = d["entries"][1:]
json.dump(d, open(p, "w"), indent=2)')" \
	"FAIL"

# Invariant 7. This case could not exist until 2026-08-10: the gate was red on
# a clean tree here (the published demo was older than `apps/web`), so any case
# written against it would have measured nothing, which is what the UNJUDGEABLE
# check reports rather than hides. The demo was refreshed, the gate went green,
# and the case became possible. CLAUDE.md said exactly this would happen.
run_case "demo-bundle-current: index.html loads an asset the manifest does not record" fail \
	'./scripts/demo-bundle-current.sh' \
	"$(py 'import json
d = json.load(open("demo/BUILD.json"))
d["bundle"] = "assets/index-NOTTHEONE.js"
json.dump(d, open("demo/BUILD.json", "w"), indent=2)')" \
	"does not exist"

# The fault that put it-rat.com seven commits behind: the remote that actually
# deploys was missing from the clone, so every push went to the mirror and
# succeeded. Mutating the SCRIPT rather than the repo config here, because a
# case that runs `git remote remove` mutates state this harness does not
# restore on a crash, and a half-removed remote is a worse mess than a missing
# case.
run_case "deploy-target: the live repository is not the one holding the domain" fail \
	'./scripts/deploy-target-current.sh' \
	"$(py 'edit("scripts/deploy-target-current.sh",
     "LIVE_REPO=\"it-rat/it-rat.github.io\"",
     "LIVE_REPO=\"TAIPANBOX/it-rat.github.io\"")')" \
	"does not hold a custom domain"

# The other half of the same fault: the two published copies disagree. This is
# what a push to the mirror leaves behind, and it is invisible from either
# repository on its own.
#
# It asserts the SHIPPING INSTRUCTION rather than the direction, and that is a
# correction rather than a compromise. This case used to expect "behind by",
# and it passed here and failed in CI with WRONG REASON, on the same two SHAs.
# The gate reports "behind by N" or "diverged (live +N, mirror +M)" depending
# on what `git rev-list --count` can compute, which depends on which objects
# the clone happens to hold: a full clone here made it 0 ahead / 157 behind, a
# shallow CI clone made the same pair 626 / 2. Both messages are true and both
# come from check 2. Asserting the one that varies made this case measure the
# object graph rather than the gate.
run_case "deploy-target: the two published copies disagree" fail \
	'./scripts/deploy-target-current.sh' \
	"$(py 'edit("scripts/deploy-target-current.sh",
     "LIVE_REPO=\"it-rat/it-rat.github.io\"",
     "LIVE_REPO=\"TAIPANBOX/it-rat-v1\"")')" \
	"ship it: git push upstream"

echo
echo "=== and what they must NOT catch ==="

# Prose that happens to contain digits is not a claim with an owner. A gate
# that flagged one would be flagging most of the site.
run_case "service-numbers: a date and a version number in prose" pass \
	'./scripts/service-numbers.sh' \
	"$(py 'import re
s = open("index.html").read()
m = re.search(r"</body>", s)
assert m, "index.html has no closing body tag"
open("index.html","w").write(s.replace(m.group(0), "<p>Since 2026, on version 2.1, this sentence carries digits and owns nothing.</p></body>", 1))')"

# Work in progress is normal. A local HEAD ahead of both published copies is
# somebody mid-edit, and a gate that failed on it would be switched off inside
# a week.
run_case "deploy-target: an uncommitted local change" pass \
	'./scripts/deploy-target-current.sh' \
	"$(py 'edit("index.html", "</body>", "<p>work in progress</p></body>")')"

echo
echo "=== and the one this estate learned the hard way ==="
echo "    a gate whose subject is gone must SAY so, not report OK on nothing"

run_case "service-numbers: numbers.json with no entries left" fail \
	'./scripts/service-numbers.sh' \
	"$(py 'import json
p = "numbers.json"
d = json.load(open(p))
d["entries"] = []
json.dump(d, open(p, "w"), indent=2)')" \
	"records no entries"

run_case "page-metadata: no HTML pages left to read" fail \
	'./scripts/page-metadata.sh' \
	"$(py 'import subprocess, pathlib
n = 0
# The gate reads *.html RECURSIVELY, so anything short of every tracked page
# leaves it something to measure and the case proves nothing.
for f in sorted(pathlib.Path(".").rglob("*.html")):
    if ".git" in str(f):
        continue
    subprocess.run(["git", "mv", str(f), str(f) + ".disabled"], check=True)
    n += 1
assert n, "no HTML pages in this repo"')" \
	"measured nothing"

echo
if [ -n "$(git status --porcelain)" ]; then
	printf 'FAIL: this script left the tree dirty, so it cannot be trusted about anything above\n'
	git status --porcelain | head -5
	exit 1
fi

if [ "$failures" -gt 0 ]; then
	printf '%d of %d cases failed.\n' "$failures" "$cases"
	printf 'A gate that has quietly stopped catching anything looks exactly like a gate\n'
	printf 'with nothing to catch, and stays that way until the fault it guards ships.\n'
	exit 1
fi

printf 'OK: %d cases. Every gate fails on its own fault, passes on a non-fault,\n' "$cases"
printf '    and refuses to report success when it measured nothing.\n'

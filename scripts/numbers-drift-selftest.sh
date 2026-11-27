#!/usr/bin/env bash
# Self-test for the "could not measure" case in scripts/numbers-drift.sh.
#
# WHY THIS IS NOT A CASE IN gates-have-teeth.sh
#
# That harness's run_case reads an exit code: a "fail" case requires the
# gate to exit non-zero on a clean tree's mutation, a "pass" case requires
# it not to. numbers-drift.sh is a tool, not a gate, by its own header, and
# it exits 0 whatever it finds; there is no exit code for run_case to read a
# verdict from. What separates a measurement from a failure here is the TEXT
# it prints, not the process exit status, so this checks that text directly
# instead of bending a tool's contract to fit a harness built for gates.
#
# HOW IT ISOLATES ITSELF
#
# It builds a throwaway repository shape in one temp directory: a copy of
# the script and a one-entry numbers.json of its own. The real numbers.json
# is never opened and nothing here mutates a tracked file.

set -uo pipefail

repo_root="$(cd "$(dirname "$0")/.." && pwd)"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT INT TERM

mkdir -p "$tmp/scripts"
cp "$repo_root/scripts/numbers-drift.sh" "$tmp/scripts/numbers-drift.sh"
chmod +x "$tmp/scripts/numbers-drift.sh"

failures=0
cases=0

# check_case <name> <manifest JSON> <must appear> <must NOT appear>
check_case() {
	local name="$1" manifest="$2" needle="$3" forbidden="$4" out rc
	cases=$((cases + 1))
	printf '%s\n' "$manifest" >"$tmp/numbers.json"

	out="$("$tmp/scripts/numbers-drift.sh" 2>&1)"
	rc=$?

	if [ "$rc" -ne 0 ]; then
		printf 'FAIL  %s\n      numbers-drift.sh must always exit 0 (its own contract); exited %d\n' "$name" "$rc"
		failures=$((failures + 1))
		return
	fi
	if ! printf '%s\n' "$out" | grep -qF -- "$needle"; then
		printf 'FAIL  %s\n      expected to find: %s\n' "$name" "$needle"
		printf '%s\n' "$out" | sed 's/^/      /'
		failures=$((failures + 1))
		return
	fi
	if [ -n "$forbidden" ] && printf '%s\n' "$out" | grep -qF -- "$forbidden"; then
		printf 'FAIL  %s\n      must NOT contain: %s\n' "$name" "$forbidden"
		printf '%s\n' "$out" | sed 's/^/      /'
		failures=$((failures + 1))
		return
	fi
	printf 'ok  %s\n' "$name"
}

# The fault this exists for: a check exits non-zero and prints a count
# beside the reason it is not a real one. Before the fix this measured 69
# and reported it as drift from the claim, 517 tests.
fault_manifest='{"entries": [
  {"page": "services/fake.html", "claim": "517 tests", "repo_dir": null,
   "check": "echo '"'"'69 tests collected, 22 errors'"'"'; exit 1"}
]}'
check_case "a check that errors and still prints a count" \
	"$fault_manifest" "COULD NOT MEASURE" "DRIFTED"

# A clean run that SAYS it had no errors is still a clean run. pytest and
# friends print "0 errors" on a good day; a rule that reads any digit beside
# the word would sweep every honest zero into COULD NOT MEASURE, which is a
# check red on a GOOD build, the worse failure. The count goes to stdout and
# the reassurance to stderr, which is where pytest puts its own.
zero_manifest='{"entries": [
  {"page": "services/fake.html", "claim": "69 tests", "repo_dir": null,
   "check": "echo '"'"'0 errors'"'"' >&2; echo 69"}
]}'
check_case "a clean run that also says 0 errors is left alone" \
	"$zero_manifest" "agrees" "COULD NOT MEASURE"

# The non-fault: a clean count, exit 0, the word "error" nowhere in it, must
# read as an ordinary measurement and must NOT be swept into COULD NOT
# MEASURE alongside it.
clean_manifest='{"entries": [
  {"page": "services/fake.html", "claim": "69 tests", "repo_dir": null,
   "check": "echo 69"}
]}'
check_case "a clean count is left alone" \
	"$clean_manifest" "agrees" "COULD NOT MEASURE"

# A claim that names several values has a check that prints one per line
# (added 2026-11-27): it agrees when every printed line is in the claim, and
# drifts when one of them is not. Thousands separators are ignored.
multi_manifest='{"entries": [
  {"page": "services/fake.html", "claim": "v1.14.0 to v1.27.1, 1,024 records", "repo_dir": null,
   "check": "printf '"'"'v1.14.0\\nv1.27.1\\n1024 records\\n'"'"'"}
]}'
check_case "a claim naming several values agrees with each printed line" \
	"$multi_manifest" "agrees" "DRIFTED"

multi_drift_manifest='{"entries": [
  {"page": "services/fake.html", "claim": "v1.14.0 to v1.27.0", "repo_dir": null,
   "check": "printf '"'"'v1.14.0\\nv1.27.1\\n'"'"'"}
]}'
check_case "a claim naming several values drifts when one line is not in it" \
	"$multi_drift_manifest" "DRIFTED" "agrees"

echo
if [ "$failures" -gt 0 ]; then
	printf '%d of %d cases failed.\n' "$failures" "$cases"
	exit 1
fi
printf 'OK: %d cases. A check that errors is reported as COULD NOT MEASURE,\n' "$cases"
printf '    never as a drifted number, and a clean count is left alone.\n'

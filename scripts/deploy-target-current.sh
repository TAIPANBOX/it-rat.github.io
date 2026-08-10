#!/usr/bin/env bash
#
# Fails when the repository that actually serves it-rat.com is behind the one
# everybody pushes to.
#
# WHY THIS EXISTS
#
# On 2026-08-10 it-rat.com was found SEVEN commits behind. The scopyx room, a
# pass fixing seven drifted figures, the site's own gate work and a rebuilt demo
# were all merged, all pushed, all reported success, and none of them were on
# the live site. Several sessions in a row had run `git push origin master`,
# watched it succeed, and believed they had shipped.
#
# They had not, because this clone has two remotes for two different
# repositories:
#
#   origin    TAIPANBOX/it-rat.github.io   a mirror; Pages serves it at
#                                          taipanbox.github.io, cname null
#   upstream  it-rat/it-rat.github.io      the domain owner, cname it-rat.com
#
# and at the time of the incident `upstream` was not configured at all. A push
# to a mirror is a successful push. Nothing about it looks wrong.
#
# THE TRAP THAT MADE IT LOOK FINE, WHICH THIS SCRIPT ENCODES
#
# The tree contains a `CNAME` file saying `it-rat.com`, in BOTH repositories,
# because it is a tracked file. Reading it is what convinced a previous session
# that the mirror was the live site. A `CNAME` in a tree is a REQUEST; the
# domain belongs to whichever repository GitHub has accepted it for, and only
# the Pages API says which that is. So this script does not trust the file: when
# it can reach the API it asks, and refuses if the answer is not the repository
# it is treating as live.
#
# WHAT IT CHECKS
#
#   1. In a local clone: the `upstream` remote exists and points at the live
#      repository. Its absence is the root cause and the cheapest thing to
#      catch.
#   2. Always: the live repository's `master` is not behind the mirror's.
#   3. When `gh` is authenticated: the repository this script calls live really
#      is the one holding the custom domain.
#
# WHAT IT DELIBERATELY DOES NOT CHECK
#
# That the local `HEAD` matches either remote. Work in progress is normal and a
# gate that failed on it would be turned off within a week. This is about the
# two published copies disagreeing, which is never normal.
#
# WHY IT CANNOT LIVE IN THE LIVE REPOSITORY'S OWN WORKFLOW
#
# A workflow there only runs when a push arrives, and the whole fault is a push
# that never arrives. The absence of a deploy cannot be detected by the thing
# that would have deployed it. So this runs beside the other gates, before a
# push and after one, and in CI on the mirror where a divergence is visible.
set -euo pipefail

cd "$(dirname "$0")/.."

LIVE_REPO="it-rat/it-rat.github.io"
MIRROR_REPO="TAIPANBOX/it-rat.github.io"
LIVE_URL="https://github.com/$LIVE_REPO.git"
MIRROR_URL="https://github.com/$MIRROR_REPO.git"
DOMAIN="it-rat.com"
BRANCH="master"

problems=0
note() { printf '     %s\n' "$1"; }
fail() { printf 'FAIL %s\n' "$1"; problems=$((problems + 1)); }

# ---------------------------------------------------------------------------
# 1. The remote that deploys must exist, and must point at the live repository.
# ---------------------------------------------------------------------------
# Not a question CI can be asked. Actions checks out ONE repository with ONE
# remote called `origin`, so "is `upstream` configured and pointing at live" is
# about a person's clone and nothing else. This branch used to be absent, and
# the workflow carried a comment saying check 1 was "skipped here by
# construction": it was not skipped, it FAILED, and it took the whole Pages
# deploy down with it for three pushes on 2026-08-10 before anybody read the
# log. Skipped LOUDLY for the same reason check 3 is: a silent skip is how a
# check stops checking.
if [ "${GITHUB_ACTIONS:-}" = "true" ]; then
	note "check 1 skipped in CI: one checkout, one remote, and the question is"
	note "about a developer's clone. Checks 2 and 3 below still ran."
elif git rev-parse --git-dir >/dev/null 2>&1; then
	if ! git remote | grep -qx upstream; then
		fail "no 'upstream' remote in this clone, so 'git push upstream $BRANCH' cannot run"
		note "this is the exact state that left it-rat.com seven commits behind:"
		note "  git remote add upstream $LIVE_URL"
	else
		configured=$(git remote get-url upstream)
		# Compare on the owner/name, not the string: ssh and https forms of the
		# same repository are both correct and neither should fail this.
		case "$configured" in
		*"$LIVE_REPO"*) ;;
		*)
			fail "'upstream' points at $configured, not at the live repository $LIVE_REPO"
			note "a push there succeeds and deploys nothing"
			;;
		esac
	fi
fi

# ---------------------------------------------------------------------------
# 2. The live repository must not be behind the mirror.
# ---------------------------------------------------------------------------
live_sha=$(git ls-remote --heads "$LIVE_URL" "$BRANCH" 2>/dev/null | cut -f1)
mirror_sha=$(git ls-remote --heads "$MIRROR_URL" "$BRANCH" 2>/dev/null | cut -f1)

if [ -z "$live_sha" ] || [ -z "$mirror_sha" ]; then
	# A gate that cannot see its subject says so rather than reporting OK on
	# nothing. This is the failure mode this repository keeps finding.
	echo "UNJUDGEABLE: could not read $BRANCH from both repositories."
	[ -z "$live_sha" ] && note "no answer from $LIVE_REPO"
	[ -z "$mirror_sha" ] && note "no answer from $MIRROR_REPO"
	note "no network, or the branch is gone. Nothing was measured, so nothing is claimed."
	exit 1
fi

if [ "$live_sha" != "$mirror_sha" ]; then
	# Which way round matters. The mirror ahead is the shipping failure; the
	# live one ahead is somebody pushing straight past the mirror, which is
	# untidy rather than dangerous, and is reported as itself.
	# The counts are the useful half of this message, so fetch what the local
	# object store is missing rather than printing "?" at somebody. A fresh CI
	# clone has neither side's tip; both fetches are shallow-friendly and cost
	# a second.
	for sha_url in "$live_sha $LIVE_URL" "$mirror_sha $MIRROR_URL"; do
		set -- $sha_url
		git cat-file -e "$1" 2>/dev/null || git fetch --quiet "$2" "$BRANCH" 2>/dev/null || true
	done
	if git cat-file -e "$live_sha" 2>/dev/null && git cat-file -e "$mirror_sha" 2>/dev/null; then
		behind=$(git rev-list --count "$live_sha..$mirror_sha" 2>/dev/null || echo "?")
		ahead=$(git rev-list --count "$mirror_sha..$live_sha" 2>/dev/null || echo "?")
	else
		# Still unreachable: say so instead of implying a direction. Two tips
		# that share no history are a different problem from being behind.
		behind="an unknown number of"
		ahead="?"
	fi
	if [ "$ahead" != "0" ] && [ "$ahead" != "?" ]; then
		fail "$LIVE_REPO and $MIRROR_REPO have diverged (live +$ahead, mirror +$behind)"
	else
		fail "$DOMAIN is behind by $behind commit(s): the live repository does not have what the mirror has"
	fi
	note "live   $LIVE_REPO   ${live_sha:0:12}"
	note "mirror $MIRROR_REPO ${mirror_sha:0:12}"
	note "ship it: git push upstream $BRANCH"
else
	note "both copies at ${live_sha:0:12}"
fi

# ---------------------------------------------------------------------------
# 3. The repository called live must be the one holding the domain.
# ---------------------------------------------------------------------------
# Skipped without `gh`, and skipped LOUDLY: a silent skip is how a check stops
# checking. The two above still ran, so this is a partial result, not a pass.
if command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1; then
	cname=$(gh api "/repos/$LIVE_REPO/pages" --jq .cname 2>/dev/null || echo "")
	if [ -z "$cname" ] || [ "$cname" = "null" ]; then
		fail "$LIVE_REPO does not hold a custom domain, so it is not what serves $DOMAIN"
		note "this script's idea of which repository is live is wrong, or Pages was reconfigured"
	elif [ "$cname" != "$DOMAIN" ]; then
		fail "$LIVE_REPO serves '$cname', not '$DOMAIN'"
	else
		note "$LIVE_REPO holds $DOMAIN, per the Pages API rather than per the CNAME file"
	fi
else
	note "gh unavailable: did NOT verify which repository holds $DOMAIN (checks 1 and 2 still ran)"
fi

if [ "$problems" -gt 0 ]; then
	printf '\n%d problem(s) between the repository you push to and the one that serves %s.\n' \
		"$problems" "$DOMAIN"
	printf 'A push to the mirror succeeds and ships nothing, which is why this is a gate\n'
	printf 'and not a note: seven commits accumulated behind it before anybody looked.\n'
	exit 1
fi

printf 'OK: %s serves %s and has everything the mirror has.\n' "$LIVE_REPO" "$DOMAIN"

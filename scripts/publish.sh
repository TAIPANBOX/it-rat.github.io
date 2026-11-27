#!/usr/bin/env bash
# Publishes master to it-rat.com, in the order that leaves nothing red.
#
# The live site deploys from `upstream` (it-rat/it-rat.github.io); `origin`
# (TAIPANBOX) is the mirror where pull requests are merged. The mirror's Pages
# workflow runs deploy-target-current.sh, which fails while the live
# repository is behind the mirror, so every merge left that run red until
# somebody pushed upstream and re-ran it by hand. Twice on 2026-11-27.
#
# Publishing is an outward action: run this only after the go to publish.
#
# Steps, each refusing rather than guessing:
#   1. the tree is clean, on master, and equal to origin/master;
#   2. upstream/master is an ancestor of master (a fast-forward, never a force);
#   3. secretscan reads what is about to be published;
#   4. push master to upstream, then wait for the live Pages run of that commit;
#   5. re-run the mirror's latest failed Pages run for that commit, and wait;
#   6. deploy-target-current.sh, which asks the Pages API who holds the domain.
set -euo pipefail
cd "$(dirname "$0")/.."

say() { printf '%s\n' "$*"; }
fail() { printf 'publish: %s\n' "$*" >&2; exit 1; }

[ -z "$(git status --porcelain)" ] || fail "the tree is not clean"
[ "$(git branch --show-current)" = master ] || fail "not on master"
git fetch -q origin master
git fetch -q upstream master
[ "$(git rev-parse master)" = "$(git rev-parse origin/master)" ] || fail "master is not origin/master; pull or merge the PR first"
sha="$(git rev-parse master)"
if [ "$(git rev-parse upstream/master)" = "$sha" ]; then
  say "upstream already serves ${sha:0:7}; nothing to push"
else
  git merge-base --is-ancestor upstream/master master || fail "upstream/master is not an ancestor of master; refusing to force"
  if command -v secretscan >/dev/null; then secretscan diff "upstream/master..master"; fi
  git push upstream master
fi

wait_run() { # repo
  local repo="$1" id=""
  for _ in $(seq 1 30); do
    id="$(gh run list -R "$repo" --workflow pages.yml --commit "$sha" -L 1 --json databaseId --jq '.[0].databaseId // empty')"
    [ -n "$id" ] && break
    sleep 5
  done
  [ -n "$id" ] || fail "no Pages run for ${sha:0:7} in $repo"
  gh run watch "$id" -R "$repo" --exit-status --interval 15 >/dev/null 2>&1 || true
  printf '%s %s\n' "$id" "$(gh run view "$id" -R "$repo" --json conclusion --jq .conclusion)"
}

read -r live_id live_c < <(wait_run it-rat/it-rat.github.io)
say "live Pages run $live_id: $live_c"
[ "$live_c" = success ] || fail "the live deploy did not succeed; the site still serves the previous commit"

read -r mid mc < <(wait_run TAIPANBOX/it-rat.github.io)
if [ "$mc" != success ]; then
  say "mirror Pages run $mid was $mc (it ran before upstream had the commit); re-running"
  gh run rerun "$mid" -R TAIPANBOX/it-rat.github.io
  sleep 10
  gh run watch "$mid" -R TAIPANBOX/it-rat.github.io --exit-status --interval 15 >/dev/null 2>&1 || true
  mc="$(gh run view "$mid" -R TAIPANBOX/it-rat.github.io --json conclusion --jq .conclusion)"
  say "mirror Pages run $mid: $mc"
  [ "$mc" = success ] || fail "the mirror's run is still $mc; read its log"
fi

./scripts/deploy-target-current.sh
say "Published ${sha:0:7} to it-rat.com."

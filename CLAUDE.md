# CLAUDE.md, working instructions for the it-rat.com site

These instructions apply to any model working in this repo. Read this file
before changing anything. It holds process and invariants only: **no status.**

## What this is

The site for IT-RAT, a boutique cloud consultancy. A self-contained static site
served from GitHub Pages at it-rat.com. The default branch here is `master`.

**Two remotes, on purpose.** `origin` is `TAIPANBOX/it-rat.github.io`;
`upstream` is `it-rat/it-rat.github.io`, the separate account the live site
deploys from. Know which one you are pushing to before you push.

## Blast radius

This is the public face of the business. A wrong claim here is not a bug report,
it is something a prospective client reads and quietly discounts. Everything
committed is published.

## Gates

```sh
./scripts/page-metadata.sh
./scripts/service-numbers.sh
./scripts/footer-shelves.sh       # invariant 10
./scripts/generated-blocks.sh     # invariant 11
./scripts/demo-bundle-current.sh
./scripts/deploy-target-current.sh  # invariant 9; needs network
# demo-bundle-current.sh also runs daily on its own schedule; see invariant 7
./scripts/gates-have-teeth.sh     # invariant 8; needs a clean tree
```

And one that is deliberately NOT a gate:

```sh
PYTHON=/path/to/venv/bin/python ./scripts/numbers-drift.sh [--slow]
```

It re-measures every figure in `numbers.json` against the sibling checkouts and
prints what drifted. Run it before a sweep, never in the publish path: see
invariant 3 for why a deploy must not depend on nine other repositories being
present and buildable.

This list did not exist until 2026-08-09: the gates were named only inside the
invariants that own them, while the Pages workflow ran three of them.

## Hard invariants

Each one carries how it is held today. Use `(gate: ...)`, `(test: ...)`,
`(partly gated: ...)` or `(not enforced)`, and use the weakest one that is
true.

1. **Every page's metadata is measured at publish, not assumed.** Title at most
   70 characters, description between 25 and 160. A truncated title in a search
   result is the first thing a stranger sees.
   *(gate: `scripts/page-metadata.sh`, run in the Pages workflow BEFORE the
   upload, so a bad page does not reach production and get fixed afterwards)*
2. **The machine-readable claims move with the copy.** JSON-LD, Open Graph,
   canonical and sitemap describe the same thing the visible text does. A pivot
   that rewrites the prose and leaves the structured data behind ships two
   different stories, and search engines read the one nobody proofread.
   **Never put `noindex` beside a canonical.**
   *(partly gated: `scripts/page-metadata.sh` holds the noindex-beside-canonical
   pair and og:title agreeing with `<title>`. JSON-LD and sitemap agreeing with
   the prose still needs a reader.)*
3. **A number on this site is a claim with an owner.** Anything measured says
   what measured it and when. If a figure came from a run, it can be pointed at;
   if it cannot, it does not belong here.
   *(gate: `scripts/service-numbers.sh` against `numbers.json`, in the Pages
   workflow before the upload. It cannot tell you a recorded figure is still
   true, because nothing here can reach another repository's suite. It makes the
   silent case impossible: every figure on a service page is in the manifest
   with its repository, the command that produces it and the date somebody last
   ran that command, and a page edited without the manifest fails. Figures
   nobody has reproduced are ALLOWED and reported every run, because refusing
   them would only teach people to leave numbers off the page. **All seven are
   reproduced as of 2026-08-05**, which took a venv, one `git clone` and reading
   two type signatures, and found four of the seven wrong: trailryx by 33,
   tokenfuse by 196, engram by 42 and verdryx by 75. Nothing keeps them true;
   the manifest keeps them dated.)*

   **It happened again on 2026-08-20, and that is the argument for the tool
   rather than for more care.** Ten days after the last sweep, five of the now
   eleven figures were stale: trailryx by 6 tests, tokenfuse by 10, idryx by 2
   detectors, stack-k8s by 3 traps, and agent-stack-go a whole release behind
   at v0.6.0. None was wrong when written, which is the same finding as last
   time and will be the same finding next time.

   So each entry now also carries `check`, a runnable form of its prose
   `command`, and `repo_dir`, the sibling checkout to run it in.
   `scripts/numbers-drift.sh` walks the manifest, re-measures everything it can
   reach and prints what drifted. **It is a tool, not a gate, and must not
   become one.** The reasoning above still holds: a publish that depended on
   nine sibling checkouts, a cargo build and GitHub answering would trade a
   silent staleness for a flaky deploy. It exits 0 whatever it finds, it says
   "measured nothing" rather than "agrees" when a check prints no value, and it
   skips the slow ones unless asked. The prose `command` stays, because it says
   WHAT is counted, which a one-liner cannot: "test functions, not subtests" is
   the difference between a number somebody can reproduce and one that merely
   looks precise.
4. **A refresh updates numbers. Only a sweep updates status sentences.** The
   sentence "we are building X" outlives the number beside it by months. When
   the numbers change, read the sentences too. *(not enforced)*
5. **Nothing unverified reads as verified, and the two mobile apps are where
   that is hardest.** They are not one case, and this invariant said they were
   until 2026-08-04. Sphere is a side project; **TokenFuse Pocket is in the
   stack**, `@decided 2026-08-03`, and the site says so.

   - **Sphere** is linked from the footer and nowhere else: not in the `STACK`
     registry, so it cannot reach the corridor rail, the prev/next walk, the
     dot strip or the jump palette. It sits under its own `side project`
     heading beside `standalone`.
   - **Pocket** is in `STACK`, on the rail, in the walk, in the palette, has
     `services/pocket.html`, and carries a coloured chip like any other room.
     What holds the invariant for it is not exclusion but a marker it cannot
     lose: `note: "not wired in yet"` in the registry, rendered on its rail
     card, in its top band, and in its own eyebrow. Its page states the limit
     in its own fact table: no hardening pass, no security review, no App
     Store.

   The reason the old rule existed has not changed, only who it applies to.
   Every other page here points at something running and measured, and that is
   the one thing this site has that cannot be copied; a promise standing next
   to those makes a reader ask which of the rest are also promises. So a room
   for something unshipped is allowed to exist and is never allowed to look
   finished.

   **Read this before "fixing" the site to match an older version of this
   file.** Between 2026-08-03 and 2026-08-04 this invariant forbade four
   things the site was already doing on purpose: Pocket in the registry, on
   the rail, with a page, with a chip. An instruction file younger than the
   decision it describes is the one way a rule like this destroys work rather
   than protecting it.
   *(not enforced)*
6. **Nothing on this site is sold, and no page says how anything is paid
   for.** No pricing, no plans, no upgrade language, and no sentence naming a
   commercial motion of any kind.

   Until 2026-08-29 this invariant read "the stack is open; consulting is the
   commercial motion", and the Genaryx FAQ carried a question answering where
   the money comes from. `@decided 2026-08-29`: there is no commercial side,
   an earlier idea of one is gone, and nothing on the site may describe one.
   The question is gone, so is the paragraph about the console once being the
   one thing that would be sold, and so is the same history in the redirect
   page's comment. What survives is the plain fact that the licence is
   Apache-2.0 and there is no tier.

   The market descriptions in `agent-tooling-compared.html` and the comparison
   row on the TokenFuse page are NOT this. They describe how other shapes of
   tooling are licensed, anonymously, which is a fact about the field rather
   than a claim about us. Leave them.
   *(not enforced)*
7. **The published demo is a build of the current genaryx.** `/demo` is not
   built here: it is a hand-pasted copy of `genaryx/apps/web/dist`, and a copy
   carries no date. Every page renders and every link works while the console
   on the site sits months behind the console in the repository, so this decays
   in the one direction nobody looks. It is refreshed with
   `scripts/refresh-demo.sh`, never by hand, because two flags in genaryx's
   build command are load-bearing and neither is guessable.
   *(gate: `scripts/demo-bundle-current.sh`, in the Pages workflow before the
   upload AND on a daily schedule of its own
   (`.github/workflows/demo-freshness.yml`), which is the half that took two
   incidents to learn. The gate was correct from the day it was written and
   caught neither of them, because the Pages workflow only runs on a push HERE
   and the demo goes stale when GENARYX changes. Between a merge there and the
   next push here it was right and silent, and both times a person found the
   stale demo by opening it. A check nothing invokes at the moment of the fault
   is documentation. It compares the last commit that touched `apps/web`, NOT genaryx's
   main tip: most commits there cannot change the bundle, and a check that
   fails on every unrelated merge is one somebody switches off. It also holds
   the local half with no network, that `demo/index.html` loads exactly the two
   files `demo/BUILD.json` records and that no previous build's hashed assets
   linger beside them, since a content-hashed name is served for as long as the
   file exists.)*

8. **A check must be able to tell "did not fail" from "did not run", and every
   gate here has been made to fail on purpose to prove it can.**
   `page-metadata.sh` and `service-numbers.sh` already refuse when their
   subject is absent, and say so in their own words: no HTML pages found,
   `numbers.json` missing, `numbers.json` recording no entries. Those sentences
   were true, were established by hand once, and nothing re-ran them.

   **This repository added a fourth property to the harness, and the reason is
   worth keeping.** A case expecting a gate to FAIL proves nothing if the gate
   was already failing before the mutation. On 2026-08-09
   `demo-bundle-current.sh` was red on a clean tree here, correctly: the
   published demo is built from an older genaryx than `apps/web` now holds. A
   case written against it would have gone green while measuring nothing, which
   is the fault this harness exists to catch, one level up. So every fail-case
   now runs the gate on the UNMUTATED tree first and reports `UNJUDGEABLE`
   rather than a pass. Verified by writing exactly that case and watching it
   refuse.
   *(gate: `scripts/gates-have-teeth.sh`, 23 cases: fifteen real faults, four
   non-faults, and four subjects taken away entirely. The non-faults are the
   ones worth keeping: prose that happens to contain digits is not a claim with
   an owner, an uncommitted local edit is not a deploy that failed to arrive,
   a paragraph arriving on a page is not a change of footer shape, and a
   comment added to the stylesheet is not a generator that stopped running. A
   gate flagging any of them would be switched off inside a week. This line said
   nine until 2026-08-29 while eleven cases ran, which is the same class of
   drift the site's own figures have: a count restated by hand and never
   measured.)*

   **`demo-bundle-current.sh` now HAS a case, and the delay is the record worth
   keeping.** This file used to say it deliberately had none, because the gate
   was red on a clean tree (the published demo was older than `apps/web`) and
   any case written against it would have measured nothing. The demo was
   refreshed on 2026-08-10, the gate went green, and the case became possible.
   The prediction held exactly: it was a deploy decision, not a gate decision.

   **What else it does not cover.** It cannot test itself. It proves each gate
   catches the faults named in it, not every fault of that kind.

9. **The repository that serves the domain is not behind the one that gets
   pushed to.** `origin` is a mirror and `upstream` is the live site, and a
   push to the mirror succeeds, reports nothing wrong and deploys nothing.

   This is not hypothetical and it is not rare. On 2026-08-10 it-rat.com was
   found **seven commits behind**: the scopyx room, the pass fixing seven
   drifted figures, this repository's own gate work, and a rebuilt demo. Every
   one had been merged and pushed. Several sessions in a row had believed they
   shipped.

   Two things made it invisible. A successful `git push` is not evidence of a
   deploy, and the tracked `CNAME` file says `it-rat.com` in BOTH repositories,
   so reading it is what convinced a session that the mirror was live. A
   `CNAME` in a tree is a request; the Pages API says who was granted it.
   *(gate: `scripts/deploy-target-current.sh`, three checks: the `upstream`
   remote exists and points at the live repository, the live repository is not
   behind the mirror, and the repository this all calls "live" really holds the
   domain per the API rather than per the file. It runs in the Pages workflow
   too, where only the second check applies, because a CI clone has no
   `upstream`. It cannot run inside the LIVE repository's own workflow and mean
   anything: that workflow only runs when a push arrives, and the fault is a
   push that never arrives.)*

10. **The footer's shape is generated, and the stylesheet's constant agrees
   with it.** Above 860px the footer row is a six-column grid, one column per
   shelf. Six is a number written into `assets/site.css`, describing content
   written from the registry in `assets/site.js`, and nothing connected the
   two: a seventh category would give every page a seventh shelf that wraps to
   a row of its own, half empty, with no build failing and no link breaking.

   Writing that grid on 2026-08-29 found the page it would have drawn wrong.
   `agent-tooling-compared.html` was published on 2026-08-11 and never added to
   `tools/footer.py`'s `PAGES`, so every regeneration since had skipped it: one
   shelf of twelve chips, CostCrew and Vouchryx missing outright, and Trailryx
   under a `standalone` heading that stopped being true the same week.
   Thirty-one pages were current and one had been stale for three months.

   So the gate does not read that list. **A hand-written list of what to check
   is itself unchecked, and that list was the bug.** It finds every page with a
   footer and judges what it finds.
   *(gate: `scripts/footer-shelves.sh`, three checks: how many shelves the
   registry would emit, that every page carrying a footer has exactly that many
   with those labels in one row, and that the column count in the stylesheet is
   the same number. In the Pages workflow before the upload. It says nothing
   about WHICH chips sit on a shelf: `tools/footer.py` writes those and
   `service-numbers.sh` owns what a page may claim.)*

11. **A page's generated blocks are on it, and they are what the generators
   would write today.** Five tools write into these pages: the footer, the top
   bar, the visible FAQ, the JSON-LD, and the markdown twins with the `llms.txt`
   index. Each keeps its own hand-written list of pages, and until 2026-08-29
   nothing compared those five lists with each other or with the pages on disk.

   Two pages were outside all of them, both for months.
   `agent-tooling-compared.html` went up on 2026-08-11 in none of the five,
   though its own commit message said it was "listed in all seven places", and
   its markdown twin, served at `it-rat.com/agent-tooling-compared.md`, was
   still publishing the competitor comparison table and a section headed "Where
   they are plainly better than us" a day after both came off the page itself by
   decision. `services/scopyx.html` went up on 2026-08-10 and was the
   one indexable page here carrying no JSON-LD at all.

   **A generated file nobody regenerates is worse than a hand-written one**,
   because everybody assumes it is current, and this one was published.
   *(gate: `scripts/generated-blocks.sh`, two halves. Coverage: every page that
   is not `noindex` carries a canonical, a JSON-LD block and a sitemap entry,
   and every page in the STACK registry carries a markdown twin. Freshness: all
   seven generators run against a copy of the tracked tree and must change
   nothing, since a generator is idempotent by design and anything it would
   rewrite is drift. It copies rather than runs in place, because a gate that
   fixes what it is judging is green the next run with nobody the wiser. In the
   Pages workflow before the upload.)*

   **The one exemption, and why it is derived rather than listed.** Sphere owes
   no markdown twin because it is not in the STACK registry. `llms.txt` is the
   stack's index for machine readers and Sphere's first sentence is that it is
   not the stack, so the exemption states its own reason and disappears the day
   somebody puts Sphere in the registry. It does carry JSON-LD, written by four
   lines of its own in `tools/seo.py`: the generic service branch would have
   claimed Apache-2.0 where the repository is MIT, "Linux, macOS" where the page
   says iOS only, and a breadcrumb through "The stack" on the page that denies
   being part of it.

   **`sitemap.xml` is the sixth generator, added 2026-08-29, and the interesting
   part is what a `lastmod` is allowed to mean.** The file had been hand-kept
   and carried three dates, the newest 2026-08-10, for pages edited on the 28th
   and 29th. The naive repair, the date of the last commit touching the file, is
   wrong here: a footer sweep writes all thirty pages in one commit, and a
   sitemap where everything changed today is one a crawler learns to ignore.
   So `tools/sitemap.py` masks the blocks the other generators own and walks
   each page's history backwards while the stripped content still matches what
   is on disk; the oldest commit that still matches is when the page became what
   it is. **Measured on the day it was written, that mask changes the answer on
   seven of thirty pages**, each of which the naive rule would have dated to
   that day while its content was between nine and thirty-three days old.

   Two things it needs to be honest about. It errs towards dates that are too
   new, never too old, because a blob from before a marker existed cannot have
   that block masked out of it. And a page whose content matches no commit takes
   today's date, which is the only clock in it: without that the tool could not
   agree with itself across the commit that introduces a change, since the
   commit being made has not happened yet. It refuses outright on a shallow
   clone, where every page would look as though it arrived at HEAD, which is why
   the Pages workflow checks out with `fetch-depth: 0`.

   **`tools/readmediagrams.py` is the seventh, and it had been refusing to run
   since 2026-08-10.** It lifts each room's schematic off its own page into a
   standalone animated SVG for that repository's README, and it checks its own
   list against the registry in both directions, which is the right design and
   is why it stopped rather than skipping: costcrew, scopyx and vouchryx were in
   STACK and in neither of its lists. Nothing ran it, so nobody read the
   refusal, and its other nine outputs went stale behind it. Three had:
   idryx's said 22 detectors where the page says 27, and platform's drew seven
   emitters where the page has drawn twelve since 2026-08-28.

   Two things it needed before those three could be added.
   **A wire that is both dashed and arrowed produced invalid XML**, because the
   overlay copy kept the original `stroke-dasharray` and then had another one
   written onto it; costcrew and vouchryx were the first rooms with such a wire,
   and GitHub renders a file like that as nothing at all. The generator now
   strips every attribute it is about to set and **parses its own output before
   writing it**. And a token whose `animateMotion` begins later than 0s sits at
   its authored coordinates until it starts, which put a red dot in the corner
   of the vouchryx picture; each one is now parked at the first point of its own
   path, which is what the frame before the start should have looked like.

   **Scopyx is sourced from a file rather than from its page**, and that is the
   one exception here. Its page schematic is filled in by
   `assets/stages/scopyx.js` as a request travels it, so a lift renders five
   empty boxes and a redirect arc frozen mid-flight. That was measured, not
   assumed: the file was generated and looked at first. The source is
   `assets/img/readme/sources/scopyx-gates.svg`, drawn for the fifth article
   where it also had to work as a still, and it carries the reason in its own
   header.

   **The sentence beside each room is pinned to the drawing it describes.** That
   sentence becomes the file's `<title>` and its `aria-label`, which is what a
   screen reader is given instead of the picture, and it is hand-written about
   generated output, so nothing could ever notice it going wrong. Platform's
   said "seven emitters, one agent-event envelope, four consumers" for three
   weeks after the page was redrawn to twelve sources and five consumers, and
   the wrong sentence was the only place on the whole site still saying seven:
   the page, its prose and its own label were all correct.

   So each room carries a short digest of its drawing's text labels, and a
   redraw stops the generator with the old sentence printed and the new digest
   ready to paste. It digests the labels rather than the file, so moving a box
   or changing a colour asks nothing, and adding, removing or rewording a label
   always does. A count in a title cannot be checked against the drawing
   directly: that was tried, and comparing the numbers in the two strings gave
   four false positives ("one graph", "one SQLite file", "one browser control
   room", "three connectors") against the one real fault, which is a gate that
   gets switched off inside a week.

## Decisions that have no gate yet

**Held by this file alone: invariants 4 and 6.** Invariant 9 arrived with its gate on the day the fault was found, which is the standing rule working rather than being quoted. Invariant 2 is half held, and invariant 3 is now half held too: the manifest is enforced, the truth of what it records is not.

Invariants 1 and 2 are now `scripts/page-metadata.sh`, and it found invariant 2
being violated rather than merely unenforced: `console.html` carried a canonical
AND a noindex. The pair says opposite things, one asking for the URL to be the
authoritative version and the other asking for it to be dropped, and which wins
is somebody else's algorithm. Resolved by dropping the canonical, since that
page is deliberately not indexed and is not in the sitemap. `/enterprise` and
`/products` resolved the same contradiction the other way round, because those
want to be folded rather than dropped, and they already carry comments saying so.

**The check knows this site rather than counting blindly**, which matters:
its first version reported three failures, and all three were the two redirect
pages and the built `/demo` app, none of which authors its own head. Redirects
are checked for a canonical instead; generated output is skipped, because
measuring it measures the bundler.

It also does NOT require `og:description` to match the meta description. They
differ deliberately on all nineteen pages that have both: the search snippet is
held under 160 and the social card is allowed to run longer. Requiring a match
would be requiring a mistake.

Invariant 7 is `scripts/demo-bundle-current.sh`, added after the site was found
serving a demo built from an unmerged branch, with nothing anywhere able to say
so. Writing it turned up a defect in the check itself, which is worth recording
because it is the shape these fail in: the manifest was parsed through a command
substitution piped into `read`, which discards the exit status, so a manifest
missing a key produced empty values and then complained about a file named
`demo/`. It reported a real failure for the wrong reason, which is the same
thing as reporting a wrong one. Each of its six refusals was then triggered
deliberately and checked to fail for its OWN reason, after a first attempt at
that whose fixture stayed broken between cases and "proved" three of them on the
previous case's damage.

What still needs a reader: JSON-LD and the sitemap agreeing with the prose,
invariant 4's status sentences, and invariant 6. Invariant 3's numbers now have
owners; what still needs a person is running the five commands `numbers.json`
names and writing the dates back.

**Invariant 5 has never had the check this file claimed for it.** The line here
said "a wordlist grep across HTML, alt text and filenames" and no such script
exists; it was looked for on 2026-08-03 and is not in `scripts/`. That was
worth more than the missing grep: a sentence describing a check nobody wrote
reads as a check somebody is running, which is exactly how the rule then went
unnoticed for a fortnight. The invariant is now held by this file and by
`STACK` being the only thing the rail, the walk and the palette read from, so
a side project cannot get into them by being added to a list.

## Standing rule

An approved architecture decision is **not finished** until it is two things: a
numbered invariant in this file, and a gate in a script if it can be checked
structurally. Until then it is a document, and documents do not stop code.

## Conventions

- **No long dashes** anywhere: not in code, docs, commit messages, or PR
  bodies. Use a comma, a colon, parentheses, or a short hyphen.
- Nothing paid or metered gets enabled without telling the user first and
  getting agreement.
- Do not delete or revoke keys, tokens, or certificates on your own initiative.

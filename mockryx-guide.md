<!-- https://it-rat.com/mockryx-guide.html -->

# Mockryx guide

> How Mockryx fire drills work, how to run and download it, the drills on main not yet released, and what it does not prove yet.

The [Mockryx room](https://it-rat.com/services/mockryx.html) keeps the fire drill, the drawing of one target URL and three exit codes, and the common questions. This guide keeps the rest of what the room used to say: what a scenario names, how a reaction is proven, how a skipped guardrail is told from a gap, where it sits in the stack, how to run and download it, the drills on main, and the limits.

- [At a glance](https://it-rat.com/mockryx-guide.html#overview)

- [How it works](https://it-rat.com/mockryx-guide.html#how-it-works)

- [What it proves](https://it-rat.com/mockryx-guide.html#what-it-proves)

- [Where it sits](https://it-rat.com/mockryx-guide.html#where-it-sits)

- [Running it](https://it-rat.com/mockryx-guide.html#run)

- [What changed](https://it-rat.com/mockryx-guide.html#changes)

- [What changed in November](https://it-rat.com/mockryx-guide.html#changes-november)

- [Limits](https://it-rat.com/mockryx-guide.html#limits)

## Mockryx at a glance.

- **Prove every guardrail holds**, against your own gateway, before real traffic.

- **Status:** pre-1.0, and main is supported.

- **Core:** Go, an outbound-only CLI. **Scenarios:** YAML, one file each.

- **Target:** your own gateway, at /v1/messages.

- **Verdicts:** exit 0 held, 1 a real gap, 2 broken.

- **Licence:** Apache-2.0.

### What it is

A guardrail nobody has ever fired is a guess. Mockryx replays hostile scenarios (a fake secret in a prompt, a budget burn, a denied tool, a forged delegation chain, an unapproved action, an injected page, a quality drift, a reaction chain that has to reach the mail, and a provider outage) against the one URL you hand it: your own pre-production gateway, with a fake provider behind it. The enforcement path is the real one; the spend is not. CI reads the verdict as an exit code.

## One target URL. One report. Three exit codes.

A scenario file names a request in the Anthropic Messages shape, the status it must be answered with, the headers that must ride the response and, optionally, the off-path event that must follow. The runner sends it at your gateway's /v1/messages, reads the gateway's own answer, polls the NDJSON event logs the off-path services write, and folds everything into a report and an exit code a CI gate can act on. It never talks to anything but the gateway you name.

### Watch every guardrail answer for itself.

The room's simulation replays five of the drills, and the shape is the real record: three of those five ran live against a real gateway on disposable boxes, twice, and held both times, 0 gaps, $0 real spend. The other two are the Wardryx scenarios that ship in the same set. The provider behind the gateway is fake, so the burn the runaway drill attempts never reaches an invoice.

## Not a mock of your gateway. Your gateway.

### Scenarios are YAML, not code

One drill is one file: the request to send, the status the guardrail must answer, the headers it must stamp. It reads like the real call it imitates. A malformed file fails the whole load, because a safety check that vanishes silently is worse than one that fails loudly.

### In-path checks, on the real path

Assertions read the gateway's own answers: the breaker's 402, DLP's 403, the deny or hold riding the x-fuse-wardryx header. No mocked gateway in the middle, so the code you rehearse is the code production traffic meets.

### Async reaction checks

A drill can demand that the off-path services actually react, not only that the gateway answered. A gateway that blocks while nobody downstream notices is half a defence.

**Proving the services that answer later answered at all.** The gateway's own status and headers can only speak for the guardrails standing in the request path. Verdryx, Idryx and Qryx never touch that response: they react off path, on their own schedule, and record what they did as an agent-event envelope in the same NDJSON format everything else in the stack writes.

So a scenario can assert on that too. Name the source and the event type it expects, optionally how long to wait, and after the synchronous check passes the runner polls those event logs for a matching event correlated by the exact run id it put on the wire. Not "an event appeared", but "the event this request should have caused appeared".

Order matters here. A synchronous mismatch is never followed by an event check: chasing a downstream reaction to a request that did not even trigger the guardrail would turn one clear failure into two confusing ones. The drill reports the thing that actually broke.

### A provider that is up but failing

Three game-day drills rehearse it: `provider-5xx`, `provider-rate-limited` and `provider-timeout`. Each sends the operator's own gateway a call and checks the chain in order. The call comes back with the provider's own status, 503, 429 or 504. The gateway puts a `dependency_failed` for the run on the bus, from source tokenfuse. And the run reaches a person: an `alert_sent` from heraldyx. The drills use the existing event check only, add no scenario capability and declare no `requires`, so a miss is a finding and never a skip.

The provider is a local stub, `internal/providerstub`, started by `scripts/provider-stub.go` with `go run`. The script is excluded from the build, so the repository still builds one binary. The stub listens on loopback only and refuses any other address before binding, exiting 2. It makes no outbound call, and it holds a timeout for at most ten seconds, under Mockryx's own fifteen-second client timeout.

Each drill is run through a model of the chain: the stub, a gateway that passes the status through and writes `dependency_failed` to a hash-chained file, and a notifier that writes `alert_sent`, read back by the real event watcher. All three pass with the chain whole. Each fails on the status when the gateway hides the failure, on `tokenfuse/dependency_failed` when the bus is silent, and on `heraldyx/alert_sent` when nobody is told. The self-test runs every drill against a gateway that answers 200 to everything, and every run comes back failed.

### A skip cannot hide a gap

A guardrail that is off looks exactly like one that is broken. The runner insists on evidence before it calls a miss either one.

**The difference between a gap and a feature you never turned on.** A finding means the guardrail was supposed to hold and did not: something to fix today. A scenario that declares an optional guardrail is telling the runner something narrower, that a miss counts as a real gap only if there is other evidence the feature is actually wired in.

The evidence is the gateway's own response headers. If the header for that feature appears even once anywhere in the run, whatever its value, the feature is clearly live and a mismatch is a genuine finding. If it never appears across every attempt, the gateway plainly does not have it configured, and the scenario reports itself as not configured, with its raw mismatches dropped: they describe an absent feature, not a broken defence.

Two things can never be excused this way. A scenario with no optional guardrail declared, the budget breaker, is core and always on, so a miss there is always a finding. And a transport error, where the gateway could not be reached at all, is always a finding too: being unreachable is never evidence that a feature is merely switched off.

When you know a guardrail must be there, one flag turns even a skip into a failure. That is the honest way round: the tool refuses to claim a pass it cannot prove, and it refuses to cry gap it cannot prove either.

### CI-native exit codes

Exit 0: every drill held. Exit 1: a real defensive gap, fail the build. Exit 2: the harness itself is broken (bad flag, unreadable scenarios), so nothing was proven. Gate on 1, fix the pipeline on 2, and never let the two blur.

### Zero real spend by design

The provider behind the gateway is fake, so the runaway scenario can burn all it wants: the meter it trips is real, the invoice is not. And every hostile input stays inside your perimeter; Mockryx only ever talks to the one gateway URL you hand it.

## It picks fights with the rest of the stack. On purpose, in pre-prod.

In the request path, Mockryx rehearses [TokenFuse](https://it-rat.com/services/tokenfuse.html): the breaker's 402 and the DLP's 403, provoked deliberately and expected to answer. It does the same to [Wardryx](https://it-rat.com/services/wardryx.html), asserting that deny and hold verdicts land in the x-fuse-wardryx header. Off path, expect.event demands that [Verdryx](https://it-rat.com/services/verdryx.html), [Idryx](https://it-rat.com/services/idryx.html) and [Qryx](https://it-rat.com/services/qryx.html) visibly react to what just happened. And every finding it makes travels as sim_run and sim_finding events on the same bus as everything else: [the shared contract](https://it-rat.com/services/platform.html).

Why rehearsal belongs in CI, and what else it sits beside: [AI agent security](https://it-rat.com/ai-agent-security.html) and [AI agent governance](https://it-rat.com/ai-agent-governance.html).

## Two commands, one gateway URL.

```
./bin/mockryx run --gateway http://127.0.0.1:8080 ./scenarios
./bin/mockryx report out/report.json
```

Add `--save out/report.json` to keep the evidence. Point it at pre-prod, never at prod: the URL you pass is the only place it will ever send traffic.

### Download, any platform

Every one of those addresses always serves the newest release, so a link saved today still works after the next one. The asset names carry no version, which is what makes that true; the version lives inside the binary, where `mockryx version` reads it back.

## Four drills on main, not yet in a release

The last release is v0.2.1. These four drills are on main and are not in any release yet.

| drill | what it rehearses |
|---|---|
| Token flood | One request asks for a very large completion on a one-cent run budget. The gateway must refuse it before it is forwarded. |
| PII in a prompt | A support prompt carries a customer's email address and phone number. With PII blocking on, the call must be refused before any model sees it. |
| Poisoned tool description | A request declares a tool whose description orders the model to call another tool first and not to mention it. The gateway must answer the request, then deny a dangerous action in the same run. |
| Respelled allow-listed tool | A policy allows a tool by its exact name. A request that declares the same tool under a respelled name must be refused by the allow-list. |

What changed from 1 to 15 October 2026, release by release, is in [the stack's changes for October](https://it-rat.com/changes-2026-10.html#mockryx).

## What changed in November

| shipped in | what it does |
|---|---|
| on main | Three game-day drills for a provider that is up but failing (a 5xx, a rate limit and a timeout), and a loopback-only local stub they run against. |

## What it does not do, and what is not released yet.

- The last release is v0.2.1. The four drills above are on main and are not in any release yet.

- Of the five drills the room replays, three ran live against a real gateway on disposable boxes, twice; the other two are the Wardryx scenarios that ship in the same set.

- It is pre-1.0, and main is supported.

- A gateway response can only speak for the guardrails standing in the request path; off-path services are proven by their own events, and a synchronous mismatch is never followed by an event check.

- A scenario that declares an optional guardrail reports itself as not configured when the gateway never shows that feature's header; one flag turns even a skip into a failure.

- It only ever talks to the one gateway URL you hand it. Point it at pre-prod, never at prod.

## Back to the room.

The [Mockryx room](https://it-rat.com/services/mockryx.html) has the fire drill, the drawing and the common questions, and [the guides index](https://it-rat.com/guides.html) has the field itself.

<!-- https://it-rat.com/services/mockryx.html -->

# Mockryx, the pre-production plane

> Fire drills for your guardrails: YAML scenarios fired at a real gateway, asserting the 402, the 403 and the downstream reaction. Zero real spend, CI-native.

A guardrail nobody has ever fired is a guess. Mockryx replays five hostile scenarios (a fake secret in a prompt, a budget burn, a denied tool, a forged delegation chain, an unapproved action) against the one URL you hand it: your own pre-production gateway, with a fake provider behind it. The enforcement path is the real one; the spend is not. CI reads the verdict as an exit code.

## Watch every guardrail answer for itself.

This is a simulation, and the shape is the real drill record: three of these five scenarios ran live against a real gateway on disposable boxes, twice, and held both times, 0 gaps, $0 real spend. The other two are the Wardryx scenarios that ship in the same set. The provider behind the gateway is fake, so the burn the runaway drill attempts never reaches an invoice.

## One target URL. One report. Three exit codes.

A scenario file names a request in the Anthropic Messages shape, the status it must be answered with, the headers that must ride the response and, optionally, the off-path event that must follow. The runner sends it at your gateway's /v1/messages, reads the gateway's own answer, polls the NDJSON event logs the off-path services write, and folds everything into a report and an exit code a CI gate can act on. It never talks to anything but the gateway you name.

## Not a mock of your gateway. Your gateway.

### Scenarios are YAML, not code

One drill is one file: the request to send, the status the guardrail must answer, the headers it must stamp. It reads like the real call it imitates. A malformed file fails the whole load, because a safety check that vanishes silently is worse than one that fails loudly.

### In-path checks, on the real path

Assertions read the gateway's own answers: the breaker's 402, DLP's 403, the deny or hold riding the x-fuse-wardryx header. No mocked gateway in the middle, so the code you rehearse is the code production traffic meets.

### Async reaction checks

A drill can demand that the off-path services actually react, not only that the gateway answered. A gateway that blocks while nobody downstream notices is half a defence.

**Q: How a reaction is proven**

The gateway's own status and headers can only speak for the guardrails standing in the request path. Verdryx, Idryx and Qryx never touch that response: they react off path, on their own schedule, and record what they did as an agent-event envelope in the same NDJSON format everything else in the stack writes.

So a scenario can assert on that too. Name the source and the event type it expects, optionally how long to wait, and after the synchronous check passes the runner polls those event logs for a matching event correlated by the exact run id it put on the wire. Not "an event appeared", but "the event this request should have caused appeared".

Order matters here. A synchronous mismatch is never followed by an event check: chasing a downstream reaction to a request that did not even trigger the guardrail would turn one clear failure into two confusing ones. The drill reports the thing that actually broke.

### A skip cannot hide a gap

A guardrail that is off looks exactly like one that is broken. The runner insists on evidence before it calls a miss either one.

**Q: How the two are told apart**

A finding means the guardrail was supposed to hold and did not: something to fix today. A scenario that declares an optional guardrail is telling the runner something narrower, that a miss counts as a real gap only if there is other evidence the feature is actually wired in.

The evidence is the gateway's own response headers. If the header for that feature appears even once anywhere in the run, whatever its value, the feature is clearly live and a mismatch is a genuine finding. If it never appears across every attempt, the gateway plainly does not have it configured, and the scenario reports itself as not configured, with its raw mismatches dropped: they describe an absent feature, not a broken defence.

Two things can never be excused this way. A scenario with no optional guardrail declared, the budget breaker, is core and always on, so a miss there is always a finding. And a transport error, where the gateway could not be reached at all, is always a finding too: being unreachable is never evidence that a feature is merely switched off.

When you know a guardrail must be there, one flag turns even a skip into a failure. That is the honest way round: the tool refuses to claim a pass it cannot prove, and it refuses to cry gap it cannot prove either.

### CI-native exit codes

Exit 0: every drill held. Exit 1: a real defensive gap, fail the build. Exit 2: the harness itself is broken (bad flag, unreadable scenarios), so nothing was proven. Gate on 1, fix the pipeline on 2, and never let the two blur.

### Zero real spend by design

The provider behind the gateway is fake, so the runaway scenario can burn all it wants: the meter it trips is real, the invoice is not. And every hostile input stays inside your perimeter; Mockryx only ever talks to the one gateway URL you hand it.

## The drill you can afford to run every release.

A yearly pentest does real work Mockryx cannot: people, phishing, infrastructure. What it cannot do is tell you tomorrow morning that yesterday's config change broke the DLP. And unit tests with a mocked gateway mostly prove the mocks still pass. Mockryx drills the assembled thing.

|  | Mockryx | Annual pentest | “Trust the unit tests” |
|---|---|---|---|
| Cadence | Every release | Yearly | Whenever |
| Tests the assembled system | Real gateway, real policies | Sometimes | No: mocks all the way down |
| Costs real tokens | No | n/a | Sometimes |
| Proves off-path services react | Yes: expect.event | No | No |
| Who reads the result | A CI gate, every merge | A PDF for the board | Nobody |

### It picks fights with the rest of the stack. On purpose, in pre-prod.

In the request path, Mockryx rehearses [TokenFuse](https://it-rat.com/tokenfuse.html): the breaker's 402 and the DLP's 403, provoked deliberately and expected to answer. It does the same to [Wardryx](https://it-rat.com/wardryx.html), asserting that deny and hold verdicts land in the x-fuse-wardryx header. Off path, expect.event demands that [Verdryx](https://it-rat.com/verdryx.html), [Idryx](https://it-rat.com/idryx.html) and [Qryx](https://it-rat.com/qryx.html) visibly react to what just happened. And every finding it makes travels as sim_run and sim_finding events on the same bus as everything else: [the shared contract](https://it-rat.com/platform.html).

Why rehearsal belongs in CI, and what else it sits beside: [AI agent security](https://it-rat.com/ai-agent-security.html) and [AI agent governance](https://it-rat.com/ai-agent-governance.html).

Add `--save out/report.json` to keep the evidence. Point it at pre-prod, never at prod: the URL you pass is the only place it will ever send traffic.

**Q: Download, any platform**

Every one of those addresses always serves the newest release, so a link saved today still works after the next one. The asset names carry no version, which is what makes that true; the version lives inside the binary, where `mockryx version` reads it back.

## Rehearsing a defence before it is needed

**Q: How do I test that my guardrails actually work?**
Fire drills. Each scenario is a YAML file describing the request to send and the answer the guardrail must give, aimed at a real gateway with the guardrails live: the breaker's 402, DLP's 403, the deny or hold from the policy plane. No mocked gateway in the middle, so the code you rehearse is the code production traffic meets.

**Q: Does running the drills spend real money?**
No. The provider behind the gateway is fake, so a runaway scenario can burn as much as it likes: the meter it trips is real, the invoice is not. Every hostile input also stays inside your perimeter, because the harness only ever talks to the one gateway URL you hand it.

**Q: What if a guardrail simply is not configured?**
Then a miss is reported as not configured rather than as a gap, and only when there is no evidence anywhere in the run that the feature is live. A core guardrail with no optional declaration is always a finding, and so is a gateway that could not be reached at all. One flag turns even a skip into a failure when you know the guardrail must be there.

**Q: Can it gate CI?**
That is the intended home. Exit 0 means every drill held, exit 1 is a real defensive gap and should fail the build, exit 2 means the harness itself is broken so nothing was proven. Gate on 1, fix the pipeline on 2, and never let the two blur.

<!-- https://it-rat.com/services/mockryx.html -->

# Mockryx, the pre-production plane

> Fire drills for your guardrails: YAML scenarios fired at a real gateway, asserting the 402, the 403 and the downstream reaction. Zero real spend, CI-native.

A guardrail nobody has ever fired is a guess. Mockryx replays hostile scenarios against the one URL you hand it: your own pre-production gateway, with a fake provider behind it. The enforcement path is the real one; the spend is not. CI reads the verdict as an exit code.

## Watch every guardrail answer for itself.

This is a simulation replaying five of the drills, and the shape is the real record: three of those five ran live against a real gateway on disposable boxes, twice, and held both times, 0 gaps, $0 real spend. The other two are the Wardryx scenarios that ship in the same set.

## One target URL. One report. Three exit codes.

The runner sends a scenario at your gateway's /v1/messages, reads the gateway's own answer, polls the NDJSON event logs the off-path services write, and folds everything into a report and an exit code a CI gate can act on. It never talks to anything but the gateway you name.

## Not a mock of your gateway. Your gateway.

### Scenarios are YAML, not code

One drill is one file: the request to send, the status the guardrail must answer, the headers it must stamp.

### In-path checks, on the real path

Assertions read the gateway's own answers: the breaker's 402, DLP's 403, the deny or hold riding the x-fuse-wardryx header.

### Async reaction checks

A drill can demand that the off-path services actually react, not only that the gateway answered.

### A skip cannot hide a gap

A guardrail that is off looks exactly like one that is broken. The runner insists on evidence before it calls a miss either one.

### Drills for a failing provider

Three drills rehearse a provider that is up but failing: a 5xx, a rate limit and a timeout. Each checks the chain in order. The call comes back with the provider's own status, the gateway puts a dependency_failed for the run on the bus, and the run reaches a person. A local stub plays the provider.

## It picks fights with the rest of the stack. On purpose, in pre-prod.

In the request path, Mockryx rehearses [TokenFuse](https://it-rat.com/services/tokenfuse.html): the breaker's 402 and the DLP's 403, provoked deliberately and expected to answer. It does the same to [Wardryx](https://it-rat.com/services/wardryx.html), asserting that deny and hold verdicts land in the x-fuse-wardryx header.

## Point it at pre-prod, never at prod.

The URL you pass is the only place it will ever send traffic.

## Not yet in a release.

- The last release is v0.2.1. Four drills are on main and are not in any release yet: a token flood, PII in a prompt, a poisoned tool description and a respelled allow-listed tool.

### The Mockryx guide

## Rehearsing a defence before it is needed

**Q: How do I test that my guardrails actually work?**
Fire drills. Each scenario is a YAML file describing the request to send and the answer the guardrail must give, aimed at a real gateway with the guardrails live: the breaker's 402, DLP's 403, the deny or hold from the policy plane. No mocked gateway in the middle, so the code you rehearse is the code production traffic meets.

**Q: Does running the drills spend real money?**
No. The provider behind the gateway is fake, so a runaway scenario can burn as much as it likes: the meter it trips is real, the invoice is not. Every hostile input also stays inside your perimeter, because the harness only ever talks to the one gateway URL you hand it.

**Q: What if a guardrail simply is not configured?**
Then a miss is reported as not configured rather than as a gap, and only when there is no evidence anywhere in the run that the feature is live. A core guardrail with no optional declaration is always a finding, and so is a gateway that could not be reached at all. One flag turns even a skip into a failure when you know the guardrail must be there.

**Q: Can it gate CI?**
That is the intended home. Exit 0 means every drill held, exit 1 is a real defensive gap and should fail the build, exit 2 means the harness itself is broken so nothing was proven. Gate on 1, fix the pipeline on 2, and never let the two blur.

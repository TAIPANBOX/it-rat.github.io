<!-- https://it-rat.com/services/mockryx.html -->

# Mockryx, the pre-production plane

> Fire drills for your guardrails: YAML scenarios fired at a real gateway, asserting the 402, the 403 and the downstream reaction. Zero real spend, CI-native.

A guardrail nobody has ever fired is a guess. Mockryx replays hostile scenarios against the URL you hand it: your own pre-production gateway, with a fake provider behind it. The enforcement path is the real one; the spend is not. CI reads the verdict as an exit code.

## Watch every guardrail answer for itself.

A replay of five drills. Three of them ran live against a real gateway on disposable boxes, twice, and held: 0 gaps, $0 real spend.

## One target URL. One report. Three exit codes.

The runner sends a scenario at your gateway's /v1/messages, reads the gateway's own answer, polls the NDJSON event logs the off-path services write, and folds everything into a report and an exit code a CI gate can act on. It talks only to the URLs you name on the command line: your gateway and, for the optional broker drills, your MCP broker.

## Not a mock of your gateway. Your gateway.

One drill is one YAML file: the request to send, the status the guardrail must answer and the headers it must stamp. [In the guide](https://it-rat.com/mockryx-guide.html#what-it-proves)

Assertions read the gateway's own answers on the real path: the breaker's 402, DLP's 403 and the Wardryx verdict in x-fuse-wardryx. [In the guide](https://it-rat.com/mockryx-guide.html#what-it-proves)

A drill can require the off-path services to react on the bus, not only the gateway to answer. [In the guide](https://it-rat.com/mockryx-guide.html#what-it-proves)

A guardrail that is off looks like one that is broken, so the runner wants evidence before it calls a miss either one. [In the guide](https://it-rat.com/mockryx-guide.html#what-it-proves)

Four game-day drills rehearse a failing provider, from a 5xx, a rate limit and a timeout to a refused connection, and check the chain in order. [In the guide](https://it-rat.com/mockryx-guide.html#what-it-proves)

It talks only to the pre-prod URLs you hand it, a plain run leaves the game-day and broker drills out, and off-path services are proven by their own events. [In the guide](https://it-rat.com/mockryx-guide.html#limits)

## It picks fights with the rest of the stack. On purpose, in pre-prod.

In the request path it rehearses TokenFuse and Wardryx, and expects each of them to answer.

## Point it at pre-prod, never at prod.

The URLs you pass are the only places it will ever send traffic.

### The Mockryx guide

## Rehearsing a defence before it is needed

**Q: How do I test that my guardrails actually work?**
Fire drills. Each scenario is a YAML file describing the request to send and the answer the guardrail must give, aimed at a real gateway with the guardrails live: the breaker's 402, DLP's 403, the deny or hold from the policy plane. No mocked gateway in the middle, so the code you rehearse is the code production traffic meets.

**Q: Does running the drills spend real money?**
No. The provider behind the gateway is fake, so a runaway scenario can burn as much as it likes: the meter it trips is real, the invoice is not. Every hostile input also stays inside your perimeter, because the harness only talks to the URLs you hand it: the gateway and, for the broker drills, the MCP broker.

**Q: What if a guardrail simply is not configured?**
Then a miss is reported as not configured rather than as a gap, and only when there is no evidence anywhere in the run that the feature is live. A core guardrail with no optional declaration is always a finding, and so is a gateway that could not be reached at all. One flag turns even a skip into a failure when you know the guardrail must be there.

**Q: Can it gate CI?**
That is the intended home. Exit 0 means every drill held, exit 1 is a real defensive gap and should fail the build, exit 2 means the harness itself is broken so nothing was proven. Gate on 1, fix the pipeline on 2, and never let the two blur.

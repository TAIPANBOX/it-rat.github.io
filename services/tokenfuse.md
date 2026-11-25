<!-- https://it-rat.com/services/tokenfuse.html -->

# TokenFuse, the money plane

> A drop-in gateway that gives every agent run a budget and answers 402 when it is crossed. Anthropic and OpenAI wires, proven on three clouds and on premises.

TokenFuse is a drop-in gateway that gives every run a budget, watches its burn in real time, and cuts the circuit with an HTTP 402 the moment a run crosses its budget. Adoption is one base-URL change; no agent framework rewrite, no SDK lock-in.

## Watch the breaker do its job.

A replay of the exact shape of the live validation runs: an agent enters a retry loop against a $0.006 budget.

## One gateway in the path. One ledger everyone trusts.

Your agent's SDK points at TokenFuse instead of the provider. In the hot path: budgets, loop detection, a model router that downgrades routine calls, a semantic cache, DLP and the Wardryx policy hook.

## Not a dashboard. A set of hands on the wheel.

The run is the unit that pays: a sub-agent's run rolls up into its parent, so its spend must fit inside every ancestor's budget. [In the guide](https://it-rat.com/tokenfuse-guide.html#how-it-works)

A sustained loop trips the breaker, and a fan-out explosion opens an incident in the Cloud, before either becomes a four-digit night. [In the guide](https://it-rat.com/tokenfuse-guide.html#how-it-works)

Reserve-then-settle accounting prices each call before it is sent, with an estimate that is honest about being one. [In the guide](https://it-rat.com/tokenfuse-guide.html#how-it-works)

tokenfuse focus-export writes the call trace as a FOCUS-style CSV, one row per call with agent and run columns, for the dashboards finance already trusts. [In the guide](https://it-rat.com/tokenfuse-guide.html#how-it-works)

A run's taint follows what an enforcement point saw happen, such as the MCP server that answered, not the tool name the agent reported. [In the guide](https://it-rat.com/tokenfuse-guide.html#how-it-works)

A provider that keeps failing is one incident in the Cloud console and API, while each per-call event stays on the bus. [In the guide](https://it-rat.com/tokenfuse-guide.html#how-it-works)

By default one gateway runs with its ledger in memory, a fleet counts its own calls rather than sharing a cap, and the router and cache start off. [In the guide](https://it-rat.com/tokenfuse-guide.html#limits)

### The loud neighbor everyone listens to.

TokenFuse asks [Wardryx](https://it-rat.com/services/wardryx.html) before letting a declared tool through, and stamps the verdict on the response. Everything travels as one envelope, the agent-event, and [Genaryx](https://it-rat.com/genaryx.html) lifts that same signed kill into a console you reach over your own tunnel, where it becomes a passkey break-glass ceremony.

Run it from [the repository](https://github.com/TAIPANBOX/tokenfuse#-get-started), where the one-line command lives beside the image tag it pulls.

Then point `ANTHROPIC_BASE_URL` at `localhost:4100` and give your next run a run id and a budget (the x-fuse-run-id and x-fuse-budget-usd headers). A call with no run id is refused with 400 metering_required. That's the whole migration.

## It stops the spend. Two neighbours stop other things.

A breaker answers a runaway. A stolen delegation is [Vouchryx](https://it-rat.com/services/vouchryx.html)'s, and next month's invoice is [CostCrew](https://it-rat.com/services/costcrew.html)'s.

### The TokenFuse guide

## How teams put a ceiling on agent spend

**Q: How do I cap what an AI agent can spend?**
Give the run a budget. Every call is priced before it happens, the reserve is taken against that budget, and the call that would cross the cap is refused with an HTTP 402 before the provider ever sees it. Budgets nest along the run tree, so a sub-agent's run also has to fit inside every ancestor run's budget. A business unit can also have a monthly cap, which the gateway enforces in enforce mode.

**Q: What happens to my agent when it hits the budget?**
It gets a 402 with the reason, which is a status every framework already understands, and an incident is recorded against that run. Nothing else in the fleet is affected, and the spend that would have followed simply never happens.

**Q: Do I have to rewrite my agent to use it?**
No. It is a one-line base-URL change to a gateway that speaks the Anthropic Messages API and the OpenAI chat completions API. Set TOKENFUSE_MODE=shadow first and it prices and records everything while refusing nothing, so you can see what would have been blocked before anything is. Its own bookkeeping fails open, so a lost event or a failed telemetry push never refuses a call; the one exception is the start, when a gateway with a Cloud configured answers 503 seed_pending until it has read its money state. What happens when the policy plane is unreachable is the deployment's choice, and all three launchers ship it closed.

**Q: Can it catch a retry loop before the bill does?**
That is the case it was built for. A sustained loop trips the breaker, and a fan-out explosion opens an incident in the Cloud; either looks the same as a compromised agent from the budget's side. In the live campaign, the runaway that mattered was caught and killed on the day, not on the invoice.

**Q: Does it still work with several gateways behind a load balancer?**
In the cluster build, yes: the spend ledger is raft-replicated and the affordability check is linearized across the fleet, so four nodes on four machines admit exactly what one budget allows. The cluster record tests that with 30 concurrent reserves against a 5-unit budget, a kill of the leader and a real network partition. That build is optional and ships as its own image tag, not what the default image runs; the default profile is one gateway whose ledger lives in memory and is read back from the Cloud when it starts, each run's spend over the last 31 days, so a restart does not hand a run its budget again. That read-back does not let two gateways share one budget; only the cluster build does.

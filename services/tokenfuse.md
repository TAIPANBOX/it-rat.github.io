<!-- https://it-rat.com/services/tokenfuse.html -->

# TokenFuse, the money plane

> A drop-in gateway that gives every agent run a budget and answers 402 when it is crossed. Anthropic and OpenAI wires, proven on three clouds and on premises.

TokenFuse is a drop-in gateway that gives every run a budget, watches its burn in real time, and cuts the circuit with an HTTP 402 the moment a run crosses its budget. Adoption is one base-URL change; no agent framework rewrite, no SDK lock-in.

## Watch the breaker do its job.

This is a simulation, but not a fantasy: it replays the exact shape of the live validation runs. An agent enters a retry loop against a $0.006 budget.

## One gateway in the path. One ledger everyone trusts.

Your agent's SDK points at TokenFuse instead of the provider. In the hot path: budgets, loop detection, a model router that downgrades routine calls, a semantic cache, DLP and the Wardryx policy hook.

## Not a dashboard. A set of hands on the wheel.

### Per-run budgets

The run is the unit that pays. A sub-agent's run rolls up into its parent run, so its spend has to fit inside every ancestor's budget.

### Loop detection

A retrying agent looks exactly like a compromised one from the budget's side. Sustained loops and fan-out explosions trip the breaker before they become a four-digit night.

### Burn forecast

Reserve-then-settle accounting prices each call before it happens. The estimate is fast and honest about being an estimate.

### FOCUS export

Agent spend lands in the same FinOps Foundation format as the rest of your cloud bill, so showback and chargeback reuse the pipes and dashboards finance already trusts.

### A label from the act

A run's taint follows what an enforcement point saw happen, not the tool name the agent reported. The MCP broker labels a call by the server that answered, and a search the provider ran itself labels the run too.

### One incident per failing provider

A provider that keeps failing is one incident in the Cloud console and API, not one per call. The per-call event stays on the bus.

### The loud neighbor everyone listens to.

TokenFuse asks [Wardryx](https://it-rat.com/services/wardryx.html) before letting a declared tool through, and stamps the verdict on the response. Everything travels as one envelope, the agent-event, and [Genaryx](https://it-rat.com/genaryx.html) lifts that same signed kill into a console you reach over your own tunnel, where it becomes a passkey break-glass ceremony.

Run it from [the repository](https://github.com/TAIPANBOX/tokenfuse#-get-started), where the one-line command lives beside the image tag it pulls.

Then point `ANTHROPIC_BASE_URL` at `localhost:4100` and give your next run a budget header. That's the whole migration.

## It stops the spend. Two neighbours stop other things.

A breaker is the right answer to a runaway and the wrong one to a compromised delegation: [Vouchryx](https://it-rat.com/services/vouchryx.html) ends that authority at every enforcement point at once. And a ceiling in the request path says nothing about the invoice that arrives a month later: [CostCrew](https://it-rat.com/services/costcrew.html) is where a bill gets taken apart, allocated and closed.

## What the default install does not do.

- The raft cluster build is an optional build, not what the shipped images run: those run one gateway with its ledger in memory.

- A business unit's monthly cap is not yet shared across a fleet of gateways: each gateway counts its own calls on top of a tally it reads from the Cloud when it starts.

- The model router and the cache ship switched off: the router is off by default, and the cache is off in the gateway and in the launchers.

### The TokenFuse guide

## How teams put a ceiling on agent spend

**Q: How do I cap what an AI agent can spend?**
Give the run a budget. Every call is priced before it happens, the reserve is taken against that budget, and the call that would cross the cap is refused with an HTTP 402 before the provider ever sees it. Budgets nest along the run tree, so a sub-agent's run also has to fit inside every ancestor run's budget. A business unit can also have a monthly cap, which the gateway enforces in enforce mode.

**Q: What happens to my agent when it hits the budget?**
It gets a 402 with the reason, which is a status every framework already understands, and an incident is recorded against that run. Nothing else in the fleet is affected, and the spend that would have followed simply never happens.

**Q: Do I have to rewrite my agent to use it?**
No. It is a one-line base-URL change to a gateway that speaks the Anthropic Messages API and the OpenAI chat completions API. Run it in shadow mode first and it prices and records everything while refusing nothing, so you can see what would have been blocked before anything is. Its own bookkeeping fails open, so a lost event or an unreachable control plane never refuses a call; what happens when the policy plane is unreachable is the deployment's choice, and both launchers ship it closed.

**Q: Can it catch a retry loop before the bill does?**
That is the case it was built for. A sustained loop or a fan-out explosion looks the same as a compromised agent from the budget's side, and both trip the breaker. In the live campaign, the runaway that mattered was caught and killed on the day, not on the invoice.

**Q: Does it still work with several gateways behind a load balancer?**
In the cluster build, yes: the spend ledger is raft-replicated and the affordability check is linearized across the fleet, so four nodes on four machines admit exactly what one budget allows. The cluster record tests that with 30 concurrent reserves against a 5-unit budget, a kill of the leader and a real network partition. That build is optional and not what the shipped images run; the default profile is one gateway whose ledger lives in memory and is read back from the Cloud when it starts, each run's spend over the last 31 days, so a restart does not hand a run its budget again. That read-back does not let two gateways share one budget; only the cluster build does.

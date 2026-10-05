<!-- https://it-rat.com/services/tokenfuse.html -->

# TokenFuse, the money plane

> A drop-in gateway that gives every agent run a budget and answers 402 when it is crossed. Anthropic and OpenAI wires, proven on three clouds and on premises.

Observability tells you about the fire in next month's bill. TokenFuse is the extinguisher: a drop-in gateway that gives every run a budget, watches its burn in real time, and cuts the circuit with an HTTP 402 the moment a run crosses its budget. Adoption is one base-URL change; no agent framework rewrite, no SDK lock-in.

## Watch the breaker do its job.

This is a simulation, but not a fantasy: it replays the exact shape of the live validation runs. An agent enters a retry loop against a $0.006 budget. Four calls land. The reserve for the fifth would cross the cap, so the ledger refuses it.

## One gateway in the path. One ledger everyone trusts.

Your agent's SDK points at TokenFuse instead of the provider. In the hot path: budgets, loop detection, a model router that downgrades routine calls, a semantic cache, DLP and the Wardryx policy hook. Behind it: the spend ledger, in one process by default; the optional cluster build replicates it with raft, so five gateways on five machines still admit exactly what one budget allows.

## Not a dashboard. A set of hands on the wheel.

### Per-run budgets

Company, team, agent, run: budgets nest, and the run is the unit that pays. Cross the cap and the answer is a clean 402 your framework already understands, not a Slack message at 9am. Since v1.5.0 an operator can also cap the budget a caller declares for its own run: `TOKENFUSE_MAX_RUN_BUDGET_USD` lowers a larger one to the ceiling and the answer says so in `x-fuse-budget-clamped`. The launchers set it to USD 5.00. It bounds each run, not an agent's total: a new run id gets a new ceiling.

**Q: How enforcement works**

Budgets are hierarchical and checked all-or-nothing. A sub-agent's spend rolls up and is tested against every ancestor it belongs to, so a run cannot slip under its own cap while quietly breaking the team's. The run is the unit that pays, because a per-key limit cannot tell one agent's afternoon of honest work from the same key looping on itself.

Accounting is reserve then settle. Each call is priced before it happens, the reserve is taken, and the real cost settles afterwards; a call that would cross the cap is refused before the provider ever sees it. Models the price book does not recognise get a fallback price rather than passing through untracked, because untracked spend is exactly the failure mode this exists to remove.

Adoption is a one-line base-URL swap, and the gateway runs in shadow mode first: it prices and records everything while refusing nothing, so you can see what would have been blocked before anything is. Its own bookkeeping fails open: a telemetry push, an event write or a control-plane call that fails never refuses a call. The one failure mode that is a choice is the policy hook, and the launchers make it for you: both ship it fail-closed, so a policy plane that cannot be reached refuses every governed call rather than waving it through. That is measured, not read off a config file: on 2026-09-17 the policy plane was stopped under a box governing two clouds and every call came back 403 in 0.3 s until it was started again. The enforcement decision itself is in-process Rust, about 0.4 microseconds at p99. The thing standing between an agent and a four-digit night should not be the slow part.

### Loop detection

A retrying agent looks exactly like a compromised one from the budget's side. Sustained loops and fan-out explosions trip the breaker before they become a four-digit night.

### Burn forecast

Reserve-then-settle accounting prices each call before it happens, with a built-in price book (the Claude 4.5 and GPT-4o families) and a deliberately high fallback rate for a model id it does not know, flagged on the response, so an unknown model is refused sooner rather than tracked never. The estimate is fast and honest about being an estimate.

### Model router

Routine calls ride a cheaper model that still clears your quality bar; hard ones stay on the frontier model. In live runs the router and cache together stripped about 22% of routine spend. Both ship switched off in the launchers (the router off, the cache in shadow), so that figure arrives when you turn them on, not by default.

### Cluster build: a raft-replicated ledger

An optional build, not what the shipped images run. Three machines held one shared budget through a leader kill and a real network partition: majority kept serving, the isolated node could not overspend, nothing split-brained.

**Q: What it survives**

The images every launcher installs run one gateway with its ledger in memory, and a restart no longer starts every run at zero. Since v1.4.1 the gateway reads each run's spend back from the Cloud before it serves, for runs active in the last 31 days, and since v1.6.0 a gateway at a remote site does the same through a read scoped to its own site. With no Cloud configured there is nothing to read back, and a run starts from zero. The read-back is proven by tests, and the remote-site half on release binaries behind a stand-in for the hub entry, not yet on a live hub. A budget only means something if two gateways racing each other cannot both spend it, and that is what the cluster build is for, a separate build of the same binary: there the ledger is a raft state machine, and the affordability check is linearized across the whole fleet: five gateways on five machines admit exactly what one budget allows, not five copies of it.

In that build, with durable storage on redb, a budget outlives more than a node crash: it survives a full process restart, because a cap that resets when a process dies is a cap an unlucky deploy can hand back to a runaway.

That was tested rather than assumed. A four-node cluster across two datacenters took a leader kill and a real network partition: the majority side kept serving, the isolated node could not overspend, and nothing split-brained. Enforcement then held under a burst of 34 concurrent agents, and the cost accounting was run on the same protocol against Hetzner, AWS and GCP so the numbers could be compared honestly.

### FOCUS export

Agent spend lands in the same FinOps Foundation format as the rest of your cloud bill, so showback and chargeback reuse the pipes and dashboards finance already trusts.

### The loud neighbor everyone listens to.

TokenFuse asks [Wardryx](https://it-rat.com/wardryx.html) before letting a declared tool through, and stamps the verdict on the response. Its Parquet traces are the raw material [Verdryx](https://it-rat.com/verdryx.html) prices outcomes from. [Mockryx](https://it-rat.com/mockryx.html) attacks it on purpose in pre-prod. [Idryx](https://it-rat.com/idryx.html) correlates its events into the identity graph. Everything travels as one envelope, the agent-event, and [Genaryx](https://it-rat.com/genaryx.html) lifts that same signed kill into a console you reach over your own tunnel, where it becomes a passkey break-glass ceremony. [Typryx](https://it-rat.com/typryx.html) sits behind the MCP broker as a named upstream; its `request.complexity` template maps onto this router's own task classes, in shadow mode only, planned rather than built.

Where this fits in the wider practice: [FinOps for AI](https://it-rat.com/finops-for-ai.html) on managing spend that creates itself, and [AI agent governance](https://it-rat.com/ai-agent-governance.html) on the rest of the runtime controls.

Run it from [the repository](https://github.com/TAIPANBOX/tokenfuse#-get-started), where the one-line command lives beside the image tag it pulls.

Then point `ANTHROPIC_BASE_URL` at `localhost:4100` and give your next run a budget header. That's the whole migration. Behind a launcher, a header above USD 5.00 is lowered to the operator's ceiling unless the operator raises it.

Want more than the gateway? [Run the live services locally](https://it-rat.com/platform.html#run) in one command.

**Q: How this one ships**

The current release is v1.6.0. The image is the way to run it in front of traffic; the binaries, since v0.4.3, are for a laptop and a first look: one file, `TOKENFUSE_UPSTREAM` set, and it listens. Each address always serves the newest release: the asset names carry no version, so a link saved today still works after the next one. No Windows build yet, and saying so is cheaper than a broken link.

## It stops the spend. Two neighbours stop other things.

A breaker is the right answer to a runaway and the wrong one to a compromised delegation, where the money is affordable and the problem is that the agent may act for somebody at all. [Vouchryx](https://it-rat.com/vouchryx.html) ends that authority at every enforcement point at once. And a ceiling in the request path says nothing about the invoice that arrives a month later: [CostCrew](https://it-rat.com/costcrew.html) is where a bill gets taken apart, allocated and closed, by a crew of agents whose work a person stamps.

## How teams put a ceiling on agent spend

**Q: How do I cap what an AI agent can spend?**
Give the run a budget. Every call is priced before it happens, the reserve is taken against that budget, and the call that would cross the cap is refused with an HTTP 402 before the provider ever sees it. Budgets nest, so a run also has to fit inside its agent, team and company caps.

**Q: What happens to my agent when it hits the budget?**
It gets a 402 with the reason, which is a status every framework already understands, and an incident is recorded against that run. Nothing else in the fleet is affected, and the spend that would have followed simply never happens.

**Q: Do I have to rewrite my agent to use it?**
No. It is a one-line base-URL change to a gateway that speaks the Anthropic Messages API and the OpenAI chat completions API. Run it in shadow mode first and it prices and records everything while refusing nothing, so you can see what would have been blocked before anything is. Its own bookkeeping fails open, so a lost event or an unreachable control plane never refuses a call; what happens when the policy plane is unreachable is the deployment's choice, and both launchers ship it closed.

**Q: Can it catch a retry loop before the bill does?**
That is the case it was built for. A sustained loop or a fan-out explosion looks the same as a compromised agent from the budget's side, and both trip the breaker. In the live campaign, the runaway that mattered was caught and killed on the day, not on the invoice.

**Q: Does it still work with several gateways behind a load balancer?**
In the cluster build, yes: the spend ledger is raft-replicated and the affordability check is linearized across the fleet, so five gateways on five machines admit exactly what one budget allows, and that was tested through a leader kill and a real network partition. That build is optional and not what the shipped images run; the default profile is one gateway whose ledger lives in memory and is read back from the Cloud when it starts, each run's spend over the last 31 days, so a restart does not hand a run its budget again. That read-back does not let two gateways share one budget; only the cluster build does.

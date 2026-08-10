<!-- https://it-rat.com/services/tokenfuse.html -->

# TokenFuse, the money plane

> A drop-in gateway that gives every agent run a budget and answers 402 the moment it is crossed. Raft-replicated, validated on Hetzner, AWS and GCP.

Observability tells you about the fire in next month's bill. TokenFuse is the extinguisher: a drop-in gateway that gives every run a budget, watches its burn in real time, and cuts the circuit with an HTTP 402 the moment a run crosses its budget. Adoption is one base-URL change; no agent framework rewrite, no SDK lock-in.

## Watch the breaker do its job.

This is a simulation, but not a fantasy: it replays the exact shape of the live validation runs. An agent enters a retry loop against a $0.006 budget. Four calls land. The reserve for the fifth would cross the cap, so the raft ledger refuses it, and every node agrees.

## One gateway in the path. One ledger everyone trusts.

Your agent's SDK points at TokenFuse instead of the provider. In the hot path: budgets, loop detection, a model router that downgrades routine calls, a semantic cache, DLP and the Wardryx policy hook. Behind it: a raft-replicated spend ledger, so five gateways on five machines still admit exactly what one budget allows.

## Not a dashboard. A set of hands on the wheel.

### Per-run budgets

Company, team, agent, run: budgets nest, and the run is the unit that pays. Cross the cap and the answer is a clean 402 your framework already understands, not a Slack message at 9am.

**Q: How enforcement works**

Budgets are hierarchical and checked all-or-nothing. A sub-agent's spend rolls up and is tested against every ancestor it belongs to, so a run cannot slip under its own cap while quietly breaking the team's. The run is the unit that pays, because a per-key limit cannot tell one agent's afternoon of honest work from the same key looping on itself.

Accounting is reserve then settle. Each call is priced before it happens, the reserve is taken, and the real cost settles afterwards; a call that would cross the cap is refused before the provider ever sees it. Models the price book does not recognise get a fallback price rather than passing through untracked, because untracked spend is exactly the failure mode this exists to remove.

Adoption is a one-line base-URL swap, and the gateway runs in shadow mode first: it prices and records everything while refusing nothing, so you can see what would have been blocked before anything is. It is fail-open by design, so it never becomes the single point of failure between your agents and their provider, and the enforcement decision itself is in-process Rust, about 0.4 microseconds at p99. The thing standing between an agent and a four-digit night should not be the slow part.

### Loop detection

A retrying agent looks exactly like a compromised one from the budget's side. Sustained loops and fan-out explosions trip the breaker before they become a four-digit night.

### Burn forecast

Reserve-then-settle accounting prices each call before it happens, with the 2026 model price book built in. The estimate is fast and honest about being an estimate.

### Model router

Routine calls ride a cheaper model that still clears your quality bar; hard ones stay on the frontier model. In live runs the router and cache together stripped about 22% of routine spend.

### Raft-replicated ledger

Three machines held one shared budget through a leader kill and a real network partition: majority kept serving, the isolated node could not overspend, nothing split-brained.

**Q: What it survives**

A budget only means something if two gateways racing each other cannot both spend it. In cluster mode the ledger is a raft state machine, and the affordability check is linearized across the whole fleet: five gateways on five machines admit exactly what one budget allows, not five copies of it.

With durable storage on redb, a budget outlives more than a node crash: it survives a full process restart, because a cap that resets when a process dies is a cap an unlucky deploy can hand back to a runaway.

That was tested rather than assumed. A four-node cluster across two datacenters took a leader kill and a real network partition: the majority side kept serving, the isolated node could not overspend, and nothing split-brained. Enforcement then held under a burst of 34 concurrent agents, and the cost accounting was run on the same protocol against Hetzner, AWS and GCP so the numbers could be compared honestly.

### FOCUS export

Agent spend lands in the same FinOps Foundation format as the rest of your cloud bill, so showback and chargeback reuse the pipes and dashboards finance already trusts.

## Where the breaker lives matters.

We would rather argue with the strongest version of the alternative than with a straw man. The best in-line proxies in this space do real work: per-agent budgets, several independent kill triggers, even fleet control planes. Every one of those triggers is software, reachable from the same estate it guards. Ours adds one that is not: a kill signed on the device's own secure element, hardware that never sat in the request path, and verifiable offline long after the incident is cold.

|  | TokenFuse | In-line budget proxies | Observability dashboards |
|---|---|---|---|
| Enforcement | In-line 402, seconds | In-line, in the request path | Alert after the fact |
| Kill switch | Software triggers, plus one that is not: an ES256 signature from a separate device's secure element, verifiable offline | Remote APIs, signals, sentinel files: all software, all reachable from the estate they guard | None |
| Shared budget across machines | Raft consensus, byte-identical state on every node | Per-agent budgets; fleet planes exist, typically behind commercial licences | n/a |
| Cost optimization | Router + semantic cache, measured 22% | Rarely a goal | Recommendations only |
| FinOps handoff | FOCUS format, the one finance already reads | Security formats: SIEM, syslog, OTLP. Not the ones finance reads | Vendor lock |
| Fleet, incidents, evidence | Cloud plane + audit hash chain | Policy distribution and evidence logs in the strongest tools | Strong, read-only |

### The loud neighbor everyone listens to.

TokenFuse asks [Wardryx](https://it-rat.com/wardryx.html) before letting a declared tool through, and stamps the verdict on the response. Its Parquet traces are the raw material [Verdryx](https://it-rat.com/verdryx.html) prices outcomes from. [Mockryx](https://it-rat.com/mockryx.html) attacks it on purpose in pre-prod. [Idryx](https://it-rat.com/idryx.html) correlates its events into the identity graph. Everything travels as one envelope, the agent-event, and [Genaryx](https://it-rat.com/genaryx.html) lifts that same signed kill into a console you reach over your own tunnel, where it becomes a passkey break-glass ceremony.

Where this fits in the wider practice: [FinOps for AI](https://it-rat.com/finops-for-ai.html) on managing spend that creates itself, and [AI agent governance](https://it-rat.com/ai-agent-governance.html) on the rest of the runtime controls.

Run it from [the repository](https://github.com/TAIPANBOX/tokenfuse#-get-started), where the one-line command lives beside the image tag it pulls.

Then point `ANTHROPIC_BASE_URL` at `localhost:4100` and give your next run a budget header. That's the whole migration.

Want more than the gateway? [Run the live services locally](https://it-rat.com/platform.html#run) in one command.

**Q: How this one ships**

No per-platform binaries here, and the honest reason is that a gateway sits in front of traffic rather than on a laptop: it ships as an image. The tag and the command to run it live in the repository, next to the version they pull.

## How teams put a ceiling on agent spend

**Q: How do I cap what an AI agent can spend?**
Give the run a budget. Every call is priced before it happens, the reserve is taken against that budget, and the call that would cross the cap is refused with an HTTP 402 before the provider ever sees it. Budgets nest, so a run also has to fit inside its agent, team and company caps.

**Q: What happens to my agent when it hits the budget?**
It gets a 402 with the reason, which is a status every framework already understands, and an incident is recorded against that run. Nothing else in the fleet is affected, and the spend that would have followed simply never happens.

**Q: Do I have to rewrite my agent to use it?**
No. It is a one-line base-URL change to a gateway that speaks the Anthropic Messages API. Run it in shadow mode first and it prices and records everything while refusing nothing, so you can see what would have been blocked before anything is. It is fail-open, so it never becomes a single point of failure.

**Q: Can it catch a retry loop before the bill does?**
That is the case it was built for. A sustained loop or a fan-out explosion looks the same as a compromised agent from the budget's side, and both trip the breaker. In the live campaign, the runaway that mattered was caught and killed on the day, not on the invoice.

**Q: Does it still work with several gateways behind a load balancer?**
Yes. The spend ledger is raft-replicated and the affordability check is linearized across the fleet, so five gateways on five machines admit exactly what one budget allows. That was tested through a leader kill and a real network partition.

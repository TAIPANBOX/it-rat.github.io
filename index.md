<!-- https://it-rat.com/index.html -->

# IT-RAT, the agent-governance stack

> Open-source runtime governance for AI agents: budgets, policy, memory, identity, cryptography, quality and pre-production drills. Apache-2.0, self-hosted.

A new hire gets a contract, a budget, a badge and a manager. An AI agent usually gets an admin key and a prayer. We build the open-source stack that closes that gap: seven services that meter, police, remember, identify, audit and rehearse your agents at runtime, proven on real infrastructure before anyone saw a slide about it. Three more stand next to them: alerts by mail, a record nobody can quietly shorten, and a kill switch out of band.

## One corridor, every door on it.

Every service has its own room: what it does, how it behaves over a live time window, and where it sits in the wiring. Twelve rooms, all Apache-2.0, with nothing behind a licence. Genaryx, first on the rail, is the control room, and it runs on your own infrastructure like the rest. After it, the seven services that are the stack, then three that stand beside it: alerts, the record, and the switch out of band. Platform, last, is the contract they all share. Walk it with the arrows on each page, scroll this rail sideways, or hit `⌘K` and type two letters.

### Genaryx

The control room over all of it, in your browser on your own box.

### Engram

The SQLite of agent memory.

### TokenFuse

Runtime spend control and the in-line kill switch.

### Wardryx

Policy decisions with a human in the loop.

### Idryx

One identity graph for humans, keys and agents.

### Qryx

Cryptography inventory and post-quantum risk.

### Verdryx

Cost per correctly resolved case, not per token.

### Mockryx

Fire drills that prove guardrails hold.

### Heraldyx

The box writes to you, with a link and never a button.

### Scopyx

Agents reach the web through a decision, not around one.

### TokenFuse Pocket

The kill switch on a device the agent's host never touches.

### Trailryx

A record nobody can quietly change or shorten.

### Platform

Agent Passport, shared contract, Terraform.

## One passport, one event bus, four planes of control.

Every request carries an Agent Passport. Money and policy sit in the request path; memory, identity, crypto, quality and rehearsal watch the same NDJSON event stream off-path. Nothing here is a dashboard after the fact: the gateway enforces in-line, in seconds. Three more sit beside those seven services rather than inside them, which is why this diagram has seven boxes while the corridor above has twelve doors: heraldyx mails you, Trailryx keeps the record, Pocket holds the switch out of band.

New to this? [Six guides](https://it-rat.com/guides.html) explain the field rather than the products: [agent governance](https://it-rat.com/ai-agent-governance.html), [FinOps for AI](https://it-rat.com/finops-for-ai.html), [agent security](https://it-rat.com/ai-agent-security.html), [observability versus governance](https://it-rat.com/ai-observability-vs-governance.html), [MCP security](https://it-rat.com/mcp-security.html), and [agent identity](https://it-rat.com/agent-identity.html). Four more cover this stack in practice: [a first alert](https://it-rat.com/first-alert.html), [one incident end to end](https://it-rat.com/one-incident-end-to-end.html), [what runs where and what it costs](https://it-rat.com/what-runs-where.html), and [what is proven and what is not](https://it-rat.com/what-is-proven.html).

## Validated on real infrastructure. Then torn down.

Before this site existed, the stack ran on disposable boxes across Hetzner, AWS and GCP with a real Anthropic key: four physical machines holding one budget over a real network, a partition with no split-brain, and a kill switch cutting real spend. Then the same stack came up again as a five-node Kubernetes cluster on each of those three clouds, which is where the cost of the governance itself finally got measured.

**Q: How these numbers were produced**

Every number above came from a run against real infrastructure, not a benchmark harness written to flatter us. The boxes were disposable, the model calls were real and paid for, and nothing from the campaign is still standing: the machines were deleted, the key revoked.

**Money.** Four nodes across two datacenters held one budget through a leader kill and a real network partition: the majority kept serving, the isolated node could not overspend, and the state stayed byte-identical on every node. Under 500 concurrent agents against a fixed budget, the ledger admitted exactly what the budget allowed and no more.

**Policy.** An enriched multi-agent campaign produced 176 real enforcement decisions with differentiated rights: an analyst agent refused a wire transfer that a treasury agent was allowed, an unattested agent refused until it attested, and shell execution refused for everyone regardless of identity. Fired as a 34-request concurrent burst, the decision point still sorted them exactly right.

**The rest.** Qryx scanned 25,586 real Linux binaries, stripped, static and truncated among them, without a crash. Engram's reflection ran against real Claude output three times on three topologies with zero contradictions. Verdryx priced a correctly resolved case at $0.00042. Mockryx fired three hostile drills against a real gateway twice, with zero gaps and zero real spend, because the provider behind that gateway was fake while every guardrail in front of it was live.

**At cluster scale.** The same manifests then came up as a five-node cluster on each of the three clouds, to answer the question the campaign above could not: what does the supervision itself cost. Six clusters went up in all: a quota ceiling capped the first GCP attempt at three nodes, and AWS was rebuilt twice, the last time a chip generation lower, once it turned out the first result had compared silicon rather than clouds. One policy pod peaks at about 2,449 decisions a second and answers in 3.2ms at p50 while the queue is short. On identical silicon the two hyperscalers land 1.2% apart, which makes choosing between them procurement rather than engineering. At full load the infrastructure under the control plane works out at EUR 0.024 per million governed decisions on Hetzner and about USD 0.21 to USD 0.23 on AWS and GCP. That is what the machines cost to run. What binds first is not the processor but the evidence: every decision is audited, not a sample of them, at 426 bytes each, which is 614 MB a day at a thousand calls a minute. Provability is measured in gigabytes and can be budgeted a year ahead from a single number.

**And what it caught.** Live testing found real bugs, which is the point of doing it. Two of them, both in the policy plane, were invisible to sequential test traffic: a request that merely declared a forbidden tool without calling it slipped past a deny rule, and a decision cache keyed without the attestation method let an unattested agent inherit a recently attested allow inside the cache window. Only the 34-agent concurrent burst surfaced the second one. Both were fixed, covered by regression tests, and re-verified live before any number here was taken as final.

**And what we withdrew.** After the first cluster we wrote down that throughput collapses past 64 concurrent callers and that a fleet should be designed to that line. It does not. On both dedicated-core clouds there is no cliff at all out to 256 concurrent, on two chip generations; only latency rises, the way a queue should. The collapse was a property of a shared-vCPU instance whose hypervisor gives the tick to a neighbour under load, not of anything we built. The retraction is in the repositories next to the claim it replaces.

The full ledger, every number and every bug, is public in each repository's `VALIDATION.md`. A validation write-up with no bug list is marketing.

You do not have to take our word for it: [run the stack's live services locally](https://it-rat.com/services/platform.html#run) in one command and watch the money plane light up. The four that are not servers, Engram, Qryx, Verdryx and Mockryx, each carry a one-line try-it on their own page.

## Governance you cannot read is governance you have to trust.

Every part of this stack is Apache-2.0, the console included, and that is not a marketing posture. These services decide what an AI agent may do: what it may spend, which tools it may call, whose authority it acts under, and what evidence exists afterwards. A control whose entire job is to remove the need for trust cannot itself be a thing you take on trust.

**Q: The longer answer**

Closed governance software asks you to believe a claim precisely where you came to stop believing claims. So the source is readable, the validation records name their own bugs, and a conclusion we got wrong is corrected in public next to the one it replaces. Everything on this site runs, which is a different claim from everything on this site is described.

And we are downstream of a great deal of work nobody billed us for. This stack stands on k3s, Calico, Longhorn, Postgres, SQLite and three language ecosystems, none of which sent an invoice. Publishing ours under Apache-2.0 is not charity and not a growth tactic; it is the ordinary way to be a participant in that rather than only a consumer of it.

Take it, run it, fork it, and never speak to us. That is the point of publishing it.

## Two of us, plus the agents.

This stack is written by two people who spend their working lives in exactly the two rooms it lives in: cloud security and cloud money.

### Yurii Kostiuk

IAM solutions architect and cloud security consultant: Zero Trust, identity, DevSecOps and platform resilience across AWS and GCP. The stack's view that an agent deserves a badge, a budget and a boundary comes straight from this desk.

### Tania Fedirko

Cloud financial governance, cost optimization and multi-cloud strategy. Tania aligns engineering, finance and business, and applies FinOps practice to LLM APIs and token-based usage: the reason this stack meters money before it meters anything else.

## The questions that come before the demo

**Q: What is AI agent governance?**
Governance is the set of controls that decide what an agent is allowed to do while it is running: a budget it cannot exceed, a policy it must ask before acting, an identity that records who it acts for, a memory that can say where a belief came from, and evidence an auditor can verify afterwards. Observability tells you what an agent did. Governance decides what it can do next. The two are not substitutes, and only one of them stops a runaway at 3am.

**Q: Is the stack open source?**
Yes, all of it. Apache-2.0, source on [GitHub](https://github.com/TAIPANBOX): TokenFuse, Wardryx, Idryx, Engram, Qryx, Verdryx and Mockryx, the shared [contract](https://it-rat.com/services/platform.html) under them, and [Genaryx](https://it-rat.com/genaryx.html), the console over all of them.

**Q: Do you host any of this, or see our data?**
No. Every plane runs on infrastructure you own: AWS, GCP, Hetzner, any cloud or on-prem. We never run your control plane, hold your keys or store your traffic, so there is nothing on our side to subpoena or breach.

**Q: What does it cost to try?**
Nothing, and no account. Every part of it is Apache-2.0, the console included. One command builds and starts the long-running services locally: see [run the live stack locally](https://it-rat.com/services/platform.html#run). The four that are libraries and CLIs each carry a one-line try-it on their own page.

<!-- https://it-rat.com/stack-guide.html -->

# How the numbers were produced

> The eight figures on the home page: how each was measured on real infrastructure, the bugs the live runs caught, and where the rest of the record is.

The [home page](https://it-rat.com/index.html#proof) shows eight figures from the validation campaign. This guide says how each one was measured, what the live runs caught along the way, and where the rest of the record is kept.

- [The eight figures](https://it-rat.com/stack-guide.html#proof)

- [What the campaign ran](https://it-rat.com/stack-guide.html#campaign)

- [What it caught](https://it-rat.com/stack-guide.html#caught)

- [Where the rest is recorded](https://it-rat.com/stack-guide.html#elsewhere)

- [How it wires](https://it-rat.com/stack-guide.html#wiring)

- [Why all of it is open](https://it-rat.com/stack-guide.html#open)

- [Run it yourself](https://it-rat.com/stack-guide.html#run)

## Validated on real infrastructure. Then torn down.

Before this site existed, the stack ran on disposable boxes across Hetzner, AWS and GCP with a real Anthropic key: four physical machines holding one budget over a real network, a partition with no split-brain, and a kill switch cutting real spend. Then the same stack came up again as a five-node Kubernetes cluster on each of those three clouds, which is where the cost of the governance itself finally got measured.

- **8000/8000** · **Money, under load.** Requests admitted against one budget by 100 to 500 concurrent agents, on a stub provider. None dropped, and none over the budget.

- **$0.00042** · **Money, per unit of work.** The measured cost of one correctly resolved case, which is the number that changes a decision. Monthly spend is not.

- **2,449/s** · **Policy, throughput.** Decisions a single pod makes each second, with no cliff out to 256 concurrent callers on dedicated cores.

- **34** · **Policy, under concurrency.** Requests fired at once and sorted exactly right: 6/6 served, 6/6 oversteppers denied, differentiated rights holding.

- **426 B** · **Evidence, per decision.** Hash-linked audit written for every decision rather than a sample. This is the line item that grows on its own.

- **12/12** · **Portability.** Deliberate budget overruns blocked, identically on Hetzner, AWS and GCP. What differs between clouds is the price, not the behaviour.

- **25,586** · **Crypto inventory.** Real Linux binaries scanned by Qryx, stripped, static and truncated among them, with zero crashes.

- **0** · **Rehearsal.** Guardrail gaps across three hostile drills fired twice at a real gateway, with zero real spend behind it.

## What the campaign ran, and what it caught.

Every number above came from a run against real infrastructure, not a benchmark harness written to flatter us. The boxes were disposable, the model calls behind the cost and policy figures were real and paid for, and nothing from the campaign is still standing: the machines were deleted, the key revoked.

**Money.** Four nodes across two datacenters held one budget through a leader kill and a real network partition: the majority kept serving, the isolated node could not overspend, and the state stayed byte-identical on every node. Under 500 concurrent agents against a fixed budget, the ledger admitted exactly what the budget allowed and no more.

**Policy.** An enriched multi-agent campaign produced 176 real enforcement decisions with differentiated rights: an analyst agent refused a wire transfer that a treasury agent was allowed, an unattested agent refused until it attested, and shell execution refused for everyone regardless of identity. Fired as a 34-request concurrent burst, the decision point still sorted them exactly right.

**The rest.** Qryx scanned 25,586 real Linux binaries, stripped, static and truncated among them, without a crash. Engram's reflection ran against real Claude output three times on three topologies with zero contradictions. Verdryx priced a correctly resolved case at $0.00042. Mockryx fired three hostile drills against a real gateway twice, with zero gaps and zero real spend, because the provider behind that gateway was fake while every guardrail in front of it was live.

**At cluster scale.** The same manifests then came up as a five-node cluster on each of the three clouds, to answer the question the campaign above could not: what does the supervision itself cost. Several clusters went up in all: a quota ceiling capped the first GCP attempt at three nodes, and AWS was rebuilt twice, the last time a chip generation lower, once it turned out the first result had compared silicon rather than clouds. One policy pod peaks at about 2,449 decisions a second and answers in 3.2ms at p50 while the queue is short. On identical silicon the two hyperscalers land 1.2% apart, which makes choosing between them procurement rather than engineering. At full load the infrastructure under the control plane works out at EUR 0.024 per million governed decisions on Hetzner and about USD 0.21 to USD 0.23 on AWS and GCP. That is what the machines cost to run. What binds first is not the processor but the evidence: every decision is audited, not a sample of them, at 426 bytes each, which is 614 MB a day at a thousand calls a minute. Provability is measured in gigabytes and can be budgeted a year ahead from a single number.

The full ledger, every number and every bug, is public in each repository's `VALIDATION.md`. A validation write-up with no bug list is marketing.

## Live testing found real bugs.

**And what it caught.** Live testing found real bugs, which is the point of doing it. Two of them, both in the policy plane, were invisible to sequential test traffic: a request that merely declared a forbidden tool without calling it slipped past a deny rule, and a decision cache keyed without the attestation method let an unattested agent inherit a recently attested allow inside the cache window. Only the 34-agent concurrent burst surfaced the second one. Both were fixed, covered by regression tests, and re-verified live before any number here was taken as final.

## Where the rest of the record is.

- **On premises.** The 2026-09-17 run on a small box behind a home router, governing agents in AWS and GCP and then taking sixteen injected failures, is in [what is proven](https://it-rat.com/what-is-proven.html), under "Seven claims and what each one stops short of" and "Sixteen ways to break it, and what each one did".

- **What we withdrew.** The throughput cliff past 64 concurrent callers that turned out to be a shared-vCPU instance is in [what is proven](https://it-rat.com/what-is-proven.html), under "Three things we published and had to withdraw", and in [what runs where](https://it-rat.com/what-runs-where.html).

## One passport, one event bus, four planes of control.

Every request carries an Agent Passport. An agent has two ways out, not one: a call to a model, and a fetch of something on the internet, and each has a gate standing in it. Below, memory, identity, crypto, quality, rehearsal, alerting, the record and the key witness read the same NDJSON stream off-path, and one of them feeds back in: Wardryx reads Verdryx's slo_burn events and can hold an agent whose error budget is spent. Nothing here is a dashboard after the fact: the gates enforce in-line, in seconds.

## Governance you cannot read is governance you have to trust.

Every part of this stack is Apache-2.0, the console included, and that is not a marketing posture. These services decide what an AI agent may do: what it may spend, which tools it may call, whose authority it acts under, and what evidence exists afterwards. A control whose entire job is to remove the need for trust cannot itself be a thing you take on trust.

Closed governance software asks you to believe a claim precisely where you came to stop believing claims. So the source is readable, the validation records name their own bugs, and a conclusion we got wrong is corrected in public next to the one it replaces. Everything on this site runs, which is a different claim from everything on this site is described.

And we are downstream of a great deal of work nobody billed us for. This stack stands on k3s, Calico, Longhorn, Postgres, SQLite and three language ecosystems, none of which sent an invoice. Publishing ours under Apache-2.0 is not charity and not a growth tactic; it is the ordinary way to be a participant in that rather than only a consumer of it.

Take it, run it, fork it, and never speak to us. That is the point of publishing it.

## You do not have to take our word for it.

You do not have to take our word for it: [install the stack](https://it-rat.com/install.html) in one command, on a box you own or on your laptop, and watch the money plane light up. The four that are not servers, Engram, Qryx, Verdryx and Mockryx, each carry a one-line try-it on their own page.

## Back to the home page.

The [home page](https://it-rat.com/index.html) has the eight figures and the people behind them, [the Stack page](https://it-rat.com/stack.html) has every service with its room and its guide, and [the guides index](https://it-rat.com/guides.html) has the field itself.

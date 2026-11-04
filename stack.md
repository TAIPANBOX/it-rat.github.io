<!-- https://it-rat.com/stack.html -->

# The stack: every service, with its room and its guide

> Every service in the stack, grouped by the ring it belongs to, each with a room that shows it working and a guide with the full story.

Each service has a room, with its drawing, its replay and its numbers, and a guide with the full story. Every one is Apache-2.0 and installs on its own.

### The control room

One room over all of it, in your browser, on your own box.

- **Genaryx** control room The control room over all of it, in your browser on your own box. [Room →](https://it-rat.com/genaryx.html)[Guide →](https://it-rat.com/genaryx-guide.html)

### Money

What it may spend, and the switch that stops it.

- **TokenFuse** money Runtime spend control and the in-line kill switch. [Room →](https://it-rat.com/services/tokenfuse.html)[Guide →](https://it-rat.com/tokenfuse-guide.html)

- **CostCrew** finops A crew of agents takes your cloud bill apart, a person stamps every deliverable. [Room →](https://it-rat.com/services/costcrew.html)[Guide →](https://it-rat.com/costcrew-guide.html)

- **TokenFuse Pocket** out of band not wired in yet The kill switch on a device the agent's host never touches. [Room →](https://it-rat.com/services/pocket.html)[Guide →](https://it-rat.com/pocket-guide.html)

### Guardrails

Who it is, what it may do, who signs the big things.

- **Wardryx** policy Policy decisions with a human in the loop. [Room →](https://it-rat.com/services/wardryx.html)[Guide →](https://it-rat.com/wardryx-guide.html)

- **Idryx** access One identity graph for humans, keys and agents. [Room →](https://it-rat.com/services/idryx.html)[Guide →](https://it-rat.com/idryx-guide.html)

- **Scopyx** egress Agents reach the web through a decision, not around one. [Room →](https://it-rat.com/services/scopyx.html)[Guide →](https://it-rat.com/scopyx-guide.html)

- **Vouchryx** delegation A delegation an agent can prove it holds, and a person can end. [Room →](https://it-rat.com/services/vouchryx.html)[Guide →](https://it-rat.com/vouchryx-guide.html)

### Proof

What it did, written so nobody can quietly change it.

- **Qryx** crypto Cryptography inventory and post-quantum risk. [Room →](https://it-rat.com/services/qryx.html)[Guide →](https://it-rat.com/qryx-guide.html)

- **Keyryx** key custody Signing keys held apart from the code that uses them, and a read-only witness of the record. [Room →](https://it-rat.com/services/keyryx.html)[Guide →](https://it-rat.com/keyryx-guide.html)

- **Verdryx** quality Cost per correctly resolved case, not per token. [Room →](https://it-rat.com/services/verdryx.html)[Guide →](https://it-rat.com/verdryx-guide.html)

- **Typryx** typed answers optional add-on A typed answer with a probability, never a guess. [Room →](https://it-rat.com/services/typryx.html)[Guide →](https://it-rat.com/typryx-guide.html)

- **Mockryx** pre-prod Fire drills that prove guardrails hold. [Room →](https://it-rat.com/services/mockryx.html)[Guide →](https://it-rat.com/mockryx-guide.html)

- **Trailryx** the record A record nobody can quietly change or shorten. [Room →](https://it-rat.com/services/trailryx.html)[Guide →](https://it-rat.com/trailryx-guide.html)

### Ground

Memory, alerts and one contract under all of it.

- **Heraldyx** alerts The box writes to you, with a link and never a button. [Room →](https://it-rat.com/services/heraldyx.html)[Guide →](https://it-rat.com/heraldyx-guide.html)

- **Engram** memory The SQLite of agent memory. [Room →](https://it-rat.com/services/engram.html)[Guide →](https://it-rat.com/engram-guide.html)

- **Platform** contract Agent Passport, shared contract, Terraform. [Room →](https://it-rat.com/services/platform.html)[Guide →](https://it-rat.com/platform-guide.html)

## One passport, one event bus, four planes of control.

Every request carries an Agent Passport. An agent has two ways out, not one: a call to a model, and a fetch of something on the internet, and each has a gate standing in it. Below, memory, identity, crypto, quality, rehearsal, alerting, the record and the key witness read the same NDJSON stream off-path, and one of them feeds back in: Wardryx reads Verdryx's slo_burn events and can hold an agent whose error budget is spent. Nothing here is a dashboard after the fact: the gates enforce in-line, in seconds.

New to this? [The guides](https://it-rat.com/guides.html) are grouped by what you came for: [where to start](https://it-rat.com/first-alert.html), [how the stack is secured](https://it-rat.com/security-by-design.html), the practice of running agents, from [governance](https://it-rat.com/ai-agent-governance.html) to [FinOps for AI](https://it-rat.com/finops-for-ai.html), each service in depth, and [what changed in October](https://it-rat.com/changes-2026-10.html). Every room above links its own guide, and [the stack in depth](https://it-rat.com/stack-guide.html) holds the rest of this page.

## Governance you cannot read is governance you have to trust.

Every part of this stack is Apache-2.0, the console included, and that is not a marketing posture. These services decide what an AI agent may do: what it may spend, which tools it may call, whose authority it acts under, and what evidence exists afterwards. A control whose entire job is to remove the need for trust cannot itself be a thing you take on trust.

## The questions that come before the demo

**Q: What is AI agent governance?**
Governance is the set of controls that decide what an agent is allowed to do while it is running: a budget it cannot exceed, a policy it must ask before acting, an identity that records who it acts for, a memory that can say where a belief came from, and evidence an auditor can verify afterwards.

**Q: Is the stack open source?**
Yes, all of it. Apache-2.0, source on [GitHub](https://github.com/TAIPANBOX): TokenFuse, CostCrew, TokenFuse Pocket, Wardryx, Idryx, Scopyx, Vouchryx, Qryx, Verdryx, Typryx, Mockryx, Trailryx, Heraldyx and Engram, the shared [contract](https://it-rat.com/services/platform.html) under them, and [Genaryx](https://it-rat.com/genaryx.html), the console over all of them.

**Q: Do you host any of this, or see our data?**
No. Every plane runs on infrastructure you own: AWS, GCP, Hetzner, any cloud or on-prem, and on-prem is measured rather than merely allowed: on 2026-09-17 the whole stack ran on a small box behind a home router, governing agents in AWS and GCP at the same time. We never run your control plane, hold your keys or store your traffic, so there is nothing on our side to subpoena or breach.

**Q: What does it cost to try?**
Nothing, and no account. Every part of it is Apache-2.0, the console included. One command builds and starts the long-running services locally: see [run the live stack locally](https://it-rat.com/services/platform.html#run). The four that are libraries and CLIs each carry a one-line try-it on their own page.

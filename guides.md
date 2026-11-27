<!-- https://it-rat.com/guides.html -->

# Guides index

> Sixteen guides: seven on the field of AI agent governance, and nine on running this stack, from a first alert to what changed in October.

Sixteen guides, grouped by what you came for: how to install it, where to start, how the stack is secured, the practice of running agents, and what changed in October. Each service has its own guide too, listed beside its room on [the Stack page](https://it-rat.com/stack.html).

## Install

*all of it*

### [The whole stack, in one command](https://it-rat.com/install.html#all)

On a Debian or Ubuntu box you own, on a Kubernetes cluster, or as a sandbox on your laptop. It comes up closed, checks itself, and adds the rest when you ask.

*one piece*

### [One service at a time](https://it-rat.com/install.html#one)

Every service is its own repository with its own releases. How each one ships, whether it runs alone, and where its install command lives.

## Start here

*start here*

### [From zero to your first alert](https://it-rat.com/first-alert.html)

One command on a box you own, one agent pointed at it, one address to write to, and then make it fire on purpose. Four steps, what each is for, and where each one goes wrong.

*the honest half*

### [What is proven here, and how it was measured](https://it-rat.com/what-is-proven.html)

What a measurement on this stack actually established, on what and with what result, sixteen injected failures and what each did, and three conclusions we withdrew.

*the operational half*

### [What runs where, and what it costs](https://it-rat.com/what-runs-where.html)

One machine, a five-node cluster, or a hyperscaler. Six clusters measured across three clouds and then destroyed: how each performed, the storage line that differs by a factor of 108, and a published conclusion we had to withdraw.

*the numbers, in full*

### [How the numbers were produced](https://it-rat.com/stack-guide.html)

The eight figures on the home page: how each was measured on real infrastructure, the bugs the live runs caught, and where the rest of the record is.

## Security

*the decisions*

### [Security by design: eight decisions, each proven by breaking it](https://it-rat.com/security-by-design.html)

Why every control sits where an agent cannot talk to it.

*the defensive half*

### [AI agent security: an old discipline with a new blast radius](https://it-rat.com/ai-agent-security.html)

The damage does not arrive as a sentence, it arrives as a tool call. Eight failure modes a fleet actually hits, the control that answers each, and what to rehearse in CI so a broken guardrail fails a build rather than an incident review.

*the newest surface*

### [MCP security: your tools are now a fetch, not a build](https://it-rat.com/mcp-security.html)

A tool used to be code you shipped. Over the Model Context Protocol it is a description you fetched, from a server that can change it after you approved it. Six failure modes, and the control that answers each.

*the join key*

### [Agent identity and authentication: how an agent proves who it is](https://it-rat.com/agent-identity.html)

A static key answers one question, badly. What an identity has to be instead, nameable, attributable, attestable and revocable, plus delegation chains, when to demand a signature per action, and how to evaluate anything in this space.

## The practice

*the umbrella*

### [AI agent governance, and what it means at runtime](https://it-rat.com/ai-agent-governance.html)

Governance is the set of controls that decide what an agent may do while it is doing it. Every question a fleet has to answer at runtime with the tool that owns it, the five decisions every governed team ends up making, and the order to adopt them in.

*the money*

### [FinOps for AI: managing spend that creates itself](https://it-rat.com/finops-for-ai.html)

Cloud FinOps assumes somebody provisioned the thing. Agent spend appears when an agent decides to try again. What breaks, what to instrument first, and how to report it in a format finance already reads.

*the record and the control*

### [The record and the control are different jobs](https://it-rat.com/ai-observability-vs-governance.html)

One explains what happened, the other decides what may happen. The same incident seen by each, why the control alone is opaque, and the single integration decision that makes them meet: one run id.

*the controls*

### [What the stack refuses before a call, and how to check it](https://it-rat.com/agent-tooling-compared.html)

Twelve controls that answer before a call: what each one does, what it does not do yet, and how to check it, one at a time.

*the second site*

### [Two sites, one control plane, no VPN](https://it-rat.com/two-sites.html)

A hub that holds the control plane and the policy, and a gateway at every site that reaches it over outbound HTTPS through one narrow door. One script on the hub, one command per site, four variables at the site, and what the runs showed.

*the walk-through*

### [One incident, end to end: a runaway agent through every plane](https://it-rat.com/one-incident-end-to-end.html)

One ordinary failure, an agent stuck in a retry loop, followed from its first over-budget call to the evidence an auditor reads months later. Eight steps, the event each one writes, and what only becomes visible in that order.

## What changed

*what changed*

### [What changed in the stack, 1 to 15 October 2026](https://it-rat.com/changes-2026-10.html)

What changed across the stack between 1 and 15 October 2026, in one place.

## Every control in the guides has an open implementation.

Every control the guides describe has an Apache-2.0 service behind it, and they run on infrastructure you own. [Walk the stack](https://it-rat.com/stack.html), or [start the live services locally in one command](https://it-rat.com/services/platform.html#run) and watch the money plane light up. Unfamiliar term? The [glossary](https://it-rat.com/glossary.html) defines the vocabulary these guides use.

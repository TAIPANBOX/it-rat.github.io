<!-- https://it-rat.com/guides.html -->

# Guides index

> Twelve guides: seven on the field of AI agent governance, and five on running this stack, from a first alert to what the numbers prove.

Twelve guides. Seven are about the practice rather than about our tools: what it means to govern an agent while it is running, how to manage spend that nobody provisions, how to secure a fleet that holds credentials and calls tools, where observability stops being enough, what changes when tools arrive over a protocol, and what the tools on this market can and cannot actually do. Each one names the open-source tool that does the job, and none of them needs you to buy anything to be useful. The other five are about this stack specifically: getting a first alert, connecting a second site without a VPN, following one incident through every plane, what the shapes cost, and what the numbers do and do not establish.

*start here*

## From zero to your first alert

One command on a box you own, one agent pointed at it, one address to write to, and then make it fire on purpose. Four steps, what each is for, and where each one goes wrong.

*the umbrella*

## AI agent governance, and what it means at runtime

Governance is the set of controls that decide what an agent may do while it is doing it. Every question a fleet has to answer at runtime with the tool that owns it, the five decisions every governed team ends up making, and the order to adopt them in.

*the money*

## FinOps for AI: managing spend that creates itself

Cloud FinOps assumes somebody provisioned the thing. Agent spend appears when an agent decides to try again. What breaks, what to instrument first, and how to report it in a format finance already reads.

*the defensive half*

## AI agent security: an old discipline with a new blast radius

The damage does not arrive as a sentence, it arrives as a tool call. Eight failure modes a fleet actually hits, the control that answers each, and what to rehearse in CI so a broken guardrail fails a build rather than an incident review.

*the record and the control*

## The record and the control are different jobs

One explains what happened, the other decides what may happen. The same incident seen by each, why the control alone is opaque, and the single integration decision that makes them meet: one run id.

*the controls*

## What the stack refuses before a call, and how to check it

Twelve controls that answer before a call: what each one does, what it does not do yet, and how to check it, one at a time.

*the operational half*

## What runs where, and what it costs

One machine, a five-node cluster, or a hyperscaler. Six clusters measured across three clouds and then destroyed: how each performed, the storage line that differs by a factor of 108, and a published conclusion we had to withdraw.

*the second site*

## Two sites, one control plane, no VPN

A hub that holds the control plane and the policy, and a gateway at every site that reaches it over outbound HTTPS through one narrow door. One script on the hub, one command per site, four variables at the site, and what the runs showed.

*the honest half*

## What is proven here, and what is not

What a measurement on this stack actually established, the limit published beside each one, three conclusions we withdrew, and the list of what nobody has established yet.

*the walk-through*

## One incident, end to end: a runaway agent through every plane

One ordinary failure, an agent stuck in a retry loop, followed from its first over-budget call to the evidence an auditor reads months later. Eight steps, the event each one writes, and what only becomes visible in that order.

*the newest surface*

## MCP security: your tools are now a fetch, not a build

A tool used to be code you shipped. Over the Model Context Protocol it is a description you fetched, from a server that can change it after you approved it. Six failure modes, and the control that answers each.

*the join key*

## Agent identity and authentication: how an agent proves who it is

A static key answers one question, badly. What an identity has to be instead, nameable, attributable, attestable and revocable, plus delegation chains, when to demand a signature per action, and how to evaluate anything in this space.

## Every control in the guides has an open implementation.

Every control the guides describe has an Apache-2.0 service behind it, and they run on infrastructure you own. [Walk the stack](https://it-rat.com/index.html#stack), or [start the live services locally in one command](https://it-rat.com/services/platform.html#run) and watch the money plane light up. Unfamiliar term? The [glossary](https://it-rat.com/glossary.html) defines the vocabulary these guides use.

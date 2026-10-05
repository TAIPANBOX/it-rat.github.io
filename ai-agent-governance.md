<!-- https://it-rat.com/ai-agent-governance.html -->

# AI agent governance

> What AI agent governance means in practice: budgets, policy, identity, delegation, egress, provenance, quality, drills and an auditable record.

An AI agent does not answer a question and stop. It calls tools, spends money, touches data and hands work to other agents, on its own schedule and at machine speed. Governance is the set of controls that decide what it is allowed to do while it is doing it: a budget it cannot exceed, a policy it must ask, an identity that records who it acts for and a delegation it can prove when it acts for somebody else, a decision before it reaches anything outside your walls, a memory that can say where a belief came from, and evidence somebody else can check afterwards.

## Observability is a witness. Governance is a brake.

Most AI tooling sold today is observability: traces, dashboards, token counters, evaluation reports. It is genuinely useful and it is not governance. A trace tells you, after the fact, that an agent looped four hundred times against a production API. A budget tells the agent, on call five, that it may not.

The distinction is not academic. Every failure mode teams actually hit with agent fleets is a failure of control, not of visibility: a retry loop that ran overnight, an agent that called a tool nobody meant to expose, a sub-agent inheriting permissions through a delegation chain nobody had drawn, a model quietly getting worse while the dashboard stayed green. In each case the data was there. Nothing was standing in the path.

**Runtime governance means the control sits in the request path, and its answer is binding.** Anything else is reporting.

## The questions a fleet has to answer, each with an owner.

Governance sounds abstract until it is broken into questions. Each one below is a separate control with an open-source tool behind it, and they are in the order a request meets them: what it may spend, what it may do, who it is, whose authority it borrowed, where it may reach, and then the planes that watch, warn and remember. The last is the one people leave out, and it is the earliest: what the agent was hired to do at all.

*money*

### What may this run spend?

Budgets that nest from company down to the single run, priced before each call and enforced in the path, so a loop is refused rather than reported.

*policy*

### May it do this at all?

Allow, deny, or hold for a human, decided per action against policy as code, with signed approval tokens for the actions that need a person.

*identity*

### Who is it acting for?

One graph of humans, service accounts, keys and agents, with delegation chains and the true blast radius of each identity, not the list of grants on its own name.

*delegation*

### Whose authority is it borrowing?

A short-lived token an agent can prove it holds and cannot lend, carrying the chain of who asked for what on whose behalf. Revoking it ends the right to act for somebody everywhere at once, whatever the token still says about its own expiry.

*egress*

### Where may it reach, and what may come back?

Every question above governs what an agent does to your own services. None watches the direction that leads outside, where a page it reads can tell it what to do next and an address it found in a prompt can receive your data. A decision before the request, another on every redirect, and a bound on the reply.

*memory*

### Why does it believe that?

Memory with provenance and two timelines, so you can ask what the agent knew in March and get March's answer, and correct a fact without erasing the reason it once held.

*quality*

### Is it still any good?

Cost per correctly resolved case rather than cost per token, with statistical drift detection that catches the small consistent regression a threshold misses.

*crypto*

### What is it holding, and for how long?

An inventory of the keys, certificates and algorithms actually running, graded against the post-quantum migration dates rather than against an architecture document.

*rehearsal*

### Do the guardrails hold?

Fire drills against a real gateway, so a broken defence fails a build rather than an incident review. A guardrail nobody tests is a guardrail nobody has.

*alerting*

### Who finds out, and when?

A control that refuses at 3am and tells nobody has stopped the spend and not the incident. One mail, from your own box, carrying a link into your own console and no button that acts: mail gateways prefetch links, so a one-click kill fires before anybody reads the sentence beside it.

*the record*

### How is any of this proven a year later?

Tamper-evident is the easy half. The hard half is the answer: ask what an agent did in March and an ordinary store hands you rows with no way to know it handed you all of them. A record that carries a completeness proof, and names the reason when it can only be partial.

*the hire*

### What was it hired to do in the first place?

The questions above meet an agent already running. This one comes before its first call: an agent is hired into a named desk with a mission, an owner, a per-task and a monthly guard, and exactly the rights its skills need and no others. Suspending it withdraws them, and the withdrawal binds, because neither queue accepts new work for a suspended mandate and the runner refuses to price anything it holds.

*the contract*

### How do they agree?

One agent identifier, one event envelope and one Go binding under all of it, so independent tools can describe the same agent without a shared runtime or database.

## Five decisions every governed fleet ends up making.

### 1. Shadow mode before enforcement

Put the control in the path first with its answer recorded and never binding. You learn what would have been blocked, on real traffic, before anything is. A policy set that has never seen production traffic is a hypothesis, and the first day it enforces is the wrong day to discover that.

### 2. Fail-open or fail-closed, chosen on purpose

Decide now what happens when the control plane is unreachable. **Fail-open** treats it as allow: availability wins, and an outage silently disables governance. **Fail-closed** treats it as deny: governance wins, and an outage stops every governed action. There is no clever third answer. The failure is only embarrassing when nobody chose and everybody assumed.

### 3. The run is the unit, not the key

Per-key rate limits cannot tell one agent's honest afternoon from the same key looping on itself. The unit that means something for an agent fleet is the run: one task, one budget, one identity, one trace, rolled up to the agent, the team and the company. Every control in this stack keys on it, which is what makes an incident, a spend and a policy decision line up on the same id.

### 4. A human in the loop, without a parked connection

Approval that holds an open connection while somebody sleeps is not a control, it is an outage waiting for a timeout. The workable shape is stateless: the agent is told to hold, a person decides out of band, and the eventual grant is proven by a signed token bound to that exact agent, run and tool set, and, where the request named the tool call, to that call's arguments, not by anyone remembering an open request.

### 5. Evidence produced as a by-product

Governance that has to be reconstructed for an audit will be reconstructed badly. If every decision, kill and approval is journaled as it happens, each record carrying the hash of the one before it, then the audit is an export rather than an archaeology project, and it stays verifiable by someone who does not trust you.

## The order that works.

Nobody governs every plane on the first day. This is the order we deploy in, and the reasoning behind it.

All of it is Apache-2.0 and runs on infrastructure you own. [One command starts the live services locally](https://it-rat.com/services/platform.html#run) if you want to see the shape before you commit to any of it, and the whole corridor is [on the stack page](https://it-rat.com/index.html#stack). The defensive half of the same job is in [AI agent security](https://it-rat.com/ai-agent-security.html).

- **Does it act in the request path, or after it?** Everything else is a detail if the answer arrives once the call has already been made.

- **Is the answer binding?** A warning an agent can proceed past is telemetry with a stern voice. Ask what physically stops the action.

- **What happens when it is unreachable?** Fail-open and fail-closed are both defensible; not having decided is not. The answer should be documented, not discovered during an outage.

- **Can it be run in shadow first?** If you cannot see what it would have blocked before it blocks anything, the first day of enforcement is also the first day of surprises.

- **Does it join on the same identifier as your traces and your bill?** If it invents its own id, the correlation project comes free with the purchase, and it is not free.

- **Can somebody who does not trust you verify the record?** An export from a dashboard is a claim. A journal whose entries each carry the hash of the one before it is evidence.

## What people ask about agent governance

**Q: What is AI agent governance?**
The controls that decide what an AI agent may do while it is running, rather than the reports that describe what it did. In practice: a budget it cannot exceed, a policy it must ask before acting, an identity that records who it acts for and a provable delegation when it acts for somebody else, a decision before it reaches anything outside, memory with provenance, quality measured in outcomes, drills that prove the guardrails still hold, and a record of all of it somebody who does not trust you can check.

**Q: How is agent governance different from LLM observability?**
Observability is a witness; governance is a brake. A trace tells you afterwards that an agent looped four hundred times against a production API. A budget tells the agent on call five that it may not. Both are useful, but only one of them is standing in the path when it matters.

**Q: Do I have to adopt all of it at once?**
No, and nobody does. The order that works is metering first, then a ceiling, then a decision in front of the web, then naming the actions that need a human, then drawing the identities and making borrowed authority provable, then rehearsing the guardrails in CI, then sealing the record, and only then measuring quality in money. Each step is a separate Apache-2.0 tool and each is useful alone.

**Q: Does putting controls in the request path slow agents down?**
The enforcement decision itself is in-process and measured in microseconds, and the gateway's own bookkeeping fails open, so a lost event never stops a call. What happens when the policy plane is unreachable is a decision the deployment makes on purpose: both launchers ship it fail-closed, and a run on 2026-09-17 measured exactly that, every call refused in 0.3 s until the plane was back. The latency people notice in agent systems comes from models and tools, not from a budget check.

**Q: Can this run on our own infrastructure?**
It is the only way it runs. Every plane is self-hosted on infrastructure you own, any cloud or on-prem, and nothing is sent to us: we never hold your keys, your traffic or your data.

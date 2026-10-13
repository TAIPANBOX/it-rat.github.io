<!-- https://it-rat.com/agent-tooling-compared.html -->

# Three shapes of agent tooling

> The controls that answer before a call: what each one does, what it does not do yet, and how to check it.

Watching an agent is useful after the fact. A budget, a policy and an egress check have to answer before the action, because by the time the invoice or the incident review arrives, the money is spent. The stack puts those answers in the path of the call. Each one is a decision that either happened or did not, and the rest of this page says what each one does and how to check it.

## Watch it happen.

The same call, sent twice: once with the control plane in the path and once without it. Pick what the agent is trying to do and see where each one ends up.

**The copy is never the control.** Every event also goes sideways into the dashboard, and it arrives after the thing already happened. What decides the call is whether something stood on the wire itself with the authority to stop it.

## Where the stack answers.

Each place answers a different question, and each one leaves a record you can check.

***A**the budget*

### A ceiling on every run

A gateway sits in front of the model calls. It gives every run a budget, prices each call against it before the call goes out, and answers 402 on the one that would cross the line, without forwarding it. Spend is reserved before the call and settled after it. The rest of the spend story, including the cache, the model router and the FOCUS export, is on the TokenFuse room.

**Answers:** may this call spend more money right now?

**Limit:** a budget governs spend. It does not judge whether an answer was good; that is measured in Verdryx.

***B**the policy point*

### Allow, deny or hold, before the action

Wardryx is the decision an agent asks for before it acts. It answers allow, deny or hold. A hold waits for a person, who grants it with a signed approval token. The token is bound to the agent, the run, the tool set and, where the policy names them, the arguments of the call. Holds nobody has decided are swept and reported, not left parked.

**Answers:** may this action happen, and if not yet, who has to say yes?

**Limit:** it decides the actions that reach it. The gateway and the egress plane are the other places that stand in the path.

***C**identity and the record*

### Whose action it was, and proof nothing is missing

Idryx keeps one identity graph for humans, keys and agents, so a delegation chain ends at a person. Trailryx keeps the record. Every answer it gives comes with a completeness proof, a short receipt that the rows shown are all the rows that match the question, and the verifier that checks it has no dependencies.

**Answers:** whose action was this, and can an auditor check that nothing is missing?

**Limit:** an agent with no attestation on record is flagged as a finding, so a chain is only as strong as what it can prove.

*and the planes around them*

### Planes that stand in the path and answer before the action

A gateway that gives every run a budget and answers 402 the moment it is crossed. A policy plane the agent asks before acting, which can hold the expensive one for a person. An egress plane that decides the destination before anything leaves the machine. An identity graph that knows which human a key ultimately belongs to. A record built so that somebody who does not trust you can still check it is complete. Each one is a decision that either happened or did not.

**Not covered:** why the model wanted to do it. The governance events can export over OTLP into your tracing backend when an endpoint is set.

## Twelve controls, and how to check each one.

Every claim below says what makes it true and where to look, so it can be checked without trusting this page. The first six show up on a single request. The second six are the ones a regulated organisation asks about before it signs anything.

### It answers before the call, not after it

The gateway prices every call against the run's budget and, on the one that would cross it, replies 402 with a stable error and never forwards the request to the provider. The policy plane answers allow, deny or hold before the action, and never performs the action itself. Neither of those is a notification.

### The agent stays where it is, and does not have to be declared at all

Integration is one base URL. Nothing is rewritten, nothing is redeployed, no SDK enters the agent. Underneath, an eBPF sensor finds agents that nobody registered, along with the model providers they reach.

### The record answers to somebody who does not trust you

Every query comes back with a completeness proof: a short receipt, checkable on its own, that the rows shown are all the rows matching the question. The verifier that checks it carries zero dependencies, so an auditor can read the whole of it before believing any of it.

### The guardrails are themselves fired, in CI, before release

Adversarial scenarios run against a real gateway with a fake provider behind it. Burn the budget and require the 402. Ask for a forbidden tool and require the 403. Present a forged delegation chain and require it to be rejected. The exit codes differ on purpose, so the pipeline can tell a genuine hole in the defence from a broken test rig.

### Governance is not behind a licence key

Apache-2.0 throughout, the console included. Nothing in the governance layer sits behind a licence key, a seat count or a tier.

### An alert is a coordinate, and a session is not an authority

The mail that wakes somebody at night carries one link into a view, and never a button that acts. A link that acts is a permission held by everyone who received or forwarded the mail, and security gateways follow links before a human reads the sentence next to them. In the console, closing a retained reservation takes a fresh passkey assertion, bound to that one reservation and its revision, rather than to whoever is signed in.

### Post-quantum sits inside the agent loop, and it has legal dates attached

The scan grades each key, certificate and algorithm it finds for quantum risk and emits a CBOM in the CycloneDX format. The grades are scored against the published CNSA timeline: new systems by 2027, legacy migration by 2030, everything by 2035.

### A person can be erased without breaking the audit trail

Every payload is encrypted under its own key, so erasing a person means destroying their keys. The content becomes unrecoverable, every earlier proof still verifies, and the record itself carries the fact that an erasure happened. Nothing is re-encrypted afterwards, and records written later are reached by the same erasure.

### A refusal is a pure function, so an auditor can rerun it

No model anywhere in the decision path. Given the same policy set and the same request, the answer is always the same, which means a refusal from six months ago can be reproduced today in front of somebody who wants to see it. The policy primitives are deliberately dull: deny a tool, deny an unattested agent, cap the number of steps, restrict the destinations, require a human above a sum.

### The kill switch does not run through the thing it kills

The out-of-band control is a phone and a watch. The signing key is generated inside the device's secure element and never leaves it, not even to the app. A kill is signed on the device and the control plane verifies that signature before it acts, so the stop still works when the agent's own host is precisely what is misbehaving or compromised.

### Changing a limit goes through code review, like changing a firewall rule

Budgets, agent passports and policies are ordinary Terraform resources: in version control, reviewed in a pull request the way an IAM policy or a security group is, planned before they apply, and diffed when somebody has changed them outside the process.

### The money is counted per resolved case, not per token

Token spend says how much was burned. It does not say whether the burning bought anything. The quality plane joins the cost trace to your own outcome tags and returns the price of a resolved case beside the price of an escalated one and an abandoned one, which is the same arithmetic a finance function already applies to everything else it funds.

### And what it costs, since none of this is free

Standing in the request path buys the refusal and charges latency for it, on every call, including the overwhelming majority that were always going to be fine. It also forces a decision: what happens when the control plane itself is unreachable. The policy plane is fail-closed. In the failure drill of 2026-09-17 it refused every governed call in about 0.3 s while it was down. **That is the trade, and it is named here on purpose.**

## Where each part of the stack answers.

A budget per run, and a 402 the moment it is crossed. The call is refused before the provider sees it.

Allow, deny, or hold for a human, asked before the action, with a hard ceiling that outranks approvals.

Every destination decided before anything leaves, and every redirect hop decided again.

One identity graph for humans, keys, service accounts and agents, so "who did this" ends at a person.

A record nobody can quietly change or shorten, where every answer carries a proof that it is complete.

Quality as the denominator: cost per correctly resolved case, rather than per token.

Fire drills for the guardrails themselves, asserting the 402 and the 403 in CI.

Decides what is worth waking a human for tonight, and mails it with one link and no button.

All of it is Apache-2.0 and runs on infrastructure you own. The governance planes export over OTLP when an endpoint is set, into whatever tracing backend you already run. **Governance data can sit in your observability stack. The enforcement decision is made on the call.**

## What people ask when they have already bought one

**Q: Do we have to drop our tracing to use this?**
No, and we would advise against it. Tracing answers a question this stack does not: why the model wanted to do the thing. Keep it, put the gateway in front of the model calls in shadow mode for a week, then turn on caps where the outliers are.

**Q: Why describe products by shape instead of naming them?**
Because a named comparison is wrong the week after a vendor ships a feature, and a reader who already runs one of these can map the shape to their tool in a second. The shapes are also more useful: they say what a category of tool can and cannot do architecturally, which is the part that does not change with a release note.

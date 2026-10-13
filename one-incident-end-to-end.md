<!-- https://it-rat.com/one-incident-end-to-end.html -->

# One incident, end to end

> A single runaway agent followed through spend, policy, identity, memory, mail and evidence: what each plane sees, what it emits, and who is told.

Every plane in this stack is easy to describe on its own and hard to judge on its own. So here is one ordinary failure, a support agent that gets stuck in a loop, followed from its first expensive call to the evidence somebody hands an auditor months later. **Nothing below is a new capability.** It is the same planes as everywhere else on this site, in the order the incident actually reaches them, which is the only order that shows why they are separate.

## An agent, a budget, and a loop.

The agent handles tier-1 support. It carries an **Agent Passport**: an `agent://` identifier, an owner, a runtime, and an attestation method. This one's attestation is `none`, which is legal and honest. The field exists so the posture is visible rather than assumed, and an agent that cannot prove what it is will matter twice before this is over.

It also carries a **delegation chain**: an ordered list, root first, of who it is acting for. A human opened a ticket, an orchestrator spawned this agent, so the chain is two hops deep. Nothing may truncate that chain while forwarding a request, because the whole point of it is that the last entry is the immediate principal and the first is the person.

The failure is dull, which is why it is worth walking. A retry loop with no ceiling: the agent asks the model, dislikes the answer, and asks again with slightly more context each time. No prompt injection, no compromised key, nobody attacking anything. Just an agent doing its job in a way nobody bounded.

## Eight steps, and who owns each one.

Read the `emits` line under each step. The planes do not call each other: they append to one shared NDJSON event stream, and everything downstream reads it. That coupling is the reason a finding can join facts no single service holds.

### The gateway meters the call, then refuses one

Every call goes through the gateway because the agent's base URL points at it, which is the whole integration: one environment variable, no SDK. The gateway prices each call, keeps a running total against the run's budget, and forwards to the provider while there is room. On the call that would cross the budget it does not forward. It answers **HTTP 402** to the agent, in the request path, before the provider is asked and therefore before the money is spent.

That distinction is the product. A dashboard that notices an overspend has noticed something that already happened. Refusing in-line means the last expensive call is the one that did not happen.

### Policy was consulted on every call, and says why

Before the gateway forwards anything it asks the policy decision point, which answers **allow**, **deny** or **hold** and nothing else. It never performs the action; it returns a verdict, and the answer is a deterministic function of the loaded policies and the request, so the same question always gets the same answer and an auditor can re-derive it.

**Hold** is the interesting one. It means a human has to agree before this proceeds, and it parks nothing: no connection waits, no goroutine sleeps. The agent gets a refusal and an approval id, somebody grants it out of band, and the proof of that grant is a signed token the agent presents on the retry. If nobody answers at all, a sweep says so rather than letting the request rot in silence.

### Identity turns three weak signals into one finding

The identity plane never sees the request. It reads the same event stream afterwards, alongside the passport documents, and it holds something neither of the first two planes has: the graph. It knows this agent is unattested, that its delegation chain is two hops deep, and now that it has a spend incident against it.

Any one of those is a shrug. A spend incident alone is an agent having a bad afternoon. Together they are a finding, and the detector raises severity on the count: it needs at least two corroborating facts before it will call this **high**. That is the argument for a separate identity plane in one sentence. The correlation is only available to something that holds every identity in one graph.

### Memory can say why the agent believed what it believed

Meanwhile the agent has been writing what happened to it into its own memory: each attempt as a raw episode, and a structured fact extracted from them afterwards. Weeks later somebody asks the question that usually has no answer, which is not what did it do but why did it think that .

Here that is a call rather than an archaeology project: ask a fact where it came from and you get the episode that produced it, the run that extracted it, and the confidence. And because facts carry two independent timelines, when they were true and when the system learned them, you can also ask what the agent believed in March, which is the question a regulator asks and a vector database cannot answer.

### Something has to tell a person, and it is deliberately almost nothing

Everything so far has been written down and read by nobody. The notifier is the one component in the box allowed to reach the outside world, and its narrowness is the design rather than an implementation detail: it reads a file and sends mail. It holds no credential for any plane, opens no connection to one, has no API of its own, and can take no action on any agent.

It also decides what is worth a human's evening. Below a severity floor an event becomes a digest line rather than a message; a repeat of something already sent is dropped; past an hourly ceiling the rest are held and counted, and the notice that reports that says how many, because a suppression notice that understates a flood is worse than no notice at all.

The mail itself carries identifiers and numbers and never content, because the event payloads sit next to prompts and model output, and mail leaves through a server nobody here controls.

### The link is a coordinate, never a control

Following the link opens the panel showing that exact incident. It does not kill anything, and the difference is not fussiness. A link that acts is an unauthenticated capability held by whoever can see or forward the message, and mail security gateways **prefetch links**, so a one-click kill would fire before a human read the sentence next to it.

So the action happens in the console, behind a sign-in. Closing a retained reservation also takes a fresh passkey confirmation, bound to that one reservation and its revision, because a stolen session should not be able to close one. What the operator typed as a reason is journaled with it.

### The same failure, rehearsed before it was real

Steps 1 to 3 are only trustworthy if somebody has watched them fire. The rehearsal harness replays this shape at a pre-production gateway standing in front of a fake provider: burn the budget and require the 402, ask for a denied tool and require the refusal, present a forged delegation chain and require it to be rejected.

It exits with differentiated codes so a CI job can tell a genuine guardrail gap from a broken harness, which is the difference between a build that should fail and a pipeline that should be fixed. A drill nobody runs is a comment with a name on it.

### Months later, somebody asks you to prove it

The question that arrives late is rarely what happened . It is show me that this is all of it , and an ordinary log cannot answer it: anyone with access could have edited it, and nothing about the remaining lines shows whether one was removed.

So the events are sealed into a chain, the chain into a signed pack, and the pack is checked by a verifier with no third-party dependencies at all, small enough that an auditor can read the whole thing before trusting any of it. A query answer comes back with a completeness proof, which is the harder claim and the one an auditor actually needs: not here are five records but five is all there ever were .

One class of event never reaches your inbox at all, and it is worth knowing why. The shared envelope requires an agent identifier, so a signal about a whole organisation rather than one agent has no subject to travel under. Its producer skips it rather than inventing one, because a fabricated subject makes every downstream count wrong and puts a name in a subject line that did not do the thing. Those signals show up in the console instead.

## Four things that only appear in order.

### For this incident, two planes are in the path, and five are not

For this incident only money and policy stop the call, and they pay for that with latency on every request. Across the stack the egress plane also sits in the path, for web fetches. Everything else reads the same event stream afterwards. That split is why the stack can add a plane without slowing anything down, and also why a plane that reads the log cannot save you in the moment: by the time identity has an opinion, the call is finished.

### The interesting finding belonged to nobody

The gateway knew about the spend. The passport knew about the missing attestation. The chain knew about the delegation depth. The **high** severity came from joining them, and no single service could have produced it. Buy one plane and you get one plane's opinion.

### The narrow component is the one that reaches you

The piece with the smallest blast radius, a process that reads a file and sends mail, is the only one allowed out. That is the opposite of the usual shape, where the alerting system holds credentials for everything it might want to mention.

### Every step wrote something down, and that is the product

Each line under a step is a real event on a shared contract, which is why an incident can be reconstructed at all. A stack whose components only log for themselves gives you eight partial stories and no way to join them.

- **Where is the last point something can be refused?** If the answer is a dashboard, nothing is being refused.

- **Which component can say why, and how long does it take?** If the answer involves grepping, it is not an answer somebody can give under pressure.

- **What holds the credentials for the thing that emails you?** If it is all of them, the alerting path is now the largest target you own.

- **Does the notification act, or point?** A link that acts is a capability, and mail gateways follow links before anyone reads them.

- **Has the guardrail been fired on purpose recently?** A control nobody has exercised is a claim, not a control.

- **Can somebody outside your company check the record?** Evidence you have to be trusted about is not evidence.

## Where this sits.

Two moves in this walk are newer than the walk itself. Stopping the spend and stopping the authority are different acts, and the second one is [a revocation](https://it-rat.com/services/vouchryx.html) that lands at every enforcement point that polls, within one poll interval, rather than a 402 on the next call. And what the incident leaves behind is [sealed](https://it-rat.com/services/trailryx.html) daily by default, so the record of it can be shown to somebody who was not there. This walk is the products in motion. [AI agent governance](https://it-rat.com/ai-agent-governance.html) is the field it belongs to, [the record and the control](https://it-rat.com/ai-observability-vs-governance.html) is why watching is not the same as stopping, and [what runs where and what it costs](https://it-rat.com/what-runs-where.html) is the same stack seen from the infrastructure side. Every service named above is Apache-2.0 and runs on hardware you own; the whole set opens from [the corridor](https://it-rat.com/index.html#stack).

## What people ask about the incident path

**Q: Which parts of the stack can actually stop a call?**
Two: the money plane and the policy plane, because both sit in the request path. The gateway answers 402 before the provider is asked, and the policy decision point answers allow, deny or hold on every call. The other five read the shared event stream afterwards. That is a deliberate split, and it has a cost worth knowing: by the time the identity plane has an opinion about a run, the call it is reasoning about has already finished.

**Q: Why does a spend incident alone not raise a high-severity finding?**
Because on its own it is an agent having a bad afternoon. The detector wants at least two corroborating facts before it will call something high, and in this walk it gets two on top of the spend event: an agent with no attestation on record, and a delegation chain two hops deep. None of the three services holds all three facts. The severity comes from the join, which is the argument for a separate identity plane rather than a rule inside the gateway.

**Q: Why does the alert email contain a link instead of a kill button?**
Because a link that acts is an unauthenticated capability held by whoever can see or forward the message, and mail security gateways prefetch links, so the action would fire before a human read the sentence beside it. The link is a coordinate: it opens the panel showing that incident in your own console. The action happens there, behind a sign-in, and anything destructive additionally needs a fresh passkey confirmation bound to that exact command.

**Q: What does the notifier hold, and what can it reach?**
It reads a file and sends mail. It holds no credential for any plane, opens no connection to one, has no API of its own, and can take no action on any agent. That narrowness is the design rather than an implementation detail: it is the one component allowed out of the box, so its blast radius has to stay small enough to state in a sentence.

**Q: Why does the mail carry identifiers and numbers but no content?**
Because event payloads are written by components that sit next to prompts, model output and matched secrets, and mail leaves through a server nobody in your perimeter controls. Values are rendered through an allowlist of keys whose contents must also pass a shape check. A denylist would be one new producer away from leaking.

**Q: Can I see this fire without waiting for a real incident?**
Yes, and you should not trust the path until you have. The pre-production harness replays the same shape at a gateway standing in front of a fake provider: burn the budget and require the 402, request a denied tool and require the refusal, present a forged delegation chain and require rejection. It exits with differentiated codes so CI can tell a real guardrail gap from a broken harness.

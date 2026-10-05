<!-- https://it-rat.com/ai-agent-security.html -->

# AI agent security

> The failure modes an autonomous agent introduces, the runtime guardrail that answers each one, and how to rehearse them in CI. Defensive practice.

A chatbot that says something wrong is a content problem. An agent that acts on something wrong is a security problem, because it holds credentials, calls tools, and decides on its own what to do with text a stranger wrote. Nothing about that is unfamiliar to anyone who has secured a service account. What is new is that the thing holding the credential now reasons, and can be talked into changing its mind.

## The boundary is the tool call, not the prompt.

Most published advice about securing AI systems is really about the model's output: filters, refusals, red-team prompts. Useful for a chat product, and mostly beside the point for a fleet of agents doing work. An agent's damage does not arrive as a sentence. It arrives as a tool call: a write to a system of record, a transfer, a shell command, a request to an internal service with a credential attached.

That is good news, because a tool call is a boundary an engineer can defend the ordinary way. It can be identified, authorised, budgeted, rate-limited, journalled and rehearsed. **The security question for an agent fleet is not what the model might say. It is which calls the agent can make, on whose authority, and what stops the one it should not have made.**

Which puts most of this guide on familiar ground: identity, least privilege, blast radius, separation of duties, evidence. The controls are old. Only the actor is new.

## Eight ways an agent fleet actually gets hurt.

Each of these is defensive: it describes what to detect and refuse on your own estate. Under each, the control that answers it.

*injected instruction reaching a tool*

### Text becomes an action

An agent reads a page, a ticket or a document that contains instructions aimed at it, and the model treats them as a task. The prompt filter is the weak place to catch this; the tool boundary is the strong one.

**Answer:** taint-track what came from outside and refuse the actions it reaches, at the policy point, per call. [Wardryx →](https://it-rat.com/services/wardryx.html)

*excessive agency*

### Admin two hops away

An agent's own grants look modest, and its delegation chain reaches an identity that can do anything. Nobody drew that chain, so nobody saw it. This is OWASP's LLM06 in one sentence.

**Answer:** compute blast radius as the union of everything reachable through the chain, and alert when it touches admin. [Idryx →](https://it-rat.com/services/idryx.html)

*shadow tooling*

### An MCP server nobody sanctioned

Tools arrive faster than registries. An agent ends up calling a server that no inventory lists, and a tool whose description silently changed after you approved it, which is the supply-chain gap a re-fetch-on-connect model opens.

**Answer:** detect servers in use but absent from the sanctioned registry, pin a fingerprint of every approved tool, and fail the build when one changes. [Idryx →](https://it-rat.com/services/idryx.html) · [the MCP guide →](https://it-rat.com/mcp-security.html)

*credentials in the context*

### The secret is in the prompt

A token handed to the model is a token in the trace, in the logs, in the memory store, and in whatever the model repeats next. Rotation does not help if the leak is structural.

**Answer:** the agent holds a handle, never a value, and the real secret is injected at the last hop. [TokenFuse →](https://it-rat.com/services/tokenfuse.html)

*slow exfiltration*

### Nothing alarming, repeatedly

No single blocked action is interesting. Twenty of them from one agent inside a day is a pattern, and it is invisible if each is only ever handled where it happened.

**Answer:** correlate blocked actions per identity over a window and raise severity on repetition. [Idryx →](https://it-rat.com/services/idryx.html)

*compromise looks like a loop*

### The bill notices first

From the outside, an agent being driven by someone else and an agent stuck retrying are the same shape: sustained, fast, expensive. Waiting to tell them apart before reacting is how both get expensive.

**Answer:** treat sustained burn as an incident in its own right and cut the circuit, then investigate. [TokenFuse →](https://it-rat.com/services/tokenfuse.html)

*unattested and unowned*

### Nobody to call, nothing to revoke

A privileged agent with no attestation and no named owner is not a governance gap, it is an unrotatable credential with a personality. It is also the most common finding on a first scan.

**Answer:** require attestation for privileged agents, flag missing owners, and keep the inventory as a bill of materials. [Idryx →](https://it-rat.com/services/idryx.html) · [the identity guide →](https://it-rat.com/agent-identity.html)

*the guardrail that quietly stopped working*

### Off looks exactly like broken

A defence that was disabled in a config change six weeks ago behaves identically to one that is holding, right up until the day it matters.

**Answer:** rehearse each guardrail against a real gateway in CI, and refuse to count an unconfigured feature as a pass. [Mockryx →](https://it-rat.com/services/mockryx.html)

## What holds up, once the novelty wears off.

### Give every agent an identity, before you give it a tool

One identifier, one owner, one runtime, one attestation method, and a delegation chain that is recorded rather than implied. Everything else in this guide depends on being able to name the actor. An agent that acts under a shared key is an incident you cannot investigate.

### Deny at the boundary, not in the prompt

A system prompt asking the model not to do something is a request. A policy point that refuses the call is a control. Keep the list of forbidden actions short, explicit and enforced per call: shell execution, writes to systems of record, anything moving money. The model never gets a vote.

### Put a human on the actions that deserve one

Not on everything, or people will click through it in a week. On the small set where a mistake is expensive and slow to reverse. The workable shape is a hold the agent can be told to wait for, with the grant proven by a signed token bound to that exact agent, run and tool set, and to the call's own arguments where the request named them, so approving one action never quietly approves the next.

### Assume the tool inventory is wrong

It is. Tools are added by the person who needed one, on the afternoon they needed it. The realistic control is not a stricter process, it is detection: notice the server nobody registered, notice the tool description that changed, notice the agent that can now reach both.

### Rehearse, and let the rehearsal fail a build

Every guardrail here is a claim, and a claim nobody tests decays. Fire the drills at a real gateway with a fake provider behind it: the meter that trips is real, the invoice is not. A defence that stopped working should fail a pull request, not an incident review.

### Keep evidence as you go

Every decision, refusal, kill and approval journalled when it happens, each record carrying the hash of the one before it, so the chain is verifiable by somebody who does not trust you. Security work that cannot be shown is security work that will be repeated under worse conditions.

Everything here is defensive: it inspects, detects and refuses on your own estate. Nothing in the stack crafts adversarial prompts, manipulates another system's outputs, or attacks anything, and the drills are rehearsals fired at your own gateway with a fake provider behind it. Where we describe an attack, it is to say what to detect and what to stop, which is the only reason to name it.

## The other two halves of the same job.

Security, cost and control are one conversation held in three rooms. If you came here first, the other two are worth twenty minutes: [AI agent governance and the runtime controls](https://it-rat.com/ai-agent-governance.html), and [FinOps for AI, on spend that creates itself](https://it-rat.com/finops-for-ai.html). The newest surface has its own guide: [MCP security](https://it-rat.com/mcp-security.html). All of the tools are Apache-2.0 and run on infrastructure you own, and [one command starts the live services locally](https://it-rat.com/services/platform.html#run).

- **Where does it enforce: the prompt or the tool call?** Filtering model output is useful and is not a boundary. The call is the boundary, because that is where the damage happens.

- **Does it model delegation as a chain?** One-hop \u201cacts on behalf of\u201d cannot show an agent reaching admin two hops away, which is the finding that matters most.

- **Is detection deterministic?** If a model sits in the detection path, a finding cannot be reproduced, and an auditor is entitled to ask you to reproduce it.

- **Does it distinguish a gap from an unconfigured feature?** A tool that reports a missing guardrail as a pass, or an absent feature as a breach, is teaching you to ignore it.

- **Can the guardrails be exercised on demand?** A defence nobody tests decays quietly. Ask how you would prove, today, that it still holds.

- **What does it do with the credential?** If the agent has to hold the real secret to use the tool, the secret is in the context window, the trace and the logs.

## What people ask about securing agents

**Q: What is different about securing an AI agent?**
The actor reasons and can be talked into changing its mind, but the damage still arrives as a tool call: a write, a transfer, a shell command, a request carrying a credential. That makes the tool boundary the place to defend, with the same discipline as any service account: identity, least privilege, blast radius, evidence.

**Q: How do I stop prompt injection from reaching a tool?**
Not with a better prompt. Taint-track what came from outside the trust boundary and refuse the actions it reaches, at the policy point, per call. A system prompt asking the model not to do something is a request; a decision point that denies the call is a control.

**Q: What is excessive agency?**
OWASP's LLM06: an agent that reaches admin-equivalent power through its delegation chain rather than through its own grants. Its own permissions look modest, and two hops away it can do anything. Finding it needs the chain drawn as a graph, because no permission list on a single identity will show it.

**Q: How do I know an agent is not exfiltrating data slowly?**
Correlate rather than count. A single blocked action is noise; a stream of blocked actions from one identity inside a day is a pattern, and severity should rise with repetition and with the privilege of the identity doing it.

**Q: How do we prove our guardrails still work?**
Rehearse them in CI against a real gateway with a fake provider behind it, so the meter that trips is real and the invoice is not. And refuse to count an unconfigured feature as a pass: a guardrail that is switched off looks exactly like one that is broken.

<!-- https://it-rat.com/services/wardryx.html -->

# Wardryx, the policy plane

> The policy plane your agents ask before acting: allow, deny or hold for a human, with signed approval tokens and a hard ceiling that outranks approvals.

Your gateway asks one question before an agent acts: POST /v1/decide. Wardryx answers allow, deny or hold in one deterministic pass. No LLM sits in the decision path, so the same policy and the same request always return the same verdict, and a big spend waits for a human who signs off with a short-lived token. The pattern is old and good: PDP/PEP, XACML's good ideas, pointed at what agents do.

## Watch the gate sort a stampede.

This is a simulation, and it says so. It replays the shape of the live validation record: a 34-request concurrent burst, different agents, budgets and policies, all hitting /v1/decide at once. In the real run the filtering came back exact: 6/6 permission oversteppers denied with 403, unattested calls denied until attested, 176 decisions across the full campaign.

## One question in. One of three answers out.

The PEP posts the proposed action: agent, tools, declared domains, step count, estimated cost, attestation. Wardryx matches policies by agent:// glob and applies the rules in a fixed order, where deny_above_usd outranks every approval and the hold check comes after it. The verdict returns with a cacheable flag, the caller's cache keys on agent, tool set and attestation, and every decision leaves as an event.

## Six primitives. One fixed order. No moods.

### Three verdicts, zero improvisation

Every answer is allow, deny or hold. No LLM sits in the decision path, so the same policy set and the same request return the same verdict, every time. A decision you can replay in a test is a decision you can defend in an audit.

### Hold means a human

A big spend becomes a hold, not a guess. A human grants it out of band and the agent resubmits with a signed token; nothing parks a connection waiting for a signature.

**Q: How a hold is resolved**

The agent asks, Wardryx answers `hold` with an approval id, and the call ends there. A human decides out of band, Wardryx mints an approval token, and the agent asks again with the token in hand; that second answer is `allow`. No connection is parked waiting for a signature, and Wardryx does not have to remember an open request: the grant is proven by the token, not by anyone's memory of it.

The token is bound to what was actually approved. Its claims name the agent, the run and the exact sorted set of tools, and carry an expiry, ten minutes by default; verification recomputes the HMAC over the still-encoded payload before decoding anything, then checks that what is being asked matches what was granted. A token for one run does not quietly authorise another.

Since v1.2.0 an approval is also bound to the tool call a person read, when the held request carried one. The person is shown the tool and its target, and the token carries a digest of the name, the target and the exact arguments, so it is refused for any other call, the same JSON re-spaced included. A call whose arguments were too large to send binds only its name and target.

The signing secret is fail-closed. With it unset, Wardryx refuses to mint or verify rather than accepting anything, because there is no such thing as an unsigned or always-valid approval. Since 1.0 a token works once by default: the first redemption is recorded atomically, so presenting the same token twice falls back to a fresh hold instead of silently allowing the action again. Setting `WARDRYX_APPROVAL_SINGLE_USE=false` makes it reusable within its window. With no shared database that single-use guarantee is per process, and the server says so at startup rather than letting you assume otherwise.

### A hard ceiling that outranks approvals

deny_above_usd is the rule no token can talk past. It is checked before the hold logic ever runs, so even a granted approval cannot authorize a spend over the ceiling. Some numbers should end the conversation, and this one does.

### Attestation as a first-class gate

deny_if_unattested demands a live attestation before an agent touches the sensitive rules. Methods are trimmed and lowercased on the way in, so a literal “None” string reads as no attestation instead of sneaking past as a value.

### Fail-open or fail-closed, your call

When the decision point is unreachable, the enforcement point picks the failure mode per deployment. The gateway's binary defaults to open and both launchers set it closed on purpose; the egress point fails closed with no override. Every default is documented, and so is the tradeoff.

**Q: The modes, and what an outage costs**

Wardryx itself never acts. It answers; the enforcement point, a gateway or a proxy, decides how much weight to give the answer. There are three settings at that call site.

Two enforcement points ask this plane, and the answer lives at the call site rather than here. **TokenFuse**'s binary defaults to open, because a money plane that refused every call whenever the policy plane blinked would cost an operator production traffic over a network partition; both launchers override that to closed, because on a box that exists to govern, policy wins. That is not a reading of the configuration. On 2026-09-17 the policy plane was stopped under a box governing two clouds, and every call came back `403 wardryx unreachable` in 0.3 s, none reaching the provider, until it was started again. **Scopyx** fails closed with no override: an egress point that failed open is an unrestricted fetch proxy wearing a governance label, and that failure would be silent.

**off** never calls the decision point at all: local development, or an environment with no policy loaded. **shadow** asks on every call and records the answer while the action always proceeds, which is how a new policy set is validated against real traffic before it can block anything. **enforce** makes the answer binding: a deny stops the call, a hold pauses it until a signed approval token is presented.

Then the question everyone postpones: what happens when the decision point cannot be reached. Fail-open treats it as allow, so availability wins and an outage silently disables policy. Fail-closed treats it as deny, so policy wins and an outage blocks every governed action until it recovers. There is no clever third answer; there is only choosing on purpose and writing the choice down.

Wardryx applies the same rule to itself. Started with no policy configured, it starts anyway and allows, and it says so in the log rather than pretending to enforce something it was never given.

### Policy admin API + Terraform

PUT, GET and DELETE /v1/policies/{id} manage a runtime policy layer with validate-then-apply semantics; the file-loaded set stays a permanent floor no API write can erase. The taipan_wardryx_policy resource drives the same API from Terraform.

## Where the no comes from matters.

Two substitutes get proposed for a policy plane: asking the model to behave in the system prompt, and pointing at the IAM you already run. Keep your IAM; it answers a different question. Neither substitute sees tools, dollars and runs in one place.

|  | Wardryx | “Prompt the model to behave” | IAM alone |
|---|---|---|---|
| Deterministic | Yes: same input, same verdict | No | Yes |
| Knows about cost | Holds above $X | No | No |
| Human approval flow | Built in, token-bound | No | Ticket queue |
| Sees declared-but-not-invoked tools | Yes, since the live-found bypass was fixed | n/a | No |
| Auditability | Every decision an event | Vibes | Partial |

### The desk every expensive idea stops at.

[TokenFuse](https://it-rat.com/tokenfuse.html)'s PEP hook asks Wardryx on every request and stamps the verdict on the response. Each decision lands on the bus as a source: wardryx event, which [Idryx](https://it-rat.com/idryx.html) correlates into the identity graph. [Mockryx](https://it-rat.com/mockryx.html) rehearses the denials in pre-prod, so the first real no is never the first no ever. And the policies themselves are code: the [Platform](https://it-rat.com/platform.html) page's Terraform provider creates, changes and destroys them like any other resource. A typed risk signal from [Typryx](https://it-rat.com/typryx.html) can turn an allow into a hold for a person and never into a deny: since v1.2.0 a decision reads `signals` and the pending `tool_call`, a `hold_if_signal` rule can only hold, and Typryx's `wardryx-proxy` adds the signal on the way in. The launchers offer it as an opt-in, off by default, and it was measured on the stub backend only.

The policy point is one control among several: see [AI agent security](https://it-rat.com/ai-agent-security.html) for the failure modes it answers, and [AI agent governance](https://it-rat.com/ai-agent-governance.html) for how the planes fit together.

Boots on `:8090` with an in-memory store: allow-all until you load a policy, and it logs that choice. Then dry-run a policy offline against a directory of Agent Passports:

## A decision is only as good as the identity under it.

This plane answers about an action. What it cannot answer is whether the caller really holds the delegation it claims, which is a different question with a different mechanism: [Vouchryx](https://it-rat.com/vouchryx.html) mints a short-lived token bound to the caller's own key and lets a person end it, and a hold resolved by a signed approval token is the same idea pointed at one action rather than at a delegation.

## Putting a human in front of the expensive actions

**Q: How do I require human approval before an agent does something expensive?**
Set a threshold in policy. Above it the answer to the agent is `hold` rather than allow, a human grants or refuses out of band, and the agent resubmits with a signed approval token bound to that agent, run and tool set, and, when the held request named the tool call, to that exact call. The token works once by default. No connection is parked waiting for a signature.

**Q: What answers can the policy plane give?**
Three, and only three: allow, deny, or hold for a human. There is no improvisation and no fourth case, which is what makes the decisions reproducible and arguable after the fact.

**Q: What happens if the policy service is unreachable?**
You choose, per deployment, and the choice is written down. Fail-open treats it as allow, so availability wins and an outage silently disables policy. Fail-closed treats it as deny, so policy wins and an outage blocks every governed action. The shipped launchers choose closed for the gateway, and it was fired on purpose on 2026-09-17: the policy plane stopped, every governed call refused in 0.3 s, none reaching the provider, and the first call after the restart allowed. Started with no policy loaded, Wardryx allows and says so in the log rather than pretending to enforce.

**Q: Can policies be reviewed like code?**
Yes. Budgets, passports and policies are Terraform resources, so they get pull requests, plans and diffs, and an edit made out of band shows up on the next plan instead of quietly persisting.

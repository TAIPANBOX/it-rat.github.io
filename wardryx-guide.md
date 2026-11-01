<!-- https://it-rat.com/wardryx-guide.html -->

# Wardryx guide

> How Wardryx decides allow, deny or hold, how to run it, what changed from 1 to 15 October 2026, and what is open by default or not proven yet.

The [Wardryx room](https://it-rat.com/services/wardryx.html) keeps the simulation, the drawing and the common questions. This guide keeps the rest of what the room used to say: how a hold is resolved, the modes and the outage choice, where it sits, how to run it, what changed from 1 to 15 October 2026, and its limits.

- [At a glance](https://it-rat.com/wardryx-guide.html#overview)

- [How it works](https://it-rat.com/wardryx-guide.html#how-it-works)

- [Where it sits](https://it-rat.com/wardryx-guide.html#where-it-sits)

- [Running it](https://it-rat.com/wardryx-guide.html#run)

- [What changed](https://it-rat.com/wardryx-guide.html#changes)

- [Limits](https://it-rat.com/wardryx-guide.html#limits)

## Wardryx at a glance.

- **Deterministic allow, deny or hold, with a human on the expensive actions.**

- **Status:** v2.4.0, surface frozen at 1.0 · main is supported.

- **Core:** Go 1.27 · deterministic PDP. **API:** POST /v1/decide on :8090.

- **Rules:** deny_tool · allow_tool · deny_if_unattested · deny_if_chain_unproven · max_steps · allow_domains · deny_above_usd · require_human_above_usd · hold_if_signal.

- **Lineage:** PDP/PEP · XACML's good ideas.

- **Licence:** Apache-2.0.

### What it is

Your gateway asks one question before an agent acts: POST /v1/decide. Wardryx answers allow, deny or hold in one deterministic pass. No LLM sits in the decision path, so the same policy and the same request always return the same verdict, and a big spend waits for a human who signs off with a short-lived token. The pattern is old and good: PDP/PEP, XACML's good ideas, pointed at what agents do.

## Rules in one fixed order. No moods.

### Sixty seconds, thirty-four requests

This is a simulation, and it says so. It replays the shape of the live validation record: a 34-request concurrent burst, different agents, budgets and policies, all hitting /v1/decide at once. In the real run the filtering came back exact: 6/6 permission oversteppers denied with 403, unattested calls denied until attested, 176 decisions across the full campaign. [Watch it in the room](https://it-rat.com/services/wardryx.html#sim).

### One question in. One of three answers out.

The PEP posts the proposed action: agent, tools, declared domains, step count, estimated cost, attestation. Wardryx matches policies by agent:// glob and applies the rules in a fixed order, where deny_above_usd outranks every approval and the hold check comes after it. The verdict returns with a cacheable flag, the caller's cache keys on agent, tool set and attestation, and every decision leaves as an event.

### Three verdicts, zero improvisation

Every answer is allow, deny or hold. No LLM sits in the decision path, so the same policy set and the same request return the same verdict, every time. A decision you can replay in a test is a decision you can defend in an audit.

### Hold means a human

A big spend becomes a hold, not a guess. A human grants it out of band and the agent resubmits with a signed token; nothing parks a connection waiting for a signature.

### A hold that holds nothing open

The agent asks, Wardryx answers `hold` with an approval id, and the call ends there. A human decides out of band, Wardryx mints an approval token, and the agent asks again with the token in hand; that second answer is `allow`. No connection is parked waiting for a signature, and Wardryx does not have to remember an open request: the grant is proven by the token, not by anyone's memory of it.

The token is bound to what was actually approved. Its claims name the agent, the run and the exact sorted set of tools, and carry an expiry, ten minutes by default; verification checks the signature over the still-encoded payload before reading any claim, then checks that what is being asked matches what was granted. A token for one run does not quietly authorise another.

Since v1.2.0 an approval is also bound to the tool call a person read, when the held request carried one. The person is shown the tool and its target, and the token carries a digest of the name, the target and the exact arguments, so it is refused for any other call, the same JSON re-spaced included. A call whose arguments were too large to send binds only its name and target.

The signing is fail-closed. The token is signed by Keyryx custody (ES256) when WARDRYX_APPROVAL_SIGNER=keyryx, which the stack-single and stack-up launchers set (and stack-k8s sets it by default from 1.6.0, tagged 2026-10-19, unless it is deployed with --without-keyryx), and with an HMAC secret otherwise. With neither a signer nor the secret, Wardryx refuses to mint or verify rather than accepting anything, because there is no such thing as an unsigned or always-valid approval. Since 1.0 a token works once by default: the first redemption is recorded atomically, so presenting the same token twice falls back to a fresh hold instead of silently allowing the action again. Setting `WARDRYX_APPROVAL_SINGLE_USE=false` makes it reusable within its window. With no shared database that single-use guarantee is per process, and the server says so at startup rather than letting you assume otherwise.

### A hard ceiling that outranks approvals

deny_above_usd is the rule no token can talk past. It is checked before the hold logic ever runs, so even a granted approval cannot authorize a spend over the ceiling. Some numbers should end the conversation, and this one does.

### Attestation as a first-class gate

deny_if_unattested demands a live attestation before an agent touches the sensitive rules. Methods are trimmed and lowercased on the way in, so a literal “None” string reads as no attestation instead of sneaking past as a value.

### Fail-open or fail-closed, your call

When the decision point is unreachable, the enforcement point picks the failure mode per deployment. The TokenFuse gateway closes under enforce when its failure mode is unset, and stays open in shadow mode, where it blocks nothing; both launchers set it closed on purpose. The egress point fails closed with no override. Every default is documented, and so is the tradeoff.

### Three modes at the call site, and one honest choice about outages

Wardryx itself never acts. It answers; the enforcement point, a gateway or a proxy, decides how much weight to give the answer. There are three settings at that call site.

Two enforcement points ask this plane, and the answer lives at the call site rather than here. **TokenFuse**'s binary closes under enforce when its failure mode is unset, and stays open in shadow mode, where it blocks nothing. It was open under enforce until 2026-10-17, for the reason a money plane gives: a call refused on every policy blink costs production traffic during a network partition. All three launchers set it closed, because on a box that exists to govern, policy wins. That is not a reading of the configuration. On 2026-09-17 the policy plane was stopped under a box governing two clouds, and every call came back `403 wardryx unreachable` in 0.3 s, none reaching the provider, until it was started again. **Scopyx** fails closed with no override: an egress point that failed open is an unrestricted fetch proxy wearing a governance label, and that failure would be silent.

**off** never calls the decision point at all: local development, or an environment with no policy loaded. **shadow** asks on every call and records the answer while the action always proceeds, which is how a new policy set is validated against real traffic before it can block anything. **enforce** makes the answer binding: a deny stops the call, a hold pauses it until a signed approval token is presented.

Then the question everyone postpones: what happens when the decision point cannot be reached. Fail-open treats it as allow, so availability wins and an outage silently disables policy. Fail-closed treats it as deny, so policy wins and an outage blocks every governed action until it recovers. There is no clever third answer; there is only choosing on purpose and writing the choice down.

Wardryx applies the same rule to itself. Started with no policy configured, it starts anyway and allows, and it says so in the log rather than pretending to enforce something it was never given.

### Policy admin API + Terraform

PUT, GET and DELETE /v1/policies/{id} manage a runtime policy layer with validate-then-apply semantics; the file-loaded set stays a permanent floor no API write can erase. A PUT whose body holds a key the policy does not declare is refused with 400 and stores nothing (since 1.3.2). The taipan_wardryx_policy resource drives the same API from Terraform.

## The desk every expensive idea stops at.

[TokenFuse](https://it-rat.com/services/tokenfuse.html)'s PEP hook asks Wardryx on every request and stamps the verdict on the response. Each decision lands on the bus as a source: wardryx event, which [Idryx](https://it-rat.com/services/idryx.html) correlates into the identity graph. [Mockryx](https://it-rat.com/services/mockryx.html) rehearses the denials in pre-prod, so the first real no is never the first no ever. And the policies themselves are code: the [Platform](https://it-rat.com/services/platform.html) page's Terraform provider creates, changes and destroys them like any other resource. A typed risk signal from [Typryx](https://it-rat.com/services/typryx.html) can turn an allow into a hold for a person and never into a deny: since v1.2.0 a decision reads `signals` and the pending `tool_call`, a `hold_if_signal` rule can only hold, and Typryx's `wardryx-proxy` adds the signal on the way in. The launchers offer it as an opt-in, off by default, and it was measured on the stub backend only.

The policy point is one control among several: see [AI agent security](https://it-rat.com/ai-agent-security.html) for the failure modes it answers, and [AI agent governance](https://it-rat.com/ai-agent-governance.html) for how the planes fit together.

### A decision is only as good as the identity under it.

This plane answers about an action. What it cannot answer is whether the caller really holds the delegation it claims, which is a different question with a different mechanism: [Vouchryx](https://it-rat.com/services/vouchryx.html) mints a short-lived token bound to the caller's own key and lets a person end it, and a hold resolved by a signed approval token is the same idea pointed at one action rather than at a delegation.

## Running it.

```
make serve
```

Boots on `127.0.0.1:8090` with an in-memory store. `serve` refuses to start without `WARDRYX_KEYS`, so `make serve` opts in to the dev key on loopback only: allow-all until you load a policy, and it logs that choice. Then dry-run a policy offline against a directory of Agent Passports:

```
./bin/wardryx check ./passports ./policies/finance.yaml
```

## What the policy plane gained from 1 to 15 October

The whole stack's fortnight, Wardryx among it, is in [the October changelog](https://it-rat.com/changes-2026-10.html#wardryx).

| shipped in | what it does |
|---|---|
| v1.3.0 | A policy can name the only tools its agents may use. A requested tool the list does not name is denied, and no approval can lift that. |
| v1.3.1 | Every document of a YAML policy file, and every value of a JSON policy file, is loaded. A file that does not load stops the service at start, and the error names the part that failed. |
| v1.3.2 | A policy write with a field the policy does not declare is refused with a 400, and nothing is stored. Before, the field was dropped and the write still answered 200. |
| v1.4.0 | A policy can hold a tool call whose risk signal never arrives (when_absent: hold), for a person to decide. |
| v1.5.0 | A policy can name the only models its agents may use. A request for any other model is denied on that call. |

## What is open by default, and what is not proven yet.

- When the decision point is unreachable, the enforcement point picks the failure mode per deployment. The TokenFuse gateway closes under enforce when its failure mode is unset, and stays open in shadow mode, where it blocks nothing; both launchers set it closed on purpose. The egress point fails closed with no override.

- Started with no policy configured, it starts anyway and allows, and it says so in the log rather than pretending to enforce something it was never given.

- With no shared database the single-use guarantee of an approval token is per process, and the server says so at startup rather than letting you assume otherwise. Setting `WARDRYX_APPROVAL_SINGLE_USE=false` makes a token reusable within its window.

- A call whose arguments were too large to send binds only its name and target.

- The typed risk signal from Typryx: the launchers offer it as an opt-in, off by default, and it was measured on the stub backend only.

- The room's stampede is a simulation, and it says so: it replays the shape of the live validation record.

## Back to the room.

The [Wardryx room](https://it-rat.com/services/wardryx.html) has the simulation, the drawing and the common questions, and [the guides index](https://it-rat.com/guides.html) has the field itself.

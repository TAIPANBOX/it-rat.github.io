<!-- https://it-rat.com/wardryx-guide.html -->

# Wardryx guide

> How Wardryx decides allow, deny or hold, how to run it, what changed from 1 to 15 October 2026, and what is open by default or not proven yet.

The [Wardryx room](https://it-rat.com/services/wardryx.html) keeps the simulation, the drawing and the common questions. This guide keeps the rest of what the room used to say: how a hold is resolved, the modes and the outage choice, where it sits, how to run it, what changed from 1 to 15 October 2026, and its limits.

- [At a glance](https://it-rat.com/wardryx-guide.html#overview)

- [How it works](https://it-rat.com/wardryx-guide.html#how-it-works)

- [Where it sits](https://it-rat.com/wardryx-guide.html#where-it-sits)

- [Running it](https://it-rat.com/wardryx-guide.html#run)

- [What changed](https://it-rat.com/wardryx-guide.html#changes)

- [What changed in November](https://it-rat.com/wardryx-guide.html#changes-november)

- [Limits](https://it-rat.com/wardryx-guide.html#limits)

## Wardryx at a glance.

- **Deterministic allow, deny or hold, with a human on the expensive actions.**

- **Status:** v2.7.0, surface frozen at 1.0 · main is supported.

- **Core:** Go 1.27 · deterministic PDP. **API:** POST /v1/decide on :8090.

- **Rules:** deny_tool · allow_tool · allow_models · allow_domains · max_steps · deny_if_unattested · require_identity_source · max_chain_depth · require_root_principal · deny_if_chain_unproven · deny_above_usd · require_human_above_usd · hold_if_signal.

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

Since v2.7.0 the person deciding a hold can also read the call's arguments first. Wardryx builds the preview from the exact bytes the token's digest covers, hides credentials and personal data by fixed rules, and seals it to the console's key, keeping only the ciphertext until the hold is decided or 24 hours pass. The record says whether the approver saw it or granted unseen. It does nothing until a preview key is set; stack-single 1.10.0 and stack-k8s 1.13.0 set one.

The signing is fail-closed. The token is signed by Keyryx custody (ES256) when WARDRYX_APPROVAL_SIGNER=keyryx, which the stack-single and stack-up launchers set (and stack-k8s sets it by default from 1.6.0, tagged 2026-10-19, unless it is deployed with --without-keyryx), and with an HMAC secret otherwise. With neither a signer nor the secret, Wardryx refuses to mint or verify rather than accepting anything, because there is no such thing as an unsigned or always-valid approval. Since 1.0 a token works once by default: the first redemption is recorded atomically, so presenting the same token twice falls back to a fresh hold instead of silently allowing the action again. Setting `WARDRYX_APPROVAL_SINGLE_USE=false` makes it reusable within its window. With no shared database that single-use guarantee is per process, and the server says so at startup rather than letting you assume otherwise.

### A spent error budget is a reason to hold

The quality plane, [Verdryx](https://it-rat.com/services/verdryx.html), writes an `slo_burn` event to its event file when an agent's error budget is exhausted or burning fast. With `WARDRYX_SIGNAL_EVENTS` pointing at that file, Wardryx adds one standing signal named `slo_burn` to the agent's decisions, and a `hold_if_signal` rule on it holds the call. A granted approval lets that one call through, as for any hold. Both launchers set it and seed the rule, so a spent budget waits for a person out of the box. On its own it is off unless the setting is set, and it changes nothing without a rule that reads the signal: same answer, same policy version.

```
name: hold-while-the-budget-is-spent
target: "agent://acme.example/support/*"
hold_if_signal:
  name: slo_burn
  values: [exhausted, fast_burn]
  min_probability: 1
```

The signal takes four values, `exhausted`, `fast_burn`, `unmeasured` and `none`, always at probability 1. An unmeasured zero is not evidence of health: a fast burn whose `burn_events_seen` is missing, zero, negative, fractional or not a number reads as `unmeasured`, never as `none` and never as `fast_burn`. An exhausted event stands on the budget, so its `burn_events_seen` does not matter. While the file is sound the signal is present for every agent, because `when_absent: hold` holds every call with no signal of the rule's name, and a signal only for agents with an event would make that setting hold the healthy ones too. Absence therefore means one thing: the file cannot be believed, and the policy's `when_absent` decides.

The reader sits outside the decision code, so the signal can add a hold and nothing else, and a recorded decision replays with the file gone. A caller's own `slo_burn` signal is dropped, so it cannot end an absence hold. An event signals for `WARDRYX_SIGNAL_EVENTS_MAX_AGE` after its time (48 hours unless set), the newest event of an indicator replaces its older ones, and the quality plane writes no event on recovery, so recovery is a weaker event or the age running out.

The file is checked before it is believed. The hash chain is verified, and a broken chain, a malformed line, a restart, a start in the middle of a chain, a time in the future or a file past its size bound reads as `broken`; a missing file, or one that is not a plain file, reads as `unreadable`. `/readyz` says which in `signal_events` without changing its status code, and the log names the file and the reason once per change.

### A hard ceiling that outranks approvals

deny_above_usd is the rule no token can talk past. It is checked before the hold logic ever runs, so even a granted approval cannot authorize a spend over the ceiling. Some numbers should end the conversation, and this one does.

### Attestation as a first-class gate

deny_if_unattested demands a live attestation before an agent touches the sensitive rules. Methods are trimmed and lowercased on the way in, so a literal “None” string reads as no attestation instead of sneaking past as a value.

### A proof is accepted once, on every instance

When a decide carries an agent's DPoP proof, Wardryx accepts that proof once. With `WARDRYX_DB` set, the record of accepted proofs is the table `agent_proof_replays`, shared by every instance on that database. A proof presented at a second instance, or again after a restart, is refused with `403 agent_token_proof_invalid`. The claim is one atomic insert and the last step of the check, so only a proof that passed every other check reaches the database, and the key is a hash over the holder's key thumbprint and the proof's id, so no client byte reaches SQL and one holder cannot spend another's id. A row is kept until the longest proof window has closed, and a purge removes the rows after that.

A record that cannot be asked refuses. A proof nobody could check for replay may be a replay, so a store that is gone answers `503 agent_token_proof_unrecorded`, a store that failed with an error of its own answers 500, and the process does not stand in with a memory of its own. TokenFuse treats any answer outside 2xx as its fail mode, closed under enforce unless an operator set it open. A request with no proof decides from memory as before. Without a database the record stays in the process, and serve says so at start.

### Fail-open or fail-closed, your call

When the decision point is unreachable, the enforcement point picks the failure mode per deployment. The TokenFuse gateway closes under enforce when its failure mode is unset, and stays open in shadow mode, where it blocks nothing; all three launchers set it closed on purpose. The egress point fails closed with no override. Every default is documented, and so is the tradeoff.

### Three modes at the call site, and one honest choice about outages

Wardryx itself never acts. It answers; the enforcement point, a gateway or a proxy, decides how much weight to give the answer. There are three settings at that call site.

Two enforcement points ask this plane, and the answer lives at the call site rather than here. **TokenFuse**'s binary closes under enforce when its failure mode is unset, and stays open in shadow mode, where it blocks nothing. It was open under enforce until 2026-10-17, for the reason a money plane gives: a call refused on every policy blink costs production traffic during a network partition. All three launchers set it closed, because on a box that exists to govern, policy wins. That is not a reading of the configuration. On 2026-09-17 the policy plane was stopped under a box governing two clouds, and every call came back `403 wardryx unreachable` in 0.3 s, none reaching the provider, until it was started again. **Scopyx** fails closed with no override: an egress point that failed open is an unrestricted fetch proxy wearing a governance label, and that failure would be silent.

**off** never calls the decision point at all: local development, or an environment with no policy loaded. **shadow** asks on every call and records the answer while the action always proceeds, which is how a new policy set is validated against real traffic before it can block anything. **enforce** makes the answer binding: a deny stops the call, a hold pauses it until a signed approval token is presented.

Then the question everyone postpones: what happens when the decision point cannot be reached. Fail-open treats it as allow, so availability wins and an outage silently disables policy. Fail-closed treats it as deny, so policy wins and an outage blocks every governed action until it recovers. There is no clever third answer; there is only choosing on purpose and writing the choice down.

Wardryx applies the same rule to itself. Started with no policy configured, it starts anyway and allows, and it says so in the log rather than pretending to enforce something it was never given.

### Policy admin API + Terraform

PUT, GET and DELETE /v1/policies/{id} manage a runtime policy layer with validate-then-apply semantics; the file-loaded set stays a permanent floor no API write can erase. A PUT whose body holds a key the policy does not declare is refused with 400 and stores nothing (since 1.3.2). The taipan_wardryx_policy resource drives the same API from Terraform.

## The desk every expensive idea stops at.

[TokenFuse](https://it-rat.com/services/tokenfuse.html)'s PEP hook asks Wardryx on every request and stamps the verdict on the response. Each decision lands on the bus as a source: wardryx event, which [Idryx](https://it-rat.com/services/idryx.html) correlates into the identity graph. [Mockryx](https://it-rat.com/services/mockryx.html) rehearses the denials in pre-prod, so the first real no is never the first no ever. And the policies themselves are code: the [Platform](https://it-rat.com/services/platform.html) page's Terraform provider creates, changes and destroys them like any other resource. A typed risk signal from [Typryx](https://it-rat.com/services/typryx.html) can turn an allow into a hold for a person and never into a deny: since v1.2.0 a decision reads `signals` and the pending `tool_call`, a `hold_if_signal` rule can only hold, and Typryx's `wardryx-proxy` adds the signal on the way in. The launchers offer it as an opt-in, off by default.

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

## What changed in November

| shipped in | what it does |
|---|---|
| v2.5.0 | With a database set, the record of accepted DPoP proofs is shared by every instance and survives a restart: a proof is accepted once, and a record that cannot be asked refuses the decide with a 503. |
| v2.5.0 | A spent error budget can put an agent's tool calls to a person: with WARDRYX_SIGNAL_EVENTS set, a hold_if_signal rule on slo_burn holds the call. |
| v2.5.1 | The policy archive is created with directory mode 0750 and file mode 0640, so the account that runs wardryx replay can read it from the group of the account that writes it. An archive written before keeps its modes until an operator widens it. |
| v2.7.0 | The person who decides a held call can read its arguments first, sealed to the console's key, with secrets and personal data hidden by fixed rules. Nothing changes until a preview key is set. |

## What is open by default, and what is not proven yet.

- When the decision point is unreachable, the enforcement point picks the failure mode per deployment. The TokenFuse gateway closes under enforce when its failure mode is unset, and stays open in shadow mode, where it blocks nothing; all three launchers set it closed on purpose. The egress point fails closed with no override.

- Started with no policy configured, it starts anyway and allows, and it says so in the log rather than pretending to enforce something it was never given.

- With no shared database the single-use guarantee of an approval token is per process, and the server says so at startup rather than letting you assume otherwise. Setting `WARDRYX_APPROVAL_SINGLE_USE=false` makes a token reusable within its window.

- A call whose arguments were too large to send binds only its name and target.

- An outage of the store behind the proof record stops every decide that carries a proof. Every instance must run this build, because an older one keeps its own record, and two clocks more than five minutes apart can accept a proof twice.

- The chain behind the budget signal shows that a line was not edited or removed from the middle. It does not say who wrote the file and cannot see lines cut from the end, so the file is as trustworthy as its permissions. An event is matched by exact agent id, in no org, and a crash mid-write leaves the file broken until it is moved aside. Under `when_absent: hold`, a file that cannot be read holds every tool call of the agents the rule matches.

- The typed risk signal from Typryx: the launchers offer it as an opt-in, off by default.

- The room's stampede is a simulation, and it says so: it replays the shape of the live validation record.

## Back to the room.

The [Wardryx room](https://it-rat.com/services/wardryx.html) has the simulation, the drawing and the common questions, and [the guides index](https://it-rat.com/guides.html) has the field itself.

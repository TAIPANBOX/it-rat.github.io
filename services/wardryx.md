<!-- https://it-rat.com/services/wardryx.html -->

# Wardryx, the policy plane

> The policy plane your agents ask before acting: allow, deny or hold for a human, with signed approval tokens and a hard ceiling that outranks approvals.

Your gateway asks one question before an agent acts: POST /v1/decide. Wardryx answers allow, deny or hold in one deterministic pass. No LLM sits in the decision path, so the same policy and the same request always return the same verdict.

## Watch the gate sort a stampede.

This is a simulation, and it says so. It replays the shape of the live validation record: a 34-request concurrent burst, different agents, budgets and policies, all hitting /v1/decide at once.

## One question in. One of three answers out.

The PEP posts the proposed action: agent, tools, declared domains, step count, estimated cost, attestation. Wardryx matches policies by agent:// glob and applies the rules in a fixed order, where deny_above_usd outranks every approval and the hold check comes after it.

## Rules in one fixed order. No moods.

### Three verdicts, zero improvisation

Every answer is allow, deny or hold. A decision you can replay in a test is a decision you can defend in an audit.

### Hold means a human

A big spend becomes a hold, not a guess. A human grants it out of band and the agent resubmits with a signed token.

### A hard ceiling that outranks approvals

deny_above_usd is the rule no token can talk past. It is checked before the hold logic ever runs, so even a granted approval cannot authorize a spend over the ceiling.

### Attestation as a first-class gate

deny_if_unattested demands a live attestation before an agent touches the sensitive rules.

### A spent error budget puts the agent to a person

The quality plane writes an slo_burn event when an agent's error budget is exhausted or burning fast. A hold_if_signal rule on it holds that agent's calls for a person, model calls included, and a granted approval lets one call through. Both launchers set this up, so a spent budget waits for a person out of the box. On its own, wardryx stays off until WARDRYX_SIGNAL_EVENTS names the event file.

### A DPoP proof is accepted once

With WARDRYX_DB set, the record of accepted proofs is shared by every instance on that database and survives a restart, so a replay at a second instance is refused. A record that cannot be asked refuses the decide instead of passing the proof.

### The desk every expensive idea stops at.

[TokenFuse](https://it-rat.com/services/tokenfuse.html)'s PEP hook asks Wardryx on every request and stamps the verdict on the response. Each decision lands on the bus as a source: wardryx event, which [Idryx](https://it-rat.com/services/idryx.html) correlates into the identity graph.

Boots on `127.0.0.1:8090` with an in-memory store. `serve` refuses to start without `WARDRYX_KEYS`, so `make serve` opts in to the dev key on loopback only: allow-all until you load a policy, and it logs that choice. Then dry-run a policy offline against a directory of Agent Passports:

## A decision is only as good as the identity under it.

This plane answers about an action. What it cannot answer is whether the caller really holds the delegation it claims, which is a different question with a different mechanism: [Vouchryx](https://it-rat.com/services/vouchryx.html) mints a short-lived token bound to the caller's own key and lets a person end it.

## What is open by default, and what is not proven yet.

- When the decision point is unreachable, the TokenFuse gateway closes under enforce when its failure mode is unset, and stays open in shadow mode, where it blocks nothing. The unset default under enforce became closed on 2026-10-17. All three launchers set the failure mode to closed on purpose.

- With no shared database, an approval token's single-use guarantee is per process, and the server says so at startup.

- With no database, the record of accepted DPoP proofs is per process too, and serve says so at start.

- The typed risk signal from Typryx is an opt-in the launchers leave off by default.

### The Wardryx guide

## Putting a human in front of the expensive actions

**Q: How do I require human approval before an agent does something expensive?**
Set a threshold in policy. Above it the answer to the agent is `hold` rather than allow, a human grants or refuses out of band, and the agent resubmits with a signed approval token bound to that agent, run and tool set, and, when the held request named the tool call, to that exact call. The token works once by default. No connection is parked waiting for a signature.

**Q: What answers can the policy plane give?**
Three, and only three: allow, deny, or hold for a human. There is no improvisation and no fourth case, which is what makes the decisions reproducible and arguable after the fact.

**Q: What happens if the policy service is unreachable?**
You choose, per deployment, and the choice is written down. Fail-open treats it as allow, so availability wins and an outage silently disables policy. Fail-closed treats it as deny, so policy wins and an outage blocks every governed action. The shipped launchers choose closed for the gateway, and it was fired on purpose on 2026-09-17: the policy plane stopped, every governed call refused in 0.3 s, none reaching the provider, and the first call after the restart allowed. Started with no policy loaded, Wardryx allows and says so in the log rather than pretending to enforce.

**Q: Can policies be reviewed like code?**
Yes. Budgets, passports and policies are Terraform resources, so they get pull requests, plans and diffs, and an edit made out of band shows up on the next plan instead of quietly persisting.

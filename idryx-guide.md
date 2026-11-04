<!-- https://it-rat.com/idryx-guide.html -->

# Idryx guide

> How Idryx builds one identity graph and what its detectors look for, how to run it, what it answers, and what it does not do or prove yet.

The [Idryx room](https://it-rat.com/services/idryx.html) keeps the simulation, the drawing and the common questions. This guide keeps the rest of what the room used to say: what the graph is made of, what the detectors look for, what it answers, where it sits, how to run it, and its limits.

- [At a glance](https://it-rat.com/idryx-guide.html#overview)

- [How it works](https://it-rat.com/idryx-guide.html#how-it-works)

- [What it answers](https://it-rat.com/idryx-guide.html#what-it-answers)

- [Where it sits](https://it-rat.com/idryx-guide.html#where-it-sits)

- [Running it](https://it-rat.com/idryx-guide.html#run)

- [What changed](https://it-rat.com/idryx-guide.html#changes)

- [What changed in November](https://it-rat.com/idryx-guide.html#changes-november)

- [Limits](https://it-rat.com/idryx-guide.html#limits)

## Idryx at a glance.

- **Every identity on one graph, every unused grant on notice.**

- **Release:** latest · prebuilt binaries. **Core:** Go 1.27 · 27 detectors.

- **Connectors:** Okta · Entra · AWS · GCP · Azure.

- **Output:** CycloneDX 1.6 Agent-BOM.

- **Posture:** read-only, proposes diffs.

- **Licence:** Apache-2.0.

### What it is

Your IdP counts the humans. Nobody counts the keys, the service accounts, or the agents acting on their behalf. Idryx reads what Okta, Entra, AWS, GCP and Azure already log, adds the agent-event bus, stitches all of it into one identity graph with delegation chains and blast radius, and runs 27 deterministic detectors over the result. Read-only by design: it proposes Terraform diffs, it never applies.

## Five identity kinds. One set of answers.

### Sixty seconds, one graph

This is a simulation, but it replays the shape of the live validation run: TokenFuse agent-event NDJSON and Agent Passports land in a Postgres-backed graph, the detectors read the state back, and findings fire. The same three detectors fired against a real Postgres 16 during validation: runaway_agent, attestation_missing, orphaned_nhi. [Watch it in the room](https://it-rat.com/services/idryx.html#sim).

### Sources in. Findings out. Nothing written back.

Read-only connectors for Okta, Entra, AWS, GCP and Azure describe the humans, keys and service accounts; the agent-event bus streams what TokenFuse, Wardryx, Mockryx, Verdryx and Scopyx watched the agents do. One core resolves the graph, walks delegation chains root-first, and runs the 27 detectors. Everything that leaves is an alert, a BOM, a proposed diff a human applies, or an identity_finding event on the bus.

### One graph, every identity

Humans, service accounts, keys, MCP servers and AI agents: five node kinds in one graph, not five tools. Agents are first-class, keyed name@url, with owner, runtime and attestation pinned to the node instead of lost in a generic service-account bucket.

### Delegation chains

on_behalf_of edges record who acts for whom: agent to sub-agent to service account to human. The walk is cycle-safe and resolves root-first, so the question audits stall on for weeks gets answered in one query.

### Five kinds of identity, five kinds of edge, one question answered

Every identity is one of five kinds: a human, a service account, a key, an AI agent, or an MCP server exposing tools. Putting them in one graph is the whole point, because the interesting failures live in the joins, not inside any single directory.

They are connected by a deliberately small set of edges. `on_behalf_of` is the dynamic delegation chain, ordered root first: who this identity is acting for right now. `owner` names the human or team accountable for rotating and revoking it. `has_scope` carries each grant along with whether it is admin-equivalent and whether it has ever been used. `calls_tool` joins an agent to the tools an MCP server exposes, which is how a poisoned tool is traced back to the agent that can call it. And a separate parent edge records the static provisioning relationship, which is an org chart, not an act of delegation, and is kept apart from one.

Resolving those edges is what makes blast radius computable: an identity's reach is the union of every permission along its chain, not the list of grants attached to its own name. That distinction is the difference between a key that looks harmless and a key that reaches admin two hops away.

### 27 deterministic detectors

Statistics and rules over the graph, in four families. The LLM is never in the detection path, so every finding is reproducible and auditable.

### What the 27 detectors look for, and why none of them ask a model

Detection is deterministic: statistics and rules over the graph. The model is an interface for asking questions in English and getting explanations back, and it is never in the detection path, so a finding can be reproduced, argued with and defended in an audit. A baseline engine learns what is normal per identity and stays quiet during its learning period rather than opening a week of false positives on day one.

**Identity threats.** Impossible travel, MFA fatigue, a privileged identity on an unseen device, and logins that deviate from that identity's learned country, device and active hours.

**Non-human identity hygiene.** Service accounts unused past ninety days, non-human identities holding admin-equivalent permissions or no owner at all, and the quiet escalation permissions that grant a path to admin without holding admin: `iam:PassRole` on AWS, `actAs` on GCP, role-assignment writes on Azure. A credential seen from many countries, IPs or devices is flagged for what it usually is: shared or leaked.

**Agents and AI.** An agent that reaches admin through its delegation chain; egress to a known external LLM API; an MCP server in use but missing from the sanctioned registry, and an agent whose declared tools are exposed by that unsanctioned server; a spend runaway correlated with the agent's privilege, delegation depth and blast radius; a privileged agent with no attestation on record; DLP-blocked actions accumulating within a day; a taint-tracked action stopped; an MCP server whose tooling changed under an agent; an agent whose passport declares one set of model providers while its egress reaches another; connections to one destination on a regular cadence (beaconing); a process that names itself an agent identity which no Passport, IAM record or event knows (claimed_agent_unknown), or that reaches an LLM provider its Passport does not declare (claimed_agent_drift); an agent whose Passport binds it to a workload while its only runtime carrier is a process that named itself (claimed_agent_unattested); and an agent whose web egress an enforcement point governs but which opened its own connections to public addresses (unrouted_egress).

**Least privilege.** Permissions granted and never exercised, with a revocation to propose. It fires only where usage data exists, so a source with no observed-usage signal produces no recommendations rather than confident nonsense.

### The Agent-BOM

When the auditor asks what agents you run, the answer is a CycloneDX 1.6 document: owner, runtime, attestation, tools and delegation chain for every agent identity. Its companion detector, bom_incomplete, flags the agents the BOM cannot yet prove.

### Blast radius

What does this key reach, transitively? Idryx computes the union of every permission reachable through an identity's delegation chain. excessive_agency fires when an agent reaches admin-equivalent power through that chain (OWASP LLM06).

### eBPF network sensor

A Linux-only sensor on a kprobe on __sys_connect_file, run on arm64 and x86_64 kernels, captures real outbound connections and flags egress to known LLM APIs. unmanaged_egress fires for identities the sensor is the only evidence of: no IAM record, no passport, just traffic. Pointed at a real agent on an x86_64 box, it labelled every one of the agent's flows with the passport the agent claimed, showed its model calls leaving through the gateway, and caught the one thing that did not: the agent connecting straight to the PyPI package hosts when it started. That was one agent turn on one lab node, on 2026-09-27; it has not yet run on a fleet or a cloud host.

### AI usage: declared, seen, in the code

`idryx ai-inventory` compared its sources provider by provider. It now also says, for each agent or service, what was declared, what was seen and what the code can reach, and it names every disagreement. Nothing in it is scored or ranked, and nothing in it is a detector.

**One row per source.** The report is built from up to five sources: `declared`, `bus`, `egress`, `ebpf` and `code`. A source nobody supplied is a row that says what its absence means. Code not scanned is not nothing in the code, and an absent capture is not a capture that saw nothing.

**One row per subject and provider, with the disagreement named:** `declared_not_seen`, `declared_bus_only`, `seen_not_declared`, `seen_no_declaration`, `declares_no_models` and `no_declaration`, and on provider rows `in_code_not_seen`. The bus names no provider, so an agent active there through an enforcement point is shown as `bus_only`, which is a different statement from not seen: a governed agent's provider connection is made by the gateway's process, where only a capture of that host sees it. A source scan finds a file and a line, and no field binds a repository to an identity, so the code column stays per provider for the whole estate.

It joins on the provider vocabulary `ai-inventory` already used, with no second vocabulary and no change to any shared contract. The JSON document gains `sources` and `subjects`, each provider row gains `gaps`, and the schema string `idryx.ai-inventory/v1` stays. There is no new subcommand and no new flag.

The report agrees with the detectors, and a test holds it. The agents it names `seen_not_declared` are exactly the agents `undeclared_llm` fires for, and the processes it names `seen_no_declaration` are exactly the ones `unmanaged_egress` grades as having reached a model API. The qryx document it reads is untrusted input: its size and the number of providers and labels are bounded, every kept string is escaped and cut, and names from a passport, a bus envelope or a capture are escaped before they reach a terminal. Three monitoring limits travel with every report: attribution is self-declared, the eBPF sensor is Linux-only, and a process with code execution can open a socket of its own.

## Built for the identities that never log in.

Your IdP counts the humans. The keys, service accounts and agents acting on their behalf are what this is built around: an agent is a node kind here, not a field bolted onto a user record. It reads Okta, Entra, AWS, GCP and Azure as sources of truth and proposes changes back as Terraform, never applying them itself.

| Question you ask | What answers it |
|---|---|
| What is acting in my estate, and on whose behalf | One graph of humans, service accounts, keys, agents and MCP servers |
| Who let this agent do that | Delegation chains, resolved root-first to the human at the top |
| What breaks if this credential is taken | Blast radius, computed over the graph |
| What is wrong right now | 27 deterministic detectors, each one named and separately testable |
| What reached an LLM API that nobody provisioned | The eBPF sensor, and unmanaged_egress for identities it is the only evidence of |
| Prove it to an auditor | A CycloneDX Agent-BOM, generated from the graph rather than typed up |
| Change something | It proposes a Terraform diff. Applying it stays your decision |
| Start today | Point it at logs you already keep. Apache-2.0, on hardware you own |

## The one that reads everything and touches nothing.

Idryx consumes the same envelope [TokenFuse](https://it-rat.com/services/tokenfuse.html), [Wardryx](https://it-rat.com/services/wardryx.html), [Mockryx](https://it-rat.com/services/mockryx.html), [Verdryx](https://it-rat.com/services/verdryx.html) and [Scopyx](https://it-rat.com/services/scopyx.html) write: the agent-event. It validates Agent Passports against the [platform contract](https://it-rat.com/services/platform.html), and the loop closes at the policy plane: Wardryx's deny_if_unattested policy refuses an agent with no live attestation, and the gateway answers that refusal with a 403 instead of your production data. Idryx's attestation_missing detector reports those agents in the graph.

Blast radius, shadow tooling and unattested agents are covered as failure modes in [AI agent security](https://it-rat.com/ai-agent-security.html), the graph's place among the planes in [AI agent governance](https://it-rat.com/ai-agent-governance.html), and what an agent identity has to be in [agent identity and authentication](https://it-rat.com/agent-identity.html).

### It records who acts for whom. It does not prove it.

The delegation chain here is a record: each identity lists the on_behalf_of chain it acts under, root first, and the graph walks that chain to show what the identity can reach. [Vouchryx](https://it-rat.com/services/vouchryx.html) is the other half, proof of possession per request and a revocation an incident can actually use, and every finding it produces lands on the same bus this graph is folded from.

## Running it.

```
idryx detect events.ndjson
```

```
idryx serve events.ndjson
```

Download [the latest release binary](https://github.com/TAIPANBOX/idryx/releases) (SHA256SUMS ships next to it), run detect against a log, then serve for the read-only dashboard on `:8080`.

### idryx, every platform

Every one of those addresses always serves the newest release, so a link saved today still works after the next one. The asset names carry no version, which is what makes that true; the version lives inside the binary, where `idryx version` reads it back.

## What changed.

Idryx's releases from 1 to 15 October 2026 are listed in [the October changelog](https://it-rat.com/changes-2026-10.html#idryx), beside the rest of the stack's.

## What changed in November

| shipped in | what it does |
|---|---|
| v1.4.0 | idryx ai-inventory reports, for each agent or service, what was declared, what was seen and what the code can reach, and names every disagreement. Additive to the idryx.ai-inventory/v1 schema. |

## What it does not do, and what is not proven yet.

- **Read-only by design:** it proposes Terraform diffs, it never applies. Applying a diff stays your decision.

- The delegation chain here is a record. Proof of possession per request, and a revocation an incident can use, are [Vouchryx](https://it-rat.com/services/vouchryx.html)'s half.

- A baseline engine learns what is normal per identity and stays quiet during its learning period rather than opening a week of false positives on day one.

- Least privilege fires only where usage data exists, so a source with no observed-usage signal produces no recommendations rather than confident nonsense.

- The companion detector bom_incomplete flags the agents the BOM cannot yet prove.

- The eBPF network sensor is Linux-only. It has attached and captured live flows on two kernels: a Docker Desktop Linux VM on a Mac (2026-09-08, arm64 kernel 7.0.12; a 12-second capture in a container, not against an agent: 3 flows on the fixed build, after 16 of the first run's 21 flows turned out to be the sensor's own traffic) and one x86_64 lab node (2026-09-27, one agent turn, 349 flows in 70 seconds). It has not yet run on a fleet or a cloud host.

- The bus carries a model only in `call_retained`, which the AI usage report does not read, so it compares no model names with anything: the egress side names a host, never a model. Whether an identity has a declaration is read from its source or from a declared model or attestation, which is a reading of the graph and not an attested fact.

- The room's runaway is a simulation, but it replays the shape of the live validation run.

## Back to the room.

The [Idryx room](https://it-rat.com/services/idryx.html) has the simulation, the drawing and the common questions, and [the guides index](https://it-rat.com/guides.html) has the field itself.

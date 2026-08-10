<!-- https://it-rat.com/services/idryx.html -->

# Idryx, the access plane

> One identity graph for humans, keys, service accounts and AI agents: delegation chains, blast radius, 22 deterministic detectors and a CycloneDX Agent-BOM.

Your IdP counts the humans. Nobody counts the keys, the service accounts, or the agents acting on their behalf. Idryx reads what Okta, Entra, AWS, GCP and Azure already log, adds the agent-event bus, stitches all of it into one identity graph with delegation chains and blast radius, and runs 22 deterministic detectors over the result. Read-only by design: it proposes Terraform diffs, it never applies.

## Watch the graph catch a runaway.

This is a simulation, but it replays the shape of the live validation run: TokenFuse agent-event NDJSON and Agent Passports land in a Postgres-backed graph, the detectors read the state back, and findings fire. The same three detectors fired against a real Postgres 16 during validation: runaway_agent, attestation_missing, orphaned_nhi.

## Sources in. Findings out. Nothing written back.

Five read-only connectors describe the humans, keys and service accounts; the agent-event bus streams what TokenFuse, Wardryx, Mockryx and Verdryx watched the agents do. One core resolves the graph, walks delegation chains root-first, and runs the 25 detectors. Everything that leaves is an alert, a BOM, or a proposed diff a human applies.

## Five identity kinds. One set of answers.

### One graph, every identity

Humans, service accounts, keys, MCP servers and AI agents: five node kinds in one graph, not five tools. Agents are first-class, keyed name@url, with owner, runtime and attestation pinned to the node instead of lost in a generic service-account bucket.

### Delegation chains

on_behalf_of edges record who acts for whom: agent to sub-agent to service account to human. The walk is cycle-safe and resolves root-first, so the question audits stall on for weeks gets answered in one query.

**Q: What the graph is made of**

Every identity is one of five kinds: a human, a service account, a key, an AI agent, or an MCP server exposing tools. Putting them in one graph is the whole point, because the interesting failures live in the joins, not inside any single directory.

They are connected by a deliberately small set of edges. `on_behalf_of` is the dynamic delegation chain, ordered root first: who this identity is acting for right now. `owner` names the human or team accountable for rotating and revoking it. `has_scope` carries each grant along with whether it is admin-equivalent and whether it has ever been used. `calls_tool` joins an agent to the tools an MCP server exposes, which is how a poisoned tool is traced back to the agent that can call it. And a separate parent edge records the static provisioning relationship, which is an org chart, not an act of delegation, and is kept apart from one.

Resolving those edges is what makes blast radius computable: an identity's reach is the union of every permission along its chain, not the list of grants attached to its own name. That distinction is the difference between a key that looks harmless and a key that reaches admin two hops away.

### 22 deterministic detectors

Statistics and rules over the graph, in four families. The LLM is never in the detection path, so every finding is reproducible and auditable.

**Q: What they look for**

Detection is deterministic: statistics and rules over the graph. The model is an interface for asking questions in English and getting explanations back, and it is never in the detection path, so a finding can be reproduced, argued with and defended in an audit. A baseline engine learns what is normal per identity and stays quiet during its learning period rather than opening a week of false positives on day one.

**Identity threats.** Impossible travel, MFA fatigue, a privileged identity on an unseen device, and logins that deviate from that identity's learned country, device and active hours.

**Non-human identity hygiene.** Service accounts unused past ninety days, non-human identities holding admin-equivalent permissions or no owner at all, and the quiet escalation permissions that grant a path to admin without holding admin: `iam:PassRole` on AWS, `actAs` on GCP, role-assignment writes on Azure. A credential seen from many countries, IPs or devices is flagged for what it usually is: shared or leaked.

**Agents and AI.** An agent that reaches admin through its delegation chain; egress to an LLM API nobody registered; an MCP server in use but missing from the sanctioned registry, and an agent whose declared tools are exposed by that unsanctioned server; a spend runaway correlated with the agent's privilege, delegation depth and blast radius; a privileged agent with no attestation on record; DLP-blocked actions accumulating within a day; a taint-tracked action stopped; an MCP server whose tooling changed under an agent; and an agent whose passport declares one set of model providers while its egress reaches another.

**Least privilege.** Permissions granted and never exercised, with a revocation to propose. It fires only where usage data exists, so a source with no observed-usage signal produces no recommendations rather than confident nonsense.

### The Agent-BOM

When the auditor asks what agents you run, the answer is a CycloneDX 1.6 document: owner, runtime, attestation, tools and delegation chain for every agent identity. Its companion detector, bom_incomplete, flags the agents the BOM cannot yet prove.

### Blast radius

What does this key reach, transitively? Idryx computes the union of every permission reachable through an identity's delegation chain. excessive_agency fires when an agent reaches admin-equivalent power through that chain (OWASP LLM06).

### eBPF network sensor

A Linux-only sensor on the sys_enter_connect tracepoint captures real outbound connections and flags egress to known LLM APIs. unmanaged_egress fires for identities the sensor is the only evidence of: no IAM record, no passport, just traffic.

## Built for the identities that never log in.

SailPoint and CyberArk are serious IGA products for the identities they were built around: employees with logins. Idryx does not replace them, and it reads Okta and Entra as sources of truth. The difference is who gets first-class treatment: the keys, service accounts and agents that never log in at all.

|  | Idryx | IGA suites | Spreadsheets + scripts |
|---|---|---|---|
| Covers AI agents natively | Yes: agents are a node kind | Bolted on | No |
| Time to first insight | Minutes: point it at logs | Quarters of rollout | Weeks of grep |
| Enforcement stance | Read-only, proposes diffs | Heavy write access | Manual |
| Delegation chains for agents | First-class, root-first | Rare | No |
| Evidence output | CycloneDX Agent-BOM | Proprietary reports | None |
| Price | Apache-2.0 | Six figures | Your weekends |

### The one that reads everything and touches nothing.

Idryx consumes the same envelope [TokenFuse](https://it-rat.com/tokenfuse.html), [Wardryx](https://it-rat.com/wardryx.html), [Mockryx](https://it-rat.com/mockryx.html) and [Verdryx](https://it-rat.com/verdryx.html) write: the agent-event. It validates Agent Passports against the [platform contract](https://it-rat.com/platform.html), and the loop closes at the policy plane: its attestation_missing detector is the reason an unattested agent meets a 403 from Wardryx policies instead of your production data.

Blast radius, shadow tooling and unattested agents are covered as failure modes in [AI agent security](https://it-rat.com/ai-agent-security.html), the graph's place among the planes in [AI agent governance](https://it-rat.com/ai-agent-governance.html), and what an agent identity has to be in [agent identity and authentication](https://it-rat.com/agent-identity.html).

Download a [v0.2.0 release binary](https://github.com/TAIPANBOX/idryx/releases) (SHA256SUMS ships next to it), run detect against a log, then serve for the read-only dashboard on `:8080`.

## Counting the identities nobody is counting

**Q: How do I find every AI agent and service account we actually have?**
Idryx reads what Okta, Entra, AWS, GCP and Azure already log, adds the agent-event bus the rest of the stack writes, and stitches all of it into one graph of humans, service accounts, keys, agents and MCP servers. The answer comes from the graph, not from a spreadsheet someone maintained until they left.

**Q: Will it change anything in my cloud?**
No. It is read-only by design: connectors read, and the output is an alert, a bill of materials, or a Terraform diff a human applies. It never writes back.

**Q: What is an Agent-BOM?**
A CycloneDX 1.6 bill of materials for your agents: who owns each one, what runtime it runs on, what it is attested by, and what it can reach. It plugs into the same supply-chain tooling that already ingests your SBOMs.

**Q: What does it actually detect?**
Twenty-two deterministic detectors in four families: identity threats, non-human identity hygiene, agents and AI, and least privilege. Detection is statistics and rules over the graph; the model is never in the detection path, so every finding is reproducible and defensible in an audit.

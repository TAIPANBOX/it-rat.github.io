<!-- https://it-rat.com/services/idryx.html -->

# Idryx, the access plane

> One identity graph for humans, keys, service accounts and AI agents: delegation chains, blast radius, 27 deterministic detectors and a CycloneDX Agent-BOM.

Idryx reads what Okta, Entra, AWS, GCP and Azure already log, adds the agent-event bus, stitches all of it into one identity graph with delegation chains and blast radius, and runs 27 deterministic detectors over the result. Read-only by design: it proposes Terraform diffs, it never applies.

## Watch the graph catch a runaway.

A replay of the live validation run: TokenFuse agent-events and Agent Passports land in the graph, the detectors read it back, and findings fire.

## Sources in. Findings out. Nothing written back.

Read-only connectors for Okta, Entra, AWS, GCP and Azure describe the humans, keys and service accounts; the agent-event bus streams what TokenFuse, Wardryx, Mockryx, Verdryx and Scopyx watched the agents do. Everything that leaves is an alert, a BOM, a proposed diff a human applies, or an identity_finding event on the bus.

## Five identity kinds. One set of answers.

### One graph, every identity

Humans, service accounts, keys, MCP servers and AI agents: five node kinds in one graph, not five tools.

### Delegation chains

on_behalf_of edges record who acts for whom: agent to sub-agent to service account to human. The walk is cycle-safe and resolves root-first.

### 27 deterministic detectors

Statistics and rules over the graph, in four families. The LLM is never in the detection path, so every finding is reproducible and auditable.

### Blast radius

What does this key reach, transitively? Idryx computes the union of every permission reachable through an identity's delegation chain.

### Declared, seen, in the code

idryx ai-inventory now says, for each agent or service, what was declared, what was seen and what the code can reach, and it names every disagreement. It is a report: nothing in it is scored, ranked or a detector.

### The one that reads everything and touches nothing.

Idryx consumes the same envelope [TokenFuse](https://it-rat.com/services/tokenfuse.html), [Wardryx](https://it-rat.com/services/wardryx.html), [Mockryx](https://it-rat.com/services/mockryx.html), [Verdryx](https://it-rat.com/services/verdryx.html) and [Scopyx](https://it-rat.com/services/scopyx.html) write: the agent-event. It validates Agent Passports against the [platform contract](https://it-rat.com/services/platform.html).

Download [the latest release binary](https://github.com/TAIPANBOX/idryx/releases) (SHA256SUMS ships next to it), run detect against a log, then serve for the read-only dashboard on `127.0.0.1:8080`, loopback only by default.

## It records who acts for whom. It does not prove it.

The delegation chain here is a record. Vouchryx is the other half: proof of possession per request and a revocation an incident can use.

## What it does not do, in short.

### Quiet while it learns

A baseline engine learns what is normal per identity and stays quiet during its learning period.

### No usage, no advice

Least privilege fires only where usage data exists, so a source with no usage signal gets no recommendation.

### The eBPF sensor is Linux-only

It has captured live flows on two kernels: a Docker VM on a Mac and an x86_64 lab node.

### The Idryx guide

## Counting the identities nobody is counting

**Q: How do I find every AI agent and service account we actually have?**
Idryx reads what Okta, Entra, AWS, GCP and Azure already log, adds the agent-event bus the rest of the stack writes, and stitches all of it into one graph of humans, service accounts, keys, agents and MCP servers. The answer comes from the graph, not from a spreadsheet someone maintained until they left.

**Q: Will it change anything in my cloud?**
No. It is read-only by design: connectors read, and the output is an alert, a bill of materials, or a Terraform diff a human applies. It never writes back.

**Q: What is an Agent-BOM?**
A CycloneDX 1.6 bill of materials for your agents: who owns each one, what runtime it runs on, what it is attested by, and what it can reach. It plugs into the same supply-chain tooling that already ingests your SBOMs.

**Q: What does it actually detect?**
Twenty-seven deterministic detectors in four families: identity threats, non-human identity hygiene, agents and AI, and least privilege. Detection is statistics and rules over the graph; the model is never in the detection path, so every finding is reproducible and defensible in an audit.

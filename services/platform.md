<!-- https://it-rat.com/services/platform.html -->

# Platform, the shared contract

> One agent:// passport, one event envelope, one Go binding and a Terraform provider: the contract every service in the stack shares. Apache-2.0.

Under the services sits a three-repo platform. agent-passport is the spec: one agent:// identifier, one Passport document, one event envelope. agent-stack-go is the Go binding, with the agent-conform checker. terraform-provider-taipan turns budgets, passports and policies into PR-reviewed code.

## One envelope, end to end.

This is a simulation, labeled as one: a replay of the envelope's normal day. A passport is issued, the planes emit their own event types into one NDJSON stream, two schema versions ride side by side, and agent-conform validates the whole stream at the end.

## Everything meets at the envelope.

Fifteen registered sources write one shape: twelve onto one NDJSON bus, and heraldyx, scopyx and the keyryx witness into files of their own (dashed). Five required fields, six optional ones. On the right, the part your platform team owns: budgets, passports and policies as Terraform resources.

## Boring on purpose. Load-bearing anyway.

### The passport

One agent, one URI: agent://trust-domain/path, at most 255 bytes, aligned with SPIFFE without requiring it. The document behind the ID names an owner, a runtime and one of six attestation methods.

### The envelope

Five required fields: schema, ts, source, type, agent_id. Event types live in a per-source registry, so tokenfuse can add a type without asking engram.

### agent-conform

A standalone conformance CLI with the canonical JSON Schemas embedded. Files are classified by their own schema field, and unrecognized content is a FAIL, never silently skipped.

### Governance as code

Four Terraform resources: taipan_budget, taipan_unit_budget, taipan_agent_passport, taipan_wardryx_policy. Run budgets, business-unit budgets, passports and policies get PRs, plans and diffs like everything else.

## Run the live stack locally.

Two ways in, and they are for different machines.

## The stack is a control plane. Your agents can be anywhere.

Nothing here has to sit next to the agents it governs. That is the whole deployment question: where the control plane lives, not where the work does.

## One contract, shared by every service.

Every event carries one agent_id and an explicit schema field. Anyone can implement the contract; it is Apache-2.0.

### The layer every other page stands on.

Every other page on this site is a producer or a consumer of this contract. [Engram](https://it-rat.com/services/engram.html) writes memory_written and reflection_run into the same stream, and [Idryx](https://it-rat.com/services/idryx.html) reads everything back into one identity graph, checking passports with the same passport.Parse this platform ships.

This installs nothing of the stack: it is the contract itself, for an agent of your own.

## Small claims, kept.

- The passport is metadata, not a token, and the spec is not an authentication protocol.

- The laptop sandbox is for trying the stack, not a production deployment: it binds loopback only, so nothing on it is reachable by an agent on another machine.

- Where the API has no delete, the Terraform provider says so instead of pretending.

### The Platform guide

## The contract every service agrees on

**Q: What is an Agent Passport?**
One identifier and one document per agent: an `agent://` URI of at most 255 bytes, aligned with SPIFFE without requiring it, and a document naming an owner, a runtime and one of six attestation methods. The delegation chain behind it is ordered root first, acyclic, and capped at 32 entries.

**Q: Do I have to adopt the whole stack to use the contract?**
No. There is no shared runtime and no shared database. Adopting it is a naming agreement plus a few optional fields on events you already emit, which is why a service can add an event type without asking any other service for permission.

**Q: Can budgets and policies live in version control?**
Yes. Four Terraform resources cover run budgets, business-unit budgets, agent passports and policies, published on the public Terraform Registry, so governance gets pull requests, plans and diffs like the rest of your infrastructure. Where the API has no delete, the provider says so instead of pretending.

**Q: How do I check that my events actually conform?**
Run `agent-conform`. It carries the canonical JSON Schemas, classifies each file by its own schema field, treats unrecognised content as a failure rather than skipping it quietly, and exits 0 or 1. It has already caught a real 63-versus-64 character hash defect. On a box, `agent-conform watch-dir` re-checks every stream's hash chain and writes a `chain_broken`, `chain_unchained` or `chain_restarted` event to its own stream when one breaks; it exits 2 on a usage or I/O error. stack-single runs it every five minutes and stack-k8s runs it as a CronJob every fifteen minutes. stack-up runs it once a day, at 06:52, as a routine.

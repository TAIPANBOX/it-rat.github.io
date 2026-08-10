<!-- https://it-rat.com/services/platform.html -->

# Platform, the shared contract

> One agent:// passport, one event envelope, one Go binding and a Terraform provider: the shared contract under all seven services of the stack. Apache-2.0.

Under the seven services sits a three-repo platform. agent-passport is the spec: one agent:// identifier, one Passport document, one event envelope. agent-stack-go is the Go binding, with the agent-conform checker. terraform-provider-taipan turns budgets, passports and policies into PR-reviewed code. No shared runtime, no shared database; adopting it is a naming agreement plus a few optional fields.

## One envelope, end to end.

This is a simulation, labeled as one: a replay of the envelope's normal day. A passport is issued, seven services emit their own event types into one NDJSON stream, two schema versions ride side by side, and agent-conform validates the whole stream at the end. Exit 0.

## Everything meets at the envelope.

Seven emitters write one shape onto one NDJSON bus: five required fields, five optional ones. Four consumers read it back: the agent-conform CLI validates against embedded copies of the canonical JSON Schemas, Idryx folds events into the identity graph, TokenFuse Cloud files them into evidence packs, and Heraldyx mails the operator about the few worth interrupting them for. On the right, the part your platform team owns: budgets, passports and policies as Terraform resources.

## Boring on purpose. Load-bearing anyway.

### The passport

One agent, one URI: agent://trust-domain/path, at most 255 bytes, aligned with SPIFFE without requiring it. The document behind the ID names an owner, a runtime and one of five attestation methods. The delegation chain is ordered root first, acyclic, and capped at 32 entries.

### The envelope

Five required fields: schema, ts, source, type, agent_id. Two versions coexist by design: v0.1 with a closed source enum, v0.2 with an open string. Event types live in a per-source registry, so tokenfuse can add a type without asking engram.

### The Go binding

agent-stack-go ships passport.Parse, an append-only event.Writer and chain.Validate, stdlib only at runtime. It is the same validation Idryx runs on ingest: a passport that parses in your pipeline parses in the graph.

### agent-conform

A standalone conformance CLI with the canonical JSON Schemas embedded. Files are classified by their own schema field, and unrecognized content is a FAIL, never silently skipped. Exit 0 or exit 1; it has already caught a real 63-versus-64 hex character prev_hash defect.

### Governance as code

Three Terraform resources: taipan_budget, taipan_agent_passport, taipan_wardryx_policy. Budgets and policies get PRs, plans and diffs like everything else, and edits made out of band surface on the next plan. Where the API has no delete, the provider says so instead of pretending.

### Honest scope

The provider is published on the Terraform Registry as `TAIPANBOX/taipan`: a normal `required_providers` block and `terraform init` pull it, GPG-verified, no build-from-source needed. The passport is metadata, not a token, and the spec is not an authentication protocol. Small claims, kept.

## Run the live stack locally.

One command builds the stack's long-running services from source, starts them on a fixed loopback port map, and prints a one-click link to your own money plane. No Docker, no account, nothing leaves your machine.

The first run builds tokenfuse in release mode and takes a few minutes; after that startup is seconds.

**Q: What the first run does**

Open the link it prints and you are looking at your own local money plane, live, with a short demo dataset already in it. Point an agent's OpenAI base URL at the gateway to feed it your own.

It builds and starts the stack's long-running services from source: TokenFuse's gateway, cloud and dashboard, plus Wardryx and Idryx. Engram, Qryx, Verdryx and Mockryx are deliberately not servers, they are libraries and one-shot CLIs, each with its own one-line try-it on its page.

Press Ctrl-C and it stops clean, with no orphaned processes.

git, Rust, Node and Python; Go adds the policy and identity planes. macOS or Linux. A sandbox to try the stack, not a production deployment.

## The stack is a control plane. Your agents can be anywhere.

Nothing here has to sit next to the agents it governs. An agent points its model endpoint at the gateway and asks the policy plane before it acts, so it can run in EKS, in GKE, in a CI job or on a laptop while the stack runs once, on infrastructure you own. That is the whole deployment question: where the control plane lives, not where the work does.

The shape the stack is actually built for: the planes share a filesystem, which is how they talk. One script puts all of it on a box you own, and it comes up closed.

**Q: Commands and what it verifies**

It comes up closed: the gateway lands on the host's loopback and everything else has no host port at all, so a box that just ran an install script is not serving an enforcement plane to the internet because nobody typed anything. One variable publishes the gateway when you mean to. Same images and same service names as the cluster deployment, because Docker resolves `http://wardryx:8090` exactly the way a Kubernetes Service did.

[The sandbox above](https://it-rat.com/#run) is this shape already, with one deliberate difference: it binds loopback only, so nothing on it is reachable by an agent on another machine. That is correct for trying it and wrong for serving a fleet.

It also brings up a WireGuard server for the people who run the box, so the console is reached over a tunnel it issues rather than an SSH forward you keep alive by hand. That is the one port here published on purpose: WireGuard answers nothing at all without a valid key, unlike an HTTP plane.

It ends by verifying itself, and two of its checks have to FAIL to pass: the money plane and the policy plane must not answer on the host. Three more test the credential rather than the port, because a plane with a malformed key spec starts cleanly, stays reachable, and authenticates nobody. One more reads back the rule Docker actually wrote for port 4100 instead of trusting the variable meant to set it, because a default that says loopback while the port says otherwise is worse than no default at all.

For teams whose answer to everything is a cluster. One script brings up k3s across your nodes with the CNI, storage and hardening the stack actually needs, then the workload applies from plain manifests.

**Q: Commands and the trade**

Both paths are one command, and both ask what they need before the long part rather than failing on it afterwards. So the trade is not convenience. Kubernetes buys high availability and costs you the one thing a single box gets for free: the planes couple through a shared event log, so a cluster needs a ReadWriteMany volume for it.

That trade, and seventy-eight other things that bite, are documented in the repositories rather than discovered by you. The same manifests came up on six clusters across Hetzner, AWS and GCP, and exactly one line of Kubernetes configuration differs between the three: Calico has to encapsulate unconditionally on GCP, because a GCE VPC routes every packet by destination and a pod address matches no route. Every trap we hit is written down and already fixed in the files.

## Two default futures, one contract.

Without a shared contract you get one of two outcomes: every tool logs its own JSON, or one vendor's schema becomes the standard and you rent it. Here is the matrix.

|  | the contract | “every tool logs its own JSON” | a vendor's proprietary schema |
|---|---|---|---|
| Cross-tool correlation | One agent_id everywhere | grep and hope | Inside one vendor only |
| Versioning | Explicit schema field; v0.1 and v0.2 coexist | None | The vendor's roadmap |
| Validation | JSON Schema + a conformance CLI | None | Closed |
| Who can implement it | Anyone; Apache-2.0 | n/a | Licensees |

### The layer every other page stands on.

Every other page on this site is a producer or a consumer of this contract. [TokenFuse](https://it-rat.com/tokenfuse.html) pushes its incident taxonomy through the envelope verbatim, zero renaming. [Wardryx](https://it-rat.com/wardryx.html) answers policy_deny in schema v0.2. [Engram](https://it-rat.com/engram.html) writes memory_written and reflection_run into the same stream, and [Idryx](https://it-rat.com/idryx.html) reads everything back into one identity graph, checking passports with the same passport.Parse this platform ships. Different rooms, one grammar.

What the contract is for, in practice: [AI agent governance](https://it-rat.com/ai-agent-governance.html) and the controls it lets seven tools share.

This installs nothing of the stack: it is the contract itself, for an agent of your own. Exit 0 means every file and every NDJSON line conforms; exit 1 means at least one did not. That is the whole interface.

**Q: Download, any platform**

Every one of those addresses always serves the newest release, so a link saved today still works after the next one. The asset names carry no version, which is what makes that true; the version lives inside the binary, where `agent-conform -version` reads it back.

## The contract seven services agree on

**Q: What is an Agent Passport?**
One identifier and one document per agent: an `agent://` URI of at most 255 bytes, aligned with SPIFFE without requiring it, and a document naming an owner, a runtime and one of five attestation methods. The delegation chain behind it is ordered root first, acyclic, and capped at 32 entries.

**Q: Do I have to adopt the whole stack to use the contract?**
No. There is no shared runtime and no shared database. Adopting it is a naming agreement plus a few optional fields on events you already emit, which is why a service can add an event type without asking any other service for permission.

**Q: Can budgets and policies live in version control?**
Yes. Three Terraform resources cover budgets, agent passports and policies, published on the public Terraform Registry, so governance gets pull requests, plans and diffs like the rest of your infrastructure. Where the API has no delete, the provider says so instead of pretending.

**Q: How do I check that my events actually conform?**
Run `agent-conform`. It carries the canonical JSON Schemas, classifies each file by its own schema field, treats unrecognised content as a failure rather than skipping it quietly, and exits 0 or 1. It has already caught a real 63-versus-64 character hash defect.

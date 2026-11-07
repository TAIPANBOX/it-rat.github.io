<!-- https://it-rat.com/platform-guide.html -->

# Platform guide

> How the Agent Passport contract works, how to run the stack on a laptop, one box or a cluster, and what it does not claim, in full.

The [Platform room](https://it-rat.com/services/platform.html) keeps the simulation, the drawing of the envelope and the common questions. This guide keeps the rest of what the room used to say: what the contract pins down, the full text for running the stack on a laptop, on one box or on a cluster, the downloads, and what the contract does not claim.

- [At a glance](https://it-rat.com/platform-guide.html#overview)

- [How it works](https://it-rat.com/platform-guide.html#how-it-works)

- [Running it](https://it-rat.com/platform-guide.html#run)

- [On your own infrastructure](https://it-rat.com/platform-guide.html#deploy)

- [The contract for your own agent](https://it-rat.com/platform-guide.html#try-it)

- [Where it sits](https://it-rat.com/platform-guide.html#where-it-sits)

- [What changed](https://it-rat.com/platform-guide.html#changes)

- [Limits](https://it-rat.com/platform-guide.html#limits)

## The contract at a glance.

- **The boring layer that makes a dozen services one system:** a three-repo platform under the services.

- **Passport schema:** v0.1 and v1.0, stable. **Event envelope:** v0.1 to v1.0, NDJSON.

- **Go binding:** agent-stack-go, latest.

- **Conformance:** agent-conform, for files and as a chain watcher.

- **As code:** taipan_budget, taipan_unit_budget, taipan_agent_passport, taipan_wardryx_policy.

- **Licence:** Apache-2.0.

### What it is

Under the services sits a three-repo platform. agent-passport is the spec: one agent:// identifier, one Passport document, one event envelope. agent-stack-go is the Go binding, with the agent-conform checker. terraform-provider-taipan turns budgets, passports and policies into PR-reviewed code. No shared runtime, no shared database; adopting it is a naming agreement plus a few optional fields.

## Boring on purpose. Load-bearing anyway.

### One envelope, end to end.

The room's simulation is labeled as one: a replay of the envelope's normal day. A passport is issued, the planes emit their own event types into one NDJSON stream, two schema versions ride side by side, and agent-conform validates the whole stream at the end. Exit 0.

### Everything meets at the envelope.

Fifteen registered sources write one shape: twelve onto one NDJSON bus, and heraldyx, scopyx and the keyryx witness into files of their own (dashed). Five required fields, six optional ones. Five consumers read it back: the agent-conform CLI validates against embedded copies of the canonical JSON Schemas and, on the box, re-checks every stream's hash chain and writes what it finds to a stream of its own, which is how it is also one of the fifteen sources; Idryx folds events into the identity graph, TokenFuse Cloud files them into evidence packs, Heraldyx mails the operator about the few worth interrupting them for, and Trailryx seals the stream into a hash-chained record. The keyryx witness also reads every stream; its findings go to a file of their own, off the bus, which Heraldyx mails and the Genaryx console shows as incidents through a read-only mount. On the right, the part your platform team owns: budgets, passports and policies as Terraform resources.

### The passport

One agent, one URI: agent://trust-domain/path, at most 255 bytes, aligned with SPIFFE without requiring it. The document behind the ID names an owner, a runtime and one of six attestation methods. The delegation chain is ordered root first, acyclic, and capped at 32 entries.

### The envelope

Five required fields: schema, ts, source, type, agent_id. Four versions stay live by design: v0.1 with a closed source enum, v0.2 with an open string, v0.3 adding a self-declared, claimed agent_id, and v1.0, which is v0.3's shape under the 1.0 compatibility promise. The passport document has two, v0.1 and v1.0. Event types live in a per-source registry, so tokenfuse can add a type without asking engram.

### The Go binding

agent-stack-go ships four packages: passport, event, chain and delegation (the RFC 8693 delegation token and offline verification of an agent's own access token). It ships passport.Parse, an append-only event.Writer and chain.Validate. passport and chain need only the standard library; event adds one dependency, gowebpki/jcs, for the RFC 8785 canonical JSON its hash chain is computed over. Since v2.0.0 the module path is github.com/TAIPANBOX/agent-stack-go/v2, and a stream file is created with mode 0640. It is the same validation Idryx runs on ingest: a passport that parses in your pipeline parses in the graph.

### agent-conform

A standalone conformance CLI with the canonical JSON Schemas embedded. Files are classified by their own schema field, and unrecognized content is a FAIL, never silently skipped. Exit 0 or exit 1; it has already caught a real 63-versus-64 hex character prev_hash defect. Since agent-stack-go v1.1.0 it also runs on the box as `watch-dir`: it re-checks every stream's hash chain and writes `chain_broken` (high), `chain_unchained` (low) or `chain_restarted` (medium, or high when no signed resume checkpoint explains it) to its own stream; with `-checkpoints` and `-checkpoint-keys` it also checks each stream's signed checkpoint. It exits 2 on a usage or I/O error. It ships as a signed, distroless image, `ghcr.io/taipanbox/agent-conform`, and runs by default every five minutes on the single box and every fifteen on a cluster.

### Governance as code

Four Terraform resources: taipan_budget, taipan_unit_budget, taipan_agent_passport, taipan_wardryx_policy. Run budgets, business-unit budgets, passports and policies get PRs, plans and diffs like everything else, and edits made out of band surface on the next plan. Where the API has no delete, the provider says so instead of pretending.

### Honest scope

The provider is published on the Terraform Registry as `TAIPANBOX/taipan`: a normal `required_providers` block and `terraform init` pull it, GPG-verified, no build-from-source needed. The passport is metadata, not a token, and the spec is not an authentication protocol. Small claims, kept.

### One contract, shared by every service.

Every event carries one agent_id and an explicit schema field. The canonical JSON Schemas ship with agent-conform, which checks a file against them. Anyone can implement the contract; it is Apache-2.0.

## Run the live stack locally.

Two ways in, and they are for different machines. On your own laptop the sandbox builds from source and binds loopback only. On a Linux box you own, one line pulls the published images and the whole governed stack is up in under two minutes.

### On a box you own, fastest

```
curl -fsSL https://raw.githubusercontent.com/TAIPANBOX/stack-single/main/install.sh | bash
```

Nothing is compiled: every plane is pulled from the public registry at a pinned version. Measured on 2026-09-13 on a fresh 2-vCPU cloud machine, from that line to a console answering on loopback: **109 seconds**, with every one of the installer's own checks green; on 2026-09-17, on a mini PC that already had Docker, **61 seconds** for the first run (exit 1: 22 checks ok, and one that fails by construction, since it probed loopback whatever the bind address was; fixed by stack-single #59) and 36 seconds for the second, with the same 22 checks ok. It needs root on Debian or Ubuntu, and docker and git; it comes back after a reboot (measured once, on 2026-09-17, on a box whose gateway sat on a tailnet address: the first reboot lost the gateway until the installer learned to order Docker after the tunnel, the second brought it back on its own); and it is reachable by agents running anywhere else, which the same day proved from two clouds at once.

### On your laptop, no Docker

```
git clone https://github.com/TAIPANBOX/stack-up
cd stack-up && ./up.sh
```

The sandbox, and it builds from source on purpose: nothing but your own compilers touches it. That is the cost as well as the point, so it wants Rust, Go, Node and Python already installed. Measured on 2026-09-01 from an empty build cache: **221 seconds** to a working dashboard. A cold run with both optional planes took **325 seconds** on 2026-09-13. Binds `127.0.0.1` only, stops on Ctrl-C, keeps nothing.

### What the first run actually does

Open the link it prints and you are looking at your own local money plane, live, with a short demo dataset already in it. Point an agent's OpenAI base URL at the gateway to feed it your own.

It builds and starts the stack's long-running services from source. Those are TokenFuse's gateway, cloud and dashboard, plus Wardryx, Idryx and Scopyx, and Keyryx (custody and witness): eight ports on loopback, as the stack-up README's port table lists them. Heraldyx is pinned to file mode there, writing what it would have mailed rather than mailing it. Trailryx is built and wired as a sealing routine rather than a port. Engram, Qryx, Verdryx and Mockryx are deliberately not servers: they are libraries and one-shot CLIs, installed into your home directory and started when you want them, each with its own try-it on its page. The delegation plane, the FinOps console and the typed-answers service stay behind a flag, `--with-delegation`, `--with-finops` and `--with-typed`, because one needs an issuer to trust, one is a different product and one is optional.

Press Ctrl-C and it stops clean, with no orphaned processes.

### What comes up

| gateway | :4100 · budgets |
|---|---|
| cloud + dashboard | :8080 · :3000 |
| wardryx | :8090 · policy |
| idryx | :8081 · identity |
| every bind | 127.0.0.1 only |

git, Rust, Node and Python; Go adds the policy and identity planes. macOS or Linux. A sandbox to try the stack, not a production deployment.

## The stack is a control plane. Your agents can be anywhere.

Nothing here has to sit next to the agents it governs. An agent points its model endpoint at the gateway and asks the policy plane before it acts, so it can run in EKS, in GKE, in a CI job or on a laptop while the stack runs once, on infrastructure you own. That is the whole deployment question: where the control plane lives, not where the work does.

### One box

The shape the stack is actually built for: the planes share a filesystem, which is how they talk. One script puts all of it on a box you own, and it comes up closed.

| install | one script |
|---|---|
| gateway | host loopback, published only on purpose |
| every other plane | no host port at all |
| the console | over WireGuard the box issues |
| images | the same as the cluster path |

**The commands, and the checks that have to fail to pass.**

```
git clone https://github.com/TAIPANBOX/stack-single
cd stack-single && ./install.sh
GATEWAY_BIND=0.0.0.0 ./install.sh
ANTHROPIC_BASE_URL=http://<your box>:4100
```

It comes up closed: the gateway lands on the host's loopback and everything else has no host port at all, so a box that just ran an install script is not serving an enforcement plane to the internet because nobody typed anything. One variable publishes the gateway when you mean to. Same images and same service names as the cluster deployment, because Docker resolves `http://wardryx:8090` exactly the way a Kubernetes Service did.

[The sandbox above](https://it-rat.com/platform-guide.html#run) is this shape already, with one deliberate difference: it binds loopback only, so nothing on it is reachable by an agent on another machine. That is correct for trying it and wrong for serving a fleet.

It also brings up a WireGuard server for the people who run the box, so the console is reached over a tunnel it issues rather than an SSH forward you keep alive by hand. That is the one port here published on purpose: WireGuard answers nothing at all without a valid key, unlike an HTTP plane.

It ends by verifying itself, and three of its checks have to FAIL to pass: the money plane and the policy plane must not answer on the host, and a gateway bound to one address must not answer on loopback. Three more test the credential rather than the port, because a plane with a malformed key spec starts cleanly, stays reachable, and authenticates nobody. One more reads back the rule Docker actually wrote for port 4100 instead of trusting the variable meant to set it, because a default that says loopback while the port says otherwise is worse than no default at all.

### Or a Kubernetes cluster

For teams whose answer to everything is a cluster. One script brings up k3s across your nodes with the CNI, storage and hardening the stack actually needs, then the workload applies from plain manifests.

| install | one script |
|---|---|
| proven on | Hetzner, AWS and GCP |
| what it buys | high availability |
| what it costs | a ReadWriteMany volume |
| traps | 160 documented, with whose fault each was |

**The commands, and the one thing a cluster costs you.**

```
git clone https://github.com/TAIPANBOX/stack-k8s
cd stack-k8s && ./deploy.sh --servers ... --hcloud-token ... --trust-domain <your domain>
```

Both paths are one command, and both ask what they need before the long part rather than failing on it afterwards. So the trade is not convenience. Kubernetes buys high availability and costs you the one thing a single box gets for free: the planes couple through a shared event log, so a cluster needs a ReadWriteMany volume for it.

That trade, and every other thing that bites, are documented in the repositories rather than discovered by you. The same manifests came up on six clusters across Hetzner, AWS and GCP, and exactly one line of Kubernetes configuration differs between the three: Calico has to encapsulate unconditionally on GCP, because a GCE VPC routes every packet by destination and a pod address matches no route. Every trap we hit is written down and already fixed in the files.

## The contract for an agent of your own.

```
# install: https://github.com/TAIPANBOX/agent-stack-go#install
agent-conform passport.json events.ndjson
```

This installs nothing of the stack: it is the contract itself, for an agent of your own. Exit 0 means every file and every NDJSON line conforms; exit 1 means at least one did not. That is the whole interface.

### agent-conform, every platform

Every one of those addresses always serves the newest release, so a link saved today still works after the next one. The asset names carry no version, which is what makes that true; the version lives inside the binary, where `agent-conform -version` reads it back.

## The layer every other page stands on.

Every other page on this site is a producer or a consumer of this contract. [TokenFuse](https://it-rat.com/services/tokenfuse.html) pushes its incident taxonomy through the envelope verbatim, zero renaming. [Wardryx](https://it-rat.com/services/wardryx.html) answers policy_deny in schema v0.2. [Engram](https://it-rat.com/services/engram.html) writes memory_written and reflection_run into the same stream, and [Idryx](https://it-rat.com/services/idryx.html) reads everything back into one identity graph, checking passports with the same passport.Parse this platform ships. Different rooms, one grammar.

What the contract is for, in practice: [AI agent governance](https://it-rat.com/ai-agent-governance.html) and the controls it lets independent tools share.

## What changed.

The platform's own list for 1 to 15 October 2026, the agent-stack-go releases, agent-passport and the Terraform provider on main, is in [the stack's changes](https://it-rat.com/changes-2026-10.html#platform).

## What the contract does not claim, and what the sandbox leaves out.

- The passport is metadata, not a token, and the spec is not an authentication protocol.

- Where the API has no delete, the provider says so instead of pretending.

- The laptop sandbox is a sandbox to try the stack, not a production deployment. It binds loopback only, so nothing on it is reachable by an agent on another machine.

- In the sandbox Heraldyx is pinned to file mode, writing what it would have mailed rather than mailing it.

- The delegation plane, the FinOps console and the typed-answers service stay behind a flag: `--with-delegation`, `--with-finops` and `--with-typed`.

- Engram, Qryx, Verdryx and Mockryx are deliberately not servers: they are libraries and one-shot CLIs.

- The one-box install coming back after a reboot was measured once, on 2026-09-17.

## Back to the room.

The [Platform room](https://it-rat.com/services/platform.html) has the simulation, the drawing and the common questions, and [the guides index](https://it-rat.com/guides.html) has the field itself.

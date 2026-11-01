<!-- https://it-rat.com/install.html -->

# Install the stack, all of it or one service at a time

> One command for the whole stack on a box you own, a cluster or your laptop, and how each service installs and runs on its own.

Every service is its own repository with its own releases, so nothing here has to be adopted whole. If you want all of it, one command brings it up on a box you own. If you want one piece, it installs and runs on its own. The exact commands, pinned to a version, live in each repository, because a second copy of an install procedure is a second thing to keep true.

- [Four ways in](https://it-rat.com/install.html#ways)

- [All of it, on one box](https://it-rat.com/install.html#all)

- [All of it, on Kubernetes](https://it-rat.com/install.html#cluster)

- [On your laptop](https://it-rat.com/install.html#laptop)

- [One service at a time](https://it-rat.com/install.html#one)

- [After it is up](https://it-rat.com/install.html#next)

## Four ways in.

one box

### All of it, on one machine

A Debian or Ubuntu machine you own, one command, every service pulled as a published image and nothing compiled.

a cluster

### All of it, on Kubernetes

The same services as plain manifests: one script for bare servers, or one apply on a cluster you already run.

your laptop

### A sandbox to look around

Built from source and run natively, with no Docker, bound to your own machine and gone when you press Ctrl-C.

one piece

### One service at a time

Any single service from its own repository. Most run on their own; the list says which lean on another.

## All of it, in one command.

You need a Debian or Ubuntu machine you control, root on it, and outbound internet. Everything else the installer brings: it adds Docker if the machine has none, pulls every service as a published image, and compiles nothing.

```
curl -fsSL https://raw.githubusercontent.com/TAIPANBOX/stack-single/main/install.sh | bash
```

It brings up the core: the gateway and the ledger behind it, policy, identity, key custody and its witness, alerts by mail, a check on the record's chain, the console, and the tunnel an operator uses to reach it. It ends by checking itself, and the last line it prints says whether every check passed.

**It comes up closed.** The gateway listens on the machine's loopback, so nothing faces the internet until you open it, and opening it is one word:

```
GATEWAY_BIND=0.0.0.0 ./install.sh
```

Then point an agent at the gateway, wherever that agent runs. Every call carries a client key, and the installer mints one for your agents when you bring none, in **/opt/agent-stack/agent-key**.

```
ANTHROPIC_BASE_URL=http://<your box>:4100
```

To check an installed box again without changing anything on it:

```
STACK_DIR=/opt/agent-stack ./install.sh status
```

### Add the rest when you want it

- **Delegation**, so an agent can prove whose authority it carries: `WITH_DELEGATION=1 ./install.sh`

- **Typed answers**, on a free, deterministic stub that makes no outbound call until you choose a model: `WITH_TYPED=1 ./install.sh`

- **Governed web access** for agents that fetch: `docker compose --profile egress up -d scopyx`

- **The FinOps console**: `docker compose --profile finops up -d costcrew`

Every flag, and what a second run does and does not change, is in the [stack-single repository](https://github.com/TAIPANBOX/stack-single#readme).

## All of it, on Kubernetes.

The same services as plain YAML and a kustomization, with no Helm. On bare servers, one script builds the cluster and the stack together:

```
git clone https://github.com/TAIPANBOX/stack-k8s && cd stack-k8s
./deploy.sh --servers ip1,ip2,ip3 --agents ip4,ip5 --hcloud-token <token> \
  --trust-domain <your domain>
```

That script is written for Hetzner: it puts up the cloud firewall, a cluster with secrets encrypted at rest and network policy that is actually enforced, and storage, then applies the manifests and runs the stack's own checks and its containment tests. AWS and GCP have deploy scripts of their own, and on a cluster you already run the manifests apply with one command:

```
kubectl apply -k manifests/
```

Some services are opt-in on a cluster too, each one more manifest to apply. The [stack-k8s repository](https://github.com/TAIPANBOX/stack-k8s#readme) names them, along with every trap found while building it.

## On your laptop, to look around.

A sandbox, not a deployment. It builds each service from source and runs it natively, with no Docker, binds everything to 127.0.0.1, and stops cleanly when you press Ctrl-C. If a toolchain or a port is missing, it says which.

```
git clone https://github.com/TAIPANBOX/stack-up && cd stack-up && ./up.sh
```

Delegation, the FinOps console and typed answers join with `--with-delegation`, `--with-finops` and `--with-typed`. The [stack-up repository](https://github.com/TAIPANBOX/stack-up#readme) has the port map and the rest.

## One service at a time.

Nothing here has to be adopted whole. Each service is its own repository with its own releases, and most of them run alone. The list says how each one ships and what, if anything, it leans on; its repository has the command, pinned to a version.

| service | how it ships | on its own | install |
|---|---|---|---|
| the control room |  |  |  |
| Genaryx | The console of the one-box and cluster installs; built from source on its own. | Reads the stack it sits on. | [genaryx ↗](https://github.com/TAIPANBOX/genaryx#readme) |
| money |  |  |  |
| TokenFuse | A container image: a proxy you start and point your agent at. | Yes, with a model provider behind it, or its stub for a dry run. | [tokenfuse ↗](https://github.com/TAIPANBOX/tokenfuse#readme) |
| CostCrew | A Go binary, or the `finops` profile of the one-box install. | Yes. It listens on loopback and reads your bills. | [costcrew ↗](https://github.com/TAIPANBOX/costcrew#readme) |
| TokenFuse Pocket | An iPhone app, not wired in yet, so there is nothing to install. | Not yet. | not yet |
| guardrails |  |  |  |
| Wardryx | A signed container image, or built from source with Go. | Yes. It answers policy questions over HTTP. | [wardryx ↗](https://github.com/TAIPANBOX/wardryx#readme) |
| Idryx | A prebuilt binary for your platform. | Yes. It reads an event log. | [idryx ↗](https://github.com/TAIPANBOX/idryx#readme) |
| Scopyx | A container image. | Asks Wardryx for every decision. | [scopyx ↗](https://github.com/TAIPANBOX/scopyx#readme) |
| Vouchryx | A container image. | Needs an issuer, a signing key and the issuers it trusts. | [vouchryx ↗](https://github.com/TAIPANBOX/vouchryx#readme) |
| proof |  |  |  |
| Qryx | A prebuilt binary, with checksums. | Yes. Point it at a path. | [qryx ↗](https://github.com/TAIPANBOX/qryx#readme) |
| Keyryx | A container image whose build you can verify. | Holds the signing keys the others use; the one-box install includes it. | [keyryx ↗](https://github.com/TAIPANBOX/keyryx#readme) |
| Verdryx | A Python package, installed from its repository. | Yes. A dry run uses a stub model, with no network and no key. | [verdryx ↗](https://github.com/TAIPANBOX/verdryx#readme) |
| Typryx | A Go binary or a container image. An optional add-on. | Yes, on its stub backend until you choose a model. | [typryx ↗](https://github.com/TAIPANBOX/typryx#readme) |
| Mockryx | A prebuilt binary. | Needs a pre-production gateway to fire its drills at. | [mockryx ↗](https://github.com/TAIPANBOX/mockryx#readme) |
| Trailryx | Container images: a receiver and a store. No Rust toolchain needed. | Takes events from the stack and keeps the record. | [trailryx ↗](https://github.com/TAIPANBOX/trailryx#readme) |
| ground |  |  |  |
| Heraldyx | A container image. | Reads an event file, and can write the mail to a file instead of sending it. | [heraldyx ↗](https://github.com/TAIPANBOX/heraldyx#readme) |
| Engram | A Python package, `pip install engdbram`: a library in your own process. | Yes. | [engram ↗](https://github.com/TAIPANBOX/engram#readme) |
| Platform | Agent Passport is a specification; agent-stack-go is a Go module with the `agent-conform` binary; the Terraform provider is on the Terraform Registry as `TAIPANBOX/taipan`. | Yes, each of them. | [agent-stack-go ↗](https://github.com/TAIPANBOX/agent-stack-go#readme) |

## Where to go next.

- **[From zero to your first alert](https://it-rat.com/first-alert.html)**: point one agent at the box and make it fire on purpose.

- **[What runs where, and what it costs](https://it-rat.com/what-runs-where.html)**: one machine, a five-node cluster or a hyperscaler, measured.

- **[The Stack page](https://it-rat.com/stack.html)**: every service with its room and its guide.

## Back to the guides.

[The guides index](https://it-rat.com/guides.html) has the rest: how the stack is secured, the practice of running agents, and what changed in October.

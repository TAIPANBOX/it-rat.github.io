<!-- https://it-rat.com/services/qryx.html -->

# Qryx, the crypto plane

> Inventory every key, certificate and algorithm you actually run, grade the post-quantum risk against the NCSC 2028, 2031 and 2035 dates, sign the evidence.

Qryx tells you what is actually running: it scans binaries, containers, live TLS, certificates, dependencies and cloud KMS, and comes back with a cryptographic asset graph instead of a slide deck.

## Watch it find every key in the building.

This is a simulation, but the shape is real: it replays a live run against 25,586 ELF binaries, a container image and a live TLS endpoint. The evidence at the end is signed with a post-quantum algorithm, not a promise.

## One graph. Every report reads the same one.

Five kinds of sources feed one scan engine: binaries, containers, live TLS, cloud KMS, and source plus Terraform. CBOM, the CNSA audit, the NCSC readiness report and the migration plan all read that same graph, so they cannot disagree with each other.

## A graph that grades itself.

### CBOM

CycloneDX 1.6, one component per unique asset and risk class, every occurrence attached. It plugs into the same supply-chain tooling that already tracks your SBOMs.

### Harvest now, decrypt later

Data encrypted with a quantum-vulnerable algorithm today can be captured now and decrypted once a cryptographically relevant quantum computer exists. The migration clock is already running.

### Post-quantum signing

Evidence attestations sign with ML-DSA (FIPS 204) straight from Go's stdlib, crypto/mldsa, no cosign dependency.

### CI drift gate

Snapshot the graph, then fail the build the moment a new weak or quantum-vulnerable asset appears: a baseline diff exits 2 on new high-risk findings.

## The inventory the rest of the stack borrows from.

Qryx can write its agent-passport findings, drift, policy violations and signed-evidence records as agent-events onto the shared bus that [Platform](https://it-rat.com/services/platform.html) defines and every service writes to (opt-in, with --events). Only a finding that names a real agent emits an event, which today means the findings of qryx agents; scans of code, binaries, TLS and cloud KMS carry no agent and emit none. Crypto posture is one plane of a wider practice: [AI agent governance](https://it-rat.com/ai-agent-governance.html), and the defensive picture in [AI agent security](https://it-rat.com/ai-agent-security.html).

## One binary, any platform.

Grab the latest binary from the [releases page](https://github.com/TAIPANBOX/qryx/releases) (Linux, macOS, Windows, SHA256SUMS included), or build from source with Go 1.27; the pinned go1.27.4 toolchain downloads itself on the first build.

## What it leaves out, on purpose.

- Identity stays Idryx's job; the agents connector stays strictly on the crypto axis.

- Cryptography in test code is scanned and counted, then kept out of the production inventory; a flag counts it as production if that is what you want.

### The Qryx guide

## Where a post-quantum migration actually starts

**Q: How do I start a post-quantum migration?**
With an inventory, because you cannot migrate what you have not found. Qryx scans binaries, containers, live TLS endpoints, certificates, dependencies and cloud KMS, and returns a cryptographic asset graph graded against the NCSC milestones: discovery by 2028, the highest-priority systems by 2031, everything by 2035.

**Q: What is a CBOM?**
A cryptographic bill of materials in CycloneDX 1.6: one component per unique asset and risk class, with every occurrence attached. It lives in the same supply-chain tooling as your SBOMs, so cryptography stops having its own isolated report nobody reads.

**Q: Can it fail a build when someone ships a weak key?**
Yes. Snapshot the graph as a baseline, and a new weak or quantum-vulnerable asset fails the build with exit code 2. The policy engine (a standards violation) and a regressed compliance trend both exit 3, so CI can tell a new weak asset from the other two. That is the day it matters, not the next audit cycle.

**Q: Does it find hardcoded keys?**
It does, and it counts them honestly: cryptography that exists only in test fixtures is scanned, reported and kept out of the production inventory, with one line saying how much was set aside. Counting fixtures inflates the number you are trying to drive to zero.

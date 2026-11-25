<!-- https://it-rat.com/services/qryx.html -->

# Qryx, the crypto plane

> Inventory every key, certificate and algorithm you actually run, grade the post-quantum risk against the NCSC 2028, 2031 and 2035 dates, sign the evidence.

Qryx tells you what is actually running: it scans binaries, containers, live TLS, certificates, dependencies and cloud KMS, and comes back with a cryptographic asset graph instead of a slide deck.

## Watch it find every key in the building.

A simulation of a live run against 25,586 ELF binaries, a container image and a live TLS endpoint. The evidence at the end is signed with a post-quantum algorithm.

## One graph. Every report reads the same one.

Five kinds of sources feed one scan engine: binaries, containers, live TLS, cloud KMS, and source plus Terraform. CBOM, the CNSA audit, the NCSC readiness report and the migration plan all read that same graph, so they cannot disagree with each other.

## A graph that grades itself.

Qryx writes a CycloneDX 1.6 CBOM with one component per asset and risk class, so the tooling that tracks your SBOMs reads it too. [In the guide](https://it-rat.com/qryx-guide.html#holds)

Data sealed today with a quantum-vulnerable algorithm can be captured now and opened later, which is why the graph grades it already. [In the guide](https://it-rat.com/qryx-guide.html#holds)

Evidence attestations are signed with ML-DSA (FIPS 204) from Go's own crypto/mldsa, with no cosign dependency. [In the guide](https://it-rat.com/qryx-guide.html#holds)

Against a snapshot of the graph, a baseline diff exits 2 the moment a new weak or quantum-vulnerable asset appears. [In the guide](https://it-rat.com/qryx-guide.html#holds)

It stays on the crypto axis and leaves identity to Idryx, and it counts cryptography in test code apart from the production inventory. [In the guide](https://it-rat.com/qryx-guide.html#limits)

## The inventory the rest of the stack borrows from.

Opt-in, and only for findings that name an agent. Crypto posture is one plane of [AI agent governance](https://it-rat.com/ai-agent-governance.html); the defensive picture is in [AI agent security](https://it-rat.com/ai-agent-security.html).

## One binary, any platform.

Grab the latest binary from the [releases page](https://github.com/TAIPANBOX/qryx/releases) (Linux, macOS, Windows, SHA256SUMS included), or build from source with Go 1.27; the pinned go1.27.4 toolchain downloads itself on the first build.

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

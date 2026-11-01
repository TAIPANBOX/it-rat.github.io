<!-- https://it-rat.com/qryx-guide.html -->

# Qryx guide

> How Qryx finds every key and grades its post-quantum risk, the risk model, how to run it, what changed in October 2026, and what it leaves out.

The [Qryx room](https://it-rat.com/services/qryx.html) keeps the sixty-second sweep, the drawing of the one graph, how to start it, and the common questions. This guide keeps the rest of what the room used to say: what it holds in full, the risk model, how it counts honestly, where it sits in the stack, downloads for every platform, what changed from 1 to 15 October 2026, and what it leaves out.

- [At a glance](https://it-rat.com/qryx-guide.html#overview)

- [How it works](https://it-rat.com/qryx-guide.html#how-it-works)

- [What it holds](https://it-rat.com/qryx-guide.html#holds)

- [The risk model](https://it-rat.com/qryx-guide.html#risk-model)

- [Counting honestly](https://it-rat.com/qryx-guide.html#counting)

- [What it reads](https://it-rat.com/qryx-guide.html#reads)

- [In the stack](https://it-rat.com/qryx-guide.html#in-the-stack)

- [Running it](https://it-rat.com/qryx-guide.html#run)

- [What changed](https://it-rat.com/qryx-guide.html#changes)

- [Limits](https://it-rat.com/qryx-guide.html#limits)

## Qryx at a glance.

- **Release:** latest · prebuilt binaries.

- **Core:** Go 1.27 · ML-DSA (FIPS 204).

- **Scans:** binaries · containers · TLS · cloud KMS · source · certs.

- **Output:** CBOM · NCSC report · signed evidence.

- **Milestones:** NCSC 2028 · 2031 · 2035.

- **Licence:** Apache-2.0.

### What it is

A crypto audit tells you what your architecture documents say you run. Qryx tells you what is actually running: it scans binaries, containers, live TLS, certificates, dependencies and cloud KMS, and comes back with a cryptographic asset graph instead of a slide deck. Every asset gets a post-quantum grade against the NCSC's 2028, 2031 and 2035 milestones, and CI fails the day a new weak key ships, not at the next audit cycle.

## One graph. Every report reads the same one.

Five kinds of sources feed one scan engine: binaries, containers, live TLS, cloud KMS, and source plus Terraform. Findings dedupe into an asset graph keyed on algorithm, key size and risk class, so a certificate that is both expired and quantum-vulnerable gets two nodes, not one silently overwriting the other. CBOM, the CNSA audit, the NCSC readiness report and the migration plan all read that same graph, so they cannot disagree with each other.

The [room](https://it-rat.com/services/qryx.html#sim) replays a live run against 25,586 ELF binaries, a container image and a live TLS endpoint. A quantum-vulnerable cert turns up mid-sweep.

## Not a PDF audit. A graph that grades itself.

### CBOM

CycloneDX 1.6, one component per unique asset and risk class, every occurrence attached. It plugs into the same supply-chain tooling that already tracks your SBOMs, so cryptography stops living in its own isolated report.

### Harvest now, decrypt later

Data encrypted with a quantum-vulnerable algorithm today can be captured now and decrypted once a cryptographically relevant quantum computer exists. The migration clock is already running.

### Post-quantum signing

Evidence attestations sign with ML-DSA (FIPS 204) straight from Go's stdlib, crypto/mldsa, no cosign dependency. All three security levels, ML-DSA-44/65/87, live-verified end to end against real openssl-generated keys.

### Context beats compliance

The asset graph keys on risk class as well as algorithm and key size, so a certificate that is both expired and quantum-vulnerable gets two findings instead of one silently overwriting the other.

### CI drift gate

Snapshot the graph, then fail the build the moment a new weak or quantum-vulnerable asset appears: a baseline diff exits 2 on new high-risk findings. The policy engine exits 3 on a standards violation; a regressed compliance trend exits 3 too.

### Agent-aware

The agents connector inventories the governance stack's own trust surface: Agent Passport attestation crypto and the agent-event hash chain's prev_hash integrity. Identity stays Idryx's job; this connector stays strictly on the crypto axis.

## Six risk classes, and a clock that started without you

### How an asset is scored

Every asset Qryx finds is scored against a post-quantum and hygiene model, not a single pass-or-fail line.

| Class | Examples | Why it is called that |
|---|---|---|
| quantum-vulnerable | RSA, ECC, DSA, DH | breakable by Shor's algorithm on a capable quantum computer |
| weak | MD5, SHA-1, DES, RC4, RSA under 2048 | broken or deprecated already, no quantum computer required |
| misconfig | TLS 1.0 and 1.1, unsafe cipher suites | a sound primitive used unsoundly |
| expired | past-due certificates | the validity window has elapsed |
| hardcoded | private keys in source or config | a secret committed into the tree |
| safe | ML-KEM, ML-DSA, SLH-DSA | the post-quantum standards, FIPS 203, 204 and 205 |

The timeline is not ours to argue with. NIST standardised the replacements in 2024, and the NCSC clock runs discovery by 2028, the highest-priority systems by 2031, and everything by 2035. The first of those dates is about knowing what you have, which is the part that takes longest and cannot be bought late.

## Two findings, not one, and why test crypto is not debt

### What the count leaves out

Keying the graph on risk class as well as algorithm and key size sounds like a detail until a certificate is both expired and quantum-vulnerable and you only hear about one of them. That exact bug turned up scanning a real endpoint, and it is fixed: an asset in two risk classes produces two findings, because they need two different fixes on two different clocks.

The opposite failure is inflation. Cryptography in test code is scanned and counted, then kept out of the production inventory: out of the asset graph, the compliance verdict, the policy gate, the saved baseline and every export. One line on stderr says how much was set aside and how much of it exists nowhere else, and a flag counts it as production if that is what you want.

This is not cosmetic. Scanning Qryx's own repository, 8 of 13 assets existed only in test fixtures, and 21 of 40 occurrences were test code. In a sibling repository a hardcoded-key finding reported three occurrences, two of them fixtures. Counting those inflates the number an operator is trying to drive to zero, and buries the findings they actually have to migrate.

The classification is not merely path-based either: Rust's in-file test modules are recognised, so an inline test block inside a production file is set aside while the production code around it still counts.

## You cannot migrate what you cannot see.

Qryx reads binaries, container images, live TLS endpoints, certificates, dependencies, cloud KMS and source code, and puts them into one graph graded against the CNSA 2.0 and NCSC milestones.

## The inventory the rest of the stack borrows from.

Qryx emits every finding as an agent-event onto the shared bus that [Platform](https://it-rat.com/services/platform.html) defines and every service writes to. It watches the same estate [TokenFuse](https://it-rat.com/services/tokenfuse.html) spends against, the binaries, endpoints and keys underneath the calls TokenFuse meters. [Mockryx](https://it-rat.com/services/mockryx.html) can demand a crypto reaction in its drills too: an expect.event assertion that a fire drill actually produced a crypto_finding, not silence.

Crypto posture is one plane of a wider practice: [AI agent governance](https://it-rat.com/ai-agent-governance.html), and the defensive picture in [AI agent security](https://it-rat.com/ai-agent-security.html).

## One binary, any platform.

```
qryx scan .
```

```
qryx tls api.anthropic.com:443
```

Grab the latest binary from the [releases page](https://github.com/TAIPANBOX/qryx/releases) (Linux, macOS, Windows, SHA256SUMS included), or build from source with Go 1.27; the pinned go1.27.2 toolchain downloads itself on the first build.

### Download, any platform

Every one of those addresses always serves the newest release, so a link saved today still works after the next one. The asset names carry no version, which is what makes that true; the version lives inside the binary, where `qryx version` reads it back.

## What changed from 1 to 15 October

No release in the window, still 1.0.0. The same entry, beside every other service's, is in [what changed in the stack](https://it-rat.com/changes-2026-10.html#qryx).

- Documentation, tests and toolchain only: the Go toolchain moved to 1.27.2, the shared library pin moved to 1.3.0, the secret scan runs on every pull request, and a test now checks every environment read against the component manifest.

## What it leaves out, on purpose.

- Identity stays Idryx's job; the agents connector stays strictly on the crypto axis.

- Cryptography in test code is scanned and counted, then kept out of the production inventory: out of the asset graph, the compliance verdict, the policy gate, the saved baseline and every export. A flag counts it as production if that is what you want.

- The sixty seconds on the room are a simulation, but the shape is real: they replay a live run against 25,586 ELF binaries, a container image and a live TLS endpoint.

## Back to the room.

The [Qryx room](https://it-rat.com/services/qryx.html) has the sweep, the drawing and the common questions, and [the guides index](https://it-rat.com/guides.html) has the field itself.

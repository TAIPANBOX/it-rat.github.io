<!-- https://it-rat.com/services/qryx.html -->

# Qryx, the crypto plane

> Inventory every key, certificate and algorithm you actually run, grade the post-quantum risk against the NCSC 2028, 2031 and 2035 dates, sign the evidence.

A crypto audit tells you what your architecture documents say you run. Qryx tells you what is actually running: it scans binaries, containers, live TLS, certificates, dependencies and cloud KMS, and comes back with a cryptographic asset graph instead of a slide deck. Every asset gets a post-quantum grade against the NCSC's 2028, 2031 and 2035 milestones, and CI fails the day a new weak key ships, not at the next audit cycle.

## Watch it find every key in the building.

This is a simulation, but the shape is real: it replays a live run against 25,586 ELF binaries, a container image and a live TLS endpoint. A quantum-vulnerable cert turns up mid-sweep. The evidence at the end is signed with a post-quantum algorithm, not a promise.

## One graph. Every report reads the same one.

Five kinds of sources feed one scan engine: binaries, containers, live TLS, cloud KMS, and source plus Terraform. Findings dedupe into an asset graph keyed on algorithm, key size and risk class, so a certificate that is both expired and quantum-vulnerable gets two nodes, not one silently overwriting the other. CBOM, the CNSA audit, the NCSC readiness report and the migration plan all read that same graph, so they cannot disagree with each other.

## Not a PDF audit. A graph that grades itself.

### CBOM

CycloneDX 1.6, one component per unique asset and risk class, every occurrence attached. It plugs into the same supply-chain tooling that already tracks your SBOMs, so cryptography stops living in its own isolated report.

### Harvest now, decrypt later

Data encrypted with a quantum-vulnerable algorithm today can be captured now and decrypted once a cryptographically relevant quantum computer exists. The migration clock is already running.

**Q: How an asset is scored**

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

### Post-quantum signing

Evidence attestations sign with ML-DSA (FIPS 204) straight from Go's stdlib, crypto/mldsa, no cosign dependency. All three security levels, ML-DSA-44/65/87, live-verified end to end against real openssl-generated keys.

### Context beats compliance

The asset graph keys on risk class as well as algorithm and key size, so a certificate that is both expired and quantum-vulnerable gets two findings instead of one silently overwriting the other.

**Q: What the count leaves out**

Keying the graph on risk class as well as algorithm and key size sounds like a detail until a certificate is both expired and quantum-vulnerable and you only hear about one of them. That exact bug turned up scanning a real endpoint, and it is fixed: an asset in two risk classes produces two findings, because they need two different fixes on two different clocks.

The opposite failure is inflation. Cryptography in test code is scanned and counted, then kept out of the production inventory: out of the asset graph, the compliance verdict, the policy gate, the saved baseline and every export. One line on stderr says how much was set aside and how much of it exists nowhere else, and a flag counts it as production if that is what you want.

This is not cosmetic. Scanning Qryx's own repository, 8 of 13 assets existed only in test fixtures, and 21 of 40 occurrences were test code. In a sibling repository a hardcoded-key finding reported three occurrences, two of them fixtures. Counting those inflates the number an operator is trying to drive to zero, and buries the findings they actually have to migrate.

The classification is not merely path-based either: Rust's in-file test modules are recognised, so an inline test block inside a production file is set aside while the production code around it still counts.

### CI drift gate

Snapshot the graph, then fail the build the moment a new weak or quantum-vulnerable asset appears: a baseline diff exits 2 on new high-risk findings. The policy engine exits 3 on a standards violation; a regressed compliance trend exits 3 too.

### Agent-aware

The agents connector inventories the governance stack's own trust surface: Agent Passport attestation crypto and the agent-event hash chain's prev_hash integrity. Identity stays Idryx's job; this connector stays strictly on the crypto axis.

## You cannot migrate what you cannot see.

A crypto audit and a CSPM checkbox both ask about cryptography. Neither one reads the binary.

|  | Qryx | Annual crypto audit | CSPM checkbox |
|---|---|---|---|
| Cadence | Every commit | Yearly PDF | Weekly dashboard |
| Sees binaries | Symbol-level, incl. static fallback | No | No |
| Post-quantum grading | NCSC + CNSA milestones | A consultant's opinion | None |
| Evidence | Signed, ML-DSA optional | Slide deck | Screenshot |
| Cost of a finding | A failed CI run | A remediation project | A ticket nobody owns |

### The inventory the rest of the stack borrows from.

Qryx emits every finding as an agent-event onto the shared bus that [Platform](https://it-rat.com/platform.html) defines and every service writes to. It watches the same estate [TokenFuse](https://it-rat.com/tokenfuse.html) spends against, the binaries, endpoints and keys underneath the calls TokenFuse meters. [Mockryx](https://it-rat.com/mockryx.html) can demand a crypto reaction in its drills too: an expect.event assertion that a fire drill actually produced a crypto_finding, not silence.

Crypto posture is one plane of a wider practice: [AI agent governance](https://it-rat.com/ai-agent-governance.html), and the defensive picture in [AI agent security](https://it-rat.com/ai-agent-security.html).

Grab the latest binary from the [releases page](https://github.com/TAIPANBOX/qryx/releases) (Linux, macOS, Windows, SHA256SUMS included), or build from source: the ML-DSA toolchain downloads itself on the first build, Go 1.27.

**Q: Download, any platform**

Every one of those addresses always serves the newest release, so a link saved today still works after the next one. The asset names carry no version, which is what makes that true; the version lives inside the binary, where `qryx version` reads it back.

## Where a post-quantum migration actually starts

**Q: How do I start a post-quantum migration?**
With an inventory, because you cannot migrate what you have not found. Qryx scans binaries, containers, live TLS endpoints, certificates, dependencies and cloud KMS, and returns a cryptographic asset graph graded against the NCSC milestones: discovery by 2028, the highest-priority systems by 2031, everything by 2035.

**Q: What is a CBOM?**
A cryptographic bill of materials in CycloneDX 1.6: one component per unique asset and risk class, with every occurrence attached. It lives in the same supply-chain tooling as your SBOMs, so cryptography stops having its own isolated report nobody reads.

**Q: Can it fail a build when someone ships a weak key?**
Yes. Snapshot the graph as a baseline, and a new weak or quantum-vulnerable asset fails the build with a distinct exit code, with separate codes for a standards violation and a regressed compliance trend. That is the day it matters, not the next audit cycle.

**Q: Does it find hardcoded keys?**
It does, and it counts them honestly: cryptography that exists only in test fixtures is scanned, reported and kept out of the production inventory, with one line saying how much was set aside. Counting fixtures inflates the number you are trying to drive to zero.

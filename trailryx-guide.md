<!-- https://it-rat.com/trailryx-guide.html -->

# Trailryx guide

> How Trailryx proves an answer complete, how erasure leaves the chain intact, the durability runs, the offline verifier, and its limits.

The [Trailryx room](https://it-rat.com/services/trailryx.html) keeps the replay of two questions and one erasure, the drawing of how a query is classified, and the short version of each part. This guide keeps the rest of what the room used to say: where it sits today, how erasure leaves the trail intact, the durability runs and what a sealed pack does and does not prove, the verifier and its downloads, what it seals lately, and the limits.

- [At a glance](https://it-rat.com/trailryx-guide.html#overview)

- [Where it sits](https://it-rat.com/trailryx-guide.html#where-it-sits)

- [How it works](https://it-rat.com/trailryx-guide.html#how-it-works)

- [Measured, not asserted](https://it-rat.com/trailryx-guide.html#proof)

- [Running it](https://it-rat.com/trailryx-guide.html#run)

- [What it seals lately](https://it-rat.com/trailryx-guide.html#sealing-lately)

- [What changed](https://it-rat.com/trailryx-guide.html#changes)

- [Limits](https://it-rat.com/trailryx-guide.html#limits)

## Trailryx at a glance.

- **A record of what your agents did** that nobody can quietly change, or quietly shorten.

- **Core:** Rust, no unsafe, and no third-party code in the core or the verifier.

- **Ingest:** OTLP protobuf, JSON, or a collector's file.

- **Proves:** record, time, agent, run and type.

- **Erasure:** crypto-erasure, per subject.

- **Licence:** Apache-2.0.

### What it is

Tamper-evident is the easy half, and most audit stores stop there: you can tell if a record was edited. The hard half is the answer. Ask "everything agent X did in March" and an ordinary store hands you rows with no way to know whether it handed you all of them. Trailryx answers with a completeness proof when it can, and says partial with the reason named when it cannot. And its store is built to erase one person on request without breaking the trail; the shipped node does not expose that yet.

## Where this sits today, stated rather than implied.

Trailryx reads the shared agent-event bus and seals it. That was the open gap on this page until 2026-08-27 and it is closed: a dedicated crate maps the envelope the other planes write, `stack-up` runs the sealing routine at 06:57 by default, and the Kubernetes install has a nightly job that packs the ledger and verifies the pack before it exits. It still takes plain OTLP as well, from a collector or straight over the wire, so it stays useful to somebody who has traces and no TAIPANBOX. **Two gaps are left.** The console has no panel for the record plane, so what is sealed is read with the CLI rather than in a browser. Erasure is a library and the demo path today: trailryx-node has no erase command and keeps no payload plane, so an operator cannot yet erase one subject through the shipped binary.

## The auditor asks. One answer carries a proof, the other admits it cannot.

Records arrive and chain. Then a question lands on one of the five dimensions the index can prove, and the matching records are a contiguous range: that contiguity is the mechanism, not a picture of it. The second question is about something nothing sorts by, so the rows are still right and the answer says so. At the end, one subject is erased and the chain still verifies.

### Erase one person in the library, and the trail still verifies.

An audit store that cannot forget anybody fails the first request it gets in Europe. One that forgets by deleting rows breaks every proof it ever issued. Trailryx separates the two planes so neither has to give way.

**Typed metadata, encrypted payload.** The plane the proofs are built on holds identifiers, enums, hashes, numbers and timestamps, and nothing else. Any prose lives in the encrypted payload under the subject's own key. A mapper that does not know where an attribute belongs puts it in the encrypted plane rather than guessing, because guessing the other way is how personal data ends up outside the erasure boundary.

**The record commits to the payload it no longer has.** Forgetting drops the key. The record keeps its hash, size, class and key id, so what it committed to is still checkable and the chain around it is untouched. The answer to "was anything removed here" stays yes-and-here-is-where, rather than becoming unanswerable.

## The number that makes the other number mean something.

A durability sweep reporting zero violations proves nothing on its own: a check that cannot fail reports zero forever. So the same harness is run against a disk that lies about its writes, and it is required to fail.

### With a disk that keeps its word

As recorded, undated, in the repository's VALIDATION.md: 400,000 seeds, roughly 800 million shard ticks, about 12 million crashes injected, nine days and six hours of simulated time in ten minutes and forty seconds of real time. Zero durability violations.

### With a disk that lies

The same harness, the honest-disk assumption removed (as recorded, undated, in VALIDATION.md): 17,869 of 20,000 seeds fail, each naming its own seed and digest. That is what makes the zero above worth reading.

### What the installed profile seals today

What the installed profile seals today, stated beside the verdict rather than under it: the `record-seal` job the launchers run keeps the typed metadata plane and writes down that it declined the payload, because a node cannot choose an operator's custody for them. Its pack verifies as self-consistent, and `trailryx-verify` says in plain words when a pack carries no root signature and no witness. All three launchers sign each sealed root through Keyryx by default and attach the witness's attestations: stack-up since 2026-10-19, stack-k8s since v1.6.1, tagged on 2026-10-20, and stack-single since v1.6.0, tagged on 2026-11-05. No witness is an outside party, since stack-up's runs on the same host as the same user, stack-k8s's in the same cluster and stack-single's on the same box, each of those two as its own user in the record plane's group, and trailryx-verify does not warn about that. So a pack's verdict proves the chain was not altered and which key signed it. A date an outside party can vouch for takes an anchor off the box.

## The offline verifier.

```
trailryx-verify incident-4471.trxevid
```

Zero third-party dependencies, because an auditor reads it rather than trusting it. A download on [GitHub releases](https://github.com/TAIPANBOX/trailryx/releases) with a SHA256SUMS file signed keyless by Sigstore, so nobody has to build it first.

### Download the verifier

Each address always serves the newest release: the asset names carry no version, so a link saved today still works after the next one. These are the offline verifier; `trailryx-ingest` sits beside them on the releases page. No Windows build yet, and saying so is cheaper than a broken link.

## The newest thing on the bus is a crew of agents.

[CostCrew](https://it-rat.com/services/costcrew.html) writes twenty-three event types about money and about its own analysts. This plane seals the two about money with everything else and refuses the other twenty-one by name, because they record a practice rather than an agent's run. The rest were refused by design rather than dropped, which is the distinction this store exists to keep.

## Releases from 1 to 15 October 2026.

What changed from 1 to 15 October 2026, release by release, is in [the stack's changes for October](https://it-rat.com/changes-2026-10.html#trailryx).

## What it does not do, and what is not proven yet.

- The console has no panel for the record plane, so what is sealed is read with the CLI rather than in a browser.

- Erasure is a library and the demo path today: trailryx-node has no erase command and keeps no payload plane, so an operator cannot yet erase one subject through the shipped binary.

- SQL is a facade in the tree and not yet a port in the shipped node: today you read the records through `read`.

- The `record-seal` job the launchers run keeps the typed metadata plane and declines the payload. All three launchers sign each sealed root through Keyryx by default and attach the witness's attestations: stack-up since 2026-10-19, stack-k8s since v1.6.1, tagged on 2026-10-20, and stack-single since v1.6.0, tagged on 2026-11-05. No witness is an outside party: stack-up's runs on the same host as the same user, stack-k8s's in the same cluster and stack-single's on the same box, each of those two as its own user in the record plane's group. trailryx-verify does not warn about that. So the verdict proves the chain was not altered and which key signed it; a date an outside party can vouch for takes an anchor off the box.

- The durability figures are as recorded, undated, in the repository's VALIDATION.md.

- No Windows build of the verifier yet.

## Back to the room.

The [Trailryx room](https://it-rat.com/services/trailryx.html) has the replay, the drawing and the short version of each part, and [the guides index](https://it-rat.com/guides.html) has the field itself.

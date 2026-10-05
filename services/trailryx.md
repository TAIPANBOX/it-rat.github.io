<!-- https://it-rat.com/services/trailryx.html -->

# Trailryx, the record

> A record of what your AI agents did that nobody can quietly change or shorten, where every answer carries a proof that it is complete.

Tamper-evident is the easy half, and most audit stores stop there: you can tell if a record was edited. The hard half is the answer. Ask "everything agent X did in March" and an ordinary store hands you rows with no way to know whether it handed you all of them. Trailryx answers with a completeness proof when it can, and says partial with the reason named when it cannot. And it can still erase one person on request without breaking the trail, which is the pair almost nothing manages at once.

**Where this sits today, stated rather than implied.** Trailryx reads the shared agent-event bus and seals it. That was the open gap on this page until 2026-08-27 and it is closed: a dedicated crate maps the envelope the other planes write, `stack-up` runs the sealing routine at 06:57 by default, and the Kubernetes install has a nightly job that packs the ledger and verifies the pack before it exits. It still takes plain OTLP as well, from a collector or straight over the wire, so it stays useful to somebody who has traces and no TAIPANBOX. **One gap is left and it is narrower:** the console has no panel for the record plane, so what is sealed is read with the CLI rather than in a browser.

## The auditor asks. One answer carries a proof, the other admits it cannot.

Records arrive and chain. Then a question lands on one of the five dimensions the index can prove, and the matching records are a contiguous range: that contiguity is the mechanism, not a picture of it. The second question is about something nothing sorts by, so the rows are still right and the answer says so. At the end, one subject is erased and the chain still verifies.

## SQL does not become a hole in the proof model.

SQL is a facade in the tree and not yet a port in the shipped node: today you read the records through `read`. What every answer carries, either way, is how much of it is actually proved, because an answer of unknown completeness must not read like a proved one.

## Erase one person, and the trail still verifies.

An audit store that cannot forget anybody fails the first request it gets in Europe. One that forgets by deleting rows breaks every proof it ever issued. Trailryx separates the two planes so neither has to give way.

### Typed metadata, encrypted payload

The plane the proofs are built on holds identifiers, enums, hashes, numbers and timestamps, and nothing else. Any prose lives in the encrypted payload under the subject's own key. A mapper that does not know where an attribute belongs puts it in the encrypted plane rather than guessing, because guessing the other way is how personal data ends up outside the erasure boundary.

### The record commits to the payload it no longer has

Forgetting drops the key. The record keeps its hash, size, class and key id, so what it committed to is still checkable and the chain around it is untouched. The answer to "was anything removed here" stays yes-and-here-is-where, rather than becoming unanswerable.

## The number that makes the other number mean something.

A durability sweep reporting zero violations proves nothing on its own: a check that cannot fail reports zero forever. So the same harness is run against a disk that lies about its writes, and it is required to fail.

### With a disk that keeps its word

400,000 seeds, roughly 800 million shard ticks, about 12 million crashes injected, nine days and six hours of simulated time in ten minutes and forty seconds of real time. Zero durability violations.

### With a disk that lies

The same harness, the honest-disk assumption removed: 17,869 of 20,000 seeds fail, each naming its own seed and digest. That is what makes the zero above worth reading.

What the installed profile seals today, stated beside the verdict rather than under it: the `record-seal` job the launchers run keeps the typed metadata plane and writes down that it declined the payload, because a node cannot choose an operator's custody for them. Its pack verifies as self-consistent, and `trailryx-verify` says in plain words that it carries no root signature and no witness until an operator configures both. So the verdict proves the chain was not altered, not who published it or when.

**Q: Download the verifier**

Each address always serves the newest release: the asset names carry no version, so a link saved today still works after the next one. These are the offline verifier; `trailryx-ingest` sits beside them on the releases page. No Windows build yet, and saying so is cheaper than a broken link.

## The newest thing on the bus is a crew of agents.

[CostCrew](https://it-rat.com/costcrew.html) writes twenty-two event types about money and about its own analysts. This plane seals the two about money with everything else and refuses the other twenty by name, because they record a practice rather than an agent's run. Measured on 2026-08-28: twenty-six events on the bus in one run, and nine of them sealed into records in that same run. The rest were refused by design rather than dropped, which is the distinction this store exists to keep.

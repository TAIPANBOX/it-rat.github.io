<!-- https://it-rat.com/services/trailryx.html -->

# Trailryx, the record

> A record of what your AI agents did that nobody can quietly change or shorten, where every answer carries a proof that it is complete.

Tamper-evident is the easy half, and most audit stores stop there: you can tell if a record was edited. The hard half is the answer. Ask "everything agent X did in March" and an ordinary store hands you rows with no way to know whether it handed you all of them. Trailryx answers with a completeness proof when it can, and says partial with the reason named when it cannot. And it can still erase one person on request without breaking the trail, which is the pair almost nothing manages at once.

**Where this sits today, stated rather than implied.** Trailryx is not wired into the rest of the stack yet. It takes the OTLP traces you already have, from a collector or straight over the wire, and it holds no knowledge of the agent-event envelope the other planes share. That is a real gap and it has a design: a small shipper reads the shared log and maps it, so this store stays useful to somebody who has OTLP and no TAIPANBOX. Until that ships, treat this as a record store that happens to live in the same estate, not as a plane of it.

## The auditor asks. One answer carries a proof, the other admits it cannot.

Records arrive and chain. Then a question lands on one of the five dimensions the index can prove, and the matching records are a contiguous range: that contiguity is the mechanism, not a picture of it. The second question is about something nothing sorts by, so the rows are still right and the answer says so. At the end, one subject is erased and the chain still verifies.

## SQL does not become a hole in the proof model.

You get ordinary SQL over the records. What you also get, on every answer, is how much of it is actually proved, because an answer of unknown completeness must not read like a proved one.

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

**Q: Download the verifier**

Each address always serves the newest release: the asset names carry no version, so a link saved today still works after the next one. These are the offline verifier; `trailryx-ingest` sits beside them on the releases page. No Windows build yet, and saying so is cheaper than a broken link.

<!-- https://it-rat.com/services/trailryx.html -->

# Trailryx, the record

> A record of what your AI agents did that nobody can quietly change or shorten, where every answer says whether it is proved complete.

Trailryx answers with a completeness proof when it can, and says partial with the reason named when it cannot. And its store is built to erase one person on request without breaking the trail; the shipped node does not expose that yet.

**Where this sits today, stated rather than implied.** Trailryx reads the shared agent-event bus and seals it. It still takes plain OTLP as well, from a collector or straight over the wire, so it stays useful to somebody who has traces and no TAIPANBOX.

## The auditor asks. One answer carries a proof, the other admits it cannot.

A question lands on one of the five dimensions the index can prove, and the matching records are a contiguous range: that contiguity is the mechanism, not a picture of it. The second question is about something nothing sorts by, so the rows are still right and the answer says so.

## SQL does not become a hole in the proof model.

SQL is a facade in the tree and not yet a port in the shipped node: today you read the records through `read`. What every answer carries, either way, is how much of it is actually proved, because an answer of unknown completeness must not read like a proved one.

## Erase one person in the library, and the trail still verifies.

Trailryx separates the two planes so neither has to give way.

### Typed metadata, encrypted payload

The plane the proofs are built on holds identifiers, enums, hashes, numbers and timestamps, and nothing else. Any prose lives in the encrypted payload under the subject's own key.

### The record commits to the payload it no longer has

Forgetting drops the key. The record keeps its hash, size, class and key id, so what it committed to is still checkable and the chain around it is untouched.

## The number that makes the other number mean something.

A durability sweep reporting zero violations proves nothing on its own: a check that cannot fail reports zero forever. So the same harness is run against a disk that lies about its writes, and it is required to fail.

### With a disk that keeps its word

As recorded, undated, in the repository's VALIDATION.md: 400,000 seeds, roughly 800 million shard ticks, about 12 million crashes injected. Zero durability violations.

### With a disk that lies

The same harness, the honest-disk assumption removed (as recorded, undated, in VALIDATION.md): 17,869 of 20,000 seeds fail, each naming its own seed and digest. That is what makes the zero above worth reading.

## The offline verifier.

## The newest thing on the bus is a crew of agents.

[CostCrew](https://it-rat.com/services/costcrew.html) writes twenty-three event types about money and about its own analysts. This plane seals the two about money with everything else and refuses the other twenty-one by name, because they record a practice rather than an agent's run.

## What is not proven yet.

- The console has no panel for the record plane, so what is sealed is read with the CLI rather than in a browser.

- Erasure is a library and the demo path today: trailryx-node has no erase command and keeps no payload plane, so an operator cannot yet erase one subject through the shipped binary.

- All three launchers sign each sealed root through Keyryx by default and attach the witness's attestations: stack-up since 2026-10-19, stack-k8s since 2026-10-20, and stack-single since 2026-11-05. No witness is an outside party: stack-up's runs on the same host as the same user, stack-k8s's in the same cluster and stack-single's on the same box, each of those two as its own user in the record plane's group. trailryx-verify does not warn about that. So the verdict proves the chain was not altered and which key signed it; a date an outside party can vouch for takes an anchor off the box.

### The Trailryx guide

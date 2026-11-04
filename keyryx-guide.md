<!-- https://it-rat.com/keyryx-guide.html -->

# Keyryx guide

> How Keyryx signs, publishes and witnesses keys and the record, its routes, how to configure, run and verify it offline, its releases, and its limits.

The [Keyryx room](https://it-rat.com/services/keyryx.html) keeps the picture of the two roles, the common questions and the short version of each part. This guide keeps the rest: the routes, the configuration it refuses to start without, the witness's findings, how to run it and verify it offline, the releases so far, and the limits an operator meets. The README's NOT PROVEN section has the full list.

- [At a glance](https://it-rat.com/keyryx-guide.html#overview)

- [How the roles work](https://it-rat.com/keyryx-guide.html#how-it-works)

- [The routes](https://it-rat.com/keyryx-guide.html#surface)

- [Configuration](https://it-rat.com/keyryx-guide.html#configuration)

- [The witness](https://it-rat.com/keyryx-guide.html#witness)

- [Running and verifying it](https://it-rat.com/keyryx-guide.html#run)

- [Releases](https://it-rat.com/keyryx-guide.html#changes)

- [Limits](https://it-rat.com/keyryx-guide.html#limits)

## A key service and a witness, in one binary that runs as two processes.

Keyryx is a service of its own: public, Apache-2.0, written in Go, and off every request path. It has two roles, **custody** and **witness**. The binary has one command for each role and a third for offline checks. The roles never share a process, a key or a data directory, the launcher gives each its own uid (stack-single does), and the witness refuses to start if it is given custody's directory or root key.

Custody holds signing keys and signs low-rate statements for consumers that were granted a key: approval tokens, record seal roots and audit manifests. It certifies the short-lived keys that high-rate signers generate for themselves, and it publishes each key set with an overlap so that a rotation is never an outage.

The witness reads the record without writing to it. It checks that every byte it saw before is still there, reads each Trailryx store's sealed manifests, and keeps its own append-only log. Each head of that log is signed with ECDSA P-384 and ML-DSA-65 side by side.

## What custody keeps, and what a consumer receives.

### The key store

Each key is one file under the data directory. Its private half is wrapped with AES-256-GCM under a key derived by HKDF from the root key, and the derivation is bound to the key's name, id and algorithm, so a record moved or swapped refuses the start. The root key is 64 hex characters in a file that no group or other account can read. Every key and statement record carries a state MAC under a second derived key: a record whose MAC does not hold is treated as revoked, is never published or used, and raises an alarm until an admin revokes the key it names.

### Algorithms

ES256 and ES384 keys use fixed-width R and S over SHA-256 or SHA-384. ML-DSA-65 follows FIPS 204 through Go 1.27's standard library. Key ids are RFC 7638 thumbprints for elliptic keys and `mldsa65:` plus the base64url SHA-256 of the public key for ML-DSA. Custody never publishes a private member, and a route that tried to would fail its own test.

### Delegated keys

A high-rate signer keeps its own key in memory and asks custody to certify it in three steps: it asks for a challenge, it signs the challenge with the key being certified, and it sends its public key, the challenge, that proof and the life it wants. Custody answers with a key statement: a JWS with one payload and exactly two signatures, ES384 and ML-DSA-65, made by the two halves of the delegation root. The key is published until its end plus the name's overlap. A key id is certified once, and a revoked one is never published or certified again. At most four keys of one name are live at once.

### The use log

Custody writes one line per signature, statement, rotation and revocation to `use.ndjson`, each line naming the SHA-256 of the line before it. A signature or statement is answered only after its line is on disk, and the log holds the digest of what was signed, never the statement itself.

### Consumers and their one way in

Each consumer in the policy authenticates exactly one way: a unix socket of its own, a bearer key held as a digest and compared in constant time, or a Kubernetes projected service-account token checked against the cluster's keys for this service's audience. A consumer signs only with a key it was granted. The policy file is read whole and strictly, and an unknown field, a duplicate, or a grant of an undeclared key refuses the start.

## Custody and witness HTTP surfaces.

### Custody

| Route | Who | What |
|---|---|---|
| `GET /healthz` | anyone | liveness |
| `GET /v1/state` | anyone | the role, the version, each key's active and next id, and the alarms: every state on disk custody could not vouch for |
| `GET /v1/keys` | anyone | the inventory, revoked keys included; never a private member |
| `GET /v1/jwks/{name}` | anyone, cacheable | the key set a verifier caches; for the delegation root, both halves |
| `GET /v1/statements/{kid}` | anyone, cacheable | the statement that certified a delegated key, and when it was revoked |
| `POST /v1/keys/{name}/sign` | a consumer granted sign | signs a statement of at most 4 KiB |
| `POST /v1/keys/{name}/challenge` and `/delegate` | a consumer granted delegate | the proof-of-possession steps for a delegated key |
| `POST /v1/keys/{name}/rotate` | an admin key | creates the next key, published before it signs |
| `POST /v1/kids/{kid}/revoke` | an admin key | takes a key id out of every key set at once |

A refusal answers its status and a word, and the reason goes to the operator's log. Admin routes answer 403 when no admin key is configured and 401 for a wrong one.

### Witness

| Route | What |
|---|---|
| `GET /healthz` | liveness |
| `GET /v1/witness/head` | the latest signed tree head |
| `GET /v1/witness/keys` | the key set the witness's heads and attestations verify under |
| `GET /v1/witness/inclusion` and `/consistency` | RFC 9162 proofs for a leaf, or between two sizes of the tree |
| `GET /v1/witness/entries` | the entries in a range, at most 1000 per answer |

The witness routes take no credential and only read. Its listener is on the loopback address by default, and its compose service in the stack-single launcher has no network at all.

## What it will not start without.

Anything missing or malformed refuses the start with exit code 2, and the message names the variable. Custody needs its data directory (mode 0700), its root key file, and a policy file of at most 1 MiB. Its listen address defaults to `127.0.0.1:4340`, and `KEYRYX_PUBLISH_AHEAD` sets how long a next or renewed key is published before it signs, 15 minutes by default.

The witness needs its own data directory (mode 0700, never custody's), its own root key file, and the bus directory it reads. The rest are optional: `KEYRYX_WITNESS_CHECKPOINTS` with a custody URL and a stream-key list, a records list for Trailryx data directories, a pin for the delegation root, an alert path, an interval (one minute by default), and an RFC 3161 time-stamping authority. Nothing calls an authority unless `KEYRYX_WITNESS_TSA_URL` is set.

Nothing has a default that signs. A key service that came up holding nothing would answer and sign nothing and look healthy, and one that came up with a default key would sign anything. Both refusals are deliberate.

## What it reads, and what it reports.

Every interval the witness reads, without writing to what it reads. It keeps the count of lines and bytes it has read and their SHA-256, not the bytes, in the prefix form of agent-passport SPEC 6.5.1, and it hashes each stream again from byte zero (hourly for a stream over 256 MiB). The prefix matters: the SPEC chain hash leaves `prev_hash` out, so a line rewritten with its successor re-linked would pass a chain check alone.

- **Streams.** A changed byte is `witness_stream_rewritten`. A stream holding fewer bytes than it was seen to hold is `witness_stream_truncated`. A new chain in the middle of a stream is `witness_chain_restarted`.

- **Checkpoints.** When a checkpoint directory is set, each record is checked by the steps of SPEC 6.5.1 against a key custody certifies for the stream's key name. A record that does not hold is `witness_checkpoint_invalid`; an unsigned one is `witness_checkpoint_unsigned`. While custody does not answer, a record waits.

- **Trailryx records.** For each store root it computes, the witness writes an ES384 attestation of trailryx's witness statement to its own volume. A sealed manifest that is rewritten or gone is `witness_root_equivocated`; a record that grows past a seal's worth with no new root is `witness_root_missing`.

Every finding is an agent-event in the alert file (by default `keyryx.ndjson` in the events directory), with counts and clipped hashes and never record content. Every observation is an entry in the witness's own RFC 9162 log over SHA-384, and each interval ends with a tree head signed by both halves of its key. The witness does not read custody's use log.

The witness pins the delegation root the first time it reads it, unless an operator sets `KEYRYX_WITNESS_DELEGATION_ROOT_PIN` beforehand. A different set served later is a high-severity finding and is not used until an operator pins it.

## Build, run, and check the outputs offline.

Build with `go build -o keyryx ./cmd/keyryx`, then start custody and the witness with their own variables, each as its own process and under its own account:

```
KEYRYX_DATA=/var/lib/keyryx KEYRYX_ROOT_KEY_FILE=/run/secrets/keyryx-root \
  KEYRYX_POLICY=/etc/keyryx/policy.json ./keyryx custody
KEYRYX_WITNESS_DATA=/var/lib/keyryx-witness KEYRYX_WITNESS_ROOT_KEY_FILE=/run/secrets/keyryx-witness-root \
  KEYRYX_WITNESS_EVENTS=/var/lib/agent-stack/events ./keyryx witness
```

The health checks are `/healthz` on the two listeners. Outputs can be checked with no service running:

```
# the witness log, against the key set it published
keyryx verify log --dir /var/lib/keyryx-witness --keys witness-keys.json
# streams and their checkpoints, against saved statements and the delegation root
keyryx verify streams --events events/ --checkpoints checkpoints/ \
  --statements statements/ --stream-keys 'wardryx.ndjson|wardryx-stream' \
  --roots delegation-root.json
```

Each check prints ok, weak or broken for each item and ends with VERIFIED (exit 0) or NOT VERIFIED (exit 1). A directory with nothing in it is reported as measured nothing, never as verified.

The image is published as `ghcr.io/taipanbox/keyryx` for linux/amd64 and linux/arm64, with no moving tag. The stack-single Compose file pins v0.1.3 by digest.

## What each release is.

- **v0.1.0**, tagged 2026-10-18: the first release. Custody and the witness, both roles, the offline checks, an SBOM and a build-provenance attestation. Its image carries no cosign signature.

- **v0.1.1**, tagged 2026-10-19: a patch on v0.1.0. It moves the shared wire-type import to agent-stack-go v2 and signs the image in the legacy `.sig` format that the cluster admission controller reads; that signature has not yet been checked with cosign. Nothing an operator sets moves with it, with one exception below.

- **v0.1.2**, tagged 2026-10-19: a patch on v0.1.1. The witness writes each attestation with mode 0640, in directories of mode 0750, so a record plane in the witness's group can read it; v0.1.1 wrote them 0600. It also moves agent-stack-go to v2.0.1, which changes no code. Attestations written by v0.1.1 keep their mode until an operator changes it once, as the release notes say.

- **v0.1.3**, tagged 2026-10-26: a patch on v0.1.2. The binary and the image are built with Go 1.27.3, which fixes GO-2026-6809 in crypto/x509 (reached through the time-stamping client, only when KEYRYX_WITNESS_TSA_URL is set). No key, statement, log, route or variable changes.

**An operator-visible change in v0.1.1.** Since agent-stack-go v2, a stream file this service creates is mode 0640, not 0644, so only its owner and its group can read it. A new stream is created only in a directory this service's account owns. A bus directory shared with other services, and not owned by this account, gets no new stream unless each file is created beforehand by the uid of the service that writes it. Check the owner of the bus directory and the mode of each stream before upgrading.

## What is not proven yet, stated here.

- The cosign signatures of v0.1.1, v0.1.2 and v0.1.3 have not been verified. The build-provenance attestation of each release has (gh attestation verify, 2026-10-19 for v0.1.0 to v0.1.2, 2026-10-26 for v0.1.3).

- No admin key is set, so custody refuses every rotation and revocation (403) until an operator sets one.

- Trailryx reads the witness's attestations into a pack only when its attestations folder is set to the witness's output. stack-up has set it by default since 2026-10-19 and stack-k8s since v1.6.1, tagged on 2026-10-20; stack-single does not set it. At keyryx v0.1.1 the witness wrote each attestation readable only by its own user, so a record plane running as another user could not open it; stack-up runs the witness and the record plane as one user, so it could. keyryx v0.1.2, tagged on 2026-10-19, writes them readable by the group, and stack-single, stack-up and stack-k8s now pin v0.1.3; stack-k8s runs the witness in the record plane's group. stack-single still does not set the attestations folder, so its packs carry no witness. None of this has run live.

- The store root is rebuilt by hand in the tests from trailryx's construction. It is checked against trailryx's source, not against a store that trailryx itself sealed in this repository.

- No public time-stamping authority has been asked. The client is tested against an authority the tests build.

- The first root is taken on first use unless the operator pins it. A real rotation of the delegation root reads as a changed root until an operator pins the new set, and no rotation has been run against a witness.

- The witness reads the bus and the record, not custody's use log, and custody writes no key rotation or revocation event yet.

- Vouchryx consumes key statements from 0.5.0 and, from 0.6.0, checks each one against a pinned root. TokenFuse consumes them for its checkpoint key from 1.18.0. Both are opt-in, no launcher switches either on, and no producer in a launcher writes signed checkpoints yet.

- The state MAC proves custody wrote a state, not that it is the latest. Whoever can write the data directory can restore an earlier copy of a record whose MAC still holds.

- Challenges live in memory, so a restart drops the outstanding ones.

- No consumer has yet authenticated with a projected service-account token on a real cluster; that path is tested against tokens the repository mints. On a kind cluster custody has served a bearer-key consumer and refused a wrong key (stack-k8s, 2026-10-18).

- No cloud key management. The root key is a file, and a KMS adapter would be a metered dependency, which is the operator's decision and not a default.

- In stack-single the witness is a separate user and volume; in stack-up both roles run as the user that started them. Either way, on one machine, it is not a separate trust domain. An off-host anchor closes that, and it is the operator's to switch on.

- Post-quantum signatures come from Go's standard library. Vouchryx from 0.6.0 checks the ML-DSA-65 half of a key statement; the shared verifier in agent-stack-go checks the classical half only. The key set's AKP form follows a JOSE draft, not an RFC.

## Back to the room.

The [Keyryx room](https://it-rat.com/services/keyryx.html) has the picture of the two roles and the common questions, and [the guides index](https://it-rat.com/guides.html) has the rest of the field.

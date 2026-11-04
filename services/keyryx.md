<!-- https://it-rat.com/services/keyryx.html -->

# Keyryx, the key custody and witness plane

> Key custody and a separate witness for the agent-governance record. Custody signs for granted consumers; the witness reads the record without writing to it.

One Go binary with two roles that never share a process. Custody holds the signing keys and signs for the consumers it grants a key. The witness reads the record without writing to it, remembers how much of it has been read and the hash of that, and reports when something it saw is gone. Neither role sits on a request path.

## Custody signs. The witness remembers.

The witness is there to disagree with custody if custody is ever compromised, so the two run as separate processes with separate keys and data directories, and the launcher gives each its own uid (stack-single does).

### Keys that stay in the store

Keys of three algorithms, each wrapped under AES-256-GCM with a key derived from the root key and bound to its name and id. A private half is never written in the clear, and a record that is moved or edited refuses to start.

### Consumers get what they were granted

A consumer authenticates one way: its own socket, a bearer key compared by digest, or a Kubernetes token. It signs only with the keys its policy grants. A refusal answers a status and nothing else, and the reason goes to the operator's log.

### Delegated keys, proven first

A high-rate signer generates its own key and proves it holds it. Custody certifies the key for a bounded life and publishes it with an overlap, so a verifier that caches the set keeps verifying through a rotation.

### A witness that remembers what it saw

The witness records how many bytes of each stream it has read and their SHA-256, and hashes the stream again from byte zero each interval (hourly for a stream over 256 MiB). It keeps no copy, so it can tell that a byte changed, never what it was. A changed byte is reported as a rewrite, a shorter stream as a truncation, and a new chain in the middle as a restart. Its own log is an RFC 9162 tree, and each head is signed with ECDSA P-384 and ML-DSA-65 side by side.

### A check you can run without the service

`keyryx verify` checks a witness log, or streams and their checkpoints, from files alone. An empty directory is reported as measured nothing, never as OK.

## Who signs, who watches, and who only reads.

Verifiers read the published key sets and never call custody for each request. In stack-single the witness reads the event bus and writes its findings to a volume of its own; by default the binary writes them to keyryx.ndjson on the bus.

## Stated rather than discovered later.

- It is on no request path. Enforcement points and agents never wait on it, and verifiers keep verifying when it is down.

- It makes no decision. It signs what a granted consumer asks, and it judges no tool call and refuses nothing for money.

- It issues no agent identity and holds no provider key.

- It never holds a delegated private key. That half stays with its consumer.

- It calls no paid service. A time-stamping authority is called only when an operator names one.

## Running in stack-single today.

- Custody and the witness run as separate containers in the stack-single Compose file, each under its own uid.

- Wardryx signs its approval tokens through Keyryx, so the approval key is held by custody.

- Vouchryx still signs its tokens with its own key file. The Keyryx signer for it is optional, and the launcher does not set it.

- The witness reads the event bus. The launcher sets no Trailryx record folder and no checkpoint folder, so the witness reads no Trailryx pack and no checkpoint yet.

- Trailryx packs are unsigned by default. The Keyryx root signer is opt-in, and the launcher leaves it off.

- Its findings go to keyryx.ndjson on a volume of their own, which Heraldyx and the console mount read only. Heraldyx mails the high ones (the medium ones go in the digest), and the console shows them as incidents. An operator can also check the witness log with keyryx verify.

- No admin key is set, so custody refuses every rotation and revocation (403) until an operator sets one.

## What is not proven yet.

- Two released consumers can ask for and renew a delegated key, each opt-in: Vouchryx from 0.5.0 (its token key) and TokenFuse from 1.18.0 (its checkpoint key). No launcher turns either on, and only Vouchryx's round trip has run against a real keyryx binary, once.

- The witness and custody share a host. In stack-single they are separate users, volumes and keys; in stack-up they share the user that started them. Either way they are not separate trust domains. An anchor off the host is the operator's to add, and no public time-stamping authority has been asked.

- The first witness read pins the delegation root that custody serves, unless an operator sets the pin before it starts.

- No consumer has yet authenticated with a projected service-account token on a real cluster; that path is tested against tokens the repository mints. On a kind cluster custody has served a bearer-key consumer and refused a wrong key (stack-k8s, 2026-10-18).

- Custody's use log is protected against edits in its middle, not against a rewrite from its first line, and the witness does not read it.

- The root key is a file. No cloud key management is wired in.

### Build the binary and read its version.

### The Keyryx guide

## Custody and the witness, in short

**Q: Is Keyryx a cloud key vault?**
No. It is a process you run beside the stack, with a wrapped key store on disk under a root key that is a file. It has no cloud key management. None is built: a cloud key adapter would be a metered dependency, which is an operator's decision and never a default.

**Q: Does a request wait on Keyryx?**
No. Verifiers cache the key sets it publishes and keep verifying when it is down. The synchronous calls are rare by design: an approval being granted, a seal, and the renewal of a delegated key.

**Q: Can the witness stop a bad write?**
No. It reads the record, reports what it finds and countersigns what it sees. Whatever follows from a finding is the operator's decision, and the finding stays in its own log either way.

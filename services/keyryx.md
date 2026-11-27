<!-- https://it-rat.com/services/keyryx.html -->

# Keyryx, the key custody and witness plane

> Key custody and a separate witness for the agent-governance record. Custody signs for granted consumers; the witness reads the record without writing to it.

One Go binary with two roles that never share a process. Custody holds the signing keys and signs for the consumers it grants a key. The witness reads the record without writing to it, remembers how much of it has been read and the hash of that, and reports when something it saw is gone. Neither role sits on a request path.

## Custody signs. The witness remembers.

The witness is there to disagree with custody if custody is ever compromised, so the two run as separate processes with separate keys and data directories, and the launcher gives each its own uid (stack-single does).

### Keys that stay in the store

Each private half is wrapped under AES-256-GCM with a key derived from the root key, and is never written in the clear.

### Consumers get what they were granted

A consumer authenticates one way and signs only with the keys its policy grants. A refusal answers a status and nothing else.

### Delegated keys, proven first

A high-rate signer proves it holds its own key, and custody certifies it for a bounded life with an overlap, so a rotation is never an outage.

### A witness that remembers what it saw

It keeps a count and a hash of every stream, never a copy, and reports a rewrite, a truncation or a restarted chain.

### A check you can run without the service

`keyryx verify` checks a witness log, or streams and their checkpoints, from files alone. An empty directory is reported as measured nothing, never as OK.

## Who signs, who watches, and who only reads.

Verifiers read the published key sets and never call custody for each request. In stack-single the witness reads the event bus and writes its findings to a volume of its own; by default the binary writes them to keyryx.ndjson on the bus.

## A signature waits for its log line. A missing byte gets noticed.

## What it refuses, where it runs, what it leaves open.

Keyryx is on no request path and decides nothing: verifiers check a cached key set, and custody signs only what a granted consumer asks. [In the guide](https://it-rat.com/keyryx-guide.html#refuses)

In stack-single custody and the witness are two containers under their own uids, and the witness, with no network, writes its findings to a file that Heraldyx mails and the console shows. [In the guide](https://it-rat.com/keyryx-guide.html#stack-single)

Rotation and revocation run only on custody's admin socket on the machine, and both roles share one host and one root key file until an operator adds an off-host anchor. [In the guide](https://it-rat.com/keyryx-guide.html#limits)

### Build the binary and read its version.

### The Keyryx guide

## Custody and the witness, in short

**Q: Is Keyryx a cloud key vault?**
No. It is a process you run beside the stack, with a wrapped key store on disk under a root key that is a file. It has no cloud key management. None is built: a cloud key adapter would be a metered dependency, which is an operator's decision and never a default.

**Q: Does a request wait on Keyryx?**
No. Verifiers cache the key sets it publishes and keep verifying when it is down. The synchronous calls are rare by design: an approval being granted, a seal, and the renewal of a delegated key.

**Q: Can the witness stop a bad write?**
No. It reads the record, reports what it finds and countersigns what it sees. Whatever follows from a finding is the operator's decision, and the finding stays in its own log either way.

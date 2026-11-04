<!-- https://it-rat.com/vouchryx-guide.html -->

# Vouchryx guide

> How Vouchryx proves and ends an agent's delegation, its seven endpoints, how to run and configure it, what changed in October and November 2026, and its limits.

The [Vouchryx room](https://it-rat.com/services/vouchryx.html) keeps the loop drawn end to end, the two kill switches, how to start it, and the common questions. This guide keeps the rest of what the room used to say: the gap it closes in full, the seven endpoints, the configuration it will not start without, a measured revocation run, what changed from 1 to 15 October 2026, and what is not proven yet.

- [At a glance](https://it-rat.com/vouchryx-guide.html#overview)

- [How it works](https://it-rat.com/vouchryx-guide.html#how-it-works)

- [The endpoints](https://it-rat.com/vouchryx-guide.html#surface)

- [Two kill switches](https://it-rat.com/vouchryx-guide.html#two-switches)

- [Configuration](https://it-rat.com/vouchryx-guide.html#configuration)

- [Running it](https://it-rat.com/vouchryx-guide.html#run)

- [What changed](https://it-rat.com/vouchryx-guide.html#changes)

- [What changed in November](https://it-rat.com/vouchryx-guide.html#changes-november)

- [Limits](https://it-rat.com/vouchryx-guide.html#limits)

## Vouchryx at a glance.

- **Status:** pre-1.0 · main is supported.

- **Core:** Go 1.27 · ES256, one runtime dependency.

- **API:** POST /v1/token on :4310.

- **Tokens:** 300s by default, capped at 3600.

- **Standards:** RFC 8693 · RFC 9449 DPoP.

- **Licence:** Apache-2.0.

### What it is

An RFC 8693 token exchange that mints a short-lived token carrying nested `act`, sender-constrained with RFC 9449 DPoP so a lifted token is useless to whoever lifted it. A revocation list enforcement points poll, and public keys anybody can verify against offline. Revoking a delegation ends the right to act on somebody's behalf at every enforcement point on its next poll of the list, 12 seconds by default at the gateway, whatever the token still says about its own expiry; a call admitted before that poll is not pulled back. The TokenFuse gateway polls that list, and so does Wardryx from 2.3.0; no other enforcement point does yet.

## The record said who acted for whom. Nothing proved it.

The Agent Passport spec disclaims two things on purpose. It is not an authentication protocol: the Passport names an agent, it does not prove possession. And it is not a freshness claim: the delegation chain records who acted on behalf of whom, not when. So the estate held the record of a delegation and pointed at a mechanism that did not exist. This is that mechanism, and it does not replace `on_behalf_of`; it makes it provable and lets it be ended.

### Proof of possession, per request

The minted token carries `cnf.jkt`, the thumbprint of the caller's own key. Spending it needs a fresh DPoP proof from that same key on every call, so a token copied out of a log buys nothing.

### Revocation an incident can use

By one token id, or by subject for every token an agent already holds. The list carries `as_of`, so an empty answer and an unreachable service are never the same answer to a machine reading it. Run end to end on a cluster: an agent revoked by subject mid-run was refused at the gateway 2.2 seconds later, with the gateway polling every second rather than its default of every 12.

### Verification without a round trip

Public keys at a JWKS endpoint, so an enforcement point verifies offline. That is also why there is no introspection endpoint, on purpose: it would put this service on the request path of every enforcement point at once.

## Seven endpoints, and one that deliberately does not exist.

| POST /v1/token | The exchange. A `subject_token` and an `actor_token` in, plus a DPoP header. Out comes a short-lived JWT with nested `act` and `cnf.jkt`. Since 2026-09-24 the same route also runs Cross App Access's jwt-bearer grant (RFC 7523, an ID-JAG in), closed unless VOUCHRYX_CLIENTS is set. It also runs the `client_credentials` grant: an agent enrolled in VOUCHRYX_AGENTS gets its own five-minute credential, bound to a key it proves with DPoP, closed while VOUCHRYX_AGENTS is unset. |
|---|---|
| POST /v1/revoke | By `jti` for one token, or by `subject` for every token an agent holds. Both `actor` and `reason` are required, because a revocation nobody can attribute is an outage rather than a decision. With `"ban": true` on a subject it is also a ban: nothing names that party again until the ban is lifted. |
| POST /v1/revoke/lift | Ends a ban. `subject`, `actor` and `reason` are required, and the subject must be banned. It never un-revokes: what the party held when it was banned stays revoked. |
| GET /v1/revocations | What enforcement points poll, carrying `as_of`. Each entry holds only what a verifier needs, `jti`, `subject`, `issued_before` and `expires`; who revoked a token and why stay in the operator's record. |
| GET /.well-known/jwks.json | Public keys. Verification is offline and stays offline. |
| GET /.well-known/oauth-authorization-server | RFC 8414 metadata for this service's own endpoints and grants. |
| GET /healthz | No credential. Answers 200 once the process is listening; with `VOUCHRYX_SIGNER=keyryx` it answers 503 until a working key is certified, so there it reads as readiness. |
| no introspection | Refused by design. Wardryx answers at a 3.2 ms p50 and nothing here is going to sit in front of that. |

## One stops the money. This one stops the authority.

[TokenFuse](https://it-rat.com/services/tokenfuse.html) refuses a call with a 402 before the provider bills, which is the right answer to a runaway. It is the wrong answer to a compromised delegation, where the spend is affordable and the problem is that the agent may act for somebody at all. Revoking ends that at every enforcement point on its next poll, and the token's own expiry has no say in it.

## It refuses to start rather than start permissive.

Three values are required and have no default: VOUCHRYX_ISSUER, VOUCHRYX_SIGNING_KEY (for the file signer; the Keyryx signer needs its own four values instead) and VOUCHRYX_TRUSTED_ISSUERS (unless VOUCHRYX_AGENTS enrols an agent). The listen address and the token lifetime have defaults, and the others switch optional features on. A missing or malformed value aborts the process and names the variable. The reason is the shape of the two failures: a token service that came up trusting nothing would issue nothing and look healthy, and one that came up trusting a default would issue everything.

In the stack-single launcher from 1.3.0 (released 2026-10-19), vouchryx starts on every default box and signs with its own key file, VOUCHRYX_SIGNING_KEY. Its optional Keyryx signer (VOUCHRYX_SIGNER=keyryx) is not set by the launcher, so tokens there are signed with the file key, not with a working key that Keyryx certifies.

The key sets of the trusted and workload issuers are read from files, and they are read again while the service runs, every `VOUCHRYX_JWKS_RELOAD_SECONDS` (thirty unless set, 0 never, a day at most). A file that cannot be used, because it is unreadable, gone, not JSON, an error page, empty of keys or holding a key with no `kty` or `kid`, never replaces the keys held: a failure is logged once while it lasts and the recovery once. A key removed from a readable file stops verifying. The service still fetches nothing: a refresh job writes the file, and the service reads it.

## Mint it, prove it, then end it.

An RFC 8693 exchange takes two signed input tokens and a DPoP proof whose public key travels in the JWS header, which is a JOSE client before it is a curl command. So the client ships with the service: `vouchryx-demo` makes the keys, performs the exchange and prints a proof.

```
# the whole local stack with the delegation door open, from TAIPANBOX/stack-up
./up.sh --with-delegation
```

```
# prints the token, its nested act and the key thumbprint bound to it
vouchryx-demo exchange -url http://127.0.0.1:4310 -idp-key idp.pem -kid idp-1 -iss https://idp.local -aud http://127.0.0.1:4310 -subject user://acme/ada -actor agent://acme/triage -holder-key holder.pem
```

### A measured run

Measured on 2026-09-27 on the forge lab, with a lab image of vouchryx rather than a published release: a call 0.9 seconds after the subject was revoked was still answered, and one 2.2 seconds after it was refused, and every call after that was refused too. 359 tests, and the repository gates that number against its own suite.

### A run against a real provider

The loop was run against a real OpenID provider, in throwaway realms with generated credentials: the exchange, the DPoP binding, hostile tokens, revoke, ban and lift, agent credentials, the hand-off, and a workload token the provider issued. A provider's token was exchanged once the provider wrote a `user://` or `agent://` URI into `sub`, and a service account's token from the provider was presented as an RFC 7523 assertion.

One phase of the run failed, rotation. The provider's new key was in its published set the second it was created, and a token signed by it was refused with `invalid_grant` (no key in the set has that kid) for the life of the process, because a key set file was read once, at start. Against the image published at the time the rotation phase failed; with the key set files followed while running, the whole run passes. The record and its commands are in `docs/live-oidc-run.md` in the repository.

## What changed from 1 to 15 October

0.1.0 to 0.2.0, one release. The same entry, beside every other service's, is in [what changed in the stack](https://it-rat.com/changes-2026-10.html#vouchryx).

| shipped in | what it does |
|---|---|
| v0.2.0 | The public revocation list no longer says who revoked a token or why. |

## What changed in November

| shipped in | what it does |
|---|---|
| v0.7.0 | Key set files are read again while the service runs (VOUCHRYX_JWKS_RELOAD_SECONDS), so a provider that rotates its signing key is followed without a restart. Found by a run against a real OpenID provider. |

## What it does not do, and what is not proven yet.

- The TokenFuse gateway polls that list, and so does Wardryx from 2.3.0; no other enforcement point does yet.

- Revoking a delegation ends the right to act on somebody's behalf at every enforcement point on its next poll of the list, 12 seconds by default at the gateway; a call admitted before that poll is not pulled back.

- The revocation timing on this page was measured on 2026-09-27 on the forge lab, with a lab image of vouchryx rather than a published release.

- The cluster run that refused a revoked agent 2.2 seconds later had the gateway polling every second rather than its default of every 12.

- The exchange takes only `user://` or `agent://` subjects, so a provider's opaque `sub` is refused; the provider has to write the URI into `sub`, which the live run did. A mapping for other providers is a naming decision, described in `docs/live-oidc-run.md`.

- There is no introspection endpoint, on purpose: it would put this service on the request path of every enforcement point at once.

- **Status:** pre-1.0, and main is supported.

## Back to the room.

The [Vouchryx room](https://it-rat.com/services/vouchryx.html) has the loop drawn end to end and the common questions, and [the guides index](https://it-rat.com/guides.html) has the field itself.

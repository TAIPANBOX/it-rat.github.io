<!-- https://it-rat.com/services/vouchryx.html -->

# Vouchryx, the delegation plane

> RFC 8693 token exchange with nested act, bound to the caller's key by DPoP. A delegation an agent can prove it holds, ended early wherever the list is polled.

An RFC 8693 token exchange that mints a short-lived token carrying nested `act`, sender-constrained with RFC 9449 DPoP so a lifted token is useless to whoever lifted it. A revocation list enforcement points poll, and public keys anybody can verify against offline.

## Mint, prove, verify, end.

Two signed tokens and a proof go in, and a short-lived token comes out. The dotted path is a revocation stopping that token before it expires. [In the guide](https://it-rat.com/vouchryx-guide.html#how-it-works)

## The record said who acted for whom. Nothing proved it.

The minted token carries cnf.jkt, the thumbprint of the caller's own key, so spending it needs a fresh DPoP proof from that key on every call. Enforcement points verify it offline against the published keys, which is why there is no introspection endpoint. [In the guide](https://it-rat.com/vouchryx-guide.html#how-it-works)

A person revokes one token by its id, or every token an agent holds by subject, naming an actor and a reason. The list carries as_of, so an empty answer and an unreachable service never read the same. [In the guide](https://it-rat.com/vouchryx-guide.html#surface)

Without its issuer, a signing key and the issuers it trusts (or an enrolled agent), the process aborts and names the variable. Key set files are read again while it runs, so a provider's rotated key is followed without a restart. [In the guide](https://it-rat.com/vouchryx-guide.html#configuration)

## One stops the money. This one stops the authority.

[TokenFuse](https://it-rat.com/services/tokenfuse.html) refuses a call with a 402 before the provider bills, which is the right answer to a runaway. It is the wrong answer to a compromised delegation, where the spend is affordable and the problem is that the agent may act for somebody at all.

## Mint it, prove it, then end it.

The client ships with the service: `vouchryx-demo` makes the keys, performs the exchange and prints a proof.

## What is not proven yet.

### Two enforcement points poll

The TokenFuse gateway polls the list, and so does Wardryx from 2.3.0; no other enforcement point does yet. [In the guide](https://it-rat.com/vouchryx-guide.html#limits)

### On the next poll

Revoking takes effect at each enforcement point on its next poll, 12 seconds by default at the gateway, and a call admitted before it is not pulled back. [In the guide](https://it-rat.com/vouchryx-guide.html#limits)

### Timed on a lab image

The revocation timing was measured on 2026-09-27 on the forge lab, with a lab image rather than a published release. [In the guide](https://it-rat.com/vouchryx-guide.html#limits)

### The Vouchryx guide

## Proving and ending a delegation

**Q: How is this different from just giving the agent an API key?**
A key names nobody and ends nowhere. This mints a short-lived token that says which human the agent is acting for, in a nested `act` claim, bound to the caller's own key so a copy of the token is useless. When the delegation should end, one revocation ends it at every enforcement point on its next poll of the list, rather than waiting for an expiry. Today the TokenFuse gateway polls that list, and so does Wardryx (from 2.3.0, when it is given the list's address); no other enforcement point does yet.

**Q: What happens to a token that is already in flight when we revoke it?**
Its next use is refused. The TokenFuse gateway polls the revocation list every 12 seconds by default (Wardryx every 30) and refuses anything on it, so the token's own expiry has no say; a call admitted before that poll is not pulled back, and a door that cannot reach the list keeps the last one it fetched and, past a minute, refuses by default. Measured on a live box: a proven chain answered 200, and after the revoke the same token answered 401.

**Q: Does this replace the delegation chain in the Passport?**
No, it is the half the Passport spec deliberately leaves out. The spec says plainly that it names an agent without proving possession, and records who acted for whom without saying when. This provides both, and the record still lives where it lived.

**Q: Why is there no introspection endpoint?**
Because it would put this service on the request path of every enforcement point at once. Verification is offline against published keys instead, and the policy plane keeps answering in single-digit milliseconds.

**Q: What does it do if it is configured wrong?**
It refuses to start and names the variable. A token service that came up trusting nothing would issue nothing and look healthy; one that came up trusting a default would issue everything. Neither failure should be quiet.

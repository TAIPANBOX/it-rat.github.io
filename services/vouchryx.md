<!-- https://it-rat.com/services/vouchryx.html -->

# Vouchryx, the delegation plane

> RFC 8693 token exchange with nested act, bound to the caller's key by DPoP. A delegation an agent can prove it holds, ended early wherever the list is polled.

An RFC 8693 token exchange that mints a short-lived token carrying nested `act`, sender-constrained with RFC 9449 DPoP so a lifted token is useless to whoever lifted it. A revocation list enforcement points poll, and public keys anybody can verify against offline.

## The record said who acted for whom. Nothing proved it.

### Proof of possession, per request

The minted token carries `cnf.jkt`, the thumbprint of the caller's own key. Spending it needs a fresh DPoP proof from that same key on every call.

### Revocation an incident can use

By one token id, or by subject for every token an agent already holds. The list carries `as_of`, so an empty answer and an unreachable service are never the same answer to a machine reading it.

### Verification without a round trip

Public keys at a JWKS endpoint, so an enforcement point verifies offline. That is also why there is no introspection endpoint, on purpose.

### It refuses to start rather than start permissive

Three values are required and have no default: VOUCHRYX_ISSUER, VOUCHRYX_SIGNING_KEY (for the file signer; the Keyryx signer needs its own four values instead) and VOUCHRYX_TRUSTED_ISSUERS (unless VOUCHRYX_AGENTS enrols an agent). A missing or malformed value aborts the process and names the variable.

### Run against a real provider

A live run with a real OpenID provider found that a provider which rotated its signing key was refused until the service restarted. The key set files are now read again while the service runs (VOUCHRYX_JWKS_RELOAD_SECONDS), and a file that cannot be used never replaces the keys held.

## Mint, prove, verify, end.

Two signed tokens and a proof go in, a short-lived one comes out, and the enforcement point verifies it without asking anybody. The dotted path is the one that matters in an incident: a revocation reaches the poller and the same token stops working before it expires.

## One stops the money. This one stops the authority.

[TokenFuse](https://it-rat.com/services/tokenfuse.html) refuses a call with a 402 before the provider bills, which is the right answer to a runaway. It is the wrong answer to a compromised delegation, where the spend is affordable and the problem is that the agent may act for somebody at all.

## Mint it, prove it, then end it.

The client ships with the service: `vouchryx-demo` makes the keys, performs the exchange and prints a proof.

## What is not proven yet.

- The TokenFuse gateway polls that list, and so does Wardryx from 2.3.0; no other enforcement point does yet.

- Revoking ends the right to act at every enforcement point on its next poll of the list, 12 seconds by default at the gateway; a call admitted before that poll is not pulled back.

- The revocation timing was measured on 2026-09-27 on the forge lab, with a lab image of vouchryx rather than a published release.

### The Vouchryx guide

## Proving and ending a delegation

**Q: How is this different from just giving the agent an API key?**
A key names nobody and ends nowhere. This mints a short-lived token that says which human the agent is acting for, in a nested `act` claim, bound to the caller's own key so a copy of the token is useless. When the delegation should end, one revocation ends it at every enforcement point on its next poll of the list, rather than waiting for an expiry. Today only the TokenFuse gateway polls that list; no other enforcement point does yet.

**Q: What happens to a token that is already in flight when we revoke it?**
Its next use is refused. Enforcement points poll the revocation list, every 12 seconds by default, and refuse anything on it, so the token's own expiry has no say; a call admitted before that poll is not pulled back, and a door that cannot reach the list keeps the last one it fetched and, past a minute, refuses by default. Measured on a live box: a proven chain answered 200, and after the revoke the same token answered 401.

**Q: Does this replace the delegation chain in the Passport?**
No, it is the half the Passport spec deliberately leaves out. The spec says plainly that it names an agent without proving possession, and records who acted for whom without saying when. This provides both, and the record still lives where it lived.

**Q: Why is there no introspection endpoint?**
Because it would put this service on the request path of every enforcement point at once. Verification is offline against published keys instead, and the policy plane keeps answering in single-digit milliseconds.

**Q: What does it do if it is configured wrong?**
It refuses to start and names the variable. A token service that came up trusting nothing would issue nothing and look healthy; one that came up trusting a default would issue everything. Neither failure should be quiet.

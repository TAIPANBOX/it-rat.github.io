<!-- https://it-rat.com/services/vouchryx.html -->

# Vouchryx, the delegation plane

> RFC 8693 token exchange with nested act, bound to the caller's key by DPoP. A delegation an agent can prove it holds, and can end before it expires at every point that polls the list.

An RFC 8693 token exchange that mints a short-lived token carrying nested `act`, sender-constrained with RFC 9449 DPoP so a lifted token is useless to whoever lifted it. A revocation list enforcement points poll, and public keys anybody can verify against offline. Revoking a delegation ends the right to act on somebody's behalf at every enforcement point on its next poll of the list, 12 seconds by default at the gateway, whatever the token still says about its own expiry; a call admitted before that poll is not pulled back.

## The record said who acted for whom. Nothing proved it.

The Agent Passport spec disclaims two things on purpose. It is not an authentication protocol: the Passport names an agent, it does not prove possession. And it is not a freshness claim: the delegation chain records who acted on behalf of whom, not when. So the estate held the record of a delegation and pointed at a mechanism that did not exist. This is that mechanism, and it does not replace `on_behalf_of`; it makes it provable and lets it be ended.

### Proof of possession, per request

The minted token carries `cnf.jkt`, the thumbprint of the caller's own key. Spending it needs a fresh DPoP proof from that same key on every call, so a token copied out of a log buys nothing.

### Revocation an incident can use

By one token id, or by subject for every token an agent already holds. The list carries `as_of`, so an empty answer and an unreachable service are never the same answer to a machine reading it. Run end to end on a cluster: an agent revoked by subject mid-run was refused at the gateway 2.2 seconds later, with the gateway polling every second rather than its default of every 12.

### Verification without a round trip

Public keys at a JWKS endpoint, so an enforcement point verifies offline. That is also why there is no introspection endpoint, on purpose: it would put this service on the request path of every enforcement point at once.

## Four endpoints, and one that deliberately does not exist.

| POST /v1/token | The exchange. A `subject_token` and an `actor_token` in, plus a DPoP header. Out comes a short-lived JWT with nested `act` and `cnf.jkt`. |
|---|---|
| POST /v1/revoke | By `jti` for one token, or by `subject` for every token an agent holds. Both `actor` and `reason` are required, because a revocation nobody can attribute is an outage rather than a decision. |
| GET /v1/revocations | What enforcement points poll, carrying `as_of`. Each entry holds only what a verifier needs, `jti`, `subject`, `issued_before` and `expires`; who revoked a token and why stay in the operator's record. |
| GET /.well-known/jwks.json | Public keys. Verification is offline and stays offline. |
| no introspection | Refused by design. Wardryx answers at a 3.2 ms p50 and nothing here is going to sit in front of that. |

## Mint, prove, verify, end.

Two signed tokens and a proof go in, a short-lived one comes out, and the enforcement point verifies it without asking anybody. The dotted path is the one that matters in an incident: a revocation reaches the poller and the same token stops working before it expires.

## One stops the money. This one stops the authority.

[TokenFuse](https://it-rat.com/tokenfuse.html) refuses a call with a 402 before the provider bills, which is the right answer to a runaway. It is the wrong answer to a compromised delegation, where the spend is affordable and the problem is that the agent may act for somebody at all. Revoking ends that at every enforcement point on its next poll, and the token's own expiry has no say in it.

## It refuses to start rather than start permissive.

Every value is required except the listen address, and none has a permissive default. A missing or malformed one aborts the process and names the variable. The reason is the shape of the two failures: a token service that came up trusting nothing would issue nothing and look healthy, and one that came up trusting a default would issue everything.

## Mint it, prove it, then end it.

An RFC 8693 exchange takes two signed input tokens and a DPoP proof whose public key travels in the JWS header, which is a JOSE client before it is a curl command. So the client ships with the service: `vouchryx-demo` makes the keys, performs the exchange and prints a proof.

Measured on 2026-08-27 on a clean box: a proven chain answered 200, and after a call to `/v1/revoke` the same token answered 401 with `reason=BadToken`. The control run is the part worth keeping: with the delegation door shut, that same revoked token answered 200, because nothing was looking at it. 218 tests, and the repository gates that number against its own suite.

## Proving and ending a delegation

**Q: How is this different from just giving the agent an API key?**
A key names nobody and ends nowhere. This mints a short-lived token that says which human the agent is acting for, in a nested `act` claim, bound to the caller's own key so a copy of the token is useless. When the delegation should end, one revocation ends it at every enforcement point on its next poll of the list, rather than waiting for an expiry.

**Q: What happens to a token that is already in flight when we revoke it?**
Its next use is refused. Enforcement points poll the revocation list, every 12 seconds by default, and refuse anything on it, so the token's own expiry has no say; a call admitted before that poll is not pulled back, and a door that cannot reach the list keeps the last one it fetched and, past a minute, refuses by default. Measured on a live box: a proven chain answered 200, and after the revoke the same token answered 401.

**Q: Does this replace the delegation chain in the Passport?**
No, it is the half the Passport spec deliberately leaves out. The spec says plainly that it names an agent without proving possession, and records who acted for whom without saying when. This provides both, and the record still lives where it lived.

**Q: Why is there no introspection endpoint?**
Because it would put this service on the request path of every enforcement point at once. Verification is offline against published keys instead, and the policy plane keeps answering in single-digit milliseconds.

**Q: What does it do if it is configured wrong?**
It refuses to start and names the variable. A token service that came up trusting nothing would issue nothing and look healthy; one that came up trusting a default would issue everything. Neither failure should be quiet.

<!-- https://it-rat.com/services/scopyx.html -->

# Scopyx, the egress plane

> Your agents already reach the web and nothing governs it. Scopyx decides every destination before anything leaves, and keeps origins rather than URLs.

Scopyx sits between an agent and whatever fetching tool you already run, and adds the four things that were missing: a decision before the request, a decision on every redirect, a bound on what comes back, and a record of the fetch and of the refusal.

## Five gates, in this order, and the order is the claim.

The verdicts run in this order: the scheme, the host, every address that name resolves to at the moment of the fetch, your policy plane, and last the site's own `robots.txt`. Pick a request and watch where it stops.

The name is resolved and your policy plane is asked before any verdict, so the cheapest refusal still costs one lookup and one policy question. What a refusal prevents is the fetch. A scheme or a host the rules refuse costs nothing, so those refusals happen while the request is still inside your own process. The site's own preference is asked last, which is the ordering that matters: a destination your policy refuses is never contacted at all, not even to read its `robots.txt`.

## The four things that were missing.

### And the socket goes where the decision looked

The checked addresses are pinned and the transport refuses to dial a host no decision covered, which makes it the floor under everything above it.

### It refuses to follow

The fetcher it ships with returns the redirect instead of following it. The target's name is looked up at the moment of the hop, never from anything remembered.

### Governed at the navigation is not governed per request

Every result says which of the two guarantees was in force, so a partial answer is visible as one rather than read as a complete one.

### Chained, so a deletion shows

Every line names its predecessor, in the same envelope the rest of the stack speaks. No identity, no record, and the skip is counted.

## It is not a browser, and that is the whole design.

Scopyx supplies no capability you do not already have. Point it at the fetching service you already run, through an HTTP endpoint that speaks scopyx's external contract (SCOPYX_EXTERNAL_ENDPOINT).

## A page is forty requests nobody named. Here is what stops them.

Two separate things stop a refused one, and they are not redundancy for its own sake. Switch either off and see.

Two mechanisms, and they are not the same kind of thing. The proxy is the floor: the browser is launched with no route to the network except it, so a refused destination is a socket that is never opened, and no flag or version of somebody else's browser can talk it out of that. CDP interception is the accountant: it sees the full URL of every request, including inside TLS, which the proxy cannot, so it produces the counts and the per-URL decisions. Where the two disagree the connection wins, because the connection is what carries bytes.

## A URL is personal data, and the record is built around that.

What is kept is the origin and a SHA-384, so two records can be compared without either holding the address.

The path and the query string are not dropped later or redacted later. The field is never built, so there is no window in which the event holds them and no code path that could log one by accident.

## Two images: default and -chromium.

## What it will not do, stated rather than discovered.

- No stealth, no CAPTCHA solving, no TLS-fingerprint matching, no bulk crawl, no image harvesting, and `robots.txt` is honoured.

- A vendor API needs an adapter in front of it, and this repository ships none.

### The Scopyx guide

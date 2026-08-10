<!-- https://it-rat.com/services/scopyx.html -->

# Scopyx, the egress plane

> Your agents already reach the web and nothing governs it. Scopyx decides every destination before anything leaves, and keeps origins rather than URLs.

Every other plane in the stack governs what your agents do to your own services: what they spend, what they may call, who they are. None of them watches the one direction that leads outside. An agent reads a page, and the page tells it what to do next. An agent posts a customer list to an address it found in a prompt. Scopyx sits between an agent and whatever fetching tool you already run, and adds the four things that were missing: a decision before the request, a decision on every redirect, a bound on what comes back, and a record of the fetch and of the refusal.

## Five gates, in this order, and the order is the claim.

The scheme, then the host, then every address that name resolves to at the moment of the fetch, then your policy plane, and last the site's own `robots.txt`. The first three are local and free, so a cheap refusal never becomes a network call. Your policy is asked fourth, which means a destination you refuse is never contacted at all, not even for its `robots.txt`. Pick a request and watch where it stops.

Nothing here is a network call until the fourth gate has answered. A scheme, a name and a set of addresses cost nothing to refuse, so the cheap refusals happen while the request is still inside your own process. The site's own preference is asked last, which is the ordering that matters: a destination your policy refuses is never contacted at all, not even to read its `robots.txt`.

## The diagram argues. This is the receipt.

Four real requests, one container, the published image against a fixture policy and the live internet. Watch where each stops: a name pointing inside your own deployment is refused before any policy runs, and the request that never became a request is the last row.

## A redirect is a destination the caller never named.

An allowed host answering 302 to a denied one is the oldest allowlist bypass there is, and it is invisible to any check that reads only the URL the caller passed.

### It refuses to follow

The fetcher it ships with returns the redirect instead of following it. Following inside the fetcher would be a second request that no decision preceded, which is exactly the bypass. Every HTTP client in every language does the opposite by default, which is why this is written down rather than assumed.

### Every hop is resolved again

The target's name is looked up at the moment of the hop, never from anything remembered. An address resolved a minute ago would satisfy the check while the fetch reached something else.

### And bounded twice

Your configured depth, and a ceiling the plane keeps regardless. Two servers pointing at each other is a fetch that never returns, and a fetch that never returns is worse than one that is refused, because nothing reports it.

## It is not a browser, and that is the whole design.

Scopyx supplies no capability you do not already have. Point it at the Firecrawl account you already pay for, the Browserbase you already run, or the fetcher it ships with, and the tool you own gains a decision, a bound and a record. Anyone proposing a feature here should ask whether it makes the fetch better or the fetch more governed. The first belongs in somebody else's product.

### The backend that needs nothing

The default fetcher wants no account, no API token and no browser on the host, so a box is governed on the day it is installed rather than the day somebody arranges a fetching service. It runs no JavaScript, and the result says so, because a page assembled in a browser arrives as the shell that assembles it.

### The one your invoice already covers

Wrapping a service you already run is the commercially important case and the least impressive code in the repository. A destination your policy refuses never reaches that service, so it never appears in your bill for it either.

## Governed at the navigation is not governed per request.

A fetch through a service you already run is decided before it is made, and then that service loads the page's images, fonts and scripts with nothing in between. The navigation was governed. The requests it caused were not. Every result says which of the two guarantees was in force, so a partial answer is visible as one rather than read as a complete one.

### A count nobody can supply is null

Zero says the page asked for nothing. Null says nobody knows. Reporting the second as the first claims perfect fidelity for exactly the backend that can see the least, and an agent that does not know it read half a page will report confidently on the half it got.

### Nothing extracted with a failure is not an empty page

It is an error. For a person, degrading to a blank frame is right. For an agent it is the worst failure available, because the model cannot tell the difference and you cannot either.

## A URL is personal data, and the record is built around that.

`https://crm.example/customers/12345?email=jane@example.com` is an address and also a name, an identifier and a contact detail. The path and the query string, which is exactly where an identifier or a session token lives, are never assembled into the event at all. What is kept is the origin and a SHA-384, so two records can be compared without either holding the address.

### Its own journal, its own volume

A component that can write the shared log can, once compromised, corrupt the trail it was adding to. This is the one part of the box that reaches the public internet on purpose, which makes it the last one that should be able to rewrite anybody else's record.

### Chained, so a deletion shows

Every line names its predecessor, in the same envelope the rest of the stack speaks. A journal that did not chain would look identical until somebody tried to verify it, which is the moment it matters and the moment it is too late.

### No identity, no record, and the skip is counted

A fabricated subject makes every downstream count wrong and puts a name on an alert that did not do the thing. A fetch with no authenticated agent behind it is not written, and the number of times that happened is reported rather than hidden.

## What it will not do, stated rather than discovered.

No stealth, no CAPTCHA solving, no TLS-fingerprint matching, no bulk crawl, no image harvesting, and `robots.txt` is honoured. It identifies itself as scopyx and never as a browser.

### Because of what this is for

Defensive tooling for an operator governing their own agents. A component that defeated a third party's controls would be the first thing here useful to somebody attacking a stranger, and that is a different product.

### And because of Article 5

The EU AI Act prohibits untargeted scraping of facial images to build recognition databases. A bulk-crawl mode is the feature that turns a governance tool into that, so there is not one.

### The one that needed code

Every other line above holds because no code path exists to do it, and an absence enforces itself. Honouring `robots.txt` is the only one that had to be written: group boundaries, longest match, Allow beating Disallow at equal length, and both wildcards. It reads as one item in a list and it is not one.

Scopyx is not an AI system under Article 3(1): it applies rules you wrote and infers nothing. Used beside one, it
 supplies evidence for Article 12 record-keeping and Article 14 human oversight. The wording here is "covers the
 requirements of Article 12", never "AI Act compliant", because there is no certification and no auditor behind
 those words, and a claim nobody can hold is worse than no claim.

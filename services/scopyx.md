<!-- https://it-rat.com/services/scopyx.html -->

# Scopyx, the egress plane

> Your agents already reach the web and nothing governs it. Scopyx decides every destination before anything leaves, and keeps origins rather than URLs.

Every other plane in the stack governs what your agents do to your own services: what they spend, what they may call, who they are. None of them watches the one direction that leads outside. An agent reads a page, and the page tells it what to do next. An agent posts a customer list to an address it found in a prompt. Scopyx sits between an agent and whatever fetching tool you already run, and adds the four things that were missing: a decision before the request, a decision on every redirect, a bound on what comes back, and a record of the fetch and of the refusal.

## Five gates, in this order, and the order is the claim.

The verdicts run in this order: the scheme, the host, every address that name resolves to at the moment of the fetch, your policy plane, and last the site's own `robots.txt`. Before the first verdict the plane resolves the name and asks your policy plane once per host, so a refused destination costs one lookup and one policy question. It is never fetched, and its `robots.txt` is never requested. Pick a request and watch where it stops.

The name is resolved and your policy plane is asked before any verdict, so the cheapest refusal still costs one lookup and one policy question. What a refusal prevents is the fetch. A scheme or a host the rules refuse costs nothing, so those refusals happen while the request is still inside your own process. The site's own preference is asked last, which is the ordering that matters: a destination your policy refuses is never contacted at all, not even to read its `robots.txt`.

## The diagram argues. This is the receipt.

Four real requests, one container, the published image against a fixture policy and the live internet. Watch where each stops: a name pointing inside your own deployment is refused before any policy runs, and the request that never became a request is the last row.

## A redirect is a destination the caller never named.

An allowed host answering 302 to a denied one is the oldest allowlist bypass there is, and it is invisible to any check that reads only the URL the caller passed. The same argument applies one layer down, to the name itself.

### It refuses to follow

The fetcher it ships with returns the redirect instead of following it. Following inside the fetcher would be a second request that no decision preceded, which is exactly the bypass. Most HTTP clients follow redirects by default, which is why this is written down rather than assumed.

### Every hop is resolved again

The target's name is looked up at the moment of the hop, never from anything remembered. An address resolved a minute ago would satisfy the check while the fetch reached something else.

### And the socket goes where the decision looked

Every HTTP client resolves the name again, inside the dialer, with no memory of what was checked, and a hostile zone answers differently between the two lookups for nothing. So the checked addresses are pinned and the transport refuses to dial a host no decision covered, which makes it the floor under everything above it: a code path that reached out without asking cannot open a socket.

### And bounded twice

Your configured depth, and a ceiling the plane keeps regardless. Two servers pointing at each other is a fetch that never returns, and a fetch that never returns is worse than one that is refused, because nothing reports it.

## It is not a browser, and that is the whole design.

Scopyx supplies no capability you do not already have. Point it at the fetching service you already run, through an HTTP endpoint that speaks scopyx's external contract (SCOPYX_EXTERNAL_ENDPOINT). A vendor API needs an adapter in front of it, and this repository ships none. Either way, the tool you own gains a decision, a bound and a record. Anyone proposing a feature here should ask whether it makes the fetch better or the fetch more governed. The first belongs in somebody else's product.

### The one that needs nothing

The default fetcher wants no account, no API token and no browser on the host, so a box is governed on the day it is installed rather than the day somebody arranges a fetching service. It runs no JavaScript, and the result names its backend as passthrough-http, which is how you can tell, because a page assembled in a browser arrives as the shell that assembles it.

### The one your invoice already covers

Wrapping a service you already run is the commercially important case and the least impressive code in the repository. A destination your policy refuses never reaches that service, so it never appears in your bill for it either.

### And a browser you installed

It runs the page's own JavaScript, so a document assembled in the browser arrives assembled. Nothing is bundled and nothing is downloaded: the image stays small, and a missing browser is refused at startup with a message about the browser rather than at the first fetch with a message about the network.

## A page is forty requests nobody named. Here is what stops them.

A rendering backend is the first one that fetches things the caller never asked for: fonts, images, scripts, each potentially a different host. Two separate things stop a refused one, and they are not redundancy for its own sake. Switch either off and see. Switch both off and the chromium test that asserts the refused server is never reached is the one that should fail. That run is not recorded yet.

Two mechanisms, and they are not the same kind of thing. The proxy is the floor: the browser is launched with no route to the network except it, so a refused destination is a socket that is never opened, and no flag or version of somebody else's browser can talk it out of that. CDP interception is the accountant: it sees the full URL of every request, including inside TLS, which the proxy cannot, so it produces the counts and the per-URL decisions. Where the two disagree the connection wins, because the connection is what carries bytes.

## Governed at the navigation is not governed per request.

A fetch through a service you already run is decided before it is made, and then that service loads the page's images, fonts and scripts with nothing in between. The navigation was governed. The requests it caused were not. Every result says which of the two guarantees was in force, so a partial answer is visible as one rather than read as a complete one.

### A count nobody can supply is null

Zero says the page asked for nothing. Null says nobody knows. Reporting the second as the first claims perfect fidelity for exactly the backend that can see the least, and an agent that does not know it read half a page will report confidently on the half it got.

### Nothing extracted with a failure is not an empty page

It is an error. For a person, degrading to a blank frame is right. For an agent it is the worst failure available, because the model cannot tell the difference and you cannot either.

## A URL is personal data, and the record is built around that.

`https://crm.example/customers/12345?email=jane@example.com` is an address and also a name, an identifier and a contact detail. The path and the query string, which is exactly where an identifier or a session token lives, are never assembled into the event at all. What is kept is the origin and a SHA-384, so two records can be compared without either holding the address.

The path and the query string are not dropped later or redacted later. The field is never built, so there is no window in which the event holds them and no code path that could log one by accident.

### Its own journal, its own volume

A component that can write the shared log can, once compromised, corrupt the trail it was adding to. This is the one part of the box that reaches the public internet on purpose, which makes it the last one that should be able to rewrite anybody else's record.

### Chained, so a deletion shows

Every line names its predecessor, in the same envelope the rest of the stack speaks. A journal that did not chain would look identical until somebody tried to verify it, which is the moment it matters and the moment it is too late.

### No identity, no record, and the skip is counted

A fabricated subject makes every downstream count wrong and puts a name on an alert that did not do the thing. A fetch with no authenticated agent behind it is not written, and the number of times that happened is reported rather than hidden.

## What it will not do, stated rather than discovered.

No stealth, no CAPTCHA solving, no TLS-fingerprint matching, no bulk crawl, no image harvesting, and `robots.txt` is honoured. It identifies itself as scopyx to robots.txt and on the default fetcher. A browser you installed sends its own user agent to the page, because the plane does not set one.

### Because of what this is for

Defensive tooling for an operator governing their own agents. A component that defeated a third party's controls would be the first thing here useful to somebody attacking a stranger, and that is a different product.

### And because of Article 5

The EU AI Act prohibits untargeted scraping of facial images to build recognition databases. A bulk-crawl mode is the feature that turns a governance tool into that, so there is not one.

### The one that needed code

Every other line above holds because no code path exists to do it, and an absence enforces itself. Honouring `robots.txt` is the only one that had to be written: group boundaries, longest match, Allow beating Disallow at equal length, and both wildcards. It reads as one item in a list and it is not one.

Scopyx applies rules you wrote and infers nothing, so we do not treat it as an AI system under Article 3(1). Whether a system you run is one is for your own legal review. Used beside one, it
 supplies evidence for Article 12 record-keeping and Article 14 human oversight. The wording here is "covers the
 requirements of Article 12", never "AI Act compliant", because there is no certification and no auditor behind
 those words, and a claim nobody can hold is worse than no claim.

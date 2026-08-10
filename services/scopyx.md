<!-- https://it-rat.com/services/scopyx.html -->

# Scopyx, the egress plane

> Your agents already reach the web. Whatever governs them does not see it. Scopyx decides every destination before anything leaves, decides every redirect again, and writes one tamper-evident record.

Every other plane in the stack governs what your agents do to your own services: what they spend, what they may call, who they are. None of them watches the one direction that leads outside. An agent reads a page, and the page tells it what to do next; an agent posts a customer list to an address in a prompt. Scopyx sits between an agent and whatever fetching tool you already run, and adds the four things that were missing: a decision before the request, a decision on every redirect, a bound on what comes back, and a record of both the fetch and the refusal.

## It is not a browser, and that is the whole design.

Scopyx supplies no capability you do not already have. Point it at the Firecrawl account you already pay for, the Browserbase you already run, or the fetcher it ships with, and the tool you own gains a decision, a bound and a record. Anyone proposing a feature should ask whether it makes the fetch better or the fetch more governed; the first belongs in somebody else's product.

### The backend that needs nothing

The default fetcher wants no account, no API token and no browser on the host, so a box is governed on the day it is installed rather than the day somebody arranges a fetching service. It runs no JavaScript, and the result says so, because a page assembled in a browser arrives as the shell that assembles it.

### The one your invoice already covers

Wrapping a service you already run is the commercially important case and the least impressive code in the repository. A destination your policy refuses never reaches that service, so it never appears in your bill for it either.

## The refusal happens before the request, and the order is the point.

Scheme, then host, then the addresses the name actually resolves to, and only then the policy plane. A cheap local refusal never becomes a network call, and a name that points inside your deployment is refused even when a policy would have allowed it, because policy languages talk about domains an agent may reach and none of them was written with the metadata endpoint in mind.

### A redirect is a destination nobody asked for

An allowed host answering 302 to a denied one is the oldest allowlist bypass there is, and it is invisible to any check that reads only the URL the caller passed. Every hop is resolved again and decided again. The fetcher it ships with refuses to follow a redirect at all; the layer above decides the target and then follows it, which is the opposite of what every HTTP client does by default.

### Refused, and it says which refusal

"The policy said no" and "the policy could not be asked" are different facts to whoever reads the trail, and collapsing them sends somebody to repair a machine that is fine. This plane fails closed and names which of the two it was.

## Governed at the navigation is not governed per request.

A fetch through a service you already run is decided before it is made, and then that service loads the page's images, fonts and scripts with nothing in between. The navigation was governed. The forty requests it caused were not. Every result carries which of the two guarantees was in force, so a partial answer is visible as one rather than read as a complete one.

### A count nobody can supply is null, never zero

Zero says the page asked for nothing. Null says nobody knows. Reporting the second as the first claims perfect fidelity for exactly the backend that can see the least, and an agent that does not know it read half a page reports confidently on the half it got.

## A URL is personal data, and the record is built around that.

`https://crm.example/customers/12345?email=jane@example.com` is an address and also a name, an identifier and a contact detail. The path and the query string, which is exactly where an identifier or a session token lives, are never assembled into the event at all. What is kept is the origin and a SHA-384, so two records can be compared without either holding the address.

### Its own journal, on its own volume

A component that can write the shared log can, once compromised, corrupt the trail it was adding to. This is the one part of the box that reaches the public internet on purpose, which makes it the last one that should be able to rewrite anybody else's record.

### The tool takes a URL and never a header

A free-form header parameter is a credential-laundering channel straight past a broker's inspection, which reads the arguments it understands and cannot read an opaque map of strings. Unknown arguments are refused by name, not ignored: ignoring is worse, because the caller believes their header was sent.

## What it will not do, stated rather than discovered.

No stealth, no CAPTCHA solving, no TLS-fingerprint matching, no bulk crawl, no image harvesting. It identifies itself as scopyx and never as a browser, and honours `robots.txt` by default.

Two of those are positioning and two are law-shaped. This is defensive tooling for an operator governing their own agents, and a component that defeated a third party's controls would be the first thing here useful to somebody attacking a stranger. Separately, EU AI Act Article 5(1)(e) prohibits untargeted scraping of facial images to build recognition databases, and a bulk-crawl mode is the feature that turns a governance tool into that.

### It is not an AI system, and it says so

Scopyx applies rules an operator wrote and infers nothing, so it is not an AI system under Article 3(1). Used beside one, it supplies evidence for Article 12 record-keeping and Article 14 human oversight. The wording throughout is "covers the requirements of Article 12", never "AI Act compliant": there is no certification and no auditor behind those words, and a claim nobody can hold is worse than no claim.

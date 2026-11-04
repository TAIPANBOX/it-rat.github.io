<!-- https://it-rat.com/scopyx-guide.html -->

# Scopyx guide

> How Scopyx decides an agent's web egress, how to run its two images, what changed from 1 to 15 October 2026, and what it will not do, in full.

The [Scopyx room](https://it-rat.com/services/scopyx.html) keeps the request in flight, the two mechanisms you can switch off, what the record keeps, and how to start it. This guide keeps the rest of what the room used to say: the measured run behind the gates, redirects, the backends it decides over, what a result admits, how to run and configure it, what changed from 1 to 15 October 2026, and what it will not do.

- [At a glance](https://it-rat.com/scopyx-guide.html#overview)

- [How it works](https://it-rat.com/scopyx-guide.html#how-it-works)

- [Redirects](https://it-rat.com/scopyx-guide.html#redirects)

- [What it decides over](https://it-rat.com/scopyx-guide.html#backends)

- [Two mechanisms in a browser](https://it-rat.com/scopyx-guide.html#mechanisms)

- [What the answer admits](https://it-rat.com/scopyx-guide.html#fidelity)

- [What is kept](https://it-rat.com/scopyx-guide.html#record)

- [Running it](https://it-rat.com/scopyx-guide.html#run)

- [Behind the broker](https://it-rat.com/scopyx-guide.html#broker)

- [What changed](https://it-rat.com/scopyx-guide.html#changes)

- [What changed in November](https://it-rat.com/scopyx-guide.html#changes-november)

- [Limits](https://it-rat.com/scopyx-guide.html#limits)

## Scopyx at a glance.

- **Shipped:** v1.2.0, two images (default and -chromium).

- **Core:** Go 1.27 · one direct dependency.

- **One way out:** http and https, and nothing else.

- **Fails:** closed, and says which refusal.

- **Keeps:** the origin and a hash, not the URL unless you opt in.

- **Licence:** Apache-2.0.

### What it is

Every other plane in the stack governs what your agents do to your own services: what they spend, what they may call, who they are. None of them watches the one direction that leads outside. An agent reads a page, and the page tells it what to do next. An agent posts a customer list to an address it found in a prompt. Scopyx sits between an agent and whatever fetching tool you already run, and adds the four things that were missing: a decision before the request, a decision on every redirect, a bound on what comes back, and a record of the fetch and of the refusal.

## Five gates, in this order, and the order is the claim.

The verdicts run in this order: the scheme, the host, every address that name resolves to at the moment of the fetch, your policy plane, and last the site's own `robots.txt`. Before the first verdict the plane resolves the name and asks your policy plane once per host, so a refused destination costs one lookup and one policy question. It is never fetched, and its `robots.txt` is never requested. The [room](https://it-rat.com/services/scopyx.html#flight) runs four requests through the gates; pick one and watch where it stops.

### The diagram argues. This is the receipt.

Four real requests, one container, the published image against a fixture policy and the live internet. Watch where each stops: a name pointing inside your own deployment is refused before any policy runs, and the request that never became a request is the last row.

The third row is the one worth reading twice. The fixture policy said **allow**, and it was refused anyway. Policy languages talk about domains an agent may reach, and none of them was written with the cloud metadata endpoint in mind: an agent that can be talked into fetching that address reads the credentials of whatever it runs on. The fourth is not a fetch at all. A free-form header parameter is a credential-laundering channel straight past a broker's inspection, so the tool has no field for one, and an unknown argument is refused by name rather than ignored.

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

A rendering backend is the first one that fetches things the caller never asked for: fonts, images, scripts, each potentially a different host. Two separate things stop a refused one, and they are not redundancy for its own sake. Switch either off and the refused server is still never reached; switch both off and it is reached once, and the chromium test that asserts otherwise goes red.

The two switches are on the [room](https://it-rat.com/services/scopyx.html#mechanisms).

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

## Two images: default and -chromium.

```
# full command, environment and volume: https://github.com/TAIPANBOX/scopyx#run-it
# it refuses to start bound wide with no credentials, deliberately
```

```
# the -chromium image, the same service with a browser: https://github.com/TAIPANBOX/scopyx#backends
# 267 MB to pull against 3.5 MB (measured on v0.1.2, 2026-08-10)
```

### Configuration the room names

- **SCOPYX_EXTERNAL_ENDPOINT:** point it at the fetching service you already run, through an HTTP endpoint that speaks scopyx's external contract. A vendor API needs an adapter in front of it, and this repository ships none.

- **SCOPYX_RETAIN=payload:** turning retention on is a decision, and the field it writes is called url_unprotected rather than url. There is no subject-keyed payload plane here, so a field called url would imply one and a reader would assume a protection that does not exist.

- **SCOPYX_ACCEPT_KEY_IN_META=1:** read a tools/call credential from the call's own metadata instead of the header, for a plane that sits behind the TokenFuse MCP broker. Off by default.

## The key can come through the TokenFuse MCP broker.

Scopyx knows an agent by the key it presents in the `X-Scopyx-Key` header. The TokenFuse MCP broker forwards a call with nothing of the caller's, so a plane behind it never sees that header, and an agent that holds the key can go round the broker. Letting the key come through the broker means the broker can put a run's label on the act itself rather than on a tool name the agent reported; the [TokenFuse guide](https://it-rat.com/tokenfuse-guide.html#how-it-works) has that half.

With `SCOPYX_ACCEPT_KEY_IN_META=1` the door reads a `tools/call` credential from `params._meta["scopyx/key"]`. The agent writes a `{{secret:NAME}}` handle, the broker fills it in on the last hop, and the agent never holds the key. The header wins when both are sent, the entry is taken out of the request at the door so nothing past it holds the key, and a `tools/call` with no id still needs a credential: this server dispatches on the method, so a missing id is not read as a notification.

It is off by default, and then the door is the header, checked before the body, as it was. Nothing in Scopyx turns the broker on; that is deployment wiring. With the switch on, the door reads a bounded request body from whoever reaches the port, so the port belongs on a network only the broker reaches.

## What changed from 1 to 15 October

No release in the window, still 1.0.1. The same entry, beside every other service's, is in [what changed in the stack](https://it-rat.com/changes-2026-10.html#scopyx).

- Documentation and toolchain only: the Go toolchain moved to 1.27.2, the shared library pin moved to 1.3.0, the secret scan runs on every pull request, and the README was corrected against the code.

## What changed in November

| shipped in | what it does |
|---|---|
| v1.2.0 | The key can come through the TokenFuse MCP broker: SCOPYX_ACCEPT_KEY_IN_META=1 reads a tools/call credential from the call's metadata, as a handle the broker fills in. Off by default. |

## What it will not do, stated rather than discovered.

No stealth, no CAPTCHA solving, no TLS-fingerprint matching, no bulk crawl, no image harvesting, and `robots.txt` is honoured. It identifies itself as scopyx to robots.txt and on the default fetcher. A browser you installed sends its own user agent to the page, because the plane does not set one.

### Because of what this is for

Defensive tooling for an operator governing their own agents. A component that defeated a third party's controls would be the first thing here useful to somebody attacking a stranger, and that is a different product.

### And because of Article 5

The EU AI Act prohibits untargeted scraping of facial images to build recognition databases. A bulk-crawl mode is the feature that turns a governance tool into that, so there is not one.

### The one that needed code

Every other line above holds because no code path exists to do it, and an absence enforces itself. Honouring `robots.txt` is the only one that had to be written: group boundaries, longest match, Allow beating Disallow at equal length, and both wildcards. It reads as one item in a list and it is not one.

### What it claims under the AI Act

Scopyx applies rules you wrote and infers nothing, so we do not treat it as an AI system under Article 3(1). Whether a system you run is one is for your own legal review. Used beside one, it supplies evidence for Article 12 record-keeping and Article 14 human oversight. The wording here is "covers the requirements of Article 12", never "AI Act compliant", because there is no certification and no auditor behind those words, and a claim nobody can hold is worse than no claim.

### What is not proven or not shipped

- A vendor API needs an adapter in front of it, and this repository ships none.

- The default fetcher runs no JavaScript: a page assembled in a browser arrives as the shell that assembles it.

## Back to the room.

The [Scopyx room](https://it-rat.com/services/scopyx.html) has the request in flight, the two switches and the record, and [the guides index](https://it-rat.com/guides.html) has the field itself.

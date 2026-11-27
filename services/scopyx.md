<!-- https://it-rat.com/services/scopyx.html -->

# Scopyx, the egress plane

> Your agents already reach the web and nothing governs it. Scopyx decides every destination before anything leaves, and keeps origins rather than URLs.

Scopyx sits between an agent and whatever fetching tool you already run, and adds the four things that were missing: a decision before the request, a decision on every redirect, a bound on what comes back, and a record of the fetch and of the refusal.

## Five gates, in this order, and the order is the claim.

The verdicts run in this order: the scheme, the host, every address that name resolves to at the moment of the fetch, your policy plane, and last the site's own `robots.txt`. Pick a request and watch where it stops.

The name is resolved and your policy asked before any verdict, so even the cheapest refusal costs one lookup and one policy question. The site's own `robots.txt` is asked last, so a destination your policy refuses is never contacted at all.

## The four things that were missing.

### And the socket goes where the decision looked

The checked addresses are pinned and the transport refuses to dial a host no decision covered, which makes it the floor under everything above it.

### Every hop is decided again

The fetcher hands each redirect back, and all five gates run again on the new destination, its name looked up afresh.

### Governed at the navigation is not governed per request

Every result says which of the two guarantees was in force, so a partial answer is visible as one rather than read as a complete one.

### Chained, so a deletion shows

Every line names its predecessor, so a deleted line shows, and a fetch with no identity is not written but counted.

## It is not a browser, and that is the whole design.

Scopyx supplies no capability you do not already have. Point it at the fetching service you already run, through an HTTP endpoint that speaks scopyx's external contract (SCOPYX_EXTERNAL_ENDPOINT).

## A page is forty requests nobody named. Here is what stops them.

Two separate things stop a refused one, and they are not redundancy for its own sake. Switch either off and see.

The proxy is the floor: the browser has no route except it, so a refused destination is a socket never opened. CDP interception is the accountant: it sees every full URL, even inside TLS, and produces the counts.

## A URL is personal data, and the record is built around that.

What is kept is the origin and a SHA-384, so two records can be compared without either holding the address.

The path and the query string are not dropped later or redacted later. The field is never built, so there is no window in which the event holds them and no code path that could log one by accident.

## Two images: default and -chromium.

## What it will not do, stated rather than discovered.

### No stealth, no crawl

No stealth, no CAPTCHA solving, no TLS-fingerprint matching, no bulk crawl, no image harvesting, and `robots.txt` is honoured.

### No vendor adapter

A vendor API needs an adapter in front of it, and this repository ships none.

### The Scopyx guide

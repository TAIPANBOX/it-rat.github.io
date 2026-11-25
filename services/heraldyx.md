<!-- https://it-rat.com/services/heraldyx.html -->

# Heraldyx, the alerts plane

> The part of the agent stack that writes to you: it reads the event log, decides what is worth a human tonight, and mails it with links into your console.

Heraldyx reads the shared event log the others already write, decides which of those events a human should hear about tonight rather than tomorrow, and sends one mail. It comes from your own box, and it carries links into your own console.

## A hundred and twenty events arrive. Twenty-one messages leave.

A scripted run of scripts/burst-demo.sh: 120 events into the real binary with the default limits. Watch where the other hundred stop.

## Five steps, in this order, and the order is the point.

The decision layer is a pure function over an event and a few counters. It performs no I/O at all, which is what makes the awkward cases (a burst, a restart, a clock that moved) testable without a mail server. A provider outage is one mail per window and not one per failed call: a dependency_failed repeats on the dependency, not on the run.

## Four short paragraphs, and three links that are views.

What happened with its numbers, what the box already did about it, what happens if nobody acts, and where to look. Nothing in it is text a model wrote.

**Q: 1 
 
 
 A new message from your box 
 prod-box · 02:14 · budget_exhausted 
 
 Plain text, no images, no tracking pixel, and no button that acts. Open it to read the whole thing, headers included. 
 open ↗**

### The links are views, never actions

A link that acts is an unauthenticated capability held by anyone who sees or forwards the message. You sign in at the console, and a destructive action asks for your passkey there.

### Identifiers and numbers, never content

Mail leaves your perimeter through a server nobody here controls, so the renderer allows twenty-two named keys and then checks the shape of every value on top.

### Who is answerable comes from a passport

Not from the event, which carries the agent and who it acted for, and neither of those is the owner. No passport means no owner line rather than a guess.

## Every message it sent, sealed, on a volume the planes cannot reach.

Every message leaves one hash-chained record behind it, in the envelope the rest of the stack speaks, so when it was sent can be proved.

## The boundaries, stated rather than discovered at three in the morning.

### It does not queue

A message that cannot be delivered is logged, recorded as a refusal and dropped. Quiet hours hold alerts below critical, and a critical is never held.

### Delegations have no sentences yet

A mail about a Vouchryx delegation event says the box has no description for it yet.

### The source check has an edge

A process that creates a plane's file first, or a writer forging its own stream, gets past it. The checkpoint gate narrows that, and it is off by default.

## Twelve planes write the log it reads.

It mails about what other planes wrote, so its reach grows with theirs.

### The Heraldyx guide

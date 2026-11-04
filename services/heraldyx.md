<!-- https://it-rat.com/services/heraldyx.html -->

# Heraldyx, the alerts plane

> The part of the agent stack that writes to you: it reads the event log, decides what is worth a human tonight, and mails it with links into your console.

Heraldyx reads the shared event log the others already write, decides which of those events a human should hear about tonight rather than tomorrow, and sends one mail. It comes from your own box, and it carries links into your own console.

## A hundred and twenty events arrive. Twenty-one messages leave.

This is a scripted scenario: `scripts/burst-demo.sh` in the repository feeds 120 events to the real binary with the default limits and counts what comes out. Watch where the other hundred stop.

## Four checks, in this order, and the order is the point.

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

"We wrote to you at 03:14, and your mail server took it at 03:14:02" is a claim somebody eventually has to prove, in an argument they did not choose. So every message leaves one hash-chained record behind it, in the same envelope the rest of the stack speaks.

## The boundaries, stated rather than discovered at three in the morning.

- It does not queue: a message that cannot be delivered is logged, written into the dispatch record as a refusal, and dropped. Quiet hours and maintenance windows are holds, not a queue: they hold alerts below critical and, when the hours or the window end, send one mail saying how many were held. A critical is never held.

- Vouchryx's delegation events have no sentences yet, so a mail about one says the box has no description for the event until one is written.

- The source check does not stop a process that creates a plane's file before that plane does, or a writer forging its own stream. The checkpoint gate, from v0.8.0, narrows that for streams a producer signs: with HERALDYX_CHECKPOINT_GATE=on, a stream is read only while a checkpoint signed by a pinned key covers it. It is off by default, it trusts a pinned key until an operator removes it, and it holds only if each producer alone can write its stream and checkpoints. No launcher has a producer writing signed checkpoints yet.

## Twelve planes write the log it reads.

This plane mails about what other planes wrote, so its reach grows when theirs does. Twelve planes write the shared log, and the Keyryx witness's findings file is read beside it. [Vouchryx](https://it-rat.com/services/vouchryx.html) reports a delegation issued, denied or revoked, and [CostCrew](https://it-rat.com/services/costcrew.html) reports spend spikes, budget thresholds and every move its crew makes on a finding.

### The Heraldyx guide

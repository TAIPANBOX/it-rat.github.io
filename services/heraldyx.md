<!-- https://it-rat.com/services/heraldyx.html -->

# Heraldyx, the alerts plane

> The part of the agent stack that writes to you: it reads the shared event log, decides what is worth a human tonight, and mails it with one link.

Every other plane in the stack records what happened. None of them wakes anybody. Heraldyx reads the shared event log the others already write, decides which of those events a human should hear about tonight rather than tomorrow, and sends one mail. It comes from your own box, and it carries a link into your own console. It reads a file and sends mail: that narrowness is the design, because this is the one component of the box allowed to open a connection to anything outside it.

## A hundred and twenty events arrive. Twenty-one messages leave.

This is a simulation of a real run: `scripts/burst-demo.sh` in the repository feeds 120 events to the actual binary with the default limits and counts what comes out. Watch where the other hundred stop. An alerting system that forwards everything teaches its operator to filter the sender to trash, and then the one that mattered is in trash too.

## Four checks, in this order, and the order is the point.

The decision layer is a pure function over an event and a few counters. It performs no I/O at all, which is what makes the awkward cases (a burst, a restart, a clock that moved) testable without a mail server. The last cell was redrawn after a run on 2026-09-17: the v0.2.3 image sent one notice at the ceiling and then nothing for 28 minutes of high and critical events. Since v0.2.4 a critical passes the ceiling and whatever is held is summarised every ten minutes until the hour turns; the launchers pin v0.3.0.

## Four short paragraphs, and one link that is a view.

What happened with its numbers, what the box already did about it, what happens if nobody acts, and where to look. Nothing in it is text a model wrote.

**Q: 1 
 
 
 A new message from your box 
 prod-box · 02:14 · budget_exhausted 
 
 Plain text, no images, no tracking pixel, and no button that acts. Open it to read the whole thing, headers included. 
 open ↗**

### The link is a view, never an action

A link that acts is an unauthenticated capability held by anyone who sees or forwards the message. Mail gateways also prefetch links, which would fire the action before a human read the sentence next to it. You sign in at the console, and a destructive action asks for your passkey there.

### Identifiers and numbers, never content

An event's data can hold anything a producer put there, and some producers sit next to prompts, model output and matched secrets. Mail leaves your perimeter through a server nobody here controls, so the renderer allows nineteen named keys and then checks the shape of every value on top. A live secret is perfectly identifier-shaped, so the key list is what stands between it and your inbox.

### Who is answerable comes from a passport

Not from the event, which carries the agent and who it acted for, and neither of those is the owner. No passport means no owner line rather than a guess: naming the wrong team at three in the morning is worse than naming nobody at all.

## Every message it sent, sealed, on a volume the planes cannot reach.

"We wrote to you at 03:14, and your mail server took it at 03:14:02" is a claim somebody eventually has to prove, in an argument they did not choose. So every message leaves one hash-chained record behind it, in the same envelope the rest of the stack speaks.

### "Accepted", never "delivered"

What the process observes is a mail server taking the message. Whether it reached a mailbox, a spam folder, or a filter that drops it silently is not knowable from here, so the record does not say it.

### A chain of one is not "verified"

The first record has no predecessor to hash, so editing it is undetectable. The tool says so instead of reporting a good chain. A check that cannot fail is worse than no check, because it is louder.

### It reports, and never repairs

A tool that could mend the chain would be a tool that could forge it. It exits non-zero on a break, so a deployment check can use it directly.

## The boundaries, stated rather than discovered at three in the morning.

### It does not queue

A message that cannot be delivered is logged, written into the dispatch record as a refusal, and dropped. A retry queue inside the one process allowed out would be the opposite of the design, and the event itself is still in the log, which outlives this process.

### It does not talk to any plane

No API, no credential, no client. It holds nothing that could act on an agent. If a fact is not in the event log, heraldyx does not know it.

### It does not report anything about a whole organisation

The shared envelope requires an agent id, so a fact about an org has no subject to travel under, and no producer is allowed to invent one to make it fit. Those facts live in the console and in each plane's own API. A mail whose subject line named an agent that had not done the thing would be worse than silence.

### It does not carry history

A first run starts at the end of the log. A month of old incidents arriving at once is how an operator learns to filter this sender to trash.

## Two more sources arrived on the bus.

This plane mails about what other planes wrote, so its reach grows when theirs does. [Vouchryx](https://it-rat.com/vouchryx.html) reports a delegation issued, denied or revoked, and [CostCrew](https://it-rat.com/costcrew.html) reports spend spikes, budget thresholds and every move its crew makes on a finding. Both are in the shared registry, so a mail about either needs no new code here.

Since v0.3.0 a line counts as the source it claims only when the file it came from may carry that source. Each plane's file carries its own name, `HERALDYX_STREAMS` declares anything else, and a line in the wrong file is refused, counted and raised once as `foreign_source`; a file nobody declared is raised once as `unknown_stream`. It does not stop a process that creates a plane's file before that plane does, or a writer forging its own stream: only signing closes those.

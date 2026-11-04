<!-- https://it-rat.com/heraldyx-guide.html -->

# Heraldyx guide

> How Heraldyx decides what reaches a human, what its mail may carry, what its dispatch record proves, what changed from v0.7.0 to v0.9.0, and its boundaries.

The [Heraldyx room](https://it-rat.com/services/heraldyx.html) keeps the burst replay, the drawing of the four checks, the sample mail and the short version of each part. This guide keeps the rest of what the room used to say: why the checks run in that order and what changed in them, what a mail may carry and who it names, what the dispatch record proves, who else writes to the log it reads, what shipped from v0.7.0 to v0.9.0, and the boundaries in full.

- [At a glance](https://it-rat.com/heraldyx-guide.html#overview)

- [How it works](https://it-rat.com/heraldyx-guide.html#how-it-works)

- [What actually arrives](https://it-rat.com/heraldyx-guide.html#the-mail)

- [The dispatch record](https://it-rat.com/heraldyx-guide.html#the-record)

- [Running it](https://it-rat.com/heraldyx-guide.html#run)

- [Who else writes to the log](https://it-rat.com/heraldyx-guide.html#sources)

- [What changed in November](https://it-rat.com/heraldyx-guide.html#changes-november)

- [What changed](https://it-rat.com/heraldyx-guide.html#changes)

- [Limits](https://it-rat.com/heraldyx-guide.html#limits)

## Heraldyx at a glance.

- **Your agents run on your infrastructure.** This is the part that writes to you.

- **One way out:** it reads the log, speaks SMTP, and nothing else.

- **Limits:** a severity floor, a dedup window of 10 minutes, and 20 mails an hour.

- **Leaves behind:** a hash-chained dispatch record.

- **Core:** Go, with two direct dependencies (the shared agent-stack-go contract and a JSON canonicaliser).

- **Licence:** Apache-2.0.

### What it is

Every other plane in the stack records what happened. None of them wakes anybody. Heraldyx reads the shared event log the others already write, decides which of those events a human should hear about tonight rather than tomorrow, and sends one mail. It comes from your own box, and it carries links into your own console. It reads a file and sends mail: that narrowness is the design, because this is the one component of the box allowed to open a connection to anything outside it.

## Four checks, in this order, and the order is the point.

The decision layer is a pure function over an event and a few counters. It performs no I/O at all, which is what makes the awkward cases (a burst, a restart, a clock that moved) testable without a mail server. The last cell of the room's drawing was redrawn after a run on 2026-09-17: the v0.2.3 image sent one notice at the ceiling and then nothing for 28 minutes of high and critical events. Since v0.2.4 a critical passes the ceiling and whatever is held is summarised every ten minutes until the hour turns; the launchers pin v0.8.2 on their main branches.

### A provider that is down is one mail, not one per call

For `dependency_failed` the dedup key is the dependency that failed and what the gateway did about it, not the run. A provider that is down fails every call that reaches it, and every call is its own run, so keyed on the run an hour of outage was one mail per call up to the hourly ceiling and a summary of the rest. Keyed on the dependency it is one mail per window. The key is read from the event's own `data.dependency` and `data.effect`, for a provider that fails calls it reads `dependency_failed:dependency/provider/call-failed`, and it is what an acknowledgement is made against and what the mail prints, so acknowledging a provider outage holds the whole storm.

The effect is part of the key because the outcomes want opposite responses. A gateway that fails open lets calls through with no policy on them, and that must not hide behind an earlier mail about calls that were refused. Only the type `dependency_failed` and only the event contract's own words qualify. No data, an unknown dependency, a value that is not text, a path-like or oversized value, or another type carrying the same field keeps the key of its run, so a field read from a log this process does not own can never fold anything into anything. The event contract does not change, no data key is added to what the mail may print, and the link in the mail points where it did.

The Cloud side of the same outage is [TokenFuse](https://it-rat.com/services/tokenfuse.html)'s one incident per failing provider. The two are independent: this one changes only what is mailed.

### A hundred and twenty events arrive. Twenty-one messages leave.

The room's replay is a scripted scenario: `scripts/burst-demo.sh` in the repository feeds 120 events to the real binary with the default limits and counts what comes out. Watch where the other hundred stop. An alerting system that forwards everything teaches its operator to filter the sender to trash, and then the one that mattered is in trash too.

## Four short paragraphs, and three links that are views.

What happened with its numbers, what the box already did about it, what happens if nobody acts, and where to look. Nothing in it is text a model wrote.

### The links are views, never actions

A link that acts is an unauthenticated capability held by anyone who sees or forwards the message. Mail gateways also prefetch links, which would fire the action before a human read the sentence next to it. You sign in at the console, and a destructive action asks for your passkey there.

### Identifiers and numbers, never content

An event's data can hold anything a producer put there, and some producers sit next to prompts, model output and matched secrets. Mail leaves your perimeter through a server nobody here controls, so the renderer allows twenty-two named keys and then checks the shape of every value on top. A live secret is perfectly identifier-shaped, so the key list is what stands between it and your inbox.

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

## Reading the dispatch record.

```
heraldyx --journal
```

The image is distroless: there is no shell in it to read the file with.

Since v0.3.0 a line counts as the source it claims only when the file it came from may carry that source. Each plane's file carries its own name, `HERALDYX_STREAMS` declares anything else, and a line in the wrong file is refused, counted and raised once as `foreign_source`; a file nobody declared is raised once as `unknown_stream`. It does not stop a process that creates a plane's file before that plane does, or a writer forging its own stream. The checkpoint gate, from v0.8.0, answers that for streams a producer signs, and it is off by default.

## Twelve planes write the log it reads.

This plane mails about what other planes wrote, so its reach grows when theirs does. Twelve planes write the shared log, and the Keyryx witness's findings file is read beside it. [Vouchryx](https://it-rat.com/services/vouchryx.html) reports a delegation issued, denied or revoked, and [CostCrew](https://it-rat.com/services/costcrew.html) reports spend spikes, budget thresholds and every move its crew makes on a finding. CostCrew's events have their own sentences here. Vouchryx's delegation events have none yet, so a mail about one says the box has no description for the event until one is written.

## What changed in November

| shipped in | what it does |
|---|---|
| v0.9.0 | A dependency_failed repeats on the dependency, so a provider storm is one mail per window instead of one per failed call. |
| v0.9.0 | The key of a dependency_failed mail is now dependency_failed:dependency/provider/call-failed. An acknowledgement made against the old per-run key does not hold the new one, so acknowledge the new key. |

## What changed in v0.8.0

| shipped in | what it does |
|---|---|
| v0.8.0 | Mail is sent only over TLS: STARTTLS by default, implicit TLS on port 465, and plain only to a loopback relay. A server that does not offer STARTTLS is refused, so set HERALDYX_SMTP_TLS for your server before you upgrade. |
| v0.8.0 | Every SMTP connection has a 10 second dial deadline and a 60 second session deadline. |
| v0.8.0 | Stream files the notifier creates are mode 0640, so only their owner and its group can read them. |
| v0.8.0 | The checkpoint gate is off by default; with it on, a stream is read only while a signed checkpoint covers it (see the boundaries). |
| v0.8.0 | Heraldyx reads a stream another service wrote only as the file's owner or in its group: a stream created at 0640 needs Heraldyx in that group. |

## What the notifier gained in v0.7.0

| shipped in | what it does |
|---|---|
| v0.7.0 | A daily pulse mail says the notifier is running and gives the counts it saw, so a quiet box can no longer look like a dead one. |
| v0.7.0 | Quiet hours hold alerts below critical every day, in a window the operator sets and in the time zone the operator names. |
| v0.7.0 | A maintenance window, opened by hand for up to 24 hours, can hold alerts from one source while that source is being upgraded. |
| v0.7.0 | An operator can acknowledge a known condition for four hours by default, seven days at most. Its repeats are counted instead of mailed, and one mail says how many alerts were held when it ends. |
| v0.7.0 | A critical is never held, whether by quiet hours, a window or an acknowledgement. |

Every release from 1 to 15 October 2026, with what each one shipped, is in [the stack's changes for October](https://it-rat.com/changes-2026-10.html#heraldyx).

## The boundaries, stated rather than discovered at three in the morning.

### It does not queue

A message that cannot be delivered is logged, written into the dispatch record as a refusal, and dropped. A retry queue inside the one process allowed out would be the opposite of the design, and the event itself is still in the log, which outlives this process. Quiet hours and maintenance windows are holds, not a queue: they hold alerts below critical and, when the hours or the window end, send one mail saying how many were held. A critical is never held.

### It does not talk to any plane

No API, no credential, no client. It holds nothing that could act on an agent. If a fact is not in the event log, heraldyx does not know it.

### It does not report anything about a whole organisation

The shared envelope requires an agent id, so a fact about an org has no subject to travel under, and no producer is allowed to invent one to make it fit. Those facts live in the console and in each plane's own API. A mail whose subject line named an agent that had not done the thing would be worse than silence.

### It does not carry history

A first run starts at the end of the log. A month of old incidents arriving at once is how an operator learns to filter this sender to trash.

### And what is not closed yet

- Vouchryx's delegation events have no sentences yet, so a mail about one says the box has no description for the event until one is written.

- The source check does not stop a process that creates a plane's file before that plane does, or a writer forging its own stream. The checkpoint gate, from v0.8.0, narrows that for streams a producer signs: with HERALDYX_CHECKPOINT_GATE=on, a stream is read only while a checkpoint signed by a pinned key covers it. It is off by default, it trusts a pinned key until an operator removes it, and it holds only if each producer alone can write its stream and checkpoints. No launcher has a producer writing signed checkpoints yet.

- The record says a mail server accepted a message, never that it was delivered, and the first record of a chain cannot be verified.

- The burst of 120 events is a scripted scenario for the rules, not a measurement of a real fleet.

## Back to the room.

The [Heraldyx room](https://it-rat.com/services/heraldyx.html) has the burst replay, the drawing of the four checks and the sample mail, and [the guides index](https://it-rat.com/guides.html) has the field itself.

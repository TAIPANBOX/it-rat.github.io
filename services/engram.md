<!-- https://it-rat.com/services/engram.html -->

# Engram, the knowledge plane

> Embeddable agent memory in one SQLite file: bitemporal facts, hybrid BM25 and vector recall, why() provenance and GDPR forget. No server, no API key to start.

Engram is an embeddable memory in one SQLite file. It stores raw episodes, distills them into facts with confidence scores, records when each fact was true, and answers why() for every belief it holds, with the episodes it came from.

## Watch five episodes become ten facts.

A simulation, but not a fantasy: it replays the shape of the live validation run, the first time Engram's reflection pipeline processed real Claude output instead of fixtures. Five episodes go in, ten subject-predicate-object facts come out, each scored and traceable to its source.

## One file on disk. Model calls only when you ask.

Your agent calls observe() and recall() against one .engram file, in-process; only reflect() and compress() leave the machine. [In the guide](https://it-rat.com/engram-guide.html#how-it-works)

## Not a log of text. Beliefs with receipts.

Observing writes an episode with no model in the path; reflect(), only when you ask, distils episodes into facts that each keep a why() chain. [In the guide](https://it-rat.com/engram-guide.html#how-it-works)

Every fact carries when it was true and when Engram learned it, so a fact that changes is closed with an end date and never deleted. [In the guide](https://it-rat.com/engram-guide.html#how-it-works)

A model's fact never closes the person's own: it is recorded beside it, and refute_fact() closes a fact while keeping its history. [In the guide](https://it-rat.com/engram-guide.html#how-it-works)

One recall call has three modes: hybrid by default, cosine for meaning, and spreading activation over the entity graph. [In the guide](https://it-rat.com/engram-guide.html#recall)

### The plane that remembers.

Engram is the knowledge plane of the stack. Every memory_written, reflection_run, contradiction_found and memory_forgotten goes out as an agent-event on the same NDJSON bus [Idryx](https://it-rat.com/services/idryx.html) correlates into the identity graph.

The PyPI name is engdbram (the plain name was taken); the import stays `from engram import Engram`.

## Agent events are off by default, and reflect() is not an MCP tool.

### Provenance over MCP

The MCP server sets provenance and scope, and it cannot see what an agent read outside engram.

### No reflect() over MCP

reflect() is deliberately not exposed to MCP clients.

### Events are opt-in

Agent events are opt-in and off by default.

### The Engram guide

## What a memory has to do that similarity search cannot

**Q: Does it need a server, a container or an API key?**
None of the three to write a memory. It is one `.engram` file on SQLite plus sqlite-vec, in-process, installed with pip. A model only enters the picture when you ask for `reflect()` or `compress()`, and even those calls can be pointed at a local model or routed through [TokenFuse](https://it-rat.com/services/tokenfuse.html) so thinking has a budget too.

**Q: Can I delete everything about one person?**
Yes, and the cascade is the point. Erasing an entity removes the episodes about them, the facts derived from those episodes, and the graph edges that made them findable, and reports how many of each it deleted. That erasure reaches every agent in a shared store on purpose, because the request is about the person. What one agent cannot do is erase another agent's episodes by id: `forget()` is agent-scoped.

**Q: Does it work with Claude Desktop, Claude Code or Cursor?**
Yes, over MCP on stdio, so there is no network listener and no port to guard. Those clients get remember, recall, why and forget against the same store with no integration code.

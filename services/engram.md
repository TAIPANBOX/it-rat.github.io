<!-- https://it-rat.com/services/engram.html -->

# Engram, the knowledge plane

> Embeddable agent memory in one SQLite file: bitemporal facts, hybrid BM25 and vector recall, why() provenance and GDPR forget. No server, no API key to start.

Vector search finds text that looks similar. It cannot say when a fact was true, where a belief came from, or that two beliefs disagree. Engram can: an embeddable memory in one SQLite file that stores raw episodes, distills them into facts with confidence scores, and answers why() for every belief it holds. No server, no Docker, and writing the first memory needs zero API keys.

## Watch five episodes become ten facts.

A simulation, but not a fantasy: it replays the shape of the live validation run, the first time Engram's reflection pipeline processed real Claude output instead of fixtures. Five episodes go in, ten subject-predicate-object facts come out, each scored and traceable to its source.

**Q: What the live run proved**

Before any of this was published, Engram's Anthropic adapter was run against a real Claude model on real infrastructure, three times, on three different box topologies. Until then the reflection pipeline had only ever seen fixtures and a deterministic stub, which is a comfortable thing to test against and proves very little.

| Run | Episodes in | Facts out | Contradictions |
|---|---|---|---|
| Three-node loopback cluster | 5 | 10 | 0 |
| Cross-machine, four separate hosts | 5 | 10, identical to the first run | 0 |
| Enriched multi-agent campaign | 8 | 17, confidence 0.80 to 0.95 | 0 |

What that settles: the reflection prompt and its parsing hold up against real model variance, not just the tidy stub output CI uses; confidence scoring is stable across three independent runs on different infrastructure; and `why()` traces a belief back to the exact observations it came from on real-model output, not only in unit tests. No contradiction was missed in any run.

The method mattered as much as the result. The boxes were disposable and deleted after each run, the code arrived as a git archive with no repository history and no secrets in it, the API key lived in a root-only file and was revoked afterwards, and the service bound to `127.0.0.1` only. Nothing from those runs is still standing.

## One file on disk. One optional network call.

Your agent calls observe() and recall() against one .engram file: SQLite plus sqlite-vec, in-process, nothing between the agent and its memory. Inside: three kinds of memory, bitemporal facts, spreading activation and Ebbinghaus decay. The only part that ever touches a network is reflect(), through a pluggable LLM adapter, and even that can route through TokenFuse.

## Not a log of text. Beliefs with receipts.

### Single file, embeddable

One .engram file on SQLite plus sqlite-vec: no server, no Docker, no config file. pip install, two lines of Python, and the first memory is on disk. Writes land in about 4 ms because no LLM sits in the write path.

### reflect() distills facts

A background reflection loop groups recent episodes and asks an LLM to extract subject-predicate-object facts, each with a confidence score. Every fact keeps a why() chain: which episodes produced it, which run extracted it, which model, at what confidence.

### Facts that know their dates

Every fact carries two timelines: when it was true in reality, and when the system learned it. When Ivan changes jobs the old fact is closed with an end date, never deleted.

**Q: Why two timelines**

A fact in Engram carries `valid_from` and `valid_to`, which say when it was true in reality, and `recorded_at` and `superseded_at`, which say when the system learned it and when it stopped believing it. Those are different clocks, and collapsing them into one is how a memory quietly starts lying.

With both, you can ask what the agent believed as of March and get March's answer rather than today's. That is the difference between an audit you can defend and a database that only ever shows the present. A support agent that promised a refund policy in March should be judged against the policy it knew in March.

It also makes correction safe. When Ivan moves from Acme to Globex, the old fact is closed with an end date and the new one opens; nothing is overwritten, so the reason the agent said what it said in March survives the correction. A vector store has no concept to hang this on: an embedding does not know when it stopped being true.

### Three ways to recall

Cosine vectors for meaning, BM25 blended with vectors when exact terms matter, and spreading activation that walks the entity graph.

**Q: How each mode searches**

One API, three modes, because one retrieval strategy does not fit every question.

**cosine** is pure vector similarity: good when the query means the same thing as the memory but says it with different words.

**hybrid** blends SQLite's FTS5 BM25 with cosine, normalised, for when exact terms carry the meaning. Identifiers, error codes and product names are precisely the tokens an embedding smooths away.

**spreading** starts from cosine nearest neighbours as seeds, then walks the entity graph along Hebbian edges that co-access reinforces, with activation decaying per hop. Results rank on similarity, activation and importance together. This is the mode that surfaces Project X for a question about Ivan when the two texts share no words at all, because the graph, not the wording, connects them.

### GDPR forget, scoped

Erasure is real and targeted: one episode, one fact, or everything about a person. Agent-scoped as of 2.2.1, so one agent cannot delete another's memories.

**Q: What forget() removes**

`forget()` erases a single episode. `forget_fact()` erases one semantic fact. `forget_entity()` cascades: the episodes about that person, the facts derived from them, and the graph edges that made them findable, and it reports how many of each it deleted.

That cascade is the part most stores get wrong. Deleting the raw text while leaving a derived fact and a graph edge behind means the person is still reachable by association, which is exactly what an erasure request was about.

Since 2.2.1 erasure is agent-scoped: in a shared store, one agent cannot reach into another agent's episodes. A delete that crosses that line is not a convenience, it is a way for one tenant to destroy another's evidence.

### MCP server, stdio only

engram-mcp speaks stdio: no network listener, no port to guard. Claude Desktop, Claude Code and Cursor get remember, recall, why and forget against the same store with zero integration code. reflect() is deliberately not exposed to clients.

## Similarity is a fraction of memory.

Pinecone, Weaviate and pgvector are good at the problem they chose: similarity search over large corpora. Engram ships a vector index too, in-process. The difference is everything similarity cannot answer: when a fact was true, where it came from, whether two beliefs disagree. The third column is what most agents actually run on today.

|  | Engram | Vector DBs | Raw chat history |
|---|---|---|---|
| What it stores | Memories with provenance | Embeddings of text | Transcripts |
| Reasons over time | Bitemporal: valid + recorded | No | No |
| Explains itself | why() chain to source episodes | No | No |
| Contradiction handling | Detected, flagged as events | Not a concept | None |
| Runs where | In-process, one file | Managed service | In your prompt window |
| Forget a person | Targeted GDPR erase | Delete by id, if you kept the ids | Impossible |

### The plane that remembers.

Engram is the knowledge plane of the stack. Its own reflect() calls can point base_url at [TokenFuse](https://it-rat.com/tokenfuse.html), so even thinking has a budget. Every memory_written, reflection_run, contradiction_found and memory_forgotten goes out as an agent-event on the same NDJSON bus [Idryx](https://it-rat.com/idryx.html) correlates into the identity graph. The envelope they travel in is the [Agent Passport contract](https://it-rat.com/platform.html): one spec, every service, including this one.

Provenance is one of the questions a governed fleet has to answer; the others are in [AI agent governance](https://it-rat.com/ai-agent-governance.html).

Install it from [the repository](https://github.com/TAIPANBOX/engram#readme), where the command lives beside the version it belongs to.

The PyPI name is engdbram (the plain name was taken); the import stays `from engram import Engram`. Your first memory needs zero API keys: an LLM enters the picture only when you ask for reflect().

**Q: How this one ships**

No per-platform binaries here either: this one is a Python library you import, so the package index is the download. The install command lives in the repository, next to the version it resolves.

## What a memory has to do that similarity search cannot

**Q: How is this different from a vector database?**
A vector store finds text that looks similar. It cannot tell you when a fact was true, where a belief came from, or that two beliefs disagree. Engram ships a vector index too, in-process, and adds the three answers similarity has no concept for: bitemporal validity, a `why()` chain back to source episodes, and contradiction detection.

**Q: Does it need a server, a container or an API key?**
None of the three to write a memory. It is one `.engram` file on SQLite plus sqlite-vec, in-process, installed with pip. A model only enters the picture when you ask for `reflect()`, and even that call can be pointed at a local model or routed through [TokenFuse](https://it-rat.com/tokenfuse.html) so thinking has a budget too.

**Q: Can I delete everything about one person?**
Yes, and the cascade is the point. Erasing an entity removes the episodes about them, the facts derived from those episodes, and the graph edges that made them findable, and reports how many of each it deleted. Erasure is agent-scoped, so in a shared store one agent cannot delete another's memories.

**Q: Does it work with Claude Desktop, Claude Code or Cursor?**
Yes, over MCP on stdio, so there is no network listener and no port to guard. Those clients get remember, recall, why and forget against the same store with no integration code.

<!-- https://it-rat.com/engram-guide.html -->

# Engram guide

> How Engram works, the live runs against real Claude, how to install it, what changed in v3.0.0 and v3.1.0, and what it does not do yet, in full.

The [Engram room](https://it-rat.com/services/engram.html) keeps the simulation, the drawing of one file on disk and the common questions. This guide keeps the rest of what the room used to say: what a memory holds and how each part works, the three live runs against real Claude, how it ships, what changed in v3.0.0 and v3.1.0, and what it does not do yet.

- [At a glance](https://it-rat.com/engram-guide.html#overview)

- [How it works](https://it-rat.com/engram-guide.html#how-it-works)

- [Recall is one part of a memory](https://it-rat.com/engram-guide.html#recall)

- [The live runs](https://it-rat.com/engram-guide.html#live-run)

- [Where it sits](https://it-rat.com/engram-guide.html#where-it-sits)

- [Running it](https://it-rat.com/engram-guide.html#run)

- [What changed](https://it-rat.com/engram-guide.html#changes)

- [What changed in November](https://it-rat.com/engram-guide.html#changes-november)

- [Limits](https://it-rat.com/engram-guide.html#limits)

## Engram at a glance.

- **The memory that remembers why:** an embeddable memory in one SQLite file.

- **Release:** latest, on PyPI as engdbram. **Core:** Python 3.11+.

- **Storage:** a single SQLite file plus sqlite-vec.

- **Recall:** hybrid BM25 and vector.

- **Integrations:** MCP, LangChain, LlamaIndex.

- **Licence:** Apache-2.0.

### What it is

Engram is an embeddable memory in one SQLite file. It stores raw episodes, distills them into facts with confidence scores, records when each fact was true, and answers why() for every belief it holds, with the episodes it came from. Two beliefs that disagree are recorded as a contradiction. No server, no Docker, and writing the first memory needs zero API keys.

## Not a log of text. Beliefs with receipts.

### One file on disk. Model calls only when you ask.

Your agent calls observe() and recall() against one .engram file: SQLite plus sqlite-vec, in-process, nothing between the agent and its memory. Inside: episodic and semantic memory, bitemporal facts, spreading activation and Ebbinghaus decay. The only calls that leave the machine are reflect() and compress(), through a pluggable LLM adapter, and even those can route through TokenFuse; the embedding model downloads once, about 64 MB, on first use.

### Single file, embeddable

One .engram file on SQLite plus sqlite-vec: no server, no Docker, no config file. pip install, two lines of Python, and the first memory is on disk. A write takes a median of 8 ms (200 writes on an Apple Silicon Mac, 2026-10-13) because no LLM sits in the write path.

### reflect() distills facts

A background reflection loop groups recent episodes and asks an LLM to extract subject-predicate-object facts, each with a confidence score. Every fact keeps a why() chain: which episodes produced it, which run extracted it, which model, at what confidence.

### Facts that know their dates

Every fact carries two timelines: when it was true in reality, and when the system learned it. When Ivan changes jobs the old fact is closed with an end date, never deleted.

**Two timelines, and the questions only two can answer.** A fact in Engram carries `valid_from` and `valid_to`, which say when it was true in reality, and `recorded_at` and `superseded_at`, which say when the system learned it and when it stopped believing it. Those are different clocks, and collapsing them into one is how a memory quietly starts lying.

With both, you can ask what the agent believed as of March and get March's answer rather than today's. That is the difference between an audit you can defend and a database that only ever shows the present. A support agent that promised a refund policy in March should be judged against the policy it knew in March.

It also makes correction safe. When Ivan moves from Acme to Globex, the old fact is closed with an end date and the new one opens; nothing is overwritten, so the reason the agent said what it said in March survives the correction.

### A person's own fact outranks a model's

A fact is the person's own when its provenance is `user` and it was not written quarantined. A reflection pass whose extraction is not the person's own no longer closes such a fact by recency, and neither does a refutation that is not. The newer fact is recorded beside it, `contradictions()` lists the pair, and the existing `contradiction_found` event, with the same two data keys, names both. `reflect()` does not count that conflict in `contradictions_resolved`, because nothing was resolved. `assert_fact()` never closed anything and still does not; it now emits the same event for such a conflict. Between two facts that are both the person's own, the newer one still wins.

A fact stamps its provenance when it is written, so the protection does not end when its source episodes are forgotten, compressed or pruned. `reflect()` stamps a fact with the least trusted provenance of all the episodes in its window, so a window that mixes `user` and `external` episodes yields facts that are not the person's own. Engram stores the provenance the caller declares and does not verify it. Over MCP a caller cannot claim `user`, and a fact written through MCP is `unknown`, so it can never be a person's fact.

### A fact can be refuted without being erased

`refute_fact()` closes a fact and keeps it: `valid_to` and `superseded_at` are set, `refuted_by` is recorded, and there is no replacement, so `timeline()` and `as_of` keep what was believed before. Every fact derived from it, at any depth and across agents, gets the refuted fact's id in `undermined_by` and stays active. A private fact of another agent is marked too and is not named in the result. `assert_fact(derived_from=[...])` records the derivation. Refuting twice changes nothing, and the person's own fact can be refuted only by the person. `forget_fact()` is unchanged: erasure stays the owner's right, and refutation is the path that keeps history.

The store moves one schema step, recorded in `PRAGMA user_version`, with three nullable columns on facts: `provenance`, `refuted_by` and `undermined_by`. The step is idempotent and rewrites no row, and export and import carry the columns.

### Three ways to recall

Cosine vectors for meaning, BM25 blended with vectors when exact terms matter, and spreading activation that walks the entity graph.

**Three retrieval modes, one call.** One API, three modes, because one retrieval strategy does not fit every question.

**cosine** is pure vector similarity: good when the query means the same thing as the memory but says it with different words.

**hybrid** blends SQLite's FTS5 BM25 with cosine, normalised, for when exact terms carry the meaning. Identifiers, error codes and product names are precisely the tokens an embedding smooths away.

**spreading** starts from cosine nearest neighbours as seeds, then walks the entity graph along Hebbian edges that co-access reinforces, with activation decaying per hop. Results rank on similarity, activation and importance together. This is the mode that surfaces Project X for a question about Ivan when the two texts share no words at all, because the graph, not the wording, connects them.

### GDPR forget, scoped

Erasure is real and targeted: one episode, one fact, or everything about a person. Since 2.2.1 an agent can forget only its own episodes; erasing a person reaches every agent in the file, on purpose.

**What erasure actually removes.** `forget()` erases a single episode. `forget_fact()` erases one semantic fact. `forget_entity()` cascades: the episodes about that person, the facts derived from them, and the graph edges that made them findable, and it reports how many of each it deleted.

That cascade is the part most stores get wrong. Deleting the raw text while leaving a derived fact and a graph edge behind means the person is still reachable by association, which is exactly what an erasure request was about.

Since 2.2.1 `forget()` is agent-scoped: in a shared store, one agent cannot reach into another agent's episodes by id. A delete that crosses that line is not a convenience, it is a way for one tenant to destroy another's evidence.

Two erasures cross it on purpose. Facts and entities are shared by every agent in the file, so `forget_fact()` removes a fact for all of them. And `forget_entity()` reaches every agent's episodes about that person, because a request to be forgotten is about the person, not about one agent's copy.

### MCP server, stdio only

engram-mcp speaks stdio: no network listener, no port to guard. Claude Desktop, Claude Code and Cursor get remember, recall, why and forget against the same store with zero integration code. reflect() is deliberately not exposed to clients.

## Recall is one part of a memory.

Engram keeps a vector index in-process. It also keeps when each fact was true, where it came from, and whether two beliefs disagree.

| Question an agent asks | What answers it |
|---|---|
| Find what I mean, not only what I typed | Hybrid recall: BM25 and cosine, blended |
| What was true in March, before we knew better | Bitemporal facts: valid time and recorded time |
| Why do you believe that | why(), a chain back to the source episodes |
| These two things disagree | Contradictions detected and recorded as events |
| Whose word counts when two disagree | A person's own fact is never closed by a lower provenance |
| That is wrong, but keep the history | refute_fact(): closed, not erased, with derived facts marked |
| Reach what the match is connected to | Spreading activation over Hebbian edges |
| Stay useful instead of growing | Importance decay, and reflection prunes the bottom |
| Forget a person | Targeted erase by episode, entity or fact |
| Run it anywhere | In-process, one file, no server and no key to write |

## Three runs against real Claude, and what they settled.

Before any of this was published, Engram's Anthropic adapter was run against a real Claude model on real infrastructure, three times, on three different box topologies. Until then the reflection pipeline had only ever seen fixtures and a deterministic stub, which is a comfortable thing to test against and proves very little.

| Run | Episodes in | Facts out | Contradictions |
|---|---|---|---|
| Three-node loopback cluster | 5 | 10 | 0 |
| Cross-machine, four separate hosts | 5 | 10, identical to the first run | 0 |
| Enriched multi-agent campaign | 8 | 17, confidence 0.80 to 0.95 | 0 |

What that settles: the reflection prompt and its parsing hold up against real model variance, not just the tidy stub output CI uses; confidence scoring is stable across three independent runs on different infrastructure; and `why()` traces a belief back to the exact observations it came from on real-model output, not only in unit tests. No contradiction was missed in any run.

The method mattered as much as the result. The boxes were disposable and deleted after each run, the code arrived as a git archive with no repository history and no secrets in it, the API key lived in a root-only file and was revoked afterwards, and the service bound to `127.0.0.1` only. Nothing from those runs is still standing.

## The plane that remembers.

Engram is the knowledge plane of the stack. Its own reflect() calls can point base_url at [TokenFuse](https://it-rat.com/services/tokenfuse.html), so even thinking has a budget. Every memory_written, reflection_run, contradiction_found and memory_forgotten goes out as an agent-event on the same NDJSON bus [Idryx](https://it-rat.com/services/idryx.html) correlates into the identity graph. The envelope they travel in is the [Agent Passport contract](https://it-rat.com/services/platform.html): one spec, every service, including this one.

Provenance is one of the questions a governed fleet has to answer; the others are in [AI agent governance](https://it-rat.com/ai-agent-governance.html).

## Engram ships as a package.

```
pip install engdbram
```

Install it from [the repository](https://github.com/TAIPANBOX/engram#readme), where the command lives beside the version it belongs to.

The PyPI name is engdbram (the plain name was taken); the import stays `from engram import Engram`. Your first memory needs zero API keys: an LLM enters the picture only when you ask for reflect().

### How this one ships

No per-platform binaries here either: this one is a Python library you import, so the package index is the download. The install command lives in the repository, next to the version it resolves.

## What changed in v3.0.0.

Engram's own list for 1 to 15 October 2026 is in [the stack's changes](https://it-rat.com/changes-2026-10.html#engram).

### Where each memory came from

Released as v3.0.0 on 2026-10-18. The library records a source for every observation: user for what the person typed, tool for what a tool returned, and external for anything else. Recall returns the source with each result, and why() reports the least trusted source behind a fact. Over MCP the server sets the most a write may carry, which defaults to external, so a caller cannot claim user. A server started with an agent id serves that agent alone; one started without serves the whole file and says so on stderr. A fact is private to its writer unless it is shared.

## What changed in November

| shipped in | what it does |
|---|---|
| v3.1.0 | A person's own fact is never closed by a lower provenance: a model's extraction or refutation is recorded beside it, and contradictions() lists the pair. |
| v3.1.0 | refute_fact() closes a fact without erasing it, and marks every fact derived from it as undermined. |
| v3.1.0 | The documents no longer claim procedural memory: the store never modelled it, and remember(kind="procedural") is refused. |
| v3.1.0 | A fact stamps its provenance when it is written, so a person's fact stays the person's after its source episodes are forgotten or pruned. The store moves to schema generation 2 with three nullable columns on facts, and assert_fact takes provenance and derived_from. |

## What it does not do, and what is still open.

- The server cannot see what an agent read outside engram. A session turns untrusted when recall or why returns a memory that is not the user's own or is quarantined, when the caller labels its input or passes read_untrusted, or when the server is started with the untrusted flag.

- Procedural memory is not part of the store: `remember(kind="procedural")` is refused.

- Refutation emits no event, because the shared event contract has no type for it. The row it leaves in the store is the record. An older Engram that opens a migrated file ignores the new columns.

- reflect() is deliberately not exposed to MCP clients.

- Agent events (memory_written, reflection_run, contradiction_found, memory_forgotten) are opt-in and off by default.

- The only calls that leave the machine are reflect() and compress(), through a pluggable LLM adapter, plus the one-time download of the embedding model on first use.

- No per-platform binaries: this one is a Python library you import, so the package index is the download.

- Nothing from the three live runs is still standing: the boxes were disposable and deleted after each run.

## Back to the room.

The [Engram room](https://it-rat.com/services/engram.html) has the simulation, the drawing and the common questions, and [the guides index](https://it-rat.com/guides.html) has the field itself.

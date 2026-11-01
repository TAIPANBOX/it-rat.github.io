<!-- https://it-rat.com/verdryx-guide.html -->

# Verdryx guide

> How Verdryx turns agent spend into cost per resolved case, its six graders, how to run it offline, what changed in October 2026, and its limits.

The [Verdryx room](https://it-rat.com/services/verdryx.html) keeps the sixty-second shift, the drawing of the graders, how to start it, and the common questions. This guide keeps the rest of what the room used to say: what it grades in full, how a case gets a price, the six graders, where it sits in the stack, how to run it, what changed from 1 to 15 October 2026, and its limits.

- [At a glance](https://it-rat.com/verdryx-guide.html#overview)

- [How it works](https://it-rat.com/verdryx-guide.html#how-it-works)

- [What it grades](https://it-rat.com/verdryx-guide.html#grades)

- [Cost per outcome](https://it-rat.com/verdryx-guide.html#cost-per-outcome)

- [The six graders](https://it-rat.com/verdryx-guide.html#graders)

- [In the stack](https://it-rat.com/verdryx-guide.html#in-the-stack)

- [Running it](https://it-rat.com/verdryx-guide.html#run)

- [What changed](https://it-rat.com/verdryx-guide.html#changes)

- [Limits](https://it-rat.com/verdryx-guide.html#limits)

## Verdryx at a glance.

- **Version:** 0.1.0 · Python 3.11+.

- **Tests:** fully offline suite.

- **Core deps:** one, rfc8785 (+ optional extras).

- **Reads:** tokenfuse Parquet traces · NDJSON · CSV.

- **Exports:** agent-events v0.2 · OTLP spans.

- **Licence:** Apache-2.0.

### What it is

Verdryx grades each case by exact match, regex, a production outcome tag, the order of its tool calls or an LLM judge, and prices the result that matters: cost per resolved case, not cost per call. On the live run in VALIDATION.md, a resolved case cost $0.00042, and each abandoned attempt cost $0.00025 for nothing.

## Six graders in, one honest number out.

Traces and eval sets go in. Exact match, regex, an outcome tag straight off the gateway or the order of the tool calls decide what happened, and where a rule cannot, an LLM judge or a typed verdict from Typryx does, with its own cost counted like everything else. What comes out: a cost-per-outcome report, a drift verdict against a stored baseline, a SQLite file, and an event or a span for whatever is already watching your stack.

### Sixty seconds, one shift

This is a simulation, but shaped by the real run: a live, Claude-backed support workload whose outcome-tagged traces were read back and graded. A shift's worth of support cases gets graded, a real cost per resolved case comes out the other side, and a drift check runs against a stored baseline before one OTLP span closes the loop. It runs on the [room](https://it-rat.com/services/verdryx.html#sim).

## Not a bigger number. A truer one.

### Cost per outcome

Resolved, abandoned, escalated: real outcome tags straight off the TokenFuse gateway turn into a dollar figure per case, not a total nobody can act on.

### Drift with statistics

A flat threshold catches the obvious drop. A two-sample significance check beside it, Welch's t plus a bootstrap interval, catches the small, consistent regression a threshold tuned for noise would miss. Point it at a baseline whose source run is gone and it fails loudly, not silently.

### The LLM judge is metered

An llm_judge case's cost is a real dollar figure, priced against the same book TokenFuse uses, not the zero placeholder the deterministic graders leave behind.

### One-dependency core

The graders and drift maths use only the standard library. The one runtime dependency is rfc8785, which canonicalises the JSON the event chain is hashed over. Anthropic and Parquet support are opt-in extras, not a tax on the common path.

### Offline test suite

The suite runs against a deterministic StubLLMAdapter, with no network and no API key. It's what Verdryx's own CI runs, and what --model stub gives you too.

### Defensive by design

Grades an operator's own agents against an eval set or a production outcome tag. The README puts it plainly: it “never manipulates outputs, never crafts adversarial prompts, and never attacks anything.”

## How a case gets a price, including the calls nobody tagged

### How the figure is built

The input is the gateway's own trace, not a second pipeline built to agree with it: run id, step, outcome tag, decision, and cost in microdollars, read straight from TokenFuse's Parquet segments, NDJSON or CSV. Verdryx reduces it the same way TokenFuse itself does, so the two never quietly disagree about what a run cost.

Rows are ordered by run and step, and the last non-empty tag a run carries is the one that counts: a case that escalated after two failed attempts is an escalation, not three separate stories.

Then the parts most reports lose. Every call in a run folds into that run's bucket, not only the tagged one, so an untagged intermediate call's cost is not dropped on the floor. A run nobody ever tagged still appears, under an explicit untagged label, rather than vanishing from the report and making the average look better than it is. And a call the breaker blocked is still counted, because a refused call is part of what the outcome cost you.

The result is one row per outcome tag, with count, total and mean, plus an overall row pooling everything. A dollar figure per resolved case is a number an operator can act on; a monthly total is not.

## Six graders, and which two of them can cost money

### What grades a case

Every case resolves to a score between zero and one, whichever of the six graders it asks for, so a case simply names the one it needs.

**Exact** and **regex** score a literal or a pattern: deterministic, free, and the right tool far more often than people expect. **Outcome tag** reads a production tag instead of an expected answer, scoring a resolved case at one, an escalation at a half and an abandonment at zero, with the whole table overridable; an unrecognised tag scores zero rather than raising, so one odd tag cannot take a report down. **Tool trace** scores the model's ordered tool calls against the calls it was supposed to make, which is the difference between a right answer and a right answer reached by touching things it should not have. **LLM judge** grades against a written rubric where those four cannot. **Typed** asks a separate [Typryx](https://it-rat.com/services/typryx.html) service a typed question about the output, a yes or no or a graded level, and scores the probability it returns; a case Typryx cannot answer is counted apart with its reason, never scored as a zero.

Only the judge and the typed grader can spend money, neither runs by default, and both say so: the judge’s cost is priced against the same book the money plane uses, and a typed verdict carries whatever cost Typryx reports for it, rather than the zero a deterministic grader honestly leaves behind. The typed grader runs only when a run is given a Typryx address with `--typed-url`. An eval suite is itself an agent workload; a quality tool that hides its own bill has no business auditing anyone else's.

The judge takes an injected adapter, so the same suite runs against a deterministic stub with no network and no key, which is what Verdryx's own tests use, or against a real model when you want the real verdict.

## The line that turns spend into a verdict.

Verdryx prices the traces [TokenFuse](https://it-rat.com/services/tokenfuse.html) writes: outcome tags and spend data share the same request path, so cost and quality can never quietly drift apart. Its `quality_drift` events ride the same bus as [Platform](https://it-rat.com/services/platform.html)'s Agent Passport contract. [Mockryx](https://it-rat.com/services/mockryx.html) can require an off-path reaction from Verdryx as part of a pre-prod drill. A typed grader from [Typryx](https://it-rat.com/services/typryx.html) sits beside its LLM judge, opt-in per run with `--typed-url`.

Cost per resolved case sits inside a wider practice: [FinOps for AI](https://it-rat.com/finops-for-ai.html), and the controls around it in [AI agent governance](https://it-rat.com/ai-agent-governance.html).

## Grade with a stub, then price the traces.

```
git clone https://github.com/TAIPANBOX/verdryx && cd verdryx
python -m venv .venv && source .venv/bin/activate
pip install -e .
```

Into a virtual environment: system Python is usually externally managed. There is no PyPI package, so the version you run is the commit you can read.

```
verdryx eval evalset.json --model stub --db verdryx.db
```

No network, no key: `--model stub` is deterministic. Then price the traces it left behind.

```
verdryx cost-per-correct --traces $TOKENFUSE_DATA_DIR
```

## What changed from 1 to 15 October

No release in the window, nine pull requests merged. The same entry, beside every other service's, is in [what changed in the stack](https://it-rat.com/changes-2026-10.html#verdryx).

- **On main:** its price book mirrors the gateway's, row for row: every listed Claude id, the Gemini rows on Vertex AI, the vendors' prices of 13 October with their long-prompt tiers, and the `openai/...` rows.

## What runs only when you ask, and what is not proven.

- Only the judge and the typed grader can spend money, and neither runs by default. The typed grader runs only when a run is given a Typryx address with `--typed-url`.

- A case Typryx cannot answer is counted apart with its reason, never scored as a zero.

- There is no PyPI package, so the version you run is the commit you can read.

- The sixty seconds on the room are a simulation, shaped by the real run: a live, Claude-backed support workload whose outcome-tagged traces were read back and graded.

## Back to the room.

The [Verdryx room](https://it-rat.com/services/verdryx.html) has the shift, the drawing and the common questions, and [the guides index](https://it-rat.com/guides.html) has the field itself.

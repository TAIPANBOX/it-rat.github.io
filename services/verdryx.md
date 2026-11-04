<!-- https://it-rat.com/services/verdryx.html -->

# Verdryx, the quality plane

> Cost per correctly resolved case, not cost per token: six graders, statistical drift detection and a metered LLM judge, scored on your own outcome tags.

Verdryx grades each case by exact match, regex, a production outcome tag, the order of its tool calls or an LLM judge, and prices the result that matters: cost per resolved case, not cost per call. On the live run in VALIDATION.md, a resolved case cost $0.00042.

## Watch spend turn into a verdict.

This is a simulation, but shaped by the real run: a live, Claude-backed support workload whose outcome-tagged traces were read back and graded.

## Six graders in, one honest number out.

Traces and eval sets go in. What comes out: a cost-per-outcome report, a drift verdict against a stored baseline, a SQLite file, and an event or a span for whatever is already watching your stack.

## Not a bigger number. A truer one.

### Cost per outcome

Resolved, abandoned, escalated: real outcome tags straight off the TokenFuse gateway turn into a dollar figure per case, not a total nobody can act on.

### Drift with statistics

A flat threshold catches the obvious drop. A two-sample significance check beside it, Welch's t plus a bootstrap interval, catches the small, consistent regression a threshold tuned for noise would miss.

### The LLM judge is metered

An llm_judge case's cost is a real dollar figure, priced against the same book TokenFuse uses.

### One-dependency core

The graders and drift maths use only the standard library. The one runtime dependency is rfc8785, which canonicalises the JSON the event chain is hashed over.

### A failure becomes a record

A drift regression or an SLO breach is stored as a finding, with its evidence and a suspect model or version. Register a fix and the runs that follow decide it: verified, failed, or pending with its reason. Unmeasured is never a pass.

### A person's grade outranks the model's

A reviewer's grade replaces the model's value in a run's mean, in drift and in the quality floor, and the model's own value stays beside it. eval has no path to a grade, and every grade carries its author.

## The line that turns spend into a verdict.

Verdryx prices the traces [TokenFuse](https://it-rat.com/services/tokenfuse.html) writes: outcome tags and spend data share the same request path, so cost and quality can never quietly drift apart. Cost per resolved case sits inside a wider practice: [FinOps for AI](https://it-rat.com/finops-for-ai.html), and the controls around it in [AI agent governance](https://it-rat.com/ai-agent-governance.html).

## Grade with a stub, then price the traces.

There is no PyPI package, so the version you run is the commit you can read.

## What runs only when you ask.

- Only the judge and the typed grader can spend money, and neither runs by default.

- The typed grader from [Typryx](https://it-rat.com/services/typryx.html) is opt-in per run with `--typed-url`.

### The Verdryx guide

## Measuring quality in money, not vibes

**Q: How do I measure cost per correct answer?**
Tag outcomes in production, then read them back off the gateway's own trace: resolved, escalated, abandoned. Verdryx turns that into a dollar figure per case, including the untagged intermediate calls a run made and the calls the breaker blocked, because both are part of what the outcome cost.

**Q: How do I know when quality has actually dropped?**
A flat threshold catches the obvious fall. Beside it, a two-sample significance check, Welch's t with a bootstrap interval, catches the small consistent regression a threshold tuned for noise would miss. Point it at a baseline whose source run is gone and it fails loudly rather than silently.

**Q: Do I need an LLM judge to use it?**
No. Four of the six graders are deterministic and free: exact, regex, outcome tag and tool trace. The judge is there for the cases a rubric can score and a pattern cannot, and when you use it, its own cost is priced against the same book the money plane uses rather than reported as zero. The sixth, the typed grader, asks a separate Typryx service and runs only when a run is given its address.

**Q: Does it need network access or a key?**
Not for the common path. The graders and drift maths use only the standard library, the one runtime dependency is a canonical-JSON library, and the whole suite runs against a deterministic stub adapter with no network and no key, which is exactly what its own CI runs.

<!-- https://it-rat.com/services/verdryx.html -->

# Verdryx, the quality plane

> Cost per correctly resolved case, not cost per token: six graders, statistical drift detection and a metered LLM judge, scored on your own outcome tags.

Verdryx grades each case by exact match, regex, a production outcome tag, the order of its tool calls or an LLM judge, and prices the result that matters: cost per resolved case, not cost per call. On the live run in VALIDATION.md, a resolved case cost $0.00042.

## Watch spend turn into a verdict.

This is a simulation, but shaped by the real run: a live, Claude-backed support workload whose outcome-tagged traces were read back and graded.

## Six graders in, one honest number out.

Traces and eval sets go in. What comes out: a cost-per-outcome report, a drift verdict against a stored baseline, a SQLite file, and an event or a span for whatever is already watching your stack.

## Not a bigger number. A truer one.

Six graders score each case between zero and one, and the outcome tags on TokenFuse's trace become a dollar figure per resolved case. Only the judge and the typed grader can spend, and the judge is priced on the same book TokenFuse uses. [In the guide](https://it-rat.com/verdryx-guide.html#grades)

A drift regression or an SLO breach becomes a finding with its evidence and a suspect, and the runs after a registered fix decide it: verified, failed or pending. A person's grade replaces the model's value, which stays beside it. [In the guide](https://it-rat.com/verdryx-guide.html#findings)

verdryx slo measures four indicators of good runs over eligible runs and enforces nothing. Wardryx turns a spent budget into a hold for a person, and Heraldyx mails the slo_burn at once. [In the guide](https://it-rat.com/verdryx-guide.html#error-budgets)

## The line that turns spend into a verdict.

Verdryx prices the traces [TokenFuse](https://it-rat.com/services/tokenfuse.html) writes: outcome tags and spend data share the same request path, so cost and quality can never quietly drift apart. Cost per resolved case sits inside a wider practice: [FinOps for AI](https://it-rat.com/finops-for-ai.html), and the controls around it in [AI agent governance](https://it-rat.com/ai-agent-governance.html).

## Grade with a stub, then price the traces.

There is no PyPI package, so the version you run is the commit you can read.

## What runs only when you ask.

### Two graders can spend

Only the judge and the typed grader can spend money, and neither runs by default. [In the guide](https://it-rat.com/verdryx-guide.html#limits)

### Typed is opt-in

The typed grader from [Typryx](https://it-rat.com/services/typryx.html) is opt-in per run with `--typed-url`. [In the guide](https://it-rat.com/verdryx-guide.html#limits)

### Grades live in the store

The store file is the trust boundary for grades, and a console build that reads scores directly shows the model's value until it reads human_grades too. [In the guide](https://it-rat.com/verdryx-guide.html#limits)

### The Verdryx guide

## Measuring quality in money, not vibes

**Q: How do I measure cost per correct answer?**
Tag outcomes in production, then read them back off the gateway's own trace: resolved, escalated, abandoned. Verdryx turns that into a dollar figure per case, including the untagged intermediate calls a run made. A call the breaker blocked is counted but adds nothing to the figure, because the cost recorded for it is an estimate of what was avoided, not a charge that settled.

**Q: How do I know when quality has actually dropped?**
A flat threshold catches the obvious fall. Beside it, a bootstrap interval on the difference catches the small consistent regression a threshold tuned for noise would miss; Welch's t is reported next to the verdict and does not decide it. Point it at a baseline whose source run is gone and it fails loudly rather than silently.

**Q: Do I need an LLM judge to use it?**
No. Four of the six graders are deterministic and free: exact, regex, outcome tag and tool trace. The judge is there for the cases a rubric can score and a pattern cannot, and when you use it, its own cost is priced against the same book the money plane uses rather than reported as zero. The sixth, the typed grader, asks a separate Typryx service and runs only when a run is given its address.

**Q: Does it need network access or a key?**
Not for the common path. The graders and drift maths use only the standard library, the one runtime dependency is a canonical-JSON library, and the whole suite runs against a deterministic stub adapter with no network and no key, which is exactly what its own CI runs.

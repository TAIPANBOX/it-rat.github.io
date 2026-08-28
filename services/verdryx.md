<!-- https://it-rat.com/services/verdryx.html -->

# Verdryx, the quality plane

> Cost per correctly resolved case, not cost per token: five graders, statistical drift detection and a metered LLM judge, scored on your own outcome tags.

Cost-per-token dashboards report what a call cost and stop there. They cannot tell a successful call from a wasted one. Verdryx grades the output, exact match, regex, a production outcome tag, or an LLM judge, and prices the result that actually matters: cost per resolved case, not cost per call. On the last live run: $0.00042 to resolve a case, $0.00025 spent on one that went nowhere.

## Watch spend turn into a verdict.

This is a simulation, but shaped by the real run: 176 real Claude calls read back as outcome-tagged traces. A shift's worth of support cases gets graded, a real cost per resolved case comes out the other side, and a drift check runs against a stored baseline before one OTLP span closes the loop.

## Four graders in, one honest number out.

Traces and eval sets go in. Exact match, regex, an outcome tag straight off the gateway, or an LLM judge decide what happened, and the judge's own calls get priced like everything else. What comes out: a cost-per-outcome report, a drift verdict against a stored baseline, a SQLite file, and an event or a span for whatever is already watching your stack.

## Not a bigger number. A truer one.

### Cost per outcome

Resolved, abandoned, escalated: real outcome tags straight off the TokenFuse gateway turn into a dollar figure per case, not a total nobody can act on.

**Q: How the figure is built**

The input is the gateway's own trace, not a second pipeline built to agree with it: run id, step, outcome tag, decision, and cost in microdollars, read straight from TokenFuse's Parquet segments, NDJSON or CSV. Verdryx reduces it the same way TokenFuse itself does, so the two never quietly disagree about what a run cost.

Rows are ordered by run and step, and the last non-empty tag a run carries is the one that counts: a case that escalated after two failed attempts is an escalation, not three separate stories.

Then the parts most reports lose. Every call in a run folds into that run's bucket, not only the tagged one, so an untagged intermediate call's cost is not dropped on the floor. A run nobody ever tagged still appears, under an explicit untagged label, rather than vanishing from the report and making the average look better than it is. And a call the breaker blocked is still counted, because a refused call is part of what the outcome cost you.

The result is one row per outcome tag, with count, total and mean, plus an overall row pooling everything. A dollar figure per resolved case is a number an operator can act on; a monthly total is not.

### Drift with statistics

A flat threshold catches the obvious drop. A two-sample significance check beside it, Welch's t plus a bootstrap interval, catches the small, consistent regression a threshold tuned for noise would miss. Point it at a baseline whose source run is gone and it fails loudly, not silently.

### The LLM judge is metered

An llm_judge case's cost is a real dollar figure, priced against the same book TokenFuse uses, not the zero placeholder the deterministic graders leave behind.

**Q: What grades a case**

Every case resolves to a score between zero and one, and five graders share one shape, so a case simply asks for the one it needs.

**Exact** and **regex** score a literal or a pattern: deterministic, free, and the right tool far more often than people expect. **Outcome tag** reads a production tag instead of an expected answer, scoring a resolved case at one, an escalation at a half and an abandonment at zero, with the whole table overridable; an unrecognised tag scores zero rather than raising, so one odd tag cannot take a report down. **Tool trace** scores the model's ordered tool calls against the calls it was supposed to make, which is the difference between a right answer and a right answer reached by touching things it should not have. **LLM judge** grades against a written rubric where the other four cannot.

Only the last one spends money, and it says so. Its cost is priced against the same book the money plane uses, rather than the zero a deterministic grader honestly leaves behind. An eval suite is itself an agent workload; a quality tool that hides its own bill has no business auditing anyone else's.

The judge takes an injected adapter, so the same suite runs against a deterministic stub with no network and no key, which is what Verdryx's own tests use, or against a real model when you want the real verdict.

### Zero-dependency core

The eval runner, graders and drift math import nothing but the standard library. Anthropic and Parquet support are opt-in extras, not a tax on the common path.

### Offline test suite

365 tests run against a deterministic StubLLMAdapter, no network, no API key. It's what Verdryx's own CI runs, and what --model stub gives you too.

### Defensive by design

Grades an operator's own agents against an eval set or a production outcome tag. The README puts it plainly: it “never manipulates outputs, never crafts adversarial prompts, and never attacks anything.”

## Cost per call was never the question.

Cost-per-token dashboards answer the easy question: what a call cost. Verdryx answers the one that matters: what did getting it right cost, and did that number just get worse.

|  | Verdryx | cost-per-token dashboards | “eyeball the transcripts” |
|---|---|---|---|
| Unit | Correct case | Token | Vibe |
| Catches quality regressions | Drift vs baseline, significance-tested | No | Sometimes, too late |
| Knows what an abandoned attempt cost | Yes, $0.00025 in the live run | No | No |
| Needs a platform | pip install, one SQLite file | A SaaS contract | Nothing but staff time |

### The line that turns spend into a verdict.

Verdryx prices the traces [TokenFuse](https://it-rat.com/tokenfuse.html) writes: outcome tags and spend data share the same request path, so cost and quality can never quietly drift apart. Its `quality_drift` events ride the same bus as [Platform](https://it-rat.com/platform.html)'s Agent Passport contract. [Mockryx](https://it-rat.com/mockryx.html) can require an off-path reaction from Verdryx as part of a pre-prod drill.

Cost per resolved case sits inside a wider practice: [FinOps for AI](https://it-rat.com/finops-for-ai.html), and the controls around it in [AI agent governance](https://it-rat.com/ai-agent-governance.html).

No network, no key: `--model stub` is deterministic. Then price the traces it left behind.

## Measuring quality in money, not vibes

**Q: How do I measure cost per correct answer?**
Tag outcomes in production, then read them back off the gateway's own trace: resolved, escalated, abandoned. Verdryx turns that into a dollar figure per case, including the untagged intermediate calls a run made and the calls the breaker blocked, because both are part of what the outcome cost.

**Q: How do I know when quality has actually dropped?**
A flat threshold catches the obvious fall. Beside it, a two-sample significance check, Welch's t with a bootstrap interval, catches the small consistent regression a threshold tuned for noise would miss. Point it at a baseline whose source run is gone and it fails loudly rather than silently.

**Q: Do I need an LLM judge to use it?**
No. Four of the five graders are deterministic and free: exact, regex, outcome tag and tool trace. The judge is there for the cases a rubric can score and a pattern cannot, and when you use it, its own cost is priced against the same book the money plane uses rather than reported as zero.

**Q: Does it need network access or a key?**
Not for the common path. The eval runner, graders and drift maths import nothing but the standard library, and the whole suite runs against a deterministic stub adapter with no network and no key, which is exactly what its own CI runs.

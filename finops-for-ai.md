<!-- https://it-rat.com/finops-for-ai.html -->

# FinOps for AI

> FinOps applied to LLM and agent spend: the unit of work, per-run budgets, reserve-then-settle, FOCUS showback and cost per resolved case.

Cloud FinOps grew up around resources somebody provisioned: an instance, a bucket, a cluster. LLM and agent spend does not work like that. Nobody provisions it. An agent creates it, in seconds, by deciding to try again, and the same task can cost thirty times more on Tuesday than it did on Monday depending on how the loop unfolds. The practice still applies; the unit of work, the controls and the reporting all have to move.

## Three assumptions that quietly break.

### Spend is no longer provisioned, it is emitted

A rightsizing recommendation assumes something is sitting there costing money. An agent's cost appears when it acts, disappears when it stops, and spikes when it retries. There is nothing to rightsize; there is only a decision to allow or refuse the next call. That moves cost management out of the monthly review and into the request path.

### The billing dimension is the wrong dimension

Providers bill per key and per model. Neither is a unit of business work. A key does not tell you whether a thousand calls were one hard task or two hundred wasted retries, and a model total cannot be charged back to the team that caused it. **The unit that means something is the run:** one task, one budget, one identity, one trace. Every number worth showing finance is an aggregation of runs.

### The feedback loop is too slow to matter

Classic FinOps runs on a monthly cadence because infrastructure spend changes at a monthly pace. A runaway agent settles the question in an afternoon. By the time an anomaly detector on the invoice notices, the money is spent and the only remaining decision is who explains it. The correct alert for agent spend fires before the call, not after the bill.

## What an AI cost-control programme actually contains.

### 1. A unit of work, defined once

Pick the run as the unit and make every plane key on it. That single decision is what later lets a spend line, an incident, a policy decision and a quality score refer to the same identifier instead of four systems arguing about which trace was which.

### 2. Budgets that nest, enforced in the path

A budget per run, rolling up to the agent, the team and the company, checked all-or-nothing so a run cannot fit under its own cap while breaking its team's. Accounting is reserve then settle: the call is priced before it happens, the reserve taken, the real cost settled afterwards, and the call that would cross the cap is refused before the provider sees it. Models the price book does not recognise get a fallback price rather than passing through untracked, because untracked spend is the failure mode this exists to remove. The fallback is a conservative rate, so for a model the book does not yet carry, the figure a team sees is a ceiling rather than the bill. Keep the book current and read the flag on the response that says a fallback was used.

- **Start in shadow mode.** Price and record everything, refuse nothing, and look at what would have been blocked before anything is.

- **Decide the failure mode on purpose.** A cost control's own bookkeeping should fail open: a lost telemetry line must never refuse a call. Whether its policy hook fails open or closed is a real choice with a real cost either way; write it down and fire it once. The shipped launchers fire closed, and that was measured on 2026-09-17: the policy plane stopped, every governed call refused within a third of a second, none of them reaching the provider.

- **Enforce where the money is spent,** in the request path, not in a nightly job that reads yesterday's logs.

### 3. Savings you can name, not a vague percentage

Three mechanisms do most of the work, and each should report separately: a **breaker** that blocks runaway spend outright, a **semantic cache** that serves a repeated question for nothing, and a **model router** that sends routine calls to a cheaper model while hard ones stay on the frontier one. Reporting them as one number invites the question nobody can answer: saved compared to what? Reporting them separately makes each one auditable, and makes it obvious which lever to pull next.

### 4. Showback in a format finance already reads

Agent spend that lives only in an engineering dashboard is invisible to the people who allocate budget. Exported in the FinOps Foundation's FOCUS format, one row per model call, it lands in the same pipelines and dashboards as the rest of the cloud bill, and showback or chargeback by team and business unit stops being a bespoke project. Measured on 2026-09-17 on a box governing two clouds: one export per gateway door, 272 rows for the customer's agents and 5 for the FinOps crew, each row carrying the agent, the run, the team, whether the call was refused and what it settled at.

### 5. Unit economics, not just totals

The number that changes a decision is not monthly spend. It is **cost per resolved case**: tag outcomes in production, then read the cost of every call in the run behind each one, including the intermediate calls nobody tagged and the calls the breaker refused. Take two support agents, one at forty cents a resolved case and one at four dollars: they are different businesses, and the total spend line cannot tell them apart. The tag is one request header, and the same 2026-09-17 run priced every outcome it carried, the refused calls included.

### 6. The line item nobody forecasts: the evidence itself

Every control above produces a record, and the records are the part of an agent programme that grows without anyone deciding to grow it. This is the rare budget line that can be forecast exactly, because it is linear in a quantity you already track: measure the bytes one governed decision writes, multiply by the decisions your fleet will make, add whatever retention your compliance function demands. On AWS and GCP the control plane measured 427.6 and 426.4 bytes per decision, with every decision audited rather than a sample. At 426 bytes, a thousand calls a minute is 614 MB a day, and a 5 GiB volume fills in about nine days.

### 7. Somebody to actually do it

Every part above is work, and it is the work that gets dropped first: the variance nobody wrote up, the shared cost nobody placed, the anomaly queue nobody triaged. [CostCrew](https://it-rat.com/services/costcrew.html) is that practice staffed by agents, with a person on the stamp: analysts hired into desks with a mandate and a spend guard, drafts that change nothing until somebody posts them, and a KPI library that refuses to report a number it cannot compute. Money there is found, never saved, because nothing is saved until a person acts on it.

Two consequences, and both are finance decisions rather than engineering ones. First, supervising an agent is cheap in processor and expensive in gigabytes, so a capacity plan built from CPU alone will be wrong in the only dimension that runs out. Second, retention is a design parameter from day one, not a cleanup task for later: when the audit volume fills, what disappears is not disk, it is the ability to prove to an auditor why each of those costs was permitted. Provability is measured in gigabytes, and it can be priced a year ahead from a single number.

## What to instrument, in what order.

The tools behind each step are open source and run on your own infrastructure: [TokenFuse](https://it-rat.com/services/tokenfuse.html) for the gateway, the budgets, the cache, the router and the FOCUS export, and [Verdryx](https://it-rat.com/services/verdryx.html) for cost per outcome. The wider set of runtime controls, of which cost is one, is laid out in [the agent governance guide](https://it-rat.com/ai-agent-governance.html), and the defensive side in [AI agent security](https://it-rat.com/ai-agent-security.html).

- **What is its unit of work?** If the finest grain is a key or a model, it cannot attribute spend to the team that caused it, and chargeback stays a spreadsheet.

- **Does it refuse, or only report?** A dashboard that shows a runaway at 09:00 and a control that refuses it at 02:00 are different products at similar prices.

- **How does it price a call it does not recognise?** A fallback price keeps spend tracked. Passing unknown models through untracked is the exact hole this category exists to close.

- **Are savings reported per mechanism?** Blocked, cached and routed are three different levers. One combined percentage cannot be audited or acted on.

- **Does it export in a format finance already reads?** Agent spend that lives only in an engineering dashboard is invisible where budgets are actually allocated.

- **What does it cost you when it fails?** Ask which of its failures are open and which are closed, and whether anybody has fired each one on purpose. A cost control that takes the fleet down by accident has traded one incident for a worse one; one that refuses on purpose while its policy plane is unreachable is a decision you should recognise as yours.

## What people ask about AI cost control

**Q: What is FinOps for AI?**
FinOps practice applied to spend that nobody provisions: LLM and agent usage created at machine speed by the decisions of an agent. It keeps the discipline of cloud FinOps, visibility, allocation and optimisation, but moves the unit of work to the run, the control into the request path, and the feedback loop from monthly to immediate.

**Q: How do I control LLM costs in production?**
Route calls through one gateway, give every run a budget that rolls up to its agent, team and company, price each call before it happens, and refuse the call that would cross the cap. Add a semantic cache and a model router to reduce spend without refusing work, and report what each mechanism saved separately.

**Q: Why is a per-key rate limit not enough?**
Because a key cannot tell one agent's honest afternoon from the same key looping on itself, and a limit expressed in requests per minute has no opinion about money. A retry storm stays comfortably inside a rate limit while spending four figures.

**Q: How do I report AI spend to finance?**
Export it in the FinOps Foundation's FOCUS format, one row per model call, so agent spend lands in the same pipelines and dashboards as the rest of the cloud bill. Showback and chargeback by team then reuse the tooling finance already trusts instead of becoming a bespoke project.

**Q: What is cost per resolved case?**
The unit economic that changes decisions: the money spent to actually resolve one piece of work, including the intermediate calls nobody tagged and the calls a breaker refused. An agent at forty cents a resolved case and one at four dollars are different businesses, and a monthly total cannot tell them apart.

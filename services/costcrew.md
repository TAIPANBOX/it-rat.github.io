<!-- https://it-rat.com/services/costcrew.html -->

# CostCrew, the finops plane

> A crew of agents takes your cloud, SaaS and AI bill apart: allocation, chargeback, unit economics, anomalies. Nothing is published until a person stamps it.

Analysts with named missions, budgets and owners take the cloud, SaaS and AI bill apart: allocation, chargeback, unit economics, anomalies and forecasts. Each one is hired into a desk, given a mandate and a monthly guard, and the work it does arrives as a draft. Nothing is published until a person stamps it. On your bill it enforces nothing at all: it watches spend, it does not spend, and it stops nothing out there. On its own crew it does enforce, because a mandate you cannot withdraw is not a mandate: suspend an analyst and its rights go to none, neither queue will hand it new work, and the runner refuses to price anything it still holds.

## A FinOps practice, staffed.

Every frame below is a fresh installation of the binary on its own seeded estate: nineteen thousand charge rows over fourteen months, thirty-nine analysts, twenty sprints. Click any still to open it full screen. The figures are the fixture's, and the console says on each page which of its numbers are real money and which the estate generated.

## A finding becomes a task, a task becomes a draft, a person stamps it.

The detector is two-sided and ranks by money: a fall matters as much as a rise, because a feed that stopped delivering and a workload switched off unnoticed both look like a drop. A Sunday is judged against Sundays, and the baseline is a median with a robust deviation, so last month's spike does not raise the bar for this month's.

### The finding names its rule

Every anomaly carries the rule that judged it, the baseline it was judged against and the day marked on its own series. A queue whose entries cannot be argued with is a queue nobody works.

### The task carries a guard

An analyst gets the task with a mandate, the rights that come with its skills and a spend guard on the row. What it may read follows from what it was hired to do, not from what is convenient.

### Only a person publishes

Work comes back as a draft. A person posts it or returns it, and the return is on the analyst's own card next to its first-pass rate, so a crew that produces confident noise is visible rather than merely busy.

## The path a number takes before anybody is charged for it.

Every screen above shows one station on this line. What no screenshot shows is the line itself, and the gate in the middle of it: an agent can carry a finding all the way to the stamp and no further. Returned work goes back up the dashed path and lands on that analyst's own card, next to its first-pass rate.

## Found, never saved.

One word is load-bearing throughout this console: money is found, never saved, because nothing is saved until somebody acts. A console that reports found money as saved is one whose numbers stop being believed the first time finance checks them against the invoice.

### Shared cost gets a defensible owner

Direct cost needs no product. This is about the part of the bill that arrived with nobody's name on it, placed by a rule a team can read and dispute rather than a figure it must accept.

### Closing a period stops the numbers

An allocation recomputed every time somebody opens the page cannot be charged to anybody: March's number is not April's, and the team is right to refuse it. A closed period freezes, and leaves as a general ledger CSV.

### A measure that cannot be computed refuses

The KPI library reports a number or says by name why it cannot. A practice that measures itself with invented figures is worse off than one that measures nothing.

## Genaryx governs agents. This is a crew of agents that works your bill.

They are floors, not alternatives. [Genaryx](https://it-rat.com/genaryx.html) is the control room over a fleet: it watches what is running now, demands a signature for anything destructive, and stops things. CostCrew's analysts are agents like any other, so Genaryx governs them too. This console runs the other way round: it reads last month's invoices, hands you drafts, and stops nothing. It emits its own work onto the same agent-event bus, so [Trailryx](https://it-rat.com/trailryx.html) can seal it and [Heraldyx](https://it-rat.com/heraldyx.html) can mail you about it.

### Runtime is not the ledger

[TokenFuse](https://it-rat.com/tokenfuse.html) counts a run in micro-dollars while it happens and can kill it. CostCrew counts an invoice line in cents a month later and allocates it. Same money, two questions, and only one of them has a kill switch.

### Hiring is registration

The hire form collects what a Passport needs, so an analyst joins the crew and the estate in one act. In the original, those were two unrelated steps and the second one mostly did not happen.

### It says what it cannot do

Per-agent attribution of AI spend is not possible from an invoice: the charge carries a model and a workload, not an agent. It becomes possible when the calls go through TokenFuse, and until then the console does not pretend. It now reads a cloud bill too: of the eighteen connectors in its catalogue, twelve are built (the AWS and GCP billing exports as FOCUS folders, the TokenFuse FOCUS export, the Anthropic and OpenAI usage reports, SaaS seats, three rightsizing and three budget-recommendation readers) and six, the Azure billing export among them, are specified with their endpoint and not written. The catalogue says which is which, per entry, and so does this page.

## One binary, one directory.

No interpreter, no virtual environment, no second database engine in the process. It listens on loopback by default and expects a proxy in front of it for TLS. First account created at /signup becomes the admin of that installation, so make one before you hand anybody the address.

Measured on a box behind a home router on 2026-09-17: the crew ran beside the single-machine stack through a gateway door of its own, one real model call was settled at USD 0.05811 and the next was refused by a monthly cap set centrally, and the notifier mailed the crew's findings with the owner taken from a passport. The same run found the runner reporting its own estimate as spent, five times under the gateway's settlement, and an import of the box's real AI spend refused by an empty severity field; both were fixed in v0.2.1. No reader for a cloud bill existed then, so the crew worked the generated estate; the current image is v0.5.0, and it has one.

v0.3.0 lets the crew's supervisor settle what its job description already said it could. It now applies an analyst's own option by itself when the amount is at or under the anomaly threshold, and still sends anything larger, anything that is the owner's call and any disagreement between two analysts to the owner. That threshold, T.anomaly, is now USD 2,500, and the urgent one, T.urgent, USD 12,500: half the earlier figures, and recorded as decisions rather than defaults, so more requests reach the owner for the same work. An admin who answers for an owner has to give a reason, and it is recorded on the option, in the journal and on the bus. A task stopped partway keeps the charge the gateway already settled instead of showing zero. The supervisor pass is tested; the console buttons were not run end to end.

v0.4.0 and v0.5.0 bring real money in and keep it honest. The console reads the AWS and GCP billing exports from a synced folder, exact to the micro-dollar, and reconciles the vendors' own usage reports against the gateway's rows. It can sign people in through the organisation's identity provider, run the whole crew on a model the organisation hosts itself, and decide how much of the bill a model is ever shown: everything, the names masked, or totals only. A re-exported gateway trace is counted once, and a call refused for identity is filed under the credential that made it, never under the agent it claimed. The AWS reader was proven on a real export, the GCP one only against a hand-written file, and sign-in only against an identity provider run inside the tests.

1,527 tests, and the repository gates more than the suite: every scenario written in the language of the request is bound to a named test in both directions, and each gate has a case that plants its own fault and requires the gate to go red.

## What a crew of agents can and cannot do to your bill

**Q: Do the agents change anything in my cloud account?**
No. This console reads exports that land in a folder and, where a connector is built, a vendor's usage API, and it writes only its own database. Twelve of its eighteen connectors read today, the AWS and GCP billing exports among them; the Azure billing export is specified and not yet written, and the catalogue says so per entry. It has no credentials that can act, it makes no outbound call while serving a page, and it enforces nothing: every deliverable is a draft until a person stamps it.

**Q: How is this different from the console that kills runs?**
Different question, different clock. [Genaryx](https://it-rat.com/genaryx.html) and [TokenFuse](https://it-rat.com/tokenfuse.html) work in micro-dollars while a run is happening and can stop it. CostCrew works in cents on last month's invoice and allocates it. The crew here are agents like any other, so Genaryx governs them too.

**Q: What does it do about anomalies nobody has time for?**
It ranks them by money rather than by how far out they sit, and it looks both ways: a fall matters as much as a rise, because a feed that stopped delivering looks exactly like a drop. A four sigma move worth three dollars is real, true, and not worth anybody's morning.

**Q: Can it tell me what each AI agent cost?**
Not from an invoice. A charge carries a model and a workload, not an agent, and the console says so rather than inventing an attribution. Route the calls through TokenFuse with an agent id and the same page answers per agent.

**Q: What does it cost to run?**
Nothing to us and nothing to a vendor: one Apache-2.0 binary on a box you already have. What can cost money is a connector, so every entry says whether running it is metered per call, because that is the fact that decides whether an integration is a good idea.

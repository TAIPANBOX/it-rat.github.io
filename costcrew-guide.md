<!-- https://it-rat.com/costcrew-guide.html -->

# CostCrew guide

> How CostCrew works, how to install and configure it, what changed from 1 to 15 October 2026, and what it does not prove yet, in full.

The [CostCrew room](https://it-rat.com/services/costcrew.html) keeps the console, the drawing of one finding end to end, and the common questions. This guide keeps the rest of what the room used to say: how the work moves, how to run and configure it, what changed from 1 to 15 October 2026, and what is not proven yet.

- [At a glance](https://it-rat.com/costcrew-guide.html#overview)

- [How it works](https://it-rat.com/costcrew-guide.html#how-it-works)

- [Found, never saved](https://it-rat.com/costcrew-guide.html#found-not-saved)

- [Where it sits](https://it-rat.com/costcrew-guide.html#where-it-sits)

- [Running it](https://it-rat.com/costcrew-guide.html#run)

- [What changed](https://it-rat.com/costcrew-guide.html#changes)

- [Limits](https://it-rat.com/costcrew-guide.html#limits)

## CostCrew at a glance.

- **A crew of agents works your bill**, and a person stamps every deliverable and decides everything above a set amount.

- **Status:** pre-1.0, and main is supported.

- **Core:** one static binary. **Store:** SQLite, in a directory you name.

- **Reads:** FOCUS from TokenFuse, AWS and GCP billing exports, seats, recommendations; the Azure billing export is specified, not read yet.

- **Enforces:** nothing on your bill, by design. Every deliverable arrives as a draft.

- **Licence:** Apache-2.0.

### What it is

Analysts with named missions, budgets and owners take the cloud, SaaS and AI bill apart: allocation, chargeback, unit economics, anomalies and forecasts. Each one is hired into a desk, given a mandate and a monthly guard, and the work it does arrives as a draft. Nothing is published until a person stamps it. On your bill it enforces nothing at all: it watches spend, it does not spend, and it stops nothing out there. On its own crew it does enforce, because a mandate you cannot withdraw is not a mandate: suspend an analyst and it gets no rights, and no new work can be handed to it.

## A finding becomes a task, a task becomes a draft, a person stamps it.

The detector is two-sided and ranks by money: a fall matters as much as a rise, because a feed that stopped delivering and a workload switched off unnoticed both look like a drop. A Sunday is judged against Sundays, and the baseline is a median with a robust deviation, so last month's spike does not raise the bar for this month's.

### The finding names its rule

Every anomaly carries the rule that judged it, the baseline it was judged against and the day marked on its own series. A queue whose entries cannot be argued with is a queue nobody works.

### The task carries a guard

An analyst gets the task with a mandate, the rights that come with its skills and a spend guard on the row. What it may read follows from what it was hired to do, not from what is convenient.

### Only a person publishes

Work comes back as a draft. A person posts it or returns it, and the return is on the analyst's own card next to its first-pass rate, so a crew that produces confident noise is visible rather than merely busy.

### The path a number takes before anybody is charged for it.

Every screen in the room's gallery shows one station on this line. What no screenshot shows is the line itself, and the gate in the middle of it: an agent can carry a finding all the way to the stamp and no further. Returned work goes back up the dashed path and lands on that analyst's own card, next to its first-pass rate.

### A FinOps practice, staffed: what each frame shows

Every frame in the room's gallery is a fresh installation of the binary on its own seeded estate, with thirty-nine analysts. The figures are the fixture's, and the console says on each page which of its numbers are real money and which the estate generated.

- **The board.** Blocked and returned work sits first on purpose: it is the work that has stopped, and a board that buries it hides its own problems.

- **The crew.** Thirty-nine analysts, 3,871.35 of work across 310 tasks, and a first-pass rate left blank where nothing has been reviewed yet, because a rate over no reviews is not a rate.

- **One analyst.** Its desk and mission, three open tasks of the thirteen it has ever been given, and 173.97 of work against a 60.00 monthly guard.

- **Hiring.** Everything the form asks is a governance fact, asked once. The name becomes part of an agent://<host>/costcrew/<name> identity that other services parse, so one gateway key bound to agent://<host>/costcrew/* covers the crew and nothing else.

- **Anomalies.** Every irregularity ranked by money rather than by how far out it sits, 2,475.10 of it still unexplained. A four sigma move worth three dollars is real and is not worth your morning.

- **One finding.** 2,054.10 above baseline on Amazon EC2, the day marked on its own series, and the rule that judged it: 3.5 robust deviations from the median of the last 28 comparable days.

- **Allocation.** The part of the bill that arrived with nobody's name on it: 136,848.58 direct against 14,540.00 shared, placed by rules a team can argue with rather than by a number it must accept.

- **Chargeback.** Closing a period is what stops the numbers moving, because an allocation recomputed every time somebody opens the page cannot be charged to anybody. Out as a general ledger CSV.

- **Results.** Found, never saved. 1,254.35 found since the board opened against 3,871.35 the crew cost, and the word is load-bearing: nothing is saved until somebody acts.

- **KPIs.** Nine report a number, three refuse and four meet their target. The refusals are the important part: a library where everything reports is one where several of the figures are invented.

- **Connectors.** Every entry says which table it fills, what it needs, and whether running it costs money, because that last one is what decides whether an integration is a good idea.

- **Audit.** Everything the console did, in order, each entry hashed against the one before it. Tamper-evidence rather than tamper-proofing, and the page says which one it is.

- **Rightsizing.** What the providers' own exports say is paid for at a size nobody uses, ranked by the saving rather than by the instance name, and flagged where a fourteen day window would call a monthly job idle. A list, never something the console applies.

- **SaaS seats.** Sixty of 315 seats issued and not signed into in thirty days, 4,047.00 a month at what is actually paid, and one renewal inside ninety days whose notice deadline falls before it.

- **Cadence.** Thirty-one tasks are due today at a worst case of 2.3050, and not one of them runs: the switch is off and the ceiling is 0.00, and both of those are a person's own act.

- **The plan.** Sixty-seven items proposed under a 1,043.00 ceiling, and nothing exists until somebody approves it. A planner that writes straight to the board has spent the budget before anybody agreed to the work.

- **Owner and told.** Every finding carries the owner it belongs to, read from the team that pays for it or from the analyst that opened it. Telling that owner is its own logged step, so on a fresh install every row still reads not yet.

## Found, never saved.

One word is load-bearing throughout this console: money is found, never saved, because nothing is saved until somebody acts. A console that reports found money as saved is one whose numbers stop being believed the first time finance checks them against the invoice.

### Shared cost gets a defensible owner

Direct cost needs no product. This is about the part of the bill that arrived with nobody's name on it, placed by a rule a team can read and dispute rather than a figure it must accept.

### Closing a period stops the numbers

An allocation recomputed every time somebody opens the page cannot be charged to anybody: March's number is not April's, and the team is right to refuse it. A closed period freezes, and leaves as a general ledger CSV.

### A measure that cannot be computed refuses

The KPI library reports a number or says by name why it cannot. A practice that measures itself with invented figures is worse off than one that measures nothing.

## Genaryx governs agents. This is a crew of agents that works your bill.

They are floors, not alternatives. [Genaryx](https://it-rat.com/genaryx.html) is the control room over a fleet: it watches what is running now, demands a signature for anything destructive, and stops things. CostCrew's analysts are agents like any other, so Genaryx governs them too. This console runs the other way round: it reads last month's invoices, hands you drafts, and stops nothing. It emits its own work onto the same agent-event bus, so [Trailryx](https://it-rat.com/services/trailryx.html) can seal it and [Heraldyx](https://it-rat.com/services/heraldyx.html) can mail you about it. Optionally it asks [Typryx](https://it-rat.com/services/typryx.html) for a typed hint about each open anomaly, a suggestion an analyst may disagree with and never an action.

### Runtime is not the ledger

[TokenFuse](https://it-rat.com/services/tokenfuse.html) counts a run in micro-dollars while it happens and can kill it. CostCrew counts an invoice line in cents a month later and allocates it. Same money, two questions, and only one of them has a kill switch.

### Hiring is registration

The hire form collects what a Passport needs, so an analyst joins the crew and the estate in one act. In the original, those were two unrelated steps and the second one mostly did not happen.

### It says what it cannot do

Per-agent attribution of AI spend is not possible from an invoice: the charge carries a model and a workload, not an agent. It becomes possible when the calls go through TokenFuse, and until then the console does not pretend. It now reads a cloud bill too: of the eighteen connectors in its catalogue, twelve are built (the AWS and GCP billing exports as FOCUS folders, the TokenFuse FOCUS export, the Anthropic and OpenAI usage reports, SaaS seats, three rightsizing and three budget-recommendation readers) and six, the Azure billing export among them, are specified with their endpoint and not written. The catalogue says which is which, per entry, and so does this page.

## One binary, one directory.

No interpreter, no virtual environment, no second database engine in the process. It listens on loopback by default. From v0.10.0 it refuses to start on any other address unless a TLS proxy is in front and -behind-tls is set, or -insecure-http says plain HTTP is intended there. First account created at /signup becomes the admin of that installation, so make one before you hand anybody the address.

```
go install github.com/TAIPANBOX/costcrew/cmd/costcrew@latest
# then: costcrew -data ./local
```

```
# the whole local stack with the console on :8321, from TAIPANBOX/stack-up
./up.sh --with-finops
```

### A measured run

Measured on a box behind a home router on 2026-09-17: the crew ran beside the single-machine stack through a gateway door of its own, one real model call was settled at USD 0.05811 and the next was refused by a monthly cap set centrally, and the notifier mailed the crew's findings with the owner taken from a passport. The same run found the runner reporting its own estimate as spent, five times under the gateway's settlement, and an import of the box's real AI spend refused by an empty severity field; both were fixed in v0.2.1. No reader for a cloud bill existed then, so the crew worked the generated estate; the current release is v0.10.0, and it reads the AWS and GCP billing exports.

### The supervisor settles what it may

v0.3.0 lets the crew's supervisor settle what its job description already said it could. It now applies an analyst's own option by itself when its figure is at or under the anomaly threshold (for an option tied to an anomaly the figure is the excess the detector recorded, since v0.7.0, and an option whose figure differs goes to the owner with both numbers), and still sends anything larger, anything that is the owner's call and any disagreement between two analysts to the owner. That threshold, T.anomaly, is now USD 2,500, and the urgent one, T.urgent, USD 12,500: half the earlier figures, and recorded as decisions rather than defaults, so more requests reach the owner for the same work. An admin who answers for an owner has to give a reason, and it is recorded on the option, in the journal and on the bus. A task stopped partway keeps the charge the gateway already settled instead of showing zero. The supervisor pass is tested; the console buttons were not run end to end.

### Real money in, kept honest

v0.4.0 and v0.5.0 bring real money in and keep it honest. The console reads the AWS and GCP billing exports from a synced folder, exact to the micro-dollar, and reconciles the vendors' own usage reports against the gateway's rows. It can sign people in through the organisation's identity provider, run the whole crew on a model the organisation hosts itself, and decide how much of the bill a model is ever shown: everything, the names masked, or totals only; from v0.10.0 the default is masked. A re-exported gateway trace is counted once, and a call refused for identity is filed under the credential that made it, never under the agent it claimed. The AWS reader was proven on a real export, the GCP one only against a hand-written file, and sign-in only against an identity provider run inside the tests.

### Announced decisions

v0.6.0, released on 2026-10-13, lets a cost decision the crew recommends be announced before it lands. Only the owner can confirm an announcement. From its first day the anomaly queue and the forecast read it: a day that lands as announced is not raised, and one that lands short, late or in the wrong direction is, with the decision's name on it. A saving cannot be larger than the median daily spend it saves on, and the forecast carries an announced step before it lands. The Anthropic price rows are the vendor's list rates, as read on 2026-10-13. The release is plain about what it does not prove yet: every run in it used the generated estate, so detection quality and forecast accuracy on real spend are still open.

### What the repository gates

The repository gates more than its suite: every scenario written in the language of the request is bound to a named test in both directions, and each gate has a case that plants its own fault and requires the gate to go red.

## What the crew gained from 1 to 15 October

| shipped in | what it does |
|---|---|
| v0.4.0 | Provider usage is read from the vendors' own usage reports and reconciled against the gateway's rows, so the gap between the two is shown. |
| v0.4.0 | Sign-in through the organisation's identity provider, over OpenID Connect with signed tokens and PKCE. Session tokens are stored hashed. |
| v0.6.0 | A cost decision the crew recommends can be announced before it lands. Only the owner can confirm it, and a day that matches the announcement is not raised as an anomaly. |
| v0.7.0 | A FOCUS 1.1 file of agent spend, by agent, unit, model and credential, for a FinOps platform's custom ingress (the costcrew-cloudability binary in the image). No file has been accepted by a live tenant yet. |

## What it does not do, and what is not proven yet.

- **On your bill it enforces nothing at all:** it watches spend, it does not spend, and it stops nothing out there.

- Per-agent attribution of AI spend is not possible from an invoice: the charge carries a model and a workload, not an agent. It becomes possible when the calls go through TokenFuse, and until then the console does not pretend.

- Of the eighteen connectors in its catalogue, twelve are built and six, the Azure billing export among them, are specified with their endpoint and not written.

- The supervisor pass, which applies an analyst's own option by itself, is tested; the console buttons were not run end to end.

- The AWS reader was proven on a real export, the GCP one only against a hand-written file, and sign-in only against an identity provider run inside the tests.

- Release gates through v0.10.0 ran on the generated estate and on test fixtures, so detection quality and forecast accuracy on real spend are still open.

- The FOCUS 1.1 file of agent spend (costcrew-cloudability, in the image since v0.7.0) has not been accepted by a live tenant yet.

- The figures in the console frames are the fixture's, and the console says on each page which of its numbers are real money and which the estate generated.

- The audit chain is tamper-evidence rather than tamper-proofing, and rightsizing is a list, never something the console applies.

## Back to the room.

The [CostCrew room](https://it-rat.com/services/costcrew.html) has the seventeen frames, the drawing and the common questions, and [the guides index](https://it-rat.com/guides.html) has the field itself.

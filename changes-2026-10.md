<!-- https://it-rat.com/changes-2026-10.html -->

# What changed in the stack, 1 to 15 October 2026

> Prices that match the bill, money that is never forgotten, tool calls judged before they run: what changed in the stack from 1 to 15 October 2026.

What changed in the services in the first half of October, why each change matters, and what it improves for the people who run AI agents and pay for them. It is grouped by the problem each change solves, not by repository, because most problems were solved by several services moving together. **Each service's own list is at the end, under its name.**

- [At a glance](https://it-rat.com/changes-2026-10.html#at-a-glance)

- [Releases, day by day](https://it-rat.com/changes-2026-10.html#releases)

- [How the work is done](https://it-rat.com/changes-2026-10.html#method)

- [1. Prices that match the vendor's bill](https://it-rat.com/changes-2026-10.html#prices)

- [2. Money that is never forgotten](https://it-rat.com/changes-2026-10.html#retained-money)

- [3. Tool calls judged before they run](https://it-rat.com/changes-2026-10.html#tool-calls)

- [4. A typo can no longer switch a control off](https://it-rat.com/changes-2026-10.html#safe-defaults)

- [5. Every refusal filed under the right name](https://it-rat.com/changes-2026-10.html#identity-evidence)

- [6. FinOps that knows what was decided](https://it-rat.com/changes-2026-10.html#finops)

- [7. Running it day to day](https://it-rat.com/changes-2026-10.html#operations)

- [14 October: breaking it on purpose](https://it-rat.com/changes-2026-10.html#failure-day)

- [What this means for a FinOps practice](https://it-rat.com/changes-2026-10.html#finops-practice)

- [By service](https://it-rat.com/changes-2026-10.html#by-service)

- [Every service, before and after](https://it-rat.com/changes-2026-10.html#before-after)

- [A few terms](https://it-rat.com/changes-2026-10.html#terms)

## Two weeks, in five numbers.

*24*

repositories changed

*532*

pull requests merged

*86*

release tags

*111*

new numbered rules in TokenFuse, CostCrew and Wardryx

day of deliberate failure on two clouds, a home server and two routers

Across 24 repositories we merged 532 pull requests (794 commits without merges) and cut 86 release tags. TokenFuse moved from 1.4.1 to 1.14.0, Wardryx from 1.1.3 to 1.5.0, CostCrew from 0.2.2 to 0.6.0 and Heraldyx from 0.2.5 to 0.7.0, and the two launchers shipped 45 releases between them to carry those versions to real machines.

**How these were counted.** Releases count tags created between 1 and 15 October; "on main" means merged but not yet in a tagged release. Counts were read from each repository's main branch and its merged pull requests on 15 October.

### The seven themes

Each theme opens with the problem in plain words, then lists what changed, then says why it matters for someone who runs agents and owns their cost. A short line at the end names the versions.

- [Prices that match the vendor's bill.](https://it-rat.com/changes-2026-10.html#prices) The gateway's price book now holds every listed model at its list rate, prices long prompts by the vendor's own tiers, and says when a call was priced from a fallback.

- [Money that is never forgotten.](https://it-rat.com/changes-2026-10.html#retained-money) A call that may have been billed but never answered is kept as money owed, survives a restart, and is closed by a named person with evidence.

- [Tool calls judged before they run.](https://it-rat.com/changes-2026-10.html#tool-calls) Tool descriptions are read for poisoning, a tool that changes after approval is refused, memory counts as untrusted text, and streamed answers are judged like any other.

- [A typo can no longer switch a control off.](https://it-rat.com/changes-2026-10.html#safe-defaults) A setting the service cannot read now stops it at start, and a policy with a misspelled rule is refused instead of stored without the rule.

- [Every refusal is filed under the right name and reaches the record.](https://it-rat.com/changes-2026-10.html#identity-evidence) Refusals are filed under the credential that made the call, and the record keeps a single writer per file.

- [FinOps that knows what was decided.](https://it-rat.com/changes-2026-10.html#finops) CostCrew can announce a saving before it lands, so a planned change is judged as a step rather than raised as an anomaly.

- [Running it day to day.](https://it-rat.com/changes-2026-10.html#operations) Alerts with quiet hours and acknowledgements, a console that shows silence and refusals, and launchers with safer defaults.

## Releases, day by day.

Most services released in two bursts: on 4 October, when the shared library, the typed risk signal and the source checks moved together, and from 12 to 15 October, when the work on retained money, tool safety and the failure day landed. The launchers, [stack-single](https://github.com/TAIPANBOX/stack-single) for one machine and [stack-k8s](https://github.com/TAIPANBOX/stack-k8s) for a cluster, release whenever a service they carry moves, which is why they lead the count.

## How the work is done.

The speed is only useful because of the method behind it, and the method is the part a reviewer can check. Every change follows the same loop.

- **A defect becomes a numbered rule.** Each repository keeps its rules (we call them invariants) in its own instructions, next to the test or gate that holds each one. In these two weeks TokenFuse's list grew from 67 to 110 rules, CostCrew's from 52 to 107, and Wardryx's from 22 to 35. The next change cannot quietly undo a fix, because its rule fails first.

- **A test must fail on the broken code before it counts.** A test that has never been red proves nothing, so every new test is run against the unfixed code first.

- **Gates are proven able to catch what they guard.** Each repository plants the fault a gate is meant to catch and requires the gate to fail on it. In TokenFuse this harness was the slowest step of the build, at 27 minutes, so it now runs as four parallel shards, with one more gate proving that the shards together run every case exactly once. CostCrew and stack-k8s did the same.

- **Release notes say what each fix was checked on.** A note states, for example, that a page fix was checked in a browser against a local stub. Nobody has to guess how far a claim goes.

- **Hygiene runs everywhere.** A secret scan now runs on every pull request and every push to main in every repository, with masked output. Security advisories in dependencies were closed within days of publication: the TLS library, the QUIC library, the WebAssembly runtime, a Parquet dependency, and 43 alerts in the gateway dashboard's dependencies. Every Go service moved to the same toolchain.

- **Facts that must agree are checked across repositories.** One cross-repository gate compares every built-in model price table with the vendors' current prices. Another keeps the tool-argument size limit identical in the gateway and in the policy service.

## Prices that match the vendor's bill.

A gateway that enforces budgets is only as good as its price book. When the book did not know a model, the call was charged at a deliberately high fallback rate, USD 15 per million input tokens and 75 per million output. That is safe for a budget, because it never under-counts. It is wrong for a report, because finance reconciles against the invoice and the invoice uses the list rate.

### What changed

- **A row for every listed model.** The book now holds every Claude id Anthropic lists (its own API, Bedrock, Google Cloud and OpenRouter), the Gemini models on Vertex AI, and, from 13 October, the vendors' current prices for Claude Haiku 5.5, the GPT-6 and GPT-5.6 families, GPT-5.5, GPT-5.4, DeepSeek, Kimi K3, GLM-5.3 and GLM-5.1 and Gemini 3.1 Pro Preview. Ids written as `openai/...` are priced at OpenAI's list rate. The rows cite the vendor page they were read from and the date.

- **Long prompts are priced the way the vendor prices them.** A model sold at two rates by prompt length is priced by the prompt each call actually sent: above the threshold (100,000 tokens for Claude Haiku 5.5, 272,000 for OpenAI's tiered models, 200,000 for Gemini 2.5 Pro and 3.1 Pro Preview) the whole call is priced at the long rate. The estimate that reserves a budget and the final settlement use the same rule.

- **Reasoning tokens are counted.** A Gemini thinking call is charged the reasoning tokens Google bills, and CostCrew counts a thinking model's reasoning as output tokens.

- **Every call says how it was priced.** A call priced from the fallback is marked in the Cloud, on the dashboard and in the FOCUS export (a new `x_price_basis` column says known or fallback). A gateway shows the book it charges with, and an operator can supply prices in a file.

- **The rest of the stack uses the same prices.** CostCrew's own table was corrected to Anthropic's list rates (Claude Sonnet 5 at 2 / 10 instead of 3 / 15, Claude Opus 5 at 5 / 25 instead of 15 / 75). Verdryx, which scores answer quality per dollar, mirrors the gateway's book. A re-exported trace is counted once in CostCrew, however many times the same calls are exported.

- **A gate keeps it true.** A cross-repository gate compares every built-in price table with the vendors' current prices, so a stale row fails the build instead of a report.

### Why it matters

In FinOps the invoice is the source of truth, and every allocation, showback and forecast inherits the price it starts from. Before these changes, a call to a model the book did not know was reported several times too high, with nothing to say so. Now a price is either the vendor's list rate, cited and dated, or it is visibly a fallback, and the export tells finance which. The reconciliation question changes from "why is this number wrong" to "which rows were estimated".

**For the record:** TokenFuse 1.7.0 (7 to 8 October), 1.8.0, 1.13.0 (13 October) and 1.14.0; CostCrew 0.5.0 and 0.6.0; Verdryx price-book mirrors; the cross-repository price gate.

## Money that is never forgotten.

When a call reaches the provider and no answer comes back (the process crashes, the connection is cut, the request times out), the provider may still bill it. The gateway kept that reservation in memory, so a restart forgot it. A gateway that had just started could also let calls through before it had read which budgets were already spent, and a gateway being stopped could lose its most recent records.

### What changed

- **An unknown outcome is kept as money owed.** The reservation is written to a journal on disk and read back when the gateway starts, on its original run and budget window. A gateway that cannot read its journal refuses to start, rather than serve as if nothing were owed.

- **A person closes it, with evidence.** An administrator closes a retained reservation by attaching evidence and a short-lived token that the operator console mints only after a passkey check. The closure reaches the Cloud the way a settled call does, so budgets stay right after a restart. The feature is off unless a closure secret is set; both launchers can set one shared secret for the gateway and the console.

- **Both moments are on the event bus.** A retained call writes `call_retained` (medium) and a closure writes `retained_closed` (high). The notifier tells a person that money is waiting, with the amount in the subject, and the record keeps the closure beside the console's own log.

- **Nothing is let through before the money state is read.** At start, a call that a budget governs waits (a retryable 503 `seed_pending`) until the gateway has read its control plane. This was found on 14 October, when a freshly started gateway admitted calls for a unit already over its monthly cap.

- **A stop does not lose records.** On shutdown the gateway stops taking calls, delivers what it still holds to the Cloud within five seconds, and logs how many records did not arrive.

- **Ceilings an operator owns.** An operator can cap the budget a caller declares for a run, and the console lets an administrator set and change a business unit's monthly cap.

### Why it matters

In agent systems, spend leaks at the edges: timeouts, crashes, retries, restarts. Finance treats a cost that has probably been incurred but not yet invoiced as an accrual, and these changes give the gateway the same discipline. An unknown is never rounded down to zero; it stays a liability, visible to a person, until someone with authority closes it with evidence, and the record shows who did.

**For the record:** TokenFuse 1.5.0 (run ceiling), 1.9.0 and 1.10.0 (12 October), 1.14.0 (15 October); console money views; Heraldyx 0.4.0 and Trailryx 1.2.0 for the new events; the stack-single and stack-k8s closure secret.

## Tool calls judged before they run.

The damage an agent can do arrives as a tool call: run a command, write a file, send a message, move money. With MCP, tools also describe themselves, and that description is text the model reads and follows. A poisoned description, or a tool that quietly changes after it was approved, can steer the agent. And one path, answers streamed token by token, was not judged at all.

### What changed

- **Tool descriptions are read for five warning signs:** a credential, an order to run another tool, a path to local credentials, text addressed to the model, and hidden text. The same scan runs offline and live in the MCP broker.

- **A tool that changed after it was pinned cannot be called.** With the scan set to block, the broker refuses a call to a tool whose definition it saw change since it was pinned, the attack known as a rug pull.

- **Tools a request declares are read too.** A poisoned description marks the run as a suspected injection, so the policy can act on it; the request itself is not refused.

- **Memory is untrusted.** Text recalled from an agent's memory is judged like text read from a web page: under the starter policy, a run that carries it cannot then run a command, write or send. Engram, on its main branch, now records and returns where each memory came from.

- **Streamed answers are judged like any other.** A tool call inside a streamed answer was not judged; on 14 October one reached an agent and ran. Both wire formats now judge streamed tool calls, and a denied one is cut before it reaches the agent.

- **The policy always gets an answerable request.** Arguments up to 12 KiB go to the policy whole; larger ones are marked as truncated, so the policy still decides. The broker now waits up to 1,000 ms for a decision instead of 50 ms, because a slow deny used to arrive after the broker had given up.

- **Wardryx gained two closed lists and a missing-signal rule.** A policy can name the only tools its agents may use (`allow_tool`) and the only models (`allow_models`). A call whose risk signal never arrived is held for a person (`when_absent: hold`). A risk signal can hold a call but never deny it, and an approval is bound to the exact call a person read.

- **Safer defaults and drills.** The launchers now run the agent firewall in enforce mode by default, and the PII scanners in shadow (they record what they find without blocking). The compliance catalog cites the OWASP MCP Top 10, each row graded by the test that holds it. Mockryx gained drills for a token flood, PII in a prompt, a poisoned tool description and a respelled allow-listed tool, and the template catalog a guardrail for a customer-facing shop.

### Why it matters

A model can be persuaded; a check in the path cannot. Every item above moves a decision out of the model's judgement and into the path of the call, where it gives the same answer every time and can be tested. For a buyer this is the difference between hoping an agent behaves and knowing what stops it when it does not. [Security by design](https://it-rat.com/security-by-design.html) explains the eight decisions this rests on.

**For the record:** TokenFuse 1.10.0 to 1.14.0 (12 to 15 October); Wardryx 1.2.0 (4 October), 1.3.0, 1.4.0 and 1.5.0 (13 to 14 October); stack-single 1.1.29 and 1.1.31; Mockryx and the template catalog on main.

## A typo can no longer switch a control off.

Several settings read a value they did not recognise as "use the weaker mode". A gateway started with `TOKENFUSE_FIREWALL=enfroce` ran in shadow, refusing nothing, while its operator believed it was enforcing. A policy written with `deny_tolls` instead of `deny_tool` was accepted and stored without the rule, and the call it was meant to stop went through.

### What changed

- **Security switches refuse a value they cannot read.** The gateway's mode, the firewall mode and nine more switches (data-loss and PII scanning, the MCP scan, the fail modes, the policy mode and two broker requirements) now stop the gateway at start, naming the variable and the accepted words.

- **Policies are read whole or not at all.** Wardryx refuses a policy write with a field the policy does not declare (400, nothing stored), and loads every document of a policy file or refuses the file, naming the one that failed.

- **No open doors by default.** The key that lifts a run's taint label is minted per install instead of being optional, the Cloud's development key fallback was removed, and client keys and the identity map are checked by the gateway image before anything restarts. CostCrew hashes its session tokens, gives one answer for every failed sign-in, signs people in through the organisation's identity provider (OIDC) and sets security headers.

- **On a cluster**, every server is now required to start with Kubernetes secrets encryption (on 14 October the secrets were found in plain text on the Google Cloud test cluster), and the cost script refuses a machine type it has no price for, instead of pricing it at zero.

### Why it matters

Misconfiguration is the most common way real systems fail, and a control that fails silently is worse than none, because people stop watching what they believe is guarded. The rule now holds across the stack: **unset means the safe default, and misspelt means stop.**

**For the record:** TokenFuse 1.5.0, 1.11.1 and 1.12.0; Wardryx 1.3.1 and 1.3.2 (13 October); CostCrew 0.4.0; stack-single and stack-k8s releases of 4 to 14 October.

## Every refusal filed under the right name.

An audit asks who did something. When a call was refused because its key claimed to be another agent, the refusal was filed under the agent that was claimed, so a misused key could put the blame on an innocent agent. A refused key left no trace on the event bus. And on 14 October a replaced pod kept writing after its successor took over, which broke the chain of its own record.

### What changed

- **Refusals are filed under the credential that made the call**, in the FOCUS export, the Cloud, the dashboard, the console and CostCrew. A call forwarded in identity warn mode is marked as such in every one of them.

- **A refused key is on the bus**, with the reason (missing or unknown) and a fingerprint, never the key itself, and rate-limited. A call that names no agent is filed under a reserved "unidentified caller" subject instead of being dropped.

- **A file may only carry its own sources.** Idryx and Heraldyx refuse an event that claims to come from a service its file is not allowed to carry, so one component cannot speak for another.

- **One writer per record file.** The shared library now locks the event file and chains from the line on disk (agent-stack-go 1.2.0 and 1.3.0). An on-box chain verifier with its own image checks the chains, and it is what flagged the break on 14 October.

- **Private by design.** PII that is found and let through is reported as kinds and counts, never the text. IBANs are detected with their check digits, and decimal numbers are no longer mistaken for card numbers. Vouchryx's public revocation list no longer says who revoked a token or why.

- **One shared vocabulary.** The event specification registered the new types (`call_retained`, `retained_closed`, `dlp_shadow`, `anomaly_hinted`, `chain_broken` and `chain_unchained`), and the record and the notifier learned to read them. Wardryx's `policy_updated` now also names the key that made each change (on main).

### Why it matters

Accountability needs two things: the record must name who actually acted, and it must show that nothing was changed or lost. These changes close both gaps. A refusal now points at the key that made the call, and the record can prove it has one writer and an unbroken chain.

**For the record:** TokenFuse 1.7.0, 1.8.0 and 1.14.0; Idryx 1.1.0 to 1.2.1; Heraldyx 0.3.0 to 0.6.0; agent-stack-go 1.1.0 to 1.3.0; Trailryx 1.1.0 to 1.2.1; Vouchryx 0.2.0; the agent-passport specification on main.

## FinOps that knows what was decided.

A cost optimisation looks like an anomaly to a detector that only sees the trend. Teams either learn to ignore the alerts after every planned change, or they stop announcing changes. CostCrew, the FinOps crew that works through the gateway, moved from 0.2.2 to 0.6.0 in this period.

### What changed

- **Announced decisions.** A recommended change can be announced before it lands: the service, the window, the expected daily change, and optionally the team. Only the owner can confirm it. From then on the anomaly detector judges each day against the announced step: a day that matches is not raised, a day that misses is raised with the decision's name. The forecast carries the step before it lands, and after the month closes each decision shows announced against measured. A saving larger than the service's median daily spend over 28 days is refused.

- **More data in, in FOCUS.** Readers for AWS Data Exports and Google Cloud billing exports in plain FOCUS; readers for the model providers' own usage, reconciled against the gateway's rows; and, on main, a month-to-date FOCUS 1.1 file of agent spend for a FinOps platform's custom ingress. No file has been accepted by a live tenant yet.

- **Showback per customer unit**, with an allocation rule a person stamps, and decided thresholds for anomalies (USD 2,500) and urgent ones (USD 12,500).

- **Control over what a model sees.** A setting decides whether a model is sent full data, masked data or aggregates only, and a model the organisation hosts itself can run the crew. Both were run on 7 and 8 October, from a fully closed network to a cloud model, and the evidence records what went over the wire in each mode.

- **AI spend that reads true.** Spend priced from a fallback is kept apart, PII let through is named, each run shows every model it used with its share, and each gateway door is shown as its own source.

### Why it matters

This closes a loop most FinOps practices leave open. A planned saving no longer floods the anomaly queue, a saving that lands short or late is named, and the forecast and the queue agree with what the owner decided. For agent spend in particular, the data now arrives in the format finance tools already read.

**For the record:** CostCrew 0.3.0 (4 October), 0.4.0 and 0.5.0 (8 October), 0.6.0 (13 October), and the changes merged on 14 and 15 October; runs recorded on 7 and 8 October.

## Running it day to day.

Controls only help if the people running them can trust the signals. An alert stream that pages at 3 a.m. for things that can wait gets muted, and a console that shows only successes hides the moment a gateway goes quiet.

### What changed

- **Alerts people can live with** (Heraldyx 0.7.0). Quiet hours and maintenance windows hold everything below critical and report it when they end. A person can acknowledge a condition for a few hours; its repeats are counted instead of mailed. A critical is never held. A quiet box sends one "alive" mail a day, so silence can no longer be mistaken for a dead notifier.

- **A console that shows what went wrong.** It shows a gateway the Cloud stopped hearing from, refused runs, fallback pricing and identity warnings in the runs table, every model a run used, and business units' monthly caps. Felyx, the console's assistant, checks its own statements about budgets against the data, uses a gateway key of its own, and refuses a provider key pasted where a reference belongs. The [public demo](https://it-rat.com/demo/) now shows the full signed-in console.

- **Launchers with safer defaults.** One-machine installs gained a status command that runs the install's checks against a running stack, an optional second gateway door that speaks the OpenAI wire format on its own keys, and the FinOps console as an optional add-on. On a cluster, DNS runs three replicas with a disruption budget, the policy store keeps a readable replica, a stopped node stops its pods before its network, and optional workloads leave a dead node within 30 seconds.

### Why it matters

Operators judge a system by its bad nights. These changes make the quiet nights quieter and the bad ones louder, and they make the most important signal, that something went silent, visible.

**For the record:** Heraldyx 0.7.0 (15 October); console image 1.1.46; stack-single 1.1.35 and stack-k8s 1.1.46.

## 14 October: breaking it on purpose.

A control nobody has fired is a guess, so on 14 October we broke the running stack deliberately: on a five-node cluster on Google Cloud, a five-node cluster on AWS, a home server, and two small routers running a third-party agent through the gateway. Every run is recorded with its date, machine and evidence. Some results, and what each one changed:

| what we did | what happened | what changed |
|---|---|---|
| Killed each of 14 services on the home server in turn | All 14 restarted in 0.38 to 0.85 s and were healthy within a second | Nothing needed; kept as a baseline |
| Reset all five servers of the Google Cloud cluster at once | Serving again in 327 s with the same state, no manual step | Nothing needed |
| Cut the policy service off from the gateway for about a minute | Calls refused from 2.5 s on, 126 of 155, each naming the closed failure mode | Confirms the failure answer is closed |
| Padded a tool call past 12 KiB | Its risk signal never arrived; the call was allowed | Wardryx 1.4.0 holds a call with no signal; re-measured on both clouds the same day |
| Streamed a tool call after a web read | It reached the agent and ran | TokenFuse 1.14.0 judges streamed tool calls |
| Started a gateway before its control plane | It admitted calls for a unit already over its cap | TokenFuse 1.14.0 waits for the money state |
| Replaced a policy pod | The old pod wrote after the new one; the on-box verifier flagged the broken chain | agent-stack-go 1.2.0 and 1.3.0: one writer per file |
| Ran the security tests on the Google Cloud cluster | Kubernetes secrets were stored in plain text | Every server is now required to start with encryption |

The TokenFuse 1.14.0 fixes were tested against stub providers, not re-measured live; the single-writer lock is pinned in Wardryx but not yet in a Wardryx release. Both are named as open in the run record. [Security by design](https://it-rat.com/security-by-design.html#proven-by-breaking) tells the same day from the side of the controls it tested.

## What this means for a FinOps practice.

- **Reconcile on price basis.** Every exported row now says whether it was priced from the list rate or a fallback. Fallback rows are the ones to chase.

- **Treat unknown outcomes as accruals.** Retained calls are real liabilities with an owner and a closing step; the notifier tells you when one appears.

- **Announce optimisations.** A saving announced before it lands keeps the anomaly queue clean and makes the month-end review a comparison of decided against measured.

- **Feed the tools finance already uses.** Agent spend now arrives as FOCUS, including a file for a FinOps platform's custom ingress, beside the cloud bills it is reconciled with.

- **Ask what fails closed.** For any control, the useful question is what it does when its dependency is down or its setting is wrong. Across the stack the answer is now written down and tested.

## Every service's own list.

The same changes, filed under the service that shipped them. "Shipped in" names the release; on main means merged but not yet in a tagged release. Where a service page used to carry its own list of changes, those lines are here.

### Genaryx the console

- An administrator closes a retained reservation by attaching evidence and a short-lived token that the console mints only after a passkey check.

- An administrator can set and change a business unit's monthly cap.

- It shows a gateway the Cloud stopped hearing from, refused runs, fallback pricing and identity warnings in the runs table, and every model a run used.

- A call refused for identity is filed under the credential that made it, not under the agent it claimed.

- Felyx, the console's assistant, checks its own statements about budgets against the data, uses a gateway key of its own, and refuses a provider key pasted where a reference belongs.

- The [public demo](https://it-rat.com/demo/) now shows the full signed-in console.

### TokenFuse the gateway

| shipped in | what it does |
|---|---|
| v1.5.0 | A gateway mode the gateway cannot read stops it at start. |
| v1.5.0 | An operator can cap the budget a caller declares for a run. |
| v1.7.0 | The price book holds a row for every Claude model Anthropic lists, at its list rate, and the Gemini models on Vertex AI. Before this, a call to a model the book did not know was charged at a fallback rate several times too high. |
| v1.7.0 | A Gemini thinking call is charged the reasoning tokens Google bills, and an operator can supply prices in a file. |
| v1.7.0 | A call refused because its key claimed another agent is exported under the credential that made it, not the agent it claimed. |
| v1.8.0 | The Cloud and the dashboard file that refusal under the credential too, show a refused run as refused, and mark calls priced from the fallback. A gateway shows the book it charges with, and a call forwarded in identity warn mode is marked as such. |
| v1.9.0 | A call whose outcome is unknown is kept as money owed. The reservation survives a restart, and a person closes it with evidence, using a short-lived token that the operator console mints after a passkey check. |
| v1.9.0 | The Cloud's development key fallback is removed. |
| v1.10.0 | A retained call and its closure are written to the event bus, so a notifier can tell a person that money is waiting. |
| v1.10.0 | The MCP broker waits up to 1,000 ms for a policy decision instead of 50 ms, because a slow deny used to arrive after the broker had given up. |
| v1.11.0 | Tool metadata is scanned for five warning signs: a credential, an order to run another tool, a path to local credentials, text addressed to the model, and hidden text. |
| v1.11.0 | With the scan set to block, a tool whose definition changed after it was pinned is refused on the call. |
| v1.11.0 | Tools a request declares are read for poisoning. A poisoned description marks the run as a suspected injection. The request itself is not refused. |
| v1.11.1 | A firewall mode the gateway cannot read, such as `enfroce`, stops it at start instead of running a firewall that refuses nothing. |
| v1.12.0 | Text recalled from an agent's memory is untrusted context. Under the starter policy, a run that carries it cannot then run a command, write a file or reach the network. |
| v1.12.0 | The compliance catalog cites the OWASP MCP Top 10, row by row, against the test that holds each control. |
| v1.12.0 | Nine more security switches (data-loss and PII scanning, the MCP scan, the fail modes, the policy mode and two broker requirements) stop the gateway at start on a value they cannot read. |
| v1.13.0 | Prices for the current OpenAI, Gemini, DeepSeek, Kimi and GLM models are at their vendors' rates. A model sold at two rates by prompt length is priced by the tier each call falls in. A model the book cannot price exactly keeps a fallback rate, and the call says so. |
| v1.13.1 | Tool arguments up to 12 KiB reach the policy whole. Larger arguments are marked as truncated, so the policy still decides. |
| v1.14.0 | A tool call inside a streamed answer is judged like one in a buffered answer, and a denied call is cut before it reaches the agent. |
| v1.14.0 | Nothing a budget governs is admitted until the gateway has read its money state, so a restart cannot admit calls for a unit already over its cap. |
| v1.14.0 | A refused client key reaches the event bus with its reason and a fingerprint of the key, never the key itself. |
| v1.14.0 | IBANs are a kind of personal data the scanner finds, checked by country code, length and check digits, and decimal numbers are no longer mistaken for card numbers. PII that is found and let through is reported as kinds and counts, never the text. |
| v1.14.0 | Every FOCUS export row says whether it was priced from the price book or from the fallback, and ids written as `openai/...` are priced at OpenAI's list rate. |
| v1.14.0 | On shutdown the gateway stops taking calls, delivers what it still holds to the Cloud within five seconds, and logs how many records did not arrive. |

### CostCrew the FinOps crew

| shipped in | what it does |
|---|---|
| v0.3.0 | Decided thresholds for anomalies (USD 2,500) and urgent ones (USD 12,500). |
| v0.4.0 | Provider usage is read from the vendors' own usage reports and reconciled against the gateway's rows, so the gap between the two is shown. |
| v0.4.0 | Sign-in through the organisation's identity provider, over OpenID Connect with signed tokens and PKCE. Session tokens are stored hashed, every failed sign-in gets the same answer, and the console sets security headers. |
| v0.4.0 | Readers for AWS Data Exports and Google Cloud billing exports in plain FOCUS. |
| v0.4.0 | Showback per customer unit, with an allocation rule a person stamps. |
| v0.4.0 | A setting decides whether a model is sent full data, masked data or aggregates only, and a model the organisation hosts itself can run the crew. Both were run on 7 and 8 October, from a fully closed network to a cloud model. |
| v0.4.0 | A thinking model's reasoning is counted as output tokens. |
| v0.5.0 | A re-exported trace is counted once, however many times the same calls are exported, and a call refused for identity is filed under the credential that made it. |
| v0.6.0 | A cost decision the crew recommends can be announced before it lands. Only the owner can confirm it, and a day that matches the announcement is not raised as an anomaly. |
| v0.6.0 | A day that misses the announcement is raised with the decision's name. The forecast carries the step before it lands, after the month closes each decision shows announced against measured, and a saving larger than the service's median daily spend over 28 days is refused. |
| v0.6.0 | Its own price table is corrected to Anthropic's list rates: Claude Sonnet 5 at 2 / 10 instead of 3 / 15, Claude Opus 5 at 5 / 25 instead of 15 / 75. |
| on main | A FOCUS 1.1 file of agent spend, by agent, unit, model and credential, for a FinOps platform's custom ingress. No file has been accepted by a live tenant yet. |
| on main | Spend priced from a fallback is kept apart, PII let through is named, each run shows every model it used with its share, and each gateway door is shown as its own source. |

### Wardryx the policy plane

| shipped in | what it does |
|---|---|
| v1.2.0 | A typed risk signal can hold a call, never deny it, and an approval is bound to the exact tool call a person read. |
| v1.3.0 | A policy can name the only tools its agents may use. A requested tool the list does not name is denied, and no approval can lift that. |
| v1.3.1 | Every document of a YAML policy file, and every value of a JSON policy file, is loaded. A file that does not load stops the service at start, and the error names the part that failed. |
| v1.3.2 | A policy write with a field the policy does not declare is refused with a 400, and nothing is stored. Before, the field was dropped and the write still answered 200. |
| v1.4.0 | A policy can hold a tool call whose risk signal never arrives (`when_absent: hold`), for a person to decide. |
| v1.5.0 | A policy can name the only models its agents may use. A request for any other model is denied on that call. |
| on main | A policy change made through the API names, on the event bus, the fingerprint of the key that made it. |
| on main | The shared library's single-writer lock is pinned, so a replaced pod cannot break its own chain. Not yet in a Wardryx release. |

### Idryx the identity graph

| shipped in | what it does |
|---|---|
| v1.1.0 | An event is ingested as the source it claims only when its file may carry that source, so one component cannot speak for another. |
| v1.2.0 | The second gateway door's file, the one that speaks the OpenAI wire format, is ingested as TokenFuse. Before, it was refused as a foreign source, so that door's agents never reached the graph. |
| v1.2.1 | Event types and sources that no detector reads are named as such, not reported as unknown. |

### Scopyx the egress gate

- Documentation and toolchain only: the Go toolchain moved to 1.27.2, the shared library pin moved to 1.3.0, the secret scan runs on every pull request, and the README was corrected against the code.

### Vouchryx delegation

| shipped in | what it does |
|---|---|
| v0.2.0 | The public revocation list no longer says who revoked a token or why. |

### Qryx the cryptography inventory

- Documentation, tests and toolchain only: the Go toolchain moved to 1.27.2, the shared library pin moved to 1.3.0, the secret scan runs on every pull request, and a test now checks every environment read against the component manifest.

### Verdryx answer quality per dollar

- On main: its price book mirrors the gateway's, row for row: every listed Claude id, the Gemini rows on Vertex AI, the vendors' prices of 13 October with their long-prompt tiers, and the `openai/...` rows.

### Typryx typed answers and risk signals

| shipped in | what it does |
|---|---|
| v0.4.0 | Ships the `action.risk_class` template, and a reverse proxy that adds a risk signal to a policy decision request. |
| v0.4.1 | A call whose arguments were truncated is counted as a skip, and its log line is rate-limited. Built with Go 1.27.2. |

### Mockryx fire drills

- On main: four drills, for a token flood, PII in a prompt, a poisoned tool description and a respelled allow-listed tool.

- On main: a scenario can carry a tool history and ask the gateway whether a tool call may run.

### Trailryx the record

| shipped in | what it does |
|---|---|
| v1.1.0 | A readiness path on the ingest listener answers 200 while ingest is healthy and 503 once it is degraded. A TLS library security update. |
| v1.2.0 | Reads the gateway's `call_retained` and `retained_closed`, so the record keeps a closure beside the console's own log. |
| v1.2.1 | A TLS library update for four published advisories. |

### Heraldyx the notifier

| shipped in | what it does |
|---|---|
| v0.3.0 | An event is processed as the source it claims only when its file may carry that source. |
| v0.4.0 | Describes the gateway's `call_retained` and `retained_closed`, so a person is told that money is waiting, with the amount in the subject, and the chain verifier's `chain_broken` and `chain_unchained`. |
| v0.5.0 | The second gateway door's file is read as TokenFuse. |
| v0.6.0 | A fix to how the notifier keeps its place in the event file. |
| v0.7.0 | A daily pulse mail says the notifier is running and gives the counts it saw, so a quiet box can no longer look like a dead one. |
| v0.7.0 | Quiet hours hold alerts below critical every day, in a window the operator sets and in the time zone the operator names. |
| v0.7.0 | A maintenance window, opened by hand for up to 24 hours, can hold alerts from one source while that source is being upgraded. |
| v0.7.0 | An operator can acknowledge a known condition for four hours by default, seven days at most. Its repeats are counted instead of mailed, and one mail says how many alerts were held when it ends. |
| v0.7.0 | A critical is never held, whether by quiet hours, a window or an acknowledgement. |

### Engram agent memory

- On main: every stored memory records where it came from, and recall returns it, so an agent framework can treat untrusted memory as untrusted context. The gateway judges recalled memory that way since TokenFuse 1.12.0.

### Platform passport, shared library, Terraform

| shipped in | what it does |
|---|---|
| agent-stack-go v1.1.0 | An on-box chain verifier (agent-conform) with a published image of its own. |
| agent-stack-go v1.2.0 | The chained event writer locks the file and chains from the line on disk, so several writers appending to one file keep one valid chain. |
| agent-stack-go v1.3.0 | A plain event writer takes the same file lock for each append. |
| agent-passport, on main | Six event types registered (`call_retained`, `retained_closed`, `dlp_shadow`, `anomaly_hinted`, `chain_broken`, `chain_unchained`), and a reserved "unidentified caller" subject. |
| Terraform provider, on main | Still 0.2.0 as a release; fixes merged since, among them the passport resource listing `dpop-key` among the attestation methods. |

### stack-single the launcher for one machine

- A status command runs the install's checks against a running stack.

- An optional second gateway door that speaks the OpenAI wire format on its own keys, and the FinOps console as an optional add-on.

- The agent firewall runs in enforce mode by default, and the PII scanners in shadow.

- One shared closure secret can be set for the gateway and the console.

### stack-k8s the launcher for a cluster

- DNS runs three replicas with a disruption budget, the policy store keeps a readable replica, a stopped node stops its pods before its network, and optional workloads leave a dead node within 30 seconds.

- Every server is required to start with Kubernetes secrets encryption.

- The cost script refuses a machine type it has no price for, instead of pricing it at zero.

- The agent firewall runs in enforce mode by default, the PII scanners in shadow, and one shared closure secret can be set for the gateway and the console.

### stack-up the developer launcher

- On main: safer defaults.

### Template catalog policies and drills

- On main: a guardrail for a customer-facing shop, and drills that go with it.

## Every service, before and after.

| service | what it does | before 1 Oct | 15 Oct | releases | PRs merged |
|---|---|---|---|---|---|
| [TokenFuse](https://it-rat.com/changes-2026-10.html#tokenfuse) | Gateway, prices and budgets, MCP broker | 1.4.1 | 1.14.0 | 14 | 97 |
| [Wardryx](https://it-rat.com/changes-2026-10.html#wardryx) | Policy decisions: allow, deny, hold | 1.1.3 | 1.5.0 | 6 | 31 |
| [CostCrew](https://it-rat.com/changes-2026-10.html#costcrew) | FinOps crew and console | 0.2.2 | 0.6.0 | 4 | 60 |
| [Heraldyx](https://it-rat.com/changes-2026-10.html#heraldyx) | Notifier | 0.2.5 | 0.7.0 | 5 | 31 |
| [Idryx](https://it-rat.com/changes-2026-10.html#idryx) | Agent identity graph and detectors | 1.0.0 | 1.2.1 | 3 | 16 |
| [Trailryx](https://it-rat.com/changes-2026-10.html#trailryx) | Tamper-evident record | 1.0.0 | 1.2.1 | 3 | 19 |
| [agent-stack-go](https://it-rat.com/changes-2026-10.html#platform) | Shared library, event writer, chain verifier | 1.0.2 | 1.3.0 | 3 | 16 |
| [Typryx](https://it-rat.com/changes-2026-10.html#typryx) | Typed answers and risk signals | 0.3.0 | 0.4.1 | 2 | 16 |
| [Vouchryx](https://it-rat.com/changes-2026-10.html#vouchryx) | Delegation tokens | 0.1.0 | 0.2.0 | 1 | 10 |
| [Console (Genaryx)](https://it-rat.com/changes-2026-10.html#genaryx) | Operator console and Felyx | image 1.1.19 | image 1.1.46 | - | 40 |
| [Engram](https://it-rat.com/changes-2026-10.html#engram) | Agent memory | 2.4.1 | 2.4.1, provenance on main | 0 | 5 |
| [Mockryx](https://it-rat.com/changes-2026-10.html#mockryx) | Drills | 0.2.1 | 0.2.1, four drills on main | 0 | 13 |
| [Verdryx](https://it-rat.com/changes-2026-10.html#verdryx) | Answer quality per dollar | - | price mirrors on main | 0 | 9 |
| [Qryx](https://it-rat.com/changes-2026-10.html#qryx), [Scopyx](https://it-rat.com/changes-2026-10.html#scopyx) | Crypto inventory, egress gate | 1.0.0, 1.0.1 | unchanged, docs and toolchain | 0 | 22 |
| [agent-passport](https://it-rat.com/changes-2026-10.html#platform) | Event and identity specification | 1.0.0 | six event types registered | 0 | 9 |
| [Terraform provider](https://it-rat.com/changes-2026-10.html#platform) | Infrastructure as code | 0.2.0 | 0.2.0, fixes on main | 0 | 11 |
| [Template catalog](https://it-rat.com/changes-2026-10.html#catalog) | Policies and drills | - | shop guardrail and drills | 0 | 6 |
| [stack-single](https://it-rat.com/changes-2026-10.html#stack-single) | Launcher for one machine | 1.1.15 | 1.1.35 | 20 | 46 |
| [stack-k8s](https://it-rat.com/changes-2026-10.html#stack-k8s) | Launcher for a cluster | 1.1.21 | 1.1.46 | 25 | 55 |
| [stack-up](https://it-rat.com/changes-2026-10.html#stack-up) | Developer launcher | - | safer defaults on main | 0 | 12 |

## A few terms.

**Invariant**
A numbered rule a service must keep, written into its repository with the test or gate that holds it.

**Fail closed**
When a dependency is down, refuse rather than allow. The opposite, fail open, lets everything through while nobody is checking.

**Shadow and enforce**
In shadow a check records what it would have refused; in enforce it refuses.

**Retained reservation**
Money reserved for a call whose outcome is unknown, kept until a person closes it with evidence.

**MCP**
The Model Context Protocol, the common way agents reach tools. The broker stands between the agent and every tool server.

**FOCUS**
The FinOps Foundation's open format for cost and usage data, which the gateway and CostCrew write and read.

[What changed from 16 October to 27 November](https://it-rat.com/changes-2026-11.html) is what came next. [Security by design](https://it-rat.com/security-by-design.html) explains the eight decisions behind the tool-safety and fail-closed work on this page. [The glossary](https://it-rat.com/glossary.html) has the rest of the vocabulary, and [the guides index](https://it-rat.com/guides.html) has every guide.

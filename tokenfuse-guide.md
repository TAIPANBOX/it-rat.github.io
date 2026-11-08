<!-- https://it-rat.com/tokenfuse-guide.html -->

# TokenFuse guide

> How TokenFuse works, how to install and configure it, what changed from 1 to 15 October 2026, and what the default install does not do, in full.

The [TokenFuse room](https://it-rat.com/services/tokenfuse.html) keeps the simulation, the drawing and the common questions. This guide keeps the rest of what the room used to say: how a cap is enforced, where it sits, how to run it, what changed from 1 to 15 October 2026, and what the default install does not do.

- [At a glance](https://it-rat.com/tokenfuse-guide.html#overview)

- [How it works](https://it-rat.com/tokenfuse-guide.html#how-it-works)

- [Where it sits](https://it-rat.com/tokenfuse-guide.html#where-it-sits)

- [Running it](https://it-rat.com/tokenfuse-guide.html#run)

- [What changed](https://it-rat.com/tokenfuse-guide.html#changes)

- [What changed in November](https://it-rat.com/tokenfuse-guide.html#changes-november)

- [Limits](https://it-rat.com/tokenfuse-guide.html#limits)

## TokenFuse at a glance.

- **The breaker between your agents and your invoice.**

- **Release:** pinned tags · ghcr images (no :latest). **Core:** Rust.

- **Ledger:** in-process by default · raft cluster build optional.

- **Enforcement:** HTTP 402, in-line.

- **Proven on:** Hetzner · AWS · GCP.

- **Licence:** Apache-2.0.

### What it is

A fire in next month's bill is too late to fight. TokenFuse is the extinguisher: a drop-in gateway that gives every run a budget, watches its burn in real time, and cuts the circuit with an HTTP 402 the moment a run crosses its budget. Adoption is one base-URL change; no agent framework rewrite, no SDK lock-in.

## Not a dashboard. A set of hands on the wheel.

### Sixty seconds, one runaway

This is a simulation, but not a fantasy: it replays the exact shape of the live validation runs. An agent enters a retry loop against a $0.006 budget. Four calls land. The reserve for the fifth would cross the cap, so the ledger refuses it. [Watch it in the room](https://it-rat.com/services/tokenfuse.html#sim).

### One gateway in the path. One ledger everyone trusts.

Your agent's SDK points at TokenFuse instead of the provider. In the hot path: budgets, loop detection, a model router that downgrades routine calls, a semantic cache, DLP and the Wardryx policy hook. Behind it: the spend ledger, in one process by default; the optional cluster build replicates it with raft, so the gateways of one cluster still admit exactly what one budget allows.

### Per-run budgets

The run is the unit that pays. A sub-agent's run rolls up into its parent run, so its spend has to fit inside every ancestor's budget. Cross the cap and the answer is a clean 402 your framework already understands, not a Slack message at 9am. Since v1.5.0 an operator can also cap the budget a caller declares for its own run: `TOKENFUSE_MAX_RUN_BUDGET_USD` lowers a larger one to the ceiling and the answer says so in `x-fuse-budget-clamped`. The launchers set it to USD 5.00. It bounds each run, not an agent's total: a new run id gets a new ceiling.

### How a cap is actually enforced, and what it costs you

Budgets are hierarchical and checked all-or-nothing. A sub-agent's spend rolls up and is tested against every ancestor it belongs to, so a run cannot slip under its own cap while quietly breaking its parent's. The run is the unit that pays, because a per-key limit cannot tell one agent's afternoon of honest work from the same key looping on itself.

A business unit can also carry a monthly cap, the first budget above the run. It is set in the gateway's identity map, or overridden from the Cloud, and counts the calendar month in UTC; in enforce mode a call that would cross it is refused with a 402. Each gateway counts its own calls on top of a tally it reads from the Cloud when it starts, so that cap is not yet shared across a fleet of gateways.

Accounting is reserve then settle. Each call is priced before it happens, the reserve is taken, and the real cost settles afterwards; a call that would cross the cap is refused before the provider ever sees it. Models the price book does not recognise get a fallback price rather than passing through untracked, because untracked spend is exactly the failure mode this exists to remove.

Adoption is a one-line base-URL swap. Since v1.19.0 the default governed profile enforces budgets; set TOKENFUSE_MODE=shadow and the gateway prices and records everything while refusing nothing, so you can see what would have been blocked before anything is. Its own bookkeeping fails open: a telemetry push or an event write that fails never refuses a call. The one exception is the start: with a Cloud configured, a gateway answers 503 seed_pending (retryable) until it has read its money state, so a restart cannot hand a run its budget again. The one failure mode that is a choice is the policy hook, and the launchers make it for you: all three ship it fail-closed, so a policy plane that cannot be reached refuses every governed call rather than waving it through. That is measured, not read off a config file: on 2026-09-17 the policy plane was stopped under a box governing two clouds and every call came back 403 in 0.3 s until it was started again. The enforcement decision itself is in-process Rust, about 0.4 microseconds at p99. The thing standing between an agent and a four-digit night should not be the slow part.

### Loop detection

A retrying agent looks exactly like a compromised one from the budget's side. A sustained loop trips the breaker, and a fan-out explosion opens an incident in the Cloud, before either becomes a four-digit night.

### Burn forecast

Reserve-then-settle accounting prices each call before it happens, with a built-in price book of the vendors' rates as they read on 2026-10-13, long-prompt tiers included, and a deliberately high fallback rate for a model id it does not know, flagged on the response, so an unknown model is refused sooner rather than tracked never. The estimate is fast and honest about being an estimate.

### Model router

Routine calls ride a cheaper model that still clears your quality bar; hard ones stay on the frontier model. Both ship switched off: the router is off by default, and the cache is off in the gateway and in the launchers.

### Cluster build: a raft-replicated ledger

An optional build that ships as its own image tag (tokenfuse:<tag>-cluster). The default image does not run it. Four nodes on four machines held one shared budget through a leader kill and a real network partition: the majority kept serving, the isolated node could not overspend, nothing split-brained.

### What a budget survives: a crash, a restart, a partition

The images every launcher installs run one gateway with its ledger in memory, and a restart no longer starts every run at zero. Since v1.4.1 the gateway reads each run's spend back from the Cloud before it serves, for runs active in the last 31 days, and since v1.6.0 a gateway at a remote site does the same through a read scoped to its own site. With no Cloud configured there is nothing to read back, and a run starts from zero. The read-back is proven by tests, and the remote-site half on release binaries behind a stand-in for the hub entry, not yet on a live hub. A budget only means something if two gateways racing each other cannot both spend it, and that is what the cluster build is for, a separate build of the same binary: there the ledger is a raft state machine, and the affordability check is linearized across the whole fleet: four nodes on four machines admit exactly what one budget allows, not four copies of it.

In that build, with durable storage on redb, a budget outlives more than a node crash: it survives a full process restart, because a cap that resets when a process dies is a cap an unlucky deploy can hand back to a runaway.

That was tested rather than assumed. A four-node cluster across two datacenters took a leader kill and a real network partition: the majority side kept serving, the isolated node could not overspend, and nothing split-brained. Enforcement then held under a burst of 34 concurrent agents, and the cost accounting was run on the same protocol against Hetzner, AWS and GCP so the numbers could be compared honestly.

### FOCUS export

Agent spend lands in the same FinOps Foundation format as the rest of your cloud bill, so showback and chargeback reuse the pipes and dashboards finance already trusts.

### A label comes from the act, not from a name

A run carries labels for what it has read, the web label for one, and its next tool call is judged with them: after a page was read, a request to run a shell is refused. That label used to follow a tool name the agent reported. The gateway read the name from the conversation the caller sends, so a fetch reported under a name the policy trusts carried that name's labels, and a fetch left out of the conversation carried none. The label now comes from two witnesses that do not depend on that string.

**The MCP broker.** It made the connection, so it knows which server answered. `TOKENFUSE_MCP_UPSTREAM_LABELS="scopyx=web"` classifies an upstream by the server, not by the name a request chose. It needs `TOKENFUSE_MCP_TAINT_GATEWAY`, and the broker refuses to start on a name that matches no upstream or on a classification with no taint gateway. After a classified upstream answers a `tools/call`, and before the answer leaves, the broker reports to `POST /v1/fuse/observed-act` and the gateway puts the labels on the run. The report has no member for a tool name. A call that names no run is refused before anything is forwarded, and an answer whose label the gateway did not take is withheld.

**The provider's answer.** `server_tool_use` and `mcp_tool_use` blocks record a tool the provider ran, such as a built-in search. The gateway reads them, buffered and streamed, and labels the run before that answer's own tool calls are judged. The name map stays as the fallback, and a run carries the union of what the three say.

The event contract does not change: the same `taint_raised` event and the same `mcp_tool_call` and `model_tool_call` stages. A deployment that sets no classification sees no difference, apart from the provider's blocks, which now label.

### One incident per failing provider

A provider that is up but failing fails every call that reaches it, and each call is its own run. The gateway counts the `dependency_failed` events whose dependency is the provider and sends the Cloud one report every two seconds, with the Cloud key it already holds; a report it cannot deliver is dropped, not queued. A provider that has failed `TOKENFUSE_CLOUD_INCIDENT_PROVIDER_FAILURES` calls (three unless set) within ten minutes opens one incident per provider and reporting site, `dependency_failed:provider:NAME` (with `@SITE` appended for a key bound to a site), with severity high, the failures folded into its occurrences and a summary naming the provider and the last detail. It shows on `GET /v1/incidents`, on the stream and in push like any incident.

The route is `POST /v1/provider-failures`, for an admin or ingest key only, and it is held to a caller who may be hostile: the body is bounded, the label is cleaned, and providers past a bound fold into one visible `other` bucket instead of evicting a real one. The provider label is the host and port of `TOKENFUSE_UPSTREAM` with any `user:password@` removed. The per-call event on the bus is unchanged, and the incident names a provider and no agent or run, so it is not exported to the bus. [Heraldyx](https://it-rat.com/services/heraldyx.html) folds the same outage into one mail on its own side.

## The loud neighbor everyone listens to.

TokenFuse asks [Wardryx](https://it-rat.com/services/wardryx.html) before letting a declared tool through, and stamps the verdict on the response. Its Parquet traces are the raw material [Verdryx](https://it-rat.com/services/verdryx.html) prices outcomes from. [Mockryx](https://it-rat.com/services/mockryx.html) attacks it on purpose in pre-prod. [Idryx](https://it-rat.com/services/idryx.html) correlates its events into the identity graph. Everything travels as one envelope, the agent-event, and [Genaryx](https://it-rat.com/genaryx.html) lifts that same signed kill into a console you reach over your own tunnel, where it becomes a passkey break-glass ceremony.

Where this fits in the wider practice: [FinOps for AI](https://it-rat.com/finops-for-ai.html) on managing spend that creates itself, and [AI agent governance](https://it-rat.com/ai-agent-governance.html) on the rest of the runtime controls.

### It stops the spend. Two neighbours stop other things.

A breaker is the right answer to a runaway and the wrong one to a compromised delegation, where the money is affordable and the problem is that the agent may act for somebody at all. [Vouchryx](https://it-rat.com/services/vouchryx.html) ends that authority at every enforcement point at once. And a ceiling in the request path says nothing about the invoice that arrives a month later: [CostCrew](https://it-rat.com/services/costcrew.html) is where a bill gets taken apart, allocated and closed, by a crew of agents whose work a person stamps.

## Running it.

Run it from [the repository](https://github.com/TAIPANBOX/tokenfuse#-get-started), where the one-line command lives beside the image tag it pulls.

Then point `ANTHROPIC_BASE_URL` at `localhost:4100` and give your next run a run id and a budget (the x-fuse-run-id and x-fuse-budget-usd headers). A call with no run id is refused with 400 metering_required. That's the whole migration. Behind a launcher, a header above USD 5.00 is lowered to the operator's ceiling unless the operator raises it.

Want more than the gateway? [Run the live services locally](https://it-rat.com/services/platform.html#run) in one command.

### TokenFuse ships as an image, and since v0.4.3 as binaries

The current release is v1.24.0. The image is the way to run it in front of traffic; the binaries, since v0.4.3, are for a laptop and a first look: one file, `TOKENFUSE_UPSTREAM` set, and it listens. Each address always serves the newest release: the asset names carry no version, so a link saved today still works after the next one. No Windows build yet, and saying so is cheaper than a broken link.

## What the gateway gained from 1 to 15 October

The whole stack's fortnight, TokenFuse among it, is in [the October changelog](https://it-rat.com/changes-2026-10.html#tokenfuse).

| shipped in | what it does |
|---|---|
| v1.7.0 | The price book holds a row for every Claude model Anthropic lists, at its list rate. Before this, a call to a model the book did not know was charged at a fallback rate several times too high. |
| v1.9.0 | A call whose outcome is unknown is kept as money owed. The reservation survives a restart, and a person closes it with evidence, using a short-lived token that the operator console mints after a passkey check. |
| v1.10.0 | A retained call and its closure are written to the event bus, so a notifier can tell a person that money is waiting. |
| v1.11.0 | Tool metadata is scanned for five warning signs: a credential, an order to run another tool, a path to local credentials, text addressed to the model, and hidden text. |
| v1.11.0 | With the scan set to block, a tool whose definition changed after it was pinned is refused on the call. |
| v1.11.0 | Tools a request declares are read for poisoning. A poisoned description marks the run as a suspected injection. The request itself is not refused. |
| v1.12.0 | Text recalled from an agent's memory is untrusted context. Under the starter policy, a run that carries it cannot then run a command, write a file or reach the network. |
| v1.12.0 | The compliance catalog cites the OWASP MCP Top 10, row by row, against the test that holds each control. |
| v1.13.0 | Prices for the current OpenAI, Gemini, DeepSeek, Kimi and GLM models are at their vendors' rates. A model sold at two rates by prompt length is priced by the tier each call falls in. A model the book cannot price exactly keeps a fallback rate, and the call says so. |
| v1.13.1 | Tool arguments up to 12 KiB reach the policy whole. Larger arguments are marked as truncated, so the policy still decides. |
| v1.14.0 | A tool call inside a streamed answer is judged like one in a buffered answer, and a denied call is cut before it reaches the agent. |
| v1.14.0 | Nothing a budget governs is admitted until the gateway has read its money state, so a restart cannot admit calls for a unit already over its cap. |
| v1.14.0 | A refused client key reaches the event bus with its reason and a fingerprint of the key, never the key itself. |
| v1.14.0 | IBANs are a kind of personal data the scanner finds, checked by country code, length and check digits. |
| v1.14.0 | Every FOCUS export row says whether it was priced from the price book or from the fallback. |

## What changed in November

| shipped in | what it does |
|---|---|
| v1.21.0 | A run's taint label comes from what an enforcement point saw: the MCP broker labels a call by the server that answered, and the provider's own tool blocks label the run before that answer's tool calls are judged. |
| v1.21.0 | A provider that keeps failing is one incident in the Cloud console and API, not one per call. |
| v1.22.0 | The MCP broker tells an upstream that labels a run which run is asking, and tells no other, so a read of the web is recorded under the run that asked for it. |
| v1.22.0 | The MCP broker follows no redirect, so the secrets it writes into a body cannot be carried to a host an upstream named, and a tool call in a stream's closing chunk is held like any other. |
| v1.22.0 | A call that searched on the OpenAI door labels its run, so a shell the run asks for afterwards can be refused. |
| v1.22.0 | A response that stopped short is charged the input as reported and the output at the request's cap, under the cost basis PartialUsage. |

## What the default install does not do, and what is not proven yet.

- **The cluster build is optional and ships as its own image tag.** The default image every launcher installs runs one gateway with its ledger in memory.

- A business unit's monthly cap: each gateway counts its own calls on top of a tally it reads from the Cloud when it starts, so that cap is not yet shared across a fleet of gateways.

- The model router and the cache both ship switched off: the router is off by default, and the cache is off in the gateway and in the launchers, so the saving seen in live runs arrives when you turn them on, not by default.

- With no Cloud configured there is nothing to read back, and a run starts from zero.

- The read-back is proven by tests, and the remote-site half on release binaries behind a stand-in for the hub entry, not yet on a live hub.

- The operator's run-budget ceiling bounds each run, not an agent's total: a new run id gets a new ceiling.

- A poisoned tool description marks the run as a suspected injection. The request itself is not refused.

- A label follows an act that passed through an enforcement point. A process with its own socket passes through none.

- A provider's built-in search is labelled and not controlled: nothing can refuse it, and no domain policy reaches it. The OpenAI wire carries its built-in search as annotations and no tool block, so it is not read.

- A deployment gets the broker half of the label by routing its fetch plane through the broker, which is separate wiring.

- No Windows build yet.

- The room's runaway is a simulation, but not a fantasy: it replays the exact shape of the live validation runs.

## Back to the room.

The [TokenFuse room](https://it-rat.com/services/tokenfuse.html) has the simulation, the drawing and the common questions, and [the guides index](https://it-rat.com/guides.html) has the field itself.

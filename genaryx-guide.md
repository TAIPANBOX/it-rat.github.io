<!-- https://it-rat.com/genaryx-guide.html -->

# Genaryx guide

> How the Genaryx console works, how Felyx is held, what every frame shows, how to take it, and what is not yet in the record, in full.

The [Genaryx room](https://it-rat.com/genaryx.html) keeps the fifteen frames, the live demo, the drawing of the plane and the common questions. This guide keeps the rest of what the room used to say: the core, the passkey ceremony and the tunnel in detail, how Felyx is held, what each frame shows, the console beside the stack by hand, taking it, and what is reported but not yet in the record.

- [At a glance](https://it-rat.com/genaryx-guide.html#overview)

- [How it works](https://it-rat.com/genaryx-guide.html#how-it-works)

- [Felyx, the copilot](https://it-rat.com/genaryx-guide.html#felyx)

- [The case file](https://it-rat.com/genaryx-guide.html#case)

- [Every frame](https://it-rat.com/genaryx-guide.html#frames)

- [Beside the stack by hand](https://it-rat.com/genaryx-guide.html#why)

- [Taking it](https://it-rat.com/genaryx-guide.html#run)

- [What changed](https://it-rat.com/genaryx-guide.html#changes)

- [What changed in November](https://it-rat.com/genaryx-guide.html#changes-november)

- [Limits](https://it-rat.com/genaryx-guide.html#limits)

## Genaryx at a glance.

- **One control room over the whole agent stack**, served from your own box and opened in a browser.

- **Core:** one shared Rust core, thin web shell.

- **Signing:** passkey ES256 per action, with an honest software fallback.

- **Remote:** WireGuard, plane off the internet. **Hosting:** self-hosted, any cloud or on-prem.

- **Copilot:** Felyx, local-first. **Crypto:** post-quantum ready, ML-DSA in the Qryx evidence it carries.

- **Licence:** Apache-2.0.

### What it is

The open services each govern one plane of an agent fleet. Genaryx is the console built on top of them for companies that run real fleets. It runs on your own infrastructure and you open it in a browser: money, policy, identity, quality, crypto, memory, drills and evidence in one window, a kill switch confirmed per action by a passkey in your hand, remote reach over its own WireGuard tunnel, and Felyx - a local-first AI copilot that can read everything and touch nothing. Self-hosted on infrastructure you own, any cloud or on-prem: your plane, your data. It is Apache-2.0 like the services under it.

### The open stack stays open.

Genaryx is Apache-2.0, like everything under it. It is the room built on top of the open services, for teams that want one pane of glass, passkey ceremonies and an incident feed instead of a dashboard per plane and a terminal, and you can read every line of it before you run it. The frames here are the real console UI from the demo build, on simulated data for a fictional tier-1 bank, `meridian.example`. The live run is in what is proven.

## Your plane stays yours. Every path in is signed.

The console reaches a client-hosted Cloud from inside your own WireGuard tunnel, so the control plane never faces the internet. Any browser on that tunnel is the whole client story: a desk at noon, a sofa at 2am, same console, same ceremonies. And Felyx sits beside it with no signing key at all.

### One shell. One Rust brain. Hardware where it counts.

### One core, one shell

The browser console is the product, and it is deliberately thin: every screen is a call into one shared Rust command layer - stores, connectors, ceremonies, the graph all live in the core, never in a screen. Written once, tested once, so a command cannot mean one thing in one place and something else in another.

### Hardware signatures, shipped

Kills, budget changes, approval grants, closing a retained reservation, revoking a delegation and stopping an agent are confirmed per action with a passkey on your own device: Touch ID, Windows Hello or a security key. Stop agent asks [Vouchryx](https://it-rat.com/services/vouchryx.html) to ban the agent, so the tokens it holds die at every door that polls the revocation list, then kills each of its open runs on the Cloud. With no passkey enrolled the action is refused until one is enrolled, unless an operator sets GENARYX_WEB_ALLOW_SOFTWARE_CEREMONY; then it still works and is journaled software-signed, labeled honestly.

**What the console signs, and what it writes down.** The console mints a challenge bound to that exact command and its exact arguments, verifies the ES256 assertion server-side, and journals which enrolled credential confirmed it, next to the typed break-glass reason. A signature over a different command, or over the same command with different arguments, does not verify.

No passkey enrolled yet? The action is refused until you enroll one. Only an operator who sets GENARYX_WEB_ALLOW_SOFTWARE_CEREMONY gets the software-signed fallback, labeled honestly, never dressed up as hardware.

Since 2026-10-19 the passkey is required by default: GENARYX_WEB_REQUIRE_PASSKEY is no longer read for its setting, and a stack that still sets it gets the same required mode. stack-up starts no console.

### WireGuard, but yours

Your box runs the WireGuard side and issues each device its own peer config as a QR: scan, connect, done. Inside that tunnel the console answers over HTTPS on its own name and nowhere else, and it never faces the internet.

**Why the tunnel, and what the certificate is actually for.** The tunnel is raised by your own client, not by anything of ours. On the box itself the console is bound to loopback, so the only way in is the tunnel.

The certificate is not decoration: a passkey ceremony cannot run without one, because WebAuthn refuses both an insecure context and a bare IP as the party it binds credentials to.

Every device that holds a way in is listed, and revoking one cuts it off at the next handshake. Issuing and revoking both take a passkey, because a road into the control plane is not something a stolen session should mint quietly. SSH stays for ops; the console does not need it.

### An audit trail that proves itself

Every governance event the stack emits carries the SHA-256 of the event before it, computed over RFC 8785 canonical JSON: one file, one chain, restarts included. Tampering does not hide, it breaks the chain exactly where it happened, and `agent-conform -chain` verifies a journal in one command.

### Post-quantum, already

Evidence packs are tamper-evident two ways: every artifact is kept byte for byte, and a manifest signed with the console's device key (ES256) records each artifact's sha256. A Qryx artifact in the pack keeps its own ML-DSA (FIPS 204) signature; the console does not sign with ML-DSA. And Qryx audits your fleet's own crypto against the NCSC and CNSA 2.0 migration timelines, so you know what will break before an adversary does.

### Self-hosted, your cloud or on-prem

We never run your Cloud plane or hold your data. The plane lives on infrastructure you own - AWS, GCP, Hetzner, any cloud or on-prem - reached only over WireGuard. Nothing to subpoena or breach on our side.

## An AI that reads everything and can touch nothing.

Felyx is the fleet's analyst. It answers money questions with numbers pulled by tools, chains an incident across money, identity, policy and memory into a root cause with cited ids, drafts the kill you were about to write, and annotates the page that wakes you. It is also an AI we can honestly ask you to trust, because the trust is structural, not a system prompt.

### Local first, by default

Out of the box Felyx talks to a model on your own hardware: Ollama, LM Studio, vLLM - any OpenAI-compatible endpoint on localhost or your private network. A residency gate refuses any other destination unless the operator opts out (off by default) or names extra hosts in GENARYX_COPILOT_LOCAL_HOSTNAMES, so a sensitive install cannot leak a prompt or a number by misconfiguration.

### Cloud only if you choose it

An operator can explicitly opt into a bring-your-own-key cloud model - Anthropic or OpenRouter - per install, in config, off by default. The app's residency banner always states which mode you are in; there is no silent fallback.

### Numbers from tools, never vibes

Every figure in an answer comes from a typed read tool over the same connectors the tabs use. The model does not do arithmetic in prose, and when a plane is not configured Felyx says what it cannot see instead of inventing it. Budgets come from a tool that reads the Cloud's own run and unit budgets with their spend, and a draft that states a budget no tool returned is sent back once for revision. Measured on 2026-10-05 on the forge lab against the Cloud's own figures read the same minute; that measurement covered budget statements.

### It points only at what a tool returned

Every run, incident, policy, agent and approval id an answer names, and every dollar amount, must be in the tool results of that same answer. A draft with a finding goes back once, and what stays is taken out statement by statement and named in a note and in the answer's unsupported claims. An explanation of an incident gives no chain through an id that was invented, and none for an incident no tool returned. An id planted in an event's text grounds nothing: only a structured field a tool returned counts.

### Plane text is data, not instructions

Every string a read tool returns is fenced as untrusted data, unless it is a listed structured field shaped like one token. Inside the fence the markup is escaped, so the text cannot close it, and the code that hands a tool result to the model accepts only fenced results, so a result that skips the fence does not compile. The answer lists the text it leans on, and anything in that text that reads like an instruction.

### A card needs a real target

Between a propose tool and a card stands a check: the target must be one a tool returned as that kind of thing, and no plane text may be asking for that action, unless the operator asked in their own words. A refused proposal is listed with the answer instead of becoming a card. The signing key stays absent. This is held by a gate in the console's CI and by a scripted model that obeys the injected line, so the proof rests on the loop around the model and needs no provider.

### Reading a case

Given the [case file](https://it-rat.com/genaryx-guide.html#case) of an incident, Felyx explains the incident from it instead of running a tool loop to gather the facts. It is given the case and no tool, it may cite only ids the case holds, and it proposes nothing; a model that asks for a tool while reading a case gets none. A draft that names a run the case does not hold is corrected once, and then the chain is withheld. A refusal filed under a key can be cited by the key without its prefix. Plane text in a case row reaches the model fenced and grounds nothing. With no model provider the answer is a sentence saying so.

### No signing key. Not restrained - absent.

The copilot crate has no dependency on the signing crate, and a build-time test asserts it stays that way. A proposal becomes action only through the same passkey ceremony a human uses (Touch ID, Windows Hello or a security key); the journal names the human who approved a copilot proposal, and the copilot is never the actor.

### It cannot silence an alert

The hard floor is deterministic code: an over-cap or runaway event fires immediately, before any model is called. Felyx may only add a short annotation inside a strict time budget. A slow, wrong or absent model changes nothing about whether you get alerted.

### Metered like any other agent

Felyx's own LLM calls carry their own run id and agent id, so pointed at the stack's TokenFuse gateway the assistant that watches your budgets has a budget: visible, cappable, killable. Where the gateway runs client keys, Felyx presents its own, named by GENARYX_COPILOT_FUSE_KEY_REF (env:NAME or file:PATH); without it the gateway refuses each question with a 401. Through that gateway, with policy enforced, it answered across the planes and stopped at its run budget with a 402. The thesis, dogfooded.

### Where Felyx can run

- **Ollama**, local

- **LM Studio**, local

- **vLLM**, local

- **any OpenAI-compatible** endpoint, local

- **Anthropic**, BYO key, opt-in

- **OpenRouter**, BYO key, opt-in

## An incident, with what the planes said about it, in one file.

Incident 360 has a Case section: a deterministic case file for an incident, assembled from reads the console already makes. There is no model in it, no new service, no new event type and no write to any plane. Each fact names its plane, its row id and a digest, the SHA-256 of the row, so a changed row gives a different digest, and the same inputs give the same case.

### What goes in

For an incident that is a bus event: the event itself, the run's timeline in time order, and the earlier events of the same type, newest first. From the identity plane, the subject agent's record and its alerts, and its blast radius; an agent the identity plane does not know is an empty answer, not a failure. From the policy plane, the policy status and the run's approvals. From the Cloud, the run's spend and the gateway's decisions on it. From Engram, what memory recalls for that kind of incident.

### A missing plane is a line in the case

A plane that did not answer is a line in the case, and a plane that answered with nothing is told apart from it. A question that was never asked is a line too. Incident 360 lists what was gathered and what is missing in the console's own words, so a case with no reachable plane still has a line for every section.

### A refusal is filed under its key

An identity refusal, such as a key that claimed another agent's name, is filed under the key and not under the agent it claimed. Nothing is asked about the claimed agent, and the identity plane is asked nothing at all.

### Event text is data

Text inside an event stays inside a fact's row, marked as data. It never becomes a label, and the console's own reasons stay plain beside it.

A money, identity or posture incident, or an unknown row, is refused by name and never given an empty case. Reading a case is a viewer read with no ceremony. The demo assembles a case on invented rows, with one plane that did not answer. Felyx can read the case and explain it; see [Felyx](https://it-rat.com/genaryx-guide.html#felyx).

## What each of the fifteen frames shows.

Every frame in the room's gallery is [the demo](https://it-rat.com/demo/), which is the console itself on simulated data: $35,818 of AI spend in the rolling window across 42 agents and 4,466,489 model calls, one runaway already killed by hand and its cap proposed by the copilot. Nothing here is a mock-up and nothing leaves your browser, so you can open the demo, click the same tabs and land on the same screens. The view groups nav in a left rail, keeps a right dock of whatever you pinned to watch, and drills any agent into a single 360 drawer. What this console did on a real box against a live plane, where it killed a runaway on live traffic, is written up in [what is proven](https://it-rat.com/what-is-proven.html).

The room's gallery holds fifteen frames from the demo, and any still opens full screen; the demo is the whole console, every tab, live, with one Rust core behind every screen. [Open the live demo](https://it-rat.com/demo/) to click through the real console yourself: simulated data, nothing leaves your browser.

- **Overview.** $35,818 of AI spend in the rolling window, $3,755 of it recovered by governance, 46 runs live across 4,466,489 model calls, and an incident centre naming every open one.

- **Incidents.** One stream for every plane: idryx shadow tools and an unsanctioned MCP server beside wardryx policy holds and a tokenfuse taint, filtered by source, by severity or by text.

- **Money.** Every run against its cap, with Replay, Cap and Kill on the row, and the governed savings split into blocked runaways, semantic cache and model router.

- **Agent 360.** One agent in one drawer: who delegated to it and whom it delegates to, 140,148 events, its rhythm against a 52 day median, and 31 stops of which none named a person.

- **Statistics.** 42 agents attributed: spend, calls, what was blocked, what an operator stopped by hand, odd behaviour and the worst breach, out as CSV or JSON.

- **Policy.** Six approvals waiting on a human, and a live decision stream where every hold carries its reason: cost approaching the per-run ceiling, or past the human-approval threshold.

- **Identity.** 45 identities off the idryx snapshot, 14 of them privileged, 5 alerts, one attestation gap, and a line saying which button re-reads and which one runs a fresh detect pass.

- **Graph.** 42 agents, 20 users, 61 links, node size following event volume, and the runaway sitting red in the middle of its own delegation chain.

- **Bus Explorer.** The raw bus, 500 events live, and 12 lines the envelope refused named at their file and offset, because a line nobody can parse must not quietly disappear.

- **Web Egress.** Ten fetches: eight through, two refused by policy and by address range, and a note saying a quarter of them were governed at navigation only rather than per request.

- **Quality.** Six eval runs read from verdryx, the latest scoring 0.950 over 30 cases for 36 cents, held against three saved baselines.

- **Copilot.** Felyx on a local model, asked which agent was the runaway: it names it, prices it at $3,828.51, and proposes a cap that a person still has to approve.

- **Memory.** The engram store as the console sees it: 52 memories, 21 facts active, 31 episodic, and a procedural store this version says plainly it does not implement.

- **Posture.** Zonds over the whole stack: governance fail-open with zero policies, idryx reachable off the box, attestation coverage flagged medium, each with the fix written under it.

- **Remote.** It reaches a stack you already run, on Hetzner, AWS, Azure, Google Cloud and eight more or bare metal, over your own WireGuard tunnel plus SSH.

## What the console adds that the stack alone does not.

You can stand up the open stack's live services yourself in one command, and plenty of teams should. Genaryx exists for the moment the fleet stops being a side project: when the person on call is not the person who built it, when an auditor asks for proof, when 2am happens.

|  | The open stack, by hand | Genaryx |
|---|---|---|
| One place to look | Per-service dashboards, curl, logs | One console, twenty tabs over one Rust core |
| Killing a runaway | A curl with an admin key | A break-glass ceremony over a device signature the plane already verifies: a passkey, a typed reason journaled beside it |
| Reaching a private plane | SSH tunnels you babysit | Your box issues each device its own peer config, lists what holds access, and revokes one in a click; the console answers only inside that tunnel |
| On call at 2am | Laptop, VPN, luck | Your console from any browser over your own tunnel, incidents sorted worst-first, and the destructive step re-signed by the passkey in your hand |
| When something is off | You read six dashboards | Felyx explains it across planes with cited ids - and can only propose, never act |
| Proving it to an auditor | Exports from each service | One signed evidence pack: EU AI Act, SR 11-7, SOC 2 mappings built in |
| Where your data lives | Your infrastructure | Still yours: AWS, GCP, Hetzner and other clouds, or on-prem |

## Clone it, run it, fork it.

Clone it, run it, fork it. Apache-2.0, the whole console, with no tier and no key. It comes up on infrastructure you own and it is reached over a tunnel your own box issues, which is the same on the first day as on the hundredth.

Or [run the open stack yourself in one command](https://it-rat.com/services/platform.html#run) today.

The practice this console is built for is written up separately: [AI agent governance and the runtime controls](https://it-rat.com/ai-agent-governance.html), [AI agent security](https://it-rat.com/ai-agent-security.html), and [FinOps for AI](https://it-rat.com/finops-for-ai.html).

## What changed.

The console's own list for 1 to 15 October 2026 is in [the stack's changes](https://it-rat.com/changes-2026-10.html#genaryx).

## What changed in November

| shipped in | what it does |
|---|---|
| on main | Incident 360 has a Case section: a deterministic case file for an incident, assembled from reads the console already makes, each fact naming its plane, its row and a digest. |
| on main | Felyx names only ids and amounts a tool returned, reads plane text as fenced data, and files a card only for a target a tool returned. |
| on main | Felyx can read a case file instead of running a tool loop: it is given the case and no tool, cites only ids the case holds and proposes nothing. |
| on main | A candidate policy is proved against the decisions already recorded (a Wardryx replay) and a candidate budget against the calls already made (a TokenFuse backtest): each says whether it would have stopped the incident and how many other decisions or calls it would have changed, and applies nothing. |
| on main | A case can be sealed as one canonical document, written in the form RFC 8785 fixes, with the operator's decision and the proofs they asked for; its digest is the target of one line in the console's own chain, and sealing changes nothing in any plane. |

## What is reported and not yet in the record, and what it does not do.

### Built, and proven on a live fleet: reported, not yet in the record

- A laptop on the public internet opened the console over a tunnel this box issued itself, with no other route in.

- Issuing a device and revoking one each needed a touch on the operator's own authenticator, journaled `webauthn-es256`.

- Every one of those records carries the hash of the event before it, and the stack's own checker verifies the chain.

- A device-signed kill went through a real fleet, against a plane closed to the internet.

- Felyx, on a live local model, named the caught runaway and filed a capped proposal only a human could approve, on 42 agents.

**The runs described behind each of those lines; none is cited here yet.** A laptop on the public internet imported the peer config this box issued itself, completed a handshake against the box's published UDP port, and opened the console over TLS inside that tunnel, from a machine that had no other route to it. It then enrolled a passkey and issued a second device, and that action was refused until the operator confirmed it on their own authenticator: the journal records it signed `webauthn-es256`, naming the credential they touched. Revoking a device cut it off the same way.

Every one of those records carries the hash of the event before it, and the stack's own conformance checker verifies the chain they sit in. The console has separately driven a real fleet and put a device-signed kill through it, against a plane closed to the internet.

Felyx has run against a live local model, named the caught runaway and what it burned, and filed a capped-budget proposal only a human could approve, on a fleet of 42 agents. No run is cited for this yet.

The practice this console is built for is written up separately: [AI agent governance and the runtime controls](https://it-rat.com/ai-agent-governance.html), [AI agent security](https://it-rat.com/ai-agent-security.html), and [FinOps for AI](https://it-rat.com/finops-for-ai.html).

### Other limits the room states

- The frames are the real console UI from the demo build, on simulated data for a fictional tier-1 bank, `meridian.example`. The live run is in [what is proven](https://it-rat.com/what-is-proven.html).

- The Felyx annotation quoted above is a paraphrase of the annotation felyx writes on a HARD page, not a recorded capture; the deterministic alert goes out first.

- Felyx's budget check was measured on 2026-10-05 on the forge lab against the Cloud's own figures. The check on ids and amounts that came after it is held by tests and a gate in the console's CI.

- With no passkey enrolled an action is refused, unless an operator sets GENARYX_WEB_ALLOW_SOFTWARE_CEREMONY; then it is journaled software-signed, labeled honestly, never dressed up as hardware.

- A Qryx artifact in an evidence pack keeps its own ML-DSA (FIPS 204) signature; the console does not sign with ML-DSA.

- The Memory tab shows a procedural store this version says plainly it does not implement.

- A cloud model for Felyx is opt-in per install, off by default, and the residency banner always states which mode you are in.

## Back to the room.

The [Genaryx room](https://it-rat.com/genaryx.html) has the fifteen frames, the live demo, the drawing and the common questions, and [the guides index](https://it-rat.com/guides.html) has the field itself.

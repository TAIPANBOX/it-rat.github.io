#!/usr/bin/env python3
"""Insert the FAQ block on each page, once, before the footer.

Plain <details>: the answers sit in the HTML whether or not anyone opens
them, so the page stays short without hiding anything from a crawler.
tools/seo.py reads this same markup back out to build the FAQPage data, so
the structured answer and the visible answer cannot disagree.

Run from the repo root:  python3 tools/faq.py   (idempotent)
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
MARK_OPEN = "<!-- faq:auto -->"
MARK_CLOSE = "<!-- /faq:auto -->"

FAQ = {
"genaryx.html": ("common questions", "What the console is, and what it is not", [
 ("Is Genaryx free, or is there a paid tier above it?",
  "<p>It is Apache-2.0, the same licence as every service under it, and an Apache grant on a version already released cannot be taken back afterwards. There is no tier above it, no seat count, no licence key and no account to create.</p>"),
 ("Is it open source, or open core with the useful parts held back?",
  "<p>Open source, and nothing is held back. The console is one repository, <a href=\"https://github.com/TAIPANBOX/genaryx\" target=\"_blank\" rel=\"noopener\">TAIPANBOX/genaryx</a>, and every tab in the screenshots above is built from it. There is no edition kept beside it, held back or otherwise.</p>"),
 ("Is Genaryx a desktop application?",
  "<p>No. The core is a Rust binary running on infrastructure you own, and you open the console in a browser. Nothing is installed on a laptop, which is the point at 2am when the person on call is using whatever machine is nearest. Reaching a private plane is the console's own WireGuard tunnel rather than a VPN somebody has to maintain.</p>"),
 ("What does the console add that the services do not already do?",
  "<p>One window over every plane, and three things no single service has a place to put: a destructive action confirmed by the passkey in your hand and journaled with the reason you typed, an incident feed sorted worst-first across every plane, and one signed evidence pack carrying EU AI Act, SR 11-7 and SOC 2 mappings.</p>"
  "<p>You can run the open stack by hand in one command, and plenty of teams should. The console is for the point where the person on call is not the person who built it.</p>"),
 ]),

"what-is-proven.html": ("common questions", "What people ask about the evidence", [
 ("What makes a validation number worth anything?",
  "<p>A companion run where the same check fails. A check that cannot produce a red result reports green forever and nobody notices, because green is what everyone expected.</p>"
  "<p>The durability sweep is the clearest case here: zero violations across four hundred thousand seeded runs means very little on its own, and means a great deal beside the same sweep with a lying disk, where 17,869 of 20,000 seeds fail.</p>"),
 ("What has been measured on real infrastructure rather than in a simulator?",
  "<p>Process-kill durability across three filesystems, policy-plane throughput on live five-node clusters on three clouds, recall on a full public benchmark rather than a fixture, a crypto scan over 25,586 real binaries and a live TLS endpoint, an adversarial pass against a running cluster that found four real holes, and, on 2026-09-17, the whole stack on a small box behind a home router governing agents in AWS and GCP at the same time through sixteen injected failures.</p>"
  "<p>Each has a limit published beside it, and the limit is part of the claim rather than a disclaimer under it.</p>"),
 ("What has this project got wrong and had to withdraw?",
  "<p>Three published conclusions. That throughput collapses past 64 concurrent callers, which turned out to be a shared-vCPU instance rather than the software. That one hyperscaler was 62% faster, which was a chip generation rather than a cloud. And a prediction that shared storage would be expensive on both, which was wrong on one by a factor of 108.</p>"
  "<p>All three retractions are published next to the claims they replace. A project with no retractions has either published nothing checkable or has not checked.</p>"),
 ("What has not been established yet?",
  "<p>Power has been pulled from a running machine once, on one small box, so durability is still mainly a claim about process death rather than power loss. There has been no external audit of the cryptographic layer. Six of the nine shipped pre-production drills have never been fired at a real gateway. The detectors have not been driven at production scale, and the federation completeness rule is specified with its transport unbuilt.</p>"),
 ("Why publish the things that went wrong?",
  "<p>Because a repository whose history only records its successes is a repository whose claims cannot be checked. The deployment ledger for the cluster now holds 119 entries and 52 of them are our own mistakes rather than platform behaviour, and that ratio is what makes the other classifications worth believing.</p>"),
]),

"first-alert.html": ("common questions", "What people ask before starting", [
 ("What do I actually need before I start?",
  "<p>A Debian or Ubuntu box you control, Docker on it, and somewhere to send mail: your own SMTP server or a corporate relay you already have. That is the whole list.</p>"
  "<p>There is no account to create, no licence key, no trial and no card. Nothing calls home, and there is no hosted plane, so there is nothing to sign up for.</p>"),
 ("Do I need an LLM provider key to try it?",
  "<p>Only if you want real calls. The gateway sits in front of whichever provider you already use, so you need the key you were already using. If you just want to watch the machinery work, it can answer from a stub instead and no provider is called at all.</p>"),
 ("How does an agent get pointed at the gateway?",
  "<p>By changing the base URL it already uses to reach its provider. That is the entire integration: one environment variable, no SDK to adopt and no framework to migrate to. From that moment every call it makes is priced, budgeted and policy-checked in the request path.</p>"),
 ("Is anything exposed to the internet after the install?",
  "<p>No. The gateway publishes to the host's loopback by default, so a machine that just ran an install script has not acquired an internet-facing enforcement plane because nobody typed anything. Opening it is one variable and a decision you make. Re-running the installer will not widen it for you either, because the environment file is left alone once it exists.</p>"),
 ("Why does this guide not list the exact commands?",
  "<p>Because they live in the repository that owns them, and a copy here would be a second place to keep true. It would drift the first time an installer grew a flag, and you would follow the pretty page into an error the README already documents. What a guide can add instead is what each step is for and how it fails.</p>"),
 ("How do I check it works without waiting for a real incident?",
  "<p>Give a run a budget of a fraction of a cent and let an agent loop against it. The gateway answers 402 in the request path, the event lands in the log and the mail arrives, which exercises the whole chain in a minute at no cost. At the default floor the mail is the control plane's budget_exhausted after the second refusal, not the first 402, so loop at least three times. Do this before you rely on it: a guardrail nobody has fired is a claim rather than a control.</p>"),
]),

"two-sites.html": ("common questions", "What people ask before connecting a second site", [
 ("Does a site need a VPN or an open inbound port?",
  "<p>No. A site only makes outbound HTTPS calls to one public entry on the hub, the same kind of connection an agent already makes to its model provider. Nothing at the site accepts a connection from outside, so there is no tunnel to run, no firewall hole to open and no client to install on anyone's machine.</p>"),
 ("Does every model call now travel through the hub?",
  "<p>No. Each site keeps its own gateway, and the call goes from that gateway straight to the provider, priced and budgeted next to the agent that made it. What reaches the hub is the gateway's telemetry and its questions to the policy plane, not the prompts and not the provider traffic.</p>"),
 ("How does the hub know which site it is talking to?",
  "<p>From the key the site pushed with. Each site gets its own pair of keys, bound to its name, and the hub never takes a site's word about who it is. That also means a copied key is that site, so the key file belongs wherever the site's other secrets live.</p>"),
 ("What happens at a site when the link to the hub drops?",
  "<p>What you configured. With the policy plane set to fail closed, the site's gateway refuses calls until the hub is back, which is what a governed fleet should do. Its telemetry is kept in a queue meanwhile and sent when the link returns; in our run nothing was lost.</p>"),
 ("How do I tell a quiet site from a dead one?",
  "<p>By its heartbeat. A gateway with nothing to report still checks in every 30 seconds by default, so the hub shows when each site last reported whether or not it had traffic. Without the heartbeat, an idle site in our run looked nearly five minutes stale; with it, never more than 22 seconds.</p>"),
 ("What does the public entry cost?",
  "<p>The software costs nothing. The entry is a load balancer, and your cloud bills it by the hour for as long as it exists, at that cloud's published rate. It is not part of the default install, so a cluster that never opens it pays nothing extra, and taking it down with the launcher's own script removes the billed part first.</p>"),
]),

"what-runs-where.html": ("common questions", "What people ask about running it", [
 ("Do I need Kubernetes to run this?",
  "<p>No, and most teams should not start there. The same binaries, ports and wiring run as containers on one machine you own, with the gateway published to loopback by default so an install does not quietly create an internet-facing enforcement plane.</p>"
  "<p>A cluster buys node failure tolerance and matches an estate that already runs Kubernetes. It also costs you a shared-storage decision the single machine hides completely.</p>"),
 ("Why does the shared storage line differ so much between clouds?",
  "<p>Because the planes couple through a shared NDJSON event log rather than through APIs, so on Kubernetes that directory needs a ReadWriteMany volume. For the same 5 GiB the published rates are EUR 0 in-cluster on Hetzner, USD 1.80 a month on EFS, and USD 194.56 a month on Filestore, which bills a whole TiB.</p>"
  "<p>Nothing about the software changes. One provider sells the capacity you use and the other sells a minimum you must buy, and a 5 GiB requirement lands inside a 1 TiB block.</p>"),
 ("Is one cloud faster than the other for this?",
  "<p>Not measurably. On matched silicon the policy plane reached 2,449 decisions per second on AWS and 2,479 on GCP, which is 1.2% apart, with p50 latencies of 3.21 ms and 3.22 ms.</p>"
  "<p>An earlier comparison of ours put AWS 62% ahead, and that was a chip generation rather than a cloud: the AWS run used a newer instance family because the equivalent GCP part was quota-blocked. If a benchmark makes two clouds look different, check the instance families first.</p>"),
 ("Does throughput really collapse past 64 concurrent callers?",
  "<p>No, and we published that it did before measuring it properly. Neither dedicated-core cloud loses throughput out to 256 concurrent on either chip generation; only latency grows. The collapse was a property of a shared-vCPU instance, which is to say a noisy neighbour rather than the software. The correction is published alongside the original claim.</p>"),
 ("How much storage does the audit trail actually need?",
  "<p>About 426 bytes per governed decision, measured at 427.6 and 426.4 on two different clouds from the same binary, because every decision is audited rather than sampled. At a thousand governed calls a minute that is roughly 614 MB a day.</p>"
  "<p>It is the line worth planning against, because it is the only one that grows without anybody deciding to grow it.</p>"),
 ("What does a cluster cost per hour rather than per month?",
  "<p>About EUR 0.20 an hour on Hetzner, USD 2.16 on AWS and USD 1.91 on GCP for five nodes at 8 vCPU and 16 GB. The hourly figure is the one that matters, because clusters get created for an afternoon and forgotten: on AWS a six hour session is about USD 13 and leaving it up for a month is about USD 1,575.</p>"),
 ("Can the stack sit in my own building while the agents run in a cloud?",
  "<p>Yes, and it has been measured that way. On 2026-09-17 the single-machine installer went onto a small Debian box behind a home router on carrier-grade NAT, with the gateway published only on a tunnel address; two clusters, one in AWS and one in GCP, joined the tunnel and ran their agents through the box to the real provider, 23 and 29 ms away. Nothing from the internet reaches such a box; the agents come in over the tunnel. The same day a failure matrix of sixteen cases ran on it, and the reboot found the one thing the installer now fixes for you: on a tunnel address, Docker has to start after the tunnel.</p>"),
]),

"one-incident-end-to-end.html": ("common questions", "What people ask about the incident path", [
 ("Which parts of the stack can actually stop a call?",
  "<p>Two: the money plane and the policy plane, because both sit in the request path. The gateway answers 402 before the provider is asked, and the policy decision point answers allow, deny or hold on every call.</p>"
  "<p>The other five read the shared event stream afterwards. That is a deliberate split, and it has a cost worth knowing: by the time the identity plane has an opinion about a run, the call it is reasoning about has already finished.</p>"),
 ("Why does a spend incident alone not raise a high-severity finding?",
  "<p>Because on its own it is an agent having a bad afternoon. The detector wants at least two corroborating facts before it will call something high, and in this walk it gets three: the spend incident, an agent with no attestation on record, and a delegation chain two hops deep.</p>"
  "<p>None of the three services holds all three facts. The severity comes from the join, which is the argument for a separate identity plane rather than a rule inside the gateway.</p>"),
 ("Why does the alert email contain a link instead of a kill button?",
  "<p>Because a link that acts is an unauthenticated capability held by whoever can see or forward the message, and mail security gateways prefetch links, so the action would fire before a human read the sentence beside it.</p>"
  "<p>The link is a coordinate: it opens the panel showing that incident in your own console. The action happens there, behind a sign-in, and anything destructive additionally needs a fresh passkey confirmation bound to that exact command.</p>"),
 ("What does the notifier hold, and what can it reach?",
  "<p>It reads a file and sends mail. It holds no credential for any plane, opens no connection to one, has no API of its own, and can take no action on any agent. That narrowness is the design rather than an implementation detail: it is the one component allowed out of the box, so its blast radius has to stay small enough to state in a sentence.</p>"),
 ("Why does the mail carry identifiers and numbers but no content?",
  "<p>Because event payloads are written by components that sit next to prompts, model output and matched secrets, and mail leaves through a server nobody in your perimeter controls. Values are rendered through an allowlist of keys whose contents must also pass a shape check. A denylist would be one new producer away from leaking.</p>"),
 ("Can I see this fire without waiting for a real incident?",
  "<p>Yes, and you should not trust the path until you have. The pre-production harness replays the same shape at a gateway standing in front of a fake provider: burn the budget and require the 402, request a denied tool and require the refusal, present a forged delegation chain and require rejection. It exits with differentiated codes so CI can tell a real guardrail gap from a broken harness.</p>"),
]),

"index.html": ("common questions", "The questions that come before the demo", [
 ("What is AI agent governance?",
  "<p>Governance is the set of controls that decide what an agent is allowed to do while it is running: a budget it cannot exceed, a policy it must ask before acting, an identity that records who it acts for, a memory that can say where a belief came from, and evidence an auditor can verify afterwards.</p>"
  "<p>Observability tells you what an agent did. Governance decides what it can do next. The two are not substitutes, and only one of them stops a runaway at 3am.</p>"),
 ("Is the stack open source?",
  "<p>Yes, all of it. Apache-2.0, source on <a href=\"https://github.com/TAIPANBOX\" target=\"_blank\" rel=\"noopener\">GitHub</a>: TokenFuse, Wardryx, Idryx, Engram, Qryx, Verdryx and Mockryx, the shared <a href=\"services/platform.html\">contract</a> under them, and <a href=\"genaryx.html\">Genaryx</a>, the console over all of them.</p>"),
 ("Do you host any of this, or see our data?",
  "<p>No. Every plane runs on infrastructure you own: AWS, GCP, Hetzner, any cloud or on-prem, and on-prem is measured rather than merely allowed: on 2026-09-17 the whole stack ran on a small box behind a home router, governing agents in AWS and GCP at the same time. We never run your control plane, hold your keys or store your traffic, so there is nothing on our side to subpoena or breach.</p>"),
 ("What does it cost to try?",
  "<p>Nothing, and no account. Every part of it is Apache-2.0, the console included. One command builds and starts the long-running services locally: see <a href=\"services/platform.html#run\">run the live stack locally</a>. The four that are libraries and CLIs each carry a one-line try-it on their own page.</p>"),
]),

"services/costcrew.html": ("common questions", "What a crew of agents can and cannot do to your bill", [
 ("Do the agents change anything in my cloud account?",
  "<p>No. This console reads exports that land in a folder and, where a connector is built, a vendor's usage API, and it writes only its own database. Twelve of its eighteen connectors read today, the AWS and GCP billing exports among them; the Azure billing export is specified and not yet written, and the catalogue says so per entry. It has no credentials that can act, it makes no outbound call while serving a page, and it enforces nothing: every deliverable is a draft until a person stamps it.</p>"),
 ("How is this different from the console that kills runs?",
  "<p>Different question, different clock. <a href=\"../genaryx.html\">Genaryx</a> and <a href=\"tokenfuse.html\">TokenFuse</a> work in micro-dollars while a run is happening and can stop it. CostCrew works in cents on last month's invoice and allocates it. The crew here are agents like any other, so Genaryx governs them too.</p>"),
 ("What does it do about anomalies nobody has time for?",
  "<p>It ranks them by money rather than by how far out they sit, and it looks both ways: a fall matters as much as a rise, because a feed that stopped delivering looks exactly like a drop. A four sigma move worth three dollars is real, true, and not worth anybody's morning.</p>"),
 ("Can it tell me what each AI agent cost?",
  "<p>Not from an invoice. A charge carries a model and a workload, not an agent, and the console says so rather than inventing an attribution. Route the calls through TokenFuse with an agent id and the same page answers per agent.</p>"),
 ("What does it cost to run?",
  "<p>Nothing to us and nothing to a vendor: one Apache-2.0 binary on a box you already have. What can cost money is a connector, so every entry says whether running it is metered per call, because that is the fact that decides whether an integration is a good idea.</p>"),
]),

"services/vouchryx.html": ("common questions", "Proving and ending a delegation", [
 ("How is this different from just giving the agent an API key?",
  "<p>A key names nobody and ends nowhere. This mints a short-lived token that says which human the agent is acting for, in a nested <span class=\"mono\">act</span> claim, bound to the caller's own key so a copy of the token is useless. When the delegation should end, one revocation ends it at every enforcement point on its next poll of the list, rather than waiting for an expiry.</p>"),
 ("What happens to a token that is already in flight when we revoke it?",
  "<p>Its next use is refused. Enforcement points poll the revocation list, every 12 seconds by default, and refuse anything on it, so the token's own expiry has no say; a call admitted before that poll is not pulled back, and a door that cannot reach the list keeps the last one it fetched and, past a minute, refuses by default. Measured on a live box: a proven chain answered 200, and after the revoke the same token answered 401.</p>"),
 ("Does this replace the delegation chain in the Passport?",
  "<p>No, it is the half the Passport spec deliberately leaves out. The spec says plainly that it names an agent without proving possession, and records who acted for whom without saying when. This provides both, and the record still lives where it lived.</p>"),
 ("Why is there no introspection endpoint?",
  "<p>Because it would put this service on the request path of every enforcement point at once. Verification is offline against published keys instead, and the policy plane keeps answering in single-digit milliseconds.</p>"),
 ("What does it do if it is configured wrong?",
  "<p>It refuses to start and names the variable. A token service that came up trusting nothing would issue nothing and look healthy; one that came up trusting a default would issue everything. Neither failure should be quiet.</p>"),
]),

"services/tokenfuse.html": ("common questions", "How teams put a ceiling on agent spend", [
 ("How do I cap what an AI agent can spend?",
  "<p>Give the run a budget. Every call is priced before it happens, the reserve is taken against that budget, and the call that would cross the cap is refused with an HTTP 402 before the provider ever sees it. Budgets nest, so a run also has to fit inside its agent, team and company caps.</p>"),
 ("What happens to my agent when it hits the budget?",
  "<p>It gets a 402 with the reason, which is a status every framework already understands, and an incident is recorded against that run. Nothing else in the fleet is affected, and the spend that would have followed simply never happens.</p>"),
 ("Do I have to rewrite my agent to use it?",
  "<p>No. It is a one-line base-URL change to a gateway that speaks the Anthropic Messages API and the OpenAI chat completions API. Run it in shadow mode first and it prices and records everything while refusing nothing, so you can see what would have been blocked before anything is. Its own bookkeeping fails open, so a lost event or an unreachable control plane never refuses a call; what happens when the policy plane is unreachable is the deployment's choice, and both launchers ship it closed.</p>"),
 ("Can it catch a retry loop before the bill does?",
  "<p>That is the case it was built for. A sustained loop or a fan-out explosion looks the same as a compromised agent from the budget's side, and both trip the breaker. In the live campaign, the runaway that mattered was caught and killed on the day, not on the invoice.</p>"),
 ("Does it still work with several gateways behind a load balancer?",
  "<p>In the cluster build, yes: the spend ledger is raft-replicated and the affordability check is linearized across the fleet, so five gateways on five machines admit exactly what one budget allows, and that was tested through a leader kill and a real network partition. That build is optional and not what the shipped images run; the default profile is one gateway whose ledger lives in memory and is read back from the Cloud when it starts, each run's spend over the last 31 days, so a restart does not hand a run its budget again. That read-back does not let two gateways share one budget; only the cluster build does.</p>"),
]),

"services/wardryx.html": ("common questions", "Putting a human in front of the expensive actions", [
 ("How do I require human approval before an agent does something expensive?",
  "<p>Set a threshold in policy. Above it the answer to the agent is <span class=\"mono\">hold</span> rather than allow, a human grants or refuses out of band, and the agent resubmits with a signed approval token bound to that agent, run and tool set, and, when the held request named the tool call, to that exact call. The token works once by default. No connection is parked waiting for a signature.</p>"),
 ("What answers can the policy plane give?",
  "<p>Three, and only three: allow, deny, or hold for a human. There is no improvisation and no fourth case, which is what makes the decisions reproducible and arguable after the fact.</p>"),
 ("What happens if the policy service is unreachable?",
  "<p>You choose, per deployment, and the choice is written down. Fail-open treats it as allow, so availability wins and an outage silently disables policy. Fail-closed treats it as deny, so policy wins and an outage blocks every governed action. The shipped launchers choose closed for the gateway, and it was fired on purpose on 2026-09-17: the policy plane stopped, every governed call refused in 0.3 s, none reaching the provider, and the first call after the restart allowed. Started with no policy loaded, Wardryx allows and says so in the log rather than pretending to enforce.</p>"),
 ("Can policies be reviewed like code?",
  "<p>Yes. Budgets, passports and policies are Terraform resources, so they get pull requests, plans and diffs, and an edit made out of band shows up on the next plan instead of quietly persisting.</p>"),
]),

"services/typryx.html": ("common questions", "A typed answer, and what it does and does not do", [
 ("Is typryx required to run the rest of the stack?",
  "<p>No. It is an optional add-on, and every other service keeps its current path unchanged when it is absent. Nothing in this repository or a planned consumer is built to depend on it.</p>"),
 ("What leaves the box when I send it a state?",
  "<p>Only the fields the template's own <span class=\"mono\">fields</span> list names, held by the type system rather than a promise: <span class=\"mono\">internal/backend.Backend.Ask</span> takes a <span class=\"mono\">template.Egress</span>, a type constructible only inside the template package. Measured on a live run: a state carrying <span class=\"mono\">user_email</span> and, separately, <span class=\"mono\">customer_iban</span>, neither reached the backend or the record.</p>"),
 ("Can a probability block anything?",
  "<p>Not here, and not in a consumer. A probability is a signal a policy can threshold; Wardryx's <span class=\"mono\">hold_if_signal</span> rule can turn one into a hold, which a person releases, and never into a deny. That path is built and released, and measured on the stub backend only.</p>"),
 ("How do I know a probability is honest?",
  "<p>Not from the number alone, which is the finding of the calibration run below: every group was 96% to 100% confident on average and right 50% to 73% of the time. <span class=\"mono\">typryx calibration</span> groups by template, version, backend and model, never pooled, and prints accuracy, mean confidence, ECE and Brier against a later truth posted to <span class=\"mono\">/v1/outcome</span>, so calibration is measured rather than assumed.</p>"),
 ("Does typryx need Jev to be useful?",
  "<p>No. Jev is one backend behind one interface, not the contract. The stub backend answers deterministically for tests and demos, and openai-logprobs reaches any OpenAI-compatible server, including a model on your own hardware. Jev has run live (2026-09-30) and was the most accurate of the three data modes on the 434 questions, but it is a hosted service: choosing it sends the fields a question names to TypeSafe AI. With your own model nothing leaves your hardware, and with typryx off the stack runs as it did before.</p>"),
 ("Can I use my own model instead of Jev?",
  "<p>Yes. Point typryx at any OpenAI-compatible server you run, such as Ollama or vLLM, and nothing leaves your hardware. On the same 434 questions a 7B model on a machine with no GPU was less accurate and less well calibrated than Jev, and slower. You can also tune a model on your own questions: typryx keeps an opt-in training log and exports the questions a person has judged, and it measures the new model against the old per template. It does not train or ship a model, and no tune has been run from an export yet.</p>"),
]),

"services/engram.html": ("common questions", "What a memory has to do that similarity search cannot", [
 ("How is this different from a vector database?",
  "<p>A vector store finds text that looks similar. It cannot tell you when a fact was true, where a belief came from, or that two beliefs disagree. Engram ships a vector index too, in-process, and adds the three answers similarity has no concept for: bitemporal validity, a <span class=\"mono\">why()</span> chain back to source episodes, and contradiction detection.</p>"),
 ("Does it need a server, a container or an API key?",
  "<p>None of the three to write a memory. It is one <span class=\"mono\">.engram</span> file on SQLite plus sqlite-vec, in-process, installed with pip. A model only enters the picture when you ask for <span class=\"mono\">reflect()</span>, and even that call can be pointed at a local model or routed through <a href=\"tokenfuse.html\">TokenFuse</a> so thinking has a budget too.</p>"),
 ("Can I delete everything about one person?",
  "<p>Yes, and the cascade is the point. Erasing an entity removes the episodes about them, the facts derived from those episodes, and the graph edges that made them findable, and reports how many of each it deleted. Erasure is agent-scoped, so in a shared store one agent cannot delete another's memories.</p>"),
 ("Does it work with Claude Desktop, Claude Code or Cursor?",
  "<p>Yes, over MCP on stdio, so there is no network listener and no port to guard. Those clients get remember, recall, why and forget against the same store with no integration code.</p>"),
]),

"services/idryx.html": ("common questions", "Counting the identities nobody is counting", [
 ("How do I find every AI agent and service account we actually have?",
  "<p>Idryx reads what Okta, Entra, AWS, GCP and Azure already log, adds the agent-event bus the rest of the stack writes, and stitches all of it into one graph of humans, service accounts, keys, agents and MCP servers. The answer comes from the graph, not from a spreadsheet someone maintained until they left.</p>"),
 ("Will it change anything in my cloud?",
  "<p>No. It is read-only by design: connectors read, and the output is an alert, a bill of materials, or a Terraform diff a human applies. It never writes back.</p>"),
 ("What is an Agent-BOM?",
  "<p>A CycloneDX 1.6 bill of materials for your agents: who owns each one, what runtime it runs on, what it is attested by, and what it can reach. It plugs into the same supply-chain tooling that already ingests your SBOMs.</p>"),
 ("What does it actually detect?",
  "<p>Twenty-seven deterministic detectors in four families: identity threats, non-human identity hygiene, agents and AI, and least privilege. Detection is statistics and rules over the graph; the model is never in the detection path, so every finding is reproducible and defensible in an audit.</p>"),
]),

"services/qryx.html": ("common questions", "Where a post-quantum migration actually starts", [
 ("How do I start a post-quantum migration?",
  "<p>With an inventory, because you cannot migrate what you have not found. Qryx scans binaries, containers, live TLS endpoints, certificates, dependencies and cloud KMS, and returns a cryptographic asset graph graded against the NCSC milestones: discovery by 2028, the highest-priority systems by 2031, everything by 2035.</p>"),
 ("What is a CBOM?",
  "<p>A cryptographic bill of materials in CycloneDX 1.6: one component per unique asset and risk class, with every occurrence attached. It lives in the same supply-chain tooling as your SBOMs, so cryptography stops having its own isolated report nobody reads.</p>"),
 ("Can it fail a build when someone ships a weak key?",
  "<p>Yes. Snapshot the graph as a baseline, and a new weak or quantum-vulnerable asset fails the build with a distinct exit code, with separate codes for a standards violation and a regressed compliance trend. That is the day it matters, not the next audit cycle.</p>"),
 ("Does it find hardcoded keys?",
  "<p>It does, and it counts them honestly: cryptography that exists only in test fixtures is scanned, reported and kept out of the production inventory, with one line saying how much was set aside. Counting fixtures inflates the number you are trying to drive to zero.</p>"),
]),

"services/verdryx.html": ("common questions", "Measuring quality in money, not vibes", [
 ("How do I measure cost per correct answer?",
  "<p>Tag outcomes in production, then read them back off the gateway's own trace: resolved, escalated, abandoned. Verdryx turns that into a dollar figure per case, including the untagged intermediate calls a run made and the calls the breaker blocked, because both are part of what the outcome cost.</p>"),
 ("How do I know when quality has actually dropped?",
  "<p>A flat threshold catches the obvious fall. Beside it, a two-sample significance check, Welch's t with a bootstrap interval, catches the small consistent regression a threshold tuned for noise would miss. Point it at a baseline whose source run is gone and it fails loudly rather than silently.</p>"),
 ("Do I need an LLM judge to use it?",
  "<p>No. Four of the five graders are deterministic and free: exact, regex, outcome tag and tool trace. The judge is there for the cases a rubric can score and a pattern cannot, and when you use it, its own cost is priced against the same book the money plane uses rather than reported as zero.</p>"),
 ("Does it need network access or a key?",
  "<p>Not for the common path. The eval runner, graders and drift maths import nothing but the standard library, and the whole suite runs against a deterministic stub adapter with no network and no key, which is exactly what its own CI runs.</p>"),
]),

"services/mockryx.html": ("common questions", "Rehearsing a defence before it is needed", [
 ("How do I test that my guardrails actually work?",
  "<p>Fire drills. Each scenario is a YAML file describing the request to send and the answer the guardrail must give, aimed at a real gateway with the guardrails live: the breaker's 402, DLP's 403, the deny or hold from the policy plane. No mocked gateway in the middle, so the code you rehearse is the code production traffic meets.</p>"),
 ("Does running the drills spend real money?",
  "<p>No. The provider behind the gateway is fake, so a runaway scenario can burn as much as it likes: the meter it trips is real, the invoice is not. Every hostile input also stays inside your perimeter, because the harness only ever talks to the one gateway URL you hand it.</p>"),
 ("What if a guardrail simply is not configured?",
  "<p>Then a miss is reported as not configured rather than as a gap, and only when there is no evidence anywhere in the run that the feature is live. A core guardrail with no optional declaration is always a finding, and so is a gateway that could not be reached at all. One flag turns even a skip into a failure when you know the guardrail must be there.</p>"),
 ("Can it gate CI?",
  "<p>That is the intended home. Exit 0 means every drill held, exit 1 is a real defensive gap and should fail the build, exit 2 means the harness itself is broken so nothing was proven. Gate on 1, fix the pipeline on 2, and never let the two blur.</p>"),
]),

"services/platform.html": ("common questions", "The contract every service agrees on", [
 ("What is an Agent Passport?",
  "<p>One identifier and one document per agent: an <span class=\"mono\">agent://</span> URI of at most 255 bytes, aligned with SPIFFE without requiring it, and a document naming an owner, a runtime and one of five attestation methods. The delegation chain behind it is ordered root first, acyclic, and capped at 32 entries.</p>"),
 ("Do I have to adopt the whole stack to use the contract?",
  "<p>No. There is no shared runtime and no shared database. Adopting it is a naming agreement plus a few optional fields on events you already emit, which is why a service can add an event type without asking any other service for permission.</p>"),
 ("Can budgets and policies live in version control?",
  "<p>Yes. Three Terraform resources cover budgets, agent passports and policies, published on the public Terraform Registry, so governance gets pull requests, plans and diffs like the rest of your infrastructure. Where the API has no delete, the provider says so instead of pretending.</p>"),
 ("How do I check that my events actually conform?",
  "<p>Run <span class=\"mono\">agent-conform</span>. It carries the canonical JSON Schemas, classifies each file by its own schema field, treats unrecognised content as a failure rather than skipping it quietly, and exits 0 or 1. It has already caught a real 63-versus-64 character hash defect.</p>"
  "<p>On a box, <span class=\"mono\">agent-conform watch-dir</span> re-checks every stream's hash chain and writes a <span class=\"mono\">chain_broken</span> event to its own stream when one breaks; it exits 2 on a usage or I/O error. Both launchers run it by default.</p>"),
]),

"ai-agent-governance.html": ("common questions", "What people ask about agent governance", [
 ("What is AI agent governance?",
  "<p>The controls that decide what an AI agent may do while it is running, rather than the reports that describe what it did. In practice: a budget it cannot exceed, a policy it must ask before acting, an identity that records who it acts for and a provable delegation when it acts for somebody else, a decision before it reaches anything outside, memory with provenance, quality measured in outcomes, drills that prove the guardrails still hold, and a record of all of it somebody who does not trust you can check.</p>"),
 ("How is agent governance different from LLM observability?",
  "<p>Observability is a witness; governance is a brake. A trace tells you afterwards that an agent looped four hundred times against a production API. A budget tells the agent on call five that it may not. Both are useful, but only one of them is standing in the path when it matters.</p>"),
 ("Do I have to adopt all of it at once?",
  "<p>No, and nobody does. The order that works is metering first, then a ceiling, then a decision in front of the web, then naming the actions that need a human, then drawing the identities and making borrowed authority provable, then rehearsing the guardrails in CI, then sealing the record, and only then measuring quality in money. Each step is a separate Apache-2.0 tool and each is useful alone.</p>"),
 ("Does putting controls in the request path slow agents down?",
  "<p>The enforcement decision itself is in-process and measured in microseconds, and the gateway's own bookkeeping fails open, so a lost event never stops a call. What happens when the policy plane is unreachable is a decision the deployment makes on purpose: both launchers ship it fail-closed, and a run on 2026-09-17 measured exactly that, every call refused in 0.3 s until the plane was back. The latency people notice in agent systems comes from models and tools, not from a budget check.</p>"),
 ("Can this run on our own infrastructure?",
  "<p>It is the only way it runs. Every plane is self-hosted on infrastructure you own, any cloud or on-prem, and nothing is sent to us: we never hold your keys, your traffic or your data.</p>"),
]),

"finops-for-ai.html": ("common questions", "What people ask about AI cost control", [
 ("What is FinOps for AI?",
  "<p>FinOps practice applied to spend that nobody provisions: LLM and agent usage created at machine speed by the decisions of an agent. It keeps the discipline of cloud FinOps, visibility, allocation and optimisation, but moves the unit of work to the run, the control into the request path, and the feedback loop from monthly to immediate.</p>"),
 ("How do I control LLM costs in production?",
  "<p>Route calls through one gateway, give every run a budget that rolls up to its agent, team and company, price each call before it happens, and refuse the call that would cross the cap. Add a semantic cache and a model router to reduce spend without refusing work, and report what each mechanism saved separately.</p>"),
 ("Why is a per-key rate limit not enough?",
  "<p>Because a key cannot tell one agent's honest afternoon from the same key looping on itself, and a limit expressed in requests per minute has no opinion about money. A retry storm stays comfortably inside a rate limit while spending four figures.</p>"),
 ("How do I report AI spend to finance?",
  "<p>Export it in the FinOps Foundation's FOCUS format, one row per model call, so agent spend lands in the same pipelines and dashboards as the rest of the cloud bill. Showback and chargeback by team then reuse the tooling finance already trusts instead of becoming a bespoke project.</p>"),
 ("What is cost per resolved case?",
  "<p>The unit economic that changes decisions: the money spent to actually resolve one piece of work, including the intermediate calls nobody tagged and the calls a breaker refused. An agent at forty cents a resolved case and one at four dollars are different businesses, and a monthly total cannot tell them apart.</p>"),
]),

"ai-agent-security.html": ("common questions", "What people ask about securing agents", [
 ("What is different about securing an AI agent?",
  "<p>The actor reasons and can be talked into changing its mind, but the damage still arrives as a tool call: a write, a transfer, a shell command, a request carrying a credential. That makes the tool boundary the place to defend, with the same discipline as any service account: identity, least privilege, blast radius, evidence.</p>"),
 ("How do I stop prompt injection from reaching a tool?",
  "<p>Not with a better prompt. Taint-track what came from outside the trust boundary and refuse the actions it reaches, at the policy point, per call. A system prompt asking the model not to do something is a request; a decision point that denies the call is a control.</p>"),
 ("What is excessive agency?",
  "<p>OWASP's LLM06: an agent that reaches admin-equivalent power through its delegation chain rather than through its own grants. Its own permissions look modest, and two hops away it can do anything. Finding it needs the chain drawn as a graph, because no permission list on a single identity will show it.</p>"),
 ("How do I know an agent is not exfiltrating data slowly?",
  "<p>Correlate rather than count. A single blocked action is noise; a stream of blocked actions from one identity inside a day is a pattern, and severity should rise with repetition and with the privilege of the identity doing it.</p>"),
 ("How do we prove our guardrails still work?",
  "<p>Rehearse them in CI against a real gateway with a fake provider behind it, so the meter that trips is real and the invoice is not. And refuse to count an unconfigured feature as a pass: a guardrail that is switched off looks exactly like one that is broken.</p>"),
]),

"ai-observability-vs-governance.html": ("common questions", "Where one ends and the other begins", [
 ("What is the difference between LLM observability and AI governance?",
  "<p>Observability reconstructs what an agent did: traces, token counts, latencies, evaluations. Governance decides what it may do next, in the request path, with a binding answer. One is a record you can question, the other is an action that did or did not happen.</p>"),
 ("Do I need both, or will tracing be enough?",
  "<p>Tracing alone leaves every insight arriving after the action and often after the invoice. Governance alone leaves you safe and opaque: you know an action was refused and cannot say what made the agent try. Most teams already have the first half, and the shortest path to the second is a gateway in shadow mode.</p>"),
 ("How do the two connect technically?",
  "<p>On one run identifier. If the trace, the spend line, the policy verdict and the outcome tag all carry the same id, a refusal links to the exact chain of calls that led to it. If they do not, you own two dashboards and an argument.</p>"),
 ("Does adding governance mean replacing our tracing stack?",
  "<p>No. The governance planes here export over OTLP into whatever backend you already run, and the gateway writes its own traces, so governance data lands in your observability stack rather than competing with it. What does not belong in a dashboard is the enforcement decision itself.</p>"),
 ("How can I tell whether a tool actually enforces anything?",
  "<p>Four questions. Does it act in the path or after it? Is the answer binding, or can the agent proceed past a warning? What happens when it is unreachable, and is that choice documented? Can somebody who does not trust you verify its record?</p>"),
]),

"agent-tooling-compared.html": ("common questions", "What people ask when they have already bought one", [
 ("Do we have to drop our tracing to use this?",
  "<p>No, and we would advise against it. Tracing answers a question this stack does not: why the model wanted to do the thing. Keep it, put the gateway in front of the model calls in shadow mode for a week, then turn on caps where the outliers are.</p>"),
 ("Our observability tool already tracks cost. Is that not the same?",
  "<p>Cost tracking and a cost control are different products. One tells you a run spent the money. The other answers 402 and the run does not spend it. One arrives with the invoice, the other instead of it.</p>"),
 ("Why describe products by shape instead of naming them?",
  "<p>Because a named comparison is wrong the week after a vendor ships a feature, and a reader who already runs one of these can map the shape to their tool in a second. The shapes are also more useful: they say what a category of tool can and cannot do architecturally, which is the part that does not change with a release note.</p>"),
 ("Could one of them add enforcement later?",
  "<p>They could, and the sensible assumption is that somebody will. It is a different architecture though: standing in the path means owning an availability decision, fail-open or fail-closed, on every call. That is a heavier commitment than receiving a copy of a trace, and it is why the categories have stayed separate so far.</p>"),
 ]),

"mcp-security.html": ("common questions", "What people ask about MCP", [
 ("What are the main security risks of the Model Context Protocol?",
  "<p>Two structural ones and the rest follow. A tool definition is a description the model reads as instructions, so it is content, not just a signature. And clients re-fetch definitions on connect, so the tool you approved is not necessarily the tool in use later. From those come poisoned descriptions, rug pulls, unsanctioned servers, credentials passing through the model, and drift nobody tracks.</p>"),
 ("What is an MCP rug pull, and how do I catch one?",
  "<p>A tool whose description or schema changes after you approved it, with no deployment on your side and no trace in your repository. Catch it the way you catch a changed dependency: pin a fingerprint of every approved tool and fail the build when the fingerprint moves. It ships as a CI action for that reason.</p>"),
 ("How do I find MCP servers nobody registered?",
  "<p>From the agent side, not the server side. Compare what your agents actually reach against the list of sanctioned servers and flag the difference; then join agents to servers on the tools they share, so an agent whose declared tools come from an unsanctioned server is a query rather than an incident.</p>"),
 ("Should an MCP server use stdio or HTTP?",
  "<p>Prefer stdio where the integration is genuinely local: no listener, no port, no network trust boundary to get wrong. Plenty of servers are remote by habit rather than need. Where a network server is required, treat it as any other internal service: authentication, network placement, and a name in the inventory.</p>"),
 ("How do I keep API keys out of the model when a tool needs one?",
  "<p>Do not hand the value to the agent. The agent holds a named handle, and the real credential is injected at the last hop, so it never enters the prompt, the trace or the model's memory. That also makes revocation meaningful, because the value lives in exactly one place.</p>"),
]),

"agent-identity.html": ("common questions", "What people ask about agent identity", [
 ("How should an AI agent authenticate to the tools it calls?",
  "<p>With an identity, not a shared secret. The agent needs a stable name, a recorded owner, and evidence binding that name to the workload: an OIDC token, a SPIFFE SVID, an mTLS certificate or an enclave key. A key in an environment variable proves only that the caller knows the key, which is the one thing an incident review never needs to establish.</p>"),
 ("What is agent attestation, and do we need it on day one?",
  "<p>Attestation is the evidence that a name belongs to the workload using it. You do not need it everywhere on day one, and most organisations honestly start with none nearly everywhere. What matters is that the absence is recorded rather than implied, so privileged agents with nothing behind their name show up as a list instead of a feeling.</p>"),
 ("Why keep a delegation chain instead of just an owner field?",
  "<p>Because an agent's real reach is the union of everything along the chain it acts through, not the grants attached to its own name. A one-hop field cannot show that an agent with modest permissions arrives at admin two hops away. Keep the chain ordered root first, acyclic and capped, and keep it separate from the static parent that provisioned the agent.</p>"),
 ("Should every agent action require human approval?",
  "<p>No, and demanding it is how a control gets clicked through within a week. Reserve per-action confirmation for the destructive and expensive few: a kill, a budget change, an approval grant, issuing or revoking access. Bind the signature to that exact command and its arguments so approving one action never quietly approves the next.</p>"),
 ("How do we keep API keys out of the model's context?",
  "<p>Hand the agent a handle rather than a value, and attach the real credential at the last hop before the call leaves. Anything in the context window is quotable, loggable and memorable, so a token given to the model is a token in the trace and in whatever it repeats next. Brokering also gives revocation exactly one place to act.</p>"),
]),
}


def block(kicker, heading, items):
    out = [MARK_OPEN,
           '<section class="sec" id="faq" style="padding-top:14px">',
           '  <div class="wrap">',
           '    <div class="sec-head rv">',
           f'      <div class="kicker">{kicker}</div>',
           f'      <h2>{heading}</h2>',
           '    </div>',
           '    <div class="faq rv">']
    for q, a in items:
        out.append("      <details>")
        out.append(f"        <summary>{q}</summary>")
        out.append(f'        <div class="a">{a}</div>')
        out.append("      </details>")
    out += ["    </div>", "  </div>", "</section>", MARK_CLOSE]
    return "\n".join(out)


def main():
    n = 0
    for path, (kicker, heading, items) in FAQ.items():
        p = ROOT / path
        h = p.read_text(encoding="utf-8")
        new = block(kicker, heading, items)
        if MARK_OPEN in h:
            h2 = re.sub(re.escape(MARK_OPEN) + r".*?" + re.escape(MARK_CLOSE), lambda _: new, h, flags=re.S)
        else:
            h2 = h.replace("<footer", new + "\n\n<footer", 1)
        if h2 != h:
            p.write_text(h2, encoding="utf-8")
            n += 1
        print(f"{path:28} {len(items)} questions {'written' if h2 != h else 'unchanged'}")
    print(f"\n{n} file(s) updated")


if __name__ == "__main__":
    main()

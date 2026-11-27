<!-- https://it-rat.com/changes-2026-11.html -->

# What changed in the stack, 16 October to 27 November 2026

> Keys held in custody, an agent's own credential at every door, a person for every ungranted tool call: what changed from 16 October to 27 November 2026.

What changed in the services in the six weeks after [the October page](https://it-rat.com/changes-2026-10.html), why each change matters, and what it improves for the people who run AI agents and answer for them. It is grouped by the problem each change solves, not by repository, because most problems were solved by several services moving together. **The period ends with the whole stack deployed again on AWS, on 27 November.**

- [At a glance](https://it-rat.com/changes-2026-11.html#at-a-glance)

- [Releases, day by day](https://it-rat.com/changes-2026-11.html#releases)

- [1. Keys in custody, the record witnessed](https://it-rat.com/changes-2026-11.html#custody)

- [2. An agent's own credential at every door](https://it-rat.com/changes-2026-11.html#credentials)

- [3. A tool call nothing grants waits for a person](https://it-rat.com/changes-2026-11.html#holds)

- [4. The MCP broker judges every call](https://it-rat.com/changes-2026-11.html#broker)

- [5. Quality becomes a signal the policy reads](https://it-rat.com/changes-2026-11.html#quality)

- [6. Running it: the bus, signed installs, drills](https://it-rat.com/changes-2026-11.html#operations)

- [27 November: the stack on AWS again](https://it-rat.com/changes-2026-11.html#aws)

- [A few terms](https://it-rat.com/changes-2026-11.html#terms)

## Six weeks, in five numbers.

*159*

release tags

*19*

repositories that released

*58*

launcher releases, 32 for a cluster and 26 for one machine

first releases: Keyryx, Verdryx and the Genaryx console

*28*

security tests passed on AWS on 27 November, none failed

Across 19 repositories we cut 159 release tags between 16 October and 27 November. TokenFuse moved from v1.14.0 to v1.27.1, Wardryx from v1.5.0 to v2.8.0 and Vouchryx from v0.2.0 to v0.9.0. Keyryx and Verdryx shipped their first releases, the console became a release of its own, and the two launchers released 58 times between them to carry those versions to real machines.

**How these were counted.** A release counts when GitHub published it between 16 October and 27 November. Ranges run from the latest release before 16 October to the latest on 27 November. Counts were read from each repository's releases on 27 November.

### The six themes

Each theme opens with the problem in plain words, then lists what changed, then says why it matters for someone who runs agents and answers for what they do. A short line at the end names the releases.

- [Keys in custody, the record witnessed.](https://it-rat.com/changes-2026-11.html#custody) The signing keys left the services that use them, and a witness outside the writers keeps its own signed log of the record.

- [An agent's own credential at every door.](https://it-rat.com/changes-2026-11.html#credentials) Both launchers require an agent's own short-lived token by default, bound to a key the agent holds, and a proof is good for one decision.

- [A tool call nothing grants waits for a person.](https://it-rat.com/changes-2026-11.html#holds) The person sees the call's arguments, sealed, can make the answer stand, and every hold ends on the record.

- [The MCP broker judges every call.](https://it-rat.com/changes-2026-11.html#broker) Batches, redirects and an unreachable gateway no longer lead around the broker's checks.

- [Quality becomes a signal the policy reads.](https://it-rat.com/changes-2026-11.html#quality) A quality failure is a finding with an owner, and an agent with a spent error budget waits for a person.

- [Running it: the bus, signed installs, drills.](https://it-rat.com/changes-2026-11.html#operations) Each plane owns its stream, only a signed release installs, and drills cover a provider that is up but failing.

## Releases, day by day.

Most services released in three bursts: from 18 to 20 October, when key custody, agent tokens and the new defaults landed together; from 4 to 15 November, when holds, the argument preview and the bus ownership work landed; and from 24 to 26 November, when key rotation moved to custody's admin socket and the console became its own release. The launchers, [stack-single](https://github.com/TAIPANBOX/stack-single) for one machine and [stack-k8s](https://github.com/TAIPANBOX/stack-k8s) for a cluster, release whenever a service they carry moves, which is why they lead the count.

## Keys in custody, the record witnessed.

A record proves what happened only if two things hold: the key that signed it was not lying around beside the code that used it, and somebody other than the writers saw the record when it was written. Until this period the services that sign, approvals, record seals and delegation tokens, each held their own keys, and nothing outside them watched the record. [Keyryx](https://it-rat.com/services/keyryx.html), first released on 18 October, answers both.

### What changed

- **Custody holds the keys and signs on request.** Wardryx's approval tokens are signed through Keyryx and verified from a cached key set. Trailryx's seals are signed through it, queued while it is down, and each signature is checked against Keyryx's pinned key before the seal is kept.

- **High-rate signers get short-lived keys it certifies.** Vouchryx signs tokens with a working key Keyryx certifies, renewed at half its life, and refuses to issue without one. A producer on the event bus can sign checkpoints of its stream with a key of its own, certified the same way.

- **A witness outside the writers.** The witness reads the record and never writes to it, checks that every byte it saw before is still there, and signs what it saw into its own append-only log, with ECDSA P-384 and ML-DSA-65 side by side. Its findings reach the notifier and the console.

- **On by default.** Every cluster launcher installs custody and the witness from 20 October, and a single box signs and witnesses its record from 5 November, including a box with 1,024 records of history written before signing existed.

- **Rotation without an outage, and only by an operator.** Key sets are published with an overlap, so a rotation never breaks a verifier. At the bound on live keys, a new key retires its owner's oldest one instead of being refused. From 25 November rotating or revoking a key is a command on custody's admin socket only, and every change is announced on the bus, where the notifier reads it.

### Why it matters

An auditor asks two questions of a record: who could have signed this, and could anyone have changed it afterwards. With the keys in custody the first has one answer, and every rotation and revocation is itself on the record. The witness answers the second from outside the services that write, and because its log carries a post-quantum signature beside the classical one, what it signs now still verifies after classical signatures are retired.

**For the record:** Keyryx v0.1.0 (18 October) to v0.2.0 (25 November); Wardryx v2.2.0; Trailryx v1.3.0 and v1.5.0; Vouchryx v0.5.0 and v0.6.0; agent-stack-go v2.0.0; stack-k8s v1.6.0 and v1.7.0; stack-single v1.6.0.

## An agent's own credential at every door.

A static client key says which key made a call, not which agent made it, and it works for anyone who copies it. An incident needs a different answer: which agent, acting for whom, and could the credential have been replayed. In this period the agent's own token became the default at both doors that take agent calls, the gateway and the MCP broker.

### What changed

- **Required by default.** From 19 October both launchers require an agent's own short-lived token at the gateway and the MCP broker. A static client key is admitted only when its id is on a named list, and Vouchryx, which issues the tokens, starts on every install and runs without an identity provider.

- **Bound to a key, good once.** Vouchryx issues per-agent credentials bound to a key the agent holds (client credentials with DPoP), workload tokens and a standing ban. Wardryx checks the token and its proof itself; a proof is good for one decision, and with a database the record of spent proofs is shared by every instance and survives a restart. Bearer keys are compared in constant time and stored by their SHA-256 digest.

- **Unconfigured means enforcing.** An unconfigured gateway and MCP broker enforce what they advertise instead of starting in observation, and a gateway that listens beyond loopback with nothing authenticating its callers refuses to start.

- **The person behind the agent.** A call made on behalf of a person carries that person's delegation beside the agent's own token, and the policy plane receives the person's chain as proven. An approval names the person who gave it, through a statement the console signs.

- **Keys that move without a restart.** Vouchryx reads its issuers' key set files again every 30 seconds, so a provider that rotates its signing key is trusted again without a restart. A revoke key can be scoped to the rights and the parties its holder needs, and an actor credential with no key is refused on a first hop.

- **Only verified images and hosts.** The default cluster install admits only verified images into the stack's namespace, and the cloud launchers check each node's SSH host key before they connect.

### Why it matters

With a token bound to a key the agent holds, a copied token is useless without that key, a replayed proof is refused, and every refusal is filed under the agent and the person behind it. The defaults matter as much as the feature: a control that has to be switched on is off on most machines, so this one now has to be switched off, by name.

**For the record:** Vouchryx v0.4.0 to v0.9.0; Wardryx v2.3.0, v2.4.0 and v2.5.0; TokenFuse v1.16.0, v1.19.0 and v1.25.0; stack-k8s v1.3.0, v1.4.0 and v1.5.0; stack-single v1.3.0.

## A tool call nothing grants waits for a person.

A tool call is where an agent acts on the world: it sends the mail, moves the file, calls the API. Before this period a tool call that no rule mentioned went through, and the person deciding a held call could not see its arguments. A queue of holds also had no end, so a hold nobody answered waited forever.

### What changed

- **Held by default.** From 7 November a tool call nothing grants waits for a person on every new install, with nothing to turn on. Model calls pass as before, and only an explicit grant lifts the hold. A box that already runs agents is told what the hold would stop before anything on it changes.

- **The person sees the arguments.** Wardryx builds a preview from the bytes the approval is bound to, hides secrets and personal data by fixed rules, and seals it so that only the console can read it. A person may deny a sealed hold without opening it. Both launchers turn the preview on from 13 November.

- **An answer can stand.** The console's approvals inbox offers "Always allow" beside Grant and Deny, and writes the same grant the installer's own command writes, so the same question does not come back.

- **Every hold ends.** A hold nobody decides is closed as expired once it has waited `WARDRYX_HOLD_TTL`, 24 hours by default, and the held agent may withdraw its own. The console shows them as "Expired, nobody decided in time" and "Withdrawn by the agent", in a neutral colour, and Trailryx writes a closing record for both.

- **The agent is told why.** A held MCP tool call says why it was held, and the broker's list of tools leaves out the ones the policy refuses the calling agent outright, so an agent is not shown tools it may never use.

### Why it matters

Human approval works only when the person can decide well and the queue cannot rot. Seeing the arguments turns a rubber stamp into a decision; a standing grant stops approval fatigue from training people to click yes; a lifetime means a forgotten hold closes as a timeout on the record instead of waiting forever. The [console](https://it-rat.com/genaryx.html) and the record show the same outcome, so an auditor reads what the approver saw.

**For the record:** Wardryx v2.6.0, v2.7.0 and v2.8.0; Trailryx v1.6.0; TokenFuse v1.23.0 and v1.24.0; stack-k8s v1.8.7 to v1.16.0; stack-single v1.7.0 to v1.12.0; Mockryx v0.5.0 for the hold drill.

## The MCP broker judges every call.

The broker stands between agents and every tool server, so a request that slips past its checks is a call nobody judged. Most fixes in this theme close a way around the judgement rather than add a new one, which is the kind of defect worth finding before anyone else does.

### What changed

- **A batch no longer walks around the checks.** The broker read `method` from one JSON-RPC object, and a batch is an array, so it skipped the policy decision, the identity requirement, the argument scan and the record. A message that is not one object is now refused before an upstream is resolved or a secret read. The refusal was re-run on a live box on 28 October.

- **Fails closed.** When the gateway cannot judge a tool call, the broker refuses it instead of letting it through unjudged, and it follows no redirect.

- **Taint from what happened.** The agent firewall takes a run's taint label from the act an enforcement point saw, not from the tool name the agent reported. The injection detector sees Unicode tag characters and bidirectional isolates, and every refusal text is cleaned before a model reads it.

- **Every door judges the arguments.** Each door judges a tool call's own arguments, and the judge of streamed calls is hardened.

- **Limits per key, credentials per upstream.** A client key can carry its own rate and concurrency limits, and each MCP upstream can have a credential of its own.

- **A web read under the run that asked for it.** A fetch through the broker carries the run that asked for it, so Scopyx, the egress gate, labels the read with the run that made it.

### Why it matters

A policy is only as strong as the request shape it forgot. An agent that has read untrusted text can be talked into anything a tool allows, so the broker has to see every call in every shape, judge it on what the agent actually did, and refuse when it cannot judge. After these changes, a call the broker cannot judge is refused.

**For the record:** TokenFuse v1.20.1 to v1.27.0; Scopyx v1.2.0 and v1.3.0; stack-single v1.8.0.

## Quality becomes a signal the policy reads.

Spend and safety are judged per call; quality is judged per outcome, and until this period it lived in reports. A failing agent showed up as a line somebody might read, while the agent went on acting. [Verdryx](https://it-rat.com/services/verdryx.html) shipped its first release on 19 October and turned that line into a signal.

### What changed

- **A quality plane with six graders.** Verdryx grades an agent's outputs against an eval set (exact, regex, outcome tag, a model as judge, a tool-call trace, and a typed verdict from Typryx), flags drift against a stored baseline, turns the gateway's traces into cost per outcome, and computes error budgets over the same traces. It measures and does not enforce.

- **A failure becomes a finding.** A quality failure is a record an operator comes back to, a fix is registered against it and judged by the runs that follow, and a person's grade outranks a model's score. The model judge stops guessing a score from a reply that carries none.

- **A spent budget holds the agent.** When Verdryx's error budget signal stands for an agent, Wardryx puts that agent's tool calls to a person, and a caller cannot remove the signal. Both launchers run the measurement and carry the rule by default from 7 November, and on that day an agent with a spent budget was held on a live box.

- **Memory that keeps the person's word.** In Engram a fact that traces to the person's own words is no longer displaced by anything a model writes, and a fact can be refuted without being erased.

- **An inventory that names disagreements.** Idryx's AI inventory says, for each agent or service, what was declared, what was seen and what the code can reach, and names every disagreement between them.

### Why it matters

An agent that keeps answering wrong costs more than its tokens. Before, the cost showed up later in a review; now a falling quality score has an owner and a fix it is judged against, and when the budget is spent the agent stops acting alone until a person looks. The same measurement feeds the FinOps view, because cost per resolved case needs to know which cases were resolved.

**For the record:** Verdryx v0.1.0 (19 October) to v0.4.0; Wardryx v2.5.0; Engram v3.1.0; Idryx v1.4.0; Typryx v0.6.0, whose backend reaches the current OpenAI models; stack-k8s v1.8.5; stack-single v1.6.3.

## Running it: the bus, signed installs, drills.

Every plane writes to one event bus, every launcher installs from the internet, and every alert reaches a person by mail. Each of those is a place where one compromised or misbehaving part could speak for another, or where a person stops reading because there is too much to read.

### What changed

- **Each plane owns its stream.** On a cluster every plane that writes the bus runs under a uid and a group of its own, and only the bus owner can create, rename or remove a name in the bus directory, so no plane can forge or replace another's stream. Stream files are readable by their owner's group and nobody else, and Wardryx writes only the event types the registry lists for it.

- **Only a signed release installs.** A piped install runs only a release whose signature verified. On one machine the installer compares what Docker runs with the pins, keeps a journal with a rollback index, and refuses a tree older than that index.

- **Drills for a provider that is up but failing.** Mockryx adds drills for a provider that answers errors, rate-limits or times out, beside the outage drill, and one for the tool hold. A drill beside the notifier proves the whole reaction chain to the operator's mail.

- **Fewer, safer mails.** Heraldyx sends mail only over an encrypted connection, a storm of failures from one dependency is one mail, and the gateway folds a provider that keeps failing into one incident.

- **Patched within days.** Every Go service was rebuilt on Go 1.27.3 and then on Go 1.27.4 for the two Go advisories of the period, and the services that read the whole bus get 1 GiB of memory.

- **The console is its own release.** Genaryx published its own signed image on 25 November, for amd64 and arm64, and both launchers run it. The FinOps console reads the gateway's spend on a cluster and on one machine.

### Why it matters

The controls above are only as good as the ground they stand on. A bus where one plane can rewrite another's stream makes the record a matter of trust; an install that runs whatever arrives makes every control optional; a notifier that sends forty mails for one outage teaches people to ignore it. These changes keep the ground under the controls as strict as the controls themselves.

**For the record:** stack-k8s v1.10.0, v1.17.0 and v1.19.0; stack-single v1.7.0, v1.13.0 and v1.15.0; Mockryx v0.4.0 and v0.5.0; Heraldyx v0.8.0 to v0.10.0; agent-passport v1.1.0; Genaryx v0.1.0.

## 27 November: the stack on AWS again.

On the last day of the period the current releases were deployed from their tags on fresh machines in AWS eu-central-1: stack-k8s v1.19.0 on five c7i.2xlarge nodes running self-managed k3s, and stack-single v1.15.0 on one m7i.xlarge beside it. Images were pulled by digest, nothing was built, and everything was torn down afterwards.

*16:30*

minutes from zero to every plane answering on five nodes

*28*

security tests passed, none failed

*21*

checks passed with the stack frozen, none failed

*5:12*

minutes to install stack-single, signature check included

*62*

checks ok in stack-single's own status

- **The cluster.** The deploy took 16 min 30 s. The security tests passed 28 with none failed, and the frozen-stack checks passed 21 with none failed. The cluster's own verify run passed 20 checks and failed one: the bus owner could not reach the root of the shared Longhorn volume and got a remote I/O error. The console answered HTTP 200 through a load balancer.

- **The single box.** stack-single v1.15.0 checked its release signature against the release workflow's identity, installed in 5 min 12 s, and its own status reported 62 checks ok and none failed, with 18 containers up.

- **The newer image.** On the current Ubuntu 26.04.1 image, with kernel 7.0, the same deploy stopped: AppArmor denied signals between containers and the policy store never left recovery. The installers learned the two kernel 7.0 host settings the same morning, and on that image the stack then ran with the bus owner working, the security tests at 28 passed and none failed, and verify at 21 passed and none failed. The fix was merged to main straight after.

- **Teardown.** 21 resources destroyed, and the region was empty by direct query.

The full logs, with public addresses and the account masked, are in [the stack-k8s evidence folder](https://github.com/TAIPANBOX/stack-k8s/tree/main/cloud/aws/evidence). [What is proven and how it was measured](https://it-rat.com/what-is-proven.html) keeps the earlier runs beside this one.

## A few terms.

**Key custody**
A service that holds signing keys and signs on request, so the keys never sit beside the code that uses them.

**Witness**
A process outside the writers that reads the record, checks nothing it saw has changed, and signs what it saw into a log of its own.

**DPoP**
Demonstrating proof of possession: a token bound to a key its holder keeps, presented with a fresh proof signed by that key.

**Hold**
A call the policy neither allows nor refuses, kept waiting until a person decides, it expires, or its agent withdraws it.

**Error budget**
How many failed outcomes an agent may have in a window before its objective is missed.

[What changed from 1 to 15 October](https://it-rat.com/changes-2026-10.html) comes before this page. [Security by design](https://it-rat.com/security-by-design.html) explains the decisions behind custody, holds and fail-closed defaults, [the glossary](https://it-rat.com/glossary.html) has the rest of the vocabulary, and [the guides index](https://it-rat.com/guides.html) has every guide.

<!-- https://it-rat.com/glossary.html -->

# Glossary of agent-governance terms

> Plain definitions for this field: agent passport, attestation, delegation chain, blast radius, per-run budget, rug pull, CBOM, FOCUS, drift.

Terms that come up when a team starts governing agents, defined plainly and in the sense this field actually uses them. Where a term is contested or means different things to different vendors, the definition says so.

## Identity

**Agent passport**
A small document describing one agent: its identifier, the human or team that owns it, the runtime it runs on, and how its name is attested. It is metadata, not a credential: holding a passport authorises nothing, and that is deliberate. See [agent identity](https://it-rat.com/agent-identity.html).

**agent:// URI**
The identifier form used for agents in this stack: a trust domain and a path, capped at 255 bytes, aligned with SPIFFE naming without requiring SPIFFE. The point of a fixed shape is that a spend record, a policy verdict and an audit entry can be joined on the same string.

**Attestation**
The evidence binding a name to the workload using it: an OIDC token, a SPIFFE SVID, an mTLS certificate, an enclave key, or explicitly nothing. Recording `none` honestly is more useful than leaving the field blank, because it turns posture into a list you can work through.

**Delegation chain on_behalf_of**
The ordered record of who an agent is acting for on this request: agent, then whatever spawned it, up to the human at the root. Kept acyclic and capped in length. Distinct from the static parent that provisioned the agent, which is an org chart rather than authority.

**Proof of possession DPoP, cnf.jkt**
Evidence that the caller holds the key a token was issued to, rather than merely holding the token. The token carries a thumbprint of the caller's public key, and every request carries a fresh signature from that key, so a token lifted from a log buys nothing. This is the half a delegation chain deliberately does not cover, and it is what [Vouchryx](https://it-rat.com/services/vouchryx.html) adds.

**Delegation revocation**
Ending an agent's right to act for somebody, at every enforcement point that polls the revocation list, within one poll interval, without waiting for a token to expire. Distinct from a kill switch, which ends spend: the money case is a runaway, the authority case is a delegation that should never have been made or should stop now. Both are one operation and both have to be attributable, so an actor and a reason are required.

**Found, not saved**
A FinOps distinction that decides whether anybody believes the rest of your numbers. A finding puts money on the table; nothing is saved until a person acts on it and the invoice changes. A console that reports found money as saved is disbelieved the first time finance checks it, and after that every other figure it prints is suspect too. See [CostCrew](https://it-rat.com/services/costcrew.html).

**Non-human identity NHI**
Any identity that is not a person: a service account, an access key, a workload, an agent. The category matters because most organisations count their humans carefully and their non-humans not at all, and the second group is usually larger.

**Blast radius**
Everything an identity can reach transitively, computed as the union of the permissions along its delegation chain rather than the grants attached to its own name. This is what makes a modest-looking agent turn out to be two hops from admin.

**Excessive agency**
An agent that arrives at admin-equivalent power through its delegation chain rather than through its own permissions. Catalogued as LLM06 in the OWASP list for large language model applications.

## Money

**Run**
One unit of agent work: a task, with a budget, an identity and a trace. The useful unit for governance, because a key cannot tell one agent's honest afternoon from the same key looping on itself, and a model total cannot be charged back to anyone.

**Per-run budget**
A spending cap attached to a run and checked against every ancestor it belongs to: agent, team, company. All-or-nothing, so a run cannot fit under its own cap while breaking its team's.

**Reserve then settle**
Pricing a call before it happens, taking the reserve against the budget, and reconciling the real cost afterwards. It is what allows a call to be refused before the provider sees it, rather than discovered after the invoice.

**Breaker HTTP 402**
The control that refuses a call once its budget is crossed, answering with a status the calling framework already understands. Sometimes described as a kill switch, though the breaker refuses one call rather than stopping a fleet.

**Semantic cache**
Serving a repeated question from a previous answer instead of paying for it again. A cost lever that refuses no work, which makes it the easiest saving to defend and the first one worth reporting separately.

**Model router**
Sending routine calls to a cheaper model while hard ones stay on the frontier model. Like the cache, it should report its savings on its own line: a combined percentage cannot be audited.

**FOCUS**
The FinOps Foundation's open specification for cost and usage data. Exporting agent spend in it means the numbers land in the same pipelines and dashboards as the rest of the cloud bill instead of in a bespoke report.

**Cost per resolved case**
The money spent to actually finish one piece of work, including the intermediate calls nobody tagged and the calls a breaker refused. The unit economic that changes decisions, where a monthly total does not.

## Control

**Runtime governance**
Controls that decide what an agent may do while it is running, with a binding answer, as opposed to reports describing what it did. See [the governance guide](https://it-rat.com/ai-agent-governance.html) and [the comparison with observability](https://it-rat.com/ai-observability-vs-governance.html).

**Shadow mode**
Running a control in the path with its answer recorded and never binding, so you can see what would have been blocked before anything is. The standard way to introduce enforcement without making its first day also its first outage.

**Fail-open and fail-closed**
What the enforcement point does when the decision point is unreachable. Fail-open treats it as allow: availability wins, and an outage silently disables policy. Fail-closed treats it as deny: policy wins, and an outage blocks governed work. Both are defensible; not deciding is not.

**Hold human in the loop**
A third answer beside allow and deny: the action waits for a person. The workable shape is stateless, so no connection is parked while somebody sleeps, and the eventual grant is proven by a signed token rather than by anyone remembering the request.

**Approval token**
A short-lived signed claim that a specific agent, run and set of tools was approved. Bound to those exact parameters so that approving one action never quietly approves the next, and verified before anything in it is trusted.

**Taint tracking**
Marking data that came from outside the trust boundary and refusing the actions it reaches. The practical answer to instructions arriving inside a web page, a ticket or a tool description, since the model cannot be relied on to ignore them.

**Break-glass**
A deliberately awkward path for an emergency action, recorded as such: a hardware-backed confirmation, a typed reason, and a journal entry naming who did it. Awkward on purpose, because the alternative is an emergency path that becomes the normal one.

## Tools, evidence and crypto

**MCP Model Context Protocol**
A protocol for exposing tools and resources to a model. It made capability something you connect to rather than something you write, which is useful, and moved tool definitions into content the model reads. See [MCP security](https://it-rat.com/mcp-security.html).

**Rug pull**
A tool whose description or schema changes after you approved it. Because clients re-fetch definitions on connect, the change needs no deployment on your side and leaves no trace in your repository. Caught by pinning a fingerprint of what was approved.

**Shadow MCP server**
An MCP server agents are using that no inventory lists. Detected from the agent side rather than the server side, because a registry can only list what somebody already knew about.

**Agent-BOM**
A bill of materials for agents, in CycloneDX: what exists, who owns each one, what runtime it runs on, what attests it. The same idea as an SBOM, applied to the actors rather than the libraries.

**CBOM**
A cryptographic bill of materials: every key, certificate and algorithm actually in use, with its risk class. The inventory a post-quantum migration cannot start without.

**Post-quantum cryptography PQC**
The standardised replacements for algorithms a sufficiently capable quantum computer would break, published by NIST in 2024: ML-KEM, ML-DSA and SLH-DSA. Relevant now because data captured today can be decrypted later, and because migration timelines have dates on them.

**Hash-chained journal**
An append-only record in which each entry carries the hash of the entry before it, over a canonical serialisation. Tampering does not hide; it breaks the chain at the point it happened, and a third party can check that without trusting the author.

**Provenance why()**
The trail from a belief back to the observations it came from: which episodes produced a fact, which run extracted it, at what confidence. What separates a memory you can audit from a store of similar-looking text.

**Bitemporal**
Keeping two independent timelines on a fact: when it was true in reality, and when the system learned it. With both, you can ask what an agent believed in March and get March's answer rather than today's.

**Quality drift**
A gradual fall in output quality that a flat threshold misses. Detected properly with a two-sample significance test beside the threshold, because the regression that matters is usually small, consistent and inside the noise band somebody tuned last quarter.

## Each of these has a guide behind it.

The [twelve guides](https://it-rat.com/guides.html) cover governance, cost, security, MCP, identity and the line between observability and control, and the [stack](https://it-rat.com/index.html#stack) is the open implementation of everything named here.

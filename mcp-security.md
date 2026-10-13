<!-- https://it-rat.com/mcp-security.html -->

# MCP security

> What changes when tools arrive over the Model Context Protocol: descriptions the model reads, servers nobody sanctioned, tools that change later.

The Model Context Protocol did for agent tooling what package managers did for libraries: it made capability something you connect to rather than something you write. That is genuinely good, and it moves two things that used to be stable. A tool is now a **description the model reads as instructions**, and it comes from a server that can change that description after you approved it. Everything below follows from those two sentences.

## Three shifts, each with an old parallel.

### The tool definition became content

A function you shipped had a signature the compiler checked. A tool over MCP has a name, a schema and a natural-language description, and that description goes into the model's context as text it will follow. The nearest old parallel is a config file that the interpreter also executes: everything that made those a bad idea applies here.

### The supply chain moved to connect time

Clients discover tools when they connect, which means the definition you reviewed on Monday is not necessarily the definition in use on Friday. The parallel is a dependency without a lockfile: the name resolves, the content is whatever the other side is serving today. This is the gap a rug pull walks through.

### Access spread faster than inventory

Adding a server is a config line, so people add them the afternoon they need one. Within a quarter the honest answer to "which agents can call which tools" is that nobody has it written down. The parallel is shadow IT, and it resolves the same way: not with a stricter process, but with detection.

## Six ways an MCP setup goes wrong.

Defensive throughout: what to detect and refuse on your own estate, with the control that answers each.

*poisoned description*

### The tool tells the model what to do

A description carrying instructions, or hidden characters the reviewer never saw, reaches the model as part of its context. Nobody attacked your agent; they published a tool and waited.

**Answer:** scan descriptions for injection phrasing and hidden characters before a tool is approved, not after it misbehaves. [TokenFuse →](https://it-rat.com/services/tokenfuse.html)

*rug pull*

### Approved once, changed later

The tool you audited is not the tool being served next week. Because clients re-fetch on connect, the change needs no deployment on your side and leaves no trace in your repository.

**Answer:** pin a fingerprint of every approved tool's description and schema, so a change shows up as a rug pull. The TokenFuse mcp-scan action runs that scan in CI and fails the build at a chosen severity, high by default. [TokenFuse →](https://it-rat.com/services/tokenfuse.html)

*shadow server*

### In use, in nobody's registry

An MCP server your agents talk to that no inventory lists. It is the OWASP MCP Top 10 entry everybody nods at and few can currently detect, because detecting it needs the agent-side view, not the server-side one.

**Answer:** compare what agents actually reach against the sanctioned registry and flag the difference. [Idryx →](https://it-rat.com/services/idryx.html)

*shadow tool on a real agent*

### The join nobody computes

Worse than an unsanctioned server on its own: an agent whose declared tools are exposed by that server. That is the exact path a poisoned tool takes to reach a model with credentials.

**Answer:** hold agents and MCP servers in one graph and join them on the tools they share, so the path is a query rather than an incident. [Idryx →](https://it-rat.com/services/idryx.html)

*credentials in the call*

### The secret goes through the model

A tool needs a token, so the token is handed to the agent, which means it is in the prompt, the trace, the logs and whatever the model says next. Rotation does not fix a leak that is structural.

**Answer:** the agent holds a handle such as a named secret reference, and the real value is injected at the last hop, never entering the model's context. [TokenFuse →](https://it-rat.com/services/tokenfuse.html)

*drift*

### Config that moves under an agent

Not a dramatic swap, just a server whose exposed tooling or configuration keeps changing under an agent that keeps its access. Each change is small; the trend is the finding.

**Answer:** track the change itself as a signal, raising severity on repetition and on privileged identities. [Idryx →](https://it-rat.com/services/idryx.html)

## What a sane MCP setup looks like.

### Treat a tool definition like a dependency, because it is one

Review it before use, pin what you reviewed, and let CI tell you when the pinned thing changed. A rug pull should fail a pull request the way a changed lockfile hash does, rather than surfacing in an incident review six weeks later.

### Prefer the transport with the smaller surface

A server that speaks stdio to a local process has no listener, no port and no network trust boundary to get wrong. Not every integration can be local, but plenty of them are made remote by habit rather than need. Where a network server is genuinely required, it deserves the same scrutiny as any other internal service: authentication, network placement, and a name in the inventory.

### Keep secrets out of the model's context

Assume anything in the context window is quotable, loggable and memorable. The workable pattern is a broker: the agent sees a handle, the credential is attached at the last hop, and the model never holds a value it could repeat. This also makes revocation meaningful, because there is exactly one place the real value lives.

### Maintain a registry, then detect what is outside it

Write down which servers are sanctioned, and accept that the list will be wrong. The control that earns its keep is the comparison: what are agents actually reaching, and which of those does nobody own? A registry without detection is a document; detection without a registry is noise.

### Deny at the tool boundary, not in the system prompt

A description that tries to talk the model into something is only dangerous if the resulting call is permitted. Keep the deny list short, explicit and enforced per call at the policy point, and taint-track what came from outside so an instruction that arrived in a tool description cannot reach an action that matters. [Wardryx](https://it-rat.com/services/wardryx.html) is where that decision lives here.

### Rehearse the refusal

Every claim above is testable: fire a drill that presents the forbidden tool and assert the policy point denies it, against a real gateway with a fake provider behind it. A guardrail nobody exercises is a guardrail nobody has. [Mockryx](https://it-rat.com/services/mockryx.html) exists for that rehearsal.

Everything here inspects, detects and refuses on your own estate. Mockryx ships a drill that crafts a poisoned tool description as a test input, and it sends that only to the operator's own gateway. Nothing in this stack attacks an MCP server or probes anyone else's infrastructure, and the scanner is meant to be pointed at servers you are entitled to review. Naming an attack is how you say what to stop.

## Where this sits.

MCP is one surface of a wider job: [AI agent security](https://it-rat.com/ai-agent-security.html) covers the rest of the failure modes, [AI agent governance](https://it-rat.com/ai-agent-governance.html) the controls around them, and [the guides index](https://it-rat.com/guides.html) the whole set. The scanner, the credential broker and the detectors are Apache-2.0 and run on infrastructure you own.

- **Does it pin what you approved?** A fingerprint of the description and schema is what turns a silent change into a failed build.

- **Does it look from the agent side?** A registry lists what you know about. Only the agent-side view finds the server nobody registered.

- **Can it join agents to the tools they can call?** An unsanctioned server is a note. An unsanctioned server exposing a tool a live agent can call is an incident waiting.

- **Does the credential ever enter the model's context?** If the answer is yes, rotation is the only mitigation available, and it is not one.

- **Is the transport chosen or inherited?** Plenty of servers are remote by habit. Ask why this one is not local, and what protects it if it must be remote.

- **Does a change fail a build, or file a ticket?** A supply-chain signal that arrives as a notification is a signal that arrives after the deploy.

## What people ask about MCP

**Q: What are the main security risks of the Model Context Protocol?**
Two structural ones and the rest follow. A tool definition is a description the model reads as instructions, so it is content, not just a signature. And clients re-fetch definitions on connect, so the tool you approved is not necessarily the tool in use later. From those come poisoned descriptions, rug pulls, unsanctioned servers, credentials passing through the model, and drift nobody tracks.

**Q: What is an MCP rug pull, and how do I catch one?**
A tool whose description or schema changes after you approved it, with no deployment on your side and no trace in your repository. Catch it the way you catch a changed dependency: pin a fingerprint of every approved tool and fail the build when the fingerprint moves. The TokenFuse repository carries a CI action file (action.yml) for that reason.

**Q: How do I find MCP servers nobody registered?**
From the agent side, not the server side. Compare what your agents actually reach against the list of sanctioned servers and flag the difference; then join agents to servers on the tools they share, so an agent whose declared tools come from an unsanctioned server is a query rather than an incident.

**Q: Should an MCP server use stdio or HTTP?**
Prefer stdio where the integration is genuinely local: no listener, no port, no network trust boundary to get wrong. Plenty of servers are remote by habit rather than need. Where a network server is required, treat it as any other internal service: authentication, network placement, and a name in the inventory.

**Q: How do I keep API keys out of the model when a tool needs one?**
Do not hand the value to the agent. The agent holds a named handle, and the real credential is injected at the last hop, so it never enters the prompt, the trace or the model's memory. That also makes revocation meaningful, because the value lives in exactly one place.

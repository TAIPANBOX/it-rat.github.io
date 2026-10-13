<!-- https://it-rat.com/agent-identity.html -->

# Agent identity and authentication

> Static keys are not identity. What an AI agent needs to be nameable, attributable, attestable and revocable, and when to demand a signature.

Most agent fleets authenticate the way the first prototype did: an API key in an environment variable, shared by whatever runs in that container. It works, and it quietly removes the one thing every later control depends on. An agent acting under a shared key cannot be told apart from the next agent, cannot be revoked without breaking both, and cannot be investigated afterwards. Identity is not paperwork here; it is the join key everything else uses.

## A key is a secret. An identity is a claim someone can check.

A static key answers one question, badly: does the caller know the secret. It says nothing about who the caller is, on whose behalf they are acting, what runtime they are running in, or whether anybody still expects them to exist. Those are the questions an incident review asks, and none of them are answerable from a key.

An identity for a workload, agent or otherwise, has to be four things at once. **Nameable**, so logs and decisions can refer to the same subject. **Attributable**, so there is a human or a team who owns it. **Attestable**, so the name is bound to a workload by something stronger than a config file. **Revocable**, so removing it is an action rather than a migration.

The uncomfortable part is that most fleets today have the first two at best, and often not even those. That is not a moral failing; it is what happens when a prototype becomes production without anyone deciding it had. The useful move is to notice which of the four you actually have, per agent, before the next control is layered on top.

## Six questions an identity has to answer.

Each one is separately answerable, and each is separately missing in most fleets.

*naming*

### What is it called?

One identifier per agent, stable across restarts and deployments, short enough to sit in every event and every log line. If a spend record, a policy verdict and an audit entry cannot be joined on it, they are three stories about three different agents.

**In practice:** an `agent://` URI, aligned with SPIFFE naming without requiring SPIFFE, capped at 255 bytes so it fits everywhere. [The contract →](https://it-rat.com/services/platform.html)

*ownership*

### Whose is it?

A human or a team accountable for rotating it, answering for it and eventually deleting it. This is the auditor's first question and the one most inventories cannot answer, because the person who created the agent has since changed teams.

**In practice:** an owner field on the agent's own document, and a detector for the ones that have none. [Idryx →](https://it-rat.com/services/idryx.html)

*attestation*

### What binds the name to the workload?

Anyone can claim a name. Attestation is the evidence behind it: an OIDC token, a SPIFFE SVID, an mTLS certificate, an enclave key, or honestly nothing at all. The last option is legitimate and common; what matters is that it is recorded rather than assumed.

**In practice:** the method is a field with five values including `none`, and a privileged agent carrying `none` is a finding. [Idryx →](https://it-rat.com/services/idryx.html)

*delegation*

### Who is it acting for, right now?

An agent rarely acts for itself. It acts for a user, or for another agent that acts for a user. That chain is what makes an action attributable to a person, and it has to be ordered, acyclic and bounded, or it becomes a way to launder authority through three hops.

**In practice:** a chain ordered root first, capped in length, kept separate from the static parent that provisioned the agent. [Idryx →](https://it-rat.com/services/idryx.html) The chain is the record; proving the agent actually holds that delegation is a different mechanism. [Vouchryx →](https://it-rat.com/services/vouchryx.html)

*authorisation per action*

### Is this particular action allowed?

Identity says who is asking. It does not say yes. For the small set of actions that are expensive or hard to reverse, the useful pattern is a signature bound to that exact command and its arguments, not a session that authorised a class of things an hour ago.

**In practice:** a policy point that answers allow, deny or hold, and a human ceremony for the few. [Wardryx →](https://it-rat.com/services/wardryx.html)

*revocation*

### How does it stop existing?

An identity you cannot switch off is a credential with a personality. Revocation has to be a single action with a visible effect, and it has to cover the paths the identity opened: its tokens, its device access, and the delegation others hold to it.

**In practice:** revocation as a first-class operation, and an inventory that shows what each identity still reaches. [Idryx →](https://it-rat.com/services/idryx.html) One call ends a delegation at every enforcement point that polls the revocation list, within one poll interval, whatever the token says about its own expiry. [Vouchryx →](https://it-rat.com/services/vouchryx.html)

## What tends to work.

### Name every agent before you give it a tool

The order matters more than the format. A fleet that names agents after they are already calling production systems spends the next quarter reconciling logs. Any stable identifier will do; what breaks is having none, or having three that nobody joins.

### Record attestation honestly, including when it is nothing

The temptation is to leave the field blank and imply something stronger than the truth. A field with an explicit `none` is far more useful: it lets you sort the fleet by how well each name is actually bound, and it turns a vague worry into a list you can work through. Most organisations start with `none` nearly everywhere, and that is fine as a starting point and dangerous as a permanent state on privileged agents.

### Treat the delegation chain as data, not as narrative

"The agent is acting for the user" is a sentence. An ordered chain from the agent, through whatever spawned it, to the human at the root is a structure you can query, cap in length and check for cycles. It is also the only way to compute what an identity can really reach, because the answer is the union of everything along the chain rather than the grants on its own name.

### Keep the static parent apart from the dynamic chain

Which agent provisioned this one is an org chart. Who it is acting for on this request is authority. Collapsing them into one field feels tidy and produces an inventory that cannot answer either question later.

### Sign the few actions that deserve it, not everything

Per-action confirmation on every call trains people to click through it within a week, which is worse than not having it. Reserve it for the destructive and expensive: a kill, a budget change, an approval grant, issuing or revoking access. Bind the signature to that exact command and its arguments, record which credential was touched, and let the ordinary path stay ordinary.

### Never put the credential in the model's context

An agent that holds a token holds it in the prompt, the trace, the logs and whatever it repeats next. A handle the agent can pass around, with the real value attached at the last hop, keeps the secret out of the context window and gives revocation exactly one place to act on.

### Count the non-human identities you already have

A first inventory looks for three things: service accounts unused for months, agents with no owner, and one credential appearing from many places at once. None of that is exotic and all of it is cheap to fix; the reason it persists is that nobody was counting.

- **Can it name the actor?** If the finest grain it offers is an API key or a service, it cannot attribute an action to an agent, and neither will you.

- **Does it record how the name is bound?** A tool that cannot express "this name is attested by nothing" will quietly imply that it is.

- **Does it model delegation as a chain?** One-hop "acts on behalf of" is a field. A chain is what catches authority reached two hops away.

- **Is revocation one action with a visible effect?** Ask what happens to tokens already issued and to devices already enrolled.

- **Does it join on the same identifier as your money, policy and trace data?** If it invents its own, you are buying the correlation project as well.

## Where identity sits.

Identity is the join key the other guides assume: [AI agent governance](https://it-rat.com/ai-agent-governance.html) for the full set of runtime controls, [AI agent security](https://it-rat.com/ai-agent-security.html) for the failure modes an identity gap opens, and [MCP security](https://it-rat.com/mcp-security.html) for the tools an agent reaches once it has one. The whole set is in [the guides index](https://it-rat.com/guides.html).

## What people ask about agent identity

**Q: How should an AI agent authenticate to the tools it calls?**
With an identity, not a shared secret. The agent needs a stable name, a recorded owner, and evidence binding that name to the workload: an OIDC token, a SPIFFE SVID, an mTLS certificate or an enclave key. A key in an environment variable proves only that the caller knows the key, which is the one thing an incident review never needs to establish.

**Q: What is agent attestation, and do we need it on day one?**
Attestation is the evidence that a name belongs to the workload using it. You do not need it everywhere on day one, and most organisations honestly start with none nearly everywhere. What matters is that the absence is recorded rather than implied, so privileged agents with nothing behind their name show up as a list instead of a feeling.

**Q: Why keep a delegation chain instead of just an owner field?**
Because an agent's real reach is the union of everything along the chain it acts through, not the grants attached to its own name. A one-hop field cannot show that an agent with modest permissions arrives at admin two hops away. Keep the chain ordered root first, acyclic and capped, and keep it separate from the static parent that provisioned the agent.

**Q: Should every agent action require human approval?**
No, and demanding it is how a control gets clicked through within a week. Reserve per-action confirmation for the destructive and expensive few: a kill, a budget change, an approval grant, issuing or revoking access. Bind the signature to that exact command and its arguments so approving one action never quietly approves the next.

**Q: How do we keep API keys out of the model's context?**
Hand the agent a handle rather than a value, and attach the real credential at the last hop before the call leaves. Anything in the context window is quotable, loggable and memorable, so a token given to the model is a token in the trace and in whatever it repeats next. Brokering also gives revocation exactly one place to act.

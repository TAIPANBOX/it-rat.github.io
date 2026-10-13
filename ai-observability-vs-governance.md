<!-- https://it-rat.com/ai-observability-vs-governance.html -->

# AI observability vs governance

> The record explains what an agent did, the control decides what it may do next, and both meet on one run id. What each one answers and what it cannot.

Every agent run leaves two kinds of evidence. One explains what happened. The other decides what may happen next. The stack keeps them apart on purpose and joins them on one id, so you can see which problem each part leaves untouched.

## What each one is for, and what it cannot do.

*the record*

### A record you can question

Traces, spans, token counts, latencies, prompt and response capture, evaluation reports. It reconstructs what an agent did, in what order, with what inputs, and how much of the context window it burned doing it. When an agent behaves strangely, this is the part that tells you why.

**Strongest at:** debugging a bad answer, understanding a slow chain, finding the tool call that returned nonsense, showing a change in behaviour after a model upgrade.

**Cannot:** stop anything. Every entry is written after the action, and the spend it shows has already happened.

*the control*

### A decision that binds

Budgets, policy verdicts, identity, approval ceremonies, hard ceilings. It sits in the request path and answers before the call happens: allowed, refused, or held for a human. Its output is not a chart, it is an action that did or did not occur, and a record that it was decided on purpose.

**Strongest at:** refusing the loop on call five, denying a tool the agent should never have, requiring a person for the expensive action, producing evidence somebody else can verify.

**Cannot:** explain why the model wanted to do it. A refusal is a decision, not an analysis.

*where they meet*

### A call the control never sees

The control only decides what reaches it. A call that never went through a gateway or a policy point is decided by nothing, and it shows up in the record only if something on its host logged it. Route the agents through the stack before anyone relies on either half.

**Worth checking:** which agents reach the gateway at all. The eBPF discovery sensor in TokenFuse lists the outbound connections it can see from its own host.

## Same incident, both halves.

Take one concrete case: an agent enters a retry loop against a production API at two in the morning and spends four figures before anyone wakes up.

|  | The record alone | The control alone | Both, on one id |
|---|---|---|---|
| At 02:00 | Records every call faithfully | Refuses the call that crosses the cap | Refuses it, and records why |
| At 09:00 | You can reconstruct exactly what happened | You know it was stopped, not why it started | Root cause and a bounded loss |
| The bill | Already spent | Capped at the budget | Capped, and attributable per run |
| The fix | A ticket for next sprint | A cap, without knowing the trigger | A cap now, the trigger fixed properly |
| The auditor | Logs, if retention was right | A signed decision record | Both, joined on one id |

The middle column is deliberately uncomfortable. The control alone is safe and opaque: you know an action was refused, and you cannot say what made the agent try. That is a worse place to debug from than most teams expect, which is why the stack keeps the record running beside the control.

## One run id, or two records that do not agree.

The join is the only integration decision that really matters. If the trace, the spend line, the policy verdict and the outcome tag all carry the same run identifier, then the two halves compose: a refusal in the governance record links to the exact chain of calls that led to it, and a spike in the trace links to the budget that stopped it. If they do not, you have two logs and no way to join them.

In this stack the run id is the unit everything keys on, and the governance planes deliberately emit rather than hoard: policy decisions and quality runs export over OTLP when an endpoint is set, into whatever tracing backend you run, the gateway writes its own traces as Parquet, and every plane emits the same agent-event envelope. **Governance data can sit in your tracing backend; the enforcement decision is made on the call.**

### What any control in the path should answer

- **Does it act in the path, or after it?** If the answer arrives after the call, it is a record, not a control.

- **Is the answer binding?** A warning an agent can proceed past is a note, not a control.

- **What happens when it is unreachable?** Fail-open or fail-closed, chosen and documented, is the honest answer; silence is not.

- **Can somebody else verify the record?** A journal whose entries each carry the hash of the one before it can be checked by a person who does not trust you. Stronger still is a completeness proof on every answer: a short receipt, checkable on its own, that the rows you were shown are all the rows that matched the question. A chain proves nothing was altered. Only a completeness proof says nothing was left out, and that is the half an auditor actually needs. An export on its own offers neither.

- **Does it join on the same id as everything else?** If a component invents its own identifier, the join has to be built by hand.

## Start with the record you already keep.

If you already keep traces but have no enforcement, the shortest path to the other half is not a migration. Route model calls through one gateway, watch in shadow mode for a week, then turn on caps where the outliers are. Your traces keep working; they gain a spend line and a verdict per run.

The governance side is laid out in [the agent governance guide](https://it-rat.com/ai-agent-governance.html), the money in [FinOps for AI](https://it-rat.com/finops-for-ai.html), and the defensive half in [AI agent security](https://it-rat.com/ai-agent-security.html). All of the tools are Apache-2.0, run on infrastructure you own, and export into the observability stack you already run, when an endpoint is set.

## Where one ends and the other begins

**Q: What is the difference between LLM observability and AI governance?**
Observability reconstructs what an agent did: traces, token counts, latencies, evaluations. Governance decides what it may do next, in the request path, with a binding answer. One is a record you can question, the other is an action that did or did not happen.

**Q: Do I need both, or will tracing be enough?**
Tracing alone leaves every insight arriving after the action and often after the invoice. Governance alone leaves you safe and opaque: you know an action was refused and cannot say what made the agent try. Most teams already have the first half, and the shortest path to the second is a gateway in shadow mode.

**Q: How do the two connect technically?**
On one run identifier. If the trace, the spend line, the policy verdict and the outcome tag all carry the same id, a refusal links to the exact chain of calls that led to it. If they do not, you own two dashboards and an argument.

**Q: Does adding governance mean replacing our tracing stack?**
No. The governance planes here export over OTLP when an endpoint is set, into whatever backend you already run, and the gateway writes its own traces, so governance data lands in your observability stack rather than competing with it. What does not belong in a dashboard is the enforcement decision itself.

**Q: How can I tell whether a tool actually enforces anything?**
Four questions. Does it act in the path or after it? Is the answer binding, or can the agent proceed past a warning? What happens when it is unreachable, and is that choice documented? Can somebody who does not trust you verify its record?

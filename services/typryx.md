<!-- https://it-rat.com/services/typryx.html -->

# Typryx, typed answers

> A typed answer, choice, score or yes/no, with a probability, never a guess: capped, journaled, and calibrated against real outcomes.

Agents already ask each other, and their models, questions that have exactly one shape: choice (which option), score (how good, on an ordered scale) or yes/no. Typryx takes a question from a versioned template and returns a typed answer read off a probability distribution, or refuses with a named reason instead of inventing one. Only the fields the template names ever leave the box, and every answer, refusal or timeout lands on a hash-chained journal.

## Every real judgement from one run, replayed in the same order.

Not an illustration: these are the 60 real arithmetic judgements from the calibration table below, qwen2.5:7b run locally on Ollama, wording v2, in the order they were asked (the real run took 9.44 seconds; this replay plays it about 2× slower). Watch the resolved probability, the verdict, and how often "confident" and "right" turn out to be different things.

## The path of one ask.

An agent reaches typryx over MCP, most often through tokenfuse's broker, both measured. Inside, a call crosses the door, the template lookup, the egress filter and the hourly cap before it reaches a swappable backend; the answer is read off the probability distribution, never taken as the backend's own claim. Everything is journaled. On the right: the calibration loop that scores a later truth, and the consumers, all still planned, that would read the journal.

## Where can an ask stop, and what does it leave behind?

Six shapes, exact codes from `internal/service/service.go` and `internal/api/api.go`. Pick one.

## Where Jev meets the stack.

Three question shapes are the whole contract: `choice`, `score`, `noul` (yes/no). A template goes to any backend unchanged, because the templates are the contract and the backend is swappable. Switch the backend and watch what is sent and what comes back change; the typed-answer shape at the far right never does.

| template | type | options | who would ask it | status |
|---|---|---|---|---|
| eval.outcome_met | noul (yes/no) | n/a | Verdryx's grading; the calibration run below used it | measured 2026-09-25 |
| eval.answer_quality | score | 4 ordered levels | Verdryx grader | measured 2026-09-25 |
| request.complexity | choice | cheap / default / hard / reasoning | TokenFuse router, shadow mode only | planned, shadow only |
| action.risk_class | choice | read_only / reversible_change / destructive / external_send / financial | Wardryx, through `wardryx-proxy`, from the tool, its arguments and its target only | released in v0.4.0, run on the stub only |

## Three modes: where your data goes.

You pick one when you install typryx, and you can change it later. With Jev, the fields a question names go to TypeSafe AI. With your own model, nothing leaves your hardware. With it off, the stack runs as it did before. All three were run on the same 434 questions, below.

### Jev

run live 2026-09-30

A hosted service from TypeSafe AI. Only the fields a template names leave the box, to a third party that handles them under its own terms. Of the three modes it was the most accurate and the best calibrated on the test below.

Whether that is worth sending those fields out is a decision for whoever answers for your data. It is never the default.

### Your own model

measured 2026-09-30

Any OpenAI-compatible server you run yourself, such as Ollama or vLLM. Nothing leaves your hardware. You choose the model, and you can tune it on your own questions (next section).

The one measured here is a small 7B model on a machine with no GPU. A model you have tuned, or a machine with a GPU, is not measured.

### Off

the default

typryx is not started. The rest of the stack runs exactly as it did before, and this is what every launcher does until you choose another mode.

Without typryx, an agent that needs a typed answer gets one fixed default. That is the bottom row of the chart.

ECE is expected calibration error: lower means the confidence a backend states matches how often it is right. The fixed answer states certainty every time, so its ECE is one minus its accuracy. The questions are synthetic and frozen, each label follows from how its question was built, and an independent re-label agreed on every one of the 434 questions. The benchmark and its runner are public: [github.com/TAIPANBOX/typryx-evalset](https://github.com/TAIPANBOX/typryx-evalset).

| mode | where it ran | accuracy | 95% interval | ECE | median time |
|---|---|---|---|---|---|
| typryx + Jev | TypeSafe AI's hosted service (jev-1.13.0), called from a laptop | 87.1% | 83.6 to 89.9 | 0.042 | 229 ms |
| typryx + your own model | qwen2.5:7b on Ollama, on an 8-vCPU machine with no GPU | 70.0% | 65.6 to 74.2 | 0.273 | 2,130 ms |
| without typryx | a fixed default answer, which is today's behaviour | 25.1% | 21.3 to 29.4 | 0.749 | no model call |

`TYPED_MODE=jev|own-model|off` for stack-single, and `--typed-mode jev|own-model|off` for stack-k8s and stack-up. Off is the default. A key is only ever a file you point at, never an environment value. released in stack-single v1.1.16 and stack-k8s v1.1.22; stack-up runs from main

## Your own model, on your own questions.

typryx does not train, fine-tune, host or ship a model. It keeps the two records a tune needs, the question as the template let it through and the truth a person posted, and it measures the result against the model it replaces. The tuning is yours, on your hardware.

### What it keeps

One line per answered, templated question, in a file on your own disk that only its owner can read: the template and its version, the answer's id, which backend and model answered, and the state as the template let it through. A field the template holds back is on your disk nowhere.

### What it never keeps

The backend's answer or its probabilities. The record has no field for them, and the package that writes it cannot reach the code that knows them. Nothing is written for a question that was refused, unanswered or free-form.

It is off by default: with no directory set, nothing is written and no directory is created.

### Why labels are human truths only

The export labels a question with the truth a person posted and with nothing else. A hosted model's answer never becomes a training label, which matters because TypeSafe's agreement forbids using Jev's output to train another model.

What typryx cannot see is how a person reached a truth. A label copied from a model's answer would get through, and the poster's own word is the only record of where it came from.

Decided 2026-09-30: a customer picks one of three data modes for typed answers, typryx does not train or ship models, and a customer can tune their own model on their own questions and measure it with typryx.

### Toggle the extra fields. The egress never changes.

Only `task` and `final_answer` are in the template's `fields`, so they are the only two that ever reach the backend, whatever else sits in the state. The type a backend receives is constructible only inside the template package, so a map or raw state cannot reach one even by an implementation mistake.

Measured on a live run: a five-field state carrying `user_email` and, separately, `customer_iban`, neither ever reached the backend or the record. Through Claude Code over MCP, an extra `api_token` field never reached the record either (`held_back_fields: 1`).

### Never invents an answer

A backend error, a timeout, missing or malformed probabilities, a cap hit: the answer is unanswered with a named reason, and the wire shape omits `answer` and `probabilities` entirely. No renormalizing, no fallback guess.

The served answer is always read back off the probability distribution itself: the argmax for a choice, the level for a score, `probabilities["true"]` for a yes-or-no, never from a claim the backend states alongside a disagreeing distribution.

## The one-token shortcut is not always faster.

Same 60 items, seed 1, timed end to end from the caller (`go run ./examples/speed`, typryx f4045e0, one run each, so read the medians as indicative rather than final).

| way of deciding | model | median | p95 | accuracy |
|---|---|---|---|---|
| typed, one token, through typryx | gpt-4.1-mini | 538 ms | 795 ms | 71.7% |
| text judge, short verdict | gpt-4.1-mini | 723 ms | 1,012 ms | 100% |
| reasoning judge | gpt-5.4-mini (current, reasoning) | 562 ms | 896 ms | 100% |
| typed, one token, through typryx | qwen2.5:7b | 148 ms | 159 ms | 66.7% (3 of 60 unparsed, counted wrong) |
| text judge, short verdict | qwen2.5:7b | 1,509 ms | 2,103 ms | 100% |

Against a hosted API the network dominates: on gpt-4.1-mini the shortcut was about 1.3× faster than a short text verdict and gave up about a third of the accuracy, and gpt-5.4-mini, a current small reasoning model, was right on all 60 in about the same time as the shortcut. Locally, on qwen2.5:7b, the shortcut is about 10× faster. A typed decision earns its place by the probability it carries and where it runs, not by speed; vendor speed claims are not on this page. Jev is not on this chart: it was measured on a different set of questions, the 434 in [Three modes](https://it-rat.com/services/typryx.html#modes), and the two sets are never mixed.

## Stated confidence and actual accuracy are not the same number.

Eight groups, 480 judgements, never pooled: `typryx calibration --min-n 30 --json` over durable ledgers, 60 arithmetic judgements per group, seed 1, template `eval.outcome_met`, backend openai-logprobs, half the items right and half wrong. Five models: three OpenAI models of the previous generation over the hosted API (gpt-4.1-mini, gpt-4o-mini, gpt-4.1-nano, each with two template wordings) and two open-weight Qwen 2.5 models run locally on Ollama (3B and 7B). Every group was 96% to 100% confident on average and right 50% to 73% of the time. Click or focus a dot for its numbers.

Every group was 96% to 100% confident on average, right 50% to 73% of the time, and the errors do not lean one way: three groups (gpt-4.1-nano in both wordings, and qwen2.5:3b) said "correct" to every one of 60 items, right exactly half the time, the base rate. gpt-4.1-mini mostly passed a wrong answer as right; gpt-4o-mini erred both ways; qwen2.5:7b never passed a wrong answer but failed a third of the right ones. Rewording (v1 to v2) barely moved accuracy, because a one-token judge has no room to work anything out before answering: it suits classification, not verification. OpenAI's current models, gpt-5.x and gpt-6, refuse token probabilities outright (probed 2026-09-25: "'logprobs' is not supported with this model"), so this backend reaches only earlier hosted models and open models.

| model | wording | n | stated | accuracy | ECE | Brier | right | lenient | strict |
|---|---|---|---|---|---|---|---|---|---|
| gpt-4.1-mini | v1 | 60 | 0.990 | 0.733 | 0.267 | 0.525 | 44 | 15 | 1 |
| gpt-4.1-mini | v2 | 60 | 0.958 | 0.733 | 0.243 | 0.505 | 44 | 15 | 1 |
| gpt-4o-mini | v1 | 60 | 0.987 | 0.583 | 0.414 | 0.823 | 35 | 11 | 14 |
| gpt-4o-mini | v2 | 60 | 0.983 | 0.633 | 0.358 | 0.716 | 38 | 5 | 17 |
| gpt-4.1-nano | v1 | 60 | 0.99999 | 0.500 | 0.500 | 1.000 | 30 | 30 | 0 |
| gpt-4.1-nano | v2 | 60 | 0.9995 | 0.500 | 0.500 | 0.999 | 30 | 30 | 0 |
| qwen2.5:3b | v2 | 60 | 0.998 | 0.500 | 0.498 | 0.995 | 30 | 30 | 0 |
| qwen2.5:7b | v2 | 60 | 0.965 | 0.667 | 0.298 | 0.597 | 40 | 0 | 20 |

Exact models: gpt-4.1-mini-2025-04-14, gpt-4o-mini-2024-07-18 and gpt-4.1-nano-2025-04-14 over OpenAI's API; qwen2.5:3b and qwen2.5:7b on Ollama on a development Mac. Wording v1 is the example template (`2d3ecbdc`), v2 asks plainly whether the answer is exactly correct (`781efaaf`); the local models ran v2 only. Every figure here is one run of 60 items, reproducible with `examples/calibration` in the repository.

**stated confidence**
The probability the model's own answer carried when it was given, averaged over the group.

**ECE**
Expected calibration error: the average gap between stated confidence and actual accuracy across the bins, 0 is perfect.

**Brier**
Mean squared error between the stated probabilities and the true outcome; here, multi-class, 0 is best and 2 is worst.

## What each part of the stack would get.

Three edges are measured live. The Wardryx edge is built and released and measured on the stub backend only; the rest are what a later integration would read, not something built. Click or focus a node.

Click or focus a node above for what typryx gives it, which template, and what happens with typryx absent.

|  | what typryx gives it | status |
|---|---|---|
| MCP clients (Claude Code and others) | a typed answer with a probability, per call, over MCP | measured |
| TokenFuse, as broker | a named upstream; one tool_call recorded against the agent | measured |
| TokenFuse, router shadow mode | the class it would have routed to, alongside cost, recorded only | planned |
| Verdryx | a typed grader beside the existing LLM judge, opt-in per run with `--typed-url` | measured |
| Wardryx | an `action.risk_class` signal a `hold_if_signal` rule may turn into a hold, never a deny; opt-in in the launchers, off by default | built and released, measured on the stub only |
| CostCrew | a suggested class or priority at triage; a person still decides | planned |
| Genaryx | a panel, live only when `GENARYX_TYPRYX_URL` resolves | planned |
| Engram | an optional importance score | planned |
| Journal readers (Trailryx, Idryx) | the same agent-event envelope; Idryx will never call typryx, its detection stays deterministic | planned |

## A probability, never an enforcement decision.

### No deny from a probability

Not here, and not in a consumer. Wardryx's `hold_if_signal` rule may turn a signal into a hold, which a person releases; nothing turns a probability into a deny. It is built and released, and measured on the stub backend only.

### Calibration, never pooled

`typryx calibration` groups by template, template version, backend and model, never averaged across any of the four. Two models under the same question with opposite calibration would otherwise cancel out on paper while neither is fine.

### A later truth, scored honestly

An outcome posted later is scored against the exact template version an answer was asked under, read from the ledger's own record, never against whatever the live template says today. A second outcome for the same answer is refused.

### One direct dependency

agent-stack-go, the stack's shared envelope library, is the only import beyond the standard library. A hostile-input sweep runs against the backends that parse bytes from outside the process, and the ledger survives a torn write mid-crash without losing the record after it.

### Spend capped by default

1,000 calls an hour by default, counted only against calls that got past the door, the template lookup and the egress filter. Disabling it logs a warning at boot rather than doing it quietly.

### Offline by default

The stub backend is deterministic and free, for tests and demos, and every answer it gives says so. The suite itself runs against httptest fakes; nothing in the test run reaches a live network.

### Optional, and it changes nothing when it is absent.

Typryx sits behind [TokenFuse](https://it-rat.com/tokenfuse.html)'s MCP broker as a named upstream, so a call an agent makes is priced and recorded there before it ever reaches typryx's own door; the `request.complexity` template maps directly onto that router's own task classes, in shadow mode only, planned rather than built. [Verdryx](https://it-rat.com/verdryx.html) can ask typryx for a typed verdict beside its existing LLM judge, opt-in per run, and post a person's label back as the truth; measured on 2026-09-25. A typed answer is a single number a policy can threshold, calibrated against real outcomes rather than assumed honest, and it does not replace the judgement Verdryx already makes. [Wardryx](https://it-rat.com/wardryx.html) can read one: `typryx wardryx-proxy` sits in front of it, asks `action.risk_class` about a pending tool call, and adds the answer to the decision request, where a `hold_if_signal` rule may turn it into a hold, which a person releases. Nothing here or in a consumer turns a probability into a deny. The launchers carry it as an opt-in, off by default, from stack-single v1.1.17 and stack-k8s v1.1.23, and it was measured on the stub backend only, never with a real model behind it.

Without it, the rest of the stack behaves exactly as it does today: nothing here is consumed by anything else unless an operator wires it in.

Released as v0.4.0 on 2026-10-04, adding the `action.risk_class` template and `wardryx-proxy`, after v0.3.0 on 2026-09-30 and a first tag, v0.1.0, on 2026-09-25: a signed image on ghcr.io for amd64 and arm64, and a release page with SBOMs; public on GitHub, CI green. Built and tested: the HTTP and MCP surfaces, the stub, openai-logprobs and jev backends, the journal and ledger, calibration, and the opt-in training log and export. Jev ran live on 2026-09-30, and all three data modes were measured on the same 434 questions.

Not yet: a model tuned from an export and measured against the one it replaces, the Wardryx signal with a real backend behind it, and the deeper consumers in the tables above.

## A typed answer, and what it does and does not do

**Q: Is typryx required to run the rest of the stack?**
No. It is an optional add-on, and every other service keeps its current path unchanged when it is absent. Nothing in this repository or a planned consumer is built to depend on it.

**Q: What leaves the box when I send it a state?**
Only the fields the template's own `fields` list names, held by the type system rather than a promise: `internal/backend.Backend.Ask` takes a `template.Egress`, a type constructible only inside the template package. Measured on a live run: a state carrying `user_email` and, separately, `customer_iban`, neither reached the backend or the record.

**Q: Can a probability block anything?**
Not here, and not in a consumer. A probability is a signal a policy can threshold; Wardryx's `hold_if_signal` rule can turn one into a hold, which a person releases, and never into a deny. That path is built and released, and measured on the stub backend only.

**Q: How do I know a probability is honest?**
Not from the number alone, which is the finding of the calibration run below: every group was 96% to 100% confident on average and right 50% to 73% of the time. `typryx calibration` groups by template, version, backend and model, never pooled, and prints accuracy, mean confidence, ECE and Brier against a later truth posted to `/v1/outcome`, so calibration is measured rather than assumed.

**Q: Does typryx need Jev to be useful?**
No. Jev is one backend behind one interface, not the contract. The stub backend answers deterministically for tests and demos, and openai-logprobs reaches any OpenAI-compatible server, including a model on your own hardware. Jev has run live (2026-09-30) and was the most accurate of the three data modes on the 434 questions, but it is a hosted service: choosing it sends the fields a question names to TypeSafe AI. With your own model nothing leaves your hardware, and with typryx off the stack runs as it did before.

**Q: Can I use my own model instead of Jev?**
Yes. Point typryx at any OpenAI-compatible server you run, such as Ollama or vLLM, and nothing leaves your hardware. On the same 434 questions a 7B model on a machine with no GPU was less accurate and less well calibrated than Jev, and slower. You can also tune a model on your own questions: typryx keeps an opt-in training log and exports the questions a person has judged, and it measures the new model against the old per template. It does not train or ship a model, and no tune has been run from an export yet.

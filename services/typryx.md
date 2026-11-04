<!-- https://it-rat.com/services/typryx.html -->

# Typryx, typed answers

> A typed answer, choice, score or yes/no, with a probability, never a guess: capped, journaled, and calibrated against real outcomes.

Typryx takes a question from a versioned template and returns a typed answer read off a probability distribution, or refuses with a named reason instead of inventing one. Every answer, refusal or timeout lands on a hash-chained journal.

## Every real judgement from one run, replayed in the same order.

Not an illustration: these are the 60 real arithmetic judgements, qwen2.5:7b run locally on Ollama, wording v2, in the order they were asked. Watch how often "confident" and "right" turn out to be different things.

## The path of one ask.

Inside, a call crosses the door, the template lookup, the egress filter and the hourly cap before it reaches a swappable backend.

## Where can an ask stop, and what does it leave behind?

Six shapes, exact codes from `internal/service/service.go` and `internal/api/api.go`. Pick one.

## Where Jev meets the stack.

Three question shapes are the whole contract: `choice`, `score`, `noul` (yes/no). Switch the backend and watch what is sent and what comes back change; the typed-answer shape at the far right never does.

## Three modes: where your data goes.

With Jev, the fields a question names go to TypeSafe AI. With your own model, nothing leaves your hardware; with it off, the stack runs as it did before.

ECE is expected calibration error: lower means the confidence a backend states matches how often it is right.

| mode | where it ran | accuracy | 95% interval | ECE | median time |
|---|---|---|---|---|---|
| typryx + Jev | TypeSafe AI's hosted service (jev-1.13.0), called from a laptop | 87.1% | 83.6 to 89.9 | 0.042 | 229 ms |
| typryx + your own model | qwen2.5:7b on Ollama, on an 8-vCPU machine with no GPU | 70.0% | 65.6 to 74.2 | 0.273 | 2,130 ms |
| without typryx | a fixed default answer, which is today's behaviour | 25.1% | 21.3 to 29.4 | 0.749 | no model call |

`TYPED_MODE=jev|own-model|off` for stack-single, and `--typed-mode jev|own-model|off` for stack-k8s and stack-up. Off is the default. released in stack-single v1.1.16 and stack-k8s v1.1.22; stack-up runs from main

## Your own model, on your own questions.

typryx does not train, fine-tune, host or ship a model.

### Toggle the extra fields. The egress never changes.

Only `task` and `final_answer` are in the template's `fields`, so on a template ask they are the only two that reach the backend. The one exception is a freeform question, which sends the whole state when TYPRYX_ALLOW_FREEFORM=1 is set (off by default).

Measured (undated, see the typryx README): a five-field state carrying `user_email` and, separately, `customer_iban`, neither ever reached the backend or the record.

## The one-token shortcut is not always faster.

Same 60 items, seed 1, timed end to end from the caller, one run each, so read the medians as indicative rather than final.

## Stated confidence and actual accuracy are not the same number.

Eight groups, 480 judgements, never pooled. Every group was 96% to 100% confident on average and right 50% to 73% of the time.

## What each part of the stack would get.

Three edges are built and wired in, and each has been run: MCP clients and the TokenFuse broker on 2026-09-25, Verdryx's typed grader against typryx v0.5.1.

Click or focus a node above for what typryx gives it, which template, and what happens with typryx absent.

## A probability, never an enforcement decision.

### Never invents an answer

A backend error, a timeout, missing or malformed probabilities, a cap hit: the answer is unanswered with a named reason.

### No deny from a probability

Wardryx's `hold_if_signal` rule may turn a signal into a hold, which a person releases; nothing turns a probability into a deny.

### A later truth, scored honestly

An outcome posted later is scored against the exact template version an answer was asked under, never against whatever the live template says today.

## What is not proven yet.

- Not yet: a model tuned from an export and measured against the one it replaces, the Wardryx signal with a real backend behind it, and the deeper consumers.

- OpenAI's current models, gpt-5.x and gpt-6, refuse token probabilities outright, so the openai-logprobs backend reaches only earlier hosted models and open models.

## Optional, and it changes nothing when it is absent.

### The Typryx guide

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

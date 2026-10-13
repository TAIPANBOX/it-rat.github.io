<!-- https://it-rat.com/first-alert.html -->

# From zero to your first alert

> One command, one address, one mail: the shortest honest path from nothing to a governed agent that writes to you when it crosses a line.

The shortest honest path from nothing to a governed agent that writes to you when it crosses a line. Four steps, on a machine you own, with no account to create and nothing to buy. **This page explains what each step does and where it goes wrong.** The exact commands live in the repositories, deliberately, because a second copy of an install procedure is a second thing to keep true.

## What you need, and what you do not.

**You need** a Debian or Ubuntu box you control, Docker on it, and somewhere to send mail: your own SMTP server, or a corporate relay you already have. That is the list.

**You do not need** an account with us, a licence key, a trial, a credit card, an API key for the store, or a cloud. Nothing in the stack calls home, and nothing about your runs, your spend or your identities travels anywhere to be displayed. There is no hosted plane, so there is nothing to sign up for.

An LLM provider key is a separate question. The gateway sits in front of whichever provider you already use, so you need whatever key you were already using.

## Four steps.

### Stand the stack up

One installer brings up the whole governed set as containers on one Docker network: the gateway, the control plane, the policy plane, the identity plane, its database, the console behind its own tunnel, and the notifier. It generates its own credentials into the box's own environment file, so no secret in it was ever ours to see.

It comes up **closed**. The gateway publishes to the host's loopback, so a machine that just ran an install script has not acquired an internet-facing enforcement plane because nobody typed anything. Opening it to the agents you actually have is one variable, and it is a decision you make rather than a default you inherit.

### Point one agent at it

The integration is a base URL. Whatever your agent already uses to reach its provider now points at the gateway instead, and from that moment every call it makes is priced, budgeted and policy-checked in the request path. No SDK to adopt, no framework to migrate to, no code change beyond an environment variable.

Send the agent's run a budget along with the request, and you have the thing worth having: a ceiling that is enforced before the provider is called rather than noticed afterwards on a bill.

### Give it an address to write to

The notifier reads the shared event log and mails you when one of your own agents crosses a line: a budget gone, a policy denial, a run killed, an agent behaving unlike itself. Set a recipient and an SMTP host, and it starts. Leave them blank and it stays healthy and silent, because not having mail is a choice an operator makes rather than a broken deployment.

What it will not do is more interesting than what it will. It holds no credential for any plane, opens no connection to one, has no API of its own, and can take no action on any agent. It reads a file and sends mail. That narrowness is the point: it is the one component allowed to reach the outside world, so its blast radius stays small enough to say in a sentence.

### Make it fire on purpose

Do not wait for a real incident to find out whether any of this works. Give a run a budget of a fraction of a cent and let an agent loop against it: the gateway answers 402 in the request path, the event lands in the log, and the mail arrives. That is the whole chain, exercised in a minute, at no cost. Know which mail you are waiting for: at the notifier's default floor a single refusal is below it, and the message comes from the control plane once a run has been refused three times, as `budget_exhausted`. A run on 2026-09-17 found that on the installer's released versions that message never reached the log at all, because the control plane could not create its own events file and said nothing; the installer on `main` creates the file for it, which is what the one-line command installs.

Then read the mail carefully, because it is deliberately almost nothing: identifiers and numbers, never content, and one link into your own console rather than a button. Following it opens the panel showing that event. The action happens there, behind your sign-in.

Every exact flag lives in the repository that owns it, and this guide points at those rather than repeating them. A copy here would be a second place to keep true, and it would drift the first time an installer grew a flag: you would follow the pretty page and hit the error the README already documents. What a guide can add is the part a README cannot, which is what the step is for and how it fails.

## Three things worth doing next, in order.

### Write one policy, not ten

The first policy that earns its keep is usually a single denied tool or a spend level above which a human has to agree. The policy plane answers allow, deny or hold on every governed call, and **hold** is the one people underuse: it does not park a connection or block a thread, it refuses with an approval id that somebody grants out of band, and the proof of that grant is a signed token the agent presents on the retry.

### Give your agents passports before you have many

A passport is a small static JSON document: an identifier, an owner, a runtime, and an attestation method. It is not a token and nothing at runtime depends on fetching it. It exists so that when something goes wrong at 3am the first question, whose agent is this, has an answer that is not a guess. Writing them for four agents is an afternoon; writing them for forty is a project.

### Decide what you are keeping, before the volume decides for you

Every governed decision is audited rather than sampled, at roughly 426 bytes each. At a thousand calls a minute that is about 614 MB a day. It is the only part of running this that grows without anyone choosing to grow it, so it is worth a retention decision early rather than a surprise later.

- **Is the gateway reachable from where you think, and only there?** Read back the rule that was actually written, not the variable that was supposed to produce it.

- **Does an unknown key get refused?** A plane that authenticates nobody looks identical to a healthy one from outside.

- **Did the mail actually arrive, on a phone?** A plain-text alert that is unreadable on the device you will read it on at 3am is not an alert.

- **Does the link in it open a view rather than perform an action?** If it acts, anyone who can forward the message holds the capability.

- **Have you fired the guardrail on purpose at least once?** Before you rely on it, not after.

- **Does it survive a reboot?** Restart the box and check that everything comes back, including the notifier's own read position. We measured one on 2026-09-17: the first reboot lost the gateway on a box whose gateway sat on a tunnel address, because Docker bound the port before the tunnel held the address, and the installer now orders the two; the second reboot, with the fix, brought the containers and the gateway back on their own.

## Where this sits.

This is the shortest path. [One incident, end to end](https://it-rat.com/one-incident-end-to-end.html) follows what happens after that first mail through every plane, [what runs where and what it costs](https://it-rat.com/what-runs-where.html) covers the shapes past one machine, and [the guides index](https://it-rat.com/guides.html) has the field itself. Everything named here is Apache-2.0 and runs on hardware you own.

## What people ask before starting

**Q: What do I actually need before I start?**
A Debian or Ubuntu box you control, Docker on it, and somewhere to send mail: your own SMTP server or a corporate relay you already have. That is the whole list. There is no account to create, no licence key, no trial and no card. Nothing calls home, and there is no hosted plane, so there is nothing to sign up for.

**Q: Do I need an LLM provider key to try it?**
Only if you want real calls. The gateway sits in front of whichever provider you already use, so you need the key you were already using.

**Q: How does an agent get pointed at the gateway?**
By changing the base URL it already uses to reach its provider. That is the entire integration: one environment variable, no SDK to adopt and no framework to migrate to. From that moment every call it makes is priced, budgeted and policy-checked in the request path.

**Q: Is anything exposed to the internet after the install?**
No. The gateway publishes to the host's loopback by default, so a machine that just ran an install script has not acquired an internet-facing enforcement plane because nobody typed anything. Opening it is one variable and a decision you make. Re-running the installer will not widen it for you either, because the environment file is left alone once it exists.

**Q: Why does this guide not list the exact commands?**
Because they live in the repository that owns them, and a copy here would be a second place to keep true. It would drift the first time an installer grew a flag, and you would follow the pretty page into an error the README already documents. What a guide can add instead is what each step is for and how it fails.

**Q: How do I check it works without waiting for a real incident?**
Give a run a budget of a fraction of a cent and let an agent loop against it. The gateway answers 402 in the request path, the event lands in the log and the mail arrives, which exercises the whole chain in a minute at no cost. At the default floor the mail is the control plane's budget_exhausted after the third refusal, not the first 402, so loop at least three times. Do this before you rely on it: a guardrail nobody has fired is a claim rather than a control.

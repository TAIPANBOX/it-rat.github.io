<!-- https://it-rat.com/pocket-guide.html -->

# TokenFuse Pocket guide

> How TokenFuse Pocket is designed to work, how it differs from Heraldyx, where it sits in the stack, and why it is not wired into a running stack yet.

The [Pocket room](https://it-rat.com/services/pocket.html) keeps the simulation, the live design mock and the drawing. This guide keeps the rest of what the room used to say: the screens in full, Pocket beside Heraldyx, where it sits, and the full account of why it is in the stack and not wired into one yet.

- [At a glance](https://it-rat.com/pocket-guide.html#overview)

- [How it works](https://it-rat.com/pocket-guide.html#how-it-works)

- [Pocket and Heraldyx](https://it-rat.com/pocket-guide.html#heraldyx)

- [Where it sits](https://it-rat.com/pocket-guide.html#where-it-sits)

- [Limits](https://it-rat.com/pocket-guide.html#limits)

## Pocket at a glance.

- **In the stack, and not wired into one yet.**

- **Watch the fleet burn live, and cut it from a device no attacker touched.**

- **Platform:** iOS · watchOS · SwiftUI. **Surfaces:** Dynamic Island · Live Activity · Watch complication.

- **Signing:** Secure Enclave, keys never leave the device.

- **Pairs with:** nothing today; genaryx-relay was removed.

- **Status:** no hardening pass, no whole-app security review. **Licence:** Apache-2.0.

### What it is

TokenFuse's gateway enforces the budget in the request path your agent runs on. Pocket asks what a control OUTSIDE that path should look like on a device you already carry: the fleet's burn rate live, and a kill signed by hardware the agent's host never touches. Both apps are built. The iPhone app's README says every screen was driven live against a real control plane on the simulator. That is a long way from shipped: no production hardening pass, no security review, no App Store. The effort goes to the web console, and this moves when there is time for it.

## Not a bigger dashboard. A switch you can actually reach.

### Sixty seconds, one kill

This is a simulation, but it replays a shape the app is built for: a run drifts from baseline to 2.4x its burn rate, crosses a budget, and gets killed from an Apple Watch before anyone opens a laptop. The signature that authorizes the kill never leaves the Secure Enclave; the gateway only has to trust the result. [Watch it in the room](https://it-rat.com/services/pocket.html#sim).

### Do not watch it. Drive it.

An interactive design mock of the iPhone and Watch apps, running here as a web page. Seven iPhone screens, a Live Activity surface and five Watch screens, all live: the burn ticks and every screen is driveable. The ceremony the app implements is stricter than this mock: a kill is confirmed by name and signed on the device, and a killed run then leaves the pager, staying in the console and the audit trail. Drive it with the steps, the tab bar, or the Watch switch.

The mock runs [in the room](https://it-rat.com/services/pocket.html). Its seven steps, in full:

- **01 Runs, the deck.** Fleet burn up top, then the exception queue: the runs at or over their cap, worst first. The healthy fleet stays quiet.

- **02 Run detail, pull the breaker.** Spend against cap, model and steps. The kill wants you to mean it: slide to arm, then Face ID.

- **03 Budgets, the ladder above a run.** A cap on each run, and a monthly cap for each business unit, both enforced by the gateways. The org, team and agent ladder on this screen is a drawn design.

- **04 Agents, sorted by behaviour.** Not spend, conduct: a runaway agent, one reaching tools it never used, an orphaned key. Tap for why it fired and its blast radius.

- **05 Pairing, one scan and a key that stays.** As designed, your console would issue a one-time code, and scanning it would mint a signing key in the Secure Enclave that never leaves the phone. No console code issues one today.

- **06 Device, and how far it reaches.** The paired iPhone and the last action it signed. The mock draws a Default and a Strict peer mode for the Device screen. Neither is built.

- **07 Alerts that mean act.** Built for a relay that pushes the moment a cap breaks. Tap a banner to land on the run, or arm the kill from the wrist.

### One phone. One key. A path the gateway never sees.

As designed, the app pairs to a relay beside TokenFuse Cloud, never to the gateway your agent talks to, and no such relay runs today. A kill or a budget change is signed on-device by the Secure Enclave, forwarded byte for byte by the relay to Cloud, and pushed out to every gateway in the fleet from there. The request path and the kill path never share a wire.

### The fuse, everywhere

Mint under budget, amber warming, ember at the cap. The run list, the Dynamic Island, and the watch face all read the fuse the same way, so nothing needs translating between screens.

### Hardware-signed kill

The design signs every kill on-device, so a fully compromised server can neither forge that order nor change it. It can still refuse to pass the order on. The same property is what the web console reaches for with a passkey, which is why this became the direction we are building first.

### The fleet at a glance

Every run with its spend, its burn rate in dollars per minute, and how close it sits to a budget break, sorted hottest first, red once it's over.

### Pairing in seconds

Scan the QR code a Genaryx relay issues. No relay runs today, so nothing can be paired yet. The key is generated inside the Secure Enclave and never leaves it, not even to the app.

## Heraldyx mails you. Pocket buzzes. They are not the same control.

Both answer one question, how a human finds out, and they answer it from the same events. The difference is what each one is allowed to do about it, and that difference is the reason both exist rather than one replacing the other.

### The same four signals

Pocket surfaces `budget_exhausted`, `sustained_loop`, `fanout_explosion` and `spend_spike`. All four are in [Heraldyx](https://it-rat.com/services/heraldyx.html)'s catalogue too, with a sentence each for what happened, what the box already did, and what happens if nobody acts.

### One arrives here and never there

`spend_spike` is about a whole organisation, and the shared envelope requires an agent id, so its producer skips it rather than inventing a subject. It was built to reach this phone through the relay's own read slice, and it never reaches the mail. An operator who only reads mail does not learn about it.

### Mail cannot act. This can

Heraldyx reads a file and speaks SMTP, holds no credential for any plane, and its link is a view with no action in it, because mail gateways prefetch links. Pocket is the opposite by design: it pairs to a relay and the kill is signed on the device. That is a bigger blast radius, and it is why it needs a Secure Enclave and a per-device pairing rather than an address.

### Different routes, on purpose

Heraldyx reads the planes' shared event log directly, on the box, and needs nothing else running. Pocket reads `relay/v1/exceptions`, so it needs a relay up and the phone paired. Two paths that fail apart: the night the relay is down, the mail still goes out, and while no relay runs at all, the mail is the only one of the two that does.

### And Trailryx?

Nothing connects them. Pocket reads the control plane's own replay, not the record store, and neither knows the other exists.

## The human end of a machine decision.

Pocket is the human end of [TokenFuse](https://it-rat.com/services/tokenfuse.html): the gateway enforces the budget in the request path, Pocket lets you watch it happen and pull the kill switch from somewhere else entirely. A kill is written as a run_killed event on the same agent-event bus the rest of the [Platform](https://it-rat.com/services/platform.html) reads. What actually gets enforced was decided upstream, by [Wardryx](https://it-rat.com/services/wardryx.html) and the budgets you set. Pocket doesn't make that call; it gives you a fast, honest way to see it and override it.

### What it pairs with

Pocket was designed to pair through [Genaryx](https://it-rat.com/genaryx.html) to a TokenFuse plane you host yourself. That relay was removed from Genaryx on 2026-07-28, so nothing pairs today. Both apps are built and open, and neither is connected to a running stack: the console is what an operator uses today.

The plane it reads is open today: [stand up the stack's live services locally in one command](https://it-rat.com/services/platform.html#run) and see the same money plane on your own machine.

## In the stack, and not wired into one yet.

**Where this sits today, stated rather than implied.** Pocket is listed in the stack registry as not wired into a running stack yet. It is designed as the out-of-band control for TokenFuse, the way to pull the Breaker when the machine running the gateway, or the machine running your console, is itself the thing that has gone wrong. That is why the signature comes from the Secure Enclave on a device the agent's host never touches.

**How it is meant to work, and what it lacks today.** The phone pairs once, by QR, to a relay beside the stack. The one it was built against, genaryx-relay, was removed from genaryx on 2026-07-28, so today there is nothing to pair with and none of this runs end to end. The relay pushes only what needs a human, an over-cap run, straight into the signed-kill flow; the kill is signed on the device and the gateway has only to check the signature. The watch pairs on its own and carries the same flow, so a deauthorized device says it was deauthorized rather than pretending.

**What is actually true today.** The interface is finished. The iPhone app's repository records every screen as driven against a real control plane on a simulator. It is not connected to anything you are running: there is no App Store build, no real push delivery, and no hardening pass or whole-app security review; a narrower review on 2026-09-06 led to one transport-security fix. Treat it as the shape of the control rather than a control you have. The console you run today is the [Genaryx](https://it-rat.com/genaryx.html) web app.

### Everything the room says is not done

- Both apps are built. The iPhone app's README says every screen was driven live against a real control plane on the simulator.

- That is a long way from shipped: no production hardening pass, no security review, no App Store. The effort goes to the web console, and this moves when there is time for it.

- The relay it was built against, genaryx-relay, was removed from genaryx on 2026-07-28, so today there is nothing to pair with and none of this runs end to end. No relay runs today, so nothing can be paired yet.

- The live screens on the room are an interactive design mock of the iPhone and Watch apps, running as a web page. The ceremony the app implements is stricter than this mock.

- The org, team and agent ladder on the Budgets screen is a drawn design.

- No console code issues a pairing code today.

- The mock draws a Default and a Strict peer mode for the Device screen. Neither is built.

- `spend_spike` never reaches the mail. An operator who only reads mail does not learn about it.

- The kill from the wrist on the room is a simulation, but it replays a shape the app is built for.

## Back to the room.

The [Pocket room](https://it-rat.com/services/pocket.html) has the simulation, the live design mock and the drawing, and [the guides index](https://it-rat.com/guides.html) has the field itself.

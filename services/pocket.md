<!-- https://it-rat.com/services/pocket.html -->

# TokenFuse Pocket, the out-of-band kill switch

> Our iPhone and Apple Watch app for TokenFuse: the fleet's burn live, and a kill signed by the Secure Enclave. Built, and not wired into a running stack yet.

**Q: what that means**

**Where this sits today, stated rather than implied.** Pocket is
 part of the stack and it is the only part of it you do not run on your own
 box: it is the out-of-band control for TokenFuse, the way to pull the
 Breaker when the machine running the gateway, or the machine running your
 console, is itself the thing that has gone wrong. That is why the
 signature comes from the Secure Enclave on a device the agent's host never
 touches.

**How it is meant to work, and what it lacks today.**
 The phone pairs once, by QR, to a relay beside the stack. The one it was
 built against, genaryx-relay, was removed from genaryx on 2026-07-28, so
 today there is nothing to pair with and none of this runs end to end. The relay pushes only
 what needs a human, an over-cap run, straight into the signed-kill flow;
 the kill is signed on the device and the gateway has only to check the
 signature. The watch pairs on its own and carries the same flow, so a
 deauthorized device says it was deauthorized rather than pretending.

**What is actually true today.** The
 interface is finished and every screen has been driven against a real
 control plane on a simulator. It is not connected to anything you are
 running: there is no App Store build, no real push delivery, and no
 hardening pass or security review. Treat it as the shape of the control
 rather than a control you have. The console you run today is the
 [Genaryx](https://it-rat.com/genaryx.html)
 web app.

TokenFuse's gateway enforces the budget in the request path your agent runs on. Pocket asks what a control OUTSIDE that path should look like on a device you already carry: the fleet's burn rate live, and a kill signed by hardware the agent's host never touches. Both apps are built and every screen was driven live against a real control plane on the simulator, which is a long way from shipped: no production hardening pass, no security review, no App Store. The effort goes to the web console, and this moves when there is time for it.

## Watch the Breaker get pulled from a wrist.

This is a simulation, but it replays a shape the app is built for: a run drifts from baseline to 2.4x its burn rate, crosses a budget, and gets killed from an Apple Watch before anyone opens a laptop. The signature that authorizes the kill never leaves the Secure Enclave; the gateway only has to trust the result.

## Do not watch it. Drive it.

An interactive design mock of the iPhone and Watch apps, running here as a web page. Five iPhone screens and five Watch screens, all live: the burn ticks and every screen is driveable. The ceremony the app implements is stricter than this mock: a kill is confirmed by name and signed on the device, and a killed run then leaves the pager, staying in the console and the audit trail. Drive it with the steps, the tab bar, or the Watch switch.

## One phone. One key. A path the gateway never sees.

As designed, the app pairs to a relay beside TokenFuse Cloud, never to the gateway your agent talks to, and no such relay runs today. A kill or a budget change is signed on-device by the Secure Enclave, forwarded byte for byte by the relay to Cloud, and pushed out to every gateway in the fleet from there. The request path and the kill path never share a wire.

## Not a bigger dashboard. A switch you can actually reach.

### The fuse, everywhere

Mint under budget, amber warming, ember at the cap. The run list, the Dynamic Island, and the watch face all read the fuse the same way, so nothing needs translating between screens.

### Hardware-signed kill

The design signs every kill on-device, so a fully compromised server can neither forge that order nor block it. The same property is what the web console reaches for with a passkey, which is why this became the direction we are building first.

### The fleet at a glance

Every run with its spend, its burn rate in dollars per minute, and how close it sits to a budget break, sorted hottest first, red once it's over.

### Pairing in seconds

Scan a QR code against your own Cloud plane. The app generates a key inside the Secure Enclave on the spot; the key never leaves it, not even to the app.

## Heraldyx mails you. Pocket buzzes. They are not the same control.

Both answer one question, how a human finds out, and they answer it from the same events. The difference is what each one is allowed to do about it, and that difference is the reason both exist rather than one replacing the other.

### The same four signals

Pocket surfaces `budget_exhausted`, `sustained_loop`, `fanout_explosion` and `spend_spike`. All four are in [Heraldyx](https://it-rat.com/heraldyx.html)'s catalogue too, with a sentence each for what happened, what the box already did, and what happens if nobody acts.

### One arrives here and never there

`spend_spike` is about a whole organisation, and the shared envelope requires an agent id, so its producer skips it rather than inventing a subject. It was built to reach this phone through the relay's own read slice, and it never reaches the mail. An operator who only reads mail does not learn about it.

### Mail cannot act. This can

Heraldyx reads a file and speaks SMTP, holds no credential for any plane, and its link is a view with no action in it, because mail gateways prefetch links. Pocket is the opposite by design: it pairs to a relay and the kill is signed on the device. That is a bigger blast radius, and it is why it needs a Secure Enclave and a per-device pairing rather than an address.

### Different routes, on purpose

Heraldyx reads the planes' shared event log directly, on the box, and needs nothing else running. Pocket reads `relay/v1/exceptions`, so it needs a relay up and the phone paired. Two paths that fail apart: the night the relay is down, the mail still goes out, and while no relay runs at all, the mail is the only one of the two that does.

Nothing connects them. Pocket reads the control plane's own replay, not the record store, and neither knows the other exists.

### The human end of a machine decision.

Pocket is the human end of [TokenFuse](https://it-rat.com/tokenfuse.html): the gateway enforces the budget in the request path, Pocket lets you watch it happen and pull the kill switch from somewhere else entirely. A kill lands as an incident on the same event bus the rest of the [Platform](https://it-rat.com/platform.html) reads. What actually gets enforced was decided upstream, by [Wardryx](https://it-rat.com/wardryx.html) and the budgets you set. Pocket doesn't make that call; it gives you a fast, honest way to see it and override it.

Pocket pairs through [Genaryx](https://it-rat.com/genaryx.html) to a TokenFuse plane you host yourself. Both apps are built and open, and neither is
 connected to a running stack: the console is what an operator uses today.

The plane it reads is open today: [stand up the stack's live services locally in one command](https://it-rat.com/platform.html#run) and see the same money plane on your own machine.

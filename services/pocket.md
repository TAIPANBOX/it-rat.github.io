<!-- https://it-rat.com/services/pocket.html -->

# TokenFuse Pocket, the out-of-band kill switch

> Our iPhone and Apple Watch app for TokenFuse: the fleet's burn live, and a kill signed by the Secure Enclave. Built, and not wired into a running stack yet.

**Q: what that means**

**Where this sits today, stated rather than implied.** Pocket is listed in the stack registry as not wired into a running stack yet.

**What is actually true today.** The interface is finished. Treat it as the shape of the control
 rather than a control you have. The console you run today is the
 [Genaryx](https://it-rat.com/genaryx.html)
 web app.

[The full account is in the guide.](https://it-rat.com/pocket-guide.html#limits)

TokenFuse's gateway enforces the budget in the request path your agent runs on. Pocket asks what a control OUTSIDE that path should look like on a device you already carry: the fleet's burn rate live, and a kill signed by hardware the agent's host never touches.

## Watch the Breaker get pulled from a wrist.

This is a simulation, but it replays a shape the app is built for: a run drifts from baseline to 2.4x its burn rate, crosses a budget, and gets killed from an Apple Watch before anyone opens a laptop.

## Do not watch it. Drive it.

An interactive design mock of the iPhone and Watch apps, running here as a web page. Drive it with the steps, the tab bar, or the Watch switch.

## One phone. One key. A path the gateway never sees.

As designed, the app pairs to a relay beside TokenFuse Cloud, never to the gateway your agent talks to, and no such relay runs today. The request path and the kill path never share a wire.

## Not a bigger dashboard. A switch you can actually reach.

### The fuse, everywhere

Mint under budget, amber warming, ember at the cap. The run list, the Dynamic Island, and the watch face all read the fuse the same way.

### Hardware-signed kill

The design signs every kill on-device, so a fully compromised server can neither forge that order nor change it. It can still refuse to pass the order on.

### Pairing in seconds

Scan the QR code a Genaryx relay issues. No relay runs today, so nothing can be paired yet.

## Heraldyx mails you. Pocket buzzes. They are not the same control.

Both tell a human from the same events; what differs is what each may do about it.

Heraldyx reads the planes' shared event log on the box and needs nothing else running; its mail carries a view with no action in it. [In the guide](https://it-rat.com/pocket-guide.html#heraldyx)

As designed, Pocket reads a relay and signs the kill on the device, but the relay it was built against was removed, so none of this runs today. [In the guide](https://it-rat.com/pocket-guide.html#heraldyx)

Wardryx and the budgets you set decide what is enforced and the gateway enforces it; Pocket lets you watch that and pull the kill from somewhere else. [In the guide](https://it-rat.com/pocket-guide.html#where-it-sits)

## Limits, in short.

### Built, driven on a simulator

Both apps are built. The iPhone app's README says every screen was driven live against a real control plane on the simulator.

### Not shipped

No production hardening pass, no security review, no App Store.

### Nothing to pair with

The relay it was built against, genaryx-relay, was removed from genaryx on 2026-07-28, so today there is nothing to pair with and none of this runs end to end.

### The Pocket guide

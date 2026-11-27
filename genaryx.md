<!-- https://it-rat.com/genaryx.html -->

# Genaryx, the console over the stack

> Genaryx: one browser control room over the whole agent stack, on your own box. Passkey-signed kills, WireGuard-only reach and signed evidence packs.

The open services each govern one plane of an agent fleet. Genaryx is the console built on top of them for companies that run real fleets. It runs on your own infrastructure and you open it in a browser.

### The open stack stays open.

Genaryx is Apache-2.0, like everything under it. It is the room built on top of the open services, and you can read every line of it before you run it.

## What the console adds that the stack alone does not.

Genaryx exists for the moment the fleet stops being a side project: when the person on call is not the person who built it, when an auditor asks for proof, when 2am happens.

## One Rust core. Eighteen frames you can open yourself.

Every frame is the demo on simulated data; the live run is in [what is proven](https://it-rat.com/what-is-proven.html). [Every frame, in the guide](https://it-rat.com/genaryx-guide.html#frames)

## An AI that reads everything and can touch nothing.

Felyx is the fleet's analyst. It is also an AI we can honestly ask you to trust, because the trust is structural, not a system prompt.

## Your plane stays yours. Every path in is signed.

The console reaches a client-hosted Cloud from inside your own WireGuard tunnel, so the control plane never faces the internet. And Felyx sits beside it with no signing key at all.

## One shell. One Rust brain. Hardware where it counts.

The browser console is deliberately thin: every screen is a call into one shared Rust command layer. [In the guide](https://it-rat.com/genaryx-guide.html#how-it-works)

Kills, budget changes and approval grants are confirmed per action with a passkey on your own device: Touch ID, Windows Hello or a security key. [In the guide](https://it-rat.com/genaryx-guide.html#how-it-works)

Your box runs the WireGuard side and issues each device its own peer config as a QR: scan, connect, done. [In the guide](https://it-rat.com/genaryx-guide.html#how-it-works)

Every governance event the stack emits carries the SHA-256 of the event before it, so tampering breaks the chain exactly where it happened. [In the guide](https://it-rat.com/genaryx-guide.html#how-it-works)

## Built, and proven on a live fleet.

- A laptop on the public internet opened the console over a tunnel this box issued itself, with no other route in.

- A device-signed kill went through a real fleet, against a plane closed to the internet.

- Felyx, on a live local model, named the caught runaway and filed a capped proposal only a human could approve, on 42 agents.

Clone it, run it, fork it. Apache-2.0, the whole console, with no tier and no key.

Or [run the open stack yourself in one command](https://it-rat.com/services/platform.html#run) today.

### The Genaryx guide

## What the console is, and what it is not

**Q: Is Genaryx free, or is there a paid tier above it?**
It is Apache-2.0, the same licence as every service under it, and an Apache grant on a version already released cannot be taken back afterwards. There is no tier above it, no seat count, no licence key and no account to create.

**Q: Is it open source, or open core with the useful parts held back?**
Open source, and nothing is held back. The console is one repository, [TAIPANBOX/genaryx](https://github.com/TAIPANBOX/genaryx), and every tab in the screenshots above is built from it. There is no edition kept beside it, held back or otherwise.

**Q: Is Genaryx a desktop application?**
No. The core is a Rust binary running on infrastructure you own, and you open the console in a browser. Nothing is installed on a laptop, which is the point at 2am when the person on call is using whatever machine is nearest. Reaching a private plane is the console's own WireGuard tunnel rather than a VPN somebody has to maintain.

**Q: What does the console add that the services do not already do?**
One window over every plane, and three things no single service has a place to put: a destructive action confirmed by the passkey in your hand and journaled with the reason you typed, an incident feed sorted worst-first across every plane, and one signed evidence pack carrying EU AI Act, SR 11-7 and SOC 2 mappings. You can run the open stack by hand in one command, and plenty of teams should. The console is for the point where the person on call is not the person who built it.

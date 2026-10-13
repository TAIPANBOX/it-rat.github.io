<p align="center">
  <img src="assets/img/readme/hero.png" alt="IT-RAT: the source of it-rat.com, an interactive control room for open agent governance" width="100%">
</p>

<p align="center">
  <a href="https://it-rat.com"><img alt="live" src="https://img.shields.io/badge/live-it--rat.com-F4B23E?style=flat-square"></a>
  <a href="https://github.com/it-rat/it-rat.github.io/actions/workflows/pages.yml"><img alt="deploy" src="https://github.com/it-rat/it-rat.github.io/actions/workflows/pages.yml/badge.svg"></a>
  <img alt="build step" src="https://img.shields.io/badge/build%20step-none-2DD4BF?style=flat-square">
  <img alt="dependencies" src="https://img.shields.io/badge/CDNs%20%C2%B7%20trackers-none-8A97A6?style=flat-square">
  <a href="https://github.com/TAIPANBOX"><img alt="stack" src="https://img.shields.io/badge/the%20stack-TAIPANBOX-B48CFF?style=flat-square"></a>
</p>

# it-rat.com

The source of **[it-rat.com](https://it-rat.com)**: a product site for the TAIPANBOX agent-governance
stack, built as an interactive control room rather than a brochure. Every service gets its own room
with a scrubbable simulation of how it behaves over time, an animated architecture diagram, and a plain account of
what it does and how it is proven.

The stack itself is **defensive**: it exists so the owner of an AI-agent fleet can see, price, govern
and stop their own agents. Nothing here is offensive tooling, and the site is written to say so.

## The rooms

| Page | Plane | What it covers |
|---|---|---|
| `index.html` | the stack | The home control room: fuse-wire hero, the service rail, the wiring diagram, live-validation numbers |
| `services/tokenfuse.html` | money | Runtime spend control, budgets, the kill switch |
| `services/engram.html` | memory | The SQLite of agent memory, single file, embeddable |
| `services/wardryx.html` | policy | Policy decisions with a human in the loop |
| `services/idryx.html` | access | One identity graph for humans, keys and agents |
| `services/qryx.html` | crypto | Cryptography inventory and post-quantum risk |
| `services/verdryx.html` | quality | Cost per correctly resolved case, not per token |
| `services/typryx.html` | typed answers | A typed answer with a probability, never a guess; an optional add-on |
| `services/mockryx.html` | pre-prod | Fire drills that prove guardrails hold |
| `services/heraldyx.html` | alerts | The box writes to you, with a link and never a button |
| `services/pocket.html` | out of band | The kill switch on a device the agent's host never touches |
| `services/trailryx.html` | the record | A record nobody can quietly change or shorten, standalone |
| `services/sphere.html` | side project | Twelve life-sphere agents on one on-device memory, not part of the stack |
| `services/platform.html` | contract | Agent Passport, the shared event envelope, Terraform |
| `genaryx.html` | control room | Genaryx, one browser control room over the whole stack, on your own box |

## How it deploys

Push to `master`. That is the whole procedure.

[`.github/workflows/pages.yml`](.github/workflows/pages.yml) checks out the tree, runs three cheap
gates, and publishes. Each one exists because this repo has actually shipped the mistake it catches:
a page pointing at a deleted screenshot (every local `src`/`href` must resolve), a page carrying both
a canonical and a noindex (`scripts/page-metadata.sh`), and a `/demo` built from a Genaryx that has
since moved on (`scripts/demo-bundle-current.sh`).

Pages is set to **GitHub Actions** as its source (since 2026-07-21), not the built-in branch builder,
so a failed publish has a log and a re-run button instead of a silent "Page build failed". The custom
domain lives in `CNAME`, HTTPS is enforced, and `.nojekyll` keeps Pages from reinterpreting the tree.

## Run it locally

```sh
python3 -m http.server 8123 --directory .
```

Then open <http://localhost:8123>. Use http rather than opening the files directly: cross-document
View Transitions do not run on `file://`.

## How it is built

No build step, no CDNs, no external fonts, no trackers. Plain HTML, one stylesheet, a handful of ES
modules, and everything works from any static file server.

- `assets/site.css` is the design system: dark control room, a per-service accent color, view-transition slides.
- `assets/site.js` holds the service registry (id, plane, accent, blurb), the command palette (`Cmd+K` or `/`), directional cross-document View Transitions, reveal-on-scroll, count-up numbers, and arrow-key paging.
- `assets/sim.js` is the timeline engine shared by every service simulation: counters, event log, play, scrub, speed, reduced-motion aware.
- `assets/stages/*.js` is one bespoke stage per service, drawn on that shared timeline: a fuse wire and budget bar for TokenFuse, decision-gate lanes for Wardryx, an estate sweep grid for Qryx, and so on. Each stage is deterministic in `t`, so scrubbing works in both directions.
- `assets/ambient.js` gives each service hero a quiet canvas motif from its own domain: gradient descent, a learned decision boundary, a memory graph with spreading activation, an identity graph, a rotating point lattice, training curves, adversarial bursts against a guardrail.
- `assets/diagram.js` handles the architecture schematics: staggered draw-in on reveal, plus a full-screen lightbox with wheel and pinch zoom, drag pan, and double-click reset, so every label stays readable.
- `assets/shotbox.js` frames and enlarges the product screenshots on the Genaryx page.
- `tools/` renders what is generated rather than hand-kept: `footer.py` (the footer and the corridor rail on every page), `ogimages.py` (one Open Graph card per room), `seo.py` (JSON-LD), `llms.py` (the markdown mirrors and `llms.txt`), `faq.py`, `readmehero.py` and `readmediagrams.py`. They read the service registry out of `assets/site.js`, so a room that leaves the registry leaves the footer, the rail and the images with it.

## House rules for edits

- **Say only what is true.** Nothing on the site is sold, so no page carries pricing; `enterprise.html` is now only a redirect to `genaryx.html`, kept because an indexed URL is somebody else's property. Numbers on the site come from the validation records in the stack repos, not from marketing.
- **No long dashes in copy.** Reword, or use a comma, a colon, parentheses, or a short hyphen.
- **Keep it self-contained.** A new dependency that needs a CDN does not belong here.
- **SVG stays legible.** No raster artwork for diagrams, and no label smaller than 10px; anything dense gets the lightbox.
- **Screenshots belong to the site**, not to the documents next to it.

## Related

The stack this site describes lives at **[github.com/TAIPANBOX](https://github.com/TAIPANBOX)** and is
Apache-2.0: TokenFuse, Engram, Idryx, Qryx, Wardryx, Verdryx, Mockryx, Heraldyx, Trailryx, the
Platform contract, the Genaryx console, and the `stack-up` launcher that runs the whole thing locally
with one command. The one exception is Sphere, a side project outside the stack, which is MIT.

<sub>&copy; 2026 IT-RAT</sub>

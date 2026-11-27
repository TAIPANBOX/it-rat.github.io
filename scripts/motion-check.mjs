#!/usr/bin/env node
// Checks that every room's motion actually runs, in headless Chrome over CDP
// (Node 22, built-in WebSocket). Run it through scripts/motion-check.sh.
//
// Per page and viewport (1440x900 and 390x844) it reports:
//   - JavaScript exceptions and console errors;
//   - the deep field (canvas.ambient-deep from assets/ambient.js): drawn and
//     changing between two samples;
//   - the hero motif (canvas.ambient): present where the page has a hero,
//     drawn and changing;
//   - every simulated replay (.sim-clock): its clock advances while in view;
//   - SMIL drawings: not paused and their clocks advancing;
//   - every tabbed picture (.fl-tabs whose buttons name aria-controls): each
//     tab presses, lights its part of the drawing and shows its caption;
//   - scroll reveal (.rv): each block, scrolled into view one by one, gets
//     its "in" class.
//
// NOT a gate, like svg-fit: it needs Chrome and a served tree, and a deploy
// must not depend on either. It exits 1 when it finds something, 0 when not.
//
// Written 2026-11-27 after a review that found the built-in browser pane is a
// background page (IntersectionObserver evidence there is worthless) and that
// a static headless screenshot shows every .rv block hidden. Background timer
// throttling is switched off here, which is what makes the timing honest.
import fs from "node:fs"; import os from "node:os"; import path from "node:path"; import { spawn } from "node:child_process";
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const CANVAS_HOOK = "";
class Chrome {
  static async launch() {
    const bin = process.env.CHROME || "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
    if (!fs.existsSync(bin)) throw new Error(`Chrome not found at ${bin}; set CHROME`);
    const dir = fs.mkdtempSync(path.join(os.tmpdir(), "svgfit-chrome-"));
    const proc = spawn(bin, [
      "--headless=new", "--remote-debugging-port=0", `--user-data-dir=${dir}`,
      "--no-first-run", "--no-default-browser-check", "--disable-extensions", "--hide-scrollbars",
      "--mute-audio", "--disable-background-timer-throttling", "--disable-renderer-backgrounding",
      "--disable-backgrounding-occluded-windows", "--disable-features=Translate,MediaRouter",
      "--force-color-profile=srgb", "about:blank",
    ], { stdio: ["ignore", "ignore", "ignore"] });
    const portFile = path.join(dir, "DevToolsActivePort");
    for (let i = 0; i < 300 && !fs.existsSync(portFile); i++) await sleep(50);
    if (!fs.existsSync(portFile)) { proc.kill("SIGKILL"); throw new Error("Chrome did not open a DevTools port"); }
    let txt = "";
    for (let i = 0; i < 40; i++) { txt = fs.readFileSync(portFile, "utf8"); if (txt.split("\n").length >= 2 && txt.split("\n")[1]) break; await sleep(50); }
    const [port, wsPath] = txt.trim().split("\n");
    const c = new Chrome(proc, dir);
    await c.connect(`ws://127.0.0.1:${port}${wsPath}`);
    return c;
  }
  constructor(proc, dir) { this.proc = proc; this.dir = dir; this.id = 0; this.pending = new Map(); this.handlers = new Map(); }
  connect(url) {
    return new Promise((resolve, reject) => {
      const ws = new WebSocket(url);
      this.ws = ws;
      ws.onopen = () => resolve();
      ws.onerror = (e) => reject(new Error("websocket error " + (e.message || "")));
      ws.onclose = () => { for (const [, p] of this.pending) p.reject(new Error("browser connection closed")); this.pending.clear(); this.closed = true; };
      ws.onmessage = (ev) => {
        const msg = JSON.parse(typeof ev.data === "string" ? ev.data : Buffer.from(ev.data).toString());
        if (msg.id) {
          const p = this.pending.get(msg.id); if (!p) return; this.pending.delete(msg.id);
          if (msg.error) p.reject(new Error(`${p.method}: ${msg.error.message}`)); else p.resolve(msg.result);
        } else {
          const hs = this.handlers.get(`${msg.sessionId || ""}|${msg.method}`);
          if (hs) for (const h of hs) h(msg.params);
        }
      };
    });
  }
  send(method, params = {}, sessionId, timeout = 60000) {
    if (this.closed) return Promise.reject(new Error("browser connection closed"));
    const id = ++this.id;
    const msg = { id, method, params }; if (sessionId) msg.sessionId = sessionId;
    return new Promise((resolve, reject) => {
      const t = setTimeout(() => { this.pending.delete(id); reject(new Error(`${method}: timed out`)); }, timeout);
      this.pending.set(id, { method, resolve: (v) => { clearTimeout(t); resolve(v); }, reject: (e) => { clearTimeout(t); reject(e); } });
      this.ws.send(JSON.stringify(msg));
    });
  }
  on(sessionId, method, fn) { const k = `${sessionId || ""}|${method}`; if (!this.handlers.has(k)) this.handlers.set(k, []); this.handlers.get(k).push(fn); }
  async newPage() {
    const { targetId } = await this.send("Target.createTarget", { url: "about:blank" });
    const { sessionId } = await this.send("Target.attachToTarget", { targetId, flatten: true });
    return new Page(this, sessionId, targetId);
  }
  async close() { try { await this.send("Browser.close", {}, undefined, 3000); } catch {} try { this.proc.kill("SIGKILL"); } catch {} try { fs.rmSync(this.dir, { recursive: true, force: true }); } catch {} }
}

class Page {
  constructor(b, sid, tid) { this.b = b; this.sid = sid; this.tid = tid; this.phase = "load"; this.errors = []; }
  send(m, p, t) { return this.b.send(m, p, this.sid, t); }
  on(m, fn) { this.b.on(this.sid, m, fn); }
  async init() {
    await this.send("Page.enable"); await this.send("Runtime.enable"); await this.send("Log.enable");
    await this.send("Page.addScriptToEvaluateOnNewDocument", { source: CANVAS_HOOK });
    try { await this.send("Emulation.setFocusEmulationEnabled", { enabled: true }); } catch {}
    this.on("Runtime.consoleAPICalled", (p) => {
      if (p.type !== "error" && p.type !== "assert") return;
      const text = (p.args || []).map((x) => x.value !== undefined ? String(x.value) : (x.description || x.type)).join(" ");
      this.errors.push({ phase: this.phase, source: "console." + p.type, text: text.slice(0, 400) });
    });
    this.on("Runtime.exceptionThrown", (p) => {
      const d = p.exceptionDetails || {};
      const text = (d.exception && d.exception.description) || d.text || "exception";
      this.errors.push({ phase: this.phase, source: "exception", text: String(text).split("\n").slice(0, 3).join(" | ").slice(0, 400), url: d.url, line: d.lineNumber });
    });
    this.on("Log.entryAdded", (p) => {
      const e = p.entry || {}; if (e.level !== "error") return;
      this.errors.push({ phase: this.phase, source: "log." + e.source, text: String(e.text).slice(0, 400), url: e.url });
    });
  }
  async eval(expr, timeout = 60000) {
    const r = await this.send("Runtime.evaluate", { expression: expr, returnByValue: true, awaitPromise: true }, timeout);
    if (r.exceptionDetails) throw new Error("in-page: " + ((r.exceptionDetails.exception && r.exceptionDetails.exception.description) || r.exceptionDetails.text));
    return r.result.value;
  }
  async call(fn, arg, timeout) { return this.eval(`(${fn.toString()})(${JSON.stringify(arg === undefined ? null : arg)})`, timeout); }
  async goto(url, timeout = 30000) {
    const loaded = new Promise((resolve) => { this._onload = resolve; });
    if (!this._wired) { this._wired = true; this.on("Page.loadEventFired", () => { if (this._onload) { const f = this._onload; this._onload = null; f(); } }); }
    const r = await this.send("Page.navigate", { url });
    if (r.errorText) throw new Error(`navigate ${url}: ${r.errorText}`);
    await Promise.race([loaded, sleep(timeout)]);
  }
  async viewport(vp, reduced) {
    const mobile = vp.w < 768;
    await this.send("Emulation.setDeviceMetricsOverride", { width: vp.w, height: vp.h, deviceScaleFactor: mobile ? 2 : 1, mobile });
    await this.send("Emulation.setEmulatedMedia", { features: [{ name: "prefers-reduced-motion", value: reduced ? "reduce" : "no-preference" }] });
  }
  async shot(clip, beyond = false) {
    const r = await this.send("Page.captureScreenshot", { format: "png", clip: { ...clip, scale: 1 }, captureBeyondViewport: beyond, fromSurface: true }, 60000);
    return Buffer.from(r.data, "base64");
  }
}

const inPage = async () => {
  const wait = (ms) => new Promise((z) => setTimeout(z, ms));
  const hash = (c) => { try { const d = c.toDataURL(); let h = 0; for (let i = 0; i < d.length; i += 7) h = (h * 31 + d.charCodeAt(i)) | 0; return h + ":" + d.length; } catch (e) { return "ERR"; } };
  const ink = (c) => { try { const x = c.getContext("2d"); if (!x || !c.width || !c.height) return 0; const d = x.getImageData(0, 0, c.width, c.height).data; let n = 0; for (let i = 3; i < d.length; i += 4 * 97) if (d[i] > 0) n++; return n; } catch (e) { return -1; } };
  const f = [];
  const deep = () => document.querySelector("canvas.ambient-deep"), motif = () => document.querySelector("canvas.ambient");
  const d0 = deep() && hash(deep()), m0 = motif() && hash(motif());
  if (!deep()) f.push("no deep field (assets/ambient.js not loaded?)");
  else if (ink(deep()) === 0) f.push("deep field draws nothing");
  const inStack = (window.STACK || []).some((r) => r.id === document.body.dataset.service); // invariant 14 is about STACK rooms; Sphere is not one
  if (document.querySelector(".svc-hero") && inStack && !motif()) f.push("hero has no motif");
  else if (motif() && ink(motif()) === 0) f.push("hero motif draws nothing");
  await wait(1200);
  if (deep() && hash(deep()) === d0) f.push("deep field does not move");
  if (motif() && hash(motif()) === m0) f.push("hero motif does not move");
  for (const clock of document.querySelectorAll(".sim-clock")) {
    clock.scrollIntoView({ block: "center" }); await wait(300);
    const a = clock.textContent; await wait(2200);
    if (clock.textContent === a) f.push("simulated replay clock stuck at " + a.trim());
  }
  const svgs = [...document.querySelectorAll("svg")].filter((s) => s.querySelector("animate,animateMotion,animateTransform"));
  const t0 = svgs.map((s) => s.getCurrentTime()); await wait(500);
  svgs.forEach((s, i) => { if (s.animationsPaused && s.animationsPaused()) f.push("SMIL paused in " + (s.id || "an svg")); else if (s.getCurrentTime() <= t0[i]) f.push("SMIL clock stuck in " + (s.id || "an svg")); });
  for (const grp of document.querySelectorAll(".fl-tabs")) {
    const btns = [...grp.querySelectorAll(".fl-tab[aria-controls]")]; if (!btns.length) continue;
    const svg = document.getElementById(btns[0].getAttribute("aria-controls"));
    for (const b of btns) {
      b.click(); await wait(80); const k = b.dataset.k;
      if (b.getAttribute("aria-pressed") !== "true") f.push(`tab ${k} does not press`);
      if (svg && svg.getAttribute("data-show") !== k) f.push(`tab ${k} does not switch #${svg.id}`);
      if (svg && !svg.querySelector(`[data-p~="${k}"]`)) f.push(`tab ${k} lights nothing in #${svg.id}`);
      const why = grp.parentElement.querySelector(`.fl-why[data-for="${k}"]`); if (why && why.hidden) f.push(`tab ${k} caption stays hidden`);
    }
    btns[0].click();
  }
  for (const el of document.querySelectorAll(".rv")) { if (el.classList.contains("in")) continue; el.scrollIntoView({ block: "center" }); await wait(250); }
  await wait(700);
  const hid = [...document.querySelectorAll(".rv")].filter((e) => !e.classList.contains("in"));
  if (hid.length) f.push(`${hid.length} reveal block(s) never shown, first: "${hid[0].textContent.trim().slice(0, 50)}"`);
  return f;
};
const args = process.argv.slice(2); const base = args.shift();
const pages = args.length ? args : null;
const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), "..");
const list = pages || ["index.html", "stack.html", "genaryx.html", ...fs.readdirSync(path.join(root, "services")).filter((n) => n.endsWith(".html")).map((n) => "services/" + n)];
const b = await Chrome.launch(); let bad = 0;
for (const vp of [{ w: 1440, h: 900 }, { w: 390, h: 844 }]) for (const p of list) {
  const pg = await b.newPage(); await pg.init(); await pg.viewport(vp, false);
  let f;
  try { await pg.goto(base + p); await sleep(2000); f = await pg.call(inPage, null, 180000); }
  catch (e) { f = ["could not run: " + e.message]; }
  f.push(...pg.errors.map((e) => `${e.source}: ${e.text}`));
  if (f.length) bad++;
  console.log(`${f.length ? "FIND" : "ok  "}  ${p} @${vp.w}` + f.map((x) => "\n        " + x).join(""));
  try { await b.send("Target.closeTarget", { targetId: pg.tid }); } catch {}
}
await b.close();
console.log(bad ? `\n${bad} page view(s) with findings.` : `\nOK: every page's motion runs at both widths.`);
process.exit(bad ? 1 : 0);

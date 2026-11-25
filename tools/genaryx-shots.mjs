// Re-shoots the Genaryx console frames on genaryx.html from the built demo.
//
// Serve the repository root (python3 -m http.server 8815 --bind 127.0.0.1),
// then, wherever Playwright is installed (forge: ~/render-env, under
// forge-heavy):
//
//   node tools/genaryx-shots.mjs <outdir>
//
// It signs into the demo, waits for the incident arc to settle, and writes one
// 1760x1138 PNG per tab plus the Agent 360 drawer, with the tab's text beside
// each so the captions can be written from what the frame shows. Convert to
// WebP (ffmpeg -c:v libwebp -quality 82) into assets/shots/enterprise/ and
// bump the ?v= on every frame in genaryx.html. See CLAUDE.md invariant 7.
import { chromium } from "playwright";
import fs from "node:fs";
const BASE = process.env.BASE || "http://127.0.0.1:8815/demo/";
const OUT = process.argv[2] || "gx";
fs.mkdirSync(OUT, { recursive: true });
const browser = await chromium.launch();
const ctx = await browser.newContext({ viewport: { width: 1760, height: 1138 }, deviceScaleFactor: 1, colorScheme: "dark" });
const page = await ctx.newPage();
const errs = [];
page.on("pageerror", (e) => errs.push(String(e)));
await page.goto(BASE, { waitUntil: "networkidle" });
await page.getByRole("button", { name: "Sign in" }).click();
await page.getByRole("button", { name: "Enter console" }).click();
await page.waitForTimeout(6000); // let the incident arc and live ticks settle
const nav = async (label) => {
  await page.locator(`button:has(span.flex-1:text-is("${label}"))`).first().click();
  await page.waitForTimeout(2500);
};
const shots = [
  ["overview", "Overview"], ["incidents", "Incidents"], ["money", "Money"],
  ["statistics", "Statistics"], ["policy", "Policy"], ["identity", "Identity"],
  ["graph", "Graph"], ["bus", "Bus Explorer"], ["egress", "Web Egress"],
  ["quality", "Quality"], ["copilot", "Copilot"], ["memory", "Memory"],
  ["posture", "Posture"], ["notifications", "Notifications"], ["keys", "Keys"],
  ["record", "Record"], ["remote", "Remote"],
];
for (const [name, label] of shots) {
  await nav(label);
  if (name === "record") {
    await page.getByRole("button", { name: "Verify now" }).click();
    await page.waitForTimeout(3000);
  }
  await page.mouse.move(5, 1130);
  await page.screenshot({ path: `${OUT}/gx-${name}.png` });
  fs.writeFileSync(`${OUT}/gx-${name}.txt`, await page.locator("body").innerText());
  console.log("saved", name);
}
// Agent 360: the drawer over Overview, opened from the watch dock.
await nav("Overview");
await page.locator("button[title^='Open '][title*='rca-copilot']").first().click({ timeout: 8000 });
await page.waitForTimeout(2500);
await page.mouse.move(5, 1130);
await page.screenshot({ path: `${OUT}/gx-agent360.png` });
fs.writeFileSync(`${OUT}/gx-agent360.txt`, await page.locator("body").innerText());
console.log("saved agent360");
// The agent card behind "Agent card", to see #162's Manage section.
const card = page.getByRole("button", { name: /Agent card/ });
if (await card.count()) {
  await card.first().click();
  await page.waitForTimeout(2500);
  await page.screenshot({ path: `${OUT}/gx-agentcard.png` });
  console.log("saved agentcard");
}
console.log("pageerrors", errs.length, errs.slice(0, 3));
await browser.close();

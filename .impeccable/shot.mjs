// Usage: node .impeccable/shot.mjs <url> <out.png> <width> [height] [--full] [--mobile]
import { spawn } from "node:child_process";
import { writeFileSync, mkdtempSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const [url, out, w = "1440", h = "900", ...flags] = process.argv.slice(2);
const full = flags.includes("--full") || h === "--full";
const mobile = flags.includes("--mobile");
const width = Number(w);
const height = h === "--full" ? 900 : Number(h);
const port = 9300 + Math.floor(Math.random() * 500);
const profile = mkdtempSync(join(tmpdir(), "shot-"));
const chrome = spawn("/usr/bin/chromium", [
  "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run",
  `--remote-debugging-port=${port}`, `--user-data-dir=${profile}`, "about:blank",
], { stdio: "ignore" });

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
let target;
for (let i = 0; i < 50 && !target; i++) {
  await sleep(200);
  try {
    const list = await (await fetch(`http://127.0.0.1:${port}/json`)).json();
    target = list.find((t) => t.type === "page");
  } catch {}
}
const ws = new WebSocket(target.webSocketDebuggerUrl);
await new Promise((r) => ws.addEventListener("open", r));
let id = 0;
const pending = new Map();
ws.addEventListener("message", (e) => {
  const m = JSON.parse(e.data);
  if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); }
});
const send = (method, params = {}) => new Promise((r) => { const i = ++id; pending.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });

await send("Page.enable");
await send("Emulation.setDeviceMetricsOverride", { width, height, deviceScaleFactor: 1, mobile });
await send("Page.navigate", { url });
await sleep(2500);
if (full) {
  await send("Runtime.evaluate", { expression: "(async()=>{for(let y=0;y<document.body.scrollHeight;y+=600){scrollTo(0,y);await new Promise(r=>setTimeout(r,60))}scrollTo(0,0)})()", awaitPromise: true });
  await sleep(1200);
}
if (process.env.PRE) { await send("Runtime.evaluate", { expression: process.env.PRE }); await sleep(600); }
const clip = full
  ? await send("Page.getLayoutMetrics").then((m) => ({ x: 0, y: 0, width, height: Math.ceil(m.result.cssContentSize.height), scale: 1 }))
  : { x: 0, y: 0, width, height, scale: 1 };
const shot = await send("Page.captureScreenshot", { format: "png", clip, captureBeyondViewport: full });
writeFileSync(out, Buffer.from(shot.result.data, "base64"));
const expr = process.env.EVAL || "JSON.stringify({sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth})";
const info = await send("Runtime.evaluate", { expression: expr, returnByValue: true });
console.log(out, clip.height, info.result.result.value);
ws.close();
chrome.kill();

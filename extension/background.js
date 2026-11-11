// Knowledge Clipper: sends pages/selections/links to the local server (./web) at 127.0.0.1:8765.
const BASE = "http://127.0.0.1:8765";
const YT = /(?:youtube\.com|youtu\.be)\//;

const getCfg = () => chrome.storage.local.get({ key: "", digest: true, pending: [] });

function badge(text, color = "#2563eb") {
  chrome.action.setBadgeText({ text });
  chrome.action.setBadgeBackgroundColor({ color });
}

function notify(title, message) {
  chrome.notifications.create({
    type: "basic", title, message,
    iconUrl: "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==",
  });
}

async function api(path, init = {}, key = "") {
  let r;
  try {
    r = await fetch(BASE + path, { ...init, headers: { "Content-Type": "application/json", "X-KB-Clip-Key": key, ...(init.headers || {}) } });
  } catch {
    throw new Error("Server not running. Start it with ./web");
  }
  const data = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error(r.status === 403 ? "Wrong clip key. Paste the one from data/clipper.key" : (data.detail || data.error || "HTTP " + r.status));
  return data;
}

// Send one clip; track the job so we can tell you when it is saved / digested.
async function send(payload) {
  const { key, digest, pending } = await getCfg();
  if (!key) throw new Error("Clip key not set. Open the extension popup and paste it.");
  const { job } = await api("/api/clip", { method: "POST", body: JSON.stringify({ ...payload, digest }) }, key);
  pending.push({ id: job, title: payload.title || payload.url, digest });
  await chrome.storage.local.set({ pending });
  badge("…");
  chrome.alarms.create("poll", { periodInMinutes: 0.5, delayInMinutes: 0.1 });
  setTimeout(poll, 4000);
  return job;
}

async function poll() {
  const { pending } = await getCfg();
  if (!pending.length) { chrome.alarms.clear("poll"); return; }
  const still = [];
  for (const p of pending) {
    let j;
    try { j = await api("/api/jobs/" + p.id); } catch { still.push(p); continue; }
    if (j.status === "running") { still.push(p); continue; }
    const short = (p.title || "").slice(0, 60);
    if (j.status === "failed") { notify("Clip failed", `${short}\n${(j.log.filter(l => l.startsWith("ERROR")).pop() || "").slice(0, 150)}`); badge("!", "#dc2626"); }
    else if (j.result && j.result.duplicate) notify("Already saved", short);
    else if (j.result && j.result.batch) notify("Digested, ready to review", `${short}\nBatch ${j.result.batch}: open the web app > Review`);
    else notify("Saved to raw/", short);
  }
  await chrome.storage.local.set({ pending: still });
  if (!still.length) { chrome.alarms.clear("poll"); setTimeout(() => badge(""), 4000); }
}

chrome.alarms.onAlarm.addListener(a => { if (a.name === "poll") poll(); });
chrome.runtime.onStartup.addListener(poll);

// What the browser sees in the tab: works for pages behind a login too.
async function grab(tabId) {
  const [{ result }] = await chrome.scripting.executeScript({
    target: { tabId },
    func: () => ({ url: location.href, title: document.title, selection: String(getSelection() || "").trim(), text: (document.body ? document.body.innerText : "").slice(0, 400000) }),
  });
  return result;
}

async function clipTab(tab, mode = "auto") {
  const g = await grab(tab.id);
  if (!/^https?:/.test(g.url)) throw new Error("This page cannot be clipped.");
  const useSel = mode === "selection" || (mode === "auto" && g.selection);
  if (mode === "selection" && !g.selection) throw new Error("Nothing is selected.");
  return send({ url: g.url, title: g.title, selection: useSel ? g.selection : "", text: YT.test(g.url) ? "" : g.text });
}

chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({ id: "clip-selection", title: "Clip selection to knowledge system", contexts: ["selection"] });
  chrome.contextMenus.create({ id: "clip-link", title: "Clip this link to knowledge system", contexts: ["link"] });
  chrome.contextMenus.create({ id: "clip-page", title: "Clip this page to knowledge system", contexts: ["page", "video", "frame"] });
});

async function run(fn) {
  try { await fn(); } catch (e) { notify("Clip failed", e.message); badge("!", "#dc2626"); }
}

chrome.contextMenus.onClicked.addListener((info, tab) => run(async () => {
  if (info.menuItemId === "clip-link") await send({ url: info.linkUrl, title: info.linkText || "" });
  else await clipTab(tab, info.menuItemId === "clip-selection" ? "selection" : "page");
}));

chrome.commands.onCommand.addListener((cmd, tab) => { if (cmd === "clip-page") run(() => clipTab(tab, "auto")); });

// Popup requests
chrome.runtime.onMessage.addListener((msg, _s, reply) => {
  if (msg.type === "clip") {
    chrome.tabs.query({ active: true, currentWindow: true }).then(([tab]) => clipTab(tab, msg.mode))
      .then(() => reply({ ok: true }), e => reply({ ok: false, error: e.message }));
    return true;
  }
  if (msg.type === "ping") {
    getCfg().then(({ key }) => api("/api/state").then(() => reply({ ok: true, hasKey: !!key }), e => reply({ ok: false, error: e.message })));
    return true;
  }
});

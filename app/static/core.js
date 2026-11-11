"use strict";
// ---------------------------------------------------------------- helpers
let TOKEN = document.querySelector('meta[name="kb-token"]').content;
const $ = (s, el = document) => el.querySelector(s);
const $$ = (s, el = document) => [...el.querySelectorAll(s)];
const app = $("#app");
const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const sleep = ms => new Promise(r => setTimeout(r, ms));
const store = { get: (k, d) => { try { return localStorage.getItem(k) ?? d; } catch { return d; } }, set: (k, v) => { try { localStorage.setItem(k, v); } catch {} } };

// theme: auto (system) / light / dark
const sysDark = matchMedia("(prefers-color-scheme: dark)");
const isDark = () => (document.documentElement.dataset.theme || (sysDark.matches ? "dark" : "light")) === "dark";
function applyTheme() { const t = store.get("kb-theme", ""); if (t) document.documentElement.dataset.theme = t; else delete document.documentElement.dataset.theme; mermaid.initialize({ startOnLoad: false, securityLevel: "strict", theme: isDark() ? "dark" : "default" }); }
applyTheme();
marked.use({ renderer: { html: t => esc(typeof t === "string" ? t : t.text) } }); // never render raw HTML from sources

// The security token changes every time the app restarts. If this tab was opened before a restart, its token
// is stale and the server answers 403; fetch a fresh token from the page and retry once instead of failing.
async function refreshToken() {
  try { const t = await (await fetch("/", { cache: "no-store" })).text(); const m = t.match(/name="kb-token" content="([^"]+)"/); if (m) { TOKEN = m[1]; return true; } } catch {}
  return false;
}
async function kbFetch(path, o) {
  const send = () => fetch(path, o.method && o.method !== "GET" ? { ...o, headers: { ...o.headers, "X-KB-Token": TOKEN } } : o);
  let r = await send();
  if (r.status === 403 && o.method && o.method !== "GET" && await refreshToken()) r = await send();
  return r;
}
async function errorText(r) {
  let m = r.statusText;
  try { const d = await r.json(); m = d.detail || d.error || m; } catch {}
  return r.status === 403 ? "Permission refused. If you just restarted the app, reload this page (Ctrl+Shift+R)." : m;
}
async function api(path, opts = {}) {
  const o = { headers: {}, ...opts };
  if (o.json !== undefined) { o.body = JSON.stringify(o.json); o.headers["Content-Type"] = "application/json"; }
  const r = await kbFetch(path, o);
  if (!r.ok) throw new Error(await errorText(r));
  return r.json();
}
const post = (p, json = {}) => api(p, { method: "POST", json });
function toast(msg, ms = 3500) { const t = $("#toast"); t.textContent = msg; t.hidden = false; clearTimeout(t._t); t._t = setTimeout(() => t.hidden = true, ms); }
const busy = async (btn, fn) => { btn.disabled = true; const old = btn.textContent; btn.textContent = "Working…"; try { return await fn(); } catch (e) { toast("Error: " + e.message, 6000); } finally { btn.disabled = false; btn.textContent = old; } };
const chip = (t, c = "") => `<span class="chip ${c}">${esc(t)}</span>`;
const confChip = c => chip(c + " confidence", c === "high" ? "ok" : c === "low" ? "warn" : "");
const statusChip = s => chip(s, s === "reviewed" ? "ok" : s === "stub" ? "warn" : "");
const skeleton = (n = 3) => `<div class="skel-wrap">${Array.from({ length: n }, () => `<div class="skel"></div>`).join("")}</div>`;

// progress ring (animated via CSS transition)
function ring(pct, color = "var(--accent)", size = 64, label = "", stroke = 7) {
  const r = (size - stroke) / 2, c = 2 * Math.PI * r, off = c * (1 - Math.max(0, Math.min(1, pct)));
  return `<svg class="ring" width="${size}" height="${size}" viewBox="0 0 ${size} ${size}"><circle cx="${size / 2}" cy="${size / 2}" r="${r}" fill="none" stroke="var(--line)" stroke-width="${stroke}"/><circle class="ring-fg" cx="${size / 2}" cy="${size / 2}" r="${r}" fill="none" stroke="${color}" stroke-width="${stroke}" stroke-linecap="round" stroke-dasharray="${c}" stroke-dashoffset="${c}" data-off="${off}" transform="rotate(-90 ${size / 2} ${size / 2})"/><text x="50%" y="50%" text-anchor="middle" dominant-baseline="central" font-size="${size / 4.2}" font-weight="700" fill="var(--ink)">${label || Math.round(pct * 100) + "%"}</text></svg>`;
}
const animateRings = (el = app) => requestAnimationFrame(() => requestAnimationFrame(() => $$(".ring-fg", el).forEach(c => c.setAttribute("stroke-dashoffset", c.dataset.off))));

// ---------------------------------------------------------------- index + subjects
let INDEX = [], SLUG = {}, SUBJECTS = [], SUBJECT = store.get("kb-subject", "");
async function loadIndex() { INDEX = await api("/api/index"); SLUG = Object.fromEntries(INDEX.map(p => [p.slug, p])); }
async function loadSubjects() { SUBJECTS = await api("/api/subjects"); drawSubjectSelect(); applySubjectColor(); }
const subj = k => SUBJECTS.find(s => s.key === k);
const inSubject = p => !SUBJECT || (p.domains || []).includes(SUBJECT);
const subjectChip = k => { const s = subj(k); return s ? `<span class="chip" style="color:${s.color};border:1px solid ${s.color}33">${esc(s.icon)} ${esc(s.name)}</span>` : chip(k); };
function applySubjectColor() { const s = subj(SUBJECT); document.documentElement.style.setProperty("--subject", s ? s.color : "var(--accent)"); }
function drawSubjectSelect() {
  const sel = $("#subject");
  sel.innerHTML = `<option value="">◎ All subjects</option>` + SUBJECTS.map(s => `<option value="${esc(s.key)}">${esc(s.icon)} ${esc(s.name)}</option>`).join("") + `<option value="__new">＋ New subject…</option>`;
  sel.value = SUBJECTS.some(s => s.key === SUBJECT) ? SUBJECT : "";
}
$("#subject").addEventListener("change", e => {
  if (e.target.value === "__new") { e.target.value = SUBJECT; openSubjectDialog(); return; }
  SUBJECT = e.target.value; store.set("kb-subject", SUBJECT); applySubjectColor(); route();
});
$("#theme").addEventListener("click", () => { const cur = isDark() ? "dark" : "light"; store.set("kb-theme", cur === "dark" ? "light" : "dark"); applyTheme(); route(); });

// ---------------------------------------------------------------- markdown
function md(text) {
  text = text.replace(/\[\[([^\]|#]+)(?:[#|][^\]]*)?\]\]/g, (m, s) => SLUG[s.trim()] ? `[${SLUG[s.trim()].title}](#/page/${s.trim()})` : esc(s));
  return marked.parse(text, { breaks: false }).replace(/\[(fact|inference|speculation)\]/g, (m, t) => `<span class="tag ${t}">${t}</span>`);
}
async function renderMermaid(el) {
  for (const [i, b] of [...el.querySelectorAll("pre code.language-mermaid")].entries()) {
    try { const { svg } = await mermaid.render("m" + Date.now() + i, b.textContent); const d = document.createElement("div"); d.className = "mermaid-out"; d.innerHTML = svg; b.parentElement.replaceWith(d); } catch { /* leave code block */ }
  }
}

// ---------------------------------------------------------------- dialogs
function openDialog(html, onMount) {
  const d = document.createElement("div"); d.className = "overlay"; d.innerHTML = `<div class="dialog">${html}</div>`;
  document.body.appendChild(d);
  const close = () => d.remove();
  d.addEventListener("mousedown", e => { if (e.target === d) close(); });
  d.addEventListener("keydown", e => { if (e.key === "Escape") close(); });
  onMount && onMount(d, close);
  return close;
}
function openSubjectDialog() {
  const icons = ["📚", "🧪", "🏛", "💼", "🎨", "⚖️", "🌍", "🧬", "💰", "🎵", "🗣", "🧮"];
  openDialog(`<h2 style="margin-top:0">New subject</h2><p class="muted small">Subjects are how this knowledge base grows beyond AI. Anything you add can belong to one, and each gets its own learning map, progress and colour.</p>
    <label class="small">Name<input id="ns-name" type="text" placeholder="e.g. World History"></label>
    <label class="small">Short description<input id="ns-desc" type="text" placeholder="What is this subject about?"></label>
    <div class="row" style="margin-top:10px"><div style="flex:1"><div class="small">Icon</div><div class="row" id="ns-icons">${icons.map(i => `<button class="ghost ico" data-i="${i}">${i}</button>`).join("")}</div></div>
    <label class="small">Colour<br><input id="ns-color" type="color" value="#7c93ff" style="width:60px;height:36px;padding:2px"></label></div>
    <div class="row" style="margin-top:16px;justify-content:flex-end"><button class="ghost" id="ns-cancel">Cancel</button><button id="ns-save">Create subject</button></div>`, (d, close) => {
    let icon = icons[0];
    $$(".ico", d).forEach(b => b.onclick = () => { icon = b.dataset.i; $$(".ico", d).forEach(x => x.classList.toggle("sel", x === b)); });
    $(".ico", d).classList.add("sel");
    $("#ns-cancel", d).onclick = close; $("#ns-name", d).focus();
    $("#ns-save", d).onclick = ev => busy(ev.target, async () => {
      const name = $("#ns-name", d).value.trim(); const key = name.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "").slice(0, 30);
      const r = await post("/api/subjects", { key, name, description: $("#ns-desc", d).value, color: $("#ns-color", d).value, icon });
      await loadSubjects(); SUBJECT = r.subject.key; store.set("kb-subject", SUBJECT); drawSubjectSelect(); applySubjectColor(); close(); toast(`Subject "${name}" created. Add your first source.`); location.hash = "#/subject/" + SUBJECT; route();
    });
  });
}

// ---------------------------------------------------------------- jobs
async function watchJob(id, onLog) {
  for (;;) {
    const d = await api("/api/jobs/" + id);
    onLog && onLog(d.log, d);
    if (d.status !== "running") return d;
    await sleep(1500);
  }
}
const lastLine = log => (log[log.length - 1] || "starting…").replace(/^(claude|tool): /, "").slice(0, 110);

// ---------------------------------------------------------------- router
const routes = {};
let timers = [];
const every = (fn, ms) => { timers.push(setInterval(fn, ms)); };
const cleanups = [];
const onLeave = fn => cleanups.push(fn);
function stopTimers() { timers.forEach(clearInterval); timers = []; while (cleanups.length) { try { cleanups.pop()(); } catch {} } }
async function route() {
  const h = location.hash.slice(1) || "/";
  const [path, qs] = h.split("?");
  const parts = path.split("/").filter(Boolean);
  const name = parts[0] || "home";
  const navOf = { page: "library", source: "library", subject: "home", play: "learn", build: "learn", mymap: "mymaps" };
  $$("nav a").forEach(a => a.classList.toggle("on", a.dataset.r === (navOf[name] || name)));
  app.className = name === "mymap" ? "wide" : "";
  stopTimers();
  window.scrollTo(0, 0);
  app.innerHTML = skeleton();
  try { await (routes[name] || routes.home)(parts.slice(1), new URLSearchParams(qs || "")); app.classList.add("fade-in"); animateRings(); }
  catch (e) { app.innerHTML = `<div class="card">Something went wrong: ${esc(e.message)}</div>`; }
  refreshBadges();
}
async function refreshBadges() {
  try { const s = await api("/api/state"); $("#b-add").textContent = s.undigested || ""; $("#b-review").textContent = s.batches.length || ""; $("#b-study").textContent = s.due_cards || ""; } catch {}
}
addEventListener("hashchange", route);

// ---------------------------------------------------------------- header search
let st;
$("#gsearch").addEventListener("input", e => {
  clearTimeout(st); const q = e.target.value.trim(); const box = $("#search-results");
  if (q.length < 2) { box.hidden = true; return; }
  st = setTimeout(async () => {
    const r = await api("/api/search?q=" + encodeURIComponent(q.replace(/[^\w\s-]/g, " ") + "*"));
    box.innerHTML = r.length ? r.map(x => `<a href="#/page/${esc((INDEX.find(p => p.id === x.id) || {}).slug || x.id)}">${chip(x.type)} <b>${esc(x.title)}</b><br><span class="muted small">${esc(x.snippet)}</span></a>`).join("") : `<a>No results</a>`;
    box.hidden = false;
  }, 250);
});
document.addEventListener("click", e => { if (!e.target.closest("#search-results") && e.target.id !== "gsearch") $("#search-results").hidden = true; if (e.target.closest("#search-results a")) { $("#search-results").hidden = true; $("#gsearch").value = ""; } });

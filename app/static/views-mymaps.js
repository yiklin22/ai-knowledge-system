"use strict";
// ================================================================ MY MAPS: build your own knowledge maps
const NODE_COLORS = { blue: "--accent", green: "--ok", orange: "--warn", red: "--bad", violet: "--violet", teal: "--info", gray: "--muted" };
const TYPE_COLOR = { concept: "--accent", claim: "--violet", source: "--muted", question: "--warn", entity: "--info", map: "--ok", insight: "--ok", project: "--warn" };
const LINK_SUGGEST = ["leads to", "is part of", "requires", "is an example of", "contradicts", "causes", "supports", "is similar to"];
// a page can be linked in both directions: merge into one entry with several relations
const groupNb = list => { const m = new Map(); list.forEach(x => { if (!m.has(x.slug)) m.set(x.slug, { slug: x.slug, title: x.title, type: x.type, rels: [] }); const g = m.get(x.slug); if (!g.rels.some(r => r.dir === x.dir && r.rel === x.rel)) g.rels.push({ dir: x.dir, rel: x.rel }); }); return [...m.values()]; };
const uid = (p = "n") => p + Math.random().toString(36).slice(2, 8);

function thumbSvg(m) {
  if (!m.nodes.length) return `<div class="thumb empty">Empty map</div>`;
  const xs = m.nodes.map(n => n.x), ys = m.nodes.map(n => n.y), x0 = Math.min(...xs), y0 = Math.min(...ys), w = Math.max(1, Math.max(...xs) - x0), h = Math.max(1, Math.max(...ys) - y0);
  const k = Math.min(190 / w, 90 / h, 1), ox = (220 - w * k) / 2, oy = (120 - h * k) / 2, P = n => [ox + (n.x - x0) * k, oy + (n.y - y0) * k], by = Object.fromEntries(m.nodes.map(n => [n.id, n]));
  return `<svg class="thumb" viewBox="0 0 220 120">${m.edges.map(e => { const a = P(by[e.from]), b = P(by[e.to]); return `<line x1="${a[0]}" y1="${a[1]}" x2="${b[0]}" y2="${b[1]}" stroke="var(--muted)" stroke-width="1" opacity=".6"/>`; }).join("")}${m.nodes.map(n => { const p = P(n); return `<circle cx="${p[0]}" cy="${p[1]}" r="4.5" fill="var(--subject)"/>`; }).join("")}</svg>`;
}

// ---------------------------------------------------------------- list
routes.mymaps = async () => {
  await loadSubjects(); if (!INDEX.length) await loadIndex();
  const list = (await api("/api/mymaps")).filter(m => !SUBJECT || !m.subject || m.subject === SUBJECT);
  app.innerHTML = `<h1>My maps</h1><p class="muted">Build your own knowledge maps: drag in pages from your vault or your own ideas, draw labelled links between them, and keep one map per topic. Nothing here changes your vault.</p>
  <div class="subjects"><a class="subject-card add" href="#" id="newmap"><span style="font-size:30px">＋</span><b>New map</b><span class="muted small">Start blank, or from a concept in your vault</span></a>
  ${list.map(m => `<a class="subject-card" href="#/mymap/${esc(m.id)}">${thumbSvg(m)}<b>${esc(m.title)}</b><span class="muted small">${m.nodes.length} ideas · ${m.edges.length} links · ${esc(m.updated || "")}</span>${m.subject ? subjectChip(m.subject) : ""}</a>`).join("")}</div>
  ${list.length ? "" : `<div class="card onboard center" style="margin-top:14px"><div style="font-size:38px">🧩</div><b>No maps yet.</b><p class="muted">Try mapping a hard topic: start from a concept, pull in what it connects to, then add your own notes and links.</p></div>`}`;
  $("#newmap").onclick = e => { e.preventDefault(); newMapDialog(); };
};

function newMapDialog() {
  openDialog(`<h2 style="margin-top:0">New map</h2><label class="small">Title<input id="nm-title" type="text" placeholder="e.g. How attention fits together"></label>
    <label class="small">Subject (optional)<select id="nm-subj"><option value="">None</option>${SUBJECTS.map(s => `<option value="${esc(s.key)}" ${s.key === SUBJECT ? "selected" : ""}>${esc(s.icon)} ${esc(s.name)}</option>`).join("")}</select></label>
    <label class="small">Start from a vault page (optional)<input id="nm-q" type="text" placeholder="Search your vault…" autocomplete="off"></label><div id="nm-res" class="list small" style="max-height:170px;overflow:auto"></div>
    <div class="row" style="margin-top:14px;justify-content:flex-end"><button class="ghost" id="nm-cancel">Cancel</button><button id="nm-go">Create map</button></div>`, (d, close) => {
    let pick = null;
    $("#nm-title", d).focus();
    $("#nm-cancel", d).onclick = close;
    $("#nm-q", d).oninput = e => { const q = e.target.value.toLowerCase(); $("#nm-res", d).innerHTML = q ? INDEX.filter(p => p.title.toLowerCase().includes(q)).slice(0, 8).map(p => `<a class="item" href="#" data-s="${esc(p.slug)}">${chip(p.type)}<b>${esc(p.title)}</b></a>`).join("") : ""; $$("#nm-res a", d).forEach(a => a.onclick = ev => { ev.preventDefault(); pick = a.dataset.s; $("#nm-q", d).value = SLUG[pick].title; $("#nm-res", d).innerHTML = ""; if (!$("#nm-title", d).value) $("#nm-title", d).value = SLUG[pick].title; }); };
    $("#nm-go", d).onclick = ev => busy(ev.target, async () => {
      const title = $("#nm-title", d).value.trim() || (pick && SLUG[pick].title); if (!title) { toast("Give the map a title."); return; }
      const nodes = [], edges = [];
      if (pick) {
        const hub = { id: uid(), label: SLUG[pick].title, note: "", color: "auto", x: 0, y: 0, page: pick }; nodes.push(hub);
        const nb = groupNb(await api("/api/neighbors/" + pick)).slice(0, 8);
        nb.forEach((g, k) => { const a = k / Math.max(1, nb.length) * 2 * Math.PI - Math.PI / 2, nn = { id: uid(), label: g.title, note: "", color: "auto", x: Math.cos(a) * 260, y: Math.sin(a) * 200, page: g.slug }; nodes.push(nn); g.rels.forEach(r => edges.push(r.dir === "out" ? { id: uid("e"), from: hub.id, to: nn.id, label: r.rel } : { id: uid("e"), from: nn.id, to: hub.id, label: r.rel })); });
      }
      const r = await post("/api/mymaps", { title, subject: $("#nm-subj", d).value, nodes, edges }); close(); location.hash = "#/mymap/" + r.id;
    });
  });
}

// ---------------------------------------------------------------- editor
routes.mymap = async ([id]) => {
  if (!INDEX.length) await loadIndex();
  const doc = await api("/api/mymaps/" + encodeURIComponent(id));
  const view = { x: 0, y: 0, k: 1 }; let sel = null, linkFrom = null, linkMode = false, undo = [], saveTimer = null, saving = false, drag = null, pan = null, moved = false, lastBg = { t: 0, x: 0, y: 0 };
  const byId = () => Object.fromEntries(doc.nodes.map(n => [n.id, n]));
  const snapshot = () => { undo.push(JSON.stringify({ nodes: doc.nodes, edges: doc.edges, title: doc.title })); if (undo.length > 40) undo.shift(); };
  const colorOf = n => cssv(n.color !== "auto" ? NODE_COLORS[n.color] : n.page && SLUG[n.page] ? TYPE_COLOR[SLUG[n.page].type] || "--accent" : "--muted");
  const wrap = t => { const words = t.split(/\s+/), lines = []; let cur = ""; for (const w of words) { if ((cur + " " + w).trim().length > 21 && cur) { lines.push(cur); cur = w; } else cur = (cur + " " + w).trim(); } if (cur) lines.push(cur); return lines.slice(0, 3).map((l, i, a) => i === 2 && words.join(" ").length > lines.join(" ").length ? l.slice(0, 19) + "…" : l); };
  const size = n => { const L = wrap(n.label); n._L = L; n.w = Math.max(96, Math.min(196, Math.max(...L.map(l => l.length)) * 7.6 + 30)); n.h = 18 + L.length * 17; };
  const edgeEnd = (n, ang) => { const hw = n.w / 2 + 2, hh = n.h / 2 + 2, c = Math.cos(ang), s = Math.sin(ang); const t = Math.min(Math.abs(c) > 1e-6 ? hw / Math.abs(c) : 1e9, Math.abs(s) > 1e-6 ? hh / Math.abs(s) : 1e9); return { x: n.x + c * t, y: n.y + s * t }; };

  app.innerHTML = `<div class="me-bar">
    <a class="btn ghost" href="#/mymaps" title="All maps">←</a><input id="me-title" type="text" value="${esc(doc.title)}" title="Map title">
    <button class="ghost" id="me-vault" title="Add a page from your vault">＋ Vault page</button><button class="ghost" id="me-note" title="Add your own idea (or double-click the canvas)">＋ Idea</button>
    <button class="ghost" id="me-link" title="Draw a link: click one idea, then another (L)">🔗 Link</button><button class="ghost" id="me-tidy" title="Auto-arrange">Tidy</button><button class="ghost" id="me-fit">Fit</button>
    <button class="ghost" id="me-zo">−</button><button class="ghost" id="me-zi">＋</button><button class="ghost" id="me-undo" title="Undo (Ctrl+Z)">↶</button><button class="ghost" id="me-svg">Export SVG</button>
    <span id="me-saved" class="small muted">Saved</span></div>
    <div class="me-wrap"><svg id="me" class="me-canvas"></svg><aside class="me-panel" id="me-panel"></aside></div>`;
  const svg = $("#me"), panel = $("#me-panel");
  const setSaved = t => $("#me-saved").textContent = t;
  const doSave = async () => { saving = true; setSaved("Saving…"); try { await post("/api/mymaps/" + id, { title: doc.title, subject: doc.subject, nodes: doc.nodes.map(({ _L, w, h, vx, vy, ...n }) => n), edges: doc.edges }); setSaved("Saved ✓"); } catch (e) { setSaved("Not saved: " + e.message); } saving = false; };
  const changed = (snap = true) => { if (snap) snapshot(); setSaved("Unsaved…"); clearTimeout(saveTimer); saveTimer = setTimeout(doSave, 600); draw(); };
  onLeave(() => { if (saveTimer) { clearTimeout(saveTimer); doSave(); } });

  const worldOf = e => { const r = svg.getBoundingClientRect(); return { x: (e.clientX - r.left - view.x) / view.k, y: (e.clientY - r.top - view.y) / view.k }; };
  function markup(forExport) {
    const nb = byId(); doc.nodes.forEach(size);
    const ink = cssv("--ink"), panelC = cssv("--panel"), muted = cssv("--muted"), line = cssv("--line");
    const edges = doc.edges.map(e => { const a = nb[e.from], b = nb[e.to]; if (!a || !b) return ""; const ang = Math.atan2(b.y - a.y, b.x - a.x), s = edgeEnd(a, ang), t = edgeEnd(b, ang + Math.PI), mx = (s.x + t.x) / 2, my = (s.y + t.y) / 2, w = e.label.length * 6.3 + 12, on = sel && sel.type === "edge" && sel.id === e.id;
      return `<g class="me-edge" data-id="${e.id}"><line x1="${s.x}" y1="${s.y}" x2="${t.x}" y2="${t.y}" stroke="${on ? cssv("--accent") : muted}" stroke-width="${on ? 2.6 : 1.6}" marker-end="url(#me-ah)" opacity=".85"/>${forExport ? "" : `<line class="hit" x1="${s.x}" y1="${s.y}" x2="${t.x}" y2="${t.y}" stroke="transparent" stroke-width="16"/>`}${e.label ? `<rect x="${mx - w / 2}" y="${my - 10}" width="${w}" height="20" rx="10" fill="${panelC}" stroke="${on ? cssv("--accent") : line}"/><text x="${mx}" y="${my + 4}" text-anchor="middle" font-size="11.5" fill="${muted}">${esc(e.label)}</text>` : ""}</g>`; }).join("");
    const nodes = doc.nodes.map(n => { const c = colorOf(n), on = sel && sel.type === "node" && sel.id === n.id, from = linkFrom === n.id;
      return `<g class="me-node" data-id="${n.id}" transform="translate(${n.x - n.w / 2},${n.y - n.h / 2})"><rect width="${n.w}" height="${n.h}" rx="12" fill="${panelC}" stroke="${c}" stroke-width="${on || from ? 3.4 : 2}" ${from ? 'stroke-dasharray="6 4"' : ""} ${on && !forExport ? `style="filter:drop-shadow(0 0 7px ${c})"` : ""}/><rect width="6" height="${n.h}" rx="3" fill="${c}"/>${n._L.map((l, i) => `<text x="${n.w / 2 + 3}" y="${19 + i * 17}" text-anchor="middle" font-size="13" font-weight="600" fill="${ink}">${esc(l)}</text>`).join("")}${n.page ? `<circle cx="${n.w - 6}" cy="6" r="4.5" fill="${cssv("--ok")}"><title>Linked to a vault page</title></circle>` : ""}${n.note ? `<circle cx="${n.w - 6}" cy="${n.h - 6}" r="3.5" fill="${muted}"><title>Has a note</title></circle>` : ""}</g>`; }).join("");
    return `<defs><marker id="me-ah" markerWidth="9" markerHeight="9" refX="8" refY="4.5" orient="auto"><path d="M0,0 L9,4.5 L0,9 z" fill="${muted}"/></marker></defs>${edges}${nodes}`;
  }
  function draw() {
    svg.innerHTML = `<rect id="me-bg" width="100%" height="100%" fill="transparent"/><g transform="translate(${view.x},${view.y}) scale(${view.k})">${markup(false)}</g>${linkMode ? `<text x="16" y="26" font-size="13" fill="${cssv("--accent")}" font-weight="600">${linkFrom ? "Now click the idea to link to" : "Link mode: click the first idea"} (Esc to cancel)</text>` : ""}`;
    $("#me-link").classList.toggle("sel", linkMode); svg.style.cursor = linkMode ? "crosshair" : "default"; drawPanel();
  }
  const fit = () => { if (!doc.nodes.length) { view.x = svg.clientWidth / 2; view.y = svg.clientHeight / 2; view.k = 1; return; } doc.nodes.forEach(size); const x0 = Math.min(...doc.nodes.map(n => n.x - n.w / 2)), x1 = Math.max(...doc.nodes.map(n => n.x + n.w / 2)), y0 = Math.min(...doc.nodes.map(n => n.y - n.h / 2)), y1 = Math.max(...doc.nodes.map(n => n.y + n.h / 2)); const W = svg.clientWidth, H = svg.clientHeight, k = Math.max(.25, Math.min(1.3, (W - 120) / Math.max(1, x1 - x0), (H - 120) / Math.max(1, y1 - y0))); view.k = k; view.x = W / 2 - k * (x0 + x1) / 2; view.y = H / 2 - k * (y0 + y1) / 2; };
  const center = () => ({ x: (svg.clientWidth / 2 - view.x) / view.k, y: (svg.clientHeight / 2 - view.y) / view.k });
  const free = (x, y) => { let p = { x, y }, tries = 0; while (doc.nodes.some(n => Math.abs(n.x - p.x) < 120 && Math.abs(n.y - p.y) < 50) && tries++ < 40) { p = { x: p.x + 40, y: p.y + 34 }; } return p; };
  const addNode = (label, x, y, page = null) => { const p = free(x, y); const n = { id: uid(), label, note: "", color: "auto", x: p.x, y: p.y, page }; doc.nodes.push(n); return n; };
  const addEdge = (from, to, label) => { if (from === to || doc.edges.some(e => e.from === from && e.to === to && e.label === label)) return null; const e = { id: uid("e"), from, to, label }; doc.edges.push(e); return e; };

  // ---- side panel
  function drawPanel() {
    const nb = byId();
    if (sel && sel.type === "node" && nb[sel.id]) {
      const n = nb[sel.id], pg = n.page && SLUG[n.page];
      panel.innerHTML = `<h3 style="margin:0 0 6px">Idea</h3>${pg ? `<div style="margin-bottom:6px">${chip(pg.type)}${statusChip(pg.status)}<a href="#/page/${esc(n.page)}" class="small">Open page →</a></div>` : `<div class="small muted" style="margin-bottom:6px">Your own idea</div>`}
        <label class="small">Label<input id="p-label" type="text" value="${esc(n.label)}"></label>
        <label class="small">Note<textarea id="p-note" placeholder="Your thoughts, an example, a question…">${esc(n.note)}</textarea></label>
        <div class="small muted" style="margin:8px 0 4px">Colour</div><div class="swatches">${["auto", ...Object.keys(NODE_COLORS)].map(c => `<button class="sw ${n.color === c ? "sel" : ""}" data-c="${c}" title="${c}" style="background:${c === "auto" ? "var(--chip)" : cssv(NODE_COLORS[c])}">${c === "auto" ? "A" : ""}</button>`).join("")}</div>
        <div class="actions" style="margin-top:12px"><button id="p-link">🔗 Link to…</button>${pg ? `<button class="ghost" id="p-nb">Add connected pages</button>` : ""}<button class="danger" id="p-del">Delete</button></div>
        <div class="small muted" style="margin-top:8px">Links: ${doc.edges.filter(e => e.from === n.id || e.to === n.id).length}</div>`;
      $("#p-label").oninput = e => { n.label = e.target.value || "Untitled"; changed(false); $("#p-label").focus(); };
      $("#p-label").onchange = () => snapshot(); $("#p-note").onchange = e => { snapshot(); n.note = e.target.value; changed(false); };
      $$(".sw", panel).forEach(b => b.onclick = () => { n.color = b.dataset.c; changed(); });
      $("#p-link").onclick = () => { linkMode = true; linkFrom = n.id; draw(); };
      $("#p-del").onclick = () => delSel();
      const nbB = $("#p-nb"); if (nbB) nbB.onclick = () => connectedDialog(n);
    } else if (sel && sel.type === "edge") {
      const e = doc.edges.find(x => x.id === sel.id); if (!e) { sel = null; return drawPanel(); }
      panel.innerHTML = `<h3 style="margin:0 0 6px">Link</h3><div class="small"><b>${esc(nb[e.from].label)}</b> → <b>${esc(nb[e.to].label)}</b></div>
        <label class="small">Label<input id="p-elabel" type="text" list="p-sug" value="${esc(e.label)}" placeholder="e.g. leads to"></label><datalist id="p-sug">${LINK_SUGGEST.map(s => `<option value="${s}">`).join("")}</datalist>
        <div class="actions" style="margin-top:10px"><button class="ghost" id="p-rev">⇄ Reverse</button><button class="danger" id="p-edel">Delete link</button></div>`;
      $("#p-elabel").oninput = ev => { e.label = ev.target.value.slice(0, 40); changed(false); $("#p-elabel").focus(); }; $("#p-elabel").onchange = () => snapshot();
      $("#p-rev").onclick = () => { snapshot(); [e.from, e.to] = [e.to, e.from]; changed(false); }; $("#p-edel").onclick = () => delSel();
    } else {
      panel.innerHTML = `<h3 style="margin:0 0 6px">${esc(doc.title)}</h3><div class="small muted">${doc.nodes.length} ideas · ${doc.edges.length} links</div>
        <ul class="small howto"><li><b>＋ Vault page</b> adds anything from your knowledge base</li><li><b>Double-click</b> empty space to add your own idea</li><li><b>🔗 Link</b>, then click two ideas to connect them and say how</li><li>Select a vault idea and choose <b>Add connected pages</b> to grow the map</li><li>Drag to move · scroll to zoom · drag the background to pan</li></ul>
        <div class="row" style="margin-top:12px"><button class="ghost danger-t" id="p-delmap">Delete this map</button></div>`;
      $("#p-delmap").onclick = async () => { if (confirm(`Delete "${doc.title}"? This cannot be undone.`)) { clearTimeout(saveTimer); saveTimer = null; await post(`/api/mymaps/${id}/delete`); location.hash = "#/mymaps"; } };
    }
  }
  function delSel() { if (!sel) return; snapshot(); if (sel.type === "node") { doc.nodes = doc.nodes.filter(n => n.id !== sel.id); doc.edges = doc.edges.filter(e => e.from !== sel.id && e.to !== sel.id); } else doc.edges = doc.edges.filter(e => e.id !== sel.id); sel = null; changed(false); }

  // ---- dialogs
  function vaultDialog() {
    openDialog(`<h2 style="margin-top:0">Add pages from your vault</h2><input id="v-q" type="text" placeholder="Search concepts, claims, sources…" autocomplete="off"><div class="row small" style="margin:8px 0"><label><input type="checkbox" id="v-subj" ${SUBJECT ? "checked" : ""}> only ${SUBJECT ? esc((subj(SUBJECT) || {}).name || "this subject") : "current subject"}</label></div><div id="v-res" class="list" style="max-height:48vh;overflow:auto"></div><div class="row" style="justify-content:flex-end;margin-top:10px"><button id="v-done">Done</button></div>`, (d, close) => {
      const q = $("#v-q", d); q.focus(); $("#v-done", d).onclick = close;
      const draw2 = () => { const t = q.value.toLowerCase(), only = $("#v-subj", d).checked && SUBJECT; const r = INDEX.filter(p => (!only || p.domains.includes(SUBJECT)) && (!t || p.title.toLowerCase().includes(t))).slice(0, 30); $("#v-res", d).innerHTML = r.map(p => { const has = doc.nodes.some(n => n.page === p.slug); return `<a class="item" href="#" data-s="${esc(p.slug)}">${chip(p.type)}<b>${esc(p.title)}</b>${has ? chip("on map", "ok") : ""}<small>${esc(p.summary)}</small></a>`; }).join("") || "<div class='muted' style='padding:10px'>No matches.</div>"; $$("#v-res a", d).forEach(a => a.onclick = e => { e.preventDefault(); const p = SLUG[a.dataset.s]; if (doc.nodes.some(n => n.page === p.slug)) { toast("Already on the map."); return; } const c = center(); const n = addNode(p.title, c.x, c.y, p.slug); sel = { type: "node", id: n.id }; changed(); draw2(); toast(`Added "${p.title}"`, 1200); }); };
      q.oninput = draw2; $("#v-subj", d).onchange = draw2; draw2();
    });
  }
  async function connectedDialog(n) {
    const list = groupNb(await api("/api/neighbors/" + encodeURIComponent(n.page)));
    if (!list.length) { toast("This page has no connections yet."); return; }
    const on = g => doc.nodes.some(q => q.page === g.slug);
    openDialog(`<h2 style="margin-top:0">Connected to “${esc(n.label)}”</h2><p class="small muted">Pick what to add to the map. Links are drawn with their relation.</p><div class="list" style="max-height:46vh;overflow:auto">${list.map((g, i) => `<label class="item" style="display:flex;gap:10px;align-items:center"><input type="checkbox" class="nbc" data-i="${i}" ${!on(g) && i < 8 ? "checked" : ""}><span>${chip(g.type)}<b>${esc(g.title)}</b> ${on(g) ? chip("already on map", "ok") : ""}<span class="muted small">${esc(g.rels.map(r => r.dir === "out" ? r.rel + " →" : "← " + r.rel).join(" · "))}</span></span></label>`).join("")}</div><div class="row" style="justify-content:flex-end;margin-top:12px"><button class="ghost" id="nb-c">Cancel</button><button id="nb-ok">Add selected</button></div>`, (d, close) => {
      $("#nb-c", d).onclick = close;
      $("#nb-ok", d).onclick = () => { const chosen = $$(".nbc:checked", d).map(c => list[+c.dataset.i]); if (!chosen.length) { close(); return; } snapshot(); const R = 230 + chosen.length * 8; chosen.forEach((g, i) => { let m = doc.nodes.find(q => q.page === g.slug); if (!m) { const a = i / chosen.length * 2 * Math.PI - Math.PI / 2; m = addNode(g.title, n.x + Math.cos(a) * R, n.y + Math.sin(a) * R, g.slug); } g.rels.forEach(r => r.dir === "out" ? addEdge(n.id, m.id, r.rel) : addEdge(m.id, n.id, r.rel)); }); close(); changed(false); fitSoon(); };
    });
  }
  function labelDialog(from, to) {
    const nb = byId();
    openDialog(`<h2 style="margin-top:0">How are they connected?</h2><p><b>${esc(nb[from].label)}</b> → <b>${esc(nb[to].label)}</b></p><input id="l-label" type="text" placeholder="e.g. leads to (optional)" autocomplete="off"><div class="row" style="margin-top:8px">${LINK_SUGGEST.map(s => `<button class="ghost sug">${s}</button>`).join("")}</div><div class="row" style="justify-content:flex-end;margin-top:14px"><button class="ghost" id="l-c">Cancel</button><button id="l-ok">Add link</button></div>`, (d, close) => {
      const inp = $("#l-label", d); inp.focus(); $$(".sug", d).forEach(b => b.onclick = () => { inp.value = b.textContent; inp.focus(); });
      const ok = () => { snapshot(); const e = addEdge(from, to, inp.value.trim().slice(0, 40)); close(); if (e) sel = { type: "edge", id: e.id }; changed(false); }; $("#l-ok", d).onclick = ok; inp.onkeydown = e => { if (e.key === "Enter") { e.preventDefault(); if (e.isComposing || e.keyCode === 229) return; ok(); } };  // IME-safe: Enter that confirms a Chinese/Japanese/Korean candidate must not submit $("#l-c", d).onclick = close;
    });
  }
  const fitSoon = () => { fit(); draw(); };

  // ---- pointer interaction
  svg.addEventListener("pointerdown", e => {
    const nodeEl = e.target.closest(".me-node"), edgeEl = e.target.closest(".me-edge");
    if (nodeEl) {
      const n = byId()[nodeEl.dataset.id];
      if (linkMode) { if (!linkFrom) { linkFrom = n.id; draw(); } else if (linkFrom !== n.id) { const f = linkFrom; linkMode = false; linkFrom = null; draw(); labelDialog(f, n.id); } return; }
      sel = { type: "node", id: n.id }; const w = worldOf(e); drag = { n, dx: n.x - w.x, dy: n.y - w.y, snap: false }; moved = false; draw(); svg.setPointerCapture(e.pointerId);
    } else if (edgeEl && !linkMode) { sel = { type: "edge", id: edgeEl.dataset.id }; draw(); }
    else {
      const now = performance.now();   // own double-click detection: the first click redraws, so the browser's dblclick would not fire
      if (!linkMode && now - lastBg.t < 380 && Math.hypot(e.clientX - lastBg.x, e.clientY - lastBg.y) < 10) {
        lastBg.t = 0; const w = worldOf(e), n = addNode("New idea", w.x, w.y); sel = { type: "node", id: n.id }; changed(); const l = $("#p-label"); if (l) { l.focus(); l.select(); } return;
      }
      lastBg = { t: now, x: e.clientX, y: e.clientY };
      if (!linkMode) sel = null; pan = { x: e.clientX, y: e.clientY, vx: view.x, vy: view.y }; moved = false; svg.setPointerCapture(e.pointerId); draw();
    }
  });
  svg.addEventListener("pointermove", e => {
    if (drag) { const w = worldOf(e); if (!drag.snap) { snapshot(); drag.snap = true; } drag.n.x = w.x + drag.dx; drag.n.y = w.y + drag.dy; moved = true; svg.querySelector("g").innerHTML = markup(false); }
    else if (pan) { view.x = pan.vx + e.clientX - pan.x; view.y = pan.vy + e.clientY - pan.y; moved = true; svg.querySelector("g").setAttribute("transform", `translate(${view.x},${view.y}) scale(${view.k})`); }
  });
  const up = () => { if (drag && moved) changed(false); drag = null; pan = null; };
  svg.addEventListener("pointerup", up); svg.addEventListener("pointercancel", up);
  svg.addEventListener("wheel", e => { e.preventDefault(); const r = svg.getBoundingClientRect(), mx = e.clientX - r.left, my = e.clientY - r.top, k2 = Math.max(.2, Math.min(2.5, view.k * (e.deltaY < 0 ? 1.12 : 1 / 1.12))); view.x = mx - (mx - view.x) * k2 / view.k; view.y = my - (my - view.y) * k2 / view.k; view.k = k2; draw(); }, { passive: false });
  const key = e => {
    if (!document.body.contains(svg)) return; const typing = /INPUT|TEXTAREA|SELECT/.test(e.target.tagName) || document.querySelector(".overlay");
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "z" && !typing) { e.preventDefault(); doUndo(); }
    else if ((e.key === "Delete" || e.key === "Backspace") && !typing) { e.preventDefault(); delSel(); }
    else if (e.key === "Escape") { linkMode = false; linkFrom = null; sel = null; draw(); }
    else if (e.key.toLowerCase() === "l" && !typing && !e.ctrlKey && !e.metaKey) { linkMode = !linkMode; linkFrom = null; draw(); }
  };
  addEventListener("keydown", key); onLeave(() => removeEventListener("keydown", key));
  function doUndo() { const s = undo.pop(); if (!s) { toast("Nothing to undo.", 1200); return; } const o = JSON.parse(s); doc.nodes = o.nodes; doc.edges = o.edges; doc.title = o.title; $("#me-title").value = doc.title; sel = null; changed(false); }

  // ---- toolbar
  $("#me-title").onchange = e => { snapshot(); doc.title = e.target.value.trim() || "Untitled map"; changed(false); };
  $("#me-vault").onclick = vaultDialog;
  $("#me-note").onclick = () => { const c = center(), n = addNode("New idea", c.x, c.y); sel = { type: "node", id: n.id }; changed(); const l = $("#p-label"); if (l) { l.focus(); l.select(); } };
  $("#me-link").onclick = () => { linkMode = !linkMode; linkFrom = sel && sel.type === "node" && linkMode ? sel.id : null; draw(); };
  $("#me-fit").onclick = fitSoon; $("#me-undo").onclick = doUndo;
  $("#me-zi").onclick = () => { view.k = Math.min(2.5, view.k * 1.2); draw(); }; $("#me-zo").onclick = () => { view.k = Math.max(.2, view.k / 1.2); draw(); };
  $("#me-tidy").onclick = () => {
    if (doc.nodes.length < 2) return; snapshot(); doc.nodes.forEach(size); const N = doc.nodes, idx = Object.fromEntries(N.map((n, i) => [n.id, i])), E = doc.edges.filter(e => idx[e.from] !== undefined && idx[e.to] !== undefined);
    N.forEach(n => { n.vx = n.vy = 0; });
    for (let t = 0; t < 500; t++) { const cool = 1 - t / 500;
      for (const a of N) for (const b of N) { if (a === b) continue; const dx = a.x - b.x || .1, dy = a.y - b.y || .1, d2 = dx * dx + dy * dy + 1, d = Math.sqrt(d2), f = 18000 / d2; a.vx += dx / d * f; a.vy += dy / d * f; if (Math.abs(dx) < (a.w + b.w) / 2 + 24 && Math.abs(dy) < (a.h + b.h) / 2 + 20) { a.vx += Math.sign(dx) * 2.5; a.vy += Math.sign(dy) * 2.5; } }
      for (const e of E) { const a = N[idx[e.from]], b = N[idx[e.to]], dx = b.x - a.x, dy = b.y - a.y, d = Math.hypot(dx, dy) || 1, f = (d - 230) * .02; a.vx += dx / d * f; a.vy += dy / d * f; b.vx -= dx / d * f; b.vy -= dy / d * f; }
      for (const n of N) { n.vx *= .82; n.vy *= .82; n.x += n.vx * cool; n.y += n.vy * cool; } }
    changed(false); fitSoon();
  };
  $("#me-svg").onclick = () => {
    if (!doc.nodes.length) { toast("The map is empty."); return; } const body = markup(true); doc.nodes.forEach(size);
    const x0 = Math.min(...doc.nodes.map(n => n.x - n.w / 2)) - 40, x1 = Math.max(...doc.nodes.map(n => n.x + n.w / 2)) + 40, y0 = Math.min(...doc.nodes.map(n => n.y - n.h / 2)) - 40, y1 = Math.max(...doc.nodes.map(n => n.y + n.h / 2)) + 40;
    const out = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="${x0} ${y0} ${x1 - x0} ${y1 - y0}" width="${x1 - x0}" height="${y1 - y0}" style="font-family:system-ui,sans-serif"><rect x="${x0}" y="${y0}" width="${x1 - x0}" height="${y1 - y0}" fill="${cssv("--bg")}"/>${body}</svg>`;
    const a = document.createElement("a"); a.href = URL.createObjectURL(new Blob([out], { type: "image/svg+xml" })); a.download = (doc.title || "map").toLowerCase().replace(/[^a-z0-9]+/g, "-") + ".svg"; a.click();
  };
  fit(); draw();
};

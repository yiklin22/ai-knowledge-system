"use strict";
const cssv = n => getComputedStyle(document.documentElement).getPropertyValue(n).trim() || "#888";
const pips = (lvl, c = "var(--ok)") => `<span class="pips">${[1, 2, 3, 4, 5].map(i => `<i class="${i <= lvl ? "on" : ""}" style="${i <= lvl ? "background:" + c : ""}"></i>`).join("")}</span>`;

// ================================================================ LEARNING MAP (personalised)
routes.learn = async () => {
  await loadSubjects(); if (!INDEX.length) await loadIndex();
  const m = await api("/api/learnmap?subject=" + encodeURIComponent(SUBJECT));
  const sub = subj(SUBJECT), sm = m.summary;
  if (!m.nodes.length) { app.innerHTML = `<h1>Learning map</h1><div class="card onboard center"><div style="font-size:40px">🗺</div><b>No concepts${sub ? ` in ${esc(sub.name)}` : ""} yet.</b><p class="muted">Add and approve a few sources and your map will appear here, ordered by what you need to learn first.</p><a class="btn" href="#/add">Add material</a></div>`; return; }
  const byId = Object.fromEntries(m.nodes.map(n => [n.id, n]));
  const cols = Array.from({ length: m.max_depth + 1 }, () => []);
  m.nodes.forEach(n => cols[n.depth].push(n));
  const NW = 196, NH = 58, CW = 262, RH = 76, PAD = 24;
  cols.forEach((col, ci) => { if (ci) col.sort((a, b) => bary(a) - bary(b)); col.forEach((n, i) => { n.y = PAD + i * RH; n.x = PAD + ci * CW; }); });
  function bary(n) { const ps = n.prereqs.map(p => byId[p]).filter(p => p && p.y !== undefined); return ps.length ? ps.reduce((a, p) => a + p.y, 0) / ps.length : 1e9; }
  const W = PAD * 2 + cols.length * CW - (CW - NW), H = PAD * 2 + Math.max(...cols.map(c => c.length)) * RH;
  const stColor = { mastered: "var(--ok)", ready: "var(--accent)", blocked: "var(--muted)" };
  const edgePath = e => { const a = byId[e.from], b = byId[e.to], x1 = a.x + NW, y1 = a.y + NH / 2, x2 = b.x, y2 = b.y + NH / 2, dx = (x2 - x1) / 2; return `M${x1},${y1} C${x1 + dx},${y1} ${x2 - dx},${y2} ${x2},${y2}`; };
  app.innerHTML = `<div class="row"><h1 style="flex:1;margin:0">Learning map ${SUBJECT ? subjectChip(SUBJECT) : ""}</h1><button id="placement" class="ghost">🎯 Placement check</button><a class="btn ghost" href="#/cmap">🕸 Concept maps</a><a class="btn ghost" href="#/play">🎛 Playgrounds</a><a class="btn ghost" href="#/build">🛠 Build mode</a><a class="btn ghost" href="#/mymaps">🧩 My maps</a></div>
  <p class="muted" style="margin:.3em 0 10px">Everything left to right is in the order you should learn it. Hover to trace prerequisites; click a concept for actions.</p>
  <div class="tiles slim"><div class="tile static"><b>${sm.mastered}/${sm.total}</b><span class="muted small">mastered</span></div><div class="tile static"><b style="color:var(--accent)">${sm.ready}</b><span class="muted small">ready now</span></div><div class="tile static"><b>${sm.blocked}</b><span class="muted small">blocked by prerequisites</span></div><div class="tile static"><b style="color:var(--warn)">${sm.gaps}</b><span class="muted small">gaps to fix</span></div></div>
  <div class="row small" style="margin:8px 0"><span class="muted">Show:</span><button class="ghost flt sel" data-f="all">All</button><button class="ghost flt" data-f="ready">Ready now</button><button class="ghost flt" data-f="gaps">Gaps</button><span style="flex:1"></span>
    <span class="lg"><i style="background:var(--ok)"></i>mastered</span><span class="lg"><i style="background:var(--accent)"></i>ready</span><span class="lg"><i style="background:var(--muted)"></i>blocked</span><span class="lg"><i style="background:var(--warn)"></i>gap</span><span class="lg"><i class="dash"></i>from another subject</span></div>
  <div class="lm-layout"><div><div class="row small" style="margin-bottom:4px"><button class="ghost" id="zo" title="Zoom out">−</button><button class="ghost" id="zi" title="Zoom in">＋</button><button class="ghost" id="zf" title="Fit everything">Fit</button><span class="muted">Drag the background to pan</span></div><div class="lm-scroll" id="lmscroll"><svg id="lm" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">
    <defs><marker id="arr" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="${cssv("--muted")}"/></marker></defs>
    ${m.edges.map(e => `<path class="lm-edge" data-a="${e.from}" data-b="${e.to}" d="${edgePath(e)}" marker-end="url(#arr)"/>`).join("")}
    ${m.nodes.map(n => `<g class="lm-node ${n.state} ${n.external ? "ext" : ""}" data-id="${n.id}" transform="translate(${n.x},${n.y})">
      <rect width="${NW}" height="${NH}" rx="12"/><rect class="bar" width="6" height="${NH}" rx="3" style="fill:${stColor[n.state]}"/>
      <text x="16" y="23" class="t">${esc(n.title.length > 24 ? n.title.slice(0, 23) + "…" : n.title)}</text>
      <g transform="translate(16,36)">${[1, 2, 3, 4, 5].map(i => `<rect x="${(i - 1) * 17}" width="13" height="7" rx="3" class="pip ${i <= n.level ? "on" : ""}" style="${i <= n.level ? "fill:" + stColor[n.state === "blocked" ? "ready" : n.state] : ""}"/>`).join("")}</g>
      ${n.gaps.length ? `<text x="${NW - 24}" y="22" class="warn-ico">⚠</text>` : ""}${n.has_playground ? `<text x="${NW - 24}" y="46" class="ico-s">🎛</text>` : ""}
    </g>`).join("")}</svg></div></div>
    <aside class="lm-panel card" id="panel"><div class="muted small">Select a concept to see its state, gaps and next actions.</div></aside></div>`;
  const nodes = $$(".lm-node"), edges = $$(".lm-edge");
  const sv = $("#lm"), sc2 = $("#lmscroll"); let zoom = 1;
  const setZoom = z => { zoom = Math.max(.3, Math.min(1.6, z)); sv.setAttribute("width", W * zoom); sv.setAttribute("height", H * zoom); };
  setZoom(Math.max(.75, Math.min(1, (sc2.clientWidth || 880) / W)));
  $("#zi").onclick = () => setZoom(zoom * 1.2); $("#zo").onclick = () => setZoom(zoom / 1.2); $("#zf").onclick = () => setZoom(Math.min(1, (sc2.clientWidth - 10) / W, (sc2.clientHeight - 10) / H));
  let pan = null; sc2.addEventListener("mousedown", e => { if (e.target.closest(".lm-node")) return; pan = { x: e.clientX, y: e.clientY, l: sc2.scrollLeft, t: sc2.scrollTop }; sc2.style.cursor = "grabbing"; });
  const mvp = e => { if (pan) { sc2.scrollLeft = pan.l - (e.clientX - pan.x); sc2.scrollTop = pan.t - (e.clientY - pan.y); } }, upp = () => { pan = null; sc2.style.cursor = ""; };
  addEventListener("mousemove", mvp); addEventListener("mouseup", upp); onLeave(() => { removeEventListener("mousemove", mvp); removeEventListener("mouseup", upp); });
  const chain = id => { const up = new Set(), down = new Set(); (function u(i) { byId[i].prereqs.forEach(p => { if (!up.has(p)) { up.add(p); u(p); } }); })(id); (function d(i) { m.nodes.forEach(n => { if (n.prereqs.includes(i) && !down.has(n.id)) { down.add(n.id); d(n.id); } }); })(id); return new Set([id, ...up, ...down]); };
  nodes.forEach(g => { g.onmouseenter = () => { const c = chain(g.dataset.id); nodes.forEach(n => n.classList.toggle("dim", !c.has(n.dataset.id))); edges.forEach(e => e.classList.toggle("dim", !(c.has(e.dataset.a) && c.has(e.dataset.b)))); }; g.onmouseleave = () => { nodes.forEach(n => n.classList.remove("dim")); edges.forEach(e => e.classList.remove("dim")); }; g.onclick = () => select(g.dataset.id); });
  function select(id) {
    const n = byId[id]; nodes.forEach(g => g.classList.toggle("sel", g.dataset.id === id));
    $("#panel").innerHTML = `<h3 style="margin:0 0 4px">${esc(n.title)}</h3><div>${chip(n.state, n.state === "mastered" ? "ok" : n.state === "ready" ? "" : "warn")}${n.domains.map(subjectChip).join("")}${n.external ? chip("other subject") : ""}</div>
      <div style="margin:8px 0">${pips(n.level, "var(--ok)")} <span class="small muted">level ${n.level}/5</span></div><p class="small muted">${esc(n.summary)}</p>
      ${n.gaps.length ? `<div class="gaps">${n.gaps.map(g => `<div>⚠ ${esc(g)}</div>`).join("")}</div>` : ""}
      ${n.accuracy !== null ? `<div class="small muted">Recall accuracy ${Math.round(n.accuracy * 100)}% over ${n.reviews} reviews</div>` : ""}
      <div class="actions" style="margin-top:10px"><a class="btn" href="#/tutor/${esc(n.slug)}">🧭 Teach me</a><a class="btn ghost" href="#/cmap/${esc(n.slug)}">🕸 Map</a><a class="btn ghost" href="#/play/${esc(n.slug)}">🎛 ${n.has_playground ? "Playground" : "Make playground"}</a><a class="btn ghost" href="#/build/${esc(n.slug)}">🛠 Build</a><a class="btn ghost" href="#/page/${esc(n.slug)}">Open page</a></div>
      <div class="selfrate" style="margin-top:10px"><span class="small muted">I'd rate myself</span> ${[0, 1, 2, 3, 4, 5].map(k => `<button class="lvl ${n.level === k ? "sel" : ""}" data-n="${k}">${k}</button>`).join("")}</div>`;
    $$("#panel .lvl").forEach(b => b.onclick = async () => { await post("/api/tutor/record", { page_id: n.id, level: +b.dataset.n, note: "self-rated" }); toast("Saved. Refreshing your map…", 1200); routes.learn(); });
  }
  $$(".flt").forEach(b => b.onclick = () => { $$(".flt").forEach(x => x.classList.toggle("sel", x === b)); const f = b.dataset.f; nodes.forEach(g => { const n = byId[g.dataset.id]; g.classList.toggle("faded", f === "ready" ? n.state !== "ready" : f === "gaps" ? !n.gaps.length : false); }); });
  $("#placement").onclick = () => placementCheck();
  const first = m.nodes.find(n => n.state === "ready" && !n.external) || m.nodes[0]; select(first.id);
};

async function placementCheck() {
  const probes = await api("/api/placement?subject=" + encodeURIComponent(SUBJECT) + "&n=8");
  if (!probes.length) { toast("No probe questions available yet. Ingest more material or study a concept first."); return; }
  let i = 0, shown = false; const results = [];
  openDialog(`<div id="pc"></div>`, (d, close) => {
    const draw = () => {
      if (i >= probes.length) { $("#pc", d).innerHTML = `<h2 style="margin-top:0">Placement complete</h2><p>I updated your levels for ${results.length} concept(s). Your learning map now reflects where you really are.</p>${results.map(r => `<div class="small">${esc(r.title)}: level ${r.level}</div>`).join("")}<div class="row" style="margin-top:12px;justify-content:flex-end"><button id="pc-done">See my map</button></div>`; $("#pc-done", d).onclick = () => { close(); routes.learn(); }; return; }
      const p = probes[i];
      $("#pc", d).innerHTML = `<div class="small muted">Question ${i + 1} of ${probes.length} · ${esc(p.title)}</div><h3 style="margin:.4em 0">${esc(p.q)}</h3>
        ${shown ? `<div class="card small"><b>A good answer shows:</b> ${esc(p.looks_for)}</div><div class="small muted" style="margin:8px 0">How did your own answer compare?</div><div class="row">${[["No idea", 0], ["Partly", 2], ["Solid", 3], ["Strong", 4]].map(([l, g]) => `<button class="${g < 3 ? "ghost" : ""}" data-g="${g}">${l}</button>`).join("")}</div>` : `<textarea placeholder="Answer in your own words first (just for you)…"></textarea><div class="row" style="margin-top:8px"><button id="pc-show">Show what a good answer shows</button><button class="ghost" id="pc-skip">Skip</button></div>`}`;
      if (!shown) { $("#pc-show", d).onclick = () => { shown = true; draw(); }; $("#pc-skip", d).onclick = () => { i++; draw(); }; $("textarea", d).focus(); }
      else $$("[data-g]", d).forEach(b => b.onclick = async () => { const level = +b.dataset.g; await post("/api/tutor/record", { page_id: p.page_id, level, note: "placement check" }); results.push({ title: p.title, level }); i++; shown = false; draw(); });
    };
    draw();
  });
}

// ================================================================ CONCEPT MAPS
const KIND = { core: ["Core idea", "--accent"], prerequisite: ["Prerequisite", "--warn"], part: ["Part / mechanism", "--info"], example: ["Example", "--ok"], misconception: ["Misconception", "--bad"], application: ["Application", "--violet"], related: ["Related", "--muted"] };

routes.cmap = async ([key]) => {
  if (!INDEX.length) await loadIndex();
  if (!key) {
    const list = await api("/api/conceptmaps");
    app.innerHTML = `<h1>Concept maps</h1><p class="muted">Stuck on a hard idea? A concept map shows how the ideas inside it connect: what it needs, what it is made of, where it is used and what people get wrong. Generate one from any concept in your vault, or from any topic you type, in any subject.</p>
    <div class="card"><b>Map any topic</b><div class="row" style="margin-top:8px"><input id="ct" type="text" placeholder="e.g. Photosynthesis, The French Revolution, Bayes' theorem…" style="flex:1"><button id="cg">Generate map</button></div><div class="small muted" style="margin-top:6px">Topics outside your vault are drawn from general knowledge and are marked as such. Add sources to ground them.</div><div id="cstatus" class="small muted"></div></div>
    <h2>Map a concept from your vault</h2><div class="card list">${INDEX.filter(p => p.type === "concept" && inSubject(p)).slice(0, 40).map(p => `<a class="item" href="#/cmap/${esc(p.slug)}"><b>${esc(p.title)}</b><small>${esc(p.summary)}</small></a>`).join("")}</div>
    <h2>Saved maps</h2><div class="card list">${list.map(m => `<a class="item" href="#/cmap/${esc(m.key)}"><b>${esc(m.topic)}</b> ${chip(m.nodes + " ideas")}${m.from_vault ? "" : chip("outside vault", "warn")}<small>${esc(m.created || "")}</small></a>`).join("") || "<div class='muted' style='padding:10px'>None yet.</div>"}</div>`;
    $("#cg").onclick = ev => busy(ev.target, async () => { const topic = $("#ct").value.trim(); if (!topic) return; const j = await post("/api/conceptmap/generate", { topic, detail: "overview" }); const d = await watchJob(j.job, (l) => $("#cstatus").textContent = lastLine(l)); if (d.status === "done") location.hash = "#/cmap/" + d.result.key; else toast("Could not build the map: " + lastLine(d.log), 7000); });
    return;
  }
  let cm = null; try { cm = await api("/api/conceptmap/" + encodeURIComponent(key)); } catch {}
  const page = SLUG[key], title = cm ? cm.topic : page ? page.title : key;
  app.innerHTML = `<div class="small muted"><a href="#/cmap">Concept maps</a> › ${esc(title)}</div>
  <div class="row"><h1 style="flex:1;margin:0">${esc(title)}</h1>${page ? `<a class="btn ghost" href="#/page/${esc(key)}">Open page</a><a class="btn ghost" href="#/tutor/${esc(key)}">🧭 Teach me</a>` : ""}</div>
  <div class="row" style="margin:10px 0"><select id="cd" style="width:auto"><option value="overview">Overview (9-14 ideas)</option><option value="detailed">Detailed</option></select><button id="cgen">${cm ? "Regenerate" : "Generate concept map"}</button>${cm ? `<button class="ghost" id="cdl">Download SVG</button>` : ""}<span id="cstatus" class="small muted"></span></div>
  <div id="cm-area">${cm ? "" : `<div class="card onboard center"><div style="font-size:40px">🕸</div><b>No map yet for this concept.</b><p class="muted">Claude builds it from your vault page and its connections, in about half a minute.</p></div>`}</div>`;
  $("#cgen").onclick = ev => busy(ev.target, async () => {
    const j = await post("/api/conceptmap/generate", page ? { page: key, detail: $("#cd").value } : { topic: title, detail: $("#cd").value });
    const d = await watchJob(j.job, l => $("#cstatus").textContent = lastLine(l));
    if (d.status === "done") routes.cmap([d.result.key]); else toast("Could not build the map: " + lastLine(d.log), 8000);
  });
  if (cm) drawConceptMap(cm, $("#cm-area"));
};

function drawConceptMap(cm, host) {
  const C = k => cssv(KIND[k][1]);
  const N = cm.nodes.map((n, i) => ({ ...n, w: Math.max(70, Math.min(190, 18 + n.label.length * 7.4)), h: 34 }));
  const idx = Object.fromEntries(N.map((n, i) => [n.id, i]));
  const E = cm.edges.map(e => ({ ...e, a: N[idx[e.from]], b: N[idx[e.to]] }));
  const core = N.find(n => n.kind === "core") || N[0]; const W = 1200, H = 760; let VB = [0, 0, W, H];
  N.forEach((n, i) => { const a = i / N.length * 2 * Math.PI; n.x = W / 2 + Math.cos(a) * (n === core ? 0 : 230); n.y = H / 2 + Math.sin(a) * (n === core ? 0 : 200); n.vx = n.vy = 0; });
  for (let t = 0; t < 700; t++) {
    const cool = 1 - t / 700;
    for (const a of N) for (const b of N) { if (a === b) continue; let dx = a.x - b.x, dy = a.y - b.y, d2 = dx * dx + dy * dy + 1, d = Math.sqrt(d2); const minX = (a.w + b.w) / 2 + 26, minY = (a.h + b.h) / 2 + 22; const f = 16000 / d2; a.vx += dx / d * f; a.vy += dy / d * f; if (Math.abs(dx) < minX && Math.abs(dy) < minY) { a.vx += Math.sign(dx || 1) * 2.4; a.vy += Math.sign(dy || 1) * 2.4; } }
    for (const e of E) { const dx = e.b.x - e.a.x, dy = e.b.y - e.a.y, d = Math.hypot(dx, dy) || 1, f = (d - 215) * .018; e.a.vx += dx / d * f; e.a.vy += dy / d * f; e.b.vx -= dx / d * f; e.b.vy -= dy / d * f; }
    for (const n of N) { n.vx += (W / 2 - n.x) * .004; n.vy += (H / 2 - n.y) * .004; n.vx *= .82; n.vy *= .82; n.x += n.vx * cool; n.y += n.vy * cool; n.x = Math.max(n.w / 2 + 8, Math.min(W - n.w / 2 - 8, n.x)); n.y = Math.max(24, Math.min(H - 24, n.y)); }
  }
  { const x0 = Math.min(...N.map(n => n.x - n.w / 2)) - 40, x1 = Math.max(...N.map(n => n.x + n.w / 2)) + 40, y0 = Math.min(...N.map(n => n.y - n.h / 2)) - 40, y1 = Math.max(...N.map(n => n.y + n.h / 2)) + 40; VB = [x0, y0, x1 - x0, y1 - y0]; }
  host.innerHTML = `<div class="cm-layout"><div class="cm-wrap"><svg id="cmsvg" viewBox="${VB.join(" ")}" width="100%" style="height:auto;display:block"></svg></div>
    <aside class="card" id="cm-panel"><div class="muted small">${cm.summary ? esc(cm.summary) : "Click a node to read what it means."}</div></aside></div>
    <div class="row small" style="margin-top:8px">${Object.entries(KIND).map(([k, [l, c]]) => `<span class="lg"><i style="background:${C(k)}"></i>${l}</span>`).join("")}<span class="muted">· ${cm.from_vault ? "Grounded in your vault page" : "From general knowledge (not in your vault)"} · a teaching aid, not evidence</span></div>`;
  const svg = $("#cmsvg"); const ink = cssv("--ink"), muted = cssv("--muted"), panel = cssv("--panel"), line = cssv("--line");
  const paint = () => {
    svg.innerHTML = `<defs><marker id="ah" markerWidth="9" markerHeight="9" refX="8" refY="4.5" orient="auto"><path d="M0,0 L9,4.5 L0,9 z" fill="${muted}"/></marker></defs><rect x="${VB[0] - 400}" y="${VB[1] - 400}" width="${VB[2] + 800}" height="${VB[3] + 800}" fill="transparent"/>` +
      E.map((e, i) => { const ax = e.a.x, ay = e.a.y, bx = e.b.x, by = e.b.y, ang = Math.atan2(by - ay, bx - ax); const s = edgeEnd(e.a, ang), t = edgeEnd(e.b, ang + Math.PI); const mx = (s.x + t.x) / 2, my = (s.y + t.y) / 2, w = e.label.length * 6.2 + 10;
        return `<g><line x1="${s.x}" y1="${s.y}" x2="${t.x}" y2="${t.y}" stroke="${muted}" stroke-width="1.4" marker-end="url(#ah)" opacity=".75"/>${e.label ? `<rect x="${mx - w / 2}" y="${my - 9}" width="${w}" height="17" rx="8" fill="${panel}" stroke="${line}"/><text x="${mx}" y="${my + 4}" text-anchor="middle" font-size="11" fill="${muted}">${esc(e.label)}</text>` : ""}</g>`; }).join("") +
      N.map(n => `<g class="cm-node" data-id="${n.id}" transform="translate(${n.x - n.w / 2},${n.y - n.h / 2})" style="cursor:pointer"><rect width="${n.w}" height="${n.h}" rx="${n.kind === "core" ? 17 : 10}" fill="${n.kind === "core" ? C("core") : panel}" stroke="${C(n.kind)}" stroke-width="${n.kind === "core" ? 0 : 2}" ${n.vault_slug ? "" : 'stroke-dasharray=""'}/><text x="${n.w / 2}" y="${n.h / 2 + 5}" text-anchor="middle" font-size="${n.kind === "core" ? 14 : 12.5}" font-weight="${n.kind === "core" ? 700 : 600}" fill="${n.kind === "core" ? "#fff" : ink}">${esc(n.label)}</text>${n.vault_slug ? `<circle cx="${n.w - 4}" cy="4" r="5" fill="${cssv("--ok")}"/>` : ""}</g>`).join("");
    $$(".cm-node", svg).forEach(g => { g.onmousedown = ev => startDrag(ev, N[idx[g.dataset.id]]); g.onclick = () => { if (!moved) show(N[idx[g.dataset.id]]); }; });
  };
  function edgeEnd(n, ang) { const hw = n.w / 2 + 2, hh = n.h / 2 + 2, c = Math.cos(ang), s = Math.sin(ang); const t = Math.min(Math.abs(c) > 1e-6 ? hw / Math.abs(c) : 1e9, Math.abs(s) > 1e-6 ? hh / Math.abs(s) : 1e9); return { x: n.x + c * t, y: n.y + s * t }; }
  function show(n) {
    $$(".cm-node rect", svg).forEach(r => r.style.filter = ""); const g = $(`.cm-node[data-id="${n.id}"] rect`, svg); if (g) g.style.filter = "drop-shadow(0 0 6px " + C(n.kind) + ")";
    const out = n.note.toLowerCase().startsWith("outside your vault");
    $("#cm-panel").innerHTML = `<h3 style="margin:0 0 4px">${esc(n.label)}</h3>${chip(KIND[n.kind][0])}${out ? chip("outside your vault", "warn") : ""}<p>${esc(n.note)}</p>
      ${n.vault_slug ? `<div class="actions"><a class="btn" href="#/page/${esc(n.vault_slug)}">Open in vault</a><a class="btn ghost" href="#/cmap/${esc(n.vault_slug)}">Map this</a><a class="btn ghost" href="#/tutor/${esc(n.vault_slug)}">🧭 Teach me</a></div>` : `<div class="small muted">Not in your vault yet. Add a source about it to ground it.</div>`}
      <div class="small muted" style="margin-top:10px">Connections:</div>${E.filter(e => e.a === n || e.b === n).map(e => `<div class="small">${e.a === n ? `→ <i>${esc(e.label)}</i> <b>${esc(e.b.label)}</b>` : `← <b>${esc(e.a.label)}</b> <i>${esc(e.label)}</i>`}</div>`).join("")}`;
  }
  let moved = false;
  function startDrag(ev, n) { moved = false; const p = svg.createSVGPoint(); const mv = e => { moved = true; p.x = e.clientX; p.y = e.clientY; const q = p.matrixTransform(svg.getScreenCTM().inverse()); n.x = q.x; n.y = q.y; paint(); }; const up = () => { removeEventListener("mousemove", mv); removeEventListener("mouseup", up); setTimeout(() => moved = false, 0); }; addEventListener("mousemove", mv); addEventListener("mouseup", up); }
  paint(); show(core);
  const dl = $("#cdl"); if (dl) dl.onclick = () => { const s = new XMLSerializer().serializeToString(svg).replace("<svg ", `<svg xmlns="http://www.w3.org/2000/svg" style="background:${panel};font-family:system-ui,sans-serif" `); const a = document.createElement("a"); a.href = URL.createObjectURL(new Blob([s], { type: "image/svg+xml" })); a.download = `concept-map-${cm.key}.svg`; a.click(); };
}

// ================================================================ PLAYGROUNDS
routes.play = async ([slug]) => {
  if (!INDEX.length) await loadIndex();
  if (!slug) {
    const m = await api("/api/learnmap?subject=" + encodeURIComponent(SUBJECT));
    const have = m.nodes.filter(n => n.has_playground), none = m.nodes.filter(n => !n.has_playground && !n.external);
    app.innerHTML = `<h1>Playgrounds</h1><p class="muted">Learn by changing variables and watching what happens. Each one starts by asking you to predict the outcome.</p>
      <div class="subjects">${have.map(n => `<a class="subject-card" href="#/play/${esc(n.slug)}"><span class="sc-ico">🎛</span><b>${esc(n.title)}</b><span class="muted small">${esc(n.summary)}</span></a>`).join("") || "<div class='card muted'>None yet.</div>"}</div>
      <h2>Make a new one</h2><p class="muted small">Pick a concept and Claude builds an interactive simulation for it (about a minute).</p><div class="card list">${none.slice(0, 40).map(n => `<a class="item" href="#/play/${esc(n.slug)}"><b>${esc(n.title)}</b></a>`).join("")}</div>`;
    return;
  }
  const info = await api("/api/playground/" + slug), p = SLUG[slug];
  app.innerHTML = `<div class="small muted"><a href="#/play">Playgrounds</a> › ${esc(p ? p.title : slug)}</div><div class="row"><h1 style="flex:1;margin:0">${esc(p ? p.title : slug)}</h1>${p ? `<a class="btn ghost" href="#/page/${esc(slug)}">Open page</a><a class="btn ghost" href="#/tutor/${esc(slug)}">🧭 Teach me</a>` : ""}${info.exists ? `<a class="btn ghost" href="/playground/${esc(slug)}.html" target="_blank" rel="noopener">Full screen ↗</a>` : ""}</div>
    ${info.exists ? `<iframe class="playframe" sandbox="allow-scripts" src="/playground/${esc(slug)}.html" title="Playground"></iframe><div class="small muted" style="margin-top:6px">Runs sandboxed with no network access. A teaching aid, not a source.</div>`
    : `<div class="card onboard center" id="pg"><div style="font-size:40px">🎛</div><b>No playground for this concept yet.</b><p class="muted">Claude can build an interactive simulation from your vault page: sliders, a live visual and a "predict first" question.</p><button id="pgen">Generate playground</button><div class="small muted" id="pst" style="margin-top:8px"></div></div>`}`;
  const g = $("#pgen"); if (g) g.onclick = ev => busy(ev.target, async () => { const j = await post("/api/playground/generate", { page: slug }); const d = await watchJob(j.job, l => $("#pst").textContent = lastLine(l)); if (d.status === "done") routes.play([slug]); else toast("Could not build it: " + lastLine(d.log), 8000); });
};

// ================================================================ LEARNING-TO-BUILD
const BUILD_KINDS = { coding: ["💻", "Coding exercise", "Write a small program from scratch, with checks you can run"], experiment: ["🧪", "Experiment", "Form a hypothesis, change something, measure, interpret"], essay: ["✍️", "Essay or explainer", "Argue it with evidence against a rubric"], project: ["🧩", "Mini project", "Apply it to something practical, in milestones"] };
routes.build = async ([slug]) => {
  if (!INDEX.length) await loadIndex();
  if (!slug) { app.innerHTML = `<h1>Build mode</h1><p class="muted">Turn what you learn into something you make. Pick a concept to get a coding task, experiment, essay prompt or mini project, with hints that never give the answer away.</p><div class="card list">${INDEX.filter(p => p.type === "concept" && inSubject(p)).slice(0, 50).map(p => `<a class="item" href="#/build/${esc(p.slug)}"><b>${esc(p.title)}</b><small>${esc(p.summary)}</small></a>`).join("")}</div>`; return; }
  const p = SLUG[slug]; let tasks = await api("/api/build/" + slug); let cur = tasks[0] ? tasks[0].kind : null;
  const draw = () => {
    const t = tasks.find(x => x.kind === cur);
    app.innerHTML = `<div class="small muted"><a href="#/build">Build mode</a> › ${esc(p ? p.title : slug)}</div><div class="row"><h1 style="flex:1;margin:0">Build with: ${esc(p ? p.title : slug)}</h1>${p ? `<a class="btn ghost" href="#/page/${esc(slug)}">Open page</a>` : ""}</div>
    <div class="kinds">${Object.entries(BUILD_KINDS).map(([k, [ic, nm, ds]]) => { const have = tasks.some(x => x.kind === k); return `<div class="kind ${cur === k ? "sel" : ""}" data-k="${k}"><span style="font-size:24px">${ic}</span><b>${nm}</b><span class="small muted">${ds}</span><span class="small">${have ? "✓ ready, open" : "Generate"}</span></div>`; }).join("")}</div>
    <div id="bstatus" class="small muted" style="margin:6px 0"></div><div id="task">${t ? "" : cur ? "" : `<div class="card muted">Choose a kind of task above.</div>`}</div>`;
    $$(".kind").forEach(k => k.onclick = async () => { const kind = k.dataset.k; if (tasks.some(x => x.kind === kind)) { cur = kind; draw(); return; } cur = kind; $$(".kind").forEach(x => x.classList.toggle("sel", x === k)); $("#bstatus").textContent = "Designing your task…"; try { const j = await post("/api/build/generate", { page: slug, kind }); const d = await watchJob(j.job, l => $("#bstatus").textContent = lastLine(l)); if (d.status !== "done") throw new Error(lastLine(d.log)); tasks = await api("/api/build/" + slug); draw(); } catch (e) { toast("Could not design it: " + e.message, 7000); $("#bstatus").textContent = ""; } });
    if (t) drawTask(t);
  };
  function drawTask(t) {
    let hints = 0;
    $("#task").innerHTML = `<div class="card"><h2 style="margin-top:0">${esc(t.title)}</h2>${chip(BUILD_KINDS[t.kind][1])}${t.time_minutes ? chip("~" + t.time_minutes + " min") : ""}<p>${esc(t.goal)}</p>
      <h3>Steps</h3><ol class="steps">${t.steps.map(s => `<li>${esc(s)}</li>`).join("")}</ol>
      ${t.starter ? `<h3>Starter ${t.language ? "(" + esc(t.language) + ")" : ""} <button class="ghost small" id="cp">Copy</button> <button class="ghost small" id="dlst">Download</button></h3><pre class="code"><code>${esc(t.starter)}</code></pre>` : ""}
      <h3>Done when</h3>${t.checks.map((c, i) => `<label class="chk"><input type="checkbox" data-i="${i}" ${t.progress[i] ? "checked" : ""}> ${esc(c)}</label>`).join("")}
      <h3>Stuck?</h3><div id="hints"></div><button class="ghost" id="hint">Give me a hint (${t.hints.length} available)</button>
      ${t.stretch ? `<h3>Stretch</h3><p class="muted">${esc(t.stretch)}</p>` : ""}</div>
      <div class="card"><h3 style="margin-top:0">Check your work</h3><p class="muted small">Paste your code, notes or draft. The reviewer asks questions and points at gaps; it will not rewrite your work.</p><textarea id="work" style="min-height:140px" placeholder="Paste your work here…"></textarea><div class="row" style="margin-top:8px"><button id="review">Get feedback</button></div><div id="fb"></div></div>
      ${t.submissions.length ? `<div class="small muted">Previous reviews: ${t.submissions.map(s => `${esc(s.at)} (${esc(s.verdict)})`).join(" · ")}</div>` : ""}`;
    $$(".chk input").forEach(c => c.onchange = () => post("/api/build/progress", { page: slug, kind: t.kind, progress: $$(".chk input").map(x => x.checked) }));
    $("#hint").onclick = () => { if (hints < t.hints.length) { $("#hints").insertAdjacentHTML("beforeend", `<div class="hint"><b>Hint ${hints + 1}</b> ${esc(t.hints[hints])}</div>`); hints++; } if (hints >= t.hints.length) $("#hint").disabled = true; };
    const cp = $("#cp"); if (cp) { cp.onclick = () => { navigator.clipboard.writeText(t.starter); toast("Copied."); }; $("#dlst").onclick = () => { const a = document.createElement("a"); a.href = URL.createObjectURL(new Blob([t.starter], { type: "text/plain" })); a.download = slug + "-starter.txt"; a.click(); }; }
    $("#review").onclick = ev => busy(ev.target, async () => {
      const work = $("#work").value; if (!work.trim()) { toast("Paste your work first."); return; }
      const fb = await post("/api/build/review", { page: slug, kind: t.kind, work });
      const li = a => a.length ? `<ul>${a.map(x => `<li>${esc(x)}</li>`).join("")}</ul>` : "<div class='muted small'>None.</div>";
      $("#fb").innerHTML = `<div class="card" style="margin-top:12px"><div>${chip(fb.verdict, fb.verdict === "ready" ? "ok" : "warn")}</div><b>What worked</b>${li(fb.worked)}<b>Gaps</b>${li(fb.gaps)}<b>Questions to think about</b>${li(fb.questions)}${fb.next_step ? `<p><b>Next step:</b> ${esc(fb.next_step)}</p>` : ""}${fb.verdict === "ready" ? `<div class="row"><a class="btn" href="#/tutor/${esc(slug)}">Check my understanding with the tutor</a></div>` : ""}</div>`;
    });
  }
  draw();
};

// ================================================================ COMMAND PALETTE (Ctrl/Cmd+K)
const COMMANDS = [["Home", "#/", "🏠"], ["Learning map", "#/learn", "🗺"], ["Library", "#/library", "📚"], ["My maps (build your own)", "#/mymaps", "🧩"],["Study Flashcards", "#/study", "🧠"], ["Tutor", "#/tutor", "🧭"], ["Concept maps", "#/cmap", "🕸"], ["Playgrounds", "#/play", "🎛"], ["Build mode", "#/build", "🛠"], ["Add material", "#/add", "📥"], ["Review proposals", "#/review", "✅"]];
function openPalette() {
  if ($(".palette")) return;
  const d = document.createElement("div"); d.className = "overlay top";
  d.innerHTML = `<div class="palette"><input id="pq" type="text" placeholder="Jump to a page, subject or action…" autocomplete="off"><div id="pl"></div><div class="small muted" style="padding:6px 12px">↑↓ to move · Enter to open · Esc to close</div></div>`;
  document.body.appendChild(d); const close = () => d.remove(); d.addEventListener("mousedown", e => { if (e.target === d) close(); });
  let sel = 0, items = [];
  const build = q => {
    q = q.toLowerCase(); const acts = [...COMMANDS.map(([t, h, i]) => ({ t, i, kind: "Go to", run: () => location.hash = h })), { t: "New subject…", i: "＋", kind: "Action", run: openSubjectDialog }, { t: "Take the tour", i: "✨", kind: "Action", run: startTour }, { t: "Toggle dark mode", i: "◐", kind: "Action", run: () => $("#theme").click() }, { t: "Placement check", i: "🎯", kind: "Action", run: placementCheck },
      ...SUBJECTS.map(s => ({ t: s.name, i: s.icon, kind: "Subject", run: () => { SUBJECT = s.key; store.set("kb-subject", s.key); drawSubjectSelect(); applySubjectColor(); location.hash = "#/subject/" + s.key; route(); } }))];
    const pg = INDEX.filter(p => !q || p.title.toLowerCase().includes(q)).slice(0, 14).map(p => ({ t: p.title, i: { concept: "💡", claim: "⚖", source: "📄", question: "❓", entity: "👤", map: "🗺" }[p.type] || "•", kind: p.type, run: () => location.hash = "#/page/" + p.slug }));
    items = [...acts.filter(a => !q || a.t.toLowerCase().includes(q)), ...pg].slice(0, 16); sel = 0; paint();
  };
  const paint = () => { $("#pl").innerHTML = items.map((it, i) => `<div class="pi ${i === sel ? "on" : ""}" data-i="${i}"><span>${esc(it.i)}</span><b>${esc(it.t)}</b><span class="muted small">${esc(it.kind)}</span></div>`).join("") || "<div class='muted' style='padding:12px'>No matches.</div>"; $$(".pi", d).forEach(e => { e.onmousemove = () => { sel = +e.dataset.i; $$(".pi", d).forEach((x, j) => x.classList.toggle("on", j === sel)); }; e.onclick = () => { close(); items[+e.dataset.i].run(); }; }); };
  const q = $("#pq"); q.focus(); q.oninput = () => build(q.value);
  q.onkeydown = e => { if (e.isComposing || e.keyCode === 229) return;  /* IME-safe: keys that pick a candidate stay with the IME */ if (e.key === "Escape") close(); else if (e.key === "ArrowDown") { e.preventDefault(); sel = Math.min(items.length - 1, sel + 1); paint(); } else if (e.key === "ArrowUp") { e.preventDefault(); sel = Math.max(0, sel - 1); paint(); } else if (e.key === "Enter" && items[sel]) { close(); items[sel].run(); } };
  build("");
}
addEventListener("keydown", e => { if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "k") { e.preventDefault(); openPalette(); } });
$("#kbtn").addEventListener("click", openPalette);

// ================================================================ ONBOARDING TOUR
function startTour() {
  const steps = [["Welcome", "This is a knowledge base that grows from anything you read, and teaches it back to you. Here is a 30-second tour.", "✨"],
    ["1 · Add anything", "Drop files, paste links or text under <b>Add</b>. Claude reads them and proposes structured pages with real, checkable quotes.", "📥"],
    ["2 · You stay in control", "Under <b>Review</b> you see every proposed page or change and approve it. Nothing enters your knowledge base without your click.", "✅"],
    ["3 · Learn it your way", "The <b>Learning map</b> shows what to learn first. Use the <b>Tutor</b>, <b>Playgrounds</b>, <b>Concept maps</b>, <b>Build mode</b> and spaced-repetition <b>Study</b>.", "🧭"],
    ["4 · Any subject", "Use the subject switcher at the top, or press <kbd>Ctrl</kbd>+<kbd>K</kbd> to jump anywhere. Create subjects for history, law, biology, anything.", "🌍"]];
  let i = 0; const close = openDialog(`<div id="tour"></div>`, d => {
    const draw = () => { const [t, b, ic] = steps[i]; $("#tour", d).innerHTML = `<div class="center"><div style="font-size:46px">${ic}</div><h2 style="margin:.2em 0">${t}</h2><p>${b}</p><div class="dots">${steps.map((_, j) => `<i class="${j === i ? "on" : ""}"></i>`).join("")}</div><div class="row" style="justify-content:center;margin-top:14px"><button class="ghost" id="tskip">Skip</button><button id="tnext">${i === steps.length - 1 ? "Start exploring" : "Next"}</button></div></div>`; $("#tskip", d).onclick = fin; $("#tnext", d).onclick = () => { if (i === steps.length - 1) fin(); else { i++; draw(); } }; };
    const fin = () => { store.set("kb-toured", "1"); d.remove(); }; draw();
  });
}

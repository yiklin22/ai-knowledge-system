"use strict";
// ================================================================ HOME (Today)
const greeting = () => { const h = new Date().getHours(); return h < 5 ? "Still up" : h < 12 ? "Good morning" : h < 18 ? "Good afternoon" : "Good evening"; };
const overallProgress = () => {
  const ss = SUBJECT ? SUBJECTS.filter(s => s.key === SUBJECT) : SUBJECTS; const w = ss.reduce((a, s) => a + s.concepts, 0);
  return w ? ss.reduce((a, s) => a + s.progress * s.concepts, 0) / w : 0;
};

routes.home = async () => {
  const [s, today, props] = await Promise.all([api("/api/state"), api("/api/today?subject=" + encodeURIComponent(SUBJECT)), api("/api/proposals"), loadSubjects()]);
  const cur = subj(SUBJECT), st = today.streak, nxt = today.next[0];
  const tile = (href, icon, title, sub, cls = "") => `<a class="tile ${cls}" href="${href}"><span class="tile-ico">${icon}</span><b>${esc(title)}</b><span class="muted small">${esc(sub)}</span></a>`;
  app.innerHTML = `
  <section class="hero">
    <div class="hero-text">
      <div class="eyebrow">${cur ? esc(cur.icon + " " + cur.name) : "All subjects"}</div>
      <h1>${greeting()}.</h1>
      <p class="muted">${today.due || nxt ? `About <b>${Math.max(5, today.minutes)} minutes</b> keeps you on track today.` : "You are all caught up. Add something new to learn from."}</p>
      <div class="row">${st.current ? `<span class="pill-big">🔥 ${st.current}-day streak${st.today_done ? " · done today" : ""}</span>` : `<span class="pill-big muted">Start a streak: review one card today</span>`}</div>
    </div>
    <div class="hero-ring">${ring(overallProgress(), "var(--subject)", 120, "", 10)}<div class="small muted">mastery</div></div>
  </section>
  <div class="tiles">
    ${tile("#/study", "🧠", today.due ? `Review ${today.due} card${today.due > 1 ? "s" : ""}` : "Recall is clear", today.due ? "Spaced repetition, due now" : "Nothing due right now", today.due ? "accent" : "")}
    ${nxt ? tile("#/tutor/" + nxt.slug, "🧭", "Learn: " + nxt.title, `Ready now · unlocks ${nxt.unlocks} more`) : tile("#/add", "＋", "Add your first material", "Then it appears in your learning map")}
    ${today.continue ? tile("#/tutor/" + today.continue.slug, "▶", "Continue: " + today.continue.title, `Level ${today.continue.level}/5 · last studied ${today.continue.day}`) : tile("#/learn", "🗺", "Open your learning map", "See gaps and prerequisites")}
    ${tile("#/add", "📥", "Add material", `${s.undigested} source${s.undigested === 1 ? "" : "s"} waiting to be digested`)}
  </div>
  ${props.length ? `<div class="card notice"><b>Waiting for your review:</b> ${props.map(p => `<a href="#/review">${esc(p.batch)}</a> ${chip(p.files.length + " pages")}`).join(" ")}</div>` : ""}
  ${SUBJECT ? "" : `<h2>Your subjects</h2><div class="subjects">${SUBJECTS.map(subjectCard).join("")}<a class="subject-card add" href="#" id="new-subj"><span style="font-size:30px">＋</span><b>Add a subject</b><span class="muted small">History, law, biology, anything you want to learn</span></a></div>`}
  ${SUBJECT ? `<h2>Open ${esc(cur.name)}</h2><a class="btn" href="#/subject/${esc(SUBJECT)}">Subject overview →</a>` : ""}
  ${today.next.length > 1 ? `<h2>Also ready</h2><div class="card list">${today.next.slice(1).map(t => `<a class="item" href="#/tutor/${esc(t.slug)}"><b>${esc(t.title)}</b> ${subjectChip(t.domains[0])}<small>${esc(t.summary)}</small></a>`).join("")}</div>` : ""}`;
  const ns = $("#new-subj"); if (ns) ns.onclick = e => { e.preventDefault(); openSubjectDialog(); };
  if (!store.get("kb-toured", "")) setTimeout(startTour, 500);
};

function subjectCard(s) {
  const empty = !s.pages;
  return `<a class="subject-card ${empty ? "empty" : ""}" href="#/subject/${esc(s.key)}" style="--sc:${s.color}">
    <div class="sc-top"><span class="sc-ico">${esc(s.icon)}</span>${empty ? "" : ring(s.progress, s.color, 54, "", 6)}</div>
    <b>${esc(s.name)}</b><span class="muted small">${esc(s.description)}</span>
    <div class="sc-stats">${empty ? `<span class="chip">empty · add the first source</span>` : `<span class="chip">${s.concepts} concepts</span><span class="chip">${s.sources} sources</span>${s.due ? `<span class="chip warn">${s.due} due</span>` : ""}`}</div></a>`;
}

// ================================================================ SUBJECT page
routes.subject = async ([key]) => {
  await loadSubjects();
  const s = subj(key); if (!s) { app.innerHTML = `<div class="card">No such subject. <a href="#/">Home</a></div>`; return; }
  const [lm, today] = await Promise.all([api("/api/learnmap?subject=" + key), api("/api/today?subject=" + key)]);
  await loadIndex();
  const mine = INDEX.filter(p => p.domains.includes(key));
  const sm = lm.summary;
  const empty = !mine.length;
  app.innerHTML = `
  <div class="subject-head" style="--sc:${s.color}"><span class="sc-ico big">${esc(s.icon)}</span>
    <div style="flex:1"><div class="small muted"><a href="#/">Home</a> › Subject</div><h1 style="margin:0">${esc(s.name)}</h1><p class="muted" style="margin:.2em 0">${esc(s.description)}</p></div>
    ${empty ? "" : ring(s.progress, s.color, 92, "", 9)}</div>
  ${empty ? `<div class="card onboard"><h2 style="margin-top:0">A fresh subject, ready for its first source</h2>
    <p>Add a few articles, a PDF, a lecture video or your own notes about <b>${esc(s.name)}</b>. Claude reads them, proposes pages with cited evidence, and you approve. Then this page fills with a learning map, flashcards and a tutor.</p>
    <ol class="steps"><li><b>Add</b> a link, file or pasted text</li><li><b>Digest</b> it into proposed pages</li><li><b>Review</b> and approve what you agree with</li><li><b>Learn</b> with the map, playgrounds and tutor</li></ol>
    <a class="btn" href="#/add">Add the first source →</a></div>` : `
  <div class="tiles slim">
    <div class="tile static"><b>${sm.mastered}/${sm.total}</b><span class="muted small">concepts mastered</span></div>
    <div class="tile static"><b>${sm.ready}</b><span class="muted small">ready to learn now</span></div>
    <div class="tile static"><b>${sm.gaps}</b><span class="muted small">need attention</span></div>
    <div class="tile static"><b>${s.due}</b><span class="muted small">cards due</span></div></div>
  <div class="row" style="margin:6px 0 14px"><a class="btn" href="#/learn">Open learning map</a><a class="btn ghost" href="#/add">Add material</a>${today.next[0] ? `<a class="btn ghost" href="#/tutor/${esc(today.next[0].slug)}">Learn: ${esc(today.next[0].title)}</a>` : ""}</div>
  <div class="two-col"><div><h2>Ready to learn</h2><div class="card list">${today.next.map(t => `<a class="item" href="#/tutor/${esc(t.slug)}"><b>${esc(t.title)}</b> ${chip("unlocks " + t.unlocks)}<small>${esc(t.summary)}</small></a>`).join("") || "<span class='muted'>Nothing ready: finish a prerequisite first.</span>"}</div>
    <h2>Open questions</h2><div class="card list">${mine.filter(p => p.type === "question").slice(0, 6).map(p => `<a class="item" href="#/page/${esc(p.slug)}">${esc(p.title)}</a>`).join("") || "<span class='muted'>None yet.</span>"}</div></div>
  <div><h2>Key claims</h2><div class="card list">${mine.filter(p => p.type === "claim").slice(0, 6).map(p => `<a class="item" href="#/page/${esc(p.slug)}"><b>${esc(p.title)}</b></a>`).join("") || "<span class='muted'>None yet.</span>"}</div>
    <h2>Sources</h2><div class="card list">${mine.filter(p => p.type === "source").slice(0, 8).map(p => `<a class="item" href="#/page/${esc(p.slug)}">${esc(p.title)}</a>`).join("") || "<span class='muted'>None yet.</span>"}</div></div></div>`}`;
};

// ================================================================ LIBRARY + PAGE
routes.library = async () => {
  await loadIndex();
  const types = [...new Set(INDEX.map(p => p.type))];
  app.innerHTML = `<h1>Library ${SUBJECT ? subjectChip(SUBJECT) : ""}</h1>
  <div class="row"><select id="f-type" style="width:auto"><option value="">All types</option>${types.map(t => `<option>${t}</option>`).join("")}</select>
  <select id="f-status" style="width:auto"><option value="">Any status</option><option>stub</option><option>draft</option><option>reviewed</option></select>
  <input id="f-q" type="text" placeholder="Filter by title…" style="flex:1;min-width:160px"></div>
  <div class="card list" id="lib"></div>`;
  const draw = () => {
    const t = $("#f-type").value, s = $("#f-status").value, q = $("#f-q").value.toLowerCase();
    const r = INDEX.filter(p => inSubject(p) && (!t || p.type === t) && (!s || p.status === s) && (!q || p.title.toLowerCase().includes(q)));
    $("#lib").innerHTML = r.map(p => `<a class="item" href="#/page/${esc(p.slug)}">${chip(p.type)}<b>${esc(p.title)}</b> ${statusChip(p.status)}${p.domains.map(d => subjectChip(d)).join("")}<small>${esc(p.summary)}</small></a>`).join("") || "<div class='muted' style='padding:12px'>No matches.</div>";
  };
  ["f-type", "f-status", "f-q"].forEach(i => $("#" + i).addEventListener("input", draw)); draw();
};

routes.page = async ([slug]) => {
  if (!INDEX.length) await loadIndex();
  if (!SUBJECTS.length) await loadSubjects();
  const d = await api("/api/page/" + encodeURIComponent(slug));
  const f = d.fm, isConcept = f.type === "concept";
  const play = isConcept ? (await api("/api/playground/" + d.slug)).exists : false;
  const groups = {};
  d.relations.forEach(r => (groups[r.rel] ||= []).push(r));
  d.incoming.forEach(r => (groups["← " + r.rel] ||= []).push(r));
  const relHtml = Object.entries(groups).map(([k, v]) => `<div class="small muted" style="margin-top:8px">${esc(k.replace(/_/g, " "))}</div>` + v.map(r => r.slug ? `<div><a href="#/page/${esc(r.slug)}">${esc(r.title)}</a> ${chip(r.type)}</div>` : `<div class="muted">${esc(r.title)} (no page yet)</div>`).join("")).join("");
  const cites = d.citations.map(c => `<div class="cite"><a href="#/source/${esc(c.id)}?loc=${encodeURIComponent(c.locator || "")}&q=${encodeURIComponent(c.quote || "")}"><b>${esc(c.title)}</b></a> ${chip(c.reliability || "")}<div class="small muted">at ${esc(c.locator || "—")}</div>${c.quote ? `<q>${esc(c.quote)}</q>` : ""}</div>`).join("");
  app.innerHTML = `<div class="layout"><div>
    <div class="small muted"><a href="#/library">Library</a> › ${esc(f.type)}</div>
    <h1>${esc(f.title)}</h1>
    <div>${chip(f.type)}${statusChip(f.status)}${confChip(f.confidence)}${f.domains.map(x => subjectChip(x)).join("")}${f.verdict ? chip("verdict: " + f.verdict) : ""}${f.state ? chip(f.state) : ""}</div>
    <p class="muted">${esc(f.summary)}</p>
    ${isConcept ? `<div class="actions"><a class="btn" href="#/tutor/${esc(d.slug)}">🧭 Teach me</a><a class="btn ghost" href="#/cmap/${esc(d.slug)}">🕸 Concept map</a>${play ? `<a class="btn ghost" href="#/play/${esc(d.slug)}">🎛 Playground</a>` : `<a class="btn ghost" href="#/play/${esc(d.slug)}">🎛 Make a playground</a>`}<a class="btn ghost" href="#/build/${esc(d.slug)}">🛠 Build it</a></div>
      <div class="selfrate"><span class="small muted">My level</span> ${[0, 1, 2, 3, 4, 5].map(n => `<button class="lvl ${d.mastery === n ? "sel" : ""}" data-n="${n}" title="${["Unseen", "Recognise it", "Explain with help", "Explain alone (mastered)", "Handle variations", "Could teach it"][n]}">${n}</button>`).join("")}</div>` : ""}
    <div class="prose" id="body">${md(d.body.replace(/^\s*# .*\n/, ""))}</div></div>
    <aside>
      <div class="card"><b>Evidence</b>${cites || "<div class='muted small'>No sources cited yet (stub or author-originated).</div>"}</div>
      <div class="card"><b>Connections</b>${relHtml || "<div class='muted small'>None yet.</div>"}</div>
      <div class="card small muted">id ${esc(f.id)}<br>created ${esc(f.created)} · updated ${esc(f.updated)}</div>
    </aside></div>`;
  $$(".lvl").forEach(b => b.onclick = async () => { await post("/api/tutor/record", { page_id: f.id, level: +b.dataset.n, note: "self-rated" }); $$(".lvl").forEach(x => x.classList.toggle("sel", x === b)); toast(`Level ${b.dataset.n} recorded.`); });
  renderMermaid($("#body"));
};

// ================================================================ SOURCE READER with annotations
const COLORS = ["yellow", "green", "pink", "blue"];
routes.source = async ([sid], qs) => {
  const [s, annos] = await Promise.all([api("/api/source/" + encodeURIComponent(sid)), api("/api/annotations/" + encodeURIComponent(sid))]);
  const loc = qs.get("loc") || "", q = qs.get("q") || "";
  const text = s.text;
  let cite = null;
  if (q) {
    const words = q.trim().split(/\s+/).map(w => w.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"));
    const m = new RegExp(words.join("\\s+"), "i").exec(text); if (m) cite = { start: m.index, end: m.index + m[0].length };
  } else {
    const ts = loc.match(/^(\d\d:\d\d)/), pg = loc.match(/p\.?\s*(\d+)/i);
    const idx = ts ? text.indexOf(`**[${ts[1]}]**`) : pg ? text.indexOf(`<!-- page ${pg[1]} -->`) : -1;
    if (idx >= 0) cite = { start: idx, end: idx + (ts ? 8 : 16) };
  }
  app.innerHTML = `<div class="small muted"><a href="javascript:history.back()">← back</a></div>
  <h1>${esc(s.title)}</h1>
  <div>${chip(s.kind || "")}${chip(s.reliability || "")}${s.author ? chip(s.author) : ""}${s.published ? chip(s.published) : ""}</div>
  <p>${s.url ? `<a href="${esc(s.url)}" target="_blank" rel="noopener noreferrer">Open original</a>` : ""} <span class="muted small">${esc(s.raw || "")}</span></p>
  ${cite ? `<div class="card small">Showing the cited passage${loc ? ` (${esc(loc)})` : ""}. <b>Select any text</b> to highlight it or add a note.</div>` : `<div class="card small"><b>Select any text</b> to highlight it or add a note. Highlights are saved with this source.</div>`}
  <div class="reader-layout"><div class="reader" id="reader"></div><aside><div class="card"><b>My notes</b><div id="annos"></div></div></aside></div>
  <div id="selbar" class="selbar" hidden>${COLORS.map(c => `<button class="dot ${c}" data-c="${c}" title="Highlight ${c}"></button>`).join("")}<button class="ghost" id="sel-note">Add note</button></div>`;
  let items = annos.slice();
  const draw = () => {
    const marks = items.map(a => ({ ...a, cls: "ann " + a.color })).sort((a, b) => a.start - b.start);
    if (cite && !marks.some(m => !(cite.end <= m.start || cite.start >= m.end))) marks.push({ start: cite.start, end: cite.end, cls: "hl", id: "cite" });
    marks.sort((a, b) => a.start - b.start);
    let html = "", pos = 0;
    for (const m of marks) { if (m.start < pos) continue; html += esc(text.slice(pos, m.start)) + `<mark class="${m.cls}" data-id="${m.id}"${m.id === "cite" ? ' id="hit"' : ""}>${esc(text.slice(m.start, m.end))}</mark>`; pos = m.end; }
    $("#reader").innerHTML = html + esc(text.slice(pos));
    $("#annos").innerHTML = items.length ? items.sort((a, b) => a.start - b.start).map(a => `<div class="anno ${a.color}" data-id="${a.id}"><q>${esc(a.text.slice(0, 120))}${a.text.length > 120 ? "…" : ""}</q><textarea placeholder="Add a note…" data-id="${a.id}">${esc(a.note)}</textarea><button class="ghost del" data-id="${a.id}">Remove</button></div>`).join("") : `<div class="muted small">No highlights yet.</div>`;
    $$("#annos textarea").forEach(t => t.onchange = () => post(`/api/annotations/${sid}/${t.dataset.id}/note`, { note: t.value }).then(() => toast("Note saved.", 1500)));
    $$("#annos .del").forEach(b => b.onclick = async () => { await post(`/api/annotations/${sid}/${b.dataset.id}/delete`); items = items.filter(x => x.id !== b.dataset.id); draw(); });
    $$("#annos .anno q").forEach(el => el.onclick = () => { const m = $(`#reader mark[data-id="${el.parentElement.dataset.id}"]`); m && m.scrollIntoView({ block: "center", behavior: "smooth" }); });
  };
  draw();
  const hit = $("#hit"); if (hit) hit.scrollIntoView({ block: "center" });
  let sel = null;
  const reader = $("#reader"), bar = $("#selbar");
  const offsets = () => {
    const r = getSelection(); if (!r.rangeCount) return null; const rg = r.getRangeAt(0); if (!reader.contains(rg.commonAncestorContainer) || rg.collapsed) return null;
    const pre = document.createRange(); pre.selectNodeContents(reader); pre.setEnd(rg.startContainer, rg.startOffset);
    const start = pre.toString().length; return { start, end: start + rg.toString().length, rect: rg.getBoundingClientRect() };
  };
  reader.addEventListener("mouseup", () => { setTimeout(() => { sel = offsets(); if (!sel || sel.end - sel.start < 2) { bar.hidden = true; return; } bar.hidden = false; bar.style.top = window.scrollY + sel.rect.top - 46 + "px"; bar.style.left = Math.max(8, sel.rect.left + sel.rect.width / 2 - 100) + "px"; }, 0); });
  const add = async (color, note = "") => { if (!sel) return; try { const a = await post("/api/annotations/" + sid, { start: sel.start, end: sel.end, color, note }); items.push(a); bar.hidden = true; getSelection().removeAllRanges(); draw(); if (note === "") toast("Highlighted."); } catch (e) { toast(e.message.includes("overlap") ? "That passage overlaps an existing highlight." : e.message, 4000); } };
  $$(".dot", bar).forEach(b => b.onmousedown = e => { e.preventDefault(); add(b.dataset.c); });
  $("#sel-note").onmousedown = async e => { e.preventDefault(); const n = prompt("Your note on this passage:"); if (n !== null) await add("yellow", n); };
  document.addEventListener("mousedown", function h(e) { if (!document.body.contains(bar)) return document.removeEventListener("mousedown", h); if (!e.target.closest("#selbar") && !e.target.closest("#reader")) bar.hidden = true; });
  onLeave(() => bar.remove());
};

// ================================================================ ADD (intake + digest)
routes.add = async () => {
  const subjOpts = `<option value="">Let Claude decide</option>` + SUBJECTS.map(s => `<option value="${esc(s.key)}" ${s.key === SUBJECT ? "selected" : ""}>${esc(s.icon)} ${esc(s.name)}</option>`).join("");
  app.innerHTML = `<h1>Add material</h1>
  <p class="muted">Bring anything in: files, exports, links or pasted text. It is saved as an untouched source first; then you choose when to turn it into proposed knowledge. Nothing enters your vault until you approve it.</p>
  <div class="card"><b>Files</b> <span class="muted small">PDF, Word, HTML, Markdown, text, ChatGPT/Claude export (.json)</span>
    <div class="dropzone" id="dz">Drop files here or <a href="#" id="pick">choose files</a><input type="file" id="fi" multiple hidden></div></div>
  <div class="card"><b>Links</b> <span class="muted small">web pages and YouTube, one per line</span>
    <textarea id="links" placeholder="https://…"></textarea><div class="row" style="margin-top:8px"><button id="go-links">Add links</button></div></div>
  <div class="card"><b>Paste text</b> <span class="muted small">a chat, notes or a document</span>
    <div class="row" style="margin:6px 0"><input type="text" id="t-title" placeholder="Title" style="flex:1"><select id="t-kind" style="width:auto"><option value="chat">AI chat</option><option value="document">Document</option></select></div>
    <textarea id="t-text" placeholder="Paste here…"></textarea><div class="row" style="margin-top:8px"><button id="go-text">Add text</button></div></div>
  <h2>Ready to digest</h2><div id="und"></div>
  <h2>Activity</h2><div id="jobs"></div>`;
  const upload = async files => { const fd = new FormData(); [...files].forEach(f => fd.append("files", f)); const r = await kbFetch("/api/intake/files", { method: "POST", headers: {}, body: fd }); if (!r.ok) { toast("Upload failed: " + await errorText(r), 6000); return; } toast("Uploading and converting…"); drawJobs(); };
  const dz = $("#dz"); $("#pick").onclick = e => { e.preventDefault(); $("#fi").click(); }; $("#fi").onchange = e => upload(e.target.files);
  dz.ondragover = e => { e.preventDefault(); dz.classList.add("over"); }; dz.ondragleave = () => dz.classList.remove("over");
  dz.ondrop = e => { e.preventDefault(); dz.classList.remove("over"); upload(e.dataTransfer.files); };
  $("#go-links").onclick = ev => busy(ev.target, async () => { const urls = $("#links").value.split(/\s+/).filter(Boolean); await post("/api/intake/links", { urls }); $("#links").value = ""; toast("Fetching…"); drawJobs(); });
  $("#go-text").onclick = ev => busy(ev.target, async () => { await post("/api/intake/text", { text: $("#t-text").value, title: $("#t-title").value, kind: $("#t-kind").value }); $("#t-text").value = ""; toast("Saved."); drawJobs(); });
  const drawUnd = async () => {
    const u = await api("/api/undigested"); const box = $("#und");
    if (!u.length) { box.innerHTML = "<div class='card muted'>Everything you have added has been digested.</div>"; return; }
    if (box.dataset.n === String(u.length)) return; box.dataset.n = u.length;
    box.innerHTML = `<div class="card list">${u.map(s => `<label class="item" style="display:flex;gap:10px;align-items:flex-start"><input type="checkbox" class="und" value="${esc(s.path)}"><span><b>${esc(s.title)}</b> ${chip(s.kind)} ${chip(Math.round(s.size / 1024) + " KB")}<small>${esc(s.path)}</small></span></label>`).join("")}
      <div class="row" style="padding:10px"><button id="sel-all" class="ghost">Select all</button><label class="small">Subject <select id="d-subj" style="width:auto">${subjOpts}</select></label><button id="digest">Digest selected → propose pages</button><span class="muted small">Takes a few minutes and uses your Claude plan.</span></div></div>`;
    $("#sel-all").onclick = () => $$(".und").forEach(c => c.checked = true);
    $("#digest").onclick = ev => busy(ev.target, async () => { const paths = $$(".und:checked").map(c => c.value); if (!paths.length) { toast("Select at least one source."); return; } const r = await post("/api/digest", { paths, subject: $("#d-subj").value }); toast("Digesting into " + r.batch + "…"); drawJobs(); });
  };
  const drawJobs = async () => {
    const js = await api("/api/jobs"); const box = $("#jobs");
    const open = new Set($$("details[open]", box).map(d => d.dataset.id));
    box.innerHTML = js.length ? js.map(j => `<details class="card" data-id="${j.id}" ${open.has(j.id) || j.status === "running" ? "open" : ""}><summary>${chip(j.kind)} <b>${esc(j.title)}</b> ${chip(j.status, j.status === "done" ? "ok" : j.status === "failed" ? "bad" : "warn")} ${j.result && j.result.batch ? `<a href="#/review">review ${esc(j.result.batch)} →</a>` : ""}</summary><div class="log" id="log-${j.id}">…</div></details>`).join("") : "<div class='card muted'>No activity yet.</div>";
    for (const j of js.slice(0, 6)) { const d = await api("/api/jobs/" + j.id); const l = $("#log-" + j.id); if (l) l.textContent = d.log.slice(-60).join("\n") || "(no output yet)"; }
    drawUnd();
  };
  drawJobs(); every(drawJobs, 3000);
};

// ================================================================ REVIEW
routes.review = async () => {
  const props = await api("/api/proposals");
  app.innerHTML = `<h1>Review</h1><p class="muted">Everything the AI proposed waits here. Read it, then approve. Approving moves pages into your vault and rebuilds search and the maps.</p>` +
    (props.length ? "" : "<div class='card muted'>Nothing to review. Add material, then digest it.</div>");
  for (const p of props) {
    const div = document.createElement("div"); div.className = "card";
    const amend = p.has_amendments;
    div.innerHTML = `<h3>${esc(p.batch)} ${p.ok ? chip("valid", "ok") : chip("has errors", "bad")} ${amend ? chip("changes existing pages", "warn") : ""}</h3>
      ${p.errors.length ? `<div class="log" style="color:var(--bad)">${p.errors.map(esc).join("\n")}</div>` : ""}
      ${p.warnings.length ? `<div class="small muted">${p.warnings.length} warning(s): ${esc(p.warnings.slice(0, 3).join("; "))}</div>` : ""}
      <div class="list">${p.files.map(f => `<a class="item" href="#" data-name="${esc(f.name)}">${chip(f.action, f.action === "amend" ? "warn" : "ok")}${chip(f.type)}<b>${esc(f.title)}</b><small>${esc(f.name)}</small></a><div class="fv" hidden></div>`).join("")}</div>
      <div class="row" style="margin-top:10px">
        ${amend ? `<label class="small"><input type="checkbox" class="ack"> I reviewed the diffs of the pages that change</label>` : ""}
        <button class="ap" ${p.ok ? "" : "disabled"}>Approve</button><button class="ghost ds">Discard batch</button></div>`;
    app.appendChild(div);
    $$(".item", div).forEach(a => a.onclick = async e => {
      e.preventDefault(); const box = a.nextElementSibling; if (!box.hidden) { box.hidden = true; return; }
      const d = await api(`/api/proposals/${encodeURIComponent(p.batch)}/file/${encodeURIComponent(a.dataset.name)}`);
      if (d.action === "amend") box.innerHTML = `<div class="diff">${d.diff.split("\n").map(l => `<div class="${l[0] === "+" ? "a" : l[0] === "-" ? "d" : ""}">${esc(l)}</div>`).join("")}</div>`;
      else box.innerHTML = `<div class="card prose small">${md(d.text.replace(/^---[\s\S]*?---\n/, ""))}</div>`;
      box.hidden = false; renderMermaid(box);
    });
    $(".ap", div).onclick = ev => busy(ev.target, async () => {
      if (amend && !$(".ack", div).checked) { toast("Tick the box to confirm you reviewed the changed pages."); return; }
      const r = await post(`/api/proposals/${encodeURIComponent(p.batch)}/approve`, { amend });
      if (!r.ok) { toast("Not approved: " + (r.errors || [])[0], 7000); return; }
      toast(`Approved: ${r.log.length} page(s) now in your vault.`); await loadIndex(); await loadSubjects(); routes.review();
    });
    $(".ds", div).onclick = ev => { if (confirm("Discard this proposal batch? The raw sources stay; only the AI's draft pages are deleted.")) busy(ev.target, async () => { await post(`/api/proposals/${encodeURIComponent(p.batch)}/discard`); routes.review(); }); };
  }
};

// ================================================================ STUDY (active recall + spaced repetition)
routes.study = async () => {
  const all = await api("/api/cards/due?n=60");
  const cards = all.filter(c => !SUBJECT || c.domains.includes(SUBJECT)).slice(0, 20);
  if (!cards.length) { app.innerHTML = `<h1>Study Flashcards</h1><div class="card center"><div style="font-size:42px">🎉</div><b>Nothing due${SUBJECT ? " in this subject" : ""}.</b><p class="muted">Cards come back on a schedule that adapts to how well you remember them. Try the tutor to learn something new.</p><a class="btn" href="#/learn">Open learning map</a></div>`; return; }
  let i = 0, shown = false, correct = 0, mine = "";
  const key = e => { if (!app.querySelector(".flash")) return; if (e.target.tagName === "TEXTAREA") { if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) reveal(); return; } if (!shown && (e.key === " " || e.key === "Enter")) { e.preventDefault(); reveal(); } else if (shown && "1234".includes(e.key)) grade([0, 2, 4, 5][+e.key - 1]); };
  document.addEventListener("keydown", key); onLeave(() => document.removeEventListener("keydown", key));
  const reveal = () => { mine = ($("#mine") || {}).value || ""; shown = true; draw(); };
  const grade = async g => { await post("/api/cards/grade", { id: cards[i].id, grade: g }); if (g >= 3) correct++; i++; shown = false; mine = ""; draw(); refreshBadges(); };
  const draw = () => {
    if (i >= cards.length) { app.innerHTML = `<h1>Study Flashcards</h1><div class="card center"><div style="font-size:42px">✨</div><h2 style="margin:.2em">Session complete</h2><p>${correct} of ${cards.length} recalled well. Hard cards will come back sooner.</p><div class="row" style="justify-content:center"><a class="btn" href="#/">Home</a><a class="btn ghost" href="#/learn">Learning map</a></div></div>`; return; }
    const c = cards[i];
    app.innerHTML = `<div class="row"><h1 style="margin:0;flex:1">Study Flashcards</h1><span class="muted small">${i + 1} / ${cards.length}</span></div>
      <div class="progress"><i style="width:${i / cards.length * 100}%"></i></div>
      <div class="small muted" style="margin-top:10px">${esc(c.page)} ${c.domains.map(subjectChip).join("")}</div>
      <div class="flash"><div class="q">${esc(c.q)}</div>
        ${shown ? `${mine ? `<div class="mine small"><span class="muted">You said:</span> ${esc(mine)}</div>` : ""}<hr><div class="a">${esc(c.a)}</div>` : `<textarea id="mine" placeholder="Try to answer from memory first (optional, but it makes it stick). Ctrl+Enter to reveal."></textarea>`}</div>
      <div class="row" style="margin-top:12px;justify-content:center">${shown ? [["Blank", 0, "1"], ["Hard", 2, "2"], ["Good", 4, "3"], ["Easy", 5, "4"]].map(([l, g, k]) => `<button class="${g < 3 ? "ghost" : ""}" data-g="${g}">${l} <kbd>${k}</kbd></button>`).join("") : `<button id="rev">Show answer <kbd>Space</kbd></button>`}</div>`;
    if (!shown) { $("#rev").onclick = reveal; $("#mine").focus(); } else $$("[data-g]").forEach(b => b.onclick = () => grade(+b.dataset.g));
  };
  draw();
};

// ================================================================ TUTOR
routes.tutor = async ([slug]) => {
  if (!INDEX.length) await loadIndex();
  if (!slug) {
    const t = await api("/api/today?subject=" + encodeURIComponent(SUBJECT));
    app.innerHTML = `<h1>Socratic tutor ${SUBJECT ? subjectChip(SUBJECT) : ""}</h1><p class="muted">The tutor asks questions instead of lecturing, grounded in your vault and your history. It uses Claude Code, so each reply takes a few seconds.</p>
    <h2>Ready to learn</h2><div class="card list">${t.next.map(x => `<a class="item" href="#/tutor/${esc(x.slug)}"><b>${esc(x.title)}</b> ${chip("unlocks " + x.unlocks)}<small>${esc(x.summary)}</small></a>`).join("") || "<span class='muted'>None ready.</span>"}</div>
    <h2>Or pick any concept</h2><input id="tq" type="text" placeholder="Filter concepts…"><div class="card list" id="tl"></div>`;
    const draw = () => { const q = $("#tq").value.toLowerCase(); $("#tl").innerHTML = INDEX.filter(p => p.type === "concept" && inSubject(p) && p.title.toLowerCase().includes(q)).slice(0, 60).map(p => `<a class="item" href="#/tutor/${esc(p.slug)}"><b>${esc(p.title)}</b> ${statusChip(p.status)}</a>`).join(""); };
    $("#tq").oninput = draw; draw(); return;
  }
  const playInfo = await api("/api/playground/" + slug);
  app.innerHTML = `<div class="small muted"><a href="#/tutor">← topics</a></div><div class="row"><h1 style="flex:1">Tutor: ${esc((SLUG[slug] || {}).title || slug)}</h1><a class="btn ghost" href="#/cmap/${esc(slug)}">🕸 Map</a>${playInfo.exists ? `<a class="btn ghost" href="#/play/${esc(slug)}">🎛 Playground</a>` : ""}</div>
    <div class="chat" id="chat"><div class="msg ai muted">Starting the session…</div></div>
    <div class="row"><textarea id="ans" placeholder="Your answer (Ctrl+Enter to send)" style="flex:1;min-height:70px" disabled></textarea></div>
    <div class="row" style="margin-top:8px"><button id="send" disabled>Send</button><button id="end" class="ghost" disabled>End session &amp; record my level</button></div><div id="result"></div>`;
  const chat = $("#chat"); let sid = null;
  const add = (who, text) => { const d = document.createElement("div"); d.className = "msg " + who; d.innerHTML = who === "ai" ? md(text) : `<p>${esc(text)}</p>`; chat.appendChild(d); d.scrollIntoView({ block: "end" }); renderMermaid(d); return d; };
  const lock = on => ["ans", "send", "end"].forEach(i => $("#" + i).disabled = on);
  try { const r = await post("/api/tutor/start", { page: slug }); sid = r.session; chat.innerHTML = ""; add("ai", r.reply); lock(false); $("#ans").focus(); }
  catch (e) { chat.innerHTML = `<div class="card">Could not start the tutor: ${esc(e.message)}</div>`; return; }
  const send = async () => {
    const t = $("#ans").value.trim(); if (!t) return; $("#ans").value = ""; add("me", t); lock(true); const wait = add("ai", "…");
    try { const r = await post("/api/tutor/message", { session: sid, text: t }); wait.remove(); add("ai", r.reply); } catch (e) { wait.remove(); toast("Tutor error: " + e.message, 6000); }
    lock(false); $("#ans").focus();
  };
  $("#send").onclick = send; $("#ans").addEventListener("keydown", e => { if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) send(); });
  $("#end").onclick = async () => {
    lock(true); $("#result").innerHTML = "<div class='card muted'>Assessing your session…</div>";
    try {
      const r = await post("/api/tutor/end", { session: sid });
      if (r.ok) { const a = r.assessment; $("#result").innerHTML = `<div class="card"><b>Level ${a.level}/5</b> ${a.level >= 3 ? chip("mastered 🎉", "ok") : ""}<br>${esc(a.note || "")}${(a.misconceptions || []).length ? `<br><span class="muted small">To revisit: ${esc(a.misconceptions.join("; "))}</span>` : ""}<div class="row" style="margin-top:10px"><a class="btn" href="#/build/${esc(slug)}">🛠 Build something with it</a><a class="btn ghost" href="#/learn">Learning map</a><a class="btn ghost" href="#/tutor">Another topic</a></div></div>`; refreshBadges(); }
      else { $("#result").innerHTML = `<div class="card">I could not read the assessment. Pick your level (0–5) to record: ${[0, 1, 2, 3, 4, 5].map(n => `<button class="ghost lv" data-n="${n}">${n}</button>`).join(" ")}</div>`; $$(".lv").forEach(b => b.onclick = async () => { await post("/api/tutor/record", { page_id: r.page_id, level: +b.dataset.n }); toast("Recorded."); location.hash = "#/"; }); }
    } catch (e) { $("#result").innerHTML = ""; toast("Error: " + e.message, 6000); lock(false); }
  };
};

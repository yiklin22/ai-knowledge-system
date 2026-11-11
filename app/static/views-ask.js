"use strict";
// Ask: questions answered from your own sources, with a scope picker and clickable citations.
const ASK_KINDS = [["web", "Web pages"], ["videos", "Videos"], ["documents", "Documents"], ["chats", "AI chats"]];
let ASK_HISTORY = []; // [{q, a}] kept for follow-ups; cleared with the button or when you leave the app

routes.ask = async () => {
  const sources = await api("/api/ask/sources");
  const count = k => sources.filter(s => s.kind === k).length;
  const saved = JSON.parse(store.get("kb-ask-scope", "null") || "null") || { vault: true, kinds: ASK_KINDS.map(k => k[0]) };
  const picked = new Set();
  app.innerHTML = `<h1>Ask your sources</h1>
  <p class="muted">Ask anything, e.g. <i>what is an agent harness?</i> Claude answers only from the passages found in the sources you select, cites them as [1], [2]…, and says what is missing. Approved vault pages are ranked above raw sources.</p>
  <div class="card">
    <b>Look in</b>
    <div class="row" style="flex-wrap:wrap;gap:6px 16px;margin:8px 0">
      <label><input type="checkbox" id="sc-vault" ${saved.vault ? "checked" : ""}> Approved vault</label>
      ${ASK_KINDS.map(([k, n]) => `<label><input type="checkbox" class="sc-kind" value="${k}" ${saved.kinds.includes(k) ? "checked" : ""}> ${n} <span class="muted small">(${count(k)})</span></label>`).join("")}
    </div>
    <details id="pick"><summary>Pick specific sources <span class="muted small" id="pick-n">(none: search all selected types)</span></summary>
      <input id="pick-q" type="text" placeholder="Filter ${sources.length} sources…" style="margin:8px 0">
      <div class="card list" id="pick-list" style="max-height:240px;overflow:auto"></div>
      <button class="ghost" id="pick-clear">Clear selection</button>
    </details>
  </div>
  <div class="chat" id="chat"></div>
  <div class="row"><textarea id="q" placeholder="Your question (Ctrl+Enter to send)" style="flex:1;min-height:70px"></textarea></div>
  <div class="row" style="margin-top:8px"><button id="go">Ask</button><button class="ghost" id="clear">New conversation</button></div>`;

  const drawPick = () => {
    const f = $("#pick-q").value.toLowerCase();
    $("#pick-list").innerHTML = sources.filter(s => s.title.toLowerCase().includes(f)).slice(0, 200).map(s =>
      `<label class="item" style="display:flex;gap:8px;align-items:flex-start"><input type="checkbox" class="pk" value="${esc(s.path)}" ${picked.has(s.path) ? "checked" : ""}><span>${esc(s.title)} ${chip(s.kind)}</span></label>`).join("") || "<span class='muted'>No match</span>";
    $("#pick-n").textContent = picked.size ? `(${picked.size} selected: only these are searched)` : "(none: search all selected types)";
  };
  $("#pick-list").addEventListener("change", e => { if (e.target.classList.contains("pk")) { e.target.checked ? picked.add(e.target.value) : picked.delete(e.target.value); drawPick(); } });
  $("#pick-q").oninput = drawPick;
  $("#pick-clear").onclick = () => { picked.clear(); drawPick(); };
  drawPick();

  const scope = () => ({ vault: $("#sc-vault").checked, kinds: $$(".sc-kind").filter(c => c.checked).map(c => c.value), paths: [...picked] });
  const chat = $("#chat");
  const add = (who, html) => { const d = document.createElement("div"); d.className = "msg " + who; d.innerHTML = html; chat.appendChild(d); d.scrollIntoView({ block: "end" }); return d; };

  function showSource(s) {
    const isVault = s.kind === "vault";
    const slug = s.path.split("/").pop().replace(/\.md$/, "");
    openDialog(`<h2 style="margin-top:0">${esc(s.title)}</h2>${chip(isVault ? "approved vault page" : s.kind + " source")} ${s.locator ? chip(s.locator) : ""}
      <p style="white-space:pre-wrap">${esc(s.snippet)}</p>
      <div class="row">${isVault ? `<a class="btn ghost" href="#/page/${esc(slug)}">Open page</a>` : `<button class="ghost" id="full">Show full source</button>`}</div><div id="full-box"></div>`, d => {
      const b = $("#full", d);
      if (b) b.onclick = async () => { b.disabled = true; try { const r = await api("/api/raw?path=" + encodeURIComponent(s.path)); $("#full-box", d).innerHTML = `<pre style="white-space:pre-wrap;max-height:50vh;overflow:auto">${esc(r.text)}</pre>`; } catch (e) { toast(e.message); } };
    });
  }

  const send = async () => {
    const question = $("#q").value.trim(); if (!question) return;
    const sc = scope();
    if (!sc.vault && !sc.kinds.length) { toast("Select at least one place to look."); return; }
    store.set("kb-ask-scope", JSON.stringify({ vault: sc.vault, kinds: sc.kinds }));
    $("#q").value = ""; add("me", `<p>${esc(question)}</p>`);
    $("#go").disabled = true; const wait = add("ai muted", "Searching your sources…");
    try {
      const r = await post("/api/ask", { question, ...sc, history: ASK_HISTORY });
      wait.remove();
      const body = md(r.answer).replace(/\[(\d{1,2})\]/g, (m, n) => r.sources.some(s => s.n == n) ? `<a href="#" class="ask-cite" data-n="${n}">[${n}]</a>` : m);
      const list = r.sources.length ? `<details style="margin-top:8px"><summary class="small muted">${r.sources.length} passages used</summary>${r.sources.map(s => `<div class="small"><a href="#" class="ask-cite" data-n="${s.n}">[${s.n}]</a> ${esc(s.title)} ${chip(s.kind)} ${s.locator ? chip(s.locator) : ""}</div>`).join("")}</details>` : "";
      const d = add("ai", body + list);
      d.addEventListener("click", e => { const a = e.target.closest("a.ask-cite"); if (!a) return; e.preventDefault(); showSource(r.sources.find(s => s.n == a.dataset.n)); });
      renderMermaid(d);
      if (r.grounded) ASK_HISTORY.push({ q: question, a: r.answer });
    } catch (e) { wait.remove(); toast("Ask failed: " + e.message, 6000); }
    $("#go").disabled = false; $("#q").focus();
  };
  $("#go").onclick = send;
  $("#q").addEventListener("keydown", e => { if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) send(); });
  $("#clear").onclick = () => { ASK_HISTORY = []; chat.innerHTML = ""; };
  $("#q").focus();
};

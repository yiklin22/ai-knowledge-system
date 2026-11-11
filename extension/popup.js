const $ = id => document.getElementById(id);
const say = (t, cls = "") => { $("msg").textContent = t; $("msg").className = cls; };

async function init() {
  const { key, digest } = await chrome.storage.local.get({ key: "", digest: true });
  $("digest").checked = digest;
  $("setup").hidden = !!key;
  $("main").hidden = !key;
  const r = await chrome.runtime.sendMessage({ type: "ping" });
  if (!r.ok) say(r.error, "err");
}

$("savekey").onclick = async () => {
  const key = $("key").value.trim();
  if (!key) return;
  await chrome.storage.local.set({ key });
  init();
};
$("digest").onchange = () => chrome.storage.local.set({ digest: $("digest").checked });

for (const [id, mode] of [["page", "page"], ["sel", "selection"]]) {
  $(id).onclick = async () => {
    say("Sending…");
    const r = await chrome.runtime.sendMessage({ type: "clip", mode });
    if (r.ok) { say("Sent. You will get a notification when it is done.", "ok"); setTimeout(() => window.close(), 1200); }
    else say(r.error, "err");
  };
}
init();

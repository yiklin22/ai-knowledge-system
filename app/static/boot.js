"use strict";
// ================================================================ BOOT
Promise.all([loadIndex(), loadSubjects()]).then(route).catch(e => { app.innerHTML = `<div class="card">Could not start: ${esc(e.message)}</div>`; });

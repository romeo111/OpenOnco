"use strict";
(() => {
  const config = JSON.parse(document.getElementById("review-config").textContent);
  const key = `openonco-review:${config.packet_id}:${config.kb_sha256}:${config.engine_sha256}:${config.scenario_sha256}`;
  const status = document.getElementById("save-status");
  const cards = [...document.querySelectorAll("[data-case]")];
  const allowed = new Set(["unreviewed", "acceptable", "needs_changes", "cannot_assess"]);
  let saved = {};
  try { saved = JSON.parse(localStorage.getItem(key) || "{}"); } catch (_) { saved = {}; }
  if (!saved || typeof saved !== "object" || Array.isArray(saved)) saved = {};
  for (const card of cards) {
    const value = saved[card.dataset.case];
    if (!value || typeof value !== "object") continue;
    if (allowed.has(value.assessment)) card.querySelector(".assessment").value = value.assessment;
    if (typeof value.comment === "string") card.querySelector(".comment").value = value.comment.slice(0, 10000);
  }
  function collect() {
    return Object.fromEntries(cards.map(card => [card.dataset.case, {
      assessment: card.querySelector(".assessment").value,
      comment: card.querySelector(".comment").value
    }]));
  }
  function save() {
    try {
      localStorage.setItem(key, JSON.stringify(collect()));
      status.textContent = "Saved in this browser. Export to retain a copy. No upload occurs.";
    } catch (_) {
      status.textContent = "Browser storage unavailable. Use Export to retain your review before leaving this page.";
    }
  }
  for (const card of cards) {
    card.querySelector(".assessment").addEventListener("change", save);
    card.querySelector(".comment").addEventListener("input", save);
  }
  document.getElementById("category").addEventListener("change", event => {
    for (const card of cards) card.hidden = event.target.value !== "all" && card.dataset.category !== event.target.value;
  });
  document.getElementById("export-review").addEventListener("click", () => {
    const data = {schema_version: 1, packet_id: config.packet_id,
      kb_sha256: config.kb_sha256, engine_sha256: config.engine_sha256,
      scenario_sha256: config.scenario_sha256, exported_at: new Date().toISOString(),
      clinical_signoff_granted: false,
      cases: Object.entries(collect()).map(([case_id, entry]) => ({case_id, ...entry}))};
    const url = URL.createObjectURL(new Blob([JSON.stringify(data, null, 2) + "\n"], {type: "application/json"}));
    const link = document.createElement("a");
    link.href = url; link.download = "openonco-dlbcl-1l-review.json";
    document.body.append(link); link.click(); link.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
    status.textContent = "Review exported. These notes do not grant clinical sign-off.";
  });
  document.getElementById("clear-review").addEventListener("click", () => {
    if (!window.confirm("Clear all assessment notes in this browser for this packet? Export first to keep a copy.")) return;
    for (const card of cards) {
      card.querySelector(".assessment").value = "unreviewed";
      card.querySelector(".comment").value = "";
    }
    save();
  });
})();

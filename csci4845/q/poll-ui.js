// Shared rendering for live results (student + presenter views).

function esc(s) {
  return String(s ?? "").replace(/[&<>"']/g,
    c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}

// Multiple choice: one row per choice — label, track+fill, "count · %".
// Bar length is proportional to the largest count; the text carries the exact
// values, so identity and magnitude are never color-alone.
export function renderMC(el, question, responses) {
  const counts = question.choices.map(() => 0);
  for (const r of responses) {
    if (Number.isInteger(r.choice) && r.choice >= 0 && r.choice < counts.length) {
      counts[r.choice]++;
    }
  }
  const total = counts.reduce((a, b) => a + b, 0);
  const max = Math.max(1, ...counts);

  el.innerHTML = question.choices.map((c, i) => {
    const n = counts[i];
    const pct = total ? Math.round((100 * n) / total) : 0;
    const w = total ? (100 * n) / max : 0;
    return `
      <div class="bar-row">
        <div class="bar-label">${esc(c)}</div>
        <div class="bar-line">
          <div class="bar-track"><div class="bar-fill" style="width:${w}%"></div></div>
          <div class="bar-count">${n} · ${pct}%</div>
        </div>
      </div>`;
  }).join("") +
  `<div class="results-total muted">${total === 0
      ? "Waiting for responses…"
      : `${total} response${total === 1 ? "" : "s"}`}</div>`;
}

// Free text: a wall of anonymous cards, newest first.
export function renderTextWall(el, responses) {
  const texts = responses
    .filter(r => (r.text ?? "").trim().length > 0)
    .sort((a, b) => (b.ts?.seconds ?? 0) - (a.ts?.seconds ?? 0));
  if (texts.length === 0) {
    el.innerHTML = `<div class="results-total muted">Waiting for responses…</div>`;
    return;
  }
  el.innerHTML =
    `<div class="wall">${texts.map(r => `<div class="note">${esc(r.text)}</div>`).join("")}</div>` +
    `<div class="results-total muted">${texts.length} response${texts.length === 1 ? "" : "s"}</div>`;
}

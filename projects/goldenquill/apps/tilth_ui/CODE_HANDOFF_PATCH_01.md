# Code Handoff — Patch Set 01

**For:** Claude Code, running in the `tilth_ui` repo.
**Source of findings:** [QA_REPORT.md](./QA_REPORT.md) — items BLK-02, BLK-03, BLK-07. See [qa_findings.json](./qa_findings.json) for evidence.
**Scope:** Three independent CSS/renderer changes. No refactors. No architectural shifts. Aim is review-ready diff in one commit per change, or one squashed commit titled `chore(ui): patch-set-01 — focus-visible, slate contrast, sign-off bullets`.
**Verification:** Existing `scripts/verify-static.mjs --all` must still pass after each change. Visual smoke test: load `/`, `/sign-off/cyc_09F82A`, and `/quarantine` in a browser and confirm focus rings appear on Tab, slate text is more legible, and the sign-off "Lock History Preview" panel no longer shows bullet markers.

---

## Patch 1 of 3 — BLK-03: Add `:focus-visible` site-wide

**Why:** `styles.css` has no focus, focus-visible, or outline rule. Keyboard-only operators have no visible cue for where focus is. WCAG 2.4.7 failure.

**File:** `styles.css`
**Action:** Append the following block to the end of the file (after the existing `@media (max-width: 900px)` block).

```css
:focus-visible {
  outline: 2px solid var(--charcoal);
  outline-offset: 2px;
  border-radius: 4px;
}

/* Pill-shaped chrome elements get a matching outline that follows their shape */
.posture:focus-visible,
.audit-pill:focus-visible,
.epoch-sync:focus-visible,
.signing-chip:focus-visible,
.badge:focus-visible,
.work-count:focus-visible,
.owner-chip:focus-visible {
  outline-offset: 3px;
}

/* Buttons already have rounded corners; don't double the radius */
.button:focus-visible,
.bundle-action:focus-visible {
  outline-offset: 2px;
  border-radius: 4px;
}
```

**Verification:**
- Reload `/` in a browser. Press Tab. The first focusable element should show a 2px charcoal outline with 2px offset.
- Continue tabbing through the sidebar nav items, the workspace-actions dropdown summary, the bundle actions inside it, and the topbar pills. Every interactive element should show a visible outline.
- `node scripts/verify-static.mjs --all` should still pass (no HTML/text content changed).

---

## Patch 2 of 3 — BLK-02: Darken `--slate` to meet WCAG AA on paper/bone

**Why:** Current `--slate: #6c7278` fails WCAG AA-normal on paper (4.32:1) and bone (3.80:1) backgrounds. Used by `.eyebrow`, `.metric span`, `.kv span`, `.inspector-stack span`, `.bundle-action span`, `.metric small`. Visible on every panel header and the sidebar.

**File:** `styles.css`
**Action:** In the `:root` block at the top (currently lines ~1-22), change one variable:

```css
/* before */
--slate: #6c7278;

/* after */
--slate: #5a5f64;
```

**Verified contrast ratios at `#5a5f64`:**

| Surface | Hex | Ratio | AA-normal |
|---|---|---:|:---:|
| paper | `#f5f1e8` | 5.72 | pass |
| bone  | `#eae3d2` | 5.04 | pass |
| surface | `#fffdf7` | 6.34 | pass |

(Computed via WCAG sRGB relative-luminance formula. Script lives at `/tmp/contrast-verify.mjs` in the QA session.)

**Verification:**
- Reload `/` in a browser. The "AVAILABLE FIELD", "WHAT'S NEW TODAY" eyebrows and the metric labels under the totals strip should be visibly darker but not heavy.
- Cross-check `/scout` (inspector labels), `/eligibility/cyc_09F82A` (metric labels), and `/sign-off/cyc_09F82A` (Lock History Preview text).
- `node scripts/verify-static.mjs --all` should still pass.

**Note:** If `#5a5f64` reads as too heavy on the surface backgrounds (some designers prefer keeping a perceptual contrast gap between slate-on-paper and slate-on-surface), `#52575c` is the next step up (6.48 / 5.71 / 7.18). Stop at `#5a5f64` first and look — only deepen if visually warranted.

---

## Patch 3 of 3 — BLK-07: Replace bullet `<ul>` in Sign-Off "Lock History Preview"

**Why:** The Sign-Off Console is the highest-stakes screen. Its right-side "Lock History Preview" panel currently renders the blocker list via `list(blockers)` (a `<ul>` with `<li>` items), producing default browser bullet markers. The rest of the app deliberately avoids bullets — checklists use a grid, audit timelines use dots, gate matrices use bordered rows. The inconsistency reads as unfinished.

**File:** `src/app.mjs`
**Action:** In `renderSignOff()` around line 947, replace the `list(blockers)` call.

**Current code (lines 944-948):**
```js
${panel("Lock History Preview", `
  <p class="mono">last verified: ${esc(data.audit_state.last_verified_event_id)}</p>
  <p>${esc(data.audit_state.unsigned_change_count)} unsigned changes pending.</p>
  ${list(blockers)}
`)}
```

**Replacement code:**
```js
${panel("Lock History Preview", `
  <p class="mono">last verified: ${esc(data.audit_state.last_verified_event_id)}</p>
  <p>${esc(data.audit_state.unsigned_change_count)} unsigned changes pending.</p>
  <div class="blocker-stack">
    ${blockers.map((b) => `<div class="blocker-line"><span class="blocker-marker"></span><span>${esc(b)}</span></div>`).join("")}
  </div>
`)}
```

**File:** `styles.css`
**Action:** Append the following block to the end of the file (after Patch 1 if both are landing together).

```css
.blocker-stack {
  display: grid;
  gap: 6px;
  margin-top: 10px;
}

.blocker-line {
  display: grid;
  grid-template-columns: 10px 1fr;
  align-items: baseline;
  gap: 10px;
  border-left: 3px solid var(--rust);
  padding: 6px 10px;
  background: var(--paper);
  border-radius: 0 4px 4px 0;
  font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  font-size: 0.86rem;
}

.blocker-marker {
  width: 6px;
  height: 6px;
  border-radius: 999px;
  background: var(--rust);
  align-self: center;
}
```

**Verification:**
- Reload `/sign-off/cyc_09F82A`. The right-side "Lock History Preview" panel should show the blocker list as rust-bordered rows with a small rust dot, no `<ul>` bullets.
- The seven blocker strings (E-102 FAIL_CLOSED, Budget validation failed, Judge panel stale, Unsigned changes pending, Linked evidence quarantined, Blocking Red Team hit, Sync conflict — depending on which trigger in current mock data) should render as separate rows.
- `node scripts/verify-static.mjs --all` should still pass — the strings inside are unchanged.

---

## Commit message template

If landing as a single squashed commit:

```
chore(ui): patch-set-01 — focus-visible, slate contrast, sign-off bullets

- Add :focus-visible site-wide outline (WCAG 2.4.7)
- Darken --slate from #6c7278 to #5a5f64 (paper 5.72, bone 5.04, surface 6.34)
- Replace bare <ul> in Sign-Off Lock History Preview with rust-bordered rows

Refs: QA_REPORT.md BLK-02, BLK-03, BLK-07
```

If landing as three separate commits:

```
fix(a11y): add :focus-visible outline site-wide (BLK-03)
fix(a11y): darken --slate to meet WCAG AA on paper and bone (BLK-02)
fix(ui): replace ul bullets with rust-bordered rows in Sign-Off (BLK-07)
```

---

## What is NOT in this patch set (deliberately)

These are real findings but they need a separate, more thoughtful pass:

- **BLK-01 (sign-off checklist drift)** — requires touching `signOffBlockers()` signature. Bigger refactor; handle in patch-set-02.
- **BLK-04 (canonical UI consolidation)** — multi-week product work.
- **BLK-05 (Stitch CDN vendoring)** — separate shell script + repo additions.
- **MED-01 through MED-10** — polish; queue for patch-set-03.

Three changes per patch set keeps review surface small and rollback trivial.

---

## After-commit handoff back to Cowork

Once landed, ping back here in the Cowork session with the commit SHA (or just "patch-set-01 landed"). I'll reload the browser, screenshot the three affected surfaces, and confirm the findings are visually resolved. If anything looks off, we file a follow-up.

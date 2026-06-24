# Stage 07 — Interrogation (refine-design-review) · dialectic

- Capability: `interrogation` · Mode: `refine-design-review` · Receipt: 3 subagent receipts + parent synthesis
- Status: **block→repair** (two must-fix blockers; one design premise code-disconfirmed)

## Subagent receipts (verdicts)

| Role | Verdict | Headline |
| --- | --- | --- |
| ergonomics-advocate (`a5bae1136f49c65e5`) | **block** | DD-F5 claims a fix the code contradicts; unattributed row is unactionable; untagged comments betray the user |
| governance-integrity-skeptic (`a48cece27ed666a2a`) | flag | s03 block only *partially* resolved; DD-F1 ancestor-rewrite silently widens scope |
| implementation-cost-realist (`a6e02656ed00e6927`) | flag | one-file/dep-free, but DD-F5 premise code-disconfirmed and DD-F1 stable-selector contradicts in-repo GAP |

## Convergent code-verified findings (independently confirmed by ≥2 roles)

- **C1 — DD-F5 is FALSE as written (high).** `diffByOdId` **excludes `<style>` nodes** (`if (tag === "style") continue` in both walk loops). The `null` bucket fires **only** for a *structural* element with no `od-id` ancestor — **not** for CSS/theme edits. A `--green` token edit yields **zero diff fragments**, not a "visual-only" row. *Why theme edits don't silently apply is the **M1 fence** (rejects out-of-scope/`null` CSS rules at gate 2A, admission.ts:128/151-162) — not the diff.* So D2 honesty for theme edits requires a **separate CSS-diff lane**, not the null bucket.
- **C2 — Unattributed row is unactionable (high).** `OdDiffFragment = {odId:null, added, changed, removed}` — three integers, no `selector`/`elementLabel`/property. "3 unattributed changes" is a warning the user cannot act on. Fix: enrich the fragment with `selector` + `elementLabel` + first differing field.
- **C3 — DD-F1 ancestor-rewrite silently widens scope (high).** Rewriting an untagged child's intent onto the nearest tagged ancestor makes the manifest record the *ancestor*, not what the human pointed at. Trades "anonymous target" for "silent scope-coarsening" (D1 intent≠applied, D2 wrong granularity). Fix: persist **both** pointed-at handle **and** rewrite-target; manifest records "pointed-at: X → applied-to: Y"; **disclose at capture and at rewrite**, never silently.
- **C4 — Minted nth-child handles are unstable (high).** In-repo `GAP-V3-NODE-IDENTITY-008` warns the sibling-index node key is brittle to legitimate reordering. So minted handles drift across synthesis → keep DD-F1 strictly **capture/preview-only**; never persist a minted handle as an apply target.
- **C5 — "Observed" props are a canonicality trap (med).** The synthesizer/fence parse **authored** CSS (raw `<style>` text); `getComputedStyle` returns *resolved* values (`16px` vs authored `1rem`) → mis-diff. Fix: mark observed props **non-transferable** into candidate authoring.
- **C6 — Prefilling required `intent`/`note` hollows the contract (med).** Auto-filling a governance-required human-attestation field defeats `COMMENT_SCHEMA_INVALID` and makes its test UI-satisfiable. Fix: prefill only non-required hints/placeholders; keep `intent`/`note` human-entered (or sentinel-reject known defaults).
- **C7 — DD-F4 reload preserves query but not DOM (med).** `location.reload()` keeps `?view=...`, but the poll never reads it back → still snaps. Fix: 3-line restore-on-load reader. No sandbox/origin snag.
- **C8 — Hover event-flood (med).** Use `mouseover` (not `mousemove`) + rAF/debounce + a **separate** listener (not folded into the click handler's `preventDefault`).

## s03 block status

**Partially resolved.** Theme edits no longer *silently apply* (the fence rejects them) — but they are still *diff-invisible* (C1), and DD-F1 replaced "anonymous target" with "scope-coarsening" (C3). Both must be repaired.

## design-review-ledger → handed to s08 Distill Repair

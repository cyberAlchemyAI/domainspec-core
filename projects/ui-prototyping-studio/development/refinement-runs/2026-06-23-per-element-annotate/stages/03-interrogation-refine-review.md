# Stage 03 — Interrogation (refine-review) · dialectic

- Capability: `interrogation` · Mode: `refine-review` · Receipt: 3 subagent receipts + parent synthesis
- Roles: `ergonomics-advocate`, `governance-integrity-skeptic`, `implementation-cost-realist`
- Anti-bias axis: ergonomic-freedom ⟷ governed-integrity, grounded by cost
- Status: **flag** (stable disagreement preserved; one block dissolved by synthesis)

## Subagent receipts (verdicts)

| Role | Verdict | Fork picks (F1–F5) |
| --- | --- | --- |
| ergonomics-advocate (`ad9a30d405b43d5fe`) | flag | F1a, F2b, F3c, F4a, F5c |
| governance-integrity-skeptic (`aa9bdd82cd2106550`) | **block** | F1c, F2a, F3a, F4b, F5b |
| implementation-cost-realist (`aa2240b504da38f30`) | flag | F1 hybrid-lite, F2b(scoped), F3a, F4a, F5c |

## Decisive new evidence (from cost-realist code dive)

- **M1 admission fence** (`admission.ts`) **REJECTs** changes whose nearest scope-chain `od-id` is ⊥/out-of-scope. ⇒ auto-minted handles for untagged elements are cheap to *capture* but **fail at apply**. This is the true F1 constraint.
- **`diffByOdId` already buckets unattributable changes under a `null` od-id key** (the `" null"` bucket). ⇒ F5 reconciliation already has a real, attributable manifest row to surface.
- **Hover-as-capture-trigger breaks the Playwright e2e** (suite drives click→postMessage). `intent`/`note` are **required** (`parseRequiredText` → `COMMENT_SCHEMA_INVALID`).
- **`getComputedStyle`** is feasible only in the `allow-scripts` wrapper on **same-origin self-contained** variant HTML.

## Stable disagreement (residue ledger)

- **R1 — F1 untagged apply.** Governance: quarantine untagged to draft, never ingest anonymous targets (F1c). Ergonomics: never block annotation on prior tagging (F1a). Cost: pure F1a dead-ends at the M1 fence; only "mint-handle-for-comment + agent rewrites into nearest in-scope od-id" survives. **Unresolved at MVP scope** → see design decision DD-F1.
- **R2 — F2 provenance.** Governance: computed style desyncs from the descriptor and "the pre-fill lies about provenance" (F2a). Ergonomics/Cost: computed style is what the user sees and is the single cheapest real win (F2b). **Residue:** label the pre-fill as *observed*, not *canonical*, to satisfy provenance honesty.
- **R3 — F3/F4 boundary.** Governance: routed view + flush-on-run for auditability (F3a/F4b). Ergonomics/Cost: reuse existing immediate POST + in-page CSS (F3a/F4a). Note F3 converges on (a) by different routes (existing `/comment` already persists on head and drains via `listPendingComments`).

## Dissolved block (synthesis win on F5)

Governance demanded F5b ("bind to a real manifest fragment, never diff-silent"); it **blocked** on F5c. Cost found the diff **already has** a real `null` od-id bucket for unattributable changes. **Synthesis:** surface that existing `null` bucket as an explicit **"⚠ visual-only / unattributed"** diff row. This is a *real, attributable manifest row* (meets governance's "not diff-silent") that does **not** suppress the change (meets ergonomics) and is ~10 LOC (meets cost). **The governance block is dissolved** without conceding D2.

## Convergence carried forward

- Keep **click** as the capture trigger; **hover only pre-fills** the form preview (protects e2e, satisfies "Figma feel").
- Pre-fill from **`getComputedStyle`**, labelled *observed*.
- Reuse the **existing immediate `/comment` + `listPendingComments`** drain (no new persistence layer).
- **In-page CSS** expand/collapse, with view-state in the URL so the 1.5s poll-reload doesn't snap back.
- Surface the **`null` bucket** as the honest-diff reconciliation.
- MVP scopes **untagged elements to props-preview + comment-capture**; **untagged apply (fence work) is deferred**.

## refine-review-ledger → handed to s04/s05

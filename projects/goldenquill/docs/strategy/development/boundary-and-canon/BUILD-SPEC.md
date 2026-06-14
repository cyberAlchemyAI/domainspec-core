# BUILD-SPEC — Boundary and Canon

- **Node:** `boundary-and-canon` (Craft ledger `craft.goldenquill.boundary_and_canon`)
- **Context gate (current):** BLOCK — `CTX-BC-ROOT.gate: block`, held by blocking decision `DEC-BC-POSTURE-VOCAB`
- **Authored:** 2026-06-13 (Refine→Invoke authoring pass; planning/spec only)
- **Status:** Ready for operator ratification in one pass
- **Scope discipline:** This document is planning/spec only. It does **not** mutate `CLAUDE.md`, `AGENTS.md`, locked architecture, or `.craft/ledger.yml`. No `orgs/` data is read or referenced (Law 3). It frames the two open decisions and the canon clean-ups so Josh can ratify, after which a separate (non-this-document) pass applies the ledger/canon edits.

---

## 1. Purpose and provenance

Keep workbook-derived tasks aligned with current Golden Quill canon, locked boundaries, and customer-facing vocabulary. This node owns cross-cutting canon drift originating from the task-role workbook.

**Source evidence (all read; none treated as canon):**

| Role | Path | Authority |
| --- | --- | --- |
| Source contract (workbook) | `docs/golden-quill-task-role-breakdown-handoff.md` | source-contract — evidence for tasks, NOT canon |
| Canon (postures) | `AGENTS.md` "Deployment Posture Vocabulary" (architecture v7.0.10 LOCKED 2026-05-11) | canon |
| Boundary register | `CLAUDE.md` (three-posture canon, v0.1 headless-only, CIC "Public Agency", Sovereign-Node disambiguation) | boundary-register |
| Research evidence | `…/refinement-runs/2026-06-12-craft-pipeline-hydration/RESEARCH-RESULT.md` (+ `.craft/ledger.yml`, `REFINE-DISPATCH.json`) | planning evidence (PASS, local-first) |
| Architecture spec | `pipeline/architecture/v0.1/architecture_v7_0_10_amendment.md` | locked architecture (referenced, not edited) |

The 2026-06-12 local-first research run found **five conflicts (F1–F5) and one negative confirmation (F6)** between workbook language and locked canon. Two of those conflicts are the open decisions framed below; the rest are canon clean-ups.

---

## 2. Decision DEC-BC-POSTURE-VOCAB — Posture vocabulary translation [BLOCKING]

**Owner:** Josh (governance) to ratify.
**Refine-status:** refine-solvable — the translation is fully determined by locked canon; only ratification remains.
**Blocker:** `BLK-BC-POSTURE-VOCAB` (vocabulary_blocker). Closes when the workbook posture row is translated into the three-posture canon and "Sanitized" is not propagated.

### 2.1 The conflict (F1 + F2)

- Workbook row B. Software — Tilth Build (`…handoff.md:50`): *"Posture system: **Unrestricted / Hybrid / Sanitized / Sovereign**, technically enforced."*
- Workbook row (`…handoff.md:51`): *"**Sanitization pipeline** + split-context drafting pattern."*
- Canon (`AGENTS.md` Deployment Posture Vocabulary; architecture v7.0.10): posture vocabulary is **exactly three values** — Frontier-Eligible, Split-Context Hybrid, Local-Only / Sovereign. The four-posture-implicit framing is deprecated; "Sanitized" / opaque-slot-token is **deprecated** and survives only as a defense-in-depth gate (`F-CLASS-SLOT-ID-NON-OPAQUE`, `F-CLASS-CLOUD-RECEIVED-OPAQUE-SLOT-FILLED`; firing = bug or attack).

### 2.2 Canonical translation table (the thing to ratify)

| Workbook term (deprecated, 4-posture) | Locked canon term (v7.0.10, 3-posture) | Mapping notes |
| --- | --- | --- |
| **Unrestricted** | **Frontier-Eligible** | Same intent — customer permits selected data to route to external/frontier models. Per-field classification register (public / shareable / confidential / operator_flagged) drives routing. "Unrestricted" is a non-canon label; do not propagate. |
| **Hybrid** | **Split-Context Hybrid** | Same intent — frontier models do structure/scaffold/dialect work on an operator-signed allow-list; confidential substance stays local; a local model inserts restricted facts separately. "Hybrid" alone is a non-canon label; use the full term. |
| **Sovereign** | **Local-Only / Sovereign** | Same intent — all drafting, review, routing, evidence stay local (maximum-custody). Carries the under-validation caveat until the `local_only_validated` manifest flag flips on SN-LLC quarterly validation. |
| **Sanitized** | **(no posture)** — DEPRECATED | **Does NOT map to a posture.** The opaque-slot / Sanitized round-trip is retired. The split-context substance/structure separation (closed-set allow-list + applicant-fact PRE-scan) achieves the "power for drafting + privacy on substance" goal without opaque-slot tokens. The slot-fill module remains in the runtime tree as **defense-in-depth only**, never normal-path. |

**Net:** 4 workbook terms → 3 canon postures + 1 deprecation. The two "technically enforced" workbook rows (`:50` posture system, `:51` sanitization pipeline) translate as follows:

- "Posture system: Unrestricted / Hybrid / Sanitized / Sovereign, technically enforced" → **"Posture system: Frontier-Eligible / Split-Context Hybrid / Local-Only-Sovereign, technically enforced (classification-driven per-call routing per architecture v7.0.10)."**
- "Sanitization pipeline + split-context drafting pattern" → **"Split-context drafting pattern (substance/structure separation under Split-Context Hybrid)."** Drop "Sanitization pipeline" as a build task; if the slot-fill defense-in-depth module is referenced at all, label it defense-in-depth, never a normal-path build deliverable.

### 2.3 What Josh must ratify

Confirm the table above as the canonical translation, so that: (a) the build-task language for the posture/enforcement rows is rewritten to the three-posture canon, (b) "Sanitization pipeline" is removed as a build deliverable and recast as defense-in-depth only, (c) the closure condition for `BLK-BC-POSTURE-VOCAB` is met and `CTX-BC-ROOT.gate` can move off BLOCK.

**Downstream this unblocks:** `GAP-TRB-POSTURE-CANON` and `GAP-NOD-CANON-VOCAB` (other Craft nodes consuming the same posture wording). F5 (below) also folds into this ratification.

**Guardrail:** Ratifying this never revives "Sanitized" or a fourth posture as canon. The three-posture customer-facing model is canonical per v7.0.10 §1.

---

## 3. Decision DEC-BC-UI-BOUNDARY / GAP-BC-UI-SCOPE — Operator console boundary

**Owner:** Josh (governance) to decide.
**Refine-status:** decision-gated — Refine has framed the options and impacts; the phase call is a governance decision, not a research output.
**Gate:** `GAP-BC-UI-SCOPE` (severity flag, treatment: decide). Non-blocking for the BLOCK gate, but must be resolved before the console row becomes executable work.

### 3.1 The conflict (F3)

- Workbook row B. Software — Tilth Build (`…handoff.md:53`): *"**Operator console UI**: read-only projection over real backend first, then interactive."* Echoed in Roles & Gaps (`:108`, "console UI").
- Canon (`CLAUDE.md`): *"Do not propose a Next.js UI or any UI layer for v0.1 — headless only."* v0.1 is **HEADLESS-ONLY (locked).**
- Conflict: the "then interactive" clause is v0.1 scope drift. The "read-only projection" sub-clause may or may not survive as a non-UI internal projection.

### 3.2 Three-option decision

| Option | What it means | v0.1 headless compliance | Impact |
| --- | --- | --- | --- |
| **(a) v0.1 read-only projection over real backend** | A read-only projection/render of real backend state (e.g., a generated HTML/Cowork artifact or CLI-rendered view) — **no interactive UI layer, no Next.js, no input surface**. Reads state, never mutates it. | Compliant *if and only if* it is genuinely non-interactive and not a "UI layer" — a render of state, not an app. Risk: drifts toward an interactive surface. | Lets operators/buyers see node state in v0.1 without a UI layer. Must be specified as projection-only with no write path. WPFA buyer-facing PDF + operator dashboard (Cowork HTML artifact, per `CLAUDE.md` §WPFA) are an existing precedent for read-only projection. |
| **(b) Deferred later-phase interactive surface** | The interactive console is acknowledged as real product scope but explicitly **deferred to a post-v0.1 phase**. v0.1 ships headless; the console lands when the headless boundary lifts. | Compliant — nothing interactive ships in v0.1. | Cleanest boundary. Workbook row gets a phase tag ("v1.x+ / post-headless"). No v0.1 build effort. Matches workbook's own "After Acceleration" framing for multi-seat/role-permission surfaces. |
| **(c) Out-of-scope for v0.1** | The console row is removed from v0.1 scope entirely with no phase commitment. | Compliant. | Strictest. Differs from (b) only in that it makes no forward commitment; revisit later as new scope. |

**An interactive v0.1 UI is NOT an option** — it violates the locked headless-only boundary.

### 3.3 Recommendation

Recommend **(a) or (b)**, never an interactive v0.1 UI.

- Choose **(a)** if Josh wants operators/buyers to *see* node state during v0.1 white-glove (leverages the existing WPFA/dashboard read-only-projection precedent) — provided it is specified as projection-only, no write path, no app/UI-layer.
- Choose **(b)** if Josh wants the simplest possible boundary and is content to defer all console work until the headless constraint lifts.

### 3.4 What Josh must decide

Pick (a), (b), or (c). The chosen option becomes `DEC-BC-UI-BOUNDARY.selected`, and the workbook console row (`:53`, `:108`) gets the corresponding phase treatment.

**Downstream this resolves:** the `console UI` line in the Roles & Gaps role map (AI Engineer, `:108`) gets the same phase tag.

**Guardrail:** Whatever is chosen, v0.1 stays headless. No interactive UI ships in v0.1 under any option.

---

## 4. Canon clean-ups (no operator gate; fold into the ratification pass)

These are vocabulary corrections, not decisions. They apply automatically once §2 is ratified.

### 4.1 F4 — "Municipal" → "Public Agency" (CIC label)

- Workbook uses **"Municipal"** in segment / domain-expert / partner-channel rows: `…handoff.md:91, :95, :113, :117`.
- Canon: the customer identity category is **"Public Agency"** (TILTH-CIC-03), explicitly the "clearer alternative to 'Municipal Steward'" (`CLAUDE.md` CIC list).
- Treatment: where workbook text would be reused at any customer-facing or CIC-labeled surface, replace "Municipal" with "Public Agency". Low severity (internal staffing context), but flag before customer-facing reuse. Specific instance: Roles & Gaps "Municipal expert criterion" (`:117`) and Domain Experts "×4 segments … Municipal …" (`:113`) → "Public Agency".

### 4.2 F5 — "Sovereign-mode" disambiguation

- Workbook "After Acceleration": *"**Sovereign-mode build** finished & audited; sanitization GA"* (`:92`) and *"Tribal-nation **Sovereign-mode** pilots"* (`:95`).
- Canon: "Sovereign" survives only inside the posture label **"Local-Only / Sovereign"** (`AGENTS.md`). **"Sovereign Node"** is a Stage-5 commons term, NOT a posture and NOT a per-node mode (`CLAUDE.md`). It is never a nickname for an individual Golden Quill.
- Treatment: disambiguate "Sovereign-mode" to the posture label **"Local-Only / Sovereign posture"** in both rows. "sanitization GA" (`:92`) re-triggers F1/F2 — drop it; the Sanitized mechanism is deprecated, there is no "sanitization GA" milestone. This clean-up folds under `DEC-BC-POSTURE-VOCAB` ratification.

### 4.3 F6 — Negative confirmation (no action)

Workbook does NOT name a stale GB floor, "Managed Edition," "metered billing," "MaatAI," or "Sovereign Node LLC." Hardware/BYOK/entity axes are clean. No correction needed.

---

## 5. External research posture

`EXT-BC-01` (public-facing terminology-risk comparison: do "Public Agency" / "Local-Only / Sovereign" read cleanly to external buyers) remains **DEFERRED**. Per `rg03` it requires a named local-evidence gap **plus Josh's explicit approval**, and triggers only if customer-facing copy is being finalized. Bound: public terminology only — NO client/org material, NO PROJECT_CONTEXT. All §2–§4 corrections need zero external evidence; canon is self-sufficient.

---

## 6. Post-ratification next moves (not executed here)

Once Josh ratifies §2 and decides §3, a separate pass (not this document):

1. Records `DEC-BC-POSTURE-VOCAB.selected` = the §2.2 translation table; closes `BLK-BC-POSTURE-VOCAB`; moves `CTX-BC-ROOT.gate` off BLOCK.
2. Records `DEC-BC-UI-BOUNDARY.selected` = (a) / (b) / (c); resolves `GAP-BC-UI-SCOPE`.
3. Advances the node to its validated Refine route (`ENA-BC-REFINE-ROUTE`, dispatch `gq-craft-hydration-boundary-and-canon-2026-06-12`) — runtime stages stay permission-gated.
4. Propagates the canon corrections to downstream nodes (`GAP-TRB-POSTURE-CANON`, `GAP-NOD-CANON-VOCAB`).

---

## 7. Per-decision verdict lines

```
DEC-BC-POSTURE-VOCAB | Josh (governance) | refine-solvable | Ratify the §2.2 translation table: Unrestricted→Frontier-Eligible, Hybrid→Split-Context Hybrid, Sovereign→Local-Only/Sovereign, Sanitized→DEPRECATED (defense-in-depth only). Closes BLK-BC-POSTURE-VOCAB; unblocks GAP-TRB-POSTURE-CANON + GAP-NOD-CANON-VOCAB. [BLOCKING]
DEC-BC-UI-BOUNDARY   | Josh (governance) | decision-gated  | Pick (a) v0.1 read-only projection over real backend / (b) deferred later-phase interactive surface / (c) out-of-scope for v0.1. Recommend (a) or (b); interactive v0.1 UI is NOT permitted (headless-only locked).
GAP-BC-UI-SCOPE      | governance        | decision-gated  | Resolved by the DEC-BC-UI-BOUNDARY choice; console row (handoff.md:53, :108) gets the matching phase tag.
F4-MUNICIPAL-LABEL   | (clean-up)        | refine-solvable | No gate — replace workbook "Municipal" with CIC "Public Agency" (TILTH-CIC-03) at any customer-facing/CIC surface. Folds into the ratification pass.
F5-SOVEREIGN-MODE    | (clean-up)        | refine-solvable | No gate — disambiguate "Sovereign-mode" → "Local-Only / Sovereign posture"; drop "sanitization GA". Folds under DEC-BC-POSTURE-VOCAB.
```

**File:** `docs/strategy/development/boundary-and-canon/BUILD-SPEC.md`

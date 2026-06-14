# Research Result - Boundary and canon

- Dispatch ID: `gq-research-strategy-boundary-and-canon-2026-06-12`
- Run: `2026-06-12-craft-pipeline-hydration`
- Mode: LOCAL-FIRST research execution (r01-r06)
- Strategy route: `RESEARCH-DISPATCH.json` (selected route `gap_triggered_external`)
- Overall verdict: **PASS** — core question answered from local Golden Quill canon only; one external comparison gap named and DEFERRED (no approval present).

## Node

- Craft node: `boundary-and-canon`
- Title: Boundary and canon
- Research lane: canon and boundary research
- Purpose: keep workbook-derived tasks aligned with current Golden Quill canon, locked boundaries, and customer-facing vocabulary.

## Core Question

Which workbook terms or assumptions conflict with locked Golden Quill canon and v0.1 boundaries?

## Findings (claim -> source path)

The source workbook is `docs/golden-quill-task-role-breakdown-handoff.md` (artifact `ART-BC-HANDOFF`). Five conflicts and one partial-match found against locked canon.

### F1 — Posture vocabulary conflict (BLOCKER; matches BLK-BC-POSTURE-VOCAB / DEC-BC-POSTURE-VOCAB)

- Workbook row B. Software — Tilth Build: "Posture system: **Unrestricted / Hybrid / Sanitized / Sovereign**, technically enforced" — `docs/golden-quill-task-role-breakdown-handoff.md:50`.
- Canon: posture vocabulary is exactly three values — **Frontier-Eligible**, **Split-Context Hybrid**, **Local-Only / Sovereign** — per `AGENTS.md:45-47` (architecture v7.0.10 LOCKED 2026-05-11). "Sanitized" is explicitly deprecated; the four-posture-implicit framing is deprecated.
- Conflict: workbook names a four-item set, uses retired "Sanitized," and uses non-canon labels "Unrestricted" and "Hybrid" (canon = "Frontier-Eligible" and "Split-Context Hybrid"). Reinforced by `CLAUDE.md` "Beta Model Strategy" section and the "do NOT revive the Sanitized vocabulary" prohibition (`CLAUDE.md:254`).

### F2 — Sanitization pipeline conflict (BLOCKER-adjacent; same canon anchor as F1)

- Workbook row: "**Sanitization pipeline** + split-context drafting pattern" — `docs/golden-quill-task-role-breakdown-handoff.md:51`.
- Canon: the opaque-slot / Sanitized round-trip is DEPRECATED; only the split-context substance/structure separation survives (`AGENTS.md:45-47`; `CLAUDE.md:254` "the Sanitized / opaque-slot-token mechanism is DEPRECATED"). The slot-fill module remains only as defense-in-depth, never normal-path.
- Conflict: "Sanitization pipeline" as a build task implies a live mechanism that canon retired. The "split-context drafting pattern" half is canon-aligned.

### F3 — Operator console UI conflict (GAP-BC-UI-SCOPE / DEC-BC-UI-BOUNDARY)

- Workbook row: "**Operator console UI**: read-only projection over real backend first, then interactive" — `docs/golden-quill-task-role-breakdown-handoff.md:53`. Echoed in Roles & Gaps ("console UI") — `:108`.
- Canon: "Do not propose a Next.js UI or any UI layer for v0.1 — headless only" — `CLAUDE.md:252`.
- Conflict: any interactive UI is out of v0.1 scope. The "read-only projection" sub-clause may survive as a non-UI internal projection, but the "then interactive" clause is v0.1 scope drift. Needs phase treatment (v0.1 / read-only projection / later-phase product surface).

### F4 — "Municipal" vs "Public Agency" CIC label (FLAG; customer-facing vocabulary)

- Workbook uses "Municipal" in segment / domain-expert / partner-channel rows — `docs/golden-quill-task-role-breakdown-handoff.md:91, :95, :113, :117`.
- Canon: the customer identity category is "**Public Agency**" (TILTH-CIC-03), explicitly a "clearer alternative to 'Municipal Steward'" — `CLAUDE.md:48`.
- Conflict: workbook "Municipal" is stale customer-facing vocabulary; canon prefers "Public Agency." Low-severity (internal staffing context), but flag before any customer-facing reuse.

### F5 — "Sovereign-mode build" terminology (PARTIAL; reconcile, not reject)

- Workbook "After Acceleration": "**Sovereign-mode build** finished & audited; sanitization GA" — `docs/golden-quill-task-role-breakdown-handoff.md:92`; "Tribal-nation **Sovereign-mode** pilots" — `:95`.
- Canon: "Sovereign" survives only inside the posture label "Local-Only / Sovereign" (`AGENTS.md:45-47`); "Sovereign Node" is a Stage-5 commons term, NOT a posture or a per-node mode (`CLAUDE.md:30`, `:34`). "sanitization GA" re-triggers F1/F2.
- Conflict: "Sovereign-mode" is ambiguous between the Local-Only / Sovereign posture and the Stage-5 Sovereign Node commons. Needs disambiguation to the posture label; "sanitization GA" is a deprecated-term recurrence.

### F6 — No conflict found on hardware/BYOK/entity terms (negative finding)

- Workbook does not name a stale GB floor, "Managed Edition," "metered billing," "MaatAI," or "Sovereign Node LLC." Checked against `CLAUDE.md:24, :30, :34, :251` and `AGENTS.md:112`. No conflict on these axes — clean.

## Lane Map (per gap)

| Gap / finding | Lane | Source class | Local-sufficient? |
| --- | --- | --- | --- |
| F1 posture vocab | local-only (canon correction) | canon (`AGENTS.md`), boundary-register (`CLAUDE.md`) | Yes — closes DEC-BC-POSTURE-VOCAB |
| F2 sanitization pipeline | local-only (canon correction) | canon (`AGENTS.md`), `CLAUDE.md` | Yes |
| F3 operator console UI | local-only (phase decision) | boundary-register (`CLAUDE.md:252`), source-contract | Yes — feeds DEC-BC-UI-BOUNDARY; needs Josh's phase call |
| F4 Municipal label | local-only (vocab correction) | boundary-register (`CLAUDE.md:48`) | Yes |
| F5 Sovereign-mode | local-only (disambiguation) | canon (`AGENTS.md`), `CLAUDE.md:30,34` | Yes |
| F6 hardware/BYOK/entity | local-only (negative confirm) | `CLAUDE.md`, `AGENTS.md` | Yes |

All findings resolved local-first. No finding required external evidence to answer the core question.

## External-Research Decision

- Route selected in dispatch: `gap_triggered_external`.
- Decision: **DEFERRED.** No external pass executed. Per `rg03` (human_approval) external research requires a named local-evidence gap plus Josh's explicit approval — not present.
- Bounded external requests deferred (named, not run):
  - **EXT-BC-01 (DEFERRED):** Public-facing terminology-risk comparison — confirm "Public Agency" / "Local-Only / Sovereign" read cleanly to external buyers vs. industry norm. Bound: public terminology only; NO client/org material; NO PROJECT_CONTEXT. Trigger: only if customer-facing copy is being finalized AND Josh approves.
- All other findings need zero external evidence; canon is self-sufficient.

## Residue

- F3 (operator console UI) and F5 (Sovereign-mode) carry open decisions (`DEC-BC-UI-BOUNDARY`, and an F5 disambiguation that folds under DEC-BC-POSTURE-VOCAB). Research surfaced the conflict and the canon anchor; the phase/term call is Josh's governance decision, not a research output.
- This run is planning evidence only (rg06). It does NOT mutate `.craft/ledger.yml`, canon files, or lifecycle artifacts.

## Next Move

Hand findings to the node's Refine route. Recommended: governance reviewer closes `DEC-BC-POSTURE-VOCAB` with the three-posture translation (covers F1, F2, F5), and takes `DEC-BC-UI-BOUNDARY` phase call (F3). F4 folds into the same vocabulary correction pass. EXT-BC-01 stays deferred unless customer-facing copy work opens and Josh approves.

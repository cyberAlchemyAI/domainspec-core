# UI Prototyping Studio UX/UI Upgrade Findings

Dispatch: `2026-07-09-ui-prototyping-studio-ux-upgrade-research`
Status: accepted research findings pending auditor closeout

## Concise Verdict

Studio has a credible reversible prototype state machine, but browser/control projection is not yet reliable governed-state projection.

This is a governance-truth finding, not a general feature backlog. The central defect is not that the UI needs polish. It is that the operator can take governed actions whose visible browser surfaces do not reliably show the current governed state, the visible diff, or the next valid control obligation.

The export edge is stronger than the preview/control surface. Beer's evidence says confirmed handoff export is core-enforced, not just CLI theater, and Body War/TROQAR is valid precedent for selector/copy obligations moving into app specs/tests, not production HTML proof (Agent 4, lines 248-278, 306-315). The upgrade path should therefore protect Studio's identity: reversible prototype exploration plus handoff evidence, not generic design generation or production UI emission.

## Evidence Boundary and Interaction Data

Evidence source: `projects/ui-prototyping-studio/development/research/20260709-ux-ui-upgrade-research/research.md`.

Interaction corpus:

- Agent 1, Turing, Alan: runtime archaeology, direct CLI and browser/control evidence, TROQAR sampling, unit/e2e validation notes, preview state defects, diff falsifier, handoff semantics (lines 7-104).
- Agent 2, Alexander, Christopher: Open Design comparison from vendored snapshot only, Studio identity boundary, safe OD borrowings, forbidden governance bypasses (lines 105-188).
- Agent 3, Schon, Donald: UX walkthrough across desktop/mobile preview states, accepted-head mismatch, durable control framing, annotation and mobile usability (lines 189-243).
- Agent 4, Beer, Stafford: governance viability, export boundary, Body War/TROQAR precedent, stale docs/test-count drift, e2e/Corepack fragility, non-goals (lines 244-325).

Validation and run evidence reported by explorers:

- TypeScript passed; unit/slice tests passed `62/62` in Turing and Beer reports (lines 16-20, 258-263).
- Shimmed Playwright e2e passed `13/13` for Turing, while Beer could not claim fresh checked-in e2e because helpers shell through `pnpm exec` and Corepack failed first (lines 16-20, 258-263, 314).
- Browser/control screenshots and logs exist under `/tmp/ups-browser-controls-F3S4lU`, `/tmp/ups-browser-clean-RCArgK`, and walkthrough screenshots under `/tmp/ups-*.png` (lines 35-44, 86-93, 195-205).
- No explorer reports retained repo edits (lines 11, 109, 193, 304).

## What Is Working Now

Studio's reversible state machine is real enough to build on.

Working properties supported by the research:

- Isolated `STUDIO_DATA` operation works, and `/tmp` artifact roots are separable from repo state (Agent 1, lines 52-55).
- Variant registration, baseline selection, two-gate apply, staged state, accept, append-only revert, revision lineage, and export confirmation all have working evidence (Agent 1, lines 54-63).
- `handoff export` without confirmation refuses with `HANDOFF_CONFIRMATION_REQUIRED`; confirmed export is also core-enforced via `exportDesignHandoff` requiring `confirmedBy` and HTTP passing `confirm` into the use case (Agent 1, lines 57-61; Agent 4, lines 248-255, 306-309).
- Browser annotation can capture a comment, and browser accept/discard/revert can work when preview starts after staged state (Agent 1, lines 59-61; Agent 3, lines 207-213).
- Exploit/explore distinction is functioning: exploit rejects structural divergence; explore can admit a new `data-od-id` target (Agent 1, lines 45-50, 62-63).
- Body War/TROQAR demonstrates an accepted prototype gate can carry selector/copy obligations into app specs/tests without claiming prototype HTML is production-ready (Agent 4, lines 273-278, 306-309).

## Where the UX/UI Breaks Trust

The trust break is state projection.

Current evidence shows that Studio can update governed state while the browser continues to display stale or misleading projections:

- After Accept, `/raw/baseline` can correctly return the accepted content while visible preview cards and annotation iframe still render the original variant. Schon observed `Continue` at `/raw/baseline` while the visible card/annotation still showed `Go`; the code path cited uses variant refs for cards and annotation, while current head is only exposed through `/raw/baseline` (Agent 3, lines 214-217, 227-239).
- The preview server does not observe external CLI writes after startup. Turing saw separate CLI synthesize/approve/apply return `RevisionApplied`, while running preview `/state` still reported `CommentsCaptured` and `stagedHash:null` (Agent 1, lines 64-68, 86-93).
- Visible CSS/theme edits can produce zero honest diff. TROQAR theme candidate returned `NOT_REJECT` with `diff.fragments: []`, `added/changed/removed: 0`, then accept recorded zero diff (Agent 1, lines 66-69; reinforced by Agents 2-4 at lines 168-170, 231-239, 310-320).
- One-click Accept/Revert are durable reversible actions, but their browser framing is too thin: no confirmation, no candidate/revision recap, no "I inspected this" friction, and Revert immediately appends a new revision (Agent 3, lines 216-218, 235-240).
- Mobile before/after is responsive but not inspectable: side-by-side panes around 143px wide read as narrow blank columns (Agent 3, lines 218-221, 240).
- Annotation UX exposes form controls before useful selection context, lacks hover/selected outlines, component list, comment list, constrained severity, and reliable iframe load/status feedback (Agent 1, lines 71-74; Agent 3, lines 219-222, 241).
- Handoff readiness semantics overclaim when integration readiness flags are true while `missingRefs` lists default refs (Agent 1, lines 69-70; Agent 4, lines 322-324).
- Docs/test-count/state sync is stale enough to create governance debt: old CRAFT/PLAN state, test-count drift, stale SPEC invariant row, and old ARCH preview wording all weaken claim discipline (Agent 4, lines 265-286, 314-325).

## Open Design Comparison

Open Design is useful as a source of structured evidence/profile patterns, not as Studio identity or authority.

Safe borrowings:

- Minimal `CraftEvidencePack` inside Studio gates: candidate-level evidence for `data-od-id`, visible-change/diff integrity, basic a11y/layout checks, target size, focus/label basics, state coverage, and anti-slop checks. Split checks into `required_gate`, `advisory`, and `subjective_review` so subjective critique cannot hard-block acceptance before calibration (Agent 2, lines 125-154, 156-187).
- Source/derived/provenance separation for handoff bundles: authored source, normalized context, candidate hash, validator results, evidence summary, and export confirmation (Agent 2, lines 129-130, 154-155, 176-177).
- Later phase only: `GeneratorProfile`, `DesignObjectiveBrief`, seed/archetype libraries, `CritiqueReview`, reversible tweak sessions, and source-derived provenance, all subordinate to Studio's register/baseline/stage/manifest gates (Agent 2, lines 146-155, 179-188).

Forbidden imports:

- Do not emit OD artifacts directly as final product without `variants register`, baseline selection, staging, manifest append, and export evidence (Agent 2, lines 139-145).
- Do not make subjective critique/taste a hard gate until calibrated by fixtures (Agent 2, lines 134-136, 164-177; Agent 3, lines 231-233).
- Do not import OD live-artifact connector/daemon assumptions into Studio's boundary (Agent 2, lines 144-145, 176-177).
- Do not treat OD as identity replacement. Studio governs reversible prototype exploration and handoff evidence; it is not a generic design generator, production HTML path, subjective critique gate, Open Design clone, or human-vs-agent identity gate.

## Ranked Upgrade Table

| Rank | Upgrade | Ownership | Smallest runnable witness | Likely file/surface | Validation receipt |
|---:|---|---|---|---|---|
| 1 | Current-head projection after accept/revert/external writes | Runtime + preview UI | Create session, stage `Go -> Continue`, Accept, then assert visible primary preview and annotation source render current head; mutate via external CLI while preview is running and assert browser `/state` refreshes | `src/cli/studio.ts` preview routes, `/raw/baseline`, `/state`, annotation routes, preview card rendering | Playwright test fails before fix on visible text mismatch; passes with screenshot and DOM assertion that current head is primary after Accept/Revert/external write |
| 2 | Visible-change diff integrity | Core diff + evidence model | Apply TROQAR-style CSS/theme candidate with raw hash change and visible style change; assert diff is not zero or explicitly reports global/style lane | Diff generation/use case behind `apply`, handoff diff fragments, pending panel diff summary | Unit fixture plus e2e receipt: `changedHash=true`, `visible/style lane present`, no `added/changed/removed: 0` confidence for visible edits |
| 3 | Preview state coherence across CLI/server mutation paths | Store/runtime boundary | Start preview, mutate state through CLI synthesize/approve/apply, then fetch `/state` and browser panel without restart | File store reload/version watcher, preview server request handlers, or route consolidation for synthesize/apply | E2E "external write observed" test with before/after state version; no stale `CommentsCaptured` after CLI `RevisionApplied` |
| 4 | Durable reversible-action framing | Preview UX + control copy | Stage a change and click Accept/Revert; require confirmation sheet with revision/candidate id, diff recap, inspected checkbox, and resulting state summary | Browser Accept/Revert POST flow, staged panel, revision controls | Playwright receipt: Accept/Revert cannot commit until confirmation conditions met; post-action page names new head/revision and undo path |
| 5 | Deterministic e2e harness as validation prerequisite | Test tooling | Run checked-in Playwright tests without ambient Corepack/pnpm dependency by using local `tsx` fallback or pinned package manager path | `e2e/helpers.ts`, package scripts, test docs | Fresh command receipt in repo: local binary path passes e2e without shim-only `/tmp` workaround |
| 6 | Handoff evidence semantics | Handoff/export model + docs | Export confirmed handoff with `missingRefs` nonempty; assert export may be confirmed but readiness flags do not imply implementation-ready | `export-design-handoff.ts`, HTTP export route, handoff bundle schema/read model | Unit/slice receipt: `confirmed=true` separated from `uiImplementReady=false` or equivalent incomplete-evidence state when refs are missing |
| 7 | Mobile before/after and annotation usability | Preview UX | Open staged preview at 390px; before/after uses vertical stack or segmented Before/After/Diff; annotation hides form until target selected and shows component/comment state | Preview HTML/CSS in `src/cli/studio.ts`, annotation iframe, pending panel | Playwright mobile screenshot receipt: panes inspectable; no blank/narrow comparison; severity constrained; hover/selected target and comment count visible |
| 8 | Governance hygiene docs/test-count/state sync | Docs + validation claims | Run a docs consistency check or explicit grep-backed review for test counts, preview capability wording, CRAFT/PLAN state, SPEC invariant row | `CRAFT.md`, `PLAN-NEXT.md`, `SPEC.md`, `ARCHITECTURE.md`, test protocol docs | Commit-time or review receipt: current unit/e2e counts match live command; stale "read-only preview" and old persistence invariant removed or marked historical |
| 9 | Minimal OD-inspired `CraftEvidencePack` slice inside Studio gates | Evidence/profile layer | Register candidate and produce minimal evidence pack with required/advisory/subjective buckets; pack cannot bypass register/baseline/stage/manifest | Candidate provenance, validation/evidence schema, handoff bundle | Unit fixture: missing required craft marks evidence incomplete; subjective critique is advisory only; accepted revision records pack id/hash |

## Quick Wins vs Larger SWUs

Quick wins:

- Fix preview card and annotation source to use current head after Accept/Revert, with original variants collapsed as history/reference. This is the highest-signal witness because Schon already identified the projection split and source shape (Agent 3, lines 214-217, 227-239).
- Add explicit iframe loading/error states and mobile before/after stacking or segmented view. This directly addresses blank/narrow panes without changing the state machine (Agent 1, lines 71-74; Agent 3, lines 218-222).
- Replace free-text severity with constrained controls; hide/disable annotation form until target selection; show selected target and captured comment count (Agent 3, lines 219-222).
- Patch `watch` next-step language so drafted/approved/staged states name the valid next action rather than reporting idle during `MutationDrafted` (Agent 1, lines 69, 80-81).
- Reconcile docs/test-count drift and preview wording before making stronger release/ergonomics claims (Agent 4, lines 265-286, 314-325).

Larger SWUs:

- Preview coherence SWU: define whether preview reloads file-backed state per request, watches store versions, or owns all mutation routes while running. The witness must include external CLI mutation while preview is active.
- Honest diff SWU: add global/style/visual diff lane and prevent zero-diff confidence when raw candidate hash or visible style changed.
- Durable action framing SWU: confirmation sheet, revision/candidate identity, diff recap, inspected checkbox, and Revert preview-before-commit.
- Evidence semantics SWU: split "export confirmed" from "implementation-ready," especially when `missingRefs` exists.
- Minimal `CraftEvidencePack` SWU: Studio-owned, candidate-level, gate-aware evidence pack. Broader `GeneratorProfile`, `DesignObjectiveBrief`, seeds, `CritiqueReview`, tweak sessions, and source-derived provenance wait for phase two.

## Non-goals / Forbidden Claims

Do not claim:

- Studio is a generic design generator.
- Studio emits production HTML or provides a production HTML path.
- Body War/TROQAR proves Studio HTML is production-ready. It proves selector/copy obligations can become app specs/tests (Agent 4, lines 273-278, 306-309).
- Browser/control projection is currently reliable governed-state projection.
- Zero-diff visible CSS/theme changes are acceptable as honest diff evidence.
- Critique/taste scoring can hard-gate durable changes before calibration.
- Open Design replaces Studio identity, runtime, admission gates, or authority.
- Studio should become an Open Design clone.
- Studio's control model is human-vs-agent identity gating. Current governance is reversibility plus explicit export confirmation; do not reopen identity gating without a new decision (Agent 4, lines 250-253, 288-293).
- Handoff `confirmed` means implementation-ready when required refs/evidence are missing.
- Fresh checked-in e2e proof exists until the Corepack/pnpm helper fragility is resolved or the validated fallback is made first-class (Agent 1, lines 16-20, 64-67; Agent 4, lines 258-263, 314).

## Verdict Matrix

| Claim | Verdict | Evidence |
|---|---|---|
| Reversible prototype state machine exists | Supported | Variant register, baseline, apply staged, accept, append-only revert, export confirmation all reported working by Turing (lines 52-63). |
| Browser/control projection is trustworthy | Not yet supported | Accepted head can be correct at `/raw/baseline` while visible card/annotation still show original variant; preview misses external CLI writes (lines 66-73, 214-217, 227-239, 310-320). |
| Export confirmation boundary is real | Supported | Core export requires `confirmedBy`; HTTP passes `confirm`; tests cover refused/confirmed paths (lines 248-255, 306-309). |
| Diff evidence is honest for visible style/theme changes | Fails current witness | TROQAR theme edit produced zero diff despite visible CSS/theme change (lines 66-69, 168-170, 237-239, 310-320). |
| Body War/TROQAR is useful precedent | Supported with constraint | Valid for selector/copy obligations into specs/tests, explicitly not production HTML proof (lines 273-278, 306-309). |
| UX ergonomics are ready for stronger claims | Not yet supported | Durable controls lack framing; mobile before/after not inspectable; annotation affordances incomplete (lines 216-222, 235-242). |
| Open Design should be imported wholesale | Rejected | Useful as evidence/profile scaffolding only; direct artifact output, connector assumptions, subjective gates, and identity replacement violate Studio governance (lines 139-145, 156-187). |
| Docs/test claims are synchronized | Not supported | CRAFT/PLAN stale state, SPEC/ARCH drift, test-count mismatch, and Corepack e2e fragility reported (lines 265-286, 314-325). |

## Next Implementation Order

1. Fix current-head projection first: accepted/reverted/current head must drive primary preview, annotation surface, before/after state labels, and recorded browser state. Include external CLI write observation in the witness.
2. Fix visible-change diff integrity: CSS/theme/layout-visible edits need a global/style lane or explicit non-attributable visible-change disclosure; zero-diff visible edits must fail validation.
3. Fix preview coherence across CLI/server mutation paths: reload, watch version, or route mutations through preview while running. Pick the smallest design that gives deterministic state receipts.
4. Add durable action framing for Accept/Revert: confirmation sheet, candidate/revision id, diff recap, inspected checkbox, and post-action undo/revert explanation.
5. Make e2e deterministic without ambient Corepack/pnpm fragility. This is a validation prerequisite, not the product's central defect.
6. Tighten handoff evidence semantics: confirmed export remains allowed, but readiness flags must not overclaim when `missingRefs` or required evidence gaps exist.
7. Improve mobile before/after and annotation usability: stacked or segmented comparison, selected/hover target outlines, component/comment list, constrained severity, iframe load/error states.
8. Reconcile governance hygiene docs, test counts, preview capability wording, and state persistence claims.
9. Add only the minimal OD-inspired `CraftEvidencePack` slice behind Studio gates. Defer broader GeneratorProfile, DesignObjectiveBrief, seed/archetype, CritiqueReview, tweak-session, and provenance expansion until browser state truth and diff truth are fixed.

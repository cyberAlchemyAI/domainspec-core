---
id: ui-prototyping-studio-work-pack
project: ui-prototyping-studio
title: "UI Prototyping Studio — Comprehensive Work-Pack (program plan + executable SWUs)"
status: proposal
node_type: work-pack
updatedAt: 2026-06-16
---

# UI Prototyping Studio — Comprehensive Work-Pack

**Goal:** one master plan for the whole studio program — the near-term buildable slice (extraction +
the mutation-execution core L0–L3 + accessibility/layout + e2e) as **executable SWUs**, and the
deferred layers + research tracks as a **roadmap with triggers**. Planning artifact — `[PROPOSAL]`,
nothing executed; each SWU is run via a separate `task-session`.

## Scope & standing decisions (do not re-open)

- **Build scope = L0→L2** survival/trust floor (`DEC-ONE-SHOT-SCOPE-002`); L3–L6 deferred.
- **Runtime = Claude Code-native via a `studio` CLI** — no MCP server, no React SPA, no API key
  (`DEC-RUNTIME-CLAUDE-CODE-011`, `DEC-CLI-NOT-MCP-012`).
- **Annotation** = in-prototype `studio preview --annotate` overlay → `data-od-id` target
  (`DEC-INPROTO-ANNOTATION-013`, `DEC-ATOMIC-IDS-014`).
- **Mutation execution = Approach C** (propose→validate→stage→accept→record; admission-boundary
  determinism) `DEC-MUTATION-EXEC-015`; V3 fence **spike-proven buildable** (`DEC-C1-SPIKE-SURVIVED-016`).
- **Extraction execution:** accept domainspec breakage (`DEC-EXT-DOMAINSPEC-BREAK-018` → P4 de-register
  is OPTIONAL); **plain move** (`DEC-EXT-GIT-HISTORY-019`); **leave changes uncommitted** for review
  (`DEC-EXT-COMMIT-POLICY-020`).
- Assumptions at defaults (confirm at execution): docs at project root (D-EXT-1); pnpm workspace
  (D-EXT-3); Node ≥20 + pnpm pinned in `engines` (D-EXT-5).
- **Review gate (`DEC-UX-REVIEW-FIX-BEFORE-BUILD-023`):** the SKILL/design draft passed a red-team review
  (dispatch `2026-06-16-ups-skill-design-review`, resolved). The doc-fix findings (F1/F3/F4/F5/F6/F7/F8)
  are **APPLIED** to the run drafts (`development/refinement-runs/20260616-ui-ux-interaction-skill/`, see
  `REFRESH-REPORT.md`). The remaining blocker is **F2 / R-S7-1** — the core has **no human-vs-agent
  identity gate** (`approve` has zero actor check; `apply` refuses only literal `system:auto`); the SKILL
  never-do spine is currently the SOLE control. Build is gated on the **F2 decision** (`PLAN-FIXES.md`).

## Program map (waves)

```
W0 Review gate     : F2a identity-gate decision · S1 install corrected SKILL · B-PRE overclaim guard  (PLAN-FIXES.md; gates the build)
W1 Extraction      : SWU-X1 backend lift → SWU-X2 studio CLI + skill        (unblocks everything)
W2 Mutation L0     : SWU-M0a schema · SWU-M0b artifact port · SWU-M0c canonicalizer   (||, after X1)
W3 Mutation L1     : SWU-M1 validator suite V1–V9b + whole-tree V3 fence     (after M0*)
W4 Mutation L2     : SWU-M2 two-gate apply state machine                     (after M1)
W5 Mutation L3     : SWU-M3 recorder atomicity + rollback                    (after M2)
W6 UX floor        : SWU-U1 accessibility (L1) · SWU-U2 layout integrity (L2) (||, after X2)
W7 Annotation/view : SWU-P preview + annotate overlay                        (after X2 + M0a)
W8 E2E + meta      : SWU-E e2e suite · SWU-Z project meta/workspace          (after the above)
— deferred —       : R2/calibration spike, UX/ergonomics research, L4–L6     (roadmap, off critical path)
```

Wave order is by dependency; SWUs marked `||` run in parallel. Each SWU is one `task-session` parent task.

---

## SWU manifest (shared)

| SWU | Title | Wave/Layer | Depends on | Write scope | Acceptance (one-line) |
|-----|-------|-----------|-----------|-------------|-----------------------|
| **X1** | Backend standalone lift | W1 / P1 | — | `backend/**` (new) | `pnpm --filter backend build` + slice test green; studio routes serve |
| **X2** | `studio` CLI + operating skill | W1 / P1.5 | X1 | `backend/src/cli/**`, `SKILL.md` | CLI drives the full loop; gates server-side; skill present |
| **M0a** | Schema migrations | W2 / L0 | X1 | `backend/.../domain/models.ts` | `MutationTask.odId`+`MutationChangeType`, `DiffSummaryHonest`/`OdDiffFragment`, `ExecutionProvenance`; tsc green; checksum re-baseline |
| **M0b** | Artifact content port | W2 / L0 | X1 | `application/ports.ts`, `infrastructure/*` | `readHtml/stageHtml/commitHtml/discardStagedHtml/removeRevision` on the store; unit tests |
| **M0c** | Shared canonicalizer | W2 / L0 | X1 | `backend/.../canonicalize.ts` | `domainspec-html-canon` deterministic; one module both sides of seam; unit tests |
| **M1** | Validator suite + V3 fence | W3 / L1 | M0a,M0b,M0c | `application/validators/**` | V1–V9b + composite fail-closed; whole-tree V3; C-1 toy-game fixtures pass as regressions |
| **M2** | Two-gate apply state machine | W4 / L2 | M1 | `application/apply-*.ts`, `domain` states | `apply`→`RevisionApplied` staged; `accept` commits exact `candidateHtmlHash`; reject/discard; AC-L0-11/12 |
| **M3** | Recorder atomicity | W5 / L3 | M2 | `application/record-*.ts`, `infrastructure` | all-or-nothing commit + compensating rollback via `removeRevision`; INV-6 one-append |
| **U1** | Accessibility (L1) | W6 | X2 | `studio preview` overlay + any surface markup | axe zero violations on surfaces; keyboard loop; focus trap on accept; AC-L1-* |
| **U2** | Layout integrity (L2) | W6 | X2 | overlay/preview CSS | no overflow/clip/overlap; ≥24×24 targets; responsive; AC-L2-* |
| **P** | `studio preview` + annotate overlay | W7 | X2, M0a | `backend/src/cli/preview.ts`, overlay asset | click-to-annotate captures `data-od-id`→`CommentEvent`; gated by INV-2; AC-L0-11 |
| **E** | E2E suite | W8 | M2,P,U1 | `e2e/**`, `playwright.config.ts` | wp01/wp02wp03 pass against a scripted proposer (no live LLM in CI) |
| **Z** | Project meta + workspace | W8 | all above | `package.json`, `pnpm-workspace.yaml`, `README` | `pnpm install && build && test && test:e2e` green from project root |
| **X4** | De-register from domainspec (OPTIONAL) | any | — | domainspec submodule | `DEC-018` accept-breakage → optional cleanup, not required |

---

## Per-SWU contracts (executable detail)

### SWU-X1 — Backend standalone lift
- **Write scope:** `projects/ui-prototyping-studio/backend/**`.
- **Steps:** move `implementation/domainspec/backend/src/modules/ui-prototyping-studio/` → `backend/src/modules/...` (plain move, `DEC-019`); write `backend/src/index.ts` (fastify + `@fastify/cors` + `registerUiPrototypingStudioRoutes` + listen; explicit `.data/` path); `package.json`/`tsconfig.json`/`.gitignore`.
- **Done:** `pnpm --filter backend build` clean; `ui-prototyping-studio.slice.test.ts` passes; `curl` a studio route. **Verify:** those three commands.

### SWU-X2 — `studio` CLI + operating skill
- **Write scope:** `backend/src/cli/**`, project `SKILL.md`.
- **Steps:** CLI (node/tsx) over the orchestration module — `session open`, `prompt submit`, `variants register --from|--fake`, `state`, `baseline select|commit`, `comment add`, `synthesize`, `batch approve`, `apply`, `accept`, `discard`, `revisions`, `handoff export`, `preview`. Gates enforced in the core behind the CLI (INV-3/4/5/8). Operating `SKILL.md`: Claude Code generates + `variants register` + stamps `data-od-id`; never self-approve/apply.
- **Done:** a scripted session drives generate→register→baseline→comment→synthesize→approve→apply→accept→handoff; `apply`/`accept` reject non-approved/auto/stale. **Verify:** CLI integration test + `--fake` e2e path.

### SWU-M0a — Schema migrations `[algorithmic]`
- **Inputs:** current `models.ts`. **Outputs:** `odId: string|null` + `MutationChangeType = 'add'|'remove'|'change'` on `MutationTask`; `DiffSummaryHonest` + per-od-id `OdDiffFragment` (counts derived from od-id set-diff, `buildDiffSummary` deleted); `htmlArtifactRef`+`candidateHtmlHash`+`provenance: ExecutionProvenance` on `RevisionManifestEntry`.
- **Rules:** `synthesize` copies `comment.target.odId`; batch `sha256` re-baselined with a **checksum version stamp** (old batches must not read as tampered). **Edge cases:** `odId` null → degrade to selector (lower fidelity, flag). **Failure modes:** unstamped batch under new checksum. **Verify:** type-check + synthesis determinism test (identical comments → identical task IDs + checksum).

### SWU-M0b — Artifact content port
- **Write scope:** `application/ports.ts` (+ file-store impl). **Outputs:** `readHtml(ref)`, `stageHtml(candidate)→tempRef`, `commitHtml(tempRef)→headRef`, `discardStagedHtml(tempRef)`, `removeRevision(id)`.
- **Done:** the store can read/stage/commit/discard HTML + remove a revision (today it has none of these). **Verify:** port unit tests incl. discard leaves no trace.

### SWU-M0c — Shared canonicalizer `[algorithmic]`
- **Inputs:** raw HTML. **Outputs:** canonical tree (attribute-order normalize, whitespace collapse, void-element normalize, od-id preserve). **Rules:** pure, clock-free, deterministic; the **same module** used by the proposer-facing and validator-facing sides (the dominant source of accidental non-determinism). **Verify:** idempotency test (canon(canon(x))==canon(x)); identity hash stable across runs.

### SWU-M1 — Validator suite + whole-tree V3 fence `[algorithmic]`
- **Reference:** port the C-1 spike `run_spike.py` logic. **Inputs:** `(candidateHtml, taskScopeOdIds, frozenBaselineBinding, r1ScopeRuleSpec)`. **Output:** `AdmissionVerdict` (admit/reject).
- **Ordered rules:** run V6→V1→V2/V4→V3→V7→V9→V9b→V5(soft)→V8; composite **fail-closed** (all required pass⇒admit). **V3 (crux):** whole-tree canonical diff with od-id attribution — any change not dominated by a TaskScope od-id ⇒ REJECT; ⊥/unattributable ⇒ REJECT. **Integrity:** candidate-asserted od-id vs `frozenBaselineBinding` mismatch ⇒ REJECT. **CSS:** rule attributed to od-ids its selector resolves to over the canonical tree.
- **Edge cases:** byte-adjacent out-of-scope sibling; CSS spanning in+out scope; forge/re-tag; node add/delete. **Failure modes:** od-index-blindness (the toy-game falsifier — must NOT regress). **Verify:** the 11 C-1 fixtures (GOOD/BAD/HELD-OUT) as passing regression tests; carry `GAP-V3-NODE-IDENTITY-008` (reordering/cascade for production).

### SWU-M2 — Two-gate apply state machine `[algorithmic]`
- **Flow:** `MutationApproved` →[propose (Claude Code, impure)]→[validate (M1)]→ required-fail ⇒ REJECT (no write, stay `MutationApproved`, bounded `maxProposeAttempts` retry); admit ⇒ **stage** candidate at temp ref (`RevisionApplied`, NOT head) + compute/show `DiffSummaryHonest` → human **accept-diff** → [record] → `RevisionRecorded`; `discard` → back to `MutationApproved`.
- **Rules:** whole-batch all-or-nothing; **idempotency-at-verdict** (commit exactly the previewed `candidateHtmlHash`, seen==recorded); accept-time staleness re-check (INV-5). **Verify:** state-transition tests + AC-L0-10/11/12; INV-3/4/5/6/8 server-side rejection tests.

### SWU-M3 — Recorder atomicity
- **Rules:** record = all-or-nothing single commit point; on failure, compensating rollback via `removeRevision` (today only detect, not compensate). **Verify:** inject a mid-record failure → no partial revision, head unchanged.

### SWU-U1 / U2 — Accessibility / Layout (L1/L2)
- **U1:** keyboard-operable gates, ARIA roles/names, focus trap + return-focus on the accept-diff dialog, `aria-live` once on state change, non-color-only cues. **Verify:** `@axe-core/playwright` zero `button-name`/`label` violations; keyboard-only loop.
- **U2:** no overflow/clip/overlap (bounding-box assertions); WCAG 2.2 ≥24×24 on irreversible controls; responsive. **Verify:** layout/measurement checks across breakpoints.

### SWU-P — `studio preview` + annotate overlay
- **Steps:** `preview [--annotate]` serves variant/revision HTML from an ephemeral local server; `--annotate` injects a click-to-annotate overlay → captures `data-od-id` (selector fallback) + label → POST → `CaptureCommentEvent` (gated INV-2). **Verify:** click an element → `CommentEvent` identical in shape to `comment add`; rejected before baseline exists.

### SWU-E / Z — E2E / Project meta
- **E:** move e2e + adapt `playwright.config.ts`; scripted proposer (no live LLM in CI); wp01/wp02wp03 green. **Z:** root `package.json` + `pnpm-workspace.yaml` + `README`; fresh `pnpm install && build && test && test:e2e` green.

---

## Implementation-layering (value/cost boundaries)

- **L0 substrate (M0a/b/c)** — minimum working unit; *unblocks everything*; promotion evidence = tsc + unit tests + determinism test.
- **L1 (M1)** — the fence is the load-bearing risk; promotion = the 11 C-1 fixtures pass.
- **L2 (M2)** — the governance/ergonomics gate; promotion = state-machine + invariant tests.
- **L3 (M3)** — durability hardening; promotion = failure-injection rollback test.
- Promotion is by evidence from the prior layer, never preference. L0–L3 build now; **L4+ is research-gated.**

## Validation strategy (per slice)

Unit tests (M0*, validators) → slice tests (M1/M2 against the orchestration module) → e2e (SWU-E, scripted proposer) → the C-1 regression fixtures guard the fence permanently. Every SWU names its verify command above.

## Deferred roadmap (off the critical path)

| Item | Type | Trigger to start |
|------|------|------------------|
| **R2 / calibration spike** (R2-a vs R2-b, `S/B/k/c`) | research track 2 (`DEC-R2-CSS-ATTRIBUTION-017`) | before L4 build; pre-registered like C-1 |
| **UX/ergonomics research** (trust meter OQ-1, the unproven ergonomics floor) | research track 1 (`GAP-ERGONOMICS-UNPROVEN-001`) | feeds L6; human-study |
| **L4 identity/DNA + conformance-delta** | future layer (`BLK-IDENTITY-TYPES-002`) | after R2 decides; atomic-design taxonomy |
| **L5 fitness scoring + preference learning** | future layer (proof-gated, D-009) | after L4 |
| **L6 human-evidence / trust ergonomics** | future layer | after UX research |
| **L3+ failure/recovery states** | `BLK-FAILURE-STATES-003` | mock failure-injection |

## Carried residue / known gaps

`GAP-V3-NODE-IDENTITY-008` (reordering/cascade for production V3) · `GAP-ACCEPTANCE-CHECK-007` (acceptanceText human-judged, not machine-checked) · `GAP-COMPONENT-REGISTRY-002` · `GAP-CONFLICT-ALGEBRA-003` · `GAP-ERGONOMICS-UNPROVEN-001` · `GAP-DOCS-CODE-SPLIT-005` (resolves when code moves, X1/X4).

## Next route

**W0 first** (`PLAN-FIXES.md`): `decision-gate` for **F2a** (the core identity-gate decision) is the only
blocker; then `task-session` for **S1** (install the corrected SKILL) + **B-PRE** (overclaim grep guard),
and **F2b** if F2a says before-build. Then `task-session` per SWU in wave order W1→W8 (start **SWU-X1**).
The two research tracks run in parallel, off this critical path.

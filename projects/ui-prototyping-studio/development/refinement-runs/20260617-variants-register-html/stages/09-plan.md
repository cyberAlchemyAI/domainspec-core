---
id: plan-variants-register-html
run_id: 20260617-variants-register-html
step_id: s9-plan
capability_ref: invoke (plan)
status: proposal
complexity: medium
updatedAt: 2026-06-17
---

# Plan — build `variants register` HTML ingestion (lifts WW2)

Non-executed. One SWU (with a small CLI + harness rider). Dependencies all EXIST (M0b, M0c, the
`htmlArtifactRef` field) — no F2 dependency; buildable now.

## SWU — MR1: registerVariants use-case + CLI + gate `[algorithmic]`

- **Write scope:** `application/register-variants.ts` (new), `application/studio-orchestration-module.ts`
  (wire), `domain/errors.ts` (+`OD_ID_MISSING`), `cli/studio.ts` (`variants register` ingestion),
  `application/register-variants.test.ts` (new).
- **Inputs:** `{ sessionId, variants: [{ label, html }], requestedBy }`.
- **Outputs:** `{ session(VariantsReady), variants: PrototypeVariant[] }` with each `htmlArtifactRef` set to
  a **committed content ref** (M0b), HTML canonicalized (M0c).
- **Ordered rules:**
  1. session exists + prompt set (mirror `generateVariants` guards).
  2. for each variant: `canonical = canonicalizeHtml(html)`.
  3. **gate:** if `canonical` has zero `data-od-id` attributes → throw `OD_ID_MISSING` (reject all, no writes).
  4. `staged = port.stageHtml(canonical)`; `ref = port.commitHtml(staged.stagedRef)`.
  5. build `PrototypeVariant{ htmlArtifactRef: ref, ... }`; `store.saveVariants`.
  6. variant count must equal supplied count (else `VARIANT_GENERATION_COUNT_MISMATCH`).
- **Edge cases:** duplicate labels (reject); 1-variant auto-commit baseline (mirror stub); re-register
  same HTML → same committed hash (idempotent, M0b). **Failure modes:** od-id-less HTML admitted (the
  toy-game BAD case must reject); dangling ref after partial write (commit only after all canonicalize+gate pass).
- **Verify:** `register-variants.test.ts` — GOOD admit + `readHtml(ref)===canonical`; BAD → `OD_ID_MISSING`;
  idempotent hash; `pnpm --filter backend test` green; `tsc` clean.

## CLI rider (within MR1 scope)

- `studio variants register <sid> --label A --file a.html` (repeatable) — reads file(s), builds the
  `{label,html}[]`, calls `registerVariants`. Keep `variants generate` as the stub testable-surface path
  (unchanged). Optional `--from <dir>` sugar deferred.

## Harness rider — WW2 closure (within scope)

- Capture the registered variant's committed HTML (via `readHtml(ref)`); the harness M2 checks `data-od-id`
  in **that HTML**, not transcript args. Add a GOOD/BAD register fixture pair. **Verify:** M2 now exercised
  (pass on GOOD, the runner flags a BAD register).

## Implementation-layering

- **L0:** the registerVariants use-case + gate (the unit). Promotion = the GOOD/BAD/idempotent tests.
- **L1:** CLI ingestion (`--label/--file`). Promotion = a live register call sets a resolvable ref.
- **L2:** harness M2 closure. Promotion = M2 exercised green on a real registered variant.

## Validation strategy

unit (register-variants.test.ts) → CLI integration (register → `state`/`readHtml` resolves) → harness M2
(GOOD pass / BAD flag) → the §3 toy-game GOOD/BAD/idempotent as regression fixtures.

## Residue / gaps

- `GAP-OD-ID-GRANULARITY`: MVP gate is coarse (≥1 `data-od-id`); per-component requirement is a follow-up.
- Real generation *content quality* (does the agent produce good variants?) is out of scope — this only
  ingests + gates structure, per the SKILL's propose-only posture.

## Next route

`task-session` to build **MR1** (no F2 dependency). After MR1, WW2 is lifted and the first test's M2 becomes
exercisable; WW3 (install) still waits on the F2 decision.

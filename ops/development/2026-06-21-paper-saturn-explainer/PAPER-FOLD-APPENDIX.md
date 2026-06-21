---
node_type: paper-appendix
title: DomainSpec — Development & Roadmap Appendix (built results fold)
status: draft
created: 2026-06-21
owner: research-synthesis
relates_to: research/projects/domainspec/papers/domainspec-paper.md
scope: appendix-only — does NOT modify the paper body
---

# Appendix — Development & Roadmap

This appendix folds REAL, BUILT results into the DomainSpec paper without altering its
body. The paper body (Section 9.4) states the determinism (E1) and mutation (E3)
experiments "have not yet been run" and grades all four contributions as architectural
except C2 (partial support from E6/E9). This appendix updates that status with shipped
artifacts and run results. Every claim cites its artifact. Claim ≤ proof.

---

## A.1 What has been built

### A.1.1 Deterministic test-derivation engine (closes C2's mechanism in code)

A deterministic test-derivation engine exists and is validated. It lives at
`implementation/domainspec/tools/test-derivation-engine/`.
Source of truth:
`implementation/domainspec/development/refinement-runs/2026-06-21-llm-replacement-plan/EXECUTION-REPORT.md`
and `implementation/domainspec/development/deterministic-test-derivation-engine/` (SPEC, ARCHITECTURE, LIFECYCLE-ARCHITECTURE, GLOSSARY, L0-ROUNDTRIP-REPORT, WORK-PACK).

The engine implements the parse → delta → key → emit pipeline. It realizes the
paper's $T = f(C, R, \Delta)$ as running code, not prose.

Built and validated (L0–L4):

- **L0 — file write.** `derive --out` writes `TEST-SPEC.engine.md` side-by-side; ran on financial-settlement (67 obligations).
- **L0 — Option-C identity.** sha1 core id + human-ID projection; `id-maps/*.idmap.json`; 9 unit tests.
- **L0 — provenance.** header outside a fenced engine region, body inside it.
- **L0 — fail-closed (G4).** parser violations return exit 4 with no write.
- **L0 — emit_dir containment (G3).** `paths/containment.ts`, 4 unit tests; retrofit on the live `emit-tests` path.
- **L0 — drift check (G2).** `check` mode proven STALE (exit 7) on in-region perturbation, FRESH otherwise.
- **L1 — source completeness gate + coverage summary.**
- **L2 — tier split (G1).** `tierOf` produces 3 tiers; financial-settlement = pure 24 / needs-harness 42 / needs-formal 1.
- **L3 — domain/rules grammar.** `parseDomain` (DomainField + Enum) + `parseRules` (transition/invariant/policy-decision δ); 3 new rule types. AEO corpus: 263 obligations (71 domain-field, 7 domain-enum, 6 policy-decision, …); financial-settlement 67→79.
- **L4 — self-derive fixpoint (closes C4 in practice).** The engine derived its OWN feature → committed `docs/features/test-derivation-engine/TEST-SPEC.engine.md` (31 obligations). "Has derived," not just "can."
- **L4 — coexistence merge boundary.** `check` scans OUTSIDE the fence for engine-ID rows and fails closed if an LLM redefines a backend ID; proven 0-overlap FRESH on all 3 features.
- **L4 — live-skill wiring.** `domainspec-generate-tests` rewired ENGINE-FIRST across all 4 mirrors (.claude/.agents/.github/copilot): engine emits the fenced backend block; the LLM authors only UI/E2E + scaffolding outside it.

Validation, real numbers:

- **95 engine tests** pass (started at 76 → +13 in the L0–L2 work, then to 95 with L3); `npm run typecheck` = 0 errors.
- Output is **byte-stable** across runs; drift/containment negative controls pass.

Honest scope (from the report): backend-domain obligations only — operation-class +
invariant/calculation/postcondition, with stable human IDs, provenance, drift detection,
and an honest tier/gap ledger. UI/E2E + scaffolding remain LLM-owned by design. The live
pipeline swap is wired but not yet run end-to-end on a feature with a UI-SPEC.

### A.1.2 E3 mutation testing — RUN (the paper body marks this "not yet run")

Source: `implementation/domainspec/docs/research/results/E3-results.md`. Tool: Stryker 9.6.1
+ vitest 4.1.1, 160 mutants on the pure `src/domain` cluster, 0 errors / 0 timeouts.

Three labelled arms, real mutation scores:

| Arm | mutation_score | covered_score |
| --- | --- | --- |
| derived (engine-emitted) | **38.75%** | 47.69% |
| pipeline-reference (existing tests) | **58.75%** | 69.63% |
| combined | **65.00%** | 74.82% |

Per-file, the engine matches or beats the existing suite where it has a value-asserting
oracle: `deal.service.ts` derived **100%** (10/10) vs pipeline-reference 40%.

After the closed-form computational-obligation fix (FoldAst/PiecewiseAst/ArithExpr,
`applyMakeupPolicy` authored closed-form from documented semantics, not the impl):

- derived aggregate **38.75% → 54.37%** (+15.6 pts).
- `makeup-policy.service.ts` **17.2% → 36.56%** (+19.4 pts, doubled).
- The regenerated `__derived__` suite passes **13/13** against the real unmutated code — no spec/impl mismatch.

Honest framing (as run): there is no clean-room manual arm (infeasible), so the comparison
is deterministic-emitter vs the project's existing tests, not spec-vs-no-spec. The 38.75%
gap was structural-but-unwritten-spec, not implementation divergence — confirmed by the
closed-form catch-up. This is the financial-settlement pilot, not a corpus-wide result.
C2 is **supported, narrowly and honestly**: the deterministic emitter produces real
fault-detecting tests reproducibly, with zero human variance.

### A.1.3 Spec-formalization metric (shipped)

The engine emits a spec-formalization metric. On financial-settlement: **96.0%**
(pure 24 / (24 + 1)), reported in the execution report and the engine's SPEC
(`implementation/domainspec/docs/features/test-derivation-engine/SPEC.md`). It is the
trustworthiness signal for derivation: the fraction of the graph that is fully formalized
versus left as honest needs-harness/needs-formal gaps.

### A.1.4 Conformance validator (defined + pre-registered, not yet built)

Source: `implementation/domainspec/development/spec-conformance-validator/EXPERIMENT.md`
(status: defined). A pre-registered experiment asks whether to add a `validate` capability
that checks LLM specs against the 25 meta-types (TAXONOMY) and 29 typed edges
(RELATIONSHIPS) — four checks V1–V4 (node meta-type, edge type, edge endpoint signature,
cross-layer/cross-feature rules). The decision criterion is frozen before any run: build +
gate iff seeded_recall = 100% on all four levels AND false_violation_rate = 0 AND a real
violation rate > 0 appears on real or held-out specs. Build prerequisites P1–P3
(registry.md parser, explicit-type resolution, signature table) gate the run. This is
designed and frozen; it is NOT yet built or run.

---

## A.2 Approved subagent dispatches

Source: `telemetry/agents/subagents-dispatch.yaml` (append-only, register-dispatch-written).
This is an honest tabulation of what actually ran — not a capability claim.

- **58 dispatches** recorded, spanning 2026-06-15 → 2026-06-17, each passing the human gate
  (final_approver set; 37 "parent", the rest named human reviewers).
- By dispatch_type: **42 research, 15 review, 1 code**. Only research/review/code appear;
  experiment/plan/suggestion are reserved names and were not dispatched.
- Invoked by the two paper authors (rondelli.vladimir / rondellivladimir, victorboscaro).
- Work pattern: research dispatches gathered inputs and mapped precedents (subagents-strategy
  wiring, framework-unification, cross-project method maps); review dispatches were adversarial
  red-teams and coverage audits (framework-unification artifacts, the DomainSpec spec template
  family, Savvy/Z-Rig/ui-prototyping-studio reviews), several closed by dedicated
  coverage-auditor / auditor approvers rather than "parent".

Honest note: these dispatches supported repository and method development around DomainSpec;
they are not the paper's controlled experiments (E1–E20). They evidence that the
subagent-governance machinery the paper describes was exercised under a held human gate, with
tensioned research/review roles, at real volume.

---

## A.3 Roadmap (planned — NOT done)

Marked explicitly as future work. None of the below is claimed as built.

- **L3 widening.** Add value-asserting oracles for more domain-field / policy-decision rows
  (currently honest needs-harness skips). The makeup-policy closed form is an under-model
  (agrees with the impl on the chosen fixture only); a fully faithful piecewise sequential
  form is required. (E3-results.md, P4.)
- **Conformance validator build.** Execute P1–P3, then run the pre-registered experiment
  against its frozen §5 criterion; gate `derive` on `validate` only if the criterion is met.
  (spec-conformance-validator/EXPERIMENT.md.)
- **Pipeline LLM-replacement remaining.** Run the rewired engine-first
  `domainspec-generate-tests` end-to-end on a feature with a UI-SPEC to exercise
  engine(backend) + LLM(UI/E2E) coexistence; the live pipeline swap is wired but gated.
  (EXECUTION-REPORT.md residue.)
- **E3 pilot → corpus.** Commit the `__derived__` suite as a real pre-registration anchor,
  add 2-rater survivor classification (κ), pre-register corpus gates from the pilot
  distribution, then re-run across the corpus. (E3-results.md gates.)
- **Paper's other open experiments.** E1 (determinism), E4/E5 (attenuation), E10
  (productivity) remain unrun; C1/C3/C4 stay architectural pending them (paper §9.4).

---

## A.4 Consolidation recommendation

**Canonical copy:** `research/projects/domainspec/papers/domainspec-paper.md` — it is the
single source of truth (it already carries the published `.html` sibling); retire the
byte-identical `implementation/domainspec/docs/research/domainspec-paper.md` to a one-line
pointer (or symlink) to avoid the two-copy drift on the author byline.

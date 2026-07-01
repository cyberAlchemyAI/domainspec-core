---
node_type: work-pack
is_session: false
status: candidate
boundary: LOCAL RESEARCH ONLY — no spec/code/schema mutation (SEED.md:56-58); engine black-box; v1 read-only
created: 2026-07-01
authored_by: invoke (mode: plan)
define: ../DEFINE.md
design: ../DESIGN.md
layering: ./implementation-layering.md
target_artifact: spec-ontology-unification toy (Lane Z falsification)
complexity: medium
---

# Spec–Ontology Unification Toy — Work-Pack

Runs the DESIGN's measurement harness over the financial-settlement corpus to decide DEFINE's frozen
four-part criterion (Lane Z substrate viability), then weighs Lane A. **Output is a verdict + evidence,
never a spec/code change** (promotion boundary). Corpus:
`impl/test-derivation-engine/__fixtures__/financial-settlement/` (v1 read-only; the fixture is the v2 copy).

## SWU manifest
| SWU | Layer | Title | Acceptance (reviewable) |
| --- | --- | --- | --- |
| **T1** | L0 | Extract the spec-graph | Typed node + edge inventory for the corpus; each item typed or flagged unclassifiable |
| **T2** | L1 | Author the two mapping tables | node→pattern + edge→composition filled for every T1 item; unmapped items listed |
| **T3** | L2 | Run the toy + attack (the falsification) | Criterion FROZEN; paper skeleton + M1–M4 + exception lists; determinism re-run matches; 3 attack lenses exercised |
| **T4** | L3 | Lane A compare + verdict | SURVIVED/FALSIFIED/INVALID vs frozen bars; Lane A weighed; promotion recommendation |

---

## T1 — Extract the spec-graph  (L0)
- **Write scope:** `research/spec-ontology-unification/toy/graph.md` (new).
- **Steps:** read the corpus `domain.md` (+ any aspect files present); list every concept as a node with its TAXONOMY type; list every relation as an edge with its RELATIONSHIPS type + endpoints.
- **Impl detail:** node row = `{id, TAXONOMY-type}`; edge row = `{from, edge-type, to}`. A concept that fits no type is recorded as `unclassifiable` (a live M1 signal, not an error to hide).
- **Validation:** every domain.md concept appears exactly once; counts noted (feeds M1). **Edge case:** if the corpus exercises <3 TAXONOMY categories → stop, mark **INVALID**, escalate to agent-execution-orchestrator (DEF-D1).
- **Verification:** reviewer confirms the inventory matches domain.md (no concept missing/invented).

## T2 — Author the two mapping tables  (L1)
- **Write scope:** `research/spec-ontology-unification/toy/mapping.md` (new).
- **Steps:** for each node-type in T1, copy its pattern from `impl/spec/TAXONOMY.md` "Architecture Mapping Appendix"; for each edge-type in T1, write its composition rule (DESIGN §2 table is the seed).
- **Impl detail:** a node-type with 0 appendix patterns or >1 candidate pattern is recorded as an exception (feeds M2). An edge with no composition rule is a gap (feeds M3). Do NOT invent a pattern to force 1:1 — an honest gap is the finding.
- **Validation:** every T1 node/edge has a row (mapped or explicitly gap). No silent drops.
- **Verification:** reviewer confirms each mapping traces to the TAXONOMY appendix or a stated rule.

## T3 — Run the toy + attack  (L2)  ← the falsification
- **Write scope:** `research/spec-ontology-unification/toy/run.md` (new).
- **PRE-STEP (gate):** FREEZE the criterion — copy DEFINE's four bars + thresholds into `run.md` header, dated, **before** computing anything. No post-hoc threshold edits (experiment discipline).
- **Steps:** apply the T2 mapping to the T1 graph → write the resulting pattern skeleton **on paper** (pattern names + how edges compose them; no real code). Compute M1–M4 with their exception lists. Re-run the computation once from the same inputs and confirm identical metrics (determinism). Then ATTACK (DESIGN §4): 1:1-break, cross-cutting-context, taxonomy-closure-under-stress — each lens gets a paragraph + any break added to the exception lists.
- **Impl detail — inputs/outputs/edge cases/failure modes:**
  - inputs: `graph.md`, `mapping.md`, frozen criterion.
  - outputs: M1–M4 numbers + per-metric exception list + attack findings.
  - edge cases: shared Value Object (Money) reached only via `contains` → classify as named-carrier (M4-b, not unbounded); cross-feature edge → M4-c candidate (unbounded) unless a carrier is named.
  - failure mode: if determinism re-run differs, the mapping is under-specified → record as an M2/M3 finding, do not paper over.
- **Validation:** the frozen criterion is present and dated before metrics; all 4 metrics + all 3 attack lenses present.
- **Verification:** an independent reader can recompute M1–M4 from `graph.md`+`mapping.md` and get the same numbers.
- **Execution route:** run T3 as an **`experiment` dispatch** (pre-registered criterion freeze → run → SURVIVED/FALSIFIED/INVALID) — the experiment skill owns the criterion-freeze + verdict vocabulary; this SWU supplies its design.

## T4 — Lane A compare + verdict  (L3)
- **Write scope:** `research/spec-ontology-unification/toy/verdict.md` (new).
- **Steps:** sketch Lane A for the same feature (generated bidirectional node→pattern map + drift check — the v1 direction); compare whether Lane A gives bounded-agent context without fusion. Render the verdict against the frozen bars: SURVIVED / FALSIFIED / INVALID. Write the promotion recommendation.
- **Impl detail:** the recommendation MUST respect the promotion boundary — it recommends the *next* approved task-session (or "do not pursue Lane Z"), never a spec-schema change here.
- **Validation:** verdict cites M1–M4 vs the frozen thresholds; Lane A explicitly weighed; recommendation names an owner + honors the boundary.
- **Verification:** the verdict is entailed by the metrics (a reader agrees SURVIVED/FALSIFIED follows from the numbers).

---

## Dispatch technique trace
`sequence` (T1→T4 strict) · `owner_boundary_check` (v1 read-only; engine black-box; promotion boundary — output is verdict-only) · `validation_loop` (each SWU acceptance = a reviewable artifact; T3 adds a determinism re-run) · `concrete_path_evidence` (corpus + TAXONOMY appendix + toy/ files named) · `scu_swu_reduction` (4 SWUs, one artifact each) · `recomposition_proof` (→ closes the SEED Lane Z-vs-A decision) · `residue_ledger` (below). **No full dispatch JSON** for the plan itself (single-owner). **T3 execution IS a dispatch** — route it through `experiment` (criterion pre-registration), registered via `register-dispatch`.

## Distill validation — flag
- **Smallest coherent units:** ✅ one artifact per SWU (graph / mapping / run / verdict).
- **Recomposition proof:** ✅ the four artifacts are exactly the evidence the SEED tower needs to decide Lane Z vs A.
- **Gaps named (repair path):** (1) **proxy gap** — the toy measures *substrate viability* (M1–M4), NOT actual agent cost/drift savings; a positive verdict authorizes only a *follow-up agent-run experiment*, not the SEED's full claim → owner: a later experiment tower. (2) **single-corpus** — one feature can falsify but not fully confirm; SURVIVED on financial-settlement → repeat on a richer feature before any promotion.
- **Verdict:** flag (routable; both gaps carried below).

## Residue
- Single corpus (financial-settlement); a SURVIVED verdict is necessary, not sufficient — needs a second feature.
- Proxy: substrate metrics stand in for "cheaper agents"; the agent-cost claim stays unproven until a runtime experiment.
- The node→pattern appendix is v1-authored; its own completeness is under test (M2/M3), so a FALSIFIED result may indict the appendix rather than the hypothesis — the verdict must distinguish these.

## Next route
`experiment` dispatch for **T3** (freeze criterion → run → verdict), with T1/T2 as its inputs and T4 as
its synthesis; or `task-session` per SWU if run solo. Result feeds back to `SEED.md` (close its Lane
assignment) and, only via a later approved task-session, to any spec decision.

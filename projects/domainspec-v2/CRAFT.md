# DomainSpec v2 — Craft (human view)

> Human view of [`.craft/ledger.yml`](.craft/ledger.yml) (source of truth). Scoped space promoted from
> cav2 `CTX-CAV2-DOMAINSPEC-V2` on 2026-07-01 (decision `DEC-DSV2-CRAFT-SCOPE`). cav2 stays umbrella and
> points here. Last updated: 2026-07-01.

## Quick links
- **Next move (root):** execute batch-1 reformulation (R1→R6b) — R3 fixes the toy-exposed edge gaps — **or** stand up the agent-cost experiment for Lane Z vs A.
- **Open decisions:** `DEC-DSV2-LANE-ZA` (Lane Z vs A — deferred).
- **Active blockers:** `BLK-DSV2-DRIFT-ENGINE` (drift not implemented), `BLK-DSV2-L2-ATTESTATION` (attestation capability, human).
- **Active gaps:** `GAP-DSV2-EDGE-CATALOG` (→R3), `GAP-DSV2-COMPOSABILITY-ENFORCE` (9/29), `GAP-DSV2-EXERCISE` (2nd corpus), `GAP-DSV2-GOVERNANCE-CARDS` (2 gov cards owed).

## Contexts
| Context | Stage / gate | State | Next move |
| --- | --- | --- | --- |
| **CTX-DSV2-ROOT** — implementation home | build / flag | spine + green + research done | execute R1→R6b or agent-cost experiment |
| **CTX-DSV2-AUTHORITY** — minted spine | minted / flag | 3 kinds RATIFIED; recursion applied | L2 attestation seal (blocked) |
| **CTX-DSV2-MAKE-IT-GREEN** — impl/ green | validated / flag | G1/G2/G3 done (L0-L2 green) | G4 CI-wiring (deferred) |
| **CTX-DSV2-REFORMULATE-BATCH1** — 6 spec docs | plan / flag | design+plan authored, **unexecuted** | task-session R1 (AXIOMS) first |
| ↳ **CTX-DSV2-META-TYPE-FORMALIZATION** (child) | build / flag | **MT0–MT3 nodes + MT-INST DONE** (14 node types + machine-instance generate/validate, source B; tests green); **MT3b edges deferred to R3** | R3 (edges) · MT4 (wire validator) · MT5 (UI, deferred) |
| **CTX-DSV2-SPEC-ONTOLOGY** — spec-as-ontology | research-complete / flag | toy T1-T4 → **SURVIVED-narrow** | Lane Z-vs-A deferred; extend composability; 2nd corpus |

## Pending by node
- **CTX-DSV2-ROOT** — next: execute reformulation or agent-cost experiment. Recompositions partial (green, toy).
- **CTX-DSV2-AUTHORITY** — blocker `BLK-DSV2-L2-ATTESTATION` (needs attestation capability, human).
- **CTX-DSV2-MAKE-IT-GREEN** — G4 (wire `validate` + fail-closed hook into CI/pre-commit) deferred.
- **CTX-DSV2-REFORMULATE-BATCH1** — R1→R6b not executed; blocker `BLK-DSV2-DRIFT-ENGINE` (drift impl); R3 armed with R3-P1/P2/P3.
  - ↳ **CTX-DSV2-META-TYPE-FORMALIZATION** (child) — **MT0 done** (Entity exemplar + schema-loading `validate-content`, green); MT1→MT5 remain; owns the formal per-type criteria + `validate-content`; R2 (TAXONOMY formal) + R7 (DS-D1/D2) consume it. **DES-D1 RESOLVED** (schema+md pair); DES-D2 engine boundary still open.
- **CTX-DSV2-SPEC-ONTOLOGY** — open decision `DEC-DSV2-LANE-ZA`; gaps `GAP-DSV2-EDGE-CATALOG` (→R3), `GAP-DSV2-COMPOSABILITY-ENFORCE`, `GAP-DSV2-EXERCISE`.

## Decisions
- **DEC-DSV2-CRAFT-SCOPE** — *closed* → own-scoped-craft. v2 outgrew one cav2 row; a scoped `.craft/` is not a new cav2 folder; cav2 points here.
- **DEC-DSV2-LANE-ZA** — *open* (default: defer). Lane Z (fuse) vs Lane A (generate+separate). The toy proved the *mapping* is viable — which both lanes need — so the decider is the unmeasured "cheaper agents" claim → agent-cost experiment.
- **DEC-DSV2-EDGE-ADMISSIBILITY** — *closed* → build-from-owned. Edge-type admissibility governed by **CAV2-D22 / D29 / D16** (an edge earns its type iff it composes into *different code*). Rulings: keep `enforces`≠`applies`; collapse `enforces`/`enforces-cross`; reject `queries` for Calc→Policy; widen `applies : Policy→{Op,Calc}`. Governance orthogonality only (not Lean/Hilbert). → **R3**.

## Artifacts
[IMPORT-MANIFEST](IMPORT-MANIFEST.md) · [impl/](impl/) · [authority/](authority/) · [make-it-green](development/make-it-green/) · [reformulate-batch1](development/reformulate-batch1/) · [import-triage](research/2026-06-29-v1-import-triage/findings.md) · [recursion-research](research/2026-06-29-recursive-governance-model/findings.md) · [spec-as-ontology research](research/2026-07-01-spec-as-ontology/findings.md) · [spec-ontology toy](research/spec-ontology-unification/) · [composability synthesis](research/2026-07-01-composability-edges-taxonomy-synthesis.md) · [definitions/](definitions/)

## Definitions (canonical, local — [definitions/](definitions/))
Cards `domainspec-v2-D1..D5` (all active, 3-voice) + INDEX + DRIFT-AUDIT + LOCALIZATION-ROUTE + `reviews/`
(backfilled 2026-07-01 to the mint baseline; v2's first mint predated the mint's definitions-lifecycle additions).
- **D1** drift · **D2** validation governance (RATIFIED kind) · **D3** edge-law admissibility (build-from-owned CAV2-D22/D29/D16) · **D4** executable typed graph · **D5** two-plane boundary.
- **Owed** (drift-audit `flag`, `GAP-DSV2-GOVERNANCE-CARDS`): `layering-governance` + `drift-governance` — the two sibling domain-originated governances still lacking cards.

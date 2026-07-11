# DomainSpec v2 — Craft (human view)

> Human view of [`.craft/ledger.yml`](.craft/ledger.yml) (source of truth). Scoped space promoted from
> cav2 `CTX-CAV2-DOMAINSPEC-V2` on 2026-07-01 (decision `DEC-DSV2-CRAFT-SCOPE`). cav2 stays umbrella and
> points here. Last updated: 2026-07-10.

## Quick links
- **Next move (root):** R0, R1, and CT-1 are landed and green; migrate UI-11 before verify-closing R2, reconcile-close R7, then continue R4/R5/R6a/R6b **or** stand up the agent-cost experiment for Lane Z vs A.
- **Open decisions:** `DEC-DSV2-LANE-ZA` (Lane Z vs A — deferred). *(`DEC-DSV2-APE-L0-DOMAIN` closed 2026-07-02 → reuse financial-settlement.)*
- **Active blockers:** `BLK-DSV2-DRIFT-ENGINE` (drift not implemented), `BLK-DSV2-L2-ATTESTATION` (attestation capability, human).
- **Active gaps:** `GAP-SH-UI11-MIGRATE` (R2 UI types must move before TAXONOMY deletion), `GAP-SH-PROSE-HOMES` (now DRIFT/R5 owner-home only), `GAP-DSV2-EXERCISE` (2nd corpus), `GAP-DSV2-APE-CARD-TRIAGE` (v1 pattern-library not triaged). *(`GAP-DSV2-COMPOSABILITY-ENFORCE` resolved by R0; AXIOMS half of `GAP-SH-PROSE-HOMES` resolved by R1.)*

## Contexts
| Context | Stage / gate | State | Next move |
| --- | --- | --- | --- |
| **CTX-DSV2-ROOT** — implementation home | build / flag | spine + green + research done; R0/R1/R3A/CT-1 landed | UI-11 migration → R2/R7, then R4/R5/R6a/R6b, or agent-cost experiment |
| **CTX-DSV2-AUTHORITY** — minted spine | minted / flag | 3 kinds RATIFIED; recursion applied | L2 attestation seal (blocked) |
| **CTX-DSV2-MAKE-IT-GREEN** — impl/ green | validated / flag | G1/G2/G3 done (L0-L2 green) | G4 CI-wiring (deferred) |
| **CTX-DSV2-REFORMULATE-BATCH1** — 6 spec docs | plan / flag | R0/R1/R3A executed; R2/R7/R4/R5/R6a/R6b remain | R2 verify-close, R7 reconcile-close, then R4/R5/R6a/R6b |
| ↳ **CTX-DSV2-META-TYPE-FORMALIZATION** (child) | build / flag | **MT0–MT4 + MT-INST DONE** (14 backend schemas, 31 signatures, edge-aware validator, aggregate wiring); UI deferred | MT5 (UI, deferred) · tools/lib extraction residue |
| **CTX-DSV2-SPEC-ONTOLOGY** — spec-as-ontology | research-complete / flag | toy T1-T4 → **SURVIVED-narrow**; R3A consumed catalog gaps | Lane Z-vs-A deferred; extend composability; 2nd corpus |
| **CTX-DSV2-APE** — architecture-pattern enforcement | build / flag | **L0 POC DONE**; R3A unblocks edge plane | L1 cleanup · TASK-CARDS triage · dynamic DS-D8 edge-law enforcement |
| **CTX-DSV2-CODE-TAG-CONFORMANCE** — code-tag conformance | build / flag | CT-1 done; code-tag taxonomy reads root schemas | CT-3, then CT-2/CT-4 |

## Pending by node
- **CTX-DSV2-ROOT** — next: UI-11 migration before R2 verify-close, R7 reconcile-close, remaining reformulation docs, or agent-cost experiment. Recompositions partial (green, toy, R0/R1/R3A/CT-1).
- **CTX-DSV2-AUTHORITY** — blocker `BLK-DSV2-L2-ATTESTATION` (needs attestation capability, human).
- **CTX-DSV2-MAKE-IT-GREEN** — G4 (wire `validate` + fail-closed hook into CI/pre-commit) deferred.
- **CTX-DSV2-REFORMULATE-BATCH1** — R0, R1, R3A, and CT-1 complete. R2's code-tag `TAXONOMY.md` landmine is closed, but R2 remains gated on `GAP-SH-UI11-MIGRATE`; R7 needs reconcile-close; R4/R5/R6a/R6b remain. `GAP-SH-PROSE-HOMES` is now DRIFT/R5 only, and blocker `BLK-DSV2-DRIFT-ENGINE` still applies to drift realization.
  - ↳ **CTX-DSV2-META-TYPE-FORMALIZATION** (child) — **MT0–MT4 + MT-INST done**: 14 backend type schemas, 31 root relationship signatures, edge-aware `validate-content`, aggregate validation wiring, and machine-instance generate/validate. Remaining: MT5 UI deferred; tools/lib extraction residue.
- **CTX-DSV2-SPEC-ONTOLOGY** — open decision `DEC-DSV2-LANE-ZA`; active gaps `GAP-DSV2-COMPOSABILITY-ENFORCE`, `GAP-DSV2-EXERCISE`. `GAP-DSV2-EDGE-CATALOG` resolved by R3A.
- **CTX-DSV2-APE** — **L0 POC DONE** (financial-settlement pack; `validate:content` 7 concepts + 5 edges ✓, `instances` 14 ✓, `engine:lint` CLEAN, red exit 1; `GAP-DSV2-APE-VACUOUS` resolved). Remaining gap `GAP-DSV2-APE-CARD-TRIAGE` (v1 pattern-library owned, not triaged); edge plane is unblocked by R3A but needs dynamic DS-D8 enforcement. Package: [architecture-pattern-enforcement](development/architecture-pattern-enforcement/). Next: `SWU-APE-004/005` cleanup · TASK-CARDS triage · dynamic edge-law enforcement.
- **CTX-DSV2-CODE-TAG-CONFORMANCE** — **CT-1 DONE**: `validate-code-tags` reads taxonomy from `spec/meta-types`, invalid type fixture rejects, and scratch validation passes with `TAXONOMY.md` absent. Remaining: CT-3 waiver/path cleanup, CT-2 schema contract, CT-4 unified gate.

## Decisions
- **DEC-DSV2-CRAFT-SCOPE** — *closed* → own-scoped-craft. v2 outgrew one cav2 row; a scoped `.craft/` is not a new cav2 folder; cav2 points here.
- **DEC-DSV2-LANE-ZA** — *open* (default: defer). Lane Z (fuse) vs Lane A (generate+separate). The toy proved the *mapping* is viable — which both lanes need — so the decider is the unmeasured "cheaper agents" claim → agent-cost experiment.
- **DEC-DSV2-EDGE-ADMISSIBILITY** — *closed* → build-from-owned. Edge-type admissibility governed by **CAV2-D22 / D29 / D16** (an edge earns its type iff it composes into *different code*). Rulings: keep `enforces`≠`applies`; collapse `enforces`/`enforces-cross`; reject `queries` for Calc→Policy; widen `applies : Policy→{Op,Calc}`. Governance orthogonality only (not Lean/Hilbert). → **R3**.
- **DEC-DSV2-APE-L0-DOMAIN** — *closed 2026-07-02 (decision-gate)* → **reuse-the-spec-ontology-toy-domain (financial-settlement)**. Build-from-owned: the domain already exists as engine fixtures + the toy's 23-node graph extraction; node-rich, connects L0 to the SURVIVED-narrow evidence. Default (author-new) demoted once grounding showed an owned real domain; the `sample` stub is empty so promote-sample folded out.

## Artifacts
[IMPORT-MANIFEST](IMPORT-MANIFEST.md) · [impl/](impl/) · [authority/](authority/) · [make-it-green](development/make-it-green/) · [reformulate-batch1](development/reformulate-batch1/) · [import-triage](research/2026-06-29-v1-import-triage/findings.md) · [recursion-research](research/2026-06-29-recursive-governance-model/findings.md) · [spec-as-ontology research](research/2026-07-01-spec-as-ontology/findings.md) · [spec-ontology toy](research/spec-ontology-unification/) · [composability synthesis](research/2026-07-01-composability-edges-taxonomy-synthesis.md) · [definitions/](definitions/) · [architecture-pattern-enforcement](development/architecture-pattern-enforcement/) · [code-tag-conformance](development/code-tag-conformance/) · [APE research](research/2026-07-02-architecture-patterns-enforcement/findings.md)

## Definitions (canonical, local — [definitions/](definitions/))
Cards `domainspec-v2-D1..D17` + `DS-D*` domain vocabulary live under root [definitions/](definitions/), with INDEX + DRIFT-AUDIT + LOCALIZATION-ROUTE + `reviews/`.
- Active R3 definitions: `DS-D2` relationship verb set + `DS-D8` relationship signature authority.
- Governance cards now resolved: `domainspec-v2-D16` layering governance + `domainspec-v2-D17` drift governance. Definition drift audit verdict: **pass**.

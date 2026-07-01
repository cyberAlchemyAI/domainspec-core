---
node_type: implementation-layering
is_session: false
status: candidate
created: 2026-07-01
authored_by: invoke (mode: plan)
work_pack: ./WORK-PACK.md
define: ../DEFINE.md
design: ../DESIGN.md
---

# Spec–Ontology Toy — Implementation Layering

**Layer-boundary heuristic:** each layer produces one artifact the next strictly needs; the criterion
is only *measured* at L2 (after it is frozen), so no layer can "pass by preference". Promotion requires
the previous layer's artifact to exist and be reviewable.

| Layer | Slice | Minimum working unit | Promotion evidence |
| --- | --- | --- | --- |
| **L0 — extract** | T1 | The spec-graph for financial-settlement: a typed node list + typed edge list. | Node/edge inventory exists; every item carries a TAXONOMY/RELATIONSHIPS type (or is flagged unclassifiable = an M1 signal). |
| **L1 — map** | T2 | The node→pattern table + edge→composition table for the corpus's types. | Both tables filled for every node/edge in T1; unmapped items explicitly listed (not silently dropped). |
| **L2 — run + attack** | T3 | The paper pattern-skeleton + M1–M4 computed + the attack break-list. | Criterion FROZEN first; M1–M4 reported with the exception lists; determinism re-run matches; attack lenses all exercised. |
| **L3 — compare + verdict** | T4 | Lane A sketch + SURVIVED/FALSIFIED/INVALID verdict + promotion recommendation. | Verdict cites M1–M4 against the frozen bars; Lane A weighed; recommendation respects the promotion boundary. |

**Dependency order:** T1 → T2 → T3 → T4 (strict; each consumes the prior artifact).

**Recomposition:** L0–L3 produce the evidence the SEED tower needs to close Lane Z-vs-A — the decision
the 2026-07-01 research explicitly deferred here.

**Boundary carried down every layer:** local research only (no spec/code mutation); engine black-box;
authority flows spec → toy, never back.

---
role: s5 validation evidence (ledger.drift-check)
dispatch: gq-impl-arch-discovery-2026-06-10
status: flag → resolved (corrections applied 2026-06-10)
---

# Drift-check ledger — victor-pattern views vs spec

Validation stage (s5) of dispatch `gq-impl-arch-discovery-2026-06-10`. Every load-bearing
claim in the four views was checked for a spec selector and for conflicts. Initial verdict
**flag**; all flags below have been corrected in-place.

## Confirmed (load-bearing claims that trace cleanly to spec)
- **Core invariant — OwnerDecision is the sole setter of `approved_allowed_uses`.** SPEC.md:89, domain.md:216, domain.md:210, SPEC.md:200; reinforced mappings.md:106,127. The pack's central thesis is correct and well-sourced.
- **Adapters cannot set approved uses / journal is not authority.** SPEC.md:198–200, SPEC.md:169–170; domain.md AdapterProducer.
- **L0 = fixture-only, audit-only, `mutation_allowed=false`.** mappings.md:114,124; SPEC.md:596–630.
- **L0 component set = C2, C3, C8 (+ DAG half of C4).** runtime-design §5, ARCHITECTURE View 3.
- **One-way authority flow + five recomposition invariants.** SPEC.md:197–201, operation roster SPEC.md:80–90; runtime-design §1–3.
- **Architecture Decision Log D-001…D-007.** architecture.md:339–345, verbatim match.
- **Event-count "13" side is real.** events.md has 13 top-level event sections.

## Flags — found and corrected
| ID | Drift | Correct value (direct count 2026-06-10) | Fix applied |
|----|-------|------------------------------------------|-------------|
| FLAG-1 | `GrantKpiKind` published as **49** (discovery Q6, engineer §1, ontology §2 + RES-1). Spec prose said "47". | **44** entries (domain.md:402–449) | **RESOLVED 2026-06-13** — all prose corrected to 44 (enum authoritative); the "47" and "49" figures struck as miscounts. |
| FLAG-2 | `GrantRunNodeKind` published as **15** with SPEC "~14" (ontology §2 + RES-3). | **16** (domain.md:329–348; SPEC.md:102–119 independently lists 16) | Count corrected to 16; RES-3 marked **resolved — not residue** (counts agree). |
| FLAG-2b | `ApplicationStage` stated as **20** (ontology §3.2 + enum table). | **19** (domain.md:378–400) | Corrected to 19. |
| FLAG-3 | engineer §2.1 stated flatly "**there is no D-E**." | D-E exists in ARCHITECTURE.md Decision Log (numpy/scipy freeze); runtime-design §6 folds the same into D-D as a sub-decision and skips the D-E heading. | Reworded: both docs correct; lettering gap is doc-sync residue, D-E is the analytics-library freeze. |
| FLAG-4 | Minor: a few SPEC.md line cites off by ~1 (e.g. SPEC.md:200). | Cites resolve to the correct rules block (SPEC.md:197–201). | Left as-is; content is correct. |

## Residue confirmed (genuinely unreconciled in the spec — not authoring errors)
- **KPI count — RESOLVED 2026-06-13.** Prose reconciled to **44** (enum authoritative); the "47" prose figure is struck.
- **Event count — RESOLVED 2026-06-13.** Two real axes named explicitly: **9 ingestion event families** (`GrantWorkEventKind` enum) and **13 operation-output events** (events.md sections). The phantom "12" is struck. OPEN-QUESTIONS-LEDGER:67, runtime-design:271, seam-map:67.
- **B-001 / TEST-SPEC T1–T35 stability** — unconfirmed; TEST-SPEC.md outside verified read set. Posture correct.
- **OQ-4 vocabulary lock (three-surface split)** — PROPOSED, blocks L1 not L0. Correctly represented.

## Final verdict
**pass (post-correction).** The load-bearing architecture — the heart (OwnerDecision = sole approver), L0 scope (C2/C3/C8, audit-only, `mutation_allowed=false`), and the one-way authority flow — traces cleanly to spec. The flags were count-hygiene + one over-absolute statement; all corrected. The KPI count (now 44) and event count (9 ingestion families + 13 operation-output events) are reconciled 2026-06-13. Remaining open items (OQ-4 lock, T1–T35 stability) are genuine spec-level residue, correctly carried as honest gaps.

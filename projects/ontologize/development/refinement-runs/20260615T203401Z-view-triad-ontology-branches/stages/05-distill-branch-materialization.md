# Distill - Branch Materialization Model

## Selected Coherent Unit

Branch materialization should be a **citation-backed coverage profile inside the existing triad**, not a new sibling view.

The unit has four parts:

1. Branch Materialization Register.
2. Branch-to-view materialization matrix.
3. B3 run-context record.
4. B4 bridge ledger plus authority map.

## Rejected Alternatives

| Alternative | Rejection Reason |
| --- | --- |
| Accept current triad unchanged | Blocks on B3/B4 under-modeling and missing branch completeness gates. |
| Add standalone branch-view artifact | Duplicates `ONTOLOGY-BRANCHES.md` and risks a fourth authority surface. |
| Put branch materialization only in ontology-view | Hides stakeholder shape and branch-boundary decisions; B3/B4 would still be under-gated. |

## Materialization Rule

Each view materializes branches only through its existing authority:

| View | Branch Materialization Authority |
| --- | --- |
| `system-view` | Names branch-shaped stakes, tensions, and stance handles. It does not decide branch status or define terms. |
| `engineer-view` | Owns branch-boundary verdict rows, enforcement authorities, schemas/contracts, runtime mechanics, and authority strikes. |
| `ontology-view` | Owns branch node typing, bridge edge legality, forbidden branch relationships, and guard status. |

## Required Branch Gates

| Gate | Rule |
| --- | --- |
| B1 meaning gate | Meaning claims cite source/authority; unresolved policy/rule/value/outcome stances become engineer-view OPEN/CRITICAL rows. |
| B2 system gate | System claims trace to event/source/mechanics evidence; RESOLVED system mechanics require reachable authority. |
| B3 run-context gate | Run boundary, denominator, lifecycle state, scope/posture, and stage-vs-outcome separation are explicit before publication. |
| B4 bridge gate | Cross-branch claims use the governed edge catalog; coined edges need route/blocker; open `contradicts` blocks promotion. |
| Recomposition gate | BI or optimization claim traces claim -> optimization chain -> owning view row -> source evidence without restating verdicts or definitions. |

## Residue

- Later execution should add one sample branch walk trace from B2 event -> B3 metric -> B4 candidate -> B1 update.
- Product-facing docs remain blocked until the pilot triad and validation report pass.

## Stage Verdict

Status: pass.


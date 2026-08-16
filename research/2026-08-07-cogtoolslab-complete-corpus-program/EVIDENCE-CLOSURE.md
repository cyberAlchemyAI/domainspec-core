# Exact-Binding Evidence Closure

Status: `blocked`
Run: `cogtoolslab-complete-corpus-run-1`
Gate: `g-explorer-coverage`
Writer admission: `denied`

## Closure matrix

| Required lane or handoff | Source identity | Retrieval status and digest | Paper-read capsule | Exact selector | State |
|---|---:|---:|---:|---:|---|
| 2024--2026, 36 rows | yes | yes | no | no | `blocked` |
| 2021--2023, 29 rows | yes | yes | yes | yes, bounded to abstract or named pages/sections | `ready` |
| 2009--2020, 25 rows | no return | no return | no return | no return | `blocked` |
| Teaching and research surfaces | no return | no return | no return | no return | `blocked` |
| Ninety-row synthesis and Tier-B deduplication | incomplete inputs | incomplete inputs | not run | not run | `blocked` |
| Reviewers | upstream gate closed | upstream gate closed | not run | not run | `blocked` |
| Writer | exact-binding closure absent | exact-binding closure absent | not admitted | not admitted | `blocked` |
| Auditor | no `findings.md` | no `findings.md` | not run | not run | `blocked` |

## Typed blockers

1. `spawn-0003` was attempted once and rejected by the native host with
   `agent thread limit reached`. Orchestrate replay protection forbids an
   implicit retry of that action, and `spawn-0004` remained unattempted.
2. `spawn-0001` enumerated and hashed all 36 assigned PDFs, but returned
   `block`: it could not semantically extract and read their text, so all 36
   paper capsules and exact page or section selectors remain absent.
3. A successful middle-period lane cannot open synthesis by itself. Exact
   coverage requires all four explorer receipts.

## Surviving evidence

- Run 1 establishes 65 distinct live publication rows with HTTP/media-type,
  byte-count, and SHA-256 evidence: 36 for 2024--2026 and 29 for 2021--2023.
- The 29 middle-period rows include paper-read capsules and bounded selectors.
- The 36 modern rows establish only enumeration and byte identity. They do not
  establish paper meaning, retraction/version status, cognition, comprehension,
  or teaching effectiveness.
- No PDF bytes were persisted or republished.

## Verdict

`blocked`, not `ready` and not `needs_feedback`. The partial-wave native spawn
failure prevents the confirmed graph from reaching its declared feedback edge.
Preserve `research.md` and this matrix; do not create `findings.md`.

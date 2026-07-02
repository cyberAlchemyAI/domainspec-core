<!-- MINT-BASELINE BACKFILL (2026-07-01) for domainspec-v2 — cast from templates/definition-drift-audit.md
     (Tier-1 addition #8, SWU-5), which post-dates v2's 2026-06-29 first mint. INTERNAL/private.
     INHERITS the drift-audit PROCEDURE + report FORMAT; LOCALIZES the audited terms. -->

# DomainSpec v2 Definition Drift Audit

Status: active (review-mode; a deterministic scan is a domain follow-up)
Owner: definitions-governance (domain-local)
Reconciles: [DEFINITIONS.md](./DEFINITIONS.md) against [DEFINITIONS-INDEX.md](./DEFINITIONS-INDEX.md)
Authority: this audit is the enforcement target named by the constitution's Load-Bearing Term Tracking
rule (`C(meta-4)`).

## What this audit checks
A **load-bearing term** = a symbol/named quantity in a formal expression, a fixture FAIL-region, a
candidate invariant, a decidable rule, a governance-kind name carrying authority, or the normative content
of a claim-ledger entry. For every load-bearing term used in the repo's definitions surface:

1. **tracked?** — does it have a row in `DEFINITIONS-INDEX.md` resolving to a card in `DEFINITIONS.md`?
2. **grounded?** — if the card is `candidate`, does it carry an `Open / to-ground:` field?
3. **non-collapsed?** — `candidate` status is not treated as validation.

A term failing (1) is a **drift defect** — create it as a `candidate` card + index row (stage in
`reviews/`), do not use it as authority until grounded.

## Audit ledger
| Load-bearing term | First cited in | Tracked (index row)? | Card status | Verdict | Route |
| --- | --- | --- | --- | --- | --- |
| drift / convergence | DEFINITIONS.md#domainspec-v2-d1 | yes → `domainspec-v2-D1` | active | `pass` | — |
| validation governance | DEFINITIONS.md#domainspec-v2-d2 | yes → `domainspec-v2-D2` | active | `pass` | — |
| edge-law admissibility | DEFINITIONS.md#domainspec-v2-d3 | yes → `domainspec-v2-D3` | active | `pass` | — |
| executable typed graph | DEFINITIONS.md#domainspec-v2-d4 | yes → `domainspec-v2-D4` | active | `pass` | — |
| two-plane boundary | DEFINITIONS.md#domainspec-v2-d5 | yes → `domainspec-v2-D5` | active | `pass` | — |
| layering governance | DEFINITIONS.md#domainspec-v2-d2 ("one of v2's three domain-originated governances"); reformulate-batch1 (C6 → layering) | **no** | — | **drift (owed)** | create candidate card + index row → definitions lifecycle; stage in `reviews/` |
| drift governance | DEFINITIONS.md#domainspec-v2-d1 ("the subject of drift governance") | **no** | — | **drift (owed)** | create candidate card + index row → definitions lifecycle; stage in `reviews/` |

## Gate
- `pass`: every load-bearing term resolves to a tracked, grounded entry.
- `flag`: an owed term is named as a gap but not yet exercised as authority.
- `block`: a load-bearing term is used as authority with no tracked card — stop until it is created.

## Current verdict: flag
Five carded terms pass. Two sibling governance-kind terms — `layering governance` and `drift governance`
(the other two of v2's three domain-originated governances; `validation governance` = `domainspec-v2-D2` is
the sibling exemplar) — are named as authority-in-waiting with no card yet. This is the same gap the
DEFINITIONS.md skeleton note records. They are **owed**, not yet exercised as authority, so this is a flag,
not a block. Route: author the two governance kind cards via the definitions lifecycle.

<!-- Emitted live: the audit runs the moment the domain has terms. Re-run when cards are added/changed. -->

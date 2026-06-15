# s4 — Research Decision

- Owner: `refine` · Mode: `research-if-gap-appears`
- Receipt kind: native-stage · Status: `pass`
- Inputs: `stages/s3-interrogation-define/REVIEW.md`

## Decision: NO external research this run (local-first holds)

The refine-review surfaced gaps G1–G4 / F1–F3. Each is resolvable from the
source doc and supplied context:

| Gap | Resolvable locally? | Why |
|-----|--------------------|-----|
| G1 entity-home unresolved | yes (as a decision menu) | The four options are named in the source; the *choice* is an operator decision, not a research question. Surfaced as a route menu + approval gate. |
| G2 authority/ownership graph | yes | All ownership rules are in the source's Entity And Partner Routing section; Design draws them. |
| G3 lane dependency / minimum spine | yes | Lane 1 + Bridge ask + entity-home are self-contained in the source (F3). |
| G4 per-partner verification status | yes (as a control) | The source already mandates "verification status on every partner"; Design encodes the field, it does not need to *look up* statuses. |

No named gap requires *external* evidence (funder rules, partner confirmations,
KU/INVAM authorization). Such facts are exactly the protected context (O1, O2)
that external research **cannot** resolve and must not assert.

## Trigger condition for re-asking

If Design or Distill-Repair produces a claim that *depends on an unconfirmed
external fact* (e.g., a specific funder eligibility rule or a partner's
commitment), Refine will stop and request operator confirmation before any
bounded research. Not triggered so far.

- Research confirmation status: not requested (no qualifying gap).
- Gate g3-research-confirmation: satisfied (no external research attempted).

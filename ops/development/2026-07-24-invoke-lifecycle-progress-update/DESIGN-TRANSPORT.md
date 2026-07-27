# Design Transport

Status: pass

## Approved planning inputs

- `DEFINE.md`
- `GLOSSARY.md`
- `DESIGN.md`
- `GLOSSARY-CONSISTENCY.md`
- `GAPS.md`
- `TEMPLATE-SELECTION.md`

## Delivery boundary

Plan public-source changes only through their lifecycle owners:

- Spellcraft: Invoke Plan, Refresh, public schemas/validators/fixtures, and
  generated Invoke surfaces;
- Sigil Development: Task Session consumption, epoch binding, and admission
  fixtures;
- named transition-admission owner: append-only transition admission;
- Workflow Reflect: observational progress/churn signals after execution.

## Fixed architecture

- one immutable epoch per selected SWU;
- declared execution-control graph and exact control digest;
- mode-specific producer/validator/consumer contract;
- independent handoff readiness;
- successor epoch for every control change;
- independent drift-impact classification;
- append-only transition relation;
- typed Refresh postconditions;
- legacy-unadmitted migration;
- generic live proof before promotion.

## Plan gate

The plan may be complete while mutation execution remains gated. The work-pack
must select `SWU-ILP-001`, a non-mutating lifecycle decision, and must not route
Task Session until that decision and all predecessor contracts produce a ready
epoch.


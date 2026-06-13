# Dispatch-Spec Validation — Refine-Solvability of Golden Quill Gaps

- Date: 2026-06-12
- Pipeline: `dispatch-spec validate → refine → invoke` over all 12 Craft spaces
- Question: which ledger gaps/decisions can be **solved by refining** (spec authorable locally now) vs. which need **operator input** or a **decision** first?
- Result: each refine-solvable item was refined and invoked into a canonical `each space's BUILD-SPEC.md (co-located in the space, tracked in its ledger)` (outside any `development/` folder). Operator-input and decision-gated items are routed to the repo-root TO-* docs.

## Legend
- **refine-solvable** — the spec/design/plan was authorable from local evidence and is now in a BUILD-SPEC, ready for the owner to build.
- **decision-gated** — a blocking/open decision must be ratified before the dependent build can execute (the decision itself is framed in a BUILD-SPEC).
- **operator-input** — only Josh can supply the value/content/staffing; no spec substitutes for it.

## Master verdict table

| ID | Node | Owner | Verdict | What happens next |
|---|---|---|---|---|
| GAP-HGI-IMAGE-VERIFY | hardware-golden-image | Vlad | refine-solvable | Build per-unit write+verify on the Ed25519 chain |
| GAP-HGI-BACKUP-RECOVERY | hardware-golden-image | Vlad | refine-solvable | Build backup/export/recovery; prove wipe→recover digest match |
| GAP-HGI-BURN-IN | hardware-golden-image | Koichi | refine-solvable (thresholds operator-input) | Author 4-axis procedure; thresholds pending EXT-HGI-2 |
| GAP-HGI-REFERENCE-SPEC | hardware-golden-image | Koichi | refine-solvable (SKU values operator-input) | Author spec template; SKU values pending EXT-HGI-1 |
| GAP-QSP-TEST-PLAN | quality-security-proof | Victor | refine-solvable | Build guardrail test matrix (16 F-CLASS + 12 F-WPFA + Five Laws) |
| GAP-QSP-CLAIMS-REGISTER | quality-security-proof | Victor | refine-solvable | Seed claims-register.yaml (claim→evidence-category) |
| GAP-QSP-INSTRUMENTATION | quality-security-proof | Victor | refine-solvable | Author instrument-definitions.yaml |
| GAP-QSP-SECURITY-REVIEWER | quality-security-proof | Josh | operator-input | Assign independent security reviewer |
| GAP-TRB-WORK-PACKS | tilth-runtime-build | Vlad+Koichi | refine-solvable | 13 sequenced work packs authored; start critical path |
| GAP-TRB-GOLDEN-IMAGE-HANDOFF | tilth-runtime-build | Vlad+Koichi | refine-solvable | Lock manifest/signature schema with hardware node |
| GAP-TRB-POSTURE-CANON | tilth-runtime-build | Josh | decision-gated | Blocked on DEC-BC-POSTURE-VOCAB |
| GAP-TRB-UI-PHASE | tilth-runtime-build | Josh | decision-gated | Blocked on DEC-BC-UI-BOUNDARY (v0.1 headless) |
| GAP-CLL-RULE-PACKS | capital-logic-library | Vlad | refine-solvable (content operator-input) | Build rule-pack schema (NO CIC→CLC binding) |
| Card schema+governance | capital-logic-library | Vlad+Josh | refine-solvable | Build card schema/testability rules |
| GAP-CLL-DOMAIN-EXPERTS | capital-logic-library | Josh | operator-input | Contract 4 segment experts |
| GAP-CLL-LAUNCH-CARDS | capital-logic-library | Josh | operator-input | Author/validate 5 cards + capture status |
| GAP-COF-SUPPORT-TRIAGE | company-operations-finance | Josh (esc: Vlad/Koichi) | refine-solvable | Stand up issue-log + triage routing |
| GAP-COF-ENTITY-HYGIENE | company-operations-finance | Josh | refine-solvable | Run the operating checklist cadence |
| GAP-COF-NODE-CARE-OPS | company-operations-finance | Josh | refine-solvable | Adopt Node Care cadence |
| GAP-COF-VALIDATION-PACKET | company-operations-finance | Josh+Victor | refine-solvable | Assemble packet (consumes QSP claims+instrumentation) |
| GAP-NOD-SEQUENCE | node-on-desk-readiness | Josh/PM | refine-solvable | Adopt the recomposition gate ladder RG-1…RG-10 |
| GAP-NOD-HOURS-RATES | node-on-desk-readiness | Josh | operator-input | Fill hours/rates worksheet |
| GAP-NOD-CANON-VOCAB | node-on-desk-readiness | Josh | decision-gated | Blocked on DEC-BC-POSTURE-VOCAB |
| GAP-WGD-PLAYBOOK | white-glove-delivery-node-care | Josh/CS | refine-solvable | Build service-wrapper delta over white_glove_v0_1_beta.md |
| GAP-WGD-DAY60 | white-glove-delivery-node-care | Victor | refine-solvable (metrics dep QSP) | Build Day-60 template |
| GAP-WGD-CS-HANDOFF | white-glove-delivery-node-care | Josh→CS | refine-solvable (trigger gated) | Build CS/Field-Tech checklist |
| GAP-AAR-SEQUENCING | after-acceleration-roadmap | Josh | refine-solvable (thresholds operator-input) | Adopt stage-gate structure; set thresholds |
| DEC-AAR-STAGE-GATES | after-acceleration-roadmap | Josh | operator-input | Set threshold values |
| GAP-AAR-REPEATABILITY | after-acceleration-roadmap | Josh | operator-input | Run non-founder install pilot |
| GAP-AAR-SERVICE-PILOTS | after-acceleration-roadmap | Josh | operator-input | Run scoped service pilots |
| DEC-BC-POSTURE-VOCAB | boundary-and-canon | Josh | decision-gated (translation authored) | **BLOCKING** — ratify 4→3 posture table |
| DEC-BC-UI-BOUNDARY / GAP-BC-UI-SCOPE | boundary-and-canon | Josh | decision-gated (options authored) | Pick console phase (not interactive v0.1) |
| GAP-SCL-SALES-MATERIALS | sales-contracting-legal | Josh | refine-solvable (claims dep QSP) | Fill sales templates |
| GAP-SCL-LEGAL-FIRST-LOI | sales-contracting-legal | Josh | operator-input | Retain fractional counsel |
| GAP-SCL-DEPOSIT-INVOICING | sales-contracting-legal | Josh | operator-input | Bookkeeper at first revenue |
| GAP-SBT-HOURS-RATES | staffing-budget-and-triggers | Josh | refine-solvable (values operator-input) | Fill budget worksheet |
| DEC-SBT-TRIGGER-MODEL | staffing-budget-and-triggers | Josh | refine-solvable (selection operator-input) | Pick trigger model A/B/C |
| GAP-SBT-ONBOARD-NOW / -LATER | staffing-budget-and-triggers | Josh | operator-input | Staffing decisions |
| DEC-OQ4 | promotion-governance | Vlad→Josh | decision-gated | **BLOCKING** — ratify decision-surface shape (rec A) |
| DEC-D2-FLIP / D3-SHARED-GATE / D4-VERIFY | promotion-governance | Vlad→Josh | decision-gated | Ratify Vlad's proposals |
| GAP-DESIGNED-NOT-BUILT | promotion-governance | Vlad | refine-solvable | Build L0 learning-loop spine |
| GAP-PROMO-ENFORCE | promotion-governance | Vlad | refine-solvable | Build promotion-authority gate + tests |
| GAP-REDACTION-TABLES | promotion-governance | governance | refine-solvable | Author per-CIC table schema (NO CLC) |
| GAP-L0L1-FLIP | promotion-governance | governance | refine-solvable (blocked on DEC-D2) | Spec per-org flip gate |
| GAP-KPI-COUNT | promotion-governance | Vlad | refine-solvable | Reconcile 47→44 (enum authoritative) |
| GAP-EVENT-COUNT | promotion-governance | Vlad | refine-solvable | Name the two axes (9 ingestion / 13 op-output); strike phantom 12 |

## Canonical specs produced (all outside `development/`)
One `BUILD-SPEC.md` per Craft space, co-located in that space and tracked in its ledger (features at `docs/features/<node>/`, strategy at `docs/strategy/development/<node>/`, repo-root space at `.craft/artifacts/`). Each carries Define→Design→Plan, acceptance criteria, concrete first steps, owner per item, and explicit operator-input / decision-gated callouts.

## Per-owner handoffs
Repo-root: [TO-VLAD.md](TO-VLAD.md) · [TO-KINOSHITA.md](TO-KINOSHITA.md) · [TO-VICTOR.md](TO-VICTOR.md) · [TO-JOSH.md](TO-JOSH.md)

## Two blocking decisions sit above everything
1. **DEC-BC-POSTURE-VOCAB** (Josh ratify) → unblocks tilth posture enforcement + node-readiness canon.
2. **DEC-OQ4** (Vlad proposes, Josh ratifies) → unblocks promotion-governance L1.

**Boundary check:** no ledgers, canonical architecture (CLAUDE.md/AGENTS.md/locked enums), or `orgs/` data mutated. Specs are planning evidence; building begins when owners pick them up and the two blocking decisions are ratified.

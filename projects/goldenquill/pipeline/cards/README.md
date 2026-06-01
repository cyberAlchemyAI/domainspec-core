# `pipeline/cards/` — Card System

**Status:** Directory scaffold landed 2026-05-15 alongside architecture v7.0.11 DRAFT + blueprint §18 DRAFT + §4 v2.x card-hardening DRAFT. Full LOCK pending L-005 two-cycle Thesis round.

## What lives here

The Card System is the runtime-machine-readable layer for Tilth's Customer Identity Cards (CIC) and Capital Logic Cards (CLC). **Customer Identity Cards** is the canonical repo term; **Customer Information Cards** is legacy / working-language only. Each card is a signed, versioned YAML knowledge artifact that translates one visual Card into executable runtime behavior for Scout, Scribe, Judge, Logician, Archivist, Report Generator, and the model router.

**Cards** = visual / conceptual layer (human-readable; PNGs at `assets/cards/customer_identification/` + `assets/cards/capital_logic/`).
**Cards** = runtime layer (machine-readable; this directory).

## Directory layout

```
pipeline/cards/
  README.md                                  # this file
  _schema/
    card_cic.schema.json           # JSON schema for CIC cards
    card_clc.schema.json           # JSON schema for CLC cards
  models.py                                  # Pydantic models mirroring each schema
  loader.py                                  # card loader (lifecycle/coupling preflight + v0.2 registration boundary)
  validators.py                              # auxiliary self-validation checks (Phase 4 card-research-time gates)
  registry.yaml                              # active signed/runtime-loadable card manifest
  CIC/                                       # six Customer Identity Card cards
    food_systems.yaml                        # fixture stub at v7.0.11 LOCK
    educator.yaml                            # NEEDED — Phase D research
    public_agency.yaml                       # NEEDED — Phase D research
    arts_culture.yaml                        # NEEDED — Phase D research
    cooperative.yaml                         # NEEDED — Phase D research
    ecosystem_intermediary.yaml              # NEEDED — Phase D research
  CLC/                                       # eight Capital Logic Card cards
    public_purpose_works.yaml                # NEEDED — Phase D research
    catalytic_change.yaml                    # NEEDED — Phase D research
    operating_capacity.yaml                  # fixture stub at v7.0.11 LOCK
    research_evidence.yaml                   # NEEDED — Phase D research
    market_access.yaml                       # NEEDED — Phase D research
    credit_underwriting.yaml                 # NEEDED — Phase D research
    sponsorship_corporate.yaml               # NEEDED — Phase D research
    shared_assets.yaml                       # NEEDED — Phase D research
  matrix/
    _FORWARD_COMPAT_ONLY.md                  # marker — matrix content forbidden before v1.x
    _schema/
      card_matrix.schema.json                # forward-compat schema only
  memory/
    profiles/
      cards_cic_profile.yaml                 # memory-layer CIC profile registration
      cards_clc_profile.yaml                 # memory-layer CLC profile registration
      cards_matrix_forward_compat_profile.yaml  # memory-layer matrix profile (inactive at v7.0.11)
```

## Canonical homes (authoritative specs)

| File | What it is |
|------|------------|
| `pipeline/architecture/v0.1/architecture_v7_0_11_card_amendment.md` | Architectural primitive declaration; schema layer; lifecycle; loader contract; memory namespace; F-CARDS-* family; routing posture interaction |
| `pipeline/blueprint/v0.1/section_18_card_system.md` | Operational specification; full schemas; phase sequence; milestones; testing requirements; research process; starter content requirements |
| `pipeline/blueprint/v0.1/section_04_logician_v2_x_card_hardening.md` | Logician hardening: F-CARDS-* family (seven primitives) + F-CIC-CLC-PATTERN-READ-DURING-ELIGIBILITY extending v7.0.8 |
| `pipeline/blueprint/v0.1/section_00_5_section_18_card_amendment.md` | §0.5 interface-index paired-commit row stubs |
| `docs/post_alpha/post_alpha_card_system_revised_2026-05-15.md` | Source ideation (revised) preserved for reference |
| `docs/post_alpha/post_alpha_card_system_source_doc.md` | Source ideation (morning version) preserved for audit trail |

## Coupling discipline (READ ME BEFORE EDITING ANY CARD)

The highest-risk failure mode is hidden CIC × CLC coupling. **Three structural prohibitions:**

1. **CIC cards MUST NOT include `common_clc_patterns_observed`** or any equivalent field that embeds CLC preference, frequency, win-rate, or recommended pairings. Killed at v7.0.11 LOCK per architecture §6.1.
2. **CLC cards MUST NOT include CIC allowlists, deny-lists, ranking preferences, or win-rate fields.** No CIC eligibility subsets at the CLC level.
3. **Matrix cards are FORWARD-COMPAT ONLY until v1.x.** No populated matrix content ships before the v1.x matrix-phase explicit amendment lands. `_FORWARD_COMPAT_ONLY.md` marker is binding.

F-CARDS-COUPLING-VIOLATION-EXTENSION and F-CIC-CLC-PATTERN-READ-DURING-ELIGIBILITY (extending v7.0.8) fail closed on violations.

## Lifecycle truth

`draft_status` is the canonical lifecycle state machine: `draft | review_passed | signed | deprecated`. `runtime_loadable` is the runtime truth flag.

Binding invariants:

- `draft_status: draft` cards are research drafts only; the loader rejects them.
- If `draft_status != signed`, then `runtime_loadable` MUST be `false`.
- If `runtime_loadable: true`, then `draft_status` MUST be `signed`, `signature_status` MUST be `signed`, `runtime_load_status` MUST be `loaded`, and `signed_at`, `signed_by`, and `content_hash` MUST be present.
- `pipeline/cards/registry.yaml` is the active-card manifest. Production-active entries must point only to signed/runtime-loadable cards.


## Version arc binding

- **v0.1 Beta scope (this LOCK):** schema + directory + Pydantic models + schema-validation CLI + active-card registry + lifecycle/coupling loader preflight + F-CARDS-* family roster. Full seat runtime registration remains v0.2 first-wave scope.
- **v0.2 first wave:** runtime context injection (CardRuntimeContext + Scout/Scribe/Judge/Logician/Report Generator wiring); F-CARDS-* predicate bodies graduate LIVE.
- **v0.2 ongoing (Paul-blocked):** research dispatch populating the 14 cards with citation-backed content.
- **v1.x:** UI surfacing; matrix content; outcome learning loop.

## Sovereignty discipline

Cards are workspace-shared knowledge (`shareable` classification by construction). They MUST NOT contain organization-specific private data — no org_slug, no client_name, no PROJECT_CONTEXT keys, no named private clients, no private cycle IDs. F-CARDS-PRIVATE-DATA-IN-CARD fail-closes loader on violation.

Per-org context lives at `orgs/<slug>/vault/` under Law 3 isolation. The cards layer never crosses that boundary.

## Signing

Cards sign via the operator-controlled Ed25519 publisher key, white-glove-pinned at appliance setup. Same trust mechanism as v7.0.7 §6.1 router-template signing and §17 v1 §17.6 Coefficient Registry signing. Production loader refuses unsigned cards (F-CARDS-UNSIGNED-PRODUCTION-LOAD); development loader permits unsigned for testing.

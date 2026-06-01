---
title: §5 Pipeline — v7.0.5 companion delta (Match DB lifecycle + Funder Intel curation cadence + Stage-5 consent tier)
filed: 2026-05-10
parent_section: pipeline/blueprint/v0.1/section_05_pipeline.md
parent_amendment: pipeline/architecture/v0.1/architecture_v7_0_5_amendment.md
status: COMPANION — v7.0.5 LOCKED 2026-05-10 (lock_history row 179)
---

# §5 Pipeline v7.0.5 companion delta

This companion catalogs the §5 Pipeline changes registered by architecture amendment v7.0.5. Pipeline-stage-specific bindings and operator-surface specifics live here; full mechanism specs in amendment §1-§7.

## §5.v7-0-5.1 Match Database lifecycle integration with grant cycle

| Stage | Match DB action | Operator surface |
|---|---|---|
| Scout DISCOVER | New candidate found by any channel A-G; if not in Match DB → create entry with `operator_action: pending` | none |
| Scout VERIFY | Live synopsis fetched; entry's `match_score` + `match_reasoning` populated; `verification_status` set | none |
| Scout REVIEW (operator gate) | Operator reviews candidate roster | confirmed_fit / rejected / declined_cycle action signed; entry's `operator_action` updated atomically with audit_chain signature |
| SP0 KFR Freshness Review (per v7.0.4) | KFR `required_for_funder` facts surfaced for current cycle's funder | operator confirms / refreshes facts |
| Drafting + Council Review (per v7 §5) | Match DB read for context; F-MATCH-DB-CROSS-ORG PRE-check on every read | none |
| Submission (per v7.0.6 Uploader) | Match DB entry's `outcome.outcome` updated to `submitted` after operator clicks final-submit on funder portal | operator clicks submit |
| Award notification | Operator updates entry's `outcome.outcome` to `awarded` / `declined` / `withdrawn`; `award_amount` populated if awarded; AWARD_INGEST mode (per v7.0.4) extracts `proposal_commitments.yaml` from won proposal | operator-explicit |
| Quarterly curation | Per-cycle Match DB outcomes feed `pipeline/institutional_memory/lessons.json` for pattern detection (e.g., "this funder rejected this client 3 cycles in a row — surface to operator before next proposal") | v0.1 operator-driven; v1.x Archivist seat |

## §5.v7-0-5.2 Funder Intelligence Database curation cadence

**v0.1 operator-driven.** Operator reviews `vault_shared/funder_intelligence/` quarterly (suggested cadence; configurable per-deployment).

**Curation prompt trigger semantics (resolves Cycle 1 E-02):**

- **Default trigger:** at Tilth wake-up (per AGENTS.md wake-up sequence), if `last_quarterly_curation_review` timestamp is older than 90 days, surface curation prompt to operator at session start.
- **Configurable:** operator can override cadence per-deployment via `tilth.config.yaml`:
  ```yaml
  funder_intel_curation:
    cadence_days: 90  # default; operator can set 60 / 120 / etc.
    trigger: wake_up | cron | explicit  # default: wake_up
    cron_schedule: "0 9 1 1,4,7,10 *"  # only used if trigger=cron; quarterly Mondays 9am
  ```
- **Lifecycle:** prompt surfaces stale docs (per F-FUNDER-CORPUS-STALE thresholds), promotion candidates (newly cited docs awaiting confirmation), integrity check results (any F-FUNDER-CORPUS-INTEGRITY events since last review), and low-relevance candidates (docs below `funder_doc_low_relevance_threshold` flagged for archive/).
- **Operator action:** promote / reject / archive / leave-pending. Each action signed; logged to register's `audit_chain`.

**v1.x Archivist takes ownership.** Quarterly curation becomes Archivist's recurring task (per v7.0.6 reservation; full spec in v1.x curation amendment). Archivist surfaces operator-action prompts at scheduled intervals; operator retains final decision authority.

## §5.v7-0-5.3 Stage-5 consent tier handling (forward-design only)

**v0.1 ships zero commons participation.** No v0.1 component reads `consent_tier` for routing. Schema reserves field for forward design.

**Schema-level enforcement (active in v0.1):**

- Match DB write wrapper validates `audit_chain.operator_signature_per_consent_tier_change` on every consent_tier mutation. Missing → F-MATCH-DB-CONSENT-TIER-VIOLATION (per §4 v7.0.5 companion + amendment §5.4).
- White-glove onboarding: `consent_tier` set per-client at first session; default `my_eyes_only`; operator can override at white-glove (Tier 2 onboarding).
- Per-cycle override: operator can change consent_tier per-grant-cycle at SP0 stage; signed audit_chain row required.

**Stage-5 forward path (out-of-scope for v0.1 / v1 / v1.x):**

- Commons-side architecture spec lives in future Stage-5 amendment.
- v7.0.5 schemas accommodate the consent_tier field so Stage-5 lands without schema migration.
- Three tiers (`my_eyes_only` / `matchable_to_opportunities` / `composable_with_others`) per cooperative sovereignty memory.
- No v0.1 / v1.x execution depends on commons existing.

## §5.v7-0-5.4 SP0 integration

SP0 KFR Freshness Review (per v7.0.4 §5) extends in v7.0.5:

- SP0 surfaces `funder_intel_documents_to_review_at_sp0`: any Funder Intel docs cited in the cycle's match reasoning that are stale per F-FUNDER-CORPUS-STALE thresholds.
- SP0 hard-blocks pipeline advance if a stale Funder Intel doc is cited and lacks operator confirmation in current cycle.
- SP0 also surfaces consent_tier defaults for the current cycle's Match DB entries; operator confirms or overrides.

## §5.v7-0-5.5 Lessons-delta integration

Match Database outcomes feed `pipeline/institutional_memory/lessons.json` per existing pattern. v7.0.5 adds per-funder pattern detection rules:

- 3+ consecutive `rejected` outcomes for same funder × same client → surface "previously declined; reconsider" advisory at next Scout REVIEW.
- Award amount drift across cycles for same funder → surface to operator if award_amount delta > 25% from prior cycle.
- Outcome statistics by `funder_type` × `sectors_relevant` feed Scout's match scoring weights at v0.2 horizon (out-of-scope for v0.1; Archivist v1.x candidate work).

Full mechanism specs at `pipeline/architecture/v0.1/architecture_v7_0_5_amendment.md`.

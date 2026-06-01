# Spec card — pipeline.intake.cic_selection (Intake CIC Selection step)

**Architecture anchor:** `pipeline/architecture/v0.1/architecture_v7_0_8_amendment.md` §6 (LOCKED 2026-05-08).
**Spec-card version:** v1
**Round:** post-v7.0.8-LOCK (companion module 2 of 3).
**Priority:** v0.1 medium — F-CIC-CLC-MATCH-NULL stays dormant per-org until this module ships and operator runs CIC Selection at white-glove.

---

## Purpose

Add the CIC Selection step to white-glove Intake (per v7.0.6 Intake module spec + v7.0.4 KFR substrate). Operator selects one or more `CustomerIdentityCategory` IDs for the org; result persists to `orgs/<slug>/PROJECT_CONTEXT.md` `cic_active` field per v7.0.8 §2. Without this module, every existing client's PROJECT_CONTEXT.md lacks `cic_active` and post-dormancy F-CIC-CLC-MATCH-NULL fail-closes.

## Five-step flow (per v7.0.8 §6)

1. **Inventory** — present operator with the six canonical CICs + their tagline + `Includes` sub-categories (per CLAUDE.md § Six Customer Identity Categories).
2. **Suggest** — Intake's BULK-mode extraction over org documents may suggest one or more CICs based on document signal. Suggestions cite verbatim quote with provenance per v7.0.4 F-EXTRACTOR-FABRICATION discipline.
3. **Operator confirm or override** — operator selects one or more `CustomerIdentityCategory` IDs.
4. **Composition implications surface** (per Cycle-1 E-05 / F-10 fix) — when operator selects multi-CIC at step 3, Intake immediately surfaces the v7.0.8 §7 composition rule the operator is opting into:
   - which primitives merge by union (Search Vocabulary, Evidence Schema)
   - which take most-stringent (Reporting Rhythm cadence)
   - which require per-grant select-one resolution (Language Register, narrative voice, tone) — and will trip F-MULTI-CIC-CHOICE-UNRESOLVED on every grant cycle until operator resolves them via `match_overrides:`
   - operator confirms the multi-CIC composition profile is understood + acceptable, OR backs out to single-CIC, before proceeding to step 5.
5. **Sign and persist** — `cic_active` populated; operator signature recorded; ledger entry filed.

## Inputs

- `org_slug` (string)
- `intake_extracted_evidence` (list of (verbatim_quote, source_path, page_number) triples) — from v7.0.4 BULK extraction
- `operator_terminal_callable` — interactive prompt callable for operator confirm/override

## Outputs

Mutates `orgs/<org_slug>/PROJECT_CONTEXT.md` to add:

```yaml
cic_active:
  - <one_or_more_of_six_canonical_ids>
cic_active_set_at: <iso8601_utc>
cic_active_set_by: <operator_signature_or_intake_module>
cic_active_set_via: white_glove_intake
```

Plus one ledger entry per BT9 hash-chain discipline.

## Acceptance tests

- All 6 canonical CICs accepted as selection targets.
- Multi-CIC selection (2+ values) triggers step-4 composition-implications surface; operator must explicitly acknowledge before step 5.
- Step-4 surface is mandatory — bypass attempt (programmatic skip) fails the acceptance suite.
- Operator backs-out from step 4 → falls back to step 3 with the multi-CIC selection cleared.
- Suggestions from step 2 cite verbatim_quote + source_path + page_number. Suggestions without provenance fail-closed (F-EXTRACTOR-FABRICATION territory).
- After step 5, `orgs/<slug>/PROJECT_CONTEXT.md` carries the canonical fields and the operator-signed ledger entry.
- Re-running CIC Selection on the same org with different selection produces a new ledger entry (operator-signed); the prior selection is archived but the new one becomes canonical.

## Migration path (per v7.0.8 §10 + RT-06 fix)

Existing orgs hit F-CIC-CLC-MATCH-NULL.cic_unset on first grant-cycle attempt post-LOCK. Per-org dormancy starts then. Operator runs Intake CIC Selection within the org's 14-day window. Dormancy state lives in `orgs/<slug>/vault/migration_state.yaml::f_cic_clc_match_null.first_attempt_iso8601` and `dormancy_expires_iso8601`.

## Coordination

- Composes against v7.0.4 (KFR Intake substrate — verbatim-quote provenance).
- Composes against v7.0.6 (Intake support agent in roster).
- Composes against v7.0.7 (Classification Review stage runs AFTER CIC Selection — CIC active list informs Card-archetype default classifications).

## Open questions for build session

1. Should the step-4 surface be a multi-screen confirmation or a single-page summary? (Suggest: single page with checkbox-confirm per primitive type — operator sees all four composition rules at once.)
2. If operator changes `cic_active` post-onboarding, do existing in-flight grant cycles get re-resolved, or do they keep the prior CIC profile? (Suggest: in-flight cycles keep prior; new cycles use new — operator can M13-bypass to re-resolve a specific in-flight grant.)
3. Programmatic-vs-interactive Intake split: this spec assumes interactive. INCREMENTAL mode (per v7.0.4) adds documents post-onboarding without re-running CIC Selection. Confirmed — INCREMENTAL doesn't trigger CIC Selection unless operator explicitly initiates.

# Scout to Sheetbook Projection Contract

## 1. Existing Target Model Summary

The target model consists of the JSON nervous-system schema (`tilth_nervous_system_schema.json`) and the workbook renderer (`build_workbook.py`). 

**Explicit Model Rules:**
- The sheetbook is a rendered projection.
- Machine truth lives in JSON/ledger rows.
- Templates define shape, not source truth. (e.g. `Tilth_Command_Workbook_TEMPLATE.xlsx`)
- Every fact-bearing row defaults to unverified.
- Workbook rows are not authoritative records.
- Manual workbook edits are non-authoritative unless captured as append-only operator decisions.

## 2. Source Inventory and Source Roles

### A. `SCOUT_MAX_2026-06-04.md`
- **source_role:** curated_scan
- **freshness_state:** current
- **org_scope:** MSI-only
- **authority:** unverified Scout interpretation
- **use:** prioritization, candidate extraction, evidence-gap extraction, action generation

### B. `PORTFOLIO_ROADMAP_2026-06-05.md`
- **source_role:** curated_strategy
- **freshness_state:** current
- **org_scope:** MSI portfolio routing
- **authority:** unverified unless operator-confirmed or RFA-verified
- **use:** strategy context, route questions, portfolio sequencing, but not route truth or RFA truth

### C. `scout_2026-04-15_*.json`
- **source_role:** raw_scan
- **freshness_state:** older discovery tier
- **authority:** raw/archival
- **use:** Grants.gov IDs, source recovery, dropped_past_close, source provenance, dedupe/disambiguation
- **warning:** useful for provenance and identity; not automatically current

**Four-pass handling:**
- `_1744` = empty / failed-run shaped, 0 hits; ignore for content.
- `_1728` = pre-dedup, 288 hits, only source of 45 `dropped_past_close` records.
- `_1746` = deduped snapshot, 223 hits.
- `_2159` = latest deduped snapshot, 224 hits.

### D. `PROJECT_CONTEXT.md`
- **source_role:** operator_context / project_context
- **authority:** operator-attested but not inerrant
- **use:** organizational context and entity constraints
- **warning:** can itself be contradicted by Scout/RFA evidence and flagged for correction

### E. `Tilth_Command_Workbook_TEMPLATE.xlsx`
- **source_role:** workbook_template
- **authority:** shape only
- **use:** tab layout / rendering shape
- **warning:** not source truth

### F. `master_workbook_v0.xlsx` (if referenced)
- **source_role:** prior_projection
- **authority:** untrusted unless rows trace to source
- **use:** design reference only unless row-level provenance exists

### G. `Golden Quill/agnostic_route_substrate/ROUTE_VERTICAL_SLICE_CONTRACTS.md` and `field_roles.json`
- **source_role:** route_scaffold / proof_scaffold
- **authority:** read-only local route substrate reference
- **warning:** currently located in git-ignored proof/scaffold directory. Note that these should be promoted to a tracked location in a later task, but do not move them now.
- **use:** route state vocabulary and route-affordance context only

## 3. Layer Model

**Pipeline Definition:**
`source files` -> `raw extraction records` -> `canonical source ledger` -> `normalized funder/opportunity/date/evidence/action/route-question tables` -> `existing Tilth nervous-system JSON files` -> `rendered sheetbook tabs` -> `append-only operator decision ledger`

Do not allow chatbot or workbook edits to write directly to canonical truth.

**Projection Invariants:**
- A rendered workbook row is never the authoritative record.
- A rendered workbook row must be reproducible from JSON ledger rows plus renderer logic.
- Manual workbook edits are non-authoritative unless captured as append-only operator decisions.
- Re-running projection with unchanged source files and unchanged decision ledger must produce stable canonical IDs.
- Re-running projection after source updates must preserve prior provenance and mark changed fields as changed, conflicted, or superseded.

## 4. Field Mapping Into Existing Schema

**Expected Mappings:**
- `funder_universe.json` -> `08_Funder_Universe`
- `opportunities.json` -> `09_Active_Candidates`
- `date_spine.json` -> `06_Date_Spine`
- `fit_likelihood_rules.json` -> `07_Fit_Likelihood_Rules`
- `evidence_assets.json` -> `13_Evidence_Checklist`
- `source_ledger.json` -> `16_Source_Ledger`
- `do_not_say_quarantine.json` -> `15_Do_Not_Say`
- `action/operator decisions` -> `11_Action_Queue` or append-only decision ledger proposal

*Note on Contradictions/Gaps:* `tilth_nervous_system_schema.json` does not currently contain definitions for an action queue, operator decisions, or the `11_Action_Queue` tab, which is present in `build_workbook.py`.

For each mapped field, distinguish:
- hard extracted fact
- Scout interpretation
- operator decision
- RFA-verified fact

Do not use workbook templates as factual sources.

**Out of Scope Files (for Scout ingest alone):**
- `entities`
- `project_lanes`
- `compliance_gates`
- `contacts`
- `packet_registry`

These are populated by operator setup, route engine, compliance logic, or later workflow stages — not by Scout discovery alone.

## 5. Schema Gap Rule

If the existing Tilth Output Standard schema lacks a field needed by this contract, do not modify the schema. Instead, document it.

**Known Schema Gaps:**
1. **Action Queue / Operator Decisions:** 
   - *Required concept:* Action tracking and append-only operator decisions.
   - *Existing closest field:* `opportunities.json` contains a `next_action` field.
   - *Proposed extension:* Add `action_queue.json` and `decision_ledger.json` definitions to `tilth_nervous_system_schema.json`.
   - *Impact:* Reduces fidelity; decisions can currently only be represented as raw notes or inferred from the opportunity's `next_action`.

2. **Deadline Normalization:**
   - *Required concept:* Multi-stage or complex deadline schemas (e.g. `deadline_type`, two-stage deadlines).
   - *Existing closest field:* `date_spine.json` contains `window` and `honest_read`.
   - *Proposed extension:* Add structured deadline fields (start, end, type, pre-application vs. full).
   - *Impact:* Reduces fidelity; complex deadlines must be written into `honest_read` or generic string fields.

## 6. State Axes

Do not collapse status into one field.

**A. funder posting / lifecycle state**
- `posted`
- `forecasted`
- `past_close`
- `rolling`
- `expected_reopen`
- `archived`
- `unknown`

**B. verification_status**
- `unverified`
- `in_review`
- `verified`
- `quarantined`

**C. disposition**
- `active_candidate`
- `parked`
- `not_fit`
- `dropped_archive`
- `do_not_say`

**D. next_action**
- `VERIFY_RFA`
- `VERIFY_ELIGIBILITY`
- `PULL_NOFO`
- `ROUTE_NEEDED`
- `OPERATOR_DECISION_NEEDED`
- `RESOLVE_CONFLICT`
- `ARCHIVE_PAST_CLOSE`

**Rule:**
- `VERIFY_RFA` is not a verification status. `VERIFY_RFA` is an `in_review` row plus `next_action`.
- Verification must be field-aware.
- A canonical opportunity may contain mixed verification states. Do not imply the whole opportunity is verified because one field is verified.

## 7. Stable ID and Hash Rules

**Stable IDs:**
- `source_file_id`
- `source_record_id`
- `canonical_funder_id`
- `canonical_opportunity_id`
- `rendered_row_id`
- `projection_run_id`
- `source_content_hash`
- `extraction_rule_version`
- `renderer_version`

**Opportunity identity rule:**
- Use Grants.gov opportunity ID / oppId when available.
- For non-federal opportunities, use: normalized funder + normalized opportunity/program title + source URL or program URL + cycle/year where available.
- Do not use row number as identity. Row number is provenance only.

**canonical_funder_id rule:**
Define `canonical_funder_id` in a way that is forward-compatible with existing FID / `pipeline/funder_intelligence` `funder_id` concepts. Avoid creating a second incompatible funder identity system.

## 8. Provenance Contract

Every rendered row must carry or be traceable to:
- `source_file_id`
- `source file path`
- `source section / JSON path / row locator`
- `extracted text or raw value`
- `transform rule`
- `source_role`
- `verification_status`
- `org_slug: mycosymbiotics_inc`
- `classification/posture` if available
- `source_ids` linking back to `source_ledger`
- `extraction_rule_version`
- `projection_run_id`

Every fact-bearing row must trace to `source_ledger`.

## 9. Fit vs Likelihood

Keep fit and likelihood separate:
- Fit = programmatic match
- Likelihood = realistic odds/readiness/competitiveness/match/timing

Never average fit and likelihood. Never collapse fit and likelihood into one score. High fit can still be low likelihood.

A historical negative signal (e.g. prior close date, prior rejection, expired cycle) lowers likelihood/readiness. It does not automatically lower programmatic fit. "Archive: closed" and "curated: high fit" is not a contradiction.

## 10. Route Binding Rule

- Entity route must come only from the route-resolution affordance/evaluator loop.
- Do not infer route from Scout notes, portfolio notes, or person mentions.
- Do not mint new route truth from funding opportunity text.
- Rows may generate route questions, but not route truth.
- Person routes stay visibly flagged.
- Unresolved routes remain UNRESOLVED until the route engine returns a valid state and human approval if required.
- Lanes/entities are referenced, not created. Scout opportunities may bind only to existing `lane_id`/`entity_id` values.
- If no valid lane/entity mapping exists: set `next_action: ROUTE_NEEDED` or `OPERATOR_DECISION_NEEDED`. Do not mint new lanes or entities. Do not infer MycoSymbiotics Cooperative data into MycoSymbiotics Inc.

## 11. Conflict Rules

- Disambiguate identity before declaring a conflict.
- If raw April JSON and curated SCOUT_MAX / roadmap disagree on material extracted fields, preserve both values. Do not choose silently.
- Set the affected field `verification_status` to `in_review`.
- Add `next_action: VERIFY_RFA`, `VERIFY_ELIGIBILITY`, or `RESOLVE_CONFLICT`.
- Add an action row for human/source resolution.
- Do not quarantine ordinary conflicts between real sources. Quarantine is only for unverifiable, fabricated, unsafe, or do-not-say claims.

**Fit/likelihood conflict rule:**
Raw April JSON does not carry judgment fields such as fit or likelihood unless the actual JSON proves otherwise. Therefore, raw-vs-curated cannot normally conflict on fit. Fit or likelihood disagreements arise only curated-vs-curated, curation-vs-operator, or operator-vs-operator.

**Supersession rule:**
Current curated Scout may supersede older raw Scout for prioritization and projection defaults, but it does not erase older raw values. Older raw values remain provenance records.

## 12. Quarantine vs Archive

**Define the difference:**
- `dropped_archive` / `not_fit` = real opportunity, wrong timing, wrong cycle, wrong fit, or not currently actionable.
- `quarantined` / `do_not_say` = unverifiable, fabricated, unsafe, misleading, unsupported, or funder-facing-dangerous claim that must not reach funder-facing output.

Do not merge these states. Do not render quarantined claims into funder-facing material. A closed real opportunity goes to `dropped_archive`, not quarantine.

## 13. Deadline Normalization

**Define fields:**
- `deadline_type`
- `deadline_date`
- `deadline_window_start`
- `deadline_window_end`
- `deadline_text_raw`
- `deadline_confidence`
- `deadline_verification_state`

**Allowed `deadline_type` values to start:**
- `fixed_date`
- `rolling`
- `annual_window`
- `expected_reopen`
- `forecast_only`
- `past_close`
- `unknown`

Do not convert expected windows into fake exact dates. Two-stage deadlines must be preserved. (Schema gap noted: currently schema uses flat `window` / `honest_read` fields, so two-stage representations must flow to `honest_read` or action rows until the schema is extended).

## 14. Operator Decision Ledger

**Define an append-only operator decision record:**
- `decision_id`
- `canonical_opportunity_id`
- `decision_type`
- `decision_value`
- `decision_note`
- `decided_by`
- `decided_at`
- `supersedes_decision_id`
- `source_ids` considered
- `verification_status_at_decision`

Rendered workbook shows latest decision but does not overwrite history. Operator decisions may affect rendered projection state but may not mutate source facts. (Schema gap noted: not natively represented in current `tilth_nervous_system_schema.json`).

## 15. Worked Examples

### A. AFRI (Required Example)
AFRI must demonstrate identity/disambiguation before conflict, not blind merge/dedupe.
- `AFRI-011677`, "Strengthening Agricultural Systems", close 2026-04-23 / past close
- `AFRI-011134`, "Foundational", close 2026-12-31
- `AFRI-011596`, "Education", close 2026-12-31
- `SCRI-011676`, close 2026-06-15

SCOUT_MAX's "AFRI Foundational & Applied Science" is a candidate match to `011134` requiring verification because SCOUT_MAX does not explicitly name that opportunity ID; it must not be treated as a confirmed binding to `011134` or merged with the closed `011677`. Therefore:
- `011677` and `011134` must be separate canonical opportunities.
- `011677` archives as `DROPPED_PAST_CLOSE` / `past_close`.
- `011677` must not contaminate or downgrade `011134`'s fit.
- `011134` may remain `active/in_review` with its own provenance.
- The example demonstrates disambiguation-before-conflict and per-field provenance.

### B. FFAR Seeding Solutions (Required Example)
FFAR must demonstrate curated-markdown-only provenance and source-located facts. 
Values to verify:
- award amount: $300K-$1M
- deadline: pre-app Jun 10 / full Jul 1
- match: non-federal match

Do not fabricate values from previous iterations or infer award, deadline, or match terms unless the current source explicitly states them. 
Schema gaps exposed: two-stage deadline (pre-application plus full proposal) and fit ranges ("3-4") which the schema lacks (schema only supports High/Medium/Low). These are recorded as schema gaps or transform-rule questions.
Verification handling:
- `curated_scan` source only
- `verification_status`: `unverified` or `in_review`
- `next_action`: `VERIFY_RFA` and `VERIFY_MATCH_REQUIREMENT`
- Scout fit remains Scout interpretation, not RFA truth.

### C. NEA Grants for Arts Projects (Optional Example)
NEA must demonstrate not-fit/archive/reroute-question behavior without cross-org contamination. It explicitly shows why an arts/culture opportunity cannot be silently imported into MycoSymbiotics Inc just because it may fit William, MycoSymbiotics Cooperative, or a partner route.
May generate: `not_fit`, `dropped_archive`, `route question`, or `operator decision needed`. It may not become an Inc opportunity fact unless the source supports Inc relevance.

## 16. Explicit Non-Inference Rules

- Do not fill missing fields from memory.
- Do not port MycoSymbiotics Cooperative data into MycoSymbiotics Inc.
- Do not treat Scout notes as RFA truth.
- Do not turn `VERIFY_RFA` into verified.
- Do not infer `entity_route`.
- Do not let chatbot write workbook cells.
- Do not use templates as factual sources.
- Do not render quarantined claims into funder-facing material.
- Do not mint new lane IDs from Scout opportunities.
- Do not mint new entity IDs from Scout opportunities.
- Do not collapse distinct program numbers into one opportunity.
- Do not convert vague windows into fake exact dates.
- Do not average fit and likelihood.
- Do not downgrade fit because of past-close status; route that signal to likelihood/readiness/disposition instead.
- Do not glob April JSON runs into one averaged source.
- Do not let the empty `_1744` run suppress valid later runs.
- Do not use ignored proof/scaffold files as output destinations for durable contracts.

## 17. Acceptance Criteria

1. Every rendered opportunity row traces to at least one `source_ledger` record.
2. No rendered fact exists without `source_file`, `source_pointer`, `extracted_value`, and `transform_rule`.
3. Workbook templates never become factual opportunity sources.
4. Dropped or past-close opportunities render only into archive/not-fit/dropped views, not active candidates.
5. MycoSymbiotics Cooperative data cannot enter `mycosymbiotics_inc` unless the source explicitly names Inc or an operator creates a valid cross-entity relationship decision.
6. `VERIFY_RFA` never renders as verified eligibility.
7. Re-running the projection with unchanged inputs produces stable IDs.
8. Operator decisions do not mutate source ledger rows.
9. Conflicting source values generate verification/action tasks instead of silent overwrites.
10. Ordinary source conflicts set affected fields to `in_review`, not `quarantined`.
11. Quarantined claims do not render into funder-facing output.
12. Distinct Grants.gov opportunity IDs remain distinct canonical opportunities.
13. Historical negative timing signals affect likelihood/readiness/disposition, not programmatic fit.
14. Route truth is never inferred from Scout notes.
15. The contract stops before workbook writing, route application, UI work, chatbot runtime, source mutation, staging, commit, or push.
16. Output contract is written to `docs/route_substrate/`, not the ignored `Golden Quill/` proof/scaffold directory.
17. April JSON pass handling preserves per-file provenance and does not average runs.

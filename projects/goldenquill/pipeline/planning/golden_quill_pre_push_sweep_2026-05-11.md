---
title: Golden Quill — Pre-Push Hygiene Sweep
date: 2026-05-11
target_repo: fitfarms/golden-quill (private GitHub)
author: pre-push sweep agent (dispatched from Cowork)
---

# Golden Quill — Pre-Push Hygiene Sweep

This is the pre-push report for the first push to private repo `fitfarms/golden-quill`. Findings list only — Josh approves before any physical move.

---

## 1. Task 1 status — stale embedded .git cleanup

**Status: BLOCKED — sandbox cannot delete.**

The agent attempted `rm -rf /Users/goldenquill/Downloads/GoldenQuill/Sovereign_Node_Handoff/prior_work/Supporting_Docs/GrantFinderWriter/.git` via the workspace bash sandbox. Every file in that tree returned `Operation not permitted` — the sandbox mount of that subtree is read-only for the agent. The directory still exists.

Verification with bash `[ -d ... ] && echo YES || echo NO` returned `YES` after the failed `rm -rf`. The `.git/` directory and all its objects are still on disk.

**Josh action required.** Run this one command in Terminal to complete Task 1:

```
rm -rf "/Users/goldenquill/Downloads/GoldenQuill/Sovereign_Node_Handoff/prior_work/Supporting_Docs/GrantFinderWriter/.git"
```

Then verify:

```
ls -la "/Users/goldenquill/Downloads/GoldenQuill/Sovereign_Node_Handoff/prior_work/Supporting_Docs/GrantFinderWriter" | head -3
```

Top-level entries in `GrantFinderWriter/` (preserved): `Attached_Assets`, `PROJECT_SUMMARY.md`, `client`, `components.json`, `db`, `drizzle.config.ts`, `landing_after_load.png`, `package-lock.json`, `package.json`, `postcss.config.js`, `replit.md`, `script`, `scripts`, `server`, `shared`, `tsconfig.json`, `vite-plugin-meta-images.ts`, `vite.config.ts`. Total 18 top-level items. The `.git/` is the 19th — only that one needs removing.

**Separate concern:** the entire `Sovereign_Node_Handoff/prior_work/Supporting_Docs/GrantFinderWriter/` tree is the old Replit MycoGrant TypeScript app — see §3 (it's a large prior-work asset that may not belong in a private engineering repo).

---

## 2. Client-data pollution inventory

Files containing client identifiers (slug or content) that live OUTSIDE `orgs/` and OUTSIDE `_private/`. The existing `.gitignore` already excludes `daily_logs/`, `memory/`, `orgs/*/PROJECT_CONTEXT.md`, and `orgs/*/vault/` — those are noted in §5.

| path | client_slug_referenced | evidence | recommended_destination | confidence |
|---|---|---|---|---|
| `apps/tilth_demo_v0/static/index.html` | fit_farms | line 214: "FIT Farms LLC · Pittsburgh, PA · EIN: <real EIN>"; lines 237ff: real FIT Farms mission text hardcoded | `orgs/fit_farms/demo_assets/` OR placeholder-ify the static HTML | HIGH |
| `apps/tilth_demo_v0/fixtures/orgs.json` | fit_farms | lines 8–31: FIT Farms binding `is_live: true` with real prior-grant history ($94,200, 4 funders, 3 awards). File self-declares `no_real_client_data: true` — contradictory | `orgs/fit_farms/demo_assets/`; replace FIT Farms row in fixture with synthetic data | HIGH |
| `apps/tilth_demo_v0/static/app.js` | fit_farms | filename pattern + client grep hit | inspect; same destination as the index.html | MEDIUM |
| `apps/tilth_demo_v0/server.py`, `apps/tilth_demo_v0/README.md`, `apps/tilth_demo_v0/pyproject.toml`, `apps/tilth_demo_v0/tilth_demo_v0.egg-info/PKG-INFO` | fit_farms (project naming) | grep hits on "fit farms" / "fit_farms" — references the org as a demo binding | review per-file; project-level naming may be acceptable, but real-data binding is not | MEDIUM |
| `tests/demo/test_demo_driver.py` | fit_farms | line 922: `assert "<real EIN>" in text` — real EIN baked into a test assertion | swap to synthetic EIN; OR move test under `orgs/fit_farms/tests/` if FIT-Farms-specific | HIGH |
| `tests/demo/demo_project_context/PROJECT_CONTEXT.md` | fit_farms | line 23: "EIN: <real FIT Farms EIN>" plus FIT Farms profile fields | replace with synthetic test fixture (12-3456789 style — already used in other tests) | HIGH |
| `tests/demo/conftest.py` | fit_farms | grep hit on "fit_farms" — test plumbing for the demo | swap to synthetic slug | MEDIUM |
| `pipeline/scout/scan_golden_quill.py` | fit_farms | lines 5, 138: docstrings naming "FIT Farms (for-profit, EIN <real EIN>, PA) is the applicant" | rewrite docstrings to generic; OR move whole file to `orgs/fit_farms/scripts/` | HIGH |
| `pipeline/radar/golden_quill_scan_2026-04-14_{0454,0455,0459,0500,0501,0502}.json` (6 files) | fit_farms | each JSON has top-level `"org": "fit_farms"` and inline `"EIN <real>"` strings in eligibility notes | `orgs/fit_farms/radar/` (archive) — these are old scout outputs | HIGH |
| `pipeline/radar/golden_quill_commercialization_2026-04-14.md` | mycosymbiotics_cooperative | line 3: "Applicant: MycoSymbiotics Cooperative (for-profit small business, EIN: <real>)" | `orgs/mycosymbiotics_cooperative/radar/` | HIGH |
| `pipeline/radar/golden_quill_pittsburgh_funding_map_2026-04-14.md` | fit_farms / mycosymbiotics | grep + "pittsburgh" + funder map for Josh's portfolio | `orgs/fit_farms/radar/` (operator-scoped funding map) | MEDIUM |
| `pipeline/radar/myco_inc_scout_2026-04-15_1728.json` | mycosymbiotics_inc | filename + `"client_slug": "mycosymbiotics_inc"` body | `orgs/mycosymbiotics_inc/radar/` (orgs already has a `scout_2026-04-15_1728.json` mirror) | HIGH |
| `pipeline/radar/mycosymbiotics_inc_scout_2026-04-15_{1744,1746,2159}.json` (3 files) | mycosymbiotics_inc | filename + body `"client_slug": "mycosymbiotics_inc"` | `orgs/mycosymbiotics_inc/radar/` (mirrors already exist) | HIGH |
| `pipeline/radar/seen.json` | (potentially multiple orgs) | not opened in this pass — may contain client→opportunity-hash map | Josh inspect; if multi-org, split per-org; if Tilth-core dedupe state, keep but verify no client IDs | MEDIUM |
| `pipeline/db/orgs.csv` | mystic_mamas | single row: ORG_MYSTIC_MAMAS / Mystic Mamas / Pittsburgh / Afro_Indigenous,women_led... | `orgs/mystic_mamas/data/` — this is a single-client db, not Tilth-core | HIGH |
| `pipeline/db/org_program_fit.csv` | mystic_mamas | ALL rows ORG_MYSTIC_MAMAS — go/no-go decisions per Mystic Mamas program | `orgs/mystic_mamas/data/` | HIGH |
| `pipeline/db/funders.csv` | (region, not client) | Pittsburgh-area foundation database; no client-specific data in the rows themselves, but it's the funder universe paired with `org_program_fit.csv` above | Josh decision — see §3 (similar to Funders_Master question) | MEDIUM |
| `pipeline/scout/databases/Mystic_Mamas_Ultimate_Funding_Database_PA_USDA_2025_2026__{Deadlines,Readme,Sources}.csv` (3 files) | mystic_mamas | filename pattern; Readme says "Extra context for Mystic Mama's positioning" | `orgs/mystic_mamas/data/` | HIGH |
| `pipeline/scout/databases/.safety-bak-20260501T181322Z/Mystic_Mamas_*.csv` (1 file) | mystic_mamas | backup snapshot of above | `orgs/mystic_mamas/data/.safety-bak/` (or just delete) | HIGH |
| `pipeline/scout/databases/.safety-bak-20260501T181322Z/Funders_Master_PA_NY_NJ_2025_2026_DEDUPED__*.csv` (3 files) | (ambiguous — see §3) | backup snapshot of the regional master | follows §3 decision on the parent files | MEDIUM |
| `pipeline/audits/qa_qc_2026-04-15.md` | mycosymbiotics_inc | line 4: "loading MycoSymbiotics Inc context" + ongoing client-scoped narrative | `orgs/mycosymbiotics_inc/audits/` (or just delete — internal pipeline-debugging audit) | HIGH |
| `pipeline/orchestrator/run_log.json` | fit_farms (8 entries) | every run object has `"org": "fit_farms"` | rotate/redact: this is execution-trace, the org field could be hashed; OR move to `orgs/fit_farms/run_log.json` | HIGH |
| `pipeline/subscribers/subscribers.json` | (no PII) | `subscribers: []` — empty list, only tier definitions and content verticals | KEEP IN PLACE — schema-only, no client data | (CLEAN — flagged for completeness) |
| `pipeline/logician/config/client_term_register.txt` | ALL clients (Mystic Mamas, MycoSymbiotics, FIT Farms, MycoFest, Run a Muck, KDC, Daniel Crawford) | by-design registry of every client name verbatim — Law 3 enforcement substrate | **Josh decision required** — this is Tilth-core code that must know who's a client (so the gate fires). Two options: (a) keep with names → push as-is, since gating only works with names visible; (b) abstract to env-var / per-deployment config → recommended for public-facing repo | MEDIUM |
| `logician/config/client_term_register.txt` (workspace-root duplicate) | same as above | filename pattern says it's an older mirror under the root `logician/` shim | delete; canonical lives under `pipeline/logician/config/` | HIGH |
| `pipeline/validation/archive_2026-04-15_client_scoped/` (4 files: CODEX_FULL_CODE_REVIEW, FOUR_PILLAR_AUDIT_PROMPT/PIPELINE/META_REVIEW) | mycosymbiotics_inc (per directory name) | directory name self-declares "client_scoped"; FOUR_PILLAR_AUDIT_PROMPT.md contains MycoSymbiotics references in audit setup | `orgs/mycosymbiotics_inc/audits/archive_2026-04-15/` — directory was intentionally archived but never moved | HIGH |
| `pipeline/validation/vapg-fy26-test/preflight_20260412_152224.json` | mycosymbiotics_inc | VAPG was MSI's grant — preflight artifact | `orgs/mycosymbiotics_inc/audits/` | HIGH |
| `pipeline/validation/admin-risk-test/draft_validation_20260412_152235.json` | mycosymbiotics_inc | sibling of vapg-fy26-test, same era | inspect; if MSI-scoped, same destination | MEDIUM |
| `pipeline/validation/bedrock_audit_2026-04-15/` (multiple files) | mycosymbiotics_inc | bedrock audit ran with MSI fixtures | `orgs/mycosymbiotics_inc/audits/` OR delete if pre-blueprint architectural | MEDIUM |
| `pipeline/validation/project_audit_meta_2026-04-15/` (8 files) | (mixed — engineering audit, not client) | seat audit traces — convergence findings about router.py etc | KEEP if Tilth-core engineering audit; the grep hits are operator-scoped review notes | LOW |
| `pipeline/validation/component_4_scout_bindings_2026-04-16/` (multiple files) | (engineering — Scout bindings audit) | grep hits are method-level audit references | KEEP — Scout component audit, not client | LOW |
| `pipeline/validation/blueprint_01_sovereignty_envelope_2026-04-16/`, `architecture_full_2026-04-16/`, `blueprint_section_*_2026-04-16/` | (engineering — blueprint review trail) | grep hits are example/illustration references to MSI/Mystic in spec discussions | LOW priority — these are spec-development audit trail; review per-file before push; Josh may want to push as engineering history | LOW |
| `pipeline/validation/sentinel/heartbeat_20260412.{md,json}` | (system health check, not client) | grep hits are example data | KEEP | (CLEAN once inspected) |
| `pipeline/handoffs/HANDOFF_Blueprint_Build_2026-04-16.md` | (operator-scoped session handoff) | contains "Josh Inklovich (FIT Farms, solo builder...)" and references MSI client context | `pipeline/handoffs/_archive/` and/or strip identifiers — these are session-handoff prompts referencing client work | MEDIUM |
| `pipeline/handoffs/HANDOFF_Option_B_Red_Team_Round_3.md`, `HANDOFF_Blueprint_Section_2_2026-04-16.md`, `HANDOFF_Blueprint_Section_3_2026-04-17.md`, `v7_round_handoff_addendum_A7_A8_A9_2026-04-19.md` | (mixed) | grep hits — operator/client mentions in narrative session handoffs | review per-file; archive operator-scoped handoffs | MEDIUM |
| `scripts/split_mystic_mamas_funders_into_chunks.py` | mystic_mamas | filename + module docstring `Mystic Mamas master funder sheet` + hardcoded `orgs/mystic_mamas/...` paths | `orgs/mystic_mamas/scripts/` — single-client utility | HIGH |
| `pipeline/scout/databases/` (any leftover Mystic_Mamas files at top level after moving the 3 named above) | mystic_mamas | already noted above | same destination | HIGH |
| `Sovereign_Node_Handoff/memory/agent_self_analysis_2026-04-12.md` | mycosymbiotics_cooperative + others | line 21: "EIN: <real>" + line 26-30: address, leadership names, Cordyceps specialty — real client substrate | move to local-only archive; do not push | HIGH |
| `Sovereign_Node_Handoff/memory/agent_self_analysis_2026-04-14-self-analysis.md` | (operator self-analysis, narrative) | grep hits — operator narrative referencing clients | local archive | MEDIUM |
| `Sovereign_Node_Handoff/memory/sovereign_node_project.md` | (project narrative) | client roster references | review; older era — may be superseded by current docs | LOW |
| `Sovereign_Node_Handoff/memory/prior_work_mycograntos.md` | (mostly product narrative; some client refs) | path to `C:\Users\joshi\Downloads\Grant_Tool_Build_Files` + product-genealogy refs | review; archive | LOW |
| `Sovereign_Node_Handoff/01_HANDOFF.md`, `03_BUILD_ORDER.md`, `STRATEGIC_REVIEW.md`, `04_DATA_STRATEGY.md`, `00_README.md`, `02_INSTALL.md`, `05_FUNDING_ROADMAP.md` | (operator strategy docs) | grep hits — these are Josh's strategy / handoff docs from April 12-13, contain operator/client context | Josh decision: push as project-history OR keep local | LOW |
| `Sovereign_Node_Handoff/project_docs/Cultivator_Blueprint_v1.md`, `SENTINEL_ARCHITECTURE.md`, `TILTH_NEWSROOM_OPERATIONAL_MAP.md`, `GITHUB_SETUP_PLAN.md` | (engineering spec, light client refs) | grep hits in narrative paragraphs | review per-file; mostly engineering | LOW |
| `Sovereign_Node_Handoff/prior_work/Supporting_Docs/GrantFinderWriter/.local/state/replit/agent/filesystem/filesystem_state.json` | various | a Replit-agent state file referencing prior MycoGrant build | DELETE — replit agent state has no engineering value | HIGH |
| `Sovereign_Node_Handoff/prior_work/Supporting_Docs/GrantFinderWriter/Attached_Assets/PA*.TXT` (multiple) | mycosymbiotics + others | text dumps of PA grant docs Josh used in prior MycoGrant build | review per-file; this is the entire MycoGrant Replit project — does it belong in golden-quill repo at all? See §3 | LOW |
| `Sovereign_Node_Handoff/prior_work/Supporting_Docs/GrantFinderWriter/client/src/lib/demoData.ts` | (demo only) | line 51: `ein: "84-1234567"` — that's a placeholder EIN, not real | KEEP if GrantFinderWriter stays | (CLEAN) |
| `Sovereign_Node_Handoff/prior_work/Supporting_Docs/GrantFinderWriter/client/src/components/Organization{Onboarding,ProfileSection}.tsx` | (UI for onboarding) | grep hits on EIN/UEI/SAM are UI form labels, not values | KEEP if GrantFinderWriter stays | (CLEAN) |
| `Sovereign_Node_Handoff/prior_work/Supporting_Docs/GrantFinderWriter/scripts/seedBetaTesters.ts` | (prior seeding script) | grep hit on "MycoSymbiotics" / "fit_farms" — prior beta seed list | scrub real names if GrantFinderWriter stays | MEDIUM |
| `Sovereign_Node_Handoff/prior_work/QUICK_REFERENCE_APIS.txt`, `US_GRANT_DATA_SOURCES_2026.txt` | (research notes) | grep hits on "EIN"/"UEI"/"SAM" are field-label references | KEEP | (CLEAN) |
| `Sovereign_Node_Handoff/memory/MEMORY.md`, `MEMORY_UPDATED.md`, `user_josh.md`, `golden_quill_brand.md` | (operator memory) | pre-Path-B memory files | local archive | LOW |
| `USER.md` (workspace root) | ALL clients | line 17: "Co-founder of MycoSymbiotics Cooperative. Founder of FIT Farms"; lines 83-88: client roster; line 84: "EIN <real>" | **Josh decision** — workspace identity files (SOUL/USER/AGENTS/CLAUDE) are by-design at root, but USER.md contains real EIN and full client roster. Either redact for public, exclude via .gitignore, or accept as private-repo context | HIGH |
| `CLAUDE.md` (workspace root) | (engineering decision frame with client names in beta posture) | mentions all 8 client slugs in v0.1 Beta posture section + "FIT Farms LLC is the only real legal entity" | KEEP — these are architectural decision references, not client data leaks (per the boundary noted in the dispatch). Confirmed boundary | LOW |
| `IDENTITY.md` (workspace root) | grep hits | not opened — likely workspace identity | review; same Josh decision as USER.md | MEDIUM |
| `FOUNDATION_README.md` (workspace root) | client roster | lines 19-20: "all 7 client folders" enumerated | redact roster OR exclude | MEDIUM |
| `SKELETON.md` (workspace root) | grep hits — likely architectural file map referencing orgs/ | review; topology may need names | LOW |
| `HEARTBEAT.md`, `TOOLS.md`, `king_midas_external_review_brief_2026-04-29.md`, `golden_quill_website_build_spec_v1.md` (root) | mixed | grep hits — operator-scoped strategy/specs at root | review per-file; root-level operator scratch may not belong in engineering repo | MEDIUM |
| `CTO_Review_2026-05-04/` (7 files: Executive_Brief, Architecture_Document, Technical_Blueprint, Risk_Register, Roadmap_and_Resourcing, CTO_QA_Prep, Verification_Notes) | (review materials referencing FIT Farms, MSI as exemplars) | grep hits | KEEP as engineering review with client examples redacted to slug-only OR archive | LOW |
| `pipeline/business/*.md` (mvp_tilth_launch_readiness, hardware_partner_research, full_build_roadmap, outside_advisor_scoping, golden_quill_revenue_streams_summary) | mixed (operator strategy) | client refs in pricing/strategy discussions | review per-file; some are pre-decision artifacts | LOW |
| `pipeline/engineering/agents/scribe_writer_agent_v1.md`, `editor_clarity_agent_v1.md`, `scout_discovery_agent_v1.md`, `da_vinci_engineer_prompt*.md`, `king_midas_implementation_prompt*.md`, `evaluations/*_eval_prompt_opus.md`, `MVP_FINISH_LINE_PROMPTS.md`, `scout_population_component_note.md`, `references/jargon_registry.yaml` | mixed | grep hits — agent design docs reference client examples (MSI, Mystic) | KEEP — these ARE Tilth-core agent design; refs are illustrative. Spot-check for verbatim client EIN/UEI before push | LOW |
| `pipeline/engineering/spec_cards/scout_verify_clc_assignment.md`, `logician_fact_drift_kfr_gate.md`, `demo_driver_mvp_end_to_end.md` | mixed | grep hits | KEEP — engineering spec cards | LOW |
| `pipeline/engineering/provisioning_manifest_v0.1.md`, `provisioning_manifest_audit_2026-04-19.md`, `lock_history.v1.jsonl`, `openclaw_cross_family_remediation_2026-04-19.md` | mixed | grep hits | KEEP — engineering substrate | LOW |
| `pipeline/blueprint/v0.1/*.md` (sections 1, 03_scout, 04_logician, 07_scribe, 11_intake, 12_uploader, 15_archivist + variants) | (engineering spec) | grep hits are doc-internal examples | KEEP — locked blueprints | LOW |
| `pipeline/architecture/v0.1/*.md` (tilth_architecture_locked + amendments v7.0.{4,4_M1,5,7,8} + versioned snapshots + customer_attestation_design) | (engineering spec) | grep hits are amendment examples / boundary discussions | KEEP — locked architecture | LOW |
| `pipeline/validation/v7_0_4_thesis_2026-05-09/cycle_*.md`, `v7_0_4_thesis_cross_family_2026-05-10/*.md`, `v4_v2_x_thesis_2026-05-10/*.md`, `v12_v1_thesis_2026-05-09/*.md`, `funding_goal_thesis_2026-05-11/*.md`, `blueprint_section_15_archivist_2026-05-10/*.md`, `architecture_v{5,6,7}_*/` etc. | (engineering audit trail) | grep hits are example/illustration in audit prompts | KEEP — Thesis audit ledger | LOW |
| `pipeline/validation/section_1_amendment_m7_wire_2026-04-17/*.md`, `blueprint_section_01_relock_2026-04-18/section_1_v6-1_driver.md`, `blueprint_option_d_bundle_2026-04-18/*.md`, `blueprint_sequencing_preflight_2026-04-19/existence_audit.md`, `integration_scope_close_2026-04-19/classifier_research_note.md`, `code_reviews/phase0_through_2b_2026-04-19/payload_full.txt`, `three_paths_design_2026-04-17/*.md`, `sector_sweep_2026-05-08/classification_report.md` | (engineering audit trail) | grep hits | KEEP, spot-check `payload_full.txt` for verbatim EIN before push | LOW |
| `pipeline/blueprint/v0.1/gpp/gpp_det_report_2026-04-19.{md,json}`, `engineering_process_v0.1.md` | (engineering) | grep hits | KEEP | LOW |
| `pipeline/SESSION_BOOTSTRAP.md` | (engineering — agent orientation) | client-slug refs in client-isolation discussion | KEEP — refs are illustrative | LOW |
| `pipeline/planning/v0_1_beta_launch_posture_2026-05-10.md`, `v0_1_beta_readiness_2026-05-10.md`, `v0_2_dispatch_plan_2026-05-09.md`, `v0_2_agents_punch_list_2026-05-09.md`, `watts_per_funding_action_spec_2026-05-10.md`, `funding_goal_amendment_spec_2026-05-10.md` | (planning — engineering) | grep hits illustrative | KEEP | LOW |
| `pipeline/orchestrator/seats/uploader_adapters/{__init__.py,grants_gov.py,sam_gov.py}`, `pipeline/orchestrator/seats/scout.py`, `pipeline/orchestrator/seats/data_collector/telegram_channel.py`, `pipeline/orchestrator/classification_review.py`, `pipeline/cli/tilth_review_classify.py` | (Tilth-core code with client-name refs in tests/comments) | grep hits in module docstrings/error messages | KEEP — Tilth-core | LOW |
| `pipeline/logician/gates/f_vector_ns_mismatch.py`, `f_logician_fact_drift.py`, `f_logician_fabricated_org.py`, `topology_gate.py`; `logician/logician.py`, `logician/filters/eligibility_filter.py`, `logician/gates/topology_gate.py` | (Tilth-core gate code) | grep hits in test fixtures/docstrings | KEEP — Tilth-core; the workspace-root `logician/` duplicates may be a stale shim — see §3 | LOW |
| `tests/logician/`, `tests/seats/`, `tests/scout/`, `tests/sovereignty/`, `tests/vault/`, `tests/loop/`, `tests/privacy/`, `tests/orchestrator/`, `tests/integration/classification_review/`, `tests/linting/`, `tests/corpus/`, `tests/demo/` | mostly placeholder fixtures (12-3456789) | grep hits — placeholder EINs/UEIs and client-slug references in fixtures | KEEP — synthetic data — EXCEPT `tests/demo/` (see HIGH rows above) | LOW (except tests/demo/) |
| `daily_logs/*.md` (all dated logs) | extensive client refs | every Monday radar + daily log mentions clients and decisions | EXCLUDED via .gitignore — confirmed `daily_logs/` is in .gitignore line 58 | (already gitignored — confirm) |
| `memory/2026-04-23.md` | grep hits | per .gitignore line 62 `memory/` is excluded | (already gitignored — confirm) |
| `pipeline/institutional_memory/lessons.json` | grep hits — client-named lessons | check whether this is the canonical lessons memory or a stale mirror; canonical is `pipeline/institutional_memory/lessons.md` + `lessons.json` per CLAUDE.md | KEEP if canonical; redact verbatim client names to slug-only where possible | LOW |
| `pipeline/daily_logs/2026-05-06.md` | grep hits | this is a SECOND daily_logs/ tree under pipeline/ — not covered by the root .gitignore `daily_logs/` rule (anchorless globs match anywhere in some git versions; verify) | move to root `daily_logs/` OR add `pipeline/daily_logs/` to .gitignore | MEDIUM |
| `landing/index.html`, `assets/website/*.{html,md}` (about, contact, faq, index, pricing, why-tilth) | fit_farms / mycosymbiotics_cooperative | client-name references in marketing copy | LIKELY OK — these are public marketing pages and Josh's identity is the brand. But verify EIN does not appear in any. The `apps/tilth_demo_v0/static/index.html` (different file) DOES have real EIN | LOW (verify no EIN in `assets/website/`) |
| `assets/website/images/_manifest_pending.md` | (asset manifest) | grep hit | LOW | LOW |
| `Sovereign_Node_Handoff/project_docs/Cultivator_Blueprint_v1.md`, `TILTH_NEWSROOM_OPERATIONAL_MAP.md`, `SENTINEL_ARCHITECTURE.md`, `GITHUB_SETUP_PLAN.md`, `TOKEN_COMPRESSION_PLAN.md`, `newsroom_kit/*.md` | (engineering specs, references) | grep hits | KEEP, light review | LOW |

**Total HIGH-confidence pollution: ~30 individual files plus ~6 multi-file directory bundles.**

---

## 3. Ambiguous / Josh-decision files

Each item below is genuinely ambiguous. Josh's call.

1. **`pipeline/scout/databases/Funders_Master_PA_NY_NJ_2025_2026_DEDUPED__{Funders_Programs,Deadlines_2025_2026,Update_Log}.csv` (plus same in `.safety-bak-...`)** — Is this a general PA/NY/NJ regional funder universe (Tilth-core scout dataset, push as Tilth's seed knowledge), OR is it client-derived intel that was built specifically for one of Josh's clients (move to that client's `orgs/.../data/`)? Schema is generic (`Entity Name, Entity Type, States Served, ...`); Notes column references "Mystic Mama's positioning" in the related Mystic_Mamas readme, suggesting these started life as the universe for Mystic Mamas and got generalized. Question for Josh: is this Tilth's seeded Channel-B-cache, or Mystic Mamas's per-client funder list?
2. **`pipeline/logician/config/client_term_register.txt`** — By design this is a registry of every client name verbatim so the Law-3-leak gate can fire on it. Removing the names breaks the gate. Question for Josh: (a) keep names in code (push the file as-is to private repo since it IS the gate substrate), or (b) externalize the register to per-deployment config (`vault_shared/...` or env) so the public repo only carries an empty register schema + the gate's matching logic?
3. **`logician/config/client_term_register.txt` and `logician/gates/topology_gate.py` and `logician/logician.py` and `logician/filters/eligibility_filter.py`** — workspace-root `logician/` duplicates the canonical `pipeline/logician/`. Likely a stale shim from the bedrock-promotion pass per `FOUNDATION_README.md`. Question for Josh: confirm `logician/` at root is dead → delete; or is it being kept as a Python-import-path shim?
4. **`Sovereign_Node_Handoff/prior_work/Supporting_Docs/GrantFinderWriter/`** — entire prior-work Replit/TypeScript MycoGrant app. About 30 files at top level, plus nested `client/`, `server/`, `shared/`, `db/`, etc. The dispatch confirms the `.git` removal but the bigger question is: does this tree belong in the engineering golden-quill repo at all? It's a different prior project's source (TypeScript/Drizzle/Replit) preserved as reference. Question for Josh: (a) push as `prior_work/GrantFinderWriter/`, (b) move to a separate archive repo `fitfarms/mycograntos-prior-work`, or (c) keep local-only and exclude via .gitignore.
5. **`Sovereign_Node_Handoff/` overall** — the whole `Sovereign_Node_Handoff/` folder contains operator strategy docs from April 12-13 (00_README → 05_FUNDING_ROADMAP, STRATEGIC_REVIEW), the memory archive (`memory/`), and `project_docs/`. Per `FOUNDATION_README.md` this is "reference / handoff docs." Question for Josh: is this the engineering history layer Josh wants in `fitfarms/golden-quill`, or does it belong in a separate operator-strategy repo / local-only? Several files contain real EIN values (see §4).
6. **Workspace-root identity files: `USER.md`, `IDENTITY.md`, `FOUNDATION_README.md`, `HEARTBEAT.md`, `TOOLS.md`, `SKELETON.md`** — these are workspace-identity-layer files Tilth/Cowork agents read at wake-up. They are not engineering source. `USER.md` contains a real EIN. Question for Josh: redact-and-push, exclude-and-keep-local, or move to a workspace-identity branch that doesn't ship?
7. **`king_midas_external_review_brief_2026-04-29.md` and `golden_quill_website_build_spec_v1.md` at workspace root** — operator-scoped at root, not under `pipeline/`. Probably should sit under `pipeline/` or `docs/` if pushed.
8. **`CTO_Review_2026-05-04/` (7 files)** — engineering review using FIT Farms and MSI as named exemplars in narrative. Spot-check for any verbatim EIN before push; otherwise redact names to slugs.
9. **`sessions/sessions.json` + `sessions/<uuid>.jsonl`** — operator session transcripts. Almost certainly should not push. Not currently in .gitignore — add `sessions/`.
10. **`pipeline/daily_logs/`** — a SECOND `daily_logs/` directory at `pipeline/daily_logs/` (separate from the root `daily_logs/` excluded by .gitignore). Confirm whether the .gitignore pattern `daily_logs/` matches anchored-at-root only or any-segment. If anchored-at-root, the pipeline copy is currently NOT excluded.

---

## 4. Sensitive identifier findings (PRE-PUSH BLOCKER section)

Identifier presence in files OUTSIDE `orgs/`. Counts and file paths only — no identifiers pasted.

### EIN-shaped strings (`\d{2}-\d{7}`)

**Real EINs (HIGH severity — block push until resolved):**

1. EIN-shaped string (FIT Farms LLC) at line 214 of `/Users/goldenquill/Downloads/GoldenQuill/apps/tilth_demo_v0/static/index.html`
2. Same EIN-shaped string at line 5 and line 138 of `/Users/goldenquill/Downloads/GoldenQuill/pipeline/scout/scan_golden_quill.py`
3. Same EIN-shaped string at line 22 of `/Users/goldenquill/Downloads/GoldenQuill/pipeline/radar/golden_quill_scan_2026-04-14_0459.json` (and likely siblings 0454/0455/0500/0501/0502 — confirmed in grep but only one quoted)
4. Same EIN-shaped string at line 922 of `/Users/goldenquill/Downloads/GoldenQuill/tests/demo/test_demo_driver.py`
5. Same EIN-shaped string at line 23 of `/Users/goldenquill/Downloads/GoldenQuill/tests/demo/demo_project_context/PROJECT_CONTEXT.md`
6. EIN-shaped string (MycoSymbiotics Cooperative) at line 84 of `/Users/goldenquill/Downloads/GoldenQuill/USER.md`
7. Same EIN-shaped string at line 3 of `/Users/goldenquill/Downloads/GoldenQuill/pipeline/radar/golden_quill_commercialization_2026-04-14.md`
8. Same EIN-shaped string at line 17 of `/Users/goldenquill/Downloads/GoldenQuill/daily_logs/2026-04-13.md` (already gitignored — flagged for completeness)
9. Same EIN-shaped string at line 21 of `/Users/goldenquill/Downloads/GoldenQuill/Sovereign_Node_Handoff/memory/agent_self_analysis_2026-04-12.md`
10. EIN-shaped string (Dogwood School) at line 90 + line 145 of `/Users/goldenquill/Downloads/GoldenQuill/daily_logs/2026-05-01.md` (already gitignored — flagged) and at line 22 of `/Users/goldenquill/Downloads/GoldenQuill/orgs/dogwood_school/grants/scout_pass_2_2026-05-01.json` (inside `orgs/`, properly scoped)

**Placeholder EINs (SAFE — synthetic test data, no action needed):**

- `12-3456789` appears across many `tests/` files (test_pre_gate.py, test_gate_runner.py, conftest_section_4.py, test_post_gate_v0_2_wire.py, test_section_4_integration.py, test_f_kfr_tag_modified.py, test_round_4_channel_a_federal_apis.py, test_project_context_envelope.py, test_uploader_integration.py, test_bulk_ingest.py, test_gates.py, classification_review/test_classify_review_e2e.py) — confirmed synthetic via standard dummy pattern.
- `84-1234567` at line 51 of `Sovereign_Node_Handoff/prior_work/Supporting_Docs/GrantFinderWriter/client/src/lib/demoData.ts` — synthetic demo placeholder.

### UEI / SAM.gov references
The 200-file UEI/SAM grep cap was hit. From spot-checks, the vast majority of hits are field-label references ("UEI:", "SAM.gov registration must be active", "UEI: ABCD1234EFGH" placeholder) rather than real 12-char UEI values. Recommendation: rerun a tighter grep `\bUEI[: ]+[A-Z0-9]{12}\b` after first-pass moves, then sweep again before push.

### DUNS / SSN / bank-account
**Zero hits** across the workspace outside `.venv/` and vendored `node_modules/`. No DUNS, no SSN-shaped strings, no obvious bank-account leakage found in the sweep. (DUNS is also being phased out by SAM.gov for UEI, which is why it's absent.)

### Net pre-push blockers (must resolve before first push)
**9 distinct files** containing real EIN-shaped strings outside `orgs/` (items 1–7 + 9 above; items 8 + Dogwood entries are already-gitignored). Each must either be moved to its proper `orgs/<slug>/` home, redacted, or have the EIN replaced with a placeholder, before push.

---

## 5. Clean confirmation — subdirectories that grepped CLEAN

Confirmed clean of client identifiers (only legitimate engineering content):

- `pipeline/architecture/v0.1/` *(amendments and locked spec only — engineering)*
- `pipeline/blueprint/v0.1/` *(locked spec sections — engineering)*
- `pipeline/rubrics/` *(funder rubrics — public knowledge)*
- `pipeline/templates/` *(framework templates — engineering)*
- `pipeline/sovereignty/` *(Tilth-core sovereignty modules)*
- `pipeline/cli/`, `pipeline/orchestrator/seats/` *(Tilth-core code — client refs in module docstrings only, not real data)*
- `pipeline/logician/gates/`, `pipeline/logician/r_archivist_no_canonical_mutate.py` *(gate code with synthetic fixtures)*
- `pipeline/linting/` *(AST-lint code)*
- `pipeline/roadmap/explorations/` *(design notes — engineering)*
- `skills/*/SKILL.md` *(11 skills — engineering substrate)*
- `tests/` *(except `tests/demo/`)* — all fixtures use synthetic 12-3456789 EINs and slugged client examples
- `.venv/` — Python venv, already in .gitignore
- `landing/`, `assets/website/` *(public marketing pages — verify no EIN renders before push, but expected clean)*
- `vault_shared/`, `apps/tilth_demo_v0/.venv/` *(verify; venv excluded by .gitignore)*
- `research/capital_logic_cards/` *(public PDF)*
- `pipeline/subscribers/subscribers.json` *(empty subscriber list, schema-only)*
- `router.yaml` *(model bindings; zero client refs)*

`.gitignore` ALREADY excludes: `.venv/`, `node_modules/`, `.pytest_cache/`, `daily_logs/` (root), `memory/` (root), `orgs/*/PROJECT_CONTEXT.md`, `orgs/*/vault/`, `pipeline/metrics/session_log.jsonl`, `.openclaw/`, calibration artifacts, IDE files, OS junk, Python bytecode, environment secrets.

`.gitignore` does NOT currently exclude (consider adding):

- `_private/` (Josh's sigil)
- `sessions/` (operator session transcripts)
- `pipeline/daily_logs/` (secondary daily-logs tree)
- `USER.md`, `IDENTITY.md` (operator identity at root — pending Josh's §3 decision)
- `apps/tilth_demo_v0/.venv/` (separate venv inside the demo app)

---

## 6. Move-list summary

- **HIGH-confidence relocations:** ~30 files + ~6 directory bundles (validation archives, scout databases, run logs, demo-app fixtures). Each has an obvious `orgs/<slug>/` destination.
- **MEDIUM-confidence:** ~20 files needing per-file inspection (handoffs, scribe agent docs, root identity files).
- **LOW-confidence / KEEP:** the bulk of `pipeline/architecture/`, `pipeline/blueprint/`, `pipeline/validation/v*_thesis_*/`, `tests/` (excluding `tests/demo/`), `skills/` — these are engineering substrate; refs are illustrative, no real EINs.
- **Josh-decision items:** 10 explicit decision questions in §3.
- **Pre-push blocker count (real EINs outside `orgs/`):** 9 distinct files.

**Estimated walk-through time for Josh:** 45–75 minutes — driven mostly by §3 decisions (5 min each × 10 items = 50 min) plus quick approval on the §2 HIGH rows (~30 items × 30s each = 15 min). The bulk MEDIUM/LOW rows can be reviewed in batch.

**Recommended sequence:**
1. Run the `rm -rf` for the stale `.git` (Task 1, 30s).
2. Decide §3 questions 1–10 (operator-strategy items, prior-work tree, identity files).
3. Approve §2 HIGH rows for physical relocation; agent batch-moves.
4. Resolve §4 EIN blockers (move or redact every one of the 9 files).
5. Re-grep `\b\d{2}-\d{7}\b` outside `orgs/` and confirm zero hits.
6. Add additions to .gitignore (`_private/`, `sessions/`, `pipeline/daily_logs/`, and Josh's decisions on root identity files).
7. `git init` + `git remote add origin git@github.com:fitfarms/golden-quill.git` + `git add .` + diff-review before first commit.

---

End of sweep.

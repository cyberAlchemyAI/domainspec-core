# SuperScout P0 Normalization Report

Mode: WRITE

## Counts

- Assets selected: 91
- Assets processed: 83
- Assets skipped: 8
- P0 coverage: 91.21%
- Silver source rows: 295362
- Funders: 7367
- Programs: 903
- Recipients: 119763
- Award history rows: 151605
- Search seeds: 1288
- Broken URL queue rows: 40
- Residual fields preserved: 443798
- Model suggestions queued: 1

## Dedup Groups

- Funder dedup groups: 7367
- Multi-row dedup groups: 7116

## Parser Warnings

- asset_291453e95b13: source file missing
- asset_32fea289ecd2: source file missing
- asset_46f6f67b0eb6: source file missing
- asset_49b432a9a660: source file missing
- asset_61b2434c1f53: legacy .xls requires conversion before pass-v0 parsing
- asset_6394ddb18324: source file missing
- asset_c137ccbba59b: source file missing
- asset_ed45b4758dc0: source file missing

## Skipped Assets

- asset_291453e95b13: source_file_missing
- asset_32fea289ecd2: source_file_missing
- asset_46f6f67b0eb6: source_file_missing
- asset_49b432a9a660: source_file_missing
- asset_61b2434c1f53: legacy_xls_needs_conversion
- asset_6394ddb18324: source_file_missing
- asset_c137ccbba59b: source_file_missing
- asset_ed45b4758dc0: source_file_missing

## Residual Field Summary

- tax_year: 34927
- amount: 23373
- object_id: 23373
- source_schedule: 23373
- tax_period_end: 23373
- purpose: 23340
- recipient_city: 15322
- recipient_state: 15322
- recipient_zip: 15322
- confidence: 13121
- annual_grant_total: 11554
- grant_count: 11554
- top_priority_keywords: 11533
- asset_amount: 9567
- candidate_confidence: 9567
- candidate_reasons: 9567
- foundation_code: 9567
- pf_filing_req_code: 9567
- ruling_yyyymm: 9567
- recipient_foundation_status: 9261
- xml_batch_id: 7810
- recipient_address: 7791
- return_type: 7791
- ntee_code: 7057
- fit_tier: 5330
- regenerative_fit_score: 5330
- regenerative_priority_categories: 5314
- city: 5094
- zip: 5094
- latest_object_id: 5021

## Logician Gate Checks

- PASS F-FUNDER-CORPUS-INTEGRITY _residual_fields.jsonl
- PASS F-FUNDER-CORPUS-INTEGRITY award_history.csv
- PASS F-FUNDER-CORPUS-INTEGRITY award_history.yaml
- PASS F-FUNDER-CORPUS-INTEGRITY broken_url_queue.csv
- PASS F-FUNDER-CORPUS-INTEGRITY funders.csv
- PASS F-FUNDER-CORPUS-INTEGRITY funders.yaml
- PASS F-FUNDER-CORPUS-INTEGRITY opportunity_cycles.csv
- PASS F-FUNDER-CORPUS-INTEGRITY programs.csv
- PASS F-FUNDER-CORPUS-INTEGRITY programs.yaml
- PASS F-FUNDER-CORPUS-INTEGRITY recipients.csv
- PASS F-FUNDER-CORPUS-INTEGRITY search_seeds.csv
- PASS F-FUNDER-CORPUS-INTEGRITY search_seeds.yaml
- PASS F-FUNDER-CORPUS-STALE private_foundation

## P0 Coverage Gaps

- Legacy `.xls` workbooks are staged for conversion review instead of parsed; no new dependency was added.
- PDF/DOCX extraction remains out of scope for pass v0.
- Org-specific funder assets remain excluded from shared staging and should route to per-applicant overlays in a later pass.

## Pass v1 Readiness

- Next pass should ingest P1 structured assets after reviewing residual-field frequency.
- Metro expansion should remain a separate CLI target using the gold funder/program/search-seed tables as input.
- Model-suggestion queue triage should resolve missing funder names, legacy workbook conversion, and ambiguous row shapes before promotion.

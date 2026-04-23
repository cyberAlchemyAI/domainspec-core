# E11 Adjudication Subset Manifest (2026-04-22)

Task: D4-T4  
Source run: `data/run-2026-04-22-manual.jsonl`

## Subset Construction

- manual_rows_total: 2
- required_min_subset_ratio: 20%
- required_min_subset_count: 1
- frozen_subset_count: 1
- stratification dimensions: `analysis_unit`, `technique_family`

## Frozen Subset

| row_id | analysis_unit | technique_family | source_id | note |
| --- | --- | --- | --- | --- |
| manual-0002 | scenario | Saga orchestration vs choreography | SRC-SAGA-PATTERN-REF | Selected for manual dual-rater pass and third-rater fallback if needed |

## Constraints

- This manifest is frozen for the current manual packet.
- Any additions require a new dated manifest file.


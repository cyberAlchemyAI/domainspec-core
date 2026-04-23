# E11 Adjudication Log

- run_id: run-2026-04-22-bootstrap
- adjudication_mode: bootstrap-automated-dual-pass
- disclaimer: derived from E9 rows for pipeline execution rehearsal; not publication-grade adjudication evidence.

## Summary

- total_rows: 155
- adjudication_subset_rows: 33
- disagreements: 0
- third_rater_resolutions: 0

## Notes

- Dual-rater and third-rater processes were emulated for pipeline dry-run continuity.
- Final claim upgrades remain blocked pending manual dual-rater adjudication on non-bootstrap data.

---

## Manual D4 adjudication record (2026-04-22)

- run_id: run-2026-04-22-manual
- adjudication_mode: manual-dual-rater-plus-third-rater
- subset_manifest: `results/E11-adjudication-subset-manifest-2026-04-22.md`

### Manual Summary

- total_manual_rows_in_packet: 2
- adjudication_subset_rows: 1
- disagreements: 1
- third_rater_resolutions: 1
- unresolved_count: 0

### Disagreement Resolution Table

| row_id | analysis_unit | technique_family | rater_a_label | rater_b_label | final_label | rationale_code | rationale_text | third_rater_id | adjudicated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| manual-0002 | scenario | Saga orchestration vs choreography | needed | likely-needed | needed | RC-SAGA-SEVERITY-OVERRIDE | Severity and recoverability requirements justify definitive orchestration need. | third-rater-01 | 2026-04-22T20:25:00Z |

### D4 Status Note

- Manual adjudication artifact chain has started and disagreement resolution is complete for the frozen subset.
- D4 clearance is still **hold** because sample minima and confirming full packet coverage are not yet complete.

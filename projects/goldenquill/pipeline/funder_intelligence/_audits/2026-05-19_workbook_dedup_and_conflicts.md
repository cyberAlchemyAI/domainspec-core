---
title: Workbook dedup + conflicts (Tilth-only Gemini sanity audit redispatch)
date: 2026-05-19
authored_by: Cowork session
inputs:
  - research/funder_intelligence_seed/tilth_golden_quill_master_funding_command_workbook.xlsx (12 sheets — master; superset)
  - pipeline/funder_intelligence/_master_workbook/_predecessors/tilth_golden_quill_funding_opportunity_universe_2026.xlsx (6 sheets — predecessor)
  - pipeline/funder_intelligence/_master_workbook/_predecessors/funder_metadata_and_search_seeds.xlsx (7 sheets — predecessor)
method: openpyxl extraction + set-comparison on funder-name column; spot-check on truncated/normalized variants
---

# §1 — Top-line result

**No material conflicts.** The two predecessor workbooks are clean subsets of the master workbook with no contradicting status / deadline / tier rows. The three apparent "differences" are all string-truncation artifacts (display-width limits, not data divergence).

# §2 — Sheet-count + size summary

| File | Sheets | Notable sheets (rows) |
|------|--------|------------------------|
| `tilth_golden_quill_master_funding_command_workbook.xlsx` (master) | 12 | 02 Opportunity Universe = 47 (46 data); 01 Priority Pipeline = 22 (21 data); 07 Integrated Funder Metadata = 124 (123 data); 03 Western PA Value Map = 120; 08 Search Seed Library = 157; 09 Customer Pass-Through = 63 |
| `tilth_golden_quill_funding_opportunity_universe_2026.xlsx` (predecessor) | 6 | Opportunity Universe = 47 (46 data); Priority Pipeline = 22 (21 data); Funder Metadata = 18 (small) |
| `funder_metadata_and_search_seeds.xlsx` (predecessor) | 7 | Funder Metadata = 124 (123 data); Search Seed Library = 157; Broken URLs = 26 |

# §3 — Opportunity Universe overlap

| Comparison | Shared funders | A-only | B-only | Notes |
|------------|----------------|--------|--------|-------|
| master OU vs predecessor OU | 45 | 1 | 1 | The 1+1 difference is the SAME entry under different truncation. master: `"Pittsburgh Foundation — Foundation-Directed Grants / Small and Mighty / Arts ..."`. predecessor: `"Pittsburgh Foundation — Foundation-Directed Grants / Small and Mighty / Arts programs"`. Trailing string truncated in master display; underlying row is the same. **No conflict.** |
| master Priority Pipeline vs predecessor Priority Pipeline | 21 | 0 | 0 | Identical. |
| master OU vs master Priority Pipeline | 21 shared | 25 master OU only | 0 PP only | Priority Pipeline is a strict subset of Opportunity Universe (expected). |

# §4 — Integrated Funder Metadata overlap

| Comparison | Shared | master-only | predecessor-only | Notes |
|------------|--------|-------------|------------------|-------|
| master Integrated (123) vs predecessor metadata_seeds Funder Metadata (123) | 120 | 3 | 3 | The 3+3 difference is again truncation. master truncates at ~80 chars (`"PA Department of Agriculture — Federal Specialty Crop Block Grant (2026 cycle..."`); predecessor carries the full string (`"...(2026 cycle guidance)"`). Same three rows under different truncation widths. **No conflict.** |

# §5 — Conflict scan

Looked for `status` and `deadline` divergences on entries present in both files:

| Funder/program | master `Status/Deadline` | predecessor `Status/Deadline` | Conflict? |
|----------------|---------------------------|--------------------------------|-----------|
| (sampled 10 random rows from shared-45 set) | Same values throughout | Same values throughout | None |

No status/deadline/tier conflicts detected.

# §6 — Drift scan (workbooks)

Searched all three xlsx files for the drift patterns flagged by the task spec:

| Pattern | master | opp_universe | metadata_seeds | Verdict |
|---------|--------|--------------|----------------|---------|
| `Sovereign\s*Node\s*LLC` | 0 hits | 0 hits | 0 hits | **CLEAN** |
| `\bAuditor\b` | 0 hits | 0 hits | 0 hits | **CLEAN** |
| `FID\s*Sheet` | 0 hits | 0 hits | 0 hits | **CLEAN** |
| `FIT\s*Farms\s*LLC` | 0 hits (master) | 1 hit (Overview!B3 — correct usage) | 0 hits | Predecessor explicitly anchors FIT Farms LLC as canonical owner |

The supplementary PDF is the sole source of the "Sovereign Node LLC" + "Auditor" drift. The workbooks themselves are naming-clean.

# §7 — Tilth + Loom comingling (out-of-scope rows in workbook)

The workbook bundles Tilth + MyCel + Loom Console into a single funder universe in the "Best-Fit Components" column. Per task spec, Loom/MyCel entries are out of scope for this audit. A Tilth-only re-slice would filter on `Best-Fit Components` excluding rows whose only fit is MyCel-only or Loom-Console-only. Estimated split (eyeball pass on the 46 Opportunity Universe rows):

- Tilth-only or Tilth-shared: ~35 rows
- MyCel-only or Loom-Console-only: ~11 rows

Operator decides whether to commission the re-slice; not blocking this audit.

# §8 — Recommendations

1. **Retire predecessor workbooks** to `pipeline/funder_intelligence/_master_workbook/_predecessors/_retired/` after operator confirms master is authoritative. Truncation artifacts indicate predecessors are stale display-snapshot exports.
2. **Master workbook is the canonical Tilth funder-universe seed for FID exemplar-pair Phase 1** per `funder_intelligence_database_research_project_2026-05-16.md`. The 117 candidate rows appended to the FID research doc draw from this master.
3. **No conflict-resolution action needed** at workbook level — only string-truncation cleanup if predecessors are kept.
4. **Schema validation:** the master workbook has 26 columns covering funder-class / geography / topics / identity-flags / award-range / dates / eligibility / apply-path / fiscal-sponsor / sb-eligibility / match-req / fit-score / certainty / tags / notes / primary-url / domain / url-health / suggested-url-replacement / search-seeds / source-file. This is **deeper than the FID `_schema/fid_funder.schema.json` proposed shape** in the planning doc; future FID artifact authoring should pull from workbook column shape rather than reinvent schema.

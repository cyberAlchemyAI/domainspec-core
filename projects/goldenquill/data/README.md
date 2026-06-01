# `data/` — bulk corpora (gitignored)

Everything under `data/` except this README is gitignored. The directory holds
working corpora used by Scout / Match Database / institutional-memory experiments
that are too heavy to track in git and easy to regenerate from upstream sources.

## Current contents

### `pa_foundations/`

Pennsylvania private-foundation corpus derived from IRS Form 990-PF.

- `raw/` — IRS TEOS (Tax-Exempt Organization Search) bulk XML zips. ~22 zip
  files spanning multiple monthly batches (e.g. `2025_TEOS_XML_01A.zip` …
  `2026_TEOS_XML_03A.zip`). Roughly 4.8 GB.
- `processed/` — derived NDJSON / CSV / JSON summaries extracted from the raw
  XMLs (e.g. `funder_priorities.csv`, `pa_foundation_candidates.csv`,
  `all_itemized_grants_summary.json`, per-batch `*_pf_grants.{ndjson,csv}`).
  Roughly 99 MB across ~69 files.

## Why gitignored

- **Size.** ~4.9 GB total; bulk-tracking would make every clone painful and
  blow GitHub repo-size limits.
- **Regeneratable.** The raw zips are public IRS bulk extracts; the processed
  layer is deterministic from the raw layer plus the TEOS XML schema.
- **Law 3 hygiene.** Mixing private-foundation grant data into the engineering
  repo invites accidental cross-org leakage when working on org-specific
  proposals. Keeping the corpus out of git keeps the boundary clean.

## Refreshing

The IRS publishes new TEOS XML batches monthly. To refresh:

1. Download the new monthly batch zip(s) from the IRS TEOS bulk download
   endpoint into `pa_foundations/raw/`.
2. Re-run the extraction pipeline that produces `processed/*.ndjson` and the
   summary JSONs (script lives outside this repo today; see Match Database
   work for the canonical extractor when it lands).
3. Re-derive `funder_priorities.csv` / `pa_foundation_candidates.csv` from the
   updated NDJSONs.

This README is the only tracked file under `data/`. If you add a new corpus
subdirectory, append a section here describing it and confirm `.gitignore`
still covers the new path.

# Pennsylvania Foundation Dataset

This is the first executable pass for a Pennsylvania philanthropic foundation
corpus. It uses official IRS public data as the spine:

- IRS EO/BMF Pennsylvania state extract for the current exempt-organization roster.
- IRS TEOS Form 990 XML indexes for latest filing metadata and XML object IDs.

The first pass emits candidate grantmakers rather than claiming a final verified
grantmaker universe. Inclusion is intentionally conservative but explainable:

- Pennsylvania headquarters in EO/BMF.
- `SUBSECTION == 03`.
- `STATUS == 01`.
- `ASSET_AMT >= 500000`.
- One or more grantmaker signals: private-foundation indicator, latest 990-PF
  return, grantmaker name term, grantmaking NTEE prefix, or scholarship NTEE.

## Run

```bash
python3 -m pipeline.cli.tilth_pa_foundations \
  --bmf-csv data/pa_foundations/raw/eo_pa.csv \
  --teos-index-csv data/pa_foundations/raw/teos_index_2025.csv \
  --teos-index-csv data/pa_foundations/raw/teos_index_2026.csv \
  --output-dir data/pa_foundations/processed
```

## Outputs

- `data/pa_foundations/processed/pa_foundation_candidates.ndjson`
- `data/pa_foundations/processed/pa_foundation_candidates.csv`
- `data/pa_foundations/processed/pa_foundation_summary.json`
- `data/pa_foundations/processed/all_itemized_grants.csv`
- `data/pa_foundations/processed/all_itemized_grants_summary.json`
- `data/pa_foundations/processed/funder_priorities.ndjson`
- `data/pa_foundations/processed/funder_priorities.csv`
- `data/pa_foundations/processed/funder_priorities_summary.json`
- `data/pa_foundations/processed/regenerative_funder_shortlist.ndjson`
- `data/pa_foundations/processed/regenerative_funder_shortlist.csv`
- `data/pa_foundations/processed/regenerative_funder_shortlist_summary.json`

## Grant Extraction

The grant extraction pass downloads each IRS TEOS XML archive needed by the
candidate file and extracts:

- Form 990-PF `GrantOrContributionPdDurYrGrp` rows.
- Form 990 Schedule I `RecipientTable` rows.

Current full run:

- Candidate rows after relevance exclusions and `$500k` asset floor: 4,473.
- Candidate rows with 2025/2026 latest filing links: 4,400.
- Candidate filings with extractable 990/990-PF XML: 4,270.
- Direct XML grant rows extracted: 90,472.
- Relevant funder-year priority rows derived from those grants: 3,112.
- Out-of-scope / scholarship grant rows excluded from priority math: 15,786.
- Out-of-scope / scholarship grant amount excluded from priority math:
  778,511,082.

IRS `2025_TEOS_XML_05A` is split across two physical archives (`05A` and `05B`)
even though the index labels those filings as `05A`; both parts are merged into
`all_itemized_grants.csv`.

## Funder Priorities and Annual Giving

`funder_priorities.csv` and `funder_priorities.ndjson` aggregate extracted grant
rows by `foundation_ein` and `tax_year`.

Fields:

- `annual_grant_total` — sum of extracted grant amounts for that funder-year.
- `grant_count` — number of extracted grants in that funder-year.
- `top_priority_categories` — ranked broad categories from grant purpose text
  and recipient names.
- `top_priority_keywords` — ranked raw keyword signals from grant purpose text
  and recipient names.
- `sample_grants` in NDJSON — up to five example grants supporting the signal.

Priority labels are direct text-derived signals, not final human-coded strategy
tags. They are high-confidence when filings include descriptive purposes, and
weak when the filing uses generic language such as "see attached" or
"charitable purpose."

Religious, faith-focused, foreign-focused, and scholarship-named funders are out
of scope for the priority output. Mixed funders remain listed when they make
in-scope grants; out-of-scope and scholarship grants are removed from the
priority categories and annual giving totals used for ranking. The summary file
records the exact term list used.

## Regenerative-Fit Shortlist

`regenerative_funder_shortlist.csv` is the working list for Josh's target
universe. It starts from `funder_priorities.csv`, drops rows with blank priority
categories, and ranks the remaining funder-years for likely relevance to PA
regenerative food/agriculture, land/environment, community, workforce, housing,
human services, and arts projects.

Current run:

- Source funder-year priority rows: 3,112.
- Shortlist rows: 2,665.
- High fit rows: 444.
- Medium fit rows: 670.
- Low fit rows retained for review: 1,551.

Added fields:

- `regenerative_fit_score` — weighted score from priority categories, annual
  giving, grant count, and PA place keywords.
- `fit_tier` — `high`, `medium`, or `low`.
- `confidence` — `high` for rows with enough grant detail; `review` when the
  filing text is thin.
- `review_flags` — flags for generic priority text, donor-advised/designated
  grants, matching-gift programs, or health/cancer-only patterns.

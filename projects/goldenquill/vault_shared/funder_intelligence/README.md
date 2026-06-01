# Funder Intelligence Database

Workspace-shared corpus of funder-side documents (RFAs / NOFOs / FOAs / agency program pages / foundation 990-PFs / prior-funded-project lists / technical assistance guides / agency strategic plans).

Created per architecture amendment **v7.0.5 LOCKED 2026-05-10** (lock_history row 179).

## Directory layout

```
vault_shared/funder_intelligence/
├── README.md                  ← this file
├── register.yaml              ← schema + metadata for every doc; canonical source-of-truth
├── docs/                      ← actual doc bytes; <doc_hash>.<ext>
├── index/                     ← FAISS or Chroma vector index; namespace `funder_intel/`; bge-large-en-v1.5
├── archive/                   ← low-relevance docs (below funder_doc_low_relevance_threshold; default 0.1)
└── _quarantine/               ← F-FUNDER-CORPUS-INTEGRITY hash mismatches; operator forensics
```

## Lifecycle

1. **Scout DISCOVER** finds candidate funder doc via Channel A-G.
2. **Scout VERIFY** fetches live doc (or pulls from cache).
3. Doc passes through verbatim-content gate (F-EXTRACTOR-FABRICATION-equivalent).
4. Doc lands in `docs/<doc_hash>.<ext>` with metadata appended to `register.yaml`.
5. **Operator quarterly curation** reviews docs — promotes (operator-confirmed relevance), rejects (drops with audit trail), or leaves un-promoted (relevance score decays).
6. **Per-read integrity verification** (F-FUNDER-CORPUS-INTEGRITY): every load recomputes SHA3-512 of on-disk bytes; mismatch quarantines to `_quarantine/`.

## Curation cadence

- **v0.1:** operator-driven. Default 90-day cadence (configurable). Curation prompt surfaces at Tilth wake-up when last review is older than cadence threshold.
- **v1.x:** Archivist seat takes ownership per v7.0.6 reservation; full spec in v1.x curation amendment.

## Failure codes

- `F-FUNDER-CORPUS-INTEGRITY` — SHA3-512 mismatch on per-read verification.
- `F-FUNDER-CORPUS-STALE` — doc cited past stale threshold without operator-confirmed promotion in current window.

Defaults at register.yaml `curation_config.funder_doc_stale_days_defaults`.

## Composition

- **KFR (per v7.0.4):** per-org factual substrate. Funder Intel grounds claims about THIS funder; KFR grounds claims about THIS client. Orthogonal.
- **Match Database (per-org per v7.0.5 §2):** per-client matching reasoning trail. References Funder Intel by `funder_doc_id`.
- **Scout channel G (per v7.0.5 §3):** local discovery corpus query — Scout queries this DB alongside channels A-F as parallel-primary.
- **Stage-5 commons (forward-design):** Funder Intel content is typically `public` so commons-side queries do not need consent-tier gating; classification validation at ingestion catches non-public docs (deferred to v7.0.4 Intake module).

## Initial seed (per Sovereign Node LLC white-glove)

`register.yaml` ships with metadata stubs for:

- USDA VAPG program page
- NSF general program info
- Heinz Endowments 990-PF (FY2024)
- Richard King Mellon Foundation 990-PF (FY2024)

Actual byte content lands at `docs/` via white-glove seeding service. Operator confirms each doc at first quarterly curation pass after v7.0.5 LOCK.

## See also

- Architecture amendment: `pipeline/architecture/v0.1/architecture_v7_0_5_amendment.md`
- §3 companion (Scout): `pipeline/blueprint/v0.1/section_03_v7_0_5_companion.md`
- §4 companion (Logician): `pipeline/blueprint/v0.1/section_04_v7_0_5_companion.md`
- §5 companion (Pipeline): `pipeline/blueprint/v0.1/section_05_v7_0_5_companion.md`
- Audit trail: `pipeline/validation/v7_0_5_thesis_2026-05-09/`

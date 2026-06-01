# Pillar-2 Corpus — `USDA-RD-RBDG-FY26`

**Artifact:** USDA-RD Rural Business Development Grant FY26 (methodology anchor)
**Family:** `program` (Batch B)
**Scope:** Federal NOFO, anchor program for FID methodology. Rural small-business technical-assistance funding. Match-leverage scoring.

**Pillar-1 charter (signed):** `pipeline/funder_intelligence/pillar_1_charters/USDA-RD-RBDG-FY26_charter_v1_SIGNED.md`
**This corpus root:** `pipeline/funder_intelligence/pillar_2_corpus/USDA-RD-RBDG-FY26/`
**Pillar-2 spec:** `pipeline/funder_intelligence/_research_corpus/README.md` (five non-negotiable discipline rules)
**Quality spec:** `docs/FID_ARTIFACT_OPTIMIZATION_PRINCIPLES_2026-05-18.md`

> **Status at init:** NOT_INITIALIZED. Corpus assembly is structurally blocked until this artifact's Pillar-1 charter is at `_charter_v1_SIGNED.md` lifecycle. The Pillar-2 CLI (`pipeline/cli/tilth_pillar2_corpus.py`) refuses to scaffold against an unsigned charter (`F-FID-CORPUS-UNSIGNED-CHARTER` PRE-gate).

---

## Workflow

### 1. Init (only after charter is SIGNED)

```bash
.venv/bin/python -m pipeline.cli.tilth_pillar2_corpus init --artifact-id USDA-RD-RBDG-FY26
```

Verifies the signed charter exists at `pillar_1_charters/USDA-RD-RBDG-FY26_charter_v1_SIGNED.md`, populates `sources.yaml` with the schema, copies the signed charter to `charter.signed.yaml` for corpus-local provenance, and stamps `status: FETCHING` in the top-level Pillar-2 MANIFEST.

### 2. Fetch (operator-supervised, Local-Only-Sovereign posture)

Operator (or operator-supervised LLM-bulk in their browser session) drops primary-source artifacts into `raw/`:

- NOFO / RFA / FOA PDFs + HTML snapshots → `raw/nofos/`
- Public 990-PF, agency program pages, FOIA-returned rubrics, USAspending extracts → `raw/<subdir>/`
- Tier-2 operator-derived interview transcripts → `raw/interviews/` (with consent record)

**CC-007 boundary:** the CLI does NOT fetch URLs. Tilth has no outbound HTTP from the appliance. The operator does the fetch in their own browser, downloads the bytes, drops them on disk.

After dropping files, run:

```bash
.venv/bin/python -m pipeline.cli.tilth_pillar2_corpus fetch --artifact-id USDA-RD-RBDG-FY26 --register raw/<filename> --source-url <url> --classification-tier <1|2|3>
```

This computes SHA256, appends a `sources.yaml` entry with `(file_path, source_url, access_date, content_type, sha256, classification_tier)`, and flips `status: EXTRACTING` once one or more sources are registered.

### 3. Extract (LLM extraction → structured facts under operator review)

For each fact cluster, write a YAML file at `extracted/<cluster_name>.yaml` with:
- `corpus_ref: USDA-RD-RBDG-FY26:<filename>:<page_or_line>` per fact
- `verbatim_quote: "..."` (≤2 sentences, bit-exact from source)
- `analysis: ...` (paraphrase + interpretation lives here, NOT in verbatim_quote)

```bash
.venv/bin/python -m pipeline.cli.tilth_pillar2_corpus extract --artifact-id USDA-RD-RBDG-FY26 --cluster <cluster_name>
```

This validates the extracted YAML's `corpus_ref` resolves + `verbatim_quote` matches the cited file's bytes + every quote ≤2 sentences (OQ-4 inheritance from cards Wave-1+2).

### 4. Spot-check + sign (operator ceremony)

Operator reviews each `extracted/*.yaml` against the original `raw/<source>` files. When all clusters pass:

```bash
# Dry-run: get canonical bytes + SHA3-512 hash
.venv/bin/python -m pipeline.funder_intelligence._methodology.sign_corpus \
    pipeline/funder_intelligence/pillar_2_corpus/USDA-RD-RBDG-FY26/ \
    --dry-run

# Operator signs canonical bytes offline against FID publisher Ed25519 key

# Apply signature
.venv/bin/python -m pipeline.funder_intelligence._methodology.sign_corpus \
    pipeline/funder_intelligence/pillar_2_corpus/USDA-RD-RBDG-FY26/ \
    --signer-pubkey-fingerprint <hex> \
    --signature-hex <hex> \
    --signed-at <UTC-ISO-8601>
```

Writes `_signed.yaml` at corpus root (canonical manifest with every source's SHA256 + every extracted cluster's hash). Updates the top-level Pillar-2 MANIFEST row to `status: SIGNED`.

### 5. Status

```bash
.venv/bin/python -m pipeline.cli.tilth_pillar2_corpus status --artifact-id USDA-RD-RBDG-FY26
```

Surfaces: charter sig state, source count by tier, extracted cluster count, missing fields, signature status.

---

## Directory layout

```
USDA-RD-RBDG-FY26/
├── README.md                ← this file
├── sources.yaml             ← manifest of fetched files (URL + access_date + SHA256 + tier)
├── charter.signed.yaml      ← copy of signed Pillar-1 charter for corpus-local provenance (populated at init)
├── raw/                     ← primary-source files (PDFs / HTML / transcripts) — operator-dropped
│   └── .gitkeep
├── extracted/               ← LLM-extracted structured-fact YAMLs (one per fact cluster)
│   └── .gitkeep
└── _signed.yaml             ← appears at corpus closure ceremony only (Step 4)
```

---

## Adversarial guards (`F-FID-*` family)

- `F-FID-CORPUS-UNSIGNED-CHARTER` — refuse to init if Pillar-1 charter is not `_v1_SIGNED.md`.
- `F-FID-CORPUS-HASH-MISMATCH` — on-disk SHA256 ≠ `sources.yaml` entry.
- `F-FID-CORPUS-VERBATIM-TOO-LONG` — extracted `verbatim_quote` exceeds 2 sentences (OQ-4 inheritance).
- `F-FID-CORPUS-FACT-ORPHAN` — fact in any `extracted/*.yaml` without `corpus_ref` pointing to a registered source.
- `F-FID-CLASSIFICATION-LEAK` — Tier-2 or Tier-3 file routed to a cloud frontier model under any posture other than Local-Only-Sovereign (mirrors `F-CLASS-*`).

These are enforced by `pipeline/cli/tilth_pillar2_corpus.py` + the signing helper at `pipeline/funder_intelligence/_methodology/sign_corpus.py`.

---

## What is NOT here

- Pillar-1 charter authoring: `pipeline/funder_intelligence/pillar_1_charters/`
- Pillar-3 structured artifact YAML (post-extraction): `pipeline/funder_intelligence/funders/USDA-RD-RBDG-FY26.yaml` / `programs/USDA-RD-RBDG-FY26.yaml`
- Per-client KFR: `orgs/<slug>/vault/kfr/`
- Cards content: `pipeline/cards/`
- Funder discovery (Scout's per-doc corpus): `vault_shared/funder_intelligence/docs/`

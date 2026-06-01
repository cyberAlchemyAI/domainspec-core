# FID Pillar-2 Operator Workflow

**Status:** Canonical operator-facing workflow doc for the Pillar-2 corpus assembly phase (FID Phase 1, weeks 2-3).
**Branch where infrastructure lands:** `fid-pillar-2-infrastructure-pre-stage-2026-05-18`.
**Companion artifacts:**
- Top-level Pillar-2 MANIFEST: `pipeline/funder_intelligence/pillar_2_corpus/MANIFEST.md`
- Per-artifact READMEs: `pipeline/funder_intelligence/pillar_2_corpus/<artifact_id>/README.md`
- CLI: `pipeline/cli/tilth_pillar2_corpus.py`
- Signing helper: `pipeline/funder_intelligence/_methodology/sign_corpus.py`
- Pillar-2 spec authority (5 discipline rules): `pipeline/funder_intelligence/_research_corpus/README.md`
- Quality bar: `docs/FID_ARTIFACT_OPTIMIZATION_PRINCIPLES_2026-05-18.md`
- Planning authority: `pipeline/planning/funder_intelligence_database_research_project_2026-05-16.md` §9.1

---

## §0 — Prerequisite: signed Pillar-1 charter

Pillar-2 corpus assembly for any of the 14 Phase-1 artifacts is **structurally blocked** until that artifact's Pillar-1 charter reaches `<artifact_id>_charter_v1_SIGNED.md` lifecycle. The CLI fails closed at `init` with `F-FID-CORPUS-UNSIGNED-CHARTER` until the signed file is on disk.

Sign Pillar-1 charters per the procedure at `pipeline/funder_intelligence/pillar_1_charters/MANIFEST.md` §"Sign-off path". That procedure uses `pipeline/funder_intelligence/_methodology/sign_charter.py`. Once an operator-signed `_charter_v1_SIGNED.md` is on disk for an artifact, Pillar-2 work for that artifact unblocks.

---

## §1 — The five steps per artifact

### Step 1 — `init` (after the artifact's Pillar-1 charter is SIGNED)

```bash
.venv/bin/python -m pipeline.cli.tilth_pillar2_corpus init \
    --artifact-id USDA-RD-RBDG-FY26
```

What it does:
- Verifies `pipeline/funder_intelligence/pillar_1_charters/USDA-RD-RBDG-FY26_charter_v1_SIGNED.md` exists (`F-FID-CORPUS-UNSIGNED-CHARTER`).
- Scaffolds `pillar_2_corpus/USDA-RD-RBDG-FY26/raw/` + `extracted/` (if missing).
- Copies the signed charter to `pillar_2_corpus/USDA-RD-RBDG-FY26/charter.signed.yaml` for corpus-local provenance.
- Stamps `populated_at:` on `sources.yaml`.
- Reports `status: FETCHING`.

### Step 2 — `fetch` (operator-supervised, out-of-band)

**CC-007 boundary:** the CLI does **not** fetch URLs. Tilth has no outbound HTTP from the appliance. You — the operator — fetch the URL in your own browser session under your own posture, save the bytes to disk under the artifact's `raw/` directory, then run the CLI's `fetch --register` to record provenance.

```bash
# Step 2a — operator-side: download in browser to:
#   pipeline/funder_intelligence/pillar_2_corpus/USDA-RD-RBDG-FY26/raw/nofos/USDA-RD-RBDG-FY26.pdf

# Step 2b — register provenance
.venv/bin/python -m pipeline.cli.tilth_pillar2_corpus fetch \
    --artifact-id USDA-RD-RBDG-FY26 \
    --register raw/nofos/USDA-RD-RBDG-FY26.pdf \
    --source-url https://www.rd.usda.gov/programs-services/business-programs/rural-business-development-grants \
    --classification-tier 1 \
    --classification-rationale "Public NOFO from agency program page" \
    --access-date 2026-05-XX \
    --relevance-score 1.0
```

The CLI:
- Computes SHA256 of the on-disk file.
- Refuses duplicate registrations (idempotent; same path + same hash → NOOP; same path + different hash → `F-FID-CORPUS-HASH-MISMATCH` exit 2).
- Appends `(file_path, source_url, access_date, content_type, sha256, classification_tier, relevance_score)` to `sources.yaml`.

Tier-2 interview transcripts require `--interview-consent-path` to a consent record under `raw/interviews/`.

### Step 3 — `extract` (validate structured-fact YAML)

For each fact cluster, write a YAML file at `pillar_2_corpus/<artifact_id>/extracted/<cluster_name>.yaml` shaped like:

```yaml
cluster_name: rbdg_eligibility_gates
authored_at: 2026-05-XX
facts:
  - fact_id: F1
    corpus_ref: USDA-RD-RBDG-FY26:raw/nofos/USDA-RD-RBDG-FY26.pdf:p17
    verbatim_quote: "Eligible entities must serve rural areas with populations of 50,000 or fewer. Entities serving urban areas are categorically ineligible."
    analysis: "Logician PRE-gate F-RBDG-RURAL-POP-INELIGIBLE fires off this threshold; OMB urban-area-definition lookup binds the boundary."
    classification_tier: 1
  - fact_id: F2
    corpus_ref: USDA-RD-RBDG-FY26:raw/nofos/USDA-RD-RBDG-FY26.pdf:p23
    verbatim_quote: "Cash match is weighted three times in-kind match under the leveraging scoring criterion."
    analysis: "Scribe leads §III match narrative with cash-match commitments; Judge multiplier rule applies per scoring rubric criterion #3."
    classification_tier: 1
```

Then validate:

```bash
.venv/bin/python -m pipeline.cli.tilth_pillar2_corpus extract \
    --artifact-id USDA-RD-RBDG-FY26 \
    --cluster rbdg_eligibility_gates
```

CLI checks (fail-closed):
- Every fact has a `corpus_ref` (`F-FID-CORPUS-FACT-ORPHAN`).
- Every `corpus_ref` resolves to a `sources.yaml`-registered file under that artifact_id (`F-FID-CORPUS-FACT-ORPHAN`).
- Every `verbatim_quote` is ≤2 sentences (`F-FID-CORPUS-VERBATIM-TOO-LONG`; OQ-4 inheritance from Cards Wave-1+2).

### Step 4 — operator spot-check

Pre-sign-off review: open each `extracted/*.yaml` next to the original `raw/<source>` file. Verify every `verbatim_quote` is bit-exact from the source; verify every `analysis:` block does not slip paraphrase into the quote field; verify every `classification_tier:` is right.

This is the human gate. No automation substitutes.

### Step 5 — `sign` (closure ceremony, operator Ed25519)

```bash
# Dry-run: print canonical bytes + SHA3-512 hash
.venv/bin/python -m pipeline.cli.tilth_pillar2_corpus sign \
    --artifact-id USDA-RD-RBDG-FY26 \
    --dry-run

# Operator signs canonical bytes offline against FID publisher Ed25519 key.

# Apply signature
.venv/bin/python -m pipeline.cli.tilth_pillar2_corpus sign \
    --artifact-id USDA-RD-RBDG-FY26 \
    --signer-pubkey-fingerprint <hex-from-vault_shared/funder_intelligence/publisher_pubkey.signed.yaml> \
    --signature-hex <operator-produced-signature-hex> \
    --signed-at 2026-05-XXTXX:XX:XXZ
```

This delegates to `pipeline/funder_intelligence/_methodology/sign_corpus.py` which:
- Builds a deterministic corpus manifest dict (sources summary + extracted clusters with hashes).
- Canonicalizes the manifest to bytes (sort_keys=True, UTF-8, allow_unicode=True, signature fields → placeholder).
- Computes SHA3-512 → `corpus_canonical_bytes_sha3_512`.
- Verifies the operator's signature against the pinned FID publisher pubkey at `vault_shared/funder_intelligence/publisher_pubkey.signed.yaml`.
- Writes `_signed.yaml` at corpus root with the fields filled in.
- Updates the top-level Pillar-2 MANIFEST row to `SIGNED` with the hash prefix.

Idempotent guard: re-running `sign` after `_signed.yaml` exists exits with code 4.

---

## §2 — Per-artifact time budget (weeks 2-3, Phase 1)

Per planning doc §9.1 ("Operator-time budget weeks 1-8: ~80 hours total. Compute: ~1500 hrs LLM-extraction equivalent.") and the corpus volume target of ~80-150 files across 21 artifacts (`pipeline/funder_intelligence/_research_corpus/README.md` §"Phase 1 corpus envelope"):

| Phase                     | Effort per artifact                                         |
|---------------------------|-------------------------------------------------------------|
| Step 1 init               | < 1 min per artifact.                                       |
| Step 2 fetch (per source) | 5-20 min operator-browser per source × ~4-10 sources.       |
| Step 3 extract            | 30-90 min per cluster × 2-4 clusters per artifact.          |
| Step 4 spot-check         | 30-45 min per artifact.                                     |
| Step 5 sign               | < 5 min per artifact (Ed25519 sign is offline + paste).     |

**Anchor sequence (per Pillar-1 MANIFEST D2):** `RBDG → SARE-NE → CFP → RCDG → VAPG (deferred — cycle closed) → PA Ag Innov`. Funder-family artifacts (Batch A) can run in any order, gateway-cap-permitting.

---

## §3 — Parallel-dispatch discipline (gateway saturation cap)

Per planning doc §10 risk row "Gateway/quota saturation under parallel dispatch" + Cards Wave-2 lesson:

> Cap concurrent dispatches at **2 artifacts × 3 seats = 6 simultaneous calls** with seat-stagger.

The CLI runs per-command, fully Local-Only-Sovereign. It does not invoke any seat or any cloud-routable LLM. The cap applies to the LLM-extraction step (Step 3 authoring) when the operator runs parallel extraction sessions via openclaw bridge or any other dispatch mechanism. Never run >6 simultaneous extraction calls across the 14 artifacts; stagger seats within each artifact's session.

---

## §4 — Failure modes the operator will hit

| Symptom                                                        | Likely cause                                                                                                                  | Fix                                                                                                                                       |
|----------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------|
| `F-FID-CORPUS-UNSIGNED-CHARTER` from `init`                    | Pillar-1 charter still at `_charter_v0_DRAFT.md`.                                                                             | Run the Pillar-1 sign ceremony first (see `pipeline/funder_intelligence/pillar_1_charters/MANIFEST.md`).                                  |
| `F-FID-CORPUS-HASH-MISMATCH` from `fetch --register`           | File on disk has a different SHA256 than the existing `sources.yaml` entry for that path.                                     | Remove the stale `sources.yaml` entry (or supersede), then re-register. The CLI refuses silent overwrite by design.                       |
| `F-FID-CORPUS-VERBATIM-TOO-LONG` from `extract`                | A `verbatim_quote` field has >2 sentences (OQ-4 rule).                                                                        | Split the fact into multiple `facts:` entries, each with a ≤2-sentence quote. Move paraphrase into adjacent `analysis:` field.            |
| `F-FID-CORPUS-FACT-ORPHAN` from `extract`                      | A fact's `corpus_ref` points at a file not yet registered in `sources.yaml`.                                                  | Run `fetch --register` for the underlying file first; verify the `corpus_ref` artifact_id prefix matches the artifact you're working on. |
| `sign` exit 2 "signature does NOT verify"                      | Operator signed wrong bytes (likely missed the `--dry-run` canonical-bytes step).                                             | Re-run `--dry-run`, copy the printed canonical bytes, sign those bytes offline, re-run `sign` with the new signature hex.                 |
| `sign` exit 4 "corpus already signed"                          | `_signed.yaml` already exists at corpus root.                                                                                 | Idempotent guard. If you need to resign (e.g., new sources added post-sign), move `_signed.yaml` aside intentionally and re-sign.        |
| `status` reports `F-FID-CORPUS-HASH-MISMATCH: [path1, ...]`    | On-disk file mutated after registration.                                                                                      | The file changed since registration. Re-fetch the source, decide whether the new bytes supersede the old, then re-register fresh.         |

---

## §5 — What is NOT in scope at Pillar-2

- Pillar-1 charter authoring → `pipeline/funder_intelligence/pillar_1_charters/`
- Pillar-3 structured artifact YAML (post-extraction) → `pipeline/funder_intelligence/funders/<id>.yaml` / `programs/<id>.yaml` (Phase 1 weeks 4-5)
- Pillar-4 field-test calibration → Phase 1 weeks 6-7
- Per-client KFR → `orgs/<slug>/vault/kfr/`
- Card content → `pipeline/cards/`
- Funder-discovery Scout corpus → `vault_shared/funder_intelligence/docs/`
- LLM extraction code → out of scope for the v0.1 infrastructure pre-stage; operator runs extraction sessions via openclaw bridge under Local-Only-Sovereign posture and writes the resulting YAML by hand into `extracted/`

---

## §6 — Sign-off checklist per artifact

- [ ] Pillar-1 charter at `_charter_v1_SIGNED.md` (verify via `tilth pillar2 corpus status --artifact-id <id>`)
- [ ] `init` ran cleanly; corpus tree exists.
- [ ] All planned primary sources registered in `sources.yaml` with correct `classification_tier`.
- [ ] All `extracted/<cluster>.yaml` files pass `extract` validation (≤2-sentence quotes, no orphan facts).
- [ ] Spot-check pass — every `verbatim_quote` bit-exact from source; every `analysis:` block kept out of the quote field.
- [ ] `sign --dry-run` produced canonical bytes; operator Ed25519-signed those bytes offline.
- [ ] `sign --signature-hex ... --signer-pubkey-fingerprint ...` exited 0; `_signed.yaml` at corpus root.
- [ ] Top-level Pillar-2 MANIFEST row updated to `SIGNED` with hash prefix.

When all 14 artifacts reach `SIGNED`, Pillar-3 extraction unblocks for weeks 4-5.

# Pillar-2 Corpus — MANIFEST

**Generated:** 2026-05-18 (Cowork session, infrastructure pre-stage).
**Branch:** `fid-pillar-2-infrastructure-pre-stage-2026-05-18`
**Pillar-1 dependency:** the 14 Pillar-1 charters at `pipeline/funder_intelligence/pillar_1_charters/MANIFEST.md` must reach `_charter_v1_SIGNED.md` lifecycle before corresponding rows here can leave `NOT_INITIALIZED`.
**Pillar-2 spec authority:** `pipeline/funder_intelligence/_research_corpus/README.md` (five non-negotiable discipline rules).
**Quality bar:** `docs/FID_ARTIFACT_OPTIMIZATION_PRINCIPLES_2026-05-18.md`.
**Operator workflow:** `docs/FID_PILLAR_2_OPERATOR_WORKFLOW_2026-05-18.md`.
**CLI:** `pipeline/cli/tilth_pillar2_corpus.py` (`init` / `fetch` / `extract` / `status` / `sign`).
**Signing helper:** `pipeline/funder_intelligence/_methodology/sign_corpus.py` (mirrors `sign_charter.py` shape).

## Status enum

| Status               | Meaning                                                                                                                              |
|----------------------|--------------------------------------------------------------------------------------------------------------------------------------|
| `NOT_INITIALIZED`    | Corpus tree scaffolded but `init` not yet run (Pillar-1 charter still at `_charter_v0_DRAFT.md`).                                    |
| `FETCHING`           | `init` ran; operator dropping primary-source files into `raw/`. No source registered in `sources.yaml` yet.                          |
| `EXTRACTING`         | One or more sources registered; operator authoring structured `extracted/<cluster>.yaml` files.                                      |
| `READY_FOR_SIGN`     | Sources + extracted clusters complete; awaiting operator spot-check + sign ceremony.                                                 |
| `SIGNED`             | `_signed.yaml` written; `corpus_canonical_bytes_sha3_512` verified against the pinned FID publisher Ed25519 pubkey.                  |

## Roster (cross-referenced with Pillar-1 MANIFEST)

| # | Artifact ID                       | Family  | Batch | Pillar-1 charter file                                                                       | Pillar-2 status     | Sig prefix                          |
|---|-----------------------------------|---------|:-----:|---------------------------------------------------------------------------------------------|---------------------|-------------------------------------|
| 1 | `USDA-RD`                         | funder  | A     | `pillar_1_charters/USDA-RD_charter_v0_DRAFT.md`                                             | NOT_INITIALIZED     | `<pending_operator_attestation>`    |
| 2 | `USDA-NIFA`                       | funder  | A     | `pillar_1_charters/USDA-NIFA_charter_v0_DRAFT.md`                                           | NOT_INITIALIZED     | `<pending_operator_attestation>`    |
| 3 | `USDA-AMS`                        | funder  | A     | `pillar_1_charters/USDA-AMS_charter_v0_DRAFT.md`                                            | NOT_INITIALIZED     | `<pending_operator_attestation>`    |
| 4 | `PA-DEPT-AG`                      | funder  | A     | `pillar_1_charters/PA-DEPT-AG_charter_v0_DRAFT.md`                                          | NOT_INITIALIZED     | `<pending_operator_attestation>`    |
| 5 | `PA-DCED`                         | funder  | A     | `pillar_1_charters/PA-DCED_charter_v0_DRAFT.md`                                             | NOT_INITIALIZED     | `<pending_operator_attestation>`    |
| 6 | `HEINZ-FOUNDATION`                | funder  | A     | `pillar_1_charters/HEINZ-FOUNDATION_charter_v0_DRAFT.md`                                    | NOT_INITIALIZED     | `<pending_operator_attestation>`    |
| 7 | `NCBA-CLUSA`                      | funder  | A     | `pillar_1_charters/NCBA-CLUSA_charter_v0_DRAFT.md`                                          | NOT_INITIALIZED     | `<pending_operator_attestation>`    |
| 8 | `RICHARD-KING-MELLON-FOUNDATION`  | funder  | A     | `pillar_1_charters/RICHARD-KING-MELLON-FOUNDATION_charter_v0_DRAFT.md`                      | NOT_INITIALIZED     | `<pending_operator_attestation>`    |
| 9 | `USDA-AMS-VAPG-FY26`              | program | B     | `pillar_1_charters/USDA-AMS-VAPG-FY26_charter_v0_DRAFT.md`                                  | NOT_INITIALIZED     | `<pending_operator_attestation>`    |
| 10| `USDA-RD-RBDG-FY26`               | program | B     | `pillar_1_charters/USDA-RD-RBDG-FY26_charter_v0_DRAFT.md`                                   | NOT_INITIALIZED     | `<pending_operator_attestation>`    |
| 11| `USDA-RD-RCDG-FY26`               | program | B     | `pillar_1_charters/USDA-RD-RCDG-FY26_charter_v0_DRAFT.md`                                   | NOT_INITIALIZED     | `<pending_operator_attestation>`    |
| 12| `USDA-NIFA-SARE-NE-FY26`          | program | B     | `pillar_1_charters/USDA-NIFA-SARE-NE-FY26_charter_v0_DRAFT.md`                              | NOT_INITIALIZED     | `<pending_operator_attestation>`    |
| 13| `PA-DEPT-AG-AGINNOV-FY26`         | program | B     | `pillar_1_charters/PA-DEPT-AG-AGINNOV-FY26_charter_v0_DRAFT.md`                             | NOT_INITIALIZED     | `<pending_operator_attestation>`    |
| 14| `USDA-RD-CFP-FY26`                | program | B     | `pillar_1_charters/USDA-RD-CFP-FY26_charter_v0_DRAFT.md`                                    | NOT_INITIALIZED     | `<pending_operator_attestation>`    |

## What unblocks on Pillar-1 sign-off

| Operator action                          | Unblocks                                                                                              |
|------------------------------------------|-------------------------------------------------------------------------------------------------------|
| Pillar-1 sign 1+ charter from Batch A    | `tilth pillar2 corpus init --artifact-id <funder_id>` for that funder; status flips to `FETCHING`.   |
| Pillar-1 sign 1+ charter from Batch B    | Same for that program; status flips to `FETCHING`.                                                    |
| Pillar-1 sign all 14 charters            | Full parallel Pillar-2 dispatch unblocks; weeks 2-3 corpus assembly fires per the planning doc §9.1.  |
| Pillar-2 sign per artifact (`_signed.yaml` lands) | That artifact's Pillar-3 extraction unblocks at weeks 4-5.                                  |

## Dispatch sequence (per Pillar-1 MANIFEST D2)

`USDA-RD-RBDG-FY26 (anchor) → USDA-NIFA-SARE-NE-FY26 → USDA-RD-CFP-FY26 → USDA-RD-RCDG-FY26 → USDA-AMS-VAPG-FY26 (deferred — cycle closed; preserve for FY27 pursuit) → PA-DEPT-AG-AGINNOV-FY26.` Funder-family artifacts (Batch A) can run in any order, gateway-cap-permitting.

## Parallel-dispatch discipline (Wave-2 lesson)

Per planning doc §10 risk row "Gateway/quota saturation under parallel dispatch": cap concurrent dispatches at **2 artifacts × 3 seats = 6 simultaneous calls** with seat-stagger. The CLI does not enforce the cap (it is per-command Local-Only-Sovereign), but the operator's parallel-extract scripts MUST respect it.

## CC-007 boundary recap

The CLI and signing helper perform zero outbound HTTP. The operator fetches sources in their own browser session under their own posture and drops the bytes into `raw/`. The CLI registers + hashes only what's already on disk.

## Cross-references

- Pillar-1 MANIFEST: `pipeline/funder_intelligence/pillar_1_charters/MANIFEST.md`
- Pillar-2 spec (5 discipline rules): `pipeline/funder_intelligence/_research_corpus/README.md`
- Quality spec: `docs/FID_ARTIFACT_OPTIMIZATION_PRINCIPLES_2026-05-18.md`
- Planning authority: `pipeline/planning/funder_intelligence_database_research_project_2026-05-16.md`
- Operator workflow: `docs/FID_PILLAR_2_OPERATOR_WORKFLOW_2026-05-18.md`
- Charter signing helper (precedent for shape): `pipeline/funder_intelligence/_methodology/sign_charter.py`
- Corpus signing helper: `pipeline/funder_intelligence/_methodology/sign_corpus.py`
- CLI: `pipeline/cli/tilth_pillar2_corpus.py`
- F-FID-* failure-code family lands at §4 v2.x.z follow-on amendment when the first Pillar-2 artifact LOCKs.

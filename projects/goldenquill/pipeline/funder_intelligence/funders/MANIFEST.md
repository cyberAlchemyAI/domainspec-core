# Pillar-3 Funder Artifacts — MANIFEST

**Generated:** 2026-05-18 (infrastructure pre-stage).
**Branch:** `fid-pillar-3-infrastructure-pre-stage-2026-05-18`
**Quality spec:** `docs/FID_ARTIFACT_OPTIMIZATION_PRINCIPLES_2026-05-18.md` §3.2.
**Pillar-1 dependency:** each row depends on the artifact's `_charter_v1_SIGNED.md`.
**Pillar-2 dependency:** each row depends on the artifact's `pillar_2_corpus/<id>/_signed.yaml`.
**CLI:** `pipeline/cli/tilth_pillar3_artifact.py` (`init` / `status` / `sign`).
**Signing helper:** `pipeline/funder_intelligence/_methodology/sign_artifact.py`.

## Lifecycle enum

| Lifecycle      | Meaning                                                                              |
|----------------|--------------------------------------------------------------------------------------|
| `stub`         | YAML file scaffolded by `init`; no body content yet.                                 |
| `draft`        | Operator-authored body content present; awaiting Codex/audit review + sign-off.      |
| `audited`      | Operator Ed25519 signature applied; canonical_bytes_sha3_512 recorded.               |
| `field_tested` | Used in at least one cycle; outcomes recorded in lessons memory.                     |
| `validated`    | Cross-cycle outcomes confirm the artifact's runtime decisions improved scoring.      |

## Roster (8 funders, Batch A)

| # | Artifact ID                       | Lifecycle | Sig prefix                          |
|---|-----------------------------------|-----------|-------------------------------------|
| 1 | `USDA-RD`                         | stub      | `<pending_operator_attestation>`    |
| 2 | `USDA-NIFA`                       | stub      | `<pending_operator_attestation>`    |
| 3 | `USDA-AMS`                        | stub      | `<pending_operator_attestation>`    |
| 4 | `PA-DEPT-AG`                      | stub      | `<pending_operator_attestation>`    |
| 5 | `PA-DCED`                         | stub      | `<pending_operator_attestation>`    |
| 6 | `HEINZ-FOUNDATION`                | stub      | `<pending_operator_attestation>`    |
| 7 | `NCBA-CLUSA`                      | stub      | `<pending_operator_attestation>`    |
| 8 | `RICHARD-KING-MELLON-FOUNDATION`  | stub      | `<pending_operator_attestation>`    |

## Cross-references

* Pillar-1 charters: `pipeline/funder_intelligence/pillar_1_charters/`
* Pillar-2 corpus:   `pipeline/funder_intelligence/pillar_2_corpus/`
* Programs MANIFEST: `pipeline/funder_intelligence/programs/MANIFEST.md`
* Operator workflow: `docs/FID_PILLAR_3_OPERATOR_WORKFLOW_2026-05-18.md`
* FID publisher pubkey (pinned): `vault_shared/funder_intelligence/publisher_pubkey.signed.yaml`

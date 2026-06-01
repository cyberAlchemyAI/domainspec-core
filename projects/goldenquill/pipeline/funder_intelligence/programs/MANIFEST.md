# Pillar-3 Program Artifacts — MANIFEST

**Generated:** 2026-05-18 (infrastructure pre-stage).
**Branch:** `fid-pillar-3-infrastructure-pre-stage-2026-05-18`
**Quality spec:** `docs/FID_ARTIFACT_OPTIMIZATION_PRINCIPLES_2026-05-18.md` §3.3.
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

## Roster (6 programs, Batch B — dispatch order)

| # | Artifact ID                  | Lifecycle | Sig prefix                          |
|---|------------------------------|-----------|-------------------------------------|
| 1 | `USDA-RD-RBDG-FY26`          | stub      | `<pending_operator_attestation>`    |
| 2 | `USDA-NIFA-SARE-NE-FY26`     | stub      | `<pending_operator_attestation>`    |
| 3 | `USDA-RD-CFP-FY26`           | stub      | `<pending_operator_attestation>`    |
| 4 | `USDA-RD-RCDG-FY26`          | stub      | `<pending_operator_attestation>`    |
| 5 | `USDA-AMS-VAPG-FY26`         | stub      | `<pending_operator_attestation>`    |
| 6 | `PA-DEPT-AG-AGINNOV-FY26`    | stub      | `<pending_operator_attestation>`    |

**Note on dispatch order:** matches the Pillar-1 MANIFEST D2 sequence
(`RBDG anchor → SARE-NE → CFP → RCDG → VAPG (deferred — cycle closed) → PA Ag Innov`).
`USDA-AMS-VAPG-FY26` charter preserved for FY27 pre-planning; FY26 cycle closed.

## Cross-references

* Pillar-1 charters: `pipeline/funder_intelligence/pillar_1_charters/`
* Pillar-2 corpus:   `pipeline/funder_intelligence/pillar_2_corpus/`
* Funders MANIFEST:  `pipeline/funder_intelligence/funders/MANIFEST.md`
* Operator workflow: `docs/FID_PILLAR_3_OPERATOR_WORKFLOW_2026-05-18.md`
* FID publisher pubkey (pinned): `vault_shared/funder_intelligence/publisher_pubkey.signed.yaml`

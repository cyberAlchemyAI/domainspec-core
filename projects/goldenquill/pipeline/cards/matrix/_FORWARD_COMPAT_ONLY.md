# `pipeline/cards/matrix/` — FORWARD-COMPAT ONLY

**Status at v7.0.11 LOCK:** Schema-only. **No populated matrix content ships before the v1.x matrix-phase explicit amendment.**

## Why this marker exists

Matrix files are the most coupling-prone surface in the Card System. Even with `binding_eligibility: false` enforced, the existence of matrix content invites runtime consumers to treat observational patterns as soft eligibility signals — re-introducing the F-CIC-CLC-COUPLING-VIOLATION (v7.0.8) ancestor that the operator killed across visual Cards on 2026-05-08 PM.

To structurally prevent that drift, v7.0.11 LOCK ships the matrix schema but **forbids any populated matrix file from existing in this directory** until v1.x explicit amendment authorizes the matrix phase.

## What may live here at v7.0.11 LOCK

- `_FORWARD_COMPAT_ONLY.md` (this file).
- `_schema/card_matrix.schema.json` — the forward-compat schema shape (per blueprint §18.7).
- Nothing else.

## What MUST NOT live here at v7.0.11 LOCK

- Any `<cic_slug>__<clc_slug>.yaml` populated matrix card.
- Any file declaring `binding_eligibility: true`.
- Any file omitting `status: "FORWARD_COMPAT_ONLY"`.

The loader at `pipeline/cards/loader.py` fails closed via `F-CARDS-COUPLING-VIOLATION-EXTENSION` on any attempt to load a populated matrix card before `v1_x_matrix_phase_active == True` per the runtime feature flag (which itself can only flip via explicit v1.x amendment LOCK).

## When this changes

The v1.x matrix-phase amendment will:

1. LOCK an explicit successor to v7.0.11 (e.g., architecture v7.1.x or a §18 v1.x amendment) authorizing matrix content.
2. Flip the `v1_x_matrix_phase_active` runtime flag.
3. Replace this marker file with a populated `README.md` documenting the active matrix layer and its allowed runtime readers (`allowed_runtime_readers: [Archivist]` per blueprint §18.7).
4. Begin shipping per-intersection matrix files at `<cic_slug>__<clc_slug>.yaml`.

Until that LOCK lands, this directory remains schema-only.

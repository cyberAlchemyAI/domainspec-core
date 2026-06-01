# Pillar-1 Depth Charters

**Status:** Week-1 staging directory for FID Phase-1.
**Authority:** `pipeline/planning/funder_intelligence_database_research_project_2026-05-16.md` §3.1 (in-tree).
**Roster authority:** self-contained in `MANIFEST.md` in this directory. An optional companion roster doc may exist at `docs/FID_EXPANDED_ROSTER_8_6_3_2026-05-18.md` but is NOT required (Codex-audit P1 remediation — see audit `findings.md §P1` on broken refs).
**Template:** `pipeline/funder_intelligence/_templates/depth_charter_template.md` (in-tree).

## What lives here

One Pillar-1 Depth Charter per FID artifact, authored as DRAFT before Pillar-2 corpus assembly fires. Each charter is operator-Ed25519-signed against the FID publisher pubkey at `vault_shared/funder_intelligence/publisher_pubkey.signed.yaml`. Until signed, a charter stays in `*_charter_v0_DRAFT.md` form and Pillar-2 work for that artifact is **blocked**.

## Validity discipline (Codex-audit P2 — 2026-05-18)

Per the Codex external-validity audit `findings.md §P2`, charter prose at Pillar 1 is allowed to frame hypotheses and define corpus scope, but the repo's anti-fabrication discipline requires every FID fact to carry `corpus_ref` + ≤2-sentence verbatim quote. **All source-like funder-fact claims in v0 DRAFT charters are pre-corpus operator assertions** and must be tagged inline `[CONJECTURE — Pillar-2 corpus pending]` (or in a per-section disclaimer at the top of §1). At Pillar-2 corpus assembly, each conjecture is either:

- Promoted to fact with `corpus_ref` + ≤2-sentence verbatim quote, or
- Removed from the artifact YAML.

Logician `F-FID-FACT-ORPHAN` enforces this at the Pillar-3 L-005 audit (any fact without a corpus pointer fails closed).

## Format discipline (Codex-audit P2 — 2026-05-18)

Per `findings.md §P2`, the planning doc's "one-page operator-signed charter" framing has drifted in v0 DRAFTs (charters are 700–1,100 words / ~110 lines). Audit alternative path: relabel these as **depth briefs / draft charters** for the v0 batch, and reserve the "one-page operator review" promise for the source-backed form (after Pillar-2 corpus assembly + operator attestation). The two anchor charters in this PR (USDA-NIFA-SARE-NE-FY26 program + USDA-RD funder, per operator override 2026-05-18) are authored to the richer Codex yaml shape with strict scope — they set the quality bar. All 14 charters now carry the honest `depth_charter_v0 (pre_corpus_hypothesis)` lifecycle label per FID Refinement Methodology Discipline 8; the prior "gold-standard" rhetoric was retired at Pass 0 + Pass 1. After Pillar-2 source-lock and operator Ed25519 attestation the lifecycle flips to `gold_standard_candidate` (post-source) and finally `gold_standard` (post-cycle); at that point the one-page-intent format discipline reconnects.

## File-naming convention

```
<artifact_id>_charter_v<N>_<lifecycle>.md
```

- `<artifact_id>` — canonical funder / program / cascade / reviewer-type ID
- `<N>` — charter version, incrementing on substantive revision (`v0` for first DRAFT, `v1` for first signed LOCK, etc.)
- `<lifecycle>` — `DRAFT` (unsigned, mutable) / `SIGNED` (Ed25519-attested, immutable except via revision-bump) / `RETIRED` (superseded; preserved for audit trail)

## Manifest

`MANIFEST.md` lists every charter in this directory with its current lifecycle marker, signature status, and pointer to corpus directory once Pillar-2 begins.

## Sign-off path

1. Cowork session authors `<artifact_id>_charter_v0_DRAFT.md` using the template.
2. Operator reviews; either approves text as-written or marks specific lines for revision.
3. **For the v0 batch, signing is MANUAL.** A canonical signing helper does **not** yet exist on disk and is tracked as a separate follow-up engineering task — see [P1: signing helper] below. Operator performs the sign step by hand against the FID publisher pubkey at `vault_shared/funder_intelligence/publisher_pubkey.signed.yaml`, producing:
   - Canonical-bytes SHA3-512 hash of the charter body (sort_keys=True, separators=(',', ':'), UTF-8, ensure_ascii=False, signature field excluded from computation)
   - Ed25519 signature over the canonical bytes
   - File rename `<artifact_id>_charter_v0_DRAFT.md` → `<artifact_id>_charter_v1_SIGNED.md`
   - Inline append of the signature block + canonical-bytes hash
4. Pillar-2 corpus assembly fires for that artifact only after the signed file is on disk and a corpus directory `_research_corpus/<artifact_id>/` is created with the signed charter copy at `_research_corpus/<artifact_id>/charter.signed.md` (per planning doc §3.2 — copy, do not move, because the charter stays canonical at its `pillar_1_charters/` path).

### [P1: signing helper] — follow-up engineering task (NOT in this PR)

Per the Codex external-validity audit at `pipeline/validation/review_qa_validity_audit_2026-05-18/findings.md` §P1 ("Signing path is described as required but is not executable on disk"), a canonical signing helper at `pipeline/funder_intelligence/_methodology/sign_charter.py` (or equivalent ceremony path) must land before any v0 → v1 SIGNED conversion is performed at scale. Minimum acceptance criteria:

- Canonical bytes exclude the signature field per the canonicalization rule above.
- Canonicalization is deterministic and byte-for-byte reproducible.
- Output path is `_research_corpus/<artifact_id>/charter.signed.md` (copy) + in-place file rename of the canonical charter to `_SIGNED` suffix.
- Unsigned DRAFT is preserved in git history (rename, not delete-recreate).
- MANIFEST regeneration is deterministic (same inputs → same lines).
- Tests at `tests/funder_intelligence/test_sign_charter.py` prove the above.

Until that helper lands, the v0 batch signs by hand. Manual checklist:

- Inputs: `pillar_1_charters/<artifact_id>_charter_v0_DRAFT.md` (canonical text + adversarial pre-check blocks populated).
- Operator action: canonicalize → SHA3-512 → Ed25519-sign against pinned FID publisher pubkey → produce signature block.
- Outputs: `pillar_1_charters/<artifact_id>_charter_v1_SIGNED.md` with signature block appended in §7; copy to `_research_corpus/<artifact_id>/charter.signed.md`; MANIFEST.md updated to reflect new lifecycle + sig status.

## What does NOT live here

- The artifact YAML itself (lives in `pipeline/funder_intelligence/<family>/<artifact_id>.yaml`)
- Primary-source corpus (lives in `pipeline/funder_intelligence/_research_corpus/<artifact_id>/`)
- Pillar-3 extracted facts (lives in the YAML)
- Pillar-4 calibration outputs (lives in `pipeline/funder_intelligence/_calibration/`)

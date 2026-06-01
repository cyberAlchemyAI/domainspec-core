# PROPOSAL — Section 5 Pipeline Amendment: Authorship Audit Trail Export Artifact (v0 scoping)

**Status:** **PROPOSAL ONLY.** Not locked. Not in audit cycle. This document is a scoping draft intended to become the v6 driver round of Section 5 (Pipeline) *after* the currently-scheduled Section 2 v7.1 and Section 4 v2.1 parent-backfill rounds land per §5 v5 sequencing.
**Author:** Claude (Cowork) under Josh's direction, 2026-04-18.
**Upstream trigger:** `pipeline/audits/advisory_synthesis_2026-04-18/SYNTHESIS.md` §2 Tomorrow / Blueprint.
**Parent architecture reference:** `pipeline/architecture/v0.1/tilth_architecture_locked.md` (v6-r2).
**Parent blueprint reference:** `pipeline/blueprint/v0.1/section_05_pipeline.md` (LOCKED v5 2026-04-18).

---

## 1. Problem statement

Tilth v0.1 enforces Law 5 (Applicant Brings the Substance) at the Logician level: Scribe cannot fabricate, augment, or substitute for applicant-supplied substance, and Logician's PRE/POST gates reject drafts that violate Law 5 semantics. The *enforcement* exists. What does not yet exist is the **packaged, externally-verifiable evidence record** that (a) a human was the structural author of the substance, (b) each section's revision lineage is attributable, and (c) the final bundle is accompanied by a standardized disclosure the funder can accept into their review record.

2026 federal funding environment — summarized in the advisory synthesis — rewards organizations that can *prove on submission* that a proposal was human-led:
- NIH / USDA originality standards (2026) prohibit applications "substantially developed by AI."
- Foundations increasingly require AI-usage disclosure; 94% want to expand AI use, 83% cite data security as the primary barrier.
- Legal-risk framing (advisory; cite-check pending before any customer use): documents without audit-ready human-authorship records may lose privilege / copyright defenses.

Without a packaged AAT artifact, Tilth's Law-5 enforcement stays *internal* — visible to the operator, invisible to the funder. The Golden Quill loses its strongest differentiator at the moment it matters most: the submission.

## 2. Proposal summary

Add the **Authorship Audit Trail (AAT) export artifact** to Section 5 submission_mode as a first-class, signed, exportable output bundled alongside the draft. The AAT is produced at `assemble_and_deliver` time from the iterations ledger (already append-only per §5 v2) and a new per-iteration metadata field capturing author class, Human Delta score, and transform type.

This proposal is structurally the **mirror of the v4 CalibrationReport amendment**: same signing discipline (BT13-style detached Ed25519 signature), same "built at assemble_and_deliver" pattern, same "forward-dep contracts with Section 2 + Section 4" pattern — but with opposite export disposition (CalibrationReport is Cedar-excluded from export; AAT is Cedar-included in the export bundle).

## 3. Scope — what this amendment does and does not do

### Does
- Add a new per-iteration metadata structure (`AATIterationEntry`) to the iterations ledger.
- Add a new per-run artifact (`AuthorshipAuditTrailReport`) assembled at `assemble_and_deliver`.
- Add a new phase in submission_mode: `assemble_aat` (runs after `judge_post` and before `bundle_export`).
- Add new failure codes: `F-PIPE-23.aat_missing_for_iteration`, `F-PIPE-24.aat_signature_mismatch`, `F-PIPE-25.aat_human_delta_below_threshold`.
- Add one new invariant (§7.17 AAT append-only parallel to iterations).
- Declare one new forward-dep contract on Section 2 (Vault) and one on Section 4 (Logician).

### Does not
- Change the Law-5 enforcement semantics. Logician still owns rejection of Law-5 violations. The AAT is *evidence*, not *enforcement*.
- Introduce any new LLM path or council mechanism. The AAT is produced by deterministic code.
- Change submission-mode or eval_mode entry points.
- Alter the CalibrationReport surface or its non-exportability.
- Add any network/egress surface.
- Extend scope to reporting-mode (v0.2 grant reporting vertical is out-of-scope for this amendment).

## 4. Mechanism sketch (driver-round material, not locked spec)

### 4.1 Per-iteration metadata (`AATIterationEntry`)

Every append to `iterations[]` in submission_mode also appends a parallel entry to `aat_iterations[]`:

```
AATIterationEntry
  iteration_index: int               # matches iterations[i]
  section_id: str                    # rubric-keyed section identifier
  author_class: AuthorClass          # HUMAN | SCRIBE | EDITOR | JUDGE_REVISION | APPLICANT_SUBSTANCE
  transform_type: TransformType      # INITIAL_SUBSTANCE | POLISH | STRUCTURAL_EDIT | CLARIFICATION | FACT_INSERT (source-pinned) | NONE
  human_delta_score: float           # 0.0–1.0; structural/authorial contribution share in this iteration
  source_citations: tuple[str, ...]  # §1 RFA-source pointers; empty iff transform_type in {POLISH, CLARIFICATION}
  timestamp: datetime (UTC, ns)      # NFC-normalized ISO-8601
  prev_hash: bytes                   # SHA-256 over prior AATIterationEntry canonical bytes; establishes per-iteration hash chain
```

The **prev_hash chain** makes AAT tamper-evident without requiring per-iteration signatures (same pattern as audit-log append-only schemes).

### 4.2 Run-level report (`AuthorshipAuditTrailReport`)

Assembled at `assemble_aat` phase from the full `aat_iterations[]`:

```
AuthorshipAuditTrailReport
  run_id: str
  org_slug: str                      # Law-3 single-client seal
  rfa_hash: bytes                    # Law-1 RFA-source-of-truth seal (matches §5 v2 submission)
  sections: tuple[AATSectionSummary] # per rubric-section roll-up
  human_delta_aggregate: float       # weighted by section-length
  disclosure_report: DisclosureReport # three-point: cover-letter / acknowledgments / methods
  iteration_chain_head: bytes        # last AATIterationEntry.prev_hash — seals the chain
  router_yaml_snapshot_hash: bytes   # model-binding attribution at run time (same pattern as CalibrationReport §4.15 step 10)
  generated_at: datetime
```

### 4.3 Signing and bundling (mirror of CalibrationReport, opposite disposition)

- **Signing.** `AuthorshipAuditTrailReport` is canonicalized to bytes (same canonical-bytes discipline as §5 v5 §5.6.4 extended in the v7.1 contract), Ed25519-signed with BT13-style detached-signature pattern (same key management as CalibrationReport at §4.15 step 10), written to Vault at `orgs/{slug}/vault/aat/{run_id}/report.{json,sig}`.
- **Bundle inclusion.** Unlike CalibrationReport, AAT is **exportable**: Cedar policy explicitly *allows* AAT bundle membership for submission-mode runs (new Cedar allowlist row on the Section 2 v7.2 contract declared below).
- **Export predicate.** `F-PIPE-23/24/25` are PRE-gate-to-bundle-export checks: missing AAT, signature mismatch, or aggregate Human Delta below operator-configured threshold all block export.

### 4.4 Human Delta scoring — deterministic, not LLM-judged

`human_delta_score` is computed deterministically from the diff between successive `iterations[i-1]` and `iterations[i]` draft bytes *plus* the `AuthorClass` declared by the actor that produced the iteration. No LLM is invoked for AAT scoring. This matters: Law-5 evidence cannot itself depend on the same LLM substrate it is meant to attest against.

Rough formula (to be pinned in driver round):
- INITIAL_SUBSTANCE and STRUCTURAL_EDIT from HUMAN → score 1.0
- APPLICANT_SUBSTANCE insert (via Scribe paste of a source-pinned quote) → score 1.0
- POLISH / CLARIFICATION from SCRIBE/EDITOR → score 0.0 (does not increase human delta, does not decrease; does not count)
- JUDGE_REVISION → score 0.0 by default; the applicant re-asserting the revision is a separate HUMAN iteration
- Aggregate per section = sum of human-delta-scoring iterations weighted by bytes-added-and-retained-in-final.

Operator-configurable minimum threshold (e.g., 0.5 default) below which `F-PIPE-25` fires at export time. Threshold is in `charter`, not hardcoded.

### 4.5 Disclosure report

Standardized three-point artifact appended to the bundle:
1. **Cover letter disclosure paragraph** — one paragraph, templated per rubric section, affirming human authorship and declaring AI assistance per funder's current disclosure requirements.
2. **Acknowledgments section** — naming Tilth seats by role (not model), router.yaml snapshot hash, Cedar policy hash.
3. **Methods section** — per-section revision counts, per-section human-delta aggregate, iteration chain head hash, submission timestamp, RFA hash.

## 5. Forward-dep contracts (mirror of v4 pattern)

This proposal declares two parent-backfill contracts that must land before Section 5 amendment locks:

### 5.1 Section 2 v7.2 contract (new allowlist rows + new intent)

- Add `aat-write` intent to `§4.10.4` allowlist (pipeline → vault write for AATIterationEntry and AuthorshipAuditTrailReport).
- Add `aat-read` intent for operator-side inspection tools.
- Add explicit Cedar *allow* rule for AAT membership in submission export bundles (opposite disposition to CalibrationReport).
- Extend `§5.6.4` canonical-bytes exhaustiveness enumeration to cover the two new dataclasses.

### 5.2 Section 4 v2.2 contract (new PRE-gate + new predicate)

- Add `F-AAT-CHAIN-BROKEN` PRE-gate failure code with predicate: `aat_iterations[i].prev_hash == sha256(canonical_bytes(aat_iterations[i-1]))` for all `i >= 1`.
- Add the Logician-side law-map row: Law 5 eval-time becomes Law 5 eval-time + Law 5 evidence-packaging.
- Extend `_assert_mode_isolation` to reject AAT writes when `mode != submission_mode`.

## 6. New Section 5 invariant

### §7.17 (proposed) — AAT append-only parallel to iterations

For every `i` in `range(len(iterations))`, `aat_iterations[i]` MUST exist, MUST share `iteration_index == i`, and MUST be append-only under the same F-PIPE-19 discipline as `iterations[]`. Violation surfaces as `F-PIPE-23.aat_missing_for_iteration`.

## 7. New failure codes (Section 5-owned)

| Code | Trigger | Severity |
|---|---|---|
| `F-PIPE-23.aat_missing_for_iteration` | `len(aat_iterations) != len(iterations)` at any checkpoint | HARD (blocks export) |
| `F-PIPE-24.aat_signature_mismatch` | `AuthorshipAuditTrailReport` signature fails Ed25519 verify at export PRE-gate | HARD (blocks export) |
| `F-PIPE-25.aat_human_delta_below_threshold` | `human_delta_aggregate < charter.aat_minimum_threshold` at export PRE-gate | HARD (blocks export, operator override available iff charter permits) |

## 8. Tests (driver-round material, not yet written)

Minimum test families the driver round must land:
- `test_aat_append_matches_iterations` — for every iteration mode path, a matched AAT entry appears.
- `test_aat_chain_tamper_detected` — mutating a middle AAT entry's bytes fails the chain-head check.
- `test_aat_signature_roundtrip` — sign + verify across a submitted report.
- `test_aat_export_bundle_inclusion` — Cedar decision at export-bundle assembly includes AAT, excludes CalibrationReport (both invariants preserved).
- `test_aat_below_threshold_blocks_export` — human_delta_aggregate < threshold → F-PIPE-25.
- `test_aat_eval_mode_no_writes` — eval_mode runs do not produce AAT entries; §4 v2.2 `_assert_mode_isolation` rejects a misplaced aat-write intent.
- `test_disclosure_report_contains_three_points` — cover-letter / acknowledgments / methods all present and populated.
- `test_router_yaml_hash_in_report` — model-binding attribution survives round-trip.

## 9. Non-ownership (mirror of §12)

Not owned by this amendment:
- The operator's funder-disclosure language templates beyond the three-point skeleton.
- Any attempt to *interpret* funder disclosure rules (Law 1: funder rules trace to the RFA; the AAT is the audit record, not the rule interpretation).
- UI for the operator to inspect AAT entries (CLI / inspector tool is operator-facing, not Section 5 code).
- Key rotation for the AAT signing key (Section 2 key-rotation protocol owns this; Section 5 uses the key).

## 10. Law map

| Law / rule | AAT coverage |
|---|---|
| **L-001 RFA Source of Truth** | `rfa_hash` sealed in report; `source_citations` tuple per iteration for FACT_INSERT transforms. |
| **L-002 No Boundary Drift** | AAT scope sealed by §4 v2.2 predicate; no in-run expansion. |
| **L-003 Org Isolation** | `org_slug` sealed in report; AAT read/write Cedar-gated to single-org like all Section 2 intents. |
| **L-004 Apolitical + Admin-Risk** | Disclosure report uses whitelist-only clean-output (same discipline as submission draft); admin-risk register applies to disclosure paragraph. |
| **L-005 Strict Two-Audit Cycle** | AAT export gate (F-PIPE-23/24/25) runs at assemble_and_deliver POST; attestation becomes part of the POST record. |
| **AR-1 Save State Always** | AAT writes checkpoint on both success and failure paths (same discipline as §5 v5 §7.6). |
| **AR-2 Test Your Own Work** | Chain-head self-verify runs at every append; signature self-verify runs at every export. |
| **AR-4 Clean Output** | Disclosure paragraphs whitelist-stripped like submission draft. |
| **Mode-isolation (v4)** | AAT writes gated to submission_mode only (§4 v2.2). |

## 11. Open questions

1. **Charter schema for `aat_minimum_threshold`.** Single org-wide default, or per-funder override? (Per-funder likely lives in the RFA intake stage, not charter.)
2. **Disclosure-report language evolution.** Does Tilth maintain a versioned library of funder-specific disclosure paragraph templates, or is the skeleton generic and the operator fills in per-funder? Argument for the library: this is institutional knowledge that compounds. Argument against: funder rules change, template rot risk.
3. **Human Delta formula pinning.** The 4.4 formula is a sketch. Driver round must either formalize it or explicitly defer ("operator-provided scoring function with registered signature"). Recommendation: formalize a deterministic default, allow operator override registered via Cedar allowlist.
4. **Section 4 v2.2 vs. a new Section 4 v3.** The parent-backfill naming convention matters: v4's new PRE-gate landed as v2.1 (a .1 bump). AAT adds one new PRE-gate + extends `_assert_mode_isolation`. Is that still a .1 bump (v2.2) or does it promote to v3? Suggest v2.2 unless Red Team surfaces additional scope.
5. **Export-bundle format.** Does AAT ship as (a) separate file alongside the draft (`.pdf` + `.aat.json` + `.aat.sig`), (b) embedded in the PDF as a structured attachment, or (c) both? (b) is what funders will prefer; (a) is what engineering wants. Suggest both.
6. **v0.2 grant reporting vertical interaction.** When v0.2 lands, reporting-mode will also want an AAT. This amendment explicitly scopes to submission_mode. Reporting-mode AAT is a future-round expansion, not this one.

## 12. Sequencing

This proposal cannot enter an audit cycle until:
1. Section 2 v7.1 parent-backfill round (eval_mode contract) LOCKS — per §5 v5 sequencing step 1.
2. Section 4 v2.1 parent-backfill round (eval_mode contract) LOCKS — per §5 v5 sequencing step 2.
3. Section 0.5 Interface Index v4 lands (adds the new rows this proposal declares).

Then:
4. Section 5 v6 driver round opens; this proposal becomes the driver input.
5. Section 5 v6 verification round (or v7, per Red Team outcome) closes Group-1 gaps.
6. Section 2 v7.2 + Section 4 v2.2 parent-backfill rounds land behind the Section 5 v6 LOCK.

If any Red Team attack-vector surfaces against `prev_hash` chain integrity (e.g., preimage attacks on canonical-bytes, replay of valid signatures across runs), the proposal regresses to a scoping round rather than closing at v6.

## 13. Not a lock

This document is scoping material. It is not a blueprint. It does not amend the locked Section 5 file. The locked Section 5 file (v5 2026-04-18) remains unchanged. When this proposal enters an audit cycle it will be rewritten as a Section 5 v6 driver document under the same L-005 strict-cycle discipline that produced v1→v5.

— End of AAT export-artifact proposal v0 —

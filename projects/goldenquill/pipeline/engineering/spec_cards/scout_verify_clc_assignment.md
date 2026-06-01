# Spec card — pipeline.scout.verify (CLC assignment delta)

**Architecture anchor:** `pipeline/architecture/v0.1/architecture_v7_0_8_amendment.md` §5 (LOCKED 2026-05-08).
**Spec-card version:** v1
**Round:** post-v7.0.8-LOCK (this is one of three companion modules pre-staged at LOCK time).
**Priority:** v0.1 medium — F-CIC-CLC-MATCH-NULL is dormant per-org until first cycle attempt; full enforcement requires Scout VERIFY to populate `clc_assigned`.

---

## Purpose

Extend Scout's existing VERIFY stage to assign one of the eight canonical Capital Logic Cards to each verified opportunity. Output flows into the Funder Intelligence Database `clc_assigned` field (per v7.0.5) and into per-match Match Database records (per v7.0.5). Without this delta, every grant cycle hits `F-CIC-CLC-MATCH-NULL.clc_unset` after the per-org dormancy expires.

---

## Inputs

- `opportunity_id` (string) — Scout's canonical hash of the opportunity record
- `synopsis_text` (string) — fetched live in current VERIFY (Grants.gov fetchOpportunity / SAM.gov / state portal scrape per Section 3 Scout v5.x)
- `program_metadata` (dict) — funder, program name, ALN, deadline, award range, eligibility stanza
- (optional) `program_rule_pack` (dict) — if attached, supplies authoritative CLC tag for the program

## Outputs

Extends the verified opportunity record with:

```yaml
clc_assigned: <one_of_pipeline.types.CapitalLogicCard>
clc_assignment_confidence: <float 0.0–1.0>
clc_assignment_rationale: <string — synopsis quotes + program-rule-pack signals>
clc_assignment_at: <iso8601_utc>
clc_assignment_by: scout_verify_stage | operator_override
clc_assignment_provenance: <hex of synopsis_text SHA3-512 + program_rule_pack version pin>
```

Below the confidence threshold (hard floor 0.50; default 0.70), output is `clc_assigned: null` and the opportunity surfaces to operator REVIEW for manual assignment.

## Hard-floor confidence discipline (per v7.0.8 §5)

- `vault_shared/scout_config.yaml::clc_assignment_threshold` is operator-tunable.
- Hard floor is 0.50. Below-floor override requires:
  - operator signature on the override entry (Ed25519 + ML-DSA-65 hybrid per A12)
  - HIGH-severity admin-risk ledger entry per BT9 audit-chain discipline
  - explicit time-bounded TTL (default 30 days, max 90 days)
- Without all three, attempting to set threshold < 0.50 fails-closed at config validation.

## Implementation outline

```python
# pipeline/scout/verify.py — add to existing VERIFY stage
from pipeline.types import CAPITAL_LOGIC_CARD_VALUES, CLC_DISPLAY, CapitalLogicCard

def assign_clc(
    *,
    synopsis_text: str,
    program_metadata: dict,
    program_rule_pack: dict | None,
    config_threshold: float,  # validated against hard floor 0.50 at config load
    structured_output_caller,  # injected Pydantic AI structured-output call
) -> CLCAssignment:
    """Returns ``CLCAssignment(clc_assigned, confidence, rationale, ...)``.

    Logic:
      1. If program_rule_pack carries a canonical clc tag, use it directly
         (confidence = 1.0; rationale = "program rule pack {pack_id}").
      2. Else: structured-output call with CapitalLogicCard literal as the
         output schema; constrain to canonical 8 via Pydantic. Score = top-1
         softmax / sum-of-all.
      3. If score < config_threshold: return null + REVIEW surface.
      4. Else: return CLCAssignment with provenance hash.
    """
```

## Acceptance tests

- All 8 canonical CLCs accepted as legitimate output values.
- Output value not in `CAPITAL_LOGIC_CARD_VALUES` raises a Pydantic validation error (defends against LLM hallucinated CLC names).
- Below-threshold opportunity returns `clc_assigned=None` and surfaces to REVIEW.
- Hard-floor 0.50 enforced — config that sets threshold to 0.30 without admin-risk ledger entry fails at config validation.
- ≤ 2 second performance budget per opportunity on baseline hardware.
- Provenance hash matches re-computed hash on re-fetch.
- Operator REVIEW override flows into `clc_assignment_by: operator_override` with operator signature.

## Coordination

- Composes against v7.0.5 (Funder Intel DB schema field `clc_assigned`).
- Composes against v7.0.6 (Scout seat surface in roster).
- Triggers on the existing VERIFY stage; doesn't add a new pipeline stage.
- F-CIC-CLC-MATCH-NULL becomes operationally meaningful once this module ships.

## Open questions for build session

1. Pydantic AI structured-output prompt: enumerate all 8 CLCs with descriptions verbatim from TILTH-CLC-00, or rely on `CapitalLogicCard` literal type alone? (Suggest: enumerate with descriptions for first 100 cycles, then evaluate hit rate.)
2. Cache strategy: same opportunity hash + same program rule pack version = cached `clc_assigned`? (Suggest: yes, cache for 14 days; below-threshold null is also cached to avoid re-prompting.)
3. Error handling: structured-output call timeout — return null + REVIEW, or fail-closed the verification? (Suggest: null + REVIEW; the opportunity stays in candidate state until operator intervenes.)

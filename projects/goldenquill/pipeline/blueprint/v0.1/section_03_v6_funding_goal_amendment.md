---
title: §3 v6 — Scout DISCOVER goal-aware input shape (compound paired-commit sibling 2/4)
filed: 2026-05-11
operator: Josh Inklovich
status: LOCKED 2026-05-11 — compound paired-commit (sibling 2/4) with §2 v7.5 + §4 v2.x.4 + §0.5 v20. L-005 strict two-cycle CLOSED with FULL LIVE CROSS-FAMILY rigor. SPEC-ONLY at v0.2 per §15 v1 precedent. Includes the §6.x prompt-template goals-block injection sub-amendment (OQ-2 "both, paired" — bundled into this single sibling for compound atomicity).
parent_locks:
  - pipeline/blueprint/v0.1/section_03_scout.md                                         # §3 v5 LOCKED 2026-04-17 — DISCOVER channels A-F
  - pipeline/architecture/v0.1/architecture_v7_0_5_amendment.md                         # v7.0.5 row 179 — Scout channel G
  - pipeline/blueprint/v0.1/section_06_operating_envelope.md                            # §6 v1-r1 LOCKED 2026-04-21 — prompt-template compilation pipeline (§6.11)
  - pipeline/blueprint/v0.1/section_02_v7_5_funding_goal_amendment.md                   # §2 v7.5 (paired-commit sibling 1/4)
  - pipeline/architecture/v0.1/architecture_v7_0_7_amendment.md                         # v7.0.7 row 180 — classification routing; F-CLASS-SLOT-ID-NON-OPAQUE PRE-gate
  - pipeline/architecture/v0.1/architecture_v7_0_8_amendment.md                         # v7.0.8 — CIC × CLC orthogonality
companion_amendment: pipeline/blueprint/v0.1/section_00_5_section_funding_goal_amendment.md  # §0.5 v20 paired-commit
compound_lock_with: section_02_v7_5_funding_goal_amendment.md + section_04_v2_x_4_funding_goal_amendment.md + section_00_5_section_funding_goal_amendment.md
---

# §3.6 DISCOVER goal-aware input shape (extends §3 v5 §3.2)

`Scout.session_call()` adds optional `funding_goals: tuple[FundingGoal, ...]` parameter, read at session start from `orgs/{slug}/vault/operational/funding_goals/` filtering `status in {"pursuing", "blocked"}`.

## §3.6.1 Slug validation (RT-01 + RT-C2-01)

`{slug}` MUST be validated:
1. Normalize to Unicode NFKC (RT-C2-01); reject any non-ASCII characters.
2. Validate against `orgs/ORG_INDEX.md` registry membership.
3. Apply regex `^[a-z0-9_-]+$` AFTER normalization.
4. Reject `..`, `/`, path separators, any character outside the set.

F-FG-CROSS-ORG-LEAK PRE-gate fails closed on validation failure with sub-tags `.path_traversal_detected` (RT-01) + `.unicode_normalization_bypass` (RT-C2-01).

## §3.6.2 O_NOFOLLOW + atomic read (RT-02 + RT-C2-02)

Every read of `operational/funding_goals/*.json` uses `os.open(path, os.O_RDONLY | os.O_NOFOLLOW)` — file descriptor used directly for `fcntl.flock(LOCK_SH)` per v7.0.4-M1 §4 atomic-read precedent. **No intermediate path-string dereference between regex check and open() call (RT-C2-02 TOCTOU mitigation).** Symlink rejection inherited from v7.0.4-M1 §4. F-FG-CROSS-ORG-LEAK PRE-gate sub-tags `.symlink_detected` (RT-02) + `.toctou_path_dereference` (RT-C2-02).

# §3.7 Channel A-G dispatch unchanged

Per §3 v5 + v7.0.5 channel G, A-G stay parallel primary. Goals modulate post-channel ranking only. **No new "goal-aware channel" — the goals modulate ranking and de-dup, not channel selection.** This preserves the channel-A-through-G architecture from v7.0.5 and avoids the L-006 dormant-binding miss.

## §3.7.1 `fit_score_cached` composition — additive per dimension (RT-17)

Bonus `[0, +25]` per active goal. **Composition is additive per matching dimension** (not AND-gated):
- `cic_match_bonus` (independent): non-zero when goal's `cic_tag` matches candidate's CIC tag.
- `clc_overlap_bonus` (independent): non-zero when goal's `clc_tags` overlap with candidate's inferred CLC tags is non-empty.
- `bonus = (cic_match_bonus) + (clc_overlap_bonus)` — both can fire independently.

Goal's `priority_weight` weights the bonus. Combined `fit_score_cached` clamped `[0, 100]`. Decimal arithmetic per v7.0.4-M1 §6.

CIC × CLC orthogonality preserved as truly additive composition (per v7.0.8 LOCK + CLAUDE.md "CIC × CLC orthogonal — never pre-map").

## §3.7.2 Per-goal de-dup pass

After channel-dispatch dedup, candidates are tagged with the set of goals they could plausibly contribute to (zero, one, or many). This tag travels through VERIFY into REVIEW and is surfaced to the operator at REVIEW.

# §3.8 §6.x prompt-compilation goals-block injection (OQ-2 "both, paired" sub-amendment)

§6.11 prompt-template compilation pipeline gains a goals-block injected at start-block + end-block (per A4 architectural FLOOR; F-CONTEXT-PLACEMENT PRE-gate already enforces; goals-block joins the existing four load-bearing markers).

## §3.8.1 Classification-aware redaction (OQ-6 + RT-10 + RT-11)

The `purpose` field default classification SHAREABLE per OQ-6 (Card-level archetype default).

**Per-grant SP0 override propagation (RT-11):** goals-block compiler reads BOTH org-level + per-grant SP0 classification register, with **per-grant override taking precedence**. Mirrors v7.0.7 §3.6 three-layer-defaults precedence rule.

**Cache-invalidation latency (RT-10 BOUNDED-by-A1+A4 + RT-C2-11):** at v0.2, classification override cache-invalidation latency is bounded by single-cycle wall (operator runs explicit cycle restart per v7.0.7 §3.6). Cache-invalidation MUST complete within **5 seconds** after operator-initiated cycle restart (RT-C2-11); any longer duration is a violation of the bounded-by-A1+A4 contract and surfaces as admin-risk-ledger entry HIGH severity. v1.x amendment lands per-cycle invalidation hook. v2 multi-tenant amendment per Section O.5 lands real-time invalidation. **v0.2 known-limitation explicitly documented.**

## §3.8.2 Numeric opaque slot enforcement (RT-12 + RT-C2-06)

Cloud-routed seats reading goals-block get `[SLOT_<int>]` opaque-slot fill when `purpose` resolves to `confidential`.

**Slot-naming requirement (RT-12):** goals-block compiler MUST emit only **numeric opaque slots**; semantic-named slots like `[SLOT_GOAL_PURPOSE_<record_id>]` are forbidden. F-CLASS-SLOT-ID-NON-OPAQUE PRE-gate's regex extended via §4 v2.x.4 to reject any slot containing alphabetic characters after `SLOT_`.

**Positive-integer slot-ID requirement (RT-C2-06):** Slot IDs MUST be positive integers ≥ 1. Compiler MUST reject any slot not matching `^\[SLOT_[1-9][0-9]*\]$` (excludes `[SLOT_0]`, `[SLOT_-1]`, `[SLOT_]`). F-CLASS-SLOT-ID-NON-OPAQUE PRE-gate sub-tag `.non_positive_integer`.

# §3.9 Per-goal de-dup tagging (extends §3 v5 §3.5 dedup pass)

Post-dedup tagging pass surfaces candidate-to-goal contribution mapping. Operator sees BOTH `match_score` (raw) AND `goal_aware_match_score` (composite) at REVIEW gate per Law 4 substance-not-style transparent surfacing.

# §3.10 §0.5 row registration

Two interface-contract rows in §0.5 v20:
- Row 466: `scout.discover.input_shape.funding_goals_block.v1` — DISCOVER goals-block injection + slug validation (RT-01) + O_NOFOLLOW (RT-02 + RT-C2-02).
- Row 467: `scout.discover.fit_score_cached.goal_aware_composer.v1` — additive composition (RT-17).

# §3.11 Changelog

- 2026-05-11 §3 v6 LOCKED — compound paired-commit (sibling 2/4). Bundles §6.x prompt-compilation goals-block injection sub-amendment per OQ-2 "both, paired" for compound atomicity. SPEC-ONLY at v0.2; v1.x Code-phase realizes LIVE composer + LIVE cache-invalidation hook.

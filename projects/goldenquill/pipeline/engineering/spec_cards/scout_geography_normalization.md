# Spec card — pipeline.scout.verify_stage (geography canonicalization)

**STATUS:** PRE-STAGED 2026-05-10
**Round:** Scout VERIFY false-negative closure — surfaced by 2026-05-10 review (finding #8).
**Canonical home:** `pipeline/scout/verify_stage.py` (+ new helper `pipeline/scout/_geography.py`)

**Framework:** per `pipeline/templates/component_analysis_template.md`.

---

## 1. Blueprint anchors

- `pipeline/blueprint/v0.1/section_03_scout.md` — VERIFY stage eligibility filter §A-GEO.
- `pipeline/architecture/v0.1/tilth_architecture_locked.md` v7 §D.1 — Scout two-stage discovery contract.
- `pipeline/architecture/v0.1/architecture_v7_0_5_locked.md` — Funder Intel + Match DB geography axis.

**Spec-card version:** v1
**Blueprint hash-at-card:** recompute on open.

---

## 2. Current state (drift)

`pipeline/scout/verify_stage.py` line 671:

```python
if profile.geography is None or profile.geography not in live.eligible_geographies:
    return (False, REASON_A_GEO_01)
```

**Problem:** `not in` is literal string compare. `profile.geography = "PA"` will false-negative against `live.eligible_geographies = {"Pennsylvania"}`. Same for `"Allegheny County, PA"` vs `"Allegheny County"`, casing, whitespace, hyphenation, or "PA-Allegheny" vs "Allegheny PA". This is a Law-3-adjacent correctness issue: legitimate-fit opportunities silently drop from the radar.

---

## 3. Scope

### 3.1 In scope

- New module `pipeline/scout/_geography.py` exporting `canonicalize_geography(value: str) -> frozenset[str]`. Returns the set of canonical tokens a single string expands to. Examples:
  - `"PA"` → `frozenset({"pennsylvania", "pa"})`
  - `"Pennsylvania"` → `frozenset({"pennsylvania", "pa"})`
  - `"Allegheny County, PA"` → `frozenset({"allegheny county, pa", "allegheny county", "pa", "pennsylvania"})`
  - `"National"` / `"nationwide"` / `"USA"` → `frozenset({"national", "nationwide", "usa", "united states"})`
- Lowercase + strip whitespace + collapse internal whitespace + strip trailing punctuation.
- State abbreviation expansion: full canonical map of US states + DC + territories. Bidirectional.
- `is_geography_match(profile_geo: str | None, live_geos: Iterable[str]) -> bool` — TRUE iff `canonicalize_geography(profile_geo) ∩ ⋃ canonicalize_geography(g) for g in live_geos` is non-empty. National/nationwide opportunities match any non-None applicant geography.
- Wire `is_geography_match` into `verify_stage.py:671`, preserving the `REASON_A_GEO_01` failure path on no-match.
- New `REASON_A_GEO_01_NORMALIZED` reason-tag carrying the canonicalized forms in audit output (for operator review when a fit is unexpected — sovereignty/explainability requirement).

### 3.2 Out of scope

- International geographies. v0.1 is US-only. Non-US tokens pass through unmodified.
- City-level matching. State + county is the v0.1 granularity.
- Fuzzy/levenshtein matching. Canonical-token-set intersection only — no string similarity heuristics.
- Match DB schema changes. The canonicalized tokens are computed at verify-time, not persisted.

---

## 4. Failure codes touched

- `REASON_A_GEO_01` — extended reason-tag to include both raw and canonical forms.
- No new failure codes minted.

---

## 5. Test surface

### 5.1 Property tests
- `canonicalize_geography` is idempotent: `f(f(x)) == f(x)`.
- Casing-invariant: `f("PA") == f("pa") == f("Pa")`.
- Whitespace-invariant.
- All 50 state abbreviations map bidirectionally to full names.
- `"National"`, `"nationwide"`, `"USA"`, `"United States"` are pairwise equivalent.

### 5.2 Match tests (positive)
- `is_geography_match("PA", ["Pennsylvania"])` → True.
- `is_geography_match("Pennsylvania", ["PA"])` → True.
- `is_geography_match("Allegheny County, PA", ["Pennsylvania"])` → True.
- `is_geography_match("PA", ["nationwide"])` → True.
- `is_geography_match("PA", ["National", "California"])` → True.

### 5.3 Match tests (negative)
- `is_geography_match("CA", ["Pennsylvania"])` → False.
- `is_geography_match(None, ["Pennsylvania"])` → False (None geography is unfit per current contract).
- `is_geography_match("PA", [])` → False.

### 5.4 Corpus tests
- `tests/corpus/scout_geography/v1/` — at least 20 real-world (geography, eligible_geographies, expected_match) tuples from past Scout runs. Mix of federal-national, state-specific, county-specific, multi-state.

### 5.5 Regression
- Existing `verify_stage` tests must continue to pass; the canonicalization layer is an INTERSECTION over current behavior (any previous literal match is also a canonical match).

---

## 6. Done definition

- `pytest pipeline/scout/tests/` green.
- New `_geography.py` module ≤ 200 LOC, fully typed.
- Zero literal `in eligible_geographies` calls remaining in `pipeline/scout/`.
- `BLUEPRINT_DEPS` on `verify_stage.py` updated to record §3 anchor.

---

## 7. Risks / open questions

- **Q1.** Does Scout currently emit `profile.geography` as a single string or a list? If a list, the API needs `is_geography_match(profile_geos: Iterable[str], …)`. Worth checking PROJECT_CONTEXT schema before estimating.
- **Q2.** Foundation feeds occasionally list `"Tri-state region"` or similar — these aren't normalizable without a domain dictionary. v0.1 behavior: pass-through unmatched, log to `pipeline/scout/_unmatched_geographies.jsonl` for operator triage. Out of scope for this card to *resolve*; in scope to *log*.
- **Q3.** Should `"PA"` match against `"Pittsburgh, PA"` (city-level eligibility)? Probably yes since the city is in PA. But that direction (county-or-city → state) is asymmetric with state → county. Document the asymmetry.

---

## 8. Suggested executor

Codex (Claude Code) authoring → cross-family two-audit committee per L-005.

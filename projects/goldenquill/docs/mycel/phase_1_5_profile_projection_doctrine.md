# Phase 1.5: Profile Projection Doctrine

## The Doctrine

MyCel preserves canonical thought Truth as append-only RAW capture and develops it through deterministic, profile-aware projection folds; profiles may interpret and rescore only by adding canonical, provenance-bearing events, never by rewriting Truth.

MyCel Core is a domain-agnostic, human-governed thought instrument whose Truth log speaks only canonical dimensions. A Profile is a tested binding of evaluators, vocabulary, tools, gates, reference material, and export targets that is applied at the Projection fold, teaching MyCel what work it is doing without poisoning Truth. Model configurations decide which intelligences participate and how they are routed. The Console skins Core control intents into a playable surface. Tilth/Quill is the original funding profile: privileged, commercially central, and deeply integrated with Golden Quill, but not the definition of MyCel.

## The Repo Tattoo

**Truth is RAW. Projection is develop. A Lens never writes. A Profile writes only provenance-bearing canonical events. No alias enters Truth.**

## MyCel as a Non-Destructive Interpretation Pipeline

MyCel is the RAW-photo model for thought.

Decision rule: For every future feature, ask: does it change the RAW or the develop?

1. **Truth is the RAW sensor capture:**
   - canonical
   - append-only
   - never edited
   - substrate-safe
   - domain-agnostic

2. **The Projection fold is develop:**
   - pure
   - deterministic
   - re-runnable
   - derived from Truth
   - never mutates RAW Truth

3. **A Lens is a develop preset:**
   - projection-only
   - zero evaluators
   - no Truth writes
   - fallback is always “show core”
   *(Under the hood, a Lens is a degenerate Profile: `evaluators: []`, `writes_truth: false`, `fallback: show_core`, `projection_only: true`)*

4. **A Profile is a develop engine:**
   - may contain evaluators
   - may rescore
   - may select which evaluator results to show
   - may alias and render canonical axes for a domain
   - may not rewrite canonical Truth
   - may not own model topology

5. **The Console is the tactile develop surface:**
   - affects playability, controls, interaction, and rendering
   - does not unlock hidden capability
   - does not bypass profile/session/model contracts

## Three-Tier Namespacing Law

1. **Axes are universal.** They are the orthogonal canonical basis.
2. **Evaluators are plural.** Different evaluators may score the same canonical axis differently in different contexts. This is not a conflict; it is provenance.
3. **Aliases are presentational.** They are skins applied at the fold. They never enter canonical Truth.

## Critical Rescore Law

A Lens never writes Truth.

A Profile rescore may write Truth, but only as a new canonical ScoreEvent with provenance.
A Profile rescore must never write a domain alias into canonical Truth.

**Correct:**
- axis_key: `structural_integrity`
- evaluator_id: `funding_rubric_structural_integrity_v1`
- profile_id: `funding_profile_v1`
- reference_corpus_id: `pa_grant_rubric_corpus_v1`
- content_version_id: `thought_object_version_abc`
- score: 0.82
- event_type: `ScoreEvent`

**Incorrect:**
- axis_key: `rubric_fit`
- score stored only in projection
- score overwrites previous score
- score lacks evaluator/profile/corpus/content provenance

## Fold Rules

1. Projection may select which ScoreEvents to display.
2. Projection may alias canonical axes.
3. Projection may show profile-specific labels.
4. Projection may show evaluator provenance.
5. Projection may show staleness.
6. Projection may not average across evaluators unless an explicit aggregator evaluator emits its own canonical ScoreEvent with provenance.
7. Projection may not hide staleness when the content version has changed after the score was produced.
8. Projection may not mutate, delete, or overwrite Truth.

## Posture Correction

Model access/session mode triplet:
- `LOCAL_ONLY`
- `HYBRID`
- `FULL_ACCESS`

Persisted V1 DataPosture enum:
- `UNRESTRICTED`
- `HYBRID`
- `SOVEREIGN`

These govern different things and must not be collapsed.
`SANITIZED` or `STERILIZED` posture modes are strictly disallowed anywhere in MyCel profile contracts. Policy may live in a profile, but the active mode is recorded on the session. A profile cannot silently become a model-routing override.

## Profile Validity Rule

A profile is invalid if any displayed domain dimension lacks:
1. a canonical core source dimension or declared derived-dimension function;
2. an evaluator binding;
3. required reference inputs;
4. a projection-only alias declaration;
5. a fallback behavior when the evaluator/input is unavailable.

# _calibration/

**STATUS: DORMANT** as of 2026-05-16 per operator scope correction. All three tracks require Tilth to generate competing grant drafts; no grant drafting / synthesis active right now. Reactivation gated on operator reactivating grant drafting. Phase-1 active scope is Pillars 1-3 only (charters + corpus + structured extraction); Pillar 4 (this directory) does not run.

When reactivated, the three-track protocol below applies. Until then, this directory holds the spec only.

---

Three-track calibration protocol per planning doc §5. Triangulates FID-depth value against shallow-card baseline.

## Track A — operator-win replay

`track_a/<win_id>/comparison.yaml` — per-win blind comparison of Tilth-shallow vs Tilth-deep vs human-written draft. Three blind reviewers (operator + 2 external) rate each draft against the funder's rubric.

Cost per win: ~$600 cash + ~8 compute-hrs + ~3 operator-hrs.

Per `feedback_no_historical_wins_as_eval_fixtures.md` (operator 2026-05-15 PM): operator's wins ARE valid for Track A here because each Track-A run involves NEW reviewers comparing deep vs shallow — not Tilth-evaluating-Tilth. Survivor-bias caveat documented in every Track-A output.

## Track B — partner-CDFI applicant pilot

`track_b/<applicant_id>/outcome.yaml` — real in-pipeline applications consenting to deep-card piloting. Funder decisions over 3-9 months. Tier-3 access only.

Optional for exemplar-pair done definition; required for scale-out validation.

## Track C — synthetic blinded panel

`track_c/<pair_id>/comparison.yaml` — 10 fictionalized applicant × opportunity pairs. Three paid blind reviewers per pair × $200/review = $6K total cash. Fast iteration.

## Pre-registration

`preregistration.signed.yaml` — operator-Ed25519-signed methodology + rubric + comparison-method + statistical-threshold posted BEFORE any draft is shown to a reviewer. Prevents methodology-cherrypicking ex post.

## Reviewer-rater agreement

Krippendorff's α per pair. If α < 0.6, pair is excluded from aggregate signal.

## Anti-conflict discipline

Blind reviewers recruited from outside Tilth's customer base + outside operator's professional network.

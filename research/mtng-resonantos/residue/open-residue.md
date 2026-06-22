# Open Residue

Unresolved questions + future tasks, with owners. Full detail in `../levels/L1-residue-map.md`.
None of these is closeable by reading the packet alone.

## Blocking (must resolve before MTNG V1 build commits)

- **R-INT — Integration mapping unperformed.** ResonantOS internals are asserted, not read;
  Phase 0 mapping admitted not done (`05`). *Owner:* MTNG author + ResonantOS maintainers.
  *Next:* read repo, run the Phase 0 working session Analog 6 recommended.
- **R-VAL — No falsifiable success criterion.** Pilot criteria are qualitative with no metric or
  baseline. *Owner:* whoever runs the pilot. *Next:* pre-register a criterion (`experiment`
  skill) against a flat-summary baseline.

## Empirical (route to `research-evidence-harness`)

- **R-CLS — Mode/Routing-Signature accuracy unmeasured** (the core failure point per Analog 6,
  Raptor, Gemini). *Next:* labeled fixtures + measured precision/recall.
- **R-OVH — Per-signal overhead unestimated.** *Next:* back-of-envelope, then measured dry run.
- **R-VPR — Post-hoc value proposition untested.** Is the packager better than a good flat
  summary + checklist? *Next:* the pilot under R-VAL's criterion.
- **R-MRG — Merge/recombination schema missing** (rules exist, algorithm doesn't). *Next:*
  author merge schema, then fixtures.

## External-source (out of this tower's reach)

- **R-OKF — OKF unverified and mis-named.** "Format" (spec) vs "Framework" (Gemini); type names
  deferred. *Next:* fetch the OKF spec, pin the name, choose OKF-compatible artifacts.

## Resolved/closing here

- **R-DST — v1-vs-v2 endorsement gap.** The Analog 6 PDF endorses v1, not the narrowed v2.
  Closing via this tower's fresh review of v2-as-written (`../REVIEW.md`).
- **R-AUT — engine autonomy boundary.** Partially addressed (`01` §9 "engine decides per
  policy"); policy unspecified → a REVIEW change request.

# Stage 7 — Interrogation (refine-design-review)

Attack on the stratified Spectralize-v2 design (RESULT.md):
- **Tension caught (zig within the dialectic):** multitaper (F2) *smooths* close partials, but the
  roughness path now uses **critical-band** roughness (F3/F4) which *also* integrates over bands — so the
  two compose rather than conflict (both deliberately discard fine partial structure that GENDYN doesn't
  stably have anyway). Not a contradiction. **Resolved.**
- **Residue (named, not hidden):** the roughness semantics change (peak-free ≠ Plomp–Levelt-over-partials).
  Must be documented + eventually validated against listeners (O1). Logged.
- **Decision exposed, not buried:** the "is a fixed perceptual model model-free?" call (F4 vs F3) is
  surfaced to the owner, not silently chosen. Good.
- Verdict: pass-with-named-residue.

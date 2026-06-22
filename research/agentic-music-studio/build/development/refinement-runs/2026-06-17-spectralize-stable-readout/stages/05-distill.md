# Stage 5 — Distill (coherent unit selection)

The five families distill to **two orthogonal axes** (representation × estimator), not five rivals — the
load-bearing insight. Selected coherent unit: a **stratified two-knob fix**:
- representation knob: drop discrete-partials → whole-spectrum moment (centroid) + critical-band
  roughness (peak-free);
- estimator knob: single-snapshot → multitaper.

**Rejected as the primary fix (with reason):**
- F5 synthesis-coupled / seed-averaging — dissolves O8 but averages away the per-take grit that IS the
  GENDYN percept (C3=1). Kept as analogy/future.
- F1 SMS alone — strong, but trades STFT-param wobble for tracking-param wobble (C2=2); folded in as an
  option for the representation knob, not the headline.

Repair target for stage 8: confirm multitaper's peak-smoothing doesn't defeat the roughness feature.

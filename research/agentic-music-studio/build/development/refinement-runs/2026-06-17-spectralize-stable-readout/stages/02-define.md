# Stage 2 — Invoke Define

**Problem defined:** Produce a timbre reading `r(spec)` (centroid, roughness, …) from a stochastic
(GENDYN) signal such that `r` is (a) deterministic given `(spec, seed)` AND (b) robust to the analyzer's
own free parameters (window/hop/threshold) — within EPS=0.05 relative drift — with no learned model.

**Define verdict:** the requirement is well-posed and falsifiable (re-run the O8 experiment on any
candidate). Single coherent target: replace the *discrete-partials × single-snapshot* readout. Pass.

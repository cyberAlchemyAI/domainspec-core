# Definitions (governed)

Canonical definitions used across this tower. These fix the *meaning* of load-bearing terms so claims and bridge decisions stay consistent. Where a definition is the paper's, it is marked PRIMARY; where it is our operating definition for the Jusbrasil call, it is marked OPERATING.

---

### Outcome prediction (the task) — OPERATING
Estimating, from information available before a ruling, the probability that a given legal matter resolves in a specified direction (here: appellate panel affirms vs reverses). In this paper the prediction is *binary and retrospective-evaluated*; for a Jusbrasil product it must become *probabilistic and forward-facing*.

### Affirm/Reverse target — PRIMARY
The label is the appellate panel's disposition relative to the first-instance decision: **Affirm** (uphold) or **Reverse** (overturn). Distribution ≈ 79% affirm / 21% reverse. This is the *only* outcome the paper predicts — not damages, not partial wins, not lawyer-side success.

### Human-expert baseline — PRIMARY
The MCC achieved by 22 experienced federal-court professionals labeling the same first-instance texts the models saw, one expert per case, 690 cases. Best individual = 0.1253. This is the comparison the paper's headline claim ("better than human experts") rests on — a *fair, same-inputs* baseline, which is its key methodological strength.

### "Better than human experts" — PRIMARY (scope-limited)
Means: best model MCC (0.3688) exceeds the best individual expert MCC (0.1253) and exceeds the group's highest CI estimate (0.226) under a 0.99 Fisher r-to-z interval. It does **not** mean the model is highly accurate in absolute terms, nor that it beats a panel deliberating with full appellate materials.

### Label provenance — PRIMARY
The target was constructed from three weak signals (case metadata, the AP-ruling filename, hand-crafted regex) combined by a ≥2-of-3 voting rule. Definitionally, the labels are *derived*, not *adjudicated ground truth* — a caveat any reuse must carry forward.

### Modest-absolute-signal — OPERATING
Our standing characterization of the result: a real, statistically defensible predictive signal whose absolute strength (MCC ≈ 0.33–0.37) is modest. Any product claim must be bounded by this — the science supports "meaningful edge," not "reliable forecast."

### "Promising results" constraint — OPERATING (anchored in PRIMARY framing)
The authors' own framing ("promising approach," "cannot replace human decision-making," "can assist courts") plus the absence of OAB/bar engagement defines a deployment constraint: an outcome-probability product is assistive decision support under professional-ethics scrutiny, not an authoritative oracle.

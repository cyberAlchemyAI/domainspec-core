# L1 — Residue Map

Named open questions, each traceable to a source and routed to a closure mechanism. IDs are
referenced from the claim ledger, gates, and `residue/open-residue.md`.

| ID | Residue | Origin | Closes via | Status |
|---|---|---|---|---|
| **R-INT** | ResonantOS architecture is asserted, not verified; Phase 0 integration mapping is unperformed. Where does Signal→Mode→Node sit vs Guardian Core / Blackboard / event bus? Who owns MTNG state long-term? | `01` §10; Analog6 §6.4; Raptor §4; `05` gap | Reading the ResonantOS repo (out of this tower's reach) → then Phase 0 mapping. **Evidence-production blocker.** | OPEN |
| **R-OKF** | "OKF" existence + correct name unverified; spec says *Format*, Gemini says *Framework*; type names deferred. | `01` §20; `07`; `05` | Fetch the OKF spec; pin the name; decide which artifacts are OKF-compatible. | OPEN |
| **R-CLS** | Mode/Routing-Signature detection accuracy unknown. Substring hints → real multi-mode decomposition is the core failure point per two reviewers. No v1 accuracy estimate. | Analog6 §6.1; Raptor §3; Gemini §3; `01` §5 | An evidence harness: labeled fixtures + measured precision/recall on fast-path vs branch decisions. | OPEN |
| **R-MRG** | Graph recombination / partial-merge has rules (`01` §17) but no schema or algorithm; merge-conflict resolution under shared synthesis targets is prose. | Analog6 §6.2; Raptor §3 | A concrete merge schema + worked conflict examples; then fixtures. | PARTIAL (rules exist, schema doesn't) |
| **R-OVH** | Per-signal overhead (latency/tokens/API calls) unestimated even for the narrowed V1. Mode detection + validation across nodes still has a cost profile. | Analog6 §6.5 | Back-of-envelope estimate, then measured dry-run on the pilot dataset. | OPEN |
| **R-VAL** | Pilot "success criteria" are qualitative ("clearer", "more actionable", "acceptable overhead") with no metric, threshold, or baseline. Cannot adjudicate pass/fail as written. | `01` §21, §25; D6 | Pre-register a falsifiable criterion (experiment skill) with a flat-summary baseline. | OPEN |
| **R-AUT** | The "not more autonomous" claim vs an engine that proposes branches/marks nodes. Where exactly is the human-in-the-loop boundary for the engine's own accept/reject of tool proposals? | Raptor §6 (D1) | Define the engine's decision authority explicitly; specify which proposals need human review. | PARTIAL (`01` §9 says engine decides "according to policy" — policy unspecified) |
| **R-DST** | The Analog 6 PDF praises **v1** (6 phases, Branch Pressure Score, 12 contribution types). v2 reviewed-now is a different, smaller design. The "validated architecture" endorsement does not cleanly transfer. | D3 | A fresh review of **v2 as written** (this tower's REVIEW.md dispatch). | CLOSING (this tower) |
| **R-VPR** | All three reviews bounded scope but none stress-tested the post-hoc value proposition itself: is a Post-Hoc Issue Packager actually better than a good flat summary + checklist? | D4 | The pilot, with R-VAL's pre-registered criterion. | OPEN |

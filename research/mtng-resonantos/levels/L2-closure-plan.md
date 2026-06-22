# L2 — Closure Plan

What this tower closes, what it hands off, and in what order.

## Closed inside this tower (source-backed understanding)

1. **Faithful corpus record** — `L0-corpus.md` (all 9 files + PDF extract).
2. **Claim adjudication** — `claim-ledger.md` separates primary-source / related-source /
   inference / analogy / operator-reading, and flags the unverified external claims.
3. **Vocabulary** — `glossary.md` + `definitions.md` for the Signal→…→Synthesis spine.
4. **Operator model** — `distill.md`.
5. **Borrow/block decisions for Arcanum** — `bridge-decisions.md`.
6. **Adversarial review of v2-as-written** — `REVIEW.md` (closes R-DST; surfaces change requests
   on R-CLS, R-MRG, R-AUT, R-VAL).

## Handed off (NOT closeable here — evidence/empirical or external-source blockers)

| Residue | Handoff target | Why this tower can't close it |
|---|---|---|
| R-INT | Read ResonantOS repo → Phase 0 mapping working session | No repo access; architecture is asserted only. |
| R-OKF | Fetch OKF spec (web) | Format not fetched; name even disputed. |
| R-CLS, R-OVH, R-VAL, R-VPR | **`research-evidence-harness`** | Need labeled fixtures, measured precision/recall, latency/token measurement, a pre-registered success criterion + baseline. Understanding is done; *data production* is the blocker. |
| R-MRG | Spec authoring then evidence harness | Needs a concrete merge schema before it can be tested. |

## Evidence-execution handoff (per the research-tower sigil)

The next blocker for MTNG is **empirical evidence production**, not more source-backed
understanding. Route to `research-evidence-harness` with:

- **Supporting artifacts:** this tower's `definitions.md` (DEF-3 branch triggers, DEF-4
  validator, DEF-5 synthesis), the pilot spec (`01` §21), the evaluation tests (`01` §25).
- **Missing mechanics:** a labeled fixture set (clean single-mode vs mixed reports), a scoring
  rubric for "branch decision correct/incorrect", a flat-summary baseline, latency/token meters.
- **Blocked claim:** Pilot Success Criteria (`01` §21) cannot be adjudicated as written (R-VAL)
  and the core value proposition (R-VPR) is untested.

## Order of operations for whoever continues

1. Pre-register a falsifiable pilot criterion (`experiment` skill) — fixes R-VAL before any run.
2. Read the ResonantOS repo; perform Phase 0 mapping — unblocks R-INT (and most "where does
   state live" maintainer questions).
3. Author the merge schema — unblocks R-MRG.
4. Build the evidence harness; run on a labeled dataset — attacks R-CLS, R-OVH, R-VPR.
5. Fetch/pin OKF — closes R-OKF.

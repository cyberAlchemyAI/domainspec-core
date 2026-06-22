# Learning Pack — MTNG for ResonantOS (v2)

> **Bridge layer (NON-SOURCE for readings).** Source-backed claims cite the packet; operator
> readings are labeled. Cutoff is honest at the bottom. Local-only.

## In one paragraph

**MTNG (Modal Tonal Nodal Graph)** is Dave Gardner's proposal to fix a real failure mode —
*one agent context asked to hold too many unresolved jobs* — by splitting a messy report into
the fewest **contracted, validated** pieces that recombine into one honest artifact. After
three outside reviews (Analog 6, Raptor mini, Gemini) all drew the same line, V1 was narrowed to
a **Post-Hoc Issue Packager**: an *offline, on-demand, selected-input, audit-first* CLI/sidecar
that turns logs + transcripts + diffs + bug notes into a developer issue packet (plus
review-only memory candidates, value-free contribution records, and an OKF export) — explicitly
**not** a live runtime orchestrator, memory promoter, or contribution valuer.

## The model you can hold in your head

`Signal → Mode → Node → Validator → Synthesis`, governed by two rules:
1. **Branch only when a contract boundary changes** (artifact / validator / tool / context /
   memory / contribution-type / safety / authority) — otherwise take the fast path. (`01` §12–13)
2. **Validate before synthesis; never flatten** — failed and partial nodes survive the merge as
   labeled status; conflicts stay `unresolved`. (`01` §17)

The cleverest idea: a **validator doubles as a misrouting detector** — a node that fails for
lack of evidence flags a reroute to a better mode, bounded to one attempt before it records
uncertainty and stops. (`01` §15)

## What to borrow into Arcanum (operator-reading)

- **Branch-only-on-named-boundary** and **validator-as-structural-gate** and
  **capture-structure-defer-valuation** all *confirm* things Arcanum already does (P1 dispatch
  triggers, check-tension, register-dispatch). Treat MTNG as **supporting precedent**, not new
  machinery. (see `bridge-decisions.md` BD-1/2/3)
- The one genuinely novel primitive worth a future look is the **node contract** (BD-9) vs
  `task-session`.

## What to keep analogy-only or block

- `closed_result ↔ exit_reason` and "don't hide conflict ↔ P10": nice mirrors, **analogy-only** —
  don't merge vocabularies.
- **Block:** MTNG-as-runtime, the numeric Branch Pressure Score (deferred even by the spec),
  substring "Routing Signature" classification.
- **future-work:** OKF — unverified and even mis-named.

## What is strong, what is missing (the review in brief)

**Strong:** accurate problem diagnosis; contracts-and-validators as an inspectable delegation
primitive; disciplined non-goals; the validator-as-router idea; the v2 narrowing itself.

**Missing / unproven (the change requests live in `REVIEW.md`):**
- **Phase 0 integration mapping is unperformed** — the host architecture MTNG must plug into is
  asserted, not mapped (R-INT). *Build-blocking.*
- **No falsifiable success criterion** — pilot criteria are qualitative, no baseline (R-VAL).
- **Classifier accuracy unmeasured** — substring→mode is the named core failure point (R-CLS).
- **Merge/recombination has rules but no schema/algorithm** (R-MRG).
- **Overhead unestimated** (R-OVH); **value proposition untested** vs a good flat summary (R-VPR).
- The Analog 6 PDF endorses **v1**, a larger design — its "validated architecture" praise does
  not cleanly transfer to the narrowed v2 (R-DST).

## Bottom line

The design is **review-ready, not build-ready.** The narrowing is genuinely good engineering
judgment; but scope was bounded, value was not proven and the host was not mapped. The honest
next steps are not code: (1) pre-register a falsifiable pilot criterion, (2) read the ResonantOS
repo and run Phase 0, (3) author a merge schema, (4) build an evidence harness to measure
classifier accuracy / overhead / value, (5) pin OKF.

## Honest cutoff

- **No ResonantOS repository was read** — all architecture claims are asserted (R-INT).
- **OKF was not fetched** and its name is disputed in the corpus itself (R-OKF).
- The Analog 6 PDF reviews **v1**; this tower reviews **v2**. Where they diverge, the ledger says so.
- Source date checked: **2026-06-22**; packet frozen **2026-06-17**.

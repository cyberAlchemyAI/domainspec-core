# DomainSpec Paper — Research-Readiness Ledger

- **Dispatch:** `domainspec-paper-evidence-hardening-20260610` (child of `domainspec-paper-update-research-20260610`)
- **Spell anchor:** `arcanum/spells/publication-research-pipeline`
- **Date:** 2026-06-10
- **Mode:** read-only + dry-run. **No live runs. No claim-status changes.** (gates `dry-run-before-live`, `claim-status-freeze`)
- **Lanes:** research-tower (phase 2), research-evidence-harness dry-run (phase 4), definitions-governance — all returned.

---

## Actioned 2026-06-10

- **Two-copy divergence RESOLVED** — the corrected research copy was forward-ported onto `implementation/domainspec/docs/research/domainspec-paper.md`; the two are now byte-identical (verified). The implementation copy's integrity regressions (unhedged §6.5, "three structural properties", missing DS-M13, Saga dropped from enumeration) are gone.
- **Refs [13] and [16] fixed with verified arXiv IDs** — [13] → A. Cunha & N. Macedo, "Validating Formal Specifications with LLM-generated Test Cases," arXiv:2510.23350, 2025; [16] → L. Miculicich et al., "VeriGuard: Enhancing LLM Agent Safety via Verified Code Generation," arXiv:2510.05156, 2025. Both author names in the original were correct; only titles/IDs were placeholders.
- **§2.5 VeriGuard claim corrected** — VeriGuard does not use TLA+; reworded to "formally verifies LLM-generated agent policies against synthesized safety specifications."
## Reference-integrity pass 2026-06-10 (full one-pass cleanup)

The reference list was renumbered to 31 contiguous entries (was 32), and now every reference is cited at least once and every inline citation resolves (verified programmatically). Fixes applied:

- **RW3 — [17] Mixture-of-Experts** replaced with a correct multi-agent reference (M. Wooldridge, _An Introduction to MultiAgent Systems_, Wiley, 2009).
- **RW5 — [1]==[14] duplicate SWE-bench** deduped: removed the duplicate, redirected the §2.5 citation to [1].
- **§1 mis-citation** fixed: "SWE-agent [1]" pointed at the SWE-bench ref → corrected to the SWE-agent ref.
- **4 orphaned references now cited** in natural homes: Kruchten 4+1 →§2.7, Kahneman →§6.2, Meadows "Leverage Points" →§6.6, Guarino "Formal Ontology" →§9.1.
- Both paper copies re-synced identical after the pass.

Checked and **clean (no fix needed):** all table totals (§8.2 89/445/146/41; §8.3 sums to 445 / 100%), meta-type and edge enumerations vs stated counts (14+11=25; 12+3+8+6=29), derivation-rule counts (δ1–δ20, O1–O16), and definition/property/table numbering.

## Definitions-canon pass 2026-06-10 (DC1–DC4 applied)

Applied to `research/projects/domainspec/definitions/DEFINITIONS.md` and the mars E11 runbook:

- **DC1** — DS-D1/DS-D2 "Paper baseline profile (24/26)" relabeled to "Pre-composition baseline profile (… historical — published papers report only the 25/29 extension profile)." No paper reports 24/26, so the old label was misleading.
- **DC2** — added a normative **canon boundary** note after DS-D2: canonical = 25/29 (shipped TAXONOMY/RELATIONSHIPS); the ~38-edge / 7+4-category study is **proposed, not adopted**.
- **DC3** — added the **DS-M13 ↔ E11 SC-TS crosswalk** table (PrecisionF1=SC-TS-5, ApplicabilityRate=SC-TS-1, AmbiguityRate=dual-rater ≤15%, TradeoffCompleteness=SC-TS-2).
- **DC4** — added a disambiguation note to the mars runbook: execution task IDs `T1`–`T9` are a distinct namespace from technique-catalog codes `T01`–`T24` (note, not rename, to avoid breaking cross-references).

- **RW4 resolved (no change needed):** ADLC is a term defined in C. West's "The Agentic Manifesto," so the body↔ref citation is correct as written.

- **Still open (your call):** RW6 [22] Boscaro "Domain-Code-Mapping" self-citation disclosure (future-dated 2026, cited as the Meta-Track antecedent). Live experiments (E7, §8 SPEC materialization, E11 re-adjudication) remain owner-gated.

## 0. Verdict summary

The paper update is sound, but evidence hardening surfaced **one root-cause defect and four publication-grade integrity items** that the earlier hedges only papered over. Promotability of the three hedged flags:

| Flag | Spell phase | Promotion verdict | Blocker |
|------|-------------|-------------------|---------|
| §8 case-study counts (89/445/146, 1·4·1·1) | 4 | **promotable-on-live-run** | No experiment needed — run the derivation extractor over the 7 feature SPECs. But **6 of 7 SPECs are not materialized**; only `auth-access-control` exists. Blocked on artifact materialization, not protocol. |
| §6.5 signal-emission rate (E7) | 4 | **hold-insufficient (needs-protocol-first)** | E7 + the E5 separated-observer arm are not implemented; live `signals.jsonl` is 0 rows. The 30–40%→60% figures stay *projected*. |
| E11 / DS-M13 promotion | 6 | **hold-insufficient (needs-protocol-first)** | D4 passed only under a single human acting as all three raters. Needs ≥2 independent human raters + third-rater, Fleiss/Cohen κ ≥ 0.60. No κ statistic exists yet. |

**Net:** none of the three can be promoted from this route (as designed — the freeze gate held). One (§8) is cheap to make reproducible; two require real experiments.

---

## 1. ROOT-CAUSE DEFECT (highest priority)

**The two paper copies have diverged, and the base copy carries a research-integrity regression.**

The recent base — `implementation/domainspec/docs/research/domainspec-paper.md` — which we copied *from*, still:
- asserts the **unhedged** "23 signals / ~30–40%" §6.5 numbers as measured fact (base lines 490–494) — the exact overclaim our update fixed in the research copy;
- omits **DS-M13** and still says "three structural properties" (Properties 1–4 only);
- **omits Saga from the `M_B` enumeration** while claiming "14 backend types" (base lines 221, 225–226) — enumerated set is only 13;
- lacks the §4.1 technique-exclusion paragraph and the §9.4 E11 paragraph.

So the *updated research copy is now ahead of and more correct than the "recent base."* This inverts the assumption that started the task.

**Recommended action (needs your decision):** either (a) forward-port the updated research copy back onto the implementation base so they re-converge, or (b) formally mark the implementation copy as an archived snapshot. Until one is done, "which copy is canonical" is ambiguous — the same drift that started this whole task.

---

## 2. PUBLICATION-INTEGRITY ITems (definition-fix / editorial — from the tower lane)

These are real paper-quality defects, independent of the evidence experiments. Surfaced by research-tower §2 review:

| ID | Item | Source | Fix class |
|----|------|--------|-----------|
| RW1 | **Ref [13]** "Cunha et al., arXiv:**2501.xxxxx**" — literal placeholder arXiv ID, likely fabricated | §2.4 / refs | must fix before publication |
| RW2 | **Ref [16]** "Miculicich et al., VeriGuard, arXiv:**2502.xxxxx**" — literal placeholder | §2.5 / refs | must fix before publication |
| RW3 | **Ref [17]** Shazeer MoE cited to support "multi-agent architectures" — MoE is not multi-agent; mismatched citation | §2.6 | fix citation |
| RW4 | **Ref [19]** body says "ADLC / Agentic Delivery Lifecycle"; ref list says "The Agentic Manifesto" — name mismatch, grey-lit | §2.6 | reconcile name |
| RW5 | **[1] == [14]** — same SWE-bench paper cited twice | refs | dedupe |
| RW6 | **[23]** "Domain-Code-Mapping, GitHub, 2026" — internal/future-dated repo presented as the Meta-Track literature antecedent | §2.7 | disclose as sibling repo, not literature |
| RW7 | Paper omits the in-repo **Lean formalization** (relevant to §9.3 SMT claims) and **MARS** (source of E11's catalog) — disclose if leveraged | §9.3 | optional disclosure |

RW1–RW2 are the sharpest: placeholder arXiv IDs in a submission read as fabricated references. RW3–RW6 are quick editorial fixes. None can be "resolved by inference" — they need your source knowledge (the real arXiv IDs, or restating the claims without those refs).

---

## 3. DEFINITION-CANON FIXES (definitions-governance lane)

Drift confined and mostly traceable to §1's two-copy divergence, plus:

| ID | Item | Fix class |
|----|------|-----------|
| DC1 | DEFINITIONS.md labels 24/26 the "Paper baseline profile," but no current paper reports 24/26 — orphaned label | relabel to "pre-composition baseline (historical)" |
| DC2 | Promote the "**~38-edge study is PROPOSED, not adopted**" guard from the ops brief into DEFINITIONS.md as a normative note, so it survives independent of ops | add normative note |
| DC3 | DS-M13 thresholds named two ways (DEFINITIONS: PrecisionF1/ApplicabilityRate/… ; E11 protocol: SC-TS-5/SC-TS-1/…) — values match (0.75/0.80/0.15/0.85), mapping implicit | add DS-M13 ↔ SC-TS crosswalk |
| DC4 | T-code namespace collision: technique catalog `T01–T24` vs mars E11 runbook task IDs `T1–T9` | cosmetic — namespace the runbook IDs |

The ADOPTED (25/29) vs PROPOSED (~38) boundary is currently **clean** in all shipped files and both papers — keep it that way (DC2 hardens it).

---

## 4. DRY-RUN EVIDENCE ARTIFACTS PRODUCED (phase 4)

The harness lane authored validated (not collected) run-schemas + fixtures for each flag, ready for a future approved live run:
- **E7 / §6.5:** per-session schema (`expected_signal_count`, `actual_signal_count`, `emission_rate`, `agent_mode` arm), target `≥0.60` separated vs `~0.30–0.40` unified; needs ≥30 rows incl. ≥10 under a real separated-observer agent.
- **§8 counts:** per-feature `case-study-counts.jsonl` (7-row census), schema-valid iff `concept_count == len(concept_ids)` and `tests_derived == Σ tests_by_rule`; aggregates must hit 89/445/146 + verdict histogram.
- **E11:** multi-rater adjudication schema with `rater_id` (≥3 distinct identities), Fleiss/Cohen κ ≥ 0.60 floor + DS-M13 validity vector; re-adjudicate the frozen 35-row subset.

Full schemas/fixtures in the harness receipt (not yet persisted to a file — available on request).

---

## 5. NEXT-ROUTE HANDOFF (each requires separate operator approval)

1. **Resolve the two-copy divergence** (§1) — forward-port or archive the implementation base. *Highest priority; it is the root cause of most definition drift.*
2. **Apply RW1–RW6 + DC1–DC4 editorial/definition fixes** — bounded, no experiments; mostly safe, but RW1–RW2 need the real citations from you.
3. **Materialize the 6 missing feature SPECs + run the derivation extractor** → makes §8 counts reproducible (`promotable-on-live-run`).
4. **Run E7 (with the E5 separated-observer arm)** → promotes §6.5 from projected to measured.
5. **Recruit ≥2 independent raters + re-adjudicate E11** → lifts the single-reviewer override, enabling the DS-M13 / C2 claim delta.

Items 3–5 are the live experiments the `dry-run-before-live` gate deliberately deferred; the schemas to run them now exist.

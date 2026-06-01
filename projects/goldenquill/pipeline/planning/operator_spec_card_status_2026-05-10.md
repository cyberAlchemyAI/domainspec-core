---
title: Operator spec-card + research-artifact status — discovery report
filed: 2026-05-10
operator: Josh
authority: orchestrator discovery dispatch — surface status on three tracked artifacts not yet on v0.1 Beta critical path + de-dup "yesterday's research" backlog
disposition: status report only — no LOCK ceremony, no amendments, no new spec cards authored
audit_class: operator-decision-support
---

# Executive summary

Three operator-tracked artifacts are filed on disk as DISPATCH_SPEC_DRAFTs or design-memo-plus-handoff bundles. Two are operator-decision-blocked, one is dispatch-ready.

1. **Funding Goal spec card** (12 OQs) — operator must answer **OQ-1 ship window first** (v0.1 Beta / v0.2 first wave / v0.2 second wave; spec recommends v0.2 first wave). Once OQ-1 lands, ~3-4 sessions to LOCK.
2. **Reflection** — synthesis design memo + pre-staged v0.1 Beta hook handoff packet already on disk; **no separate "design spec card" needed for the v0.1 hook** — the handoff IS the dispatch artifact. **Fire-ready as a Thesis round NOW.** v0.2 SPEC + v1.x runtime stages still need authoring (one spec card each).
3. **Watts per Funding Action (WPFA)** — operator-LOCKED at v0.1 Beta scope today; defaults stand per "ready for Thesis dispatch." **Fire-ready NOW.** ~3-4 sessions to LOCK.

Beyond the three tracked artifacts, the surfaced research backlog contains **eight ideas-from-research** not yet absorbed into LOCKED amendments or in-flight dispatch. The biggest is a fourth standalone artifact — **Reflection Packet** (sibling to WPFA, distinct from §15 Archivist Reflection sub-mode) — currently research-only at `pipeline/research/reflection_packet_grounding/findings_2026-05-10.md`. **It is the next derivable spec card** if operator wants to go beyond the three tracked items.

---

# §1. Funding Goal spec card

**Path on disk.** `pipeline/planning/funding_goal_amendment_spec_2026-05-10.md`

**Status.** DISPATCH_SPEC_DRAFT — pre-Thesis dispatch packet; no LOCK ceremony. Self-check complete (§12 of the spec).

**Open questions.** 12 total (OQ-1 through OQ-12). Each carries trade-offs and a recommended default.

- **OQ-1 — Ship window (largest).** v0.1 Beta / v0.2 first wave / v0.2 second wave. Spec recommends **v0.2 first wave** because v0.1 Beta is paper-light per the readiness audit and adding a compound LOCK family extends Beta scope.
- OQ-2 — §6 vs §3 amendment shape (default: both, paired).
- OQ-3 — Past-deadline goal at construction: reject vs WARNING (default: reject).
- OQ-4 — RED severity on blocked goals (default: RED).
- OQ-5 — Status mutation: thin resolution helper vs seat-side walk (default: thin helper).
- OQ-6 — `FundingGoal.purpose` default classification: shareable vs confidential (default: shareable).
- OQ-7 — `scoring-callable` as new §0.5 primitive_kind vs route under interface-contract (default: interface-contract).
- OQ-8 — Status transition closure permissiveness (default: as proposed in §6).
- OQ-9 — F-GOAL-SCHEMA-INVALID family: sub-code collapse vs one-module-per-code (default: collapse, matches §4 v2.x precedent).
- OQ-10 — F-GOAL-* in F-CLASS-COVERAGE-INCOMPLETE META gate (default: exclude).
- OQ-11 — Match DB schema bump v1→v2: migration shim vs schema-of-record only (default: schema-of-record only).
- OQ-12 — Push-notify v0.1 surface scope (default: D + A only — CLI-on-next-run + Monday brief).

**Dispatch readiness.** Operator-decision-needed-first on **OQ-1 only**. All other OQs have defaults that survive Thesis. Once OQ-1 lands (or operator confirms default), **fire-ready as a Thesis round**.

**Compound LOCK shape.** §2 v7.3 + §6 ??/§3 v6 + §4 v2.x.1 follow-on + §0.5 v16 amendment. Anticipated rows ≥ 198 (subject to ordering with WPFA + Reflection v0.1 hook).

**Estimated sessions to LOCK.** 3-4 sessions = 1 spec card revision absorbing OQ-1 + 1 Thesis Cycle 1 + 1 Thesis Cycle 2 + 1 compound-LOCK ceremony with companion edits.

**Pre-staged handoff.** None yet — spec card has not yet been promoted to a handoff packet (blocked on OQ-1). When OQ-1 lands, a handoff at `pipeline/handoffs/ws_fg_funding_goal_handoff_<date>.md` is the derivable next artifact.

---

# §2. Reflection — design memo + pre-staged handoff

**Paths on disk.**

| Artifact | Path |
|---|---|
| Five-lane research | `pipeline/research/reflection/lane_{1,2,3,4,5}_*.md` |
| Pre-Thesis scoping draft | `pipeline/research/reflection/scoping_draft_reflection_as_archivist_submode.md` |
| Synthesis design memo (canonical design) | `pipeline/research/reflection/synthesis_design_memo_2026-05-10.md` |
| Pre-staged v0.1 Beta hook handoff packet | `pipeline/handoffs/ws_reflection_v0_1_hook_handoff_2026-05-10.md` |

**Status.** Synthesis design memo is design-complete (§1-§11 closed). Pre-staged dispatch packet is authored per CLAUDE.md proactive pre-staging. **No formal "spec card" artifact** in the `pipeline/engineering/engineering_process_v0.1.md` §11 sense — but the synthesis memo + handoff packet bundle covers the same surface area as a spec card.

**Does a separate design spec card need to be authored?** The operator's note said "no design spec card yet — that's the next dispatch if you want it." Reading both artifacts:

- For **v0.1 Beta hook** (dormant Cedar/Python gate primitives only — 17 net-new F-REFLECTION-* + 5 sub-tag extensions on existing F-ARCHIVIST-*): **NO separate spec card needed.** The synthesis memo §7.1 specifies the three artifacts (arch v7.0.9 + §4 v2.x.2 + §0.5 §15.x sub-amendment) and the handoff packet at `pipeline/handoffs/ws_reflection_v0_1_hook_handoff_2026-05-10.md` is the dispatch artifact. **Fire-ready as a Thesis round NOW.**
- For **v0.2 SPEC-only** (full Reflection sub-mode SPEC LOCK; mirrors §13/§14/§15 v0.2 SPEC-ONLY discipline): **separate spec card recommended** per the §11/§12/§13/§14 precedent. Not yet authored. Estimated authoring cost: medium (mirrors WS-K §15 pattern).
- For **v1.x runtime** (predicate bodies + reflection_agent + scheduled cadence): **separate spec card recommended.** Not yet authored. Estimated authoring cost: high.

**Open questions remaining for operator review (synthesis memo §9, 5 items).**

1. Top-level F-REFLECTION-* (default: 17 top-level + 5 sub-tag) vs purist all-sub-tag-under-F-ARCHIVIST-* (22 sub-tags across 5 parents).
2. Reflection cadence: third top-level cadence vs sub-mode of quarterly (default: third cadence).
3. Heavy-Judge swap analog for end-of-quarter consolidations at v1.x (default: ship; cost = NVMe + ~2-5 min wall).
4. Probe registry membership for `F-REFLECTION-PROBE-COVERAGE-INCOMPLETE` (default: 4 probe families — sycophancy, loop_divergence, fabrication_on_failure, proxy_metric_drift).
5. Inoculation-frame template wording — **operator-voice required per CLAUDE.md "Applicant brings substance."** Lane 5 F-4 evidence base only.

**Dispatch readiness.**

- **v0.1 Beta hook: fire-ready as a Thesis round NOW.** No operator decisions block it (all 5 OQs above are v0.2/v1.x scope). Cycle-1 dispatch via the bridge pattern (Editor=Llama/Groq + Judge=Gemini/Google + Red Team=GPT-OSS/Groq).
- v0.2 SPEC: blocked on Q1/Q2 operator decisions + on v0.1 Beta hook LOCK.
- v1.x runtime: blocked on v0.2 SPEC LOCK + Q3/Q4/Q5 operator decisions.

**Compound LOCK shape (v0.1 Beta hook).** Three rows: architecture v7.0.9 amendment + §4 v2.x.2 sub-amendment + §0.5 §15.x sub-amendment. Anticipated next-sequential rows (~200/201/202 after row 199 §4 v2.x.1 LOCK).

**Estimated sessions to LOCK (v0.1 Beta hook).** 2-3 sessions per handoff packet's `session_estimate` line — 1 author session + 2 Thesis cycles. Does NOT block v0.1 Beta close-out (parallel work).

**Pre-staged handoff.** `pipeline/handoffs/ws_reflection_v0_1_hook_handoff_2026-05-10.md` — under 50 lines, self-contained per CLAUDE.md handoff discipline. Coordinator can fire when bandwidth opens.

---

# §3. Watts per Funding Action (WPFA) spec card

**Path on disk.** `pipeline/planning/watts_per_funding_action_spec_2026-05-10.md`

**Status.** DISPATCH_SPEC_DRAFT — pre-Thesis dispatch packet. Per operator LOCKED-2026-05-10 directive: v0.1 Beta scope; buyer-facing PDF is sales lever (NOT deferred); defaults stand. Self-check complete (§16 of the spec).

**Open questions.** 11 Josh-facing (OQ-A through OQ-K) + 9 Thesis-resolvable (OQ-1 through OQ-9) + 2 operator-proposed DECISIONS-PENDING-CONFIRMATION (DPC-1 quarterly baseline cadence, DPC-2 methodology disclosure level).

- All 11 Josh-facing OQs carry recommended defaults that the spec marks as operator-confirmable rather than operator-blocking. Spec text explicitly says "defaults stand, ready for Thesis dispatch" per today's operator directive.
- Highlights:
  - OQ-A: §17 section number (default §17).
  - OQ-B: §0.5 row range — Scenario A (rows 400-431 if Funding Goal locks first) vs Scenario B (rows 377-408 if WPFA locks first; recommended per operator-LOCKED-2026-05-10 directive).
  - OQ-E: F-WPFA-OPERATOR-SIGNATURE-MISSING M13 bypass — NOT permitted (default; structural attestation boundary).
  - OQ-J: dashboard refresh model — operator-on-demand at v0.1 (default).

**Dispatch readiness.** **Fire-ready as a Thesis round NOW.** No operator-decision-blocking OQs per operator directive. All defaults are Thesis-overrideable but not Thesis-blocking.

**Compound LOCK shape.** §17 v1 (new section) + §4 v2.x.z F-WPFA-* family + Coefficient Registry signed-asset spec + §0.5 v17 amendment. Anticipated rows ≥ 200. 32 §0.5 rows.

**Estimated sessions to LOCK.** 3-4 sessions = 1 spec card consolidation + 1 Thesis Cycle 1 + 1 Thesis Cycle 2 + 1 compound-LOCK ceremony + companion edits (Cycle Accountant module skeleton + Coefficient Registry signed-asset class + buyer-facing PDF template + operator dashboard).

**Pre-staged handoff.** None yet — spec card has not been promoted to a handoff packet. When operator greenlights dispatch, a handoff at `pipeline/handoffs/ws_wpfa_handoff_<date>.md` is the derivable next artifact.

**Sibling-not-nested note.** WPFA shares the cycle-close trigger + Logfire span tree with the Reflection Packet (see §4 below). Hard discipline per spec §13.1: zero shared output, zero shared consumer, zero shared schema. WPFA and Reflection Packet do NOT compose at v0.1.

---

# §4. Yesterday's research — surfacing eight ideas not yet absorbed

Deduplicated against LOCKED amendments (rows 178-199 today) + in-flight dispatch (handoff packets under `pipeline/handoffs/`) + the v0.2 dispatch plan (`pipeline/planning/v0_2_dispatch_plan_2026-05-09.md`) + the v0.1 Beta readiness audit. Each item has a clear next step.

## §4.1 Reflection Packet (sibling artifact to WPFA — biggest unabsorbed surface)

**Path on disk.** `pipeline/research/reflection_packet_grounding/findings_2026-05-10.md`

**What it is.** Per WPFA spec card §0 + §3 (sibling-artifact frontmatter line): a typed Pydantic BaseModel emitted at every cycle close, distinct from the §15 Archivist Reflection sub-mode design. Consumes the same Logfire span tree as WPFA. Different consumer: feeds the Archivist learning loop, not the operator dashboard or buyer PDF. The 5-lane research file (Hermes / Dreaming / Academic / Pydantic AI / Field-failures) IS the grounding research for this artifact — but the design synthesis at `pipeline/research/reflection/synthesis_design_memo_2026-05-10.md` is currently aimed at the §15 sub-mode, not the cycle-close packet emission shape.

**Status.** Research findings only. No spec card. No design synthesis distinct from the §15 Archivist sub-mode synthesis. **The disambiguation is itself an open question** — the WPFA spec card cites `F-REFLECTION-SPAN-PROVENANCE-MISSING` as a sibling-failure-code, but the synthesis memo's F-REFLECTION-* family is aimed at the Archivist sub-mode. These may or may not be the same family.

**Why it strengthens Tilth.** The cycle-close packet emission is the load-bearing input substrate for the §15 Archivist Reflection sub-mode at v1.x runtime. It is also the cycle-close grounding signal for the Match DB outcome rollup at v1.x. Without a packet emission spec, the Archivist Reflection sub-mode has no defined input shape at v0.2 SPEC LOCK time.

**Next step.** Author a Reflection Packet spec card distinct from the §15 sub-mode synthesis — sibling-not-nested with WPFA — clarifying the disambiguation. ~1-2 sessions. Operator decision needed first on whether this is a v0.1 Beta scope (sibling with WPFA) or v0.2 horizon (sibling with §15 v0.2 SPEC LOCK).

## §4.2 v0.1 Beta launch posture documentation

**What it is.** README.md + CLAUDE.md + docs/ARCHITECTURE_OVERVIEW.md need a "v0.1 Beta launch posture" section per `pipeline/planning/v0_1_beta_readiness_2026-05-10.md` §2.6 + §3.2. Paper-light, no LOCK ceremony.

**Status.** Not authored. Flagged in v0_1_beta_readiness as remaining paper-light v0.1 Beta item.

**Why it strengthens Tilth.** Closes the v0.1 Beta cut documentation gap. Without it, README/CLAUDE.md/ARCHITECTURE_OVERVIEW describe the product surface as if it's pre-v0.1.

**Next step.** Single Cowork session, ~1 session. Operator-decisions-not-needed.

## §4.3 Heavy-Judge swap analog for Reflection (v1.x horizon)

**What it is.** Synthesis memo §9 Q3: on-demand 200B-class local model loaded for end-of-quarter Reflection consolidations, mirroring Anthropic's opus-4-7 selection for Dreams pipeline. NVMe + ~2-5 min wall per heavy cycle.

**Status.** Open question only. Not in any LOCKED amendment.

**Why it strengthens Tilth.** Symmetry with §4 Logician's existing heavy-Judge swap pattern (per v7.0.4 + v7.0.7 + CLAUDE.md). Without it, Reflection at v1.x runs on the routine 70B-class local model only — Lane 5 evidence suggests this is sufficient but Anthropic's choice is the cross-reference.

**Next step.** Operator decision at v0.2 SPEC LOCK time (not blocking v0.1 hook). No spec card needed yet.

## §4.4 Reflection probe registry — 4 probe families

**What it is.** Synthesis memo §9 Q4: `F-REFLECTION-PROBE-COVERAGE-INCOMPLETE` META-gate (#16 in the synthesis §4.3 table) requires a registry of probe families — sycophancy_probes, loop_divergence_probes, fabrication_on_failure_probes, proxy_metric_drift_probes. Each is non-trivial design work.

**Status.** Named at architectural-primitive layer in the synthesis memo. No probe-family design synthesis. Realization deferred to v1.x runtime per synthesis §7.3.

**Why it strengthens Tilth.** Without a probe registry, the META-gate has no enforceable coverage check — `F-REFLECTION-PROBE-COVERAGE-INCOMPLETE` becomes a dormant stub that never activates.

**Next step.** Probe-family design synthesis per probe (one design pass each = ~4-5 sessions). v1.x runtime work; can pre-stage at v0.2 SPEC LOCK time as a follow-on registry.

## §4.5 Inoculation-frame template wording (operator-voice required)

**What it is.** Synthesis memo §9 Q5: `F-REFLECTION-INOCULATION-FRAME-MISSING` requires a fixed-string "self-improvement-as-acceptable" inoculation frame in the Reflection prompt template, per Anthropic's emergent-misalignment paper (Lane 5 F-4). Synthesis flags but does not draft template wording.

**Status.** Open question only. Operator-voice required per CLAUDE.md "Applicant brings substance."

**Why it strengthens Tilth.** Without the inoculation frame, Reflection prompts at v1.x runtime risk the Anthropic-documented misalignment-generalization path.

**Next step.** Operator drafts inoculation-frame template wording in their idiom. ~1 session of dialogue. Cycle-1 Thesis-author task once v0.2 SPEC LOCK is in motion.

## §4.6 Reflection vs Reflection Packet F-REFLECTION-* disambiguation

**What it is.** The synthesis memo's F-REFLECTION-* family (17 top-level codes at §4.3) is named generically. The WPFA spec card cites `F-REFLECTION-SPAN-PROVENANCE-MISSING` as a sibling-family code that pairs with `F-WPFA-SPAN-PROVENANCE-MISSING`. These may or may not be the same code-family. The synthesis memo's `F-REFLECTION-FABRICATION-ON-FAILURE` (POST-effect) is also a candidate sibling for a WPFA equivalent.

**Status.** Disambiguation not yet performed. Surfaces when both spec cards (Reflection v0.1 hook + WPFA + the unwritten Reflection Packet spec card) dispatch in parallel.

**Why it strengthens Tilth.** Without a disambiguation pass, the §4 v2.x.2 amendment from the Reflection v0.1 hook handoff may collide with a future §4 v2.x.z amendment from WPFA when registered against §0.5.

**Next step.** Brief reconciliation note authored before the Reflection v0.1 hook Thesis dispatch fires. ~10 min of architectural-naming triage. Worth doing as a tiny pre-Thesis pass.

## §4.7 Reflection cadence vs §15 weekly/quarterly cadences

**What it is.** Synthesis memo §9 Q2: Reflection lands as a third top-level Archivist cadence (default — synthesis recommendation) or as a sub-mode of quarterly cadence (alternative — naturally aligned with Match DB outcome cadence at quarter boundary).

**Status.** Open question only. Not blocking the v0.1 Beta hook (cadence decision lands at v0.2 SPEC LOCK time).

**Why it strengthens Tilth.** Operator-facing cadence vocabulary clarity. Three top-level cadences (weekly / quarterly / reflection) means three independent invocation surfaces; sub-mode-of-quarterly means one less invocation but tighter coupling to funder outcome cadence.

**Next step.** Operator decision at v0.2 SPEC LOCK time. No spec card needed.

## §4.8 Section E carve-out documentary hygiene

**What it is.** Per the daily_log 2026-05-10 entry "Docs hygiene: Cowork→openclaw bridge + Section E discipline landed in primary surfaces": WS-C v7.0.4 reflexively defaulted to Section E carve-out citing "multi-provider routing may not yet be live" — but routing has been live since 2026-04-19 and was proven live the same calendar day. Hygiene pass landed in AGENTS.md + SESSION_BOOTSTRAP.md + CLAUDE.md.

**Status.** Landed already today. Not a backlog item but a closure-noted-for-completeness.

**Why it strengthens Tilth.** Prevents future WS sessions from defaulting to Section E without a logged dispatch failure.

**Next step.** Already landed. No further action needed.

---

# §5. Summary table

| # | Artifact | Path | Status | Operator-decisions-needed-first? | Dispatch-ready now? | Est. sessions to LOCK | Pre-staged handoff |
|---|---|---|---|---|---|---|---|
| 1 | Funding Goal spec card | `pipeline/planning/funding_goal_amendment_spec_2026-05-10.md` | DISPATCH_SPEC_DRAFT | **Yes — OQ-1 ship window** | No (blocked on OQ-1) | 3-4 | No |
| 2 | Reflection v0.1 Beta hook | `pipeline/handoffs/ws_reflection_v0_1_hook_handoff_2026-05-10.md` | Pre-staged dispatch packet (synthesis at `…/synthesis_design_memo_2026-05-10.md`) | No (5 OQs are all v0.2/v1.x scope) | **Yes** | 2-3 | **Yes** |
| 3 | Reflection v0.2 SPEC-only | not authored | Open question; needs spec card | Yes (Q1 + Q2 from synthesis memo §9) | No | 3-4 (after v0.1 hook LOCK) | No |
| 4 | Reflection v1.x runtime | not authored | Open question; needs spec card | Yes (Q3 + Q4 + Q5 from synthesis memo §9) | No | 5-8 (after v0.2 SPEC LOCK) | No |
| 5 | WPFA spec card | `pipeline/planning/watts_per_funding_action_spec_2026-05-10.md` | DISPATCH_SPEC_DRAFT | No (operator-LOCKED 2026-05-10; defaults stand) | **Yes** | 3-4 | No |
| 6 | Reflection Packet (sibling to WPFA) | `pipeline/research/reflection_packet_grounding/findings_2026-05-10.md` | Research findings only | Yes (disambiguation with §15 sub-mode + v0.1 vs v0.2 scope) | No | 1-2 (spec card) + 3-4 (LOCK) | No |
| 7 | v0.1 Beta launch posture docs | not authored | Flagged in `pipeline/planning/v0_1_beta_readiness_2026-05-10.md` | No | **Yes** (paper-light) | 1 | No |
| 8 | Heavy-Judge swap analog for Reflection | open Q only (synthesis §9 Q3) | Open question | Yes (v0.2 SPEC LOCK time) | — | — | — |
| 9 | Reflection probe registry (4 families) | open Q only (synthesis §9 Q4) | Open question | Yes (v1.x runtime time) | — | 4-5 sessions per probe | — |
| 10 | Inoculation-frame template wording | open Q only (synthesis §9 Q5) | Open question; operator-voice required | Yes | — | 1 dialogue session | — |
| 11 | F-REFLECTION-* vs WPFA disambiguation | not authored | Disambiguation pass needed | No | **Yes** (tiny pass) | 0.2 | No |
| 12 | Reflection cadence (third top-level vs quarterly sub-mode) | open Q only (synthesis §9 Q2) | Open question | Yes (v0.2 SPEC LOCK time) | — | — | — |

---

# §6. Recommended dispatch ordering (operator-suggested defaults)

If operator wants to fire dispatches in parallel with v0.1 Beta close-out (Intake full-impl, Uploader full-impl, Classification Review UX, WS-L LOCK, v0.1 Beta launch docs):

1. **Fire-ready now (parallel to Beta close-out):**
   - Reflection v0.1 Beta hook (item 2) — dispatch packet ready; LOW cost.
   - WPFA spec card (item 5) — operator-LOCKED today; defaults stand.
   - F-REFLECTION-* vs WPFA disambiguation (item 11) — tiny pass, do before Reflection v0.1 hook Thesis fires.
2. **Operator-decision-then-fire (one OQ each):**
   - Funding Goal spec card (item 1) — OQ-1 ship window.
   - Reflection Packet (item 6) — disambiguation + v0.1 vs v0.2 scope.
3. **Paper-light docs (any time):**
   - v0.1 Beta launch posture documentation (item 7).
4. **v0.2 SPEC LOCK time:**
   - Reflection v0.2 SPEC-only (item 3).
   - Reflection cadence decision (item 12).
   - Heavy-Judge swap analog (item 8).
5. **v1.x runtime time:**
   - Reflection v1.x runtime (item 4).
   - Reflection probe registry (item 9).
   - Inoculation-frame template wording (item 10).

---

# §7. Self-check

- Operator-tracked artifacts surfaced with path + status + OQ count + dispatch readiness + estimated session count + pre-staged handoff path: yes (§§1-3).
- "Yesterday's research" deduplicated against LOCKED amendments + in-flight handoffs + v0.2 dispatch plan: yes (§4 enumerates 8 items, each with status / next step).
- Done definition file path matches dispatch: yes (`pipeline/planning/operator_spec_card_status_2026-05-10.md`).
- No new amendments, no LOCK ceremony, no spec cards authored: confirmed.
- Time-bound: discovery + report only — under 25 min as requested.
- Pre-staged next task: identifying which item operator wants to dispatch first is the operator's decision; this report surfaces the decision space without forcing a path.

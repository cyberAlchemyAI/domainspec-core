---
title: F-REFLECTION-* vs F-WPFA-* naming reconciliation — pre-Thesis disambiguation pass
filed: 2026-05-10
operator: Josh
authority: orchestrator pre-Thesis triage to prevent code-family collision between three forthcoming dispatches
disposition: status + decision-surface only; no LOCK ceremony, no amendment
scope: surface the cross-reference collision risk between three independent dispatch artifacts; defer resolution to operator decision (Q2(b) in `pipeline/planning/operator_spec_card_status_2026-05-10.md`)
---

# Why this pass exists

Three forthcoming dispatches all use the F-REFLECTION-* name-prefix at different scopes:

1. **§15 Archivist Reflection sub-mode** — synthesis memo at `pipeline/research/reflection/synthesis_design_memo_2026-05-10.md`. Pre-staged handoff at `pipeline/handoffs/ws_reflection_v0_1_hook_handoff_2026-05-10.md`. Names **17 net-new F-REFLECTION-\*** codes + 5 sub-tag extensions on existing F-ARCHIVIST-* parents (synthesis §4.3 table).

2. **WPFA cycle-close emission** — spec card at `pipeline/planning/watts_per_funding_action_spec_2026-05-10.md`. Names **12 F-WPFA-\*** codes + cross-references a sibling code `F-REFLECTION-SPAN-PROVENANCE-MISSING` (spec card §6 trigger column for `F-WPFA-SPAN-PROVENANCE-MISSING`).

3. **Reflection Packet (sibling-to-WPFA, distinct from §15 sub-mode)** — research findings only at `pipeline/research/reflection_packet_grounding/findings_2026-05-10.md`. **No spec card.** Pending operator scope decision (Q2 in the spec-card-status report).

If all three dispatch in parallel with no naming triage, the §15 sub-mode's F-REFLECTION-* family and the Reflection Packet's intended F-REFLECTION-* family collide at the §4 Logician v2.x.z code-registry layer. F-CIC-CLC-COUPLING-VIOLATION-class catch (closed-set membership check on code names + parent-family routing) would fire fail-closed at compound-LOCK time.

This pass surfaces the collision before either dispatch fires. Resolution is operator-decision per Q2(b).

# §1. Code-by-code overlap inventory

## §1.1 The §15 Archivist Reflection sub-mode family (synthesis §4.3)

17 top-level codes, all at the Tilth-internal-memory-substrate-write scope. Each predicates on **memory writes** (reflection digest → operator-attached Archivist state). All 17 fail-close at PRE-write / POST-write / COMMIT layer of the **reflection_agent's** seat-mode-dispatcher.

| # | Code | Scope |
|---|---|---|
| 1 | F-REFLECTION-NO-EXTERNAL-SIGNAL | Reflection write substrate: grounding signal class set ⊇ ≥1 class |
| 2 | F-REFLECTION-EVAL-ONLY-GROUNDED | Reflection write: blocks LLM-evaluator-only grounding |
| 3 | F-REFLECTION-INSUFFICIENT-EVIDENCE | Reflection write: N-cycle minimum |
| 4 | F-REFLECTION-RFA-SPEC-OVERRIDE | Reflection write: blocks RFA/PROJECT_CONTEXT override |
| 5 | F-REFLECTION-INTENT-ANCHOR-DRIFT | Reflection trajectory drift |
| 6 | F-REFLECTION-DEPTH-EXCEEDED | Reflection-of-reflection depth bound |
| 7 | F-REFLECTION-CONTENT-LOOP-DETECTED | Reflection text similarity |
| 8 | F-REFLECTION-SELF-EVALUATOR-FAMILY-CLASH | Cross-family rigor on reflection critic vs author |
| 9 | F-REFLECTION-SYCOPHANCY-LOOP-DETECTED | META cycle-level: score-vs-corpus-drift slope |
| 10 | F-REFLECTION-EVAL-SURROGATE-DIVERGENCE | META cycle-level: Judge improves while funded outcomes flat |
| 11 | F-REFLECTION-SELF-REPORTED-CONFIDENCE | Reflection text contains self-reported confidence |
| 12 | F-REFLECTION-FABRICATION-ON-FAILURE | Reflection verdict ≠ gate-outcome ledger |
| 13 | F-REFLECTION-OPERATOR-OVERRIDE-MASK | Reflection proposes mutation to operator-set key |
| 14 | F-REFLECTION-INOCULATION-FRAME-MISSING | Reflection prompt template integrity |
| 15 | F-REFLECTION-WRITE-WITHOUT-COMMIT | journal/commit pattern enforcement |
| 16 | F-REFLECTION-PROBE-COVERAGE-INCOMPLETE | META: probe registry membership |
| 17 | F-REFLECTION-COVERAGE-INCOMPLETE | META: F-REFLECTION-* primitives realized |

Plus **5 sub-tag extensions** under existing F-ARCHIVIST-* parents (§4.2 table; `.reflection_cross_org_read`, `.reflection_attach_unsigned`, `.reflection_instance_in_pattern_field`, `.reflection_interval_drift`, `.reflection_evidence_out_of_run`).

## §1.2 The WPFA family (spec card §6)

12 codes, all at the cycle-close emission scope. Each predicates on **cycle-close artifact emission** (CycleReceipt + buyer-facing PDF). Fail-close at PRE-load / PRE-emission / PRE-write / POST-load / PRE-PDF-emit layer of the **Cycle Accountant** module.

| # | Code | Scope |
|---|---|---|
| 1 | F-WPFA-COEFFICIENT-REGISTRY-UNSIGNED | Coefficient Registry trust |
| 2 | F-WPFA-COEFFICIENT-SIGNATURE-INVALID | Coefficient Registry signature verify |
| 3 | F-WPFA-MODEL-COEFFICIENT-MISSING | model_id resolves in registry |
| 4 | F-WPFA-BASELINE-MISSING | quarterly baseline resolves |
| 5 | F-WPFA-SPAN-PROVENANCE-MISSING | every claim traces to Logfire span |
| 6 | F-WPFA-COUNTERFACTUAL-INFLATION | baseline matches registry's published baseline |
| 7 | F-WPFA-OPERATOR-SIGNATURE-MISSING | buyer-facing PDF attestation |
| 8 | F-WPFA-DIMENSION-UNSUPPORTED | dimensions_active closed set |
| 9 | F-WPFA-REGISTRY-DRIFT | local measurement vs registry coefficient advisory |
| 10 | F-WPFA-SCHEMA-INVALID | CycleReceipt schema invariants |
| 11 | F-WPFA-CROSS-ORG-LEAK | Law 3 defense-in-depth |
| 12 | F-WPFA-PDF-CONFIDENTIAL-LEAK | classification register vs PDF content |

No F-WPFA-* code overlaps directly with the §15 Reflection sub-mode family by name. **The collision is in cross-references, not in code identity.**

## §1.3 The collision surface (one explicit cross-reference today; structural similarity in others)

**Explicit cross-reference in WPFA spec card §6 (F-WPFA-SPAN-PROVENANCE-MISSING row):**

> Mirrors `F-REFLECTION-SPAN-PROVENANCE-MISSING` (sibling artifact). Sub-tags `.no_trace_id`, `.trace_id_unresolvable_in_logfire`, `.claim_key_unmapped`.

But **the §15 synthesis memo's F-REFLECTION-* family does NOT contain a `F-REFLECTION-SPAN-PROVENANCE-MISSING` code** — the closest is F-REFLECTION-FABRICATION-ON-FAILURE (#12) which predicates on gate-outcome ledger mismatch, not on Logfire-span-trace-id mapping. The WPFA spec card is referencing a code from the **Reflection Packet's** intended-but-unauthored code family, not from the §15 sub-mode family.

**Other structural-similarity-but-not-collision pairs:**

| §15 Reflection sub-mode code | WPFA code | Same code or sibling? |
|---|---|---|
| F-REFLECTION-COVERAGE-INCOMPLETE (META gate) | n/a — WPFA uses F-CLASS-COVERAGE-INCOMPLETE pattern indirectly | **Different scope.** §15 META is reflection-write predicates; F-CLASS is classification-routing predicates. Both are pattern-instances of L-006 dormant-binding META gates but distinct families. |
| F-REFLECTION-SELF-REPORTED-CONFIDENCE | n/a | §15 only — WPFA emits deterministic numbers, no LLM self-confidence. |
| F-REFLECTION-FABRICATION-ON-FAILURE | F-WPFA-COUNTERFACTUAL-INFLATION | **Sibling pattern, different scope.** §15: verdict ≠ gate ledger. WPFA: counterfactual baseline ≠ registry-signed baseline. Both detect "claimed value ≠ ground-truth value" but at different substrate layers. |
| F-REFLECTION-WRITE-WITHOUT-COMMIT (COMMIT) | n/a | §15 only — WPFA's CycleReceipt write is one-shot, no journal/commit two-stage. |
| (none in §15) | F-WPFA-SPAN-PROVENANCE-MISSING | **WPFA cites this as cross-referencing a "F-REFLECTION-SPAN-PROVENANCE-MISSING" that does not exist in §15.** Collision is here. |

# §2. The actual question — three resolution paths

The WPFA spec card §6 was authored with the expectation that a Reflection Packet design (sibling-to-WPFA) would ship its own F-REFLECTION-SPAN-PROVENANCE-MISSING code. The §15 synthesis memo author independently named 17 codes under the F-REFLECTION-* prefix without coordinating with the WPFA spec card author. **Both spec cards are correct on their own; the collision is at the join.**

## Path A — Fold Reflection Packet into F-REFLECTION-* family (single owner: §15 + reflection_packet)

The §15 Archivist Reflection sub-mode and the Reflection Packet are both named "Reflection" because they both consume the same Logfire span tree at cycle close + both feed Archivist's learning loop. **Fold both into one F-REFLECTION-\* family** owned jointly by:

- §15 Archivist seat (reflection sub-mode → memory writes).
- §16 Reflection Packet seat-class (proposed) (cycle-close emission → Packet emitted as Pydantic BaseModel).

The §15 synthesis memo's 17 codes stay. The WPFA spec card's `F-REFLECTION-SPAN-PROVENANCE-MISSING` reference resolves to a NEW 18th code added to the family at the Reflection Packet spec card LOCK time. Code count: 17 + N (where N = number of Packet-specific codes; likely 3-5 based on the WPFA spec card's cross-references).

- **Pro:** single semantic owner for the "reflection over cycle-close data" concept. Easier to reason about for downstream consumers (Archivist v0.2 SPEC LOCK reads both Packet-side and sub-mode-side codes from one registry).
- **Con:** the §15 synthesis memo's authorship boundary blurs. F-REFLECTION-FABRICATION-ON-FAILURE (sub-mode scope) and a future F-REFLECTION-SPAN-PROVENANCE-MISSING (Packet scope) live in the same family despite different invocation paths.

## Path B — Separate the Reflection Packet into a F-PACKET-* family

Reserve F-REFLECTION-* for the §15 Archivist sub-mode exclusively. The Reflection Packet ships its own F-PACKET-* family (or similar — F-CYCLE-PACKET-*, F-REFL-PACKET-*).

The WPFA spec card §6 is amended at WPFA Thesis Cycle 1 to cite `F-PACKET-SPAN-PROVENANCE-MISSING` instead of `F-REFLECTION-SPAN-PROVENANCE-MISSING`. The §15 synthesis memo stays untouched.

- **Pro:** clean separation of seat/concern boundaries. Each family has a single seat owner. F-PACKET-* + F-REFLECTION-* + F-WPFA-* are three siblings under §4 v2.x.z, mirroring the §13 F-DATACOLLECTOR-* + §14 F-REPORT-* + §15 F-ARCHIVIST-* sibling pattern.
- **Con:** if the Reflection Packet design *internally* converges with the §15 sub-mode's grounding-signal-class set + cross-family-rigor + inoculation-frame, those mechanisms get duplicated across two code families.

## Path C — Defer the Reflection Packet entirely to v0.2 horizon; resolve naming at v0.2 SPEC LOCK time

Today's directive landed WPFA at v0.1 Beta scope. The Reflection Packet is currently research-only (no spec card). If the Reflection Packet is v0.2 horizon, the naming question doesn't surface until v0.2 SPEC LOCK time — and WPFA Thesis Cycle 1 can simply remove the `F-REFLECTION-SPAN-PROVENANCE-MISSING` cross-reference from §6 (replace with a forward-design note: "this code is a sibling to a forthcoming Reflection Packet code; naming resolution deferred to Reflection Packet spec card LOCK").

The §15 synthesis memo proceeds unchanged. WPFA proceeds with a documentary-only edit to §6.

- **Pro:** zero coordination overhead this dispatch cycle; no naming-collision risk at v0.1 Beta LOCKs.
- **Con:** the §6 cross-reference is the only signal that WPFA and Reflection Packet are siblings; removing it weakens the sibling-not-nested discipline the spec card's §0 + §13.1 carefully establishes.

# §3. Recommended default (operator-overridable at Q2(b))

**Path B** — separate F-PACKET-* family for the Reflection Packet, F-REFLECTION-* reserved for §15 sub-mode.

Rationale:
- Mirrors the §13 / §14 / §15 sibling-family pattern (F-DATACOLLECTOR-* / F-REPORT-* / F-ARCHIVIST-*) that already exists in the LOCKED corpus.
- Each family has a single seat-owner — minimizes downstream-consumer confusion.
- Resolves the WPFA §6 cross-reference cleanly (just a code-name swap at WPFA Thesis Cycle 1 absorption).
- Allows the §15 synthesis memo to dispatch unchanged.
- Preserves the sibling-not-nested discipline at the F-WPFA-* / F-PACKET-* boundary.

# §4. Impact on the three in-flight dispatches (per Path B default)

## §4.1 §15 Archivist Reflection sub-mode (v0.1 Beta hook)

**Zero changes.** Synthesis memo + handoff packet stand as authored. Thesis Cycle 1 fires the 17 F-REFLECTION-* codes + 5 sub-tag extensions as currently named.

## §4.2 WPFA spec card

**One documentary edit in §6.5 (F-WPFA-SPAN-PROVENANCE-MISSING row):**

> Before: "Mirrors `F-REFLECTION-SPAN-PROVENANCE-MISSING` (sibling artifact). Sub-tags `.no_trace_id`, `.trace_id_unresolvable_in_logfire`, `.claim_key_unmapped`."
>
> After: "Sibling pattern to a forthcoming `F-PACKET-SPAN-PROVENANCE-MISSING` (Reflection Packet artifact, scope deferred per Q2). Sub-tags `.no_trace_id`, `.trace_id_unresolvable_in_logfire`, `.claim_key_unmapped`."

Plus a similar one-line edit in spec card §0 + §13.1 to replace "F-REFLECTION-* / F-WPFA-*" sibling-family naming with "F-PACKET-* / F-WPFA-*" (frontmatter sibling_artifact line is unaffected — it references the research-findings doc by path).

This is a fold-in at WPFA Thesis Cycle 1 absorption; no pre-Thesis re-author needed. Reviewer should not flag the naming as a defect (the WPFA Thesis prompt should include this reconciliation note as a pre-Thesis context.)

## §4.3 Reflection Packet (research-only → forthcoming spec card)

**Pending operator Q2.** If Q2(a) = v0.1 Beta scope, the Reflection Packet spec card authors immediately and the F-PACKET-* family registers at LOCK time. If Q2(a) = v0.2 horizon, the spec card authors at v0.2 SPEC LOCK time and F-PACKET-* registers then.

Either way, F-PACKET-* is the spec card's owned family per Path B default. Q2(b) resolves to **(a) F-PACKET-\* family** (default).

# §5. F-CIC-CLC-COUPLING-VIOLATION-class regression test

At each Thesis cycle for any of the three artifacts, the audit prompt MUST include a code-family closed-set membership check. Specifically:

- F-REFLECTION-* codes belong only to §15 Archivist sub-mode + sub-tag extensions on F-ARCHIVIST-*.
- F-WPFA-* codes belong only to §17 WPFA.
- F-PACKET-* codes (when authored) belong only to §16 Reflection Packet.
- No F-* code crosses seat ownership.

This mirrors the F-CIC-CLC-COUPLING-VIOLATION (v7.0.8) pattern at the seat-family layer rather than the customer-archetype-vs-capital-logic layer.

# §6. Done definition

- [x] All three forthcoming artifacts surveyed for naming collision (§1).
- [x] Collision surface identified (§1.3): WPFA §6 cross-reference to a non-existent §15 code.
- [x] Three resolution paths enumerated with trade-offs (§2).
- [x] Recommended default selected with rationale (§3 = Path B).
- [x] Impact on each in-flight dispatch documented (§4).
- [x] Regression-test pattern named (§5).
- [x] No LOCK ceremony, no amendments, no spec cards authored.

# §7. Hand-back

Reconciliation note is the pre-Thesis context that should travel with both Reflection v0.1 hook + WPFA Thesis Cycle 1 dispatch packets. Add reference at:

- `pipeline/handoffs/ws_reflection_v0_1_hook_handoff_2026-05-10.md` — add to "Sources" or "Bootstrap" pointing here.
- (forthcoming) `pipeline/handoffs/ws_wpfa_handoff_2026-05-10.md` — add same reference at handoff authoring time.

Operator Q2 answer determines Path A / B / C selection. Default = Path B unless operator overrides.

---

**Filed:** 2026-05-10. Pre-Thesis disambiguation pass. Not a LOCK candidate.

---

**Update 2026-05-15:** Path B ADOPTED at compound triple LOCK for the Reflection Packet (§16 v1 + §4 v2.x.y + §0.5 v22; lock_history rows 216/217/218). The Reflection-Packet half of Path B is now realized on-disk:
- F-PACKET-* family (19 codes) registered at §4 v2.x.y predicate-signature layer.
- §16 Reflection Packet artifact section authored with sibling-not-nested verification table.
- §17 v1 §6.5 forward-reference to `F-PACKET-SPAN-PROVENANCE-MISSING` RESOLVED at this LOCK (sub-tag list at the predicate body in `pipeline/logician/gates/f_packet_span_provenance_missing.py`).
- AST-lint cross-family-import ban scope extended per §4 v2.x.y §6 (static-import scope at v0.1 hook; dynamic-import BOUNDED-by-A1+A4 with v2 Section O.5 mitigation track).
- F-CIC-CLC-COUPLING-VIOLATION-class regression test PASS at LOCK ceremony (no F-PACKET-* code crosses to §15 / §17; no F-REFLECTION-* / F-WPFA-* / F-ARCHIVIST-* code crosses to §16).

The collision identified in §1.3 of this reconciliation is now structurally closed.

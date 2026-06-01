---
status: pre-Thesis scoping draft (NOT a blueprint amendment, NOT a LOCK)
authored: 2026-05-10
author: Cowork lane-2 session (post-lane-2 file)
target: Tilth-Reflection — design feedstock for the Thesis dispatch that will follow lane-synthesis
companion: pipeline/research/reflection/lane_2_dreaming.md
disposition: pre-staged per CLAUDE.md "proactive pre-staging" rule
folds: Anthropic Dreams (research-preview, 2026-05-06) + Tilth §15 Archivist v1 SPEC LOCKED 2026-05-10
explicitly_unfolded: lanes 1, 3, 4, 5 — to be merged at Thesis Audit #1
---

# Reflection-as-Archivist-Submode — Scoping Draft

## 0. Why this file exists

Lane 2 (Anthropic's Dreams / Auto Dream) is filed. Lanes 1/3/4/5 are concurrent. Josh wants Tilth-Reflection designed and built ahead of the curve. This draft scopes the parallelizable work that is **safe to author before lane synthesis**, and surfaces the operator decisions that block crystallization. It is **not** a blueprint amendment, **not** a §15 / §4 / §0.5 update, and **not** a LOCK candidate.

When lanes 1/3/4/5 file, the operator (or a synthesizer session) folds their findings against this scoping draft. If the lane-merge changes the seat home (Archivist-submode vs. new seat), the trigger model, or the classification posture, this draft is the diff target — not a competing artifact. **Throw-away-friendly by design.**

## 1. Single-sentence frame

> Tilth-Reflection is a between-cycle Archivist sub-mode that reads (read-only) the live memory state plus N past session transcripts, produces a staged candidate memory state in a separate path, and refuses to displace the live state without operator attach-step approval.

This sentence is the load-bearing claim. Every section below is a derivation of it, plus the Tilth-specific deltas vs. Anthropic Dreams.

## 2. Six structural primitives borrowed wholesale from Anthropic

Anthropic's Dreams design ships these six. All six map cleanly onto Tilth's existing discipline. Pull them in directly:

1. **Input immutability.** Live memory state is read-only during a Reflection run. Logician gate enforces.
2. **Fresh output target.** Reflection writes to a separate staging path; never overwrites live state in place.
3. **Operator attach-step.** Reflection produces a candidate; operator decides whether to attach it. Mirrors Anthropic's `outputs[]` + explicit attach pattern + Tilth's existing "operator clicks final submit" Uploader discipline.
4. **Per-cycle instructions card.** Anthropic ships a 4,096-char `instructions` parameter. Tilth analog: per-Reflection SP0-signed scoping (e.g., "this run: KFR maintenance only; ignore funder-intel"). Bounded by classification posture.
5. **Lock-file concurrency.** Anthropic prevents concurrent dreams; Tilth analog: filesystem lock at the staging directory. One Reflection run per workspace at a time.
6. **Sandboxed write surface.** Anthropic's Auto Dream is sandboxed to the memory directory. Tilth analog: Reflection can only write to the staging path; AST-lint + runtime guard + Cedar policy (three-layer defense mirroring Archivist's existing proposes-only architecture).

## 3. Six Tilth-specific deltas vs. Anthropic

Anthropic ships less safety than Tilth needs. These are net-new vs. Dreams:

1. **PII / admin-risk-term scanning at dream-time.** Anthropic's dream sees whatever's in the inputs. Tilth's Law 4 (Apolitical Language + Admin-Risk Term Scanning) means Reflection over content with flagged terms passes through the same scanner discipline as Scribe. Operator approves each substitution; no silent rewrite.
2. **Provenance preservation.** Anthropic merges duplicates without explicit per-fact provenance preservation. Tilth's Intake KFR ships verbatim-quote-with-page provenance — Reflection MUST NOT strip it during consolidation. Candidate gate: `F-REFLECTION-PROVENANCE-STRIPPED`.
3. **Cross-family review of Reflection output.** Anthropic relies on operator review at attach time. Tilth's L-003 cross-family discipline argues for Editor + Red-Team review-PASS on the staged candidate before the attach-step is even offered. Logician PRE-attach gate.
4. **Signed audit trail.** Anthropic surfaces dream-id + session-id; that's it. Tilth needs append-only audit-log entries: `(reflection_run_id, input_state_hash, output_candidate_hash, operator_attach_decision, operator_ed25519_signature, timestamp_utc)`.
5. **Classification-routing on Reflection input.** Per v7.0.7 LOCKED, the Reflection invocation's routing decision uses `classification = max(input_memory_classifications ∪ input_session_classifications)`. Any `confidential` or `operator_flagged` → local-only routing. Heavy-Judge swap analog available for end-of-quarter heavy consolidations.
6. **Opaque-slot discipline at Reflection prompt.** Per F-CLASS-SLOT-ID-NON-OPAQUE LOCKED, Reflection's cloud-routed prompt (if and only if the routing decision lands cloud) uses opaque `[SLOT_<numeric_id>]` only. Slot-fill agent renders Confidential values into the post-Reflection candidate, not into the prompt.

## 4. Five candidate Logician gates (pre-Thesis sketch — names provisional)

Surfaced in lane_2_dreaming.md §Tilth implications. These are SKETCHES, not LOCK candidates. Thesis dispatch will refine names, contracts, and PRE/POST/COMMIT semantics.

| Gate (provisional) | Layer | Triggers when | Fail-mode |
|---|---|---|---|
| `F-REFLECTION-INPUT-MUTATED-DURING-RUN` | PRE-attach | Live memory state hash at run-start ≠ hash at attach-time | Fail-closed; reject attach; surface diff |
| `F-REFLECTION-OUTPUT-AUTOAPPLIED` | PRE-attach | Attach attempted without operator Ed25519 signature on `(input_hash, output_hash, run_id)` | Fail-closed; refuse attach |
| `F-REFLECTION-PROVENANCE-STRIPPED` | POST-stage | Any KFR fact in input state appears in output state without its verbatim-quote provenance | Fail-closed; refuse stage |
| `F-REFLECTION-ROUTING-INDETERMINATE` | PRE-invoke | Per-call classification decision cannot resolve cloud vs. local for the input set | Fail-closed to local (extends existing F-CLASS-ROUTING-INDETERMINATE) |
| `F-REFLECTION-CROSS-FAMILY-MISSING` | PRE-attach | Staged candidate lacks Editor-PASS + Red-Team-PASS (cross-family rigor) | Fail-closed; refuse attach |

**Naming hazard:** all five F-REFLECTION-* could potentially be subsumed under existing Archivist gate codes if Reflection lands as an Archivist sub-mode (per §1 frame). The §15 v1 LOCK already owns `F-ARCHIVIST-CROSS-ORG-LEAK`, `F-ARCHIVIST-LESSON-INSTANCE-LEAK`, `F-ARCHIVIST-AUTO-APPLY-ATTEMPTED`, `F-ARCHIVIST-CADENCE-DRIFT`, `F-ARCHIVIST-READ-WITHOUT-VAULT-INTENT`. Thesis decides whether Reflection extends F-ARCHIVIST-* (sub-tag pattern like row 198's `R-ARCHIVIST-NO-CANONICAL-MUTATE` six-sub-tag extension) or stands up F-REFLECTION-* as a fresh family.

Default recommendation pre-Thesis: **extend F-ARCHIVIST-* with sub-tags** (analog to the §4 v2.x.1 narrow-corrective pattern that LOCKED today). Keeps the seat-owner consistent and avoids new top-level rows.

## 5. Trigger model — three candidate defaults

Anthropic ships two trigger surfaces: operator-invoked (API tier) and dual-gate auto (24h + >5 sessions, Claude Code tier). Tilth has three plausible defaults; the choice is operator's:

| Candidate | Source of authority | Reflection runs when | Fit with Tilth posture |
|---|---|---|---|
| **A. Operator-invoked per-cycle** | Explicit operator command via CLI / future GUI | Operator issues `tilth reflection start --org <slug>` | Highest sovereignty; matches Uploader's "operator clicks final submit" pattern. **Recommended default for v0.1-attached / v1.x ship.** |
| **B. Per-grant SP0-bound** | Per-grant SP0 signature includes a `trigger_reflection_on_close: true` field | Operator signs grant-close SP0 with the flag set | Compositional with existing SP0 chain. Risk: leaks Reflection cadence into per-grant SP0 surface. |
| **C. Dual-gate cadence (Anthropic analog)** | Workspace policy: 24h + >N runs | Background daemon checks dual-gate on session-close | Lowest sovereignty; closest to Anthropic Auto Dream. **v0.2 horizon at earliest** — requires Classification Review UX to handle cadence-policy classification first. |

**Pre-Thesis recommendation:** A as v1.x default; B as opt-in per-org policy; C deferred to v0.2 or later.

## 6. Seat home — three options revisited from lane 2

| Option | Where Reflection lives | Pros | Cons |
|---|---|---|---|
| **A. Archivist sub-mode** | New sub-mode on §15 Archivist v1 (alongside weekly + quarterly cadences) | Reuses three-layer proposes-only defense (AST-lint + runtime guard + Cedar). No new seat = no §0.5 row, no Council rebalancing. Single LOCK target. | Archivist scope grows; "consolidation" vocabulary gets two flavors (Archivist's existing curation vs. Reflection). |
| **B. New ninth support agent ("Reflector")** | Net-new seat under v1.x horizon | Cleaner conceptual seam matching Anthropic's API. Easier to reason about independently. | New seat = new audit round, §0.5 row, classification-register entry, router.yaml entry. Higher blast radius. |
| **C. Logician-orchestrated pipeline stage** | No new seat; Logician PRE/POST gates over an Archivist invocation | Smallest delta. Existing Logician machinery handles it. | Conflates orchestration with policy enforcement — Logician's deterministic-only doctrine doesn't fit the LLM-invocation pattern Reflection needs. |

**Pre-Thesis recommendation:** A. Mirror the §4 v2.x.1 narrow-corrective pattern + Cycle-1 RT-09 fold-in style. Reflection becomes a §15 v1.x amendment, paired with §0.5 §15.x sub-tag extension. No new top-level §-section.

## 7. Target version — three timeline scopes

| Scope | What lands | When | Cost |
|---|---|---|---|
| **v0.1 Beta hook only** | Reflection gate primitives (the 5 above) registered as dormant Cedar/Python predicates; runtime not yet invoked | This cycle (v0.1 Beta close-out window) | LOW. Pattern matches the F-CLASS-* dormant primitives at architecture v7.0.7 / WS-L §4 v2.x. Doesn't compete with Beta finalization. |
| **v0.2 SPEC-ONLY amendment** | Full Reflection seat-spec authored, LOCKED at SPEC layer; v1.x implementation deferred | Post v0.1 Beta first cut | MEDIUM. Mirrors §13 Data Collector v1 / §14 Report Gen / §15 v1 pattern. |
| **v1.x runtime amendment** | Reflection runtime impl, paired with §15 v1.x Archivist runtime impl | v1.x horizon | HIGH. Cross-family L-005 two-cycle. Touches §15, §4, §0.5, router.yaml. |

**Pre-Thesis recommendation:** ship dormant gate primitives in v0.1 Beta hook (LOW cost, doesn't block Beta), schedule SPEC-only amendment for v0.2 (composed with §13/§14/§15 v0.2 family), defer runtime to v1.x. **Three-stage ship.** This is the Cards-vs-Cards-resolved-at-the-visual-layer-and-§8-deferred pattern again: ship the load-bearing primitive now, the spec next, the runtime last.

## 8. L-005 two-cycle Thesis plan (sketch)

**Audit #1 — scoping.** Editor (Llama/Groq) + Judge (Gemini/Google) + Red Team (GPT-OSS/Groq), cross-family per L-003. Deliverable from each:

- **Editor:** READY / NEEDS_FIXES / NOT_READY on the scoping draft as a whole. Flags vocabulary collisions with Archivist's existing curation language. Flags any place where this draft contradicts §15 v1 LOCKED.
- **Judge:** Scores against §15 v1 + v7.0.7 + v7 A1-A12 invariants. Specifically: input-immutability, classification-routing, cross-family-review, audit-trail signing. 100-pt rubric.
- **Red Team:** Adversarial. Find ways the proposed gate set fails-open. Especially: (a) symlink / dynamic-call / Path-equivalents bypasses on the input-immutability gate (per RT-07/08/10 disposition pattern from §4 v2.x.1 today); (b) classification leak via session-transcript embedding in the prompt; (c) provenance-stripping via paraphrase rather than removal; (d) attach-step replay attacks.

**Fold/defer/reject.** Cycle-1 findings → operator decision per row-170 disposition pattern.

**Audit #2 — verification.** Same trio. Verify Cycle-1 fixes landed. PASS / REQUIRES_MINOR_FIXES / REQUIRES_THIRD_ROUND. Per L-005 strict two-cycle: no silent third round. Tripwire = escalation to operator.

**LOCK target.** Whichever scope in §7 the operator picks. Default: v0.1 Beta hook (dormant gates only) + v0.2 SPEC-ONLY amendment paired.

## 9. Out-of-scope for this draft

Anything that requires lane 1/3/4/5 to file first:

- **Cross-Tilth Reflection (Stage-5 Sovereign Node commons).** Anthropic's Dreams is per-workspace. Whether Tilth-Reflection ever federates is a Stage-5 question. Tabled.
- **Whether Reflection generates training data for fine-tunes.** Out of scope for v0.1 (BYOK, model weights are not Tilth's to touch). Stage-5 question at earliest.
- **Whether Outcomes-grader composes with Reflection.** Anthropic's Outcomes is a separate Managed Agents feature; whether Tilth-Reflection should grade its own output via an Outcomes-analog is an open question deferred to v0.2.
- **Memory-store schema parity with Anthropic.** Lane-2-recommended noting; out of scope until / unless Tilth wants Dreams-as-a-service for offline batches (which is unlikely given sovereignty-promise).
- **Reflection over Funder Intelligence DB vs. Match DB vs. KFR vs. lessons.md.** Each has different classification, different cadence, different consumer. Card work for the SPEC-only amendment.

## 10. Compatibility check — does this draft survive lane 1/3/4/5?

The four open lanes are not named in this session's context. The draft is engineered to be **lane-agnostic** along the following axes:

| Lane finds … | Draft survives? | If not, what changes |
|---|---|---|
| A different memory-consolidation paper / system | ✅ | §2 primitives may gain or lose items; §3 deltas may shift. Frame in §1 stays. |
| A different cadence model (e.g., event-driven) | ✅ | Adds Option D to §5. |
| A different seat-home pattern (e.g., Council-seat-not-support-agent) | ⚠️ | §6 needs rework. §1 frame still holds (between-cycle, sandboxed, attach-gated). |
| A classification-routing nuance not in v7.0.7 | ⚠️ | §3.5 + §4 routing-indeterminate gate may need narrowing. |
| A Stage-5-relevant finding | ✅ | §9 absorbs it. |

If lanes invalidate §1's single-sentence frame, this draft is throw-away. That's by design — the lanes are why we don't LOCK off lane 2 alone.

## 11. Operator decisions — batched

Pre-Thesis questions that block crystallization. Batched per CLAUDE.md "Batch all open questions":

1. **Target version scope (§7).** v0.1 Beta dormant-gate hook only? v0.2 SPEC-only amendment? v1.x runtime? Or the three-stage default (all three, staged)?
2. **Seat home (§6).** Archivist sub-mode (default A) or new ninth seat (B)? Lane synthesis may change this; do you want the scoping to assume A and rework if lanes flip it, or scope both A and B in parallel?
3. **Trigger model default (§5).** Operator-invoked only (default A), per-grant SP0-bound (B), or both available as per-org policy?
4. **Lane synthesis timing.** Wait for all 5 lanes to file before Thesis dispatch, or dispatch Thesis Audit #1 on lane 2 only and absorb the other 4 at Cycle-1-fold? (The latter is faster but risks Cycle-1 churn proportional to how much the other lanes invalidate §1.)
5. **v0.1 Beta competition.** v0.1 Beta close-out has Intake full-impl + Uploader full-impl + WS-L LOCK + white-glove playbook outstanding. Should Reflection scoping pre-empt one of these, run parallel (different session), or wait for Beta first cut?

## 12. Pre-staged next action

If operator answers Q1=v0.1-Beta-hook + Q2=A + Q3=A-only + Q4=wait-for-all-5-lanes + Q5=parallel-different-session: next session writes a **Thesis kickoff packet** at `pipeline/validation/reflection_thesis_2026-MM-DD/dispatch_packet.md`, structure per §8, with lane synthesis folded in. Dispatch via cross-family bridge pattern (Editor=Llama/Groq, Judge=Gemini/Google, Red Team=GPT-OSS/Groq) per AGENTS.md.

If operator answers differently, this draft gets edited at the affected sections, not throw-out.

## Sources

- `pipeline/research/reflection/lane_2_dreaming.md` (companion file)
- `memory/project_blueprint_section_15_archivist_v1_locked.md` (§15 v1 SPEC LOCKED 2026-05-10)
- `memory/project_blueprint_section_04_v2_x_locked.md` + `_v2_x_1_locked.md` (§4 v2.x family LOCKED 2026-05-10)
- `memory/project_architecture_v7_0_7_locked.md` (classification-driven routing)
- `pipeline/architecture/v0.1/tilth_architecture_locked.md` (v7 LOCKED 2026-04-19 A1-A12)
- CLAUDE.md (proactive pre-staging + batched questions + match-operator-register)

---

**Filed:** 2026-05-10. Pre-Thesis scoping draft. Not a LOCK candidate. Lane-merge-friendly by design.

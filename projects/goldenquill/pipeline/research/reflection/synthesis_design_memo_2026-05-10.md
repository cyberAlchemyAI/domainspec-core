---
status: design synthesis memo — no LOCK ceremony, no Cedar/Python implementation
authored: 2026-05-10
session: Cowork reflection-synthesis (post-five-lane fold)
inputs:
  - pipeline/research/reflection/lane_1_hermes.md
  - pipeline/research/reflection/lane_2_dreaming.md
  - pipeline/research/reflection/lane_3_academic.md
  - pipeline/research/reflection/lane_4_pydantic_ai.md
  - pipeline/research/reflection/lane_5_field_failures.md
  - pipeline/research/reflection/scoping_draft_reflection_as_archivist_submode.md
  - pipeline/blueprint/v0.1/section_15_archivist.md (§15 v1 SPEC LOCKED 2026-05-10 row 191/192)
  - pipeline/architecture/v0.1/architecture_v7_0_4_amendment.md §9 + §9.1 (curation slot reservation + J-06 closure)
  - memory/project_blueprint_section_04_v2_x_1_locked.md (sub-tag extension pattern, row 198/199)
  - memory/project_architecture_v7_0_7_locked.md (classification-driven routing + L-006 dormant-binding precedent)
companion_dispatch_packet: pipeline/handoffs/ws_reflection_v0_1_hook_handoff_2026-05-10.md
disposition: design feedstock for the Thesis dispatch this memo unblocks
---

# Tilth-Reflection — Integrated Design Synthesis Memo

## Executive summary (for the hand-back)

Five research lanes converge on one architecture. Reflection lives as a third cadence under §15 Archivist (sub-mode A from the pre-Thesis scoping draft), inherits the existing three-layer proposes-only defense and the J-06 operator → archivist slot transition, and adds ~17 new top-level `F-REFLECTION-*` Logician gate codes plus ~5 sub-tag extensions to existing `F-ARCHIVIST-*` families. The load-bearing finding is Lane 3's: Tilth's grounding signal class set must be Logician gate outcomes + operator approval + funder award outcomes + KFR fact-drift + admin-risk-ledger entries — never Judge / Editor / Red Team scores alone. Ship plan is three-stage: v0.1 Beta hook (dormant Cedar/Python primitives only — LOW cost, doesn't compete with Beta close-out); v0.2 SPEC-only `§15 v2.x` amendment paired with `§0.5 §15.x` sub-tag extension + `§4 v2.x.2` sub-amendment; v1.x runtime where predicates activate when Archivist transitions to scheduled-task-driven. The v0.1 Beta hook dispatch packet is pre-staged at `pipeline/handoffs/ws_reflection_v0_1_hook_handoff_2026-05-10.md`.

---

## §1. Cross-lane convergent findings

### §1.1 Where the five lanes agree (load-bearing)

**Five-for-five agreement** (every lane independently surfaces this — these are the architectural primitives that cannot be negotiated):

| Convergent finding | L1 Hermes | L2 Dreams | L3 Academic | L4 Pydantic AI | L5 Field-failures |
|---|---|---|---|---|---|
| External grounding signal required (no pure intrinsic self-evaluation) | implicit (tool-execution evidence) | explicit (operator-attach) | **explicit (Huang 2024 + Kamoi 2024)** | implicit (`EvaluatorContext` requires grounded inputs) | **explicit (F-1, F-4, F-13)** |
| Cross-family / cross-persona evaluator separation | "no agent should verify its own work" | operator review at attach | MAR / MAD / N-CRITICS | multi-agent hand-off idiom | **F-8 Reflexion confirmation bias** |
| Input immutability + atomic write + rollback | `_atomic_write_text` + tarball | input store never modified | rate-limited trigger | write-on-commit (GH #4679) | F-1 rollback only worked because prior snapshot retrievable |
| Reflection state must be bounded (depth / cardinality / cadence) | 7d/2h curator interval | dual-gate trigger | Park importance-score; Reflexion 3-buffer | history_processors token cap | **F-7 + F-12 long-context destabilization** |

**Four-for-five agreement** (Lane 1 is the dissenter; Hermes is single-tenant developer-assistant by design and doesn't surface these):

| Convergent finding | L2 | L3 | L4 | L5 |
|---|---|---|---|---|
| Classification / cross-tenant isolation at the storage layer | classification routing per v7.0.7 | Law 3 reflection-layer question | `Deps` plumbing per-org | **F-14 UCC (default failure mode, no attacker needed)** |
| Proposes-only / operator-attach gate (vs. auto-apply) | Anthropic operator-attach pattern | Park importance-threshold | output_validator → commit | **F-2 Replit, F-3 Tay, F-9 ChatGPT memory injection** |
| Signed / hash-pinned audit trail | dream-id (weak) | provenance | `ModelMessagesTypeAdapter` round-trip | F-1 rollback worked because hash-pinned |

### §1.2 Where the lanes conflict (operator must decide one or synthesis picks default)

| Conflict axis | Lane 1 view | Lanes 2/3/4/5 view | Synthesis pick |
|---|---|---|---|
| **Auto-apply default?** | Hermes: auto-apply + tarball rollback | All others: proposes-only fail-closed | Lanes 2-5 win. Tilth fails-closed; auto-apply requires operator Ed25519 sign-off |
| **Cryptographic provenance?** | Hermes: none (atomic write suffices) | L2/L3/L5: signed audit mandatory | L2/L3/L5 win. Ed25519 on every reflection artifact + `(input_hash, output_hash, run_id)` tuple |
| **Retrieval model?** | Hermes: description-string LLM match (3K-token catalog) | L4 + L5: structured / vector at scale | L4 + L5 win for v1.x horizon; L1 pattern (flat list) is fine for v0.1 Beta hook cardinality (single-digit reflections per org) |
| **Trigger model default?** | Hermes: live + background + calendrical (all three) | L2: dual-gate auto OR operator-invoked; L3 + L5 F-7: operator-invoked safer | Operator-invoked at v0.1/v0.2; cadenced at v1.x post Classification Review UX |
| **Per-cycle vs. background fork agent?** | Hermes: separate sub-agent fork (clean prompt cache) | L4: separate `reflection_agent` (multi-agent hand-off) | L1 + L4 agree on the *shape* (separate agent); synthesis: separate Pydantic AI agent inside Archivist sub-mode dispatcher |
| **Catalog size assumption?** | Hermes: 20-200 skills survives flat retrieval | L1 itself flags this breaks at v1.x | Defer structured retrieval to v1.x amendment when cardinality crosses threshold |

**Single irreducible conflict — Hermes vs. everyone else.** Hermes treats reflection writes as Git-style commits (atomic, rollbackable, after-the-fact-auditable). Lanes 2-5 require reflection writes to be grant-claim-class (fail-closed, signed, cross-family-reviewed, classification-routed). Tilth picks the Lanes 2-5 posture without ambiguity — Hermes's discipline is wrong for grant-writing where the worst-case mutation is a fabricated funder commitment or a silently-rewritten Law-4 flagged term. Hermes's *mechanics* (trigger surfaces, atomic write, telemetry sidecar, curator cadence) port wholesale; Hermes's *posture* (auto-apply, no signing, no semantic gating) does not.

---

## §2. Seat-home decision — Archivist sub-mode (Option A from scoping draft)

**Decision: Reflection is a third cadence under §15 Archivist.** Specifically: a new `reflection` cadence alongside `weekly` and `quarterly`, invoked at v0.2 SPEC as `tilth archivist reflection --org <slug>` or `tilth archivist reflection --workspace`, transitioning to scheduled-task-driven at v1.x per §15 J-06 slot transition.

### §2.1 Justification against the four binding inputs

**Against §15 Archivist v1 SPEC's proposes-only / three-layer defense.**
- The three-layer defense (AST-lint at module load → runtime guard via Vault read intent → Cedar policy via `F-ARCHIVIST-*` family) is exactly the right enclosure for reflection writes. Reflection inherits it for free. No new `R-REFLECTION-NO-CANONICAL-MUTATE` AST-lint needed — the existing `R-ARCHIVIST-NO-CANONICAL-MUTATE` (with its 6 sub-tags from row 198) already forbids the low-level write primitives reflection would otherwise reach for.
- The proposes-only posture matches Lane 2's operator-attach pattern exactly: reflection produces a candidate digest entry; operator confirms via the existing `tilth archivist review` flow.
- Three of the five existing `F-ARCHIVIST-*` gates already cover load-bearing reflection failure modes via sub-tag extension (see §4.2).

**Against §15 J-06 slot-transition timing.**
- v7.0.4 §9 reserves the curation slot for v1.x Archivist; §9.1 (J-06 closure) pins the operator → archivist transition discipline. Reflection rides this seam without inventing a parallel transition. At v1.x, Reflection's cadence-driven invocation lands the same way Archivist's weekly + quarterly cadences land: scheduled-task-driven via the `schedule` skill, with operator-explicit invocation always remaining valid.
- The slot-owner field's `operator → archivist` flip happens once at v1.x for the whole Archivist seat, not per-cadence. Reflection inherits.

**Against v7.0.4 curation slot reservation.**
- Curation slot was reserved for KFR maintenance + Funder Intel curation + Match DB lessons-delta + Benchmarks Register freshness. Reflection is structurally a fourth member of this family — same operator-facing digest discipline, same proposes-only posture, same signed audit trail. Reservation absorbs it.

**Against Anthropic Dreams' "operator attaches the output" pattern.**
- Archivist's existing operator-review surface (`tilth archivist review --org <slug> --cadence <weekly|quarterly>`) extends to `--cadence reflection`. The attach step is the existing review-and-confirm flow. Reflection's staged candidate enters `orgs/<slug>/archivist_digests/reflection_<run_id>.yaml` exactly the way weekly/quarterly digests do.

### §2.2 Why NOT a new ninth support agent

- New seat = new audit round + new §0.5 row + new router.yaml entry + new classification-register entry. Blast radius too high for marginal conceptual clarity gain.
- The "Reflector" naming would compete with Archivist's existing curation vocabulary, not complement it. Two flavors of "between-cycle consolidation under one seat" is cleaner than two seats both called consolidation.
- §15 already names "lessons memory" as a v1.x duty. Reflection IS lessons-memory-curation. The naming hazard from scoping draft §6 dissolves once we accept that "Archivist's third cadence is reflection over the lessons substrate."

### §2.3 Why NOT a Logician-orchestrated pipeline stage (Option C from scoping draft)

- Logician's deterministic-only doctrine doesn't fit LLM invocations. Reflection's pattern-detection prompt is an LLM call (per v1.x extraction substrate). Logician gates over it, but does not own the seat.
- This was correctly ruled out in the scoping draft.

### §2.4 Internal mechanics (Pydantic AI shape lives inside the sub-mode)

The seat-home decision is Archivist sub-mode at the **seat-blueprint layer**. The **implementation mechanic** is Lane 4's `reflection_agent` pattern: Archivist's seat-mode-dispatcher routes `--cadence reflection` to a small dedicated Pydantic AI agent with three tools (`read_priors`, `record_reflection`, `score_against_priors`), its own `Deps`, its own classification posture (always-local — see §5.2). The user-facing surface is "Archivist's third cadence." The runtime under the hood is a separate Pydantic AI agent. Both framings are true at different layers. This reconciles Lane 2's seat-home recommendation with Lane 4's multi-agent hand-off idiom without conflict.

---

## §3. The grounding signal call — Lane 3's killer insight

Lane 3 ends with the single most load-bearing claim across all five lanes: *Tilth's Reflection cannot ground on Judge scores.* Reflexion's HumanEval gains came from ground-truth unit tests (an oracle); Huang ICLR 2024 + Kamoi TACL 2024 demonstrate that when the evaluator is itself an LLM, intrinsic self-correction either fails to improve or actively degrades performance. Tilth's Judge is an LLM. Therefore Reflection must ground on something other than Judge.

### §3.1 The grounding signal class set (canonical, precedence-ordered)

Eight classes, ranked highest authority → lowest. Reflection gate `F-REFLECTION-EVAL-ONLY-GROUNDED` (see §4.1) fail-closes any reflection whose declared grounding signal set ⊆ {class 7, class 8} only.

| Rank | Class name | Source | Authority | Cadence | Determinism |
|---|---|---|---|---|---|
| 1 | `external_funder_outcome` | Funded / not funded ledger from Match DB | **Highest** — actual real-world signal | Slow (weeks-months post-submit), sparse | Binary, observed |
| 2 | `operator_approval` | Operator Ed25519-signed attach decision; KFR confirmation; classification decision; SP0 signature | High — operator-intent-laden but explicit | Dense at points of attach/confirm | Cryptographically attested |
| 3 | `logician_gate_outcome` | `F-*` gate PASS / FAIL / sub-tag from PRE/POST gate executions | High — deterministic Python+Cedar, zero-token | Densest local signal | Fully deterministic |
| 4 | `kfr_drift_event` | KFR fact hash change; canonical-signature-invalidation; status transition | High — substrate ground truth | Event-driven, infrequent | Cryptographic hash diff |
| 5 | `admin_risk_event` | Law 4 flagged-term substitution; operator approve/reject of substitution | Medium-high — operator-mediated | Event-driven | Audited |
| 6 | `match_db_outcome` | Per (client × funder) cycle outcome rollup | Medium — aggregated proxy for class 1 until class 1 lands | Quarterly | Aggregated from class 1 + operator action_state |
| 7 | `council_split_event` | Judge × Red Team >10pt disagreement per A3 | **NOT primary** — same-trajectory signal | Per draft | LLM-derived; only counts because cross-family rigor enforced |
| 8 | `editor_verdict` / `judge_score` / `red_team_score` (any single LLM-eval verdict alone) | LLM-only | **NEVER primary alone** — fails F-REFLECTION-EVAL-ONLY-GROUNDED | Per draft | LLM-derived |

### §3.2 Precedence rule (the structural answer to Huang 2024)

A reflection's `grounding_signal_classes: set[str]` field is mandatory. The Logician PRE-write gate `F-REFLECTION-NO-EXTERNAL-SIGNAL` fail-closes if the set is empty. The gate `F-REFLECTION-EVAL-ONLY-GROUNDED` fail-closes if the set ⊆ {`editor_verdict`, `judge_score`, `red_team_score`, `scribe_self_assessment`}. At least one of classes 1-6 must be present.

`council_split_event` (class 7) is admitted because cross-family rigor at A3 forces the split signal to derive from *different model families*, which is the field-validated mitigation per Lane 5 retrofits-that-worked. But class 7 alone is insufficient — at least one of classes 1-6 must accompany it.

### §3.3 What this means for v0.1 Beta hook

`F-REFLECTION-NO-EXTERNAL-SIGNAL` and `F-REFLECTION-EVAL-ONLY-GROUNDED` are dormant Cedar/Python primitives at v0.1 Beta hook (no live reflection invocations yet); their predicate bodies enumerate the class set. This is the architectural-primitive layer that Beta deployment commits to before any Reflection runtime lands. Matches L-006 dormant-binding precedent + the F-CLASS-* pattern from v7.0.7.

---

## §4. The gate family — dedup, classification, sub-tag vs. top-level

### §4.1 Dedup inventory

The five lanes surfaced ~45 distinct gate candidate names. Dedup collapses them to:

- **5 sub-tag extensions on existing `F-ARCHIVIST-*` families** (where an Archivist parent already owns the predicate)
- **17 net-new top-level `F-REFLECTION-*` codes** (where no Archivist parent exists)
- **3 reservations** (predicates that depend on v0.2+ horizon substrate not yet specced)

Total: **22 architectural-primitive gate registrations** at v0.1 Beta hook (matches the ~12 estimate in the dispatch prompt + the additional structural gates surfaced by Lane 3 and Lane 5 in detail).

### §4.2 Sub-tag extensions to existing F-ARCHIVIST-* families

These fold under the existing 5-gate Archivist family per the §4 v2.x.1 narrow-corrective sub-tag-extension pattern (row 198, six sub-tags on `R-ARCHIVIST-NO-CANONICAL-MUTATE`):

| Parent F-ARCHIVIST-* code (existing) | New sub-tag | Lane source | Predicate sketch |
|---|---|---|---|
| `F-ARCHIVIST-CROSS-ORG-LEAK` | `.reflection_cross_org_read` | L1 + L4 + L5 F-14 | Reflection invocation crosses `org_slug` boundary during read; reuses existing symlink-escape + Vault-read-intent enforcement |
| `F-ARCHIVIST-AUTO-APPLY-ATTEMPTED` | `.reflection_attach_unsigned` | L1 + L2 + L5 F-2/F-3 | Reflection digest attach attempted without operator Ed25519 signature on `(input_hash, output_hash, run_id)` |
| `F-ARCHIVIST-LESSON-INSTANCE-LEAK` | `.reflection_instance_in_pattern_field` | L3 §3.2 + L5 F-8 | Reflection pattern-summary field contains instance-level details that should have been pattern-rolled; reuses existing pattern-vs-instance enforcement |
| `F-ARCHIVIST-CADENCE-DRIFT` | `.reflection_interval_drift` | L1 curator-interval-drift + L2 cadence | Reflection cadence runs outside declared interval without operator-initiated flag |
| `F-ARCHIVIST-READ-WITHOUT-VAULT-INTENT` | `.reflection_evidence_out_of_run` | L1 + L4 EVIDENCE-OUT-OF-RUN | Reflection cites evidence outside the current run's transcript / KFR / Match DB substrate — bypassing Vault read intent |

**No new top-level Archivist gates needed.** The existing five fully cover the reflection-as-substrate-write surface. Sub-tag extensions inherit AST-lint enforcement + runtime guard + Cedar policy from the parent.

### §4.3 New top-level F-REFLECTION-* codes (where no Archivist parent exists)

These predicate the *reflection content* and *grounding-signal discipline* — domains the existing F-ARCHIVIST-* family does not cover. Each row carries: PRE/POST/META position, predicate sketch, evidence threshold, signal-class dependency.

| # | New top-level code | Layer | Predicate sketch | Evidence threshold | Signal class dependency |
|---|---|---|---|---|---|
| 1 | `F-REFLECTION-NO-EXTERNAL-SIGNAL` | PRE-write | `grounding_signal_classes` field empty | N/A — empty fails | Requires ≥1 class |
| 2 | `F-REFLECTION-EVAL-ONLY-GROUNDED` | PRE-write | `grounding_signal_classes` ⊆ {LLM-evaluator-only} | N/A — set membership | Requires ≥1 of classes 1-6 per §3.1 |
| 3 | `F-REFLECTION-INSUFFICIENT-EVIDENCE` | PRE-write | Reflection generalizes from < N independent grant cycles | N = operator-configured at white-glove (default: 3 per-funder, 2 per-CIC, 5 per-CLC) | Counts class-1 + class-6 events |
| 4 | `F-REFLECTION-RFA-SPEC-OVERRIDE` | PRE-write | Reflection text asserts funder intent / RFA scope not present in original RFA + PROJECT_CONTEXT | N/A — string-match + Law-2 admin-risk scan | None — substrate scan |
| 5 | `F-REFLECTION-INTENT-ANCHOR-DRIFT` | POST-write META | Rolling N-cycle similarity check between reflection trajectory and original task anchor exceeds threshold | N = operator-configured rolling window (default: 5 cycles) | Computed across class-1 + class-2 events |
| 6 | `F-REFLECTION-DEPTH-EXCEEDED` | PRE-fire | Reflection-of-reflection depth exceeds bound | Hard cap: depth-1 at v0.2; v1.x configurable | None — counter |
| 7 | `F-REFLECTION-CONTENT-LOOP-DETECTED` | POST-write | Reflection text similarity to last K reflections exceeds threshold | K = 5, threshold = operator-configured (default: cosine 0.85) | None — content similarity |
| 8 | `F-REFLECTION-SELF-EVALUATOR-FAMILY-CLASH` | PRE-fire | Reflection critic and reflection author share model family | N/A — router.yaml family field comparison | Extends A3 cross-family rigor |
| 9 | `F-REFLECTION-SYCOPHANCY-LOOP-DETECTED` | META (cycle-level) | Score-vs-cycle slope > 0 over N cycles AND corpus-drift entropy < threshold | N = operator-configured (default: 4 cycles) | Computed across class-7 + class-8; correlates against class-1 + class-6 |
| 10 | `F-REFLECTION-EVAL-SURROGATE-DIVERGENCE` | META (cycle-level) | Judge / Red Team scores improve while ground-truth (funded ↔ class-1) flat-or-down across window W | W = operator-configured (default: 8 cycles) | Two ledgers: class-7+8 vs. class-1 |
| 11 | `F-REFLECTION-SELF-REPORTED-CONFIDENCE` | POST-write (rewrites) | Reflection text contains self-reported confidence value | N/A — string-match + field-presence | LLM-self-confidence values discarded; deterministic value computed from class-1..6 evidence counts |
| 12 | `F-REFLECTION-FABRICATION-ON-FAILURE` | POST-effect | Reflection claimed verdict ≠ underlying gate-outcome ledger | N/A — hash comparison | Class-3 ground truth |
| 13 | `F-REFLECTION-OPERATOR-OVERRIDE-MASK` | PRE-write | Reflection proposes write to key operator has explicitly set in classification register / PROJECT_CONTEXT / per-grant SP0 | N/A — key-set membership | Class-2 inputs |
| 14 | `F-REFLECTION-INOCULATION-FRAME-MISSING` | PRE-fire (template) | Reflection prompt template lacks fixed-string inoculation frame from signed template store | N/A — template-hash verification | None — template integrity |
| 15 | `F-REFLECTION-WRITE-WITHOUT-COMMIT` | COMMIT | Reflection write attempted outside output-validator-success → commit path | N/A — journal/commit pattern enforcement | Mirrors §12 Uploader prepare-and-stage |
| 16 | `F-REFLECTION-PROBE-COVERAGE-INCOMPLETE` | META (pre-cycle deployment) | v0.2/v1.x deployment ships without required probe families | Required probe registry: {sycophancy, loop_divergence, fabrication_on_failure, proxy_metric_drift} | None — probe registry membership |
| 17 | `F-REFLECTION-COVERAGE-INCOMPLETE` | META (PRE-cycle) | Any F-REFLECTION-* primitive unrealized at runtime | N/A — analog of `F-CLASS-COVERAGE-INCOMPLETE` | None — gate-realization registry |

### §4.4 Reservations (deferred to v0.2 or v1.x amendment)

These three appeared in Lane 3/5 but depend on substrate not yet specced; surfaced as registrations-only at v0.1 Beta hook with no predicate body:

- `F-REFLECTION-TRIGGER-THRESHOLD-NOT-MET` — needs Park-style importance scoring substrate (v1.x)
- `F-REFLECTION-STALE-ABOVE-THRESHOLD` — needs reflection-staleness ledger (v1.x)
- `F-REFLECTION-OPERATOR-PIN-VIOLATION` — needs per-reflection pin metadata (v1.x)

### §4.5 PRE/POST/COMMIT/META position distribution

Of the 17 new top-level codes:
- **PRE-fire** (4): #6, #8, #14, #17
- **PRE-write** (5): #1, #2, #3, #4, #13
- **POST-write** (3): #5, #7, #11
- **POST-effect** (1): #12
- **COMMIT** (1): #15
- **META cycle/deployment** (3): #9, #10, #16

This distribution matches §4 Logician v2.x.1 PRE/POST/COMMIT layering. The META-gate cluster (#9, #10, #16) is the new structural axis Reflection introduces — cycle-level analysis rather than per-call analysis. Pattern-matches `F-PIPE-TRACK-FROZEN` META (row 188-189) but at a different temporal scope.

---

## §5. The Pydantic AI shape (Lane 4)

### §5.1 Four gate-insertion seams

| Pydantic AI seam | When it fires | F-REFLECTION-* gates routed here |
|---|---|---|
| `history_processors` | Before every model request, pre-token-spend | `F-ARCHIVIST-CROSS-ORG-LEAK.reflection_cross_org_read`, `F-REFLECTION-OPERATOR-OVERRIDE-MASK` |
| `@agent.system_prompt` / `@agent.instructions` | Run-start | `F-REFLECTION-INOCULATION-FRAME-MISSING`, `F-REFLECTION-DEPTH-EXCEEDED`, `F-REFLECTION-SELF-EVALUATOR-FAMILY-CLASH` |
| `@agent.tool` body (entry) | Model invokes a reflection tool | `F-REFLECTION-NO-EXTERNAL-SIGNAL`, `F-REFLECTION-EVAL-ONLY-GROUNDED`, `F-REFLECTION-INSUFFICIENT-EVIDENCE`, `F-REFLECTION-RFA-SPEC-OVERRIDE`, `F-ARCHIVIST-READ-WITHOUT-VAULT-INTENT.reflection_evidence_out_of_run`, `F-ARCHIVIST-LESSON-INSTANCE-LEAK.reflection_instance_in_pattern_field` |
| `@agent.output_validator` | After model produces final structured output | `F-REFLECTION-CONTENT-LOOP-DETECTED`, `F-REFLECTION-SELF-REPORTED-CONFIDENCE`, `F-REFLECTION-FABRICATION-ON-FAILURE`, `F-REFLECTION-INTENT-ANCHOR-DRIFT` |
| (COMMIT layer) | output_validator success → commit; failure → rollback | `F-REFLECTION-WRITE-WITHOUT-COMMIT`, `F-ARCHIVIST-AUTO-APPLY-ATTEMPTED.reflection_attach_unsigned` |

META-gates (#9, #10, #16) fire at cycle boundaries outside Pydantic AI's per-call seams — they're invoked by Archivist's cadence orchestrator, not the reflection_agent itself.

### §5.2 Dedicated reflection_agent (separate from seat agents)

Per Lane 4's recommendation §7.2: small dedicated `reflection_agent` (Pydantic AI `Agent` instance), three tools (`read_priors`, `record_reflection`, `score_against_priors`), its own `Deps`, **always-local classification posture** (Reflection derives from post-fill drafts which contain Confidential KFR-resolved slot values; per v7.0.7, any input containing Confidential → local-only). The seat-mode-dispatcher inside Archivist constructs this agent on `--cadence reflection` and tears it down at end-of-cadence. Cleanly isolated Logfire spans; gate ownership unambiguous (all `F-REFLECTION-*` on this one agent).

### §5.3 Per-org store at canonical-gate-checked path

`orgs/<slug>/vault/reflection/store.{yaml,sqlite}` — matches the canonical-gate-checked path pattern for `orgs/<slug>/vault/classification/register.yaml` (per the Classification Review wrapper landed earlier this cycle). The four `F-ARCHIVIST-*.reflection_*` sub-tags + the storage gates use this path. `ReflectionStore` is org-bound at construction; cross-org instantiation raises `CriticalPolicyError(BaseException)` at module load (mirrors §13 Cedar engine discipline + §4 v2.x.1 immutability hardening).

### §5.4 Journal/commit pattern (GH #4679 anti-pattern mitigation)

`record_reflection` tool writes to a journal entry under `pipeline/validation/reflection_journal/<run_id>/<entry_id>.yaml`. Only on `output_validator` success does the COMMIT-gate flip the journal entry → live `store.yaml`. On `output_validator` failure (including any `F-REFLECTION-*` POST-write fail), the journal entry is preserved (Rule 1 — Save State Always — on failure too) but never reaches live state. Mirrors §12 Uploader prepare-and-stage discipline exactly. `F-REFLECTION-WRITE-WITHOUT-COMMIT` enforces.

### §5.5 What this means for v0.1 Beta hook

At v0.1 Beta hook, none of the Pydantic AI seams are wired (no reflection_agent constructed). The gate primitives exist as dormant Cedar/Python predicates registered at the architectural-primitive layer — they enumerate the predicate signatures + the substrate paths + the dependency on the not-yet-built reflection_agent. `F-REFLECTION-COVERAGE-INCOMPLETE` is the PRE-cycle META-gate that prevents any v1.x Beta deployment shipping without the predicate bodies realized (matches `F-CLASS-COVERAGE-INCOMPLETE` precedent from v7.0.7).

---

## §6. The Anthropic Dreams gap — what Tilth adds

Anthropic shipped Dreams on 2026-05-06; Lane 2 documents what's there. The seven gaps Tilth-Reflection closes:

| Capability | Anthropic Dreams | Tilth-Reflection |
|---|---|---|
| **PII / admin-risk-term scanning at dream-time** | Not present — dream sees whatever's in input transcripts | Law 4 scanner runs PRE-write; operator approves each substitution. `F-REFLECTION-RFA-SPEC-OVERRIDE` is the structural enforcement |
| **Provenance preservation during consolidation** | Not present — dreams merge duplicates without explicit per-fact provenance | Verbatim-quote-with-page provenance per Tilth KFR pattern preserved; `F-ARCHIVIST-LESSON-INSTANCE-LEAK.reflection_instance_in_pattern_field` enforces |
| **Cross-family review of consolidation output** | Relies on operator review at attach time only | L-003 cross-family rigor extended to reflection writes; `F-REFLECTION-SELF-EVALUATOR-FAMILY-CLASH` enforces; Editor + Red Team PRE-attach review required |
| **Signed audit trail** | Dream-id + session-id only; no cryptographic attestation | Ed25519 on `(input_hash, output_hash, run_id, operator_attach_decision, timestamp_utc)` per reflection run; mirrors v7.0.4-M1 KFR canonical-signing regime |
| **Classification-driven routing** | Workspace-isolated only; no per-call classification posture | Per v7.0.7: any Confidential input → local-only; `F-CLASS-ROUTING-INDETERMINATE` extension fail-closes; heavy-Judge swap analog for end-of-quarter consolidations |
| **Opaque-slot discipline** | Cloud-routed prompt sees raw content | Reflection's cloud-routed prompt (rare; reflection is typically always-local) uses opaque `[SLOT_<numeric_id>]` only per `F-CLASS-SLOT-ID-NON-OPAQUE` |
| **Inoculation framing in prompt** | No equivalent | Per Lane 5 F-4 (Anthropic's own emergent-misalignment work): reflection prompt template includes a fixed-string "self-improvement-as-acceptable" inoculation frame; `F-REFLECTION-INOCULATION-FRAME-MISSING` enforces template integrity |

**What Tilth-Reflection ships LESS of than Anthropic Dreams**: auto-trigger cadence (Tilth defers dual-gate to v1.x at earliest; Anthropic Auto Dream ships 24h+5-session dual-gate at launch). This is deliberate per Lane 3 + Lane 5 F-7 — operator-invoked is safer default until Classification Review UX matures.

---

## §7. Phased ship plan

### §7.1 v0.1 Beta hook (this cycle, parallel to Beta close-out)

**Scope.** Dormant Cedar/Python gate primitives at architectural-primitive layer. No reflection_agent constructed. No runtime invocation. Predicate signatures + substrate paths + dependency graph registered; bodies raise `NotImplementedError` (matches §15 v1 SPEC LOCK pattern for Archivist gates pending §4 v2.x WS-L realization).

**Artifacts produced.**
- **Architecture amendment** `pipeline/architecture/v0.1/architecture_v7_0_9_amendment.md` — registers 17 net-new top-level `F-REFLECTION-*` primitives + 5 sub-tag extensions; binds them to Archivist sub-mode seat-home decision; declares dormant-binding per L-006 precedent; companion-LOCK rows planned.
- **§4 v2.x.2 sub-amendment** `pipeline/blueprint/v0.1/section_04_logician_v2_x_2_amendment.md` — gate-family registrations at predicate-signature layer; NotImplementedError bodies; named drift-test bindings for v1.x amendment-realization.
- **§0.5 §15.x sub-tag extension** `pipeline/blueprint/v0.1/section_00_5_section_15_reflection_amendment.md` — 22 rows added to interface index (17 top-level + 5 sub-tag), follows §0.5 v15 amendment pattern from §13 LOCK today.
- **`F-REFLECTION-COVERAGE-INCOMPLETE` META-gate** registered at predicate-signature layer; prevents future v1.x Beta deployment shipping without realized predicates (matches `F-CLASS-COVERAGE-INCOMPLETE` precedent from v7.0.7).

**Cost.** LOW. No code beyond predicate-signature stubs. Doesn't compete with Intake / Uploader full-impl, Classification Review UX, or WS-L §4 v2.x Code phase. L-005 strict two-cycle Thesis with FULL live cross-family rigor (Editor=Llama/Groq, Judge=Gemini/Google, Red Team=GPT-OSS/Groq).

**Does NOT block v0.1 Beta close-out.** Reflection v0.1 hook is parallel; Beta gate primitives (`F-CLASS-COVERAGE-INCOMPLETE` etc.) ship independently.

### §7.2 v0.2 SPEC-only amendment (post v0.1 Beta first cut)

**Scope.** Full Reflection sub-mode SPEC LOCK. Mirrors §13/§14/§15 v0.2 SPEC-ONLY discipline. Predicates remain skeleton; implementation deferred to v1.x. Authored alongside the v0.2 family (§13 Data Collector + §14 Report Generator + §15 v1 already SPEC-LOCKED today).

**Artifacts.**
- **§15 v2.x amendment** `pipeline/blueprint/v0.1/section_15_archivist_v2_x_reflection_amendment.md` — adds third cadence to seat spec; input contract (`ArchivistReflectionInput`); output contract (`archivist_reflection_digest.v1` schema); operator-review surface; reflection_agent dispatcher; per-org store path; grounding signal class registry.
- **Companion §0.5 paired-commit** — 5 new schema-related rows.
- **Companion §4 v2.x.3 sub-amendment** — predicate body sketches (still NotImplementedError at v0.2 SPEC LOCK).
- **Operator UX wrapper** at `pipeline/orchestrator/seats/archivist/reflection_mode.py` SCAFFOLD (no live invocation).

**Cost.** MEDIUM. Mirrors §13/§14 v1 LOCK template; reuses §15 v1 seat-lifecycle wrapper extensively.

### §7.3 v1.x runtime amendment (post v0.2 Beta horizon)

**Scope.** Predicate bodies realize. Reflection_agent constructed. Three tools (`read_priors`, `record_reflection`, `score_against_priors`) live. Scheduled-task-driven cadence via `schedule` skill (per §15 J-06 slot transition: operator → archivist for the curation slot, including reflection). META-gates active.

**Artifacts.**
- **§4 v2.x.4 (or successor) sub-amendment** — predicate bodies live.
- **§15 v3.x amendment** — runtime invocation paths.
- **Heavy-Judge swap analog** — on-demand 200B-class local model loaded for end-of-quarter heavy consolidations per Lane 2 §Tilth implications #5.
- **Probe registry realization** — sycophancy, loop_divergence, fabrication_on_failure, proxy_metric_drift probes ship; `F-REFLECTION-PROBE-COVERAGE-INCOMPLETE` flips from META-stub to live PRE-cycle gate.

**Cost.** HIGH. Cross-family L-005 two-cycle. Touches §15, §4, §0.5, router.yaml.

### §7.4 Three-stage ship rationale

Matches the *Cards-vs-Cards-resolved-at-the-visual-layer-and-§8-deferred* pattern: ship the load-bearing primitive now (architecture v7.0.9 + §4 v2.x.2 + §0.5 §15.x), the spec next (§15 v2.x + §4 v2.x.3), the runtime last (§4 v2.x.4 + §15 v3.x). Operator decisions absorbed at each stage transition.

---

## §8. Answer Lane 2's five batched questions (from scoping draft §11)

**Q1. Target version scope (§7).** Three-stage default — v0.1 Beta hook dormant primitives + v0.2 SPEC-only amendment + v1.x runtime. The v0.1 hook is the only thing that ships this cycle; v0.2 SPEC composes with §13/§14/§15 family; v1.x runtime activates when Archivist transitions per J-06 slot.

**Q2. Seat home (§6).** Option A. Archivist sub-mode. Justified against §15 v1 SPEC's proposes-only / three-layer defense, J-06 slot-transition timing, v7.0.4 curation slot reservation, and Anthropic Dreams operator-attach pattern (see §2.1 of this memo). Lane 4's `reflection_agent` idiom is preserved internally — the seat-mode-dispatcher inside Archivist constructs the dedicated Pydantic AI agent on `--cadence reflection`.

**Q3. Trigger model default (§5).** Operator-invoked at v0.1/v0.2 (Option A from scoping draft §5). Per-grant SP0-bound (Option B) becomes opt-in per-org policy at v0.2 SPEC LOCK with `trigger_reflection_on_close: true` field. Dual-gate cadence (Option C) deferred to v1.x runtime — needs Classification Review UX to handle cadence-policy classification first (per scoping draft + Lane 5 F-7 evidence that auto-trigger without progress-evidence gating is the Auto-GPT failure mode).

**Q4. Lane synthesis timing.** All 5 lanes filed; this memo IS the synthesis. The pre-Thesis scoping draft's §1 frame (`Tilth-Reflection is a between-cycle Archivist sub-mode that reads (read-only) the live memory state plus N past session transcripts, produces a staged candidate memory state in a separate path, and refuses to displace the live state without operator attach-step approval`) survives lane synthesis intact. Thesis dispatch fires off this synthesis via the pre-staged packet (§10).

**Q5. v0.1 Beta competition.** Parallel, different session. Dormant gate primitives (v0.1 Beta hook) are LOW cost, do not compete with Beta finalization items: Intake full-impl, Uploader full-impl, Classification Review UX wrapper, WS-L §4 v2.x LOCK + Code phase, white-glove playbook subset. The Reflection v0.1 hook can dispatch immediately on coordinator bandwidth.

---

## §9. Open questions remaining for operator review

Five items the synthesis cannot resolve without operator input. Batched per CLAUDE.md "Batch all open questions":

1. **Top-level F-REFLECTION-* vs. all-sub-tag extension under F-ARCHIVIST-*.** Synthesis defaults to 17 new top-level codes + 5 sub-tag extensions. The "purist Option A" is to fold every reflection gate under F-ARCHIVIST-* sub-tags (extreme version of seat-home decision). Pro purist: seat-ownership clarity is monomaniacal; everything reflection-related rolls up under `F-ARCHIVIST-*`. Con purist: 17 sub-tags on existing parents would break sub-tag readability (the §4 v2.x.1 precedent of 6 sub-tags on `R-ARCHIVIST-NO-CANONICAL-MUTATE` is already at the upper bound of digestible). **Operator decision: synthesis default (17 top-level + 5 sub-tag) OR purist (22 sub-tags across 5 parents)?**

2. **Reflection cadence vs. existing weekly/quarterly cadences.** Synthesis recommends Reflection as a third top-level cadence (`tilth archivist reflection`). Alternative: Reflection rides as a sub-mode of quarterly (per-org Match DB outcome rollup naturally produces reflection feedstock at quarterly boundary). Pro third-cadence: clarity, independent invocation, separate audit trail. Pro sub-mode-of-quarterly: less surface, naturally aligned with funder outcome cadence. **Operator decision: third cadence OR sub-mode of quarterly?**

3. **Heavy-Judge swap analog for Reflection.** Lane 2 §Tilth-implications #5 surfaces this. Synthesis defaults YES — on-demand 200B-class local model loaded for end-of-quarter consolidations, mirroring Anthropic's opus-4-7 selection for Dreams pipeline model. Cost: NVMe storage + ~2-5 min wall per heavy cycle. **Operator decision: ship heavy-Reflection swap at v1.x runtime, or defer indefinitely?**

4. **Probe registry membership for `F-REFLECTION-PROBE-COVERAGE-INCOMPLETE`.** Synthesis proposes {sycophancy_probes, loop_divergence_probes, fabrication_on_failure_probes, proxy_metric_drift_probes} per Lane 5 §4 retrofits-that-worked + §7 gate sketch. Each probe family is non-trivial design work. **Operator decision: synthesis default set OR narrower / wider set?**

5. **Inoculation-frame template wording (`F-REFLECTION-INOCULATION-FRAME-MISSING`).** Lane 5 F-4 is the only evidence base — Anthropic's emergent-misalignment paper found "self-improvement is acceptable" framing cut misalignment generalization, even when reward-hacking still occurred. Synthesis flags but does not draft template wording. **Operator decision: who drafts? Synthesis recommends Cycle-1 Thesis-author (likely Scribe-class seat in a future session) per CLAUDE.md "Applicant brings substance" — Josh's voice on what reflection-acceptance looks like in Tilth's idiom.**

---

## §10. Pre-staged dispatch packet

**Location.** `pipeline/handoffs/ws_reflection_v0_1_hook_handoff_2026-05-10.md` (companion file landed alongside this memo).

**Pattern.** Matches today's WS-* handoff packets (compound-LOCK structure: amendment row + paired §0.5 sub-amendment + §4 v2.x sub-amendment). Compound-LOCK rows planned: architecture v7.0.9 amendment row + §4 v2.x.2 row + §0.5 §15.x sub-amendment row (paired-commit triple). L-005 strict two-cycle Thesis with FULL live cross-family rigor.

**Scope.** v0.1 Beta hook only — dormant Cedar/Python gate primitives. No reflection_agent. No runtime invocation. Predicate signatures + substrate paths + dependency graph + drift-test bindings.

**Dispatch readiness.** Packet is self-contained per CLAUDE.md handoff discipline (under 50 lines excluding bootstrap reference). Coordinator can fire when bandwidth opens.

---

## §11. Done definition checklist

- [x] Synthesis memo authored (this file)
- [x] Dispatch packet pre-staged at `pipeline/handoffs/ws_reflection_v0_1_hook_handoff_2026-05-10.md`
- [ ] Daily log entry (next file write)
- [ ] Session metrics entry (last act before sign-off)

No LOCK ceremony. No Cedar/Python implementation. Pure design synthesis + pre-staging.

---

## Sources

- All five lane files under `pipeline/research/reflection/`
- Scoping draft `pipeline/research/reflection/scoping_draft_reflection_as_archivist_submode.md`
- §15 Archivist v1 SPEC LOCKED 2026-05-10 row 191/192
- §4 v2.x.1 narrow-corrective LOCKED 2026-05-10 row 198/199 (sub-tag-extension pattern reference)
- §4 v2.x LOCKED 2026-05-10 rows 193/194 (L-006 dormant-binding ACTIVATED via F-CLASS-COVERAGE-INCOMPLETE)
- Architecture v7.0.4 §9 + §9.1 (curation slot reservation + J-06 closure)
- Architecture v7.0.7 LOCKED row 180 (classification-driven routing; F-CLASS-* gate family pattern)
- Architecture v7.0.4-M1 LOCKED row 190 (KFR canonicalization + Ed25519 signing regime; pattern reference for reflection-artifact signing)
- Classification Review operator UX wrapper LANDED 2026-05-10 (per-org vault path pattern reference)

---

## [v7.0.10 footer addendum 2026-05-11]

Architecture amendment v7.0.10 LOCKED 2026-05-11 (lock_history row 215) deprecates the "Sanitized" / opaque-slot-token posture entirely as a first-class customer-facing routing posture. The §6 row in this synthesis memo's "Opaque-slot discipline" capability — *"Reflection's cloud-routed prompt (rare; reflection is typically always-local) uses opaque [SLOT_<numeric_id>] only per F-CLASS-SLOT-ID-NON-OPAQUE"* — RETRACTS. Reflection's always-local-on-Confidential posture is preserved under v7.0.10 vocabulary (Reflection's reflection_agent always operates under Local-Only / Sovereign or Split-Context Hybrid posture; reflection inputs always carry Confidential content; reflection_agent's prompt never traverses cloud routing under any v7.0.10 posture). The other §6 capability rows are unchanged at v7.0.10.

See: pipeline/architecture/v0.1/architecture_v7_0_10_amendment.md §8

[end addendum]

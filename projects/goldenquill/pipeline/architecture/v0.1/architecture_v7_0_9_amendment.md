---
title: Tilth Architecture — Amendment v7.0.9 (Reflection v0.1 Beta hook — 8 BINDING + 9 HORIZON/PROBE-DEPENDENT F-REFLECTION-* primitives + 5 F-ARCHIVIST-* sub-tag extensions + Archivist sub-mode seat-home + grounding-signal-class registry + operator-supplied inoculation frame + internal-vs-external naming discipline)
filed: 2026-05-10
operator: Josh Inklovich
amendment_status: LOCKED 2026-05-10 — substantive architectural addition with operator-refined scope (8 BINDING F-REFLECTION-* primitives + 9 HORIZON/PROBE-DEPENDENT registrations + 5 F-ARCHIVIST-* sub-tag extensions + Archivist sub-mode seat-home binding + grounding-signal-class registry + F-REFLECTION-COVERAGE-INCOMPLETE META-gate ACTIVE as v0.1 BINDING + operator-drafted inoculation frame template wording + internal-vs-external naming discipline). Cedar/Python predicate bodies for the 8 BINDING gates ship as NotImplementedError stubs at §4 v2.x.2 paired sub-amendment (v0.1 hook); HORIZON gate bodies land at v0.2 SPEC §15 v2.x; PROBE-DEPENDENT gate body lands at v1.x runtime per probe-registry realization. L-005 strict two-cycle Thesis CLOSED with FULL LIVE CROSS-FAMILY RIGOR (Editor=Llama-3.3-70B/Groq + Judge=Gemini-2.5-Pro/Google + Red Team=GPT-OSS-120B/Groq via openclaw bridge per AGENTS.md). Cycle 1: Editor READY_TO_LOCK + 4 findings folded + Judge READY_TO_LOCK 99/100 + 1 LOW folded + Red Team REQUIRES_FIXES with 4 BLOCKING + 6 HIGH + 4 MED + 2 LOW (17 FOLDED + 5 BOUNDED-by-A1+A4 + 1 REJECTED-with-rationale per row-170 transparent disposition). Cycle 2: UNANIMOUS READY_TO_LOCK (Editor READY + Judge 100/100 + Red Team READY; no new probes; all 17 fold-ins CLOSED; all 5 BOUNDED MAINTAINED; 1 REJECTED MAINTAINED). Tenth substantive v0.1+v0.2 round to LOCK at FULL live cross-family rigor (after WS-D v7.0.5 + WS-F §12 + WS-E §11 + WS-H §2 v7.2 + WS-G §5 v8 + WS-K §15 + WS-C-M1 v7.0.4-M1 + WS-L §4 v2.x + WS-I §13 + WS-J §14 + §4 v2.x.1 narrow-corrective). First substantive Reflection-family LOCK in the audit trail. Companion-LOCK with §4 v2.x.2 sub-amendment + §0.5 v18 §15.x reflection sub-amendment (compound paired-commit triple per §6.17 Option-B; single-commit atomicity per §0.5 §15.x §G Cycle-1 RT-11 closure).
parent_lock: pipeline/architecture/v0.1/tilth_architecture_locked.md
parent_amendment: pipeline/architecture/v0.1/architecture_v7_0_7_amendment.md  # F-CLASS-* dormant-primitive precedent (L-006 dormant-binding pattern)
predecessor_amendments_chain:
  - v7.0.4 (LOCKED 2026-05-09; row 178) — KFR + SP0 + Logician fact-drift family
  - v7.0.4-M1 (LOCKED 2026-05-10; row 190) — narrow-corrective post cross-family verification
  - v7.0.5 (LOCKED 2026-05-10; row 179) — Funder Intel DB + Match DB + Scout channel G + Stage-5 consent-tier on-ramp + Archivist curation slot
  - v7.0.6 (SELF-LOCKED 2026-05-09) — six-seat roster + support-agent slots
  - v7.0.7 (LOCKED 2026-05-10; row 180) — classification-driven routing + F-CLASS-* dormant primitives; CANONICAL PRECEDENT FOR L-006 DORMANT-BINDING PATTERN + BINDING-vs-HORIZON SPLIT
  - v7.0.8 (LOCKED 2026-05-08) — CIC × CLC orthogonality F-CIC-CLC-COUPLING-VIOLATION enforcement
companion_amendment_paired_commit:
  - pipeline/blueprint/v0.1/section_04_logician_v2_x_2_amendment.md  # predicate-signature-layer realization (8 BINDING + 9 HORIZON/PROBE-DEPENDENT registrations + 5 sub-tag extensions; NotImplementedError bodies; named drift-test bindings; PRE/POST/COMMIT/META distribution)
  - pipeline/blueprint/v0.1/section_00_5_section_15_reflection_amendment.md  # interface-index rows: 1 marker + 17 failure-code rows (8 BINDING + 9 HORIZON/PROBE-DEPENDENT) — sub-tag extensions noted as annotations under existing rows 299-303 per §4 v2.x.1 row-198 precedent
companion_skeleton_landed:
  - pipeline/orchestrator/seats/archivist/reflection_mode.py  # SCAFFOLD only — Pydantic AI agent stub + dataclass schemas + 17 NotImplementedError predicate stubs + 5 sub-tag extension wiring + drift-test bindings
companion_tests_landed:
  - tests/logician/gates/test_reflection_gates_skeleton.py  # predicate-signature + sub-tag-coverage + binding-vs-horizon tier + META-gate registration tests
operator_refinement_session: 2026-05-10 mid-Thesis — operator pinned five scope reductions + one naming directive to keep v0.1 hook surface minimal and the binding-gate ↔ runtime-future contract tight. Refinement applied PRE-LOCK; this DRAFT reflects the post-refinement state.
authority_source: pipeline/research/reflection/synthesis_design_memo_2026-05-10.md (five-lane fold synthesis; coordinator-resolved Q1-Q5 open questions); architecture v7.0.7 LOCKED 2026-05-10 (F-CLASS-* dormant-primitive precedent at row 180 + Sovereign Node LLC continuous-tracking BINDING-vs-HORIZON split shape); architecture v7.0.4 §9 + §9.1 (curation slot reservation + J-06 slot-transition); §15 Archivist v1 SPEC LOCKED 2026-05-10 rows 191/192 (proposes-only / three-layer defense / F-ARCHIVIST-* family / J-06 slot-transition timing); §4 v2.x LOCKED 2026-05-10 rows 193/194 (L-006 dormant-binding ACTIVATED via F-CLASS-COVERAGE-INCOMPLETE META-gate — the canonical realization pattern this amendment mirrors); §4 v2.x.1 LOCKED 2026-05-10 rows 198/199 (sub-tag-extension precedent for the 5 F-ARCHIVIST-* parent extensions); Operator refinement 2026-05-10 mid-Thesis (scope reductions + naming directive).
version_wording_discipline: "DRAFT" in this file refers to pre-Thesis pre-LOCK on-disk state at filing time. "LOCKED" status flips at compound-LOCK ceremony pending unanimous L-005 strict two-cycle READY_TO_LOCK across Editor + Judge + Red Team with FULL live cross-family rigor. The 17 F-REFLECTION-* primitives (8 BINDING + 9 HORIZON/PROBE-DEPENDENT) + 5 sub-tag extensions + F-REFLECTION-COVERAGE-INCOMPLETE META-gate are named at v7.0.9 LOCK at the architectural-primitive layer. The 8 BINDING primitives have DORMANT Cedar/Python realization (predicate bodies raise NotImplementedError at §4 v2.x.2 paired sub-amendment — predicate-signature layer); the 9 HORIZON/PROBE-DEPENDENT primitives have NO predicate body even at signature layer (signature reserved; body lands at v0.2 SPEC or v1.x runtime). The §4 Logician v2.x.2 sub-amendment realizes the BINDING predicate signatures + named drift-test bindings in a PAIRED-LOCK with this amendment per WS-Reflection (architecture v7.0.9 + §4 v2.x.2 + §0.5 v18 §15.x land as a single compound transaction; neither lands without the other two).
threat_severity_at_v0_1_beta_hook: LOW — dormant Cedar/Python primitives only; no live reflection_agent constructed; no runtime invocation; no live cadence; predicate bodies raise NotImplementedError for BINDING gates and remain signature-only for HORIZON/PROBE-DEPENDENT gates. Activation gated by F-REFLECTION-COVERAGE-INCOMPLETE PRE-cycle META-gate (analog of F-CLASS-COVERAGE-INCOMPLETE per v7.0.7 §5.1). The v0.1 Beta hook does NOT compete with v0.1 Beta close-out items (Intake full-impl + Uploader full-impl + Classification Review UX wrapper + WS-L §4 v2.x LOCK + white-glove playbook subset); parallel session, independent compound-LOCK.
audit_trail: pipeline/validation/reflection_v0_1_hook_thesis_2026-05-10/
session_metrics: pipeline/metrics/session_log.jsonl
---

# Amendment intent

The v0.1 architecture as locked names six seats + five support-agent slots and routes drafting/review/scoring through classification-driven posture per v7.0.7. It has no architectural-primitive layer for **Reflection** — the between-cycle pattern-curation discipline that lessons-memory, sycophancy-loop detection, fabrication-on-failure detection, and proxy-metric-drift detection sit on top of. Anthropic shipped Dreams on 2026-05-06; five research lanes (Hermes, Anthropic Dreams, Academic literature, Pydantic AI design idiom, Field-failure forensics — read at `pipeline/research/reflection/lane_{1,2,3,4,5}*.md`) converged on a single architectural shape, synthesized at `pipeline/research/reflection/synthesis_design_memo_2026-05-10.md`. This amendment registers that shape's load-bearing primitives at the architectural-primitive layer so that future v0.2 SPEC + v1.x runtime amendments compose against a stable architectural commitment rather than redesigning the architecture each step.

**Operator-refined scope (2026-05-10 mid-Thesis).** The synthesis-default 17 BINDING primitives were operator-narrowed to 8 BINDING primitives with the rationale "17 binding gates would inherit a cathedral before the chapel exists — operator wants a real runtime future for every binding gate." The remaining 9 still register in this amendment + §4 v2.x.2 + §0.5 §15.x, but tagged either **HORIZON** (v0.2 SPEC realization dependency) or **PROBE-DEPENDENT** (depends on the narrowed probe registry). Sub-tag extensions on F-ARCHIVIST-* parents unchanged (still 5). Probe registry narrowed from synthesis-default {sycophancy, loop_divergence, fabrication_on_failure, proxy_metric_drift} to {sycophancy, proxy_metric_drift, fabrication_on_failure} — loop_divergence deferred (insufficient reflection volume in v0.2 to make it meaningful). Heavy-Reflection swap deferred ENTIRELY (no v1.x reservation as a planned dependency). Operator drafted the inoculation frame wording verbatim; registered here as the authoritative template body when the predicate lands at v0.2 SPEC.

This amendment introduces four load-bearing primitives at the architectural-primitive layer:

1. **F-REFLECTION-\* gate family — 8 BINDING dormant primitives (v0.1 hook) + 9 HORIZON / PROBE-DEPENDENT registrations (v0.2 / v1.x) + 5 sub-tag extensions on existing F-ARCHIVIST-\* parents.** Cedar/Python realization deferred to §4 v2.x.2 paired sub-amendment at predicate-signature layer (NotImplementedError bodies for the 8 BINDING; signature-only registration for the 9 HORIZON/PROBE-DEPENDENT). Activation gated by F-REFLECTION-COVERAGE-INCOMPLETE META-gate.

2. **Archivist sub-mode seat-home binding.** Reflection lives as a third cadence under §15 Archivist (sub-mode A from the pre-Thesis scoping draft per `pipeline/research/reflection/scoping_draft_reflection_as_archivist_submode.md`), alongside the existing `weekly` + `quarterly` cadences. **Operator-facing CLI surface** (external naming per §8 below): `tilth archivist lessons --org <slug>` or `tilth archivist lessons --workspace`. **Internal cadence flag value** (code-level, blueprint-level): `--cadence reflection`. Implementation mechanic: a dedicated `reflection_agent` (Pydantic AI Agent instance, three tools — `read_priors` / `record_reflection` / `score_against_priors` — own Deps, always-local classification posture) is constructed by Archivist's seat-mode-dispatcher on `--cadence reflection` and torn down at end-of-cadence. The user-facing surface is "Archivist's Lessons Memory cadence." The runtime under the hood is a separate Pydantic AI agent. Both framings are true at different layers.

3. **Grounding-signal-class registry.** Eight signal classes ranked highest authority → lowest, with the structural enforcement that no reflection ground only on `editor_verdict` / `judge_score` / `red_team_score` / `scribe_self_assessment` alone (Huang 2024 + Kamoi 2024 lesson from Lane 3 — Reflexion's HumanEval gains came from ground-truth unit tests, an oracle; intrinsic LLM-self-correction without external grounding degrades performance). Registry lives at the architectural-primitive layer; F-REFLECTION-NO-EXTERNAL-SIGNAL + F-REFLECTION-EVAL-ONLY-GROUNDED enforce as BINDING v0.1 primitives.

4. **Internal-vs-external naming discipline.** Internal name remains `reflection_agent` + "Reflection sub-mode" / "Reflection cadence" (code identifiers, blueprint text, architecture text, audit trails, internal docs). External-facing surfaces — README, docs/ARCHITECTURE_OVERVIEW.md, customer-facing materials, investor/business-plan language, operator-facing CLI — MUST use **"Lessons Memory"** / **"Outcome Learning"** / **"Funding Lessons Digest."** Rationale: the word "Reflection" without context implies self-awareness / self-improvement (uncomfortable customer/investor framing); "Lessons Memory" implies preservation-and-consolidation (accurate description of what the cadence actually does). Codified at §8 below.

# What changes

## §1. Seat-home decision — Archivist sub-mode (synthesis §2)

**Decision: Reflection is a third cadence under §15 Archivist.** Not a ninth support-agent slot. Not a Logician-orchestrated pipeline stage. The seat-home binding rides on four load-bearing inputs:

**§1.1 §15 Archivist v1 SPEC's proposes-only / three-layer defense (rows 191/192).** The three-layer defense (AST-lint at module load → runtime guard via Vault read intent → Cedar policy via F-ARCHIVIST-\* family) is the right enclosure for reflection writes. Reflection inherits it. No new R-REFLECTION-NO-CANONICAL-MUTATE AST-lint is needed — the existing R-ARCHIVIST-NO-CANONICAL-MUTATE (with its six sub-tags from §4 v2.x.1 row 198) already forbids the low-level write primitives reflection would otherwise reach for. Three of the five existing F-ARCHIVIST-\* gates already cover load-bearing reflection failure modes via sub-tag extension (§3 below).

**§1.2 §15 J-06 slot-transition timing (v7.0.4 §9.1 + v7.0.6).** Reflection rides the operator → archivist slot transition seam at v1.x without inventing a parallel transition. At v1.x, Reflection's cadence-driven invocation lands the same way Archivist's weekly + quarterly cadences land: scheduled-task-driven via the `schedule` skill, with operator-explicit invocation always remaining valid.

**§1.3 v7.0.4 curation slot reservation (§9 + §9.1).** The curation slot was reserved for KFR maintenance + Funder Intel curation + Match DB lessons-delta + Benchmarks Register freshness. Reflection is structurally a fourth member of this family — same operator-facing digest discipline, same proposes-only posture, same signed audit trail. Reservation absorbs it.

**§1.4 Anthropic Dreams' operator-attach pattern.** Archivist's existing operator-review surface (`tilth archivist review --org <slug> --cadence <weekly|quarterly>`) extends to `--cadence reflection` (internal) / `tilth archivist lessons` (external). The attach step is the existing review-and-confirm flow. Reflection's staged candidate enters `orgs/<slug>/archivist_digests/reflection_<run_id>.yaml` exactly the way weekly/quarterly digests do.

**Why not a ninth support agent.** New seat = new audit round + new §0.5 row + new router.yaml entry + new classification-register entry. Blast radius too high for marginal conceptual clarity gain. §15 already names "lessons memory" as a v1.x duty; Reflection IS lessons-memory-curation. "Archivist's third cadence is reflection over the lessons substrate."

**Why not a Logician-orchestrated pipeline stage.** Logician's deterministic-only doctrine doesn't fit LLM invocations. Reflection's pattern-detection prompt is an LLM call (per v1.x extraction substrate). Logician gates over it, but does not own the seat.

## §2. F-REFLECTION-* gate family — 8 BINDING + 9 HORIZON/PROBE-DEPENDENT (architectural-primitive layer)

Per L-006 (preflight enforcement-layer existence), a v7.0.9 LOCK that depends on aspirational Logician code violates the lesson. v7.0.9 LOCK names the F-REFLECTION-\* primitives at the **architectural-primitive layer** here with a **BINDING-vs-HORIZON split** matching the v7.0.7 precedent for F-CLASS-\* gates (BINDING gates have NotImplementedError bodies at predicate-signature layer; HORIZON gates have signature-only registration awaiting v0.2 SPEC bodies). The §4 Logician v2.x.2 sub-amendment realizes the predicate signatures in a **paired-LOCK** with this amendment.

### §2.1 BINDING primitives (8 — predicate signatures + NotImplementedError bodies ship at §4 v2.x.2)

These eight v0.1 BINDING gates are the architectural-primitive commitment for v0.1 Beta hook. Each has a NotImplementedError predicate body at §4 v2.x.2 (the body realizes at v1.x runtime amendment). Operator-rationale: "operator wants a real runtime future for every binding gate" — each of these eight has a concrete runtime path; the other nine depend on substrate not yet specced.

| # | Code | Stage | Scope | Failure mode | Grounding-signal class dependency (per §4) | Realization horizon |
|---|---|---|---|---|---|---|
| 1 | F-REFLECTION-NO-EXTERNAL-SIGNAL | PRE-write | per-reflection-write | `grounding_signal_classes: set[str]` field empty | Requires ≥1 class | v1.x runtime (body); v0.1 hook (signature) |
| 2 | F-REFLECTION-EVAL-ONLY-GROUNDED | PRE-write | per-reflection-write | `grounding_signal_classes` ⊆ {`editor_verdict`, `judge_score`, `red_team_score`, `scribe_self_assessment`} | Requires ≥1 of classes 1-6 per §4 | v1.x runtime (body); v0.1 hook (signature) |
| 3 | F-REFLECTION-INSUFFICIENT-EVIDENCE | PRE-write | per-reflection-write | Reflection generalizes from < N independent grant cycles (N = operator-configured at white-glove; default 3 per-funder, 2 per-CIC, 5 per-CLC) | Counts class-1 + class-6 events | v1.x runtime (body); v0.1 hook (signature) |
| 4 | F-REFLECTION-RFA-SPEC-OVERRIDE | PRE-write | per-reflection-write | Reflection text asserts funder intent / RFA scope not present in original RFA + PROJECT_CONTEXT (string-match + Law-2 admin-risk scan) | None — substrate scan | v1.x runtime (body); v0.1 hook (signature) |
| 5 | F-REFLECTION-DEPTH-EXCEEDED | PRE-fire | per-reflection-invocation | Reflection-of-reflection depth exceeds bound (hard cap: depth-1 at v0.2; v1.x configurable) | None — counter | v1.x runtime (body); v0.1 hook (signature) |
| 6 | F-REFLECTION-SELF-EVALUATOR-FAMILY-CLASH | PRE-fire | per-reflection-invocation | Reflection critic and reflection author share model family (router.yaml family field comparison) | Extends A3 cross-family rigor | v1.x runtime (body); v0.1 hook (signature) |
| 7 | F-REFLECTION-WRITE-WITHOUT-COMMIT | COMMIT | per-reflection-write | Reflection write attempted outside output-validator-success → commit path (mirrors §12 Uploader prepare-and-stage discipline) | None — journal/commit pattern enforcement | v1.x runtime (body); v0.1 hook (signature) |
| 8 | F-REFLECTION-COVERAGE-INCOMPLETE | META | PRE-cycle | Any F-REFLECTION-\* BINDING primitive unrealized at runtime (analog of F-CLASS-COVERAGE-INCOMPLETE from v7.0.7 §5.1) | None — gate-realization registry | v0.1 hook (ACTIVE — coverage check against BINDING set) |

**Why these 8.** Each has a concrete runtime mechanism the v1.x amendment can realize without inventing new substrate primitives. NO-EXTERNAL-SIGNAL + EVAL-ONLY-GROUNDED + INSUFFICIENT-EVIDENCE enforce the grounding-signal-class registry (§4) — Lane 3's killer insight; all three have clear field-set + count semantics. RFA-SPEC-OVERRIDE composes against existing string-match + Law-4 admin-risk scanner (already on disk). DEPTH-EXCEEDED is a counter. SELF-EVALUATOR-FAMILY-CLASH is a router.yaml field comparison. WRITE-WITHOUT-COMMIT mirrors §12 Uploader prepare-and-stage discipline (already on disk). COVERAGE-INCOMPLETE is the META-gate analog of v7.0.7's F-CLASS-COVERAGE-INCOMPLETE (already proven pattern). The remaining nine depend on probes (sycophancy / proxy-metric-drift / fabrication-on-failure) or substrate (intent-anchor ledger / similarity index / template-store) that v0.2 SPEC introduces or v1.x runtime activates.

### §2.2 HORIZON primitives (8 — v0.2 SPEC realization dependency; signature-only registration at v0.1 hook)

These gates have **no predicate body at v0.1 hook** — not even NotImplementedError. The signature is reserved in the gate registry; v0.2 SPEC §15 v2.x Reflection amendment authors the predicate signature with NotImplementedError body; v1.x runtime amendment authors the body. The HORIZON tier exists to keep the v0.1 architectural-primitive layer honest about scope without losing the design memory.

| # | Code | Stage | Scope | Failure mode | Realization path |
|---|---|---|---|---|---|
| 1 | F-REFLECTION-INTENT-ANCHOR-DRIFT | POST-write META | rolling N-cycle window | Rolling N-cycle similarity check between reflection trajectory and original task anchor exceeds threshold (N = operator-configured rolling window; default 5 cycles) | v0.2 SPEC: signature lands. v1.x: needs intent-anchor ledger substrate + similarity index. |
| 2 | F-REFLECTION-CONTENT-LOOP-DETECTED | POST-write | per-reflection-write | Reflection text similarity to last K reflections exceeds threshold (K = 5, threshold = operator-configured; default cosine 0.85) | v0.2 SPEC: signature lands. v1.x: needs similarity-index substrate. |
| 3 | F-REFLECTION-EVAL-SURROGATE-DIVERGENCE | META | cycle-level | Judge / Red Team scores improve while ground-truth (funded ↔ class-1) flat-or-down across window W (W = operator-configured; default 8 cycles) | v0.2 SPEC: signature lands. v1.x: needs paired-ledger substrate (class-7+8 vs. class-1). |
| 4 | F-REFLECTION-OPERATOR-OVERRIDE-MASK | PRE-write | per-reflection-write | Reflection proposes write to key operator has explicitly set in classification register / PROJECT_CONTEXT / per-grant SP0 (key-set membership) | v0.2 SPEC: signature lands. v1.x: needs operator-pin-metadata substrate. |
| 5 | F-REFLECTION-INOCULATION-FRAME-MISSING | PRE-fire | per-reflection-invocation (template) | Reflection prompt template lacks fixed-string inoculation frame from signed template store (template-hash verification against operator-supplied authoritative wording per §7 below) | v0.2 SPEC: signature lands + template-store substrate. v1.x: hash-verification runtime. |
| 6 | F-REFLECTION-SELF-REPORTED-CONFIDENCE | POST-write | per-reflection-write (rewrites) | Reflection text contains self-reported confidence value; LLM-self-confidence values discarded; deterministic value computed from class-1..6 evidence counts | v0.2 SPEC: signature lands. v1.x: needs evidence-count substrate + rewrite path. |
| 7 | F-REFLECTION-FABRICATION-ON-FAILURE | POST-effect | per-reflection-write | Reflection claimed verdict ≠ underlying gate-outcome ledger (hash comparison against class-3 ground truth) | v0.2 SPEC: signature lands. v1.x: needs class-3 ledger live. Realized as part of `fabrication_on_failure_probes` per §6 probe registry. |
| 8 | F-REFLECTION-PROBE-COVERAGE-INCOMPLETE | META | pre-cycle deployment | v1.x deployment ships without required probe families (probe registry per §6) | v0.2 SPEC: signature lands. v1.x: probe registry realization flips this from META-stub to live PRE-cycle gate. |

### §2.3 PROBE-DEPENDENT primitive (1 — depends on narrowed probe registry)

This gate has signature-only registration at v0.1 hook; predicate body realizes when the corresponding probe family activates at v1.x runtime.

| # | Code | Stage | Scope | Failure mode | Realization path |
|---|---|---|---|---|---|
| 1 | F-REFLECTION-SYCOPHANCY-LOOP-DETECTED | META | cycle-level | Score-vs-cycle slope > 0 over N cycles AND corpus-drift entropy < threshold (N = operator-configured; default 4 cycles); depends on `sycophancy_probes` family per §6 probe registry | v0.2 SPEC: signature lands. v1.x: predicate body realizes when `sycophancy_probes` ship per §6 narrowed probe registry. |

### §2.4 v1.x reservations (named at architectural-primitive layer; NO predicate body at any tier in this triple; bodies land at v1.x runtime amendment per §6.3)

- F-REFLECTION-TRIGGER-THRESHOLD-NOT-MET — needs Park-style importance scoring substrate (v1.x)
- F-REFLECTION-STALE-ABOVE-THRESHOLD — needs reflection-staleness ledger (v1.x)
- F-REFLECTION-OPERATOR-PIN-VIOLATION — needs per-reflection pin metadata (v1.x)

These three are NOT in the seventeen registered at v0.1 hook; they are surfaced here as forward-binding markers so v1.x amendment authors know the registry was forward-aware.

### §2.5 Architectural commitment — dormant pattern per L-006 + v7.0.7 §5.1 precedent

The 17 F-REFLECTION-\* primitives above (8 BINDING + 8 HORIZON + 1 PROBE-DEPENDENT) are named at v7.0.9 LOCK at the architectural-primitive layer. The §4 v2.x.2 paired sub-amendment is bound at its OWN LOCK time to:

1. Register all 8 BINDING predicate signatures with NotImplementedError bodies + named drift-test bindings (per §4 v2.x.1 row-198 sub-tag-extension pattern).
2. Register all 8 HORIZON predicate signatures with `# SIGNATURE-ONLY at v0.1 hook; body lands at v0.2 SPEC §15 v2.x` comment-marker (no body at v0.1).
3. Register the 1 PROBE-DEPENDENT predicate signature with `# SIGNATURE-ONLY at v0.1 hook; body lands at v1.x runtime per probe registry realization` comment-marker.

Any §4 v2.x.2 paired sub-amendment that omits, reorders, or weakens these primitives fails the v7.0.9 architectural commitment and cannot LOCK. The dormant-binding matches the proven F-CLASS-\* pattern from v7.0.7 LOCK 2026-05-10 — architectural names primitives at v0.1 LOCK; the binding fires at the future spin's LOCK ceremony.

**Why this is L-006-compliant.** L-006 prohibits "locking around ASPIRATIONAL infrastructure" but allows architectural primitives "scoped to the future phase that brings the ASPIRATIONAL mechanism online." v7.0.9 §2.1 names the EXISTS-tier architectural primitives (this table is on-disk evidence — not aspirational). §2.2 + §2.3 name the FORWARD-binding primitives, each with an explicit realization path. The Cedar/Python predicate-body realization is the named future phase (§4 v2.x.4 at v1.x runtime amendment). The structural-Reflection claim of v7.0.9 §1 is anchored by the on-disk BINDING primitive table here + the predicate-signature table at the §4 v2.x.2 paired sub-amendment, not by code that doesn't yet exist.

## §3. Sub-tag extensions on existing F-ARCHIVIST-* parents (synthesis §4.2 — unchanged by operator refinement)

Five sub-tag extensions fold under the existing 5-gate F-ARCHIVIST-\* family per the §4 v2.x.1 narrow-corrective sub-tag-extension pattern (row 198, six sub-tags on R-ARCHIVIST-NO-CANONICAL-MUTATE). Each extension inherits AST-lint enforcement + runtime guard + Cedar policy from the parent. Operator refinement did not alter the sub-tag extension set — these five remain v0.1 BINDING (their parent F-ARCHIVIST-\* gates are already live at §4 v2.x WS-L LOCK rows 193/194).

| Parent F-ARCHIVIST-* code | New sub-tag | Lane source | Predicate sketch |
|---|---|---|---|
| F-ARCHIVIST-CROSS-ORG-LEAK | `.reflection_cross_org_read` | Lane 1 + Lane 4 + Lane 5 F-14 | Reflection invocation crosses `org_slug` boundary during read; reuses existing symlink-escape + Vault-read-intent enforcement |
| F-ARCHIVIST-AUTO-APPLY-ATTEMPTED | `.reflection_attach_unsigned` | Lane 1 + Lane 2 + Lane 5 F-2 / F-3 | Reflection digest attach attempted without operator Ed25519 signature on `(input_hash, output_hash, run_id)` |
| F-ARCHIVIST-LESSON-INSTANCE-LEAK | `.reflection_instance_in_pattern_field` | Lane 3 §3.2 + Lane 5 F-8 | Reflection pattern-summary field contains instance-level details that should have been pattern-rolled; reuses existing pattern-vs-instance enforcement |
| F-ARCHIVIST-CADENCE-DRIFT | `.reflection_interval_drift` | Lane 1 curator-interval-drift + Lane 2 cadence | Reflection cadence runs outside declared interval without operator-initiated flag |
| F-ARCHIVIST-READ-WITHOUT-VAULT-INTENT | `.reflection_evidence_out_of_run` | Lane 1 + Lane 4 EVIDENCE-OUT-OF-RUN | Reflection cites evidence outside the current run's transcript / KFR / Match DB substrate — bypassing Vault read intent |

**No new top-level F-ARCHIVIST-\* gates needed.** The existing five fully cover the reflection-as-substrate-write surface. Sub-tag extensions inherit AST-lint enforcement + runtime guard + Cedar policy from the parent — no parallel R-REFLECTION-\* AST-lint rule, no parallel predicate body, no parallel runtime-guard wrapper. The §0.5 §15.x paired sub-amendment registers these as sub-tag annotations under existing rows 299-303 (no new failure-code rows per §4 v2.x.1 row-198 sub-tag-extension §0.5 precedent). New top-level F-REFLECTION-\* predicates would (a) duplicate existing F-ARCHIVIST-\* coverage, (b) cost five additional gate-realization-registry entries with no semantic gain, and (c) break the single-source-of-truth contract between the AST-lint rule + runtime guard + Cedar policy at §15.9.3 / §15.13.1 line 694.

**Monotonic `run_id` discipline for `.reflection_attach_unsigned` sub-tag (Cycle-1 RT-01-C closure).** The Ed25519 signature on `(input_hash, output_hash, run_id)` per architecture v7.0.4-M1 audit-log monotonic-counter pattern is insufficient on its own — replay against a previously-signed `(input_hash, output_hash)` pair with a stale `run_id` would still satisfy verification. The v1.x runtime amendment MUST realize the `.reflection_attach_unsigned` sub-tag with a Vault-stored monotonic counter binding: the `run_id` MUST be strictly greater than the last recorded `run_id` for that `(input_hash, output_hash)` pair, with rejection-on-equal-or-less. Operator override requires per-grant SP0 signature + admin-risk ledger entry. v0.1 hook records the contract; v1.x amendment realizes the counter substrate.

## §4. Eight signal-class ranks — grounding-signal-class registry (synthesis §3.1 — the Lane 3 killer insight; 11 enum members across 8 ranks)

Lane 3's load-bearing claim: *Tilth's Reflection cannot ground on Judge scores.* Reflexion's HumanEval gains came from ground-truth unit tests (an oracle); Huang ICLR 2024 + Kamoi TACL 2024 demonstrate that when the evaluator is itself an LLM, intrinsic self-correction either fails to improve or actively degrades performance. Tilth's Judge is an LLM. Therefore Reflection must ground on something other than Judge alone.

**Eight signal classes (canonical, precedence-ordered, highest authority → lowest):**

| Rank | Class name | Source | Authority | Cadence | Determinism |
|---|---|---|---|---|---|
| 1 | `external_funder_outcome` | Funded / not funded ledger from Match DB | **Highest** — actual real-world signal | Slow (weeks-months post-submit), sparse | Binary, observed |
| 2 | `operator_approval` | Operator Ed25519-signed attach decision; KFR confirmation; classification decision; SP0 signature | High — operator-intent-laden but explicit | Dense at points of attach/confirm | Cryptographically attested |
| 3 | `logician_gate_outcome` | F-\* gate PASS / FAIL / sub-tag from PRE/POST gate executions | High — deterministic Python+Cedar, zero-token | Densest local signal | Fully deterministic |
| 4 | `kfr_drift_event` | KFR fact hash change; canonical-signature-invalidation; status transition | High — substrate ground truth | Event-driven, infrequent | Cryptographic hash diff |
| 5 | `admin_risk_event` | Law 4 flagged-term substitution; operator approve/reject of substitution | Medium-high — operator-mediated | Event-driven | Audited |
| 6 | `match_db_outcome` | Per (client × funder) cycle outcome rollup | Medium — aggregated proxy for class 1 until class 1 lands | Quarterly | Aggregated from class 1 + operator action_state |
| 7 | `council_split_event` | Judge × Red Team >10pt disagreement per A3 | **NOT primary** — same-trajectory signal; admitted only because cross-family rigor at A3 forces split derivation from different model families | Per draft | LLM-derived; only counts because cross-family rigor enforced |
| 8 | `editor_verdict` / `judge_score` / `red_team_score` / `scribe_self_assessment` (any single LLM-eval verdict alone) | LLM-only | **NEVER primary alone** — fails F-REFLECTION-EVAL-ONLY-GROUNDED | Per draft | LLM-derived |

**Precedence rule (the structural answer to Huang 2024).** A reflection's `grounding_signal_classes: set[str]` field is mandatory. F-REFLECTION-NO-EXTERNAL-SIGNAL fail-closes if the set is empty. F-REFLECTION-EVAL-ONLY-GROUNDED fail-closes if the set ⊆ {`editor_verdict`, `judge_score`, `red_team_score`, `scribe_self_assessment`}. At least one of classes 1-6 must be present. Class 7 is admitted because cross-family rigor at A3 forces the split signal to derive from *different model families*, which is the field-validated mitigation per Lane 5 retrofits-that-worked. But class 7 alone is insufficient — at least one of classes 1-6 must accompany it.

**Registry persistence at v0.1 hook.** The registry is named at v7.0.9 LOCK at the architectural-primitive layer. The §4 v2.x.2 paired sub-amendment realizes the enum at code-level (NotImplementedError predicate bodies for the 8 BINDING gates reference the enum members by name). Runtime population of class-1-through-6 ledgers happens at v1.x runtime amendment per §6.3.

## §5. F-REFLECTION-COVERAGE-INCOMPLETE META-gate — ACTIVE at v0.1 hook (synthesis §4.3 #17)

Per L-006 dormant-binding pattern + F-CLASS-COVERAGE-INCOMPLETE precedent (v7.0.7 §5.1):

**F-REFLECTION-COVERAGE-INCOMPLETE** is the PRE-cycle META-gate that fail-closes at every v1.x Beta cycle start: any v1.x pipeline cycle that attempts to run with Reflection cadence ACTIVE and any of the 8 BINDING predicate bodies NOT REALIZED is rejected. This is the v1.x Beta hard precondition: until v1.x runtime amendment LOCKs and realizes the 8 BINDING bodies, Reflection cadence is architecturally inactive and the deployment cannot ship v1.x Reflection.

**Coverage check scope.** META-gate checks the 8 BINDING primitives. HORIZON + PROBE-DEPENDENT primitives are NOT checked at v0.1 hook — they are forward-binding markers, not v0.1 coverage obligations. v0.2 SPEC promotes the 8 HORIZON gates to "signature-present" check; v1.x runtime promotes all 17 (BINDING + HORIZON + PROBE-DEPENDENT) to "body-realized" check.

**Operator-visible.** At v0.1 Beta hook (today), the Classification Review stage at white-glove cannot register `cadence_reflection_enabled: true` without F-REFLECTION-COVERAGE-INCOMPLETE clearance. The white-glove playbook subset at `docs/white_glove_v0_1_beta.md` (per Classification Review UX wrapper landed 2026-05-10) carries a forward-marker noting that Reflection cadence (externally: **Lessons Memory cadence**) is gated on v1.x runtime amendment LOCK.

**This is the architectural lever** that prevents v1.x Beta deployment from shipping with un-realized F-REFLECTION-\* BINDING enforcement. It matches the F-CLASS-COVERAGE-INCOMPLETE PRE-cycle gate behavior from v7.0.7 — same dormant-binding shape, different gate family, different target version (v1.x for Reflection vs. v0.1 Beta for Classification).

### §5.1 META-gate body preservation contract (Cycle-1 RT-05 closure)

A future v1.x amendment author could replace the F-REFLECTION-COVERAGE-INCOMPLETE predicate body with a stub returning `PASS` unconditionally (or NotImplementedError), effectively disabling the dormant-binding lever. Mirror of the same risk class faced by F-CLASS-COVERAGE-INCOMPLETE at v7.0.7 §5.1 + §4 v2.x rows 193/194. Neither precedent shipped a META-META gate as the structural counter — the discipline is encoded in **paired-commit + lock_history audit trail + L-005 strict two-cycle Thesis with FULL live cross-family rigor** at every amendment touching the META-gate body.

**Forward-binding contract on any v1.x amendment that modifies F-REFLECTION-COVERAGE-INCOMPLETE:**

1. The amendment MUST preserve the gate-realization-registry inspection behavior (predicate body returns FAIL_CLOSED iff any of the 7 NotImplementedError-bodied BINDING predicates lack realized body; PASS iff all are realized).
2. The amendment MUST add a Cycle-1 + Cycle-2 verification probe against the META-gate's behavior on a synthetic registry where each BINDING predicate is independently mocked NotImplementedError vs realized.
3. The amendment MUST cross-reference back to this §5.1 contract in its frontmatter.
4. The L-005 strict two-cycle Thesis MUST surface any deviation from these three contracts.

NO META-META gate is added — the contract relies on amendment-discipline + cross-family rigor + audit-trail integrity, matching the F-CLASS-COVERAGE-INCOMPLETE precedent.

## §6. Probe registry (operator-narrowed per Q4 refinement)

The synthesis-default probe registry was {sycophancy_probes, loop_divergence_probes, fabrication_on_failure_probes, proxy_metric_drift_probes}. Operator refinement narrows to three:

**Probe registry at v0.1 hook (architectural-primitive layer):**

| Probe family | Predicate it serves | Realization horizon |
|---|---|---|
| `sycophancy_probes` | F-REFLECTION-SYCOPHANCY-LOOP-DETECTED (PROBE-DEPENDENT per §2.3) | v1.x runtime |
| `proxy_metric_drift_probes` | F-REFLECTION-EVAL-SURROGATE-DIVERGENCE (HORIZON per §2.2) | v1.x runtime |
| `fabrication_on_failure_probes` | F-REFLECTION-FABRICATION-ON-FAILURE (HORIZON per §2.2) | v1.x runtime |

**Deferred (NOT in v0.1 hook registry):** `loop_divergence_probes` — operator rationale: "insufficient reflection volume in v0.2 to make it meaningful." Re-evaluation deferred to v1.x runtime amendment. If reflection volume crosses the threshold where loop divergence becomes measurable, the v1.x amendment may add the probe family + register a fourth PROBE-DEPENDENT predicate. Until then, F-REFLECTION-CONTENT-LOOP-DETECTED (HORIZON per §2.2 row 2) uses similarity-index substrate alone, not probe-based detection.

### §6.1 REQUIRED_PROBE_FAMILIES immutability contract (Cycle-1 RT-08 closure)

REQUIRED_PROBE_FAMILIES at `logician/gates/reflection_gates.py` is a Python tuple constant. The deferral of `loop_divergence_probes` is captured in operator rationale (architecture v7.0.9 §6) but Python tuples are mutable at source-edit time. A future v1.x author could silently re-add the deferred family by modifying the tuple — bypassing operator approval.

**Binding contract on any modification of REQUIRED_PROBE_FAMILIES:**

1. Modification requires a **paired-commit amendment** (paired with this architecture amendment family) + **operator Ed25519 sign-off** + a **lock_history row** documenting the change.
2. No silent re-addition. The skeleton test `test_required_probe_families_immutable_at_v0_1_hook` asserts the source file's tuple matches the v7.0.9 §6 architectural-primitive contract exactly: `("sycophancy_probes", "proxy_metric_drift_probes", "fabrication_on_failure_probes")` — drift in either direction (addition, removal, reordering) fails the test.
3. v0.2 SPEC + v1.x runtime amendments that propose to add a fourth family MUST cross-reference this §6.1 contract in frontmatter + explicit operator sign-off + dated lock_history entry.

This mirrors the discipline F-INDEX-STALE enforces on §0.5 row mutations — convention-level at v0.1 hook with a binding contract for future amendments.

**F-REFLECTION-PROBE-COVERAGE-INCOMPLETE** (HORIZON per §2.2 row 8) checks against this narrowed three-family registry, not the original four-family synthesis default. v1.x deployment shipping `sycophancy_probes` + `proxy_metric_drift_probes` + `fabrication_on_failure_probes` realized clears the gate; missing any of the three fail-closes.

## §7. Inoculation frame — operator-drafted template wording (Q5 closure)

Per synthesis §9 Q5 + operator refinement: template wording for F-REFLECTION-INOCULATION-FRAME-MISSING (HORIZON per §2.2 row 5) lands at v0.1 hook as operator-supplied authoritative wording. Predicate body deferred to v0.2 SPEC (signature) + v1.x runtime (hash-verification). At v0.1 hook the template string is registered as the authoritative wording so v0.2 SPEC amendment author + v1.x runtime predicate author have a stable string to hash-verify against.

**Authoritative inoculation frame body (operator-drafted, verbatim):**

> Reflection is permitted to improve process memory, identify recurring failure patterns, and propose safer future defaults. Reflection is not permitted to rewrite facts, override operator judgment, infer commitments, invent lessons from insufficient evidence, or treat evaluator approval as real-world success.

**Discipline.** This wording is the TEMPLATE BODY. The reflection prompt template at v0.2 SPEC must contain this exact string as a fixed-string preamble (delimited by sentinel markers `<INOCULATION_FRAME_BEGIN>` … `<INOCULATION_FRAME_END>` per v0.2 SPEC template-store discipline). The signed template store at v1.x runtime hash-verifies the preamble against `sha3_512(inoculation_frame_body_v1)` where `inoculation_frame_body_v1` is the verbatim text above (UTF-8, LF line endings, no trailing whitespace, no BOM).

**Why this wording is load-bearing.** Anthropic's emergent-misalignment paper (Lane 5 F-4) found that "self-improvement is acceptable" framing cut misalignment generalization even when reward-hacking still occurred. The operator's draft binds the SCOPE of acceptable reflection (improve process memory + identify recurring failure patterns + propose safer future defaults) AND enumerates the prohibited surfaces.

**Inoculation-frame prohibition → F-REFLECTION-\* gate map (Cycle-1 E-03 closure):**

| Inoculation-frame prohibition clause | Corresponding F-REFLECTION-\* gate(s) | Gate tier |
|---|---|---|
| "rewrite facts" | F-REFLECTION-RFA-SPEC-OVERRIDE | BINDING |
| "override operator judgment" | F-REFLECTION-OPERATOR-OVERRIDE-MASK | HORIZON |
| "infer commitments" | F-REFLECTION-RFA-SPEC-OVERRIDE + F-REFLECTION-INSUFFICIENT-EVIDENCE | BINDING |
| "invent lessons from insufficient evidence" | F-REFLECTION-INSUFFICIENT-EVIDENCE | BINDING |
| "treat evaluator approval as real-world success" | F-REFLECTION-EVAL-ONLY-GROUNDED + F-REFLECTION-EVAL-SURROGATE-DIVERGENCE | BINDING + HORIZON |

The wording is not stylistic — every prohibition clause has a structural enforcement gate.

**Hash-verification exact-match semantics (Cycle-1 RT-04 closure).** The v1.x runtime amendment's predicate body for F-REFLECTION-INOCULATION-FRAME-MISSING MUST enforce **exact-match semantics**, NOT substring-match. The predicate signature at §4 v2.x.2 §3 row 5 binds via the default keyword argument `exact_match: bool = True`. The body computation MUST be `hash = sha3_512(full_prompt.encode("utf-8")).hexdigest()` and the assertion MUST be `hash == INOCULATION_FRAME_BODY_V1_SHA3_512` — NEVER `INOCULATION_FRAME_BODY_V1_SHA3_512 in hash_set` or any containment check. v1.x author who realizes substring-match opens a prompt-injection bypass where an attacker prepends or appends adversarial content to the inoculation frame body. The drift test at `tests/logician/gates/test_reflection_inoculation_frame_missing_body_drift.py::test_substring_match_fails_closed` is a forward-binding v1.x deliverable per §4 v2.x.2 §11.

**Persistence at v0.1 hook.** The inoculation frame body text + its `sha3_512` digest are recorded at §4 v2.x.2 sub-amendment Appendix as `inoculation_frame_body_v1` + `inoculation_frame_body_v1_sha3_512`. The v0.2 SPEC amendment cross-references; v1.x runtime amendment realizes hash-verification against this digest.

## §8. Internal-vs-external naming discipline (NEW — operator directive 2026-05-10)

The word "Reflection" without context implies self-awareness / self-improvement — an uncomfortable framing for customer-facing materials, investor language, and business-plan documents. The accurate description of what the cadence does is preservation-and-consolidation of grant-cycle lessons memory. This amendment codifies a two-tier naming discipline:

### §8.1 Internal naming (UNCHANGED — code identifiers + blueprint text + architecture text + audit trails + internal docs)

| Layer | Term |
|---|---|
| Code identifier (Pydantic AI agent variable name) | `reflection_agent` |
| Module path | `pipeline/orchestrator/seats/archivist/reflection_mode.py` |
| Cadence flag value (internal CLI argument) | `--cadence reflection` |
| Blueprint / architecture text | "Reflection sub-mode" / "Reflection cadence" |
| Failure-code prefix | `F-REFLECTION-*` |
| AST-lint rule prefix (if any) | `R-REFLECTION-*` (none registered at v0.1 hook) |
| Test-file naming | `test_reflection_*.py` |
| Audit-trail directory naming | `pipeline/validation/reflection_*` |
| Memory-file naming | `project_*reflection*.md` |

### §8.2 External naming (NEW — README + docs/ARCHITECTURE_OVERVIEW.md + customer-facing materials + investor / business-plan language + operator-facing CLI)

| Surface | Term |
|---|---|
| Primary external term | **Lessons Memory** |
| Forward-looking alternative | **Outcome Learning** |
| Digest artifact name | **Funding Lessons Digest** |
| Operator-facing CLI surface | **`tilth archivist lessons --org <slug>`** / **`tilth archivist lessons --workspace`** |
| Customer-facing UI label (forward-binding for v2 GUI) | "Lessons Memory" panel / "Funding Lessons Digest" review |
| Business plan section heading | "Lessons Memory + Outcome Learning" |
| Investor pitch language | "Lessons Memory: between-cycle preservation of recurring-failure patterns + funder-outcome signals" |

**CLI surface choice rationale.** Operator gave discretion between `tilth archivist lessons` and `tilth archivist memory --cadence reflection`. This amendment selects **`tilth archivist lessons`** as the v0.1 customer-facing surface because (a) "lessons" reads as a direct noun rather than `memory --cadence reflection` which leaks the internal cadence taxonomy, (b) "lessons" aligns with the existing `pipeline/institutional_memory/lessons.json` + `/lessons.md` substrate (already on disk; customer-mental-model continuity), and (c) "memory" is broader than the actual scope (KFR is "memory" too; "lessons" is specifically the curation surface). The internal `--cadence reflection` flag still exists at the dispatcher layer; `tilth archivist lessons` is a customer-facing alias that resolves to `tilth archivist <internal-dispatch> --cadence reflection` under the hood.

### §8.3 Discipline enforcement

Two rules:

1. **No "Reflection" or "reflection" without internal context.** README, docs/ARCHITECTURE_OVERVIEW.md, customer-facing materials, investor/business-plan language MUST use the external terms from §8.2. Internal-context surfaces (blueprint files under `pipeline/blueprint/`, architecture files under `pipeline/architecture/`, code under `pipeline/orchestrator/`, audit trails under `pipeline/validation/`, this amendment text) continue to use the internal terms from §8.1.

2. **CLI prompts surface external names.** Operator-facing CLI help text + error messages + progress output use "Lessons Memory" not "Reflection." Internal log lines + audit-trail entries continue to use `reflection_agent` / `--cadence reflection` for grep-ability.

This discipline lands as a `# NO-EXTERNAL-NAMING-DRIFT` companion-edit guard in CLAUDE.md (per §11 companion file edits) + a `What NOT to Do` row in the same.

**Automated lint promotion (Cycle-1 RT-09 closure).** Manual review at v0.1 hook is convention-level — prone to drift across multiple v0.2 + v1.x authors. Promote to v0.2 SPEC deliverable:

- **Approved-terms JSON manifest** at `pipeline/blueprint/v0.1/assets/external_naming_approved_terms.json` recording the {Lessons Memory, Outcome Learning, Funding Lessons Digest} surface plus the `--cadence reflection` internal-cadence-flag value.
- **Documentation-lint test** at `tests/external_naming_discipline_test.py` (v0.2 forward-binding) scans `README.md`, `docs/ARCHITECTURE_OVERVIEW.md`, CLI `--help` strings, and Pydantic AI agent `description=` strings for the forbidden token "Reflection" outside of internal-context files (`pipeline/blueprint/`, `pipeline/architecture/`, `pipeline/orchestrator/`, `pipeline/validation/`, `logician/`, audit trails). Test fails if external-facing files contain the word "Reflection" without an explicit `# INTERNAL-NAMING-EXCEPTION` comment.
- **Lint rule landing horizon:** v0.2 SPEC amendment authors the test + manifest; v1.x runtime amendment may extend to CI integration. v0.1 hook records the contract here.

Compliance verification at v0.2 SPEC + v1.x runtime LOCK ceremonies via the documentation lint pass.

## §9. Phased ship plan (synthesis §7 — operator-refined scope)

### §9.1 v0.1 Beta hook (THIS amendment + paired §4 v2.x.2 + §0.5 v18 §15.x triple)

**Scope.** Dormant Cedar/Python gate primitives at architectural-primitive layer per the operator-refined BINDING-vs-HORIZON split. No reflection_agent constructed. No runtime invocation. No live cadence.

- 8 BINDING primitive predicate signatures + NotImplementedError bodies at §4 v2.x.2 (paired sub-amendment).
- 8 HORIZON primitive signatures reserved at §4 v2.x.2 with `# SIGNATURE-ONLY at v0.1 hook` comment-marker (no body).
- 1 PROBE-DEPENDENT primitive signature reserved at §4 v2.x.2 with `# SIGNATURE-ONLY at v0.1 hook` comment-marker (no body).
- 5 F-ARCHIVIST-\* sub-tag extensions per §3 — predicate bodies inherit from parent gates already live at §4 v2.x WS-L LOCK rows 193/194.
- Probe registry narrowed to three families per §6.
- Inoculation frame body authoritative wording recorded per §7.
- Internal-vs-external naming discipline codified per §8.

**Artifacts.**
- architecture v7.0.9 (THIS file)
- §4 v2.x.2 paired sub-amendment (predicate signatures + named drift-test bindings)
- §0.5 v18 §15.x reflection sub-amendment (rows added to interface index)
- `pipeline/orchestrator/seats/archivist/reflection_mode.py` SCAFFOLD only

**Cost.** LOW. No code beyond predicate-signature stubs. Doesn't compete with Intake / Uploader full-impl, Classification Review UX, or WS-L §4 v2.x Code phase. L-005 strict two-cycle Thesis with FULL live cross-family rigor (Editor=Llama/Groq, Judge=Gemini/Google, Red Team=GPT-OSS/Groq) via openclaw bridge.

**Does NOT block v0.1 Beta close-out.** Reflection v0.1 hook is parallel; Beta gate primitives (F-CLASS-COVERAGE-INCOMPLETE etc.) ship independently.

### §9.2 v0.2 SPEC-only amendment (post v0.1 Beta first cut)

**Scope.** Full Reflection sub-mode SPEC LOCK. Mirrors §13 / §14 / §15 v0.2 SPEC-ONLY discipline. Eight HORIZON gates promote from "signature-reserved at v0.1 hook" to "signature-present + NotImplementedError body at v0.2 SPEC." Predicates remain skeleton; implementation deferred to v1.x. Authored alongside the v0.2 family.

**Artifacts.**
- `pipeline/blueprint/v0.1/section_15_archivist_v2_x_reflection_amendment.md` — adds third cadence to seat spec; input contract (`ArchivistReflectionInput`); output contract (`archivist_reflection_digest.v1` schema); operator-review surface; reflection_agent dispatcher; per-org store path; grounding signal class registry realization.
- Companion §0.5 paired-commit — 5 new schema-related rows.
- Companion §4 v2.x.3 sub-amendment — 8 HORIZON predicate signatures land with NotImplementedError bodies; PROBE-DEPENDENT predicate stays signature-only.
- Operator UX wrapper at `pipeline/orchestrator/seats/archivist/reflection_mode.py` SCAFFOLD lifted to SPEC.
- Inoculation frame template store substrate per §7.

**Cost.** MEDIUM. Mirrors §13 / §14 v1 LOCK template; reuses §15 v1 seat-lifecycle wrapper extensively.

### §9.3 v1.x runtime amendment (post v0.2 Beta horizon)

**Scope.** Predicate bodies realize for all 17 F-REFLECTION-\* primitives (8 BINDING bodies first; 8 HORIZON bodies second; 1 PROBE-DEPENDENT body third — depends on `sycophancy_probes` realization). Reflection_agent constructed. Three tools (`read_priors`, `record_reflection`, `score_against_priors`) live. Scheduled-task-driven cadence via `schedule` skill (per §15 J-06 slot transition: operator → archivist for the curation slot, including reflection). META-gates active.

**Artifacts.**
- §4 v2.x.4 (or successor) sub-amendment — predicate bodies live (8 BINDING first; 8 HORIZON second; 1 PROBE-DEPENDENT third).
- §15 v3.x amendment — runtime invocation paths.
- Probe registry realization — `sycophancy_probes` + `proxy_metric_drift_probes` + `fabrication_on_failure_probes` per §6 narrowed registry; F-REFLECTION-PROBE-COVERAGE-INCOMPLETE flips from HORIZON-signature-only to live PRE-cycle gate.
- v1.x deployment may revisit `loop_divergence_probes` deferral if reflection volume crosses the meaningful-measurability threshold; if added, register fourth PROBE-DEPENDENT predicate at that ceremony.

**Cost.** HIGH. Cross-family L-005 two-cycle. Touches §15, §4, §0.5, router.yaml.

**NO heavy-Reflection swap binding.** Per operator refinement Q3: defer entirely. No swap-binding at v0.1 hook, no v1.x reservation as a PLANNED dependency. v1.x amendment may reserve "institutional/end-of-quarter consolidation" as a FORWARD MARKER only — never as a binding obligation. The heavy-Judge swap from v7.0.7 §4 stays scoped to Judge runs; reflection inherits Judge model bindings via router.yaml but does not invoke a separate heavy-Reflection swap path.

**No router-policy reuse for F-REFLECTION-\* (Cycle-1 RT-10 closure).** A v1.x amendment author MUST NOT reuse the heavy-Judge swap path for end-of-quarter Reflection consolidations under the rationale "we're using the existing Judge swap." Explicit binding:

1. The Cedar router-policy at v1.x runtime amendment MUST include a predicate `router_swap_allowed(gate_id: str) -> bool` that returns `False` for any gate ID matching `^F-REFLECTION-` regex.
2. The router.yaml schema at v1.x MUST reject any swap-list entry whose `gate_id` matches the F-REFLECTION-\* prefix at config-validation time.
3. Any future amendment proposing to enable a Reflection swap path MUST be paired with an operator-refinement amendment that explicitly overrides this deferral (mirrors §6.1 immutability contract on REQUIRED_PROBE_FAMILIES).
4. Drift test at `tests/router/test_router_swap_excludes_reflection.py` is a v1.x forward-binding deliverable.

### §9.4 Three-stage ship rationale

Matches the *Cards-vs-Cards-resolved-at-the-visual-layer-and-§8-deferred* pattern: ship the load-bearing primitive now (architecture v7.0.9 + §4 v2.x.2 + §0.5 v18 §15.x), the spec next (§15 v2.x + §4 v2.x.3 promoting HORIZON to signature-present), the runtime last (§4 v2.x.4 + §15 v3.x realizing all bodies). Operator decisions absorbed at each stage transition.

## §10. What this amendment does not do

- Does not modify A1-A12.
- Does not modify the Five Operating Laws or the Four Autonomy Rules.
- Does not modify Section K hardware tier mapping (128 GB Pro tier stands).
- Does not introduce new council seats — uses v7.0.6 roster.
- Does not modify v7.0.3 substrate decision (Pydantic AI substrate stands).
- Does not realize Cedar policy text or Python predicate bodies for any HORIZON or PROBE-DEPENDENT gate (deferred to v0.2 SPEC or v1.x runtime per §9).
- Does not construct the reflection_agent (v1.x scope).
- **Does not name a heavy-Reflection swap, neither at v0.1 hook nor as a planned v1.x dependency.** Per operator refinement Q3, the swap is deferred entirely; v1.x amendment may carry a FORWARD MARKER for "institutional/end-of-quarter consolidation" but no binding obligation. The heavy-Judge swap from v7.0.7 §4 remains scoped to Judge — reflection does not invoke a separate heavy-Reflection swap path.
- Does not specify v0.2 Reflection sub-mode SPEC details (input contract, output contract, operator-review surface, dispatcher) — that's §9.2 scope.
- Does not specify v1.x runtime invocation paths — that's §9.3 scope.
- Does not modify the F-CLASS-\* family or the classification-driven routing pattern from v7.0.7 — Reflection inherits all classification-driven routing posture (reflection_agent always-local per synthesis §5.2 because reflection derives from post-fill drafts which contain Confidential KFR-resolved slot values).
- Does not modify the F-ARCHIVIST-\* family's existing five top-level codes or their existing sub-tag closures — the five sub-tag extensions in §3 are additive only.
- Does not introduce a new Capital Logic Card or modify CIC × CLC orthogonality from v7.0.8.
- Does not retire or rename any v7.0.6 support-agent slot (Intake, Uploader, Data Collector, Report Generator, Archivist all stand).
- Does not modify the Classification Review stage's required steps from v7.0.7 §3 (white-glove operator review remains mandatory for v0.1 Beta; the `cadence_reflection_enabled` knob is forward-binding for v1.x and is gated on F-REFLECTION-COVERAGE-INCOMPLETE clearance).
- **Does not register a fourth probe family (`loop_divergence_probes`).** Per operator refinement Q4, the three families in §6 are the v0.1 hook registry; `loop_divergence_probes` is deferred entirely until v1.x runtime evaluates reflection volume measurability. The §6.1 immutability contract binds future amendments to operator sign-off for any change.
- **Does not enable a heavy-Reflection swap path.** Per operator refinement Q3, deferred entirely; §9.3 codifies the no-router-policy-reuse-for-F-REFLECTION-\* contract.
- **Does not realize the META-META gate.** F-REFLECTION-COVERAGE-INCOMPLETE has a live body at v0.1 hook (architecture v7.0.9 §5) but no META-META gate guards against its replacement at future amendment ceremonies. Per §5.1 the discipline is encoded in paired-commit + lock_history audit trail + L-005 strict two-cycle Thesis — matching the F-CLASS-COVERAGE-INCOMPLETE precedent at v7.0.7 §5.1 + §4 v2.x rows 193/194.

## §11. Companion file edits at LOCK

Pending L-005 two-cycle CLOSED verification, the following companion edits land at v7.0.9 LOCK (paired-commit pattern):

- **§4 v2.x.2 sub-amendment** (`pipeline/blueprint/v0.1/section_04_logician_v2_x_2_amendment.md`) — predicate-signature-layer registration of 8 BINDING F-REFLECTION-\* codes + 8 HORIZON signature-only reservations + 1 PROBE-DEPENDENT signature-only reservation + 5 F-ARCHIVIST-\* sub-tag extensions + named drift-test bindings; NotImplementedError bodies for BINDING set; PRE/POST/COMMIT/META distribution table; inoculation frame body Appendix per §7.
- **§0.5 v18 §15.x reflection sub-amendment** (`pipeline/blueprint/v0.1/section_00_5_section_15_reflection_amendment.md`) — interface-index row append: 1 marker + 17 failure-code rows (8 BINDING + 8 HORIZON + 1 PROBE-DEPENDENT). Sub-tag extension annotations under existing rows 299-303 per §4 v2.x.1 row-198 precedent.
- **`pipeline/orchestrator/seats/archivist/reflection_mode.py`** SCAFFOLD — Pydantic AI agent module skeleton + dataclass schemas + 17 NotImplementedError predicate stubs + 5 sub-tag extension wiring + drift-test bindings.
- **`tests/logician/gates/test_reflection_gates_skeleton.py`** — predicate-signature + sub-tag-coverage + binding-vs-horizon tier + META-gate registration tests.
- **CLAUDE.md** — adds two guards: (a) "What NOT to Do" row on Reflection cadence enabling without F-REFLECTION-COVERAGE-INCOMPLETE clearance (forward-binding for v1.x); (b) `NO-EXTERNAL-NAMING-DRIFT` guard codifying the internal-vs-external naming discipline per §8.
- **docs/ARCHITECTURE_OVERVIEW.md** — adds a "Lessons Memory" section (external naming per §8) noting the dormant-binding pattern; v0.1 Beta hook = primitive layer only; v1.x = runtime amendment.

NOT a v7.0.9 LOCK companion (deferred):
- v0.2 SPEC `§15 v2.x` Reflection amendment.
- v1.x runtime amendment.
- Heavy-Reflection swap decision — deferred entirely per operator refinement Q3.
- Probe registry realization — v1.x runtime amendment.
- `loop_divergence_probes` deferral re-evaluation — v1.x runtime.

The Logician §4 v2.x.4 runtime predicate-body realization is NOT a v7.0.9 LOCK companion — it lands at v1.x runtime amendment per the dormant-binding pattern. v7.0.9 LOCK + §4 v2.x.2 paired sub-amendment + §0.5 v18 §15.x paired sub-amendment is sufficient per L-006 architectural-corollary.

## §12. Cross-references

- **Parent locked architecture:** `pipeline/architecture/v0.1/tilth_architecture_locked.md` (v7 LOCKED 2026-04-19; A1-A12).
- **Canonical L-006 dormant-binding precedent:** `pipeline/architecture/v0.1/architecture_v7_0_7_amendment.md` §5.1 (F-CLASS-\* dormant-primitive family + F-CLASS-COVERAGE-INCOMPLETE META-gate; row 180).
- **Canonical sub-tag-extension precedent:** `pipeline/blueprint/v0.1/section_04_v2_x_1_amendment.md` (row 198) — six sub-tags on R-ARCHIVIST-NO-CANONICAL-MUTATE; the five F-ARCHIVIST-\* sub-tag extensions in §3 mirror this pattern.
- **Canonical L-006 ACTIVATION precedent:** `pipeline/blueprint/v0.1/section_04_v2_x_amendment.md` (rows 193/194) — F-CLASS-COVERAGE-INCOMPLETE META-gate ACTIVATED; F-REFLECTION-COVERAGE-INCOMPLETE mirrors this shape at a different target version (v1.x vs. v0.1 Beta).
- **Seat-home authority (§15 Archivist v1 SPEC):** `pipeline/blueprint/v0.1/section_15_archivist.md` (rows 191/192) — proposes-only / three-layer defense / F-ARCHIVIST-\* family / J-06 slot-transition.
- **Curation-slot reservation:** `pipeline/architecture/v0.1/architecture_v7_0_4_amendment.md` §9 + §9.1 (J-06 slot transition: operator → archivist).
- **Synthesis design memo:** `pipeline/research/reflection/synthesis_design_memo_2026-05-10.md` (five-lane fold).
- **Pre-Thesis scoping draft:** `pipeline/research/reflection/scoping_draft_reflection_as_archivist_submode.md`.
- **Five research lanes:** `pipeline/research/reflection/lane_{1,2,3,4,5}*.md`.
- **Dispatch packet (this round):** `pipeline/handoffs/ws_reflection_v0_1_hook_handoff_2026-05-10.md`.
- **Operator refinement directive (this round):** logged at `pipeline/validation/reflection_v0_1_hook_thesis_2026-05-10/operator_refinement_2026-05-10.md`.
- **Audit trail (this round):** `pipeline/validation/reflection_v0_1_hook_thesis_2026-05-10/`.

## §13. Lock-history note + sequencing

Forward-pending:

- **v7.0.9 (DRAFT 2026-05-10, this file):** Reflection v0.1 Beta hook — 8 BINDING + 8 HORIZON + 1 PROBE-DEPENDENT F-REFLECTION-\* primitives + 5 F-ARCHIVIST-\* sub-tag extensions + Archivist sub-mode seat-home binding + grounding-signal-class registry + F-REFLECTION-COVERAGE-INCOMPLETE META-gate (BINDING) + operator-drafted inoculation frame body + internal-vs-external naming discipline. Awaiting L-005 strict two-cycle Thesis with FULL live cross-family rigor. Companion-LOCK target: §4 v2.x.2 paired sub-amendment + §0.5 v18 §15.x paired sub-amendment (compound paired-commit triple per §6.17 Option-B).

- **Compound-LOCK row anticipation:** triple lands at next sequential lock_history rows (anticipated 202 / 203 / 204 after row 201 §14 Report Generator LOCK 2026-05-10). LOCKs atomically — all three or none, per paired-commit discipline.

Forward-binding to future amendments:

- **v0.2 SPEC §15 v2.x Reflection amendment** — per §9.2. Promotes 8 HORIZON to signature-present.
- **v1.x runtime §4 v2.x.4 + §15 v3.x amendment** — per §9.3; activates F-REFLECTION-COVERAGE-INCOMPLETE clearance (BINDING bodies realized) + may promote PROBE-DEPENDENT to live (after probe registry realization) + may revisit `loop_divergence_probes` deferral.
- **Heavy-Reflection swap decision** — deferred entirely per operator refinement Q3; v1.x amendment-realization carries the FORWARD MARKER only.

## §14. Author response log — Thesis closure (Cycle 2 verification 2026-05-10)

L-005 strict two-cycle Thesis CLOSED 2026-05-10 with FULL LIVE CROSS-FAMILY RIGOR. Audit trail at `pipeline/validation/reflection_v0_1_hook_thesis_2026-05-10/`.

**Cycle 1 (2026-05-10T18:03Z..18:09Z):**
- Editor (Llama-3.3-70B / Groq, Meta family): READY_TO_LOCK with 4 findings (E-01 LOW, E-02 MEDIUM, E-03 LOW, E-04 MEDIUM) — all FOLDED.
- Judge (Gemini-2.5-Pro / Google): READY_TO_LOCK at 99/100 with 1 finding (J-01 LOW on terminology ambiguity) — FOLDED.
- Red Team (GPT-OSS-120B / Groq, OpenAI-OSS family): REQUIRES_FIXES with 16 probes (4 BLOCKING + 6 HIGH + 4 MED + 2 LOW). Per row-170 transparent disposition pattern: 11 FOLDED + 5 BOUNDED-by-v7-LOCKED-A1+A4 + 1 REJECTED-with-rationale.

**Cycle 2 (2026-05-10T18:16Z..18:17Z):**
- Editor: READY_TO_LOCK — all Cycle-1 findings CLOSED; no new findings.
- Judge: READY_TO_LOCK at 100/100 (+1 from Cycle 1) — J-01 CLOSED; Lane 3 dimension restored to 10/10.
- Red Team: READY_TO_LOCK — all 17 FOLDED items dispositioned CLOSED; all 5 BOUNDED MAINTAINED; 1 REJECTED MAINTAINED; no new Cycle-2 probes surfaced.

UNANIMOUS READY_TO_LOCK at Cycle 2 close. No third round invoked. Synthesis at `pipeline/validation/reflection_v0_1_hook_thesis_2026-05-10/audit_v2_synthesis.md`.

# End of amendment

---

## [v7.0.10 footer addendum 2026-05-11]

Architecture amendment v7.0.10 LOCKED 2026-05-11 (lock_history row 215) deprecates the "Sanitized" / opaque-slot-token posture as a first-class customer-facing routing posture. The sentence in §6 of v7.0.9 referencing F-CLASS-SLOT-ID-NON-OPAQUE for Reflection's cloud-routed prompt RETRACTS. Reflection's always-local-on-Confidential posture is PRESERVED under v7.0.10 vocabulary: Reflection's reflection_agent always operates under Local-Only / Sovereign or Split-Context Hybrid posture; reflection inputs always carry Confidential content; reflection_agent's prompt never traverses cloud routing under any v7.0.10 posture. The F-REFLECTION-* family + F-ARCHIVIST-* sub-tag extensions + grounding-signal-class registry + inoculation frame from v7.0.9 are UNCHANGED at v7.0.10 — v7.0.10 is purely a routing-vocabulary simplification.

See: pipeline/architecture/v0.1/architecture_v7_0_10_amendment.md §8

[end addendum]

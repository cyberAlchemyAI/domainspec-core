---
title: Blueprint §10 Red Team — adversarial-review seat (v1 SCOPING DRAFT)
filed: 2026-05-01
operator: Josh
status: **LOCKED 2026-05-02** — v1.1 LOCKED under L-005 strict two-cycle. Round 1 (DRIVER) 2026-05-02: Judge READY_TO_LOCK 100/100 zero residuals; Editor REQUIRES_MINOR_FIXES (5 handwave items, all DEFENDED at trace-substance — already addressed in §10 prose); Red Team REQUIRES_MAJOR_MITIGATIONS 3 HIGH + 4 MEDIUM + 1 LOW → triage: 4 ACCEPTED narrow-fix + 1 OQ-deferred (F6) + 3 DESIGN-DEFENDED (F2, F5, F7). v1 → v1.1 narrow-fix carve-out applied 2026-05-02 (sha `2b2c0c61e1325f0a` → `08666230283e217a`). Round 2 (VERIFICATION) 2026-05-02: Editor READY (verifies all 4 closures) + Judge READY_TO_LOCK 100/100 re-affirmed (zero residuals; ready_to_lock=true) + Red Team REQUIRES_MAJOR_MITIGATIONS literal → READY trace-substance (4/4 narrow-fix closures CONFIRMED in Red Team's own premises; 0 NEW in-scope findings; 3 re-statements of v0.2-deferred items already in OQ-10.9 + OQ-10.10 + OQ-10.11). Tier reconciliation per §7 v1.1.1 precedent. Closeout: `pipeline/validation/section_10_thesis_round_2/CLOSEOUT.md`. Compound v1 LOCK with §5 v7 amendment + §0.5 §10 amendment per §6.17 Option-B paired-commit pattern.
parent_locks:
  - pipeline/architecture/v0.1/tilth_architecture_locked.md                      # v7 LOCKED 2026-04-19 — A3 SFR three-block verdict format mandatory for Red Team; §E cross-family rigor; §F.1 F-VERDICT-CERT-MALFORMED POST-gate; §M13 review-seat outage escape valve
  - pipeline/blueprint/v0.1/section_02_vault_topology.md                         # v7.1 LOCKED 2026-04-19 — Red Team writes verdicts via Vault-owned primitives; never raw open()
  - pipeline/blueprint/v0.1/section_04_logician.md                               # v2.1 LOCKED 2026-04-19 — Red Team's PRE/POST gates are enforced by Logician
  - pipeline/blueprint/v0.1/section_04_v2_4_v2_5_amendment.md                    # v2.5 LOCKED 2026-04-19 — F-ROUTER-FAMILY-COLLISION is the architecture-level enforcer; §10's F-RT-FAMILY-OVERLAP is its Red-Team-scoped subclass
  - pipeline/blueprint/v0.1/section_05_pipeline.md                               # v6 LOCKED 2026-04-19 — §5 v7 amendment is the prerequisite-interlock that wires Red Team into the inner loop alongside Judge (§10.10)
  - pipeline/blueprint/v0.1/section_06_operating_envelope.md                     # v1-r1 LOCKED 2026-04-21 — SFR parser implementation; prompt-template compilation pipeline; track-registry row for Red Team probe template
  - pipeline/blueprint/v0.1/section_07_scribe.md                                 # v1.1.1 LOCKED 2026-04-21 — Red Team consumes SectionDraft + claim_evidence_map emitted by Scribe (§7.5)
  - pipeline/blueprint/v0.1/section_00_5_interface_index_locked.md               # §0.5 v5 LOCKED 2026-04-19 — Red Team primitives row-append at v6.x amendment paired with §10 v1 LOCK
prerequisite_interlock: pipeline/blueprint/v0.1/section_05_pipeline.md (§5 v7 amendment — wires Red Team invocation into §4.6 revision loop alongside Judge; defines RT_DISAGREEMENT_THRESHOLD constant; routes F-COUNCIL-SPLIT through §4.7 POST-gate). §10 v1 LOCK is gated on §5 v7 amendment LOCK in the same way §7 v1 LOCK was gated on §6 v1 LOCK; the SCOPING DRAFT pins shapes that §5 v7 must consume.
companion_module: pipeline/orchestrator/seats/red_team.py (operational today as a standalone CLI; this blueprint lifts its content into seat-lifecycle discipline and pins the contract that the future `pipeline/seats/red_team/` production seat must satisfy. The on-disk CLI is NOT modified by this blueprint — the seat-lifecycle port is a downstream R1 round).
downstream_siblings_out_of_scope: §8 Editor (LOCKED-as-a-whole 2026-05-01), §9 Judge (LOCKED-as-a-whole 2026-05-01). §10 pins the consumer-side contracts (read SectionDraft + JudgeVerdict) but does NOT respec §7/§8/§9 internals. Any §7/§8/§9 content surfaced during Thesis-round audit must be kicked back.
---

# §10.1 Purpose and scope

Red Team is the **adversarial-review seat** of the Tilth council. Its job is to attack the draft — find the weakest claims, the unsupported assertions, the dialect mismatches, the boundary drift — and produce two artifacts: (a) an **independent score** commensurable with Judge's, and (b) a **prosecutorial memo** richer than a number. Red Team does NOT draft (that is Scribe, §7), does NOT clarity-edit (that is Editor, §8), does NOT score on the funder's terms (that is Judge, §9), and does NOT enforce determinism (that is Logician, §4). Red Team prosecutes; the operator decides.

**v0.1 scope.** One seat type: adversarial reviewer firing on every Scribe finalization (revision-loop trigger per §5 v7 amendment). Two output shapes: a `RedTeamVerdict` (score + prosecutorial memo, §10.5) and an SFR three-block certificate (§10.4) serializing the verdict for `F-VERDICT-CERT-MALFORMED` POST-gate consumption. One register at a time (Law 4 — Red Team's own prose obeys the active dialect; Red Team does NOT code-switch the draft, only critiques it). Score parity with Judge (§10.8) — same rubric, same `max_score`, but **scored fresh** with explicit anti-anchoring discipline.

**Out of scope for v0.1 (explicit non-goals).** Red Team does NOT produce edited drafts. Red Team does NOT route revisions back to Scribe (revision-loop dispatch is §5 v7's job; Red Team's findings ride alongside Editor's into §8.12 handoff). Red Team does NOT hold veto power — it produces a verdict, the operator weighs it. Red Team does NOT adjudicate disagreement with Judge — when Red Team's score and Judge's score differ by ≥ `RT_DISAGREEMENT_THRESHOLD` (§10.6), the **operator** breaks the tie via `F-COUNCIL-SPLIT` POST-gate routing.

**Substance comes from the draft + the rubric (Laws 1 + 5).** Red Team's evidence quotes MUST be byte-identical substrings of the draft (Law 5 mirror of Judge's verbatim invariant); Red Team's per-criterion scoring MUST cite the rubric tier-language verbatim (Law 1). Red Team never invents weaknesses by referencing facts not in the draft, never imputes intent the applicant has not stated, never attacks identity claims that trace cleanly through Scribe's `KgiePreflightResult.identity_claims`.

**Why a second voice (architectural rationale).** Architecture §F.1 + §A3 mandate cross-family ensemble review specifically because single-family models share blind spots — a Judge that only "sees" through one provider's lens can miss a class of weakness uniformly. Red Team is the second voice. Per §A3: "Semantic correctness is the REVIEWER's job — the cross-family rigor at Section E is the architectural mechanism that catches a reviewer who cites fabricated paths or builds on false premises; a second reviewer's independent verdict is what flags the semantic defect." Red Team is that second reviewer.

# §10.2 Five Operating Laws — enforcement mapping

Each of the Five Laws is enforced by a combination of PRE-gates (Logician, before Red Team sees the prompt), in-seat discipline (Red Team's own output contract), and POST-gates (Logician, after Red Team returns a verdict). Failure codes enumerated in §10.9.

**Law 1 — RFA is the source of truth.**
- PRE-gate: `F-RT-RFA-MISSING` — Logician refuses the run if the RFA file or its session-pinned hash is absent (subclass of §7.13 `F-SCRIBE-RFA-MISSING` for Red Team's input contract).
- In-seat: Red Team's verdict cites rubric-tier language verbatim per criterion (`tier_matched` field is a substring of `RubricCriterion.tier_descriptions[<tier>]`).
- POST-gate: `F-RT-EVIDENCE-NOT-IN-DRAFT` — Logician walks every `attack_memo.top_weaknesses[i].claim` and every `criteria[j].evidence` against the draft body; non-substring → hard-block. This is the Law 5 mirror gate; phrased here as Law 1 because the cited evidence must trace to the **draft text** which itself traces to RFA + PROJECT_CONTEXT + USER_DATA.

**Law 2 — No boundary drift.**
- PRE-gate: `F-RT-SCOPE-MISSING` — compiled prompt missing scope statement at start OR end (subclass of `F-CONTEXT-PLACEMENT`; §6 Operating Envelope owns the lint).
- In-seat: Red Team's `attack_memo.boundary_drift` field SURFACES drift findings as the explicit critique vector — Red Team is in fact obligated to look for boundary drift. Red Team's own prose MUST stay inside the rubric's scope; Red Team does NOT propose changes to the RFA's scope or recommend new program priorities.
- POST-gate: `F-RT-VERDICT-CERT-MALFORMED` (§10.4) — SFR three-block parser rejects a verdict whose conclusion appeals to premises not declared in block 1 (out-of-scope reasoning). This is the architecture-level `F-VERDICT-CERT-MALFORMED` from §F.1, scoped to Red Team verdicts.

**Law 3 — Org isolation.**
- PRE-gate: `F-RT-ORG-CROSS-REF` — Logician refuses the run if the prompt is compiled from more than one `orgs/<slug>/` PROJECT_CONTEXT (mirrors §7.2 Law 3 for Scribe). Red Team's prompt carries the SAME PROJECT_CONTEXT slug as Scribe's draft; cross-org draft+context pairing is rejected.
- In-seat: Red Team's prompt template NEVER ships prior-client weaknesses or comparative critiques against other applicants. Adversarial language stays scoped to THIS draft against THIS RFA.
- POST-gate: `F-LOGICIAN-S10A-NO-ORG-ATTRIBUTES` (forwarded from §4) — Red Team verdicts are scanned for cross-org slug references; draft blocked on leakage.

**Law 4 — Apolitical sector language + admin-risk term scanning.**
- PRE-gate: `F-RT-DIALECT-UNCLASSIFIED` — Red Team's prompt requires the funder's dialect classification (mirrors §7.2 Law 4). Red Team critiques the draft's dialect-fit; absent a classification, no benchmark exists.
- In-seat: Red Team's `attack_memo.dialect_mismatches` field surfaces register-drift findings. Red Team's OWN prose obeys the active dialect (a Red Team verdict on a Soul-fire-dialect draft uses Conservative-or-neutral analytical voice, not Soul-fire vocabulary — Red Team is the analyst, not the author).
- POST-gate: `F-RT-ADMIN-RISK-UNFLAGGED` — Logician scans Red Team's verdict body for admin-risk-register terms at severity ≥ Medium emitted without a `[ADMIN-RISK:flag]` comment. Red Team is not exempt from Law 4; if Red Team needs to QUOTE an admin-risk term to critique it, Red Team flags the quote.

**Law 5 — Applicant brings the substance.**
- PRE-gate: `F-RT-INPUT-MISSING` — `SectionDraft` set, `JudgeVerdict`, and rubric all required. Red Team CANNOT run on a partial draft (no in-progress critique).
- In-seat: Red Team's `attack_memo.unsupported_assertions` field is the load-bearing Law 5 enforcement site — every claim Red Team flags as unsupported is checked against `SectionDraft.claim_evidence_map`. If a claim Red Team flagged DOES have evidence, that's a Red Team error (false-positive critique); if a claim has no evidence, that's a Scribe error (Law 5 violation that Scribe POST-gate `F-SCRIBE-UNSOURCED-CLAIM` should already have caught — Red Team is defense-in-depth).
- POST-gate: `F-RT-EVIDENCE-NOT-IN-DRAFT` (Law 5 mirror) — every quoted evidence string MUST be a byte-identical substring of `SectionDraft.body_text` for the cited section. Red Team cannot fabricate quotes.

# §10.3 Phase 0 — Input contract

Before any adversarial review, Red Team consumes a fully-finalized input bundle. Red Team is the LAST review seat in the inner loop (§5 v7 amendment, after Editor + Judge); it sees what the operator will see at sign-off, plus Judge's score for context.

**Input bundle (`RedTeamInput`, frozen, kw_only):**
- `run_id: str` — Scribe's run-scoped UUID; pins the input bundle to the same run.
- `section_drafts: tuple[SectionDraft, ...]` — finalized drafts from Scribe (§7.5); ordered by `section_order` ascending.
- `claim_evidence_map: tuple[ClaimEvidence, ...]` — flattened claim-evidence map across all sections (§7.2 Law 1).
- `rfa_extracted_record: RfaExtractedRecord` — Phase 0 RFA extraction (§7.3); Red Team reads `evaluation_criteria` for rubric reconciliation, `eligible_project_activities` for boundary-drift critique, `key_terms` for dialect-fit critique.
- `rubric: Rubric` — same rubric Judge used; pinned by content-hash to the session manifest.
- `judge_verdict: JudgeVerdict | None` — Judge's score + per-criterion breakdown (§9 LOCKED 2026-05-01). PROVIDED AS CONTEXT, NOT AUTHORITY (§10.8 anti-anchoring discipline). `None` is permissible only when Judge has hard-failed AND the operator has issued an M13 review-seat bypass (§10.10) — production runs never see `judge_verdict=None`.
- `funder_dialect: Literal["conservative", "centrist", "progressive", "soul_fire"]` — dialect classification pinned at Phase 0; informs `attack_memo.dialect_mismatches` analysis.
- `admin_risk_register_snapshot: AdminRiskRegisterSnapshot` — the same 18-entry (v0.1) register Scribe consumed; Red Team checks the draft for unflagged terms (defense-in-depth against Scribe's own POST-gate).
- `prepared_at_utc: datetime`.

**Bundle invariants.**
- `claim_evidence_map` MUST be the union of `section_drafts[*].claim_evidence_map` — extra entries OR missing entries trip `F-RT-INPUT-INCONSISTENT` at PRE-gate.
- `rubric.content_hash` MUST equal the rubric hash pinned in the session manifest at Phase 0; mismatch trips `F-RT-RUBRIC-DRIFT` (mirror of `F-SCRIBE-RFA-DRIFT`).
- `judge_verdict.run_id == run_id` — input bundle is run-scoped; cross-run mixing is rejected.
- `judge_verdict.rubric_hash == rubric.content_hash` — Judge and Red Team scored against the SAME rubric bytes.

# §10.4 SFR three-block verdict format

Per architecture §F.1 (A3 amendment, LOCKED 2026-04-19), every Red Team verdict is serialized as a **Semi-Formal Reasoning** three-block certificate:

1. **Premises** — explicit facts + citations. Each premise carries a citation pointer to a source artifact: `RFA:<path>:<line-range>` (RFA scope/eligibility/criteria), `RUBRIC:<id>:<tier>` (rubric tier-language), `DRAFT:<section_name>:<paragraph_index>:<sha3_512_substring_prefix>` (draft body, where the prefix is a 32-hex-char SHA-3-512 prefix of the cited substring per the same width-discipline as §7.4a USER_DATA anchors), `JUDGE:<criterion_id>:<score>` (Judge's per-criterion datum, cited only when Red Team is contrasting positions). Premises with no citation are not premises; they are unsupported claims that must be removed or grounded.
2. **Execution trace** — ordered steps citing premises by ID. Each step references one or more premises (`P1`, `P2`, ...) and applies a named inference rule (e.g., "by RFA-source-of-truth from Law 1," "by rubric-tier-monotonicity," "by claim-without-evidence anti-pattern"). Steps that do not cite premises are floating reasoning and must be re-grounded.
3. **Conclusion** — derives ONLY from declared premises + trace. The conclusion MUST include: (a) `recommendation ∈ {"competitive", "marginal", "not_ready"}`, (b) `total_score: int` with `0 ≤ total_score ≤ rubric.max_score`, (c) the residual list (top weaknesses) — every residual MUST trace back to a specific step or premise. A conclusion that depends on an undeclared premise OR an absent trace step trips `F-RT-VERDICT-CERT-MALFORMED` at POST-gate.

**Logician POST-gate `F-RT-VERDICT-CERT-MALFORMED`.** Subclass of architecture-level `F-VERDICT-CERT-MALFORMED` (§F.1). The Logician's SFR parser (implemented by §6 Operating Envelope per A3) parses Red Team's verdict markdown into the three-block structure; parse failure → hard-block with a structured error citing the specific malformation (missing block, premise without citation, step without premise reference, conclusion grounded in undeclared premise). **Structural gate, not semantic** — F-RT-VERDICT-CERT-MALFORMED does not evaluate whether citations point at real artifacts or whether premises are factually correct. Semantic correctness is defended by cross-family rigor (§10.7).

**Red Team's structural-vs-semantic boundary.** Red Team's `attack_memo` IS the semantic critique; the SFR certificate is the verdict's machine-readable structure. The two are emitted together — `RedTeamVerdict` (§10.5) carries both fields, and the SFR-serialization step is a deterministic mapping from `RedTeamVerdict` to markdown.

# §10.5 Attack memo schema

`RedTeamVerdict` is the shape Red Team emits; the SFR certificate (§10.4) is the markdown serialization. Both are LOCKed at this blueprint round.

**`RedTeamVerdict`, frozen, kw_only:**
- `run_id: str` — input bundle's run_id (must match).
- `rubric_id: str` / `rubric_hash: str` — rubric identity + content-hash (must match input bundle).
- `total_score: int` — Red Team's authoritative total. **Computed-from-criteria invariant** (§10.8): `total_score == sum(c.score for c in criteria)`. The model's reported total is captured in `total_score_correction` if it disagrees; the computed sum is authoritative.
- `max_score: int` — `rubric.max_score`; pinned for safety.
- `recommendation: Literal["competitive", "marginal", "not_ready"]`.
- `criteria: tuple[RedTeamCriterionScore, ...]` — one entry per rubric criterion (§10.8).
- `attack_memo: AttackMemo` — the prosecutorial memo (below).
- `total_score_correction: TotalScoreCorrection | None` — populated only when the model's reported total ≠ computed total; carries `model_reported`, `computed_from_criteria`, `delta` for audit. Authoritative total in `total_score` is always the computed value.
- `verdict_at_utc: datetime`.
- `red_team_dialect: Literal["conservative", "centrist", "progressive", "soul_fire"]` — Red Team's analytical dialect snapshot (typically conservative/centrist regardless of `funder_dialect`; pinned to detect register-drift in Red Team's own prose).

**`RedTeamCriterionScore`, frozen, kw_only:**
- `criterion_id: str` — matches a `RubricCriterion.id`.
- `criterion_name: str` — denormalized for SFR readability.
- `max_points: int` — copied from `RubricCriterion.max_points`; monotone-checked at POST-gate.
- `score: int` — Red Team's score. `0 ≤ score ≤ max_points` (`F-RT-SCORE-OUT-OF-RANGE` if violated).
- `tier_matched: str` — verbatim substring of one of `RubricCriterion(id=<this_criterion_id>).tier_descriptions[<tier>]` for the SPECIFIC criterion (NOT any criterion in the rubric); `F-RT-TIER-NOT-VERBATIM` if mismatched. Per-criterion scoping closes RT-r1-F4 (substring-could-match-wrong-criterion attack).
- `evidence: str` — verbatim substring of `SectionDraft.body_text` for the section the criterion targets; `F-RT-EVIDENCE-NOT-IN-DRAFT` if mismatched. Length-bounded to ≤ 320 characters (long quotes are summarized, not pasted; full draft is on-disk).
- `missing: tuple[str, ...]` — what the draft would need to score higher; each entry is a short noun phrase, not a paragraph.
- `notes: str` — Red Team's prosecutorial note for this criterion (≤ 480 characters).

**`AttackMemo`, frozen, kw_only:**
- `top_weaknesses: tuple[Weakness, ...]` — at most 5, at least 1 (`F-RT-WEAKNESSES-EMPTY` if zero — Red Team must produce at least one weakness; a draft with literally zero weaknesses is a Red Team error, not a draft achievement).
- `unsupported_assertions: tuple[str, ...]` — claims Red Team believes lack evidence; each entry is a verbatim draft substring per Law 5 (§10.2).
- `dialect_mismatches: tuple[str, ...]` — places the draft speaks the wrong dialect for the funder; verbatim draft substrings.
- `boundary_drift: tuple[str, ...]` — places the draft exceeds RFA scope; verbatim draft substrings.
- `overall_verdict: str` — single-paragraph summary (≤ 480 characters); the prosecutor's closing argument.

**`Weakness`, frozen, kw_only:**
- `severity: Literal["high", "medium", "low"]`.
- `claim: str` — the exact claim or section being attacked; verbatim draft substring (≤ 320 characters).
- `why_it_fails: str` — why this fails under reviewer scrutiny (one sentence, ≤ 25 words per the orchestrator-CLI tersity discipline).
- `what_a_reviewer_would_say: str` — what a real reviewer would write in the margin.
- `fix_hint: str` — short direction; NOT a rewrite (Red Team does not edit).

**Field length discipline.** Per the orchestrator-CLI source (`pipeline/orchestrator/seats/red_team.py`, line 157): "Each string field: one sentence, maximum 25 words." Blueprint pins `top_weaknesses ≤ 5`, `evidence ≤ 320 chars`, `notes ≤ 480 chars`, `overall_verdict ≤ 480 chars`. These bounds keep Red Team's response within free-tier TPM ceilings (e.g., Groq GPT-OSS-120B 30k TPM) while leaving room for the SFR-certificate serialization overhead.

# §10.6 Council-split detection — F-COUNCIL-SPLIT

**Trigger.** Per the §M13-adjacent operator-tie-breaker discipline: when `|JudgeVerdict.total_score - RedTeamVerdict.total_score| ≥ RT_DISAGREEMENT_THRESHOLD`, the council is **split**. The operator decides — Red Team does not adjudicate, Judge does not adjudicate, no automatic averaging is permitted.

**Constant.** `RT_DISAGREEMENT_THRESHOLD: Final[int] = 10` — pinned in §5 v7 amendment §8 constants table. Threshold rationale: a 10-point gap on a 100-point rubric represents a category-level disagreement (one tier on most rubric dimensions); lower gaps are noise that fits within independent-scoring variance, higher gaps indicate the two seats are reading the draft fundamentally differently. The threshold is operator-configurable per-org via `PROJECT_CONTEXT.rt_disagreement_threshold_override: int | None`; the override is ledger-stamped at Phase 0 (admin-risk register Medium-severity entry).

**POST-gate `F-COUNCIL-SPLIT`.** Logician POST-gate fires when the threshold is exceeded. The gate is **non-blocking on the run** but **blocking on auto-finalization** — the run transitions to phase `signoff_pending_council_split` (a new sub-state of `signoff_pending` per §5 v7 amendment §3.2.1), the operator-signoff prompt carries:
- Both scores (Judge's and Red Team's).
- The per-criterion delta map (which criteria diverged most).
- The full `attack_memo` (Red Team's prosecutorial argument).
- Judge's per-criterion notes (Judge's defense).
- A single binary operator decision: PROCEED-WITH-JUDGE / PROCEED-WITH-RED-TEAM / REVISE / DROP.

**Operator decision invariant.** The operator's decision is captured in `RunState.council_split_decision: CouncilSplitDecision | None` and ledger-stamped HIGH-severity to the admin-risk register. A draft cannot ship with `phase == signoff_pending_council_split` — phase advancement to `report_signed` is gated on `council_split_decision is not None`.

**Anti-averaging invariant.** The pipeline NEVER computes any arithmetic combination of judge_score and red_team_score (mean, median, weighted average, geometric mean, statistics.mean, etc.) and presents it as the run's score. Averaging two seats' scores defeats the purpose of having a second voice (architecture §F.1: "a second reviewer's independent verdict is what flags the semantic defect"). The operator picks one seat's verdict, or revises, or drops. This invariant is enforced as an AST-grep test in §10.11 (`test_no_score_averaging_in_pipeline`) banning **the closed list** of these patterns anywhere in `pipeline/`: `(judge_score + red_team_score) / N`, `(judge_total_score + red_team_total_score) / N`, `mean(judge_score, red_team_score)`, `statistics.mean([..., judge, ..., red_team, ...])`, `(judge*W1) + (red_team*W2)` with weighted-sum patterns. v0.2 roadmap commitment (closes RT-r1-F1): expand AST-grep coverage to include weighted-arithmetic and statistics-module callsites; pinned as **OQ-10.11**.

**Anti-anchoring smoke check.** When `|JudgeVerdict.total_score - RedTeamVerdict.total_score| < 2` AND the draft is non-trivial (rubric ≥ 5 criteria, draft ≥ 1000 words), Logician POST-gate emits `F-RT-JUDGE-ANCHOR-SUSPECTED` as a **non-blocking ADVISORY** (admin-risk register LOW-severity entry, surfaced at sign-off). Two independent cross-family seats agreeing within 2 points on a complex rubric is statistically suspicious; the advisory does not block the run but does flag the verdict for operator review. Threshold of 2 is a heuristic — operator may suppress the advisory per-org.

# §10.7 Cross-family discipline (3-way distinct)

**Invariant (architecture §E + §10).** Red Team's resolved provider family MUST differ from BOTH Scribe's resolved family AND Judge's resolved family. This is a strict 3-way distinct constraint, stricter than §E's pairwise rule (Scribe ≠ Judge).

**Why 3-way distinct.** Per §F.1: "the cross-family rigor at Section E is the architectural mechanism that catches a reviewer who cites fabricated paths or builds on false premises; a second reviewer's independent verdict is what flags the semantic defect." If Red Team shares family with Judge, the second voice collapses into Judge's family blind spot — defeating the architectural purpose. If Red Team shares family with Scribe, Red Team risks reading Scribe's own register sympathetically (a reviewer in the same family as the author is biased toward charity).

**Enforcement: `F-RT-FAMILY-OVERLAP` PRE-gate.** Subclass of `F-ROUTER-FAMILY-COLLISION` (§4.16, v2.5). Fires at Red Team invocation time when:
- `resolved_red_team_family == resolved_scribe_family` (sub-tag `.with_scribe`), OR
- `resolved_red_team_family == resolved_judge_family` (sub-tag `.with_judge`).

The check happens AFTER Scribe and Judge have resolved their families (so cascades-have-fired), via `RunState.run_iteration_families_so_far` (§5 v6 §3.2.1 — a dict `{seat_kind: (family, model_id)}`). On collision: hard-abort the Red Team invocation with `F-RT-FAMILY-OVERLAP`; admin-risk HIGH-severity ledger stamp.

**Cascade interaction.** Red Team's `ProviderCascade` (per `router.yaml`) is reordered at runtime to skip any family already landed by Scribe or Judge. If after reordering the cascade is empty, the seat hard-aborts (no `F-RT-FAMILY-OVERLAP` — instead `F-RT-NO-COMPLIANT-FAMILY`, a Red Team-specific subclass of M13 review-seat outage). M13 escape valve applies: operator may issue a signed review-seat bypass authorization (§M13 architecture, mirrored for Red Team).

**Current router.yaml binding (2026-04-19, source of truth).** Scribe = Anthropic; Judge = Google; Red Team = OpenAI-OSS (Groq `gpt-oss-120b` primary) / Anthropic (fallback). The fallback Anthropic creates a 3-way-collision risk if Scribe is also resolved to Anthropic — `F-RT-FAMILY-OVERLAP.with_scribe` PRE-gate catches this at Red Team invocation time. Recommendation for §5 v7 amendment: extend Red Team's cascade to include OpenAI direct (`gpt-5.1` per the 2026-04-19 router.yaml addition) as a tertiary cross-family-safe option to reduce the M13-bypass-required failure mode.

# §10.8 Score parity contract

Red Team scores against the **same rubric** Judge used. Score parity means: same `max_score`, same criterion IDs, same tier-language. But **scored fresh** — anti-anchoring discipline (§10.6).

**Per-criterion identity invariant.** `RedTeamVerdict.criteria` and `JudgeVerdict.criteria` are tuples over the SAME rubric criterion IDs in the SAME order. `F-RT-CRITERION-MISSING` fires at POST-gate if Red Team's `criteria` is missing a rubric criterion (or has a criterion not in the rubric).

**Score range invariants.** Per criterion: `0 ≤ score ≤ max_points` (`F-RT-SCORE-OUT-OF-RANGE`). Total: `0 ≤ total_score ≤ max_score` (`F-RT-SCORE-OUT-OF-RANGE.total`). Computed-from-criteria: `total_score == sum(c.score for c in criteria)` (mismatch is auto-corrected to the sum and logged in `total_score_correction`; a non-None `total_score_correction` is itself a Red Team smoke signal — frequent corrections indicate the model is computing totals incorrectly; track via admin-risk LOW-severity over time).

**Tier-verbatim invariant.** `RedTeamCriterionScore.tier_matched` MUST be a verbatim substring of one of the rubric's tier-description strings for that criterion (e.g., for VAPG criterion 5 "Need", the tier_matched MUST appear in `RubricCriterion(id="need").tier_descriptions["high"]` or `["medium"]` or `["low"]`). `F-RT-TIER-NOT-VERBATIM` if mismatched. This pins Red Team to the rubric's vocabulary and prevents the model from inventing its own tier-language.

**Anti-anchoring discipline.** Red Team's prompt template (lifted from `pipeline/orchestrator/seats/red_team.py` SYSTEM_PROMPT, lifted-into-blueprint per §10.13) carries explicit anti-anchoring instructions: "Judge's scoring is context, not authority. Form your own view ... Never anchor to Judge's score. You score fresh ... disagreement with Judge is a feature, not a bug." The instruction is load-bearing (placed at start AND end of the prompt per §6 context-placement lint, which also catches `F-RT-CONTEXT-PLACEMENT` on absence).

**Middle-block contradiction surface (v1.1, closes RT-r1-F3).** §10's start/end placement check leaves the middle block uncovered — an attacker (or an LLM under cascade-fallback who reads the middle differently) could inject an instruction like "ignore the anti-anchoring instruction" between the head and tail anchors and evade detection. §10 acknowledges this surface and forwards mitigation to **`F-CONTEXT-MIDDLE-CONTRADICTION`** (§6 Operating Envelope-owned PRE-gate per §A4); §10's role is to forward this code as a Red Team blocker per §10.9 forwarded codes. v0.2 roadmap commitment: §10 may add a Red-Team-specific middle-block lint that scans for known anti-anti-anchoring phrasings ("ignore the previous instruction", "Judge's score IS authority", etc.) — pinned as **OQ-10.10** at this round.

**Judge-context exposure window.** Red Team's prompt sees Judge's `total_score`, `max_score`, `recommendation`, and `overall_notes` (truncated to 400 chars per orchestrator CLI). Red Team does NOT see Judge's per-criterion breakdown — that would maximize anchoring. The truncation prevents Judge's full critique from biasing Red Team's read.

**Smoke check `F-RT-JUDGE-ANCHOR-SUSPECTED`.** Per §10.6: `|judge - red_team| < 2` on a non-trivial draft is statistically suspicious; advisory-only.

# §10.9 Failure codes

Red Team-specific failure codes (emitted by Logician PRE or POST-gates enforcing §10 invariants):

**PRE-gates (before Red Team runs):**
- **`F-RT-INPUT-MISSING`** — `RedTeamInput` fields missing or empty (`section_drafts`, `claim_evidence_map`, `rubric`, `judge_verdict`, `funder_dialect` all required).
- **`F-RT-INPUT-INCONSISTENT`** — `claim_evidence_map ≠ union(section_drafts[*].claim_evidence_map)`; OR `judge_verdict.run_id ≠ run_id`; OR `judge_verdict.rubric_hash ≠ rubric.content_hash`.
- **`F-RT-RUBRIC-DRIFT`** — `rubric.content_hash ≠ session_manifest.rubric_hash`; rubric file changed mid-run.
- **`F-RT-RFA-MISSING`** — RFA file or session-manifest hash absent (mirrors §7.13).
- **`F-RT-SCOPE-MISSING`** — compiled prompt missing scope statement at start OR end (subclass of `F-CONTEXT-PLACEMENT`).
- **`F-RT-ORG-CROSS-REF`** — prompt compiled from more than one `orgs/<slug>/` PROJECT_CONTEXT.
- **`F-RT-DIALECT-UNCLASSIFIED`** — `funder_dialect` missing from session manifest.
- **`F-RT-FAMILY-OVERLAP`** — Red Team's resolved family matches Scribe's (`.with_scribe`) OR Judge's (`.with_judge`); §4.16 subclass.
- **`F-RT-NO-COMPLIANT-FAMILY`** — after cascade reorder excluding Scribe + Judge families, no provider remains; M13 escape valve required.
- **`F-RT-ADMIN-RISK-REGISTER-STALE`** — admin-risk register snapshot age exceeds §7.16 freshness bound (mirrors `F-SCRIBE-ADMIN-RISK-REGISTER-STALE`).
- **`F-RT-CONTEXT-PLACEMENT`** — Red Team-specific context-placement subclass of §6 lint; anti-anchoring instructions absent at start OR end of prompt.

**POST-gates (after Red Team emits a verdict):**
- **`F-RT-VERDICT-CERT-MALFORMED`** — SFR three-block parse failure (subclass of architecture §F.1 `F-VERDICT-CERT-MALFORMED`); sub-tags `.missing_block`, `.premise_without_citation`, `.step_without_premise_reference`, `.conclusion_grounded_in_undeclared_premise`.
- **`F-RT-EVIDENCE-NOT-IN-DRAFT`** — any `criteria[*].evidence` OR `attack_memo.top_weaknesses[*].claim` OR `attack_memo.unsupported_assertions[*]` OR `attack_memo.dialect_mismatches[*]` OR `attack_memo.boundary_drift[*]` is not a byte-identical substring of the cited section's `body_text`. Law 5 mirror.
- **`F-RT-SCORE-OUT-OF-RANGE`** — any `criteria[*].score > max_points` OR `< 0`; OR `total_score > max_score` OR `< 0`. Sub-tags `.criterion`, `.total`.
- **`F-RT-SCORE-SUM-MISMATCH`** — `total_score ≠ sum(c.score for c in criteria)` AND `total_score_correction is None` (correction must be explicit, not silent).
- **`F-RT-CRITERION-MISSING`** — `criteria` missing a rubric criterion OR carrying a criterion not in the rubric.
- **`F-RT-TIER-NOT-VERBATIM`** — `tier_matched` not a verbatim substring of any rubric tier-description for that criterion.
- **`F-RT-WEAKNESSES-EMPTY`** — `attack_memo.top_weaknesses` empty (Red Team must produce at least one).
- **`F-RT-WEAKNESS-FIELD-MISSING`** — `top_weaknesses[i]` missing `severity` OR `claim` OR `why_it_fails` OR `what_a_reviewer_would_say` OR `fix_hint`.
- **`F-RT-RECOMMENDATION-INVALID`** — `recommendation` not in `{"competitive", "marginal", "not_ready"}`.
- **`F-RT-ADMIN-RISK-UNFLAGGED`** — Medium+ severity admin-risk term in verdict prose without `[ADMIN-RISK:…]` comment. Enforcement reuses §7.11 / §4.10 admin-risk register POST-gate scanner (Logician-side; same regex + register-snapshot integrity model as Scribe's `F-SCRIBE-ADMIN-RISK-UNFLAGGED`); §10 does NOT re-implement the scanner. Closes RT-r1-F8.
- **`F-RT-DIALECT-DRIFT`** — Red Team's verdict prose drifts dialect (Soul-fire vocabulary in a Conservative analytical voice, etc.).
- **`F-COUNCIL-SPLIT`** — `|judge_score - red_team_score| ≥ RT_DISAGREEMENT_THRESHOLD`; non-blocking on run, blocking on auto-finalization (§10.6).
- **`F-RT-JUDGE-ANCHOR-SUSPECTED`** — non-blocking advisory; `|judge - red_team| < 2` on non-trivial draft.

**Forwarded (not Red Team-emitted but can block Red Team runs):**
- `F-CONTEXT-PLACEMENT` (architecture §D.8 / §6).
- `F-CONTEXT-MIDDLE-CONTRADICTION` (architecture §A4 / §6) — forwarded per v1.1 RT-r1-F3 closure; covers middle-block injection between head + tail anti-anchoring anchors.
- `F-ROUTER-FAMILY-COLLISION` (§4.16; canonical, of which `F-RT-FAMILY-OVERLAP` is a subclass).
- `F-VERDICT-CERT-MALFORMED` (architecture §F.1; canonical, of which `F-RT-VERDICT-CERT-MALFORMED` is a subclass).
- `F-LOGICIAN-S10A-NO-ORG-ATTRIBUTES` (§4 — cross-org leakage scan in verdict prose).
- `F-LOGICIAN-TOKEN-LEAK` (§4 §4.12 PRE-append, if Red Team output touches admin-risk ledger).

# §10.10 §5 R11 `run_pipeline` integration (prerequisite-interlock §5 v7 amendment)

§5 v6 LOCKED 2026-04-19 specifies the inner loop as Scribe → Editor → Judge → POST-gate → operator-signoff → tab-delivery. Red Team is NOT in v6's lifecycle. §10 v1 LOCK is gated on **§5 v7 amendment LOCK** that wires Red Team into the inner loop alongside Judge.

**§5 v7 amendment scope (proposed at this SCOPING DRAFT round; LOCKs in a future session before §10 v1 LOCK).**

1. **§4.5 Judge invocation** — unchanged from v6.
2. **§4.5a Red Team invocation (NEW v7).** Fires AFTER Judge returns; consumes `JudgeVerdict` as context input. Same subprocess + cross-family + minimal-env discipline as Judge (§4.5 v6). Tuple return signature: `(verdict_hash, landed_family, landed_model_id)`. Cross-family check via `F-RT-FAMILY-OVERLAP` PRE-gate against `run_state.run_iteration_families_so_far["scribe"]` AND `["judge"]`.
3. **§4.6 Revision-loop control (v6 → v7 amendment).** Add Red Team to the per-iteration invocation sequence: after Judge returns, Red Team fires; both verdicts are written to checkpoint BEFORE iteration advances. Bounded revision loop unchanged (max 3 iterations per architecture).
4. **§4.7 POST-gate invocation (v6 → v7 amendment).** Add `F-COUNCIL-SPLIT` to POST-gate evaluation (§10.6). When threshold exceeded, transition to new sub-phase `signoff_pending_council_split` instead of `signoff_pending`.
5. **§3.2.1 RunState (v6 → v7 amendment).** Add `red_team_verdict_ref: str | None` (vault path to current iteration's RedTeamVerdict; mirror of Judge's existing telemetry); add `council_split_decision: CouncilSplitDecision | None`; add `signoff_pending_council_split` to the phase Literal.
6. **§8 Constants (v6 → v7 amendment).** Add `RT_DISAGREEMENT_THRESHOLD: Final[int] = 10` with module-load integrity assert (mirroring V1 TAB_ORDERING discipline). Add `RT_ANCHOR_SUSPECTED_THRESHOLD: Final[int] = 2` for the §10.6 smoke check.
7. **§9 Tests (v6 → v7 amendment).** Add property tests for council-split detection, anti-averaging, 3-way family distinct, anti-anchoring smoke check.

**§5 v7 amendment authoring is OUT OF SCOPE for this SCOPING DRAFT round.** §10 v1 LOCK requires §5 v7 to be authored, Thesis-passed, and LOCKed. Per §7 v1.1.1 LOCK precedent (which gated on §6 v1-r1 LOCK), the discipline is "do not LOCK §10 ahead of §5 v7."

**Compound-transaction option.** §5 v7 amendment + §10 v1 may LOCK as a compound transaction with §0.5 v6.x amendment (mirror of §6 v1-r1 / §7 v1.1.1 / §0.5 v6 compound-LOCK pattern from 2026-04-21). Same Option-B compound-txn discipline as §6.17.

# §10.11 Test surface

**Unit tests on the verdict + criterion + memo + weakness shapes (frozen-dataclass invariants).**
- `test_red_team_verdict_is_frozen` — every field immutable; slots+frozen.
- `test_red_team_criterion_score_constructs_with_required_fields` — empty `tier_matched` raises invariant violation.
- `test_attack_memo_top_weaknesses_at_least_one_required` — empty tuple raises (mirrors POST-gate `F-RT-WEAKNESSES-EMPTY`).
- `test_weakness_severity_closed_set` — severity not in `{"high", "medium", "low"}` raises.
- `test_total_score_corrected_when_disagrees_with_sum` — model reports 85, criteria sum to 87; `total_score=87`, `total_score_correction.delta=2`.

**SFR three-block parser tests (consumed from §6 Operating Envelope's parser implementation).**
- `test_sfr_parser_accepts_canonical_red_team_verdict` — golden three-block markdown parses cleanly.
- `test_sfr_parser_rejects_missing_premises_block` — `F-RT-VERDICT-CERT-MALFORMED.missing_block`.
- `test_sfr_parser_rejects_premise_without_citation` — `F-RT-VERDICT-CERT-MALFORMED.premise_without_citation`.
- `test_sfr_parser_rejects_floating_step` — step references no premise → `F-RT-VERDICT-CERT-MALFORMED.step_without_premise_reference`.
- `test_sfr_parser_rejects_conclusion_undeclared_premise` — conclusion references P5 but only P1-P3 declared → `F-RT-VERDICT-CERT-MALFORMED.conclusion_grounded_in_undeclared_premise`.

**Property tests.**
- `test_prop_red_team_score_is_int_in_range` — over 1000 fuzzed-input runs, every emitted `criteria[*].score` is `0 ≤ s ≤ max_points`.
- `test_prop_evidence_is_byte_identical_substring_of_draft` — every `evidence` field is a substring of the cited section's `body_text` (string-search, not paraphrase-tolerant).
- `test_prop_council_split_threshold_monotone` — varying judge-vs-red-team scores; F-COUNCIL-SPLIT fires iff `|delta| ≥ 10`.
- `test_prop_3way_family_distinct_invariant` — over 1000 router cascade draws, never observe a 3-way collision (or `F-RT-FAMILY-OVERLAP` fires).
- `test_prop_total_score_equals_sum_of_criteria` — over 1000 runs, `total_score == sum(criteria.score)` after auto-correction.

**Adversarial tests.**
- `test_adv_red_team_scores_within_2_of_judge` — Red Team's score is within 2 of Judge's on a non-trivial draft → `F-RT-JUDGE-ANCHOR-SUSPECTED` advisory fires (non-blocking).
- `test_adv_red_team_quotes_evidence_not_in_draft` — Red Team paraphrases instead of quoting verbatim → `F-RT-EVIDENCE-NOT-IN-DRAFT` POST-gate hard-blocks.
- `test_adv_red_team_invents_criterion_not_in_rubric` — `criteria` carries a fabricated criterion ID → `F-RT-CRITERION-MISSING` (extra criterion sub-case).
- `test_adv_red_team_disagrees_strongly_with_judge` — Judge=85, Red Team=70; F-COUNCIL-SPLIT fires; phase transitions to `signoff_pending_council_split`; operator decision required to advance.
- `test_adv_no_score_averaging_in_pipeline` — AST-grep test scans `pipeline/` for `(judge_score + red_team_score) / N` patterns; none found (anti-averaging invariant §10.6).
- `test_adv_red_team_resolves_to_scribe_family` — router cascade lands Red Team on Anthropic when Scribe also resolved to Anthropic → `F-RT-FAMILY-OVERLAP.with_scribe` PRE-gate hard-aborts.
- `test_adv_red_team_resolves_to_judge_family` — same with Judge family → `F-RT-FAMILY-OVERLAP.with_judge`.
- `test_adv_red_team_omits_overall_verdict` — `attack_memo.overall_verdict == ""` → `F-RT-WEAKNESS-FIELD-MISSING` (overall_verdict sub-case).

**Integration tests (Red Team + Logician + §5 v7 inner loop).**
- `test_int_red_team_emits_verdict_atomically` — verdict written via §2 Vault dispatcher SIMPLE path; crash mid-write leaves no partial verdict.
- `test_int_red_team_runs_under_seat_runner` — Red Team invoked via §5 v7 seat-runner; telemetry matches §5 §5.6 per_invocation_telemetry_record.
- `test_int_red_team_3way_cross_family_enforced` — router.yaml binds Red Team and Judge to same family; pipeline start trips `F-RT-FAMILY-OVERLAP.with_judge`.
- `test_int_council_split_routes_to_operator` — Judge=90, Red Team=78; phase transitions to `signoff_pending_council_split`; operator-signoff prompt carries both verdicts; `council_split_decision` written before phase advances to `report_signed`.
- `test_int_m13_review_seat_bypass_for_red_team` — all Red Team families FAILED for ≥ 24h; operator issues signed bypass authorization; run proceeds with rigor-breach flag in rails report (§4.17).

**Golden corpus (`tests/corpus/red_team/v1/`).**
- `pass/vapg_strong_draft/` — Scribe golden VAPG draft + Judge=85 + expected Red Team verdict (75 ± 5; recommendation marginal-or-competitive; ≥ 3 weaknesses).
- `pass/vapg_weak_draft/` — Scribe golden VAPG draft with deliberate weaknesses + Judge=55 + expected Red Team verdict (40 ± 10; recommendation not_ready; ≥ 5 weaknesses).
- `fail/red_team_anchors_to_judge/` — synthetic verdict matching Judge within 1 point on a 7-criterion non-trivial draft → `F-RT-JUDGE-ANCHOR-SUSPECTED` advisory.
- `fail/red_team_evidence_paraphrased/` — synthetic verdict with paraphrased quotes → `F-RT-EVIDENCE-NOT-IN-DRAFT`.
- `fail/sfr_malformed_missing_premises/` — synthetic verdict with no Premises block → `F-RT-VERDICT-CERT-MALFORMED.missing_block`.
- `fail/council_split_at_threshold/` — Judge=85, Red Team=75 (delta exactly 10) → `F-COUNCIL-SPLIT` fires (boundary inclusive).
- `fail/council_split_below_threshold/` — Judge=85, Red Team=76 (delta 9) → `F-COUNCIL-SPLIT` does NOT fire (strict inequality boundary).

# §10.12 Interfaces and forward dependencies

**Upstream (Red Team consumes):**
- §0.5 Interface Index — Red Team primitives register as rows (see §10.13).
- §1 Sovereignty Envelope — BYOK key reading via `keys.py` (Red Team's API key per `router.yaml`).
- §2 Vault Topology — `RedTeamVerdict` written via SIMPLE `vault_write` under §4.10 dispatcher.
- §3 Scout — funder dialect classification at Phase 0 (§7.4 alignment).
- §4 Logician — PRE-gates and POST-gates enforcing §10.2 Five-Laws mapping.
- §5 v7 amendment Pipeline — seat-runner that invokes Red Team alongside Judge (§10.10).
- §6 Operating Envelope — SFR parser (§A3); prompt-template compilation pipeline; track-registry row for Red Team probe template; context-placement lint.
- §7 Scribe — `SectionDraft[]` + `claim_evidence_map` consumed at Phase 0.
- §9 Judge — `JudgeVerdict` consumed as context (NOT authority); rubric-shape contract.

**Downstream (Red Team emits to):**
- Operator — consumes verdict + attack memo + Judge verdict + council-split decision UI at sign-off.
- Tab delivery (§5 §4.11) — Red Team's verdict appears in the Council Draft tab alongside Judge's.
- Vault audit chain — verdict bytes contribute to per-run Merkle root (§2 §4.12).

**Prerequisite interlock (§5 v7 amendment) — NOT YET LOCKED.** §10 v1 LOCK is gated on §5 v7 amendment LOCK. The discipline mirrors §7 v1's gating on §6 v1: SCOPING DRAFT pins the shapes, Thesis Round 1 + Round 2 verifies, narrow-fix carve-out lands within L-005 boundary if needed. §10 v1 LOCK seals only after §5 v7 amendment LOCK lands (compound-transaction option per §10.10).

**Sibling-out-of-scope pin.** §7 Scribe, §8 Editor, §9 Judge are LOCKED-as-a-whole-section as of 2026-05-01. §10 v1 names the consumer-side handoff contracts (§10.3 input bundle, §10.6 council-split dispatch) but does NOT respec sibling-seat internals. Any §7/§8/§9 content surfaced during Thesis-round audit must be kicked back.

# §10.13 §0.5 Interface Index rows (proposed at LOCK)

At §10 v1 LOCK, row-append to §0.5 (current LOCKED v5 / pending v6 from §7 v1.1.1; next version slot v6.x):

- `red_team.input_bundle.v1` (schema) — §10.3 `RedTeamInput` shape; parent §10 v1.
- `red_team.verdict.v1` (schema) — §10.5 `RedTeamVerdict` shape; parent §10 v1.
- `red_team.criterion_score.v1` (schema) — §10.5 `RedTeamCriterionScore` shape; parent §10 v1.
- `red_team.attack_memo.v1` (schema) — §10.5 `AttackMemo` shape; parent §10 v1.
- `red_team.weakness.v1` (schema) — §10.5 `Weakness` shape; parent §10 v1.
- `red_team.total_score_correction.v1` (schema) — §10.5 audit shape; parent §10 v1.
- `red_team.council_split_decision.v1` (schema) — §10.6 operator decision shape; parent §10 v1 + §5 v7.
- `red_team.constant.rt_disagreement_threshold.v1` (constant) — §10.6 / §5 v7 §8: `RT_DISAGREEMENT_THRESHOLD = 10`; parent §10 v1 + §5 v7.
- `red_team.constant.rt_anchor_suspected_threshold.v1` (constant) — §10.6 / §5 v7 §8: `RT_ANCHOR_SUSPECTED_THRESHOLD = 2`; parent §10 v1 + §5 v7.
- `red_team.invariant.three_way_family_distinct.v1` (invariant) — §10.7 strict 3-way family-distinct invariant; parent §10 v1 + architecture §E.
- `red_team.invariant.no_score_averaging.v1` (invariant) — §10.6 anti-averaging invariant; parent §10 v1 + architecture §F.1.
- `red_team.invariant.computed_total_authoritative.v1` (invariant) — §10.8 sum-of-criteria authoritative; parent §10 v1.
- `red_team.invariant.tier_matched_verbatim.v1` (invariant) — §10.8 rubric-tier-language verbatim; parent §10 v1.
- `red_team.failure_code.F-RT-INPUT-MISSING.v1` through `red_team.failure_code.F-RT-JUDGE-ANCHOR-SUSPECTED.v1` — one row per failure code in §10.9 (~22 rows); parent §10 v1 + §4 v2.x.
- `red_team.failure_code.F-COUNCIL-SPLIT.v1` (failure-code) — §10.6 + §10.9; parent §10 v1 + §5 v7.
- `red_team.pre_gate.input_consistency.v1` (pre-gate-check) — §10.3 input-bundle invariants; parent §10 v1 + §4 v2.x.
- `red_team.pre_gate.three_way_family_distinct.v1` (pre-gate-check) — §10.7 / §4.16 subclass; parent §10 v1 + §4 v2.5.
- `red_team.post_gate.evidence_in_draft.v1` (post-gate-check) — §10.9 `F-RT-EVIDENCE-NOT-IN-DRAFT` enforcement; parent §10 v1 + §4 v2.x.
- `red_team.post_gate.sfr_three_block_parse.v1` (post-gate-check) — §10.4 / §F.1 subclass; parent §10 v1 + §6 v1 + §4 v2.x.
- `red_team.post_gate.council_split.v1` (post-gate-check) — §10.6 disagreement-threshold enforcement; parent §10 v1 + §5 v7 + §4 v2.x.
- `red_team.post_gate.score_sum_authoritative.v1` (post-gate-check) — §10.8 computed-total enforcement; parent §10 v1 + §4 v2.x.
- `red_team.test.corpus.v1` (test) — §10.11 golden corpus; parent §10 v1.

Row count: approximately 50 rows. All rows enter §0.5 at `stability_tier = PARENT_UNLOCKED` while §10 is in SCOPING DRAFT; promote to `STABLE` at §10 v1 LOCK (post §5 v7 amendment LOCK, in compound transaction with §0.5 v6.x amendment per §10.10).

# §10.14 Open questions (for Thesis-round attention)

**OQ-10.1 — Threshold recalibration mechanism.** §10.6 pins `RT_DISAGREEMENT_THRESHOLD = 10` and `RT_ANCHOR_SUSPECTED_THRESHOLD = 2`. Both are heuristics. Is there a calibration mechanism to tune them per-org based on observed Judge-vs-Red-Team disagreement distribution over a calibration corpus? Recommendation: defer to v0.2 (need observational data first); v0.1 ships the constants with operator-override per `PROJECT_CONTEXT`.

**OQ-10.2 — Red Team revision-loop participation.** §5 v6 inner loop is bounded at 3 iterations. Does Red Team's verdict in iteration N gate the entry to iteration N+1, or does Red Team only fire on the FINAL iteration? Spec card §5 R5 implies Red Team fires every iteration alongside Judge. Recommendation: confirm at §5 v7 amendment Thesis round; lean toward firing every iteration for symmetry with Judge but accept token-cost concern as a v0.2 optimization.

**OQ-10.3 — Council-split decision UX at sign-off.** §10.6 specifies `signoff_pending_council_split` phase + 4-option binary decision. Is the UX inline in the operator-signoff prompt, or a separate decision phase? Recommendation: inline at sign-off; keeps the operator within one decision moment and avoids a second prompt.

**OQ-10.4 — Anti-anchoring smoke check sensitivity.** §10.6 pins `< 2` as the suspect-anchoring threshold on a 100-point scale. Is 2 right? Too tight (false positives on small rubrics)? Too loose? Tie-break: gather observational data over v0.1 deployment; tune in v0.2 amendment.

**OQ-10.5 — Red Team evidence quote length cap (320 chars).** §10.5 caps `evidence` at 320 chars. Is this right? VAPG criterion 5 (Need) might need longer quotes for nuance. Recommendation: cap stays; Red Team summarizes in `notes` if 320 isn't enough; full draft is on-disk for operator deep-dive.

**OQ-10.6 — Per-section Red Team verdict vs whole-draft verdict.** §10.5 RedTeamVerdict has a single `criteria` tuple over the whole draft. Should Red Team also emit per-section critiques (mirror of `SectionDraft` emission)? Recommendation: NO at v1 — Red Team's `attack_memo` already names sections in `claim` strings; per-section verdict adds token cost without commensurate value. Reopen at v0.2 if operator deployment shows missing per-section signal.

**OQ-10.7 — Soul-fire dialect Red Team prosecution.** Red Team's analytical voice is conservative-or-neutral by §10.5 design. But a Soul-fire-dialect funder may want the prosecution to ALSO speak Soul-fire (a critique in the funder's own register). Is this a v0.1 scope question? Recommendation: defer to v0.2 — analytical voice stays conservative-or-neutral at v0.1 to keep Red Team's anti-anchoring discipline maximally legible; v0.2 may register-match per funder-classification.

**OQ-10.8 — Score parity with Judge sub-criteria.** Judge §9 supports hierarchical rubrics (parent + subcriteria). Does Red Team score at parent-level only, subcriteria-level only, or both? Recommendation: SAME structure as Judge — if Judge scored subcriteria, Red Team scores subcriteria; if Judge scored parent, Red Team scores parent. **CLOSED at v1.1** — implemented at R2 `pipeline/seats/red_team/cross_rubric_dispatch.py` (`select_scoring_targets` + `assert_red_team_id_set_matches_judge` identity-invariant). §10.8 + §10.9 carry the F-RT-CRITERION-MISSING enforcement.

**OQ-10.9 (NEW v1.1; closes RT-r1-F6) — MIN_TOP_WEAKNESSES = 1 vs flawless drafts.** v1 enforces ≥ 1 weakness; on a genuinely flawless draft this could force the model to invent. v0.2 roadmap commitment: add a structural-pass escape (`top_weaknesses` may be empty when accompanied by `attack_memo.no_material_weakness_attestation: str` carrying ≤ 80-char operator-or-model-attested justification + Logician POST-gate verifying the attestation traces to draft strengths, not absence-of-coverage). v0.1 retains the ≥ 1 invariant deliberately — Red Team's prosecutorial purpose is undermined by silent passes; the MIN-1 pressure is a feature for the typical case (real drafts have weaknesses), and the v0.2 escape is for the genuinely-flawless edge case.

**OQ-10.10 (NEW v1.1; closes RT-r1-F3) — Middle-block anti-anchoring lint.** §10.8 head + tail placement leaves the middle block uncovered. v0.2 roadmap commitment: Red-Team-specific middle-block lint scanning for known anti-anti-anchoring phrasings ("ignore the previous instruction", "Judge's score IS authority"). v0.1 forwards `F-CONTEXT-MIDDLE-CONTRADICTION` from §6 (architecture §A4) per §10.9.

**OQ-10.11 (NEW v1.1; closes RT-r1-F1) — Anti-averaging AST-grep coverage expansion.** v1 bans the closed list of arithmetic patterns; v0.2 expands to weighted-arithmetic and `statistics` module callsites.

# §10.15 Version history

- **v1.1 narrow-fix carve-out 2026-05-02 (Round 1 author-fixes).** Thesis Round 1 verdicts: Judge READY_TO_LOCK 100/100 zero residuals; Editor REQUIRES_MINOR_FIXES (5 handwave items, all addressed in current §10 prose — Editor mis-read scope; documentary-level only); Red Team REQUIRES_MAJOR_MITIGATIONS 3 HIGH + 4 MEDIUM + 1 LOW. Triage: 4 findings ACCEPTED → narrow-fixes applied this round (RT-r1-F1 anti-averaging AST-grep expansion → §10.6 closed-list ban + OQ-10.11; RT-r1-F3 middle-block surface → §10.8 v1.1 acknowledgment + F-CONTEXT-MIDDLE-CONTRADICTION forward + OQ-10.10; RT-r1-F4 tier-matched per-criterion scoping → §10.5 schema text tightened; RT-r1-F8 admin-risk-flag enforcement → §10.9 reuse-§7.11-scanner clarified); 1 finding ACCEPTED with v0.2 commitment + OQ-10.9 (RT-r1-F6 MIN_TOP_WEAKNESSES=1 escape); 3 findings DESIGN-DEFENDED (RT-r1-F2 cascade-reorder-before-family-check already specified at §10.7; RT-r1-F5 CouncilSplitDecision constructor-vs-gate boundary deliberate per §10.6 commentary; RT-r1-F7 SFR structural-only by architecture §F.1 LOCKED); 0 findings escalated to architecture round. Awaits Round 2 VERIFICATION dispatch.

- **v1 SCOPING DRAFT 2026-05-01.** First blueprint section for Red Team. Lifted from `pipeline/orchestrator/seats/red_team.py` (operational today, 337 LOC, predates the seat-lifecycle pattern) + architecture §A3 (SFR three-block, LOCKED v7 2026-04-19) + architecture §E (cross-family rigor) + architecture §F.1 (`F-VERDICT-CERT-MALFORMED` POST-gate) + architecture §M13 (review-seat outage escape valve) + §4 v2.5 (`F-ROUTER-FAMILY-COLLISION`) + §7 Scribe v1.1.1 (input contract: `SectionDraft` + `ClaimEvidence`) + §9 Judge whole-section LOCK 2026-05-01 (input contract: `JudgeVerdict`) + the orchestrator-CLI's existing attack memo schema (`top_weaknesses`, `unsupported_assertions`, `dialect_mismatches`, `boundary_drift`, `overall_verdict`). Authored under operator directive "Draft §10 Red Team blueprint ... BUDGET MODE OK if scoped tight (no Thesis dispatch this session). Preps for Thesis round." Status: **SCOPING DRAFT awaiting Thesis Round 1.** Prerequisite interlock for v1 LOCK: §5 v7 amendment LOCK (must wire Red Team into the inner loop alongside Judge per §10.10); §0.5 v6.x amendment row-append (~50 rows per §10.13). Thesis Round 1 dispatch deferred to a future session per BUDGET MODE; this round LOCKs the SCOPING DRAFT shape, not the v1 content.

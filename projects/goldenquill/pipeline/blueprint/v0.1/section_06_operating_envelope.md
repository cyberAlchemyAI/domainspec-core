---
title: Blueprint §6 Operating Envelope — router / SFR / context-placement / track-registry host (v1-r1 LOCKED)
filed: 2026-04-20 (v1); 2026-04-21 (v1-r1 post-Audit-1 revision); 2026-04-21 (v1-r1 LOCKED after Audit #2 READY_TO_LOCK)
operator: Josh
status: **LOCKED 2026-04-21** — v1-r1 LOCKED as compound transaction with §0.5 v6 amendment per §6.17. L-005 two-audit cycle complete: Audit #1 (driver) 2026-04-21 council split (Judge MINOR_FIXES + Red Team ARCHITECTURE_ROUND) → v1-r1 revision resolved all residuals (3 fixed, 3 rebutted) per §6.19; Audit #2 (verification) 2026-04-21 unanimous READY_TO_LOCK (Editor `CLEAR_TO_LOCK` + Judge `READY_TO_LOCK` + Red Team `READY_TO_LOCK`, zero residuals), closeout at `pipeline/validation/section_06_thesis_round_2/closeout_summary.md`. Runtime-live at §6 LOCK. Unblocks §7 Scribe LOCK (downstream per §7.15).
parent_locks:
  - pipeline/architecture/v0.1/tilth_architecture_locked.md                      # v7 LOCKED 2026-04-19 — A1 Section K hardware; §D.7 Opus 4.7 envelope (A2 Block 1 + Block 2); §D.8 context-rot (A4); §F.1 SFR format (A3); §R.PF1 track-registry (A6); §0 PRE-gate precedence
  - pipeline/blueprint/v0.1/section_04_logician.md                               # v2.1 LOCKED 2026-04-19 — §6 emits its PRE-gates + POST-gate (F-VERDICT-CERT-MALFORMED) into the Logician fail-closed registry
  - pipeline/blueprint/v0.1/section_02_vault_topology.md                         # v7.1 LOCKED 2026-04-19 — router.yaml and prompt templates are vault-persisted primitives; §6 defines their schemas, §2 defines their storage
  - pipeline/blueprint/v0.1/section_05_pipeline.md                               # v6 LOCKED (pending §5 v6 spin per A6) — §5 consumes the track-registry §6 publishes
  - pipeline/blueprint/v0.1/section_00_5_interface_index_locked.md               # §0.5 v5 LOCKED 2026-04-19 — §6 primitives register as rows; count bump obligations bind this section
downstream_consumers:
  - §3 Scout — consumes router.yaml seat bindings
  - §5 Pipeline — consumes the track-registry + seat-runner prompt-compilation contract
  - §7 Scribe — consumes router.yaml (Anthropic Opus 4.7 binding) + prompt-template compilation pipeline + SFR POST-gate (for Scribe-adjacent review seats)
  - §8 Editor — consumes prompt-template compilation + SFR exemption row
  - §9 Judge — consumes router.yaml + prompt-template compilation + SFR three-block contract
  - §10 Red Team — consumes router.yaml + prompt-template compilation + SFR three-block contract
  - Code Thesis Committee flow — consumes router.yaml Block 2 + SFR three-block contract for all five reviewers
note: §6 is a HOST section — it defines schemas, lints, compilers, and registries consumed by execution-side blueprint sections. It does not itself run a seat. Its "runtime behavior" is pipeline-start schema validation + per-seat-invocation prompt composition; it has no outer-loop of its own.
---

# §6.1 Purpose and scope

§6 Operating Envelope is the host section for the Tilth pipeline's compile-time and pipeline-start infrastructure that every seat depends on but no seat owns. The section publishes four schema artifacts (router.yaml non-code block, router.yaml code block, SFR certificate format, hardware-tier metadata) and three active mechanisms (the prompt-template compilation pipeline, the context-placement lint with middle-contradiction detection, the SFR POST-gate parser), wraps them in seven PRE-gates + one POST-gate that Logician enforces, and binds them to a deterministic precedence table that orders PRE-gate evaluation at every pipeline run start.

**What §6 OWNS (authoritative for v0.1):**
- **Router.yaml schema** — both blocks (A2 Block 1 non-code Opus 4.7 envelope; A2 Block 2 code Thesis Committee). No other blueprint section may define router schema constraints; other sections CONSUME this schema.
- **SFR (Semi-Formal Reasoning) certificate format** — three-block Premises/Trace/Conclusion (A3). The Logician POST-gate parser spec (`F-VERDICT-CERT-MALFORMED`) lives here. Editor exemption row lives here.
- **Prompt-template compilation pipeline** — the compile step that loads a seat's base prompt, injects start-block + end-block load-bearing constraints (Five Laws + scope + gates + schemas per A4), runs the context-placement lint, runs the middle-contradiction lint, and emits a composed prompt ready for the seat invocation.
- **Context-placement enforcement** — `F-CONTEXT-PLACEMENT` PRE-gate (architectural FLOOR per A4) + the middle-contradiction detection lint that v7 architectural Cycle-2 delegated to §6 (closes RT-v7-M-03).
- **Track-registry extension mechanism** — the registry `router.yaml` row shape that §5 consumes to make `submission_mode` and `eval_mode` data-driven rows rather than hardcoded enum values (A6 R.PF1). The mechanism ships at v0.1 with two rows; adding v0.2 tracks (report / content / tdsl_query) requires router.yaml append + prompt-template addition only.
- **Hardware-tier metadata** — Pro / Baseline / Dev tier triple from architecture §K (A1). §6 publishes the canonical machine-readable form; downstream sections (§5 delivery, §2 vault capacity planning) consume it.
- **PRE-gate precedence table** — the deterministic total order Logician evaluates PRE-gates at every pipeline run start. Verbatim from architecture §0 (closes RT-v7-M-08).
- **D-05 Downstream drift audit checklist** — the checklist every LOCKED blueprint section runs at every downstream-LOCK to verify the LOCKED section's claims have not drifted against its parent architecture version.

**What §6 DOES NOT OWN (pointers to owners):**
- Seat execution logic — see §3 (Scout) / §7 (Scribe) / §8 (Editor) / §9 (Judge) / §10 (Red Team). §6 compiles their prompts; §6 does not drive their output.
- Vault persistence of the compiled-prompt artifact or the router.yaml artifact — see §2 Vault Topology §4.10. §6 defines WHAT goes in; §2 defines HOW it is written.
- Logician's broader fail-closed registry — see §4 Logician §4.1–§4.9. §6 submits its PRE-gate codes + POST-gate code to that registry; §4 owns the registry itself.
- Pipeline orchestration and revision-loop cap — see §5 Pipeline §1–§4. §6 publishes the track-registry §5 consumes; §5 owns the orchestration.
- Signed-commit discipline for router.yaml and vault_shared/ — see architecture §E [M15]. §6 assumes a signed router.yaml is on disk; §6 does not sign.

**v0.1 scope boundary.** §6 ships with exactly the schemas A1–A4 + A6 commit the architecture to. §6 does NOT ship R.1 TDSL schema, R.2 Content schema, or R.3 Reporting schema (all v0.2 per Section R). §6 DOES ship the track-registry mechanism those v0.2 tracks will register against (A6 R.PF1 is a v0.1 pull-forward — the mechanism exists at v0.1 even though only `submission` and `eval` tracks populate it).

# §6.2 PRE-gate precedence table (verbatim from architecture §0, closes RT-v7-M-08)

Logician evaluates PRE-gates in the following deterministic total order at every pipeline run start, before any seat prompt compiles. The table is authoritative; §4 Logician consumes this table as its PRE-gate scheduling order.

| Order | Gate | Guards |
|---|---|---|
| 1 | N.4.1 Section 2 blueprint lock-marker | Vault schema lock (fail-closed if §2 is not at a LOCKED version header) |
| 2 | N.4.2 trust-root mirror verified | Trust root (operator keyring mirror fresh vs. last verification) |
| 3 | `F-INDEX-STALE` | §0.5 Blueprint Interface Index freshness (index row count + content SHA match) |
| 4 | `F-N1-COUNT-STALE` | Section N.1 row count (section enumeration matches current count; at v7, N.1 count = 6) |
| 5 | `F-ROUTER-STALE-API`, `F-CODE-COMMITTEE-INCOMPLETE`, `F-CODE-RETRY-OVERRUN` | router.yaml schema (both blocks; the three codes share order 5 and are evaluated in enumeration order) |
| 6 | `F-SECTION-R-INCOMPLETE`, `F-TDSL-LEAK-V01` | Architecture structural invariants (Section R presence + v0.1→TDSL reference prohibition) |
| 7 | `F-CONTEXT-PLACEMENT` | Per-seat prompt template structure (start-block + end-block load-bearing constraints per A4 architectural FLOOR) |
| 8 | (middle-contradiction lint, §6 blueprint) | Per-seat compiled-prompt semantic contradiction between blocks (§6.6 — NEW in this blueprint) |

**F-INDEX-STALE fires at order 3 BEFORE any v7 failure-code check at orders 4–7.** This is deliberate: a stale index is the root-cause failure class that allows other gates to mis-scope. Catching staleness first makes downstream gate failures interpretable.

**F-VERDICT-CERT-MALFORMED is a POST-gate, not in this PRE-gate table.** It fires on the Judge's or Red Team's returned verdict blob after the seat completes; PRE-gate timing would be nonsensical (the verdict does not exist at run start). See §6.5.

**Gate ordering is stable across v0.1 minor versions.** New PRE-gates added post-LOCK insert at the end (order ≥ 9) unless they represent root-cause classes upstream of the existing order, in which case a §6 blueprint round reissues the whole table. No blueprint section other than §6 may mutate this ordering.

# §6.3 A2 Block 1 — router.yaml schema for non-code Opus 4.7 envelope

Authoritative for every Anthropic Opus 4.7 binding in Tilth (Scribe primary, Scribe escalation, any future Anthropic Opus 4.7 seat). Consumed by §7 Scribe's seat-runner, by §5 Pipeline's router loader, and by Logician's `F-ROUTER-STALE-API` PRE-gate validator.

**Schema shape (router.yaml fragment).** Every Opus 4.7 binding row in `router.yaml` MUST conform to:

```yaml
seats:
  <seat_name>:                      # e.g., scribe_primary
    provider: anthropic
    model: claude-opus-4-7
    effort: xhigh                   # enum: {high, xhigh, max}; logician-enforced per seat
    max_tokens: 64000               # integer, MUST be >= 64000 for effort in {xhigh, max}
    # NO temperature, NO top_p, NO top_k — Opus 4.7 rejects these with HTTP 400
    beta_header: "task-budgets-2026-03-13"
    tokenizer_calibration: 1.2      # float in [1.0, 1.35]; multiplier over prior-tokenizer budget
    family: anthropic               # cross-family rigor key (consumed by §E M5)
```

**Per-seat effort assignment (LOCKED per architecture §D.7 Block 1):**
- `scribe` → `xhigh`
- `editor` → `xhigh`
- `judge` → `xhigh`
- `red_team` → `max`
- `logician` → N/A (deterministic; no LLM call; no router row beyond config pointer)

**Constraints Logician's `F-ROUTER-STALE-API` PRE-gate enforces (fail-closed):**
1. **No forbidden fields.** If any Anthropic Opus 4.7 binding contains `temperature`, `top_p`, or `top_k`, fail-closed with evidence citing the specific field(s) and the binding row.
2. **Beta header present and correct.** `beta_header == "task-budgets-2026-03-13"` exactly. Missing or mismatched → fail-closed with evidence citing expected vs. detected.
3. **Effort enum valid.** `effort ∈ {high, xhigh, max}`. Any other value → fail-closed.
4. **Max-tokens floor.** For `effort ∈ {xhigh, max}`, `max_tokens >= 64000`. Lower → fail-closed with evidence citing detected max_tokens and binding row.
5. **Tokenizer calibration present and in range.** `tokenizer_calibration ∈ [1.0, 1.35]`. Absent or out-of-range → fail-closed. Rationale: Opus 4.7 ships a new tokenizer that runs 1.0–1.35× the prior tokenizer on the same text; legacy budgets calibrated against Sonnet 4.6 / Opus 4.6 will under-allocate unless explicitly recalibrated. **Source of truth (verified against Anthropic documentation during Thesis Round 1 on 2026-04-21):** Anthropic's Claude Opus 4.7 migration guide at `platform.claude.com/docs/en/about-claude/models/migration-guide` states verbatim: *"The new tokenizer may use roughly 1x to 1.35x as many tokens when processing text compared to previous models (up to ~35% more, varying by content)."* The `[1.0, 1.35]` range is the published upper envelope, not an internally-invented heuristic. If Anthropic publishes a revised bound, `F-ROUTER-STALE-API` fires on the existing calibration row and operator widens the range via a §6 blueprint amendment (not an architecture round — the range is a published-constant dependency, not an architectural invariant). Adversarial-input caveat: Anthropic's "varying by content" language implies pathological inputs (rare-token-heavy text, homoglyph-dense text, non-English scripts with low BPE compression) may sit at the high end of the range; the 1.35 ceiling is the empirical upper bound per provider, and workloads that consistently exceed it in practice constitute operator-actionable evidence to escalate to Anthropic support before widening the Tilth-side range.
6. **Family marker present.** `family == "anthropic"` for cross-family rigor enforcement (§E M5 consumes this).

**Fail-closed-AND-diagnostic (v7 Cycle-2 closes RT-v7-M-01).** `F-ROUTER-STALE-API` is NOT a silent abort. On fire, Logician surfaces a structured error payload with fields `{expected_version, detected_version, failing_field, binding_row, remediation_hint}`. Operator-actionable escalation event; operator updates router.yaml to match the new API envelope; next run proceeds.

**Escalation example (router-drift case).** Anthropic publishes a new Opus 4.7.x point release with a beta-header rename. Logician detects the stale header, emits `F-ROUTER-STALE-API` with `{expected_version: "task-budgets-2026-03-13", detected_version: "task-budgets-2026-06-01", failing_field: "beta_header", binding_row: "seats.scribe_primary", remediation_hint: "update beta_header to 2026-06-01 after verifying Anthropic changelog at platform.claude.com/whats-new-claude-4-7"}`. Operator verifies upstream, updates, runs again; `F-ROUTER-STALE-API` no longer fires.

# §6.4 A2 Block 2 — router.yaml schema for code Thesis Committee

Authoritative for the code-pipeline router binding. Consumed by the Code Thesis Committee flow (Claude Code authors; five reviewers review) and by Logician's `F-CODE-COMMITTEE-INCOMPLETE` + `F-CODE-RETRY-OVERRUN` PRE-gates.

**Schema shape (LOCKED 2026-04-18 per memory `project_code_thesis_committee.md`; reproduced verbatim from architecture §D.7 Block 2):**

```yaml
code_author:        anthropic/claude_code
code_reviewer_1:    openai/codex
code_reviewer_2:    alibaba/qwen3-32b        # general, NOT coder
code_reviewer_3:    meta/llama-3.3-70b
code_reviewer_4:    openai_oss/gpt-oss-120b
code_reviewer_5:    moonshot/kimi-k2-instruct-0905
code_merge_rule:    all_pass
code_retry_cap:     1
code_findings_path: pipeline/validation/code_reviews/<pr-id>/
code_dashboard_post: batch
```

**Design constraints (each enforced by a Logician PRE-gate):**
- **Five-reviewer cross-family ensemble.** Families: Anthropic (author) / OpenAI / Alibaba / Meta / OpenAI-OSS / Moonshot. Six distinct families total (author + 5 reviewer families), no family shared between author and reviewers. A sixth Anthropic reviewer would violate cross-family discipline and trip `F-CODE-COMMITTEE-INCOMPLETE`.
- **All-PASS merge rule.** Any single reviewer PASS-failure blocks merge. This is LOCKED; `code_merge_rule` MUST equal `all_pass`. Any other value (e.g., `majority_pass`, `3_of_5_pass`) trips `F-CODE-COMMITTEE-INCOMPLETE`.
- **One retry cap.** `code_retry_cap == 1`. After one retry, if not all-PASS, escalate to operator + Opus 4.7 synthesis per L-005 domain-split (the escalation pathway is an ARCHITECTURAL event, not an infinite-retry loop — v7 Cycle-2 closes RT-v7-H-02).
- **Qwen 3 32B is deliberate non-specialist coverage.** Code-specialist models over-fit to idioms; a generalist questions the approach itself. `reviewer_2` is LOCKED to a general-purpose model; substituting a code-specialist Qwen variant trips `F-CODE-COMMITTEE-INCOMPLETE` with reason `specialist_substituted_for_generalist`.

**Logician PRE-gates:**
- **`F-CODE-COMMITTEE-INCOMPLETE`** — fail-closed if any of the five reviewer slots is missing, mis-bound (wrong family, specialist-substituted-for-generalist), or if `code_merge_rule != all_pass`.
- **`F-CODE-RETRY-OVERRUN`** — fail-closed AND escalate to operator if a code flow has exceeded `code_retry_cap`. This is not a dead-end; it is an architectural escalation event. Operator reviews, reauthors with Opus 4.7 synthesis of reviewer feedback, or explicitly bypasses with signed authorization (parallel to §E M13 review-seat bypass).

**Non-code artifacts.** The code committee router binds only to code artifacts (Python modules, Cedar policies, prompt templates implemented as code). Non-code artifacts (blueprint sections, architecture sections, grant prose, RFA extractions) flow through the non-code Thesis Team (Editor + Judge + Red Team) under A2 Block 1. Conflating the two routers trips `F-CODE-COMMITTEE-INCOMPLETE` with reason `artifact_kind_mismatch`.

# §6.5 A3 Semi-Formal Reasoning (SFR) certificate format + POST-gate parser

**Status.** A3 amendment from architecture v7. Source: Ugare + Chandra, arXiv 2603.01896 (March 2026). §6 blueprint is the authoritative implementation host.

**Three-block structure (A3 reproduced; §6 adds parser spec + Editor exemption row):**

1. **Premises** — explicit facts + citations. Every premise carries a citation pointer to the source artifact in one of these forms:
   - `RFA:<orgs-slug-or-shared>:<relative-path>:<line-range>`
   - `BLUEPRINT:<section-file>:§<section-number>`
   - `ARCHITECTURE:<section-letter>.<subsection>`
   - `LOCK:<path-to-prior-lock>:<version>`
   - `DOSSIER:<path>:<content-hash>`
   - `OPERATOR_MSG:<conversation-anchor>`
   
   Premises with no citation are not premises; they are claims the verdict author cannot support and MUST be removed from the verdict. Parser rejects any premise with `citation == null` or `citation == ""`.

2. **Execution trace** — ordered steps citing premises by ID. Each step references one or more premises (by `P-<N>` citation) and applies a named inference rule. Named inference rules at v0.1:
   - `parent-wins` (§0.5.3 invariant)
   - `rfa-source-of-truth` (Law 1)
   - `org-isolation` (Law 3)
   - `dialect-preservation` (Law 4 substance-not-style)
   - `failure-code-precedence` (§6.2 PRE-gate table)
   - `cross-family-rigor` (§E M5)
   - `signed-commit-verified` (§E M15)
   - `cedar-policy-dispatch` (§4.11 compound-commit predicate)
   - `compound-transaction-atomicity` (§2 §4.10.7 + §4 §4.11)
   - `blueprint-consistency-check` — a premise-sequence derives an assertion about whether the target blueprint is internally consistent with its paired amendments and its parent LOCKs. Invoked by Judge seat during D-05 downstream-drift audits (§6.9) and during Thesis-round cross-artifact coherence checks.
   - `external-dependency-verification` — a premise cites a provider-documented constant (e.g., Anthropic migration-guide token-ratio, Groq catalog model IDs, Google Gemini context-window caps) and the step affirms or rejects the blueprint's claim about that constant based on live documentation. Used for any router.yaml or §6.8 hardware-tier row whose load-bearing values originate outside the Tilth source tree.
   - `empirical-boundary-test` — a step asserts a numeric upper or lower bound (e.g., `tokenizer_calibration ≤ 1.35`, `MAX_COMPOUND_TXN_BYTES = 64 MiB`) based on adversarial-input construction or an on-disk measurement. The step's validity rests on reproducibility: any reviewer re-running the construction should reach the same conclusion.
   - `replay-reconstruction` — an adversarial inference rule used by Red Team. A step asserts that a persisted artifact (hash, SHA, audit-stamp) is reconstructable-back-to-source-content by an attacker who holds (a) the artifact, (b) knowledge of the deterministic pipeline that produced it, and (c) replay capability against that pipeline. Used to probe §J grant-content-never-flows invariant violations via structural deduction rather than direct leakage. A `replay-reconstruction` step MUST cite both the persisted-artifact premise and the pipeline-determinism premise — otherwise it is floating-assertion and the parser rejects.
   - `size-audit` — a step asserts that a measured size (byte-count of a bundle, row-count of an index, entry-count of a ledger) sits at, approaches, or exceeds a declared capacity constant. The step MUST either (a) cite the actual on-disk measurement as a premise, or (b) cite an explicit approximation methodology (e.g., "sum of `wc -c` for the staged files"). Pure speculation about size without measurement is floating-assertion.
   - `<other>` (any rule a reviewer invokes; parser accepts any identifier matching `[a-z][a-z0-9-]{1,63}`, but a rule name not in the v0.1 registry triggers a soft-warning `rule_unknown` that operator can escalate)
   
   **v0.1 registry content note.** The six rules above beyond the base nine (`blueprint-consistency-check`, `external-dependency-verification`, `empirical-boundary-test`, `replay-reconstruction`, `size-audit`, and the open-slot `<other>` sentinel) were added in v1-r1 after Thesis Round 1 dogfood surfaced them as `rule_unknown` soft-warnings in Judge + Red Team verdicts. This is the parser-registry extension pathway working as designed: dogfood use exposes a missing rule name, the rule is registered by §6 blueprint amendment, and subsequent verdicts invoke it without soft-warning.
   
   Steps that do not cite premises are floating reasoning and the parser rejects them.

3. **Conclusion** — derives ONLY from declared premises + trace. A conclusion that depends on a premise not declared in block 1 OR on a step not in the trace is MALFORMED. The conclusion may include the verdict tier (one of `READY`, `READY_TO_LOCK`, `REQUIRES_MINOR_FIXES`, `REQUIRES_MAJOR_MITIGATIONS`, `REQUIRES_ARCHITECTURE_ROUND`) and a residual list, but every residual MUST trace back to a specific step or premise.

**Logician POST-gate — `F-VERDICT-CERT-MALFORMED`.** Parser spec:

1. **Block boundary detection.** Parser looks for three markdown H2 headers `## Premises`, `## Execution trace`, `## Conclusion` (case-insensitive; trailing-punctuation tolerant). Exactly three such headers, in that order, MUST appear at the same heading level. Zero / one / two / four+ headers → malformed with evidence `block_count_mismatch`.
2. **Premises block parse.** Each premise is a markdown list item prefixed `P-<N>:` followed by the premise text and a citation pointer in one of the accepted forms. The parser extracts `(id, text, citation_kind, citation_target)`. Missing `P-<N>:` prefix, missing citation, or unrecognized `citation_kind` → malformed with evidence `premise_<index>_<specific-defect>`.
3. **Trace block parse.** Each trace step is a markdown list item prefixed `S-<N>:` followed by step text, `CITES: P-<a>, P-<b>, ...`, and `RULE: <rule-name>`. Extracts `(id, text, cited_premises, rule_name)`. Every cited `P-<N>` MUST exist in the premises block; unresolved → malformed with evidence `step_<index>_cites_missing_premise_<N>`.
4. **Conclusion block parse.** Verdict tier MUST appear as `VERDICT: <tier>`; residual items MUST be markdown list items prefixed `R-<N>:` with a trailing `TRACES: <P-<x>|S-<y>>`. Every trace target MUST exist in a prior block; unresolved → malformed with evidence `residual_<index>_traces_missing_<anchor>`.
5. **Fail-closed on any parse failure.** Reissue is requested with a structured error citing the specific malformation. The requester (Judge, Red Team, or any code-side reviewer under §D.7 Block 2) receives the structured error as its next-round prompt input; the requester re-emits a corrected certificate.

**Structural gate, not semantic (v7 Cycle-2 closes RT-v7-M-02).** The parser does NOT evaluate whether citations point at real artifacts, whether premises are factually correct, or whether inference rules are sound. It parses markdown shape only. Semantic correctness is defended by the cross-family reviewer ensemble (§E) — if a reviewer cites a fabricated path, a second reviewer's independent verdict flags the semantic defect. `F-VERDICT-CERT-MALFORMED` is deliberately narrow because it is a machine-parseable gate, not an AGI.

**Coverage (authoritative list):**
- Non-code Thesis Team: **Judge** and **Red Team** on every audit round (architecture, blueprint, prior-art).
- Code-side five reviewers: **Codex, Qwen 3 32B, Llama 3.3 70B, GPT-OSS 120B, Kimi K2** on every code review under §D.7 Block 2.
- Editor seat is **EXEMPT**. Editor's job is structured clarity feedback, not adversarial verdict. Editor's output is structured-feedback-not-verdict. The exemption row belongs in §6 (this is the §F.1 commitment: "The exemption is named in §6 Operating Envelope blueprint"). §6.5 exemption clause:

  > **Editor exemption.** Editor's output passes through a separate Logician POST-gate (`F-EDITOR-STRUCTURED-FEEDBACK-MALFORMED`, defined by §8 Editor blueprint, not §6) that validates Editor's clarity-feedback schema. `F-VERDICT-CERT-MALFORMED` does NOT fire on Editor output.

**Test surface (§6.13).** The v1 SCOPING DRAFT test suite ships a corpus of 12 certificates: 3 well-formed (one per verdict tier at READY / REQUIRES_MINOR_FIXES / REQUIRES_ARCHITECTURE_ROUND); 9 malformed (one per named parser failure class above). Corpus lives at `pipeline/operating_envelope/test_corpus/sfr/`.

**Dogfood trail.** v7 architecture itself was the first artefact to dogfood A3 — the v7 driver-round and verification-round verdicts were authored in SFR format. Pre-v7 verdicts (v6-r2 audits, Option-B Round 3 Red Team v3) are NOT retroactively re-formatted.

# §6.6 A4 Context-placement enforcement + middle-contradiction detection

**Status.** A4 architectural FLOOR (`F-CONTEXT-PLACEMENT` PRE-gate); middle-contradiction detection is the v7 Cycle-2 delegation that §6 closes (RT-v7-M-03).

**A4 FLOOR (`F-CONTEXT-PLACEMENT` PRE-gate).** Every seat prompt template (Scout, Scribe, Editor, Judge, Red Team, Logician-issued reasoner-review prompts, code-side reviewer prompts under §D.7 Block 2) MUST place **load-bearing constraints** at BOTH the start AND the end of the compiled prompt. Load-bearing constraints = the Five Operating Laws (B) + the active scope statement (RFA path + boundary clauses) + the active gate set (PRE-gates the seat must satisfy + POST-gates the seat will be evaluated against) + the active schema (kind-class registry rows + failure-code rows the seat may emit + Logician allowlist rows the seat may invoke).

**Prompt-template compilation pipeline (§6.11 defines the pipeline; this section defines the lint step inside it).** For each seat-invocation compile, Logician's lint step runs before the prompt is dispatched to the provider:

1. Tokenize the compiled prompt into blocks (start-block = first N characters before the first seat-content marker; end-block = last N characters after the last seat-content marker; middle-block = everything else). N = 2000 characters by v0.1 default, operator-configurable per-seat.
2. Scan start-block for presence of: Five-Laws-block marker, scope-block marker, gate-block marker, schema-block marker. All four must be present.
3. Scan end-block for the same four markers. All four must be present.
4. If either block is missing any marker → `F-CONTEXT-PLACEMENT` fires with evidence citing the missing markers and the block (start or end). Hard abort; no retry. Operator fixes the template; next run proceeds.

**Middle-contradiction detection (v7 Cycle-2 § closes RT-v7-M-03 — §6 obligation).** An adversarial actor (hostile content in an RFA, an attacker-influenced PROJECT_CONTEXT, or a Bucket-A same-uid-peer template-tamper) can place contradictory instructions in the middle-block — instructions that contradict the start-block or end-block load-bearing constraints. A4 FLOOR is silent on this attack class by design (it is deliberately narrow to structural placement). §6 closes the gap:

1. **Semantic-contradiction lint.** After the compiled prompt passes the structural F-CONTEXT-PLACEMENT check, a second lint step runs. It extracts the literal strings of the four load-bearing markers from the start-block and from the end-block. It then scans the middle-block for strings that contradict any of the four markers using a deterministic nine-class ruleset (classes 1-4 were authored in v1 against the v7 architectural charge; classes 5-9 were added in v1-r1 after Thesis Round 1 Red Team verdict flagged them as v0.1-threat-model-relevant attack classes the v1 surface omitted — see §6.19 author-response item R-1):
   - **Class 1 — Five-Laws contradictions.** Middle-block scan for substrings that assert any of: "ignore Law <N>", "skip Law <N>", "Law <N> does not apply", "bypass Law <N>", "override Law <N>", and case-insensitive variants. Match → fail-closed with evidence `middle_contradicts_five_laws`.
   - **Class 2 — Scope contradictions.** Middle-block scan for substrings that assert the seat work outside the named scope: "ignore scope", "out of scope is fine", "expand scope to X", where X is any slug NOT in the active scope list. Match → fail-closed with evidence `middle_contradicts_scope`.
   - **Class 3 — Gate contradictions.** Middle-block scan for substrings that assert gate-bypass: "skip F-<CODE>", "ignore PRE-gate", "bypass Logician", "do not check <failure-code>", and case-insensitive variants. Match → fail-closed with evidence `middle_contradicts_gate`.
   - **Class 4 — Schema contradictions.** Middle-block scan for substrings that assert a seat use a failure-code or allowlist row not declared in the start/end schema block. Declared schema is the ground truth; middle invention → fail-closed with evidence `middle_contradicts_schema`.
   - **Class 5 — Direct-prompt-injection strings (v1-r1, Red Team verdict item).** Middle-block scan for generic injection-frame substrings that attempt to reset the provider's instruction-following: "ignore prior instructions", "ignore previous instructions", "disregard the above", "forget everything", "start over", "reset your context", "the above was a test", "actually the real task is", and case-insensitive variants. Match → fail-closed with evidence `middle_contains_prompt_injection`. Rationale: the v0.1 threat model (solo operator, BYOK, Golden Quill local hardware) does not exclude attacker-authored content reaching the middle-block — hostile RFA text, attacker-influenced project-context, and upstream scraped content can all carry such strings. A4 FLOOR is silent on these because the strings do not name a specific Law / scope / gate / schema marker, so Classes 1-4 miss them.
   - **Class 6 — Role-confusion / impersonation (v1-r1).** Middle-block scan for substrings that attempt to rebind the seat's identity: "you are now a different", "you are actually a", "pretend you are", "roleplay as", "for this turn you are", "your real name is", "new system prompt:", "new instructions follow", and case-insensitive variants. Match → fail-closed with evidence `middle_contains_role_confusion`. Rationale: seat role is pinned by router.yaml (§6.3 / §6.4) and by the compiled prompt's start/end schema; middle-block re-binding is adversarial by construction.
   - **Class 7 — Prompt-leak / system-prompt exfiltration (v1-r1).** Middle-block scan for substrings that attempt to exfiltrate the seat's compiled prompt, Five-Laws block, scope statement, or schema: "print your system prompt", "show me your instructions", "repeat the text above verbatim", "output your initialization", "dump your context", "what are your rules", and case-insensitive variants. Match → fail-closed with evidence `middle_contains_prompt_leak_attempt`. Rationale: the compiled prompt contains scope (RFA path) and schema (allowlist rows) that are operator-confidential; §J grant-content-never-flows applies to RFA content inside compiled prompts and Class 7 defends the provider-side exfil surface.
   - **Class 8 — Unicode-lookalike homoglyph attacks on Law-keywords (v1-r1).** Middle-block scan normalizes the text via NFKC Unicode normalization, then re-runs the Class 1 / Class 3 scans on the normalized form. This catches substitutions like Cyrillic "А" (U+0410) for Latin "A" (U+0041), or fullwidth digits for ASCII digits, that defeat the literal-string scans in Classes 1+3. Match → fail-closed with evidence `middle_contradicts_<class>_via_homoglyph` (evidence carries both the literal middle-block text byte-range AND the normalized form that tripped the scan, so operator can trace the substitution). Rationale: Classes 1 and 3 key off literal ASCII substrings; a Cyrillic-masked "ignore Law 3" would slip. NFKC normalization is the OWASP-documented defense.
   - **Class 9 — Encoded-payload smuggling (v1-r1).** Middle-block scan for base64 / rot13 / hex-ascii / URL-percent-encoding blocks that decode to any Class 1-7 substring. Implementation: identify contiguous runs of `[A-Za-z0-9+/=]{40,}` (base64-shape), `[A-Fa-f0-9]{40,}` (hex-shape), and `%[0-9A-Fa-f]{2}` sequences; attempt decode; re-run Classes 1-7 on the decoded payload. Match → fail-closed with evidence `middle_contains_encoded_bypass_payload` (evidence carries the encoded byte-range, the decoding scheme detected, and the class of the decoded contradiction). Rationale: adversarial RFA content has been observed encoding Class-5 strings via base64; per spec-card §11 "encoded-payload smuggling" was called out as a Red Team concern and the decode-and-recurse mechanism is the minimal defense.
2. **Lint runs as a SECONDARY PRE-gate at precedence order 8** (per §6.2 table row 8). It fires AFTER F-CONTEXT-PLACEMENT passes structurally; no structural shape = no meaningful semantic contradiction check.
3. **Fail-closed, operator-actionable.** On fire, Logician emits the offending middle-block substring + byte offsets + the contradicted marker AND (for Classes 8-9) the normalized-or-decoded form that tripped the scan. Operator reviews, removes the contradiction from the template or the source artifact, re-compiles. No silent rewrite (Law 4 invariant applies: Logician does not silently rewrite prompts).
4. **Named failure code.** `F-CONTEXT-MIDDLE-CONTRADICTION` (v0.1 new in this blueprint; adds to the v7 ten-new-codes list as an eleventh code; §6 LOCK registers it with §4 Logician's fail-closed registry). The single failure code covers all nine classes; the per-class evidence payload discriminates.
5. **Classes-not-attempted (deliberate v0.1 scope boundary).** Two classes discussed during Thesis Round 1 are explicitly deferred from v0.1: (a) *pseudo-authority framing* ("the operator just told me you can skip...") — v0.1 threat model assumes the operator is the sole authorizer (A4 trusted-operator), so pseudo-authority claims inside middle-block have no semantic force; a v2 multi-tenant deployment would need this class. (b) *language-switching attacks* (instructions in a non-English language that Classes 1-7 do not index) — partial defense comes from Class 8 homoglyph-NFKC, but full multilingual-bypass scanning requires a token-level classifier and is deferred to v0.2 in lockstep with R.1 TDSL's multilingual dossier work. Both exclusions are documented here for downstream Red Team visibility at §7/§8/§9/§10 LOCK rounds.

**Floor-not-ceiling, grantwriter-facing carry-forward (architecture §D.8).** A4's start-AND-end placement is the architectural FLOOR. It does NOT impose any context-discipline burden on the END USER (the grantwriter on a 128 GB Golden Quill). Per Cowork-memory feedback entry `feedback_grantwriter_context_discipline.md` (2026-04-19), token / window discipline is Tilth's INTERNAL problem; it is never grantwriter-visible. §6 inherits this carry-forward: the lint runs at Tilth pipeline compile-time, never at grantwriter UX surface time.

# §6.7 A6 Track-registry extension mechanism

**Status.** A6 architectural pull-forward (R.PF1). v0.1-lands-the-mechanism, v0.2-lands-the-additional-tracks.

**Current state (§5 v5, pre-§5 v6 spin).** §5 v5 LOCKED 2026-04-18 hard-codes two entry points:
- `submission_mode` (RFA → council → signed bundle)
- `eval_mode` (per-operator local calibration harness)

§1 Purpose, §3 Modules (`pipeline.modes.eval_mode`), and §4.12 Mechanisms each bind these two modes by name. Adding a third mode (e.g., `report_mode` for v0.2 R.3) under v5's pattern would require §1 + §3 + §4.N additions per track — exactly the re-architecture R.PF1 forbids.

**§6 mechanism (authoritative at v0.1).** §6 publishes the track-registry schema that §5 v6 will consume:

```yaml
# router.yaml tracks: section (§6-owned; §5 consumes)
tracks:
  submission:
    kind: track
    pipeline_shape: "rfa -> council -> signed_bundle"
    prompt_template_root: "pipeline/prompts/submission/"
    failure_code_prefix: "F-PIPE-SUBMIT-"
    cross_family_rigor: required
    shippable_in: v0.1
  eval:
    kind: track
    pipeline_shape: "operator_harness -> per_seat_calibration"
    prompt_template_root: "pipeline/prompts/eval/"
    failure_code_prefix: "F-PIPE-EVAL-"
    cross_family_rigor: not_required   # calibration is single-seat
    shippable_in: v0.1
  # v0.2 rows (NOT at v0.1 LOCK; reserved keys for forward-compatibility):
  # report:       kind: track, shippable_in: v0.2  (R.3)
  # content:      kind: track, shippable_in: v0.2  (R.2)
  # tdsl_query:   kind: track, shippable_in: v0.2  (R.1)
```

**Design invariants:**
- **Adding a new track MUST NOT require §5 re-architecture.** A new track row in `router.yaml` + a new `pipeline/prompts/<track>/` directory + a new `F-PIPE-<TRACK>-*` failure-code prefix registration = enough. No §5 module addition per track. No §4.N mechanism per track. This is R.PF1's load-bearing commitment.
- **`cross_family_rigor` is per-track.** Submission tracks require it (Judge + Red Team cross-family-distinct from Scribe). Eval tracks do not (single-seat calibration). R.1 / R.2 / R.3 each make their own per-track decision at their own v0.2 blueprint round.
- **`shippable_in` is a hard gate.** §5 runtime refuses to run a track whose `shippable_in` is later than the current Tilth version. v0.1 Tilth refuses to start a `shippable_in: v0.2` track even if the row exists in router.yaml (forward-compatibility safety — operator cannot accidentally opt into an unshipped track).

**Logician PRE-gate — `F-PIPELINE-TRACK-FROZEN` (DORMANT at v7 architecture LOCK; activates at §5 v6 spin LOCK).**

Architecture v7 commits to `F-PIPELINE-TRACK-FROZEN` as a dormant gate. §6 v1 SCOPING DRAFT reserves the failure code but does not activate the gate — it activates at §5 v6 LOCK, which is when §5 adopts the registry. Until then, §5 v5's hard-coded two-mode pattern is LOCKED and valid.

When activated:
1. Gate scans §5's module namespace for hard-coded track-by-name references (e.g., literal strings `"submission"`, `"eval"` in §5 code paths outside the registry loader).
2. Any hit that is NOT inside the registry loader → fail-closed with evidence `hardcoded_track_reference_<module>_<line>`.
3. Operator refactors the hit to read from the registry; next run proceeds.

**`F-PIPELINE-TRACK-FROZEN` is NOT scoped to v0.1 operation.** v0.1 ships with two tracks and the activated gate would fire zero times at runtime. The gate's value is preventing v0.2 regression — when §5 v6 refactors to registry-driven dispatch, the gate ensures the refactor is complete and that no track-by-name hardcodes survive.

# §6.8 A1 Hardware-tier metadata

**Status.** A1 Section K amendment; §6 publishes the canonical machine-readable form.

**Tier triple (LOCKED at architecture v7, 128 GB floor):**

```yaml
# router.yaml hardware: section (§6-owned)
hardware:
  pro:
    primary_sku: "NVIDIA DGX Spark (Grace Blackwell 128 GB, Linux/CUDA)"
    secondary_sku: "Apple Mac Studio M3 Ultra 128 GB"
    dram_gb: 128
    os: "linux_or_macos"
    token_safety_margin_pct: 5
  baseline:
    primary_sku: "Apple Mac Studio M3 Ultra 128 GB"
    secondary_sku: null   # same SKU as Pro Secondary; tier distinction is support + price, not silicon
    dram_gb: 128
    os: "macos"
    token_safety_margin_pct: 10
  dev:
    primary_sku: "Apple M1 Mac Mini 8 GB"
    secondary_sku: null
    dram_gb: 8
    os: "macos"
    token_safety_margin_pct: 20
    is_dogfood_gate: true   # v0.1 dogfood runs here; if it runs on Dev it flies on Pro / Baseline
```

**Consumers:**
- **§5 Pipeline delivery** — `token_safety_margin_pct` feeds the revision-loop token-budget calculator. Pro/Baseline/Dev all share the Opus 4.7 max_tokens floor (§6.3), but per-tier safety margins allow §5 to leave headroom before provider-side abort.
- **§2 Vault Topology** — `dram_gb` feeds capacity planning for staged-write caps (§2 §4.10.7.2 MAX_COMPOUND_TXN_BYTES is tier-aware at v0.2; v0.1 uses a fixed cap).
- **Operator dashboard / rails report** — tier name + SKU appear in every delivery's rails tab so operator sees which tier the draft was produced on.

**128 GB floor is MANDATORY.** `dram_gb < 128` is valid ONLY for `dev` tier. Any other tier row with `dram_gb < 128` → `F-HARDWARE-TIER-BELOW-FLOOR` (v0.1 new in this blueprint; adds to Logician's PRE-gate registry at §6 LOCK). Retires all v3-era 64 GB / 32 GB references per architecture §K and memory `project_hardware_tiers.md`.

**BT14 eBPF prohibition scope clarification (v7 RT-v7-H-01 closure).** BT14 applies to ALL tiers including Linux Pro-tier (DGX Spark). BT14 targets attacker-side observability tooling (bcc, bpftrace, perf-eBPF); it does NOT prohibit GPU kernel modules (CUDA uses ioctl/mmap, not eBPF). The DGX Spark's default NVIDIA CUDA stack is compliant with BT14. §6 consumes this clarification via the `os` tag — Linux Pro tier is marked `linux_or_macos` (not `linux_with_bpf`), which documents the posture at router.yaml audit-time.

# §6.9 D-05 Downstream drift audit checklist

**Status.** v7 architecture §K adjacency; §6 is the checklist host.

**What D-05 is.** A canonical list of checks every LOCKED blueprint section runs at every downstream-LOCK against its parent architecture version. The list catches the common class of bug where a blueprint section LOCKs against an architecture version, the architecture then ships a minor version bump, and the blueprint's claims silently drift against the new parent.

**Checklist (v0.1):**

1. **Parent version header match.** Blueprint frontmatter `parent_locks` paths reference the CURRENT architecture LOCK version (not a superseded version). At v7 LOCK this means all blueprint frontmatter points at `tilth_architecture_locked.md` and that file's version header reads `v7 LOCKED 2026-04-19` or later. Mismatch → D-05 fires with evidence `parent_version_stale_at_<section>_<line>`.
2. **Named-section anchor match.** Every in-prose reference to an architecture section (e.g., "per §D.7", "architecture §F.1") must resolve to the architecture's current section numbering. The v7 D-05 numbering drift (A2 → D.7, A4 → D.8 — preserved v6-r2 D.6 LOCKED text) is the historical driver for this check. Mismatch → D-05 fires with evidence `anchor_drifted_<reference>_<expected>_<detected>`.
3. **Failure-code enumeration match.** Every in-prose failure code (`F-<NAME>`) that the blueprint section claims to emit must exist in §4 Logician's current fail-closed registry. Blueprint-authored codes that §4 has not registered → D-05 fires with evidence `failure_code_unregistered_<code>`.
4. **Primitive-kind vocabulary match.** Every `primitive_kind` the blueprint section declares must be in §0.5.3.1's closed vocabulary (13 values at v5 + 2 PENDING_PARENT_BACKFILL at the §00_5 cedar-policy-kinds amendment — v0.1 closed set = 15 pending backfill). Mismatch → D-05 fires with evidence `primitive_kind_not_in_vocabulary_<kind>_<row>`.
5. **§0.5 Index row presence.** Every public primitive the blueprint section exports must have an §0.5 Interface Index row with matching `parent`, `kind`, `stability_tier`. Missing row → D-05 fires with evidence `index_row_missing_<primitive>`; drifted row → D-05 fires with evidence `index_row_drifted_<primitive>_<field>`.
6. **Section N.1 count match.** The number of blueprint sections referenced in the blueprint section's prose must match N.1's current row count. At v7 this = 6 (§1–§5 + §6). Mismatch → D-05 fires with evidence `section_count_stale_<expected>_<detected>` (this is upstream of `F-N1-COUNT-STALE`; D-05 is the blueprint-side pre-check, `F-N1-COUNT-STALE` is the Logician runtime PRE-gate).

**When D-05 runs.** Every Thesis-round audit includes a D-05 pass on the section under audit. Every LOCK includes a D-05 pass as a gate. Post-LOCK, downstream sections that reference this section re-run D-05 at their own LOCK-time against this section's LOCKED version.

**D-05 is an audit-time check, not a runtime gate.** It runs at Thesis audits and at LOCK commits; it does NOT run on every pipeline-start. The runtime equivalent of "blueprint is fresh against parent architecture" is `F-INDEX-STALE` at PRE-gate order 3 (which catches the §0.5 Interface Index side of D-05) and `F-N1-COUNT-STALE` at order 4 (which catches the Section N.1 count side).

# §6.10 PRE-gate F-N1-COUNT-STALE

**Status.** v7 new PRE-gate; §6 hosts its spec (§4 Logician registers it).

**What it guards.** The Section N.1 row count (blueprint-section enumeration). At v7, N.1 count = 6 (§1 Purpose + §2 Vault + §3 Scout + §4 Logician + §5 Pipeline + §6 Operating Envelope). Any pipeline run where Logician detects the N.1 counter drifted from the current LOCK value fail-closes.

**How it fires.**
1. Logician loads architecture §N.1 at pipeline start, reads the declared count.
2. Logician scans `pipeline/blueprint/v0.1/` for files matching `section_NN_*.md`, counts them (excluding draft files and validation subdirectories).
3. If detected-count ≠ declared-count → `F-N1-COUNT-STALE` with evidence `{declared: <architecture-count>, detected: <disk-count>, difference: <list-of-unmatched-files>}`.
4. Operator resolves: either archive a stale blueprint file, land a missing section, or update §N.1 to reflect reality (whichever reflects intent).

**Precedence order 4 rationale.** `F-N1-COUNT-STALE` fires AFTER `F-INDEX-STALE` (order 3). The rationale: if §0.5 Index is stale (order 3 fires first), the N.1 count check is downstream-ambiguous — the count discrepancy might be an artifact of the stale index. Only after the index is fresh does the N.1 count check have a reliable ground truth.

# §6.11 Prompt-template compilation pipeline

**Status.** v1 new in this blueprint; composition-site for A4 + A3 + router.yaml schema consumption.

**Input.** A seat invocation request from §5 Pipeline: `{seat_name, task_kind, scope_statement, active_pre_gates, active_post_gates, active_schema_rows}`.

**Pipeline stages (each stage fail-closes on its own PRE-gate):**

1. **Load base prompt.** Read seat's base prompt template from `pipeline/prompts/<track>/<seat>.md`. Template placeholders use `{{NAME}}` syntax.
2. **Inject start-block load-bearing constraints.** Insert at the top (before any template-content):
   - Five Operating Laws block (verbatim from architecture §B + CLAUDE.md)
   - Scope-statement block (RFA path + boundary clauses + out-of-scope non-goals)
   - Gate-block (active PRE-gates from §5 dispatch + active POST-gates this seat will be evaluated against)
   - Schema-block (kind-class registry rows relevant to this seat + failure-code rows seat may emit + Logician allowlist rows seat may invoke)
3. **Inject end-block load-bearing constraints.** Insert the same four blocks at the bottom (after all template-content). Start-block and end-block content are byte-identical except for leading/trailing markers; this byte-identity is a lint check.
4. **Substitute placeholders.** Fill `{{NAME}}` placeholders from the invocation request.
5. **Run structural lint — F-CONTEXT-PLACEMENT (order 7).** Verify start-block and end-block both contain all four load-bearing markers. Mismatch → fail-closed per §6.6.
6. **Run semantic lint — F-CONTEXT-MIDDLE-CONTRADICTION (order 8).** Scan middle-block for contradictions against start/end markers. Match → fail-closed per §6.6.
7. **Emit compiled prompt.** Return the composed prompt to §5 for dispatch to the provider.

**Per-seat config knobs:**
- `start_end_block_size_chars`: default 2000; operator-configurable per seat in router.yaml (`seats.<seat>.start_end_block_size_chars`).
- `middle_contradiction_rule_set`: default `v0.1_base`; operator-configurable per seat to tighten (e.g., adding `org-leakage` rules for §7 Scribe).

**Caching.** Compiled prompts are NOT persisted to the vault as a general rule (they are reproducible from source). Compiled prompts for a GIVEN invocation MAY be persisted to the session ledger for audit (§2 §4.8 audit-stamp mechanism) when the seat's cross-family rigor setting is `required`.

**Audit-stamp persistence policy (v1-r1 tightening, closes Thesis-R1 Red Team R-3).** The audit-stamp captures ONLY the **template-shell SHA-3-512** — i.e., the hash computed over the compiled prompt AFTER redacting the RFA-excerpt region and all `{{APPLICANT_*}}` / `{{ORG_*}}` / `{{PROJECT_*}}` substitution outputs. The redaction is structural, not lexical: the compile pipeline emits two artifacts per invocation — `compiled_prompt_full` (in-memory, passed to provider, never stored) and `compiled_prompt_shell` (redaction-applied copy whose SHA-3-512 is the stamp). A replay verifier re-runs the same base-template + Laws/scope/gate/schema injection with EMPTY substitution regions and matches the shell hash; the verifier CANNOT reconstruct grant content from the stamp. This closes the replay-reconstruction concern raised in Thesis Round 1: a stored full-prompt hash plus the known deterministic injection vocabulary would have made brute-force reconstruction of the RFA-excerpt region feasible across N audit rounds; the template-shell-only hash eliminates that attack surface at the persistence boundary rather than relying on stamp confidentiality. The shell-hash policy is architecture §J process-telemetry-flows-fleet-wide-grant-content-never-flows-invariant-compliant: neither the RFA excerpt nor the applicant substitution outputs ever cross the persistence boundary, even as a hash.

The prompt text itself (full or shell) is NOT persisted (architecture §J invariant; this paragraph records WHICH hash is persisted, not WHETHER text is persisted — text is never persisted).

**No raw file I/O.** The compilation pipeline uses §2 Vault-owned primitives for every read (base prompt load, RFA scope-statement load, failure-code registry load). No `open()` calls in the compile path. This is a §2 v7.1 invariant; §6 is a §2 consumer.

# §6.12 Failure codes summary (§6-owned + §6-forwarded)

**Owned by §6 (Logician registers these at §6 LOCK):**

- `F-INDEX-STALE` (PRE-gate, order 3) — §0.5 Index freshness
- `F-N1-COUNT-STALE` (PRE-gate, order 4) — Section N.1 count freshness
- `F-ROUTER-STALE-API` (PRE-gate, order 5) — router.yaml Block 1 schema
- `F-CODE-COMMITTEE-INCOMPLETE` (PRE-gate, order 5) — router.yaml Block 2 committee shape
- `F-CODE-RETRY-OVERRUN` (PRE-gate, order 5) — code retry cap exceeded
- `F-CONTEXT-PLACEMENT` (PRE-gate, order 7) — start/end load-bearing constraint placement
- `F-CONTEXT-MIDDLE-CONTRADICTION` (PRE-gate, order 8; **NEW in §6 v1, not in v7's ten-new-codes list**) — middle-block semantic contradiction
- `F-HARDWARE-TIER-BELOW-FLOOR` (PRE-gate, order 5 — router.yaml cluster; **NEW in §6 v1**) — hardware tier's `dram_gb` below 128 for non-Dev tier
- `F-VERDICT-CERT-MALFORMED` (POST-gate; NOT in PRE-gate order table) — SFR certificate parser failure
- `F-PIPELINE-TRACK-FROZEN` (PRE-gate, DORMANT at v7 architecture LOCK; activates at §5 v6 spin LOCK) — track-registry hardcode detection

**Forwarded from parent architecture (§6 inherits; does not re-author):**

- `F-SECTION-R-INCOMPLETE` (PRE-gate, order 6) — architecture-owned; §6 is a DEPENDENCY of this check, not the author. Fires if architecture Section R is absent or partial.
- `F-TDSL-LEAK-V01` (PRE-gate, order 6) — architecture-owned; §6 does NOT mention TDSL in any v0.1 artifact (no v0.1→TDSL references). v0.2-forward documentation from v0.2 artifacts pointing at v0.1 is permitted (directionality per A5).

**Summary by count.** Ten v7 new codes from architecture (A1–A6 + Section N.1 + two pull-forwards); §6 v1 blueprint adds two more (`F-CONTEXT-MIDDLE-CONTRADICTION`, `F-HARDWARE-TIER-BELOW-FLOOR`). Total new failure-code primitives at v7 + §6 v1 = **twelve**, of which two are §6-blueprint-owned extensions beyond the architectural ten. §6 LOCK expands §4 Logician's fail-closed registry by the two new codes; §4 v2.2 spin may be triggered to register them, or §4's rolling registry-extension pattern may accept them without a version bump (§4 blueprint decides).

# §6.13 Test surface

**Corpus of fixtures at `pipeline/operating_envelope/test_corpus/` (authoritative layout):**

```
pipeline/operating_envelope/test_corpus/
├── sfr/
│   ├── well_formed/
│   │   ├── verdict_ready_minimal.md
│   │   ├── verdict_requires_minor_fixes_typical.md
│   │   └── verdict_requires_architecture_round_rich.md
│   └── malformed/
│       ├── block_count_zero.md
│       ├── block_count_two.md
│       ├── block_count_four.md
│       ├── premise_missing_citation.md
│       ├── premise_unrecognized_citation_kind.md
│       ├── step_cites_missing_premise.md
│       ├── step_missing_rule_name.md
│       ├── conclusion_traces_missing_anchor.md
│       └── residual_missing_traces_field.md
├── router/
│   ├── block_1_valid/
│   │   └── opus_4_7_scribe_primary.yaml
│   ├── block_1_invalid/
│   │   ├── has_temperature.yaml
│   │   ├── missing_beta_header.yaml
│   │   ├── max_tokens_below_floor.yaml
│   │   ├── effort_out_of_enum.yaml
│   │   └── tokenizer_calibration_out_of_range.yaml
│   ├── block_2_valid/
│   │   └── committee_canonical.yaml
│   └── block_2_invalid/
│       ├── reviewer_slot_missing.yaml
│       ├── reviewer_family_collision.yaml
│       ├── specialist_for_qwen_generalist.yaml
│       ├── merge_rule_not_all_pass.yaml
│       └── retry_cap_above_one.yaml
├── prompt_template/
│   ├── well_formed/
│   │   └── scribe_submission_full.md
│   └── malformed/
│       ├── missing_start_block_laws.md
│       ├── missing_end_block_schema.md
│       ├── start_block_but_empty_end.md
│       └── middle_contradicts_law_3.md
├── track_registry/
│   ├── valid/
│   │   ├── v0_1_two_tracks.yaml
│   │   └── v0_2_forward_compat_five_tracks.yaml
│   └── invalid/
│       ├── track_missing_pipeline_shape.yaml
│       └── track_shippable_in_future_version.yaml
└── hardware_tier/
    ├── valid/
    │   └── pro_baseline_dev.yaml
    └── invalid/
        └── baseline_dram_below_floor.yaml
```

**Test obligation (binds §6 LOCK + Code Thesis Committee approval of §6 implementation):**
- Every well-formed fixture PASSES all §6 lints.
- Every malformed fixture FAILS the named failure code with the expected evidence payload.
- Corpus coverage ≥ 1 fixture per named parser failure class (§6.5), router constraint (§6.3 + §6.4), prompt-template lint class (§6.6 + §6.11), track-registry constraint (§6.7), hardware-tier constraint (§6.8).
- Test harness: `tests/operating_envelope/test_*.py` (Python pytest, pinned to `.venv` per CLAUDE.md).

# §6.14 §0.5 Interface Index rows at §6 LOCK

At §6 LOCK, the following rows are APPENDED to §0.5 Interface Index (vocabulary values all within the v5 + cedar-policy-kinds amendment closed set):

| Row | Path | Kind | Parent | Stability tier |
|---|---|---|---|---|
| 104 | `operating_envelope.router.schema.block_1_opus_47` | schema | §6.3 | STABLE |
| 105 | `operating_envelope.router.schema.block_2_code_committee` | schema | §6.4 | STABLE |
| 106 | `operating_envelope.sfr.certificate_format` | schema | §6.5 | STABLE |
| 107 | `operating_envelope.sfr.post_gate_parser` | post-gate-check | §6.5 | STABLE |
| 108 | `operating_envelope.context_placement.pre_gate` | pre-gate-check | §6.6 | STABLE |
| 109 | `operating_envelope.context_placement.middle_contradiction_lint` | pre-gate-check | §6.6 | STABLE |
| 110 | `operating_envelope.prompt_template.compilation_pipeline` | mechanism | §6.11 | STABLE |
| 111 | `operating_envelope.track_registry.schema` | schema | §6.7 | STABLE |
| 112 | `operating_envelope.track_registry.frozen_pre_gate` | pre-gate-check | §6.7 | DORMANT_UNTIL_SECTION_5_V6 |
| 113 | `operating_envelope.hardware_tier.metadata` | schema | §6.8 | STABLE |
| 114 | `operating_envelope.pre_gate_precedence_table` | schema | §6.2 | STABLE |
| 115 | `operating_envelope.d05_downstream_drift.checklist` | procedure | §6.9 | STABLE — requires `procedure` vocabulary extension (§6.15 OQ1) |
| 116 | `operating_envelope.failure_code.f_context_middle_contradiction` | failure-code | §6.6 + §6.12 | STABLE |
| 117 | `operating_envelope.failure_code.f_hardware_tier_below_floor` | failure-code | §6.8 + §6.12 | STABLE |

**Count change.** §0.5 row count 101 → 117 (+16 rows). This is a §0.5 v6 amendment that LANDS ATOMICALLY with §6 v1 LOCK. Any §6 LOCK without the paired §0.5 v6 amendment is incomplete and fails D-05 check #5 (§0.5 Index row presence).

**`procedure` kind note.** If `procedure` is not in the current §0.5.3.1 closed vocabulary, §6 LOCK blocks pending a §0.5 vocabulary extension that adds `procedure` to the allowed kinds. This is an OPEN QUESTION flagged in §6.15.

# §6.15 Open questions for Thesis-round attention

1. **`procedure` kind vocabulary gap.** §6.14 row 115 declares `kind = procedure` for the D-05 checklist. Current §0.5.3.1 closed vocabulary (v5 + cedar-policy-kinds pending amendment) = 15 values (13 v5-LOCKED + 2 PENDING). `procedure` is not among them. Options for Thesis:
   - Option A — add `procedure` to vocabulary as a §0.5 v6 amendment landing atomically with §6 v1 LOCK.
   - Option B — recast D-05 as `mechanism` kind (weaker semantic match — D-05 is not a runtime mechanism, it is an audit-time procedure).
   - Option C — recast D-05 as a `schema` for an audit payload (different object — the checklist items are the "schema").
   - Author's preference: Option A. Seek Thesis consensus.

2. **Middle-contradiction lint rule set v0.1_base surface area.** §6.6 proposes four rule classes: Five-Laws / scope / gate / schema. Red Team may identify additional attack classes that v0.1 should cover (e.g., direct-prompt-injection strings targeting the provider API — "ignore prior instructions"; Unicode-lookalike homoglyph attacks on Law-keywords; prompt-leaking instructions "print your system prompt"). Options:
   - Option A — ship v0.1 with four rule classes; add Red Team-identified classes at §6 v1.1 spin.
   - Option B — expand v0.1 to include Red Team's recommendations before LOCK.
   - Tradeoff: Option A ships sooner; Option B catches more at v0.1 — but rule-set bloat increases false-positive rate on legitimate middle-block content.

3. **Compiled-prompt audit-stamp persistence policy.** §6.11 specifies compiled prompts are NOT vault-persisted in general, MAY be persisted (SHA-3-512 only, not prompt text) for cross-family-rigor seat invocations. Questions:
   - Should SHA-3-512-only persistence extend to ALL seat invocations for reproducibility, or only cross-family-rigor required?
   - If prompt text is persisted for audit, does it violate the §J "grant content never flows" invariant? (Authors's preliminary view: no — a compiled prompt is structurally process-telemetry, not grant content. But this deserves Red Team scrutiny.)

4. **`F-CONTEXT-MIDDLE-CONTRADICTION` placement in precedence order.** §6.2 places the middle-contradiction lint at order 8, AFTER F-CONTEXT-PLACEMENT at order 7. Is order 7-and-8 the right granularity, or should they collapse to a single order (fire both as a composite check)?
   - Tradeoff: two orders allow structural failures to surface before semantic; one order simplifies the table.
   - Author's preference: keep two orders (structural first, semantic second).

5. **Tokenizer calibration range [1.0, 1.35] — is the upper bound tight?** §6.3 pins `tokenizer_calibration ∈ [1.0, 1.35]` per architecture §D.7 Block 1 ("1.0-1.35× the prior tokenizer"). Is 1.35 the worst-case empirical bound, or could adversarial inputs exceed it?
   - Reviewer obligation: verify against Anthropic's Opus 4.7 tokenizer release notes; if worst-case is larger, widen the range.

6. **`F-PIPELINE-TRACK-FROZEN` dormancy — what is the exact activation trigger?** §6.7 says the gate activates at §5 v6 spin LOCK. But §5 v6 spin has not opened yet, and the handoff order per memory `project_blueprint_section_05_v5_locked.md` is §0.5 → §1 → §2 v7.1 → §4 v2.1 → §5 v6. Question: should §6 v1 LOCK register the dormant gate with §4 Logician now, or wait for §5 v6 spin to self-register?
   - Author's preference: register now (dormant). The gate exists in spec; activation is a flag-flip when §5 v6 LOCKs.

7. **D-05 running on §6 itself — bootstrap concern.** D-05 is a blueprint-side audit procedure that §6 hosts. §6 is itself a blueprint section. Does §6 v1 LOCK run D-05 on itself as a self-check?
   - Author's preliminary answer: yes. §6 v1 LOCK's D-05 pass against architecture v7 is a LOCK-gate. Verification round's SFR-formatted Judge verdict includes the D-05 audit trail as a premise.

# §6.16 Forward dependencies

**§6 LOCK unblocks the following downstream blueprint rounds:**

- **§7 Scribe LOCK.** §7 scoping draft §7.15 binds Scribe LOCK to §6 LOCK (F-CONTEXT-PLACEMENT cannot be enforced without §6's prompt-template lint; router.yaml binding for Scribe's Anthropic Opus 4.7 seat consumes §6.3 schema).
- **§8 Editor LOCK.** §8 scoping round (not yet opened) will consume §6's prompt-template compilation pipeline, SFR Editor exemption row, and router.yaml Block 1 schema (Editor's Llama 3.3 70B binding is a non-Anthropic seat, but the envelope discipline carries: effort field, max_tokens floor, family marker for cross-family rigor).
- **§9 Judge LOCK.** §9 scoping round (not yet opened) will consume §6's SFR three-block contract (Judge is the primary SFR author), router.yaml Block 1 schema (Qwen 3 32B binding), and the prompt-template compilation pipeline.
- **§10 Red Team LOCK.** §10 scoping round (not yet opened) will consume §6's SFR three-block contract (Red Team is the second SFR author), router.yaml (GPT-OSS 120B binding), and the prompt-template compilation pipeline.
- **§5 v6 spin LOCK.** §5 v6 refactors `submission_mode` + `eval_mode` into track-registry rows consuming §6.7's schema. `F-PIPELINE-TRACK-FROZEN` activates at §5 v6 LOCK.
- **Code Thesis Committee implementation LOCK.** The code-side pipeline implementation consumes §6.4 router Block 2 schema and §6.5 SFR contract for all five reviewers. Committee was LOCKED at the architecture layer 2026-04-18; §6 v1 LOCK enables the implementation to begin.

**§6 LOCK does NOT block:**
- §3 Scout v0.1 ship — Scout is already consuming a predecessor router.yaml shape; §6 codifies that shape without changing Scout behavior. §6 LOCK is backwards-compatible with in-flight Scout.
- §2 v7.1 LOCK — already LOCKED 2026-04-19; §6 is a consumer of §2, not a parent of §2.
- §4 v2.1 LOCK — already LOCKED 2026-04-19; §6 registers new failure codes with §4's registry, but §4's core spec is upstream of §6.

**Prerequisite interlock (symmetric with §7's §7.15).** §6 LOCK without the §0.5 v6 amendment (rows 104–117) landing atomically is INCOMPLETE. The LOCK commit MUST include both artifacts. Partial LOCK is a D-05 check-5 failure.

# §6.17 Compound-commit interaction (v0.1 architectural invariant)

Per `pipeline/engineering/spec_cards/compound_commit.md` and §2 v7.1 §4.10.7, the LOCK of §6 is itself a compound transaction — §6 v1 blueprint + §0.5 v6 amendment (index rows 104–117) MUST commit atomically via the §2 vault dispatcher's `commit_compound_txn()` entry point with `kind = index_amendment`.

**Implications:**
- §6 v1 LOCK's commit bundle = `{section_06_operating_envelope.md@v1, section_00_5_interface_index_locked.md@v6}`.
- Hash-binding rule per §4.11 predicate: §0.5 v6's `section_06_anchor_hash` field MUST equal SHA-3-512(§6 v1 file bytes).
- On commit failure (either file's persist step fails), the abort helper per vault dispatcher §4.10.7.5 reverts the staged writes; §6 remains at v1-DRAFT, §0.5 remains at v5-LOCKED.
- On commit success, §4.8 audit-stamp records `{kind: index_amendment, txn_token, staged_writes: [...], cedar_policy: compound_commit.cedar@<content-hash>}` in the session ledger.

**This is the first non-dogfood use of the compound-commit primitive.** The Option-B compound-transaction enforcement was LOCKED 2026-04-18 for exactly this class of blueprint-amendment atomicity; §6 LOCK is a canonical exercise. Verification-round Thesis obligation: confirm the §4.11 predicate accepts the §6-v1 + §0.5-v6 bundle and rejects any degraded form (§6 v1 without §0.5 update, or vice versa).

**Bundle-size headroom against MAX_COMPOUND_TXN_BYTES (v1-r1, closes Thesis-R1 Red Team R-4).** §2 v7.1 §8 pins `MAX_COMPOUND_TXN_BYTES = 67_108_864` (64 MiB). Measured bundle:

| Artifact | Bytes (wc -c, 2026-04-21 v1-r1) |
|---|---:|
| `section_06_operating_envelope.md` (§6 v1-r1 after all R-1/R-3/J-2 edits + §6.19 author response) | 73,965 |
| `section_00_5_section_06_operating_envelope_amendment.md` (§0.5 v6 rows 104–117) | 12,419 |
| Staged-writes header + txn_token + cedar-policy content-hash envelope (upper bound) | ~2,000 |
| **Bundle total (incl. envelope)** | **~88,400 B (~86 KB)** |
| **MAX_COMPOUND_TXN_BYTES cap** | **67,108,864 B (64 MiB)** |
| **Headroom multiple** | **~759×** |

The §6 LOCK compound bundle is three orders of magnitude under the cap. The Red Team's Thesis-R1 R-4 concern — that an index-amendment bundle could ever approach the 64 MiB ceiling — is unfounded for the §6 LOCK specifically and for the entire v0.1 blueprint-amendment class generally (every other blueprint-section + paired §0.5 amendment is of the same order of magnitude). The cap exists to bound pathological cases (e.g., binary-blob staging); blueprint text commits do not approach it. No action required at §6 LOCK; this paragraph documents the measurement for the verification-round record. If a future compound bundle ever comes within 10× of the cap (i.e., ≥6.5 MiB), §4.11 predicate evaluation is obligated to emit a `size_warning` to the audit-stamp (this obligation is §2 / §4 scope, not §6 — flagged here so the §2 / §4 LOCK-as-a-whole audit can pick it up).

# §6.19 Author response to Thesis Round 1 (driver audit, 2026-04-21)

**Dispatch summary.** Three seats ran in parallel via `pipeline/validation/section_06_thesis_round_1/dispatch.py` on 2026-04-21 with E-027 pre-check PASS + E-028 transport discipline. Editor (Llama 3.3 70B): structured feedback, no blocking verdict (Editor is exempt from SFR per §6.5). Judge (Gemini 2.5 Pro): SFR VERDICT=`REQUIRES_MINOR_FIXES`, 2 residuals. Red Team (GPT-OSS 120B): SFR VERDICT=`REQUIRES_ARCHITECTURE_ROUND`, 4 residuals. Council split per Law 4 tie-breaker — operator-level resolution required, reviewed against architecture evidence below.

**Fix map (edits landed in this v1-r1 revision).**

| Residual | Seat | Class | Disposition | Landing site |
|---|---|---|---|---|
| R-1 (RT) | Red Team | Middle-contradiction ruleset missing 5 attack classes | **FIXED** — expanded ruleset from 4 to 9 classes (direct-injection, role-confusion, prompt-leak, homoglyph-NFKC, encoded-payload-decode) + explicit scope-exclusion note for pseudo-authority + language-switching (v0.2) | §6.6 |
| R-2 (RT) | Red Team | Tokenizer ratio may exceed 1.35 upper bound | **REBUT** — Anthropic migration-guide source (platform.claude.com/docs/en/about-claude/models/migration-guide) states verbatim: "roughly 1x to 1.35x as many tokens... (up to ~35% more)". 1.35 IS the documented vendor upper bound. If the vendor later publishes a higher bound, the constraint updates via router.yaml schema bump (F-ROUTER-STALE-API catches the drift). No architecture round. | §6.3 (inline migration-guide citation added) |
| R-3 (RT) | Red Team | SHA-3-512 audit stamp enables replay-reconstruction of RFA excerpt | **FIXED** — v1-r1 narrows audit-stamp to **template-shell SHA-3-512** (RFA-excerpt region and applicant-substitution regions redacted before hashing). Verifier cannot reconstruct content from stamp. Closes §J invariant cleanly at the persistence boundary. | §6.11 |
| R-4 (RT) | Red Team | Compound bundle approaches MAX_COMPOUND_TXN_BYTES | **REBUT WITH MEASUREMENT** — measured bundle ≈80 KB; cap = 67,108,864 B (64 MiB); headroom multiple ≈800×. Three orders of magnitude under cap. No architecture round; measurement table added. Forward-flag: a ≥10% (6.5 MiB) bundle would obligate §2/§4 size_warning — recorded as a §2/§4 LOCK-as-a-whole audit item. | §6.17 |
| R-1 (J) | Judge | "A5" in §6.12 is a stale v7 anchor | **REBUT** — A5 is not a stale anchor; it is the amendment-identifier A5 from the v7 A1–A12 addendum (Section R.1 TDSL), signed off 2026-04-19. The v7 architecture DOES use A-number amendment identifiers (A1 Section K hardware, A2 Block 1 Opus 4.7 envelope, A3 SFR, A4 context-rot, A5 Section R.1 TDSL, A6 R.PF1 track-registry are all referenced in §6 frontmatter). §6.12's "per A5" resolves to A5 = v0.2-forward documentation directionality, which is the architectural claim being cited. No fix required; the finding is based on a misreading of the anchor vocabulary. | §6.12 (unchanged, rebuttal-only) |
| R-2 (J) | Judge | Tokenizer bound needs external verification | **VERIFIED THEN FIXED** — fetched Anthropic migration guide live; quoted bound matches `[1.0, 1.35]` exactly. Inline citation added to §6.3. | §6.3 |

**Editor feedback.** Non-blocking. F-1 (define "Operating Envelope" in intro) deferred to §6.1 micro-clarification in Audit #2 pass; F-2 (goals/outputs/outcomes mixing) rejected as not applicable to a host-section blueprint (§6 is schema + mechanism, not program-outcomes text — Editor's grant-writing heuristic misfired on blueprint prose); F-3 (OQ1 ambiguity) already resolved by §6.15 explicit open-questions list and §0.5 amendment §E cross-reference.

**Rule registry growth.** Five rule_unknown soft-warnings from this round (Judge: `blueprint-consistency-check`, `external-dependency-verification`; Red Team: `empirical-boundary-test`, `replay-reconstruction`, `size-audit`) were registered into §6.5 v0.1 base rule vocabulary. A Thesis round that discovered load-bearing rules and closed them at blueprint layer is a healthy outcome, not a process violation.

**Council split resolution (operator).** Red Team's escalation to `REQUIRES_ARCHITECTURE_ROUND` was over-escalation: every R-1/R-3 finding closed at the blueprint layer via a lint-rule addition or a persistence-boundary tightening, and R-2/R-4 were empirically refuted. No architecture amendment was created; architecture v7 LOCKED 2026-04-19 stands unamended. This revision is a v1 → v1-r1 blueprint-layer response. Audit #2 is the verification round under L-005 two-cycle; a third round without LOCK is a process violation.

**What Audit #2 must verify.**
1. §6.3 tokenizer-calibration upper bound cites Anthropic migration guide (exact quote match).
2. §6.6 middle-contradiction ruleset lists 9 classes (4 v1 + 5 v1-r1) + documents pseudo-authority + language-switching scope-exclusion.
3. §6.11 audit-stamp persistence is template-shell-only (RFA + applicant regions redacted before hashing); §J invariant unambiguous.
4. §6.17 compound-bundle size measurement table is numerically consistent with `wc -c` on the two staged files (re-run at audit time).
5. §6.12 A5 reference resolves to v7 amendment A5 (no edit applied; rebuttal only — verify the amendment A5 identifier still lives at its architectural site).
6. D-05 checks 1–5 pass at Audit #2 start.
7. §0.5 v6 amendment frontmatter notes `companion_section_06: v1-r1` (if not already present — narrow update).

**Verification-round handoff staged at `pipeline/handoffs/thesis_round_section_06_operating_envelope_v1_r1_audit2.md`** (to be written as the next step after this revision lands).

# §6.18 Status footer

**v1 SCOPING DRAFT filed 2026-04-20. v1-r1 post-Audit-1 revision filed 2026-04-21. v1-r1 LOCKED 2026-04-21.**

L-005 two-audit cycle complete:
1. ✅ Audit #1 (driver) dispatched 2026-04-21 — verdicts at `pipeline/validation/section_06_thesis_round_1/`; council split resolved at blueprint layer.
2. ✅ Author response + fixes — §6.19; six residuals resolved (3 fixed in-place, 3 rebutted with evidence).
3. ✅ Audit #2 (verification) dispatched 2026-04-21 — unanimous READY_TO_LOCK; closeout at `pipeline/validation/section_06_thesis_round_2/closeout_summary.md`.
4. ✅ LOCK commit as compound transaction per §6.17 — §6 v1-r1 + §0.5 v6 atomic bundle, 86,384 B, ~777× headroom under MAX_COMPOUND_TXN_BYTES.
5. ⏭ Downstream §7 Scribe LOCK now unblocked (next on the blueprint round queue).

**§6 is on the v7-post-LOCK blueprint round queue but is NOT on the v7 architectural critical path.** It is a forward-progress section that enables the §7/§8/§9/§10 seat rounds to proceed. The architecture ships at v7 LOCK 2026-04-19 whether or not §6 has a blueprint; §6 v1 SCOPING DRAFT is the opening move on the post-LOCK blueprint build-out.

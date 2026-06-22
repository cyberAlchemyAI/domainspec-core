# Lens B — Readiness / Integration attack (raw return)

- **Dispatch:** `2026-06-22-mtng-v2-review` · group `review-lenses` · agent **Capucci, Matteo** (skeptic)
- **anti_bias axis:** attack-vector — readiness/FIX-THEN-BUILD side
- **Verdict:** FIX-THEN-BUILD
- **Status:** integrated into `../REVIEW.md` (parent synthesis). Raw, unedited below.

> **Parent verification correction (P8 trust-but-verify):** F7 states "§22 has no … `contribution_hooks`."
> This is wrong — §22 `BranchNode` *does* list `contribution_hooks` (line 1189). The field genuinely
> absent from **both** §14 and §22 schemas is `merge_target` (named only in §5's prose node
> declaration). The rest of F7's schema-drift finding (output_artifact{type,path} vs
> output_artifact_type; `assigned_tool` in §22 not §14; §23 singular `validator` vs list)
> is confirmed against the spec. Severity unchanged.

---

# MTNG v2 — READINESS/INTEGRATION Red-Team (reviewer: Matteo Capucci)

Granting MTNG is worth building. The question is whether **this spec is safe to build as written**. It is not yet — but every defect below is a fixable precondition, not a kill reason.

### F1 — Phase 0 is a hard dependency the build order both requires and skips
**severity: blocker** · **§10, §24 Stage 0, §21, changelog "Remaining Gaps"**
§10 asserts seven ResonantOS systems and §24 Stage 0 makes integration mapping the *first* build step — yet the changelog admits Phase 0 "has not yet been performed." §10 poses open questions but supplies no answers; its inputs (the ResonantOS repo) are not in hand.
*Verification:* §10, §24 Stage 0, §21, `05` line 42; L0 honest cutoff; L1 R-INT "evidence-production blocker."
*Change request:* Before any code, either (a) execute Phase 0 against the real repo and append a mapping table (each §10 question → named component or "no analog"), or (b) declare V1 **fully standalone CLI**, zero ResonantOS coupling, and strike §10/§11 from the V1 critical path.

### F2 — Recombination has prose rules but no merge algorithm or conflict-detection
**severity: major** · **§17, §22 SynthesisArtifact**
§17 never defines: (1) what happens when a *required* node is failed/rejected/needs_human (allowed_results lists only passed/partial — block, or degrade?); (2) how a conflict is *detected* (the Conflict Rule fires an action with no triggering predicate); (3) precedence when nodes target the same section.
*Verification:* §17 (required_nodes allowed_results, no else-branch; Conflict Rule = action without predicate); L1 R-MRG PARTIAL; Analog6 §6.2.
*Change request:* Add (a) a required-node-unsatisfied rule (recommend emit with explicit `blocked: missing required node X`); (b) a concrete conflict-detection predicate; (c) a worked two-node conflict example; (d) a `conflicts[]` field on SynthesisArtifact.

### F3 — Pilot success criteria are unadjudicatable
**severity: major** · **§21, §25**
§21 criteria 1/2/8 are adjectives ("clearer," "more actionable," "acceptable overhead") with no metric/threshold/baseline/judge; no flat-summary baseline procedure is defined; §25 Test 2 asserts "no root cause without evidence" with no detector. A run cannot return PASS/FAIL.
*Verification:* §21 lines 1128-1139; §25; L1 R-VAL; ledger D6.
*Change request:* Pre-register: a fixed flat-summary baseline procedure, ≥1 quantitative metric per claim (e.g. validator recall on N seeded-missing-info fixtures, threshold stated), a named adjudicator, and the no-go threshold §27 Q8 poses but never answers.

### F4 — Engine accept/reject "policy" is undefined; authority boundary + audit actor fuzzy
**severity: major** · **§9, §10, §22 AuditEvent**
§9: the engine accepts/rejects proposals "according to policy" — no policy specified. Which of the six proposal types auto-accept vs escalate is open. For a standalone V1 there is no Guardian, so §10's "Guardian/maintainer approval path" has no actor. §22 `AuditEvent.actor_ref: string` can't distinguish engine-auto from human-approved.
*Verification:* §9 line 524; §10 line 598; §22; L1 R-AUT PARTIAL; ledger D1.
*Change request:* Specify a V1 acceptance policy table (per proposal type → auto-accept | validate-then-accept | queue-for-human). Recommend all six auto-accept into *run-local* state; memory candidates + future ingestion are write-only-to-review-queue. Constrain `actor_ref` to enum `{engine, operator, tool:<id>}`.

### F5 — Mode / Routing-Signature detection is substring-based with no accuracy measurement or method
**severity: major** · **§5, §13, §22 ModeProposal, §23**
Routing signatures are literal substrings; §22 `confidence: number` is unpopulated; §13 "one dominant mode" is undefined (no threshold/tie-break); §23 binds modes to validators but not to a detection method. With a single bounded reroute (§15), one misroute + one wrong reroute = stop.
*Verification:* §5 lines 200-216; §13 line 674; §22; L1 R-CLS; ledger D5; Analog6 §6.1, Gemini "Metaphor Trap."
*Change request:* Add a detection-method spec (signature→mode table + confidence rule + dominance/tie-break threshold) and a measurement obligation (labeled fixtures, reported precision/recall on branch-vs-fast-path) before the pilot is declared successful. State the misroute rate the single-reroute budget assumes.

### F6 — Per-signal overhead never estimated, yet a success criterion depends on it
**severity: minor** · **§21 #8, §9, §22**
§9 lists "budget limits" as engine-owned and §21 #8 requires "acceptable overhead," but there is no cost model, no budget schema, no RunProfile budget field. The thing the engine "owns" has no representation in §22.
*Change request:* Add a budget object to RunProfile (`max_tokens`, `max_llm_calls`, `max_wall_clock`) and a per-run overhead line in the audit log / validator report; produce a back-of-envelope estimate (calls = detect + Σnodes·(process+validate) + synthesis) before the pilot.

### F7 — OKF unverified/mis-named; schema inconsistencies across §14/§22/§23
**severity: minor** · **§20; §14 vs §22; §22 vs §23**
OKF: §20 says "Open Knowledge **Format**," Gemini says "**Framework**"; existence/owner/name unverified; Stage 5 commits to it against an unpinned target.
Schema drift: §14 uses `output_artifact:{type,path}`, `validator:[…]`, no `assigned_tool`; §22 uses flat `output_artifact_type`, `output_ref`, `assigned_tool`. §23 binds each mode to a singular `validator`; §14/§22 model `validator` as a list.
*(Parent correction: §22 **does** include `contribution_hooks`; the field absent from both schemas is `merge_target`.)*
*Verification:* §20 line 948 vs `07`/L0/ledger D2/C3; §14 lines 759-766 vs §22 lines 1183-1189; §23 lines 1238-1268; L1 R-OKF.
*Change request:* (1) Fetch and pin OKF; correct the name and freeze V1 type names, or strike OKF from Stage 5 until pinned. (2) Publish ONE canonical BranchNode schema referenced by §14/§22/§23; reconcile `validator` cardinality (recommend list everywhere); ensure `assigned_tool`/`merge_target`/`contribution_hooks` each appear exactly once.

## OVERALL VERDICT — **FIX-THEN-BUILD**
Every defect is a missing precondition or internal inconsistency, not a conceptual dead end; the v2 narrowing is sound. But shipping against the spec as written would bake in an unverified integration surface (F1), an unimplementable merge step (F2), an unfalsifiable pilot (F3), and contradictory node schemas (F7).
**Single most important precondition before any code:** Resolve F1 — execute Phase 0 against the real ResonantOS repo and publish the mapping table, or formally declare V1 a fully standalone CLI with zero coupling.

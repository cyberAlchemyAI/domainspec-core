# attacks.md — collected attacker + verifier returns (verbatim)

Dispatch: `2026-06-16-comparison-answer-review` · target: `target.md` · robot_talks group (3 attackers), initial + final positions preserved (P14).

---

## Ashby, W. Ross — GOVERNANCE-DERIVATION

### Initial position
Method: derived what each SKILL licenses, tested target claims as entailments. The two skills are peers under a shared register-dispatch/constitution stack (subagents-strategy is a ROUTER that "defines no field and no type-specific judgment"; dispatch-spec is a Formulae route-shape validator). Neither doc establishes a hierarchy. Findings:
- "two layers of the same pipeline … governs the PIPELINE … governs ONE STAGE inside that pipeline" (L33-42) — **MAJOR**: neither doc establishes a containment relation; nesting is the author's synthesis.
- "dispatch-spec is the outer contract, domainspec-subagents-strategy is the governed engine for one step in it" (L50) — **MAJOR**: converts peers into parent/child.
- "that handoff is precisely where domainspec-subagents-strategy takes over" (L44) — **MAJOR**: dispatch-spec L104-106 names "usually Refine" as orchestrator, not subagents-strategy.
- "governs … the governed engine" — **MINOR**: overclaims a self-described ROUTER (sub-strat L3).
- Accurate cells confirmed: "A router" table row (L22), P1 triggers gloss, 25 rules, human-gate contrast.
- (Initial validator path claim: `.claude/skills/dispatch-spec/scripts/validate-dispatch.py`.)

### Final position (after confront)
- takes-over/Refine: **escalated MAJOR → CRITICAL** ("merge with Quine"); verified L98-100 himself ("usually Refine").
- two-layers framing (F2) and outer-contract/governed-engine (part of F2): **HOLD MAJOR** — literal cites landing doesn't rescue the entailment.
- "governs/governed engine" overclaim: **HOLD MINOR**.
- **Conceded:** his validator path was wrong-form; corrected to `arcanum/formulae/...`. Owns the error.
- Convergence: "all three lenses independently land on the Refine-handoff sentence as the central defect … I do not dissent."

---

## Turing, Alan — LITERAL-EXECUTION

### Initial position
Opened the actual files. Findings:
- "returns pass/flag/block (L31-32)" — **MAJOR**: L31-32 is purpose/scope prose; pass/flag/block lives at L148 (Output Contract) and L166-169 (Failure Policy).
- "Formulae — a deterministic validator (L11-29)" — **MINOR**: tier at L11, but "Deterministic Validator" section is L56-68.
- validator path — **MINOR** (initial): claimed it was only under `arcanum/formulae/...`, not repo-root.
- "none inherent — it's a linter" — **MINOR**: omits Rule 22 (L93) `authorization=requires_user_permission`.
- Confirmed accurate: 25 rules (L72-96), L98-120, L1-4, L10, L17.

### Final position (after confront)
- Validator path **RESOLVED**: ran ls on both — `.claude/skills/dispatch-spec/scripts/validate-dispatch.py` AND `arcanum/formulae/dispatch-spec/scripts/validate-dispatch.py` BOTH exist, both 28.2K, byte-identical (runtime copy vs canonical source). **Path finding DOWNGRADED to NEGLIGIBLE** — the "Python validator" claim is true; either path is valid.
- L31-32 cite error: **HOLD MAJOR** (uncontested).
- takes-over/Refine: opened lines 97-99 ("does **not** execute subagents. The orchestrating capability, **usually Refine** …") — **CONFIRMS** as ground truth; "takes over" is the wrong verb (dispatch-spec never relinquishes control to a non-orchestrating capability).
- Convergence: confirms the Refine misattribution as severest; his L31-32 MAJOR stands uncontested.

---

## Quine, Willard Van Orman — REFERENCE-TRACING

### Initial position
Traced each cross-reference to its referent. Findings:
- "that handoff is precisely where domainspec-subagents-strategy takes over" (L44) — **CRITICAL** (initial): misattributed referent; dispatch-spec L104-106 names "usually Refine"; L98-120 proves only that a subagent_strategy block exists.
- L98-120 cite chained to the unsupported attribution — **MAJOR**.
- check-tension "quality mechanism" (L29) — **MINOR**: check-tension is a separate skill the router points to (sub-strat L56 Pointers), not owned; "owns no field and no type judgment" (check-tension L12).
- Verified accurate: research/review/experiment LIVE (L43/45/48), incl. RESERVED set.

### Final position (after confront)
- Severity: **CONCEDED CRITICAL → MAJOR** — CRITICAL is for "flatly contradicts governing law / corrupts a record"; the target is an explanatory answer, not a governing artifact. "Ashby's MAJOR is the honest call." (Note: Ashby simultaneously moved up to CRITICAL — see synthesizer's settlement.)
- **Grouping proposal:** his takes-over/L98-120 finding and Turing's L31-32 finding share one root — "**line-accurate-looking but non-licensing cites**": cites that pass a line-number check but fail a does-this-line-support-the-claim check. More dangerous because they pass the cheap verification.
- two-layers framing: co-signs as the structural generalization of his point finding; defers ownership to Ashby's governance lens.
- Convergence: "Three attackers converge on a single root — attributing authority to domainspec-subagents-strategy that its own ROUTER self-description disclaims — my only concession CRITICAL→MAJOR; no residual dissent."

---

## Verifier (Popper) — refutation pass

Opened all three artifacts at the literal cited lines. **7/7 findings SUBSTANTIATED, 0 dropped.** Key confirmations:
- #1: dispatch-spec L104-106 verbatim names "the orchestrating capability, **usually Refine**"; full-file scan — "domainspec-subagents-strategy" appears **zero** times in dispatch-spec. Misattribution real. MAJOR correctly rated.
- #2: no "two layers / outer contract / governed engine" language in either SKILL — invented. **Softest MAJOR** — target hedges it under "the mental model that makes it click", a defensible MINOR; FIX verdict unaffected.
- #3: dispatch-spec L31 is scope prose with no pass/flag/block; enum at L148 + L165-169. Finding's "L166-169" off-by-one (cosmetic). SUBSTANTIATED.
- #4–#7: all confirmed at L3 / L56+check-tension L12 / L56-68 / Rule 22 L93.
- Dropped items re-confirmed correct: 25 rules (L72-96, counted), validator referenced L61, LIVE table L41-48.

zig-zag convergence: verifier raised no refutation → exchange terminates (1 turn).

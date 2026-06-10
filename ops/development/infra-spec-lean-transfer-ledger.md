# Infra-Spec Lean Transfer Ledger

Lane: L2 — Lean Infra Translator
Date: 2026-06-08
Parent dispatch: `infra-spec-research-strategy-20260603`
Status: read-only research receipt. Not infra-spec authority.

## Question

Which Lean-formalization lessons should constrain infra-spec, and which must remain analogy?

## Scope And Evidence Boundary

This lane scrubbed the **in-checkout** Lean/formalization evidence only:

- `ops/development/domainspec-lean-formalization-claim-discipline-ledger.md`
- `ops/development/domainspec-lean-formalization-research-brief.md`
- `ops/development/domainspec-lean-formalization-fanout-receipts.md`
- `ops/development/domainspec-lean-formalization-interpretation-tournament.md`
- `ops/development/domainspec-lean-formalization-next-route-handoff.md`
- `ops/development/domainspec-lean-formalization-relation-ledger.md`
- `ops/development/domainspec-lean-formalization-validation-ledger.md`
- `ops/RUNTIME-SURFACE-CONVERGENCE-REFINE.md` — checked; contains **no** Lean/formalization references (it covers skill-surface cleanup vs orchestration runtime), so it is out of scope per the strategy's "only if it references Lean" condition.
- `arcanum/` — checked for formalization / reflection-tower / residue material.

Critical evidence caveats this lane inherits and must not paper over:

- **`implementation/domainspec/` is EMPTY in this worktree.** It contains only a `.git` pointer file (89 bytes); `git submodule status` shows `+6f26de2... implementation/domainspec (heads/main)` (uncommitted/out-of-sync pointer), and `find implementation/domainspec -name "*.lean"` returns nothing. The actual Lean source corpus (`lean-formalization/*.lean`, `DomainSpec.lean`, `ReflectionTower.lean`, `M2Counter.lean`, etc.) is **NOT present in this checkout**. Every Lean source-line citation below (e.g. `lean-formalization/ReflectionTower.lean:349`) is **transcribed from the prior research ledgers, not re-verified against live source**. The Lean source is therefore **explicitly deferred** — see Residue R1.
- The prior route's own validation ledger (`domainspec-lean-formalization-validation-ledger.md:53-68`) records that **the Lean build never completed** (Lake/Mathlib ref-lock + toolchain fetch failures). So even in the original route, proof-closure was never build-validated. Infra-spec must treat all "proved" labels below as **source-claimed-but-not-build-verified**.

Per the Non-Negotiables, every claim cites a path and is classified as
source-backed (the prior Lean route's own source citations),
implementation-backed (live infra/code in this checkout),
analogy, candidate, stale, contradiction, or unsupported. Analogies are labeled explicitly.

---

## Lean-to-Infra Transfer Table

| # | Lesson | Source path (in-checkout) | How it maps to infra-spec | Reuse verdict |
|---|--------|---------------------------|---------------------------|---------------|
| L1 | **Schema vs instance are two irreducible budgets**: preserving schema-level structure does not force instance-level fidelity. | `domainspec-lean-formalization-research-brief.md:11`, `:141-145`; `domainspec-lean-formalization-interpretation-tournament.md:118-120` (M6 strong / M2 unrestricted refuted) | Infra-spec must split **schema/spec preservation** (topology, contract, declared deployment unit) from **instance/runtime preservation** (the deployed instance, its state, its observed behavior). A correct architecture diagram does not prove the running system matches it. Two budgets: spec-fidelity and runtime-fidelity. | **safe-to-reuse** (as structural discipline) |
| L2 | **Counterexample discipline**: every attractive preservation claim needs a failure witness; counterexamples are load-bearing results, not failed attempts. | `domainspec-lean-formalization-research-brief.md:47-58`, `:151-153`; `domainspec-lean-formalization-claim-discipline-ledger.md:118-129` | Every positive infra pattern ("this topology is resilient", "this deploy preserves state") needs at least one **violation/failure fixture** showing where it breaks. Aligns directly with the strategy's "counterexample discipline" candidate concept (`infra-spec-research-strategy.md:280`). | **safe-to-reuse** |
| L3 | **Build / proof / sorry-free / axiom-free / PR-ready are FOUR-PLUS DISTINCT statuses**, never collapsed. | `domainspec-lean-formalization-claim-discipline-ledger.md:142-150` ("Treat green build, no active `sorry`, no axioms, and PR-ready as four different statuses"); `domainspec-lean-formalization-fanout-receipts.md:32`, `:36-37` | Infra-spec operational proof status must separate `specified` / `implemented` / `deployed` / `observed` / `validated` / `reflected` / `promoted` (matches `infra-spec-research-strategy.md:278`). A green CI run is not a successful deploy; a successful deploy is not validated behavior; validated behavior is not promotion authority. | **safe-to-reuse** |
| L4 | **Typed residue**: leftover/leaked information is classified (by layer, axis, bridge status, proof status), not vague. | `domainspec-lean-formalization-research-brief.md:147-149`; `domainspec-lean-formalization-claim-discipline-ledger.md` (label structure throughout) | Infra residue (what does not cross cleanly from spec to deploy/runtime/telemetry/incident recovery, per `infra-spec-research-strategy.md:275`) should be **typed**: which environment, which boundary object, which state namespace, which proof-status it failed at. | **safe-to-reuse** (typing structure); residue *content* is infra-specific |
| L5 | **Active-sorry / build-blocker claim discipline**: a text scan that finds `sorry` is enough to DEMOTE a "complete" claim, but NOT enough to assert proof-closure; and a build failure is a tooling blocker, not a proof failure. | `domainspec-lean-formalization-claim-discipline-ledger.md:16-35` (text scan, 30 sorries / 8 files, "not a full Lake build"); `:57-67`; `domainspec-lean-formalization-validation-ledger.md:53-68` | Infra-spec needs the same asymmetry: a cheap negative check (e.g. missing health probe, unpinned dependency, drift detector firing) is enough to **demote** a "deployed/validated" claim, but green telemetry alone is **not** enough to assert "validated" — and an environment/tooling failure (e.g. CI runner down) must be recorded as a **blocker**, not a system failure. | **safe-to-reuse** |
| L6 | **Analogy demotion rules**: bridge/relation language must carry an explicit status label (formal / documented / operational / analogy / candidate / demoted); "isomorphism" / "same object" is demoted unless formal equivalence is supplied. | `domainspec-lean-formalization-relation-ledger.md:7-17`, `:82-96`; `domainspec-lean-formalization-claim-discipline-ledger.md:103-116` | Infra-spec must label every cross-register claim (Lean → infra, reflection-tower → infra, residue → infra, CyberAlchemy → infra) and refuse to promote analogy to obligation. Matches Non-Negotiable: "Analogies from Lean, reflection tower, residue, or CyberAlchemy must be labeled". | **safe-to-reuse** (the *discipline*); the underlying *content mappings* are mostly **must-remain-analogy** — see below |
| L7 | **Reflection tower**: local run evidence does not become authoritative by existing; it climbs through staged registers. The DomainSpec "reflection tower" is a Lean object about typed persistence (`ReflectionTower.lean`), and the "tower" applied to operations is itself an **analogy** that the corpus deliberately demotes. | `domainspec-lean-formalization-claim-discipline-ledger.md:45` (`ReflectionTower.lean:349` persistence), `:110`, `:126` (finite Lawvere/fixed-point reading structurally blocked); `domainspec-lean-formalization-relation-ledger.md:82-96` (Arcanum↔reflection-tower "isomorphism" demoted) | The **promotion-gate principle** transfers: infra runtime evidence climbs only through receipt → validation → synthesis → decision → owner review (matches `infra-spec-research-strategy.md:279`). The **Lean reflection-tower object itself** (typed persistence / diagonal axis / fixed-point) does **NOT** transfer as math — it is an explanatory bridge. | **promotion-gate principle: safe-to-reuse; Lean tower object: must-remain-analogy** |
| L8 | **Promotion gates / candidate-before-canon**: gaps and relations become canonical only through an explicit gate, never by accumulation. | `domainspec-lean-formalization-research-brief.md:85-93`, `:159-161` (research-gpt makes gaps first-class; named residue must be typed/blocked/actionable); `domainspec-lean-formalization-relation-ledger.md:7-17` (graded relation labels) | Infra-spec: runtime evidence cannot self-promote to promotion authority (echoes Non-Negotiable at `infra-spec-research-strategy.md:40`). Every promotion needs a gate with an owner. Also corroborated operationally (not via Lean) by Arcanum's `candidate-before-canon` in `arcanum/arcana/residuality-spec/SKILL.md` and necronomicon vault discipline. | **safe-to-reuse** (gate principle); cross-validated by operational register |
| L9 | **Front-door summaries go stale**; a mechanical current-truth refresh must run before reusing status claims. | `domainspec-lean-formalization-claim-discipline-ledger.md:142-151`; `domainspec-lean-formalization-next-route-handoff.md:26-37`; `domainspec-lean-formalization-fanout-receipts.md:29` (counts drift: README says 122/23, local found 144/29) | Infra-spec status fields (deployed version, env config, topology doc) drift from reality. The spec must require a **mechanical refresh / drift check** before any status field is trusted as promotion input. Directly motivates a drift detector. | **safe-to-reuse** |
| L10 | **Two-layer-by-three-axis residue frame** (vertical schema/instance; horizontal time/evolution; diagonal promotion/persistence). | `domainspec-lean-formalization-research-brief.md:60-72`; `domainspec-lean-formalization-interpretation-tournament.md:110-111` | Tempting to map: vertical = spec/runtime, horizontal = version/migration evolution, diagonal = promotion/reflection. The **vertical** axis maps cleanly (it IS schema/instance, L1). The **horizontal and diagonal axes are category-theoretic constructs** (Kan extensions, fixed-point persistence) with no infra theorem behind them. | **vertical axis: safe-to-reuse (= L1); horizontal/diagonal: must-remain-analogy** |
| L11 | **Categorical machinery** (functors, adjunctions, Kan extensions, units/counits, fully-faithful thresholds, "fractal" = full-faithfulness on adjunction slots). | `domainspec-lean-formalization-research-brief.md:37-45`; `domainspec-lean-formalization-fanout-receipts.md:27` (`README.md:29`, `NAMING.md:14`) | No infra-spec construct should claim functoriality, adjunction, or Kan-extension structure. These are the *mechanism* of the Lean proofs and have **no validated infra counterpart**. | **must-remain-analogy** (do not import the math) |
| L12 | **Thermodynamic / Noether / Lawvere bridges** — finite/discrete only; continuous physical claims open; Noether is a scope warning not a theorem; Lawvere fixed-point demoted. | `domainspec-lean-formalization-research-brief.md:74-83`, `:113`; `domainspec-lean-formalization-claim-discipline-ledger.md:97`, `:109-110` | Any "infra has an entropy/second-law/conservation-law" framing is **pure analogy** with even weaker support than in the Lean corpus (where it is bounded to finite/discrete witnesses). Do not let "infra residue ≈ entropy" become a load-bearing claim. | **must-remain-analogy** |

---

## Concepts Safe To Reuse

These transfer as **structural discipline** (not as borrowed theorems). Each is a *method*, validated by the Lean route's own claim discipline:

1. **Two-budget split** (L1): spec/schema preservation ≠ instance/runtime preservation. Evidence: `domainspec-lean-formalization-research-brief.md:141-145`.
2. **Status separation** (L3): `specified` / `implemented` / `deployed` / `observed` / `validated` / `reflected` / `promoted` are distinct. Evidence: `domainspec-lean-formalization-claim-discipline-ledger.md:147`.
3. **Counterexample / violation-fixture discipline** (L2): every positive infra pattern carries a failure fixture. Evidence: `domainspec-lean-formalization-research-brief.md:151-153`.
4. **Typed residue typing** (L4): residue is classified by axis/layer/boundary/status, not vague. Evidence: `domainspec-lean-formalization-research-brief.md:147-149`.
5. **Negative-check-demotes / blocker-is-not-failure asymmetry** (L5): cheap negatives demote a positive claim; tooling failures are blockers, not system failures. Evidence: `domainspec-lean-formalization-claim-discipline-ledger.md:16-35`, `domainspec-lean-formalization-validation-ledger.md:64-68`.
6. **Graded relation / analogy-demotion labels** (L6): formal / documented / operational / analogy / candidate / demoted. Evidence: `domainspec-lean-formalization-relation-ledger.md:7-17`.
7. **Promotion gate + candidate-before-canon** (L7 principle, L8): runtime evidence climbs through receipt→validation→synthesis→decision→owner review; nothing self-promotes. Evidence: `domainspec-lean-formalization-relation-ledger.md:7-17`; operationally cross-validated in `arcanum/arcana/residuality-spec/SKILL.md`.
8. **Mechanical current-truth refresh before trusting status** (L9). Evidence: `domainspec-lean-formalization-next-route-handoff.md:26-37`.

## Concepts That Must Remain Analogy (labeled explicitly)

These are **analogies** — useful explanatory bridges, NOT infra obligations or theorems. They MUST carry the `analogy` label in any infra-spec artifact:

- **[ANALOGY] The Lean "reflection tower" object** (typed persistence, diagonal axis, fixed-point structure) as a model of infra promotion. Only the *gate principle* transfers; the categorical object does not. Evidence: `domainspec-lean-formalization-claim-discipline-ledger.md:110`, `:126`; `domainspec-lean-formalization-relation-ledger.md:82-96` (the Arcanum↔reflection-tower "isomorphism" is itself demoted).
- **[ANALOGY] Categorical machinery** — functor/adjunction/Kan-extension/fully-faithful "fractal" framing applied to infra. No validated infra counterpart. Evidence: `domainspec-lean-formalization-research-brief.md:37-45`.
- **[ANALOGY] Horizontal & diagonal residue axes** (time/evolution; promotion/persistence) as formal infra structure. Only the vertical (schema/instance) axis maps cleanly. Evidence: `domainspec-lean-formalization-research-brief.md:60-72`.
- **[ANALOGY] Thermodynamic / Noether / Lawvere bridges** ("infra entropy", "conservation law", "fixed point"). Even in Lean these are bounded/demoted; in infra they have no support. Evidence: `domainspec-lean-formalization-research-brief.md:74-83`; `domainspec-lean-formalization-claim-discipline-ledger.md:103-116`.
- **[ANALOGY] CyberAlchemy / Arcanum reflection-tower "same object" framing.** Operational register, explicitly `operational`+`analogy`, "isomorphism" demoted. Evidence: `domainspec-lean-formalization-relation-ledger.md:66-96`.

## Proof / Build / Status Caution List

Hard cautions infra-spec must encode, inherited from the Lean route's failures:

1. **No "validated/deployed/proven" claim without the matching distinct status.** Mirrors "treat green build, no `sorry`, no axioms, PR-ready as four different statuses" — `domainspec-lean-formalization-claim-discipline-ledger.md:147`.
2. **A passing check is necessary, not sufficient.** A text scan can demote but cannot certify (`:35`, `:39`). For infra: green telemetry / passing CI demotes "broken" but does not certify "validated".
3. **Tooling/environment failures are BLOCKERS, not system failures.** The Lean Lake/Mathlib build never completed and that was correctly NOT read as a proof failure — `domainspec-lean-formalization-validation-ledger.md:53-68`. Infra-spec must distinguish "deploy failed" from "deploy pipeline/runner unavailable".
4. **Counts and status fields drift; never trust front-door summaries.** README claimed 122/23 files; local found 144/29 — `domainspec-lean-formalization-fanout-receipts.md:29`. Infra-spec status fields (version, replica count, config) need a drift/refresh gate.
5. **Build status ≠ proof closure was never independently re-established here.** All "proved/source-level" labels in the source ledgers are *source-claimed, not build-verified* — `domainspec-lean-formalization-claim-discipline-ledger.md:38-56`. Infra-spec should not inherit any "validated" status transitively.
6. **The Lean source backing every transferred lesson is NOT in this checkout** (see Residue R1). The transfers above are sound as *discipline*; the *source-line citations* are second-hand until the submodule is restored.

---

## Claim Classification (every claim cites a path)

| Claim | Classification | Citation |
|-------|----------------|----------|
| Schema preservation does not force instance preservation (two budgets). | source-backed (prior route) | `domainspec-lean-formalization-research-brief.md:141-145` |
| Build/sorry/axiom/PR-ready are four distinct statuses. | source-backed | `domainspec-lean-formalization-claim-discipline-ledger.md:147` |
| Counterexamples are load-bearing, not failures. | source-backed | `domainspec-lean-formalization-research-brief.md:151-153` |
| Residue is typed by layer/axis/status. | source-backed | `domainspec-lean-formalization-research-brief.md:147-149` |
| Text scan demotes but cannot certify; build failure is a blocker. | source-backed | `domainspec-lean-formalization-claim-discipline-ledger.md:35`; `domainspec-lean-formalization-validation-ledger.md:64-68` |
| Relations are graded; "isomorphism" demoted. | source-backed | `domainspec-lean-formalization-relation-ledger.md:7-17`, `:82-96` |
| Promotion gate / nothing self-promotes. | source-backed | `domainspec-lean-formalization-research-brief.md:85-93` |
| Candidate-before-canon also holds operationally in Arcanum. | implementation-backed (operational register, not Lean) | `arcanum/arcana/residuality-spec/SKILL.md` |
| Reflection-tower *object* maps to infra promotion. | **analogy** | `domainspec-lean-formalization-relation-ledger.md:82-96` |
| Categorical machinery maps to infra. | **analogy** | `domainspec-lean-formalization-research-brief.md:37-45` |
| Horizontal/diagonal axes map to infra as formal structure. | **analogy** | `domainspec-lean-formalization-research-brief.md:60-72` |
| Thermodynamic/Noether/Lawvere → infra entropy/conservation. | **analogy** | `domainspec-lean-formalization-research-brief.md:74-83` |
| The Lean source corpus is present and re-verifiable in this checkout. | **contradiction / stale** | `implementation/domainspec/` empty (only `.git`, 89B); `git submodule status` shows out-of-sync pointer `+6f26de2...` |
| All source-line proof citations were re-verified by this lane. | **unsupported** (deferred) | `domainspec-lean-formalization-validation-ledger.md:53-68` (build never completed even originally) |
| `ops/RUNTIME-SURFACE-CONVERGENCE-REFINE.md` informs Lean transfer. | stale/out-of-scope (no Lean content) | `ops/RUNTIME-SURFACE-CONVERGENCE-REFINE.md` (skill-surface vs orchestration only) |

---

## Residue

- **R1 (deferred — Lean source absent).** `implementation/domainspec/` is empty in this worktree (only an 89-byte `.git` pointer; `git submodule status` = `+6f26de2ecf10056fca683b44f01079fb9fd60aac implementation/domainspec (heads/main)`, out of sync; no `*.lean` files found). The live Lean corpus that backs L1–L12 (`DomainSpec.lean`, `ReflectionTower.lean`, `M2Counter.lean`, `M6Counter.lean`, `Bicyclic.lean`, etc.) is **NOT available**. All Lean source-line citations are transcribed from the prior ledgers and **not re-verified**. **Verdict: explicitly deferred** — re-verification requires submodule init/update and is out of this read-only lane's scope.
- **R2 (build status never closed).** Even the originating route never completed a Lean build (`domainspec-lean-formalization-validation-ledger.md:53-68`). No transferred lesson should carry a "build-verified" or "proof-closed" status into infra-spec. The cautions transfer; the proof-closure does not.
- **R3 (gate-principle vs tower-object boundary is the highest-risk transfer).** L7/L10 are the easiest to over-import: the *promotion-gate principle* is safe, but the *reflection-tower object* and *diagonal/horizontal axes* are analogy. An infra-spec author under deadline is likely to collapse these. This boundary should be a named validation check in the infra-spec validator.
- **R4 (operational vs formal register conflation).** Arcanum's `residuality-spec` / `candidate-before-canon` / necronomicon promotion vocabulary *rhymes* with the Lean residue/promotion vocabulary but is a separate operational register (already labeled `operational`+`analogy` in `domainspec-lean-formalization-relation-ledger.md:66-96`). Infra-spec must not silently merge them.

---

## Child Dispatch Proposals

One proposal warranted (Residue R1 crosses a checkout/submodule boundary and is a hard blocker on full source-backing).

### CD-L2-01: Lean Source Re-Verification Pass

- **parent_dispatch_id**: `infra-spec-research-strategy-20260603`
- **scope**: After `implementation/domainspec` (or the `domainspec-lean-formalization` source tree) is checked out, re-verify the source-line citations behind L1–L12 against live `*.lean` files, and run the deferred dependency-cone sorry/axiom audit so transferred lessons carry an accurate (not transcribed) source status.
- **owning lane**: L2 — Lean Infra Translator
- **roles**: Lean corpus re-verifier; skeptical math auditor (re-run); owner-boundary reviewer.
- **inputs**: this ledger; `domainspec-lean-formalization-claim-discipline-ledger.md`; restored Lean source corpus; `domainspec-lean-formalization-validation-ledger.md` (W0/W1 build-repair work units in `domainspec-lean-formalization-next-route-handoff.md:39-68`).
- **expected artifacts**: a verification appendix to this ledger flipping each `source-backed (transcribed)` claim to `source-verified` or `contradiction`.
- **stop conditions**: stop before mutating any Lean proof source (inherit `domainspec-lean-formalization-next-route-handoff.md:128-130`); stop if submodule cannot be initialized (record as blocker, do not fabricate).
- **join policy**: results merge back as an appendix; no infra-spec status field may claim "Lean-source-verified" until this child closes.
- **validation evidence**: re-run the dispatch validator; diff transcribed vs live citations; record build/sorry/axiom status per headline file.

---

## Receipt

- **role_id**: L2-lean-infra-translator
- **ledger_path**: `ops/development/infra-spec-lean-transfer-ledger.md`
- **lessons_extracted**: 12 (L1–L12)
- **safe_to_reuse**: two-budget split; status separation; counterexample/violation-fixture discipline; typed-residue typing; negative-demotes/blocker-not-failure asymmetry; graded analogy-demotion labels; promotion gate + candidate-before-canon; mechanical current-truth refresh
- **must_remain_analogy**: reflection-tower *object*; categorical machinery (functor/adjunction/Kan/fractal); horizontal+diagonal residue axes; thermodynamic/Noether/Lawvere bridges; CyberAlchemy/Arcanum "same object" framing
- **key_findings**:
  - Lean's core warning transfers as *discipline*, not as math: spec/runtime are two budgets and a correct diagram does not prove a correct deployment (`domainspec-lean-formalization-research-brief.md:141-145`).
  - The four-distinct-statuses rule is the single most reusable lesson and directly seeds infra's `specified/implemented/deployed/observed/validated/reflected/promoted` split (`domainspec-lean-formalization-claim-discipline-ledger.md:147`).
  - Negative-check-demotes / tooling-failure-is-a-blocker asymmetry transfers cleanly (`domainspec-lean-formalization-validation-ledger.md:64-68`).
  - The reflection-tower *principle* (gated promotion) is safe; the reflection-tower *object* and the horizontal/diagonal axes and all physics/Lawvere bridges must stay labeled analogy (`domainspec-lean-formalization-relation-ledger.md:82-96`).
  - `ops/RUNTIME-SURFACE-CONVERGENCE-REFINE.md` has no Lean content — correctly out of scope.
- **residue**: R1 — `implementation/domainspec/` EMPTY (broken/out-of-sync submodule pointer, only 89-byte `.git`, zero `*.lean`); Lean source explicitly **deferred**, all source-line citations transcribed not re-verified. R2 — Lean build never closed even originally; no "build-verified" status transfers. R3 — gate-principle vs tower-object is the highest over-import risk. R4 — operational (Arcanum residuality) vs formal (Lean residue) registers must not merge.
- **child_dispatch_proposals**: 1 (CD-L2-01: Lean Source Re-Verification Pass)
- **path_citation_confirmed**: yes
- **blocked_fields_or_no_block**: no-block (R1 is recorded as deferred residue + child dispatch, not a lane blocker; this read-only lane completed within its in-checkout evidence scope)

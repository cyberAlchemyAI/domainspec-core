---
tags: [cyber-alchemy-space, capability-taxonomy, research, raw-returns, knowledge-craft-governance]
node_type: research
is_session: false
layer: architecture
nature: reference
status: draft
created: 2026-06-18
dispatch_id: 2026-06-18-cyberalchemy-capability-taxonomy
dispatch_type: research
working_folder: research/cyber-alchemy-space/capability-taxonomy/
sources: [arcanum/, implementation/domainspec/, projects/ontologize, projects/framework-unification, cyberAlchemy/, .claude/skills/]
---

# Research — CyberAlchemy capability taxonomy (collected returns)

Raw returns for dispatch `2026-06-18-cyberalchemy-capability-taxonomy`. Groups: explorers (4,
pairwise tensioned on methodology × source-corpus) → synthesizer (1) ↔ reviewers (3 skeptics:
precedent / non-vacuity / definitional-soundness) → auditor (final approver). The cited synthesis
lives in [findings.md](findings.md); this file is the verbatim evidence trail. check-tension gate
passed (2 independent agents) before the human confirm.

Question: what capabilities does the repo already have, viewed through CyberAlchemy-as-method
(symmetries + recursive structures), and do they organize into a taxonomy (seed buckets
Knowledge / Craft / Governance, open to emergent types like *interviewer*)?

---

## Explorers (Wave 1)

### E1 — Simon, Herbert · empirical bottom-up (shipped catalog IS the capability set)

Walked the shipped catalog on disk; verb-tagged each unit.

- **Arcanum formulae (2):** dispatch-spec (route), observability-setup (observe/install).
- **Arcanum transmutations (4):** context-builder (distill), feature-glossary (define), implementation-layering (plan), codex-goal-profile (route/translate).
- **Arcanum arcana (~35):** architecture-pattern-inventory (ontologize), audit-alignment (validate), code-tag-audit (validate, parochial), constitution-governance (govern), craft (govern/track), decision-gate (govern/gate), definitions-governance (define), discipline-governance (govern), distill (distill), experiment-harness (validate/run), integration-spec (design), inventory (ontologize), invoke-example-runner (validate, parochial), observability-derivation (distill/derive), ontology-vault (ontologize), refine (refine), research-evidence-harness (validate), research-tower (research), residuality-spec (design/harden), robot-talks (research/multi-agent), scope-interview (interview), sigil-development (refine/lifecycle, parochial), sigil-runtime-installer (route/install, parochial), signal-observer (observe), skill-decomposer (distill/extract), skill-transcriptor (refine/convert), spellcraft (design/compose, parochial), structured-interview-kits (interview, = interrogation alias), sync-user-stories (distill/derive, parochial), task-session (execute), test-derivation (distill/derive), ux-evidence-validator (validate), workflow-reflect (observe/reflect), x-ray (distill/visualize), interrogation (interview).
- **Arcanum spells (13, composed):** arcanum-bootstrap (route/install, parochial), discovery-to-inventory (ontologize), goal (route), guide-architecture (research/teach), implementation-readiness (validate), invoke (invoke — dev intent → define/design/plan/handoff/refresh), necronomicon (ontologize), observed-invocation-loop (observe, parochial), ontology-harness (ontologize), publication-research-pipeline (research), repository-harness (ontologize), sigil-maintenance-loop (refine, parochial), whisper (author).
- **Disciplines (DISCIPLINES.md):** 19 named practices (doc says 19; E1 counts 21 rows — self-undercount). Reflection-layer, NOT shipped executable units; each names a verb already practiced by a sigil.
- **Repo `.claude/skills` delta (net-new beyond arcanum mirror):** anti-bias-vector-composition (design/govern), check-tension (validate/gate), domainspec-subagents-strategy (route), register-dispatch (govern/record), research / review / experiment (dispatch type-skills), ontology-view / system-view / engineer-view / paired-views (ontologize/design triad), orchestrate (route), close-session (govern), commit-message (govern). → a **dispatch/anti-bias governance layer** absent from arcanum proper.
- **implementation/domainspec/.claude/skills delta:** ~45 `domainspec-*` (a parochial product pipeline: scaffold/interview/spec/derive/implement/audit/sync/reflect/route/bridge) — all DomainSpec-bound; ~70 `gsd-*` (a SECOND complete project-management OS) — entirely vendored, NOT Arcanum-portable.

**Grouped by verb (Arcanum core + repo-delta):** distill (8), validate (12+), ontologize (8), govern (8), route (8), research (4), refine (5), observe (5), interview (2), define (2), design (3), plan (1), execute (1), invoke (1), author (1).

**Dominant verbs:** validate, distill, ontologize, govern, route ≈ 70% of catalog → the shipped set is overwhelmingly a **knowledge-governance + verification machine, not a generation machine.** **Singletons:** plan, execute, invoke, author — each represented by exactly ONE unit; generative/creative verbs are one-deep.

**Self-flagged bias (catalog-as-truth):**
- OVER-counts via mirroring/aliasing: `.claude/skills` largely duplicates `arcanum/`; structured-interview-kits is an explicit alias of interrogation; spells are compositions of already-counted sigils; gsd-* (~70) is a vendored external product, not a CyberAlchemy capability. Path count inflates true capabilities ~30–40%.
- OVER-counts disciplines as capabilities (reflection labels, not units; doc miscounts its own rows).
- UNDER-counts the generative axis: one-unit-per-verb for plan/execute/author/invoke more likely signals a *missing* capability family (no first-class synthesize / prototype / negotiate / migrate).
- UNDER-counts emergent/composed capability: dispatch-spec + register-dispatch + check-tension + subagents-strategy + research/review/experiment together are ONE coherent "governed multi-agent dispatch" capability that row-per-unit shatters into ~7 fragments.
- Net: row count is an upper bound on *files*, a lower bound on *true distinct capabilities*.

### E2 — Lawvere, F. William · formal top-down (capability types the LAW requires)

Derivation principle: a capability type is REQUIRED iff some law clause cannot close without an owner of that type. Collapsed the 13 method steps + Governing Primitives + A1–A6→C1–C11 chains into 16 types.

| # | Type | Law clause that demands it | Shipped owner? |
|---|---|---|---|
| 1 | Orient / intent-naming | METHOD 1–3; Objective-Artifact Pair, Intent Before Machinery | yes (scope-interview, invoke, refine) |
| 2 | Discover / research | METHOD 4; Research Before Closure, Cheap Evidence Baseline, Unknowns Registry | yes (research, research-tower, necronomicon) |
| 3 | Route | METHOD 5+12; Route Before Work, Authority-Bound Composition | yes (orchestrate, dispatch-spec, domainspec-orchestrate) |
| 4 | Define (vocabulary/ontology) | METHOD 6; Local Vocabulary First, Trace Before Promotion; BUSINESS-ONTOLOGY; ontology-conventions | yes (ontology-vault, definitions-governance, feature-glossary, ontology-view) |
| 5 | Design | METHOD 6; Dev Packet "Design"; AUTHORITY-MAP ARCHITECTURE row | yes (invoke design, system-view, engineer-view, architecture-pattern-inventory) |
| 6 | Plan / layer | METHOD 6; Layered Proof Progression, Closure Seeding | yes (implementation-layering, invoke plan, implementation-readiness) |
| 7 | Tension / critique | METHOD 7; Tension Over Summary, Balancer role; check-tension | yes (robot-talks, review, check-tension, residuality-spec) |
| 8 | Execute | METHOD 5 + 8; Lifecycle Ownership | yes (task-session, domainspec-implement, domainspec-pipeline) |
| 9 | Validate / gate | METHOD 8 + Quality Bar; Gate Before Mutation, Pass/Flag/Block; C5/C7/C8/C3 | yes (decision-gate, verify-feature, readiness-gate, audits) |
| 10 | **Navigate / make-legible** | METHOD 9; Navigable Work Surface; Ergonomics Is Governance | **partial — no dedicated enforcing owner** |
| 11 | Trace / preserve | METHOD 11; Artifact As State, Traceability Is Memory; vault edges | yes (close-session, scratchpad, vault Connections) |
| 12 | Observe | METHOD 13 + Observer role; AXIOM A4; C4/C9; Split Observer from Executor | yes (signal-observer, observability-setup, observed-invocation-loop) |
| 13 | Reflect / evolve | METHOD 13; Reflection Outer Loop; A5/A6; C10/C11 | yes (workflow-reflect, domainspec-reflect, Via-Negativa) |
| 14 | Govern / promote | Trace Before Promotion, Human Gate, Authority-Bound Composition; A1–A6→C1–C11; AUTHORITY-MAP | yes (constitution-governance, decision-gate, AUTHORITY-MAP) |
| 15 | **Bridge / translate** | BUSINESS-ONTOLOGY Bridge Layer; C6 @biz/@sys; Boundary Extraction Before Conversion | **partial — no continuous drift comparator** |
| 16 | Delegate / dispatch-health | Role-Separated Agent Work, Delegation Health | yes (subagents-strategy, register-dispatch, arcanum-stage-worker) |

**Gaps the law REQUIRES but owner is thin/absent:**
- **Type 10 (Navigate) has no enforcing owner** — legibility is a governance obligation (Ergonomics Is Governance) + Quality-Bar close condition, yet the validator checks artifact class/retention, not whether an artifact exposes entrypoint/status/next-route. Legibility is asserted, not gated. (Clearest law-vs-owner gap.)
- **Type 15 (Bridge) lacks a continuous comparator** — law treats Business→System as the antifragility engine ("continuously compare"); GOVERNANCE-ATTENUATION itself diagnoses System-3 Control as "manual trigger" and @biz/@sys binding as roadmap (G11). Law-acknowledged gap.
- Type 14 sub-obligation "Policy (System 5)" was MISSING in the VSM mapping but CONSTITUTION.md/AXIOMS.md now exist → marked **closed**.

**Self-flagged bias (idealized types):** strongly law-anchored = 1–9, 11–14, 16. My own abstraction: Type 10 (Navigate) as a *standalone type* (law makes it a cross-cutting property, not necessarily an owner) — strongest interpretive move; Type 15 split (translate/anchor/drift as one type) is mine though it rests on "continuously compare"; collapsing 13 steps → 16 types is an editorial functor (another explorer could produce 11 or 20).

### E3 — Mandelbrot, Benoit · computational/structural (capabilities as RECURRENCES)

CyberAlchemy "chases symmetry between layers" (Symmetry-pursuit principle). Five recurrences; three load-bearing, two decorative.

- **R1 — intent↔reality symmetry (the GENERATING recurrence) — LOAD-BEARING.** Invariant: keep *meant* and *actual* mutually traceable; the gap is a first-class object (drift/residue); reducing it is the work. Same structure at 4 altitudes: domain run (B1 meaning vs B2 system, gap = `drifts_from`/B4); engine run (spec vs code, gap = I2 connection-integrity/ADLC tags); claim level (claim vs proof, gap = claim≤proof / I4 / P10); meta (schema vs data, gap = TranslationResidue). `drifts_from`, `alignment-gap`, `claim≤proof`, "residue reduction" are the **same gap-detector recurring**. The `drifts_from` (raw) vs `contradicts` (adjudicated) split = research's KILL-vs-owner = engine's signal→TUNING-REPORT (raw-signal→adjudicated-verdict).
- **R2 — altitude-shift / recursive self-application (I9) — LOAD-BEARING.** "Every stage is the same process at a different altitude; the pipe runs on itself." A tier-D engine artifact, while being developed, grows its own tier-A problem-statement→discovery→plan→spec. ontology-view is explicitly the bridge (ARTIFACTS L116): produced per-run (tier-A), feeds cross-run (tier-B) — same authoring verb, two altitudes. pipeline-signals→TUNING-REPORT = one observe-capability at two altitudes.
- **R3 — router → type-skill → form recursion — LOAD-BEARING.** Fixed three-tier division of law: *when/whether+universal* | *type judgment* | *fill mechanics*. Dispatch chain (subagents-strategy → research/review/experiment → register-dispatch); same shape inside one dispatch (group/edge/dispatch = layers/loop_cap/max_loops, "smallest scope wins"); same shape one altitude up (CLAUDE.md routers → skills → constitutions). The router's "field defs live in §5/register-dispatch, not here" = ontology-view's single-owner invariant (I5: every term one home) = view-triad's no-double-decision — **the same capability** (routing-by-single-owner = define-each-thing-once).
- **R4 — view-triad symmetry (ontology/system/engineer) — PARTLY LOAD-BEARING.** Decompose any target into 3 non-overlapping authorities (vocabulary / shape+stances / mechanics+verdicts), single-owner cross-check. This is **R3's division-of-law projected onto knowledge representation**: router/type/form ≅ ontology/system/engineer. Load-bearing = the 3-way separation (single-owner invariant as authoring procedure); ontologize **refused a 4th branch-view** — the refusal (resisting a 4-branch×3-view grid) is the load-bearing part; the grid is decorative.
- **R5 — four-branch model as the same gap-machine — DECORATIVE (mostly).** B1/B2/B3/B4 ≅ M2/M1/M0 is rhyme, not recurrence (ARTIFACTS hedges "another angle"). Load-bearing piece inside: B3 run-context = R1's "actual" pole made first-class (honest denominators). The quadrant is decorative scaffolding; the B1↔B2-via-B4 gap edge is R1 again.

**Self-flagged bias (symmetry over-fit):** demotes R5 plane-mapping (rhyme), R4 4×3 grid (deliberately declined by the team — the absence of branch-view is the signal). Test offered: a recurrence is load-bearing **iff something breaks when you collapse the altitudes** — R1/R2/R3 pass (silent drift / two-hats-on-one-file confusion / read-budget blowup); R4-grid and R5-planes cost only a diagram. **The one capability under all of it: *preserve-both-poles-and-route-the-gap-to-a-single-owner.*** Drift detection, claim≤proof, single-owner registry, view-triad no-double-decision, dispatch router = five names for that one recurring verb at five altitudes.

### E4 — Ashby, W. Ross · adversarial seam-mining (does Knowledge/Craft/Governance partition cleanly?)

**Verdict up front: it is NOT a clean partition.**

| # | Overlap | Nature | Buckets | Breaks partition? | Real vs name-only |
|---|---|---|---|---|---|
| S1 | "define" in invoke (authoring act) vs domainspec (canonical DS-* meaning) | multi-bucket + authority-contested | Craft (act) vs Knowledge (artifact); research DEFINITIONS normative | **YES** | real collision of names, distinct units |
| S2 | research/review as dispatch type-skills vs as pipeline method steps | duplicate-name, distinct-kind | Governance (dispatch control) vs Craft/Knowledge (artifact) | YES | **NOT real** — name hazard; never compete for authority |
| S3 | Arcanum registry/SIGILS.md vs domainspec docs/registry.md (sync-registry) | duplicate function, diff scope | Craft/Governance meta (tool index) vs Knowledge (concept index) | YES | real collision of "registry"; cross-repo no-owner gap |
| S4 | sync-registry vs definitions-governance vs feature-glossary vs AUTHORITY-MAP glossary | authority-contested + duplicate | all Governance over Knowledge | YES | partial real — global vs feature vs canonical all write terminology |
| S5 | audit-alignment vs code-tag-audit vs audit-layering | overlapping (drift) | all Governance | partially | mostly distinct (3 surfaces); only audit-alignment §4a vs generate-tests coverage is real |
| S6 | generate-tests vs audit-alignment §4a vs framework-unif "tests/claim≤proof" | multi-bucket | Craft (produce) ∩ Governance (gate) | **YES** | real seam at Craft/Governance boundary |
| S7 | invoke plan/design vs refine vs implementation-layering vs distill | overlapping front-doors | all Craft | no (1 bucket) but no-owner-arbitration of which to pick | name-distinct; real *selection* gap |
| S8 | paired-views/single-owner invariant vs definitions-governance vs AUTHORITY-MAP | authority-contested (meta) | Governance — the partition-enforcer itself | **YES, reflexively** | real & load-bearing |

**Counterexamples to a clean 3-partition:**
- **A (define/definitions, S1+S4+S8):** producing a definition is Craft; the canonical meaning is Knowledge; keeping it un-redefined is Governance — one cluster in all three buckets.
- **B (test catalogue, S6):** generate-tests produces TEST-SPEC (Craft); audit-alignment/claim≤proof gate it (Governance) — same artifact is product AND gate input.
- **C (cross-cutting, S8 + the vertical mechanisms):** framework-unification's own model = ONE pipeline (horizontal artifacts) + THREE mechanisms (typing, provenance, residue/gate) cutting VERTICALLY through every artifact. Governance is a vertical mechanism, not a peer of artifact-producing stages.
- **D (no-arbiter seams, S3+S7):** "registry" and the four vague-intent front-doors have no owner that arbitrates between colliding units; AUTHORITY-MAP resolves which *file* wins, not which *skill* owns a mutation or which entry-point to choose.

**Self-flagged bias (false-collision audit):** S2, S3-as-duplication over-counted (name hazards, not functional dupes); S5 mostly distinct. Real collisions/multi-bucket: S1, S4 (partial), S6, S8.

**Bottom line:** Knowledge & Craft are roughly a producer/product pair, nearly disjoint with discipline; **Governance is the wrong shape for a third peer bucket** — the corpus's own framework-unification model treats it as a *vertical mechanism over all artifacts*. Recommend **two axes (artifact buckets × cross-cutting mechanisms), not three sibling buckets.**

---

## Synthesizer (zig-zag turn 1) — Spivak, David

Drafted an 18-row verdict matrix + a PROPOSED two-axis taxonomy (Axis A artifact-lifecycle
Orient→Discover→Define→Design→Plan→Execute→Distill→Reflect; Axis B six "verticals" Route/Critique/
Validate/Trace/Observe/Govern), demoting Governance from peer bucket to vertical mechanism; named
"TΩ = preserve-both-poles-and-route-the-gap-to-a-single-owner" as the one recurring capability;
flagged a generative gap (T17). Mapped emergent types (interviewer→Orient, router→Route,
observer→Observe, validator→Validate, bridge→partial). Honesty ledger pre-flagged its weakest leaps
for the skeptics. (Full draft superseded by the corrected synthesis in findings.md.)

## Reviewers (zig-zag turn 1 — 3 skeptics, one gate each)

### S1 — Kuhn · precedent gate (4/5 build-from-owned wins)
- **interviewer → BUILD-FROM-OWNED:** scope-interview, interrogation/structured-interview-kits, domainspec-interview-scope/kits; DISCIPLINES.md `interview` (active-pattern). Not emergent.
- **two-axis FRAME → BUILD-FROM-OWNED, NOT novel:** `framework-unification/CONCEPT-MAP.md §"two axes"` (lines ~37–89), frontmatter `two-axis`, "one pipeline × three mechanisms (representation/communication/epistemology)", pipeline order LOCKED OQ-A owner decision 2026-06-16. The draft's "PROPOSED two-axis taxonomy" is reuse. Two corrections: (1) the owned vertical axis is THREE mechanisms, not the draft's SIX verticals (those are E2 capability types, not mechanisms); (2) Governance-as-vertical is inherited from E4 (research.md), not a synthesis novelty.
- **K/C/G → precedent-clean label, NO owner; 4 rival owned groupings** (DISCIPLINES, method-tiers, BUSINESS-ONTOLOGY Business/System/Bridge, METHOD phases). Demotion correct.
- **TΩ → BUILD-FROM-OWNED:** = E3 R1 (research.md) + CONCEPT-MAP I5 single-owner. Correction: **no `AUTHORITY-MAP` file in arcanum**; single-owner = CONCEPT-MAP I5 + paired-views. Name the fusion if you like, but it's a naming of an owned recurrence.
- **T17 generative gap → OVERCLAIM, narrow it:** author IS owned (whisper, text-only), design/plan owned (invoke), spec→code owned (domainspec-implement). Net precedent-clean gap = **portable, non-text, non-spec-bound** synthesize/prototype/negotiate/migrate.

### S2 — Gödel · non-vacuity gate → VERDICT: VACUOUS (as stated)
- Placed 30 shipped capabilities: **15/30 fit one slot cleanly; 15/30 break.**
- **Closed negatives (fit NO slot):** `whisper` (author/text producer — a parallel end-product lifecycle the axes omit; single fatal witness); `invoke` (multi-mode front-door spanning 3+ stages, a router-over-stages); the **view-triad** (ontology/system/engineer = three ownership LAYERS of one act, no axis coordinate).
- **Fit TWO+ slots:** definitions-governance & ontology-vault (Define∩Govern); test-derivation (Define∩Validate, draft concedes); **workflow-reflect / signal-observer / constitution-governance** — Reflect is a *consumer of Observe and driver of Govern*; A-stage Reflect vs B-vertical Observe/Govern is arbitrary (sharpest internal contradiction).
- **TΩ "explains everything, gates nothing" → unfalsifiable/vacuous** unless reframed as a discriminating predicate some capability FAILS.
- "4/5 emergent types are verticals" **refuted** — the emergent ones (whisper, view-triad, reflect/observe/govern loop) are exactly the unplaceable ones.
- **Smallest fix:** (a) admit a 2nd Axis-A lifecycle for end-products (whisper text, x-ray HTML); (b) collapse Reflect into the Observe→Govern loop; (c) model view-triad as an ownership-layer dimension; (d) reframe or drop TΩ.

### S3 — Wittgenstein · definitional-soundness gate → all 4 COLLAPSE
- **Two-axis model → COLLAPSE** to CONCEPT-MAP "one pipeline × three mechanisms" (owned, locked 2026-06-16). Permissible ONLY if called a reuse, never "the taxonomy's discovery."
- **Symmetry/recursion thesis + TΩ → COLLAPSE + TAUTOLOGY KILL:** "method of symmetries" = owned synthesis thesis; "recursion" = I9 verbatim; TΩ = symmetry-thesis + I9 + I5 relabeled, and as phrased is **true of every governed two-representation system → says nothing CyberAlchemy-specific** (terminal tautological KILL).
- **K/C/G (minus Governance) → COLLAPSE** to BUSINESS-ONTOLOGY Business/System(/Bridge) poles (≈ I10 phase segments); demoting Governance reveals the triad as a rename.
- **Six verticals → COLLAPSE + residual-definition weakness:** defined by negation ("not a stage") = no intension; where real, they re-cut the owned THREE mechanisms into six. Recommend: re-present as a citation/reuse map over CONCEPT-MAP axes + I1–I10 + BUSINESS-ONTOLOGY poles.

## Synthesizer (zig-zag turn 2 — accepted all corrections)

The writer revised to accept every skeptic objection: reframed the two-axis model as **build-from-owned**
(cite CONCEPT-MAP, locked 2026-06-16), NOT a discovery; corrected six-verticals → the owned **three
mechanisms** with capabilities mapped onto them; demoted TΩ from "discovery" to a fused owned recurrence
(I5+I9) failing the tautology test as stated (OD-4: reframe as a discriminating predicate or drop);
added the non-vacuity fixes (2nd end-product lifecycle for whisper/x-ray; view-triad as ownership-layer
dimension; Reflect folded into the Observe→Govern loop); narrowed T17 to portable non-text non-spec-bound
generation; fixed the AUTHORITY-MAP miscitation. Convergence reached. Final corrected synthesis in
[findings.md](findings.md).

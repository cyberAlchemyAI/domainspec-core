---
tags: [cyber-alchemy-space, capability-taxonomy, findings, knowledge-craft-governance, two-axis, reuse-map]
node_type: findings
is_session: false
layer: architecture
nature: reference
status: draft
created: 2026-06-18
dispatch_id: 2026-06-18-cyberalchemy-capability-taxonomy
dispatch_type: research
working_folder: research/cyber-alchemy-space/capability-taxonomy/
sources: [arcanum/, implementation/domainspec/, projects/framework-unification, projects/ontologize, cyberAlchemy/, .claude/skills/]
---

# Findings — CyberAlchemy capability taxonomy (corrected after 3-skeptic pass)

> **Honesty contract.** Every claim is tagged **BUILT** (on disk), **OWNED** (a skill/doc claims it,
> cited), **PROPOSED** (synthesis, not yet owned), or **OPEN** (owner must decide). The first draft
> sold a "two-axis taxonomy" as a discovery; a precedent / non-vacuity / definitional skeptic pass
> **retracted that framing**: the two-axis model is **already OWNED** by `framework-unification/CONCEPT-MAP.md`
> (locked 2026-06-16). This revision re-presents the work as a **citation/reuse map + capability census**,
> not a discovery. See [research.md](research.md) for the verbatim explorer + skeptic returns.

## Part 0 — The one-line answer

The repo's capabilities **already organize**, but **not** under Knowledge / Craft / Governance as three
sibling buckets. They organize under a model the repo **already owns**: `framework-unification/CONCEPT-MAP.md`'s
**one horizontal artifact pipeline × three vertical mechanisms** (representation/typing · communication/provenance ·
epistemology/residue-gate), locked 2026-06-16 (OQ-A). Knowledge↔Craft is the **producer/product split of that one
pipeline**; **Governance is one of the vertical mechanisms, not a third peer.** "interviewer", "router",
"observer", "validator", "bridge" are all **owned** already. The single honest net-new is a **generative gap**
(no portable synthesize/prototype/negotiate/migrate). [OWNED frame; BUILT census.]

## Part 1 — Build-from-OWNED (reuse as-is, do not re-vend)

1. **The two-axis structure is OWNED.** `framework-unification/CONCEPT-MAP.md §"The two axes"` (lines ~37–89):
   "**one pipeline** (a horizontal sequence of artifacts) and **three mechanisms** that cut *vertically* through
   every artifact" — representation, communication, epistemology. Pipeline order LOCKED (OQ-A, owner decision
   2026-06-16). **Anything calling this "two axes" is reuse, not discovery.** **OWNED.**
2. **Single-owner law is OWNED.** `CONCEPT-MAP.md` **I5**: "each concept/term has exactly one canonical home;
   no term defined twice, every stance decided once" — owner = `paired-views`, enforced by `review`. (Correction:
   there is **no `AUTHORITY-MAP.md` in arcanum**; single-owner lives in I5 + the view-triad. `implementation/domainspec/AUTHORITY-MAP.md`
   is the *domainspec* file-precedence doc.) **OWNED.**
3. **Recursive self-application is OWNED.** `CONCEPT-MAP.md` **I9**: "every stage is the same process at a
   different altitude; the pipe runs on itself." This is the recursion the user's "CyberAlchemy as method" names. **OWNED.**
4. **The intent↔reality / residue thesis is OWNED.** `cyberAlchemy/agentic-system-ontology-synthesis.md`:
   "the system is built to chase symmetry across translations… a residue-reduction system looking for broken
   symmetries"; the Business/System/Bridge pole-pair (deferring to `arcanum/BUSINESS-ONTOLOGY.md`). The
   gap-as-first-class-object (`drifts_from`, `claim≤proof`, residue) recurs at every altitude. **OWNED.**
5. **The capability census itself is BUILT** (E1): ~the Arcanum sigil set (formulae/transmutations/arcana/spells,
   indexed in `arcanum/registry/SIGILS.md`) plus the repo `.claude/skills` dispatch/anti-bias governance layer. The
   ~70 `gsd-*` and ~45 `domainspec-*` skills are **out of scope** (vendored / DomainSpec-product-bound, not
   CyberAlchemy capabilities). **BUILT.**

> **Scope note (auditor-added).** Two project-bound corpora were **out of scope as product-bound but introduce
> capability verbs not in the Arcanum census**: `domainspec-lean-formalization/` ships a **formal-proof + machine-verify**
> family (`writing-lean-proof`, `verifying-lean-build`, `mathlib-precedent-search`, `preparing-lean-pr`) — notably
> `verifying-lean-build` is a **machine-checkable proof gate**, a different shape from the assertion-level Validate
> family; and `validation/poker-team/` ships a `mars-research-*` **empirical-analysis-pipeline** (data→validated
> conclusions). If either is brought in scope, it adds genuinely new verbs (machine-gating, empirical-analysis). [BUILT, out-of-scope.]

## Part 2 — The capability census (what we already have)

A capability = an operating verb with a shipped owner. After de-duplicating mirrors, aliases, and compositions
(E1: path count over-counts true capabilities ~30–40%), the distinct verbs and their owners:

| Capability (verb) | Owners (BUILT/OWNED) | Pipeline-stage or vertical-mechanism | CyberAlchemy altitude (E3) |
|---|---|---|---|
| **Orient / interview** | scope-interview, interrogation (= structured-interview-kits), domainspec-interview-scope/kits; DISCIPLINES `interview` | stage (entry) | — |
| **Discover / research** | research-tower, robot-talks, research(dispatch), publication-research-pipeline | stage | R1 (gather the "actual") |
| **Define / ontologize** | ontology-vault, definitions-governance, feature-glossary, ontology-view, inventory, necronomicon | stage **+** representation-mechanism | R1 "meant" pole; I5 |
| **Design** | invoke(design), system-view, engineer-view, architecture-pattern-inventory, residuality-spec, spellcraft | stage | view-triad = R4 |
| **Plan / layer** | implementation-layering, invoke(plan), implementation-readiness | stage | — |
| **Execute** | task-session, domainspec-implement (spec-bound) | stage | — |
| **Distill** | distill, x-ray, skill-decomposer, test-derivation | stage / cross | R2 (altitude shift) |
| **Reflect / evolve** | workflow-reflect, refine, sigil-development | **consumer of Observe→driver of Govern** (one loop, not a clean stage) | R2; I9 |
| **Route / dispatch** | dispatch-spec, orchestrate, codex-goal-profile, subagents-strategy+register-dispatch+check-tension+research/review/experiment (ONE capability, 7 files) | **vertical** | R3 (router→type→form) |
| **Critique / tension** | check-tension, anti-bias-vector-composition, robot-talks, review, residuality-spec | **vertical** (→ epistemology mech) | R1 (claim vs proof) |
| **Validate / gate** | decision-gate, audit-alignment, experiment-harness, ux-evidence-validator, readiness; (heaviest family, E1: 12+) | **vertical** (→ epistemology mech) | R1 (gap-gate) |
| **Trace / provenance** | register-dispatch, close-session, craft, vault `## Connections` | **vertical** (→ communication mech) | R1 (residue ledger) |
| **Observe** | signal-observer, observability-setup, observed-invocation-loop, domainspec-emit-signals | **vertical** (→ communication mech) | R2 (per-run→cross-run) |
| **Govern / promote** | constitution-governance, decision-gate, definitions-governance, the I-invariant set | **vertical** (→ all mechs; the promotion gate) | I5; I9 ("govern the governor") |
| **Author (text/visual)** | whisper (text), x-ray (HTML) | **separate end-product lifecycle** (NOT the spec/build pipeline) | parallel pipeline |
| **Bridge / translate** | partial: @biz/@sys anchors, paired-views, domainspec-brownfield-translation | **vertical, NO continuous comparator** | R1 at the @biz↔@sys altitude |

**Reading.** Of E1's verb counts, **validate/distill/ontologize/govern/route ≈ 70%** of the catalog: the system is
a **knowledge-governance + verification machine**, not a generation machine (E1). The "governed multi-agent dispatch"
is **one** capability fragmented across 7 files, not 7 capabilities (E1, confirmed Kuhn).

## Part 3 — The taxonomy (reuse map, corrected for non-vacuity)

The seed Knowledge / Craft / Governance does **not** survive as three peers. Corrected structure, all reused from
owned models:

- **Axis A — the artifact pipeline (horizontal, producer→product).** Owned: CONCEPT-MAP Axis-1. Knowledge-flavored
  stages (Discover, Define, Distill) and Craft-flavored stages (Design, Plan, Execute) **alternate on one axis** —
  so "Knowledge vs Craft" is a producer/product *split of one pipeline* (≈ BUSINESS-ONTOLOGY intent vs realization),
  **not two buckets** (E4 "nearly disjoint"; Wittgenstein: collapses to Business/System). Order:
  `Orient → Discover → Define → Design → Plan → Execute → Distill`.
- **Axis B — three vertical mechanisms (applied to every artifact).** Owned: CONCEPT-MAP Axis-2 = **representation/typing
  · communication/provenance · epistemology/residue-gate.** The shipped *capabilities* serve these mechanisms:
  Route+Define-typing → representation; Trace+Observe → communication; Critique+Validate+Govern → epistemology.
  **Governance is here, as the promotion face of the epistemology mechanism — not a peer bucket** (E4-C, Kuhn, Wittgenstein).
  (Correction from draft: do **not** invent "six verticals" — that was a residual "not-a-stage" grab-bag (Wittgenstein).
  There are **three owned mechanisms**; the capabilities map *onto* them.)
- **A third dimension the pipeline needs — ownership layer.** The view-triad (ontology/system/engineer) is **not** one
  pipeline stage; it is three **ownership layers** of the Define+Design+Validate act (Gödel). Model it as a layer
  dimension, not a stage.
- **A second pipeline — end-products.** `whisper` (text) and `x-ray` (HTML) produce **end-product artifacts**, not
  spec/build intermediates; they sit on a **parallel producer lifecycle** the spec pipeline omits (Gödel: whisper is
  the single fatal witness against a one-pipeline placement).
- **Emergent types are all already owned and all map to a vertical** (Kuhn): interviewer→Orient stage; router→Route;
  observer→Observe; validator→Validate; bridge→Bridge(partial). None is net-new.

## Part 4 — Consolidated OPEN owner-decisions

| # | Decision | Status | Owner must decide |
|---|----------|--------|-------------------|
| OD-1 | **3-bucket vs 2-axis** | Two-axis model OWNED (CONCEPT-MAP, 2026-06-16); K/C/G has no owner, collapses to Business/System + a cross-cutter | **ANSWERED:** adopt the owned two-axis frame; demote Governance to the epistemology mechanism. Do NOT ship K/C/G as a discovered structure. |
| OD-2 | **Navigate / legibility (E2 type-10)** | Law-required (Ergonomics Is Governance, Quality-Bar close cond.) but **no enforcing owner** — legibility asserted, not gated | Fold legibility into a **Validate check** (build-from-owned, preferred) OR charter a Navigate gate (novel). Currently no owner. |
| OD-3 | **Bridge comparator (E2 type-15)** | Law-acknowledged gap: no **continuous** Business↔System drift comparator; System-3 Control is "manual trigger" (G11 roadmap). **Caveat (auditor):** `domainspec-lean-formalization`'s `verifying-lean-build` is an existing **machine-checkable gate** — the "no machine comparator" premise is partial, not absolute | **build-from-owned:** instantiate the existing `drifts_from`/residue detector (R1) — and the `verifying-lean-build` machine-gate pattern — at the @biz↔@sys altitude. Charter now or keep manual. |
| OD-4 | **Name/own "TΩ" (the recurring capability)** | TΩ = I9 + I5 + symmetry-thesis fused (Kuhn); **fails tautology test as stated** (true of every governed 2-representation system — Wittgenstein) | Either **reformulate as a discriminating predicate** (e.g. "emits a residue-ledger entry" — some capabilities fail it) or **drop the TΩ framing** and just cite I5+I9. Do not sell it as a discovery. |
| OD-5 | **Generative gap (T17)** | BUILT gap (E1): generative verbs are one-deep; **no portable synthesize / prototype / negotiate / migrate** | Decide: intentional (system governs generation done elsewhere) or a gap to fill? **Narrowed (Kuhn):** author IS owned (whisper, text-only), design/plan owned (invoke), spec→code owned (domainspec-implement). Net-clean gap = **portable, non-text, non-spec-bound** generation. |
| OD-6 | **No-arbiter seams (registry + front-doors)** | E4-D: two "registry" concepts (Arcanum tool-index vs domainspec concept-index) + 4 vague-intent front-doors (invoke/refine/implementation-layering/distill) with no entry-point arbiter | Assign a single owner to **entry-point selection** (a Route sub-decision). Currently unowned. |

## Part 5 — Verdict matrix (per candidate, corrected)

| candidate | owner / precedent | witnessed? | sound? | verdict | use-mode |
|---|---|---|---|---|---|
| two-axis taxonomy frame | CONCEPT-MAP §two-axes (2026-06-16) | yes | yes | **GO** | **build-from-owned** (NOT novel) |
| Knowledge/Craft/Governance as 3 peers | no owner; 4 rival owned groupings | — | **no** (collapses) | **KILL-as-structure** | — (use Business/System + mechanism instead) |
| Governance as vertical mechanism | E4-C + CONCEPT-MAP Axis-2 | yes | yes | **GO** | already-deployed |
| interviewer / router / observer / validator | scope-interview / dispatch-spec / signal-observer / decision-gate+audits | yes | yes | **GO** | already-deployed |
| TΩ (one recurring capability) | E3 R1 + I9 + I5 | yes (as invariant) | **no, as stated** (tautological) | **KILL-as-named-law** unless reframed | build-from-owned (cite I5+I9) |
| Navigate as standalone type | partial (E2 t10) | partial | disputed | **OPEN** → fold into Validate | build-from-owned |
| Bridge continuous comparator | partial (E2 t15) | partial | disputed | **OPEN** | build-from-owned |
| portable generative family | **no owner** (E1) | no | n/a | **GO-as-gap** | novel-attempt |

**Bottom line.** Nothing in the proposed taxonomy is a novel discovery; the organizing model was **owned and locked
two days before this dispatch**. The honest deliverable is a **reuse map** (capabilities → CONCEPT-MAP's pipeline ×
three mechanisms, with an ownership-layer dimension and a parallel end-product lifecycle) plus **one real net-new gap**
(portable generation) and **two law-acknowledged gaps** (Navigate-as-gate, Bridge-comparator). The user's
Knowledge/Craft/Governance intuition is *directionally* right but resolves to **producer/product (one pipeline) +
cross-cutting mechanisms**, which the repo already governs.

## Connections

| Document | Type | Description |
|---|---|---|
| [research.md](research.md) | `derives-from` | Verbatim explorer + skeptic returns. |
| [../findings.md](../findings.md) | `relates-to` | Prior architecture-unification findings (same cyber-alchemy-space study). |
| [../../../projects/framework-unification/CONCEPT-MAP.md](../../../projects/framework-unification/CONCEPT-MAP.md) | `cites` | The OWNED two-axis model + I1–I10 invariants. |
| [../../../cyberAlchemy/agentic-system-ontology-synthesis.md](../../../cyberAlchemy/agentic-system-ontology-synthesis.md) | `cites` | The OWNED symmetry/residue thesis + Business/System/Bridge. |

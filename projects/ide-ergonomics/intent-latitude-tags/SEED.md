# Tower Seed: Intent-Latitude Tags

Status: seeded (precedent sweep complete; two lanes not yet executed)
Date: 2026-06-18
Depth: standard
Owner: DomainSpec v2

## Underlying problem (solution-independent)

A model interpreting a prompt has no explicit signal for **how much latitude** it
has over any given span. So it drifts: it reads a span *too literally* (reproduces
or obeys something meant as flexible context) or *too freely* (paraphrases away
something that had to be exact, or pursues the literal words instead of the
intended outcome). DomainSpec specs and dispatches carry the same hazard — every
instruction silently mixes "do this exactly," "achieve this outcome however you
like," and "never cross this line," with nothing marking which is which.

## Hypothesis under test (Lane Z anchor)

Mark the **interpretation latitude** of a span with a small, closed tag vocabulary
(`[literal]` / `[goal]` / `[constraint]`) whose meaning is **grounded by a
validator contract**, not by the model re-inferring the bracket from the word
inside it. Grounding is the whole hypothesis: an ungrounded `[target-state]` tag
collapses into an ordinary prose header (see [FINDINGS.md](FINDINGS.md)); a
*validator-enforced* `[literal]` tag does something a prose header cannot, because
its force comes from the check, not the word.

## Primary sources (precedent sweep already ran — see FINDINGS.md)

- `precedent-owner` (concept): Searle & Vanderveken, *Foundations of Illocutionary
  Logic* (Cambridge UP, 1985) — the **Illocutionary Force Indicating Device
  (IFID)**: an explicit marker fixing the intended force of a span. This tower
  builds "an inline IFID for prompts" and must cite it, not claim it novel.
- `precedent-engineering`: ISO 24617-2 / DiAML (from DAMSL) — a standard for
  tagging spans with their communicative-intent role.
- `name-collision-to-disclaim`: Gmeiner et al., "Intent Tagging," CHI 2025
  (arXiv 2502.18737) — same term + `[label:value]` format, but content-bearing
  tags on a 2D canvas, not inline latitude markers.
- `failure-motivation`: prompt-defect taxonomy "Intent Misalignment" (arXiv
  2509.14404); spec-gaming (DeepMind/Krakovna); format-sensitivity
  (FormatSpread arXiv 2310.11324; IFEval arXiv 2311.07911).

Originating dispatch (full collected returns):
`domainspec-core/research/intent-annotation-tags/` (research + findings),
ledger row `2026-06-18-intent-annotation-tags`.

## Lane assignment

- **Lane Z (zig-zag):** Adopt grounded interpretation-latitude tags as the
  primitive. Build the concrete spec + validator contract ([SPEC.md](SPEC.md))
  for one DomainSpec span, then attack it: does the validator *mechanically*
  enforce, or does enforcement of `[goal]`/`[constraint]` degrade to an LLM-judge
  that re-imports the very drift the tag was meant to remove? Where does the tag
  earn its keep over a prose header, and where is it ceremony?
- **Lane A (alternatives):** Hold the problem (latitude is unsignalled) fixed;
  propose a genuinely different solution. Candidates: a **clarification loop**
  (model asks before acting on ambiguous latitude); **preference uncertainty**
  (Russell — the model treats the objective as uncertain rather than literal);
  **controlled natural language** (ACE/SBVR — restrict the grammar so latitude is
  unambiguous by construction, instead of tagging it); or **fitness
  functions / oracles** instead of `[goal]` spans. Argue why tags beat — or lose
  to — one of these for an agent that must verify "done."

## Authored artifacts (invoke define/design/plan)

Governed authoring pass over this tower lives in
[`development/`](development/): [SPEC.md](development/SPEC.md) +
[GLOSSARY.md](development/GLOSSARY.md) (define), [ARCHITECTURE.md](development/ARCHITECTURE.md)
(design, six-view), [IMPLEMENTATION-LAYERING.md](development/IMPLEMENTATION-LAYERING.md)
+ [WORK-PACK.md](development/WORK-PACK.md) (plan, L0 active). Research-only; next
route is `task-session` on the L0 work-pack after a promotion decision.

## Connection to sibling towers

- **[target-state](../../domainspec-v2/research/target-state/SEED.md):** the `[goal]` / `[target-state]`
  latitude tag *is* an inline form of that tower's "buildable target state." If
  target-state lands as a first-class artifact, `[goal]` is how a span points at
  it. The two towers should reconcile vocabulary before either promotes.
- **[spec-ontology-unification](../../domainspec-v2/research/spec-ontology-unification/SEED.md):** latitude
  could become an edge/annotation type in the typed spec graph rather than inline
  text — a Lane A candidate worth recording.

## Promotion boundary

Local research only. Adding a latitude-tag field/section to a DomainSpec template,
or wiring the validator contract into the v1 validator/runtime, requires a later
approved `task-session`. The grounding mechanism (a validator) is the load-bearing
claim — it must be demonstrated, not asserted, before promotion.

## Non-goals

- Shipping tags as "magic markers the model is trained on" — the FINDINGS kill the
  naive form explicitly.
- Treating the precedent sweep as a substitute for Lane A — an alternatives lane
  still owes a genuinely different solution to the same problem.

## Open residue (pre-execution)

- Is `[literal]` scoped to reproduced **content** only (mechanically checkable), or
  also to **instructions** (not mechanically checkable)? SPEC.md draws the line at
  content; Lane Z must test whether that scope is too narrow to be useful.
- For `[goal]`/`[constraint]`, is an LLM-judge an acceptable grounding, or does it
  fail the non-tautology bar because the judge drifts too? This is the tower's
  central open question.
- Per-span inline tags vs a separate latitude section vs a graph edge — which
  placement actually reduces author burden rather than adding ceremony?

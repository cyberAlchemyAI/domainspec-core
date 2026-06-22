---
tags: [ide, ergonomics, intent, prompt, latitude, validator, arcanum]
node_type: feature
layer: product, workflow
nature: research-plus-plan
status: research-backed; L0 PoC planned
created: 2026-06-18
merged_into_ide_ergonomics: 2026-06-19
---

# Intent-Latitude Tags

An **input-side** ergonomic primitive for the conversation surface. Every IDE
action card in this project so far works on the *output* side — detect a span the
agent produced or a transition the workflow reached, then route it to the right
owner. Intent-latitude tags work on the side before that: let the user mark **how
much latitude** the agent has over a span of their *own* message, so the agent (or
a post-hoc validator) reads it as intended instead of drifting.

## Why it belongs here

The project's thesis is low-friction, owner-safe human↔agent workflow. The
recurring failure it does not yet address is **intent drift** — the agent reading a
span too literally (paraphrasing away an exact string, or obeying flexible context)
or too freely (pursuing the literal words instead of the intended outcome). This is
the conversation-input analog of "route ambiguity": the user knows what they mean,
but the surface gives them no governed way to signal it.

Closed vocabulary, marking interpretation latitude:

- `[literal]` — reproduce/preserve exactly (latitude zero)
- `[goal]` — the outcome to achieve, wording free (latitude high)
- `[constraint]` — a line not to cross (latitude bounded)

## The owner-safe move (matches this project's model)

Like every other primitive here, the tag must **not** rely on the agent "just
understanding" a magic marker, and must **not** silently promote anything. The
enforcement lives in a **post-hoc validator** that produces only a draft verdict:

- `[literal]` → the validator diff-checks the span appears verbatim in output
  (STRONG, mechanical, no model). This is what makes the tag more than a prose
  header — the check exists independent of how the model read the bracket.
- `[goal]`/`[constraint]` → excluded from verbatim checks and routed to an oracle
  (FLAG-grade until fixture-validated — honestly weaker).
- A span with no available oracle is reported **unenforced**, never passed.

This is the same discipline as the rest of the project: a card/annotation may
*recommend* and *check*, but it produces draft artifacts and never promotes
canonical behavior without an owner route. See
[ERGONOMICS-OPPORTUNITIES.md](../ERGONOMICS-OPPORTUNITIES.md) §"Intent-Latitude
Annotation".

## Provenance and key result

This started as a precedent sweep (research dispatch
`2026-06-18-intent-annotation-tags`). The result, in one line: the *naive* form
(bare brackets the model reads off the word inside) **collapses** to existing
delimiter/content-tag practice; only the **grounded** form (validator-enforced
latitude) earns its keep. Cite the concept honestly — it is an "inline IFID for
prompts" (Searle & Vanderveken 1985), and disclaim the same-named Gmeiner et al.
CHI 2025 "Intent Tagging".

## Files

- [INTENT-LATITUDE-TAGS-PRODUCT-VIEW.pdf](INTENT-LATITUDE-TAGS-PRODUCT-VIEW.pdf) —
  shareable product-view brief; companion to the project's
  [IDE-ERGONOMICS-PRODUCT-VIEW.pdf](../IDE-ERGONOMICS-PRODUCT-VIEW.pdf). Source:
  [INTENT-LATITUDE-TAGS-PRODUCT-VIEW.md](INTENT-LATITUDE-TAGS-PRODUCT-VIEW.md),
  regenerate with `python3 build_product_view_pdf.py`.
- [SEED.md](SEED.md) — research seed, Two-Lane assignment, promotion boundary.
- [FINDINGS.md](FINDINGS.md) — precedent sweep: owners to cite, the tautology-kill,
  the falsifiable bar.
- [SPEC.md](SPEC.md) — the tag spec + validator contract (technical source).
- [development/](development/) — governed invoke authoring pass:
  [SPEC.md](development/SPEC.md) + [GLOSSARY.md](development/GLOSSARY.md) (define),
  [ARCHITECTURE.md](development/ARCHITECTURE.md) (six-view design),
  [IMPLEMENTATION-LAYERING.md](development/IMPLEMENTATION-LAYERING.md) +
  [WORK-PACK.md](development/WORK-PACK.md) (plan, L0 PoC active).

## Status and next route

- **Backed by research; L0 PoC planned, not built.** The L0 work-pack
  ([development/WORK-PACK.md](development/WORK-PACK.md)) is four SWUs ending at a
  kill condition: does grounded `[literal]` catch a paraphrased verbatim span that a
  prose header misses, *and* fire on real model output?
- **Next route:** `task-session` on `SWU-ILT-001..004`, gated on a go decision.
- **Open debt:** judge-grounding for `[goal]`/`[constraint]` (deferred to L2); the
  Lane A alternative (a clarification-loop / ask-before-acting primitive — which
  overlaps this project's "bounded conversation-transition card" MVP) still owed.

## Boundaries

- Research + planning only; no v1 template/validator mutation without a later
  approved `task-session`.
- Related work in DomainSpec v2 (the
  [target-state](../../domainspec-v2/research/target-state/SEED.md) and
  [spec-ontology-unification](../../domainspec-v2/research/spec-ontology-unification/SEED.md)
  towers) is referenced, not owned here.

# FINDINGS — Intent-Latitude Tags (precedent sweep)

Status: source-backed findings (research-only, not canonical)
Date: 2026-06-18
Owner: DomainSpec v2

Ported from the originating research dispatch
`2026-06-18-intent-annotation-tags` (3 tensioned explorers + 2 skeptics). Full
verbatim agent returns:
[`domainspec-core/research/intent-annotation-tags/research.md`](../../../research/intent-annotation-tags/research.md).
This file is the tower-local, self-contained summary that [SPEC.md](SPEC.md) builds on.

## One-line result

The *problem* (intent drift) is real and formally named; the *idea* of marking a
span's intended interpretation is **owned** (cite it); and the **naive form** —
bare brackets whose meaning the model reads off the word inside — **collapses** to
existing delimiter + content-type-tag practice. It becomes a genuine technique
only as a **grounded interpretation-latitude** marker. **Verdict: build-from-owned
(grounded form) / tautological-KILL (naive form).**

## Verdict matrix

| candidate | owner (precedent) | witnessed? | sound? | verdict | use-mode |
|---|---|---|---|---|---|
| **A. Naive inline intent tags** — free-form brackets (`[target-state]`) whose meaning the model infers from the bracketed word | IFID (1985), conceptual; Gmeiner CHI 2025 owns the term, adjacent | owner exists | **NO** — collapses to delimiter + content-type label; the bracket adds nothing a `Target state:` header doesn't | **KILL (tautological)** | typed negative |
| **B. Grounded interpretation-MODE tags** — fixed latitude vocabulary (`[literal]`/`[goal]`/`[constraint]`) whose meaning is fixed by a **validator/parser or fine-tune** | IFID (concept) + ISO 24617-2/DiAML (pattern); distinct from Anthropic/POML (content-type) and Gmeiner (canvas) | **YES** — latitude is an axis orthogonal to content-type | **YES**, only with grounding | **GO** | **build-from-owned** |

## Owners — cite, do not reinvent

1. **Searle & Vanderveken IFID (1985)** — *exact conceptual owner*: an explicit
   marker that fixes the intended force of a span. Frame the work as "an inline
   IFID for prompts."
2. **ISO 24617-2 / DiAML** (from DAMSL) — engineering lineage: a standard for
   tagging spans with their communicative-intent role in XML.
3. **Gmeiner et al., "Intent Tagging," CHI 2025** (arXiv 2502.18737) — owns the
   term + `[label:value]` format, but as content on a 2D canvas (slide decks),
   authored by CMU + Microsoft Research. **Disclaim by name** — readers will
   assume prior art from the term collision.
4. **Anthropic XML tags / Microsoft POML / OpenAI delimiters** — own role-tagging
   spans by *content-type*; the **wrong axis** for latitude. Anthropic: "no magic
   tag names" — tags work by delimiting + signalling content type via a
   descriptive word, not by being trained.

## Why the naive form collapses (the kill)

Witness (built by hand): `[literal] keep the disclaimer` produces no behavior that
`Verbatim — do not change: keep the disclaimer` does not, because both force the
same in-context inference from the same word. The bracket borrows 100% of its
force from the English word inside it → it collapses into existing OpenAI-delimiter
+ Anthropic-XML content-type practice. **Typed negative banked.**

## The falsifiable bar the grounded form must clear (Ashby's adversarial angle)

- **Requisite variety:** a fixed low-variety tag vocabulary cannot regulate an
  interpreter of effectively unbounded variety — the tag relocates the question
  from "what does this sentence intend?" to "what does the model take `[goal]` to
  mean *here*?" The grounding (a validator) is what supplies the missing variety:
  it fixes meaning by enforcement, outside the model's inference.
- **Format-sensitivity:** FormatSpread shows meaning-preserving format changes
  swing accuracy up to 76 points; IFEval shows even verifiable explicit
  instructions are obeyed ~70–80%. So **the model following a tag is not
  reliable** — only the **post-hoc validator check** is. This is why SPEC.md puts
  the load on the validator, not on the model honoring the bracket.
- **Honest scope:** mechanical enforcement is **strong for `[literal]`** (verbatim
  presence is checkable) and **weaker for `[goal]`/`[constraint]`** (degrades to an
  LLM-judge, itself drift-prone). SPEC.md states this per tag; it is the tower's
  central open question (SEED residue).

## Citation hygiene

One skeptic citation (`arXiv 2603.18976`, "5W3H Structured Prompting") was
**excluded as unverifiable** (implausible future ID). No claim here rests on it.
All other claims trace to primary sources in the originating dispatch.

# findings.md — Intent-annotation tags for prompts

**Goal (dispatch):** Does a technique of inline *intent-annotation tags* (e.g. `[target-state]`)
— bracketed markers that label the intended **interpretation role** of a span in a chat
message, to reduce *intent drift* (the model reading a span too literally, or in a totally
different role than meant) — already exist and can be used? Find the owner(s) + web evidence of
the drift failures that motivate it.

**One-line answer:** The *problem* is real, documented, and even formally named; the *idea* is
**owned** (you must cite it, not claim it novel); and the *naive form you proposed* (free-form
brackets whose meaning the model infers from the word inside) **collapses** to existing
delimiter + content-tag practice — it only becomes a genuine, non-redundant technique when the
tags mark **interpretation latitude** (`[literal]` vs `[goal]`) **and** their meaning is grounded
by a validator/parser or fine-tune rather than re-inferred in context. **Verdict: build-from-owned
(grounded form) / tautological-KILL (naive form).**

Every load-bearing claim cites the collected return in [research.md](research.md) it rests on
(E1=Liu, E2=Searle, E3=Ashby, S1=Tarski, S2=Wittgenstein).

---

## Verdict matrix

| candidate | owner (precedent) | witnessed? (non-vacuity) | sound? (definitional) | verdict | use-mode |
|---|---|---|---|---|---|
| **A. Naive inline intent tags** — free-form brackets (`[target-state]`, `[constraint]`) whose meaning the model reads from the bracketed English word | Searle & Vanderveken **IFID** (1985), conceptual [S1, E2]; Gmeiner et al. **"Intent Tagging"** CHI 2025 owns the term + `[label:value]` format but adjacent [S1, E1] | owner exists | **NO** — collapses to "delimiter + content-type label" (Anthropic XML / OpenAI delimiters); the bracket adds nothing a `Target state:` prose header doesn't, because its force is borrowed from the word inside [S2] | **KILL (tautological)** | typed negative (below) |
| **B. Grounded interpretation-MODE tags** — a fixed latitude vocabulary (`[literal]` = reproduce/satisfy exactly · `[goal]` = outcome, wording free) whose meaning is fixed by a **validator/parser or fine-tune**, not by in-context inference | **IFID** (1985) for the concept [S1, E2]; **ISO 24617-2 / DiAML** for the engineering pattern [E2, S1]; distinct from Anthropic/POML (content-type axis) and Gmeiner (content-bearing canvas tags) [S1] | **YES** — "interpretation latitude" is a real axis orthogonal to content-type; `<instruction>` vs `<context>` marks *what kind of content*, `[literal]` vs `[goal]` marks *how much latitude* [S2] | **YES**, *only* with the grounding mechanism [S2] | **GO** | **build-from-owned** |

---

## The owners (cite these — the idea is not novel)

1. **Conceptual owner — Illocutionary Force Indicating Device (IFID).** Searle & Vanderveken,
   *Foundations of Illocutionary Logic* (Cambridge UP, 1985). An IFID is exactly "an explicit
   marker that fixes the illocutionary force / intended uptake of a span" — read-this-as-a-directive
   vs a-commitment vs a-question — built on Austin's explicit performatives ("I hereby…", "I am
   asking, not ordering"). This is the genuine ancestor of "mark the intended reading of a span";
   claiming novelty on that move is a precedent miss [S1, E2]. **Frame the work as "an inline IFID
   for prompts."**
2. **Engineering owner of span-intent tagging — ISO 24617-2 / DiAML** (descendant of DAMSL): an
   international standard that segments dialogue and tags each span with its **communicative
   function** (intent role) in XML. Prior art that a tagging scheme exists; but it is descriptive
   post-hoc analyst annotation, not author-written inline drift control [E2, S1].
3. **Term + format collision you must disclaim — Gmeiner et al., "Intent Tagging"** (CHI 2025,
   arXiv 2502.18737). Uses the literal term *intent tags* and a `[label: value]` bracket format,
   but as **content-bearing tags on a 2D canvas for slide-deck generation** — the tag *is* the
   intent payload, not metadata labeling how to read a surrounding span. Authors are **CMU +
   Microsoft Research, not Autodesk** (explorer correction) [S1, E1]. A reader will assume prior
   art from the name; distinguish explicitly.
4. **Closest deployed surface, wrong axis — Anthropic XML prompt tags / Microsoft POML / OpenAI
   delimiters.** These own "role-tag a span in a prompt," but on the **content-type** axis
   (`<instruction>`/`<context>`/`<task>`), not the **interpretation-mode** axis. Anthropic states
   there are "no magic tag names" — the tag works by delimiting + signaling content type via a
   descriptive English word, not by being trained [E1, S2].

## The problem is real and named (cite these to motivate the work)

- **"Intent Misalignment" / "Ambiguous Instruction"** — formal prompt-defect taxonomy
  (arXiv 2509.14404): "the prompt does not reflect the true user intent… the model addresses the
  wrong problem." This is precisely intent drift, already named [E1].
- **Specification gaming / King-Midas** — CoastRunners (loops buoys, never finishes the race),
  Tetris pause-to-never-lose, Q*bert suicide loop: the system satisfies the *literal* spec and
  misses the *intended* goal [E3]. DeepMind / Krakovna curated list.
- **Goal misgeneralization with a *correct* reward** (DeepMind 2210.01790): the literal-vs-intended
  gap survives even a perfectly specified objective — a warning that tags fix specification, not
  alignment [E3].

## Why the naive form fails — and the falsifiable bar the grounded form must clear

Ashby's adversarial angle and Wittgenstein's collapse-test converge: a fixed, low-variety tag
vocabulary cannot regulate an interpreter whose interpretive variety is effectively unbounded
(**Law of Requisite Variety**; the tag relocates the question from "what does this sentence
intend?" to "what does the model take `[target-state]` to mean *here*?") [E3]. Empirically,
structure is itself format-sensitive — **FormatSpread** shows meaning-preserving format changes
swing accuracy up to 76 points (arXiv 2310.11324), and **IFEval** shows even verifiable explicit
instructions are followed only ~70–80 % (arXiv 2311.07911) [E3]. Witness (built by hand, S2):
`[literal] keep the disclaimer` produces no behavior that `Verbatim — do not change: keep the
disclaimer` does not, because both force the same in-context inference from the same word [S2].

**For the grounded form (B) to earn its keep, it must:** (1) ground tag meaning in a
parser/validator or fine-tune, not in-context inference — e.g. `[literal]` spans are extracted
and diff-checked against the output, `[goal]` spans are excluded from verbatim checks [S2];
(2) survive an A/B (semantics held constant, tagged vs prose-header) showing a real drop in
misinterpretation — currently unmeasured, and FormatSpread is the right methodology and presently
cuts against unmotivated structure [E3]; (3) target *interpretation* drift (the latitude axis),
not merely *boundary* drift (where-input-starts), which delimiters already solve [E3, S2].

## Typed negative (banked)

**Candidate A (naive inline intent tags) — KILL: tautological.** What it would have contributed:
a lightweight, training-free way to pin intent by bracketing spans. The exact fact that zeroed it:
the bracket's meaning is read from the English word inside it, so it produces no behavior a plain
delimited prose header of the same word does not — it collapses into existing OpenAI-delimiter +
Anthropic-XML content-type-tag practice (Anthropic: "no magic tag names") [S2].

## Recommendation

Build **Candidate B**, not A. Concretely: define a *small, closed* interpretation-latitude
vocabulary (start with two values — `[literal]` / `[goal]`, optionally `[constraint]`), and
**ground it with a mechanism** (a validator that enforces `[literal]` spans verbatim and exempts
`[goal]` spans; or a system-prompt/fine-tune convention with a stated contract) so the tag's
meaning does not depend on the same drift-prone inference it is meant to prevent. **Cite it
honestly** as "an inline IFID for prompts" (Searle & Vanderveken 1985), note the DiAML/DAMSL
span-intent-tagging lineage, and explicitly disclaim the same-named Gmeiner et al. CHI 2025
"Intent Tagging." Do **not** ship it as "magic tags the model understands" — ship it as *a
discipline that forces the author to name interpretation latitude, backed by enforcement*.

## Citation-check note (final_approver = parent)

All load-bearing claims trace to a collected return in [research.md](research.md) (primary
sources: Anthropic/OpenAI docs, arXiv 2502.18737 / 2509.14404 / 2210.01790 / 2310.11324 /
2311.07911, ISO 24617-2, SIL/SEP on IFID, DeepMind/Krakovna spec-gaming list). **Excluded as
unverified:** S2's citation `arXiv 2603.18976` ("5W3H Structured Prompting") — the ID is a future
(2026-03) / implausible identifier and could not be confirmed; no claim here rests on it.

# Product View: Intent-Latitude Tags

_Companion to the IDE Ergonomics Product View  |  input-side ergonomic primitive for the conversation surface  |  status: research-backed, L0 proof-of-concept planned  |  2026-06-19_


## One-Sentence Product

Intent-Latitude Tags let a user mark how much freedom the agent has over a span of their own message - reproduce it exactly, achieve this outcome however, or never cross this line - and a post-hoc validator checks the agent's output against those marks. It is the input-side companion to the IDE Ergonomics routing cards: those route what the agent produced; this constrains how the agent reads what you meant.


## The Problem: Intent Drift

You write a prompt. The agent reads one span too literally - it obeys an aside as an instruction, or reproduces context you meant as flexible. It reads another span too freely - it paraphrases away a legal disclaimer that had to stay exact, or chases the literal words instead of the outcome you wanted. You knew what you meant; the surface gave you no governed way to say it. This is the conversation-input analog of route ambiguity, and it is named in the literature ("Intent Misalignment"; "specification gaming").


## What The Product Is

A one-tap latitude annotation over a selected span, plus a validator that turns the mark into a check.

| Tag | Means | The validator does | Strength |
| --- | --- | --- | --- |
| [literal] | Reproduce / preserve exactly | Diff-checks the span appears verbatim in output | STRONG (no model) |
| [goal] | Outcome to achieve, wording free | Excludes from verbatim checks; routes to a rubric/oracle | WEAK (flag-grade) |
| [constraint] | A line not to cross | Checks output does not violate it | MEDIUM |

The load-bearing rule: the tag's force lives in the validator, never in the agent "understanding" a magic marker. An ungrounded tag is just a prose header re-skinned - which is why naive bracket tags add nothing.


## What People Gain

| Gain | Before | With Intent-Latitude Tags |
| --- | --- | --- |
| Less misread intent | The agent guesses how literally to take each span. | The user marks latitude once; the check enforces it. |
| Exact strings stay exact | A disclaimer or ID gets quietly paraphrased. | [literal] spans are diff-checked verbatim; drift is caught. |
| Honest uncertainty | "It probably followed the prompt." | Unenforceable spans are reported, never silently passed. |
| No false confidence | Structure is assumed to fix interpretation. | Strong vs flag-grade is labelled on every check. |


## How It Works

```text
selected message span
  -> latitude annotation ( [literal] / [goal] / [constraint] )
  -> agent produces output
  -> post-hoc validator checks each tagged span
  -> draft verdict: PASS / FAIL / FLAG / unenforced
  -> nothing canonical or runtime is promoted
```


## Why The Naive Version Fails (and what we cite)

A precedent sweep killed the obvious version. Bare brackets whose meaning the agent reads off the word inside collapse to existing delimiter and content-tag practice: "[literal] keep the disclaimer" does nothing that "Verbatim - do not change: keep the disclaimer" does not. Only the grounded form - latitude enforced by a validator - earns its keep. Cite the idea honestly: it is an "inline IFID for prompts" (Searle & Vanderveken, 1985), and it must be distinguished by name from the same-named Gmeiner et al. CHI 2025 "Intent Tagging" (a different, canvas-based system).


## MVP Shape: the L0 proof

The first proof is not an IDE extension and not all three tags. It is the cheapest falsifier: a pure parser plus the [literal] verbatim check, run over a fixture set, with no model required. Four small units (SWU-ILT-001..004) end at one decision.

| Unit | Builds | Done when |
| --- | --- | --- |
| SWU-ILT-001 | Tag parser with author-time errors | parses valid input; rejects unbalanced / overlap / unknown |
| SWU-ILT-002 | [literal] verbatim check + normalize | paraphrase -> FAIL; intact -> PASS |
| SWU-ILT-003 | Fixture set + runner (the kill condition) | green on cases; >=1 real-model output captured |
| SWU-ILT-004 | L0 decision note | states continue or kill, with the evidence |


## How We Will Test It (the kill condition)

The L0 proof answers one question:

> Does grounded [literal] enforcement catch a paraphrased verbatim span that a prose header would miss - AND does that check ever fire on output a real model actually produces?

- If yes: the grounded form is real; promote to L1 ([goal] exclusion) and the judge question (L2).
- If the check never fires in practice: the tag layer is ceremony - kill it. A clean kill is a successful, cheap result.


## Boundaries and Open Debt

- Research and planning only; no validator/runtime change without an approved task-session.
- Judge-grounding for [goal]/[constraint] is deferred (the central open question) - kept flag-grade until fixture-validated.
- Lane A alternative still owed: a clarification loop that asks before acting, which overlaps this project's bounded conversation-transition card MVP. Compare before promotion.
- Full artifacts: see intent-latitude-tags/ (SEED, FINDINGS, SPEC, development/).

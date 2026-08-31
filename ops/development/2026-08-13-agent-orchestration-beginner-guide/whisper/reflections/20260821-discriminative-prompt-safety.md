# Whisper Reflection Sidecar — Discriminative Prompt Safety

## Reflection Context

- Sigil: `whisper`
- Tier: spell
- Reflection trigger: manual
- User correction: the first choice was too obvious; apply the same reasoning to the other cards and make the lesson reusable by Whisper
- Signals reviewed: one operator correction, one Recovery 006 jury, 11 interactive question cards, and one read-only observer pass
- Observer pass: subagent
- Authority effect: none

## Evidence And Inference

Usage evidence is deliberately narrow. The operator identified answer leakage,
and the Recovery 006 jury independently warned that dialogue or explanatory
voices can cue an answer before the learner acts. No intended-reader rationales,
think-aloud sessions, answer distributions, or transfer results exist yet.

The observer found artifact-level cue risks: 8 of 11 correct choices were
strictly the longest choice; in the eight three-choice cards, the correct answer
was last six times and first zero times; several pre-attempt surfaces stated the
relation later repeated by the correct choice. These are review signals, not
proof of learner behavior.

## Question-Level Findings And Applied Response

| Question | Observed risk | Applied response |
| --- | --- | --- |
| `choose-one` | setup and correct choice both said one inspectable report | concrete multi-cause incident; both work shapes plausible; feedback distinguishes complexity from a required judgment boundary |
| `choose-two` | “two reviewers” and “separately” disclosed the answer | concrete non-substitutable release concerns without naming the route; feedback reveals why attribution must remain separate |
| `prove-state` | premise named terminal closeout and missing admission | observable log facts plus parallel adjacent-state status notes |
| `relay-predecessor` | “every required result” mirrored “all required checked records” | concrete partial evidence set; options represent return, admission, and join transitions |
| `relay-limit` | heading stated that a gate cannot start work | changed release case; alternatives are plausible neighboring transitions |
| `code-boundary` | field name and inspector disclosed the answer | honestly labeled recognition check testing the relation between positive and negative scope |
| `code-owner` | owner cards negated both distractors | application sequence with parallel owner allocations; retained as taught-map application rather than comprehension proof |
| `fail-code` | error labels encouraged lexical matching | asks for the missing causal event; error name appears only in feedback |
| `fail-boundary` | context stated the rule and distractors were caricatures | neutral broken-history setup plus three plausible recovery policies |
| `lab-claim` | expected-result prose denied both distractors | concrete output inventory and three claim-ceiling statements |
| `transfer-start` | setup repeatedly stated that worker input was missing | concrete owner handoff; asks which exact causal transition remains absent |

All question IDs, hidden values, expected answers, form controls, repository
paths, commands, scripts, and navigation bindings remain unchanged. Existing
answer order was preserved because it is part of the accepted interaction
surface; the clustering signal remains a future control-design concern.

## Reusable Lesson Applied To Whisper

Canonical Whisper now requires `discriminative_prompt_safety` for scored
interactions. The audit records the target distinction, pre-attempt disclosures,
distractor misconceptions, choice parity, a counterfactual switch,
feedback relation, and final status. It also separates intentionally
`recognition_only` prompts from discrimination, transfer, or comprehension
evidence.

Static lint may flag overlap, length, position, absolute-language, and
formal-token cues. Human editorial judgment retains authority over plausibility,
pedagogy, and whether the question measures the intended distinction.

## Rejected Changes

- No product story, mandatory analogy, or guide-specific prose was copied into public Arcanum.
- No machine pedagogy score or automatic comprehension claim was introduced.
- No control IDs, expected answers, scripts, commands, accepted scaffold, receipt, rendered sibling, deployment, or Git history was changed.
- No recognition check was relabeled as comprehension evidence.

## Contract Preservation

- Core Whisper lifecycle preserved: yes
- Compatibility impact: minor additive validation requirement for scored prompts
- Reflection outcome: targeted update
- Next manual review: after intended beginners provide rationales and a changed-case transfer answer, or after three related prompt-safety corrections

## Validation

- Status: pass for the bounded copy and contract update
- HTML binding parity: pass for 11 question IDs, expected answers, input names, values, and control order; 75 element IDs, four command blocks, and the complete script block remain byte-identical to the accepted rendered sibling
- Cue audit: correct choice uniquely longest reduced from 8 of 11 cards to 0 of 11; answer-position order remains unchanged and is not claimed as resolved
- Browser behavior: pass at 390×844 and 1280×900 across all seven lessons; wrong-answer feedback, progressive reveals, all expected controls, accessible legends/labels/live regions, runtime errors, and horizontal overflow checked
- Canonical/generated parity: pass; canonical Whisper README and both generated README bodies have SHA-256 `c0aa00200ce950cf4eecdc240056c5cd60cd64a50c2e114c44d2add171000d84`
- Canonical checks: Markdown links, generated-package idempotence, experiment-fixture JSON, public/private-language sweep, and scoped whitespace checks pass
- Revised guide: SHA-256 `a8bd3398aa6a8e6f72717ac019895287ddc1dde6285f27d140df58925d6fd3cf`, 115,829 bytes
- Claim ceiling: this pass does not establish intended-reader comprehension, rationale quality, transfer, transport proof, publication, or deployment

---
id: cogtoolslab-complete-corpus-research-strategy-result-synthesis
kind: query
type: synthesis
title: CogTools Lab complete-corpus research strategy result
updated: 2026-08-07
status: candidate
confidence: high
dispatch_id: 2026-08-07-cogtoolslab-complete-corpus
dispatch_type: research
working_folder: research/2026-08-07-cogtoolslab-complete-corpus-program
tags:
  - inventory
  - strategy-result
  - dispatch
  - subagents
  - research
  - exact-binding
  - claim-le-proof
  - non-authority
sources:
  - research/2026-08-07-cogtoolslab-complete-corpus-program/dispatch-sheet.json
  - research/2026-08-07-cogtoolslab-complete-corpus-program/DISPATCH-ROUTE.json
  - research/2026-08-07-cogtoolslab-complete-corpus-program/STRATEGY.md
  - research/2026-08-07-cogtoolslab-complete-corpus-program/strategy-inventory-packet.json
  - research/2026-08-07-cogtoolslab-complete-corpus-program/CHECK-TENSION.md
  - research/2026-08-07-cogtoolslab-complete-corpus-program/material-strategy.json
  - research/2026-08-07-cogtoolslab-complete-corpus-program/confirmation.json
  - research/2026-08-07-cogtoolslab-complete-corpus-program/research.md
  - research/2026-08-07-cogtoolslab-complete-corpus-program/EVIDENCE-CLOSURE.md
  - research/2026-08-07-cogtoolslab-complete-corpus-program/orchestrate/run-1/partial-wave-result.json
  - research/2026-08-07-cogtoolslab-complete-corpus-program/orchestrate/run-1/evidence-validation.json
  - https://cogtoolslab.github.io/papers.html
  - https://cogtoolslab.github.io/teaching.html
  - https://cogtoolslab.github.io/research.html
selectors:
  - '#p1-trigger-and-program-boundary'
  - '#lanes-groups-and-subagents'
  - '#dependency-flow'
  - '#gate-confirmation-registration-and-ledger-state'
  - '#inventory-preflight'
  - '#partial-run-result'
  - '#next-human-action'
evidence_card_ids: []
evidence_set_ids: []
residue:
  - dispatch-closed-error
  - sixty-five-publication-byte-bindings-observed
  - thirty-six-modern-semantic-rows-unclosed
  - historical-and-teaching-lanes-not-run
  - one-hop-teaching-reading-count-unknown
  - inaccessible-or-mutable-teaching-surfaces-may-remain
  - no-findings-produced
  - inventory-index-sync-pending-tooling-repair
---

# CogTools Lab Complete-Corpus Research Strategy Result

This is a non-authority Inventory read model of a confirmation-ready strategy.
It does not confirm, register, execute, publish, promote, or establish the
completeness or correctness of the later research result.

## P1 trigger and program boundary

Dispatch is required because the live publication surface directly lists 90
papers, the public teaching surfaces may add a distinct one-hop reading corpus,
and completeness plus interpretation require independent attacks. The frozen
program has three source tiers:

1. all 90 PDFs linked directly by `papers.html` in the run snapshot;
2. all papers explicitly named by the five public one-hop teaching or syllabus
   surfaces, deduplicated against the publication list; and
3. the framing on `research.html`, which exposes no additional direct paper
   links in the preflight snapshot.

Recursive bibliographies and cited-by graphs are excluded. Complete means the
frozen site snapshot, not every past or future CogTools Lab paper. Durable
outputs retain citations, access receipts, digests, selectors, paraphrased
capsules, and residue; they do not commit or republish PDF bytes.

## Lanes, groups, and subagents

- **Explorers, four parallel lanes:** Graeme Halford covers the 36 publications
  from 2024--2026; Andrew Saxe covers the 29 publications from 2021--2023
  through benchmark-shift reconstruction and developmental-method transitions;
  Gregory Bateson covers the 25 publications from 2009--2020 with attention to
  historical terminology; Herbert Simon covers seven courses, five linked
  one-hop teaching surfaces, deduplicated readings, and the research framing.
- **Synthesizer:** Stafford Beer reconciles the 90 publication rows, teaching
  deduplication, temporal and thematic mappings, contradictions, and a
  cognitive-tools crosswalk without treating the corpus as one theory.
- **Reviewers, three parallel attacks:** Ian Hacking attacks precedent and
  theoretical ownership; Karl Popper attacks count, digest, reread,
  deduplication, and failure-mutant reproducibility; Willard Van Orman Quine
  attacks definitions and the boundaries among paper, corpus, cognition, and
  formal analogy.
- **Writer:** Peter Senge writes `findings.md` only after exact-binding evidence
  closure and cannot manufacture missing paper evidence.
- **Auditor:** Martin Brandenburg independently audits completeness, copyright,
  and claim ceilings and may authorize at most one bounded writer revision.

The explorer group is anti-biased across temporal and source-corpus
disagreement. The reviewers are anti-biased across precedent, non-vacuity, and
definition/scope disagreement.

## Dependency flow

The four explorer lanes run in parallel, then join at the synthesizer. The
synthesizer and three reviewers have one bounded zig-zag cycle; one bounded
feedback edge may return missing identity, access, digest, or selector work to
the relevant explorer. Exact-binding evidence closure gates the writer. The
auditor follows the writer and may return one bounded evidence-preserving edit.
The parent remains final approver.

## Gate, confirmation, registration, and ledger state

- The schema-`0.8.0` sheet passes deterministic registrar validation at SHA-256
  `40057058d95e90515ce04d43a508b05e1e860cefaa8069faf98314cca33dd988`.
- The material projection SHA-256 is
  `203623ea0fd112718bacffb81d9ad4dccceb3a47d59e3ab60db5e6c0e0727a21`.
- Dispatch Spec validation passes and retains
  `requires_user_permission` authorization.
- Two independent tension checks return `PASS/PASS` on the current sheet digest.
  Their initial shared rejection of a cloned explorer lens and the exact repair
  are preserved in `CHECK-TENSION.md`.
- Human confirmation was received for the unchanged material strategy under
  handle `confirmation-cogtoolslab-40057058-20260807`.
- Registration was appended exactly once under schema `0.8.0`.
- Orchestrate run 1 closed fail-closed in the explorer wave. Two explorers
  spawned, joined, and closed; the third native spawn failed on the host agent
  thread limit, and the fourth was not attempted.
- The middle lane closed 29 paper rows. The modern lane bound 36 URLs, media
  types, byte counts, and digests but blocked all semantic capsules and exact
  selectors. Historical and teaching lanes did not run.
- Evidence closure is `blocked`; no synthesizer, reviewer, writer, auditor, or
  `findings.md` was admitted.
- The dispatch ledger has exactly one close row with `exit_reason: error`.

## Partial run result

`research.md` preserves the two verbatim explorer returns. Together they bind
65 live publication rows at the byte level. Only the 29 middle-period rows carry
paper-read capsules and bounded selectors. The 36 modern rows must not be used
for semantic synthesis until re-read with a PDF extraction path. The local
runtime does expose `pypdf` and `pdfminer`, despite lacking command-line PDF
utilities, but that diagnostic does not retroactively repair the closed run.

`EVIDENCE-CLOSURE.md`, the partial-wave receipt, and causal event validation
preserve the exact block. No PDF bytes were retained.

## Inventory preflight

The root machine index is lookup-ready with 301 entries, zero failures, 146
inherited historical-tag warnings, and partial source coverage. Selected
adjacent evidence covers structural teaching review, operational/formal/analogy
non-collapse, the boundary between an agent pretest and human comprehension,
and exact-binding research precedent. Selective-promotion comprehension,
high-attention models, and dispersed cartography were excluded because they do
not own this corpus.

No Inventory entry owns CogTools Lab or this corpus. Therefore the live pages,
not Inventory, own enumeration; exact source rows own paper evidence; and
comprehension claims remain separate from formal or computational analogy.
`strategy-inventory-packet.json` preserves the selected and excluded records,
selectors, sources, gaps, and residue.

## Next human action

Construct a fresh replay-safe recovery strategy only after native agent capacity
is available. Do not reopen or silently retry the closed action identifiers.

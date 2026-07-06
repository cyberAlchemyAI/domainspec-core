---
tags: [research, strategy-result, dispatch, subagents, ai-assurance, certification-readiness, auditability, attestation, verifier, bp]
node_type: strategy
is_session: false
layer: research
nature: proposal
status: confirmed
created: 2026-07-06
dispatch_id: 2026-07-06-ai-assurance-certification-vocabulary-research
---

# AI Assurance / Certification Vocabulary Research Strategy

## P1 Trigger Decision

Dispatch is justified. The question combines more than three corpora and lenses:
repo-local vocabulary, external standards/regulatory vocabulary, formal verifier
machinery, operational governance POCs, and investor BP positioning. It also
benefits from isolation and parallelism because "certification" can easily
overclaim if standards language, proof language, and product readiness language
are collapsed.

## Goal

Determine the repository's strongest AI assurance/certification vocabulary and
evidence base: find explicit and implicit terms around certification,
conformity, auditability, assurance, attestation, verifier, correctness, trust,
quality management, documentation, logs, traceability, readiness, governance
evidence, ISO/IEC 42001, NIST AI RMF, and EU AI Act-style compliance pressure;
then map how the existing POCs compound into a credible investor BP claim
without overclaiming certification or correctness.

## Lanes / Groups

### Explorers

Parallel, robot-talks enabled. Anti-bias axis: composite source-corpus +
methodology + temporal-prior. Purpose: discover hidden local vocabulary and
align it to standards pressure without importing claims the repo does not own.

- van Lamsweerde, Axel - requirements/compliance standards corpus, modern
  external alignment.
- Turing, Alan - formal correctness/verifier/attestation corpus,
  computational/formal methodology.
- Ashby, W. Ross - operational governance/control corpus, systems methodology.
- Shannon, Claude - semantic/information-lineage repo term mining, mixed
  temporal prior.

### Synthesizer

Sequential after explorers. Simon, Herbert reconciles explorer returns into a
candidate thesis, vocabulary map, and assurance/certification ladder.

### Reviewers

Parallel, robot-talks enabled. Anti-bias axis: attack-vector. Purpose:
adversarially test the candidate thesis.

- Popper, Karl - precedent gate.
- Taleb, Nassim Nicholas - non-vacuity gate.
- Quine, Willard Van Orman - definitional-soundness gate.

### Writer

Drucker, Peter writes `findings.md` only.

### Auditor

Brandenburg, Martin audits `findings.md` only and is the final approver.

## Dependency Flow

`explorers -> synthesizer -> reviewers -> writer -> auditor`

Edges:

- `explorers -> synthesizer`: sequential.
- `synthesizer -> reviewers`: zig-zag, `loop_cap: 2`.
- `synthesizer -> explorers`: feedback, `loop_cap: 1`, only if coverage is
  materially missing.
- `reviewers -> writer`: sequential.
- `writer -> auditor`: sequential.
- `auditor -> writer`: feedback, `loop_cap: 1`.

## Gate / Ledger State

Check-tension gate returned double PASS:

- Checker: `019f35d8-548c-7630-85a7-fa67654d47cf` (Mendel) - PASS.
- Reviewer: `019f35d8-5542-7cf3-bb84-859db390e6b0` (Lovelace) - PASS.

Human confirmation received on 2026-07-06. Dispatch is ready to register and
run. Ledger row must be appended through the deterministic appender before
subagents are launched.

## Expected Outputs

- `research.md`: explorer returns and robot-talks positions, preserved by the
  strategist.
- `findings.md`: cited synthesis, vocabulary map, standards-alignment table,
  compounding POC thesis, evidence grades, forbidden claims, and next witness
  queue.

## Early Local Vocabulary Hints

Before the dispatch run, a narrow parent-side term census surfaced likely
candidate wording:

- `AI assurance`
- `audit readiness`
- `attestation`
- `verifier`
- `traceability`
- `conformity`
- `governance proof package`
- `readiness gates`
- `evidence/receipt bundle`

These hints are not findings. The dispatch must verify them against source
evidence and reviewer gates.

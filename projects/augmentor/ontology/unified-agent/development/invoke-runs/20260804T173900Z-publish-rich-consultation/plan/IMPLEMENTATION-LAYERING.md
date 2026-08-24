---
module: augmentor-rich-consultation-publication
version: candidate-0.1.0
status: planned
updatedAt: 2026-08-04
docType: implementation-layering
---

# Implementation Layering

## Target and scope

- Target: rich Augmentor consultation publication
- Scope: deployment workflow spanning page, read-only API, neutral bundle, and
  protected production route
- State: brownfield, partially deployed

## L0 — Trustworthy release closure

After this layer, the candidate packager proves that the runtime receives every
file required by family `1.1.0`, and no external transport has occurred.

- Repair required-file checks and copy closure.
- Bind release identity to the whole candidate, not only the page.
- Change smoke input and assertions from `1.0.0` evidence-only to `1.1.0`
  guided explanation support.
- Prove missing glossary/schema and mixed-version candidates fail before SSH.

Promotion evidence: unit tests, shell syntax, candidate inventory and digest,
negative closure cases.

## L1 — Repeatable candidate proof

After this layer, another operator can rebuild the exact candidate and obtain
the same local behavior and dry-run release manifest without credentials or
production access.

- Run producer, consumer, page, docs, ownership, alpha, and browser suites.
- Assemble the dry-run release and verify all exact hashes.
- Rehearse rollback against an isolated local or test fixture.

Promotion evidence: complete command log, release manifest, local acceptance
matrix, rollback rehearsal.

## L2 — Reliable protected publication

After this layer, one production generation is current, the prior generation is
recoverable, and the page/API are observed through their owned boundaries.

- Upload and atomically switch the exact W1 candidate.
- Roll back automatically on start or acceptance failure.
- Verify internal rich consultation, public anonymous/wrong-auth denial,
  deployed hashes, topology, restart, and unrelated homepage isolation.

Promotion evidence: current/previous ids, deployed hashes, production health and
behavior results, rollback status.

## L3 — Operable release closeout

After this layer, the release is reproducible and auditable without secrets, and
any missing human public-browser proof has a named owner and next route.

- Append the deployment receipt.
- Record rollback command and exact prior target.
- Record residue and post-release monitoring window.
- Bind the next route to Task Session closeout or incident rollback.

Promotion evidence: repository-local receipt and deterministic successor.

## Deliberate exclusions

New authentication, anonymous access, source-data migration, API writes,
reasoning-engine integration, ontology promotion, Git publication, and broader
ResonantOS release are outside all four layers.


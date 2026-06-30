---
title: ResonantOS CyberAlchemy Integration Package
status: draft-package
updated: 2026-06-29
audience: host memory-system engineers and collaborators
---

# ResonantOS CyberAlchemy Integration Package

This package stages the CyberAlchemy governance integration for a ResonantOS Living Archive style
host. It is written for a generic host collaborator, not for a named person.

The package is a governance blueprint with runnable validation contracts. It is not a turnkey
memory service and it does not replace the host archive.

## What This Package Contains

- `INTEGRATION-GUIDE.md`: package-safe integration guide.
- `OWNED-BASE.md`: public-safe owned base and runnable-vs-design accounting.
- `FINDINGS.md`: concise seam findings and claim boundaries.
- `MANIFEST.md`: file inventory and intended use.
- `boundaries.md`: scrub and claim policy.
- `contracts/`: copied public-safe evidence-card, EvidenceSet, and index schemas.
- `tools/`: copied validator scripts from public Arcanum inventory.
- `fixtures/`: synthetic package-specific evidence-card, Review Queue, and no-promotion fixtures.
- `docs/`: implementation contracts for Review Queue mapping, scope tags, observer slice, no-promotion,
  validator policy, and host promotion provider body.
- `examples/`: non-production observer and provider-body examples.
- `source-material/`: redacted source copies used to build this package.

## Integration Position

The host archive owns the read map and fact-over-time substrate. CyberAlchemy adds a write-side
governance package: candidates, promotion ownership, no-promotion guardrails, receipt debt, and the
contract for a host-side trusted-write provider body behind the host's existing promotion seam.

## First Build Slice

1. Validate the evidence-card fixture.
2. Review the candidate -> Review Queue -> decide -> promote mapping.
3. Exercise the read-only observer contract.
4. Only then implement the host-side trusted-write provider body.

## Claim Boundary

The promotion provider body is not implemented here. This package states the contract and validation
expectations for that body.

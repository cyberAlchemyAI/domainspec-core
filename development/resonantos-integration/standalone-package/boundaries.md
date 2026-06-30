# Boundaries

## Package Boundary

This package is a standalone staging package. It may be committed later as package content, but it
does not carry private parent repository history.

## Audience Boundary

The package is not directed to a named person. It is written for a generic host archive engineer or
collaborator.

## Public-Safe Content

Allowed:

- CyberAlchemy governance model.
- Evidence-card and EvidenceSet contracts.
- Promotion owner and default-deny vocabulary.
- Review Queue mapping.
- Scope tags.
- No-promotion guardrail.
- Host-side provider body contract.

Blocked:

- Private local checkout paths.
- Named individual handoff language.
- Private parent history.
- Private codenames or engine internals.
- Internal layer maps.
- Claims that a host-side trusted-write provider is already implemented.
- Claims that this package replaces the host archive's fact-over-time machinery.

## Copy Policy

This package copies public-safe schemas and validators. Redacted source-material copies are included
for traceability, not as canonical runtime contracts.

## Promotion Policy

Package evidence may not promote Inventory, Ontology, glossary, runtime, or trusted-write authority.
All package outputs remain candidate artifacts until reviewed by the appropriate owner.

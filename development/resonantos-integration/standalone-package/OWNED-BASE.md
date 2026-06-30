# Owned Governance Base

## Runnable Surface

This package carries a thin runnable surface:

- Evidence-card schema.
- EvidenceSet schema.
- Inventory index schema.
- Evidence-card slice validator.
- Evidence-card fixture validator.
- Inventory index validator.

These are copied into `contracts/` and `tools/`.

## Design Surface

The broader governance model is design guidance, not a compiled memory service:

- Candidate records enter as low-authority evidence.
- Promotion is owner-gated and default-deny.
- A candidate owes receipts before it can advance.
- Definitions, ontology, or runtime authority are promoted only by their owning lifecycle.

## Importance Boundary

The host archive owns recall importance: what to retrieve, keep, prune, or surface.
CyberAlchemy adds govern/rely-on importance: whether a candidate may be stood on or promoted.

The two compose. A host may recall a candidate while CyberAlchemy still refuses promotion.

## First Slice

1. Validate synthetic evidence-card fixtures.
2. Port no-promotion guardrail into the host decide step.
3. Keep trusted writes blocked until owner approval and provider-body validation.

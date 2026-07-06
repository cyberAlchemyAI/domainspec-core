---
tags: [inventory, findings, mint, body-war, attestation, claim-le-proof, build-from-owned, promotion-guardrail]
node_type: query-findings
is_session: false
status: candidate
created: 2026-07-04
boundary: INTERNAL - cav2/Mint/private Body War evidence; promotes nothing
sources:
  - .arcanum/inventory/index.json
  - .arcanum/inventory/entries/mint-foundry-content-autonomy-synthesis.md
  - .arcanum/inventory/entries/evidence-cards/2026-06-29-mint-foundry-experiments-cards.md
  - .arcanum/inventory/entries/evidence-sets/2026-06-29-mint-foundry-experiments-sets.md
  - .arcanum/inventory/entries/constitution-namespaces-and-axioms-role-synthesis.md
  - cyberAlchemy-v2/development/mint/HANDOFF.md
  - cyberAlchemy-v2/development/mint/experiment-foundry-boundary/run/findings.md
  - cyberAlchemy-v2/development/mint/experiment-content-autonomy/run-findings.md
  - projects/body-war/docs/PROJECT-DECISIONS.md
  - projects/body-war/domainspec/CONSTITUTION.md
  - projects/body-war/docs/features/troqar-product-architecture/INVOKE-TRANSPORT.md
  - projects/body-war/docs/features/parque-taquaral-online-mvp/DISCOVERY.md
---

# Query Findings - Mint / Body War Relation

Candidate Inventory query result. This is a read model only; it does not promote Body War into the
frozen Mint experiment, does not change cav2 authority, and does not claim Mint is shipped.

## Question

Search for the relation between `cyberAlchemy-v2/development/mint/` and `projects/body-war/`,
especially the remembered claim that Body War was evidence Mint would work because it reached the
same kind of result by another path.

## Machine-Index Result

The machine index already contains the formal Mint evidence packet:

- `entries-mint-foundry-content-autonomy-synthesis`
- `entries-evidence-cards-2026-06-29-mint-foundry-experiments-cards`
- `entries-evidence-sets-2026-06-29-mint-foundry-experiments-sets`
- `cyberalchemy-v2-mint-sigil-capability`
- `cyberalchemy-v2-mint-cav2-inheritance-audit-findings`
- `cyberalchemy-v2-universal-baseline-partition-findings`

The indexed Mint packet does not name Body War as one of the formal foundry-autonomy spines.
The frozen experiment domains are:

| Spine | Formal Mint role |
| --- | --- |
| `research` / resonantos re-mint | methodological inherit-route |
| `process` / release-approval | process object-authority route |
| `product` / API-contract governance | product object-authority route |

## Direct Relation Found

`cyberAlchemy-v2/development/mint/HANDOFF.md` names Body War directly, but as a guarded adjacent
witness:

- Attestation L1 gates Mint L2.
- Body War / TROQAR zone-control is a planned runnable witness for the discriminating-verify
  pattern's generality: `verify(valid)` and `verify(tampered)`.
- Scope guard: this is a different claim from the frozen N=3 foundry-autonomy experiment, so Body
  War must not be folded into the research/product/process domain set without authoring a new
  criterion.

So the strongest direct relation is:

> Body War is candidate evidence for the generality of the attestation / discriminating-verify
> pattern that Mint L2 depends on, not current evidence inside the frozen Mint content-autonomy
> experiment.

## Convergent-Path Relation

Body War also supports the remembered intuition in a second, weaker way: it reached a similar
structural shape by a different route.

Body War was not minted from cav2 Mint. It was built as a project-local Body War / TROQAR surface
with:

- a selected project-local DomainSpec bundle, chosen to make the project self-contained;
- local governance rules in `projects/body-war/domainspec/CONSTITUTION.md`;
- owner-boundary checks stating Body War consumes DomainSpec without promoting DomainSpec methods;
- project-local candidate definitions that remain unpromoted until a definitions-governance route;
- a runtime-backed Strava validation channel plus Craft ledger state for evidence, blockers, and
  recomposition.

This converges with Mint's later result:

- inherit reusable governance / method machinery;
- localize the domain's own content, rules, and evidence;
- keep the domain surface operable under its own local authority boundary;
- avoid laundering upstream authority into runtime decisions.

That is very close to Mint's corrected autonomy measure: content-localization + no-leak +
non-circularity. The evidence status is still different: Body War is precedent/convergence evidence,
while the formal Mint packet remains the N=3 research/product/process experiment.

## Claim Boundary

Use this relation as:

- yes: adjacent evidence that the pattern is not purely theoretical;
- yes: convergence evidence for "same result by another path";
- yes: a candidate future witness for attestation verify-pattern generality;
- no: proof that Body War is already a Mint experiment spine;
- no: permission to edit the frozen Mint criterion;
- no: authority promotion for Mint, Body War, attestation, or cav2.

## Lookup Handles

- Primary Mint synthesis: `.arcanum/inventory/entries/mint-foundry-content-autonomy-synthesis.md`
- Selector cards: `.arcanum/inventory/entries/evidence-cards/2026-06-29-mint-foundry-experiments-cards.md`
- EvidenceSet: `evset-mint-foundry-obs-verdicts`
- Direct scope guard: `cyberAlchemy-v2/development/mint/HANDOFF.md#connection--scope-guard-attestation--body-war-candidate-witness`
- Body War local project evidence: `projects/body-war/docs/PROJECT-DECISIONS.md`, `projects/body-war/domainspec/CONSTITUTION.md`

## Residue

Body War is marked planned/intended-not-built for the discriminating-verify witness in the Mint
handoff. To turn it into stronger evidence, a future task should produce a runnable Body War
verify-pattern specimen with both valid and tampered outcomes, then file it as a separate attestation
evidence card rather than adding it to the frozen Mint foundry-autonomy packet.

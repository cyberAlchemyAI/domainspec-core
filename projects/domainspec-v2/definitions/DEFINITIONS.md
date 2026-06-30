<!-- MINT-ACT OUTPUT (L1) for domainspec-v2. Cast from templates/definitions.md. INTERNAL/private.
     INHERITS the three-voice card FORMAT. SKELETON: seeds 2 cards; the owner authors the rest via the
     definitions lifecycle. Obs-B: an Evidence cav2/v1 citation is provenance, never a resolution path. -->

# DomainSpec v2 Local Definition Cards

Status: active
Promotion scope: local-domainspec-v2-only
Canonical source: yes

Local definitions for this repository. They do not define the implementation contract, governance
weight, launch readiness, or external policy. Each card keeps three voices (Formal / Plain-language /
Domain-context).

> **Citation vs authority (Obs-B).** A card's `Evidence:` MAY cite a harvested v1/cav2 snapshot —
> that is provenance, not a resolution path. The normative meaning is owned **here**; removing the
> framework attachment does not change it. A `Source kind:` of method-authority points at **this
> repo's own constitution**, never at v1 or cav2.

## domainspec-v2-D1. Drift

Source kind: operator-reading; local-inference

Evidence: [impl/spec/DRIFT-CONVERGENCE.md](../impl/spec/DRIFT-CONVERGENCE.md)

Formal voice:

```text
drift =
  measurable divergence between intended DomainSpec behavior and observed system reality
  across surfaces { semantic, contract, runtime, governance, coordination }
convergence =
  evidence-backed sustained reduction of critical drift over time
```

Plain-language voice: drift is the problem signal — the spec and reality have pulled apart;
convergence is the trend of pulling them back, with receipts.

Domain-context voice: the subject of **drift governance**; measured across the 5 surfaces, acted on
(not defined) by Saturn.

Use carefully: drift is a *signal*, not a correction; one signal is not (non-)convergence.

Misuse warning: do not conflate drift (the divergence) with Saturn (the loop that acts on it), or
detecting drift with converging.

Promotion boundary: local-only (grounds drift-governance; not an external policy term)

## domainspec-v2-D2. Validation governance ⟵ *domain-originated*

Source kind: local-inference  *(may cite v1 precedent in Evidence — citation only)*

Evidence: [authority/AUTHORITY-MODEL.md](../authority/AUTHORITY-MODEL.md),
[impl/spec/TEST-PIPELINE.md](../impl/spec/TEST-PIPELINE.md)

Formal voice:

```text
validation governance =
  the authority over BUILD-TIME FIDELITY of a typed spec:
    which obligations it must derive into (TEST-PIPELINE -> engine derive)
    AND what counts as pass/fail (engine lint; audit-alignment)
  resolving to THIS repo's authority/, never to a framework
```

Plain-language voice: the authority that says "for this typed spec, these checks must hold, and here
is what passing means" — exercised by the engine `derive`/`lint`, `generate-tests`, `audit-alignment`.

Domain-context voice: one of v2's three domain-originated governances (owner route
`validation-governance`); the methods are the already-built tools, the governance is the authority
over them.

Use carefully: build-time fidelity is necessary, not sufficient — it is not runtime conformance.

Misuse warning: do not treat a passing derived test as correctness, and do not collapse it into
cav2's `gate` / SMT meta-validation (that is meta-validation of governance rules; this is object
validation of specs/impls).

Promotion boundary: RATIFIED kind (owner, 2026-06-29); L2 attestation seal pending

<!-- SKELETON ENDS. The owner authors the layering-governance + drift-governance cards, a
     definitions-index, and a drift-audit as the card set grows (constitution load-bearing-term rule). -->

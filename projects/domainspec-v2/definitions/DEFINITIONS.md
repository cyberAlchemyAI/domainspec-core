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

## domainspec-v2-D3. Edge-Law Admissibility ⟵ *build-from-owned (CAV2-D22/D29/D16)*

Source kind: local-inference  *(cites cav2 CAV2-D22/D29/D16 in Evidence — citation only)*

Evidence: [development/reformulate-batch1/DESIGN.md](../development/reformulate-batch1/DESIGN.md) (R3),
[research/2026-07-01-composability-edges-taxonomy-synthesis.md](../research/2026-07-01-composability-edges-taxonomy-synthesis.md);
provenance: cav2 CAV2-D22 (orthogonal classification), CAV2-D29 (axis orthogonality), CAV2-D16 (typed coupling)

Formal voice:

```text
edge-law admissibility =
  an edge TYPE is admissible IFF it composes into different code
  (adds a non-redundant distinction over the axes
   {concept-type, relation-kind, composition-shape, feature-boundary})
corollary =
  widen a SOURCE endpoint (same target, same semantics) = clean
  change the TARGET type = overload -> reject
```

Plain-language voice: an edge deserves its own name only if it makes the code compose differently; else
widen an existing edge or add a flag. Widening *who* uses an edge is fine; changing *what it points at* is not.

Domain-context voice: governs R3 (RELATIONSHIPS reformulation). Rulings: keep `enforces`≠`applies`; collapse
`enforces`/`enforces-cross`; reject `queries` for Calc→Policy; widen `applies`→Policy→{Op,Calc} and
`queries`→Behavioral→Entity. See DEC-DSV2-EDGE-ADMISSIBILITY.

Use carefully: this is classification/governance orthogonality (CAV2-D22/D29), NOT Lean/Hilbert projector
orthogonality (excluded from cav2 authority).

Misuse warning: do not overload an edge's target type to reuse a name; do not conflate with the
linear-algebra orthogonality.

Promotion boundary: local-only (governs the v2 edge-law; cites cav2, transfers no cav2 authority)

## domainspec-v2-D4. Executable Typed Graph

Source kind: local-inference; synthesis

Evidence: [research/2026-07-01-composability-edges-taxonomy-synthesis.md](../research/2026-07-01-composability-edges-taxonomy-synthesis.md)

Formal voice:

```text
executable typed graph =
  the spec surface as ONE graph:
    nodes   = TAXONOMY meta-types (each -> one code pattern)
    edges   = RELATIONSHIPS typed edge-law
    realize = composability (how connected patterns reference each other in code)
  governed on 3 axes: layering (structure) / validation (derivation) / drift (alignment)
```

Plain-language voice: the spec is a typed graph you can build code from — the things (nodes), how they
connect (edges), and how each connection turns into code (composability).

Domain-context voice: thesis of the composability/edges/taxonomy synthesis; the substrate the spec-ontology
toy tested (verdict SURVIVED-narrow). Two enforcement arms: engine derivation (validation) + code-tag
composability (drift).

Use carefully: "executable" = derivable/checkable, not that the spec runs.

Misuse warning: do not collapse the three axes; engine derivation (moat) ≠ the composability check.

Promotion boundary: local-only

## domainspec-v2-D5. Two-Plane Boundary

Source kind: local-inference (resolves the spec-as-ontology research)

Evidence: [research/2026-07-01-spec-as-ontology/findings.md](../research/2026-07-01-spec-as-ontology/findings.md)

Formal voice:

```text
two-plane boundary =
  ontology framing governs the AUTHORING plane (writing/editing/organizing the spec)
  derivation governs the CONTRACT plane (the crisp, total, engine-facing spec)
  authority flows contract -> authoring, never reverse
```

Plain-language voice: use ontology tooling while you write the spec, but the strict engine-facing spec stays
the source of truth — help flows one way only.

Domain-context voice: interim stance while DEC-DSV2-LANE-ZA (fuse vs generate) is deferred to an agent-cost
experiment.

Use carefully: authoring-plane metadata (confidence/premises) is non-authoritative over the crisp docs until
an owner route ratifies a consumer.

Misuse warning: do not let authoring-plane ontology labels leak into the engine-facing contract docs.

Promotion boundary: local-only

<!-- SKELETON note: D1-D2 mint-seeded; D3-D5 consolidated 2026-07-01 into this canonical home (was the
     separate governance surface DSV2-D1/2/3, now removed). Companions backfilled 2026-07-01 to the current
     mint baseline: DEFINITIONS-INDEX + DEFINITION-DRIFT-AUDIT + DEFINITION-LOCALIZATION-ROUTE + reviews/.
     Still owed: layering-governance + drift-governance kind cards (tracked as owed in the drift audit). -->

# Agent Reasoning Engine ontology

Status: private first-class candidate package. Authority effect: none.

## Purpose

This durable ontology package defines the Agent Reasoning Engine as the
CyberAlchemy-v2 capability for both governed reasoning and context management.
It keeps business meaning, DomainSpec-authored system structure, generated
system projections, implementation evidence, and unresolved gaps distinct.
The current bounded system branch includes checkpointed append-only Reasoning
State recovery, disposable-index rebuilding, and a measured evolution cycle
with isolated variants and reversible controlled-local activation. Production
research providers, automatic code materialization, deployment, repair,
cross-process coordination, and Session semantics remain outside the realization.

The package uses the `business-system-bridge` ontology archetype because the
requested capability spans product meaning and runtime structure. Its business
branch defines the outcomes, actors, concepts, workflows, and non-collapse
rules. Its system branch is authored in DomainSpec v2 and compiled
deterministically. The bridge links only what current evidence supports.

## D65 construction state

| Stage | State | Meaning |
|---|---|---|
| Canonical definitions | validated | Exact CAV2-D65 and CAV2-D67 sections are source-bound. |
| Product ontology | referenced | The capability belongs to the existing CyberAlchemy product. |
| Product Capability | candidate | Stable combined reasoning/context outcome; not adopted by file presence. |
| Business ontology | candidate | Capability-local product meaning and rules. |
| DomainSpec source | candidate | Package-local authored nodes under `domainspec/`. |
| Compiled graph | candidate-generated | Deterministic projection, not independent authority. |
| System ontology | candidate-generated | Deterministic projection; profile admission is not granted. |
| Bridge validation | candidate | Partial realization and gaps are explicit. |
| Implementation | candidate partial realizations | Routing, context, context-bound semantic integrity, journal, app-server, reusable reasoning-state, exact-dispatch, checkpoint, fail-closed recovery, and measured evolution verticals have bounded evidence; they do not constitute the whole engine. |
| Static conformance | not evaluable | No accepted exact implementation binding. |
| Runtime evidence | not evaluable | No complete engine or context manager. |

## Key files

- [`product-capability.json`](product-capability.json) owns the candidate stable
  product outcome.
- [`business-ontology.json`](business-ontology.json) owns business meaning.
- [`domainspec/`](domainspec/) owns the authored system source and generated
  projections.
- [`bridge.json`](bridge.json) owns cross-branch traceability and evidence gaps.
- [`sources.json`](sources.json) binds the exact selected dependencies.
- [`residue.jsonl`](residue.jsonl) preserves unresolved construction state.

## Validation

From the repository root:

```text
python3 cyberAlchemy-v2/development/agent-reasoning-engine/ontology/scripts/validate.py --verify-build
python3 -m unittest discover cyberAlchemy-v2/development/agent-reasoning-engine/ontology/tests
```

Check-only validation writes nothing. A validation receipt is materialized only
with the separate `--write-receipt --receipt-name <unique-name>` operation.

The current candidate projection includes checkpointed completed-turn Reasoning
State Frontiers. They preserve explicit semantic and continuation results for
zero-call recovery replay, but do not acknowledge downstream successor delivery,
create a durable Session, or grant authority.

It also includes fail-closed context-bound semantic integrity: the binding,
Problem Frame, entry gate, authority snapshot, selected Context Items, freshness,
and claim ceiling must agree exactly, and context-bound receipts retain those
identities without changing historical unbound receipt bytes.

## Claim ceiling

A PASS proves that this candidate package is internally coherent, its selected
sources are current, its business and system endpoints close, bounded
realization edges carry implementation evidence, and its generated artifacts
replay deterministically. It does not adopt the Product Capability or decision
profile, admit the DomainSpec profile or system ontology, provide general
context management, integrate the whole engine, accept an implementation
binding, prove conformance, publish, release, deploy, or authorize an effect.

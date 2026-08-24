# Refine Result — Cohesive Modular Arcanum

Status: `flag` — design and plan ready for Decision Gate; implementation not admitted.

## The answer

Make Arcanum cohesive by standardizing how owner boundaries are described and verified, not by creating a universal builder that owns them.

The selected architecture is:

- one structural transition grammar, OBTC;
- versioned bilateral adapters between named producer and consumer owners;
- owner-native artifacts and receipts as the only semantic authority;
- an optional non-authoritative causal event projection for diagnostics;
- one effect owner and one authoritative writer per transition;
- explicit owner gates between authoring, readiness, execution, closeout, continuity, lifecycle, and release.

In plain language: share the plugs and the shipping labels, not the machines or their decisions.

## System shape

```text
Invoke authors
  -> WPRA freezes and selects
  -> Task Session admits and executes one SWU
  -> Continuation Router carries one owner hop
  -> Invoke Refresh mutates or proves no-op
  -> Router joins the owner receipt
  -> Task Session derives synchronized result and cursor
  -> one series owner may advance the frontier
```

A material producer enters Task Session through its own receipt. Capability lifecycle and registry release remain later, separate owner gates. Craft, Inventory, Necronomicon, ontology/context harnesses, and observability remain scoped ledgers or projections; none becomes build authority.

## What becomes shared

- transition identity, attempt/cause correlation, native handles and digests;
- structural owner/role singularity;
- gate and expected-receipt descriptors;
- freshness, replay, outcome-unknown, CAS/lease, residue, and reroute fields;
- structural validation and negative fixtures;
- parity and public-boundary evidence shapes.

## What remains sovereign

- Invoke authorship and Refresh mutation;
- WPRA freeze/audit/selection evidence;
- material production;
- Task Session entry, admission, one-SWU execution, synchronization, and current cursor;
- Continuation Router transport/join;
- ordered-series state;
- Craft ledger state;
- sigil/spell lifecycle judgment;
- registry release;
- Inventory and observability projections.

## Key design decisions

1. The OBTC kernel validates structure only. Semantic legality stays with the consumer/effect owner.
2. `AuthoredWorkPack` and `FrozenWorkPackSnapshot` are different records with different owners.
3. Closeout is split into execution terminal, Refresh mutation/no-op, Router join, synchronized result, continuity cursor, and series advance.
4. `outcome_unknown` prohibits automatic retry; only the effect owner may reconcile.
5. Mutation admission must recheck state atomically at the effect boundary with CAS or a scoped lease.
6. Causal events are projections, not authority; they are either ephemeral fixtures or persisted by an explicitly admitted local owner.
7. Migration is bilateral and versioned, with shadow comparison and one authoritative writer. Extract common fields only after two materially different boundaries pass.
8. Implementation Readiness is recommended as the sole series reducer. Task Session Until Blocker becomes a stateless compatibility facade only after Decision Gate and lifecycle acceptance.
9. The two known Orchestrate defects remain separate repairs: exact expected receipt sets and run-global pre-spawn action IDs.
10. Any public capability must be reconstructed from public sources after lifecycle authorization; private refinement prose is not publication source.

## Migration plan

The non-executed Work Pack contains seven tasks and seventeen one-behavior SWUs:

- pre-L0: bind the five owner/persistence decisions;
- L0: privately prove WPRA → Task Session projection, structural validation, and owner-native shadow acceptance;
- L1: prove Task Session → Refresh plus outcome reconciliation, concurrency, compatibility, privacy, and causal-event mode;
- L2: consolidate series ownership, repair both Orchestrate defects, prove generated parity, and run a real Invoke-to-Refresh owner-chain witness;
- L3: run lifecycle/public reconstruction and registry gates.

No SWU is selected. The first candidate, `SWU-ABP-001`, remains blocked until Decision Gate and a new Task Session authorization.

## Evidence

- Context Builder: pass, 12/12 obligations.
- Invoke Define: pass.
- First interrogation/critic: flag/blocking counterexamples routed into repair.
- Architecture tournament: hybrid protocol plus bilateral-adapter-first migration selected.
- Invoke Design: `design-validator-pass`, fixed point, no diagnostics.
- Repaired toy game: pass, 13 unique cases, one synthetic positive and twelve fail-closed negatives.
- Invoke Plan: pass for structure, seven tasks and seventeen SWUs; mutation handoff blocked.
- Final boundary critic: `flag`, no remaining structural authority collapse; safe only for Decision Gate.

## Required decisions

- `DECISION-ABP-SERIES`: ordered-series owner and compatibility facade.
- `DECISION-ABP-PROTOCOL`: protocol capability class/steward with owner-local version acceptance.
- `DECISION-ABP-PRODUCER`: exact material producer.
- `DECISION-ABP-REGISTRY`: exact registry release owner.
- `DECISION-ABP-EVENTS`: ephemeral versus admitted local persistence owner.

## Proof ceiling

Nothing was implemented or run against a real product owner chain. This result is not implementation readiness, synchronized runtime proof, canonical defect repair, generated parity, lifecycle promotion, registry release, publication, deployment, or production readiness.

Next route: Decision Gate. Task Session is deliberately deferred.

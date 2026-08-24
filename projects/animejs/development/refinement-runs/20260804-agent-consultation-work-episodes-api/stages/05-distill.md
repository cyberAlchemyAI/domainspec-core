# Stage 05 — Initial Distill

Status: `pass`

## Smallest coherent unit

The minimum system that satisfies the intent and preserves the ontology's evidence rules has four atoms:

1. immutable consultation projection and bounded query service;
2. validated episode command protocol with a distinct append grant;
3. append-only event journal plus deterministic reducer;
4. derived episode projection consumable by the read service.

Removing atom 1 leaves agents unable to consult. Removing atom 2 allows arbitrary writes. Removing atom 3 makes replay, correction, and proof impossible. Removing atom 4 leaves later agents unable to consult recorded work.

Lesson verification is deliberately not part of the unit. It can pass or fail independently and has a different owner and evidence ceiling.

## Rejected alternatives

- Direct writes to `nodes/nodes.json`: destroys append history and conflates episode evidence with graph truth.
- One CRUD endpoint: erases command invariants and enables in-place mutation.
- One read/write capability key: violates effect separation.
- Free-form agent notes: cannot bind attempts, outcomes, versions, or evidence.
- Automatic lesson extraction on close: converts lifecycle completion into epistemic approval.
- Vector-only retrieval: loses deterministic typed traversal and digest-bound explanation.

## Recomposition proof

`Task + VersionContext + ordered Attempts + EvidenceHandles + terminal Outcome` reduces into one immutable episode snapshot. Episode snapshots contribute typed candidate nodes/relations to a derived projection. The consultation API can query that projection alongside documentation knowledge while disclosing evidence state and never treating it as verified Lesson knowledge.

## Evolution profile

- L0 proves contracts and reducer determinism using local fixtures.
- L1 proves a candidate-local journal and query service.
- L2 proves separately authorized host adapters, recovery, and security.
- L3 covers non-loopback packaging/deployment only after owner selection and current evidence.

## Distill residue

Host choice, federation, retention, and Lesson review are deferred without weakening L0.

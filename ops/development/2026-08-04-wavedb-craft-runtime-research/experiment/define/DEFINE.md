# Define: WaveDB as a disposable Craft projection runtime

## What this experiment owns

This package determines whether the reviewed WaveDB Node binding can support a
candidate-local, digest-addressed projection of one frozen Craft YAML fixture
without acquiring any Craft authority. It owns fixture compilation, isolated
store operations, exact verification, negative controls, observation receipts,
and the stop decision.

It does not own Craft schemas, Craft ledgers, called-capability receipts,
canonical storage, package publication, deployment, or promotion.

## Problem statement

Craft currently defines a file-backed operating method but no automated command
runner or database projection runtime. WaveDB exposes plausible hierarchical
key/value, batch, iterator, and persistence primitives, but static source review
cannot establish package provenance, build compatibility, exact projection
correctness, failure behavior, or recovery behavior.

The experiment must produce empirical evidence without allowing the database to
become authoritative or allowing a failed package gate to turn into an install.

## Bounded hypothesis

If and only if the exact registry artifact can be bound to the reviewed source,
a deterministic adapter can build and completely verify a disposable WaveDB
generation addressed by the fresh SHA-256 of `.craft/ledger.yml`. After any
staleness, corruption, incomplete verification, wrong workspace, or invalid
fixture signal, the adapter emits zero rows and preserves canonical YAML bytes.

## Capabilities

| Capability | Outcome | Boundary |
| --- | --- | --- |
| Freeze inputs | Exact package, source, toolchain, parser, serializer, fixture, and digest identities | Fails before install on any unresolved mapping |
| Compile projection | Closed key/value manifest from fresh canonical YAML | No active pointer and no unlisted key |
| Verify and query | Complete readback and fresh-YAML admission before output | Zero output on any mismatch |
| Observe failure | Deterministic negative controls on isolated copies | No live-store or power-loss claim |
| Quarantine and rebuild | External observation record plus fresh sibling generation | No in-place repair |
| Close experiment | Honest BOUND/HOLD/KILL receipt and next-owner route | No promotion or publication |

## Source contracts

| ID | Selector | Digest | Role |
| --- | --- | --- | --- |
| SC-CRAFT-SKILL | `arcanum/arcana/craft/SKILL.md` | `f3f5d9deabc5c8630513590ccfc8eb0ae0d99e16ea3bf90d910bef27eb9558b3` | Canonical operating and storage authority |
| SC-CRAFT-ARCH | `arcanum/arcana/craft/ARCHITECTURE.md` | `c306e2326162a13630981030d26bc1993832815cc6acffccaacecbf14cc71bbe` | Canonical architecture baseline |
| SC-FINDINGS | `ops/development/2026-08-04-wavedb-craft-runtime-research/findings.md` | `958ed1ae74cfad7483a70f6ca7a78ba5a970a97e928da4d88e40979f680b53f0` | Audited experiment contract and claim ceiling |
| SC-RESEARCH | `ops/development/2026-08-04-wavedb-craft-runtime-research/research.md` | `1a5999ab113e7d22a52022e18a817912f1575ffe2db2b0422e76bb0762af55bd` | Frozen fixture and source evidence |
| SC-CLOSURE | `ops/development/2026-08-04-wavedb-craft-runtime-research/receipts/evidence-closure.json` | `59d74b990e50444e04c1a8661a124e8fbba1bd9706ce2f316f38c6f3e4047f0d` | Cross-source evidence closure |

## Invariants

1. Canonical YAML bytes are hashed before and after every operation and never
   change.
2. Workspace resolution and authorization happen on the filesystem before any
   database access.
3. A generation is selected only by the fresh YAML digest; v0 has no mutable
   active-generation pointer.
4. Every stored non-manifest key/value is enumerated and individually digested.
5. Query output is forbidden until a complete independent readback succeeds.
6. Database bytes, derived views, receipts, and quarantine records never flow
   back into YAML.
7. All destructive controls target explicit isolated copies only.
8. Package/source mismatch blocks before native build or install.
9. Process termination does not justify a power-loss or durability claim.
10. A passing experiment remains candidate-local evidence, not a Craft runtime
    promotion decision.

## Required states

`unfrozen -> package-gate-pass -> fixture-frozen -> built -> verified ->
observed -> closed`

`package-gate-blocked`, `verification-failed`, and `quarantined` are terminal
for the affected run. A new sibling run requires new exact inputs.

## Acceptance

The experiment passes only when WP-0 through WP-6 each have exact receipts and
all positive and negative oracles pass. It blocks immediately at the first
owner, provenance, build, fixture, verification, or acceptance-critical
failure. A correct early block is successful control-flow evidence but is not a
passing WaveDB/Craft projection result.

## Non-goals

- WaveDB as a canonical Craft store;
- a transactional YAML writer or database-to-YAML path;
- multi-writer support, schema migration, encryption lifecycle, deployment,
  package publication, prefix deletion, or in-place corruption repair;
- changes under `arcanum/arcana/craft/` or `arcanum/development/craft/`;
- claims about production readiness, crash/power durability, or performance.

## Discovery and interrogation disposition

Discovery is satisfied by the completed, audited research package. The user's
confirmation admits only the finite candidate-local experiment. The first
newly discovered consequential choice is package provenance; the gate cannot be
inferred because the registry `gitHead` and versioned source disagree.

## Define gate

- Result: `pass`
- Reason: intent, authority, scope, invariants, failure semantics, and stop
  conditions are explicit; no implementation permission is inferred beyond the
  candidate-local experiment.

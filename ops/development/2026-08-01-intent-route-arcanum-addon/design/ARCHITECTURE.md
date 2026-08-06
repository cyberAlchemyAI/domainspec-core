# Architecture

## View 1 — system context

```text
runtime intent capture
  -> runtime-owned source adapter
  -> generated intent-route-resolver package
       -> public-safe pure core
       -> digest-bound read-only catalog
       -> trusted non-authorizing disposition
  -> runtime display or clarification
  -> human-confirmed existing Dispatch/group/seat
  -> retained host binding, authorization, execution, and evidence owners
```

The resolver sits before inference and before execution. It reduces a typed
intent against a supplied finite catalog. It does not decide whether work may
run.

## View 2 — canonical and generated containers

| Container | Intended location | Authority | Contents |
|---|---|---|---|
| candidate staging | private development package selected by `sigil-development` | candidate only | public-safe draft core, schemas, manifest, synthetic fixtures, scans |
| canonical sigil | `arcanum/arcana/intent-route-resolver/` | public Arcanum after explicit acceptance | `SKILL.md` plus executable support closure and acceptance runners |
| Codex projection | `.agents/skills/intent-route-resolver/` | generated | exact canonical closure plus generated metadata |
| Claude projection | `.claude/skills/intent-route-resolver/` | generated | exact canonical closure plus admitted profile token normalization |
| consumer adapter | consumer-owned source tree | consumer runtime owner | request projection/rejection and strict local-process transport |
| private compatibility edge | `cyberAlchemy-v2/**` | private CAV2 owner | private IntentRecord/ACI bindings; never public source |

Canonical source precedes generation. Generated packages are disposable
projections and are never hand-edited semantic owners.

## View 3 — component contracts

| Component | May | Must not |
|---|---|---|
| public core | validate, trace eligibility, apply explicit dominance, abstain, canonicalize | import runtime/private types, discover skills, call a model, authorize, persist, execute |
| JSON port | enforce closed protocol and bounded single-document input/output | become a daemon, accept extra documents, leak stack traces |
| catalog projector | project named owner IDs/revisions/digests or reject | create IDs, repair, rank, register, or persist independently |
| Bootstrap | select accepted sigil and project closure into named profiles | resolve intent, accept canonical source, or grant authority |
| runtime wrapper | invoke the pinned local closure and preserve bytes/exits | add profile-specific semantics or fallback |
| source adapter | preserve raw capture, posture, evidence refs, constraints, and mapping identity | infer missing policy, repair invalid values, choose a route |
| consumer | display advice, ask exact clarification, stop, or forward separately confirmed binding | treat candidate as selected/authorized or claim effect |

## View 4 — state and event

The resolver is a pure invocation with exhaustive terminal output:

```text
received -> transport-rejected
received -> request-admitted -> catalog-invalid -> invalid
received -> request-admitted -> catalog-admitted -> evaluated
evaluated -> candidate | ambiguous | no-match
```

These terminal dispositions are not persisted lifecycle states. Candidate
admission follows the separate evidence sequence in `define/states.md`.

## View 5 — authority and trust

Trust is split across independent proofs:

- support evidence says why a source field was declared or inferred;
- catalog bindings say which owner material was projected;
- the disposition integrity digest says response bytes are intact;
- a human-confirmed existing Dispatch binding embodies the route choice;
- authorization, execution, effect, and completion receipts remain with their
  existing owners.

No proof upgrades another by mere presence. Detailed rules are in
[AUTHORITY-TRUST.md](AUTHORITY-TRUST.md).

## View 6 — integration, quality, and evolution

Integration is local-process and version/digest bound. Core semantics are one
canonical closure; wrappers are thin. The accepted acceptance addendum freezes
JSON-port, public-core, Codex, Claude, and orchestrator-adapter cases.

Evolution proceeds through four layers: public boundary decision, candidate
sigil witness, canonical generation parity, then independent consumer/private
admission. Compatibility and rollback are tested before a real consumer is
mutated. See [INTEGRATION-VERSIONING.md](INTEGRATION-VERSIONING.md) and
[VALIDATION-CONTRACTS.md](VALIDATION-CONTRACTS.md).

## Failure model

Malformed input, unsupported version, missing executable, nonzero exit,
multiple stdout documents, oversized output, stderr, timeout, digest drift,
disabled integration, and rollback mismatch all fail closed. An adapter may
return a typed rejection but may not retry semantically or choose a fallback.

## Persistence and concurrency

The resolver, wrapper, and adapter own no durable store, queue, journal, or
registry. ACI may later reference content-addressed request/disposition bytes
from its existing journal after its owner binds fields. Each invocation is
isolated and catalog-digest bound; concurrent calls share no mutable state.

## Privacy and data lifecycle

Public fixtures are synthetic. Private inputs and outputs remain consumer-owned
and must not enter public fixtures, generated provenance, or diagnostics. The
core returns no stack traces. Retention is outside the resolver and requires an
existing owner contract.

## Deployment and rollback

Generation and installation are distinct. Selective sync stages one package,
validates it, applies checksum-based synchronization, and restores exact
pre-install bytes on failure. A generated-package pass is not release or
deployment evidence.


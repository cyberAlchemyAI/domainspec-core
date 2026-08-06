---
title: Intent Route Arcanum Add-on specification
status: candidate
invoke_mode: define
authority_effect: none
---

# Intent Route Arcanum Add-on specification

## Objective

Define a fresh public-safe, project-agnostic Arcanum sigil that exposes one
small deterministic relation to any agentic runtime:

```text
intent-route.request@1 + digest-bound route catalog
  -> candidate | ambiguous | no-match | invalid
```

The relation returns possible routes or visible ambiguity before inference and
before execution. It never promotes similarity, eligibility, or a single
candidate into permission.

## Expected end state

If every later gate is independently approved and passed:

1. `arcanum/arcana/intent-route-resolver/` is an accepted canonical sigil with
   a public-safe core, JSON port, schemas, synthetic fixtures, zero-authority
   manifest, and deterministic acceptance runners.
2. Bootstrap selectively generates the same closure into
   `.agents/skills/intent-route-resolver/` and
   `.claude/skills/intent-route-resolver/`.
3. Both runtime packages produce byte-identical canonical case responses,
   exits, reason codes, and zero-authority counters except for explicitly
   admitted provenance/tool-token differences.
4. Any agent runtime may provide a thin source adapter and invoke the pinned
   local JSON process; the adapter may project or reject only.
5. Augmentor may capture ordinary-language intent, display candidate routes,
   or ask the exact clarification. It retains no route-truth, approval, or
   execution authority.
6. The orchestrator may call a thin adapter before `_workflow_envelope()`.
   Only a separately confirmed canonical Dispatch/group/seat may enter the
   existing workflow-binding owner.
7. Private `cyberAlchemy-v2` may reference the generic contract at entry
   routing while private semantic judgment, ACI, actor protocol, memory,
   effects, evidence admission, and promotion remain separately owned.

This is a target state, not current software.

## Current baseline

- The private standalone resolver has a bounded 34-pass test witness.
- It is not a canonical public sigil and cannot be selected by Bootstrap.
- No Claude/Codex generated package, consumer installation, orchestrator
  adapter, or private runtime integration currently exists.
- The accepted future acceptance design freezes 78 logical cases, but no
  runner result exists yet.

## Scope

In scope for the planned capability:

- a JSON-only request, catalog, disposition, and runtime-port protocol;
- deterministic validation, eligibility, explicit dominance, abstention, and
  canonicalization;
- a zero-permission executable support closure under one sigil;
- synthetic public fixtures and static private-content/import scans;
- selective Bootstrap generation for Claude and Codex;
- thin adapter contracts for arbitrary runtimes and a later orchestrator seam;
- owner-preserving Augmentor and private reasoning-stack composition;
- isolated install, disable, rollback, timeout, size, stderr, and byte-parity
  acceptance.

Out of scope:

- copying or publishing the private package or private vocabulary;
- live capability discovery or ownership creation;
- a route registry, selection table, adapter ledger, or second lifecycle;
- semantic repair, enrichment, policy inference, ranking, model fallback, or
  natural-language quality claims;
- Dispatch authorship, approval, authorization, scheduling, persistence,
  replay, rollback ownership, execution, effects, or completion claims;
- current ResonantOS, orchestrator, Augmentor, Claude, Codex, or CAV2 mutation;
- promotion, release, deployment, production, or whole-engine claims.

## Contracts

`intent-route.request@1` contains `request_id`, preserved intent and typed
discriminator postures, support evidence references, constraints, `catalog_id`,
`catalog_digest`, and optional `supersedes_request_id`.

The catalog contains a schema version, ID, content digest, `derived_from`
owner/revision/digest bindings, and finite projected route entries. It is
validated read-only and never repaired.

The trusted runtime-port response contains the request/catalog bindings,
complete evaluated route traces, reason codes, optional clarification or
candidate identity, a disposition integrity digest, and
`authority_effect: none`. Transport rejection does not fabricate a trusted
disposition.

## Normative rules

| ID | Rule |
|---|---|
| IRO-R01 | Validate protocol, catalog identity/digest, unique route IDs, owner bindings, and acyclic dominance before matching. |
| IRO-R02 | Preserve declared, inferred, and unresolved postures; never fill an unresolved discriminator. |
| IRO-R03 | Evaluate exclusions before required predicates and use only explicit catalog dominance. |
| IRO-R04 | Return `ambiguous` whenever missing information can change eligibility. |
| IRO-R05 | Return `candidate` only for one non-dominated eligible route; return `no-match` without fallback. |
| IRO-R06 | Canonicalize responses and emit exactly one typed response or typed transport rejection. |
| IRO-R07 | Every trusted disposition has `authority_effect: none`; no component in this closure opens or appends Dispatch, binds workflow, authorizes, schedules, persists effects, spawns a host, or claims completion. |
| IRO-R08 | Runtime adapters may project or reject only; semantic retry and compatibility fallback are forbidden. |
| IRO-R09 | Generated Claude and Codex packages originate from one accepted canonical closure and pass per-case behavior parity. |
| IRO-R10 | Human confirmation reuses the existing canonical Dispatch/group/seat; no parallel route-decision lifecycle is introduced. |

## Acceptance criteria

| ID | Criterion | Evidence owner |
|---|---|---|
| IRO-A01 | Public candidate contains no private content/import and declares zero authority/permissions. | sigil-development candidate witness |
| IRO-A02 | JSON-port cases cover all four dispositions and all closed transport failures with exact bytes/exits. | public core runner |
| IRO-A03 | Catalog/order permutations preserve canonical bytes; removed evidence cannot improve a disposition. | core metamorphic tests |
| IRO-A04 | Selective Bootstrap generation produces complete Claude and Codex closures from one canonical source digest. | Bootstrap owner |
| IRO-A05 | Claude and Codex execute the frozen 15-case wrapper matrices with per-case byte parity. | runtime package parity runner |
| IRO-A06 | Disable and rollback restore the exact pre-install closure in isolated roots. | add-on lifecycle runner |
| IRO-A07 | The thin adapter enforces 5000 ms timeout, request/stdout/stderr ceilings, version/digest checks, and zero semantic fallback. | adapter runner |
| IRO-A08 | Orchestrator negative cases prove resolver output alone causes zero workflow binds, authorization, spawns, or effects. | orchestrator consumer owner |
| IRO-A09 | Only a confirmed existing Dispatch binding can cross to the existing workflow-binding owner. | Dispatch and orchestrator owners |
| IRO-A10 | Augmentor and arbitrary runtimes can consume the protocol without importing private engine types or gaining authority. | consumer contract test |
| IRO-A11 | Private CAV2 admission references the generic entry contract without moving private semantic/ACI/effect authority public. | private authority gate |
| IRO-A12 | Browser execution proves only the declared portable wrapper/core cases in the tested Chromium; no product acceptance claim is inferred. | acceptance harness owner |

The normative future acceptance matrix is the accepted addendum at
`research/2026-07-30-intent-router-bootstrap-runtime-integration/acceptance-contract-addendum.md`.

## Integration sequence

```text
runtime-owned intent capture
  -> source adapter projects or rejects intent-route.request@1
  -> pinned local public resolver closure reads a digest-bound catalog
  -> non-authorizing disposition
  -> runtime displays candidate, ambiguity, no-match, or invalid
  -> human confirms or authors existing Dispatch/group/seat
  -> retained Dispatch/orchestrator owners bind, authorize, and execute
  -> retained evidence owners report outcome
```

## Open residue

Open owner decisions are centralized in [../OPEN-QUESTIONS.md](../OPEN-QUESTIONS.md).
Until they close, implementation may produce only a candidate-local public-safe
extraction witness outside canonical public Arcanum.


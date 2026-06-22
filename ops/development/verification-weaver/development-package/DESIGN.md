# Design: Verification Weaver

## Capability Shape

`verification-weaver` is a candidate public Arcana router. It receives a
testing target, classifies it, selects owner lanes, records expected evidence,
and emits a parent `VERIFICATION-WEAVE` receipt that references native lane
receipts.

It does not execute owner lanes by default. A future adapter may invoke owner
commands only when the owner capability defines a safe input contract and
receipt contract.

## Target Classification

| `target_kind` | Discriminants | Owner lane | Default status |
| --- | --- | --- | --- |
| `spec_derivation` | DomainSpec aspect docs, derivation rules, oracle available. | `test-derivation` | route |
| `frontend_ux` | UI spec, route/page, browser-observable behavior, UX evidence request. | `ux-evidence-validator` | flag while seed-only |
| `execution_repeatability` | Command manifest, fixture runner, package scripts, validation harness. | `experiment-harness` | route |
| `architecture_gap` | Architecture folder/spec, test alignment question, repo evidence. | `architecture-pattern-inventory` | route |
| `research_evidence` | Protocol, claim, fixture/run data, metric or evidence status. | `research-evidence-harness` | route |
| `mixed` | More than one owner lane required. | parent decomposition | split or block |
| `unsupported` | No recognized owner, oracle, or evidence contract. | none | block |

## Owner Lane Contract

Each owner lane must declare:

- `owner_capability_ref`;
- `owned_verb`;
- `input_contract`;
- `output_receipt`;
- `evidence_artifact`;
- `stop_conditions`;
- `promotion_boundary`.

## Oracle Binding

No formal/testing claim can pass without an oracle type:

- `deterministic_derivation`;
- `fixture_runner`;
- `proof_checker`;
- `browser_evidence`;
- `human_review`;
- `research_run_data`;
- `explicit_gap`.

If no oracle is bound, status is `block` or `flag` with residue.

## Parent Receipt Policy

`VERIFICATION-WEAVE` is a parent receipt only. It may join:

- target classification;
- lane route decisions;
- owner receipt references;
- obligations and expected evidence;
- gaps;
- residue;
- next route.

It may not upgrade, promote, or rewrite the owner lane results.

## Public-Safety Rules

Public package content may include:

- synthetic fixtures;
- abstracted public-safe examples;
- public Arcanum contracts;
- public schema examples;
- public fixture runner examples.

Public package content must block:

- private implementation paths as fixtures;
- private project examples;
- generated runtime outputs as promotion evidence;
- local observability logs as source evidence;
- copied private code;
- `.claude/worktrees` or other local worktrees;
- credentials, tokens, personal data, or real user data.

## Status Model

| Status | Meaning |
| --- | --- |
| `pass` | Every selected lane returned acceptable native receipt evidence and no hard gap remains. |
| `flag` | Evidence exists but residue, seed-only status, soft UX concern, or owner review remains. |
| `block` | Unsupported target, missing oracle, private leak, generated-only proof, adapter failure, flaky evidence, or explicit owner block. |

## Promotion Boundary

Promotion action is restricted to:

- `none`;
- `candidate-request`.

Only the owning capability can promote its own artifact after its own evidence
gates pass.

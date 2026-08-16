# Work Pack: Public App Server Adapter Repair

- Work Pack ID: WP-RWO-CODEX-APP-SERVER-REPAIR-001
- Predecessor plan epoch: WP-RWO-CODEX-MIGRATION-001-E2
- Trigger: accepted CX003 insufficiency finding
- Status: canonical validators and v2 readiness pass; awaiting exact human acceptance
- Admission timing: selected-unit-at-task-session
- Frontier: SWU-RWO-CX-003R only
- Authority effect: none
- Publication effect: none
- Mutation ready: false

## Objective

Make the public `app-server` adapter selectable and executable through `tools/arcanum` while preserving Task Session as the sole semantic coordinator. Close exactly the three CX003 gaps: live adapter unavailability, missing generic capsule bridge, and unverified installed-schema parity.

## One-Behavior Boundary

SWU-RWO-CX-003R owns one behavior: a caller can select `app-server`, execute one bounded stdio JSON-RPC exchange through a fake local process, normalize raw host evidence, and return control to Task Session without manufacturing semantic authority. Registration, driver, fake test, installed parity, and documentation are one atomic acceptance surface: exposing any subset would either register an unusable adapter or claim an unvalidated contract.

## Architecture Invariants

1. Task Session remains the sole owner of task selection, admission, semantic review, owner verdict, closeout, and successor projection.
2. The App Server adapter owns only child-process stdio transport, JSON-RPC correlation, provider-local identity, raw event normalization, bounded teardown, and raw host evidence.
3. `tools/arcanum` owns adapter selection and runtime envelope evidence; it must not become a second Task Session controller.
4. Fake-stdio validation performs no network, provider, credential, App Server, or model turn.
5. Installed parity is generated from the installed Codex binary by `codex app-server generate-json-schema`; schema generation is not App Server execution.
6. No private CX002 source or fixture byte may be copied into public Arcanum. Only generic method names and generic runtime contracts cross the boundary.
7. Existing E2 plan bytes, CX002 terminal evidence, and CX003 finding/validation remain immutable.
8. Success returns to a fresh CX003 sufficiency audit attempt. It does not advance to CX004.

## Exact Material Scope

Modify:

- `arcanum/tools/arcanum`
- `arcanum/framework/runtime/README.md`
- `arcanum/framework/runtime/adapters/app-server-fixture.md`
- `arcanum/arcana/task-session/runtime-adapters/README.md`

Create:

- `arcanum/framework/runtime/adapters/app-server.md`
- `arcanum/framework/runtime/adapters/app_server.py`
- `arcanum/framework/runtime/development/fixtures/app-server/live-fake/fake_app_server.py`
- `arcanum/framework/runtime/development/fixtures/app-server/live-fake/test_app_server_adapter.py`
- `arcanum/framework/runtime/development/fixtures/app-server/live-fake/validate_installed_parity.py`
- `arcanum/arcana/task-session/runtime-adapters/app-server.md`

Private execution evidence is limited to the new `SWU-RWO-CX-003R/` E/O/V/P/C/B/T set and `public-runtime-repair/INSTALLED-PARITY.json`.

## Validation Strategy

- shell syntax for `tools/arcanum`;
- deterministic fake stdio unit/integration test;
- adapter listing and resolution checks;
- installed schema parity against the captured Codex binary and the seven required methods;
- no-network/no-model/no-credential assertions;
- exact write-algebra and baseline checks;
- E/O/V/P/C/B/T closeout before any successor.

## Gate Sequence

1. Dispatch, execution-entry, and audit-config schema validation pass against the exact authored bytes.
2. Work Pack Readiness Audit v2 freezes the one-unit umbrella-root candidate and returns `PLAN_SEMANTIC_READY`.
3. Candidate inventory and digest bind the authored files plus all three readiness outputs.
4. Exact human owner acceptance binds that post-readiness candidate digest.
5. Implementation Readiness selects SWU-RWO-CX-003R.
6. Task Session rehashes all ten baselines and issues one single-use mutation admission.
7. Invoke Refresh produces the exact material package and proposed bytes; Task Session alone admits the package and executes/applies the mutation.
8. Acceptance-critical validation and public-runtime owner review pass.
9. E/O/V/P/C/B/T closes the one-unit Work Pack with a terminal sentinel and no in-pack successor.
10. Continuation Router hands the terminal to the public-runtime sufficiency owner for one fresh SWU-RWO-CX-003 audit attempt; it never projects CX004 directly.

## Claim Ceiling

Candidate planning evidence and, once emitted separately, frozen-input readiness evidence only. It grants no public mutation, adapter compatibility, installed App Server execution, model turn, framework acceptance, promotion, publication, deployment, release, or production claim.

# TASK-RWO-CX-003R2 — Split-Provenance Public Adapter Apply

```json
{
  "schema_version": "rwo.task-contract/v2",
  "task_id": "TASK-RWO-CX-003R2",
  "swu_id": "SWU-RWO-CX-003R2",
  "primary_owner": "public-runtime-owner",
  "dependencies": [
    "SWU-RWO-CCP-003"
  ],
  "canonical_successors": [
    "TERMINAL:CONTROL-CONTENT-PROVENANCE-WORK-PACK"
  ],
  "objective": "Package, admit, apply, and validate the ten clean-room adapter files using private controls and exact public content sources under Invoke 1.1 and Task Session 1.3.",
  "command": {
    "argv": [
      "task-session",
      "execute",
      "--work-pack",
      "WP-RWO-CONTROL-CONTENT-PROVENANCE-002",
      "--swu",
      "SWU-RWO-CX-003R2",
      "--task",
      "ops/development/2026-08-16-rwo-control-content-provenance-successor-r2/candidate-plan-epoch/work-pack/tasks/TASK-RWO-CX-003R2.md"
    ],
    "cwd": ".",
    "expected_exit": 0,
    "timeout_seconds": 3600,
    "environment": {
      "inherit_allowlist": [
        "PATH"
      ],
      "fixed": {
        "LC_ALL": "C",
        "PYTHONDONTWRITEBYTECODE": "1"
      },
      "forbidden": [
        "OPENAI_API_KEY",
        "ANTHROPIC_API_KEY"
      ]
    },
    "runtime_identity": {
      "kind": "host-native-capability",
      "name": "task-session",
      "binding_policy": "selected-unit-exact-split-package"
    },
    "risk": {
      "class": "repository-local-reversible",
      "external_effect": false,
      "destructive": false,
      "network": false,
      "model_turn": false,
      "credentials": false
    }
  },
  "execution_mode": "routed-mutation",
  "write_profile": "material-bound",
  "material_writes": [
    "arcanum/tools/arcanum",
    "arcanum/framework/runtime/README.md",
    "arcanum/framework/runtime/adapters/app-server-fixture.md",
    "arcanum/arcana/task-session/runtime-adapters/README.md",
    "arcanum/framework/runtime/adapters/app-server.md",
    "arcanum/framework/runtime/adapters/app_server.py",
    "arcanum/framework/runtime/development/fixtures/app-server/live-fake/fake_app_server.py",
    "arcanum/framework/runtime/development/fixtures/app-server/live-fake/test_app_server_adapter.py",
    "arcanum/framework/runtime/development/fixtures/app-server/live-fake/validate_installed_parity.py",
    "arcanum/arcana/task-session/runtime-adapters/app-server.md"
  ],
  "execution_output_groups": [
    {
      "prefix": "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/SWU-RWO-CX-003R2",
      "members": [
        "executor.json"
      ]
    }
  ],
  "allowed_writes_rule": "Task Session admission materialWrites equals the exact material set; executionOutputs is exactly the separately route-authorized E receipt; allowedWrites is their exact union; pre-execution, validation, and remaining lifecycle paths are excluded",
  "control_artifacts": [
    {
      "path": "ops/development/2026-08-16-rwo-control-content-provenance-successor-r2/candidate-plan-epoch/work-pack/tasks/TASK-RWO-CX-003R2.md",
      "role": "task-contract",
      "authority_class": "private"
    },
    {
      "path": "ops/development/2026-08-16-rwo-control-content-provenance-successor-r2/candidate-plan-epoch/WORK-PACK.md",
      "role": "work-pack",
      "authority_class": "private"
    },
    {
      "path": "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/SWU-RWO-CX-003R2/context-pack.md",
      "role": "context-pack",
      "authority_class": "private"
    }
  ],
  "source_artifacts": [
    {
      "path": "arcanum/tools/arcanum",
      "sha256": "84dff7a59b6c251f3ce038c6b4684b1e29b0df7356a4ae12457061af5a41e231",
      "size_bytes": 73568,
      "authority_class": "public"
    },
    {
      "path": "arcanum/framework/runtime/README.md",
      "sha256": "878fe0c9273d5c03a8861445324d61535bb1c99458ed874a3df52439da59f31c",
      "size_bytes": 5318,
      "authority_class": "public"
    },
    {
      "path": "arcanum/framework/runtime/adapters/app-server-fixture.md",
      "sha256": "866171bfe37ce39e1ff7f6e6dcc5151c75ff6aaecd1f750af55acef0ba98d569",
      "size_bytes": 2135,
      "authority_class": "public"
    },
    {
      "path": "arcanum/arcana/task-session/runtime-adapters/README.md",
      "sha256": "2f6e1a86609a160ff5e6cd2a451a783a80ee5b16ca768db3bf7d3d92e0308712",
      "size_bytes": 2338,
      "authority_class": "public"
    },
    {
      "path": "arcanum/framework/runtime/templates/APP-SERVER-HOST-RESULT.json",
      "sha256": "c7897125ebc39b599d0c23edcc355b243e99da084db5f8f4eb80e7c6e2b8892d",
      "size_bytes": 1070,
      "authority_class": "public"
    },
    {
      "path": "arcanum/framework/runtime/development/fixtures/app-server/validate_fixture.py",
      "sha256": "6802af32b6cc8818f402feaf31df2564bb10513d89523e267ca820e6b5644258",
      "size_bytes": 16110,
      "authority_class": "public"
    },
    {
      "path": "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/INSTALLED-CODEX-SCHEMAS.json",
      "authority_class": "public",
      "exact_ref_source": "CCP-003-terminal"
    },
    {
      "path": "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/INSTALLED-CODEX-METHOD-MANIFEST.json",
      "authority_class": "public",
      "exact_ref_source": "CCP-003-terminal"
    },
    {
      "path": "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/HELPER-REQUEST.json",
      "authority_class": "public",
      "exact_ref_source": "CCP-003-terminal"
    }
  ],
  "source_coverage_evidence": [
    "PUBLIC-INPUT-MANIFEST.json",
    "HELPER-RECEIPT.json",
    "NO-PRIVATE-INPUT-RECEIPT.json",
    "DISCLOSURE-REVIEW-RECEIPT.json",
    "CANDIDATE-MANIFEST.json",
    "TARGET-INVENTORY.json",
    "SWU-RWO-CCP-003/terminal.json"
  ],
  "target_baselines": [
    {
      "path": "arcanum/tools/arcanum",
      "state": "present",
      "sha256": "84dff7a59b6c251f3ce038c6b4684b1e29b0df7356a4ae12457061af5a41e231",
      "size_bytes": 73568,
      "mode": "0755"
    },
    {
      "path": "arcanum/framework/runtime/README.md",
      "state": "present",
      "sha256": "878fe0c9273d5c03a8861445324d61535bb1c99458ed874a3df52439da59f31c",
      "size_bytes": 5318,
      "mode": "0644"
    },
    {
      "path": "arcanum/framework/runtime/adapters/app-server-fixture.md",
      "state": "present",
      "sha256": "866171bfe37ce39e1ff7f6e6dcc5151c75ff6aaecd1f750af55acef0ba98d569",
      "size_bytes": 2135,
      "mode": "0644"
    },
    {
      "path": "arcanum/arcana/task-session/runtime-adapters/README.md",
      "state": "present",
      "sha256": "2f6e1a86609a160ff5e6cd2a451a783a80ee5b16ca768db3bf7d3d92e0308712",
      "size_bytes": 2338,
      "mode": "0644"
    },
    {
      "path": "arcanum/framework/runtime/adapters/app-server.md",
      "state": "absent",
      "sha256": null,
      "size_bytes": null,
      "mode": null
    },
    {
      "path": "arcanum/framework/runtime/adapters/app_server.py",
      "state": "absent",
      "sha256": null,
      "size_bytes": null,
      "mode": null
    },
    {
      "path": "arcanum/framework/runtime/development/fixtures/app-server/live-fake/fake_app_server.py",
      "state": "absent",
      "sha256": null,
      "size_bytes": null,
      "mode": null
    },
    {
      "path": "arcanum/framework/runtime/development/fixtures/app-server/live-fake/test_app_server_adapter.py",
      "state": "absent",
      "sha256": null,
      "size_bytes": null,
      "mode": null
    },
    {
      "path": "arcanum/framework/runtime/development/fixtures/app-server/live-fake/validate_installed_parity.py",
      "state": "absent",
      "sha256": null,
      "size_bytes": null,
      "mode": null
    },
    {
      "path": "arcanum/arcana/task-session/runtime-adapters/app-server.md",
      "state": "absent",
      "sha256": null,
      "size_bytes": null,
      "mode": null
    }
  ],
  "receipt_topology": {
    "E": "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/SWU-RWO-CX-003R2/executor.json",
    "O": "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/SWU-RWO-CX-003R2/owner.json",
    "V": "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/SWU-RWO-CX-003R2/validation.json",
    "P": "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/SWU-RWO-CX-003R2/precloseout.json",
    "C": "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/SWU-RWO-CX-003R2/closeout-owner.json",
    "B": "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/SWU-RWO-CX-003R2/observation.json",
    "T": "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/SWU-RWO-CX-003R2/terminal.json"
  },
  "attempt_contract": {
    "id_policy": "sha256(plan-epoch,swu-id,task-session-request-id,attempt-ordinal=1)",
    "collision_policy": "fresh context/package/request/admission and exact current ten-target baselines required",
    "success_teardown": "join E/O/V/P/C/B/T and route to fresh CX003 sufficiency audit",
    "failure_teardown": "restore any changed public targets, preserve diagnostics, emit no T or successor"
  },
  "authority_class": "public",
  "publication_class": "public",
  "claim_ceiling": "local public adapter candidate plus fake/schema evidence; no live App Server, publication, deployment, release, or production claim",
  "task_session_partition_contract": {
    "schema_version": "arcanum.task-session.fast-entry-partition/v1",
    "runner_semantics": "requested writes equal materialWrites; admission executionOutputs is exactly the separately route-authorized E receipt",
    "route_expected_receipt": "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/SWU-RWO-CX-003R2/executor.json",
    "route_write_scope": [
      "arcanum/arcana/task-session/runtime-adapters/README.md",
      "arcanum/arcana/task-session/runtime-adapters/app-server.md",
      "arcanum/framework/runtime/README.md",
      "arcanum/framework/runtime/adapters/app-server-fixture.md",
      "arcanum/framework/runtime/adapters/app-server.md",
      "arcanum/framework/runtime/adapters/app_server.py",
      "arcanum/framework/runtime/development/fixtures/app-server/live-fake/fake_app_server.py",
      "arcanum/framework/runtime/development/fixtures/app-server/live-fake/test_app_server_adapter.py",
      "arcanum/framework/runtime/development/fixtures/app-server/live-fake/validate_installed_parity.py",
      "arcanum/tools/arcanum",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/SWU-RWO-CX-003R2/executor.json"
    ],
    "pre_execution_controls": [
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/SWU-RWO-CX-003R2/context-pack.md",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/SWU-RWO-CX-003R2/context-pack-index.json",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/SWU-RWO-CX-003R2/material-package.json",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/SWU-RWO-CX-003R2/material-package-receipt.json",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/SWU-RWO-CX-003R2/mutation-admission-request.json",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/SWU-RWO-CX-003R2/mutation-admission-receipt.json"
    ],
    "admission_material_writes": [
      "arcanum/tools/arcanum",
      "arcanum/framework/runtime/README.md",
      "arcanum/framework/runtime/adapters/app-server-fixture.md",
      "arcanum/arcana/task-session/runtime-adapters/README.md",
      "arcanum/framework/runtime/adapters/app-server.md",
      "arcanum/framework/runtime/adapters/app_server.py",
      "arcanum/framework/runtime/development/fixtures/app-server/live-fake/fake_app_server.py",
      "arcanum/framework/runtime/development/fixtures/app-server/live-fake/test_app_server_adapter.py",
      "arcanum/framework/runtime/development/fixtures/app-server/live-fake/validate_installed_parity.py",
      "arcanum/arcana/task-session/runtime-adapters/app-server.md"
    ],
    "admission_execution_outputs": [
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/SWU-RWO-CX-003R2/executor.json"
    ],
    "admission_allowed_writes": [
      "arcanum/arcana/task-session/runtime-adapters/README.md",
      "arcanum/arcana/task-session/runtime-adapters/app-server.md",
      "arcanum/framework/runtime/README.md",
      "arcanum/framework/runtime/adapters/app-server-fixture.md",
      "arcanum/framework/runtime/adapters/app-server.md",
      "arcanum/framework/runtime/adapters/app_server.py",
      "arcanum/framework/runtime/development/fixtures/app-server/live-fake/fake_app_server.py",
      "arcanum/framework/runtime/development/fixtures/app-server/live-fake/test_app_server_adapter.py",
      "arcanum/framework/runtime/development/fixtures/app-server/live-fake/validate_installed_parity.py",
      "arcanum/tools/arcanum",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/SWU-RWO-CX-003R2/executor.json"
    ],
    "target_baseline_paths": [
      "arcanum/tools/arcanum",
      "arcanum/framework/runtime/README.md",
      "arcanum/framework/runtime/adapters/app-server-fixture.md",
      "arcanum/arcana/task-session/runtime-adapters/README.md",
      "arcanum/framework/runtime/adapters/app-server.md",
      "arcanum/framework/runtime/adapters/app_server.py",
      "arcanum/framework/runtime/development/fixtures/app-server/live-fake/fake_app_server.py",
      "arcanum/framework/runtime/development/fixtures/app-server/live-fake/test_app_server_adapter.py",
      "arcanum/framework/runtime/development/fixtures/app-server/live-fake/validate_installed_parity.py",
      "arcanum/arcana/task-session/runtime-adapters/app-server.md"
    ],
    "validation_outputs": [
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/SWU-RWO-CX-003R2/validation.json"
    ],
    "lifecycle_outputs": [
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/SWU-RWO-CX-003R2/owner.json",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/SWU-RWO-CX-003R2/precloseout.json",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/SWU-RWO-CX-003R2/closeout-owner.json",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/SWU-RWO-CX-003R2/observation.json",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/SWU-RWO-CX-003R2/terminal.json"
    ]
  }
}
```

## Task Session Fast-Entry Partition

The route expected receipt is `projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/SWU-RWO-CX-003R2/executor.json` and is independently authorized by the Execution Entry route. Pre-execution controls are built before executor mutation. The mutation admission uses only the exact partition above. `V` is validation evidence; `O/P/C/B/T` remain lifecycle outputs. None of those paths is laundered into the executor mutation set. The accepted R1 admission/token is unconsumed historical evidence but is invalid for this R2 Work Pack identity and must never be replayed.


## Split Admission Contract

Build a strict Context Builder index whose `selected_sources` exactly equals the nine content sources above by normalized path/digest/size/authority and includes nonempty obligation coverage. Build material package `1.1.0` with the three private controls and the nine public sources. The frontiers must be nonempty, exact, normalized-path-disjoint, independently duplicate-free, and version-correct. Build request `1.3.0` with matching `controlArtifacts` and `sourceArtifacts`. Any missing/stale/private/uncovered/self-asserted source, role mismatch, cross-version pairing, or frontier mismatch blocks.

The clean-room staged ten files are outputs, never sources. Their target/output mapping and hashes must equal the CCP-003 candidate manifest and terminal. The old CX003R-R2 material package, rejecting receipt, and staged bytes are historical evidence only and must not be read or compared during this unit.

## Exact Validation Contracts

1. `bash -n tools/arcanum` from cwd `arcanum`; exit 0.
2. `python3 -m unittest discover -s framework/runtime/development/fixtures/app-server/live-fake -p test_app_server_adapter.py` from cwd `arcanum`; exit 0.
3. `tools/arcanum --resolve-adapter app-server` from cwd `arcanum`; exit 0 and exact public adapter path.
4. Run `validate_installed_parity.py` with the exact Codex binary/digest and a run-local output; exit 0 and all seven methods pass without starting App Server/model/network.
5. Rehash exact ten applied outputs against clean-room candidate manifest; validate modes, no undeclared delta, no private token/prose, and scoped whitespace; exit 0.
6. Owner review confirms raw evidence authority is null and Task Session remains semantic/lifecycle owner.

## Apply, Rollback, Closeout, Handoff

Task Session alone consumes one fresh single-use 1.3 admission and applies exactly ten changes. Any baseline, package, source, validation, disclosure, or owner failure restores all changed targets to pre-attempt state, leaves absent targets absent, preserves diagnostics, and emits no T. Success requires E/O/V/P/C/B/T with exact package/admission/source/candidate/validation bindings. After the terminal sentinel, hand T to the public-runtime sufficiency owner for one fresh `SWU-RWO-CX-003` audit attempt; never project CX004 directly.

## First Stop

Missing exact acceptance/CCP-003 terminal; source/control overlap or mismatch; private/uncovered content source; old staged-byte access; target drift/collision; partial apply; validation or rollback failure; undeclared write; network/model/live App Server/credential/Git/publication/promotion/deploy/release effect.

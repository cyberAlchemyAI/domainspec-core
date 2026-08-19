# TASK-RWO-CCP-003 — Public-Only Clean-Room Adapter Rematerialization

```json
{
  "schema_version": "rwo.task-contract/v2",
  "task_id": "TASK-RWO-CCP-003",
  "swu_id": "SWU-RWO-CCP-003",
  "primary_owner": "public-clean-room-owner",
  "dependencies": [
    "SWU-RWO-CCP-002"
  ],
  "canonical_successors": [
    "SWU-RWO-CX-003R2"
  ],
  "objective": "Reconstruct, validate, and independently review ten public adapter candidate bytes from exact public inputs only.",
  "command": {
    "argv": [
      "task-session",
      "execute",
      "--work-pack",
      "WP-RWO-CONTROL-CONTENT-PROVENANCE-002",
      "--swu",
      "SWU-RWO-CCP-003",
      "--task",
      "ops/development/2026-08-16-rwo-control-content-provenance-successor-r4/candidate-plan-epoch/work-pack/tasks/TASK-RWO-CCP-003.md"
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
      "binding_policy": "selected-unit-exact-protected-helper"
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
  "write_profile": "execution-output-only",
  "material_writes": [],
  "execution_output_groups": [
    {
      "prefix": "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1",
      "members": [
        "PUBLIC-INPUT-MANIFEST.json",
        "INSTALLED-CODEX-SCHEMAS.json",
        "INSTALLED-CODEX-METHOD-MANIFEST.json",
        "INSTALLED-PARITY.json",
        "HELPER-REQUEST.json",
        "HELPER-RECEIPT.json",
        "NO-PRIVATE-INPUT-RECEIPT.json",
        "DISCLOSURE-REVIEW-RECEIPT.json",
        "CANDIDATE-MANIFEST.json",
        "TARGET-INVENTORY.json"
      ]
    },
    {
      "prefix": "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/staged",
      "members": [
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
      ]
    }
  ],
  "allowed_writes_rule": "expand the exact execution_output_groups as output-only mutation outputs; the separately route-authorized E receipt, pre-execution controls, validation output, and lifecycle outputs are excluded",
  "public_helper_inputs": [
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
    }
  ],
  "installed_protocol_binding": {
    "codex_path": "/home/vrondelli/.vscode-server/extensions/openai.chatgpt-26.810.50856/bin/linux-x86_64/codex",
    "codex_sha256": "86a4286b2451c69d4c00ad1772fcee5170013f2924e7d257ad2d4f19290c2a20",
    "codex_version": "codex-cli 0.148.0-alpha.9",
    "schema_file_count": 285,
    "required_methods": [
      "initialize",
      "initialized",
      "thread/start",
      "turn/start",
      "turn/interrupt",
      "item/commandExecution/requestApproval",
      "turn/completed"
    ],
    "evidence_ceiling": "fresh generated-schema evidence only; no App Server/model execution"
  },
  "generic_helper_request_contract": {
    "path": "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/HELPER-REQUEST.json",
    "authority_class": "public",
    "exact_binding": "CCP-003 terminal binds path, sha256, size_bytes, public classification, obligations, and helper context digest"
  },
  "immutable_and_forbidden": [
    "ops/development/2026-08-16-rwo-control-content-provenance-successor-r4/candidate-plan-epoch",
    "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/RWO-CODEX-MIGRATION-001",
    "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/bootstrap",
    ".git",
    ".craft",
    "telemetry",
    "ops/development/2026-08-16-rwo-control-content-provenance-successor/candidate-plan-epoch",
    "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-001"
  ],
  "receipt_topology": {
    "E": "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/SWU-RWO-CCP-003/executor.json",
    "O": "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/SWU-RWO-CCP-003/owner.json",
    "V": "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/SWU-RWO-CCP-003/validation.json",
    "P": "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/SWU-RWO-CCP-003/precloseout.json",
    "C": "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/SWU-RWO-CCP-003/closeout-owner.json",
    "B": "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/SWU-RWO-CCP-003/observation.json",
    "T": "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/SWU-RWO-CCP-003/terminal.json"
  },
  "attempt_contract": {
    "id_policy": "sha256(plan-epoch,swu-id,task-session-request-id,attempt-ordinal=1)",
    "collision_policy": "all clean-room outputs absent; no resume after helper spawn unless exact helper input digest and output manifest match",
    "success_teardown": "join helper, disclosure reviewer, E/O/V/P/C/B/T; expose CX003R2",
    "failure_teardown": "preserve diagnostics and isolated outputs, emit no T, expose no apply route"
  },
  "authority_class": "private",
  "publication_class": "internal",
  "claim_ceiling": "public-classified staged candidate and local fake/schema evidence only; no public target mutation",
  "task_session_partition_contract": {
    "schema_version": "arcanum.task-session.fast-entry-partition/v1",
    "runner_semantics": "requested writes equal output-only mutation execution outputs and exclude the separately route-authorized E receipt",
    "route_expected_receipt": "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/SWU-RWO-CCP-003/executor.json",
    "route_write_scope": [
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/SWU-RWO-CCP-003/executor.json",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/CANDIDATE-MANIFEST.json",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/DISCLOSURE-REVIEW-RECEIPT.json",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/HELPER-RECEIPT.json",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/HELPER-REQUEST.json",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/INSTALLED-CODEX-METHOD-MANIFEST.json",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/INSTALLED-CODEX-SCHEMAS.json",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/INSTALLED-PARITY.json",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/NO-PRIVATE-INPUT-RECEIPT.json",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/PUBLIC-INPUT-MANIFEST.json",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/TARGET-INVENTORY.json",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/staged/arcanum/arcana/task-session/runtime-adapters/README.md",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/staged/arcanum/arcana/task-session/runtime-adapters/app-server.md",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/staged/arcanum/framework/runtime/README.md",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/staged/arcanum/framework/runtime/adapters/app-server-fixture.md",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/staged/arcanum/framework/runtime/adapters/app-server.md",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/staged/arcanum/framework/runtime/adapters/app_server.py",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/staged/arcanum/framework/runtime/development/fixtures/app-server/live-fake/fake_app_server.py",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/staged/arcanum/framework/runtime/development/fixtures/app-server/live-fake/test_app_server_adapter.py",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/staged/arcanum/framework/runtime/development/fixtures/app-server/live-fake/validate_installed_parity.py",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/staged/arcanum/tools/arcanum"
    ],
    "pre_execution_controls": [
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/SWU-RWO-CCP-003/context-pack.md",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/SWU-RWO-CCP-003/context-pack-index.json",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/SWU-RWO-CCP-003/mutation-admission-request.json",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/SWU-RWO-CCP-003/mutation-admission-receipt.json"
    ],
    "admission_material_writes": [],
    "admission_execution_outputs": [
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/PUBLIC-INPUT-MANIFEST.json",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/INSTALLED-CODEX-SCHEMAS.json",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/INSTALLED-CODEX-METHOD-MANIFEST.json",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/INSTALLED-PARITY.json",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/HELPER-REQUEST.json",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/HELPER-RECEIPT.json",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/NO-PRIVATE-INPUT-RECEIPT.json",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/DISCLOSURE-REVIEW-RECEIPT.json",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/CANDIDATE-MANIFEST.json",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/TARGET-INVENTORY.json",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/staged/arcanum/tools/arcanum",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/staged/arcanum/framework/runtime/README.md",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/staged/arcanum/framework/runtime/adapters/app-server-fixture.md",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/staged/arcanum/arcana/task-session/runtime-adapters/README.md",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/staged/arcanum/framework/runtime/adapters/app-server.md",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/staged/arcanum/framework/runtime/adapters/app_server.py",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/staged/arcanum/framework/runtime/development/fixtures/app-server/live-fake/fake_app_server.py",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/staged/arcanum/framework/runtime/development/fixtures/app-server/live-fake/test_app_server_adapter.py",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/staged/arcanum/framework/runtime/development/fixtures/app-server/live-fake/validate_installed_parity.py",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/staged/arcanum/arcana/task-session/runtime-adapters/app-server.md"
    ],
    "admission_allowed_writes": [
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/CANDIDATE-MANIFEST.json",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/DISCLOSURE-REVIEW-RECEIPT.json",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/HELPER-RECEIPT.json",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/HELPER-REQUEST.json",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/INSTALLED-CODEX-METHOD-MANIFEST.json",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/INSTALLED-CODEX-SCHEMAS.json",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/INSTALLED-PARITY.json",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/NO-PRIVATE-INPUT-RECEIPT.json",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/PUBLIC-INPUT-MANIFEST.json",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/TARGET-INVENTORY.json",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/staged/arcanum/arcana/task-session/runtime-adapters/README.md",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/staged/arcanum/arcana/task-session/runtime-adapters/app-server.md",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/staged/arcanum/framework/runtime/README.md",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/staged/arcanum/framework/runtime/adapters/app-server-fixture.md",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/staged/arcanum/framework/runtime/adapters/app-server.md",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/staged/arcanum/framework/runtime/adapters/app_server.py",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/staged/arcanum/framework/runtime/development/fixtures/app-server/live-fake/fake_app_server.py",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/staged/arcanum/framework/runtime/development/fixtures/app-server/live-fake/test_app_server_adapter.py",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/staged/arcanum/framework/runtime/development/fixtures/app-server/live-fake/validate_installed_parity.py",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/staged/arcanum/tools/arcanum"
    ],
    "target_baseline_paths": [
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/PUBLIC-INPUT-MANIFEST.json",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/INSTALLED-CODEX-SCHEMAS.json",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/INSTALLED-CODEX-METHOD-MANIFEST.json",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/INSTALLED-PARITY.json",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/HELPER-REQUEST.json",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/HELPER-RECEIPT.json",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/NO-PRIVATE-INPUT-RECEIPT.json",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/DISCLOSURE-REVIEW-RECEIPT.json",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/CANDIDATE-MANIFEST.json",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/TARGET-INVENTORY.json",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/staged/arcanum/tools/arcanum",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/staged/arcanum/framework/runtime/README.md",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/staged/arcanum/framework/runtime/adapters/app-server-fixture.md",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/staged/arcanum/arcana/task-session/runtime-adapters/README.md",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/staged/arcanum/framework/runtime/adapters/app-server.md",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/staged/arcanum/framework/runtime/adapters/app_server.py",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/staged/arcanum/framework/runtime/development/fixtures/app-server/live-fake/fake_app_server.py",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/staged/arcanum/framework/runtime/development/fixtures/app-server/live-fake/test_app_server_adapter.py",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/staged/arcanum/framework/runtime/development/fixtures/app-server/live-fake/validate_installed_parity.py",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/clean-room/CX003R2-R1/staged/arcanum/arcana/task-session/runtime-adapters/app-server.md"
    ],
    "validation_outputs": [
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/SWU-RWO-CCP-003/validation.json"
    ],
    "lifecycle_outputs": [
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/SWU-RWO-CCP-003/owner.json",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/SWU-RWO-CCP-003/precloseout.json",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/SWU-RWO-CCP-003/closeout-owner.json",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/SWU-RWO-CCP-003/observation.json",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/SWU-RWO-CCP-003/terminal.json"
    ]
  }
}
```

## Task Session Fast-Entry Partition

The route expected receipt is `projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/SWU-RWO-CCP-003/executor.json` and is independently authorized by the Execution Entry route. Pre-execution controls are built before executor mutation. The mutation admission uses only the exact partition above. `V` is validation evidence; `O/P/C/B/T` remain lifecycle outputs. None of those paths is laundered into the executor mutation set. Earlier selection/admission artifacts are historical evidence only and invalid for this R4 candidate.


## Protected Helper Boundary

Task Session may read private governance controls to select the unit, but it must construct a distinct helper request containing only the exact six public Arcanum inputs, fresh installed schema bundle/method manifest, generic adapter objective, ten output paths, and validation contract above. The helper has no repository exploration fallback. The helper write scope is exactly the ten staged paths plus `HELPER-RECEIPT.json`; Task Session owns all other outputs.

The helper and disclosure reviewer must not receive or read any private plan/task/context/decision/finding, the bootstrap capsule, or any byte under the old `CX003R-R2` material/staging root. The old staged bytes are comparison-forbidden: no `diff`, `cmp`, hash comparison, import, copy, prompt excerpt, or semantic review against them is permitted. They remain non-authoritative historical evidence.

## Public Source And Obligation Contract

`PUBLIC-INPUT-MANIFEST.json` exact-binds the six Arcanum files, fresh installed schema/method artifacts, and public-classified generic helper request by path/digest/size/authority. Every input and every candidate output maps to one or more generic obligations: provider-neutral registration, bounded stdio JSON-RPC transport, exact correlation and teardown, raw host evidence with null semantic authority, fake local validation, installed seven-method schema parity, Task Session ownership, and public/private noninterference.

The helper receipt lists the complete read set, input digest, write set, output hashes/sizes/modes, runtime identity, and zero forbidden access. `NO-PRIVATE-INPUT-RECEIPT.json` independently compares the dispatch context/read trace to the denylist. `DISCLOSURE-REVIEW-RECEIPT.json` independently reviews only public inputs and new outputs; verdict must be `pass` with no private token/path/prose finding.

## Exact Validation Contracts

1. Generate schemas with the exact bound Codex binary into an isolated temporary directory, parse all 285 JSON files, sort by normalized relative path, serialize one UTF-8 canonical JSON object with sorted keys and compact separators into `INSTALLED-CODEX-SCHEMAS.json`, and emit a method/path/hash manifest binding the construction algorithm and consolidated artifact hash; binary/schema/count/method/hash drift blocks.
2. `bash -n <clean-root>/staged/arcanum/tools/arcanum` — exit 0.
3. `<clean-root>/staged/arcanum/tools/arcanum --resolve-adapter app-server` — exit 0 and resolves inside the clean staging root.
4. `python3 -m unittest discover -s <clean-root>/staged/arcanum/framework/runtime/development/fixtures/app-server/live-fake -p test_app_server_adapter.py` — exit 0; no network/model/credential use.
5. Run staged `validate_installed_parity.py` with the exact Codex path/digest and output `INSTALLED-PARITY.json`; exit 0 and all seven methods pass.
6. Parse all JSON outputs; validate exact ten-entry target inventory and candidate manifest; expected exit 0.
7. Require no-private-input and disclosure verdicts pass; exact helper input/read/write/output closure; no forbidden access.
8. Scoped whitespace and executable-mode checks over the ten staged outputs; exit 0.
9. Rehash all live public inputs; they remain unchanged.

## First Stop

Missing exact acceptance/CCP-002 terminal; public input or binary drift; output collision; helper context/read expansion; old staged-byte access; private disclosure; incomplete source-obligation coverage; malformed/unknown/oversized/timeout/teardown test failure; undeclared write; live public target change; network/model/App Server/credential/Git/publication/promotion/deploy/release effect.

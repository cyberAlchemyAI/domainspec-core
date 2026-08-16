# TASK-RWO-CX-003R - Public App Server Adapter Repair

~~~json
{
  "schema_version": "rwo.task-contract/v2",
  "task_id": "TASK-RWO-CX-003R",
  "swu_id": "SWU-RWO-CX-003R",
  "primary_owner": "public-runtime-owner",
  "dependencies": [],
  "canonical_successors": [
    "TERMINAL:CX003R-WORK-PACK"
  ],
  "objective": "Make the public app-server adapter selectable and executable through tools/arcanum while preserving Task Session as semantic owner.",
  "primary_behavior": "one generic bounded stdio App Server adapter from selection through raw host evidence and return to Task Session",
  "command": {
    "argv": [
      "task-session",
      "execute",
      "--work-pack",
      "WP-RWO-CODEX-APP-SERVER-REPAIR-001",
      "--swu",
      "SWU-RWO-CX-003R",
      "--task",
      "ops/development/2026-08-16-rwo-cx003r-public-runtime-repair/candidate-plan-epoch/work-pack/tasks/TASK-RWO-CX-003R.md"
    ],
    "cwd": ".",
    "expected_exit": 0,
    "timeout_seconds": 1800,
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
      "binding_policy": "selected-unit-exact-package",
      "required_fields": [
        "resolved_path",
        "version",
        "sha256"
      ]
    },
    "risk": {
      "class": "repository-local-reversible-public-runtime-source",
      "external_effect": false,
      "destructive": false,
      "network": false,
      "model_turn": false,
      "credentials": false
    }
  },
  "implementation_detail": {
    "inputs": [
      "strict Task Session context pack",
      "immutable CX003 finding and validation",
      "exact ten-path baseline",
      "installed Codex identity and generated schemas"
    ],
    "outputs": [
      "one public adapter registration/profile/driver/test/docs set",
      "one private installed-parity receipt",
      "E/O/V/P/C/B/T receipts"
    ],
    "ordered_rules": [
      "rehash all ten baselines and stop on collision or drift",
      "stage all material bytes through Invoke Refresh after selection",
      "register app-server only with its executable driver and fail-closed profile",
      "spawn only the explicit fake stdio process during execution tests",
      "correlate JSON-RPC ids, bound message size and timeout, persist raw result evidence, and reject unknown or malformed messages",
      "generate schemas from the bound installed Codex binary without starting App Server",
      "verify initialize, initialized, thread/start, turn/start, turn/interrupt, item/commandExecution/requestApproval, and turn/completed",
      "keep all semantic and lifecycle authority null in adapter evidence",
      "close E/O/V/P/C/B/T before routing to a fresh CX003 audit attempt"
    ],
    "edge_cases": [
      "missing binary",
      "binary digest drift",
      "schema method missing",
      "duplicate response id",
      "unknown notification",
      "oversized line",
      "timeout",
      "child exits early",
      "malformed JSON",
      "permission request without response",
      "interrupt before terminal"
    ],
    "failure_modes": [
      "no partial registration acceptance",
      "no inferred success",
      "no retry after ambiguous write",
      "no terminal receipt",
      "no CX003 or CX004 successor"
    ]
  },
  "validation_contracts": [
    {
      "command_id": "cx003r-shell-syntax",
      "argv": [
        "bash",
        "-n",
        "tools/arcanum"
      ],
      "cwd": "arcanum",
      "expected_exit": 0,
      "timeout_seconds": 60,
      "max_output_bytes": 1048576,
      "environment": {
        "inherit_allowlist": [
          "PATH"
        ],
        "fixed": {
          "LC_ALL": "C"
        }
      },
      "runtime_identity": {
        "executable": "bash",
        "version_policy": "capture-path-version-sha256-at-admission"
      },
      "risk": "read-only"
    },
    {
      "command_id": "cx003r-fake-stdio",
      "argv": [
        "python3",
        "-m",
        "unittest",
        "discover",
        "-s",
        "framework/runtime/development/fixtures/app-server/live-fake",
        "-p",
        "test_app_server_adapter.py"
      ],
      "cwd": "arcanum",
      "expected_exit": 0,
      "timeout_seconds": 300,
      "max_output_bytes": 4194304,
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
        "executable": "python3",
        "version_policy": "capture-path-version-sha256-at-admission"
      },
      "risk": "read-only-local-fake-process"
    },
    {
      "command_id": "cx003r-adapter-resolution",
      "argv": [
        "tools/arcanum",
        "--resolve-adapter",
        "app-server"
      ],
      "cwd": "arcanum",
      "expected_exit": 0,
      "timeout_seconds": 60,
      "max_output_bytes": 1048576,
      "environment": {
        "inherit_allowlist": [
          "PATH"
        ],
        "fixed": {
          "LC_ALL": "C"
        },
        "forbidden": [
          "OPENAI_API_KEY",
          "ANTHROPIC_API_KEY"
        ]
      },
      "runtime_identity": {
        "executable": "tools/arcanum",
        "version_policy": "capture-path-sha256-at-admission"
      },
      "risk": "read-only"
    },
    {
      "command_id": "cx003r-installed-schema-parity",
      "argv": [
        "python3",
        "framework/runtime/development/fixtures/app-server/live-fake/validate_installed_parity.py",
        "--codex-bin",
        "/home/vrondelli/.vscode-server/extensions/openai.chatgpt-26.810.50856/bin/linux-x86_64/codex",
        "--expected-codex-sha256",
        "86a4286b2451c69d4c00ad1772fcee5170013f2924e7d257ad2d4f19290c2a20",
        "--output",
        "../projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/RWO-CODEX-MIGRATION-001/public-runtime-repair/INSTALLED-PARITY.json"
      ],
      "cwd": "arcanum",
      "expected_exit": 0,
      "timeout_seconds": 300,
      "max_output_bytes": 4194304,
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
        "executable": "python3",
        "version_policy": "capture-path-version-sha256-at-admission"
      },
      "risk": "bounded-write-private-evidence-only"
    }
  ],
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
  "execution_outputs": [
    "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/RWO-CODEX-MIGRATION-001/public-runtime-repair/INSTALLED-PARITY.json",
    "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/RWO-CODEX-MIGRATION-001/SWU-RWO-CX-003R/executor.json",
    "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/RWO-CODEX-MIGRATION-001/SWU-RWO-CX-003R/owner.json",
    "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/RWO-CODEX-MIGRATION-001/SWU-RWO-CX-003R/validation.json",
    "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/RWO-CODEX-MIGRATION-001/SWU-RWO-CX-003R/precloseout.json",
    "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/RWO-CODEX-MIGRATION-001/SWU-RWO-CX-003R/closeout-owner.json",
    "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/RWO-CODEX-MIGRATION-001/SWU-RWO-CX-003R/observation.json",
    "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/RWO-CODEX-MIGRATION-001/SWU-RWO-CX-003R/terminal.json"
  ],
  "allowed_writes": [
    "arcanum/tools/arcanum",
    "arcanum/framework/runtime/README.md",
    "arcanum/framework/runtime/adapters/app-server-fixture.md",
    "arcanum/arcana/task-session/runtime-adapters/README.md",
    "arcanum/framework/runtime/adapters/app-server.md",
    "arcanum/framework/runtime/adapters/app_server.py",
    "arcanum/framework/runtime/development/fixtures/app-server/live-fake/fake_app_server.py",
    "arcanum/framework/runtime/development/fixtures/app-server/live-fake/test_app_server_adapter.py",
    "arcanum/framework/runtime/development/fixtures/app-server/live-fake/validate_installed_parity.py",
    "arcanum/arcana/task-session/runtime-adapters/app-server.md",
    "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/RWO-CODEX-MIGRATION-001/public-runtime-repair/INSTALLED-PARITY.json",
    "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/RWO-CODEX-MIGRATION-001/SWU-RWO-CX-003R/executor.json",
    "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/RWO-CODEX-MIGRATION-001/SWU-RWO-CX-003R/owner.json",
    "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/RWO-CODEX-MIGRATION-001/SWU-RWO-CX-003R/validation.json",
    "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/RWO-CODEX-MIGRATION-001/SWU-RWO-CX-003R/precloseout.json",
    "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/RWO-CODEX-MIGRATION-001/SWU-RWO-CX-003R/closeout-owner.json",
    "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/RWO-CODEX-MIGRATION-001/SWU-RWO-CX-003R/observation.json",
    "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/RWO-CODEX-MIGRATION-001/SWU-RWO-CX-003R/terminal.json"
  ],
  "target_baselines": [
    {
      "path": "arcanum/tools/arcanum",
      "state": "present",
      "sha256": "84dff7a59b6c251f3ce038c6b4684b1e29b0df7356a4ae12457061af5a41e231",
      "size_bytes": 73568,
      "type": "file",
      "mode": "0755"
    },
    {
      "path": "arcanum/framework/runtime/README.md",
      "state": "present",
      "sha256": "878fe0c9273d5c03a8861445324d61535bb1c99458ed874a3df52439da59f31c",
      "size_bytes": 5318,
      "type": "file",
      "mode": "0644"
    },
    {
      "path": "arcanum/framework/runtime/adapters/app-server-fixture.md",
      "state": "present",
      "sha256": "866171bfe37ce39e1ff7f6e6dcc5151c75ff6aaecd1f750af55acef0ba98d569",
      "size_bytes": 2135,
      "type": "file",
      "mode": "0644"
    },
    {
      "path": "arcanum/arcana/task-session/runtime-adapters/README.md",
      "state": "present",
      "sha256": "2f6e1a86609a160ff5e6cd2a451a783a80ee5b16ca768db3bf7d3d92e0308712",
      "size_bytes": 2338,
      "type": "file",
      "mode": "0644"
    },
    {
      "path": "arcanum/framework/runtime/adapters/app-server.md",
      "state": "absent",
      "sha256": null,
      "size_bytes": null,
      "type": null,
      "mode": null
    },
    {
      "path": "arcanum/framework/runtime/adapters/app_server.py",
      "state": "absent",
      "sha256": null,
      "size_bytes": null,
      "type": null,
      "mode": null
    },
    {
      "path": "arcanum/framework/runtime/development/fixtures/app-server/live-fake/fake_app_server.py",
      "state": "absent",
      "sha256": null,
      "size_bytes": null,
      "type": null,
      "mode": null
    },
    {
      "path": "arcanum/framework/runtime/development/fixtures/app-server/live-fake/test_app_server_adapter.py",
      "state": "absent",
      "sha256": null,
      "size_bytes": null,
      "type": null,
      "mode": null
    },
    {
      "path": "arcanum/framework/runtime/development/fixtures/app-server/live-fake/validate_installed_parity.py",
      "state": "absent",
      "sha256": null,
      "size_bytes": null,
      "type": null,
      "mode": null
    },
    {
      "path": "arcanum/arcana/task-session/runtime-adapters/app-server.md",
      "state": "absent",
      "sha256": null,
      "size_bytes": null,
      "type": null,
      "mode": null
    }
  ],
  "immutable_paths": [
    "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/refinement-runs/20260814T191109Z-rwo-codex-runtime-migration/refresh-runs/20260815T140002Z-execution-readiness-repair/candidate-plan-epoch",
    "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/RWO-CODEX-MIGRATION-001/public-sufficiency",
    "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/RWO-CODEX-MIGRATION-001/SWU-RWO-CX-002/terminal.json",
    "projects/cyberalchemy-orchestrator/implementations/rwo-sidecar-go/codex_profile.go",
    "projects/cyberalchemy-orchestrator/implementations/rwo-sidecar-go/codex_protocol.go",
    "projects/cyberalchemy-orchestrator/implementations/rwo-sidecar-go/codex_contract_test.go",
    "arcanum/framework/runtime/templates/APP-SERVER-HOST-RESULT.json",
    "arcanum/framework/runtime/development/fixtures/app-server/validate_fixture.py",
    "Inventory",
    ".craft",
    "telemetry",
    ".git"
  ],
  "installed_protocol_binding": {
    "codex_path": "/home/vrondelli/.vscode-server/extensions/openai.chatgpt-26.810.50856/bin/linux-x86_64/codex",
    "codex_sha256": "86a4286b2451c69d4c00ad1772fcee5170013f2924e7d257ad2d4f19290c2a20",
    "codex_version": "codex-cli 0.148.0-alpha.9",
    "schema_file_count": 285,
    "schema_manifest_sha256": "40c152e6540afeaece50e7367755e44bc9d15eecafc1224ad5fdda0292787bf5",
    "required_methods": [
      "initialize",
      "initialized",
      "thread/start",
      "turn/start",
      "turn/interrupt",
      "item/commandExecution/requestApproval",
      "turn/completed"
    ],
    "evidence_ceiling": "installed generated-schema parity only; no App Server or model execution"
  },
  "attempt_contract": {
    "id_policy": "sha256(semantic-epoch,swu-id,task-session-request-id,attempt-ordinal=1)",
    "collision_policy": "same-id-same-input may resume; any baseline, package, binary, schema, or output mismatch blocks",
    "success_teardown": "join E/O/V/P/C/B/T, close the in-pack terminal sentinel, then hand off to the public-runtime sufficiency owner for a fresh SWU-RWO-CX-003 audit attempt",
    "failure_teardown": "retain diagnostics, no T, no public acceptance, no successor, no App Server/model/network effect"
  },
  "receipt_topology": {
    "E": {
      "path": "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/RWO-CODEX-MIGRATION-001/SWU-RWO-CX-003R/executor.json",
      "owner": "task-session-executor"
    },
    "O": {
      "path": "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/RWO-CODEX-MIGRATION-001/SWU-RWO-CX-003R/owner.json",
      "owner": "public-runtime-owner"
    },
    "V": {
      "path": "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/RWO-CODEX-MIGRATION-001/SWU-RWO-CX-003R/validation.json",
      "owner": "task-session-validation-reconciler"
    },
    "P": {
      "path": "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/RWO-CODEX-MIGRATION-001/SWU-RWO-CX-003R/precloseout.json",
      "owner": "task-session-precloseout-owner"
    },
    "C": {
      "path": "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/RWO-CODEX-MIGRATION-001/SWU-RWO-CX-003R/closeout-owner.json",
      "owner": "task-session-closeout-owner"
    },
    "B": {
      "path": "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/RWO-CODEX-MIGRATION-001/SWU-RWO-CX-003R/observation.json",
      "owner": "signal-observer"
    },
    "T": {
      "path": "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/RWO-CODEX-MIGRATION-001/SWU-RWO-CX-003R/terminal.json",
      "owner": "task-session-governance-terminal-owner"
    }
  },
  "closeout_sync": {
    "terminal_source_receipt": "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/RWO-CODEX-MIGRATION-001/SWU-RWO-CX-003R/terminal.json",
    "synchronization_targets": [
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/RWO-CODEX-MIGRATION-001/public-runtime-repair/INSTALLED-PARITY.json",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/RWO-CODEX-MIGRATION-001/SWU-RWO-CX-003R/executor.json",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/RWO-CODEX-MIGRATION-001/SWU-RWO-CX-003R/owner.json",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/RWO-CODEX-MIGRATION-001/SWU-RWO-CX-003R/validation.json",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/RWO-CODEX-MIGRATION-001/SWU-RWO-CX-003R/precloseout.json",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/RWO-CODEX-MIGRATION-001/SWU-RWO-CX-003R/closeout-owner.json",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/RWO-CODEX-MIGRATION-001/SWU-RWO-CX-003R/observation.json",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/RWO-CODEX-MIGRATION-001/SWU-RWO-CX-003R/terminal.json"
    ],
    "baseline_binding": "exact ten-entry target_baselines",
    "admitted_delta_classes": [
      "create",
      "modify"
    ],
    "forbidden_delta_classes": [
      "delete",
      "move",
      "mode-change-outside-declared-baseline"
    ],
    "lifecycle_owner_validation": "public-runtime-owner O receipt binds all ten material hashes and four validation results",
    "expected_owner_receipt": "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/RWO-CODEX-MIGRATION-001/SWU-RWO-CX-003R/owner.json",
    "successor_policy": "close this one-unit graph at TERMINAL:CX003R-WORK-PACK; after T, hand off to the public-runtime sufficiency owner for a fresh SWU-RWO-CX-003 audit attempt; never CX004 directly"
  },
  "split_analysis": {
    "candidate_children": [
      "registration",
      "stdio driver",
      "fake test",
      "installed parity",
      "documentation"
    ],
    "retained_boundary": "All children are required to expose one safely selectable/executable behavior; no subset independently satisfies acceptance."
  },
  "execution_owner_recommendation": "local-fallback",
  "handoff_note": "Build one strict context pack from this task, the Work Pack, immutable CX003 finding/validation, public target baselines, and installed protocol binding. Do not inspect or copy private capsule source.",
  "expected_result_shape": {
    "result": "pass|flag|block|interrupted",
    "files_touched": "exact allowed_writes subset",
    "validation": "four exact commands",
    "blockers": "array",
    "residue": "array",
    "reroute": "fresh CX003 audit or none"
  },
  "first_stop": [
    "baseline drift",
    "private capsule copy",
    "duplicate controller",
    "public write outside ten paths",
    "installed binary drift",
    "missing required schema method",
    "network/model/provider effect",
    "failed acceptance-critical validation"
  ],
  "claim_ceiling": "public adapter candidate and local fake/schema evidence only; no live App Server compatibility, framework acceptance, semantic acceptance, publication, deployment, release, or production claim"
}
~~~

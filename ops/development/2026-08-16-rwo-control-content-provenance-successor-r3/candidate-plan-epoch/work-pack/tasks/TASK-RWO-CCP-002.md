# TASK-RWO-CCP-002 — Atomic Provenance Contract And Native Runtime Repair

```json
{
  "schema_version": "rwo.task-contract/v2",
  "task_id": "TASK-RWO-CCP-002",
  "swu_id": "SWU-RWO-CCP-002",
  "primary_owner": "provenance-contract-owner",
  "dependencies": [],
  "external_predecessor_receipts": [
    {
      "dependency_id": "SWU-RWO-CCP-001",
      "artifact_ref": {
        "path": "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/SWU-RWO-CCP-001/terminal.json",
        "sha256": "ad79f1c55fb50b4a3fb78afcaa890611fa7832a1be4edeb699cd5fe9dc6b1223",
        "size_bytes": 6234
      },
      "required_result": "pass",
      "continuation_role": "immutable-completed-predecessor"
    }
  ],
  "canonical_successors": [
    "SWU-RWO-CCP-003"
  ],
  "objective": "Use only the public-safe bootstrap capsule to atomically install separated provenance admission in canonical and generated native runtime surfaces.",
  "command": {
    "argv": [
      "task-session",
      "execute",
      "--work-pack",
      "WP-RWO-CONTROL-CONTENT-PROVENANCE-002",
      "--swu",
      "SWU-RWO-CCP-002",
      "--task",
      "ops/development/2026-08-16-rwo-control-content-provenance-successor-r3/candidate-plan-epoch/work-pack/tasks/TASK-RWO-CCP-002.md"
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
      "binding_policy": "selected-unit-exact-public-bootstrap-package"
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
  "material_write_groups": [
    {
      "prefix": "",
      "members": [
        "arcanum/transmutations/context-builder/SKILL.md",
        "arcanum/transmutations/context-builder/README.md",
        "arcanum/transmutations/context-builder/templates/runtime-handoff-index.json",
        "arcanum/transmutations/context-builder/templates/codex-goal-handoff-index.json",
        "arcanum/spells/invoke/schemas/material-package.schema.json",
        "arcanum/spells/invoke/schemas/material-package-receipt.schema.json",
        "arcanum/spells/invoke/scripts/material_package_validator.py",
        "arcanum/spells/invoke/development/run_material_package_fixtures.py",
        "arcanum/spells/invoke/development/fixtures/material-package-cases.json",
        "arcanum/spells/invoke/refresh.md",
        "arcanum/spells/invoke/README.md",
        "arcanum/arcana/task-session/schemas/mutation-admission-request.schema.json",
        "arcanum/arcana/task-session/schemas/mutation-admission-receipt.schema.json",
        "arcanum/arcana/task-session/scripts/verify-mutation-readiness.py",
        "arcanum/arcana/task-session/scripts/task-session-governance-runner.py",
        "arcanum/arcana/task-session/development/validate-mutation-admission.py",
        "arcanum/arcana/task-session/development/fixtures/mutation-admission-cases.json",
        "arcanum/arcana/task-session/development/test_plan_once_admission.py",
        "arcanum/arcana/task-session/development/validate-governance-runner.py",
        "arcanum/arcana/task-session/development/test_plan_once_governance.py",
        "arcanum/arcana/task-session/SKILL.md",
        "arcanum/arcana/task-session/README.md",
        ".agents/skills/context-builder/SKILL.md",
        ".agents/skills/context-builder/README.md",
        ".agents/skills/context-builder/templates/runtime-handoff-index.json",
        ".agents/skills/context-builder/templates/codex-goal-handoff-index.json",
        ".claude/skills/context-builder/SKILL.md",
        ".claude/skills/context-builder/README.md",
        ".claude/skills/context-builder/templates/runtime-handoff-index.json",
        ".claude/skills/context-builder/templates/codex-goal-handoff-index.json",
        ".claude/skills/context-builder/templates/runtime-handoff-pack.md",
        ".claude/skills/context-builder/templates/codex-goal-handoff-pack.md",
        ".agents/skills/invoke/README.md",
        ".agents/skills/invoke/SKILL.md",
        ".agents/skills/invoke/refresh.md",
        ".agents/skills/invoke/schemas/material-package.schema.json",
        ".agents/skills/invoke/schemas/material-package-receipt.schema.json",
        ".agents/skills/invoke/scripts/material_package_validator.py",
        ".claude/skills/invoke/README.md",
        ".claude/skills/invoke/SKILL.md",
        ".claude/skills/invoke/refresh.md",
        ".claude/skills/invoke/schemas/material-package.schema.json",
        ".claude/skills/invoke/schemas/material-package-receipt.schema.json",
        ".claude/skills/invoke/scripts/material_package_validator.py",
        ".agents/skills/task-session/README.md",
        ".agents/skills/task-session/SKILL.md",
        ".agents/skills/task-session/schemas/mutation-admission-request.schema.json",
        ".agents/skills/task-session/schemas/mutation-admission-receipt.schema.json",
        ".agents/skills/task-session/scripts/verify-mutation-readiness.py",
        ".agents/skills/task-session/scripts/task-session-governance-runner.py",
        ".claude/skills/task-session/README.md",
        ".claude/skills/task-session/SKILL.md",
        ".claude/skills/task-session/schemas/mutation-admission-request.schema.json",
        ".claude/skills/task-session/schemas/mutation-admission-receipt.schema.json",
        ".claude/skills/task-session/scripts/verify-mutation-readiness.py",
        ".claude/skills/task-session/scripts/task-session-governance-runner.py"
      ]
    }
  ],
  "execution_output_groups": [
    {
      "prefix": "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/SWU-RWO-CCP-002",
      "members": [
        "executor.json"
      ]
    }
  ],
  "allowed_writes_rule": "Task Session admission materialWrites equals the exact material set; executionOutputs is exactly the separately route-authorized E receipt; allowedWrites is their exact union; pre-execution, validation, and remaining lifecycle paths are excluded",
  "legacy_required_control_artifacts": [
    {
      "path": "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/bootstrap/CCP-BOOTSTRAP-R2/PUBLIC-TASK-RWO-CCP-002.md",
      "role": "task-contract",
      "authorityClass": "public"
    },
    {
      "path": "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/bootstrap/CCP-BOOTSTRAP-R2/PUBLIC-WORK-PACK.md",
      "role": "work-pack",
      "authorityClass": "public"
    },
    {
      "path": "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/bootstrap/CCP-BOOTSTRAP-R2/PUBLIC-CONTEXT-PACK-INDEX.json",
      "role": "context-pack",
      "authorityClass": "public"
    }
  ],
  "legacy_source_role_paths": [
    "arcanum/transmutations/context-builder/SKILL.md",
    "arcanum/transmutations/context-builder/README.md",
    "arcanum/transmutations/context-builder/templates/runtime-handoff-index.json",
    "arcanum/transmutations/context-builder/templates/codex-goal-handoff-index.json",
    "arcanum/spells/invoke/schemas/material-package.schema.json",
    "arcanum/spells/invoke/schemas/material-package-receipt.schema.json",
    "arcanum/spells/invoke/scripts/material_package_validator.py",
    "arcanum/spells/invoke/development/run_material_package_fixtures.py",
    "arcanum/spells/invoke/development/fixtures/material-package-cases.json",
    "arcanum/spells/invoke/refresh.md",
    "arcanum/spells/invoke/README.md",
    "arcanum/arcana/task-session/schemas/mutation-admission-request.schema.json",
    "arcanum/arcana/task-session/schemas/mutation-admission-receipt.schema.json",
    "arcanum/arcana/task-session/scripts/verify-mutation-readiness.py",
    "arcanum/arcana/task-session/scripts/task-session-governance-runner.py",
    "arcanum/arcana/task-session/development/validate-mutation-admission.py",
    "arcanum/arcana/task-session/development/fixtures/mutation-admission-cases.json",
    "arcanum/arcana/task-session/development/test_plan_once_admission.py",
    "arcanum/arcana/task-session/development/validate-governance-runner.py",
    "arcanum/arcana/task-session/development/test_plan_once_governance.py",
    "arcanum/arcana/task-session/SKILL.md",
    "arcanum/arcana/task-session/README.md",
    "arcanum/transmutations/context-builder/templates/runtime-handoff-pack.md",
    "arcanum/transmutations/context-builder/templates/codex-goal-handoff-pack.md",
    "arcanum/tools/sync-generated-skill-package.sh",
    "arcanum/tools/bootstrap_arcanum.sh",
    "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/bootstrap/CCP-BOOTSTRAP-R2/HELPER-REQUEST.json",
    "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/control/bootstrap/CCP-BOOTSTRAP-R2/PUBLIC-SOURCE-MANIFEST.json"
  ],
  "legacy_material_rule": "material-package 1.0.0 source_artifacts and request 1.2.0 controlArtifacts are the exact same thirty-one-entry path/digest/size/authority set: one public task, one public work-pack, the machine-readable PUBLIC-CONTEXT-PACK-INDEX.json as the unique context-pack, plus role=source for all twenty-six actual public semantic/build inputs, the exact public generic helper request, and the public source manifest; PUBLIC-CONTEXT-PACK.md is human-only and outside the set; staged outputs are never sources; manifest-only indirection, missing semantic source coverage, any private source, or any mismatch rejects",
  "immutable_paths": [
    "ops/development/2026-08-16-rwo-control-content-provenance-successor-r3/candidate-plan-epoch",
    "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/RWO-CODEX-MIGRATION-001",
    ".git",
    ".craft",
    "telemetry",
    "ops/development/2026-08-16-rwo-control-content-provenance-successor/candidate-plan-epoch",
    "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-001"
  ],
  "protected_equal_hash_paths": {
    "arcanum/spells/invoke/scripts/refresh_material_handoff.py": "820500e2c19baf14c32b6eb39f5cfc88cbe210a0f1b76f131e71cfdc4a95db5e",
    ".agents/skills/invoke/scripts/refresh_material_handoff.py": "820500e2c19baf14c32b6eb39f5cfc88cbe210a0f1b76f131e71cfdc4a95db5e",
    ".claude/skills/invoke/scripts/refresh_material_handoff.py": "820500e2c19baf14c32b6eb39f5cfc88cbe210a0f1b76f131e71cfdc4a95db5e",
    ".agents/skills/invoke/scripts/__pycache__/material_package_validator.cpython-312.pyc": "6287c37437a50881f4a5b8e781f009eee9a7219e1b9018bda878a259b315fc99",
    ".agents/skills/invoke/scripts/__pycache__/design_scope_extractor.cpython-312.pyc": "7cbaf13734492579e23ae5bd8dc0c7633e72e9b92d3540fdccba1788d92416ea",
    ".agents/skills/task-session/scripts/__pycache__/fast_execution_entry_guard.cpython-312.pyc": "7b4f292fcf7485043d49506b9bb2facf68dac61c4c95b1c3810faf40e5b7bf66"
  },
  "receipt_topology": {
    "E": "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/SWU-RWO-CCP-002/executor.json",
    "O": "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/SWU-RWO-CCP-002/owner.json",
    "V": "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/SWU-RWO-CCP-002/validation.json",
    "P": "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/SWU-RWO-CCP-002/precloseout.json",
    "C": "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/SWU-RWO-CCP-002/closeout-owner.json",
    "B": "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/SWU-RWO-CCP-002/observation.json",
    "T": "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/SWU-RWO-CCP-002/terminal.json"
  },
  "attempt_contract": {
    "id_policy": "sha256(plan-epoch,swu-id,task-session-request-id,attempt-ordinal=1)",
    "collision_policy": "capsule/terminal/current fifty-six baselines must match exactly",
    "success_teardown": "full suites pass, all protected hashes pass, join E/O/V/P/C/B/T, expose CCP-003",
    "failure_teardown": "restore all fifty-six live pre-attempt bytes atomically, preserve caches and protected files, rerun baseline proof, emit no T"
  },
  "authority_class": "public",
  "publication_class": "public",
  "claim_ceiling": "local contract and generated-runtime parity only; no adapter application or publication authority",
  "task_session_partition_contract": {
    "schema_version": "arcanum.task-session.fast-entry-partition/v1",
    "runner_semantics": "requested writes equal materialWrites; admission executionOutputs is exactly the separately route-authorized E receipt",
    "route_expected_receipt": "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/SWU-RWO-CCP-002/executor.json",
    "route_write_scope": [
      ".agents/skills/context-builder/README.md",
      ".agents/skills/context-builder/SKILL.md",
      ".agents/skills/context-builder/templates/codex-goal-handoff-index.json",
      ".agents/skills/context-builder/templates/runtime-handoff-index.json",
      ".agents/skills/invoke/README.md",
      ".agents/skills/invoke/SKILL.md",
      ".agents/skills/invoke/refresh.md",
      ".agents/skills/invoke/schemas/material-package-receipt.schema.json",
      ".agents/skills/invoke/schemas/material-package.schema.json",
      ".agents/skills/invoke/scripts/material_package_validator.py",
      ".agents/skills/task-session/README.md",
      ".agents/skills/task-session/SKILL.md",
      ".agents/skills/task-session/schemas/mutation-admission-receipt.schema.json",
      ".agents/skills/task-session/schemas/mutation-admission-request.schema.json",
      ".agents/skills/task-session/scripts/task-session-governance-runner.py",
      ".agents/skills/task-session/scripts/verify-mutation-readiness.py",
      ".claude/skills/context-builder/README.md",
      ".claude/skills/context-builder/SKILL.md",
      ".claude/skills/context-builder/templates/codex-goal-handoff-index.json",
      ".claude/skills/context-builder/templates/codex-goal-handoff-pack.md",
      ".claude/skills/context-builder/templates/runtime-handoff-index.json",
      ".claude/skills/context-builder/templates/runtime-handoff-pack.md",
      ".claude/skills/invoke/README.md",
      ".claude/skills/invoke/SKILL.md",
      ".claude/skills/invoke/refresh.md",
      ".claude/skills/invoke/schemas/material-package-receipt.schema.json",
      ".claude/skills/invoke/schemas/material-package.schema.json",
      ".claude/skills/invoke/scripts/material_package_validator.py",
      ".claude/skills/task-session/README.md",
      ".claude/skills/task-session/SKILL.md",
      ".claude/skills/task-session/schemas/mutation-admission-receipt.schema.json",
      ".claude/skills/task-session/schemas/mutation-admission-request.schema.json",
      ".claude/skills/task-session/scripts/task-session-governance-runner.py",
      ".claude/skills/task-session/scripts/verify-mutation-readiness.py",
      "arcanum/arcana/task-session/README.md",
      "arcanum/arcana/task-session/SKILL.md",
      "arcanum/arcana/task-session/development/fixtures/mutation-admission-cases.json",
      "arcanum/arcana/task-session/development/test_plan_once_admission.py",
      "arcanum/arcana/task-session/development/test_plan_once_governance.py",
      "arcanum/arcana/task-session/development/validate-governance-runner.py",
      "arcanum/arcana/task-session/development/validate-mutation-admission.py",
      "arcanum/arcana/task-session/schemas/mutation-admission-receipt.schema.json",
      "arcanum/arcana/task-session/schemas/mutation-admission-request.schema.json",
      "arcanum/arcana/task-session/scripts/task-session-governance-runner.py",
      "arcanum/arcana/task-session/scripts/verify-mutation-readiness.py",
      "arcanum/spells/invoke/README.md",
      "arcanum/spells/invoke/development/fixtures/material-package-cases.json",
      "arcanum/spells/invoke/development/run_material_package_fixtures.py",
      "arcanum/spells/invoke/refresh.md",
      "arcanum/spells/invoke/schemas/material-package-receipt.schema.json",
      "arcanum/spells/invoke/schemas/material-package.schema.json",
      "arcanum/spells/invoke/scripts/material_package_validator.py",
      "arcanum/transmutations/context-builder/README.md",
      "arcanum/transmutations/context-builder/SKILL.md",
      "arcanum/transmutations/context-builder/templates/codex-goal-handoff-index.json",
      "arcanum/transmutations/context-builder/templates/runtime-handoff-index.json",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/SWU-RWO-CCP-002/executor.json"
    ],
    "pre_execution_controls": [
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/SWU-RWO-CCP-002/material-package.json",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/SWU-RWO-CCP-002/material-package-receipt.json",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/SWU-RWO-CCP-002/mutation-admission-request.json",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/SWU-RWO-CCP-002/mutation-admission-receipt.json"
    ],
    "admission_material_writes": [
      "arcanum/transmutations/context-builder/SKILL.md",
      "arcanum/transmutations/context-builder/README.md",
      "arcanum/transmutations/context-builder/templates/runtime-handoff-index.json",
      "arcanum/transmutations/context-builder/templates/codex-goal-handoff-index.json",
      "arcanum/spells/invoke/schemas/material-package.schema.json",
      "arcanum/spells/invoke/schemas/material-package-receipt.schema.json",
      "arcanum/spells/invoke/scripts/material_package_validator.py",
      "arcanum/spells/invoke/development/run_material_package_fixtures.py",
      "arcanum/spells/invoke/development/fixtures/material-package-cases.json",
      "arcanum/spells/invoke/refresh.md",
      "arcanum/spells/invoke/README.md",
      "arcanum/arcana/task-session/schemas/mutation-admission-request.schema.json",
      "arcanum/arcana/task-session/schemas/mutation-admission-receipt.schema.json",
      "arcanum/arcana/task-session/scripts/verify-mutation-readiness.py",
      "arcanum/arcana/task-session/scripts/task-session-governance-runner.py",
      "arcanum/arcana/task-session/development/validate-mutation-admission.py",
      "arcanum/arcana/task-session/development/fixtures/mutation-admission-cases.json",
      "arcanum/arcana/task-session/development/test_plan_once_admission.py",
      "arcanum/arcana/task-session/development/validate-governance-runner.py",
      "arcanum/arcana/task-session/development/test_plan_once_governance.py",
      "arcanum/arcana/task-session/SKILL.md",
      "arcanum/arcana/task-session/README.md",
      ".agents/skills/context-builder/SKILL.md",
      ".agents/skills/context-builder/README.md",
      ".agents/skills/context-builder/templates/runtime-handoff-index.json",
      ".agents/skills/context-builder/templates/codex-goal-handoff-index.json",
      ".claude/skills/context-builder/SKILL.md",
      ".claude/skills/context-builder/README.md",
      ".claude/skills/context-builder/templates/runtime-handoff-index.json",
      ".claude/skills/context-builder/templates/codex-goal-handoff-index.json",
      ".claude/skills/context-builder/templates/runtime-handoff-pack.md",
      ".claude/skills/context-builder/templates/codex-goal-handoff-pack.md",
      ".agents/skills/invoke/README.md",
      ".agents/skills/invoke/SKILL.md",
      ".agents/skills/invoke/refresh.md",
      ".agents/skills/invoke/schemas/material-package.schema.json",
      ".agents/skills/invoke/schemas/material-package-receipt.schema.json",
      ".agents/skills/invoke/scripts/material_package_validator.py",
      ".claude/skills/invoke/README.md",
      ".claude/skills/invoke/SKILL.md",
      ".claude/skills/invoke/refresh.md",
      ".claude/skills/invoke/schemas/material-package.schema.json",
      ".claude/skills/invoke/schemas/material-package-receipt.schema.json",
      ".claude/skills/invoke/scripts/material_package_validator.py",
      ".agents/skills/task-session/README.md",
      ".agents/skills/task-session/SKILL.md",
      ".agents/skills/task-session/schemas/mutation-admission-request.schema.json",
      ".agents/skills/task-session/schemas/mutation-admission-receipt.schema.json",
      ".agents/skills/task-session/scripts/verify-mutation-readiness.py",
      ".agents/skills/task-session/scripts/task-session-governance-runner.py",
      ".claude/skills/task-session/README.md",
      ".claude/skills/task-session/SKILL.md",
      ".claude/skills/task-session/schemas/mutation-admission-request.schema.json",
      ".claude/skills/task-session/schemas/mutation-admission-receipt.schema.json",
      ".claude/skills/task-session/scripts/verify-mutation-readiness.py",
      ".claude/skills/task-session/scripts/task-session-governance-runner.py"
    ],
    "admission_execution_outputs": [
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/SWU-RWO-CCP-002/executor.json"
    ],
    "admission_allowed_writes": [
      ".agents/skills/context-builder/README.md",
      ".agents/skills/context-builder/SKILL.md",
      ".agents/skills/context-builder/templates/codex-goal-handoff-index.json",
      ".agents/skills/context-builder/templates/runtime-handoff-index.json",
      ".agents/skills/invoke/README.md",
      ".agents/skills/invoke/SKILL.md",
      ".agents/skills/invoke/refresh.md",
      ".agents/skills/invoke/schemas/material-package-receipt.schema.json",
      ".agents/skills/invoke/schemas/material-package.schema.json",
      ".agents/skills/invoke/scripts/material_package_validator.py",
      ".agents/skills/task-session/README.md",
      ".agents/skills/task-session/SKILL.md",
      ".agents/skills/task-session/schemas/mutation-admission-receipt.schema.json",
      ".agents/skills/task-session/schemas/mutation-admission-request.schema.json",
      ".agents/skills/task-session/scripts/task-session-governance-runner.py",
      ".agents/skills/task-session/scripts/verify-mutation-readiness.py",
      ".claude/skills/context-builder/README.md",
      ".claude/skills/context-builder/SKILL.md",
      ".claude/skills/context-builder/templates/codex-goal-handoff-index.json",
      ".claude/skills/context-builder/templates/codex-goal-handoff-pack.md",
      ".claude/skills/context-builder/templates/runtime-handoff-index.json",
      ".claude/skills/context-builder/templates/runtime-handoff-pack.md",
      ".claude/skills/invoke/README.md",
      ".claude/skills/invoke/SKILL.md",
      ".claude/skills/invoke/refresh.md",
      ".claude/skills/invoke/schemas/material-package-receipt.schema.json",
      ".claude/skills/invoke/schemas/material-package.schema.json",
      ".claude/skills/invoke/scripts/material_package_validator.py",
      ".claude/skills/task-session/README.md",
      ".claude/skills/task-session/SKILL.md",
      ".claude/skills/task-session/schemas/mutation-admission-receipt.schema.json",
      ".claude/skills/task-session/schemas/mutation-admission-request.schema.json",
      ".claude/skills/task-session/scripts/task-session-governance-runner.py",
      ".claude/skills/task-session/scripts/verify-mutation-readiness.py",
      "arcanum/arcana/task-session/README.md",
      "arcanum/arcana/task-session/SKILL.md",
      "arcanum/arcana/task-session/development/fixtures/mutation-admission-cases.json",
      "arcanum/arcana/task-session/development/test_plan_once_admission.py",
      "arcanum/arcana/task-session/development/test_plan_once_governance.py",
      "arcanum/arcana/task-session/development/validate-governance-runner.py",
      "arcanum/arcana/task-session/development/validate-mutation-admission.py",
      "arcanum/arcana/task-session/schemas/mutation-admission-receipt.schema.json",
      "arcanum/arcana/task-session/schemas/mutation-admission-request.schema.json",
      "arcanum/arcana/task-session/scripts/task-session-governance-runner.py",
      "arcanum/arcana/task-session/scripts/verify-mutation-readiness.py",
      "arcanum/spells/invoke/README.md",
      "arcanum/spells/invoke/development/fixtures/material-package-cases.json",
      "arcanum/spells/invoke/development/run_material_package_fixtures.py",
      "arcanum/spells/invoke/refresh.md",
      "arcanum/spells/invoke/schemas/material-package-receipt.schema.json",
      "arcanum/spells/invoke/schemas/material-package.schema.json",
      "arcanum/spells/invoke/scripts/material_package_validator.py",
      "arcanum/transmutations/context-builder/README.md",
      "arcanum/transmutations/context-builder/SKILL.md",
      "arcanum/transmutations/context-builder/templates/codex-goal-handoff-index.json",
      "arcanum/transmutations/context-builder/templates/runtime-handoff-index.json",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/SWU-RWO-CCP-002/executor.json"
    ],
    "target_baseline_paths": [
      "arcanum/transmutations/context-builder/SKILL.md",
      "arcanum/transmutations/context-builder/README.md",
      "arcanum/transmutations/context-builder/templates/runtime-handoff-index.json",
      "arcanum/transmutations/context-builder/templates/codex-goal-handoff-index.json",
      "arcanum/spells/invoke/schemas/material-package.schema.json",
      "arcanum/spells/invoke/schemas/material-package-receipt.schema.json",
      "arcanum/spells/invoke/scripts/material_package_validator.py",
      "arcanum/spells/invoke/development/run_material_package_fixtures.py",
      "arcanum/spells/invoke/development/fixtures/material-package-cases.json",
      "arcanum/spells/invoke/refresh.md",
      "arcanum/spells/invoke/README.md",
      "arcanum/arcana/task-session/schemas/mutation-admission-request.schema.json",
      "arcanum/arcana/task-session/schemas/mutation-admission-receipt.schema.json",
      "arcanum/arcana/task-session/scripts/verify-mutation-readiness.py",
      "arcanum/arcana/task-session/scripts/task-session-governance-runner.py",
      "arcanum/arcana/task-session/development/validate-mutation-admission.py",
      "arcanum/arcana/task-session/development/fixtures/mutation-admission-cases.json",
      "arcanum/arcana/task-session/development/test_plan_once_admission.py",
      "arcanum/arcana/task-session/development/validate-governance-runner.py",
      "arcanum/arcana/task-session/development/test_plan_once_governance.py",
      "arcanum/arcana/task-session/SKILL.md",
      "arcanum/arcana/task-session/README.md",
      ".agents/skills/context-builder/SKILL.md",
      ".agents/skills/context-builder/README.md",
      ".agents/skills/context-builder/templates/runtime-handoff-index.json",
      ".agents/skills/context-builder/templates/codex-goal-handoff-index.json",
      ".claude/skills/context-builder/SKILL.md",
      ".claude/skills/context-builder/README.md",
      ".claude/skills/context-builder/templates/runtime-handoff-index.json",
      ".claude/skills/context-builder/templates/codex-goal-handoff-index.json",
      ".claude/skills/context-builder/templates/runtime-handoff-pack.md",
      ".claude/skills/context-builder/templates/codex-goal-handoff-pack.md",
      ".agents/skills/invoke/README.md",
      ".agents/skills/invoke/SKILL.md",
      ".agents/skills/invoke/refresh.md",
      ".agents/skills/invoke/schemas/material-package.schema.json",
      ".agents/skills/invoke/schemas/material-package-receipt.schema.json",
      ".agents/skills/invoke/scripts/material_package_validator.py",
      ".claude/skills/invoke/README.md",
      ".claude/skills/invoke/SKILL.md",
      ".claude/skills/invoke/refresh.md",
      ".claude/skills/invoke/schemas/material-package.schema.json",
      ".claude/skills/invoke/schemas/material-package-receipt.schema.json",
      ".claude/skills/invoke/scripts/material_package_validator.py",
      ".agents/skills/task-session/README.md",
      ".agents/skills/task-session/SKILL.md",
      ".agents/skills/task-session/schemas/mutation-admission-request.schema.json",
      ".agents/skills/task-session/schemas/mutation-admission-receipt.schema.json",
      ".agents/skills/task-session/scripts/verify-mutation-readiness.py",
      ".agents/skills/task-session/scripts/task-session-governance-runner.py",
      ".claude/skills/task-session/README.md",
      ".claude/skills/task-session/SKILL.md",
      ".claude/skills/task-session/schemas/mutation-admission-request.schema.json",
      ".claude/skills/task-session/schemas/mutation-admission-receipt.schema.json",
      ".claude/skills/task-session/scripts/verify-mutation-readiness.py",
      ".claude/skills/task-session/scripts/task-session-governance-runner.py"
    ],
    "validation_outputs": [
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/SWU-RWO-CCP-002/validation.json"
    ],
    "lifecycle_outputs": [
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/SWU-RWO-CCP-002/owner.json",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/SWU-RWO-CCP-002/precloseout.json",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/SWU-RWO-CCP-002/closeout-owner.json",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/SWU-RWO-CCP-002/observation.json",
      "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/SWU-RWO-CCP-002/terminal.json"
    ]
  }
}
```

## Task Session Fast-Entry Partition

The route expected receipt is `projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/SWU-RWO-CCP-002/executor.json` and is independently authorized by the Execution Entry route. Pre-execution controls are built before executor mutation. The mutation admission uses only the exact partition above. `V` is validation evidence; `O/P/C/B/T` remain lifecycle outputs. None of those paths is laundered into the executor mutation set. The failed R2 CCP-002 admission is immutable diagnostic evidence and cannot authorize this R3 successor.


## Current Generated Baselines And Inherited Drift

Every current generated material path must be frozen by SHA-256/size/mode in the capsule target inventory and rehashed at admission. The known current digests are:

- Context Builder repo-codex: `SKILL.md` `ee507a7d2104d0d2186cab49c219bad271cd9d09a1df0543124cb03963d69568`; README/indexes equal their canonical baselines.
- Context Builder Claude: `SKILL.md` `49538409714163287361721b54375b30756bf19091c717d3ca4697f28318fd82`; README/indexes equal canonical; inherited formatter drift is `runtime-handoff-pack.md` `cfc3edb009a76a007e01f89c3c666e9bf0cc96f846e6168add9569f9463e5fbe` and `codex-goal-handoff-pack.md` `428d941820be493983fa28604a0cd369b26d91ca40378dd3aeda9c988031107d`.
- Invoke repo-codex/Claude README, refresh, schemas, and validator equal canonical baselines. Generated SKILL digests are repo-codex `f287d213a60cd1e5ce40f97b603f723ce08ce5eb584a68d205b754ae6b866259` and Claude `87ae30073dbdad9442afa6819d9f433c760f0bc53d951fb2964c4add3c2ad50c`.
- Task Session repo-codex/Claude README, schemas, verifier, and governance runner equal canonical baselines. Generated SKILL digests are repo-codex `558c40e0f6e7cce5ae02cd32307c35d8a6bf89d592008474827d2d7ac1d1ff05` and Claude `b14e1b65094635d2f08b04fd60d2f41f0af4e95bf2f8873b7d831d75d66a9cb6`.

The capsule manifest supplies exact sizes/modes and new output hashes. Three Claude Context Builder changes are classified `pre-existing-generated-parity-drift`, not caused solely by Option A. The three live cache files are not material writes; live preview may report them as deletion residue, but application copies declared file outputs directly and leaves cache bytes untouched.

## Required Contract Changes

### Context Builder

Add `sha256`, `size_bytes`, and `authority_class` to every selected source in both runtime and Codex Goal index templates. Require nonempty obligations, exact normalized identity, and public authority for sources selected to feed public material. Update only the four declared canonical files.

### Invoke 1.1

Add nonempty `control_artifacts` with role/path/digest/size/authority, preserve `source_artifacts` as content provenance, require normalized path disjointness, unique required control roles, no `source` role in new controls, exact read checks, public-source policy, and separate receipt results/reasons. Preserve legacy 1.0 fail-closed semantics and reject cross-version/field mixing. Add positive private-control/public-source and all-public cases plus all named negative cases.

### Task Session 1.3

Add `sourceArtifacts` and independently compare request controls/sources to package controls/sources. Compare sources with strict Context Builder `selected_sources` by path/digest/size/authority and obligation coverage. Retain unique required controls, reject source role in new controls, reject public/private source escape and cross-version pairs, preserve exact package/receipt/plan/baseline/write/dependency/owner/publication checks, and retain legacy 1.2. Update both active consumers (`verify-mutation-readiness.py`, `task-session-governance-runner.py`) and all four focused validation/test files plus fixtures/docs.

## Exact Validation Contracts

After all fifty-six declared files have been installed and before terminal emission:

1. Before apply, validate that legacy package sources/request controls contain the exact thirty-one-entry set, every entry is exact and public, every actual helper input is present, staged outputs are absent, and manifest-only indirection/incomplete semantic coverage rejects. After apply, `python3 arcanum/spells/invoke/development/run_material_package_fixtures.py` exits 0; legacy and split positives/negatives plus generated parity pass.
2. `python3 arcanum/arcana/task-session/development/validate-mutation-admission.py` — exit 0; legacy/split and cross-version cases pass.
3. `python3 arcanum/arcana/task-session/development/test_plan_once_admission.py` — exit 0.
4. `python3 arcanum/arcana/task-session/development/validate-governance-runner.py --family prepare` — exit 0.
5. Repeat the governance validator for `executor-join`, `reconcile`, and `commit-resume` — each exit 0.
6. `python3 arcanum/arcana/task-session/development/test_plan_once_governance.py` — exit 0.
7. Parse both canonical Context Builder indexes with `python3 -m json.tool`; each exit 0, and exact field/obligation checks pass.
8. Run all three live selective-sync commands without `--apply`; output may contain only the three known cache deletion residues and no declared file difference.
9. Rehash all fifty-six installed files against capsule outputs, all three protected refresh scripts, and all three live cache files; exact match required.
10. Scoped whitespace check over all fifty-six material files; exit 0/no error.

All commands use cwd `.`, fixed `LC_ALL=C`, bytecode outside the repository, captured executable path/version/hash, bounded output, and first-failure preservation. Full fixture/parity success is part of CCP-002; it is not deferred.

## Admission, Apply, Rollback, And Handoff

- Treat the exact passing CCP-001 terminal as an immutable external predecessor, then select CCP-002 only after fresh exact owner acceptance of this candidate.
- Build a legacy `1.0.0` package from the exact thirty-one public capsule/control/source artifacts, with the JSON index as `context-pack` and the Markdown companion excluded. Its changes/output refs point only to the fifty-six capsule-staged files.
- Build a legacy `1.2.0` request whose control set exactly equals package sources, with unique required roles plus every actual semantic/build input as role `source`; bind current baselines, package/receipt/schema, validation surface, and exact write partitions.
- Task Session alone consumes one single-use admission. No new split contract is trusted until the coupled transaction passes.
- Apply all fifty-six material bytes as one transaction. On any write/validation/owner/closeout failure, restore every pre-attempt file, prove exact hashes, preserve evidence, emit no T or successor.
- On success, E/O/V/P/C/B/T binds package/admission IDs, capsule manifest, all installed hashes, inherited-drift classification, protected-file/cache equality, and validation results; hand only T to CCP-003.

## First Stop

Private successor artifact in legacy sources; stale capsule/terminal/baseline; incomplete or cross-version package; partial write; new preview difference; live cache or protected refresh change; any regression failure; rollback failure; undeclared write; Git/network/model/App Server/credential/publication/promotion/deploy/release effect.

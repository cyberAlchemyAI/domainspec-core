# TASK-RWO-CCP-001 — Public-Safe Bootstrap Capsule

```json
{
  "schema_version": "rwo.task-contract/v2",
  "task_id": "TASK-RWO-CCP-001",
  "swu_id": "SWU-RWO-CCP-001",
  "primary_owner": "task-session-bootstrap-owner",
  "dependencies": [],
  "canonical_successors": ["SWU-RWO-CCP-002"],
  "objective": "Create and validate a public-safe legacy bootstrap capsule without canonical, generated, Git, or external mutation.",
  "command": {
    "argv": ["task-session", "execute", "--work-pack", "WP-RWO-CONTROL-CONTENT-PROVENANCE-001", "--swu", "SWU-RWO-CCP-001", "--task", "ops/development/2026-08-16-rwo-control-content-provenance-successor/candidate-plan-epoch/work-pack/tasks/TASK-RWO-CCP-001.md"],
    "cwd": ".",
    "expected_exit": 0,
    "timeout_seconds": 3600,
    "environment": {"inherit_allowlist": ["PATH"], "fixed": {"LC_ALL": "C", "PYTHONDONTWRITEBYTECODE": "1"}, "forbidden": ["OPENAI_API_KEY", "ANTHROPIC_API_KEY"]},
    "runtime_identity": {"kind": "host-native-capability", "name": "task-session", "binding_policy": "selected-unit-exact-package"},
    "risk": {"class": "repository-local-reversible", "external_effect": false, "destructive": false, "network": false, "model_turn": false, "credentials": false}
  },
  "execution_mode": "routed-mutation",
  "write_profile": "execution-output-only",
  "material_writes": [],
  "execution_output_groups": [
    {
      "prefix": "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-001/SWU-RWO-CCP-001",
      "members": ["context-pack.md", "context-pack-index.json", "mutation-admission-request.json", "mutation-admission-receipt.json", "executor.json", "owner.json", "validation.json", "precloseout.json", "closeout-owner.json", "observation.json", "terminal.json"]
    },
    {
      "prefix": "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-001/control/bootstrap/CCP-BOOTSTRAP-R1",
      "members": ["PUBLIC-WORK-PACK.md", "PUBLIC-TASK-RWO-CCP-002.md", "PUBLIC-CONTEXT-PACK.md", "PUBLIC-CONTEXT-PACK-INDEX.json", "PUBLIC-SOURCE-MANIFEST.json", "HELPER-REQUEST.json", "HELPER-RECEIPT.json", "NO-PRIVATE-INPUT-RECEIPT.json", "DISCLOSURE-REVIEW-RECEIPT.json", "CAPSULE-MANIFEST.json", "TARGET-INVENTORY.json"]
    },
    {
      "prefix": "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-001/control/bootstrap/CCP-BOOTSTRAP-R1/staged",
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
  "allowed_writes_rule": "expand each exact prefix/member pair; because material_writes is empty, allowed_writes equals the exact execution-output expansion",
  "immutable_paths": ["arcanum", ".agents/skills", ".claude/skills", ".git", ".craft", "telemetry", "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/RWO-CODEX-MIGRATION-001/control/material/CX003R-R2"],
  "receipt_topology": {
    "E": "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-001/SWU-RWO-CCP-001/executor.json",
    "O": "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-001/SWU-RWO-CCP-001/owner.json",
    "V": "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-001/SWU-RWO-CCP-001/validation.json",
    "P": "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-001/SWU-RWO-CCP-001/precloseout.json",
    "C": "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-001/SWU-RWO-CCP-001/closeout-owner.json",
    "B": "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-001/SWU-RWO-CCP-001/observation.json",
    "T": "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-001/SWU-RWO-CCP-001/terminal.json"
  },
  "attempt_contract": {"id_policy": "sha256(plan-epoch,swu-id,task-session-request-id,attempt-ordinal=1)", "collision_policy": "all outputs absent; same-id same-input resume only before helper spawn", "success_teardown": "join helper and E/O/V/P/C/B/T then expose CCP-002", "failure_teardown": "preserve diagnostics, emit no T, expose no successor"},
  "execution_owner_recommendation": "task-session-with-one-protected-native-helper",
  "authority_class": "private",
  "publication_class": "internal",
  "claim_ceiling": "private run evidence and staged public-classified candidate bytes only"
}
```

## Inputs And Protected Context

Task Session may read this private task, the accepted successor candidate, exact selection/admission evidence, and current public Arcanum baselines. The bounded helper must receive only a generic public contract-repair objective, the twenty-two exact public canonical mutation baselines, two unchanged Context Builder pack templates, and the two exact public generation tools listed below. It must not receive or read:

- this successor Work Pack or any private task/context;
- `DECISION.md`, Option-A design/review, or selection receipt;
- the old CX003 finding/task/Work Pack/context;
- `control/material/CX003R-R2` or any old staged adapter byte;
- `.craft`, Inventory, telemetry, Git state, credentials, network, model, or live App Server state.

The helper is one bounded native helper owned and joined by Task Session. Its write scope is exactly the bootstrap capsule paths below. Any undeclared read/write, context exposure, collision, or missing join receipt blocks.

## Exact Public Input Baselines

| Path | SHA-256 | Size | Mode |
| --- | --- | ---: | --- |
| `arcanum/transmutations/context-builder/SKILL.md` | `d37a7c938f8e190d5c8c4f9bbb1796d8122346a90144ebfeb64cd77ee1c1c1b4` | 6124 | 0644 |
| `arcanum/transmutations/context-builder/README.md` | `39968ff5bd317126663df69f1add94a2d1cbda0d5a25173376ec257763e6e460` | 3776 | 0644 |
| `arcanum/transmutations/context-builder/templates/runtime-handoff-index.json` | `03be2b2c2e933c9235b8eaa5c4522ef92577730dfe6e1bde1f60e63b1b392dd3` | 1533 | 0644 |
| `arcanum/transmutations/context-builder/templates/codex-goal-handoff-index.json` | `930c3d5822d88fd266d12284691bb0855ba42356957515197653eaf65601888f` | 1536 | 0644 |
| `arcanum/spells/invoke/schemas/material-package.schema.json` | `63230c9459b179a91add893a33036fcc2fec40d1916ce199d9af961bd1d232d1` | 9231 | 0644 |
| `arcanum/spells/invoke/schemas/material-package-receipt.schema.json` | `89b842ac515c03f7b12b04ab3bfdd2e9d473005b5c863eae237bc2f5ee980b66` | 4078 | 0644 |
| `arcanum/spells/invoke/scripts/material_package_validator.py` | `04c98e3ebd7a9d4a215bba6fa9a8584537bf1acdc20e16e5f41519618cad1b36` | 17147 | 0644 |
| `arcanum/spells/invoke/development/run_material_package_fixtures.py` | `54328c06ce0a0e0e9654d1590c35280e81a4816c964fa4944a71cb9849c3f8db` | 14849 | 0755 |
| `arcanum/spells/invoke/development/fixtures/material-package-cases.json` | `4b3d164c353d70ce51e42f5145b2bc227dbd8f2275742e103e64c8a7c0e93dc5` | 3098 | 0644 |
| `arcanum/spells/invoke/refresh.md` | `1fef6b4149210cb8b78a40c7dde1925bf35a676d766aa896955c6a53c4699938` | 16393 | 0644 |
| `arcanum/spells/invoke/README.md` | `f32a536358a2c7826d81dcc1305dac6a3b096f18d5f866ef27995995c051659e` | 30979 | 0644 |
| `arcanum/arcana/task-session/schemas/mutation-admission-request.schema.json` | `e9017a5efa7a00870ffbe6db1f3671f23700d9a8390dba6058a14ba2fc1379a4` | 7653 | 0644 |
| `arcanum/arcana/task-session/schemas/mutation-admission-receipt.schema.json` | `1eb07937cf40e5487af790f65be6b6be844f705e091d63bc4079d4fcc67ecfb6` | 7987 | 0644 |
| `arcanum/arcana/task-session/scripts/verify-mutation-readiness.py` | `ed23868da2b833600983e9f8c691dba83806b41740e5380405a574029a4684a2` | 29358 | 0644 |
| `arcanum/arcana/task-session/scripts/task-session-governance-runner.py` | `fdaf210967aa2be5f5c94c32c7be22344ff23737d6213b31826ba9ba0d24fa1c` | 94447 | 0644 |
| `arcanum/arcana/task-session/development/validate-mutation-admission.py` | `ee534b7a7b88637668585f1d70561fbe58166b8e05a04dd0301fad113874742f` | 22497 | 0644 |
| `arcanum/arcana/task-session/development/fixtures/mutation-admission-cases.json` | `4583b9814276837a804676f98894b43798f66877204bd8780c0c71cb6043634f` | 4765 | 0644 |
| `arcanum/arcana/task-session/development/test_plan_once_admission.py` | `cd5ecc7dfa3fd25b46a59cef4a6aee2afbe20afc422c4c6bfc5e1a3b91658d18` | 18062 | 0644 |
| `arcanum/arcana/task-session/development/validate-governance-runner.py` | `b34406298f57f8d89be7ff5c7ff30b6b88db8e76fa6791888c99622a363eeea4` | 79713 | 0644 |
| `arcanum/arcana/task-session/development/test_plan_once_governance.py` | `71bc3bc2dad1476f8be77bc9d391c02665ef43316ee13fd55272cad3b4930f4f` | 27147 | 0644 |
| `arcanum/arcana/task-session/SKILL.md` | `46df13e7422161ce35111677e7c21c8a298146af978fc975a056b1c6b85eb407` | 43522 | 0644 |
| `arcanum/arcana/task-session/README.md` | `ebb9e01a1ce3ce4097687d8a7438455f32788767b310d1fc1141860d529d1938` | 19805 | 0644 |
| `arcanum/transmutations/context-builder/templates/runtime-handoff-pack.md` | `4b6befbb4c8edd69ec400ba0aac23d39b90d41b2d24d303f18c20816fc1adbe9` | 1569 | 0644 |
| `arcanum/transmutations/context-builder/templates/codex-goal-handoff-pack.md` | `75731d256c78042f0db25a31de02a93ad13a7896bfba8b3bd7565cf0a9d7622e` | 1576 | 0644 |
| `arcanum/tools/sync-generated-skill-package.sh` | `bdfc1b8c12a5b18cdfd139979ee88e18c46b9885e58eff71a645b00e4db997c4` | 8954 | 0755 |
| `arcanum/tools/bootstrap_arcanum.sh` | `fb5da9bf846d6b7607f826844f7f0b6f2daa28e9f7f83b126293ab810269bd0c` | 76032 | 0755 |

## Exact Execution Outputs

Run-control outputs:

- `projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-001/SWU-RWO-CCP-001/context-pack.md`
- `projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-001/SWU-RWO-CCP-001/context-pack-index.json`
- `projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-001/SWU-RWO-CCP-001/mutation-admission-request.json`
- `projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-001/SWU-RWO-CCP-001/mutation-admission-receipt.json`
- the seven `executor.json`, `owner.json`, `validation.json`, `precloseout.json`, `closeout-owner.json`, `observation.json`, and `terminal.json` files in that same SWU directory.

Capsule-control outputs under `.../implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-001/control/bootstrap/CCP-BOOTSTRAP-R1/`:

- `PUBLIC-WORK-PACK.md`
- `PUBLIC-TASK-RWO-CCP-002.md`
- `PUBLIC-CONTEXT-PACK.md`
- `PUBLIC-CONTEXT-PACK-INDEX.json`
- `PUBLIC-SOURCE-MANIFEST.json`
- `HELPER-REQUEST.json`
- `HELPER-RECEIPT.json`
- `NO-PRIVATE-INPUT-RECEIPT.json`
- `DISCLOSURE-REVIEW-RECEIPT.json`
- `CAPSULE-MANIFEST.json`
- `TARGET-INVENTORY.json`

Capsule staged outputs are the twenty-two public canonical input paths above plus the thirty-four exact generated files listed below, each with the prefix `.../control/bootstrap/CCP-BOOTSTRAP-R1/staged/`. Generate the native packages only in one fresh isolated temporary Git root, use selective sync there with `--apply`, and copy only these declared file bytes into capsule staging. No live generated package is an apply target in CCP-001.

Generated Context Builder files:

- `.agents/skills/context-builder/SKILL.md`
- `.agents/skills/context-builder/README.md`
- `.agents/skills/context-builder/templates/runtime-handoff-index.json`
- `.agents/skills/context-builder/templates/codex-goal-handoff-index.json`
- `.claude/skills/context-builder/SKILL.md`
- `.claude/skills/context-builder/README.md`
- `.claude/skills/context-builder/templates/runtime-handoff-index.json`
- `.claude/skills/context-builder/templates/codex-goal-handoff-index.json`
- `.claude/skills/context-builder/templates/runtime-handoff-pack.md`
- `.claude/skills/context-builder/templates/codex-goal-handoff-pack.md`

Generated Invoke files in both `.agents/skills/invoke/` and `.claude/skills/invoke/`:

- `README.md`
- `SKILL.md`
- `refresh.md`
- `schemas/material-package.schema.json`
- `schemas/material-package-receipt.schema.json`
- `scripts/material_package_validator.py`

Generated Task Session files in both `.agents/skills/task-session/` and `.claude/skills/task-session/`:

- `README.md`
- `SKILL.md`
- `schemas/mutation-admission-request.schema.json`
- `schemas/mutation-admission-receipt.schema.json`
- `scripts/verify-mutation-readiness.py`
- `scripts/task-session-governance-runner.py`

No directory glob grants authority; `TARGET-INVENTORY.json` must enumerate all fifty-six normalized canonical/generated paths, output hashes, sizes, modes, operations, and current baselines.

`allowed_writes` is the exact set union of the zero material writes and every run-control, capsule-control, and twenty-two staged output named above. The sets are disjoint.

## Capsule Requirements

- `PUBLIC-WORK-PACK.md`, `PUBLIC-TASK-RWO-CCP-002.md`, and `PUBLIC-CONTEXT-PACK.md` are minimal public-generic controls for the coupled contract repair; no private project name/path/prose is permitted.
- The index uses exact selected-source path/digest/size/authority/obligation fields proposed by the repair.
- The public task declares the twenty-two canonical targets, exact baselines, atomic rollback, validation surface, and no promotion/publication claim.
- The public source manifest maps every staged change to the actual exact public semantic/build inputs. Manifest-only indirection is invalid: all twenty-six public input artifacts and the exact generic helper request must remain individually bindable by path/digest/size/authority.
- The disclosure reviewer is independent of the helper and sees only capsule/public inputs.
- Every capsule path must be absent before the attempt. Collision means stop; no overwrite/resume with different bytes.

## Validation Contracts

1. Parse every capsule JSON and every staged JSON schema/template with `python3 -m json.tool`; expect exit 0.
2. Compile the three staged Python runtime scripts and three staged development scripts with bytecode redirected outside the repository; expect exit 0.
3. Validate that the target inventory has exactly fifty-six unique paths, exact output hashes/sizes/modes, and exact current canonical/generated baselines; expect exit 0.
4. Require `NO-PRIVATE-INPUT-RECEIPT.json` and `DISCLOSURE-REVIEW-RECEIPT.json` verdict `pass`, empty forbidden-read/write sets, and an exact helper input/output manifest.
5. Scan capsule public text and staged public text for every private path/name token supplied by Task Session's protected-context denylist; expected `rg` exit 1.
6. Rehash the canonical twenty-two paths after capsule creation; all must remain equal to the table above.

## Attempt, Rollback, Receipts, Handoff

- Attempt ID: SHA-256 of accepted semantic epoch, SWU ID, fresh Task Session request ID, and ordinal 1.
- Collision policy: every output must be absent; same-ID/same-input resume is allowed only before helper spawn and only with exact receipt match.
- Failure teardown: preserve diagnostics, delete nothing automatically, emit no T, expose no CCP-002 route.
- Success teardown: join helper plus E/O/V/P/C/B/T; T binds exact capsule manifest and canonical no-change proof.
- Handoff: CCP-002 receives only the public capsule trio/source manifest, staged target inventory, and CCP-001 terminal. The private successor controls remain protected governance evidence, never legacy material sources.

## First Stop

Missing exact owner acceptance; private input exposure; canonical/generated write; output collision; incomplete target inventory; disclosure failure; undeclared helper read/write; validation failure; network/model/App Server/credential/Git/publication/promotion/deploy/release effect.

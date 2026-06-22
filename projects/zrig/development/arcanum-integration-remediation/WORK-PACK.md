# Work-Pack: Z-Rig Arcanum Integration Remediation

Status: invoke plan output
Complexity: high, split work-pack
Execution owner: later `task-session` invocations, one SWU at a time
Current execution gate: ready for one selected private SWU, blocked for product-mode assurance

## Work-Pack Intent

Convert the Z-Rig engine/product-mode review into bounded remediation work. This work-pack is private, evidence-linked, and intentionally does not create public Arcanum runtime surfaces.

## Source Anchors

- Integration handoff: `projects/zrig/research/2026-06-17-arcanum-integration-handoff/INVOKE-HANDOFF.md`
- Integration findings: `projects/zrig/research/2026-06-17-arcanum-integration-handoff/findings.md`
- Product-mode findings: `projects/zrig/review/2026-06-17-zrig-engine-product-mode/findings.md`
- Understanding map: `projects/zrig/review/2026-06-17-zrig-engine-product-mode/understanding-map.md`
- Gate source: `projects/zrig/z-rig-turbo-v5.5.3-engine/z-rig-orchestrator/src/zrig/gates.py`
- Pipeline source: `projects/zrig/z-rig-turbo-v5.5.3-engine/z-rig-orchestrator/src/zrig/pipeline.py`

## Work-Pack Gate Status

| Gate | Status | Rationale |
| --- | --- | --- |
| Private artifact planning | pass | Required packet files now exist under `projects/zrig/**`. |
| Engine mutation | conditional | Allowed only through one selected SWU in `EXECUTION-PACK.md`. |
| Product-mode assurance | blocked | F1-F14 remain unresolved until engine checks pass. |
| Public promotion | blocked | Runtime adapter, public sigil/spell, generated package, and registry work are parked. |

## SWU Manifest

| SWU | Findings | Task File | Write Scope | Verification | Status |
| --- | --- | --- | --- | --- | --- |
| SWU-ZRIG-MGMT-001 | artifact obligation | `work-pack/tasks/TASK-ZRIG-CRAFT-STATE.md` | `projects/zrig/.craft/ledger.yml`, `projects/zrig/CRAFT.md` | Ledger/view exist and link evidence. | ready, not selected |
| SWU-ZRIG-F1-GATE-PROOF | F1, F2 boundary | `work-pack/tasks/TASK-ZRIG-F1-GATE-PROOF.md` | `src/zrig/gates.py`, focused tests | Failed W10/W11 payloads fail; generic gate gap closed or fails closed. | selected next |
| SWU-ZRIG-F3-F8-AUDITABILITY | F3, F8 | `work-pack/tasks/TASK-ZRIG-F3-F8-AUDITABILITY.md` | `src/zrig/residue.py`, `src/zrig/pipeline.py`, `pyproject.toml`, tests | Residue schema works; fatality/degraded policy tested; deps declared. | pending |
| SWU-ZRIG-F4-F7-LIVE-BOUNDARIES | F4, F5, F6, F7 | `work-pack/tasks/TASK-ZRIG-LIVE-BOUNDARIES.md` | `src/zrig/live_executor.py`, docs, deploy config/schema tests | Identity spoof fails; deploy/sentinel absent config fails closed or is intentionally threaded; docs expose contracts. | pending |
| SWU-ZRIG-F9-F14-RUNTIME-ACCOUNTING | F9, F10, F11, F12, F13, F14 | `work-pack/tasks/TASK-ZRIG-RUNTIME-ACCOUNTING.md` | dispatch, pipeline, metrics, docs/tests | Shared failover cap, clean-run policy, skipped accounting, `AUTO`, metrics status validated. | pending |
| SWU-ZRIG-READINESS-AUDIT | F1-F14 | `work-pack/tasks/TASK-ZRIG-READINESS-AUDIT.md` | review/update artifacts only | Boundary scan, evidence table, proof/no-proof status. | pending |

## Execution Order

1. W0 Planning State: confirm packet, authority inventory, observability obligations, and optional Craft state.
2. W1 F1 Gate Proof: execute selected SWU `SWU-ZRIG-F1-GATE-PROOF`.
3. W2 Auditability: handle F3/F8 after F1 proof or dependency blocker is explicit.
4. W3 Live Boundaries And Runtime Accounting: handle F4-F7 and F9-F14 in smaller task-session slices.
5. Readiness Audit: decide whether any public-safe extraction can even be proposed.

## Validation Strategy

Planning/artifact checks:

```bash
git diff --check projects/zrig/development/arcanum-integration-remediation projects/zrig/architecture
find projects/zrig/development/arcanum-integration-remediation -type f | sort
```

Parent/submodule checks before any parent publication:

```bash
make doctor
make bump-check
```

Selected F1 SWU check target:

```bash
cd projects/zrig/z-rig-turbo-v5.5.3-engine/z-rig-orchestrator
PYTHONPATH=src python3 -m pytest tests/test_pipeline.py -k "gate or W10 or W11"
```

If that command is blocked by missing dependencies, record the exact blocker under F8 and do not claim F1 completion.

## Parked Work

- Runtime handoff adapter.
- Signal Observer bridge.
- Experiment Harness package.
- Public Z-Rig sigil/spell.
- Public generated runtime package.
- Any public command surface mentioning private Z-Rig product assumptions.

## Completion Criteria

The work-pack is complete only when:

- each F1-F14 row has evidence or an explicit deferred decision;
- selected SWUs have command/check output;
- blocked checks are represented as blockers, not successes;
- public/private boundary scans stay clean;
- final language distinguishes bounded remediation from product-mode assurance.

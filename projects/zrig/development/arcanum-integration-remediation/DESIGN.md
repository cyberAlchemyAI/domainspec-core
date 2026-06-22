# Z-Rig Arcanum Integration Remediation Design

Status: invoke design output
Design mode: discovery from approved research packet
Define baseline: no separate `DEFINE.md`; the source boundary is the reviewed research and handoff material.

## Design Thesis

Use Arcanum as a private lifecycle and governance wrapper around Z-Rig remediation, not as Z-Rig's runtime engine. The architecture should make Z-Rig's product-mode authority surfaces visible, convert findings F1-F14 into bounded remediation SWUs, and preserve public/private boundaries until engine proofs and extraction policy exist.

## View 1: Context

Z-Rig is trying to be a governed multi-agent orchestration engine: mode-aware pipeline, state transitions, seats, gates, failure routing, residue, deploy, and sentinel monitoring. The review found the named surfaces are present, but product-mode assurance collapses when generic gates, stub completion, bridge-reported identity, non-fatal residue failure, and missing deploy/sentinel reachability are treated as proof.

The private remediation architecture therefore has three rings:

| Ring | Owns | Must Not Claim |
| --- | --- | --- |
| Z-Rig engine | Source, tests, CLI, gates, manifests, bridge, deploy/sentinel modules | Product-mode trust before proofs |
| Private parent wrapper | Research, invoke packet, work-pack, Craft state, observed inventories | Runtime authority |
| Public Arcanum | Generic lifecycle patterns only | Z-Rig-specific product behavior |

## View 2: High-Level Structure

```text
projects/zrig/
  review/2026-06-17-zrig-engine-product-mode/
    findings.md
    understanding-map.md
  research/2026-06-17-arcanum-integration-handoff/
    INVOKE-HANDOFF.md
    findings.md
    research.md
  architecture/
    PRODUCT-MODE-AUTHORITY-INVENTORY.md
  development/arcanum-integration-remediation/
    SPEC.md
    DESIGN.md
    IMPLEMENTATION-LAYERING.md
    WORK-PACK.md
    EXECUTION-PACK.md
    OBSERVABILITY-OBLIGATIONS.md
    work-pack/
      shared/
      tasks/
      waves/
  z-rig-turbo-v5.5.3-engine/z-rig-orchestrator/
    src/zrig/
    tests/
```

The package is intentionally private and evidence-linked. It can guide later code changes but does not itself mutate the engine.

## View 3: Low-Level Components

| Component | Role | Anchors |
| --- | --- | --- |
| `SPEC.md` | Requirements and acceptance for the private remediation package. | Handoff lines 43-70 |
| `DESIGN.md` | Architecture views and ownership boundaries. | Understanding map lines 33-87 |
| `IMPLEMENTATION-LAYERING.md` | L0-L3 sequencing from artifact discipline to possible public-safe extraction. | Invoke plan contract |
| `WORK-PACK.md` | Complete SWU manifest and validation strategy. | Findings lines 101-109 |
| `EXECUTION-PACK.md` | One selected next SWU only. | Handoff lines 65-70 |
| `PRODUCT-MODE-AUTHORITY-INVENTORY.md` | Observed architecture/gap inventory. | Handoff lines 111-130 |
| `OBSERVABILITY-OBLIGATIONS.md` | Design-only obligations for future evidence. | Handoff lines 132-142 |
| `work-pack/tasks/*.md` | Executable task cards for task-session or human review. | Work-pack acceptance |
| `work-pack/waves/*.md` | L0-L3 execution sequence. | Plan layering |

## View 4: Workflow Process

1. Read the research and review evidence.
2. Keep all new Z-Rig remediation artifacts private.
3. Maintain the authority inventory as the live map from F1-F14 to engine surfaces.
4. Use the work-pack to select one SWU.
5. Run `task-session` only for the selected SWU.
6. Capture validation output and update the work-pack/Craft state.
7. Repeat SWU selection only after the previous SWU has evidence.

The first selected SWU is `SWU-ZRIG-F1-GATE-PROOF`: make spec-governed waves fail closed when their gates are missing/generic, with focused W10/W11 regression evidence.

## View 5: Decision Flow

```text
Is the work private parent-local?
  no  -> stop; public extraction policy needed
  yes -> Is it runtime adapter/public sigil/spell/Experiment Harness/Signal Observer?
          yes -> park
          no  -> Does it map to F1-F14 or artifact obligation?
                  no  -> refine before planning
                  yes -> Does it select exactly one execution SWU?
                          no  -> keep in planning/backlog
                          yes -> task-session may execute bounded SWU
```

## View 6: Dependency Interface

| Interface | Current State | Required Design Stance |
| --- | --- | --- |
| Gate evaluation | `G4/G5/G8/G8.5/G9/G10/G11` map from waves but lack specific evaluators; generic fallback can pass failed W10/W11 payloads. | Fail closed or implement specific evaluators before product-mode claims. |
| Residue persistence | Pipeline calls `PerWaveResidue(..., entries=...)`; dataclass has different fields; error is non-fatal. | Align schema and decide fatality/degraded-assurance policy. |
| Live bridge identity | W2 parsing trusts output-provided `model_actual` and `family_actual`. | Treat bridge identity as untrusted; derive from assigned seats or signed metadata. |
| Deploy/sentinel | Direct W10/W11 execution requires context keys not supplied by normal pipeline context. | Thread config intentionally or fail closed when absent. |
| Failover | Wave cap is represented through per-seat mutable lists. | Enforce shared wave authority under concurrency. |
| Dependencies | `pyproject.toml` has no dependency list beyond metadata/script. | Declare runtime and test dependencies before verification claims. |

## Design Risks

- A plan that starts with adapter or public promotion would misrepresent authority.
- F1 execution can be blocked by F8 dependency gaps; blocked-run evidence should be captured instead of pretending tests passed.
- Craft management can improve review state, but cannot confer runtime authority.
- Observability obligations are useful only as design until metrics are wired.

## Handoff To Plan

Plan owns decomposition into SWUs, L0-L3 waves, validation commands, and the one-SWU execution pack. The selected first execution route is F1 gate fail-closed remediation.

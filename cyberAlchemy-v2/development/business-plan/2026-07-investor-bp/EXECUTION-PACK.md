---
module: investor-business-plan-package
version: current
status: flag
updatedAt: 2026-07-10
docType: execution-pack
---

# EXECUTION-PACK: Investor Business Plan Package

## Purpose

Wave-by-wave execution choreography for the BP package. The source of truth for
task and SWU contracts remains `WORK-PACK.md`.

## Execution Boundary

- Execute one SWU at a time.
- Keep all outputs private under this directory.
- Do not write to `arcanum/` from this BP execution stream.
- Do not draft investor-facing prose before the evidence registry and financial assumptions exist.
- Do not claim investor-readiness until `claim-audit.md` passes.

## Waves

| Wave | Layer | SWUs | Outcome | Gate |
| --- | --- | --- | --- | --- |
| W0 | L0 | `SWU-BP-001` | Evidence registry and source trace. | Every BP section has evidence, missing witness, and demotion gate. |
| W1 | L1 | `SWU-BP-002`, `SWU-BP-003` | Financial assumptions and operating plan. | Numbers are driver-based assumptions; wedge loop is scoped. |
| W2 | L2 | `SWU-BP-004` | Full BP draft. | Claim <= proof is visible in every section. |
| W3 | L3 | `SWU-BP-005` | Investor memo and deck substrate. | Memo/deck introduce no new claims. |
| W4 | L3 | `SWU-BP-006` | Claim audit and handoff. | Forbidden claims absent or explicitly demoted. |

## Parallelization

Do not parallelize W0. The registry/source trace is the substrate for all later
work.

After W0, financial assumptions and operating plan can be drafted in close
sequence, but not independently: operating capacity, pricing, and cash timing
must agree.

Memo and deck drafting must wait for the BP body. They are compression layers,
not discovery tools.

## First Handoff

Recommended next command route:

```text
task-session SWU-BP-001
```

Context anchors:

- `WORK-PACK.md#swu-execution-handoff`
- `INVOKE-PLAN.md#source-context`
- `.arcanum/inventory/queries/2026-07-09-business-plan-build-research/findings.md`
- `.agents/skills/whisper/presets/business-plan/preset.yaml`

Expected first outputs:

- `diligence-evidence-registry.md`
- `source-trace.md`

Acceptance evidence:

- Each BP section has a source evidence row.
- Each BP section has a missing witness row.
- Each BP section has a falsifier or demotion gate.
- Forbidden claims are listed as forbidden, not supported.

## Stop Conditions

Stop execution and route through decision-gate if:

- the founder wants a specific funding ask in the BP but ask/runway are still undecided;
- the BP must claim unique/first/only status before comparator refresh;
- legal, certification, audit-ready, or compliance language becomes load-bearing;
- private DomainSpec/CAV2 mechanism details are requested for public Arcanum copy;
- a draft tries to treat artifact breadth as traction, market pull, or platform proof.


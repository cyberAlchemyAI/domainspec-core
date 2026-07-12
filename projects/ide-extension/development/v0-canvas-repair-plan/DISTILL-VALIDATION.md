# Distill Validation: V0 Canvas Repair Plan

## Run Profile

- Target context: current V0 canvas findings only.
- Objective/output: mutation-ready split work-pack with one-SWU Task Session
  handoffs.
- Mode: `validate`.
- Budget: one Balancer-led pass and one reconciliation pass.
- Role path: labeled local Proposer/Balancer.
- Verdict: `pass`.

## Role Conversation Trace

### Proposer

Treat the repair as one broad unit: align canvas policy, fix path containment,
add regression tests, and close evidence.

### Balancer

| Objection category | Objection |
| --- | --- |
| Responsibility closure | Policy selection and runtime mutation have different acceptance evidence. |
| Hidden acceptance | Content fetch, not only publish, calls the vulnerable helper. |
| Overbuild | Four layers for two issue classes may become ceremony. |
| Evidence quality | A path helper pass does not prove no external bytes leave the HTTP route. |
| Scope drift | Operations V1 storage and parser concerns could leak into the repair. |

### Reconciliation

- Split policy into SWU-VCR-001 so runtime work implements a settled contract.
- Keep helper/server behavior in SWU-VCR-002 and include both publish and
  content-fetch error mappings.
- Keep adversarial API evidence in SWU-VCR-003 because it has a different write
  scope and proves no-byte leakage.
- Keep SWU-VCR-004 as evidence/status-only closeout required by the existing
  review trace.
- Exclude all Operations V1 source work explicitly.

The four SWUs are not four implementations. They are the minimum independent
policy, mutation, adversarial proof, and closure units required by the plan
contract.

## Smallest Coherent Units

- Policy unit: state the trusted-local canvas exception and distinguish audit
  events from execution receipts.
- Runtime unit: canonicalize one target, prove it is beneath the canonical
  root, then read it through one file handle.
- Evidence unit: adversarial API matrix plus existing canvas compatibility.
- Closure unit: review-linked evidence and status synchronization.

## Recomposition Proof

| Review obligation | SWU evidence |
| --- | --- |
| G1-A approval contradiction | SWU-VCR-001 explicit preview/display exception. |
| G1-R receipt contradiction | SWU-VCR-001 audit-event versus receipt distinction. |
| G1-I route behavior | SWU-VCR-001 confirms no approval field is required under the exception. |
| K1/P1 symlink escape | SWU-VCR-002 canonical admission and SWU-VCR-003 adversarial route tests. |
| K2/P2 read clarification | SWU-VCR-001 narrows prose; SWU-VCR-002 uses one opened handle. |

All retained current-V0 findings have an implementation path and an evidence
path. Removing any of the first three units leaves an obligation unclosed;
removing closeout leaves accepted review state unsynchronized.

## Technique Trace

| Technique | Hook | Outcome |
| --- | --- | --- |
| abstraction-level guard | Review mixed current defects and future operations. | Selected only current V0 repair. |
| recomposition proof | Four SWUs split one repair. | Matrix above covers every retained obligation. |
| evolution profile | Operations V1 is known future work. | Separate design handle; no shared implementation SWU. |
| frame-expiry note | Policy or threat model may change. | Named below. |
| navigable result | Plan must identify one start point. | SWU-VCR-001 is ready. |
| cognitive load check | Medium split plan risks ceremony. | Three task files group four SWUs; no extra task family. |
| boundary-object check | Workspace path crosses into kernel read authority. | Canonical target and bounded error table are explicit. |
| premortem | A lexical-only partial fix may pass normal tests. | External, nested, and retargeted API cases are mandatory. |

Tournament and requisite-variety expansion were skipped: the accepted review
already selected the policy options and only one runtime path helper owns both
affected reads.

## Hidden-Gap And Overbuild Check

- No state migration exists.
- V0 request and response schemas remain unchanged.
- Content fetch uses the same helper and is explicitly covered.
- Platform-perfect hostile race safety is named as residue, not claimed.
- No approval UI, receipt schema, snapshot, parser, blob, operation, or region
  mechanism is introduced.

## Premortem

Likely failure: implementation adds `realpath` to publish but leaves content
fetch returning a server error or external bytes after a link retarget. Guard:
the helper is shared and the content route has a mandatory retarget test.

## Frame Expiry

This plan expires if the operator chooses approval-gated canvas publication,
the project admits hostile/multi-user filesystem writers, or Operations V1
replaces V0 rather than remaining a separate surface. Route those changes back
to design or Decision Gate.

## Navigation Guide

Start at `work-pack/tasks/TASK-CANVAS-POLICY.md`, execute only SWU-VCR-001,
then synchronize its Task Session receipt before selecting SWU-VCR-002.

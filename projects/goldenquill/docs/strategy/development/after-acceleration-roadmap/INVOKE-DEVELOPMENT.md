---
node: after-acceleration-roadmap
docType: invoke-development
status: flag
updatedAt: 2026-06-13
sourceLedger: docs/strategy/development/after-acceleration-roadmap/.craft/ledger.yml
sourceBuildSpec: docs/strategy/development/after-acceleration-roadmap/BUILD-SPEC.md
dispatch: docs/strategy/development/non-strict-coding-node-invoke/NON-STRICT-CODING-INVOKE.dispatch.json
---

# Invoke Development - After-Acceleration Roadmap

## Invoke Result

- Mode: define -> design -> plan
- Phase status: flag
- Target artifact: post-capital roadmap and stage-gate package
- Template family: governance decision packet
- Coding boundary: no runtime work is executed; this artifact sequences future
  business/product themes against evidence triggers
- Next route: Josh stage-gate threshold decision

## Non-Strict-Coding Classification

This node is selected because its current work is roadmap sequencing and
founder judgment, not code: repeatability, sales channels, product hardening,
capital logic expansion, service pilots, new markets, financing, and team build
out.

## Define Artifact

Objective: turn the after-acceleration themes into evidence-triggered stages
instead of an unordered future-work list.

Source contracts:

- `docs/strategy/development/after-acceleration-roadmap/BUILD-SPEC.md`
- `docs/strategy/development/after-acceleration-roadmap/.craft/ledger.yml`
- `docs/golden-quill-task-role-breakdown-handoff.md`

Terms:

- stage gate;
- deployed-node count;
- renewal evidence;
- service pilot;
- non-founder install proof;
- team build-out trigger.

Open decisions and gaps:

- `DEC-AAR-STAGE-GATES`
- `GAP-AAR-SEQUENCING`
- `GAP-AAR-REPEATABILITY`
- `GAP-AAR-SERVICE-PILOTS`

## Design Artifact

Context view: this node defines what happens after startup capital without
pulling future scope into v0.1.

High-level structure: eight post-capital themes mapped to evidence triggers and
sequence lanes.

Low-level components:

- repeatability proof lane;
- sales beyond founder network lane;
- product hardening lane;
- capital logic library expansion lane;
- service-line validation lane;
- new-market lane;
- next-financing lane;
- team build-out lane.

Workflow process: use node-on-desk readiness evidence and Day-60/renewal data
to decide when each theme unlocks.

Decision flow: stage thresholds are Josh-owned. Service-line pilots do not
create an admin lead until controlled pilot evidence exists.

Dependency interface: consumes NOD readiness, WGD repeatability, COF validation
packet, QSP instrumentation, and SBT staffing triggers.

## Plan Artifact

Implementation layering for this authoring pass:

| Layer | Decision Question | Minimum Working Unit | Exit Evidence |
| --- | --- | --- | --- |
| L0 | Can themes be sequenced by evidence? | Stage-gate table. | Each theme has trigger field. |
| L1 | Can repeatability unlock scale? | Non-founder install proof gate. | Repeatability criterion. |
| L2 | Can service pilots avoid premature hiring? | Controlled pilot rule. | Pilot evidence requirement. |
| L3 | Can next financing/team expansion use real data? | Data-room evidence map. | Unit economics inputs. |

Work-pack:

| Task ID | Goal | Write Scope | Validation |
| --- | --- | --- | --- |
| AAR-AUTH-001 | Author stage-gate table. | Roadmap docs. | All eight themes mapped. |
| AAR-AUTH-002 | Define repeatability unlock. | Roadmap docs. | Non-founder install proof required. |
| AAR-AUTH-003 | Define service-pilot gate. | Roadmap docs. | Pilot evidence before admin lead. |
| AAR-AUTH-004 | Map financing/team evidence inputs. | Roadmap docs. | Renewal/support/unit-economics fields. |

SWU handoff:

| SWU ID | Parent Task | Done Criteria | Execution Owner |
| --- | --- | --- | --- |
| SWU-AAR-001 | AAR-AUTH-001 | Stage-gate table is ready for threshold values. | manual |
| SWU-AAR-002 | AAR-AUTH-002 | Repeatability gate references WGD/NOD proof. | local-fallback |
| SWU-AAR-003 | AAR-AUTH-003 | Service-pilot gate prevents premature hiring. | local-fallback |
| SWU-AAR-004 | AAR-AUTH-004 | Data-room evidence inputs are named. | local-fallback |

Residue: threshold values remain operator judgment.


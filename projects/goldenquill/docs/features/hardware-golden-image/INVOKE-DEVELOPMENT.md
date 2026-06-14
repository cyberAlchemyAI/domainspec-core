---
node: hardware-golden-image
docType: invoke-development
status: flag
updatedAt: 2026-06-13
sourceLedger: docs/features/hardware-golden-image/.craft/ledger.yml
sourceBuildSpec: docs/features/hardware-golden-image/BUILD-SPEC.md
dispatch: docs/strategy/development/non-strict-coding-node-invoke/NON-STRICT-CODING-INVOKE.dispatch.json
---

# Invoke Development - Hardware and Golden Image

## Invoke Result

- Mode: define -> design -> plan
- Phase status: flag
- Target artifact: hardware and image procedure specification
- Template family: procedure/proof specification packet
- Coding boundary: this artifact defines procedures and receipts; later scripts
  such as image verification or backup export are separate implementation work
- Next route: task-session or engineer-owned implementation after thresholds and
  manifest interface are confirmed

## Non-Strict-Coding Classification

This node is selected because the immediate work is a testable hardware/image
spec: reference workstation fields, burn-in procedure, image-write verification,
backup/export, recovery, and receipt contracts. Scripts may follow later, but
the current gap is the spec.

## Define Artifact

Objective: define the hardware-to-Golden-Image chain so a unit can be accepted,
imaged, verified, backed up, exported, and recovered without relying on tacit
engineer knowledge.

Source contracts:

- `docs/features/hardware-golden-image/BUILD-SPEC.md`
- `docs/golden-quill-task-role-breakdown-handoff.md`
- `router.yaml` signing and boot-manifest notes
- `CLAUDE.md` hardware and sovereignty constraints

Terms:

- reference workstation spec;
- approved alternative rule;
- burn-in acceptance receipt;
- Golden Image manifest;
- per-unit verification receipt;
- customer-owned export.

Open gaps:

- `GAP-HGI-REFERENCE-SPEC`
- `GAP-HGI-BURN-IN`
- `GAP-HGI-IMAGE-VERIFY`
- `GAP-HGI-BACKUP-RECOVERY`

## Design Artifact

Context view: the node turns a physical machine plus a signed image into a
repeatable customer-owned appliance.

High-level structure: reference spec -> procurement -> burn-in -> OS baseline
-> Golden Image write -> image verification -> backup/export/recovery.

Low-level components:

- `reference_workstation_spec.yaml` shape with the 128GB floor;
- `burn_in_thresholds.yaml` shape with operator-supplied values;
- Golden Image manifest contract with digest set and Ed25519 signature;
- per-unit verification receipt;
- backup/export manifest and recovery receipt.

Workflow process: capture SKU/spec values, run burn-in, verify signed image,
write image, verify post-write digests, boot-verify, then prove backup and
recovery.

Decision flow: threshold and SKU values remain operator/external-deferred. The
procedure shape can be authored before those values are filled.

Dependency interface: consumes Tilth runtime's signed image artifact and feeds
node-on-desk readiness plus white-glove delivery.

## Plan Artifact

Implementation layering for this authoring pass:

| Layer | Decision Question | Minimum Working Unit | Exit Evidence |
| --- | --- | --- | --- |
| L0 | Do we know the hardware/image evidence shape? | Reference spec and receipt fields. | Reviewable YAML/receipt contract. |
| L1 | Can the procedure reject bad units or bad writes? | Burn-in and byte-flip verification toy game. | Expected failure cases named. |
| L2 | Can backup/recovery preserve customer custody? | Export/recovery contract. | Sovereignty criteria captured. |
| L3 | Can a field tech repeat it? | Checklist-ready procedure. | Non-author run criterion. |

Work-pack:

| Task ID | Goal | Write Scope | Validation |
| --- | --- | --- | --- |
| HGI-AUTH-001 | Author reference workstation template. | Future spec file or this packet. | 128GB floor check. |
| HGI-AUTH-002 | Author burn-in receipt and threshold table. | Procedure spec. | Metrics captured even on failure. |
| HGI-AUTH-003 | Lock Golden Image manifest interface with runtime build. | Interface contract. | Digest/signature fields agreed. |
| HGI-AUTH-004 | Author backup/export/recovery receipt shape. | Procedure spec. | Wipe -> restore digest criterion named. |

SWU handoff:

| SWU ID | Parent Task | Done Criteria | Execution Owner |
| --- | --- | --- | --- |
| SWU-HGI-001 | HGI-AUTH-001 | Template fields and approved-alternative rule complete. | local-fallback |
| SWU-HGI-002 | HGI-AUTH-002 | Four-axis burn-in procedure has receipt contract. | local-fallback |
| SWU-HGI-003 | HGI-AUTH-003 | Manifest producer/consumer boundary with TRB is explicit. | subagent |
| SWU-HGI-004 | HGI-AUTH-004 | Backup/export/recovery criteria preserve customer custody. | local-fallback |

Residue: SKU datasheet values and burn-in thresholds still require operator
input or approved bounded external research.


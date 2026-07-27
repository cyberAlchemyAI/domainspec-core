# Context Pack — UI Prototyping Studio Architecture Review Refresh

- Task: apply the accepted architecture-review changes to the executable
  planning and Craft surfaces.
- Mode: standard, strict.
- Repository commit at selection:
  `82be80e6ab74553d974d818160ff4b3e22313801`.
- Files selected: 12.
- Obligation coverage: 10/10.
- Handoff pack: none; this is Invoke Refresh authoring evidence.
- Authority: selector-level evidence only. The accepted review and Craft owner
  govern their respective decisions; Inventory is discovery-only.

## Obligations

| ID | Obligation | Evidence | Status |
| --- | --- | --- | --- |
| R-01 | Preserve the accepted 11-finding review boundary. | Review `findings.md#approval`; `PARENT-APPROVAL.md#accepted-result`. | covered |
| R-02 | Keep June deep spec historical, not canonical. | Review `findings.md#deep-spec-disposition--keep-as-historical-evidence`. | covered |
| R-03 | Remove the July package's false canonical wording without rewriting its historical bytes wholesale. | July `README.md#output-map`; review F-01. | covered |
| R-04 | Produce one stable task/SWU identity crosswalk. | July `WORK-PACK.md#swu-manifest`; review F-09. | covered |
| R-05 | Choose one deterministic browser proof route before projection work. | Review F-02/F-06; `backend/e2e/helpers.ts` launch and exit paths. | covered |
| R-06 | Require an application-owned projection contract and fresh persisted state. | Review F-03/F-04/F-08; July architecture Views 2–4. | covered |
| R-07 | Preserve a distinct style/global diff lane. | Review F-05; `application/admission.ts` `diffByOdId`. | covered |
| R-08 | Resolve confirmation policy consistently with existing actor-neutral acceptance. | Review F-07; Craft DEC-026; July Task GSP-003. | covered |
| R-09 | Separate export confirmation from evidence/readiness semantics. | Review F-14; `export-design-handoff.ts`; slice test handoff case. | covered |
| R-10 | Delay root-doc/Craft closeout claims until implementation receipts exist. | Review F-01/F-11 and dependency-safe recommendation. | covered |

## Included Context

| Path | Selectors | Obligation fit |
| --- | --- | --- |
| `development/reviews/20260727-architecture-plan-deep-spec-review/findings.md` | Evidence Boundary; F-01–F-14; Dependency-Safe Next Recommendation; Approval | R-01–R-10 |
| `development/reviews/20260727-architecture-plan-deep-spec-review/PARENT-APPROVAL.md` | Basis; Accepted Result | R-01 |
| `.craft/ledger.yml` | root/extraction/UX contexts; DEC-026; current indexes and next moves | R-03, R-08, R-10 |
| `CRAFT.md` | Quick Links; root next move; current evidence claims | R-03, R-10 |
| July `README.md` | Output Map; Boundary | R-03 |
| July `ARCHITECTURE-UPGRADE.md` | Views 2–6; gaps | R-06–R-09 |
| July `WORK-PACK.md` | Delivery Slices; Task Status Board; SWU Manifest; Distill Validation | R-04–R-10 |
| July Task GSP-001 | implementation detail; acceptance evidence | R-05, R-06 |
| July Task GSP-003 | confirmation framing | R-08 |
| July Task GSP-004 | helper, handoff, docs mixed SWUs | R-04, R-05, R-09, R-10 |
| `backend/e2e/helpers.ts` | `runCli`; `startPreview`; child-process exit handling | R-05 |
| `backend/src/modules/ui-prototyping-studio/application/export-design-handoff.ts` | `missingRefs`; integration readiness update | R-09 |

## Exclusions

- Root `README.md`, `ARCHITECTURE.md`, `SPEC.md`, `WORK-PACK.md`, and
  `development/PLAN-NEXT.md` are closeout targets, not refresh-authoring
  targets; they change only after implementation receipts.
- Open Design provenance and `CraftEvidencePack` remain deferred because the
  accepted review found no defect requiring that optional L3 expansion.
- Body War and TROQAR are not authority for this plan.

## Resolution

The exact first unit is the shared local-`tsx` evidence helper. It has one
primary behavior—deterministic, fail-fast browser-process launch—and
recomposes into every later Playwright witness. Projection, freshness, diff,
action framing, handoff semantics, and documentation then receive distinct
one-to-one SWUs.

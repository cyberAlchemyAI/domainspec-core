---
module: body-war-login-suggest-track-score-preview
version: current
status: pass-with-owned-decisions
updatedAt: 2026-07-28
docType: invoke-define-transport
---

# Invoke Define Transport

## Intent Record

- Target: Body War SuggestedTrack child context.
- Requested action: map the entire login-to-score-preview journey using
  ontology so a working prototype can be implemented and tested.
- Authorized mutation: this new Invoke run only.
- Not authorized: application implementation, deployment, Craft recomposition,
  ontology promotion, or execution of a planned SWU.
- Existing completed BWOI artifacts remain immutable historical evidence.

## Discovery and Inventory Gate

- Discovery:
  `projects/body-war/docs/features/parque-taquaral-online-mvp/DISCOVERY.md`
- Current research:
  `projects/body-war/development/research/20260727-suggested-track-testable-prototype-gap/findings.md`
- Inventory lookup readiness: pass.
- Selected Inventory entry:
  `body-war-suggested-track-testable-prototype-gap-research-result-synthesis`.
- Inventory authority: read model only; raw Body War sources and the Craft
  ledger remain load-bearing.

## Template Selection

| Candidate | Eligibility | Selection |
| --- | --- | --- |
| DomainSpec spec family | Typed actors, objects, operations, states, interfaces, and acceptance claims. | selected |
| Architecture bundle | Crosses auth, external provider, privacy, storage, calculation, UI, and evidence boundaries. | selected for Design |
| UX plan | Natural-person consent, responsive Help binding, and score explanation are acceptance-critical. | selected for Design |
| Research family | Official Strava contract needed a current primary-source check; no broader external research is needed. | bounded reference check complete |

## Define Sanity Tension

Standard Distill budget is assumed because the user did not request a custom
budget.

| Pressure | Proposed resolution | Residue |
| --- | --- | --- |
| “Confirm track” could imply promotion. | Define confirmation as exact runner consent plus candidate attachment only. | operator promotion remains later |
| Geometry is necessary for score but current consent omits maps. | Add a versioned geometry-use consent and store only a privacy-filtered candidate. | privacy filter parameters need ratification |
| A visible score is desired but the source supplies only weights. | Require a versioned ScorePolicy; provide a bounded V0 decision shape. | normalizers/caps remain an owner decision |
| Testing should start soon, but real Strava and hosting remain open. | Separate L0 fixture, L1 moderated local, and L2 real-provider evidence lanes. | each lane has its own gate |

## Define Result

- Spec: `SPEC.md`
- Glossary: `GLOSSARY.md`
- Candidate ontology: `ONTOLOGY-MAP.md`
- Context: `CONTEXT-PACK.md`
- Design blockers: none
- Numeric implementation blocker: ScorePolicy V0 owner ratification
- Real-provider implementation blockers: token read/decrypt/refresh, activity
  gateway, geometry gateway, hosted admission
- Next route: Invoke Design


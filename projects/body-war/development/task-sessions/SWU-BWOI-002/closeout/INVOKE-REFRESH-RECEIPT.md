---
module: body-war-suggested-track-domainspec-witness
status: pass
updatedAt: 2026-07-27
docType: invoke-refresh-owner-receipt
---

# Invoke Refresh Receipt

- Mode: refresh
- Spell: invoke
- Canonical ID: invoke
- Scope: Body War SWU-BWOI-002 closeout
- Phase status: pass
- Phase status basis: exact execution evidence produced four safe deltas with
  zero Refresh authoring blockers
- Handoff readiness: ready
- Mutation mode: apply-approved
- Activation source: continuation
- Source signals: one evidence-added signal
- Target artifacts: four, exact declared inventory
- Applied changes: DomainSpec SWU completed; integration SWU selected; Craft
  evidence and next route synchronized; successor receipt alias repaired
- Skipped changes: none
- Material package: pass, ready,
  `body-war:SWU-BWOI-002:closeout-refresh`,
  digest `f6bfa3bbe186177371d3a575e870b2ecbe468f9d0301467a03aaacd72600ac26`
- Dependency result: pass
- Owner boundary: pass
- Publication boundary: pass
- Mutation ready: true
- Validation: DomainSpec 3/3; Body War application 3/3; Craft
  YAML/index/view pass; scoped diff check pass
- Blockers by scope: none
- Unresolved gaps: the proof remains one experimental CT-2 seam; the
  digest-bound integration witness remains unexecuted
- Next route: Task Session to `SWU-BWOI-003`

The returned route is bookkeeping output only. This Refresh did not execute
`SWU-BWOI-003`, promote either standalone witness, release DomainSpec,
publish, or deploy.

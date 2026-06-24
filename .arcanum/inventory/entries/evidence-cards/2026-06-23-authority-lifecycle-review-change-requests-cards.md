---
tags: [inventory, cyberalchemy-v2, authority-lifecycle-invariant, review-change-request, promotion-guardrail, definitions-governance, constitution-governance, claim-proof]
node_type: evidence-card
is_session: false
layer: architecture
nature: reference
status: candidate
created: 2026-06-23
sources: [telemetry/agents/subagents-dispatch.yaml, .arcanum/inventory/entries/authority-lifecycle-invariant-synthesis.md, .arcanum/inventory/entries/scientific-authority-lifecycle-synthesis.md, cyberAlchemy-v2/authority/AUTHORITY-MODEL.md, cyberAlchemy-v2/authority/promotion-policy.md, cyberAlchemy-v2/authority/definitions/source-clusters/authority-lifecycle.md]
---

# Evidence Cards - Authority Lifecycle Review Change Requests

Verified change requests from the inline review dispatch
`2026-06-23-authority-lifecycle-artifacts-review` (3 reviewers: claim>proof /
contradiction / vacuity; all findings P8-verified by the parent before reporting).
Each card is a candidate Inventory read model and a **non-authority** handoff: it
records a requested change and the owner that must apply it. **None is applied.**

## `cr1-rescope-or-demote-lifecycle-invariant`

- ID: `cr1-rescope-or-demote-lifecycle-invariant`
- Status: **resolved (applied 2026-06-23)**
- Severity: major
- Claim or candidate: the invariant `no authority without a lifecycle`
  (`CAV2-CAND-LIFECYCLE-002`) is largely a **re-skin of the existing Authority
  Rule**; its only verified non-vacuous core is a **kind-table closure /
  default-deny rule for unenumerated authority kinds** (OQ-2's `invariant`/`axiom`
  are the live instance; no closure rule exists). Action: re-scope `-002` + the
  `CAV2-C16` draft to the closure rule, or demote to a descriptive restatement.
- Resolution: **re-scoped** (not demoted) — `CAV2-CAND-LIFECYCLE-002` and the
  `CAV2-C16` draft re-scoped to `closed authority-kind enumeration (default-deny
  for unenumerated kinds)`, bound to OQ-2, in `source-clusters/authority-lifecycle.md`.
  Re-scope absorbed the collapse-test-baseline fix (now tested against the Authority
  Rule + ladder) and replaced the redundant "authority-bearing only" scope card.
- Source refs:
  `cyberAlchemy-v2/authority/AUTHORITY-MODEL.md` (Authority Rule, line ~25),
  `.arcanum/inventory/entries/authority-lifecycle-invariant-synthesis.md`,
  `cyberAlchemy-v2/authority/definitions/source-clusters/authority-lifecycle.md`
- Authority level: review change-request, non-authority
- Promotion owner: definitions-governance (term) + constitution-governance (rule)
- Trace: P8-verified — Authority Rule wording confirmed; grep confirmed no existing closure/default-deny rule
- Residue: **applied 2026-06-23** (re-scoped to closed authority-kind enumeration); absorbed the CR3 collapse-test-baseline fix and replaced the CR4 scope-card.

## `cr2-one-term-three-names`

- ID: `cr2-one-term-three-names`
- Status: **resolved (applied 2026-06-23)**
- Severity: major
- Resolution: canonical-track term set to `authority promotion lifecycle`; `scientific authority lifecycle` + `pattern authority lifecycle` recorded as **aliases** (`-001` in `source-clusters/authority-lifecycle.md`; reconciled in `scientific-authority-lifecycle-synthesis.md` Candidate Name). `pattern authority lifecycle` kept alias-only (adjacent to `CAV2-D43`).
- Claim or candidate: the lifecycle object carries three competing names —
  `scientific authority lifecycle` / `pattern authority lifecycle` (descriptive)
  vs `authority promotion lifecycle` (normative) — while the normative synthesis
  says "name it once." Action: pick one canonical-track term, list the others as
  aliases, across both syntheses + the candidate.
- Source refs:
  `.arcanum/inventory/entries/scientific-authority-lifecycle-synthesis.md` (Candidate Name),
  `.arcanum/inventory/entries/authority-lifecycle-invariant-synthesis.md`
- Authority level: review change-request, non-authority
- Promotion owner: definitions-governance
- Trace: P8-verified — name counts confirmed across the two syntheses
- Residue: **applied 2026-06-23.**

## `cr3-fix-evidence-attribution`

- ID: `cr3-fix-evidence-attribution`
- Status: **resolved (applied 2026-06-23)**
- Severity: major-to-minor
- Resolution: added an "Evidence backing (per CR-3)" note to the normative synthesis — SAL cards back the descriptive thesis only; the normative load is backed by `authority-lifecycle-invariant-cards.md`.
- Claim or candidate: the SAL evidence-cards back only the **descriptive** thesis;
  the normative load (D46, growth rule, invariant, collapse-test) is backed by the
  separate `authority-lifecycle-invariant-cards.md`. Action: add a note in the
  normative synthesis stating which card set backs which, so no future task cites
  SAL cards as authority for the invariant.
- Source refs:
  `.arcanum/inventory/entries/evidence-cards/2026-06-23-scientific-authority-lifecycle-cards.md`,
  `.arcanum/inventory/entries/evidence-cards/2026-06-23-authority-lifecycle-invariant-cards.md`
- Authority level: review change-request, non-authority
- Promotion owner: inventory (note) / definitions-governance
- Trace: P8-verified — SAL card `sources:` confirmed to exclude D46/invariant/promotion-policy
- Residue: not applied.

## `cr4-build-from-owned-overclaims`

- ID: `cr4-build-from-owned-overclaims`
- Status: **resolved (applied 2026-06-23)**
- Severity: minor
- Resolution: changed to "build-from-owned **generalization inference**" in the synthesis Generalization row + thesis, the `-001` row/sketch, and the generalization card (the parent object is named in no owned source).
- Claim or candidate: "build-from-owned, **not invention**" overclaims — no owned
  source names the unified parent lifecycle object; naming D43/D46/Growth-Rule as
  instances of one shape is a **generalization inference**. Action: change to
  "build-from-owned **composition / generalization inference** (owner-gated)";
  align the card with its own residue ("instances not yet formally registered").
- Source refs:
  `.arcanum/inventory/entries/authority-lifecycle-invariant-synthesis.md`,
  `.arcanum/inventory/entries/evidence-cards/2026-06-23-authority-lifecycle-invariant-cards.md`
- Authority level: review change-request, non-authority
- Promotion owner: definitions-governance
- Trace: P8-verified — grep confirmed no owned source names the parent object
- Residue: not applied.

## `cr5-demote-settled-tone-framings`

- ID: `cr5-demote-settled-tone-framings`
- Status: **resolved (applied 2026-06-23)**
- Severity: minor
- Resolution: softened the synthesis intro to "**proposed** decision ... not yet enacted"; the Lineage row now reads "candidate drift finding, routed to discipline-governance — not yet confirmed."
- Claim or candidate: candidate findings read as adjudicated/enacted — "CAV2-D43
  != discipline growth rule (gap)" and "the decision to make binding." Action: add
  "(candidate, routed to discipline-governance)"; soften to "**proposed**
  decision ... not yet enacted."
- Source refs:
  `.arcanum/inventory/entries/authority-lifecycle-invariant-synthesis.md`
- Authority level: review change-request, non-authority
- Promotion owner: definitions-governance
- Trace: P8-verified against the synthesis decision-spine + the source-cluster Promotion Gate
- Residue: not applied.

## `cr6-make-scope-boundary-explicit`

- ID: `cr6-make-scope-boundary-explicit`
- Status: **resolved (applied 2026-06-23)**
- Severity: minor
- Resolution: added a "Scope (per CR-6)" clause to the descriptive synthesis Boundary — only the `PromotionCandidate -> ...Authority` segment is binding-rule scope.
- Claim or candidate: the descriptive synthesis is unscoped (whole flow) while the
  normative one is "authority-bearing only" — boundary is implicit. Action: add a
  clause to the descriptive Boundary noting only the
  `PromotionCandidate -> ...Authority` segment is binding-rule scope.
- Source refs:
  `.arcanum/inventory/entries/scientific-authority-lifecycle-synthesis.md` (Boundary, Scientific Method Reading),
  `.arcanum/inventory/entries/authority-lifecycle-invariant-synthesis.md` (Scope row)
- Authority level: review change-request, non-authority
- Promotion owner: definitions-governance
- Trace: P8-verified — descriptive scope is unscoped; normative scopes authority-bearing only
- Residue: not applied.

---
tags: [domainspec-core, cyber-alchemy-lean-fusion, arcanum, permguard, resonantos, vision, capability-foundry, residue, subagent-partition, stages-vs-substrate]
node_type: discovery
is_session: true
layer: architecture, application
nature: explanatory, procedural
status: active
created: 2026-06-15
timestamp: 2026-06-15T21:08:32-03:00
conversation_id: 2026-06-15-capability-foundry-vision-permguard-map
decisions_made: true
contradictions_found: false
specs_updated: [projects/cyber-alchemy-lean-fusion/VISION.md, projects/cyber-alchemy-lean-fusion/DESIGN.md, projects/cyber-alchemy-lean-fusion/discovery/MAP.md, projects/cyber-alchemy-lean-fusion/PERMGUARD-IN-ARCANUM.md]
promoted_candidates: []
expected_importance: 7
importance_rationale: "Lays the high-level VISION map for the capability foundry (stages vs substrate, the two output types, the formal-layer differentiator), banks the permguard×product feature-gap dispatch, and proposes the reusable specialist-subagent partition that future build sessions will load instead of the whole corpus."
---

# Capability Foundry — VISION map + permguard product gap + subagent partition

## Summary

Organizing (no-code) session to assemble the high-level map for the `cyber-alchemy-lean-fusion`
capability foundry — the tool that turns a **vague user intention into a useful artifact**
(knowledge OR executable code). Sibling to `2026-06-15-2100-framework-integration-two-axis-fusion`
(same program, adjacent artifacts). This session produced the **`VISION.md` skeleton**, ran a
**permguard×product feature-gap research dispatch** (8 agents, registered+closed), did an
independent **ResonantOS recon**, and proposed the **specialist-subagent knowledge partition**.

## Decisions & findings

- **Product framing fixed:** the organizing question is "vague intent → useful artifact", where
  the artifact bifurcates into **knowledge** (text, Lean file, phrase) or **code that executes**.
  Now = internal tool for Victor+Vladimir to build code; product later.
- **The differentiator is the formal layer, not the architecture.** The ResonantOS recon proved
  the four-part decomposition is *convergent* — `ResonantOS/2.0.0-alpha` (browser-first agent OS,
  MIT, alpha, 235 commits/0 releases) independently built ~80% of it informally: Delegation Packet
  ≈ governed lifecycle, `ArtifactReturn.residualRisks`+Logician ≈ epistemic core, capability-grant
  broker ≈ permguard, executive/worker/verifier ≈ dispatch — but with **zero formal verification**.
  Our moat = the **three formal legs**: typed/categorical residue, verified permission kernel
  (permguard), subset-rule (claim≤proof).
- **Modeling correction (load-bearing): stages vs substrate.** The flow is STAGES
  (intent-framing → dispatch → verify/residue → artifact); **permguard / observability /
  memory-archive are CROSS-CUTTING SUBSTRATE**, not stages. permguard was mis-placed as a domain
  only; it is the verified, fail-closed gate on every tool-call.
- **Output type decides which substrate carries the weight:** knowledge → residue/subset-rule;
  executable code → permguard. New explicit rule in the VISION.
- **permguard×product feature-gap dispatch (research, 8 agents).** Verified per-request authz is
  **commodity** (Cedar is Lean-verified, shipped in AWS Verified Permissions; Permguard product
  uses Cedar). The only genuine here-not-there capability is the **stateful session taint→egress**
  (rungs 5/8/9) — no product ships it — but it is **vacuous-as-shipped** (secret-label = path-prefix
  on the trust border; bash-egress-bypass proved) and **owned-as-research** (FIDES/CaMeL). C2
  (composition law) and C3/C4 (trust-border + proved-negative) survive as build-from-owned assurance
  artifacts; C5 (tool-typed matchers) KILLed as commodity. Auditor: all PASS.
- **Missing seam surfaced:** the foundry had no MEMORY/ARCHIVE component; ResonantOS Living Archive
  (source-integrity + human/strategist/auto approval tiers) is the strongest external prior art.
  Added as substrate domain #5.
- **Venue/boundary written down** (the thing whose absence caused a misplacement this session — a
  permguard note first written into public `Arcanum/`, then removed and relocated to the private
  fusion project): private research stays in `domainspec-*`; only concept-level goes to public Arcanum.

## Next Steps

- **Dispatch the five specialist domain agents** (VISION §5): Intent & Goal-framing, Dispatch &
  Orchestration, Verification & Residue, Permission & Tool-governance, Memory & Artifact-lifecycle.
  Each produces a compact `projects/cyber-alchemy-lean-fusion/context-packs/<domain>.md` and fills
  its VISION §5 stub — reusable specialists that future build sessions load instead of the whole
  corpus. (Optionally a first batch of the 3 core: Intent, Dispatch, Verification/Residue.)
- **Resolve the open gate (VISION §7 / discovery View 01):** a `research` dispatch in the Lean repo
  on whether an artifact-level residue carries a TYPE that mechanically fires the subset-rule gate.
  Candidate machinery already scoped (MI/resource theories, codensity/nucleus, Σ-fibre, refinement
  types, Galois, residuality theory).
- **Then** synthesize the packs into the full map; only after that consider building.
- **Uncommitted:** the new `cyber-alchemy-lean-fusion/` artifacts (VISION, discovery/, PERMGUARD-IN-ARCANUM)
  in `core`; the `permguard-product-feature-map/` dispatch + telemetry rows in the Lean repo.

## Open Questions

- **The residue-TYPE gate (VISION §7) is OPEN** and load-bearing — the epistemic core (stage 3) and
  residue-as-through-line depend on it. Collapse-test: if the residue is prose with no type that
  fires the gate, the foundry's epistemic half collapses to Arcanum's `residuality-spec` renamed.
- Adopt the Lean repo's axis-separation (reflection / capability / ontology towers distinct) or fuse
  into one layered architecture? (Carried from the sibling 21:00 session — still open.)
- Dispatch all five specialists at once, or the three core first?

## Files touched

- Created (in `core`): `projects/cyber-alchemy-lean-fusion/VISION.md`, `.../README.md`, `.../DESIGN.md`,
  `.../discovery/MAP.md` + `.../discovery/views/01..05`, `.../PERMGUARD-IN-ARCANUM.md`.
- Created (in `domainspec-lean-formalization`): `research-security/permguard-product-feature-map/`
  (`dispatch.yaml`, `agents/01-08`, `research/findings.md`).
- Modified (in `domainspec-lean-formalization`): `telemetry/agents/subagents-dispatch.yaml` — dispatch
  `2026-06-15-permguard-product-feature-map` registered + closed (8 agents, 4 layers).
- Removed (relocations): `domainspec-lean-formalization/research-tooling/cyberalchemy-fusion/` (moved to
  core project); `Arcanum/research/permguard-tool-governance/` (public-repo misplacement, relocated to
  the private fusion project as `PERMGUARD-IN-ARCANUM.md`).
- Dispatch: ResonantOS recon ran as a single helper invocation (P11), not registered as a fan-out.

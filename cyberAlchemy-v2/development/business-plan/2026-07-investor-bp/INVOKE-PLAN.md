---
tags: [invoke, plan, business-plan, investor-bp, private, claim-le-proof]
node_type: invoke-plan
layer: plan
status: flag
created: 2026-07-10
updatedAt: 2026-07-10
docType: implementation-plan
observed_capability: invoke
invoke_mode: plan
target_artifact: investor business plan package
target_owner: private business-plan development cycle
---

# Invoke Plan: Investor Business Plan Package

## Invoke Result

- Mode: plan
- Spell: invoke
- Canonical ID: invoke
- Scope: library
- Phase status: flag
- Mode contract: `.agents/skills/invoke/plan.md`
- Outputs: `INVOKE-PLAN.md`, `IMPLEMENTATION-LAYERING.md`, `WORK-PACK.md`, `EXECUTION-PACK.md`
- Design views: n/a
- Glossary consistency: n/a
- Dispatch techniques: selected trace below; full dispatch document not required because this package does not dispatch subagents
- Distill validation: flag; local validation recorded below, independent Distill sigil run not executed in this turn
- Implementation layering: `IMPLEMENTATION-LAYERING.md`
- Work-pack: `WORK-PACK.md`; single-file SWU manifest with execution-pack companion
- Complexity: medium
- Per-layer planning: L0, L1, L2, L3
- Implementation detail: task specs complete enough for next planning/writing handoff; final BP prose not drafted here
- Smallest working units: complete for planning handoff, selected first SWU is `SWU-BP-001`
- Target artifact: private investor BP package, owned by business-plan development cycle
- Template or recipe selection: Invoke plan + implementation-layering + work-pack + business-plan Whisper preset
- Decisions: build from wedge outward; keep DomainSpec/CAV2 as private substrate; draft evidence registry before front-stage prose
- Unresolved gaps: funding ask/runway, buyer calls, paid pilot/SOW, fresh runnable receipts, comparator refresh, independent Distill run
- Next route: task-session to `SWU-BP-001`, then Whisper business-plan drafting after evidence registry and financial assumptions exist

## Purpose

Turn the accepted business-plan research substrate into an executable plan for a
private investor BP package. This plan does not draft the BP. It defines the
artifact order, evidence gates, SWU handoff boundaries, and claim discipline
needed to draft the BP without letting the story outrun proof.

## Source Context

| Source | Use In This Plan |
| --- | --- |
| `.arcanum/inventory/queries/2026-07-09-business-plan-build-research/findings.md` | Controls BP build order, wedge selection, non-claims, evidence registry, financial model, and 30/60/90 witness queue. |
| `.agents/skills/whisper/presets/business-plan/preset.yaml` | Controls BP composition, audience modes, output modes, required sections, validation checks, and fail conditions. |
| `.agents/skills/invoke/plan.md` | Controls plan-mode gates, implementation layering, SWUs, dispatch technique trace, and Distill validation. |
| `.agents/skills/invoke/templates/work-pack.md` | Controls work-pack structure and SWU fields. |
| `.agents/skills/invoke/templates/implementation-layering.md` | Controls L0-L3 layer decisions and promotion evidence. |

## Target Output Set

The BP execution stream should eventually produce these private artifacts in
this directory:

| Artifact | Role | Current Status |
| --- | --- | --- |
| `diligence-evidence-registry.md` | Source roster, maturity labels, receipts, witnesses, non-claims, and gaps. | Planned first. |
| `source-trace.md` | Source-to-claim map for BP sections and investor artifacts. | Planned first. |
| `financial-assumptions.md` | Bottom-up sprint-unit model, scenarios, sensitivities, runway, use of funds. | Planned after registry. |
| `business-plan.md` | Full private BP for investor confidence and internal operating alignment. | Draft only after registry and financial assumptions. |
| `investor-memo.md` | Decision case for first investor. | Draft after BP body and financial model. |
| `deck-substrate.md` | Meeting-getter compression layer; no new claims beyond BP/data room. | Draft last. |
| `operating-plan.md` | Delivery loop for one paid Metric Trust / AI Work Readiness wedge. | Draft after financial assumptions. |
| `claim-audit.md` | Claim <= proof audit across BP, memo, deck, and registry. | Required before any investor-facing use. |

## Core Planning Decisions

1. Lead with one buyer pocket and one blocked decision, not the whole portfolio.
2. Use the front-stage wedge: fixed-scope Metric Trust / governed AI Work Readiness.
3. Treat DomainSpec/CAV2 as private substrate and diligence evidence, not public product proof.
4. Use Arcanum public-safe evidence only where wording stays inside public/private boundaries.
5. Present founder velocity and artifact breadth as operating-discipline evidence, not traction.
6. Use bottom-up sprint-unit assumptions until paid evidence validates price, hours, costs, cash timing, conversion, and repeat work.
7. Write visible non-claims into every investor artifact.
8. Do not claim certification, compliance, audit-ready status, provably correct agents, finished platform, platform revenue, market pull, unique/first/only, or proven moat.
9. Phrase the compounding effect as a conditional residue hypothesis: repeated paid work may reuse schemas, gates, receipts, owner routes, and bounded witnesses.
10. Use "verifiable" only for named checks/validators/receipts/formal witnesses, and "provable" only where a named formal witness exists.

## Dispatch Spec Technique Trace

Full dispatch JSON is not required for this plan package because this turn does
not fan out to subagents, external executors, or mutation-capable lifecycle
owners. The route still carries protected private context, so the trace records
boundary and evidence gates explicitly.

| Technique ID | Applied To | Validation Expectation | Status |
| --- | --- | --- | --- |
| sequence | Registry -> section map -> financial assumptions -> operating plan -> BP -> memo/deck -> claim audit. | Later artifacts cannot introduce claims unsupported by earlier evidence. | pass |
| frame_handoff | Invoke plan -> task-session / Whisper drafting. | Next route receives exact artifact list, scope, first SWU, and source anchors. | pass |
| handle_handoff | SWU handoff fields in `WORK-PACK.md`. | Each SWU has write scope, done criteria, evidence, and validation surface. | pass |
| residue_ledger | Evidence registry and claim audit. | Compounding substrate is tracked as residue/evidence, not asserted as proof. | pass |
| owner_boundary_check | Invoke vs Task Session vs Whisper. | Invoke plans; Task Session executes bounded SWUs; Whisper drafts prose after evidence inputs exist. | pass |
| artifact_contract_bridge | Whisper preset and BP outputs. | Output artifacts mirror preset-required sections and validation checks. | pass |
| validation_loop | Every slice and SWU. | Each unit has a reviewable check or command. | pass |
| concrete_path_evidence | All planned artifacts. | Future file paths are named and scoped. | pass |
| observability_grouping | Planning package and later execution receipts. | BP evidence stays inspectable by artifact class. | pass |
| scu_swu_reduction | Work-pack SWUs. | The first executable unit is `SWU-BP-001`; later units are sequenced by evidence dependencies. | pass |
| recomposition_proof | SWUs -> BP package. | Every SWU contributes to a named BP artifact or validation gate. | pass |
| execution_receipt_handoff | Task-session route. | Each execution SWU has acceptance evidence and validation surface. | pass |
| authority_split_gate | Private BP vs public Arcanum. | Private substrate remains under `cyberAlchemy-v2/`; no private claims are promoted into `arcanum/`. | pass |

Skipped technique note: subagent fan-out strategy is deferred. The next BP
drafting pass may use subagents for market refresh, financial model review, and
claim audit, but this invoke plan does not dispatch them.

## Build Sequence

1. Create the evidence registry and source trace first.
2. Build a BP section map with evidence, missing witness, and demotion gate for every section.
3. Build the bottom-up sprint-unit financial assumption model.
4. Draft the operating plan around one paid wedge and one receipt bundle.
5. Draft the full BP with explicit evidence boundary and non-claims.
6. Draft the investor memo and deck substrate last.
7. Run a claim audit before investor use.

## Distill Validation

| Check | Result | Evidence Or Gap |
| --- | --- | --- |
| Smallest coherent unit or SWU boundary | pass | `SWU-BP-001` creates the evidence registry and source trace, the minimum base needed before BP prose. |
| Recomposition proof | pass | Registry, financial assumptions, operating loop, BP, memo/deck, and claim audit recompose into the target investor BP package. |
| Hidden acceptance-critical gaps | flag | Ask amount, runway, target investor type, buyer-call evidence, paid-pilot packet, and fresh receipts are missing. |
| Deferred complexity | flag | Full subagent research dispatch and independent Distill sigil validation are deferred. |
| Navigation to first executable unit | pass | Start with `WORK-PACK.md` -> `SWU-BP-001`. |

Verdict: `flag`. The plan can guide the next planning/writing work, but it
should not be treated as mutation-capable investor artifact readiness until the
flagged gaps are either filled or explicitly labeled in the BP.

## Gap Ledger

| Gap ID | Scope | Description | Owner | Repair Path |
| --- | --- | --- | --- | --- |
| BP-GAP-001 | Funding | Ask amount, runway, use-of-funds milestones, and desired investor instrument are not specified. | founder | Decide ask/runway or draft with placeholder assumptions clearly marked. |
| BP-GAP-002 | Market | 5-10 buyer calls around one blocked metric/workflow decision are not yet recorded. | founder / research | Run interview queue and record owner, urgency, budget path, workaround, and willingness to pay. |
| BP-GAP-003 | Commercial | No paid pilot/SOW packet is recorded for the lead wedge. | founder | Create SOW specimen, then validate with one paid pilot. |
| BP-GAP-004 | Evidence | Fresh runnable receipts are not yet collected for the diligence registry. | task-session | Rerun selected tests/builds/audits and store results in registry. |
| BP-GAP-005 | Competition | Comparator archive needs dated refresh before any unique/first/only claim. | research | Refresh spec-first, AI governance, traceability, formal methods, and audit categories. |
| BP-GAP-006 | Validation | Independent Distill validation was not executed in this turn. | invoke follow-up | Run a dedicated Distill validate pass after the first artifact set exists. |

## Next Route

Start a bounded `task-session` on `SWU-BP-001`: create
`diligence-evidence-registry.md` and `source-trace.md` from the accepted findings
without drafting investor prose. After that, use the business-plan Whisper preset
for controlled drafting only once evidence and financial assumptions exist.


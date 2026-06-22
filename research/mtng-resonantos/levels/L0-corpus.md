# L0 — Corpus (source record)

> **Source boundary.** Everything below is `primary-source` *for the packet* — i.e. a faithful
> record of what the packet files say and where. The packet's own claims about external systems
> (ResonantOS internals, OKF) are recorded here as **what the packet asserts**, not as verified
> external fact. Date checked: **2026-06-21** (UTC packet creation: 2026-06-17T21:50:39Z).

## Source record

| Field | Value |
|---|---|
| Target | MTNG Review Packet v2 |
| Path | `research/MTNG-review-packet-v2-2026-06-17-clean/` (sibling; immutable) |
| Packet name | `MTNG-review-packet-v2-2026-06-17-clean` |
| Author of spec | Dave Gardner |
| Target system | ResonantOS |
| Mutability | Immutable — `manifest.json` carries per-file SHA-256 + `source_archive_sha256` |
| Files | 9 (8 markdown + 1 PDF) + manifest |
| Fetched/extracted | All 8 markdown read in full; PDF extracted via pdfkit → `/tmp/analog6.md` (6 pages) |

## Packet map (file by file)

| File | Bytes | Role | Source kind |
|---|---|---|---|
| `00-README.md` | 1711 | Packet intro + suggested review instruction (review the v2 spec as an outside architect; be critical) | primary-source |
| `01-MTNG-build-spec-v2.md` | 33953 | **The main proposal.** 29 sections: exec summary, V1 positioning, problem statement, core concept, deployment model, run profiles, data minimization, engine+tools, Phase 0 integration mapping, provider fabric, branching rules, fast path, node lifecycle, validators, loop breaker, recombination, memory, contribution, OKF, pilot, data structures, mode registry, build order, tests, risks, maintainer questions, non-goals, summary | primary-source |
| `02-technical-review-analog6.pdf` | 203180 | Prior **Analog 6** technical review (reviewer for Dave; "Strong foundation, recommended for build conversation with integration mapping first"). 6 pages. Reviews the *v1* spec. | related-source |
| `03-review-questions.md` | 1810 | 21 focused questions for next reviewer/maintainers across V1 scope, integration, branching/validation, OKF, memory/contribution, failure conditions | primary-source |
| `04-optional-context.md` | 1311 | Origin story (resonance-like branching metaphor), the Post-Hoc Issue Packager flow, and 6 "MTNG is not …" interpretation guards | primary-source |
| `05-changelog-v2.md` | 2282 | 11 major scope changes made after Raptor mini + Gemini; 4 remaining intentional gaps | primary-source |
| `06-Raptor-mini-review.md` | 9521 | Outside audit (GitHub Copilot / "Raptor mini"): "conceptually sound … too abstract to implement directly … schema/inspection pipeline not live runtime" | related-source |
| `07-Gemini-review.md` | 7008 | Outside review (Gemini): "Strongly Recommended with Strict Boundary Conditions … never an online runtime orchestration layer in V1" | related-source |
| `08-review-response.md` | 2495 | How v2 responds to the three reviews; 9 changes + 5 remaining maintainer questions | primary-source |

## What the spec proposes (v2, faithful summary)

- **Core thesis.** Agent workflows fail because one context is asked to hold too many
  unresolved jobs at once. (`01` §4; echoed by Analog 6 as "state-space collapse / attention thrash".)
- **Pipeline.** `Signal → Mode → Node → Validator → Synthesis` (`01` §5).
- **Core boundary rule.** "Branch only when validation, output artifact, context needs, tool
  requirements, memory treatment, contribution record type, safety boundary, or authority
  boundary changes." (`01` §1, §12).
- **V1 = Post-Hoc Issue Packager.** On-demand CLI/sidecar, selected inputs only, run-local
  state, audit-first; explicitly *not* always-on, *not* live orchestration, *not* auto memory
  promotion, *not* contribution valuation, *not* a Guardian Core / provider-routing replacement
  (`01` §1, §3, §28).
- **Outputs.** `signal-manifest.yaml`, `branch-nodes.yaml`, `developer-issue-packet.md`,
  `memory-candidates.md`, `contribution-records.yaml`, `validator-report.md`, `audit-log.jsonl`,
  `okf/` (`01` §1, §21).
- **V1 simplifications vs v1.** Binary branch triggers (numeric *Branch Pressure Score*
  deferred); "Tone" → "Routing Signature"; lifecycle `proposed → processing → closed` (+
  `closed_result`); hard loop limits (1 reroute, 1 validator failure/node, stop on 2nd)
  (`05`; `01` §12–§16).
- **OKF policy.** OKF-first for exported knowledge artifacts; MTNG-native YAML/JSON for
  operational state and edge cases; explicit `edge_case_flags` when OKF is insufficient (`01` §20).

## Analog 6 PDF — extracted content (related-source)

6-page review of the **v1** spec by "Analog 6", dated 2026-06-16, author of spec Dave Gardner.
Verdict: *"Strong foundation. Recommended for build conversation with integration mapping as the
first step."* It documents the **v1** vocabulary that v2 later simplified:

- v1 had **6 processing phases** (Intake, Mode Detection, Branch Creation, Contracted Delegation,
  Synthesis & Memory Promotion, Contribution Accounting) — v2 collapses lifecycle to 3 states.
- v1 **Branch Pressure Score**: weighted signals (safety/authority=6, validation contract=5,
  failed tool retry=5, goal conflict=5, agent/tool change=4, output artifact=4, context
  pollution=4, memory use=4, interpretation shift=3, contribution record=3) with escalation
  thresholds (≥5 split, ≥8 human review, ≥10 stronger model, ≥12 stop/freeze) — **v2 defers all
  of this** to binary triggers.
- v1 **12 contribution types**; v1 5-tier mode detection — both simplified in v2.
- The PDF's **§6 concerns** (the ones v2 claims to answer): mode-detection accuracy gap, graph
  recombination complexity, fast-path definition, integration with existing ResonantOS
  architecture, overhead scaling. These are the spine of the residue map (`L1`).

## Honest cutoff

- The **ResonantOS repository was not read.** Guardian Core, Blackboard, Bridge Server, Event
  bus, Provider fabric / provider broker, Living Archive, add-on capability model are named by
  the spec and the reviewers; this tower has **no source** confirming their existence or shape.
- **OKF was not fetched.** The spec calls it "Google's Open Knowledge Format"; the Gemini review
  calls it "Open Knowledge Framework (OKF)". The discrepancy is unresolved and the format itself
  is unverified.
- The Analog 6 PDF reviews **v1**, not v2; some of its concerns are addressed by v2's
  narrowing, some are deferred rather than solved. The ledger tracks which is which.

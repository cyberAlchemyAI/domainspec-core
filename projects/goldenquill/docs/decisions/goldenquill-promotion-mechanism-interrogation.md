---
title: GoldenQuill Promotion Mechanism Interrogation
date: 2026-06-01
status: complete
target_scope: goldenquill-promotion-mechanism
mode: blocker-decision-interview
decision_record: goldenquill-promotion-mechanism-open-gaps.md
questions_asked: 6
decisions_recorded: 6
---

# GoldenQuill Promotion Mechanism Interrogation

## Purpose

Resolve the six blocker decisions recorded in
`goldenquill-promotion-mechanism-open-gaps.md` one question at a time.

## Interview Order

1. DG-001: Promotion Unit Home.
2. DG-002: First Implementation Location.
3. DG-003: `allowed_uses` Ownership.
4. DG-004: KPI Authority Boundary.
5. DG-005: Org-Scoped Feedback Generalization.
6. DG-006: Stage-Depth Scoring.

## Active Question: DG-001 Promotion Unit Home

Context: the current design proposes `PromotionCandidate` as the bridge between
`MemoryEvidencePacket` evidence and owner-owned `PromotionRecord` or equivalent
decision artifacts.

Why it matters: this choice determines which lifecycle owner gets schema
pressure first and whether the first implementation is GoldenQuill-specific,
Ontology Vault-general, or explicitly bridged.

Recommended default: bridge artifact for design, with GoldenQuill-local toy
fixtures for the first validation slice.

Unresolved risk if unanswered: implementation may either overfit GoldenQuill and
drift from Ontology Vault, or over-govern the first slice before a toy validator
proves the grant-specific need.

Target artifact: `goldenquill-promotion-mechanism-open-gaps.md`

Options:

| Option | Meaning | Trade-off |
| --- | --- | --- |
| A. GoldenQuill local model | `PromotionCandidate` lives in GoldenQuill first. | Fastest toy validation, higher drift risk. |
| B. Ontology Vault companion schema | Promotion is designed as an Ontology Vault companion first. | Strong governance, slower and broader. |
| C. Bridge artifact | `PromotionCandidate` is a bridge that can map to GoldenQuill fixtures now and Ontology Vault `PromotionRecord` later. | Best boundary preservation, slightly more schema. |

## Decision Log

- DG-001 selected and revised: GoldenQuill local model with Ontology Vault as
  an explicit governance layer. Rationale: GoldenQuill needs local grant
  semantics, but promotion governance should be embedded through Ontology Vault
  compatibility rather than invented as ungoverned memory authority.
- DG-002 selected: first executable slice lives in GoldenQuill local
  `grant_dag`, with an Ontology Vault layer or adapter. Rationale: GoldenQuill
  can test grant lifecycle, KPI, and outcome semantics locally while enforcing
  PromotionRecord-compatible constraints.
- DG-003 selected D: split proposed/approved uses. Rationale:
  `PromotionCandidate` expresses requested use, while the Ontology Vault
  governance layer or owner decision records authorized use.
- DG-004 selected B: selected KPIs create candidates. Rationale: metrics can
  trigger outcome-driven learning only after source, denominator, org-scope,
  and interpretation checks; they never promote directly.
- DG-005 selected B: redaction/generalization gate. Rationale: feedback remains
  org-scoped by default, but reusable learning can be created after
  privacy-safe abstraction and owner approval.
- DG-006 selected C: global stage plus local profile override. Rationale: a
  shared baseline enables toy validation and dashboard comparison, while
  funder-family overrides preserve accuracy when evidence shows the global
  scale is too coarse.

## Resolved Question: DG-002 First Implementation Location

Context: DG-001 selected Ontology Vault companion schema as the home for
promotion semantics. We still need a first executable or fixture slice.

Why it matters: this determines whether the next task pressures Ontology Vault
fixtures first, builds a GoldenQuill validator first, or keeps everything in a
development-only schema pressure pack.

Recommended default after DG-001: Ontology Vault fixtures first, then a
GoldenQuill `grant_dag` consumer validator after the companion schema shape is
proved.

Unresolved risk if unanswered: implementation may start in GoldenQuill and
accidentally re-own promotion semantics despite DG-001.

Target artifact: `goldenquill-promotion-mechanism-open-gaps.md`

Options:

| Option | Meaning | Trade-off |
| --- | --- | --- |
| A. GoldenQuill `grant_dag` first | Implement toy validator under `projects/goldenquill/pipeline/grant_dag/`. | Fast local tests, but risks re-owning promotion semantics. |
| B. Memory mesh development first | Add schema pressure fixtures near `MemoryEvidencePacket`. | Keeps evidence close, but may confuse evidence capture with promotion. |
| C. Ontology Vault fixtures first | Add or design companion-schema pressure fixtures in Ontology Vault, then consume from GoldenQuill. | Best alignment with DG-001, slower before GoldenQuill code. |

Selected answer: GoldenQuill local implementation with Ontology Vault as an
explicit layer. This is a custom hybrid of A and C.

## Resolved Question: DG-003 Allowed Uses Ownership

Context: the model now has GoldenQuill-local grant semantics with an Ontology
Vault governance layer. `allowed_uses` controls whether evidence or a promoted
candidate may be used for orientation, drafting, decision input, citation,
learning, or promotion.

Why it matters: this decides whether use permissions are attached to raw
evidence, the proposed candidate, the owner decision, or split across the
lifecycle.

Recommended default: split proposed and approved uses. The candidate can request
`proposed_allowed_uses`; the owner decision or PromotionRecord-compatible layer
sets `approved_allowed_uses`.

Unresolved risk if unanswered: GoldenQuill may treat retrieved evidence as
draft-safe or promotion-safe before the Ontology Vault layer has approved that
use.

Target artifact: `goldenquill-promotion-mechanism-open-gaps.md`

Options:

| Option | Meaning | Trade-off |
| --- | --- | --- |
| A. Evidence packet owns uses | `MemoryEvidencePacket` carries allowed uses. | Simple, but overloads evidence capture. |
| B. Candidate owns uses | `PromotionCandidate` declares allowed uses. | Good for proposals, but can overclaim before owner approval. |
| C. Owner decision owns final uses | Only the Ontology Vault / owner decision sets allowed uses. | Safest, but less expressive before decision. |
| D. Split proposed/approved uses | Candidate proposes uses; owner decision approves final uses. | Most precise, a little more schema. |

Selected answer: D. Split proposed/approved uses.

## Resolved Question: DG-004 KPI Authority Boundary

Context: the refresh added `GrantKpiObservation` nodes for win rates, stage
depth, review movement, cycle time, compliance pass rate, relationship
touchpoints, and similar metrics.

Why it matters: KPIs are seductive little troublemakers. If they become
authority too early, GoldenQuill may optimize for dashboard movement instead of
truthful grant learning.

Recommended default: selected KPIs may create `PromotionCandidate` records only
after source, denominator, org-scope, and interpretation checks. KPIs never
promote directly.

Unresolved risk if unanswered: win/loss metrics could silently become learning
authority without evidence, denominator semantics, or owner review.

Target artifact: `goldenquill-promotion-mechanism-open-gaps.md`

Options:

| Option | Meaning | Trade-off |
| --- | --- | --- |
| A. Dashboard-only | KPIs are read models only. | Safest, but weak learning loop. |
| B. Selected KPIs create candidates | KPIs can create `PromotionCandidate` records after validation checks. | Balanced; needs denominator and source validation. |
| C. KPI thresholds can promote | Repeated KPI thresholds can trigger promotion after configured gates. | Powerful but too risky until mature validation exists. |

Selected answer: B. Selected KPIs create candidates.

## Resolved Question: DG-005 Org-Scoped Feedback Generalization

Context: wins, rejections, reviewer comments, and funder feedback can teach
GoldenQuill, but they can also expose private applicant facts, funder
relationships, or proposal strategy.

Why it matters: this decides whether learning from real outcomes remains
private, can become reusable after redaction/generalization, or depends on
manual operator promotion.

Recommended default: org-scoped by default; workspace-safe learning only after
a redaction/generalization gate plus owner approval.

Unresolved risk if unanswered: rejection or win feedback could leak private org
context into shared GoldenQuill learning or ontology.

Target artifact: `goldenquill-promotion-mechanism-open-gaps.md`

Options:

| Option | Meaning | Trade-off |
| --- | --- | --- |
| A. Always org-scoped | Feedback never becomes workspace-global. | Safest, but loses cross-client learning. |
| B. Redaction/generalization gate | Feedback can become reusable only after privacy-safe abstraction and approval. | Balanced, needs fixtures and policy. |
| C. Manual operator promotion only | Human manually decides every generalization. | Careful but slow and inconsistent. |

Selected answer: B. Redaction/generalization gate.

## Resolved Question: DG-006 Stage-Depth Scoring

Context: `stage_depth_score` measures how far a grant got through the lifecycle
even when it did not win. The current enum includes prospect, eligible match,
LOI, full invite, submitted, portal validated, agency retrieved, under review,
feedback received, awarded, declined, post-award active, reporting current, and
closed out.

Why it matters: the scoring model affects dashboards, KPI candidate generation,
and cross-funder comparison.

Recommended default: global stage enum for toy validation, with local
funder-family profile overrides later.

Unresolved risk if unanswered: a federal-centric score may misrepresent
foundation or corporate grants, while fully custom scores may become impossible
to compare.

Target artifact: `goldenquill-promotion-mechanism-open-gaps.md`

Options:

| Option | Meaning | Trade-off |
| --- | --- | --- |
| A. Global enum/score | One stage-depth scale for every funder. | Simple and testable, but may overfit federal grants. |
| B. Funder-family-specific score | Separate score per funder family. | Accurate, but harder to compare and validate. |
| C. Global stage plus local profile override | Shared baseline with optional funder-family overrides. | Balanced, slightly more schema. |

Selected answer: C. Global stage plus local profile override.

## Pending Questions

None.

## Verdict

`pass`

All blocker questions have been answered. The decision gate may proceed to
artifact refresh, Refine, or bounded Task Session.

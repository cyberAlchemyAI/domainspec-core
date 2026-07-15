---
module: domainspec-v2-foundation-execution
version: current
status: planned
updatedAt: 2026-07-14
docType: implementation-layering
---

# Implementation Layering: Foundation Execution

## Purpose

Keep Layer 0 minimal and prevent the desired engine from inventing the authority, profile, or direction it is supposed to consume.

## Layer Decision Table

| Layer | Decision question | Minimum working unit | Included now | Deferred scope | Exit evidence | Promotion decision |
|---|---|---|---|---|---|---|
| L0 Guard trust | After this layer, we know whether current repository evidence still satisfies the retired-orchestration invariant. | Review four violating files, pin exact dispositions, restore the guard, kill seeded active and digest-drift fixtures. | SGRM-006/007 retry only. | Authority census and all semantic artifacts. | retry receipts and zero-violation report. | proceed to FPR-01 or stop on active reference. |
| L1 Authority and profile | After this layer, we know whether one ratified source baseline can support one exact backend profile. | FPR-01 baseline followed by FPR-02 profile digest. | source census/dispositions, counts/statuses, product/profile/pilot matrices. | B-to-Spec content, graph schema, compiler. | owner ratification and stable profile digest with red controls. | proceed to direction/mapping or reopen owner decision. |
| L2 Governed meaning | After this layer, we know whether a bounded business plane has explicit precedence and a total mapping into authoritative Spec sources. | direction decision plus CT-1 and EC-3/EC-4 mapping witnesses. | BO, BK, B manifest, contradiction policy, total B-to-Spec map. | compiler IR, architecture/formal/verification planes. | accepted decision, mapping receipt, endpoint/orphan/collapse mutants. | proceed to projection or remediate direction. |
| L3 Semantic projection | After this layer, we know whether one exact Spec source can be projected and independently retracted without silent loss. | two nodes, one admitted edge, one explicit quotient, separate comparator. | required-source manifest, Sg/G artifacts, schemas, quotient registry, mutants. | broader type/edge coverage and FPR-05 onward. | totality report and independent retraction receipt. | admit read-only dogfood or reopen FPR-04. |

## Non-Regression Guardrails

- Later layers must rerun the live guard and preserve every earlier receipt input digest.
- A downstream artifact cannot replace its upstream authority source.
- A generated graph is a projection, not a second semantic authority.
- The FPR-04 comparator must not call the compiler/retraction function as its oracle.
- Deferred breadth stays deferred even if the current prototype can parse more types.

## Recommended Next Layer

- Next layer: L1, beginning with the deterministic `SWU-FPR01-001` authority census.
- Evidence consumed: accepted W0 retry receipt with zero current violations and passing positive and negative controls.
- Major deferred scope: owner dispositions, authority promotion, profile freezing, and semantic-engine mutation.

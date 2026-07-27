---
module: ui-prototyping-studio-interface-workbench
version: current
status: draft-pending-plan-distill
updatedAt: 2026-07-27
docType: implementation-layering
---

# Implementation Layering: Interface Workbench Rework

## Target And Scope

- Target: governed local browser workbench
- Scope: brownfield product workflow and validation
- Boundary heuristic:
  `decision unlocked + operator-visible outcome + risk reduced` versus
  `implementation + verification + coordination cost`

## Layer Decision Table

| Layer | Decision question | Minimum working unit | Included | Deferred | Operator-visible outcome | Risk reduced | Exit evidence | Promotion |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | After this layer, we know whether a coherent server projection and stable shell can observe real transitions without reload, stale action state, mixed DOM, or valid-context loss. | deterministic versioner -> coherent snapshot -> versioned `/state` -> inert shell -> trailing refresh -> rollback-capable commit -> context reconciliation | SWU-UPW-001–007; UPW-FIX-001–006 and 015–019 | complete region hierarchy, responsive composition, copy polish, broad hardening | unchanged polls stop disrupting work; real changes apply once or recover | torn reads, null drift, stale action refresh, partial commit, and context destruction | focused unit/E2E receipts plus L0 witness subset | continue to L1 only when L0 evidence passes |
| L1 | After this layer, we know whether the six-region target and mobile order make the current task primary without weakening governance. | one independently accepted region at a time, then responsive order and copy | SWU-UPW-008–015; UPW-FIX-007–010, 013–014, 020 | bounded a11y/security hardening and full closure | lifecycle spine, canvas, inspector, review, actions, and collapsed history follow task order | history dominance, staged/current confusion, copy drift, mobile overflow | region-specific browser receipts and state/copy matrix | continue to L2 only when all six region receipts recompose |
| L2 | After this layer, we know whether bounded keyboard/focus/live-region, sandbox/route, and full regression contracts hold under failure. | one accessibility-semantics SWU, one security SWU, then closure audit | SWU-UPW-016–017 plus TASK-UPW-VERIFY exemption; UPW-FIX-011–012 and 021–024 | human study, cross-browser claims, release/deployment | exact keyboard/focus/status behavior and fail-closed frame/route boundaries | inaccessible action paths, overbroad announcements, unsafe route/frame regression | full `tsc`, unit, Playwright, validator, and governance receipts | route to separate human-study/readiness owner or remediate |
| L3 | After this layer, we know whether separately owned human and broader readiness evidence justifies a later release decision. | no implementation SWU in this work-pack | explicit handoff only after L2 | cross-browser route, human study, accessibility certification, release, deployment | none claimed by this Plan | false promotion from automation to human/release claims | separately owned study and release receipts | outside this work-pack |

## Non-Regression Guardrails

- Current/staged identity, acknowledgment, append-only Revert, and terminal-only
  Export remain exact.
- Later layers preserve zero unchanged navigation, one application per unseen
  version, recoverable commit, and valid-context continuity.
- Browser versions remain opaque; canonical digest authority stays server/test
  owned.
- No layer adds framework, push transport, durable draft authority, remote
  origin, or release scope.

## Recommended Next Layer

- Next layer: `L0`
- First candidate: `SWU-UPW-001`
- Decision unlocked: whether deterministic server-owned projection identity has
  an independently reproducible contract
- Major deferred scope: visual hierarchy, region rollout, human evidence, and
  release
- Selection state: recommendation only; `selected_swu: none`

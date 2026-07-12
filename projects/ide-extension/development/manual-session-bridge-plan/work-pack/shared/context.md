# Planning Context

## Obligation Matrix

| ID | Obligation | Evidence | Coverage |
| --- | --- | --- | --- |
| O-MSB-001 | Manual operator `poll` remains the only agent trigger. | Approved architecture and prior choice. | covered |
| O-MSB-002 | Skill is undisclosed to the session until successful claim. | Architecture constraints and experiment evidence. | covered |
| O-MSB-003 | L0 effects are `skill.invoke` + `preview.read` only. | `DECISIONS.md` DG-MSB-001. | covered |
| O-MSB-004 | Authorization and execution have separate receipts. | DG-MSB-002 and glossary pass. | covered |
| O-MSB-005 | Interrupted claim recovery is operator-only. | DG-MSB-003 and UX plan. | covered |
| O-MSB-006 | Session assurance remains explicitly unattested. | DG-MSB-004. | covered |
| O-MSB-007 | Exactly one desk-selected request is ready for poll. | DG-MSB-005. | covered |
| O-MSB-008 | Existing v1 event history stays replayable and unmodified. | Brownfield projector/storage source plus no-silent-migration rule. | covered by plan decision |
| O-MSB-009 | Actual result returns to kernel evidence before terminal completion. | Architecture result/receipt contracts. | covered |
| O-MSB-010 | Every medium-plan task has executable SWUs and validation. | Invoke plan contract. | covered |

## Selected Context

1. Approved manual-session-bridge architecture, decisions, UX, glossary, and
   layering seed.
2. Formal no-op refresh proving target artifact synchronization.
3. Current `SPEC.md` and `ARCHITECTURE.md` boundaries.
4. Current receipt/envelope/approval/request schemas and explicit schema
   registry.
5. Current `dry-run-envelope.mjs`, grants policy, projector, storage, artifacts,
   and server route implementation.
6. Current Approval Desk HTML, workbench/API tests, hostile/recovery tests, and
   Playwright harness.
7. Existing L0 split-plan conventions and Invoke plan templates.

## Excluded Context

- Browser-first MV3 and MCP/chat implementation details.
- OpenRouter/provider execution.
- VSCodium wrapper/browser-control research.
- OpenClaw, Hermes, Kernel Cloud, Nimbalyst, and external services.
- Whole-session transcripts and generated runtime handoff packs.

## Authority Precedence

1. `DECISIONS.md` controls the five selected product/policy choices.
2. Approved architecture/UX controls state/interface behavior.
3. This work-pack controls implementation sequencing and evidence only.
4. Current source/tests show brownfield behavior but cannot override approved
   design.
5. Task Session owns execution; kernel owns runtime receipts; the operator owns
   ready/recovery actions; Codex owns skill resolution after claim.

## Strict Coverage

- Planning obligations covered: 10/10.
- Missing blocker decisions: none.
- Runtime handoff pack: not generated; Task Session/Context Builder creates it
  for the selected SWU at execution time.

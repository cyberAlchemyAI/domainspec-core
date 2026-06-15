---
module: keystone-lift
version: current
status: draft
updatedAt: 2026-06-14
docType: execution-pack
---

# EXECUTION-PACK: Keystone Lift

Cross-task choreography for medium-complexity execution. Source-of-truth SWU definitions live in [WORK-PACK.md](WORK-PACK.md); this file owns ordering, parallelization, and wave gates.

## Wave order + gates

| Wave | Layer | Tasks | Parallelizable | Entry gate | Exit gate (promotion evidence) |
| --- | --- | --- | --- | --- | --- |
| W0 | L0 | TASK-DEF-LIFT, TASK-TPL-PORT | yes (disjoint write scopes: `definitions/` vs `templates/`) | none | link-checker + definitions-index green; templates render; sanitization grep clean |
| W1 | L1 | TASK-INVOKE-CUTOVER | no | S-001 + S-002 done | `define` dry-run emits DomainSpec SPEC referencing canonical IDs |
| W2 | L2 | TASK-DEFS-REF-PRIVATE, TASK-PROSE-RECOMPOSE, **TASK-AUDIT** | refs+prose parallel; AUDIT last | S-001 + S-003 done | **TASK-AUDIT green (B-KSL-2)** — the gate that unblocks push |
| W3 | L3 | TASK-MF-REMOVE, TASK-VERIFY | no | S-003 + S-005 done | no MF refs; VERIFY PASS; whole-diff audit re-run green |

## Execution-owner routing
- **spellcraft:** TASK-INVOKE-CUTOVER (invoke spell lifecycle).
- **task-session (subagent SWUs):** TASK-DEF-LIFT, TASK-TPL-PORT, TASK-DEFS-REF-PRIVATE, TASK-PROSE-RECOMPOSE.
- **local-fallback:** TASK-MF-REMOVE, SWU-KSL-004/005 (governance text).
- **closure:** TASK-AUDIT, TASK-VERIFY.

## Hard stops (no silent progression)
1. **No push before TASK-AUDIT green** (B-KSL-2). The audit runs on the staged arcanum diff.
2. **No parent gitlink bump before arcanum (and domainspec) commit+push** (B-KSL-3; `make bump-check`).
3. **W2 DS-side edit only after the arcanum side is audited clean** — protects against a half-public moat.
4. Any audit hit or VERIFY BLOCK halts the wave and routes back to the owning task.

## Rollback
All waves are reversible until the W2/W3 push. Rollback = discard the local arcanum/domainspec changes; no published state to revert.

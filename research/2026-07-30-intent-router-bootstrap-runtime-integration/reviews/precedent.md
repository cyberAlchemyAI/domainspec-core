# Precedent and Ownership Review — Lakatos, Imre

dispatch_id: `2026-07-30-intent-router-bootstrap-runtime-integration`  
step_id: `s3`  
capability_ref: `research`  
capability_target: `dispatch-sheet.json`  
capability_mode: `review`  
wave_id: `review`  
write_scope: `[]`  
status: `BLOCK`  
artifacts: `[]`  
validation: `Read-only review of synthesis.md, research.md, receipts/synthesis.json, three explorer receipts, and only synthesis-cited source selectors. No mutation or runtime execution.`  
observer_status: `not-invoked-read-only-review`

blockers:

- The proposed separately persisted, human-owned `selection artifact` and `awaiting-selection` lifecycle are not reconciled with the existing confirmed Dispatch/group/seat and ACI journal owners.
- The proposed capability route catalog lacks a named canonical owner and could become a second capability/route registry.
- The proposed request/disposition/selection persistence is not explicitly subordinate to the existing one-journal ACI authority.

residue:

- `selection-owner-reconciliation`
- `catalog-derived-view-contract`
- `ACI-journal-projection`
- `normalization-owner`

reroute: `Revise the target contract so routing evidence is built into existing owner artifacts and the ACI journal, then repeat precedent/ownership review before implementation.`  
handoff_note: `Installer/generator/wrapper/resolver boundaries pass review. The block is confined to selection, catalog, and persistence ownership; no source implementation is authorized.`

## Exact defects and bounded repairs

1. **Second approval/selection artifact and lifecycle.** The synthesis introduces a new authoritative `selection_id` artifact plus `awaiting-selection` and `awaiting-clarification` states. Yet the actual launch seam already binds an existing `dispatch_id/group_id/seat_index` and authorizes it through `RuntimeService.bind_host_workflow_turn()` (`host_dispatch_hook.py:373-427`). The runtime then owns idempotency, authorization, journal acceptance, persistence, and terminal lifecycle (`service.py:5516-5761`; `009_host_workflow_binding.sql:1-30`). A parallel authoritative selection object or state machine would duplicate approval and lifecycle ownership.

   **Repair:** define selection as a build-from-owned result: the human confirms or authors the existing canonical Dispatch/seat binding through its current owner. The resolver disposition may be cited as non-authorizing input evidence. Do not add `selection_id`, a selection table, or an `awaiting-selection` lifecycle unless ACI explicitly adopts them as fields/states within its one journal.

2. **Second catalog/registry risk.** The resolver specification says the snapshot is compiled by a later owner-owned adapter (`define/SPEC.md:115-129`), while the synthesis leaves catalog authority unnamed and describes a host-supplied catalog snapshot. Without a derivation contract, this can become an independent route registry whose capability identities, modes, exclusions, or dominance rules drift from canonical capability and Dispatch owners.

   **Repair:** require a read-only, digest-bound projection built from explicitly named canonical owners. The adapter may reject or project; it may not repair, enrich, schedule, approve, or independently govern capability identities. Keep the route catalog a frozen derived input, never a new authority ledger.

3. **Persistence wording exceeds the ACI-subordinate decision.** The synthesis says the orchestrator should record immutable request, disposition, and human selection evidence, but does not bind that recording to the existing ACI command/event/artifact journal. The selected architecture explicitly assigns integrated command/event lifecycle, acceptance identity, replay, and effects to ACI (`DECISION.md:33-38,48-55`). Separate resolver persistence would violate that one-writer decision.

   **Repair:** persist resolver request and disposition only as content-addressed ACI artifacts referenced by an existing or ACI-owned command/event. Preserve `authority_effect: none` from `resolve.mjs:172-185`. No resolver database, adapter ledger, or second replay/rollback mechanism.

All other attacked ownership boundaries are acceptable as stated:

- Bootstrap selects canonical sigils; it does not resolve semantics (`bootstrap_arcanum.sh:371-411`).
- Generated wrappers remain projections, not authority (`bootstrap_arcanum.sh:795-821,1028-1033,1215`).
- Python semantic reimplementation and smart adapters are correctly killed.
- Resolver ambiguity and candidate production remain non-authorizing (`resolve.mjs:74-100,137-185`).
- Scheduling, dispatch, approval, effects, and runtime closure remain with existing owners.
- Augmentor remains capture/clarification only (`define/SPEC.md:75-85`).
- Semantic judgment and whole-engine reasoning ownership remain outside the resolver (`agent-reasoning-engine/spec/SPEC.md:127-178,287-302`).
- Public/private copying is correctly prohibited.
- Rollback remains package/version restoration, not a second runtime lifecycle.

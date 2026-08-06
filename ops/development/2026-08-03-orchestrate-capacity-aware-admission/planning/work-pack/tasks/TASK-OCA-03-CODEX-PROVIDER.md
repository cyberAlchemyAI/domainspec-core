---
taskId: TASK-OCA-03
swuId: SWU-OCA-003
status: planned
layer: L1
wave: W3
---

# Codex capacity evidence provider

## Objective and boundary

Bind the neutral capacity contract to what the Codex native host can currently
prove. This SWU is a host-profile capability declaration, not an invented live
provider. Exact evidence may admit only if a named native operation exists;
otherwise the profile returns typed `unsupported` and strict preflight blocks.

Primary behavior: host evidence preserves its real authority ceiling.

Independent acceptance boundary: an inventory-only observation cannot produce
a numeric total, available-unit count, reservation, or release claim.

## Source anchors and future write scope

- add `arcanum/runtime/orchestrate/schemas/capacity-provider-profile.schema.json`
- edit `arcanum/runtime/orchestrate/hosts/codex-native.md`
- edit `arcanum/runtime/orchestrate/SKILL.md`
- add `arcanum/runtime/orchestrate/tests/codex-capacity-provider/codex-provider-fixtures.json`
- add `arcanum/runtime/orchestrate/tests/codex-capacity-provider/test_codex_capacity_provider.py`
- edit `arcanum/runtime/orchestrate/tests/preflight/test_preflight_contract.py`

## Implementation detail

Add a versioned profile object whose provider state is `authoritative` only
when it names an active host operation and field mappings. Otherwise Codex is
declared `unsupported`, with no `spawnable_units`. The preflight maps that
profile state to the existing neutral block. Treat visible agent inventory as
lifecycle observation only. A completed or logically closed entry remains
retained/unknown until the host proves physical release or reuse. Provider
preflight must not spawn, wait, interrupt, or close an agent.

Tests cover the current unsupported profile, a synthetic authoritative profile
with an explicit operation mapping, malformed profile, inventory-only input,
retained completion, and unsupported reservation.

## Done and evidence

- every field maps to a documented host authority or remains absent/unknown;
- no numeric limit is hard-coded or inferred from error text/counts;
- provider/preflight matrix and all L0 regressions pass;
- claim ceiling explicitly distinguishes snapshot from reservation evidence.

Dependency: L0 gate pass. Owner: Codex host-profile owner plus Orchestrate
interface owner. Closeout uses the `SWU-OCA-003` inventory row. An honest
conservative block is acceptable; inventing a provider is not.

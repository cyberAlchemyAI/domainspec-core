# Naming Observer Receipt

Observer agent id: `019ee0d3-0e46-7011-82b9-8901d85e7a55`
Mode: `observe`
Skill frame: `sigil-development`
Governance reference: `arcanum/arcana/discipline-governance/README.md`
Status: `flag`

## Recommendation

- Canonical route id: `local-arena-cli-v0`
- Human label: `Local Arena CLI v0`

## Naming Rules

1. Route IDs name the durable surface, not the first fixture: `[scope]-[surface]-[interface]-[version]`.
2. Target 3-4 dense tokens, around 18-24 characters; 30 characters is the soft ceiling.
3. Put fixture names in fixture and SWU artifacts, not the canonical route id.
4. Use `v0` for the first executable cut; reserve `M0`, `L0`, and `SWU` for layer and work-pack fields.
5. A good route id should survive changing fixture order. If swapping Kuhn/Leduc forces a rename, it is too specific.

## Artifact Recommendations

- Route: `local-arena-cli-v0`
- Route label: `Local Arena CLI v0`
- Route description: first local CLI arena proof with protocol, runner, transcript, replay, diagnostics, sample agents, and toy-fixture gates.
- Work pack: `WP-PAA-001: Local Arena CLI v0 Work Pack`
- Repair SWU: `SWU-PAA-001R: Repair Local Arena CLI v0 Handoff`
- First executable SWU: `SWU-PAA-001: Freeze Local Arena CLI v0 Contract`
- Fixture SWUs: keep fixture-specific names, such as `SWU-PAA-002: Add Kuhn Fixture Gate` and `SWU-PAA-003: Add Leduc Board-Reveal Extension`.
- Spec folders: keep `spec/l0/` as the versioned contract root; put route wording in headings, not folder names.
- Fixture folders: keep game specificity under `fixtures/l0/kuhn_hidden_info/`, `fixtures/l0/leduc_board_reveal/`, `fixtures/l0/invalid_output_matrix/`, `fixtures/l0/timeout_fallback/`, `fixtures/l0/fallback_abuse/`, and `fixtures/l0/leak_canary/`.

## Avoid Or Demote

- Demote `local-kuhn-cli-mvp` from canonical route id to historical review evidence and Kuhn fixture gate language.
- Avoid `kuhn-leduc-cli-mvp` unless the whole first route truly requires both games.
- Avoid `local-engine-cli-v0` for this route because `engine` is reserved for M1 Hold'em engine parity.
- Avoid `mvp` inside repeated artifact ids; use it in prose and result headings.

## Rationale

`sigil-development` separates observer findings from edits and lifecycle claims. This receipt is observation evidence; the parent applies edits separately.

`discipline-governance` favors small, bounded recurring practices. The convention is small enough to reuse: route names describe durable surfaces, fixture names describe proof cases, and dense details stay inside artifact bodies.

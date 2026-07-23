# TASK-WFE-009 — Validate Inventory Projection Conformance

- Change: INT-2 / WFE-R09
- Layer/slice/wave: L2 / S2 / W2
- Lifecycle owner: `sigil-development` for Inventory
- Status: complete; see
  `../session-evidence/SWU-WFE-009/receipt.json`

## Objective

Add a deterministic bidirectional conformance check among governed source entry
files, `index.json`, derived indexes, `index.md`, and enabled projections, and
make lookup report the current validator result.

## Sources

- `arcanum/arcana/inventory/SKILL.md`: synchronized indexes, lint, machine view,
  projection policy, lookup output
- `arcanum/arcana/inventory/scripts/validate-index-json.sh`: current partial checks
- `.arcanum/inventory/`: live source/index/human/projection layout after INT-1
- accepted findings INT-2

## SWU-WFE-009

- Primary behavior: emit one projection-conformance verdict with independent
  source coverage, identity, existence, derived-map, human-view, and freshness
  subresults.
- Acceptance boundary: missing source row, orphan machine row, missing path,
  stale digest/timestamp, by-id mismatch, and human/machine identity mismatch
  fail; a current complete fixture passes; historical uncontrolled tags warn
  unless a closed vocabulary is separately governed.
- Split analysis: subchecks are independently reported but jointly determine one
  downstream readiness claim; partial pass cannot authorize lookup-ready output.

## Algorithm

1. Enumerate governed entry sources under configured Inventory roots.
2. Compare stable IDs and paths in both directions with `index.json`.
3. Verify every indexed path exists and every required derived index references
   only current IDs with exact identity.
4. Parse the human index links and compare ID/path/type/status where represented.
5. For each enabled projection, require source=`index.json`, declared purpose,
   and digest/freshness equal to the current primary index.
6. Emit structured subresults and overall pass/fail; lookup packets carry this
   result and never substitute parseability.

## Scope and validation

- Generic validator/fixtures: canonical Inventory lifecycle source under
  `arcanum/arcana/inventory/`.
- Live package proves integration under `.arcanum/inventory/`.
- Generated runtime docs synchronize only if canonical contract text changes.

```bash
bash arcanum/arcana/inventory/scripts/validate-index-json.sh .arcanum/inventory/index.json
bash arcanum/arcana/inventory/development/run-projection-validation-fixtures.sh
git diff --check -- arcanum/arcana/inventory .arcanum/inventory .agents/skills/inventory .claude/skills/inventory
```

The projection harness does not exist yet; creating that exact focused harness
and proving each red/green fixture is part of this SWU. Its pre-SWU absence is
planned output, not evidence that a prose-only review is sufficient.

- Dependencies: SWU-WFE-004B and TASK-WFE-008 program-order receipt.
- Execution owner: `sigil-development`.
- Receipt: fixture matrix, live conformance report, lookup packet with validator
  status, tag-warning boundary.

## Done

The primary machine index and all enabled read models agree bidirectionally, or
lookup reports a blocking validation result instead of weaker parseability.

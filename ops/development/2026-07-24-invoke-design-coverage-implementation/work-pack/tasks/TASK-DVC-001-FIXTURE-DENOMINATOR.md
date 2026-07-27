# TASK-DVC-001: Freeze Fixture Denominator

- Slice/layer/wave: S0 / L0 / W0.
- Source: `../../../DESIGN.md`, accepted research `Validator and
  frozen-fixture requirements`.
- Dependencies: dispatch validation only.
- Gap owned: DVC-G07.

## Objective

Create the implementation-independent corpus that fixes inputs, source trace,
exact expected concern dispositions, selected outputs, evidence states, and
diagnostic codes before schemas or algorithms exist.

## SWU-DVC-001

- Primary behavior: freeze one complete fixture-denominator contract.
- Independent acceptance: the corpus parses, all IDs are unique, every case
  names exact expectations, and a stable corpus digest is emitted.
- Candidate child units: positive cases; negative cases; mutation cases;
  expected outputs; digest.
- Retained boundary: no subset constrains implementation without the complete
  case-to-expectation mapping and source trace.
- Write scope:
  `arcanum/spells/invoke/development/fixtures/design-selection/`.
- Execution owner: local fallback under Spellcraft.

## Required cases

Positive/bounded:

- pure local function;
- static deterministic artifact;
- semantics-preserving style token;
- backend protocol with no human effect;
- ordinary authenticated CRUD;
- operator governed-state workflow;
- lifecycle/admission system;
- stored-version conversion.

Negative:

- omitted queue, store, external API, log sink, second writer, and
  operator-visible evidence;
- changed focus, reflow, and accessible name;
- false “no durable data,” stale denominator, fabricated/self-issued receipt,
  N/A without extraction, unbound signal, changed pass two, missing owner, and
  planned fixture mislabeled as executed.

Mutation matrix:

- invert every required predicate;
- drop every manifest field class once;
- replace each owner with null/self;
- alter one digest after receipt creation;
- alter one pass-two output;
- promote one `recommended` output to selected.

## Ordered implementation

1. Copy no implementation code or private witness text.
2. Assign stable fixture and signal IDs.
3. Bind each case to accepted research selectors.
4. State exact input shape and expected primary concern.
5. State exact four-state disposition and selected output set.
6. State exact diagnostic code for every block.
7. Mark expected evidence state.
8. Canonically sort records and compute the corpus SHA-256.
9. Emit a source-trace file and denominator receipt.

## Validation

```bash
python3 -m json.tool arcanum/spells/invoke/development/fixtures/design-selection/fixture-matrix.json
jq -e '(.cases | length) >= 24 and ([.cases[].fixture_id] | unique | length) == (.cases | length)' arcanum/spells/invoke/development/fixtures/design-selection/fixture-matrix.json
git diff --check -- arcanum/spells/invoke/development/fixtures/design-selection
```

## Failure modes

- missing expected selection or diagnostic;
- expected N/A without a negative signal;
- fixture copied from private project evidence;
- expectation changed after implementation begins;
- path overlaps an existing unreviewed fixture.

## Done and closeout

Done when Spellcraft returns the corpus path, digest, source trace, commands,
and zero unresolved expectation gaps. Synchronize only the DVC-001 targets in
`../shared/CLOSEOUT-CONTRACT.md`.

## Completion evidence

- Result: pass.
- Corpus: 28 frozen cases and 27 predicate/field mutations.
- Digest:
  `347618abe9ae700fb515a127d4d5a75a78665013dbc68fd637bd5bd7200a5c74`.
- Receipt: `../session-evidence/SWU-DVC-001/execution-receipt.json`.
- Successor: `SWU-DVC-002A`.

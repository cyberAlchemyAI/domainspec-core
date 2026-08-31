---
module: invoke-preacceptance-governance-defect
version: draft-2
status: proposal-only
updatedAt: 2026-08-26
docType: execution-pack
---

# Execution Pack: Invoke Preacceptance Governance Defect

## Execution Boundary

This is an ordered implementation design for Spellcraft. It is not an admitted run.
No wave may begin until the preceding gate passes on exact current bytes.

## Wave Plan

| Wave | Layer | Units | Question answered | Promotion evidence | Parallel policy |
| --- | --- | --- | --- | --- | --- |
| W0 — baseline and contract freeze | pre-L0 | no product SWU | Which current bytes are owned, and which exact versioned state/content/stage contract is accepted? | Scoped dirty-byte inventory, complete state/mode/verdict/handoff consumer inventory, compatibility matrix, accepted token/version decision, exact candidate write scope. | Read-only checks may run together; no mutation. |
| W1 — staged candidate | L0 | SWU-IGD-001 | Can nonempty staged bytes validate without apply authority? | Material fixtures and all downstream no-collapse controls pass. | Serial; schema, producer, receipt, and consumer semantics share one invariant. |
| W2 — content and effect | L1 | SWU-IGD-002, SWU-IGD-003 | Can declared structured/text formats and the exact owner effect be validated? | JSON/Markdown/YAML-file positive fixture and content/effect negatives pass. | Logically independent but serialize in one worktree because both touch preacceptance schema/tests. |
| W3 — truthful closure | L2 | SWU-IGD-004, SWU-IGD-005 | Are all reachable results collected, and did the exact candidate cross the real consumer? | Dependency-aware receipt set, first-nonzero status, actual material receipt, anti-help/anti-adapter negatives. | SWU-IGD-004 first; SWU-IGD-005 consumes its stage result contract. |
| W4 — canonical lifecycle closure | L3 | SWU-IGD-006 | Does the canonical repair compose through request emission? | Full synthetic lifecycle runs twice byte-stably; complete canonical suite passes; independent review binds canonical bytes. | Verification-only; no generated mutation. |
| W5 — generated packaging | L3 | SWU-IGD-007 | Do installed generated runtimes project the verified canonical repair? | Canonical sync changes only accepted generated targets; generated validation and parity pass. | Serial material packaging after W4. |

## Implementation Detail

### SWU-IGD-001 — Candidate state and authority semantics

- Inputs: current material package/receipt schemas, validator, handoff consumer,
  fixture corpus, accepted three-row state table.
- Output: candidate-staged packages validate exact material but emit the W0-accepted
  distinct non-authorizing outcome and never mutation readiness.
- Ordered rules:
  1. Validate structure and all exact references before interpreting authority.
  2. Derive one of the three allowed rows from the W0-accepted, versioned mode/state
     contract and approval class.
  3. For staged candidate, require nonempty sources, changes, target inventory, and
     validation commands; require `approval.class=none` and empty approval scope.
  4. Run dependency, owner, publication, mirror, and exact-output validation.
  5. Emit exact digest/paths with the accepted review-required/gated handoff.
  6. For apply-authorized material, retain exact approval-scope equality and ready
     handoff.
- Failure modes: invalid row, candidate with approval, empty candidate, scope escape,
  stale output, unknown token treated as approved, or a consumer using one field
  alone.
- Verification: material-package fixture suite plus refresh-handoff no-collapse
  cases.

### SWU-IGD-002 — Typed postimage assertions

- Inputs: final-postimage manifest entries and exact postimage bytes.
- Output: one explicitly typed JSON or UTF-8 text document plus compatible
  assertions; YAML files use the text route unless a structural parser contract is
  separately accepted.
- Ordered rules:
  1. Validate exact ref digest/size.
  2. Select parser only from `content_kind`; never from path extension.
  3. Decode JSON or UTF-8 text under the declared contract. If structural YAML is
     selected, require the pinned safe parser/version and admitted JSON-compatible
     subset; dependency absence is a blocker.
  4. Dispatch only compatible structured or literal assertion operators.
  5. Apply text hygiene only to declared textual kinds.
  6. Report an exact target/assertion blocker without dropping other reachable
     checks.
- Failure modes: unknown type, invalid UTF-8, invalid JSON,
  selector/operator mismatch, failed assertion, or an unowned/unpinned YAML parser.
- Verification: JSON plus Markdown/YAML-file-as-text fixture and per-kind negatives;
  structural YAML fixtures only when that optional contract is selected.

### SWU-IGD-003 — Requested-effect equality

- Inputs: schema-valid manifest requested effect and base request.
- Output: request only when both effect objects are structurally and canonically
  identical.
- Ordered rules:
  1. Require `base_request.requested_effect`.
  2. Compare exact object equality.
  3. Compare the canonical digest used by eligibility.
  4. Emit only after both checks and all existing closure/review/adoption gates pass.
  5. Re-run the same canonical emitter during `validate-request`.
- Failure modes: missing effect, different owner/target/effect ceiling, reordered
  non-canonical set-like arrays, eligibility matching manifest while base differs.
- Verification: positive equality plus each mismatch class.

### SWU-IGD-004 — Reachable blocker collection

- Inputs: an ordered stage list with explicit `depends_on_stage_ids`.
- Output: one result per declared stage: `pass`, `block`, or `not_evaluable`, plus
  the exact first nonzero process status in the receipt and versioned CLI contract.
- Ordered rules:
  1. Validate acyclic dependencies and that they point only to earlier stages.
  2. Run every stage whose dependencies passed.
  3. Mark a dependent stage `not_evaluable` with causal blocker IDs when any
     dependency blocks or is not evaluable.
  4. Continue independent reachable stages after failures.
  5. Preserve the first nonzero exit status in the receipt and return it from the
     versioned preacceptance CLI; W0 inventories callers before changing this public
     exit-code contract.
  6. Never let cleanup or later success replace that status.
- Failure modes: cycle, unknown dependency, omitted stage, false PASS after upstream
  failure, first failure masked, ordinary early break.
- Verification: two independent failures plus a dependent chain in one run.

### SWU-IGD-005 — Actual candidate-bound consumer

- Inputs: exact material-package ref/root, final-postimage set, material schemas, and
  isolated rehearsal root.
- Output: schema-valid material receipt bound to the exact package digest and staged
  outputs.
- Ordered rules:
  1. Bind the exact package ref into the closure graph.
  2. Invoke the real validator with the real package/root/schema arguments and an
     isolated receipt output.
  3. Validate the receipt schema and package digest.
  4. Require the exact W0-accepted non-authorizing candidate outcome.
  5. Require package target inventory to equal final-postimage targets and each
     output ref to equal its final postimage ref.
  6. Require `create -> create + absent baseline` and
     `update -> replace + present baseline`.
  7. When `plan_binding.target_baselines` exists, require exact path/state/digest/size
     equality with final-postimage baselines.
  8. Include the output receipt in deterministic run evidence.
- Failure modes: `--help`, wrong valid package, target/ref mismatch, create/present or
  update/absent contradiction, plan-baseline drift, stale package, zero exit without
  receipt, invalid receipt, write outside rehearsal root.
- Verification: actual consumer positive and all anti-adapter negatives.

### SWU-IGD-006 — Canonical lifecycle closure

- Inputs: final canonical candidate from all prior units.
- Output: synthetic full-chain evidence, complete canonical validator results, and
  an independent repair review.
- Ordered rules:
  1. Run the material and preacceptance fixture suites.
  2. Run the complete Invoke validation suite.
  3. Run the synthetic no-effect lifecycle twice and compare bytes.
  4. Run the existing Task Session live-entry fixture through its declared validation
     wrapper against the v3 owner-request graph; changes are limited to test setup and
     wrapper reachability, not runtime behavior.
  5. Run the independently reachable requested-effect regression against the v3
     base-request, manifest, digest, and canonical-replay binding.
  6. Run scoped content/whitespace checks over tracked and create canonical targets.
  7. Freeze exact canonical candidate inventory and obtain independent review.
- Failure modes: masked command status, untracked target omitted, private fixture
  leak, or a project-specific readiness overclaim.

### SWU-IGD-007 — Generated runtime packaging and parity

- Inputs: independently reviewed canonical Invoke repair and exact generated-target
  inventory.
- Output: generated Codex/Claude Invoke packages that are exact projections of the
  accepted canonical source.
- Ordered rules:
  1. Use only the canonical spell sync tool; never edit generated files directly.
  2. Inspect the changed-byte inventory and reject unrelated generated changes.
  3. Re-run material, preacceptance, and complete Invoke validation through generated
     runtime surfaces.
  4. Prove byte parity with canonical projections.
  5. Regenerate any project closure graph/request against the new executable refs.
- Failure modes: parity drift, unrelated generated replacement, direct generated
  edit, old graph reused, or project-specific readiness overclaim.

## Validation Commands For The Future Candidate

These commands are planned validation surfaces; they were not run by this planning
turn:

```text
python3 arcanum/spells/invoke/development/run_material_package_fixtures.py --canonical-only
bash arcanum/spells/invoke/development/run-preacceptance-closure-fixtures.sh
INVOKE_VALIDATION_SCOPE=canonical-only bash arcanum/spells/invoke/development/run-validation-fixtures.sh

# After exact authorization and generated sync:
bash arcanum/spells/invoke/development/run-validation-fixtures.sh
```

Before accepting repaired bytes, Spellcraft must also run scoped whitespace/content
checks that explicitly include every untracked/create target, and it must preserve the
first failed command status across the complete validation wrapper.

## Stop Conditions

Stop before the next mutation or effect when:

- current dirty bytes cannot be attributed or safely isolated;
- the state/content/dependency contract requires an owner choice;
- any fixture or actual-consumer rehearsal fails;
- an output path, approval scope, authority class, or public/private boundary expands;
- a generated surface differs from canonical output;
- credentials, external network, publication, Git, deployment, privacy, or product
  semantics enter scope;
- an old closure graph, review, acceptance, or request would be reused after an
  authority-bearing executable changed.

## Closeout

W5 may close only with a fresh exact candidate inventory, passing independent review,
generated parity, and a Spellcraft lifecycle receipt. It may then hand a separately accepted repair to
the Body War continuation owner for a new preacceptance rehearsal. It may not auto-
resume the old Body War chain.

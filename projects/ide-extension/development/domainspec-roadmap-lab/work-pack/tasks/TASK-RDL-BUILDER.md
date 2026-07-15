# Task Contract: Roadmap Builder And Bindings

## Control

| Field | Value |
| --- | --- |
| Task ID | `TASK-RDL-BUILDER` |
| Objective | Externalize presentation copy and generate deterministic, reviewable build bindings. |
| Layer / slice / wave | L0 / S-002 / W1 |
| Dependencies | SWU-RDL-001 and SWU-RDL-002 pass |
| Blockers | Existing untracked visibility artifacts require ownership-preserving diff review. |
| Execution | Completed: SWU-003 and SWU-004 passed. |

## Sources

- [RDL-O01 build flow](../../ARCHITECTURE-BUNDLE.md#rdl-o01-build-and-publish-learning-surface)
- [Implementation fingerprint algorithm](../../IMPLEMENTATION-PLAN.md#deterministic-fingerprint)
- `visibility/tools/build-roadmap.py`, `roadmap.template.html`,
  `test_build_roadmap.py`, current generated `roadmap-data.json`/`roadmap.html`.

## SWU-RDL-003 — Extract presentation copy and coverage

- **Objective:** Move human mappings out of executable template code into the
  stable copy contract without changing roadmap authority.
- **Dependencies:** SWU-RDL-001.
- **Write scope:** `visibility/roadmap-copy.json`, builder, template, builder/
  contract tests, and regenerated roadmap outputs. No roadmap manifest or Craft
  ledger mutation.
- **Rules:** preserve current wording initially; key every migrated node,
  frontier, critical step, heading, and explanatory field; reject missing/
  duplicate/unused required fields; eliminate migrated literal fallback from
  template JavaScript; retain generated-output determinism.
- **Edge cases:** optional versus required copy, unknown current node, newline/
  HTML escaping, duplicate roles, dead copy entries, exact source wording that
  must remain authority rather than copy.
- **Done:** current rendered semantics remain equivalent, required human copy is
  wholly data-driven, and coverage failures are actionable.
- **Acceptance evidence:** old/new mapping inventory, coverage report, generated
  diff explanation, and builder suite output.
- **Validation:**
  `python3 -m unittest discover -s projects/domainspec-v2/development/first-production-release/visibility/tests -p 'test_build_roadmap.py'`.
- **Owner:** `local-fallback`.
- **Handoff:** identify the stable FPR-01 field IDs for SWU-RDL-005.
- **Result:** [PASS](../../task-sessions/20260714T221718Z-swu-rdl-003/TASK-SESSION-RESULT.md) —
  67 presentation-only fields externalized to `roadmap-copy.json`, builder
  coverage rejects missing/duplicate/unknown/unused copy, migrated template
  fallbacks removed, outputs regenerated through the builder, and the full
  visibility suite passed.

## SWU-RDL-004 — Fingerprint and projection manifest

- **Objective:** Make every proposal traceable to deterministic build inputs and
  rendered targets.
- **Dependencies:** SWU-RDL-002 and SWU-RDL-003.
- **Write scope:** visibility builder/template/build metadata tests and
  regenerated outputs only.
- **Rules:** hash a version-tagged normalized input manifest; include roadmap,
  copy, and source-ref digests; embed fingerprint, schema versions, rendered
  node/field IDs, and source refs; exclude absolute paths and timestamps from
  deterministic output; prove each declared input mutation changes fingerprint.
- **Edge cases:** key reordering, line endings, unused copy, source-order changes,
  missing file, same logical JSON bytes, generated output used as input.
- **Done:** two unchanged builds are byte-identical; material input changes alter
  the fingerprint; every FPR-01 field/source can be resolved from embedded data.
- **Acceptance evidence:** build digests, mutation table, no-absolute-path scan,
  generated artifact check.
- **Validation:** full visibility unittest suite; builder `--check` if provided;
  run generation twice and compare SHA-256.
- **Owner:** `local-fallback`.
- **Handoff:** provide fingerprint version and embedded manifest selectors to
  SWU-RDL-005.
- **Result:** [PASS](../../task-sessions/20260714T222610Z-swu-rdl-004/TASK-SESSION-RESULT.md) —
  `roadmap-build-inputs.v1` embeds relative input digests, rendered node/source/
  copy-field selectors, FPR-01 field ids, material mutation proof, deterministic
  double-build hashes, and no absolute or temp paths.

## Synchronization And Completion

Do not hand-edit generated `roadmap-data.json` or `roadmap.html`. Regenerate only
through the builder and report their diffs separately from source changes.

Task complete. Later SWUs may consume the generated fingerprint and selectors,
but changes to the build-input manifest version or copy-field contract require
impact review across guided UI, history, and review-packet adapters.

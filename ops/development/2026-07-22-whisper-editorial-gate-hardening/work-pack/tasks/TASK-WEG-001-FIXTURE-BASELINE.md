# TASK-WEG-001 — Fixture Baseline

## Objective and mapping

- Layer/slice/wave: L0 / S0 / W0.
- Decision: make the known false-positive shapes executable before changing Whisper behavior.
- Dependency: none.
- Blockers: none.

## Implementation detail

Create a public-safe Experiment Harness definition and a fixture corpus under the canonical Whisper development tree. Include:

- green: proven transport, frozen intent, exact editorial/comprehension/post-apply evidence;
- red: candidate requests `pass`;
- red: structural and render axes pass while comprehension is absent;
- red: volatile intent requests a full derivative;
- red: approval names a different surface digest;
- red: ambient approval lacks `approval_kind`;
- red: retell is rendered without replacement/distinct-job accounting;
- red: post-apply review references the pre-apply digest.

Record the current baseline honestly: where no run-receipt evaluator exists, mark the expected gate as `not-enforced`, not as a passing or failing implementation result.

## Smallest Working Unit: SWU-WEG-001

- Primary behavior: fixtures encode expected outcomes without changing canonical runtime behavior.
- Independent acceptance boundary: the corpus parses, pairs each red case with an expected reason, includes at least one green control, and contains no private project language.
- Split analysis: red cases, green controls, and baseline record were considered separately; without all three the experiment cannot distinguish causal rejection from a broken harness.
- Source anchors: `../../DEFINE.md#required-outcomes`, `../../DESIGN.md#view-5-decision-flow`, canonical Whisper `README.md` candidate/intent/audition sections.
- Related context: `../shared/context.md`, `../shared/traceability.md`.
- Write scope: `arcanum/spells/whisper/development/VALIDATION-EXPERIMENT.md`, `arcanum/spells/whisper/development/fixtures/editorial-admission/**`, `arcanum/spells/whisper/development/editorial-admission-baseline.json`.
- Done criteria: all cases have stable IDs, generic text, expected verdict/reason, and regime tags; baseline distinguishes absent enforcement from incorrect enforcement.
- Acceptance evidence: parsed corpus inventory plus privacy sweep result.
- Verification:

```bash
find arcanum/spells/whisper/development/fixtures/editorial-admission -type f -print
python3 -m json.tool arcanum/spells/whisper/development/editorial-admission-baseline.json >/dev/null
rg -n "UnlockDoor|DoorUnlocked|BTE|DomainSpec v2" arcanum/spells/whisper/development/VALIDATION-EXPERIMENT.md arcanum/spells/whisper/development/fixtures/editorial-admission
```

- Execution owner: `local-fallback` through Task Session under Spellcraft.
- Handoff note: do not edit `README.md`, schemas, or validators in this SWU; a non-empty privacy sweep blocks.

## Synchronization

Return the fixture list and baseline receipt, then update WORK-PACK state only after acceptance. W0 remains on SWU-WEG-001 until this receipt passes.

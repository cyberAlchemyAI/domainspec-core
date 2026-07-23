# TASK-WEG-006 — Candidate Technical Explainer First Surface

## Objective and mapping

- Layer/slice/wave: L1 / S1 / W1.
- Decision: give newcomer technical explainers a complete source-ordered audition surface that teaches the human situation before machine detail.
- Dependencies: SWU-WEG-003 and SWU-WEG-004.
- Blockers: none.

## Inputs and outputs

- Inputs: generic transport profile schema, composed artifact selectors, audience mode.
- Outputs: candidate `interactive_technical_explainer` preset/profile, surface manifest contract, complete/incomplete fixtures.
- State touched: transport metadata only; no promotion state.

## Rules

1. Profile proof status is `candidate` and cannot be locally raised.
2. A newcomer first surface includes roles in reading order: context, heading, human situation, present capability, missing capability, human limit.
3. Machine terms may follow the human situation; the contract does not impose a global forbidden-word list.
4. A phrase sample cannot satisfy first-surface completeness.
5. Source-order claims remain distinct from browser viewport claims.
6. Comprehension question IDs map to situation, present capability, missing capability, and human decision.

Failure modes: a profile that embeds BTE names or private paths blocks; a profile that calls itself proven blocks; a manifest missing required roles flags/blocks according to the transport gate.

## Smallest Working Unit: SWU-WEG-006

- Primary behavior: validate role-complete first-surface manifests for one candidate transport.
- Independent acceptance boundary: complete generic manifest passes profile validation; incomplete/isolated/private/promotion controls fail; final status remains capped at flag.
- Split analysis: profile, roles, and fixtures were considered separately; the transport contract cannot be trialed without all three, while composition/render implementation is explicitly excluded.
- Source anchors: `../../DESIGN.md#31-transport-profile-extension`, `#32-surface-manifest`, July 22 reflection ordinary-language first screen.
- Related context: SWU-WEG-003 ceiling and SWU-WEG-004 binding.
- Write scope: `arcanum/spells/whisper/presets/interactive-technical-explainer/**`, generic surface schema additions, profile fixture subtree, canonical Whisper transport table/gates.
- Done criteria: public generic profile and examples exist, private sweep is empty, and all completeness/status tests match expectations.
- Acceptance evidence: profile validation report and candidate-all-gates result `flag`.
- Verification:

```bash
python3 arcanum/spells/whisper/tools/validate-whisper-run-receipt.py --fixtures arcanum/spells/whisper/development/fixtures/editorial-admission/first-surface
rg -n "UnlockDoor|DoorUnlocked|BTE|DomainSpec v2" arcanum/spells/whisper/presets/interactive-technical-explainer arcanum/spells/whisper/development/fixtures/editorial-admission/first-surface
```

- Execution owner: `local-fallback` through Task Session under Spellcraft.
- Handoff note: keep the profile generic and record transport-specific private residue outside `arcanum/`.

## Synchronization

Do not regenerate `.agents/skills/whisper` yet. Add the profile paths to the eventual SWU-WEG-009 drift scope.

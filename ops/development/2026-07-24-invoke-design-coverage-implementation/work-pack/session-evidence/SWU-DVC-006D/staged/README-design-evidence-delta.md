# SWU-DVC-006D Staged Delta

- Target: `arcanum/spells/invoke/README.md`
- Required preimage SHA-256:
  `e0875ff2c5e4b1922e34ec9a80d4007d7a21e579dffcf1b17d7234dd9b49f991`
- Preserve every existing byte except the anchored additions and one Design
  mode status replacement below.

## Replacement

Replace `implemented (L1 contract)` with
`implemented (L1 contract with deterministic selection validation)` and
replace the note claiming that validation examples still gate promotion with a
note that names the closed manifest, denominator, total two-pass selection,
and separate Plan evidence.

## Anchored additions

Add the following public contract concepts to their matching root sections:

- evidence capability: Design selection does not collapse authored, registry,
  runtime, or Plan evidence;
- shared state: `DesignScopeManifest`, `DesignDenominatorReceipt`, and
  `DesignSelectionResult`;
- global handoff: Design selection receipt, Design evidence state and ceiling,
  exact target gaps, and explicit Spellcraft handoff when the target is a
  spell;
- global gates: normal Plan requires `design-validator-pass`; authored-only
  remediation is bounded; planned witnesses remain `plan-evidence-pending`;
- observability and root output: report Design selection receipt, Design
  evidence state, Design evidence ceiling, and Plan evidence separately.

No other README content may change.

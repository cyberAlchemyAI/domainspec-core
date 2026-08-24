# Dispatch Spec validation

- Dispatch: `DISPATCH.json`
- Validator: `.agents/skills/dispatch-spec/scripts/validate-dispatch.py`
- Initial result: `flag`; the live canonical `decision-gate` package was absent
  from the validator's static canonical capability allowlist.
- Repair: add explicit step metadata pointing to
  `arcanum/arcana/decision-gate/SKILL.md` and classify it as a validated local
  allowlist extension. No route semantics changed.
- Final result: `pass`
- Blocks: none
- Flags: none

This proves the three-step owner-gate route shape only. It does not execute the
dispatch or authorize L1.


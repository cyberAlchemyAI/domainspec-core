# Stage 07 — Interrogation (refine-design-review)
Capability: `interrogation` · Mode: `refine-design-review` · Status: **pass**
Roles: design-advocate, risk-reviewer, repair-synthesizer

## Design-advocate
Schema is self-contained and runnable; reuses dispatch `$def` shapes; encodes all six discipline checks as either shape constraints (now) or named governance rules (deferred). The fixture set exercises both layers.

## Risk-reviewer
1. **Self-contained `gate_action` vs `$ref` to dispatch** — inlining avoids an unresolvable cross-file `$ref` in a run-folder candidate; parity with dispatch `gate_action` enum preserved. Acceptable; the eventual package can switch to `$ref`.
2. **`not.required[status]`** — catches collapsed-status cheaply at shape layer (verified by v-collapsed-status). Good.
3. **Governance layer unbuilt** — three violations (no-rollback, self-promoting-gate, status-floor) pass shape; the design must NOT claim them caught. README marks them "needs script". Honest.
4. **Ladder/enum still candidate** — `status_class: const candidate` + README guardrail prevent overclaiming. Holds.
5. **Owner boundary** — all writes in run folder; submodule contents untouched. Holds.

## Repair-synthesizer (residue)
- Repair check for Stage 08: run jsonschema, confirm spine-pass passes + all 6 shape violations fail + 3 governance ones pass shape.
- Residue: governance validator deferred; ladder transition rules unproven.

## Verdict
`pass` — no design risk blocks the candidate; falsification check routed to s08.

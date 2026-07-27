# Invoke Refresh Report — Deterministic Chain Contract

- Result: `PASS`
- Mode: `refresh:apply-approved`
- Package:
  `ups-gsp-chain-contract-refresh-apply-20260727`
- Package digest:
  `2b2bda949bd409c58f1aa54cd0b64e180f5c922e378ac6e95b69139ba28e4889`
- Targets: 15
- Exact live/staged parity: 15/15
- Material patch verdict: `pass`
- Mutation handoff: `ready`
- Chain validator: `pass`
- Craft YAML/index validation: `pass`
- Diff hygiene: `pass`

The refresh serializes the seven already-approved SWUs and adds exact Task
Session/Invoke closeout contracts. It changes no application source and
produces no implementation, human-study, release, promotion, or publication
claim.

Next route: `task-session-until-blocker` beginning at `SWU-GSP-001`.

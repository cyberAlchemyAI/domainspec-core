# Run Manifest — 2026-06-08-lean-functor-validation

- Owner: refine
- Target: DomainSpec Language design ↔ lean-code-validator bridge
- Preset: deep
- Research mode: bounded-research (pending operator confirmation)
- Subagent strategy: required (pending operator authorization)
- Dispatch: `REFINE-DISPATCH.json` — validated against `formulae/dispatch-spec/dispatch.schema.yml` (10 steps, 8 gates, shape conforms)
- Status: **awaiting operator permission** (pre-execution; no stages run, no subagents spawned)

## Artifacts owned by refine

- `REFINE-SEED-PROPOSAL.md` — written
- `REFINE-DISPATCH.json` — written + validated
- `RUN-MANIFEST.md` — this file
- `evidence-index.json` — written
- `RUNTIME-HANDOFF.md` — deferred until permission granted
- `RESULT.md` — deferred until after final synthesis

## Canonical stage ledger

| #   | Stage                           | Capability      | Status  | Artifact / blocked reason             |
| --- | ------------------------------- | --------------- | ------- | ------------------------------------- |
| s1  | Context Builder baseline        | context-builder | not_run | pending permission                    |
| s2  | Invoke Define                   | invoke          | not_run | pending permission                    |
| s3  | Interrogation refine-review     | interrogation   | not_run | pending permission                    |
| s4  | Research decision (bounded)     | refine          | not_run | pending permission + research confirm |
| s5  | Distill (model tournament)      | distill         | not_run | pending permission                    |
| s6  | Invoke Redefine/Design          | invoke          | not_run | pending permission                    |
| s7  | Interrogation design-review     | interrogation   | not_run | pending permission                    |
| s8  | Distill Repair (toy-game)       | distill         | not_run | pending permission                    |
| s9  | Invoke Plan                     | invoke          | not_run | pending permission                    |
| s10 | Final Interrogation + synthesis | interrogation   | not_run | pending permission                    |

## Subagent ledger (pending)

| role_id                 | status      | receipt |
| ----------------------- | ----------- | ------- |
| lean-validator-xray     | not spawned | —       |
| categorical-formalizer  | not spawned | —       |
| translator-designer     | not spawned | —       |
| spec-correctness-prover | not spawned | —       |
| residue-skeptic         | not spawned | —       |

# Stage 08 — Distill Repair (validate)

Capability: `distill` · Mode: `validate` · Overlay carry: `validation_loop` · Status: **pass**

## Repair acceptance test (toy-game / controlled validation)

The repair is only "done" if the *promoted* artifact — not merely the run-folder candidate — passes the validator, and the diff stays surgical. Acceptance checks:

| Check | Method | Result |
| --- | --- | --- |
| T1 — candidate validates | `validate-dispatch.py` on run-folder repaired JSON | `VALIDATION=pass` ✓ |
| T2 — surgical diff | semantic diff vs original | "everything-else identical: True" ✓ |
| T3 — receipt reqs additive | count 5 → 21, originals retained | ✓ |
| T4 — 4 capability handles labeled | `capability_status=local-extension` + provenance | ✓ |
| T5 — promoted file validates in place | run `validate-dispatch.py` on canonical path after promotion (Stage 09) | deferred to s09 gate |
| T6 — self-test command runnable | the `.md` command path exists in checkout | ✓ (path `.claude/skills/dispatch-spec/scripts/validate-dispatch.py`) |

## Failure-routing

If T5 fails after promotion, route back: revert the canonical file (git), re-open Stage 06 design. No silent fallback.

## Residue carried forward

- B-opt MVP-first ordering: unforced recommendation for the handoff.
- `arcanum/` submodule empty: local gap; owner = fan-out executor; resolution = `git submodule update --init arcanum`.

## Verdict

`pass` — T1–T4, T6 satisfied; T5 is the promotion gate executed in Stage 09. Repair is ready to promote.

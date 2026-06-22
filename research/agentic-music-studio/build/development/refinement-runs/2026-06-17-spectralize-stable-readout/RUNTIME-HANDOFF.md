# RUNTIME-HANDOFF — 2026-06-17-spectralize-stable-readout

- **Runtime objective:** run the bounded-research tournament + synthesize a Spectralize-v2 direction.
- **Validated dispatch:** `REFINE-DISPATCH.json` (validated, status pass).
- **Strategy permission:** operator-confirmed ("run all refine") — covers delegated subagent execution.
- **Adapter:** native (parent coordinator) + 5 native research subagents via the Agent tool.
- **Run folder:** this directory. **Authorization:** granted. **Status:** complete.
- **Blocked fields:** none.

## Handoff out
- Owner decision required before build: "is a fixed psychoacoustic model model-free?" (F4 vs F3 roughness).
- Next route: `invoke design` (Spectralize-v2, carry `RESULT.md`) → `task-session` → re-run `experiments/o8_spectralize_stability.py` on v2 → if PASS, unblock O1 via `research-evidence-harness`.

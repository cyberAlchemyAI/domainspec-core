# Runtime Handoff — autoads-seed-20260610

- **Runtime objective:** Execute the validated canonical refine loop to produce the autoads seed
  (DEFINE, DESIGN, PLAN) grounded in the ontologize ontology+DAG loop.
- **Validated dispatch:** `REFINE-DISPATCH.json` — `dispatch-spec` VALIDATION=`pass`.
- **Strategy permission state:** `approved` (operator confirmed preset=full, research=research-if-gap-appears,
  subagents=all 4).
- **Adapter:** native parent runtime (Claude Code skills) + role-bound subagents via the Agent tool.
- **Run folder:** `projects/autoads/development/refinement-runs/autoads-seed-20260610/`
- **Subagent strategy:** `required` / `authorization=approved`. 4 roles: ontology-reuse,
  creative-pipeline, ad-network-measurement, auto-research. Parallelism `fanout`, join `parent_synthesis`.
- **Blocked fields:** none.
- **Runtime status:** `running` → updated to `complete` in RESULT.md after final synthesis.
- **Guardrails:** ontologize/GoldenQuill read-only; write only under `projects/autoads/`; no live
  ad-network calls, credentials, or PII; outputs are a candidate seed pending owner decision.

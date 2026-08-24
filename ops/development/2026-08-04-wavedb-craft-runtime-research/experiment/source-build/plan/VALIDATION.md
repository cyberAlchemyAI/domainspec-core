# Plan validation

All checks are acceptance-critical.

1. Define transport is pass and records explicit source-build authorization.
2. Design selection is `design-validator-pass`, fixed point, and diagnostic-free.
3. Architecture has all six required views.
4. Layering defines L0–L3 decisions and only L0 is active.
5. Work Pack is medium/split and links useful task, wave, and shared files.
6. Exactly two unique SWUs exist, each with one parent, primary behavior,
   split analysis, source anchors, write scope, done criteria, validation,
   execution owner, and closeout row.
7. Exactly one unit is selected: SWU-WCSB-001.
8. SWU-WCSB-002 depends on SWU-WCSB-001 pass and cannot run initially.
9. Full Dispatch Spec validates pass with no subagents.
10. Distill returns pass with zero task-shaped SWUs.
11. No Plan artifact claims build/test/runtime evidence.

Suggested deterministic checks:

```bash
jq -e '.verdict == "pass" and .fixed_point == true' ../design/DESIGN-SELECTION-RESULT.json
python3 arcanum/formulae/dispatch-spec/scripts/validate-dispatch.py source-build.dispatch.json --json
rg -n 'SWU-WCSB-00[12]' WORK-PACK.md work-pack/tasks work-pack/waves/W0-SOURCE-BUILD.md
git diff --check -- plan
```

# MTNG v2 Changelog

This packet revises the original MTNG review packet after Raptor mini and Gemini outside reviews.

## Major Scope Changes

1. **Reframed V1 as the Post-Hoc Issue Packager**
   V1 is now explicitly an on-demand, selected-input issue-packaging and artifact-extraction pipeline.

2. **Deferred live runtime orchestration**
   V1 must not dynamically branch live user intent during active runtime. Targeted live mode is deferred.

3. **Run-local state ownership**
   V1 MTNG state lives in the output directory, not inside ResonantOS core state. ResonantOS may later ingest selected outputs through review gates.

4. **Numeric branch-pressure scoring deferred**
   Hardcoded weights are replaced by binary V1 branch triggers. Numeric scoring is reserved for future empirical tuning.

5. **"Tone" renamed to "Routing Signature" for implementation clarity**
   The metaphor remains in the name, but V1 implementation language is operational.

6. **Simplified lifecycle**
   V1 uses `proposed → processing → closed`, with `closed_result` preserving passed/partial/failed/rejected/superseded/needs_human.

7. **Misrouting loop limits added**
   V1 caps reroutes and validator failures to prevent oscillation.

8. **Provider fabric relationship clarified**
   MTNG does not own model/provider routing in V1. It either runs standalone with explicit model config or uses existing ResonantOS provider policy.

9. **Add-on capability grants clarified**
   MTNG specialty tools must request capabilities through existing ResonantOS add-on/tool permission systems when run inside ResonantOS.

10. **OKF-first with MTNG-native fallback preserved**
    OKF is preferred for exported knowledge artifacts, but MTNG-native YAML/JSON keeps operational state and edge cases.

11. **Contribution capture remains non-economic**
    V1 records contribution structure only. Valuation, compensation, governance weight, or credits remain out of scope.

## Remaining Intentional Gaps

- Phase 0 integration mapping has not yet been performed.
- Exact OKF type names are deferred until the team chooses conventions.
- Actual implementation storage paths must be chosen with maintainers.
- Runtime integration remains deferred until the post-hoc pilot proves value.

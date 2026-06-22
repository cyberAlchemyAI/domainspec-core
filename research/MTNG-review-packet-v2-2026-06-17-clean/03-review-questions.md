# Review Questions for MTNG Packet v2

Please evaluate the revised MTNG proposal against these questions.

## V1 Scope

1. Is the "Post-Hoc Issue Packager" pilot small enough to build without disrupting ResonantOS runtime architecture?
2. Does the proposal sufficiently defer live runtime orchestration?
3. Are the non-goals strong enough to prevent scope creep?

## Integration

4. Is run-local state ownership acceptable for V1?
5. Which ResonantOS component should eventually ingest MTNG outputs, if any?
6. Should V1 be CLI-only, sidecar service, schema-only pipeline, or developer inspection panel?
7. Does the proposal respect Guardian Core, provider fabric, memory review gates, and add-on capability grants?

## Branching and Validation

8. Are binary branch triggers better for V1 than numeric branch-pressure scoring?
9. Are the fast-path rules clear enough to prevent over-processing simple signals?
10. Are validators sufficient as the main safety net for misrouting?
11. Are the reroute limits strict enough to prevent oscillation?
12. Are V1 recombination rules concrete enough to avoid false synthesis?

## OKF and Exports

13. Is the OKF-first / MTNG-native fallback policy sensible?
14. Which exported artifacts should be OKF-compatible in V1?
15. Are the edge-case flags enough to prevent OKF flattening from hiding operational meaning?

## Memory and Contribution

16. Are review-only memory candidates safe enough for V1?
17. Is contribution capture clearly separated from valuation?
18. Are contribution records useful if no economic or governance weight is assigned yet?

## Failure Conditions

19. Where is MTNG most likely to fail first?
20. What should be removed, clarified, or deferred before showing this to maintainers?
21. What would make MTNG not worth pursuing after the pilot?

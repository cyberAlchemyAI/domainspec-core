# Cross-Task Decisions

| Decision | Status | Rule |
| --- | --- | --- |
| DEC-ZRIG-PRIVATE-SCOPE | accepted | Keep Z-Rig remediation artifacts under `projects/zrig/**`. |
| DEC-ZRIG-NO-PUBLIC-PROMOTION | accepted | Park public command/sigil/spell/runtime package work. |
| DEC-ZRIG-FIRST-SWU | accepted | Select F1 gate fail-closed behavior as first execution SWU. |
| DEC-ZRIG-OBSERVABILITY | accepted | Obligations are design-only until engine metrics/events are wired. |
| DEC-ZRIG-CRAFT-AUTHORITY | accepted | Craft can manage review state; it does not prove runtime/product authority. |
| DEC-ZRIG-BLOCKED-DEPS | accepted | Missing pytest/runtime deps are F8 evidence, not successful F1/F3 validation. |

Open decisions to resolve in later SWUs:

- DEC-ZRIG-GATE-POLICY: implement all specific gates or fail closed for missing spec-governed gates.
- DEC-ZRIG-LIVE-IDENTITY-AUTHORITY: choose trusted identity source.
- DEC-ZRIG-DEPLOY-SURFACE: thread deploy/sentinel config or fail closed when absent.
- DEC-ZRIG-RESIDUE-FATALITY: decide mode-specific fatality/degraded-assurance policy.
- DEC-ZRIG-AUTO-SPEC: promote `AUTO` to spec or mark it as implementation extension.
- DEC-ZRIG-METRICS-STATUS: wire metrics or mark prototype/non-product.

# Spec card — pipeline.privacy (Phase 2a — Privacy Router)

**STATUS:** LOCKED

**Blueprint anchor:** `pipeline/blueprint/v0.1/section_04_v2_3_amendment.md` §4.14 (v2.3)
**Spec-card version:** v1
**Round:** Phase 2a
**Futureproofing scope:** §4.1 public-API boundary, §4.6 blueprint-code drift, §4.10 type hints,
§4.11 docstring references, §4.9 regression tests

---

## Public API (goes in `__all__`)

- `PrivacyTag` — `str, Enum` with values LOCAL_ONLY / CLOUD_ELIGIBLE / CLASSIFIER_ERROR [§4.14]
- `PrivacyRouteResult` — frozen dataclass [§4.14 gate logic table]
- `run_privacy_pregate(payload: str, seat: str, default_routing: str) -> PrivacyRouteResult` — gate entry point [§4.14]
- `PRIVACY_FAILURE_CODE_CLASSIFIER_ERROR: str` — `"F-PRIVACY-CLASSIFIER-ERROR"` [§6 v2.3]
- `PRIVACY_FAILURE_CODE_BYPASS_ATTEMPT: str` — `"F-PRIVACY-PAYLOAD-TAGGED-LOCAL-ONLY-BYPASSED"` [§6 v2.3]

---

## Data structures

```python
class PrivacyTag(str, Enum):
    LOCAL_ONLY = "LOCAL_ONLY"
    CLOUD_ELIGIBLE = "CLOUD_ELIGIBLE"
    CLASSIFIER_ERROR = "CLASSIFIER_ERROR"

@dataclass(frozen=True)
class PrivacyRouteResult:
    tag: PrivacyTag              # classifier output tag
    routed_local: bool           # True when gate forces or confirms local routing
    failure_code: str | None     # set when tag != CLOUD_ELIGIBLE
    detail: dict | None          # rails-report context
```

---

## Algorithms

1. Call `classify_payload(payload) -> PrivacyTag` inside try/except.
2. On exception: treat as `CLASSIFIER_ERROR`.
3. Map tag → result per §4.14 gate logic table:
   - `CLOUD_ELIGIBLE` → `routed_local=False, failure_code=None`
   - `LOCAL_ONLY` → `routed_local=True, failure_code=None`
   - `CLASSIFIER_ERROR` → `routed_local=True, failure_code=F-PRIVACY-CLASSIFIER-ERROR`
4. Return frozen `PrivacyRouteResult`.

---

## Failure codes

| Code | Trigger |
|---|---|
| `F-PRIVACY-CLASSIFIER-ERROR` | Classifier returns CLASSIFIER_ERROR or raises exception |
| `F-PRIVACY-PAYLOAD-TAGGED-LOCAL-ONLY-BYPASSED` | Orchestrator dispatches cloud after routed_local=True (detected by caller, not by gate itself) |

---

## Test surface

### Property tests
- `run_privacy_pregate` always returns a `PrivacyRouteResult`
- When `tag != CLOUD_ELIGIBLE`, `routed_local` is always True
- When `tag == CLOUD_ELIGIBLE`, `routed_local` is always False
- When `failure_code` is set, it is one of the two defined constants

### Failure-code tests
- `F-PRIVACY-CLASSIFIER-ERROR`: stub path; classifier-exception path
- `F-PRIVACY-PAYLOAD-TAGGED-LOCAL-ONLY-BYPASSED`: not directly tested by gate (gate emits on bypass attempt from caller); gate returns `routed_local=True` which caller must respect

### Corpus tests
- `tests/corpus/privacy_router/v1/` — 3 vectors (classifier_error, local_only_contract, cloud_eligible_contract)

---

## Futureproofing commitments

- Public-API surface declared in `__all__`
- No on-disk artifacts in Phase 2a (no schema version needed)
- Classifier is injected via module-level function for testability (swap real classifier at v0.2 by replacing `_classifier.py`)
- `BLUEPRINT_DEPS` dict declares §4 v2.3 anchor

---

## Done definition

- All pytest green
- `F-PRIVACY-CLASSIFIER-ERROR` covered by test
- `routed_local` invariant test green
- Spec card every row satisfied
- 100% coverage on `_router.py` and `_classifier.py`

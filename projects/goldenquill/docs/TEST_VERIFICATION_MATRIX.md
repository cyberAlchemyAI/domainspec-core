# Test Verification Matrix

This matrix maps Tilth subsystems to their corresponding test suites and the `F-*` gate families they guard. When modifying a subsystem, run the associated test commands to prove the failure gates still hold.

## 1. Orchestrator & Router

**Subsystem:** `pipeline/orchestrator/` (Router, Dispatcher, Provider Boundary)
**Guards:** `F-CLASS-*` (Classification Context), `R-NO-DIRECT-PROVIDER-HTTP`

When touching `pipeline/orchestrator/router.py` or the provider boundary, verify with:
```bash
scripts/run_tests.sh tests/orchestrator/test_router_classification_boundary.py \
                     tests/orchestrator/test_provider_boundary.py \
                     tests/linting/test_r_no_direct_provider_http.py \
                     tests/logician/gates/test_f_class_*
```

## 2. Logician Core

**Subsystem:** `pipeline/logician/` (Gate definitions, Predicates, Rubrics)
**Guards:** `F-LOGICIAN-*`, `F-DIALECT-*`, `F-CARDS-*`, `F-PACKET-*`, `F-WPFA-*`

When modifying any gate predicate or logging mechanism:
```bash
# Full logician suite (takes ~15-20s)
scripts/run_tests.sh tests/logician/
```

## 3. Council Seats (Scribe, Editor, Judge, Red Team)

**Subsystem:** `pipeline/seats/` and `pipeline/orchestrator/seats/`
**Guards:** `F-CLASS-HEAVY-JUDGE-CLOUD-DOWNLOAD`, `F-SEAT-*`

When touching seat implementations or provider bindings (e.g. `_call_anthropic`, `_call_google`):
```bash
# Exercise cross-family dispatch & capstone hash pins
scripts/run_tests.sh tests/seats/
```

## 4. Cards & Sub-kind Registries

**Subsystem:** `pipeline/cards/`, `pipeline/cards/_schema/`
**Guards:** `F-CARDS-SIGNATURE-INVALID`, `F-CARDS-COUPLING-VIOLATION-EXTENSION`

When changing card schemas, matrix YAMLs, or lifecycle loaders:
```bash
scripts/run_tests.sh tests/cards/ \
                     tests/logician/gates/test_f_cards_coverage_incomplete.py \
                     tests/logician/gates/test_f_cards_dormant_primitives.py
```

## 5. Sovereignty Envelope & Vault

**Subsystem:** `pipeline/sovereignty/`, `vault_shared/`
**Guards:** Ed25519 signatures, Lockfile Integrity, Org Isolation (`Law 3`)

When modifying boot sequence, `PROJECT_CONTEXT`, or data isolation:
```bash
scripts/run_tests.sh tests/sovereignty/ \
                     tests/vault/ \
                     tests/institutional_memory/ \
                     tests/scripts/test_audit_term_signer.py
```

## 6. AST Linting

**Subsystem:** `pipeline/linting/`
**Guards:** Static codebase hygiene, `R-NO-POLITICAL-AXIS-LITERAL`, `R-INTAKE-NO-LOGFIRE-IMPORT-BEFORE-ENV`

When adding a new AST-lint rule or modifying existing footprint constraints:
```bash
scripts/run_lint.sh pipeline
scripts/run_tests.sh tests/linting/
```

## 7. Nervous System

**Subsystem:** `pipeline/nervous_system/`
**Owner/Status:** needs owner assignment
**Verification:**
```bash
scripts/run_tests.sh tests/nervous_system/
```

## 8. Scout

**Subsystem:** `pipeline/scout/`
**Owner/Status:** needs owner assignment
**Verification:**
```bash
scripts/run_tests.sh tests/scout/
```

## 9. Loop

**Subsystem:** `pipeline/loop/`
**Owner/Status:** needs owner assignment
**Verification:**
```bash
scripts/run_tests.sh tests/loop/
```

## 10. CLI

**Subsystem:** `pipeline/cli/`
**Owner/Status:** needs owner assignment
**Verification:**
```bash
scripts/run_tests.sh tests/cli/
```

## 11. Integration

**Subsystem:** integration layer
**Owner/Status:** needs owner assignment
**Verification:**
```bash
scripts/run_tests.sh tests/integration/
```

---
*Note: Always verify your changes against the full suite (`scripts/run_tests.sh`) before submitting a PR. Local macOS tests may miss platform-specific CI failures caught by the Linux wheel-smoke matrix.*

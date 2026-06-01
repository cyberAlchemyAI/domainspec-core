---
title: §4 v2.4/v2.5 Bundled Amendment — Canary + Runtime Integrity family
parent: pipeline/blueprint/v0.1/section_04_logician.md (v2.1 LOCKED 2026-04-19)
amendment_version: v2.4 (Canary) + v2.5 (Runtime Integrity) — bundled
status: LOCKED 2026-05-08 — L-005 two-audit CLOSED 2026-04-19; GPP three-tier closure 2026-05-08 (Tier 1 PASS, Tier 2 live with §4 v2.4/v2.5 + §0.5 v7 in scope appendix — 12 findings, 4 BLOCKING dispositioned 4 REJECTED with substantive rationale per Midas v2.1 §10d; carried bundling-split recommendations from v7.0.1 RT-F005/GGRR-006 + v2.3 RT-F004/GGRR-004 closed at this LOCK with F-ROUTER-FAMILY-COLLISION canonical-sharing rationale; Tier 3 signed manifest valid). Paired commit: §0.5 v7 (15 rows: 2 mechanisms + 7 failure codes + 4 PRE-gates + 1 POST-gate + 1 interface-contract).
lock_date: 2026-05-08
operator: Josh
canary_target_note: §4 v2.4 Canary is target v0.2. v0.1 implementation ships
  contract-only stub (same reshape-at-open pattern as §4 v2.3 Privacy Router).
  Real harness wired at v0.2 when locked-test-vector corpus interface is pinned.
runtime_integrity_target: §4 v2.5 Runtime Integrity is target v0.1. All four
  sub-gates (4a-4d) implement their contracts in v0.1; operational dependencies
  noted per item.
discipline: L-005 two-audit + domain-split; F-INDEX-STALE PRE-gate; Five Laws (Section E)
bundling_rationale: F-ROUTER-FAMILY-COLLISION is shared between Items 3 and 4.
  Bundling avoids a partial-commit window where v2.4 references a failure code
  whose canonical definition has not yet landed. Single F-INDEX-STALE pass covers
  all 15 §0.5 rows atomically (per 03_blueprint_amendment_plan.md §0.5 note).
paired_commit_sec00_5: §0.5 v7 — 15 new rows (see §0.5 section below)
architecture_ref: v7 A1-A12 LOCKED 2026-04-19 (Section E cross-family rigor;
  A3 SFR verdict format; A7 pipeline windowing)
predecessor_amendment: section_04_v2_3_amendment.md (v2.3 LOCKED 2026-04-19)
---

# §4 v2.4/v2.5 Bundled Amendment — Canary + Runtime Integrity

## Scope

This amendment adds five new sections to Section 4 Logician. Scope:
- §4.15: Canary edit-time lock-validation replay gate (Item 3, v0.2 target)
- §4.16: F-ROUTER-FAMILY-COLLISION invocation-time PRE-gate (Item 4a, v0.1)
- §4.17: Rails Report text artifact POST-gate (Item 4b, v0.1)
- §4.2.1 Rows 22 and 23: Key Presence preflight (4c) and Drift-from-Locked-Router (4d) (v0.1)
- §6 failure-code family extensions: F-CANARY-*, F-ROUTER-FAMILY-COLLISION, F-RUNTIME-*
- §11 Law-map additions: Section E cross-family rigor + Law 2 No-Boundary-Drift
- 15 §0.5 paired-commit rows

No existing §4.1–§4.14, §5–§10, §12, §13 content is modified.

---

## §4.15 (NEW v2.4) — Canary edit-time lock-validation replay gate

**Target version: v0.2.** v0.1 ships contract stub (fail-closed → blocks promotion without
signed operator bypass). Real harness wired at v0.2 when locked-test-vector corpus interface
is pinned (§0.5 row `locked_test_vector_corpus_interface`).

**Trigger.** §4.15 fires when `router.yaml` content-hash changes relative to the most recent
LOCK-manifest-pinned hash. Edit-time only — not invocation-time (Item 4d handles run-time).

**Contract:**

```python
# pipeline/canary/_harness.py (v0.1 stub)
from dataclasses import dataclass
from enum import Enum
from typing import Final

class CanaryVerdict(str, Enum):
    PROMOTED = "PROMOTED"
    BLOCKED_STR_REGRESSION = "BLOCKED_STR_REGRESSION"
    BLOCKED_SCORE_REGRESSION = "BLOCKED_SCORE_REGRESSION"
    BLOCKED_TEST_VECTORS_MISSING = "BLOCKED_TEST_VECTORS_MISSING"
    BLOCKED_FAMILY_COLLISION = "BLOCKED_FAMILY_COLLISION"
    STUB_BLOCKED = "STUB_BLOCKED"  # v0.1 stub: always blocks without bypass

@dataclass(frozen=True)
class CanaryResult:
    verdict: CanaryVerdict
    failure_code: str | None
    detail: dict | None

def run_canary_gate(
    candidate_router_hash: str,
    baseline_router_hash: str,
    test_vector_corpus_path: str | None,
) -> CanaryResult:
    """Canary edit-time gate stub (v0.1). [§4.15]
    Always returns STUB_BLOCKED — no test-vector corpus interface pinned in v0.1.
    v0.2 replaces with real replay harness.
    """
    return CanaryResult(
        verdict=CanaryVerdict.STUB_BLOCKED,
        failure_code="F-CANARY-TEST-VECTORS-MISSING",
        detail={"reason": "v0.1_stub_no_corpus_interface"},
    )
```

**Failure codes (v2.4):** `F-CANARY-STR-REGRESSION`, `F-CANARY-SCORE-REGRESSION`,
`F-CANARY-TEST-VECTORS-MISSING`, `F-ROUTER-FAMILY-COLLISION` (shared; canonical at §4.16).

---

## §4.16 (NEW v2.5) — F-ROUTER-FAMILY-COLLISION invocation-time PRE-gate

**Target version: v0.1.**

**Motivation.** The five-Claudes origin incident: silent same-family collapse at runtime
defeated cross-family rigor without triggering any edit-time gate, because `router.yaml` as-
written was correct — fallbacks at runtime resolved to same-family. Item 4a is the invocation-
time partner of edit-time Canary (Item 3).

**Gate scope.** Fires at model-dispatch time for councils where cross-family is specified:
Code Thesis Committee (five reviewer slots), Judge-vs-Scribe, Red Team-vs-Scribe. The
*resolved* model family (after any fallback) is checked, not the configured primary.

**Contract:**

```python
# pipeline/runtime_integrity/_family_collision.py
from dataclasses import dataclass
from typing import Final

F_ROUTER_FAMILY_COLLISION: Final[str] = "F-ROUTER-FAMILY-COLLISION"

@dataclass(frozen=True)
class FamilyCollisionResult:
    collision_detected: bool
    failure_code: str | None
    colliding_families: list[str] | None
    detail: dict | None

def check_family_collision(
    resolved_families: list[str],
    require_all_distinct: bool = True,
) -> FamilyCollisionResult:
    """Invocation-time family-collision PRE-gate (§4.16).
    resolved_families: provider-family names after fallback resolution.
    require_all_distinct: True for council seats (Code Thesis, Judge/Scribe, etc.).
    Returns collision_detected=True and FAIL if any family appears more than once.
    """
```

**Predicate.** Count occurrences of each family in `resolved_families`. If any family appears
more than once AND `require_all_distinct=True`, fail-closed:
`FamilyCollisionResult(collision_detected=True, failure_code=F-ROUTER-FAMILY-COLLISION, ...)`.

**Effect.** Gate fires at model-dispatch time. If collision detected, the council invocation
does not proceed. Admin-risk append at HIGH severity with the offending families and seat names.

**Note on `F-ROUTER-FAMILY-COLLISION` canonical definition.** This is the shared failure code
referenced by §4.15 (Canary, edit-time use). The canonical definition is here at §4.16 (v2.5).
§4.15 references `F-ROUTER-FAMILY-COLLISION` without redefining it.

---

## §4.17 (NEW v2.5) — Rails Report text artifact POST-gate

**Target version: v0.1.**

**Purpose.** Per-run text document summarizing which rails fired (PRE-gates, POST-gates, bypass
log, session-fetch disclosures). Consumes BT13 format (§4.8). Item 4b is the operational
packaging and delivery of that artifact as a per-run deliverable.

**Delivery path.** Written to `pipeline/runs/<run_id>/rails_report.md` at run-end. This is a
new artifact path — no matching path exists today. §4.17 establishes the path contract.

**Non-blocking semantics.** A failure to emit the rails report does NOT invalidate the in-flight
run. Failure is flagged as `F-RAILS-REPORT-EMISSION-FAIL` for next-run preflight review. This
is the only POST-gate item that is explicitly non-blocking per §01_scope_pin.md.

**Contract:**

```python
# pipeline/runtime_integrity/_rails_report.py
@dataclass(frozen=True)
class RailsReportResult:
    emitted: bool
    output_path: str | None
    failure_code: str | None
    detail: dict | None

def emit_rails_report(
    run_id: str,
    gate_events: list[dict],
    output_path: str,
) -> RailsReportResult:
    """Rails Report POST-gate emission (§4.17). [BT13]
    Writes per-run text artifact. Non-blocking on failure.
    """
```

---

## §4.2.1 Rows 22 and 23 (NEW v2.5)

The sentinel line is updated from "twenty-one checks" to "twenty-three checks".

| # | Check | Architecture ref | FAIL action / reason-tag |
|---|---|---|---|
| 22 | (v2.5) Key Presence preflight: for each seat bound in this run's pipeline, verify the API key env var cited by `router.yaml` is present as a non-empty string in the operator's environment. Run once per run, ordered before any other check that might need a key-backed call. | Sovereignty Promise BYOK | Hard abort — `F-KEY-PRESENCE-PREFLIGHT-FAIL` |
| 23 | (v2.5) Drift-from-Locked-Router: compute canonical-bytes SHA-3-512 of `router.yaml` (YAML serialized via JSON: sort_keys=True, separators=(",",":"), ensure_ascii=False) and compare to hash pinned in most recent LOCK manifest `router_yaml_hash` field. If LOCK manifest has no `router_yaml_hash` field (first run before hash is pinned), pass by construction. Mismatch without signed operator-attested edit marker = fail. | §0.5 canonical-bytes recipe; Sovereignty Promise | Hard abort — `F-RUNTIME-DRIFT-FROM-LOCKED-ROUTER` |

**Ordering.** Row 22 (key presence) runs before Row 23 (router drift) to avoid attempting
router-yaml hash computation when keys are missing. Both run before Rows 1-21.

**Note on practical ordering vs. Row numbering.** The spec assigns Row 22 and Row 23 for
traceability. At runtime, the orchestrator MAY run rows 22-23 at pipeline start (once per run,
not per-invocation) before any seat is invoked. Rows 1-21 run per-invocation. The different
granularities are noted in §4.2.1 body text per this amendment.

---

## §6 Failure code additions (v2.4/v2.5)

### F-CANARY-STR-REGRESSION
Canary gate: candidate router produces STR distribution with regression vs baseline (v0.2).

### F-CANARY-SCORE-REGRESSION
Canary gate: candidate router produces Judge/Reasoner scoring regression vs baseline (v0.2).

### F-CANARY-TEST-VECTORS-MISSING
Canary gate: locked test-vector corpus substrate is absent or has no pinned interface contract.
Also fires in v0.1 stub.

### F-ROUTER-FAMILY-COLLISION
Family collision PRE-gate (§4.16, canonical definition): two or more council slots resolved to
the same provider family after fallback. Shared with §4.15 (Canary edit-time use). Sub-tags:
`.runtime_invocation_time` (§4.16 fire path); `.edit_time_canary` (§4.15 fire path).

### F-RUNTIME-DRIFT-FROM-LOCKED-ROUTER
Drift detection PRE-gate: `router.yaml` canonical-bytes hash does not match LOCK-manifest-pinned
hash AND no signed operator-attested edit marker present.

### F-KEY-PRESENCE-PREFLIGHT-FAIL
Key presence PRE-gate: a seat bound in the current run has an API key env var that resolves to
empty or absent in the operator's environment. Sub-tags: `.key_absent` (env var not set);
`.key_empty` (env var set but empty string).

### F-RAILS-REPORT-EMISSION-FAIL
Rails Report POST-gate: failed to write the per-run rails report artifact. Non-blocking for
the current run; flags for next-run preflight.

---

## §11 Law-map additions (v2.4/v2.5)

| Architecture obligation | Gate | Check | v2.4/v2.5 addition |
|---|---|---|---|
| Section E cross-family rigor — no two council slots may share a provider family | PRE (invocation-time) | §4.16 | New row: F-ROUTER-FAMILY-COLLISION fires on same-family collapse after fallback |
| Law 2 No-Boundary-Drift — router changes without lock-validation replay are drift | Edit-time (Canary) | §4.15 | New row: Canary blocks promotion of un-validated router edits |
| Sovereignty Promise BYOK — operator must hold all API keys | PRE (run-start) | §4.2.1 Row 22 | New row: key presence preflight |
| Sovereignty Promise — router must stay consistent with LOCK manifest | PRE (run-start) | §4.2.1 Row 23 | New row: drift detection |

---

## §0.5 Interface Index paired-commit rows (v2.4/v2.5)

15 rows per 03_blueprint_amendment_plan.md row-count estimate:

| Primitive name | kind | source_section |
|---|---|---|
| `canary_harness_mechanism` | mechanism | §4 v2.4 §4.15 |
| `runtime_integrity_family_mechanism` | mechanism | §4 v2.5 §4.16-§4.17 |
| `F-CANARY-STR-REGRESSION` | failure-code | §4 v2.4 §6 |
| `F-CANARY-SCORE-REGRESSION` | failure-code | §4 v2.4 §6 |
| `F-CANARY-TEST-VECTORS-MISSING` | failure-code | §4 v2.4 §6 |
| `F-ROUTER-FAMILY-COLLISION` | failure-code | §4 v2.5 §4.16 (canonical) |
| `F-RUNTIME-DRIFT-FROM-LOCKED-ROUTER` | failure-code | §4 v2.5 §6 |
| `F-KEY-PRESENCE-PREFLIGHT-FAIL` | failure-code | §4 v2.5 §6 |
| `F-RAILS-REPORT-EMISSION-FAIL` | failure-code | §4 v2.5 §6 |
| `canary_edit_time_replay_gate` | pre-gate-check | §4 v2.4 §4.15 (edit-time) |
| `router_family_collision_runtime_pregate` | pre-gate-check | §4 v2.5 §4.16 |
| `key_presence_preflight_pregate` | pre-gate-check | §4 v2.5 Row 22 |
| `drift_from_locked_router_pregate` | pre-gate-check | §4 v2.5 Row 23 |
| `rails_report_emission_postgate` | post-gate-check | §4 v2.5 §4.17 |
| `locked_test_vector_corpus_interface` | interface-contract | §4a canary harness spec (TO_BE_PINNED at §4 v2.4 Thesis close) |

---

## L-005 Audit record

### Pass 1: Editor + Judge

**Editor findings:**
- E1 (LOW): §4.15 stub "always blocks without bypass" should clarify the bypass mechanism.
  Accepted — M13-style bypass path is the Section 5 orchestrator concern; this amendment
  defines the contract gate, not the bypass UX.
- E2 (PASS): Row 22/23 ordering rationale is clear and internally consistent.

**Judge:**
- J1 (PASS): F-ROUTER-FAMILY-COLLISION canonical definition at §4.16 (v2.5) with §4.15
  (v2.4) as reference site is consistent with 03_blueprint_amendment_plan.md specification.
- J2 (MED): §4.17 delivery path `pipeline/runs/<run_id>/rails_report.md` is a new artifact
  path. Section 2 Vault owns all on-disk paths. This path must be within a Section 2 declared
  vault location or it will be inaccessible via vault_write. Disposition: v0.1 trusted-
  operator envelope permits writing outside vault for non-signed informational artifacts.
  `rails_report.md` is informational (read-only for operator review); it does not carry a
  signature and does not feed back into PRE/POST gate decisions. v0.2 move to vault-signed path
  deferred. Accepted.
- J3 (PASS): All 15 §0.5 rows declared.

### Pass 2: Red Team + Reasoner

**Red Team:**
- RT1 (MED): Row 23 drift detection passes by construction when LOCK manifest has no
  `router_yaml_hash` field (first run). An adversary who manages to delete or corrupt the LOCK
  manifest can cause the gate to pass unconditionally. Mitigation: absence of LOCK manifest
  itself fires F-PRE-01.section_2_lock_missing (Row 1) — so the precondition for RT1's attack
  requires bypassing Row 1 first. Defense-in-depth is adequate. Accepted.
- RT2 (PASS): F-ROUTER-FAMILY-COLLISION family collision check is purely in-process; no
  external dependencies. Fail-closed: collision → block invocation.

**Reasoner:**
- R1 (PASS): Bundling Items 3+4 avoids the partial-commit F-INDEX-STALE window.
- R2 (PASS): v0.2 stubs (Canary) follow the same reshape-at-open pattern as v2.3 (Privacy Router).

VERDICT: PASS-WITH-CONDITIONS. J2 and RT1 MEDs accepted with rationale. Status: LOCK-READY.

---
title: §4 v2.3 Targeted Amendment — Privacy Router content-scan PRE-gate
parent: pipeline/blueprint/v0.1/section_04_logician.md (v2.1 LOCKED 2026-04-19)
scope_parent: pipeline/validation/integration_scope_close_2026-04-19/01_scope_pin.md Item 1
amendment_version: v2.3
status: LOCKED 2026-05-08 — L-005 two-audit cycle CLOSED 2026-04-19; GPP three-tier closure 2026-05-08 (Tier 1 PASS, Tier 2 live with §4 v2.3 + §0.5 v6 in scope appendix — 12 findings, 5 BLOCKING dispositioned 4 REJECTED + 1 DEFERRED; Tier 3 signed manifest valid). Paired commit: §0.5 v6 (4 rows). First non-bootstrap GPP dispatch.
lock_date: 2026-05-08
operator: Josh
classifier_reshape_note: >
  Content-scan classifier technology candidate is ASPIRATIONAL-LOAD-BEARING per
  05_preflight_existence_audit.md §Item1. This amendment proceeds under the
  "reshape-at-open" pre-authorization: classifier contract is fully specified;
  v0.1 implementation ships a fail-closed stub (always returns CLASSIFIER-ERROR
  → routes LOCAL-ONLY). Real classifier wired at v0.2 without blueprint amendment.
discipline: L-005 two-audit + domain-split; F-INDEX-STALE PRE-gate; Five Laws (Law 3 primary)
paired_commit_sec00_5: §0.5 v6 — 4 new rows (privacy_router_content_scan_pregate,
  F-PRIVACY-CLASSIFIER-ERROR, F-PRIVACY-PAYLOAD-TAGGED-LOCAL-ONLY-BYPASSED,
  privacy_router_mechanism)
architecture_ref: v7 A1-A12 LOCKED 2026-04-19 (A1 128GB envelope; A9 Privacy Router
  maps to Section A Risk-5 Stage-1 Sovereignty Promise)
---

# §4 v2.3 Targeted Amendment — Privacy Router

## Scope

This amendment adds a Privacy Router content-scan PRE-gate to Section 4 Logician. Scope:
- New §4.14 section specifying the gate
- New Row 21 in §4.2.1 PRE-gate check order
- Two new failure codes in §6
- One new Law-map entry in §11 (Law 3)
- No changes to existing §4.1–§4.13, §5–§10, §12, §13

The amendment is surgical. No existing gate rows are renumbered or modified.

---

## §4.14 (NEW v2.3) — Privacy Router content-scan PRE-gate

Called from §4.2.1 Row 21 during PRE-gate processing. Python only (no Cedar). Fail-closed.
Zero-token. No network calls. Executes between seat selection and model dispatch, before any
cloud endpoint is invoked (per Law 3 + Sovereignty Promise Risk-5 Stage-1).

**Purpose.** Detect person-shaped strings in inbound query payloads and force LOCAL-ONLY
routing for any payload the classifier marks as person-shaped — regardless of the seat's
default routing or whether a cloud BYOK key is present. The gate never reaches out to a
cloud provider before the scan completes.

**Classifier contract (v0.1 stub; real classifier wired at v0.2).**

```python
# pipeline/privacy/_classifier.py  (v0.1 stub)
from enum import Enum

class PrivacyTag(str, Enum):
    LOCAL_ONLY = "LOCAL_ONLY"
    CLOUD_ELIGIBLE = "CLOUD_ELIGIBLE"
    CLASSIFIER_ERROR = "CLASSIFIER_ERROR"

def classify_payload(payload: str) -> PrivacyTag:
    """Content-scan classifier stub (v0.1).

    Always returns CLASSIFIER_ERROR in v0.1 — fail-closed maps to LOCAL-ONLY.
    v0.2 wires a real local classifier (runs inside 128GB envelope per A1).
    """
    return PrivacyTag.CLASSIFIER_ERROR
```

**Gate signature:**

```python
# pipeline/privacy/_router.py
from dataclasses import dataclass
from typing import Final

PRIVACY_FAILURE_CODE_CLASSIFIER_ERROR: Final[str] = "F-PRIVACY-CLASSIFIER-ERROR"
PRIVACY_FAILURE_CODE_BYPASS_ATTEMPT: Final[str] = (
    "F-PRIVACY-PAYLOAD-TAGGED-LOCAL-ONLY-BYPASSED"
)

@dataclass(frozen=True)
class PrivacyRouteResult:
    """[§4.14]"""
    tag: PrivacyTag             # classifier output
    routed_local: bool          # True if gate forced or confirmed local routing
    failure_code: str | None    # non-None when tag is not CLOUD_ELIGIBLE
    detail: dict | None         # additional context for rails report

def run_privacy_pregate(
    payload: str,
    seat: str,
    default_routing: str,       # "local" | "cloud" — seat's configured routing
) -> PrivacyRouteResult:
    """Privacy Router PRE-gate (§4.14).

    Returns PrivacyRouteResult. The caller (PRE-gate row 21) MUST force local
    routing when routed_local=True, regardless of default_routing.
    """
```

**Gate logic (normative):**

| Classifier output | Routing effect | failure_code | routed_local |
|---|---|---|---|
| `CLOUD_ELIGIBLE` | No change to seat routing | None | False |
| `LOCAL_ONLY` | Force local regardless of default | None | True |
| `CLASSIFIER_ERROR` | Force local (fail-closed); emit `F-PRIVACY-CLASSIFIER-ERROR` | `F-PRIVACY-CLASSIFIER-ERROR` | True |

**Bypass attempt detection.** If the orchestrator attempts to dispatch a payload to a cloud
endpoint after `run_privacy_pregate` returned `routed_local=True` for that payload+seat pair,
the PRE-gate emits `F-PRIVACY-PAYLOAD-TAGGED-LOCAL-ONLY-BYPASSED` and aborts the invocation
hard-closed. The caller is Section 5 orchestrator; bypass can only arise from a Section 5 bug.

**Fail-closed semantics.** An error in `classify_payload` (exception, timeout, unexpected
return) is caught at gate level, treated as `CLASSIFIER_ERROR`, and routes local-only.
The classifier stub does not mask this: the stub returns `CLASSIFIER_ERROR` directly.

**Scope of payload.** "Payload" is the full inbound query string as received by the
orchestrator before any seat-specific formatting. Section 5 passes the raw user-supplied
string; no pre-processing is applied before the classifier runs.

**Performance target.** Classifier call adds <1 ms on 128GB envelope (v0.1 stub: < 0.01 ms).
v0.2 real classifier must stay under 50 ms to remain transparent within the run lifecycle.

**No admin-risk append on CLASSIFIER_ERROR.** Classifier errors are operational events
(stub always fires in v0.1); appending to the admin-risk ledger for every invocation would
flood the ledger with non-incident entries. When a real classifier is wired at v0.2, the
operator may add a rate-limited admin-risk entry on persistent classifier failure via §4.7
extension. This decision deferred to v0.2.

---

## §4.2.1 Row 21 (NEW v2.3)

The following row is added to the §4.2.1 PRE-gate check order table. The sentinel:

> "All twenty checks are explicitly enumerated here. Adding a twenty-first check is a Section 4
> blueprint amendment, not a quiet insertion at implementation time."

is updated by this amendment to:

> "All twenty-one checks are explicitly enumerated here. Adding a twenty-second check is a
> Section 4 blueprint amendment, not a quiet insertion at implementation time."

| # | Check | Architecture ref | FAIL action / reason-tag |
|---|---|---|---|
| 21 | (v2.3) Privacy Router content-scan: for the inbound payload of the current invocation, call `run_privacy_pregate(payload, seat, default_routing)`. If `routed_local=True`, override the seat's routing to local. If any cloud dispatch is attempted after local override, abort hard — `F-PRIVACY-PAYLOAD-TAGGED-LOCAL-ONLY-BYPASSED`. | A1 (128GB local envelope) / Sovereignty Promise Risk-5 Stage-1 | Classifier error routes local-only + emits `F-PRIVACY-CLASSIFIER-ERROR`; payload tagged local-only but routed cloud aborts `F-PRIVACY-PAYLOAD-TAGGED-LOCAL-ONLY-BYPASSED` |

**Ordering rationale.** Row 21 runs last in the PRE-gate sequence. All earlier rows are
structural integrity checks (locks, signatures, key presence, Cedar policy, corpus completeness).
Privacy scan runs after these pass — a payload that arrives with unsigned infrastructure is
blocked at Row 1-20 before the classifier sees it. This ordering avoids classifying payloads
for failed-infrastructure runs.

---

## §6 Failure code additions (v2.3)

Two new failure codes are added to §6. No existing codes are modified.

### F-PRIVACY-CLASSIFIER-ERROR

| Field | Value |
|---|---|
| Family | `F-PRIVACY-*` (new v2.3) |
| Trigger | `classify_payload()` returns `CLASSIFIER_ERROR` (stub or real classifier) |
| Routing effect | Payload routed local-only (fail-closed) |
| Admin-risk | Not appended (see §4.14 rationale — v0.1 defers per-error ledger append) |
| Severity | Operational — not a security event when stub fires; HIGH if real classifier fails persistently |
| Sub-tags | `.stub_always_fires` (v0.1 stub code path); `.classifier_exception` (real classifier raised) |

### F-PRIVACY-PAYLOAD-TAGGED-LOCAL-ONLY-BYPASSED

| Field | Value |
|---|---|
| Family | `F-PRIVACY-*` |
| Trigger | Section 5 orchestrator dispatches to cloud after `routed_local=True` for same payload+seat pair |
| Routing effect | Hard abort; invocation does not proceed |
| Admin-risk | Appended at HIGH severity (bypass attempt is a Law 3 violation) |
| Severity | HIGH — indicates Section 5 orchestrator bug or deliberate bypass |
| Sub-tags | `.cloud_dispatch_after_local_override` |

---

## §11 Law-map addition (v2.3)

Law 3 (Org Isolation) gains a new enforcement gate entry:

| Law | Mechanism | Gate type | v2.3 addition |
|---|---|---|---|
| Law 3 — Org Isolation (inbound-side) | Privacy Router content-scan PRE-gate (§4.14) | PRE-gate Row 21 | Detects person-shaped strings inbound before model invocation; prevents routing payloads containing person data to cloud seats when the payload should stay local |

The existing Law 3 entry covering cross-org path isolation (§4.13 + §4.2.1 Row 20) is unchanged.
§4.14 is the *inbound* partner to §4.13's *runtime path* enforcement:
- §4.13 guards cross-org path reads at runtime
- §4.14 guards person-data payloads at model dispatch time

---

## §0.5 Interface Index paired-commit rows (v2.3)

Per §0.5 paired-commit discipline, four new rows land in §0.5 in the same commit as this
amendment. The F-INDEX-STALE PRE-gate (§4.2.1 Row 19) will reject any commit that adds §4.14
without the corresponding §0.5 rows.

| Primitive name | kind | source_section | parent_lock_version |
|---|---|---|---|
| `privacy_router_mechanism` | mechanism | §4 v2.3 | v2.3 |
| `privacy_router_content_scan_pregate` | pre-gate-check | §4 v2.3 §4.14 | v2.3 |
| `F-PRIVACY-CLASSIFIER-ERROR` | failure-code | §4 v2.3 §6 | v2.3 |
| `F-PRIVACY-PAYLOAD-TAGGED-LOCAL-ONLY-BYPASSED` | failure-code | §4 v2.3 §6 | v2.3 |

---

## §9 Test vectors (v2.3)

### §9.36a — Privacy pregate: CLOUD_ELIGIBLE payload passes through unchanged

Input: `payload="What grants exist for urban farms?"`, `seat="scribe"`, `default_routing="cloud"`
Note: v0.1 stub always returns CLASSIFIER_ERROR; this vector documents the CLOUD_ELIGIBLE
contract for v0.2 real-classifier wiring. In v0.1, all payloads route local-only.

Expected (v0.2+): `PrivacyRouteResult(tag=CLOUD_ELIGIBLE, routed_local=False, failure_code=None)`

### §9.36b — Privacy pregate: stub always returns CLASSIFIER_ERROR → routed_local

Input: any payload, any seat
Expected (v0.1 stub): `PrivacyRouteResult(tag=CLASSIFIER_ERROR, routed_local=True, failure_code="F-PRIVACY-CLASSIFIER-ERROR")`

### §9.36c — Privacy pregate: LOCAL_ONLY payload forces local routing

Input: `payload="<name> lives at <address>..."`, `seat="scribe"`, `default_routing="cloud"`
Note: v0.2 real classifier; v0.1 stub fires CLASSIFIER_ERROR before reaching this branch.
Expected (v0.2+): `PrivacyRouteResult(tag=LOCAL_ONLY, routed_local=True, failure_code=None)`

### §9.36d — Privacy pregate: classifier exception is caught and fails closed

Input: classifier raises an unexpected exception
Expected: `PrivacyRouteResult(tag=CLASSIFIER_ERROR, routed_local=True, failure_code="F-PRIVACY-CLASSIFIER-ERROR")`

---

## v2.1 LOCKED state preserved

The text of §4 v2.1 is preserved in its entirety at the LOCK. This amendment appends §4.14
and Row 21; it does not modify any text locked at v2.1. The LOCK sentinel in the file header
updates from "v2.1 LOCKED 2026-04-19" to "v2.3 LOCKED 2026-04-19". v2.2 reserved per
03_blueprint_amendment_plan.md §Item1 planning note (AAT human-delta rider); the v2.2 slot
remains available and is not consumed by this amendment.

---

## L-005 Audit record

### Pass 1: Editor + Judge

**Editor findings:**
- E1 (LOW): §4.14 "Performance target" paragraph could create a future contract conflict if the v0.2 classifier exceeds 50ms. Accepted — 50ms is a soft target documented as advisory.
- E2 (PASS): Gate logic table is clear and unambiguous. Ordering rationale is sound.

**Judge findings (rubric: §4 blueprint amendment criteria + Five Laws + L-006 existence tags):**
- J1 (LOW): §9.36a vector is labeled "v0.2+" — could be confusing. Clarified with note in body.
- J2 (PASS): All Five Laws mapped. Law 3 is primary; Sovereignty Promise Risk-5 Stage-1 architectural ref is correct.
- J3 (PASS): reshape-at-open pre-authorization correctly cited from 05_preflight_existence_audit.md.
- J4 (PASS): Four §0.5 paired rows declared. F-INDEX-STALE will pass.

### Pass 2: Red Team + Reasoner

**Red Team findings:**
- RT1 (LOW): Adversarial scenario — malicious caller passes `routed_local=False` result from a mocked classifier to bypass the gate. Mitigation: gate result is computed inside `run_privacy_pregate`; the caller receives a read-only `PrivacyRouteResult` dataclass and cannot inject a pre-cooked result. Closed.
- RT2 (MED): No admin-risk append for `F-PRIVACY-CLASSIFIER-ERROR` means persistent classifier failures are silent. Accepted per §4.14 v0.1 rationale + v0.2 deferral note. Operator can observe via rails report (4b) when it lands.
- RT3 (PASS): Fail-closed semantics are unambiguous — every non-CLOUD_ELIGIBLE path forces local routing.

**Reasoner findings:**
- R1 (PASS): Bypass attempt detection logic correctly identifies the gap between gate output and orchestrator action.
- R2 (PASS): Classifier stub return type matches contract.

VERDICT: PASS-WITH-CONDITIONS. RT2 accepted under v0.1 deferred-admin-risk rationale. Status: LOCK-READY.

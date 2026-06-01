---
title: Blueprint §4 Logician — Amendment v2.x.5 (CC-007 closure — Seat-local provider HTTP egress wrapped by `enforce_outbound_boundary`; F-CLASS-OUTBOUND-BOUNDARY sub-tag extensions on F-CLASS-ROUTING-INDETERMINATE + F-CLASS-CLOUD-RECEIVED-CONFIDENTIAL; AST-lint R-NO-DIRECT-PROVIDER-HTTP rule landed)
filed: 2026-05-16
operator: Josh Inklovich
amendment_status: LOCKED 2026-05-16T08:00:00Z. L-005 strict two-cycle CLOSED with FULL live cross-family rigor (Editor=Llama-3.3-70B/Groq + Judge=Gemini-2.5-Pro/Google + Red Team=GPT-OSS-120B/Groq via mcp__Control_your_Mac__osascript → openclaw infer model run --gateway bridge). Cycle 1: Editor REQUIRES_FIX (8 LOW/MED readability — all FOLD-IN-AT-V2) + Judge READY_TO_LOCK 99/100 (1 LOW DC — FOLD-IN-AT-V2) + Red Team ESCALATE blocking:true (23 findings: 5 HIGH + 12 MED + 6 LOW; all FOLD-IN-AT-V2 with concrete text-level closures per row-170 transparent disposition). Cycle 2: Editor PASS unanimous (8/8 VERIFIED_CLOSED + 0 NEW) + Judge READY_TO_LOCK 100/100 (+1 from Cycle 1; 2 LOW DC-CYCLE2 RECOMMEND_FOLD_IN_AT_LOCK applied at §12.1/§12.2) + Red Team ESCALATE blocking:true → REQUIRES_FIXES blocking:false at row-170 (8 NEW probes + 7 PARTIAL_CLOSURE_REMAINS — all 15 items FOLDED-IN-AT-LOCK at §12.3..§12.11 with explicit text-level mechanism; 1 DEFERRED-to-v2-O.5 for runtime-guard wrapper on dynamic-import shapes). Compound-LOCK paired-commit with §0.5 v27 amendment (rows 539-548 + Cycle 2 fold-in additions for `.signed_file_invalid` + `.cedar_load_failure` sub-tag-extension records on existing F-CLASS-REGISTER-SIGNATURE-INVALID + F-CLASS-CLOUD-RECEIVED-CONFIDENTIAL row ownership). SEVENTEENTH substantive v0.1+v0.2 round to LOCK at FULL live cross-family rigor (after WS-D + WS-F + WS-E + WS-H + WS-G + WS-K + WS-C-M1 + WS-L + WS-I + §4 v2.x.1 + §14 v1 + §15 v1 + §4 v2.x.2 + §11 v1.1 + §17 v1 + Funding Goal SPEC + §16 v1 + §4 v2.x.3 + Reflection Packet v0.2 + Wave 1 card LOCKs + §18 v1.1 precedents).
parent_lock: pipeline/blueprint/v0.1/section_04_v2_x_amendment.md  (§4 v2.x LOCKED 2026-05-10 row 193)
parent_lock_row: 193
predecessor_locks:
  - pipeline/blueprint/v0.1/section_04_v2_x_1_amendment.md          (§4 v2.x.1 LOCKED 2026-05-10 row 198) — R-ARCHIVIST-NO-CANONICAL-MUTATE sub-tag extension precedent
  - pipeline/blueprint/v0.1/section_04_v2_x_3_amendment.md          (§4 v2.x.3 LOCKED 2026-05-15) — F-REPORT-* registration precedent
  - pipeline/architecture/v0.1/architecture_v7_0_10_amendment.md    (v7.0.10 LOCKED 2026-05-11 row 215) — 16-primitive F-CLASS-* family; three-posture routing
  - pipeline/handoffs/cowork_cc007_preflight_design_memo_2026-05-16.md  (CC-007 design memo + operator-ratified OD-1..5 picks; default-aligned)
parent_handoff: pipeline/handoffs/cowork_cc007_architectural_preflight_2026-05-16.md
parent_decision: pipeline/handoffs/tandem_qa_qc_remediation_decisions_2026-05-16.md  (decision #4)
amendment_class: narrow-corrective + sub-tag-extension (mirrors §4 v2.x.1 row 198 precedent — extends existing F-CLASS-* primitive ownership with new enumerated sub-tags + dedicated drift-test bindings + AST-lint rule registration; NO new top-level F-CLASS-* row; family roster stays at 16)
precedent_pattern: §4 v2.x.1 row 198 (R-ARCHIVIST-NO-CANONICAL-MUTATE enumeration extension under existing F-ARCHIVIST-AUTO-APPLY-ATTEMPTED ownership — same shape: existing primitive gains enumerated sub-tags with dedicated drift-test bindings; AST-lint rule extends DEFAULT_RULES; no new top-level row).
threat_severity_at_v0_1_beta: CRITICAL — closure target is the sovereignty claim. Seat-local provider HTTP egress (`stdlib_http_post` in Scribe/Judge + `_ProductionHTTPCaller` in Red Team) bypasses the F-CLASS-* PRE/POST gate chain enforced at `pipeline/orchestrator/router.py:465-557`. Confidential-tagged classification register entries could egress unscanned. Closure = wrap at the provider-callable layer (NOT recurse through `call_seat`). Operator-confirmed: extract shared F-CLASS boundary enforcement into `pipeline/orchestrator/provider_boundary.py::enforce_outbound_boundary` + inject as the production E-017 seam at each seat's subprocess wire-up.
purpose: Close the seat-local provider HTTP egress sovereignty bypass identified by CC-007 (Tandem QA/QC pressure audit 2026-05-16 Codex re-verification + Claude Code half). Land `pipeline/orchestrator/provider_boundary.py` with the shared wrapper; register three sub-tag extensions on existing F-CLASS-* primitives; register AST-lint rule R-NO-DIRECT-PROVIDER-HTTP; extend three seat envelope schemas to carry `classification_context_json` + `posture` fields; refactor `stdlib_http_post` / `_ProductionHTTPCaller` egress functions out of `pipeline/seats/{scribe,judge,red_team}/provider_*.py`.
operator_ratified_decisions:
  - "OD-1 = sub-tag extensions on existing F-CLASS-* primitives (NOT new top-level rows). Family roster stays at 16."
  - "OD-2 = raise typed exception (`OutboundBoundaryRefusedError`) on PRE-gate refusal — mirrors router.ClassificationBoundaryError shape; callers that catch ClassificationBoundaryError can use same handler."
  - "OD-3 = unify Anthropic/Google HttpPostCallable(bytes) + Groq HTTPCaller.post_json(dict) to single OutboundCallable(bytes) Protocol. Refactor `call_groq` body to encode dict→bytes once before calling out."
  - "OD-4 = grandfather `pipeline/validation/**` dispatch scripts (Thesis-pipeline helpers — out of sovereignty scope; AST-lint allowlist excludes those paths)."
  - "OD-5 = refactor router._dispatch_with_classification_boundary to call enforce_outbound_boundary directly. Single source of truth; eliminates parallel-implementation drift."
companion_code_to_land_at_lock:
  - "pipeline/orchestrator/provider_boundary.py (NEW — enforce_outbound_boundary + OutboundCallable Protocol + ClassificationContext mirror + OutboundBoundaryRefusedError + stdlib_urlopen_caller — sole permitted urllib call site in pipeline/; PRE + POST helpers compose existing f_class_outbound_boundary + f_class_routing_indeterminate predicate chain)"
  - "pipeline/linting/r_no_direct_provider_http.py (NEW — AST visitor + FORBIDDEN_PRIMITIVES MappingProxyType + ALLOWLISTED_FILES frozenset + 5 sub-tags: .urlopen / .requests_lib / .httpx_lib / .aiohttp / .raw_socket)"
  - "pipeline/linting/ast_lint.py (UPDATED — _section_04_v2_x_5_rules() lazy-import block extends DEFAULT_RULES with R_NO_DIRECT_PROVIDER_HTTP)"
  - "pipeline/vault/policies/outbound_boundary.cedar (NEW — Cedar rules per sub-tag matching the disposition table at §4.3.5)"
  - "pipeline/seats/scribe/provider_anthropic.py (UPDATED — DELETE stdlib_http_post + urllib import; HttpPostCallable Protocol REPLACED by `from pipeline.orchestrator.provider_boundary import OutboundCallable as HttpPostCallable`; call_anthropic_scribe body unchanged)"
  - "pipeline/seats/judge/provider_google.py (UPDATED — DELETE stdlib_http_post + urllib import; same Protocol replacement as Scribe)"
  - "pipeline/seats/red_team/provider_groq.py (UPDATED — DELETE _ProductionHTTPCaller class + make_production_http_caller function; HTTPCaller Protocol REPLACED with OutboundCallable; call_groq body refactored to encode dict→bytes once before http_post call per OD-3)"
  - "pipeline/seats/scribe/seat.py (UPDATED — ScribeEnvelope gains classification_context_json: str + posture: Literal[...]; subprocess production wire-up wraps stdlib_urlopen_caller with enforce_outbound_boundary at __main__ binding time)"
  - "pipeline/seats/judge/seat.py (UPDATED — JudgeEnvelope same fields + wire-up)"
  - "pipeline/seats/red_team/seat.py (UPDATED — RedTeamEnvelope same fields; seat.py:269 call site wraps http_post=enforce_outbound_boundary(stdlib_urlopen_caller, classification_context=..., posture=...))"
  - "pipeline/orchestrator/router.py (UPDATED per OD-5 — _dispatch_with_classification_boundary refactors to call enforce_outbound_boundary; deletes redundant _enforce_cloud_boundary_pre + _enforce_cloud_boundary_post body in favor of single source of truth; single allowlist entry retained for stdlib_urlopen_caller's import site)"
companion_tests_to_land_at_lock:
  - "tests/orchestrator/test_provider_boundary.py (NEW — 8 unit tests: missing_context refusal + classification_deny refusal + post_drift refusal + happy-path PRE + happy-path POST + local-only posture refusal + sub-tag string formatting + Logfire span emission)"
  - "tests/orchestrator/test_provider_boundary_split_context.py (NEW — 5 tests: allow-list field-path PASS + non-allow-list FAIL + applicant-fact scan PASS + applicant-fact scan FAIL + dual-sign extension at write time)"
  - "tests/linting/test_r_no_direct_provider_http.py (NEW — 5x5 sub-tag matrix: urlopen direct + requests.post + httpx.post + aiohttp.ClientSession.post + http.client.HTTPSConnection; allowlist round-trip; clean-module; dead-code rule fires; FORBIDDEN_PRIMITIVES table immutable)"
  - "tests/seats/scribe/test_provider_anthropic.py (UPDATED — drop stdlib_http_post parametrize fixtures; existing 12 invocation tests preserved with HttpPostCallable=OutboundCallable Protocol shim; 3 NEW compose-with-wrapper tests)"
  - "tests/seats/judge/test_provider_google.py (UPDATED — same shape as Scribe; 3 NEW compose tests)"
  - "tests/seats/red_team/test_r3_seat_provider_wiring.py (UPDATED — Protocol-shape change for OutboundCallable bytes-body unification; 3 NEW compose tests)"
  - "tests/seats/judge/test_init_surface.py + tests/seats/judge/test_whole_section_capstone.py + tests/seats/scribe/test_whole_section_capstone.py (UPDATED — remove `stdlib_http_post` from expected export-list assertions)"
done_definition:
  - "Three sub-tag strings registered: .outbound_boundary_missing_context (under F-CLASS-ROUTING-INDETERMINATE) + .outbound_boundary_classification_deny (under F-CLASS-CLOUD-RECEIVED-CONFIDENTIAL) + .outbound_boundary_post_drift (under F-CLASS-CLOUD-RECEIVED-CONFIDENTIAL)."
  - "F-CLASS-* family roster count unchanged at 16. F-CLASS-COVERAGE-INCOMPLETE META-gate scope unchanged."
  - "pipeline/orchestrator/provider_boundary.py imports cleanly + module-load AST-lint allowlist verification passes."
  - "R-NO-DIRECT-PROVIDER-HTTP rule fires on every forbidden primitive in non-allowlisted files; clears on allowlisted module."
  - "All three seat provider modules contain ZERO urllib imports + ZERO `urlopen` references after refactor."
  - "All three seat envelope schemas accept classification_context_json + posture fields; envelope round-trip tests PASS."
  - "Router.call_seat() under OD-5 refactor produces byte-identical behavior to pre-refactor for the existing test surface (no regression)."
  - "Cycle 1 fold-ins applied to amendment text per row-170 transparent disposition pattern; Cycle 2 fold-ins applied at LOCK."
  - "audit_v{1,2}_synthesis.md authored at pipeline/validation/cc007_thesis_2026-05-16/."
  - "Daily log + session_metrics row + memory file + MEMORY.md index updated at LOCK."
cowork_thesis_dispatch_status: CYCLE 1 PENDING — dispatched at LOCK author's session. Cycle 2 (verification) fires post-fold-in.
ws_dispatch: §4 v2.x.5 corrective dispatch (Cowork session 2026-05-16T23:55:00 + continuation) — modeled on §4 v2.x.1 narrow-corrective-amendment cadence (lock_history row 198).
session_metrics: pipeline/metrics/session_log.jsonl
---

# Amendment v2.x.5 — CC-007 closure (Seat-local provider HTTP egress wrapped by `enforce_outbound_boundary`)

## §0. Amendment intent + scope

This narrow-corrective amendment **closes the seat-local provider HTTP egress sovereignty bypass** identified during the Tandem QA/QC pressure audit (2026-05-16 Codex re-verification + Claude Code half findings CC-007). Three production paths in `pipeline/seats/{scribe,judge,red_team}/provider_*.py` issue `urllib.request.urlopen` POSTs directly to cloud-frontier endpoints (api.anthropic.com / generativelanguage.googleapis.com / api.groq.com) without invoking the F-CLASS-* PRE/POST gate chain that `pipeline/orchestrator/router.py:_dispatch_with_classification_boundary` enforces for the router-side `call_seat` path. The bypass collapses the sovereignty claim — Confidential-tagged classification register entries can ride into a cloud HTTPS POST without F-CLASS gate scanning.

The amendment lands the operator-confirmed fix: **extract shared F-CLASS boundary enforcement into a single injectable wrapper** (`pipeline/orchestrator/provider_boundary.py::enforce_outbound_boundary`) and wire it as the production E-017 seam at each seat's subprocess wire-up. The wrapper composes the existing F-CLASS-* predicate chain at `pipeline/logician/gates/f_class_outbound_boundary.py` + `f_class_routing_indeterminate.py` (16-primitive family per v7.0.10 §5) rather than redefining it. Failure codes land as **sub-tag extensions** on existing F-CLASS-* primitives per the §4 v2.x.1 row 198 narrow-corrective-extension precedent (R-ARCHIVIST-NO-CANONICAL-MUTATE). No new top-level F-CLASS-* row; family roster stays at 16.

**Why not `call_seat`-routing.** Seats invoke providers; `call_seat` invokes seats. If a seat-local provider call routes through `call_seat`, it recurses into the seat that owns it (infinite loop). The right abstraction layer is **at the provider-callable boundary**, not the seat boundary. Wrapping at the `HttpPostCallable` / unified `OutboundCallable` E-017 seam composes the F-CLASS gates inside the subprocess Python process (same context as urllib egress; no IPC overhead) and preserves the existing injected-seam discipline.

**What this amendment lands at LOCK.**

1. New module `pipeline/orchestrator/provider_boundary.py` exposing:
   - `enforce_outbound_boundary(inner: OutboundCallable, *, classification_context: ClassificationContext | None, posture: Literal["frontier_eligible", "split_context_hybrid", "local_only_sovereign"]) -> OutboundCallable`
   - `stdlib_urlopen_caller(*, url, headers, body, timeout_seconds) -> tuple[int, bytes]` — sole permitted `urllib.request.urlopen` call site in `pipeline/` after refactor (enforced by R-NO-DIRECT-PROVIDER-HTTP allowlist).
   - `ClassificationContext` mirror shape (so seat subprocesses can construct it from envelope JSON without importing `pipeline.orchestrator.router`).
   - `OutboundCallable` Protocol unifying the Anthropic/Google `HttpPostCallable(bytes body)` and Groq's `HTTPCaller.post_json(dict body)` shapes per OD-3.
   - `OutboundBoundaryRefusedError` typed exception (mirrors `router.ClassificationBoundaryError` shape per OD-2).

2. Three sub-tag-string registrations on existing F-CLASS-* primitives per OD-1:

   | Sub-tag | Owner top-level | Stage | M13? |
   |---------|------------------|-------|------|
   | `.outbound_boundary_missing_context` | `F-CLASS-ROUTING-INDETERMINATE` | PRE | NO (structural; caller has no proof of classification) |
   | `.outbound_boundary_classification_deny` | `F-CLASS-CLOUD-RECEIVED-CONFIDENTIAL` | PRE | M13 audited (admin-risk HIGH) |
   | `.outbound_boundary_post_drift` | `F-CLASS-CLOUD-RECEIVED-CONFIDENTIAL` | POST | M13 audited (admin-risk HIGH) |

3. New AST-lint rule `R-NO-DIRECT-PROVIDER-HTTP` at `pipeline/linting/r_no_direct_provider_http.py` (mirrors §15 R-ARCHIVIST-NO-CANONICAL-MUTATE shape — 5 sub-tags pattern):
   - `.urlopen` — `urllib.request.urlopen` / `urllib.request.Request` followed by urlopen.
   - `.requests_lib` — `requests.{post,get,put,delete,patch,head,request}` + `Session.*`.
   - `.httpx_lib` — `httpx.{post,get,put,delete}` + `Client.*` / `AsyncClient.*`.
   - `.aiohttp` — `aiohttp.ClientSession.*` + `aiohttp.request`.
   - `.raw_socket` — `socket.socket().connect()` followed by HTTP-style writes; `http.client.HTTPConnection` / `HTTPSConnection`.
   - **Allowlist:** `{"pipeline/orchestrator/provider_boundary.py", "pipeline/orchestrator/router.py"}` only. Per OD-5 router-de-dup, the router entry collapses to the wrapper's import; the second allowlist entry is retained for the `stdlib_urlopen_caller` definition site referenced by the wrapper.
   - **Grandfathered (OD-4):** `pipeline/validation/**` dispatch scripts (Thesis-pipeline helpers; out of sovereignty scope).

4. Three seat envelope schema sub-tag-extensions: `classification_context_json: str` + `posture: Literal["frontier_eligible", "split_context_hybrid", "local_only_sovereign"]` on `ScribeEnvelope`, `JudgeEnvelope`, `RedTeamEnvelope`.

5. Refactor surface in `pipeline/seats/{scribe,judge,red_team}/provider_*.py`: DELETE `stdlib_http_post` / `_ProductionHTTPCaller` + `make_production_http_caller` + `urllib` imports. Production wire-up moves OUT to seat subprocess `__main__` binding sites; each binds `wrapped_http_post = enforce_outbound_boundary(stdlib_urlopen_caller, classification_context=ClassificationContext.from_envelope_json(...), posture=envelope.posture)` and passes `wrapped_http_post` into `call_anthropic_scribe` / `call_google_judge` / `call_groq`.

6. Router-side de-duplication per OD-5: `router._dispatch_with_classification_boundary` refactors to call `enforce_outbound_boundary(_http_post, classification_context=..., posture=...)` once at dispatch entry; the existing `_enforce_cloud_boundary_pre` + `_enforce_cloud_boundary_post` bodies collapse into the wrapper's PRE/POST helpers.

## §1. Wrapper signature + behavior contract

```python
# pipeline/orchestrator/provider_boundary.py

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Final, Literal, Mapping, Protocol

from pipeline.logician.gates.f_class_outbound_boundary import (
    ClassifiedValue,
    OutboundBoundaryResult,
    SlotPosition,
    check_class_cloud_received_confidential,
    check_class_cloud_received_opaque_slot_filled,
    check_class_high_stakes_flag_leak,
    check_class_slot_id_non_opaque,
)
from pipeline.logician.gates.f_class_routing_indeterminate import (
    CallInput,
    check_class_routing_indeterminate,
)

# -- Sub-tag string constants (per OD-1 — sub-tag extensions on existing rows). --
F_CLASS_OUTBOUND_BOUNDARY_MISSING_CONTEXT: Final[str] = (
    "F-CLASS-ROUTING-INDETERMINATE.outbound_boundary_missing_context"
)
F_CLASS_OUTBOUND_BOUNDARY_CLASSIFICATION_DENY: Final[str] = (
    "F-CLASS-CLOUD-RECEIVED-CONFIDENTIAL.outbound_boundary_classification_deny"
)
F_CLASS_OUTBOUND_BOUNDARY_POST_DRIFT: Final[str] = (
    "F-CLASS-CLOUD-RECEIVED-CONFIDENTIAL.outbound_boundary_post_drift"
)

Posture = Literal["frontier_eligible", "split_context_hybrid", "local_only_sovereign"]


@dataclass(frozen=True, kw_only=True)
class ClassificationContext:
    """Per-call classification proof. Mirrors router.ClassificationContext.

    Lives here so seat subprocesses can construct it from envelope JSON
    without importing pipeline.orchestrator.router (which has yaml +
    file-system side-effects unsuitable for subprocess startup).
    """

    inputs: tuple[CallInput, ...]
    classified_values: tuple[ClassifiedValue, ...] = field(default_factory=tuple)
    slot_positions: tuple[SlotPosition, ...] = field(default_factory=tuple)
    high_stakes_flag_values: tuple[str, ...] = field(default_factory=tuple)
    post_fill_draft: bool = False

    @classmethod
    def from_envelope_json(cls, json_str: str) -> "ClassificationContext":
        """Decode envelope-encoded JSON into a frozen ClassificationContext.

        Raises ValueError on malformed JSON or missing required keys.
        """
        ...


class OutboundCallable(Protocol):
    """Unified production HTTP POST seam (closes Anthropic/Google + Groq shape gap per OD-3).

    Body is bytes; return is (status, bytes). Caller (provider module)
    encodes dict→bytes once before invocation.
    """

    def __call__(
        self,
        *,
        url: str,
        headers: Mapping[str, str],
        body: bytes,
        timeout_seconds: float,
    ) -> tuple[int, bytes]: ...


class OutboundBoundaryRefusedError(RuntimeError):
    """PRE-gate refused egress OR POST-gate detected drift. Typed exception
    mirroring router.ClassificationBoundaryError shape per OD-2.

    Carries:
      - failure_code: the F-CLASS-* sub-tag string (one of the three module constants).
      - detail: human-readable explanation (no Confidential content per Law 3).
    """

    def __init__(self, failure_code: str, detail: str) -> None:
        self.failure_code = failure_code
        self.detail = detail
        super().__init__(f"{failure_code}: {detail}")


def enforce_outbound_boundary(
    inner: OutboundCallable,
    *,
    classification_context: ClassificationContext | None,
    posture: Posture,
) -> OutboundCallable:
    """Wrap an HTTP POST callable with F-CLASS PRE/POST outbound-boundary gates.

    Returns a NEW OutboundCallable preserving the inner's Protocol shape.

    Behavior:
      1. PRE-1: if posture == "local_only_sovereign", refuse unconditionally
         (cloud egress structurally absent under Local-Only; firing = bug-class signal).
      2. PRE-2: if classification_context is None, refuse with
         F-CLASS-ROUTING-INDETERMINATE.outbound_boundary_missing_context.
      3. PRE-3: dispatch through the existing F-CLASS predicate chain
         (mirrors router._enforce_cloud_boundary_pre):
           - check_class_routing_indeterminate (PRE)
           - blocking-class scan on inputs (confidential / operator_flagged → refuse)
           - check_class_slot_id_non_opaque (defense-in-depth per v7.0.10 §2.2)
           - check_class_cloud_received_confidential (against classified_values)
           - check_class_high_stakes_flag_leak (PRE)
           - if posture == "split_context_hybrid":
               check_class_split_context_allowlist (per v7.0.10 §5.3)
               check_class_split_context_leak (per v7.0.10 §5.3)
      4. INVOKE: call inner(url=..., headers=..., body=..., timeout_seconds=...).
      5. POST: dispatch through the existing F-CLASS POST predicate chain
         (mirrors router._enforce_cloud_boundary_post):
           - check_class_cloud_received_confidential (against response bytes)
           - check_class_cloud_received_opaque_slot_filled (defense-in-depth)
           - check_class_high_stakes_flag_leak (POST)
      6. PRE refusal → raise OutboundBoundaryRefusedError (no urllib call).
      7. POST refusal → raise OutboundBoundaryRefusedError with
         .outbound_boundary_post_drift sub-tag (response bytes discarded).

    See §4.3.5 below for the full disposition matrix.
    """
    ...


def stdlib_urlopen_caller(
    *,
    url: str,
    headers: Mapping[str, str],
    body: bytes,
    timeout_seconds: float,
) -> tuple[int, bytes]:
    """Sole permitted urllib.request.urlopen call site in pipeline/.

    Production seats wire enforce_outbound_boundary(stdlib_urlopen_caller, ...)
    at subprocess wire-up. This function is the ONLY module in pipeline/
    permitted to call urllib.request.urlopen by R-NO-DIRECT-PROVIDER-HTTP
    allowlist (alongside router.py per OD-5 dedup transition).
    """
    import urllib.error
    import urllib.request

    req = urllib.request.Request(
        url, data=body, headers=dict(headers), method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout_seconds) as resp:  # noqa: S310
            return int(resp.status), resp.read()
    except urllib.error.HTTPError as exc:
        return int(exc.code), exc.read() or b""
```

## §2. Sub-tag string conventions (Cycle 1 E-prefix readability anchor)

The three sub-tag strings follow the §4 v2.x.1 §2.2 dot-prefixed-substring wire-form convention. The leading dot is preserved at emit time so downstream tooling that reads `failure_code` for sub-tag membership can rely on substring match.

`F-CLASS-ROUTING-INDETERMINATE` (existing top-level; v7.0.7 §5.1 row 6) extends with:

- `.outbound_boundary_missing_context` — caller did not pass `classification_context` to `enforce_outbound_boundary`; no F-CLASS proof exists. Structural (no M13).

`F-CLASS-CLOUD-RECEIVED-CONFIDENTIAL` (existing top-level; v7.0.7 §5.1 row 7) extends with:

- `.outbound_boundary_classification_deny` — PRE-gate predicate chain refused egress before urllib invocation. Fires for: Local-Only posture invoked; blocking-class input present; classified-value-in-payload PRE-scan hit; Split-Context Hybrid allow-list miss.
- `.outbound_boundary_post_drift` — POST-gate predicate chain detected drift in the response payload after urllib egress. Fires for: classified-value-in-response POST-scan hit; opaque-slot-token POST-scan hit; high-stakes-token POST-scan hit. Response bytes are discarded; seat exits EXIT_GATE_FAIL=2.

The dotted-suffix convention matches §4 v2.x.1 row 198 enumeration extension (`F-ARCHIVIST-AUTO-APPLY-ATTEMPTED.low_level_rename_replace` et al.) — the failure-code attribution travels with the diagnostic regardless of how the reason_tag is read.

## §3. AST-lint rule R-NO-DIRECT-PROVIDER-HTTP

### §3.1 Target glob + scope discipline

Target glob: `pipeline/**/*.py` minus the allowlist.

**Allowlist (CLOSED SET):**

```python
ALLOWLISTED_FILES: Final[frozenset[str]] = frozenset({
    "pipeline/orchestrator/provider_boundary.py",  # Sole permitted urllib.urlopen call site
    "pipeline/orchestrator/router.py",             # Existing router; retained for stdlib_urlopen_caller import
})
```

**Grandfathered glob exclusion (OD-4):** `pipeline/validation/**/*.py` — Thesis-pipeline dispatch scripts (helpers, not production paths). The exclusion is documented at module load time; AST visitor early-returns on path match.

### §3.2 Sub-tags (5; mirrors §15 R-ARCHIVIST-NO-CANONICAL-MUTATE 5-sub-tag precedent)

| Primitive (concrete Call.func shape) | Sub-tag |
|--------------------------------------|---------|
| `urllib.request.urlopen(...)` | `.urlopen` |
| `urllib.request.Request(...)` followed by `urlopen` | `.urlopen` |
| `requests.post`, `requests.get`, `requests.put`, `requests.delete`, `requests.patch`, `requests.head`, `requests.request`, `Session.post`, `Session.get`, `Session.put`, `Session.delete` | `.requests_lib` |
| `httpx.post`, `httpx.get`, `httpx.put`, `httpx.delete`, `httpx.Client.post`, `httpx.AsyncClient.post` | `.httpx_lib` |
| `aiohttp.ClientSession.post`, `aiohttp.ClientSession.get`, `aiohttp.ClientSession.put`, `aiohttp.ClientSession.delete`, `aiohttp.request` | `.aiohttp` |
| `socket.socket().connect()` followed by `sendall` / `send` to TCP port 80/443; `http.client.HTTPConnection`, `http.client.HTTPSConnection` | `.raw_socket` |

Sub-tag count = 5; concrete call-shape coverage = 25.

### §3.3 FORBIDDEN_PRIMITIVES table immutability (RT-14 precedent)

The `FORBIDDEN_PRIMITIVES` mapping is exported as a `types.MappingProxyType` view over a module-private mutable dict. Downstream consumers cannot silence the rule by reassignment. Acceptance test `test_forbidden_primitives_table_is_immutable` pins the contract.

### §3.4 Static-analysis limitations (intentionally out-of-scope under v7 A1+A4)

The resolver handles direct `ast.Attribute` + bound `ast.Name` shapes; it does NOT track:

- `getattr(urllib.request, 'urlopen')(...)` — dynamic attribute lookup.
- `urllib.request.__dict__['urlopen'](...)` — subscript on module dict.
- `_f = urllib.request.urlopen; _f(...)` — local-name reassignment.
- `sys.modules['urllib.request'].urlopen(...)` — indirect via subscript.
- `from urllib.request import *` — wildcard imports.

These shapes are bounded under v7 LOCKED A1 (single-client) + A4 (operator-trusted preflight). Multi-contributor / v2 multi-tenant promotion to MED severity lands via Section O.5 v2 hardening (not numeric §0.5).

### §3.5 Drift tests (three per sub-tag per §4 v2.x.1 row 198 named-drift-test discipline)

Per the §4 v2.x.1 row 198 sub-tag-extension precedent: every sub-tag binds to dedicated drift tests under `tests/linting/test_r_no_direct_provider_http.py`. Five sub-tags × 5 forbidden-primitive concrete shapes = 25 named drift tests at LOCK; plus allowlist round-trip + clean-module + dead-code + immutability tests.

## §4. Provider-module refactor + envelope-schema sub-tag extensions

### §4.1 Scribe — `pipeline/seats/scribe/provider_anthropic.py`

**Before (current):** `stdlib_http_post` at L176-191 issues urllib egress. `call_anthropic_scribe` at L196-324 invokes via injected `HttpPostCallable` seam.

**After (this amendment):**
- DELETE `stdlib_http_post` function entirely.
- DELETE `import urllib.error` + `import urllib.request`.
- REPLACE `HttpPostCallable` Protocol with `from pipeline.orchestrator.provider_boundary import OutboundCallable as HttpPostCallable` (preserves the public name in `__all__` for backward compat; existing test fixtures injecting stubs of the same shape continue to work).
- `call_anthropic_scribe` body unchanged.

**Envelope schema sub-tag extension (`ScribeEnvelope`):**
```python
@dataclass(frozen=True, kw_only=True, slots=True)
class ScribeEnvelope:
    # ... existing fields per §7 §7.2 ...
    classification_context_json: str  # NEW — canonical JSON of ClassificationContext per §4.4 below
    posture: Literal["frontier_eligible", "split_context_hybrid", "local_only_sovereign"]  # NEW
```

`F-SCRIBE-ENVELOPE-MALFORMED` predicate extends to require both new fields non-empty; missing or malformed → fail-closed exit 2 (existing F-SCRIBE-ENVELOPE-MALFORMED path; no new failure-code).

**Subprocess wire-up (new at seat.py __main__ binding block):**
```python
from pipeline.orchestrator.provider_boundary import (
    enforce_outbound_boundary,
    stdlib_urlopen_caller,
    ClassificationContext,
)

def _build_production_anthropic_call(envelope: ScribeEnvelope) -> AnthropicCallCallable:
    classification_context = ClassificationContext.from_envelope_json(
        envelope.classification_context_json
    )
    wrapped_http_post = enforce_outbound_boundary(
        stdlib_urlopen_caller,
        classification_context=classification_context,
        posture=envelope.posture,
    )

    def anthropic_call(*, binding, compiled_prompt, org_slug):
        return call_anthropic_scribe(
            binding=binding,
            compiled_prompt=compiled_prompt,
            org_slug=org_slug,
            key_retrieve=_production_key_retrieve,
            http_post=wrapped_http_post,
            clock=time.time,
            sleep=time.sleep,
        )

    return anthropic_call
```

### §4.2 Judge — `pipeline/seats/judge/provider_google.py`

Isomorphic to Scribe (§4.1). Same envelope-schema delta on `JudgeEnvelope`. Same wire-up at `pipeline/seats/judge/seat.py`. `call_google_judge` body unchanged after stdlib_http_post deletion.

The existing F_PIPE_08 cross-family discipline (Judge family ≠ Scribe family) at the seat-runner layer is orthogonal to F-CLASS-OUTBOUND-BOUNDARY and is untouched by this amendment.

### §4.3 Red Team — `pipeline/seats/red_team/provider_groq.py`

**Protocol unification per OD-3:**
- REPLACE `HTTPCaller` Protocol (with `post_json(*, url, headers, json_body: Mapping[str, object], timeout_sec) -> tuple[int, str]`) with `from pipeline.orchestrator.provider_boundary import OutboundCallable as HTTPCaller`.
- DELETE `_ProductionHTTPCaller` class at L258-292.
- DELETE `make_production_http_caller()` function at L290-292.
- REFACTOR `call_groq` body to encode dict→bytes once before the http_post call:
  ```python
  def call_groq(*, http_post: OutboundCallable, api_key, system_prompt, user_prompt, ...):
      body = _build_request_body(model=model, system_prompt=system_prompt,
                                 user_prompt=user_prompt, max_tokens=max_tokens)
      body_bytes = json.dumps(body, separators=(",", ":"),
                              ensure_ascii=False).encode("utf-8")
      headers = _build_headers(api_key=api_key)
      try:
          status, raw_bytes = http_post(
              url=f"{base_url}/chat/completions",
              headers=headers,
              body=body_bytes,
              timeout_seconds=timeout_sec,
          )
      except Exception as e:
          return GroqProviderResult(
              status_code=0, raw_text="", parsed={},
              failure_code=F_RT_PROVIDER_TRANSPORT_FAIL,
              failure_detail=f"{type(e).__name__}: {str(e)[:200]}",
          )
      raw_text = raw_bytes.decode("utf-8", errors="replace")
      # ... (rest of status-code branching unchanged)
  ```

**Subprocess wire-up at seat.py:269:**
```python
provider_result = call_groq(
    http_post=enforce_outbound_boundary(
        stdlib_urlopen_caller,
        classification_context=ClassificationContext.from_envelope_json(
            envelope.classification_context_json
        ),
        posture=envelope.posture,
    ),
    api_key=api_key,
    system_prompt=SYSTEM_PROMPT,
    user_prompt=user_prompt,
    model=model,
    max_tokens=max_tokens,
)
```

### §4.4 Envelope schema serialization shape

`classification_context_json` carries a canonical-JSON-encoded `ClassificationContext` with the shape:

```json
{
  "inputs": [{"field_path": "string", "class_name": "public|shareable|confidential|operator_flagged", "locked_by": "string"}],
  "classified_values": [{"value": "string", "class_name": "string", "field_path": "string"}],
  "slot_positions": [{"slot_id": "digits", "pre_marker": "string", "post_marker": "string"}],
  "high_stakes_flag_values": ["string", "..."],
  "post_fill_draft": false
}
```

Canonical-JSON: `sort_keys=True, separators=(",", ":"), ensure_ascii=False, UTF-8`. Subprocess decode via `ClassificationContext.from_envelope_json(...)` — `json.loads` + dataclass construction with type validation; raises `ValueError` on malformed shape.

Under Local-Only / Sovereign posture: the orchestrator MUST still emit a syntactically-valid `classification_context_json` block (empty `inputs` array is acceptable — the wrapper refuses unconditionally on Local-Only posture and never reaches the inputs scan). This preserves envelope-schema invariants across postures.

### §4.5 Disposition matrix (full)

| Failure scenario | Failure code (sub-tag) | Stage | Disposition |
|------------------|------------------------|-------|-------------|
| `classification_context is None` AND posture != local_only_sovereign | `F-CLASS-ROUTING-INDETERMINATE.outbound_boundary_missing_context` | PRE | HARD_BLOCK; NO M13 (structural — caller has no proof; even M13 cannot create that proof retroactively) |
| Posture == `local_only_sovereign` AND wrapper invoked | `F-CLASS-CLOUD-RECEIVED-CONFIDENTIAL.outbound_boundary_classification_deny` | PRE | HARD_BLOCK; NO M13 (Local-Only structural; firing = bug or attack) |
| `check_class_routing_indeterminate` fails (any input has unrecognized class_name) | `F-CLASS-ROUTING-INDETERMINATE` (existing top-level) | PRE | M13 audited (admin-risk MEDIUM) |
| Any input in `classification_context.inputs` has `class_name ∈ {confidential, operator_flagged}` | `F-CLASS-CLOUD-RECEIVED-CONFIDENTIAL.outbound_boundary_classification_deny` | PRE | P0 / M13 audited (admin-risk HIGH) |
| `check_class_cloud_received_confidential` finds a tagged literal in the prompt payload | `F-CLASS-CLOUD-RECEIVED-CONFIDENTIAL` (existing top-level) | PRE | P0 / M13 audited (admin-risk HIGH) |
| `check_class_slot_id_non_opaque` finds a slot-shaped token | `F-CLASS-SLOT-ID-NON-OPAQUE` (existing top-level — defense-in-depth per v7.0.10 §2.2) | PRE | HARD_BLOCK; NO M13 (firing = bug/attack) |
| `check_class_high_stakes_flag_leak` finds a high-stakes literal | `F-CLASS-HIGH-STAKES-FLAG-LEAK` (existing top-level) | PRE | HIGH / M13 audited |
| Under split_context_hybrid: prompt field-path not in allow-list | `F-CLASS-SPLIT-CONTEXT-ALLOWLIST` (existing top-level — v7.0.10 §5.3) | PRE | HARD_BLOCK |
| Under split_context_hybrid: applicant-fact scan hits | `F-CLASS-SPLIT-CONTEXT-LEAK` (existing top-level — v7.0.10 §5.3) | PRE | HARD_BLOCK + admin-risk HIGH |
| Response bytes contain a tagged Confidential literal (POST scan) | `F-CLASS-CLOUD-RECEIVED-CONFIDENTIAL.outbound_boundary_post_drift` | POST | P0 / M13 audited |
| Response bytes contain `[SLOT_*]` pattern (defense-in-depth) | `F-CLASS-CLOUD-RECEIVED-OPAQUE-SLOT-FILLED` (existing top-level — v7.0.10 §2.2) | POST | P0 / M13 audited |
| Response bytes contain a high-stakes literal | `F-CLASS-HIGH-STAKES-FLAG-LEAK` (existing top-level) | POST | HIGH / M13 audited |

All POST-gate failures imply response bytes have been received. Wrapper discards bytes; seat exits `EXIT_GATE_FAIL=2`; admin-risk ledger records the egress event with the failure-code.

## §5. Cedar policy

`pipeline/vault/policies/outbound_boundary.cedar` (NEW; ~30 LOC):

```cedar
// CC-007 — outbound-boundary Cedar policy companion to enforce_outbound_boundary.
// Composes with existing F-CLASS-* policies; no new principals or resources
// beyond v7.0.7 §3.7 definitions.

forbid (
  principal,
  action == Action::"http_egress",
  resource
)
when {
  resource.posture == "local_only_sovereign"
};

forbid (
  principal,
  action == Action::"http_egress",
  resource
)
when {
  !resource has classification_context_provided ||
  resource.classification_context_provided == false
};

forbid (
  principal,
  action == Action::"http_egress",
  resource
)
when {
  resource has classified_input_classes &&
  ("confidential" in resource.classified_input_classes ||
   "operator_flagged" in resource.classified_input_classes)
};
```

## §6. Logfire integration

The wrapper emits three Logfire spans per HTTP POST: `tilth.outbound_boundary.pre_gate` (entry/result with predicate-by-predicate trace) + `tilth.outbound_boundary.invoke` (HTTP duration + status_code + url_host) + `tilth.outbound_boundary.post_gate` (entry/result). On PRE refusal, only the pre_gate span exists; the invoke + post_gate spans are absent. On POST refusal, all three exist with the post_gate span carrying the refusal.

Per CC-008 (Logfire disable-by-default for v0.1, redaction processor v0.2 first wave): the spans are emitted only if Logfire is configured to upload. In-process span tree exists regardless and is consumed by WPFA cycle-receipt computation (§17 v1) for accurate counterfactual accounting of refused egress events.

## §7. Router-side de-duplication (OD-5)

`pipeline/orchestrator/router.py:_dispatch_with_classification_boundary` (currently at L560-583) refactors to:

```python
def _dispatch_with_classification_boundary(
    *,
    provider_name: str,
    provider_cfg: dict,
    seat_cfg: dict,
    messages: list[dict],
    system: str | None,
    classification_context: ClassificationContext | None,
) -> dict:
    if not _is_cloud_provider(provider_name, provider_cfg):
        return _dispatch(provider_cfg, seat_cfg, messages, system)

    # Adapt router's per-provider dispatch into OutboundCallable shape:
    def inner(*, url, headers, body, timeout_seconds):
        # _http_post is router's existing urlopen wrapper at L586-599.
        # Returns (int, bytes) per OutboundCallable shape.
        return _http_post_outbound_shape(url, headers, body, timeout_seconds)

    posture = _load_deployment_posture()  # reads from routing.yaml + signed register

    wrapped = enforce_outbound_boundary(
        inner,
        classification_context=classification_context,
        posture=posture,
    )

    # ... existing provider-specific payload-construction + parse logic ...
```

The router's existing `_enforce_cloud_boundary_pre` + `_enforce_cloud_boundary_post` functions (L465-557) are DELETED. The wrapper is the single source of truth.

## §8. Threat model + bounded scope

Bounded under **v7 LOCKED A1 (single-client) + A4 (operator-trusted preflight)**. The amendment's threat model:

- **Closure target:** the provable sovereignty bypass — three production paths that issue cloud-frontier urllib POSTs without F-CLASS PRE/POST gate enforcement.
- **In scope:** seat-local provider HTTP egress (Scribe/Judge/Red Team) + router-side urllib egress (existing F-CLASS path; subject to OD-5 dedup).
- **Out of scope (residual; documented at §11):**
  - Heavy-Judge swap binary integrity at v7.0.10 §5.3 `F-CLASS-HEAVY-JUDGE-CLOUD-DOWNLOAD` — filesystem read, not HTTP egress.
  - WPFA cycle-receipt energy counterfactual computation (§17 v1) — receives refusal events; does not modify wrapper shape.
  - BYOK key retrieval lifecycle — governed by `pipeline/orchestrator/keyring_loader.py` per v0.1 §1 keys.py discipline; unchanged.
  - Static-analysis evasion shapes per §3.4 (getattr / __dict__ / local reassignment / wildcard imports) — Section O.5 v2 hardening.
  - Brain Shape A/B/C boundary integration — separate v0.2 question; wrapper is shape-agnostic.

## §9. Test surface

### §9.1 New tests at LOCK

**`tests/orchestrator/test_provider_boundary.py` (8 tests):**
- `test_outbound_boundary_missing_context_fails_closed` — classification_context is None under non-Local-Only posture; raises `OutboundBoundaryRefusedError(F_CLASS_OUTBOUND_BOUNDARY_MISSING_CONTEXT, ...)`.
- `test_outbound_boundary_classification_deny_local_only_fails_closed` — posture == local_only_sovereign; raises `OutboundBoundaryRefusedError(...classification_deny...)` regardless of inputs.
- `test_outbound_boundary_classification_deny_confidential_input_fails_closed` — input class confidential; raises before inner is called.
- `test_outbound_boundary_classification_deny_payload_scan_hit` — classified_value literal in prompt; raises before inner is called.
- `test_outbound_boundary_post_drift_classification_hit_fails_closed` — response bytes carry tagged confidential literal; inner is called but raises post-receive.
- `test_outbound_boundary_post_drift_opaque_slot_filled_fails_closed` — response bytes carry `[SLOT_xxx]` pattern; defense-in-depth POST scan fires.
- `test_outbound_boundary_happy_path_public_input_returns_inner_result` — all-public input + posture frontier_eligible; inner is called and result is returned unmodified.
- `test_outbound_boundary_logfire_spans_emitted` — three spans emitted on happy path; one (pre_gate only) on PRE refusal; three (with post_gate refusal) on POST refusal.

**`tests/orchestrator/test_provider_boundary_split_context.py` (5 tests):**
- `test_split_context_allowlist_field_path_pass` — input field-path in allow-list; PASS.
- `test_split_context_allowlist_field_path_fail` — input field-path NOT in allow-list; raises with `F-CLASS-SPLIT-CONTEXT-ALLOWLIST`.
- `test_split_context_leak_applicant_fact_scan_pass` — public-classed Public + Shareable input without applicant-fact pattern; PASS.
- `test_split_context_leak_applicant_fact_scan_fail` — public-classed Public + Shareable input contains EIN pattern; raises with `F-CLASS-SPLIT-CONTEXT-LEAK`.
- `test_split_context_dual_sign_extension_required` — extension to allow-list at write time requires dual signature (operator Ed25519 + second-tier).

**`tests/linting/test_r_no_direct_provider_http.py` (25 sub-tag matrix + 5 hygiene):**
- 5 × 5 sub-tag × concrete-shape matrix: per sub-tag, deliberately add a forbidden primitive call in a non-allowlisted file fixture; rule fires with the expected sub-tag.
- `test_allowlist_round_trip` — every entry in ALLOWLISTED_FILES is verified to exist on disk + each calls a forbidden primitive that the rule would otherwise flag.
- `test_clean_module_no_violations` — a module with no forbidden primitives produces zero violations.
- `test_dead_code_rule_fires` — rule fires on a forbidden call inside `if False:` (no data-flow pass; the call exists in AST).
- `test_forbidden_primitives_table_is_immutable` — `FORBIDDEN_PRIMITIVES["new"] = ...` raises TypeError.
- `test_validation_dispatch_grandfather_glob_excluded` — `pipeline/validation/**/*.py` paths are excluded per OD-4.

### §9.2 Existing tests touched

12 invocation-shape updates to scribe + judge provider tests; 6 Red Team Protocol-shape changes; 4 export-list assertions updated. No logic changes — fixture shape only.

## §10. Lock_history compound rows at LOCK

Three lock_history rows append at LOCK ceremony per the compound paired-commit precedent (§4 v2.x.1 row 198/199 + §17 v1 row 205-208):

- **Row N (this amendment):** `lock_class: blueprint`, `lock_kind: compound-paired-commit-double-member-1`, `lock_cycle: §4 v2.x.5 CC-007 closure`, parent_lock = §4 v2.x row 193.
- **Row N+1 (§0.5 v27 paired-commit):** `lock_class: blueprint-interface-index`, `lock_kind: compound-paired-commit-double-member-2`, `parent_lock_row: <N>`.
- Single compound `lock_timestamp_utc` per §6.17 Option-B.

The AST-lint rule registration row optionally lands as a third compound row per §17 v1 row 207 precedent if discrete attribution helps; otherwise the rule registration is recorded inside §0.5 v27 (row class `ast-lint`) and rolls into the §0.5 row.

## §11. Cycle 1 disposition (CLOSED 2026-05-16)

Per L-005 row-170 transparent disposition. Full Cycle 1 outputs at `pipeline/validation/cc007_thesis_2026-05-16/audit_v1_{editor,judge,red_team}.md`; full disposition synthesis at `pipeline/validation/cc007_thesis_2026-05-16/foldins_v1.md`.

**Editor (8 findings; verdict REQUIRES_FIX; all FOLD-IN-AT-V2):**
- E-01 MED → §1.0 TL;DR 3-step overview ADDED.
- E-02 LOW → §2 §C.2 leading-dot wire-form emphasis ADDED + §4.5 cross-ref.
- E-03 MED → §4.0 per-seat refactor summary table ADDED.
- E-04 LOW → §4.4 NEW callout box: JSON shape + canonical-encoding + posture enum + cycle_id + payload_sha3_512_commitment.
- E-05 MED → §4.5 M13 column standardized to three values: STRUCTURAL_NO_M13 / M13_AUDITED_HIGH / M13_AUDITED_MEDIUM + legend.
- E-06 LOW → §7.0 drift-risk motivation paragraph ADDED at section open.
- E-07 LOW → §9.1 NEW 3-line summary on new-test count.
- E-08 MED → composite of E-01..E-07.

**Judge (1 DC; verdict READY_TO_LOCK 99/100; FOLD-IN-AT-V2):**
- DC-01 LOW → §7 router refactor uses `stdlib_urlopen_caller` directly; ALLOWLISTED_FILES collapses to `{"pipeline/orchestrator/provider_boundary.py"}` only.

**Red Team (23 findings; verdict ESCALATE blocking:true at Cycle 1; resolves to REQUIRES_FIXES blocking:false at amendment-v2):**

| Finding | Severity | Disposition | Closure mechanism (see foldins_v1.md for full text) |
|---------|----------|-------------|-----------------------------------------------------|
| RT-01 (injected-seam swap) | HIGH | FOLD-IN | §1.1 NEW runtime identity guard `inner is stdlib_urlopen_caller`; NEW sub-tag `.outbound_boundary_runtime_integrity_fail`. |
| RT-02 (typo bypass) | MED | RESOLVED-by-RT-01 | — |
| RT-03 (monkey-patch) | MED | RESOLVED-by-RT-01 + Cedar | RT-01 + §5 Cedar runtime-loaded per RT-20 fold-in. |
| RT-04 (forged context — empty inputs hides Confidential) | HIGH | FOLD-IN | §1.1 NEW raw-bytes PRE-scan against operator-signed register's classified_values (not envelope's; envelope untrusted). |
| RT-05 (cross-cycle replay) | HIGH | FOLD-IN | §4.4 ClassificationContext gains `cycle_id` + `payload_sha3_512_commitment`; wrapper verifies body sha3-512 match. NEW sub-tag `.outbound_boundary_payload_commitment_mismatch`. |
| RT-06 (malformed envelope alternate path) | MED | FOLD-IN | §4 envelope post_init refuses; no alternate fallback path. Documented at §4.4. |
| RT-07 (posture forgery vs signed register) | HIGH | FOLD-IN | §1.1 NEW posture cross-check against operator-signed deployment register; NEW sub-tag `.outbound_boundary_posture_mismatch` on F-CLASS-POSTURE-MID-CYCLE-CHANGE. |
| RT-08 (posture mismatch envelope vs router) | MED | RESOLVED-by-RT-07 | — |
| RT-09 (cloud echoes payload — caught) | NONE | NO-ACTION | Already correctly handled by POST-gate. |
| RT-10 (substring match) | MED | DEFERRED-to-v0.2 | Predicate body at `f_class_outbound_boundary.py`; v0.2 hardening. §11 deferred-dispositions register. |
| RT-11 (Unicode normalization) | LOW | DEFERRED-to-v0.2 | Same as RT-10. |
| RT-12 (timing side-channel) | LOW | DEFERRED-to-v2-O.5 | Section O.5 hardening. |
| RT-13 (dynamic getattr) | MED | BOUNDED-by-v7-A1+A4 | §3.4 documents as static-analysis-evasion bounded by single-contributor envelope; RT-01 runtime identity catches dynamic-import-then-call. |
| RT-14 (new HTTP library bypass) | HIGH | FOLD-IN + DEFER-PARTIAL | (a) §3.2 EXTEND FORBIDDEN_PRIMITIVES with closed-set ALLOWED_HTTP_LIBS `{"urllib", "urllib.request", "urllib.parse"}`; new sub-tag `.unknown_http_library_import`. (b) DEFERRED to v2/Section O.5: runtime-guard wrapper layer that intercepts dynamic-import shapes. |
| RT-15 (pathlib remote file) | MED | OUT-OF-SCOPE | Not HTTP egress; v0.2 Section O.5 filesystem-egress hardening. |
| RT-16 (legacy fallback refs) | MED | FOLD-IN | §7 NEW: LOCK ceremony grep-verifies zero `_enforce_cloud_boundary_pre/post` references survive. |
| RT-17 (double-gate firing) | LOW | FOLD-IN | §7 NEW: post-refactor invokes `enforce_outbound_boundary` exactly once; pinned via integration test. |
| RT-18 (no runtime assertion wrapper called) | MED | RESOLVED-by-RT-01 + sentinel | RT-01 + module-level thread-local `_OUTBOUND_BOUNDARY_INVOKED` sentinel; new sub-tag `.outbound_boundary_never_invoked`. |
| RT-19 (integration test gap) | LOW | FOLD-IN | §9.1 NEW: `tests/integration/test_cc007_e2e_confidential_envelope_refused.py`. |
| RT-20 (Cedar policy documentary-only) | MED | FOLD-IN | §5 NEW: Cedar policy LOADED at runtime by `pipeline/logician/cedar_engine.py`; second-layer defense; F-CEDAR-* family composition. |
| RT-21 (Cedar split-context composition) | LOW | FOLD-IN | §5 NEW: `outbound_boundary.cedar` imports `split_context.cedar` via `include` directive. |
| RT-22 (multi-tenant scope creep) | HIGH | BOUNDED-by-v7-A1+A4 + DEFERRED-to-Stage-5 | §8 explicit v2-deferral-marker: tenant-binding (HMAC-with-tenant-key + tenant-ID-in-envelope) lands at Stage 5 Sovereign Node commons. v0.1 bounded under A1+A4. |
| RT-23 (Logfire span body leak) | MED | FOLD-IN | §6 NEW: explicit statement — Logfire spans carry ZERO request/response body bytes. Pinned via integration test. |

**Cycle-1-introduced new sub-tags (5 — all under EXISTING top-level rows; family stays at 16):**
- `.outbound_boundary_runtime_integrity_fail` (F-CLASS-CLOUD-RECEIVED-CONFIDENTIAL; RT-01)
- `.outbound_boundary_payload_commitment_mismatch` (F-CLASS-CLOUD-RECEIVED-CONFIDENTIAL; RT-05)
- `.outbound_boundary_posture_mismatch` (F-CLASS-POSTURE-MID-CYCLE-CHANGE; RT-07)
- `.outbound_boundary_never_invoked` (F-CLASS-CLOUD-RECEIVED-CONFIDENTIAL; RT-18)
- `.unknown_http_library_import` (R-NO-DIRECT-PROVIDER-HTTP AST-lint sub-tag; RT-14)

**§0.5 v27 paired-commit impact:** 5 new sub-tag-extension records added; existing 8 rows expand to 13. Family roster still 16 top-level primitives. NO new top-level F-CLASS-* row.

## §11.1 §1 wrapper-signature delta at v2 (RT-01 + RT-04 + RT-05 + RT-07 fold-in)

The wrapper signature gains four runtime guards (all PRE-2 layer, executed in order before the existing PRE-3 predicate chain):

```python
def enforce_outbound_boundary(
    inner: OutboundCallable,
    *,
    classification_context: ClassificationContext | None,
    posture: Posture,
    operator_signed_register: ClassificationRegister,  # NEW at v2; loaded once at wrapper construction
) -> OutboundCallable:
    """Wrap an HTTP POST callable with F-CLASS PRE/POST outbound-boundary gates.

    Cycle 1 RT-fold-ins (PRE-2a..PRE-2d, before existing PRE-3):

      PRE-2a (RT-01 runtime identity guard): refuse if `inner is not stdlib_urlopen_caller`.
        Raises OutboundBoundaryRefusedError(...runtime_integrity_fail...).
        Identity check (not equality) — test fixtures use a separate test-only entry point.

      PRE-2b (RT-07 posture cross-check): refuse if `posture` from envelope differs from
        operator_signed_register's posture. Raises OutboundBoundaryRefusedError(...posture_mismatch...)
        under F-CLASS-POSTURE-MID-CYCLE-CHANGE family.

      PRE-2c (RT-05 payload commitment): compute sha3-512 of `body` bytes; refuse if mismatch with
        classification_context.payload_sha3_512_commitment.
        Raises OutboundBoundaryRefusedError(...payload_commitment_mismatch...).

      PRE-2d (RT-04 raw-bytes scan against signed register): for every classified_value entry in
        operator_signed_register whose class is confidential/operator_flagged, scan request body
        bytes (UTF-8 decoded with errors=replace + Unicode-NFC normalized). If any literal appears,
        refuse with OutboundBoundaryRefusedError(...classification_deny...).
        Source-of-truth = signed register, NOT envelope's classified_values (envelope untrusted).

    Existing PRE-3 chain runs after PRE-2a..PRE-2d pass.

    Sentinel (RT-18 fold-in): wrapper sets thread-local `_OUTBOUND_BOUNDARY_INVOKED = True` flag
    on successful PRE/INVOKE/POST round-trip. Seat shutdown discipline reads the flag and refuses
    to exit clean if the flag was never set on a cloud-routable subprocess.
    """
    ...
```

## §11.2 §3.2 FORBIDDEN_PRIMITIVES extension (RT-14 fold-in)

The AST-lint rule extends with a closed-set ALLOWED_HTTP_LIBS check:

```python
ALLOWED_HTTP_LIBS: Final[frozenset[str]] = frozenset({
    "urllib", "urllib.request", "urllib.parse",
})

# At module-load AST visit time:
# - Any `import <lib>` or `from <lib> import ...` where <lib> matches a known HTTP-class
#   library name pattern AND <lib> is NOT in ALLOWED_HTTP_LIBS → emit Violation with
#   sub-tag `.unknown_http_library_import`.
```

Sub-tag count = 6 (5 existing + `.unknown_http_library_import`); concrete primitive coverage = 25 + N where N is the set of known third-party HTTP libraries (httpx / aiohttp / requests / urllib3 / httpcore / pycurl). Out-of-scope shapes (per §3.4 + RT-13 bounded disposition): dynamic imports via `importlib` / `__import__` / `getattr` — RT-01 runtime identity guard catches these at the wrapper invocation site.

## §11.3 §4.4 ClassificationContext schema extension (RT-05 fold-in)

```json
{
  "inputs": [{"field_path": "string", "class_name": "public|shareable|confidential|operator_flagged", "locked_by": "string"}],
  "classified_values": [{"value": "string", "class_name": "string", "field_path": "string"}],
  "slot_positions": [{"slot_id": "digits", "pre_marker": "string", "post_marker": "string"}],
  "high_stakes_flag_values": ["string", "..."],
  "post_fill_draft": false,

  "cycle_id": "string",                              // NEW at v2 (RT-05) — current run's cycle identifier
  "payload_sha3_512_commitment": "128-hex-string"    // NEW at v2 (RT-05) — sha3-512 of canonical body bytes pre-envelope-serialization
}
```

Orchestrator computes `payload_sha3_512_commitment` BEFORE envelope serialization (canonical-bytes commit). Wrapper recomputes at invocation time and verifies match. Cross-cycle replay attempts fail because the body bytes differ from the original.

## §11.4 §5 Cedar policy runtime-load (RT-20 + RT-21 fold-in)

```cedar
// pipeline/vault/policies/outbound_boundary.cedar (UPDATED at v2)
include "split_context.cedar"  // RT-21 fold-in: compose with v7.0.10 §5.3 split-context Cedar rules

forbid (
  principal,
  action == Action::"http_egress",
  resource
)
when {
  resource.posture == "local_only_sovereign" ||
  !resource has classification_context_provided ||
  resource.classification_context_provided == false ||
  ("confidential" in resource.classified_input_classes) ||
  ("operator_flagged" in resource.classified_input_classes) ||
  resource.payload_sha3_512_commitment_mismatch == true ||  // RT-05
  resource.posture_mismatch_with_register == true ||         // RT-07
  resource.runtime_integrity_failed == true                  // RT-01
};
```

`pipeline/logician/cedar_engine.py` LOADS `outbound_boundary.cedar` at module load; evaluates Cedar rules at every wrapped invocation as a second-layer defense. If Cedar evaluation fails-closed while Python wrapper passes (or vice versa), F-CEDAR-CONSISTENCY-DIVERGENCE sub-tag fires + admin-risk HIGH.

## §11.5 §6 Logfire span body-bytes prohibition (RT-23 fold-in)

Logfire spans MUST NOT carry request OR response body bytes. Permitted span attributes:
- `status_code: int`
- `url_host: str` (host only; path stripped)
- `latency_ms: float`
- `failure_code: str | None`
- `sub_tag: str | None`
- `trace_id: str`
- `posture: str` (Posture enum value)
- `cycle_id: str`

Forbidden span attributes (PIN via test):
- Any field containing request body bytes / decoded text.
- Any field containing response body bytes / decoded text.
- Any field containing API keys / headers / authentication tokens.

Integration test `tests/integration/test_logfire_spans_carry_no_body_bytes.py` pins the contract by spawning a wrapped invocation + asserting span attributes are a subset of the permitted set.

## §11.6 §7 router de-duplication completion (RT-16 + DC-01 fold-in)

Router refactor lands at v2 with:
- `_enforce_cloud_boundary_pre` + `_enforce_cloud_boundary_post` DELETED — verified via grep at LOCK ceremony (zero references survive).
- `_http_post_outbound_shape` REPLACED by direct import + call of `stdlib_urlopen_caller` (DC-01 fold-in).
- ALLOWLISTED_FILES collapses to `{"pipeline/orchestrator/provider_boundary.py"}` only.
- Router calls `enforce_outbound_boundary(stdlib_urlopen_caller, ...)` exactly once per dispatch; no second POST-gate (RT-17 fold-in).
- LOCK ceremony executes `grep -rn "_enforce_cloud_boundary_pre\\|_enforce_cloud_boundary_post" pipeline/orchestrator/router.py` and fails-closed if any match.

## §11.7 §8 multi-tenant deferral marker (RT-22 BOUNDED)

§8 explicit addition at v2:

> **v2 / Stage-5 deferral — tenant-binding of ClassificationContext.** Under v0.1 single-client + A4 operator-trusted-preflight envelope, ClassificationContext is trusted to originate from the operator without cryptographic tenant binding. At Stage-5 Sovereign Node commons (multi-tenant compute pool), tenant-binding becomes mandatory: each ClassificationContext MUST be HMAC-signed with a tenant-specific key + envelope MUST carry tenant_id; wrapper MUST verify HMAC against tenant's pinned key before accepting context. Deferral marker recorded at §11 deferred-dispositions register; pre-staged at architecture v7.0.x Stage-5 amendment when commons goes through L-005 round.

## §11.8 §9.1 test surface extensions

New tests at v2 (additions to §9.1 base list):
- `tests/orchestrator/test_provider_boundary.py::test_runtime_identity_guard_refuses_non_canonical_inner` (RT-01)
- `tests/orchestrator/test_provider_boundary.py::test_posture_mismatch_envelope_vs_register_refuses` (RT-07)
- `tests/orchestrator/test_provider_boundary.py::test_payload_commitment_mismatch_refuses` (RT-05)
- `tests/orchestrator/test_provider_boundary.py::test_raw_bytes_scan_catches_forged_empty_context` (RT-04)
- `tests/orchestrator/test_provider_boundary.py::test_sentinel_thread_local_set_on_invocation` (RT-18)
- `tests/linting/test_r_no_direct_provider_http.py::test_unknown_http_library_import_flags` (RT-14)
- `tests/integration/test_cc007_e2e_confidential_envelope_refused.py` (RT-19)
- `tests/integration/test_logfire_spans_carry_no_body_bytes.py` (RT-23)
- `tests/logician/cedar/test_outbound_boundary_cedar_loaded_at_runtime.py` (RT-20)
- `tests/logician/cedar/test_split_context_cedar_composed.py` (RT-21)

Total new tests after Cycle 1 fold-ins: ~53 (43 base + 10 RT-fold-in).

## §11.9 Deferred dispositions register (carried forward to v0.2 / Section O.5)

| Item | Source | Defer to |
|------|--------|----------|
| Token-aware (vs substring) Confidential matching | RT-10 | v0.2 predicate-body hardening |
| Unicode normalization in POST-scan | RT-11 | v0.2 predicate-body hardening |
| Constant-time predicate evaluation (timing side-channel) | RT-12 | v2 Section O.5 |
| Runtime-guard wrapper layer for dynamic-import shapes | RT-14 (partial) | v2 Section O.5 |
| Filesystem-egress hardening (pathlib remote files) | RT-15 | v2 Section O.5 |
| Multi-tenant ClassificationContext HMAC binding | RT-22 | Stage 5 Sovereign Node commons amendment |

## §12. Cycle 2 disposition (CLOSED 2026-05-16; FOLD-IN-AT-LOCK per L-005 row-170)

Full Cycle 2 outputs at `pipeline/validation/cc007_thesis_2026-05-16/audit_v2_{editor,judge,red_team}.md`.

**Cycle 2 summary verdicts:**
- **Editor:** PASS. All 8 Cycle 1 findings VERIFIED_CLOSED. 0 new probes.
- **Judge:** READY_TO_LOCK 100/100 (+1 from Cycle 1's 99/100). 2 LOW DC-CYCLE2 findings, both RECOMMEND_FOLD_IN_AT_LOCK.
- **Red Team:** ESCALATE blocking:true at face value; resolves to REQUIRES_FIXES blocking:false per row-170 transparent-disposition discipline. 8 new probes (2 HIGH + 4 MED + 2 LOW) + 7 Cycle 1 findings flagged PARTIAL_CLOSURE_REMAINS. All 15 items map to concrete text-level closures here; no defect requires v2.1 follow-on.

**Disposition decision (per L-005 row-170):** Cycle 2 NEW probes that name structurally-addressable holes get FOLD-IN-AT-LOCK with explicit text-level mechanism at §12.1..§12.10. Cycle 2 PARTIAL_CLOSURE_REMAINS findings overlap heavily with Cycle 2 NEW probes (RT-04↔RT-C2-01; RT-07↔RT-C2-07; RT-18↔RT-C2-03; RT-20↔RT-C2-04; RT-21↔RT-C2-05) — joint closure here. Cycle 2 BOUNDED items (RT-01/RT-03 monkey-patching `stdlib_urlopen_caller` itself) are bounded by v7 LOCKED A1 single-client + A4 operator-trusted preflight envelope + Cedar second-layer defense per §12.4.

### §12.1 Judge DC-CYCLE2-01 — sentinel-posture-conditional check (LOW; FOLD-IN-AT-LOCK)

The `_OUTBOUND_BOUNDARY_INVOKED` thread-local sentinel from §11.1 RT-18 fold-in is **conditionally enforced based on posture**: seat shutdown discipline reads the flag AND `envelope.posture`:

```python
# Seat exit discipline (in run_seat tail):
if envelope.posture in ("frontier_eligible", "split_context_hybrid"):
    if not _process_outbound_boundary_invocation_count_atomic >= 1:
        # No cloud-routable invocation occurred but posture would have permitted one.
        # NOTE: this is an OPERATOR-SIGNAL refusal, not a P0 — under posture==frontier_eligible
        # a public-only cycle may legitimately route fully cloud without seat sentinel firing
        # if the cycle was a fast-fail before any provider call. Refusal class = INFO-level
        # admin-risk-ledger entry, NOT EXIT_GATE_FAIL.
        pass  # acceptable; cycle short-circuited
# Under posture == "local_only_sovereign": sentinel MUST NOT have been invoked.
# Wrapper refuses unconditionally under local-only (§1.1 PRE-2a), so any non-zero count = bug.
elif envelope.posture == "local_only_sovereign":
    if _process_outbound_boundary_invocation_count_atomic > 0:
        # Wrapper invocation under Local-Only means PRE-2a fired-and-refused, but the counter
        # only increments on successful POST-gate clearance. Non-zero = the wrapper was bypassed.
        raise OutboundBoundaryRefusedError(
            "F-CLASS-CLOUD-RECEIVED-CONFIDENTIAL.outbound_boundary_never_invoked",
            "wrapper invocation counter non-zero under local_only_sovereign posture; "
            "bypass attempt detected",
        )
```

Pinned by `tests/integration/test_cc007_e2e_confidential_envelope_refused.py` parametrize across all three postures.

### §12.2 Judge DC-CYCLE2-02 — URL scheme assertion in `stdlib_urlopen_caller` (LOW; FOLD-IN-AT-LOCK)

`stdlib_urlopen_caller` adds a structural URL-scheme assertion at entry:

```python
def stdlib_urlopen_caller(*, url: str, headers, body, timeout_seconds):
    if not url.startswith("https://"):
        raise OutboundBoundaryRefusedError(
            "F-CLASS-CLOUD-RECEIVED-CONFIDENTIAL.outbound_boundary_classification_deny",
            f"stdlib_urlopen_caller refused non-https scheme: {url[:64]!r}",
        )
    # ... existing urllib.request.urlopen call ...
```

Prevents `file://`, `http://` (non-TLS), `ftp://`, and other-scheme injection at the urllib call site. Defense-in-depth against (a) misconfigured router.yaml endpoints, (b) header-injection attacks that mutate the URL field, (c) future provider adapters that fail to enforce https. Pinned by `tests/orchestrator/test_provider_boundary.py::test_stdlib_urlopen_caller_refuses_non_https`.

### §12.3 RT-C2-01 (HIGH) — operator_signed_register injection via PYTHONPATH

The §11.1 PRE-2d raw-bytes scan loads `operator_signed_register` once at wrapper construction. An attacker with PYTHONPATH-write access could replace the register module with a forged version containing no confidential literals. FOLD-IN-AT-LOCK:

The register loads from a **signed file** at `vault_shared/classification/operator_signed_register.signed.yaml`, NOT from a Python module. The loader (`pipeline.vault.classification.signed_register_loader.load_signed_register()`) verifies the file's Ed25519 signature against the operator's pinned public key (mirrors v7.0.7 §6.1 router-template signing discipline byte-for-byte). Verification failure → `OutboundBoundaryRefusedError("F-CLASS-REGISTER-SIGNATURE-INVALID.signed_file_invalid", ...)` (existing F-CLASS-REGISTER-SIGNATURE-INVALID primitive gains sub-tag `.signed_file_invalid` per the sub-tag-extension precedent). The loaded register is wrapped in a `MappingProxyType` view exposed as an immutable module-level constant; reassignment attempts raise TypeError.

PYTHONPATH-based module-replacement attacks fail because the loader does NOT import a Python module — it reads + verifies the signed YAML at startup. Mirrors §4 v2.x.1 row 198 RT-14 closure (MappingProxyType immutability) + v7.0.7 §6.1 signed-asset pattern.

### §12.4 RT-C2-02 (MED) + RT-01/RT-03 PARTIAL closure — monkey-patching `stdlib_urlopen_caller` itself

The runtime identity guard (§11.1 PRE-2a) catches `inner is not stdlib_urlopen_caller`. But if an attacker monkey-patches the `stdlib_urlopen_caller` symbol itself (e.g., `pb.stdlib_urlopen_caller = malicious_func` before any seat subprocess starts), the identity check still passes because `inner is stdlib_urlopen_caller == True` (the symbol now points at the malicious function).

FOLD-IN-AT-LOCK (joint closure for RT-01 + RT-03 PARTIAL + RT-C2-02):

1. **Module-level identity pin.** At `pipeline/orchestrator/provider_boundary.py` module load, the canonical `stdlib_urlopen_caller` function object is captured to a module-private read-only variable `_CANONICAL_STDLIB_URLOPEN_CALLER` via `MappingProxyType`-style identity-binding pattern. The wrapper's PRE-2a check compares `inner is _CANONICAL_STDLIB_URLOPEN_CALLER`, NOT the public `stdlib_urlopen_caller` symbol. Monkey-patching the public symbol does NOT mutate the captured identity.

2. **Cedar second-layer enforcement.** Cedar policy at `outbound_boundary.cedar` evaluates ALSO at every wrapped invocation. If the Python wrapper is bypassed entirely (e.g., via a sufficiently sophisticated monkey-patch), Cedar's structural rule still fires because Cedar is loaded by `pipeline/logician/cedar_engine.py` at process startup BEFORE seat subprocesses spawn, and Cedar evaluation is gated structurally on the request's classification-context-and-posture pair. Per RT-20 fold-in, Cedar failure fails-closed.

3. **Bounded under v7 A1+A4.** Monkey-patching attacks require code-execution on the appliance. Under v7 LOCKED A1 single-client + A4 operator-trusted preflight envelope, this is contributor-discipline-shaped (the operator is the only contributor; no adversarial code-execution surface). Multi-tenant promotion to MED severity lands at Section O.5 v2 hardening + Stage-5 Sovereign Node commons amendment.

Pinned via `tests/orchestrator/test_provider_boundary.py::test_canonical_identity_pin_resists_monkey_patch`.

### §12.5 RT-C2-03 (MED) + RT-18 PARTIAL closure — thread-local → process-wide atomic counter

`_OUTBOUND_BOUNDARY_INVOKED` thread-local upgrades to `_PROCESS_OUTBOUND_BOUNDARY_INVOCATION_COUNT_ATOMIC` (a `threading.Lock`-guarded int counter at module scope). The wrapper increments inside its successful POST-gate clearance section (after `inner()` returns AND POST-gate predicates pass). Seat exit discipline (per §12.1) reads the counter under posture-conditional rules.

Worker-thread bypass attempts (where a worker thread calls `stdlib_urlopen_caller` directly without going through `enforce_outbound_boundary`) fail because:

1. Direct call to `stdlib_urlopen_caller` is permitted only inside `provider_boundary.py` (AST-lint allowlist; §3.1).
2. If a worker thread somehow obtains the canonical function reference and calls it directly, the call IS the actual urllib egress — but the wrapper's PRE/POST gates never ran. Process-wide counter does NOT increment.
3. Per §12.1, seat exit discipline under posture==frontier_eligible/split_context_hybrid expects counter ≥ 1; counter == 0 with non-Local-Only posture and non-empty drafts indicates either a fast-fail short-circuit (acceptable) or a bypass (which surfaces at admin-risk audit but not as EXIT_GATE_FAIL alone — combined with the runtime identity pin at §12.4, the bypass path is structurally closed).

Additional belt-and-suspenders: `stdlib_urlopen_caller` itself sets a thread-local `_INSIDE_WRAPPER` flag at entry (set by the wrapper before calling `inner`); if `_INSIDE_WRAPPER` is False when `stdlib_urlopen_caller` is invoked, the function raises `OutboundBoundaryRefusedError("F-CLASS-CLOUD-RECEIVED-CONFIDENTIAL.outbound_boundary_never_invoked.direct_call", ...)`. This catches direct-call bypasses at the call site.

Pinned via `tests/orchestrator/test_provider_boundary.py::test_direct_stdlib_urlopen_caller_call_outside_wrapper_refuses`.

### §12.6 RT-C2-04 (HIGH) + RT-20 PARTIAL closure — Cedar load fail-closed

Cedar policy load at `pipeline/logician/cedar_engine.py` startup uses a strict try/except + module-level fail-closed flag:

```python
# pipeline/logician/cedar_engine.py
try:
    OUTBOUND_BOUNDARY_POLICY = _load_cedar_policy("pipeline/vault/policies/outbound_boundary.cedar")
    SPLIT_CONTEXT_POLICY = _load_cedar_policy("pipeline/vault/policies/split_context.cedar")
    _CEDAR_LOAD_SUCCEEDED = True
except (FileNotFoundError, CedarParseError, CedarSyntaxError) as exc:
    _CEDAR_LOAD_SUCCEEDED = False
    _CEDAR_LOAD_FAILURE_CLASS = type(exc).__name__
    # NO silent fall-through. Process aborts on cedar_load failure for any cloud-routable seat.

def evaluate_outbound_boundary_cedar(*, classification_context, posture) -> CedarResult:
    if not _CEDAR_LOAD_SUCCEEDED:
        raise OutboundBoundaryRefusedError(
            "F-CLASS-CLOUD-RECEIVED-CONFIDENTIAL.cedar_load_failure",
            f"Cedar policy failed to load at startup: {_CEDAR_LOAD_FAILURE_CLASS}; "
            "second-layer defense unavailable; fail-closed",
        )
    return _evaluate(OUTBOUND_BOUNDARY_POLICY, ...)
```

NEW sub-tag `.cedar_load_failure` on F-CLASS-CLOUD-RECEIVED-CONFIDENTIAL. Pinned via `tests/logician/cedar/test_cedar_load_failure_fails_closed.py` — injects a malformed Cedar file and asserts wrapper refuses with the new sub-tag.

### §12.7 RT-C2-05 (MED) + RT-21 PARTIAL closure — Cedar include precedence

Cedar evaluation order is documented per the project's pinned Cedar version (Cedar 3.x: deny-by-default + first-match-forbid-wins). The `outbound_boundary.cedar` file pins the precedence explicitly:

```cedar
// pipeline/vault/policies/outbound_boundary.cedar
// Forbid rules ALWAYS appear AFTER include directives so first-match-forbid evaluates last
// in textual order. Cedar 3.x semantics: `forbid` rules take precedence over `permit` rules
// at evaluation time regardless of declaration order, but include-precedence pin is
// belt-and-suspenders defense-in-depth.

include "split_context.cedar"

forbid (
  principal,
  action == Action::"http_egress",
  resource
)
when {
  // ... (full conditions per §11.4 fold-in)
};
```

AST-lint companion test `tests/logician/cedar/test_outbound_boundary_cedar_forbid_after_includes.py` parses the combined Cedar file and asserts the forbid clause appears AFTER all include directives in textual order.

### §12.8 RT-C2-06 (LOW) — ALLOWED_HTTP_LIBS closed-set drift

Closed-set drift over future stdlib evolution. FOLD-IN-AT-LOCK:

`pipeline/linting/r_no_direct_provider_http.py::ALLOWED_HTTP_LIBS` is regenerated at LOCK ceremony time via a helper script `scripts/regenerate_allowed_http_libs.py` that reads `sys.stdlib_module_names` filtered for HTTP-class names (regex: `^(urllib|http|httpx|requests|aiohttp|urllib3|httpcore)`). The script emits a build-time warning if the regenerated set diverges from the hard-coded constant. The hard-coded constant remains the canonical source; the script is a drift-detector, not a runtime patch.

Operator runs the script as part of major-version stdlib upgrades (Python 3.x → 3.y) and updates the constant accordingly. v2.x.5 hard-codes `frozenset({"urllib", "urllib.request", "urllib.parse"})` for Python 3.11/3.12/3.13/3.14. Drift-test `tests/linting/test_r_no_direct_provider_http.py::test_allowed_http_libs_matches_stdlib_module_names_filter` pins the contract.

### §12.9 RT-C2-07 (MED) + RT-07 PARTIAL closure — posture per-call lookup

Posture lookup at `enforce_outbound_boundary` PRE-2b is per-call, NOT cached at import. The wrapper calls `pipeline.orchestrator.deployment_posture.get_current_posture()` at every invocation. The helper reads from a process-shared, thread-safe atomic container (`threading.local()` is INSUFFICIENT — uses `multiprocessing.Value` or a similar process-shared primitive) that the orchestrator updates atomically when a posture change attestation lands.

Posture changes mid-cycle: per v7.0.10 §5.3 `F-CLASS-POSTURE-MID-CYCLE-CHANGE` (existing primitive at family row 13), mid-cycle changes are themselves fail-closed at the architectural layer — the orchestrator refuses to attest a posture change while a cycle is open. The wrapper's per-call lookup picks up the new posture starting at the next cycle. Test: `tests/orchestrator/test_provider_boundary.py::test_posture_per_call_lookup_picks_up_post_cycle_change`.

### §12.10 RT-C2-08 (LOW) + RT-19 enhancement — integration test fixture alignment

`tests/integration/test_cc007_e2e_confidential_envelope_refused.py` loads the **production signed register** (NOT a stub) and verifies the test's confidential literal exists in the loaded register before exercising the wrapper. Additionally:

- New test case `test_e2e_confidential_token_absent_from_register_wrapper_still_refuses_via_envelope_inputs` — envelope claims a confidential token NOT in the register; wrapper still refuses because `classification_context.inputs` has class_name==confidential.
- New test case `test_e2e_posture_mismatch_envelope_vs_register_refuses` — envelope says frontier_eligible, register says local_only_sovereign; wrapper refuses with `.outbound_boundary_posture_mismatch`.
- New test case `test_e2e_cedar_load_failure_refuses` — Cedar file deliberately malformed at test setup; wrapper refuses with `.cedar_load_failure`.

### §12.11 RT-14 PARTIAL closure — runtime dynamic-import bypass

`R-NO-DIRECT-PROVIDER-HTTP` AST-lint rule catches static imports but not dynamic imports (`importlib.import_module("requests").post(...)`). Per §3.4 + Cycle 1 RT-13 disposition, this is bounded by v7 A1+A4 (no adversarial contributor). Cycle 2 RT-14 PARTIAL_CLOSURE_REMAINS confirms this is still a documented gap. FOLD-IN-AT-LOCK closure:

- **§3.4 explicit text:** documents the dynamic-import-via-importlib bypass as v7 A1+A4 bounded. The runtime identity pin (§12.4 PRE-2a) catches the actual call attempt because the dynamic-import result is NOT `_CANONICAL_STDLIB_URLOPEN_CALLER`.
- **DEFERRED-to-v2 Section O.5:** the runtime-guard wrapper layer that intercepts dynamic-import shapes at the importlib call site. v0.1 bounded.

### §12.12 Cycle 2 cumulative new sub-tags + AST-lint rules

Cycle 2 fold-in introduces additional sub-tags (all under EXISTING top-level rows; family stays at 16):

- `.signed_file_invalid` (under F-CLASS-REGISTER-SIGNATURE-INVALID; §12.3 RT-C2-01)
- `.cedar_load_failure` (under F-CLASS-CLOUD-RECEIVED-CONFIDENTIAL; §12.6 RT-C2-04)
- `.outbound_boundary_never_invoked.direct_call` (sub-sub-tag under existing `.outbound_boundary_never_invoked`; §12.5 RT-C2-03)
- `.outbound_boundary_classification_deny` extends to cover non-https URL scheme refusal (§12.2 DC-CYCLE2-02)

**§0.5 v27 paired-commit row delta:** the 5 Cycle 1 sub-tag-extension records expand by 2 new records at Cycle 2 (`.signed_file_invalid` + `.cedar_load_failure`). The other Cycle 2 sub-tags are sub-sub-tags or extensions of existing rows — recorded in §0.5 v27 §A.2 amendment text as nested-extension notes, no additional rows. Total §0.5 v27 row delta after Cycle 2 fold-ins: **10 rows** (was 8 at Cycle 1; +2 for new sub-tag-extension records).

**Family roster count: still 16 top-level F-CLASS-* primitives.** Cycle 2 closes without family expansion. F-CLASS-COVERAGE-INCOMPLETE META-gate scope unchanged.

### §12.13 LOCK readiness

Per L-005 strict two-cycle CLOSED with row-170 transparent disposition:

- **Editor Cycle 2:** PASS (8/8 VERIFIED_CLOSED + 0 NEW).
- **Judge Cycle 2:** READY_TO_LOCK 100/100 + 2 LOW DC-CYCLE2 FOLD-IN-AT-LOCK.
- **Red Team Cycle 2:** ESCALATE blocking:true at face → REQUIRES_FIXES blocking:false at row-170 transparent disposition (all 8 NEW probes + 7 PARTIAL_CLOSURE folded in at LOCK with concrete text-level mechanism per §12.3..§12.11; 1 DEFERRED-to-v2-O.5 marker for the dynamic-import runtime-guard).

**Amendment ready for LOCK.** No defect requires v2.1 follow-on. The Cycle 2 fold-ins close the structural surface area surfaced by Cycle 2 to the v7 A1+A4 bounded scope, with explicit Section O.5 v2 + Stage-5 commons deferral markers for residuals.

## §13. Composition with existing F-CLASS-* family

Family roster after this amendment: **sixteen primitives, unchanged** (no top-level row added).

Sub-tag map after this amendment (showing only the rows touched by §4 v2.x.5):

| Top-level primitive | Existing sub-tags | Added at v2.x.5 |
|---------------------|--------------------|-----------------|
| F-CLASS-ROUTING-INDETERMINATE | — | `.outbound_boundary_missing_context` |
| F-CLASS-CLOUD-RECEIVED-CONFIDENTIAL | (none enumerated) | `.outbound_boundary_classification_deny` (PRE) · `.outbound_boundary_post_drift` (POST) |

F-CLASS-COVERAGE-INCOMPLETE META-gate scope: unchanged. The META-gate validates the sixteen primitives are runtime-loaded; sub-tag extensions inherit the parent primitive's runtime-load status.

## §14. Done definition (recap)

See header `done_definition` block. Authoring of this amendment + §0.5 v27 paired-commit + companion code/test landings + L-005 strict two-cycle CLOSED with cross-family rigor = LOCK ceremony fires.

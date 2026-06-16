---
node_type: findings
status: decision-pending
owner: qa-measurement
decision_owner: founder
created_by: victorboscaro@gmail.com
created: 2026-06-15
feeds: GAP-QSP-TEST-PLAN
---

# Findings — F-CLASS guardrail roster drift ("16 claimed vs 13 enforced")

> **Decision needed (Josh):** the architecture claims **16 F-CLASS-\* primitives**; the
> live enforcement surface contains **13**. Four named codes have **no gate module and no
> test**. Choose: (A) build the four missing gates+tests, or (B) correct the documents to
> the real count. This gates whether `guardrail-test-matrix.yaml` can honestly claim
> 16-code coverage. It does **not** block authoring the matrix for the 13 real codes.

## Bottom line

The Golden Quill enforcement gates are in better shape than the handoff implied: **every
gate that exists on disk already has a test.** The guardrails-as-tests work is therefore
mostly *cataloguing and proving* existing coverage, not writing it from scratch.

But there is one real discrepancy, independently confirmed by three investigation passes:
the **documentation is ahead of the code** on the F-CLASS family. "Sixteen primitives" is
currently a written claim, not a verified fact. Surfacing this before it reaches a customer
claim is exactly the QSP role's job.

## Evidence

### What the documents claim

`CLAUDE.md` (§ "Beta Model Strategy", v7.0.10 LOCKED 2026-05-11) states the F-CLASS roster
is **"sixteen primitives (ten legitimate-runtime ... + two repurposed defense-in-depth ...
+ four new at v7.0.10: POSTURE-MID-CYCLE-CHANGE + SPLIT-CONTEXT-ALLOWLIST +
SPLIT-CONTEXT-LEAK + HEAVY-JUDGE-CLOUD-DOWNLOAD)."** `BUILD-SPEC.md` §1 repeats "sixteen
F-CLASS-\* primitives" and names these four in its Axis A–C cross-walk.

### What the code actually enforces

`pipeline/logician/gates/f_class_coverage_incomplete.py` — the META gate that fail-closes
deployment if any required code lacks a live module + test — declares
`REQUIRED_F_CLASS_CODES` as exactly **13 codes** (its test asserts `len == 13`):

```
F-CLASS-REGISTER-MISSING                     F-CLASS-SLOT-ID-NON-OPAQUE
F-CLASS-REGISTER-UNSIGNED                    F-CLASS-PER-GRANT-OVERRIDE-UNSIGNED
F-CLASS-REGISTER-SIGNATURE-INVALID           F-CLASS-ROUTER-TEMPLATE-SIGNATURE-INVALID
F-CLASS-REGISTER-HASH-MISMATCH               F-CLASS-HIGH-STAKES-FLAG-LEAK
F-CLASS-NEW-FACT-UNCLASSIFIED                F-CLASS-VOICE-CONFIDENTIAL-CLOUD-STT
F-CLASS-ROUTING-INDETERMINATE                (+ F-CLASS-COVERAGE-INCOMPLETE, the META gate
F-CLASS-CLOUD-RECEIVED-CONFIDENTIAL           itself, which excludes itself from its own list)
F-CLASS-CLOUD-RECEIVED-OPAQUE-SLOT-FILLED
```

All 13 map to live gate modules in `pipeline/logician/gates/f_class_*.py`, and every one
has a test under `tests/logician/gates/`. Coverage of the *existing* surface is complete.

### The four codes that are claimed but absent

| Code (named in CLAUDE.md / BUILD-SPEC) | Gate module on disk? | Test on disk? | In META `REQUIRED_F_CLASS_CODES`? |
| --- | --- | --- | --- |
| `F-CLASS-POSTURE-MID-CYCLE-CHANGE` | **No** | **No** | **No** |
| `F-CLASS-SPLIT-CONTEXT-ALLOWLIST` | **No** | **No** | **No** |
| `F-CLASS-SPLIT-CONTEXT-LEAK` | **No** | **No** | **No** |
| `F-CLASS-HEAVY-JUDGE-CLOUD-DOWNLOAD` | **No** | **No** | **No** |

These are precisely the v7.0.10 **Split-Context Hybrid** posture guards. The posture is
described as customer-facing and operator-most-common in CLAUDE.md, but its named
enforcement codes are not realized in the gate tree.

### F-WPFA family — consistent, minor count check only

The F-WPFA family (CLAUDE.md: "12 codes, 10 modules") is broadly consistent: ~12 codes
across 11 gate modules, all covered by `tests/logician/gates/test_f_wpfa_all_gates.py` +
`tests/integration/test_wpfa_end_to_end.py`. One small ambiguity to confirm — whether
`F-WPFA-COEFFICIENT-ROLLBACK-INVALID` is counted, which would make it 13 on disk vs 12
claimed. Not load-bearing; note and move on. **The F-CLASS drift is the real finding.**

## Why it matters

1. `F-CLASS-COVERAGE-INCOMPLETE` — the gate that is supposed to guarantee "no Beta ship
   with un-realized F-CLASS enforcement" — only audits the **13** codes in its own list.
   It will pass green while the four v7.0.10 codes do not exist. The deployment gate cannot
   catch a gap it doesn't know about.
2. Any future customer/sales claim that Tilth "enforces sixteen classification primitives"
   or "the Split-Context Hybrid posture is gate-enforced" would currently be **unevidenced**
   under the QSP claims-register discipline (`evidence_category: guardrail-test` with no
   resolvable test handle).
3. `guardrail-test-matrix.yaml` cannot honestly assert 16-code coverage until this is
   resolved one way or the other.

## Options

**Option A — build the four missing gates + tests.** Realize
`F-CLASS-POSTURE-MID-CYCLE-CHANGE`, `-SPLIT-CONTEXT-ALLOWLIST`, `-SPLIT-CONTEXT-LEAK`,
`-HEAVY-JUDGE-CLOUD-DOWNLOAD` as live modules, add tests, and add them to
`REQUIRED_F_CLASS_CODES`. The roster then truly is 16.
- *Pro:* the Split-Context posture becomes actually enforced; "16" becomes true.
- *Con:* real engineering against the LOCKED v7.0.10 architecture; the Split-Context
  PRE-scan/allow-list logic is non-trivial; should not be done without founder sign-off
  since it changes the locked enforcement surface and the META gate's required list.

**Option B — correct the documents to 13.** Amend CLAUDE.md and BUILD-SPEC §1 to state the
real enforced count, and record the four codes as **deferred / not-yet-realized** (e.g. a
v0.x horizon item) rather than as shipped primitives.
- *Pro:* fast; the docs stop overstating the enforcement surface; no locked-architecture
  change.
- *Con:* the Split-Context Hybrid posture remains described-but-not-gate-enforced; that
  fact must then be reflected wherever the posture is offered to customers.

## Recommendation

Author `guardrail-test-matrix.yaml` now for the **13 real F-CLASS + ~12 F-WPFA** codes
(value delivered immediately, deployment gate honestly described), and take Option A-vs-B to
Josh as a scoped decision. The matrix should mark the four codes `status: deferred` with a
pointer to this note, so the gap is visible and tracked rather than silently dropped.

## Sources

- `pipeline/logician/gates/f_class_coverage_incomplete.py` — `REQUIRED_F_CLASS_CODES` (13)
- `pipeline/logician/gates/f_class_*.py` (8 modules) · `f_wpfa_*.py` (11 modules)
- `tests/logician/gates/` · `tests/logician/gates/test_f_wpfa_all_gates.py` · `tests/integration/test_wpfa_end_to_end.py`
- `CLAUDE.md` § Beta Model Strategy (v7.0.10) · `docs/features/quality-security-proof/BUILD-SPEC.md` §1
- Investigation dispatch: `telemetry/agents/subagents-dispatch.yaml#2026-06-15-qsp-guardrail-matrix-scoping`

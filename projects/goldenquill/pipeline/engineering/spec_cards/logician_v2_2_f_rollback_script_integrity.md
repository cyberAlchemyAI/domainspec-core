# Spec card — Logician gate F-ROLLBACK-SCRIPT-INTEGRITY (§4 v2.2 amendment-policy enforcement)

**STATUS:** LOCKED

**Blueprint anchors:**
- `pipeline/blueprint/v0.1/section_04_logician.md` v2.1 (current LOCK)
- `pipeline/engineering/amendments/agent_sdk_thesis_2026-04-19/` — EN-001 RT-NEW-01 follow-through
- Consolidated backlog: `pipeline/engineering/spec_cards/logician_v2_2_gates.md` gate #5

**Spec-card version:** v1
**Round:** Logician v2.2 — Wave 3 (external state: Ed25519 + HMAC-SHA3-512)
**Date:** 2026-04-20
**Failure-code prefix:** `F-AMDT-05`

---

## Gate name and failure code

- **Gate:** `F-ROLLBACK-SCRIPT-INTEGRITY`
- **Failure code:** `F-AMDT-05`
- **Kind:** PRE-gate on rollback-script execution

## Purpose

Every amendment with a rollback script carries an implicit trust claim: "if this amendment fails, run this script to revert." A tampered rollback script could corrupt pipeline state under the authority of the original amendment's audit evidence. This gate verifies two integrity properties before any rollback script executes: (a) the script's Ed25519 signature is valid against the pinned public key, and (b) the ledger hash at the ledger head matches the script's pinned ledger hash, ensuring the script was authored for the current state of the lock history.

## Trigger condition

Fires as a PRE-gate before execution of any script registered in the `rollback_scripts` manifest (currently `spike_rollback.sh` from EN-001; extensible to future rollback scripts). Gate fires on the execution request, not on script registration.

## Input contract

```python
@runtime_checkable
class SignatureVerifyCallable(Protocol):
    def __call__(self, script_bytes: bytes, signature: bytes, public_key: bytes) -> bool: ...

@runtime_checkable
class LedgerHashReaderCallable(Protocol):
    def __call__(self) -> str: ...

@runtime_checkable
class ScriptMetadataReaderCallable(Protocol):
    def __call__(self, script_path: str) -> dict: ...
```

- `script_path: str` — path to the rollback script to be executed.
- `script_bytes: bytes` — raw bytes of the script file (read externally, passed in).
- `signature: bytes` — Ed25519 signature over `script_bytes` (from the rollback_scripts manifest or sidecar `.sig` file).
- `public_key: bytes` — pinned Ed25519 public key from the sovereignty envelope.
- `ledger_hash_reader: LedgerHashReaderCallable` — injected callable returning the current HMAC-SHA3-512 hash at the ledger head.
- `script_metadata_reader: ScriptMetadataReaderCallable` — injected callable returning script metadata including `ledger_hash_at_pin`.

## Pass/fail criteria (deterministic — no LLM)

1. **Signature check:** call `signature_verify(script_bytes, signature, public_key)`. If returns `False` → FAIL.
2. **Ledger hash check:** read current ledger hash via `ledger_hash_reader()`. Read script's `ledger_hash_at_pin` from metadata via `script_metadata_reader(script_path)`. Compare exact string equality. Mismatch → FAIL.
3. **PASS:** both checks succeed.
4. **FAIL (`F-AMDT-05`):** either check fails. Detail specifies which check(s) failed.
5. **FAIL (`F-AMDT-05`):** any injected callable raises. Fail-closed.

## Failure behavior

- **DENY** the rollback script execution. Script does NOT run.
- Emit structured failure record to `pipeline/metrics/session_log.jsonl` with `event: "F-AMDT-05"`, `gate: "F-ROLLBACK-SCRIPT-INTEGRITY"`, `check_failed: "signature"|"ledger_hash"|"both"`, `script_path`.
- Mandatory operator escalation. A failed rollback integrity check may indicate tampering — operator must inspect manually before any manual rollback.

## Implementation notes

- Pure Python, zero LLM tokens, fail-closed.
- Uses §2 Round M `crypto_primitives` if available; falls back to stdlib `hashlib` + third-party Ed25519 per E-011 crypto-agility envelope.
- All crypto operations via injected Protocols (E-017 pattern). No direct `import hashlib` or `import nacl` in gate code.
- Lives at `pipeline/logician/gates/f_rollback_script_integrity.py`.
- AST-lint R1–R5 clean at module load.
- Wave 3 because it depends on Ed25519 infrastructure and HMAC-SHA3-512 ledger hash (external state).

## Test criteria

### Unit tests (≥30)
- Valid signature + matching ledger hash → PASS.
- Invalid signature + matching ledger hash → DENY.
- Valid signature + mismatched ledger hash → DENY.
- Invalid signature + mismatched ledger hash → DENY (both failures reported).
- Empty script bytes + valid signature over empty bytes → PASS (degenerate but valid).
- Script modified by single byte → signature invalid → DENY.
- Ledger hash differs by one character → DENY.
- Parametrized over multiple script paths (registered scripts).
- Metadata missing `ledger_hash_at_pin` → DENY.
- Signature is empty bytes → DENY.
- Public key is wrong key → DENY.

### Adversarial tests (≥5)
- `test_adv_signature_verify_raises` → DENY (fail-closed).
- `test_adv_ledger_hash_reader_raises` → DENY (fail-closed).
- `test_adv_script_metadata_reader_raises` → DENY (fail-closed).
- `test_adv_signature_valid_but_for_different_script` → signature verifies against different bytes, not `script_bytes` → DENY (signature is checked against the actual bytes passed in).
- `test_adv_ledger_hash_is_prefix_match_not_exact` → ledger hash is a prefix of the pinned hash → DENY (exact equality, not startswith).

## Dependencies

- §2 Round M `crypto_primitives` or stdlib Ed25519 (E-011 fallback).
- Sovereignty envelope with pinned public key (exists in locked architecture).
- `lock_history.v1.jsonl` HMAC-SHA3-512 ledger hash (computed at head).
- Rollback scripts manifest (currently contains `spike_rollback.sh`).
- §4 v2.1 gate infrastructure (PRE-gate hook on script execution).

## §0.5 paired-commit rows

| Row | Content |
|-----|---------|
| Code | `pipeline/logician/gates/f_rollback_script_integrity.py` |
| Tests | `tests/logician/gates/test_f_rollback_script_integrity.py` + `tests/logician/gates/test_adv_f_rollback_script_integrity.py` |
| Lock history | `pipeline/engineering/lock_history.v1.jsonl` row with `gate: "F-ROLLBACK-SCRIPT-INTEGRITY"`, `failure_code: "F-AMDT-05"` |
| Blueprint amendment | §4 v2.2 blueprint delta row for F-AMDT-05 |
| Memory | MEMORY.md index entry |

---

*Spec card v1 — 2026-04-20 — per-gate card split from consolidated logician_v2_2_gates.md.*

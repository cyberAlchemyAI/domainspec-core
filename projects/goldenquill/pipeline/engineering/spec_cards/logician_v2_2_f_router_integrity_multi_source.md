# Spec card — Logician gate F-ROUTER-INTEGRITY-MULTI-SOURCE (§4 v2.2 amendment-policy enforcement)

**STATUS:** LOCKED

**Blueprint anchors:**
- `pipeline/blueprint/v0.1/section_04_logician.md` v2.1 (current LOCK)
- `pipeline/engineering/amendments/agent_sdk_thesis_2026-04-19/en003_cross_family_audit_cycle4/red_team_verdict.md` — EN-003 Cycle 4 C4-NEW-02
- Consolidated backlog: `pipeline/engineering/spec_cards/logician_v2_2_gates.md` gate #10
- Related module: `pipeline/sovereignty/router_integrity.py` (Round H)

**Spec-card version:** v1
**Round:** Logician v2.2 — Wave 3 (external state: git log + HMAC-chain reader)
**Date:** 2026-04-20
**Failure-code prefix:** `F-AMDT-10`

---

## Gate name and failure code

- **Gate:** `F-ROUTER-INTEGRITY-MULTI-SOURCE`
- **Failure code:** `F-AMDT-10`
- **Kind:** PRE-gate on `router.yaml` change promotion (paired with `router_integrity.pinned.json`)

## Purpose

C4-NEW-02 (EN-003 Cycle 4 Red Team): the existing same-commit pair rule — "changes to `router.yaml` MUST co-commit with `router_integrity.pinned.json`" — is defeated by a single malicious commit touching both files. A tampering adversary with write access can craft one commit that updates `router.yaml` and simultaneously rewrites the pinned hashes to match. The rule as text enforces co-presence but not authenticity. This gate adds a third independent integrity source — an HMAC-chained manifest signed per-update with a key held outside the repo — so a valid router change requires agreement across three sources: (1) the live `router.yaml`, (2) `router_integrity.pinned.json` hashes, (3) the external HMAC-chained manifest signature. No single-commit mutation can satisfy all three.

## Trigger condition

Fires as a PRE-gate on any operation that promotes a `router.yaml` change (detected by diff against the last-known-good hash, or by any write-lock release on the file). Gate validates the three-source consistency before the change lands in any seat's runtime binding.

## Input contract

```python
@runtime_checkable
class RouterYamlReaderCallable(Protocol):
    def __call__(self) -> bytes: ...

@runtime_checkable
class PinnedHashReaderCallable(Protocol):
    def __call__(self) -> dict: ...

@runtime_checkable
class ExternalManifestReaderCallable(Protocol):
    def __call__(self) -> dict: ...  # {chain_head_hash, signature, prior_chain_head_hash}

@runtime_checkable
class SignatureVerifyCallable(Protocol):
    def __call__(self, manifest_bytes: bytes, signature: bytes, public_key: bytes) -> bool: ...
```

- `router_yaml_reader: RouterYamlReaderCallable` — returns raw bytes of current `router.yaml`.
- `pinned_hash_reader: PinnedHashReaderCallable` — returns parsed `router_integrity.pinned.json` content.
- `external_manifest_reader: ExternalManifestReaderCallable` — returns the HMAC-chained manifest from an external path (out-of-repo vault, operator-controlled).
- `signature_verify: SignatureVerifyCallable` — injected Ed25519 verifier (matches F-ROLLBACK-SCRIPT-INTEGRITY pattern).
- `public_key: bytes` — pinned public key from sovereignty envelope.

## Pass/fail criteria (deterministic — no LLM)

1. **Source 1 (live file hash).** Compute SHA3-512 of `router_yaml_reader()` output. Call this `live_hash`.
2. **Source 2 (pinned hash).** Read `pinned_hash_reader()["router_yaml_sha3_512"]`. Call this `pinned_hash`. If absent → FAIL.
3. **Source 3 (external manifest).** Read `external_manifest_reader()`. Extract `chain_head_hash`, `signature`, `prior_chain_head_hash`. If any absent → FAIL.
4. **Pairwise consistency:**
   - `live_hash == pinned_hash` (router.yaml matches pinned record) → else FAIL `F-AMDT-10-PAIR`.
   - Manifest's `chain_head_hash == live_hash` (external manifest records the current router state) → else FAIL `F-AMDT-10-EXTERNAL`.
5. **Signature verification:** manifest bytes signed with Ed25519 signature; `signature_verify` returns `True` → else FAIL `F-AMDT-10-SIGNATURE`.
6. **Chain continuity:** `prior_chain_head_hash` must match the prior live-known `router_yaml_sha3_512` recorded in the previous manifest row (HMAC-chain property — out-of-repo manifest has its own chain history). If break → FAIL `F-AMDT-10-CHAIN-BREAK`.
7. **PASS:** all four checks succeed.
8. **FAIL-CLOSED:** any injected callable raises → DENY `F-AMDT-10-READER-FAIL`.

## Failure behavior

- **DENY** the router.yaml promotion. Change is rejected; seats keep prior bindings.
- Emit to `pipeline/metrics/session_log.jsonl` with `event: "F-AMDT-10-{PAIR|EXTERNAL|SIGNATURE|CHAIN-BREAK|READER-FAIL}"`, `live_hash`, `pinned_hash`, `manifest_chain_head`, `signature_valid`.
- Operator remediation: three-source divergence is a security-class incident. Operator inspects all three sources, signs a new manifest row only after manual reconciliation.

## Implementation notes

- Pure Python, zero LLM tokens, fail-closed.
- External manifest path is operator-configurable via a pinned envelope reference; default location is **outside the repo** (e.g., `~/.tilth/sovereignty/router_integrity_manifest.jsonl`), so a repo-write-only adversary cannot tamper with it.
- `SignatureVerifyCallable` reuses the Ed25519 Protocol contract from F-ROLLBACK-SCRIPT-INTEGRITY (gate #5). Shared infrastructure, not re-declared.
- Chain history is a hash-chain (each row's `prior_chain_head_hash` points to the previous row's `chain_head_hash`) — gate only checks the head-to-prior link; full chain walk is a separate integrity scan cron.
- Lives at `pipeline/logician/gates/f_router_integrity_multi_source.py`.
- AST-lint R1–R5 clean at module load.
- Wave 3 because it depends on Ed25519 signature verification + external manifest reader.

## Test criteria

### Unit tests (≥30)

- Three sources consistent + valid signature + chain-continuous → PASS.
- `live_hash != pinned_hash` → DENY `F-AMDT-10-PAIR`.
- `manifest_chain_head != live_hash` → DENY `F-AMDT-10-EXTERNAL`.
- Signature invalid → DENY `F-AMDT-10-SIGNATURE`.
- Chain break (`prior_chain_head_hash` doesn't match prior manifest row) → DENY `F-AMDT-10-CHAIN-BREAK`.
- Pinned hash field missing → DENY.
- External manifest missing → DENY.
- Public key empty bytes → signature check fails → DENY.
- Parametrized: all four checks individually mutated → each FAIL maps to the correct failure-code suffix.

### Adversarial tests (≥5 — C4-NEW-02 threat model)

- `test_adv_single_commit_mutates_router_and_pinned` — simulate a single malicious commit that mutates both `router.yaml` and `router_integrity.pinned.json` to new consistent values. External manifest still reflects prior state. → DENY `F-AMDT-10-EXTERNAL` (the attack the gate is designed to catch).
- `test_adv_signature_valid_but_for_different_manifest` — signature verifies over a different manifest payload → DENY `F-AMDT-10-SIGNATURE`.
- `test_adv_chain_head_is_current_but_prior_chain_head_forged` — adversary crafts a fake chain-continuity link → DENY `F-AMDT-10-CHAIN-BREAK`.
- `test_adv_all_readers_raise` → DENY fail-closed on first raise.
- `test_adv_router_yaml_empty` — empty file, hash matches pinned record of empty, manifest consistent → PASS (degenerate but valid — operator cleared the file intentionally).

## Dependencies

- `pipeline/sovereignty/router_integrity.py` (Round H) for hash computation reuse.
- Ed25519 signature infrastructure from F-ROLLBACK-SCRIPT-INTEGRITY (gate #5) — shared Protocol.
- External manifest file under operator-controlled path (`~/.tilth/sovereignty/router_integrity_manifest.jsonl` default).
- §4 v2.1 gate infrastructure (PRE-gate hook on router promotion).

## §0.5 paired-commit rows

| Row | Content |
|-----|---------|
| Code | `pipeline/logician/gates/f_router_integrity_multi_source.py` |
| Tests | `tests/logician/gates/test_f_router_integrity_multi_source.py` + `tests/logician/gates/test_adv_f_router_integrity_multi_source.py` |
| External manifest schema | Documented in sovereignty envelope + bootstrap row for the initial router state |
| Lock history | `pipeline/engineering/lock_history.v1.jsonl` row with `gate: "F-ROUTER-INTEGRITY-MULTI-SOURCE"`, `failure_code: "F-AMDT-10"` |
| Blueprint amendment | §4 v2.2 blueprint delta row for F-AMDT-10 |
| Memory | MEMORY.md index entry |

## Origin

EN-003 Cycle 4 Red Team Finding C4-NEW-02: `router.yaml` + `router_integrity.pinned.json` same-commit pair rule is satisfied by a single malicious commit touching both files. Text-level closure cannot bind an in-repo pair rule to external integrity; structural closure via a third out-of-repo HMAC-chained signed manifest is required.

---

*Spec card v1 — 2026-04-20 — new gate from EN-003 Cycle 4 C4-NEW-02 parked to v2.2 queue per operator disposition.*

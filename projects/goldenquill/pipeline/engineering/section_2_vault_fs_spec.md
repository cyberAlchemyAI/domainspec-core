# Round E — `vault_fs.py` Spec Card

**Section:** 1 (Sovereignty Envelope)
**Module:** `pipeline/sovereignty/vault_fs.py`
**Dependencies:** Round A (`crypto_primitives` including the Round-C extension: `SecretBytes`, `aesgcm_encrypt/decrypt`, `pbkdf2_sha3_512`); Round B (`topology` — `canonicalize_vault_path`, `is_doc_sourced_path`); Round C (`keys` — `KeyStore`, `MacOSKeychainKeyStore`, `FileKeyStore`, `NonceReused`); Round D (`isolation` — `OrgRootNamespace`, `within_org_root`, `with_org_root`).
**Downstream consumer:** Section 2 Vault (`vault_write` / COMPOUND dispatcher). vault_fs is the Section-1 envelope primitive that Section 2 sits on top of — Section 2 adds the COMPOUND transaction + path-allowlist layer; vault_fs provides the at-rest encryption + signed binding substrate.
**Filed:** 2026-04-19
**Status:** Spec draft — awaiting Round D LOCK-internal (isolation.py) before kickoff.

---

## 1. Purpose

Implements the Section-1 secrets-at-rest envelope. Every vault artifact under `orgs/{slug}/vault/` is:

1. Written atomically (temp-file + `RENAME_NOREPLACE` / `RENAME_EXCL` → no torn reads).
2. Encrypted with AES-GCM-256 under a per-artifact DEK derived from an operator KEK via HKDF (implemented here with `pbkdf2_sha3_512` to stay stdlib-plus-`cryptography` per the Round-C LOCK).
3. Signed with the operator's Ed25519 key over the canonical-JSON header + ciphertext.
4. Bound to the `OrgRootNamespace` that produced it — a sealed file from `ns(A)` cannot be opened under `ns(B)` even with the right keys (Law 3 enforcement at the primitive layer).

Section 2's `vault_write` intents (`claim-evidence-write`, `admin-risk-append`, `conversation-log-append`, `rails-report-write`, `lessons-delta-append`) all flow through `vault_fs.seal()` at persist time; reads flow through `vault_fs.open_and_verify()`.

## 2. Primitives

### 2.1 `SealedArtifact` (frozen dataclass, kw_only)

Public carrier type; returned by `seal()`, consumed by `open_and_verify()`.

Fields:
- `header: SealedArtifactHeader` — signed-over metadata (see §2.2).
- `ciphertext: bytes` — AES-GCM ciphertext (plaintext + tag).
- `operator_signature: OperatorSignature` (from `_types.py` A12.3) — Ed25519 over `canonical_bytes(header) || ciphertext`.

### 2.2 `SealedArtifactHeader` (frozen dataclass, kw_only)

Signed-over envelope metadata. Bound into the signature so tampering the header fails verify.

Fields:
- `schema_version: str` — `"vault_fs.v1"`.
- `org_slug: str` — canonical slug; MUST match the containing `OrgRootNamespace`.
- `vault_path_relative: str` — path relative to `orgs/{slug}/vault/` (e.g. `"claim_evidence/2026-04-19T12:00:00Z.json"`).
- `content_type: str` — MIME-ish tag (`"application/json"`, `"text/markdown"`, etc.); used by readers to pick decoders.
- `dek_salt_hex: str` — 16 bytes hex; salt for KEK → DEK derivation via `pbkdf2_sha3_512` (§8 FILE_KEYSTORE_PBKDF2_ITERATIONS carries forward).
- `aead_nonce_hex: str` — 12 bytes hex; per-write nonce (enforced unique via Round-C `NonceRegistry`).
- `aead_aad: bytes` — AAD binds `(schema_version || org_slug || vault_path_relative || ns.root_inode || ns.volume_uuid)` so a sealed file cannot be relocated between orgs or replayed after a volume remount.
- `created_at_iso8601: str` — UTC `Z`.
- `key_id: str` — KEK identifier from `keys.py` KeyStore; used by the reader to fetch the KEK for DEK re-derivation.
- `not_after_iso8601: str | None` — optional expiry; `None` means no ceiling. When set, `open_and_verify()` refuses reads after the ceiling (fail-closed).

Signed-over canonical bytes: `canonical_bytes(header) || ciphertext`. Nothing outside the header fields participates in the signature — the ciphertext integrity is covered by GCM's tag AND by the outer Ed25519 sig.

## 3. Public API

### 3.1 `seal(plaintext, *, ns, vault_path_relative, content_type, key_store, operator_key_id, nonce_registry, not_after=None) -> SealedArtifact`

Encrypts + signs + returns an in-memory sealed artifact. Does NOT touch the filesystem — write is a separate primitive (`seal_and_write`) so callers can seal-for-transport.

Pre-conditions enforced in order:
1. `ns.org_slug == canonical_slug(vault_path_relative.split('/')[0] or ns.org_slug)` — header/org binding.
2. `vault_path_relative` does NOT contain `..` or absolute roots (belt-and-suspenders against path-escape).
3. `ns.root_inode` still matches the filesystem (via `within_org_root(ns.root_path, ns)`); fails `F-VAULT-FS-INODE-DRIFT` if not.
4. `nonce_registry` returns False for the generated `aead_nonce_hex` (otherwise raise `NonceReused`).

Post-conditions:
- DEK is `SecretBytes`-wrapped and zeroized before return.
- Nonce is committed to the registry only AFTER the sig is computed (atomic against a crash-mid-seal leaving a phantom nonce).

### 3.2 `seal_and_write(plaintext, *, path, ns, ...same args as seal) -> Path`

Composes `seal()` + atomic write. Uses `with_org_root(ns)` so the directory FD is held for the entire temp-file-rename cycle (TOCTOU closure). Write pattern:
1. `tempfile.NamedTemporaryFile(dir=parent_of(path), delete=False)` — same directory so rename is atomic.
2. Write canonical-JSON-of-full-`SealedArtifact` bytes.
3. `fsync(fd)` then `os.rename(temp, path)` using `RENAME_NOREPLACE` (Linux) / `renamex_np(..., RENAME_EXCL)` (macOS) per §8 of the provisioning manifest.
4. `fsync(parent_fd)` to durably persist the directory entry.

Returns the canonical resolved path (post-rename).

### 3.3 `open_and_verify(path, *, ns, key_store, nonce_registry) -> VerifiedArtifact`

Inverse of `seal_and_write`. Fail-closed checks in order; any failure short-circuits with a well-formed exception:

1. `within_org_root(path, ns)` — `F-VAULT-FS-PATH-ESCAPE`.
2. Read bytes via an `O_NOFOLLOW | O_CLOEXEC` open under `with_org_root(ns)` directory FD.
3. Parse outer `SealedArtifact`; reject unknown `schema_version`.
4. Verify operator Ed25519 signature over `canonical_bytes(header) || ciphertext` — `F-VAULT-FS-SIG-INVALID`.
5. Check `not_after_iso8601` — `F-VAULT-FS-EXPIRED`.
6. Check `aead_aad`-embedded `ns.root_inode` and `ns.volume_uuid` against current ns state — `F-VAULT-FS-NS-REBIND` if drift.
7. Look up KEK in `key_store` by `header.key_id`; derive DEK via `pbkdf2_sha3_512(kek, salt, §8 ITERATIONS, 32)` inside a `SecretBytes`.
8. AES-GCM-decrypt with DEK + nonce + AAD; on failure → `F-VAULT-FS-AEAD-INVALID`.
9. Check nonce NOT in the registry's replay index (separate from §3.1's uniqueness-at-write check) — `F-VAULT-FS-NONCE-REPLAY`.
10. Return `VerifiedArtifact(header=..., plaintext=plaintext, verified_at=utcnow())`.

Plaintext is returned as `bytes` (not `SecretBytes`) — the caller owns the lifetime and zeroization decision. Rationale: vault content is JSON/markdown the caller immediately decodes; wrapping in `SecretBytes` adds friction without meaningful security because plaintext ends up on the caller's heap anyway.

### 3.4 `rotate_dek(path, *, ns, key_store, nonce_registry, new_operator_key_id) -> Path`

Re-seals an existing artifact under a new operator KEK without plaintext exfiltrating the trusted boundary. Composes `open_and_verify` → in-`SecretBytes` re-encrypt → atomic rename. Used by Section 1 A12 crypto-agility rotations (v0.2 Ed25519 → hybrid).

## 4. Failure-code surface (F-VAULT-FS-*)

All fail-closed; all carry enough context to populate an admin-risk ledger row:

| Code | Trigger |
|---|---|
| `F-VAULT-FS-INODE-DRIFT` | ns root inode changed mid-seal |
| `F-VAULT-FS-VOLUME-DRIFT` | ns volume UUID changed mid-seal or mid-open |
| `F-VAULT-FS-PATH-ESCAPE` | path not under ns.root after resolution |
| `F-VAULT-FS-SIG-INVALID` | Ed25519 verify failure |
| `F-VAULT-FS-AEAD-INVALID` | GCM tag mismatch (tampered ciphertext OR wrong key) |
| `F-VAULT-FS-EXPIRED` | `not_after_iso8601` in past |
| `F-VAULT-FS-NS-REBIND` | AAD-embedded inode/volume doesn't match current ns |
| `F-VAULT-FS-NONCE-REPLAY` | nonce appears twice in registry |
| `F-VAULT-FS-SCHEMA-UNKNOWN` | header schema_version not recognized |
| `F-VAULT-FS-KEY-MISSING` | KEY_ID not resolvable in key_store |

All codes carry the `org_slug` + `vault_path_relative` + `key_id` (never the raw key bytes — per §4.10.7.9 token non-logging discipline inherited from Section 4).

## 5. Test surface (Round E LOCK gate)

Per Autonomy Rule 2 + Round A/B/C/D lessons:

**Unit (`tests/sovereignty/test_vault_fs.py`):**
- `test_seal_roundtrip_plaintext_recovered`
- `test_seal_returns_distinct_nonces_across_writes`
- `test_open_and_verify_rejects_wrong_operator_key`
- `test_open_and_verify_rejects_wrong_org_ns`
- `test_open_and_verify_rejects_tampered_ciphertext`
- `test_open_and_verify_rejects_tampered_header`
- `test_open_and_verify_rejects_expired_artifact`
- `test_seal_rejects_path_escape`
- `test_seal_and_write_atomic_on_crash` (simulate mid-rename crash)
- `test_rotate_dek_changes_key_id_without_plaintext_leak`

**Adversarial (`tests/sovereignty/test_vault_fs_adversarial.py`):**
- `test_adv_nonce_replay_caught_across_sessions`
- `test_adv_header_swapped_between_two_sealed_artifacts`
- `test_adv_ciphertext_grafted_onto_foreign_header`
- `test_adv_symlink_swap_during_seal_and_write` (TOCTOU race vs isolation.py gate)
- `test_adv_key_rotation_mid_read_fails_closed`
- `test_adv_not_after_in_past_blocks_open`
- `test_adv_volume_remount_between_seal_and_open_fails_closed`
- `test_adv_nonce_registry_corruption_fails_closed`

## 6. Property tests (feed Round J harness)

- **P-VFS-1:** For every `(plaintext, ns, path)` input, `open_and_verify(seal_and_write(plaintext, ...))` yields bytes equal to `plaintext`.
- **P-VFS-2:** For every sealed artifact `A` signed by key `K`, verify fails for every `K' ≠ K`.
- **P-VFS-3:** Mutating any byte of the on-disk ciphertext OR header fails `open_and_verify`.
- **P-VFS-4:** Two seals of the same plaintext produce distinct ciphertexts (GCM nonce uniqueness).
- **P-VFS-5:** A sealed artifact produced under `ns_A` never successfully opens under `ns_B`, even when `A.org_slug == B.org_slug` but `root_inode` differs.

## 7. Provisioning manifest delta

No new Python deps — `cryptography` already pulled in by Round C. Post-Round-E LOCK, the manifest §3.3 row for `cryptography` adds "§5.4 BT4 AES-GCM + vault_fs seal/open" to the Purpose column. No §8.x constant changes; Round E re-uses `FILE_KEYSTORE_PBKDF2_ITERATIONS`, `FILE_KEYSTORE_SALT_BYTES`, `FILE_KEYSTORE_AEAD_NONCE_BYTES` from Round-C's §8 block.

One manifest §7 addition (`orgs/{slug}/vault/.vault_fs_nonce_registry.jsonl` — the append-only nonce registry file). Signed on every append via the Round-A HMAC trailer pattern; chained hash per Section-1 audit-ledger conventions.

## 8. Out of scope (explicit non-goals)

- **Compound-transaction staging** — that's Section 2 v7.1's `begin/commit/abort` surface. vault_fs.seal() is always SIMPLE; COMPOUND is Section 2's wrapper that stages multiple `seal()` calls and commits atomically.
- **Cedar policy evaluation** — Section 4 Logician's job. vault_fs's path-escape / ns-binding checks are the mechanical enforcement only; policy is layered on top.
- **Post-quantum signature** — v0.2 work item per A12. Round E ships Ed25519-only; the `OperatorSignature.algorithm` field's `"hybrid-ed25519-ml-dsa-65"` value is reserved but not implemented.
- **Key rotation scheduling** — the `rotate_dek()` primitive exists; policy for when to invoke it lives in Section 4 Logician's rotation cadence.

## 9. Handoff

Ready for Claude Code implementation after Round D (isolation.py) LOCK-internal. Two CC windows expected:

- **Window A** — implementation + unit tests (~2-3 hours on Mac Mini 8GB; module + ~15 unit tests).
- **Window B** — adversarial tests + property tests (~1-2 hours; 8 adversarial + 5 property). Committee dispatch as a separate window after Window B.

Per engineering-process §2 batching criteria: Round E is a single-module ship (no public-API breakage, no cross-section-boundary change) so it does NOT batch with any sibling round. It ships alone and integrates at Section-2 sealing time.

Per L-005 two-audit discipline: Audit #1 (scoping) → fix → Audit #2 (verification) → LOCK-internal or escalate. No silent third round.

# Customer-Side Attestation Tool — Design Document

**Status:** DESIGN — pinned for Phase One contractor implementation
**Created:** 2026-05-04
**Addresses:** B2 (Golden Quill Improvement Plan), CTO Q&A Prep Q3 gap
**Architecture anchor:** v7 LOCKED A12 (crypto-agility), M15 (signed-commit discipline), Section T (hybrid signature path)

---

## 1. Purpose

A read-only verifier that runs on the Golden Quill appliance and produces a signed attestation report. The customer inspects their own appliance's posture without trusting Sovereign Node's binaries. The tool answers: "Is my appliance configured the way I was told it would be?"

The tool is NOT part of the pipeline. It does not write to the Vault, does not invoke seats, does not require API keys, and does not make outbound network calls. It is a standalone inspection binary.

---

## 2. Verification Surface — What the Tool Inspects

The attestation report covers seven inspection targets. Each produces a deterministic value the customer can compare against their deployment manifest's expected values.

| # | Target | What is captured | Expected-value source |
|---|--------|-----------------|----------------------|
| 1 | **Posture configuration** | Active posture enum (`sovereign`, `hybrid`, `unrestricted`) + loaded posture manifest path + manifest content hash (SHA-3-512) | Deployment manifest delivered at provisioning |
| 2 | **Loaded modules** | Sorted list of Python/LangGraph module paths currently importable by the pipeline process, with per-module content hash. Specifically flags presence/absence of outbound-capable modules (Anthropic client, OpenAI client, Google client, Groq client, Channel-F web-search BYOK module) | Sovereign-mode manifest declares zero outbound modules loaded |
| 3 | **Network egress** | Enumeration of all outbound-capable socket paths: active connections (via `ss`/`netstat`), configured DNS resolvers, SearxNG bind address if present, firewall rules (nftables/iptables export). Under Sovereign posture: egress allowlist must be empty or localhost-only | Sovereign-mode: zero non-loopback egress. Hybrid-mode: only declared provider endpoints |
| 4 | **M15 ledger head** | Current HEAD commit hash of `vault_shared/` signed-commit ledger + operator signature verification status (VALID / INVALID / MISSING) against operator keyring | Customer receives operator public key at provisioning; ledger HEAD matches last known-good |
| 5 | **Golden Image signature** | Content hash of the appliance's base system image (read from immutable partition or verified filesystem snapshot) + signature verification against Sovereign Node LLC's release signing key | Published release manifest on Sovereign Node's signed-releases page |
| 6 | **Loaded Cedar policy hash** | SHA-3-512 of the concatenated Cedar policy files currently loaded by Logician, in deterministic sorted order | Policy hash published in deployment manifest; changes require M15.3 HIGH-severity ledger entry |
| 7 | **Declared seat slate** | Contents of `router.yaml` — seat names, primary model bindings, fallback model bindings, family tags — plus the M15-signed commit hash of the file | Matches provisioning-time router.yaml delivered to customer |

---

## 3. Signing Discipline — How Output Is Authenticated

### 3.1 Software-backed signing (Phase One, v0.1–v0.2)

The attestation tool signs its output with the **appliance's attestation keypair** — generated on the appliance at first boot, never exported. The keypair follows architecture A12's crypto-agility commitment:

- **v0.1:** Ed25519 signing key. `OperatorSignature` dataclass with `algorithm: str` (never hardcoded pattern-match per F-CRYPTO-AGILITY-HARDCODED).
- **v0.2:** Hybrid Ed25519 + ML-DSA-65 (FIPS 204, 128-bit PQ security). Both legs must verify for the report to be accepted as valid.
- **v0.3:** Pure ML-DSA-65 after fleet-wide key rotation.

The **public key** is:
1. Displayed to the customer at provisioning (QR code + hex fingerprint on physical card shipped with Golden Quill).
2. Registered in a customer-accessible verification registry (signed by Sovereign Node LLC's release key).
3. Optionally publishable to a customer-controlled keyserver if the customer wants third-party verification.

### 3.2 Signature structure

```
AttestationReport {
  version: "1.0"
  timestamp_iso8601: string
  appliance_id: string (hardware serial or provisioning UUID)
  posture: PostureAttestation
  modules: ModuleAttestation
  egress: EgressAttestation
  m15_ledger: LedgerAttestation
  golden_image: ImageAttestation
  cedar_policy: CedarAttestation
  seat_slate: SeatSlateAttestation
  report_hash: SHA-3-512 of canonical JSON of above fields
  signature: {
    algorithm: string  // "ed25519" | "ed25519+ml-dsa-65" | "ml-dsa-65"
    ed25519_sig: bytes | null
    ml_dsa_sig: bytes | null
    public_key_fingerprint: string
  }
}
```

### 3.3 Verification flow (customer side)

1. Customer runs attestation tool → receives signed JSON + human-readable report.
2. Customer verifies signature against the public key they received at provisioning.
3. Customer compares each field against the expected values in their deployment manifest.
4. Any mismatch = the appliance is not in the declared state. Customer contacts support or takes remedial action.

The verification does NOT require network access. It is fully offline-capable.

---

## 4. Hardware-Backed Extension (Longer Arc)

### 4.1 Trust root upgrade path

| Hardware | Trust primitive | Timeline |
|----------|---------------|----------|
| NVIDIA DGX Spark | TPM 2.0 — attestation key stored in hardware, platform measurement registers (PCR) chain from firmware to application | Phase Two (post-v0.2 fleet) |
| Apple Mac Studio | Secure Enclave Processor (SEP) — hardware-bound signing key, anti-replay monotonic counter, boot-policy attestation | Phase Two (Mac Studio fleet) |
| M1 Mac Mini (dev) | Software-only (no SEP attestation API exposed to userland on M1 with macOS constraints) | Dev-tier remains software-signed |

### 4.2 Hardware attestation adds

- **Measured boot chain:** PCR values from firmware → bootloader → kernel → application form a hash chain. Attestation report includes PCR quote signed by hardware key. Customer verifies the quote against known-good PCR values published per release.
- **Anti-rollback:** Monotonic counter prevents replaying an old attestation report as if it were current.
- **Key non-exportability:** The signing key physically cannot leave the hardware. Even a compromised OS cannot extract it — only produce signatures through the hardware interface.
- **Remote attestation (optional):** For customers who want third-party verification without physical access, the hardware attestation quote can be verified against the TPM/SEP manufacturer's endorsement key chain. This is opt-in and does not require the appliance to phone home.

### 4.3 Transition discipline

Hardware-backed attestation does not replace software attestation — it layers over it. The report carries both:
- Software signature (attestation keypair, per §3.1)
- Hardware quote (TPM/SEP, when available)

A customer who trusts only the hardware root ignores the software signature. A customer on dev-tier hardware uses only the software signature. Both are valid verification paths.

---

## 5. Customer Ergonomics

### 5.1 Single-command invocation

```bash
tilth attestation report
```

No arguments required for default behavior. Optional flags:

```bash
tilth attestation report --format json        # JSON only (default: both)
tilth attestation report --format human       # Human-readable only
tilth attestation report --output /path/to/   # Write to specific directory
tilth attestation report --verify /path/to/manifest.json  # Auto-compare against expected values
```

### 5.2 Output artifacts

Every invocation produces two files in the working directory (or `--output` path):

1. **`attestation_report_<timestamp>.txt`** — Human-readable report. Plain English description of each inspection target, its current value, and PASS/FAIL/WARN status if `--verify` was provided. No jargon. A non-technical executive director can read it.

2. **`attestation_report_<timestamp>.json`** — Signed JSON (per §3.2 schema). Machine-parseable. Carries the cryptographic signature. This is the evidentiary artifact for audits, compliance reviews, or dispute resolution.

### 5.3 Human-readable report structure (example)

```
=== Golden Quill Attestation Report ===
Generated: 2026-05-04T14:23:07Z
Appliance: GQ-2026-0042 (Mac Studio 128GB)

POSTURE: Sovereign
  Manifest hash: a3f8...c912 (SHA-3-512)
  Status: MATCHES expected value

LOADED MODULES: 47 modules loaded
  Outbound-capable modules: NONE LOADED
  Status: PASS (Sovereign mode verified)

NETWORK EGRESS:
  Active outbound connections: 0
  Firewall rules: deny-all-egress (nftables)
  SearxNG: bound to 127.0.0.1:8888
  Status: PASS

M15 LEDGER:
  HEAD: 7b2e...f401
  Operator signature: VALID (key: josh@fitfarms fingerprint b8c1...4d22)
  Status: PASS

GOLDEN IMAGE:
  Image hash: 91dc...3a8f
  Release signature: VALID (Sovereign Node LLC release key)
  Status: MATCHES published release GQ-v1.2.0

CEDAR POLICIES:
  Policy hash: e4a7...b193 (6 policy files, sorted)
  Status: MATCHES deployment manifest

SEAT SLATE (router.yaml):
  Scout: [primary family] / [fallback family]
  Scribe: [primary family] / [fallback family]
  Editor: [primary family] / [fallback family]
  Judge: [primary family] / [fallback family]
  Logician: deterministic (no model)
  M15 commit hash: VALID
  Status: MATCHES provisioning configuration

OVERALL: ALL CHECKS PASS
Signature: Ed25519 (fingerprint b8c1...4d22)
```

### 5.4 Verification against expected values

When `--verify` is provided with a manifest path, the tool performs field-by-field comparison and reports:

- **PASS** — observed value matches expected value exactly.
- **WARN** — observed value differs in a non-security-critical dimension (e.g., additional non-outbound modules loaded since provisioning).
- **FAIL** — observed value contradicts a security-critical expected value (outbound module loaded under Sovereign posture, egress path open, policy hash mismatch, signature invalid).

Exit codes: `0` = all PASS, `1` = any FAIL, `2` = tool error.

### 5.5 No elevated privileges required

The tool reads system state through standard inspection interfaces (procfs, ss/netstat, nftables list, filesystem reads). It does NOT require root except for:
- Golden Image verification (read access to immutable partition — may require `sudo` depending on mount configuration)

If run without root, the tool reports Golden Image status as `SKIPPED (requires elevated privileges)` and all other targets proceed normally.

---

## 6. Security Properties of the Tool Itself

- **Read-only.** The tool writes only its output report files. It never modifies appliance state, Vault content, pipeline configuration, or Cedar policies.
- **No network.** The tool makes zero network calls. All inspection is local.
- **Deterministic.** Same appliance state → same report content (modulo timestamp). Two consecutive runs with no intervening state change produce identical field values.
- **Self-verifiable.** The tool binary itself is covered by the Golden Image hash. A tampered tool would produce a report whose Golden Image hash differs from the published release — detectable by comparing against the published hash out-of-band.
- **Open-source verification path.** The tool's source is published. A sufficiently motivated customer can compile from source and verify the binary matches the shipped binary (reproducible builds are a Phase Two target but source-auditable in Phase One).

---

## 7. Integration with Architecture

| Architecture primitive | How attestation tool relates |
|----------------------|----------------------------|
| A12 crypto-agility | Signing discipline follows the Ed25519 → hybrid → pure ML-DSA migration path. `OperatorSignature` dataclass reused. F-CRYPTO-AGILITY-HARDCODED enforced on tool source. |
| M15 signed-commit | Tool verifies M15 ledger HEAD signature as one of its seven targets. Uses same keyring verification logic. |
| M14 Vault | Tool does NOT read Vault content (grant data). Only reads Vault-adjacent config (`router.yaml`, Cedar policies, manifest). Law 3 preserved. |
| Section T | Tool is the first consumer of the A12 hybrid signing path in customer-facing context. |
| v7.0.1 GPP (DRAFT) | GPP discipline runs Logician-side at pipeline start. Attestation tool runs customer-side on demand. Complementary, not overlapping. GPP is internal enforcement; attestation is external verification. |
| BT14 org-isolation | Tool reveals no org-specific data. Report contains only system-level configuration state. |

---

## 8. Implementation Scope for Phase One Contractor

**In scope (must ship):**
- Single compiled binary (Rust or Go — contractor's choice, must produce reproducible build)
- Seven inspection targets per §2
- Ed25519 signing per §3.1 (v0.1 path)
- Human-readable + signed JSON dual output per §5.2
- `--verify` comparison mode per §5.4
- Exit codes per §5.4
- Unit tests covering each inspection target independently
- Integration test against a known-good Sovereign-mode appliance image

**Out of scope (Phase Two):**
- Hardware-backed signing (§4)
- ML-DSA-65 hybrid (arrives with v0.2 crypto-agility rollout)
- Remote attestation
- Reproducible-build CI pipeline (target, not gate)
- GUI or web dashboard for report viewing

---

## 9. Open Questions for Contractor Kickoff

1. **Language choice:** Rust (smaller binary, better memory safety guarantees, harder to hire) vs. Go (faster contractor onboarding, larger binary, adequate for read-only tool). Operator leans Rust but defers to contractor expertise + timeline.
2. **Golden Image verification mechanism:** Immutable partition with dm-verity hash tree (Linux/DGX Spark) vs. Signed System Volume (macOS/Mac Studio). May need platform-specific codepath.
3. **Key ceremony:** How the attestation keypair is generated at first boot, how the public key is extracted for the provisioning card, and how key rotation works if the appliance is re-provisioned. Needs a key-ceremony spec before implementation begins.

---

*End of design document.*

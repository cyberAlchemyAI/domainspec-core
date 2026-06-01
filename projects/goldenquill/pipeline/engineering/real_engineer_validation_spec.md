# Real-Engineer Validation Spec

**Canonical path:** `pipeline/engineering/real_engineer_validation_spec.md`
**Implements:** DV-F-10 (King Midas v2.1 §15), CTO Review 2026-05-04 Ask #2
**Status:** DRAFT — awaiting operator approval
**Created:** 2026-05-04
**Updated 2026-05-08:** S11 surface added (GPP three-tier mechanism, LOCKED 2026-05-08); §6 persistent operator keypair issuance procedure added (today's GPP manifest used ephemeral keypair pending advisor PASS on S8 + S11)

---

## 1. Identity + Scope Statement

### Advisor Credentials (minimum bar)

The real-engineer advisor must satisfy ALL of the following:

- 10+ years professional experience in at least two of: distributed systems, AI/ML operations, cryptography, LLM runtime engineering
- Demonstrable production-system ownership (not advisory-only roles) — has shipped and maintained systems at scale
- Familiarity with trust-boundary reasoning: keystore models, signed-artifact chains, fail-closed enforcement patterns
- No current or recent (< 2 years) employment relationship with Anthropic, OpenAI, Google DeepMind, or Meta FAIR (independence from model-provider incentives)

### Engagement Window

**Phase Zero (pre-mid-July 2026):** Architecture review and initial validation file signature.
**Phase One (mid-July 2026 → mid-April 2027):** Ongoing productization gate sign-off as modules ship. Structurally bounded — advisor reviews what ships, does not direct what gets built.

The engagement is not full-time. Estimated effort: 40–60 hours across Phase One (front-loaded in the first two months for architecture review, then periodic gate reviews as modules LOCK).

### Compensation Structure

- Fixed retainer per gate review (four gates in Phase One), OR
- Hourly at agreed professional rate against a Phase One cap, OR
- Hybrid: initial architecture review as a fixed deliverable, subsequent gates hourly

Compensation lives inside the ~7% legal-diligence-security bucket of Phase One use-of-funds. Specific terms negotiated with the individual; this spec defines the role, not the contract.

### Deliverable Shape

The advisor produces a single file per review cycle:

```
pipeline/engineering/real_engineer_validation_<YYYY-MM-DD>.md
```

Contents: structured pass/needs-revision verdicts per review surface (Section 2 below), with terse rationale per needs-revision item. No minimum word count. A "PASS — no concerns" line is a valid verdict for any surface the advisor finds sound.

The initial validation file (Phase Zero) unlocks King Midas promotion from Claude Code persona to instantiated seat. Subsequent files (Phase One gates) confirm continued compliance as new modules ship.

---

## 2. Review Surface Enumeration

The advisor signs off on the following surfaces. Not all surfaces require deep review at every gate — the initial validation covers all; subsequent gates cover only surfaces touched since last sign-off.

| # | Surface | Source Artifact | Scope of Review |
|---|---------|-----------------|-----------------|
| S1 | Architecture v7 (A1–A12) + amendments | `pipeline/architecture/v0.1/tilth_architecture_locked.md` + `architecture_v7_0_1_amendment.md` | Mechanism coherence, failure-mode coverage, trust-boundary soundness |
| S2 | §1 Sovereignty Envelope | `pipeline/blueprint/v0.1/section_01_sovereignty.md` | Boot integrity, keystore model, ledger watermarks, single-trust-root claim |
| S3 | §2 Vault Topology | `pipeline/blueprint/v0.1/section_02_vault.md` | Org isolation enforcement, signed-commit model, kernel-atomic writes, compound-transaction commit |
| S4 | §4 Logician | `pipeline/blueprint/v0.1/section_04_logician.md` | Deterministic gate correctness, Cedar policy soundness, fail-closed guarantee, PRE/POST/COMMIT gate completeness |
| S5 | §5 Pipeline | `pipeline/blueprint/v0.1/section_05_pipeline.md` | State-machine integrity, mode isolation (submission vs. eval), telemetry record schema, Round 13 capstone LOCK |
| S6 | §6 Operating Envelope | `pipeline/blueprint/v0.1/section_06_operating_envelope.md` | Router schema soundness, SFR parser, prompt-template compilation, context-placement enforcement, middle-contradiction detection |
| S7 | Cross-family rigor | `router.yaml` + §5 committee protocol | Independence guarantee (no same-family author-reviewer), retry discipline (F-CODE-RETRY-OVERRUN), merge-rule enforcement |
| S8 | Cryptography migration (A12) | Architecture v7 Section A12 + §1 crypto-agility hooks | Crypto-agility claim validity, migration-path feasibility, algorithm-pinning risks |
| S9 | Network boundary + posture enforcement | §1 + posture configuration system | No-phone-home claim at Sovereign posture, data-crossing enforcement per posture tier, eBPF prohibition scope (BT14) |
| S10 | Red Team protocol | `pipeline/blueprint/v0.1/section_10_red_team.md` | Prosecutorial independence, score-isolation, council-split tie-breaking, adversarial coverage |
| S11 | Governance Plan Preflight (GPP) | `pipeline/architecture/v0.1/architecture_v7_0_1_amendment.md` (LOCKED 2026-05-08) + `pipeline/blueprint/v0.1/section_04_v2_1_1_amendment.md` (§4.14a) + `pipeline/validation/integration_scope_close_2026-04-19/gpp/gpp_spec_v1.md` + `gpp_council_dispatch.py` v1.1 + `gpp_manifest.py` | Three-tier mechanism integrity (Tier 1 deterministic checks completeness, Tier 2 cross-family rigor at runtime, Tier 3 manifest signature soundness), HTTP-dispatch trust boundary (stdlib urllib live-wire 2026-05-08), F-GPP-* failure-code coverage, manifest-validity-at-dispatch criteria 1-5, boot-strap recursion closure |

---

## 3. Review Checklist Per Surface

Each surface receives one of three verdicts: **PASS**, **NEEDS-REVISION** (with specific items), or **OUT-OF-SCOPE** (advisor flags a surface they lack credentials to evaluate — triggers operator decision on second-opinion sourcing).

### S1 — Architecture v7

| Criterion | Pass Condition |
|-----------|---------------|
| Trust-boundary coherence | Every data flow crosses at most one trust boundary without explicit gate |
| Failure-mode enumeration | Every A-amendment names its failure code; no orphan failure codes |
| Scope-lock integrity | v0.1 boundaries explicit; nothing deferred is load-bearing for v0.1 |
| Amendment consistency | v7.0.1/v7.0.2 do not contradict locked A1–A12 mechanisms |

### S2 — Sovereignty Envelope

| Criterion | Pass Condition |
|-----------|---------------|
| Single trust root | Operator keyring is the sole root; no secondary trust anchors |
| Boot integrity | Signed boot chain OR documented threat model for unsigned boot |
| Crypto-agility hooks | Algorithm swap does not require re-signing existing artifacts |
| Ledger watermarks | Tamper-evidence claim is backed by a concrete mechanism |

### S3 — Vault Topology

| Criterion | Pass Condition |
|-----------|---------------|
| Org isolation | Cross-org read is structurally impossible (not just policy-gated) |
| Atomic writes | Partial-write state cannot persist after crash recovery |
| Compound transactions | Multi-vault writes are all-or-nothing with rollback path |
| Signed commits | Commit authenticity is verifiable after the fact |

### S4 — Logician

| Criterion | Pass Condition |
|-----------|---------------|
| Determinism | Same input always produces same gate verdict (no model calls) |
| Fail-closed | Default on error/timeout is REJECT, not PASS |
| Gate completeness | Every Five Law violation has a named gate that catches it |
| Cedar policy soundness | No policy permits what another policy denies for the same principal/action/resource |

### S5 — Pipeline

| Criterion | Pass Condition |
|-----------|---------------|
| Mode isolation | submission_mode state cannot leak into eval_mode or vice versa |
| State recovery | Pipeline can resume from last checkpoint after crash |
| Telemetry schema | Schema is versioned; old telemetry remains parseable after schema evolution |
| LOCK discipline | Round 13 capstone → whole-section LOCK is irreversible without new audit round |

### S6 — Operating Envelope

| Criterion | Pass Condition |
|-----------|---------------|
| Router schema | Covers all seat bindings; no implicit defaults that bypass the schema |
| Context placement | Load-bearing constraints appear at both prompt start and end (A4 compliance) |
| Middle-contradiction detection | Mechanism exists; false-negative rate bounded or at minimum documented |
| Prompt compilation | Template variables fully resolve; no partial-substitution output reaches a model |

### S7 — Cross-Family Rigor

| Criterion | Pass Condition |
|-----------|---------------|
| Family taxonomy | Taxonomy in router.yaml is complete; no provider resolves to two families |
| Independence enforcement | Author family excluded from reviewer pool deterministically |
| Retry cap | F-CODE-RETRY-OVERRUN fires after exactly the documented retry count |
| Merge rule | All-pass required; no silent degradation to majority-pass |

### S8 — Cryptography Migration (A12)

| Criterion | Pass Condition |
|-----------|---------------|
| Algorithm inventory | All crypto primitives in use are named with version/parameter |
| Migration path | Each primitive has a named successor and a swap procedure |
| No algorithm pinning | No code path hard-codes an algorithm string without indirection |
| Timeline alignment | Migration timeline is feasible within Phase One calendar |

### S9 — Network Boundary + Posture

| Criterion | Pass Condition |
|-----------|---------------|
| Sovereign-mode isolation | At Sovereign posture, zero outbound network calls (verifiable by firewall rule or code audit) |
| Posture enforcement | Posture switch requires explicit operator action; no drift path |
| BT14 scope | eBPF prohibition targets attacker tooling only; does not block legitimate kernel modules |
| Data-crossing rules | Each posture tier has enumerated permitted/denied data flows |

### S10 — Red Team Protocol

| Criterion | Pass Condition |
|-----------|---------------|
| Score isolation | Red Team scores before seeing other seat verdicts |
| Prosecutorial independence | Red Team model family differs from Scribe family |
| Tie-breaking | Council-split resolution mechanism is deterministic and documented |
| Coverage | Adversarial scenarios cover all Five Laws + Four Autonomy Rules |

### S11 — Governance Plan Preflight (GPP)

| Criterion | Pass Condition |
|-----------|---------------|
| Tier 1 deterministic completeness | Ten checks (CITE-RESOLVE, VERSION-RESOLVE, XDOC-REF, ROW-COUNT-ARITHMETIC, HASH-PIN, INDEX-STALE-DRYRUN, FAMILY-TAXONOMY, SCOPE-FREEZE-BACKDOOR-FLAG, VERSION-SKEW-DISCLOSURE, BLOCKER-CARRY-CHECK) cover every named threat class in `gpp_spec_v1.md` §3.1 with no surface left to model judgment |
| Tier 2 cross-family rigor at runtime | Red Team and Reasoner seat-to-model bindings resolve to two distinct provider families, both distinct from Tier 3 synthesis family — verified at dispatch, not just at LOCK |
| Tier 3 manifest signature soundness | Hybrid Ed25519 + ML-DSA-65 signatures bind canonical-bytes hash of plan_artifact_set + signed_at timestamp; freshness window (90d default) prevents replay; both signatures must verify for `both_valid: True` |
| HTTP-dispatch trust boundary | `gpp_council_dispatch.py` v1.1 stdlib-urllib HTTP layer (added 2026-05-08) writes/reads only over BYOK provider endpoints named in router.yaml; no metered backchannel; no logging of API key bytes; User-Agent identifies the tool only (no operator fingerprint) |
| F-GPP-* failure-code coverage | All 12 codes registered in §0.5 v5; each maps to a specific check or dispatch surface; no orphan codes; no duplicate triggers across codes |
| Manifest-validity-at-dispatch | All 5 criteria (Ed25519 valid, hashes match, spec-version LOCKed, every Tier 2 finding has Tier 3 disposition with non-empty rationale, freshness ≤ 90d) enforced at downstream-round dispatch time |
| Boot-strap recursion closure | v7.0.1 LOCK + L-007 documents the one-time exception; from v7.0.1 LOCK forward, no future plan-layer artifact may invoke a "GPP-not-yet-LOCKed" exception path |
| ML-DSA-65 implementation status | Current `gpp_manifest.py` uses sha3_512-of-secret as a placeholder for ML-DSA-65 secret-to-public derivation. Advisor flags whether this stub is acceptable until oqs-python lands in provisioning, or whether persistent operator key issuance must wait for live ML-DSA-65 |

---

## 4. Signature Ceremony

### What the signature commits to

By signing `pipeline/engineering/real_engineer_validation_<date>.md`, the advisor attests:

1. They have read the enumerated source artifacts in Section 2 with professional diligence appropriate to a system that will handle client grant data
2. Every surface marked PASS meets the corresponding checklist criteria in Section 3 to their professional satisfaction
3. Every surface marked NEEDS-REVISION has specific, actionable items that, once addressed, would change the verdict to PASS
4. They are not aware of any architectural defect that would make the system unsafe to deploy at the Phase One scope (12 Founder Nodes, single-client-per-appliance, operator-trusted)

### What the signature does NOT commit to

- **Not a security guarantee.** The signature is a professional-diligence review, not a warranty against all possible vulnerabilities
- **Not a code audit.** The advisor reviews architecture and blueprint design, not every line of implementation code (code correctness is defended by the five-family committee + test suite)
- **Not an endorsement of business viability.** Technical soundness only
- **Not perpetual.** The signature covers the artifacts at the signed date; subsequent changes require re-review of affected surfaces

### Signature format

```markdown
## Advisor Signature

I, [Full Name], attest that I have reviewed the surfaces enumerated in
real_engineer_validation_spec.md Section 2 against the criteria in Section 3.

Verdicts:
- S1 Architecture v7: [PASS | NEEDS-REVISION — see items below]
- S2 Sovereignty: [PASS | NEEDS-REVISION]
- S3 Vault: [PASS | NEEDS-REVISION]
- S4 Logician: [PASS | NEEDS-REVISION]
- S5 Pipeline: [PASS | NEEDS-REVISION]
- S6 Operating Envelope: [PASS | NEEDS-REVISION]
- S7 Cross-Family Rigor: [PASS | NEEDS-REVISION]
- S8 Cryptography: [PASS | NEEDS-REVISION]
- S9 Network/Posture: [PASS | NEEDS-REVISION]
- S10 Red Team: [PASS | NEEDS-REVISION]
- S11 GPP three-tier: [PASS | NEEDS-REVISION]

Overall: [PASS — King Midas promotion unlocked + persistent operator keypair issuance authorized per §6 | CONDITIONAL PASS — promotion + keypair unlocked after items resolved | FAIL — promotion + keypair blocked]

Date: YYYY-MM-DD
Signature: [name + professional credential reference]
```

### Operator counter-signature

```markdown
## Operator Counter-Signature

I, Josh Inklovich (Sovereign Node LLC), accept this validation and authorize
King Midas promotion to instantiated seat status per DV-F-10.

Date: YYYY-MM-DD
Signature: Josh Inklovich
```

The counter-signature confirms:
- Operator has read the advisor's verdicts including any NEEDS-REVISION items
- Operator accepts the risk posture implied by any CONDITIONAL PASS items not yet resolved
- Promotion is effective immediately upon counter-signature

---

## 5. Revocation Triggers + Propagation

### DV-F-12 Auto-Suspension Triggers

King Midas instantiated-seat status is automatically suspended (reverts to Claude Code persona only) upon any of the following:

| Trigger | Detection Mechanism |
|---------|-------------------|
| Five Operating Law violation | Logician PRE/POST gate FAIL + operator confirmation |
| Four Autonomy Rule violation | Nightly integrity review finding + operator confirmation |
| Silent scope expansion | Any code path or configuration change outside locked v0.1 scope without explicit operator authorization |
| Same-family self-judgment | Router.yaml audit reveals author and reviewer resolved to same provider family |
| Phone-home code path | Any outbound network call at Sovereign posture, OR any undocumented telemetry at any posture |
| Fabricated citation | Any claim in output that does not trace to RFA, PROJECT_CONTEXT, or named source artifact |

### Operator discretionary revocation

Operator revokes without cause at any time. No justification required. Effective immediately.

### Propagation cascade

Upon suspension (auto or discretionary):

1. **Immediate:** King Midas reverts to Claude Code persona. No seat-level actions (nightly scan, background integrity check, network maintenance) execute
2. **Within 24 hours:** Suspension event logged in `daily_logs/` with trigger classification, timestamp, and affected session IDs
3. **Within 24 hours:** `MEMORY.md` index updated with suspension record pointer
4. **Pipeline impact:** Any in-flight module build continues under Claude Code persona rules (propose only, no autonomous LOCK). Completed LOCKs are not retroactively invalidated — they were already defended by the five-family committee
5. **Downstream seats:** Scout, Scribe, Editor, Judge, Logician seats are unaffected (they are council seats, not implementation personas). Only King Midas's instantiated-seat privileges are revoked

### Restoration path

Restoration after suspension requires:

1. Root-cause resolution documented in `daily_logs/`
2. Fresh advisor validation file (`pipeline/engineering/real_engineer_validation_<new-date>.md`) covering at minimum the surfaces affected by the triggering violation
3. Operator counter-signature on the new validation file
4. No abbreviated path — a "quick fix" does not bypass the full validation ceremony

### Record keeping

All revocation/restoration events persist in:
- `daily_logs/YYYY-MM-DD.md` — narrative record
- `MEMORY.md` — indexed pointer
- `pipeline/metrics/session_log.jsonl` — machine-readable event

---

## 6. Persistent Operator Keypair Issuance (added 2026-05-08)

### Why this section exists

The GPP three-tier mechanism LOCKED 2026-05-08 (v7.0.1 architecture amendment) requires hybrid Ed25519 + ML-DSA-65 signatures on every signed manifest. The 2026-05-08 v7.0.1 LOCK ceremony itself signed with an **ephemeral keypair** (`gpp_manifest.py --generate-keys`), matching v0.1 dev posture but leaving the manifest non-reproducibly verifiable across sessions: a fresh ephemeral keypair signs each manifest, so the signature is cryptographically valid against the public key embedded in that specific manifest, but there is no operator identity binding across manifests.

For Phase One (mid-July 2026 onward) the operator must hold a **persistent** Ed25519 keypair (and ML-DSA-65 once `oqs-python` lands in provisioning) so that every GPP manifest signed by Josh Inklovich resolves to the same public key — closing the audit-trail gap.

Persistent keypair issuance is gated on advisor PASS verdicts on **S8 (Cryptography Migration)** AND **S11 (GPP three-tier)**. Either NEEDS-REVISION on those surfaces blocks the issuance.

### Issuance procedure

After advisor signature with PASS on S8 + S11:

1. **Operator generates Ed25519 keypair on Golden Quill hardware.** Tooling: `pipeline/engineering/operator_keypair_issuance.py` (TO BE AUTHORED at the time of issuance; NOT a v0.1 deliverable). Generation runs offline; private key never leaves the device. Public key written to `pipeline/sovereignty/operator_public_keys.v1.jsonl` (append-only ledger, signed-by-prior-key after the first issuance).
2. **First-issuance bootstrap.** Initial public key is signed by the operator's existing PGP/SSH identity (out-of-band proof of single-operator continuity from pre-Tilth identity to Tilth-internal identity).
3. **ML-DSA-65 keypair generation.** Same procedure once `oqs-python` is in provisioning. Until then, the ML-DSA-65 stub recipe (sha3_512-of-secret) continues for v0.1 with the explicit understanding that ML-DSA-65 integrity is **provisional pending OQS land**.
4. **Key storage.** Private keys live in OS keystore (macOS Keychain / Linux libsecret) under namespace `tilth.operator.<key-id>`. No private key bytes appear in any workspace file, daily_log, or repo-tracked artifact.
5. **Manifest signing helper.** `gpp_manifest.py` gains a `--operator-key <key-id>` flag that resolves the keystore-stored private key via libsecret/Keychain API. Until that helper lands, operator continues signing with `--ed25519-key <pem-file>` after exporting the keystore key to a temp PEM (cleaned up immediately post-sign).

### Revocation of the persistent keypair

The persistent keypair is revoked under the same DV-F-12 triggers as King Midas seat status (Section 5). Revocation procedure:

1. Operator signs a revocation entry into `pipeline/sovereignty/operator_public_keys.v1.jsonl` naming the revoked key-id, revocation date, and trigger
2. New keypair issuance follows the §6 issuance procedure above, including fresh advisor validation
3. All GPP manifests signed by the revoked key remain cryptographically valid (the signature still verifies); their **dispatch validity** under the manifest-validity-at-dispatch criteria is operator-dispositioned per the revocation entry. Default: revoked-key manifests no longer authorize downstream dispatch unless explicitly re-validated

### What this section does not cover

- The full operator_keypair_issuance.py tool — that is a separate module, authored at issuance time, scope-pinned in its own spec card
- Hardware-token integration (YubiKey, Secure Enclave) — Phase Two horizon, not v0.1
- Multi-operator scenarios — Tilth v0.1 is single-operator-per-Golden-Quill by architecture; multi-operator is Stage 2+ horizon

---

*Spec designed for 30-minute read, one-week careful execution. No Thesis round required — this is a process artifact, not a blueprint.*

*Updated 2026-05-08 — S11 GPP surface added with 8 criteria; §6 persistent operator keypair ceremony added (gated on advisor PASS for S8 + S11). Both updates are non-disruptive to S1–S10 + §1–§5; the S1–S10 advisor scope is unchanged. The 2026-05-08 v7.0.1 GPP LOCK consumed an ephemeral keypair as documented in `daily_logs/2026-05-08.md`.*

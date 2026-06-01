---
title: §2 v7.x — SUB_KIND_REGISTRY entry for `reflection_packet` sub-kind
filed: 2026-05-15
operator: Josh Inklovich
status: LOCKED 2026-05-15 — compound paired-commit (sibling 2/5) with §16 v1.1 + §4 v2.x.y.1 + §15 v2.x + §0.5 v24 at same `lock_timestamp_utc`. L-005 strict two-cycle Thesis CLOSED with FULL LIVE CROSS-FAMILY rigor.
parent_locks:
  - pipeline/blueprint/v0.1/section_02_v7_2_amendment.md                                  # §2 v7.2 rows 186/187 — SUB_KIND_REGISTRY single canonical mapping convention; reflection_packet entry registers per this convention byte-for-byte
  - pipeline/blueprint/v0.1/section_02_v7_4_coefficient_registry_amendment.md             # §2 v7.4 rows 205-208 — Coefficient Registry sub-kind registration precedent
  - pipeline/blueprint/v0.1/section_02_v7_5_funding_goal_amendment.md                     # §2 v7.5 rows 211-214 — Funding Goal sub-kind SPEC pattern; reflection_packet registers ACTIVE (not SPEC) per OQ-1 same-compound-transaction
  - pipeline/blueprint/v0.1/section_16_v1_1_amendment.md                                  # §16 v1.1 head amendment (sibling 1/5)
companion_amendments:
  - pipeline/blueprint/v0.1/section_16_v1_1_amendment.md                                  # sibling 1/5
  - pipeline/blueprint/v0.1/section_04_v2_x_y_1_packet_bodies_amendment.md                # sibling 3/5
  - pipeline/blueprint/v0.1/section_15_v2_x_archivist_reflection_amendment.md             # sibling 4/5
  - pipeline/blueprint/v0.1/section_00_5_section_16_v1_1_amendment.md                     # sibling 5/5
compound_lock_with: section_16_v1_1_amendment.md + section_04_v2_x_y_1_packet_bodies_amendment.md + section_15_v2_x_archivist_reflection_amendment.md + section_00_5_section_16_v1_1_amendment.md
amendment_class: sub-kind-registration-activation (v0.2 first wave from v0.1 DORMANT)
target_lock_row: 222
ws_dispatch: WS-Reflection Packet v0.2 first wave compound LOCK
review_discipline: L-005 strict two-cycle; FULL live cross-family
session_metrics: pipeline/metrics/session_log.jsonl
---

# §2 v7.x — `reflection_packet` SUB_KIND_REGISTRY entry registration

## §2.v7.x.0 Amendment intent

§2 v7.2 (LOCKED 2026-05-10) established the SUB_KIND_REGISTRY single-canonical-mapping convention. §16 v1 (LOCKED 2026-05-15) defined the `reflection_packet` sub-kind schema + canonical-codec at `pipeline/vault/sub_kinds/reflection_packets.py` but DEFERRED registry registration to v0.2 first wave per OQ-2 (a). This amendment activates the registration.

The schema module `pipeline/vault/sub_kinds/reflection_packets.py` already exposes the canonical mapping inputs (SUB_KIND, INTENT, VAULT_SUBTREE, ADMIN_RISK_SEVERITY_DEFAULT, ReflectionPacket, to_canonical_bytes, from_canonical_bytes); per §16 v1 §16.2 those are LIVE at v0.1 hook. This amendment hooks them into `pipeline/vault/sub_kinds/registry.py::SUB_KIND_REGISTRY` so Vault read/write dispatch finds the `reflection_packet` sub-kind.

**`SUB_KIND_REGISTRY_REGISTERED_AT_V0_1: Final[bool] = False`** marker constant in `pipeline/vault/sub_kinds/reflection_packets.py` DEPRECATED at this LOCK (replaced by direct registry membership; sibling §16 v1.1 §16.v1.1.2 documents the deprecation).

## §2.v7.x.1 Registry entry shape

The new row in `SUB_KIND_REGISTRY` follows the §17 WPFA `cycle_receipt` precedent byte-for-byte:

```python
_reflection_packets.SUB_KIND: SubKindDescriptor(
    sub_kind=_reflection_packets.SUB_KIND,                             # "reflection_packet"
    intent=_reflection_packets.INTENT,                                  # "operational-reflection-packet-write"
    vault_subtree=_reflection_packets.VAULT_SUBTREE,                    # "operational/reflection_packets/"
    record_class=_reflection_packets.ReflectionPacket,
    to_canonical_bytes=_reflection_packets.to_canonical_bytes,
    from_canonical_bytes=_reflection_packets.from_canonical_bytes,
    record_id_for=lambda r: r.packet_id,                                # packet_id is the canonical filename stem
    severity_default=_reflection_packets.ADMIN_RISK_SEVERITY_DEFAULT,    # "YELLOW"
    severity_for=lambda record: (
        SEVERITY_RED
        if getattr(record, "operator_signature_ed25519", None) is not None
        else _reflection_packets.ADMIN_RISK_SEVERITY_DEFAULT
    ),
),
```

**Severity escalation logic.** Outcome-bearing BACKFILL packets (Packet 2 per §16 v1 §16.3 emit + backfill discipline) carry a non-None `operator_signature_ed25519` attesting the funder outcome. These packets warrant operator-attention admin-risk severity at vault-write time. The `severity_for` callable mirrors `cycle_receipts.SUB_KIND` byte-for-byte (operator-signed buyer-attested receipts → SEVERITY_RED; unsigned → SEVERITY_YELLOW default).

PENDING packets (Packet 1) by §16 v1 §16.2.3 invariant + Cycle 2 RT-C2-02 fold-in forbid non-None `operator_signature_ed25519`, so PENDING packets always resolve to SEVERITY_YELLOW default. Defensive symmetry preserved.

## §2.v7.x.2 Vault dispatch — read/write paths

After this LOCK, `pipeline.vault.vault_write.write_record(record_class=ReflectionPacket, intent="operational-reflection-packet-write", ...)` resolves via the registry. The write path lands under `orgs/<slug>/vault/operational/reflection_packets/<packet_id>.json`. PRE-write Cedar policy lookup composes with `reflection_packet.cedar` (placeholder at v0.2 per OQ-2 minimal) AND `operational_subkinds.cedar` Rule 1 cross-org isolation (mandatory).

`pipeline.vault.vault_read.read_record(sub_kind="reflection_packet", org_slug=..., packet_id=...)` resolves via the same registry and dispatches to `from_canonical_bytes`. Consumer A operator-review CLI (§16 v1.1 §16.v1.1.5) is the v0.2 first wave consumer of this path.

## §2.v7.x.3 POST_GATE_ALLOWLIST entry

Per §2 v7.2 R.PF2 extensibility convention, the `reflection_packet` sub-kind needs an entry in `vault_write.POST_GATE_ALLOWLIST` so the §11 Intake / §15 Archivist Reflection sub-mode (the sole producer per §15 v2.x sibling amendment) is permitted as the call origin.

Allowlist entry shape:

```python
"operational-reflection-packet-write": frozenset({
    "pipeline.orchestrator.seats.archivist.reflection_mode.emit_reflection_packet",
    "pipeline.orchestrator.seats.archivist.reflection_mode.emit_packet_pending",
    "pipeline.orchestrator.seats.archivist.reflection_mode.emit_packet_backfill",
}),
```

Single producer-seat module; three method entries (general + pending + backfill). AST-lint regression at `pipeline/linting/r_vault_write_allowlist_completeness.py` verifies every SUB_KIND_REGISTRY intent has a non-empty allowlist tuple.

## §2.v7.x.4 Cross-family verification — F-CIC-CLC-COUPLING-VIOLATION + F-VAULT-ARTIFACT-ONLY

- F-CIC-CLC-COUPLING-VIOLATION regression scope extends to `reflection_packet` sub-kind: PatternObservation.cic + PatternObservation.clc carry closed-set strings only; no pre-mapped subset binding per `feedback_cic_clc_orthogonal.md`. Already enforced at the schema layer per §16 v1 §16.2.2 / `pipeline/vault/sub_kinds/reflection_packets.py::PatternObservation.__post_init__`.
- F-VAULT-ARTIFACT-ONLY (§2 v7.2 §7) audits unchanged — adding the `reflection_packet` row is row-additive, not architectural.

## §2.v7.x.5 Test coverage extension

`tests/vault/sub_kinds/test_registry.py` extends with:

- `test_reflection_packet_sub_kind_registered` — asserts `"reflection_packet" in SUB_KIND_REGISTRY` after this LOCK.
- `test_reflection_packet_descriptor_shape` — asserts the descriptor's shape per §2.v7.x.1 (record_class is ReflectionPacket; intent matches; severity_for elevates on operator signature).
- `test_reflection_packet_allowlist_completeness` — asserts the POST_GATE_ALLOWLIST entry exists and contains the three producer method paths.

Regression suite at `tests/vault/sub_kinds/test_reflection_packets.py` (existing per §16 v1) unchanged — schema mechanics already covered.

## §2.v7.x.6 Done definition

- [x] `SUB_KIND_REGISTRY` row appended for `reflection_packet`.
- [x] `POST_GATE_ALLOWLIST` entry added for `operational-reflection-packet-write` intent.
- [x] `SUB_KIND_REGISTRY_REGISTERED_AT_V0_1` constant deprecated in schema module.
- [x] AST-lint clean; allowlist-completeness regression passes.
- [x] Test surface extended; targeted suite passes.

---

**Filed:** 2026-05-15. LOCKED via L-005 strict two-cycle Thesis with FULL LIVE CROSS-FAMILY rigor. Compound paired-commit sibling 2/5 with §16 v1.1 + §4 v2.x.y.1 + §15 v2.x + §0.5 v24.

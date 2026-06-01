---
title: §4 v2.x Logician — Card Hardening (F-CARDS-* + F-CIC-CLC-PATTERN-READ-DURING-ELIGIBILITY)
filed: 2026-05-15
operator: Josh Inklovich
status: DRAFT — LOCK-READY. Paired with architecture v7.0.11 + §18 v1 + §0.5 v?? paired-commit. Predicate signatures land at LOCK with `NotImplementedError` bodies (graduates LIVE at v0.2 first wave per architecture v7.0.11 §5 binding split). Mirrors precedent set by §4 v2.x §5.1 F-CLASS-* dormant primitives (LOCKED 2026-05-10 row 193/194) and §4 v2.x.y F-PACKET-* (LOCKED 2026-05-15 row 222).
parent_locks:
  - pipeline/blueprint/v0.1/section_04_v2_x_amendment.md                          # §4 v2.x LOCKED 2026-05-10 — F-CLASS-* family format pattern this section mirrors byte-for-byte
  - pipeline/blueprint/v0.1/section_04_v2_x_3_amendment.md                        # §4 v2.x.3 LOCKED 2026-05-15 row 219 — F-REPORT-* graduation precedent
  - pipeline/architecture/v0.1/architecture_v7_0_8_amendment.md                   # v7.0.8 LOCKED 2026-05-08 — F-CIC-CLC-COUPLING-VIOLATION family origin (extended by F-CIC-CLC-PATTERN-READ-DURING-ELIGIBILITY below)
parent_amendment_paired_DRAFT: pipeline/architecture/v0.1/architecture_v7_0_11_card_amendment.md
companion_amendments_DRAFT:
  - pipeline/blueprint/v0.1/section_18_card_system.md
  - pipeline/blueprint/v0.1/section_00_5_section_18_card_amendment.md
authority: Operator directive 2026-05-15 + revised feedback PDF (preserved at docs/post_alpha/post_alpha_card_system_revised_2026-05-15.md §11). Splits the Logician hardening into its own §4 amendment per the revised feedback's lock-candidate-package list.
predicate_realization_horizon: v0.2 first wave (graduates NotImplementedError → LIVE alongside Phase B runtime context injection per architecture v7.0.11 §5).
---

# §4.X.0 — Purpose

The Card System introduces a workspace-shared knowledge layer (`cards:cic:*`, `cards:clc:*`, `cards:matrix:*`) consumed by Scout, Scribe, Judge, Logician itself, Archivist, Report Generator, and the model router. Without dedicated Logician hardening, the card layer would create six new failure modes (schema invalidity, unsigned production load, private-data leak into shared cards, cross-org namespace mixing, CIC↔CLC coupling re-introduction, and pattern-read-during-eligibility coupling). This section authors the F-CARDS-* family and one extension to v7.0.8's F-CIC-CLC-* family.

**Predicate body horizon.** Following the v7.0.7 §5.1 F-CLASS-* dormant-primitives precedent + v7.0.9 F-REFLECTION-* dormant pattern + §16 v1 F-PACKET-* row-222 NotImplementedError-then-graduate pattern, this section LOCKs the predicate signatures + Cedar policy stubs at v7.0.11 with `NotImplementedError` bodies. Bodies graduate LIVE at v0.2 first wave when seat-level card consumers exist (Phase B runtime context injection per architecture v7.0.11 §5). The META-gate **F-CARDS-COVERAGE-INCOMPLETE** carries LIVE body at v7.0.11 LOCK as the dormant-binding lever (mirrors §16 v1 F-PACKET-COVERAGE-INCOMPLETE row-222 + §4 v2.x F-CLASS-COVERAGE-INCOMPLETE).

# §4.X.1 — F-CARDS-* family roster (seven primitives + one extension)

## §4.X.1.1 F-CARDS-COVERAGE-INCOMPLETE

**Gate kind:** META PRE-cycle gate.

**Mode-sensitive behavior** (per architecture v7.0.11 §1.6 #1; differs from F-CLASS-COVERAGE-INCOMPLETE byte-for-byte mirror — bifurcates by mode + field essentiality):

- Development mode: WARN on any missing required card field; never FAIL.
- Production mode + missing field's seat dependency declared in `pipeline/cards/loader.py` seat-defaults registration: FAIL CLOSED.
- Production mode + missing field is nonessential or explicitly `_status: forward_compat`: WARN; do not block.

**Module:** `pipeline/logician/gates/f_cards_coverage_incomplete.py`.

**Predicate body status at v7.0.11 LOCK:** LIVE. The META-gate is the dormant-binding lever for the rest of the F-CARDS-* family; it must work at LOCK to gate the deployment.

**Predicate signature:**

```python
def f_cards_coverage_incomplete(
    *,
    environment: Literal["development", "production"],
    card_namespace: str,
    seat_dependencies: Mapping[str, frozenset[str]],
    card_fields_present: frozenset[str],
) -> GateOutcome:
    """
    Returns PASS, WARN, or FAIL based on environment and field essentiality.
    """
    ...
```

## §4.X.1.2 F-CARDS-SCHEMA-INVALID

**Gate kind:** Loader-time PRE-load gate.

**Fires:** when a card does not validate against its declared `card_axis`'s schema (CIC, CLC, or matrix).

**Module:** `pipeline/logician/gates/f_cards_schema_invalid.py`.

**Predicate signature:**

```python
def f_cards_schema_invalid(
    *,
    card_path: str,
    card_body: Mapping[str, object],
    declared_axis: Literal["CIC", "CLC", "MATRIX"],
) -> GateOutcome:
    raise NotImplementedError("graduates LIVE at v0.2 first wave per arch v7.0.11 §5")
```

## §4.X.1.3 F-CARDS-UNSIGNED-PRODUCTION-LOAD

**Gate kind:** Loader-time production-environment PRE-load gate.

**Fires:** when production runtime attempts to load a card with `signature_status != signed`.

**Module:** `pipeline/logician/gates/f_cards_unsigned_production_load.py`.

**Predicate signature:**

```python
def f_cards_unsigned_production_load(
    *,
    card_path: str,
    signature_status: Literal["unsigned", "signed", "revoked"],
    environment: Literal["development", "production"],
) -> GateOutcome:
    raise NotImplementedError("graduates LIVE at v0.2 first wave per arch v7.0.11 §5")
```

## §4.X.1.4 F-CARDS-SIGNATURE-INVALID

**Gate kind:** Loader-time production-environment PRE-load gate.

**Fires:** when Ed25519 signature verification of card canonical-bytes against operator-pinned publisher pubkey fails.

**Module:** `pipeline/logician/gates/f_cards_signature_invalid.py`.

**Predicate signature:**

```python
def f_cards_signature_invalid(
    *,
    card_path: str,
    canonical_bytes: bytes,
    ed25519_signature_hex: str,
    publisher_pubkey: bytes,
) -> GateOutcome:
    raise NotImplementedError("graduates LIVE at v0.2 first wave per arch v7.0.11 §5")
```

## §4.X.1.5 F-CARDS-PRIVATE-DATA-IN-CARD

**Gate kind:** Loader-time PRE-load gate (all environments).

**Fires:** when a card body contains any field matching the private-org-data shape — org_slug, client_name, PROJECT_CONTEXT keys (EIN, UEI, address, banking, named individuals, named private clients, private cycle IDs), or any source text excerpt that belongs inside an organization namespace under `orgs/<slug>/vault/`.

**Module:** `pipeline/logician/gates/f_cards_private_data_in_card.py`.

**Predicate signature:**

```python
def f_cards_private_data_in_card(
    *,
    card_path: str,
    card_body: Mapping[str, object],
    private_data_field_pattern_registry: frozenset[str],
) -> GateOutcome:
    raise NotImplementedError("graduates LIVE at v0.2 first wave per arch v7.0.11 §5")
```

## §4.X.1.6 F-CARDS-CROSS-ORG-NAMESPACE-LEAK

**Gate kind:** Runtime memory-retrieval PRE-call gate.

**Fires:** when a retrieval request originating from `orgs:<org_slug>:*` context attempts to read from `orgs:<different_org_slug>:*`, or when a single retrieval call mixes `cards:*` and `orgs:<org_slug>:*` scopes opaquely without explicit namespace allow-list declaration.

**Module:** `pipeline/logician/gates/f_cards_cross_org_namespace_leak.py`.

**Predicate signature:**

```python
def f_cards_cross_org_namespace_leak(
    *,
    requesting_org_slug: str,
    requested_namespaces: frozenset[str],
    retrieval_mode: Literal["discover", "explicit_allowlist"],
) -> GateOutcome:
    raise NotImplementedError("graduates LIVE at v0.2 first wave per arch v7.0.11 §5")
```

## §4.X.1.7 F-CARDS-COUPLING-VIOLATION-EXTENSION

**Gate kind:** Loader-time PRE-load gate (all environments). **Extends v7.0.8's F-CIC-CLC-COUPLING-VIOLATION discipline** from code/schema/prompts/knowledge-pack-scoring-weights/config (v7.0.8 scope) to **card file format** (this gate's scope).

**Fires when:**

- A CIC card body includes CLC allowlists, deny-lists, ranking preferences, win-rate fields, frequency fields, or any field implying one CIC should or should not pursue one or more CLCs. **Explicitly includes** `common_clc_patterns_observed` and any equivalent renaming.
- A CLC card body includes CIC allowlists, deny-lists, ranking preferences, win-rate fields, or any field implying one CLC is restricted to one or more CICs.
- A matrix card body declares `binding_eligibility: true` or omits `status: "FORWARD_COMPAT_ONLY"` before the v1.x matrix-phase explicit amendment.

**Module:** `pipeline/logician/gates/f_cards_coupling_violation_extension.py`.

**Predicate signature:**

```python
def f_cards_coupling_violation_extension(
    *,
    card_path: str,
    card_body: Mapping[str, object],
    declared_axis: Literal["CIC", "CLC", "MATRIX"],
    forbidden_field_registry: Mapping[Literal["CIC", "CLC", "MATRIX"], frozenset[str]],
    v1_x_matrix_phase_active: bool,
) -> GateOutcome:
    raise NotImplementedError("graduates LIVE at v0.2 first wave per arch v7.0.11 §5")
```

**Forbidden field registry (canonical at v7.0.11 LOCK):**

```python
FORBIDDEN_FIELD_REGISTRY: Mapping[Literal["CIC", "CLC", "MATRIX"], frozenset[str]] = {
    "CIC": frozenset({
        "common_clc_patterns_observed",        # killed at v7.0.11 LOCK
        "eligible_clc_subset",
        "clc_allowlist",
        "clc_denylist",
        "preferred_clcs",
        "clc_win_rate",
        "clc_ranking_preferences",
    }),
    "CLC": frozenset({
        "eligible_cic_subset",
        "cic_allowlist",
        "cic_denylist",
        "preferred_cics",
        "cic_win_rate",
        "cic_ranking_preferences",
    }),
    "MATRIX": frozenset({
        # Matrix cards MAY declare cic_slug + clc_slug (that's their nature),
        # but MUST NOT declare binding_eligibility: true, and MUST declare
        # status: "FORWARD_COMPAT_ONLY" before v1.x matrix-phase amendment.
    }),
}
```

## §4.X.1.8 F-CIC-CLC-PATTERN-READ-DURING-ELIGIBILITY

**Gate kind:** Runtime read-path gate. **Extends v7.0.8's F-CIC-CLC-COUPLING-VIOLATION family.** Family prefix `F-CIC-CLC-*` (not `F-CARDS-*`) preserves orthogonality-discipline ancestry.

**Fires:** when Scout, Scribe, Judge, or eligibility-evaluation code attempts to read matrix card fields or any historical-pattern field during opportunity eligibility evaluation, fit gating, opportunity exclusion, or ranking suppression.

**Allowed reader during v1.x matrix phase:** Archivist, retrospectively, via the explicit `allowed_runtime_readers` registry in matrix card bodies.

**Possible future reader after explicit amendment:** Match DB advisory layer, only if (a) the result is labeled as a non-binding suggestion in audit log, AND (b) it cannot suppress or exclude opportunities.

**Module:** `pipeline/logician/gates/f_cic_clc_pattern_read_during_eligibility.py`.

**Predicate signature:**

```python
def f_cic_clc_pattern_read_during_eligibility(
    *,
    reader_identity: Literal["Scout", "Scribe", "Judge", "Logician_as_evaluator", "Archivist", "MatchDB"],
    read_context: Literal["eligibility_evaluation", "fit_gating", "opportunity_ranking", "opportunity_exclusion", "retrospective_lesson"],
    card_axis: Literal["CIC", "CLC", "MATRIX"],
    field_path: str,
) -> GateOutcome:
    raise NotImplementedError("graduates LIVE at v0.2 first wave (or earlier if v1.x matrix phase begins) per arch v7.0.11 §5")
```

**Note on v0.1 Beta fire surface.** At v0.1 Beta the primary fire surface is **schema-violation-introduction defense** — `common_clc_patterns_observed` is forbidden at v7.0.11 LOCK so the read-time gate guards against any future re-introduction. Matrix-read defense activates when v1.x matrix content begins shipping; until then the gate fail-closes on any matrix-read call simply because the namespace is empty.

# §4.X.2 — Cedar policy stubs (v7.0.11 LOCK shape)

Cedar policies authored at `pipeline/vault/policies/cards.cedar`. At v7.0.11 LOCK, the policy file ships with one LIVE rule (META-gate body) and seven BINDING-placeholder rules (graduating LIVE at v0.2 first wave). Mirrors §16 v1 Reflection Packet Cedar policy pattern (LOCKED 2026-05-15 row 222) byte-for-byte.

```cedar
// Rule 0 — LIVE at v7.0.11 LOCK — META-gate body realization
permit (
  principal == Card::Loader,
  action == Action::"LoadCard",
  resource is Card
) when {
  resource.coverage_complete == true ||
  context.environment == "development" ||
  (resource.missing_fields_nonessential == true)
};

// Rules 1-7 — BINDING-placeholder; bodies authored at v0.2 first wave LOCK round
// (signatures + module shells exist at v7.0.11 LOCK; full Cedar conditions land at graduation).
```

# §4.X.3 — AST-lint rules

One new AST-lint rule extension at `pipeline/linting/r_cards_no_coupling_field.py`:

**R-CARDS-NO-COUPLING-FIELD.** Scans all `pipeline/cards/CIC/**.yaml` and `pipeline/cards/CLC/**.yaml` files for any top-level field name matching the canonical `FORBIDDEN_FIELD_REGISTRY` (per §4.X.1.7 above). Fails AST-lint exit code 1 on match.

`MappingProxyType`-wrapped `FORBIDDEN_FIELD_REGISTRY` constants per the §4 v2.x.1 row-198 RT-14 fold-in (immutability against runtime monkey-patching).

# §4.X.4 — Test surface

Tests at `tests/logician/gates/test_f_cards_*.py` + `tests/cards/test_coupling_violation_extension.py` + `tests/linting/test_r_cards_no_coupling_field.py`. Target count at v7.0.11 LOCK: 40-50 skeleton tests (mostly `pytest.raises(NotImplementedError)` smoke tests + the META-gate LIVE-body test set + AST-lint matrix tests).

Tests graduate from `pytest.raises(NotImplementedError)` to real-behavior assertions at v0.2 first wave when predicate bodies land LIVE.

# §4.X.5 — Compound paired-commit at LOCK

When L-005 LOCKs the v7.0.11 amendment cluster, this section paired-commits at the same `lock_timestamp_utc` with:

- `pipeline/architecture/v0.1/architecture_v7_0_11_card_amendment.md`
- `pipeline/blueprint/v0.1/section_18_card_system.md`
- `pipeline/blueprint/v0.1/section_00_5_section_18_card_amendment.md`
- All eight gate-module stubs at `pipeline/logician/gates/f_cards_*.py` + `f_cic_clc_pattern_read_during_eligibility.py`
- Cedar policy at `pipeline/vault/policies/cards.cedar`
- AST-lint rule at `pipeline/linting/r_cards_no_coupling_field.py`
- Skeleton tests under `tests/logician/gates/` + `tests/cards/` + `tests/linting/`
- `lock_history.yaml` row appended

Per §6.17 Option-B compound-paired-commit pattern established by §17 WPFA + §16 Reflection Packet + §14 Report Generator + §13 Data Collector LOCKs.

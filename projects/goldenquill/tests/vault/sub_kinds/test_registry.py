"""Registry + layout extension tests for v7.2 operational sub-kinds. [§2.12, §5]"""

from __future__ import annotations

from pathlib import Path

import pytest

from pipeline.vault.layout import VaultLayout
from pipeline.vault.sub_kinds.registry import (
    OPERATIONAL_INTENTS,
    OPERATIONAL_SUBTREE_PREFIX,
    SUB_KIND_REGISTRY,
    SEVERITY_GREEN,
    SEVERITY_RED,
    SEVERITY_YELLOW,
    descriptor_for_intent,
    descriptor_for_sub_kind,
    operational_subtree_for,
)
from pipeline.vault.vault_write import POST_GATE_ALLOWLIST


EXPECTED_SUB_KINDS = frozenset(
    {
        "metrics",
        "financials",
        "photos",
        "narrative_entries",
        "timeline_of_activities",
        "beneficiary_records",
        "attachments",
        # §17 WPFA cycle_receipt sub-kind — LOCKED 2026-05-11 row 205.
        "cycle_receipt",
    }
)

EXPECTED_INTENTS = frozenset(
    {
        "operational-metrics-write",
        "operational-financials-write",
        "operational-photos-write",
        "operational-narrative-write",
        "operational-timeline-write",
        "operational-beneficiary-write",
        "operational-attachment-write",
        # §17 WPFA cycle_receipt intent.
        "operational-cycle-receipt-write",
    }
)


class TestRegistryShape:
    def test_seven_sub_kinds_registered(self) -> None:
        # Eight sub-kinds since §17 v1 LOCK 2026-05-11 (was 7 pre-WPFA).
        assert frozenset(SUB_KIND_REGISTRY) == EXPECTED_SUB_KINDS

    def test_intents_match_expected(self) -> None:
        assert OPERATIONAL_INTENTS == EXPECTED_INTENTS

    def test_severity_constants_match_admin_risk_taxonomy(self) -> None:
        # Must remain in sync with pipeline.sovereignty.admin_risk.SEVERITY_LIMITS.
        from pipeline.sovereignty.admin_risk import SEVERITY_LIMITS

        for label in (SEVERITY_GREEN, SEVERITY_YELLOW, SEVERITY_RED):
            assert label in SEVERITY_LIMITS, label

    def test_each_subtree_under_operational_prefix(self) -> None:
        for descriptor in SUB_KIND_REGISTRY.values():
            assert descriptor.vault_subtree.startswith(OPERATIONAL_SUBTREE_PREFIX)
            assert descriptor.vault_subtree.endswith("/")


class TestRegistryLookups:
    def test_descriptor_for_sub_kind(self) -> None:
        d = descriptor_for_sub_kind("metrics")
        assert d.intent == "operational-metrics-write"

    def test_descriptor_for_unknown_sub_kind_raises(self) -> None:
        with pytest.raises(KeyError):
            descriptor_for_sub_kind("not-a-real-sub-kind")

    def test_descriptor_for_intent(self) -> None:
        d = descriptor_for_intent("operational-photos-write")
        assert d is not None
        assert d.sub_kind == "photos"

    def test_descriptor_for_intent_unknown_returns_none(self) -> None:
        assert descriptor_for_intent("not-a-real-intent") is None

    def test_operational_subtree_for(self) -> None:
        assert operational_subtree_for("metrics") == "operational/metrics/"


class TestPostGateAllowlistAlignment:
    """Every registered intent must have a matching POST_GATE_ALLOWLIST row.

    Drift here would let a sub-kind register without enforcement.
    """

    def test_every_operational_intent_in_allowlist(self) -> None:
        missing = [i for i in OPERATIONAL_INTENTS if i not in POST_GATE_ALLOWLIST]
        assert not missing, f"missing allowlist rows for: {missing}"

    def test_allowlist_prefix_matches_registry_subtree(self) -> None:
        for intent in OPERATIONAL_INTENTS:
            entry = POST_GATE_ALLOWLIST[intent]
            descriptor = descriptor_for_intent(intent)
            assert descriptor is not None
            assert entry.vault_relative_prefix == descriptor.vault_subtree

    def test_every_operational_intent_simple_class_write_if_absent(self) -> None:
        for intent in OPERATIONAL_INTENTS:
            entry = POST_GATE_ALLOWLIST[intent]
            assert entry.kind_class == "SIMPLE", intent
            assert entry.permitted_modes == frozenset({"write-if-absent"}), intent


class TestLayoutExtensions:
    def test_operational_root_under_org_vault(self, tmp_path: Path) -> None:
        layout = VaultLayout.from_repo_root(tmp_path)
        root = layout.org_vault_operational_root("myco")
        assert root.parent.name == "vault"
        assert root.name == "operational"

    def test_each_sub_kind_path_helper_present(self, tmp_path: Path) -> None:
        layout = VaultLayout.from_repo_root(tmp_path)
        # Helper name pattern: org_vault_operational_<dir-leaf>
        cases = {
            "metrics": layout.org_vault_operational_metrics("myco"),
            "financials": layout.org_vault_operational_financials("myco"),
            "photos": layout.org_vault_operational_photos("myco"),
            "narratives": layout.org_vault_operational_narratives("myco"),
            "timeline": layout.org_vault_operational_timeline("myco"),
            "beneficiaries": layout.org_vault_operational_beneficiaries("myco"),
            "attachments": layout.org_vault_operational_attachments("myco"),
        }
        for leaf, p in cases.items():
            assert p.parent.name == "operational"
            assert p.name == leaf

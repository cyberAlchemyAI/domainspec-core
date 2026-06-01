"""§12 Uploader — portal adapter tests.

Spec card: ``pipeline/blueprint/v0.1/section_12_uploader.md`` (§12.10, §12.13.2).

Coverage targets:
- PortalAdapterProtocol conformance for all 7 adapters.
- Grants.gov filename convention (no spaces, max 50 chars).
- Grants.gov required format (PDF for narrative, XLSX for budget).
- SAM.gov portal_id correct + no narrative surface (required_format → None).
- CopyPaste / CommonGrantApp baseline format expectations.
- v0.1.x deferred adapters (Foundant / Submittable / Fluxx) still
  scaffold-only — assemble_package raises NotImplementedError per
  §12.10.5.
"""

from __future__ import annotations

import pytest

from pipeline.orchestrator.seats.uploader import PortalAdapterProtocol
from pipeline.orchestrator.seats.uploader_adapters.grants_gov import GrantsGovAdapter
from pipeline.orchestrator.seats.uploader_adapters.sam_gov import SamGovAdapter
from pipeline.orchestrator.seats.uploader_adapters.common_grant_app import CommonGrantAppAdapter
from pipeline.orchestrator.seats.uploader_adapters.foundant import FoundantAdapter
from pipeline.orchestrator.seats.uploader_adapters.submittable import SubmittableAdapter
from pipeline.orchestrator.seats.uploader_adapters.fluxx import FluxxAdapter
from pipeline.orchestrator.seats.uploader_adapters.copy_paste import CopyPasteAdapter


ALL_ADAPTERS = [
    GrantsGovAdapter,
    SamGovAdapter,
    CommonGrantAppAdapter,
    FoundantAdapter,
    SubmittableAdapter,
    FluxxAdapter,
    CopyPasteAdapter,
]

EXPECTED_IDS = [
    "grants_gov",
    "sam_gov",
    "common_grant_app",
    "foundant",
    "submittable",
    "fluxx",
    "copy_paste",
]

# v0.1 first-ship implementations — scope per §12 v1 LOCK adapter foursome.
V1_IMPLEMENTED_ADAPTERS = [
    GrantsGovAdapter,
    SamGovAdapter,
    CommonGrantAppAdapter,
    CopyPasteAdapter,
]
V1_DEFERRED_ADAPTERS = [
    FoundantAdapter,
    SubmittableAdapter,
    FluxxAdapter,
]


class TestProtocolConformance:
    """Every adapter must satisfy PortalAdapterProtocol at runtime."""

    @pytest.mark.parametrize("adapter_cls", ALL_ADAPTERS)
    def test_is_protocol_instance(self, adapter_cls: type) -> None:
        adapter = adapter_cls()
        assert isinstance(adapter, PortalAdapterProtocol)

    @pytest.mark.parametrize(
        "adapter_cls, expected_id",
        list(zip(ALL_ADAPTERS, EXPECTED_IDS)),
    )
    def test_portal_id(self, adapter_cls: type, expected_id: str) -> None:
        adapter = adapter_cls()
        assert adapter.portal_id == expected_id


class TestGrantsGovAdapter:
    def test_filename_no_spaces(self) -> None:
        adapter = GrantsGovAdapter()
        result = adapter.filename_convention(None, "Project Narrative Final.pdf")
        assert " " not in result

    def test_filename_max_50_chars(self) -> None:
        adapter = GrantsGovAdapter()
        long_name = "A" * 80 + ".pdf"
        result = adapter.filename_convention(None, long_name)
        assert len(result) <= 50

    def test_filename_underscores_only(self) -> None:
        adapter = GrantsGovAdapter()
        result = adapter.filename_convention(None, "Hello-World Foo.pdf")
        # Hyphens and spaces both collapse to underscores.
        assert "-" not in result
        assert " " not in result

    def test_required_format_narrative_pdf(self) -> None:
        adapter = GrantsGovAdapter()
        assert adapter.required_format("Project Narrative") == "pdf"

    def test_required_format_budget_xlsx(self) -> None:
        adapter = GrantsGovAdapter()
        assert adapter.required_format("Budget Detail SF-424A") == "xlsx"

    def test_file_size_limit(self) -> None:
        adapter = GrantsGovAdapter()
        limit = adapter.file_size_limit(None)
        assert limit is not None
        assert limit == 20 * 1024 * 1024


class TestSamGovAdapter:
    def test_portal_id(self) -> None:
        assert SamGovAdapter().portal_id == "sam_gov"

    def test_required_format_no_narrative(self) -> None:
        # No narrative surface — required_format returns None (any format
        # accepted) so the readiness checklist does not flag the validation
        # workbook as a format mismatch.
        assert SamGovAdapter().required_format(None) is None


class TestCopyPasteAdapter:
    def test_always_returns_pdf(self) -> None:
        adapter = CopyPasteAdapter()
        assert adapter.required_format(None) == "pdf"
        assert adapter.required_format("anything") == "pdf"

    def test_no_page_limit(self) -> None:
        adapter = CopyPasteAdapter()
        assert adapter.page_limit(None) is None

    def test_no_file_size_limit(self) -> None:
        adapter = CopyPasteAdapter()
        assert adapter.file_size_limit(None) is None


class TestCommonGrantAppAdapter:
    def test_portal_id(self) -> None:
        assert CommonGrantAppAdapter().portal_id == "common_grant_app"

    def test_required_format_narrative(self) -> None:
        assert CommonGrantAppAdapter().required_format("Project Narrative") == "pdf"

    def test_required_format_budget(self) -> None:
        assert CommonGrantAppAdapter().required_format("Budget Plan") == "xlsx"


class TestV1ImplementedAdaptersHaveAssembly:
    """v0.1 first-ship adapters MUST implement assemble_package — no
    NotImplementedError. Per §12 v1 LOCK adapter foursome.
    """

    @pytest.mark.parametrize("adapter_cls", V1_IMPLEMENTED_ADAPTERS)
    def test_assemble_package_callable(self, adapter_cls: type, tmp_path) -> None:
        adapter = adapter_cls()
        manifest = adapter.assemble_package((), (), None, str(tmp_path))
        # Empty input → empty (or stub) manifest, NOT a NotImplementedError.
        assert manifest is not None
        # Adapter id is set on the manifest.
        assert manifest.adapter_id == adapter.portal_id


class TestV1DeferredAdaptersScaffoldOnly:
    """v0.1.x deferred adapters (Foundant / Submittable / Fluxx) — scaffold
    only per §12.10.5. assemble_package raises NotImplementedError.
    """

    @pytest.mark.parametrize("adapter_cls", V1_DEFERRED_ADAPTERS)
    def test_assemble_package_raises(self, adapter_cls: type, tmp_path) -> None:
        adapter = adapter_cls()
        with pytest.raises(NotImplementedError):
            adapter.assemble_package((), (), None, str(tmp_path))

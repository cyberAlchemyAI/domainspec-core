"""Regression fixture: every BLUEPRINT_DEPS section citation must resolve
to a real heading in the cited blueprint file.

L-XXX rationale (pending number — append to lessons.md on synthesis):
the existing ``TestBlueprintDepsPin`` family asserts only that the hash
prefix matches, which catches *blueprint-file drift* but does NOT catch
*code-claim drift* — a module can pin the correct hash yet name a
section that does not exist (e.g. ``§4.13``) or mis-anchor a section
(e.g. ``§2.9 FDBrokerRequest`` when FDBrokerRequest lives at §2.7).
Batch 3 (2026-04-21) blocked 2/6 modules on exactly this self-inflicted
traceability failure. This fixture greps the blueprint TOC for every
cited section heading at import time, so the next self-inflicted mis-
anchor fails loudly at ``pytest`` collection instead of in committee.
"""

from __future__ import annotations

import importlib
import pkgutil
import re
from pathlib import Path
from typing import Final

import pytest

import pipeline.vault as _vault_pkg

_REPO_ROOT: Final[Path] = Path(__file__).resolve().parents[2]
_BLUEPRINT_DIR: Final[Path] = _REPO_ROOT / "pipeline" / "blueprint" / "v0.1"

# ``## 1. Foo`` → section_num = "1"
# ``### 2.7 FDBrokerRequest`` → section_num = "2.7"
# ``## §4.10.4 (NEW v6) — …`` → section_num = "4.10.4"
_HEADING_RE: Final[re.Pattern[str]] = re.compile(
    r"^#{1,6}\s+§?(\d+(?:\.\d+)*)(?=[\s.\-—:]|$)",
)

# Numbered-list step items under a top-level heading, e.g. under
# ``## 9. Vault boot sequence`` the line ``2. **Stable-UUID floor check.**``
# resolves the citation ``§9.2``. Supports ``2.`` and ``2a.`` forms.
_LIST_STEP_RE: Final[re.Pattern[str]] = re.compile(
    r"^(\d+)([a-z]?)\.\s+\*?\*?\S",
)

# ``§2.7 FDBrokerRequest mint …`` → section_num = "2.7"
_CITATION_RE: Final[re.Pattern[str]] = re.compile(
    r"^§?(\d+(?:\.\d+)*)(?=[\s.\-—:]|$)",
)


def _headings_in(blueprint_path: Path) -> frozenset[str]:
    """Return every anchor resolvable in ``blueprint_path``.

    Covers both markdown headings (``## 2.7`` / ``## §4.10.4``) and
    numbered step items under a top-level heading (``## 9.`` + list item
    ``2.`` yields ``9.2``).
    """
    anchors: set[str] = set()
    current_top: str | None = None
    for raw_line in blueprint_path.read_text(encoding="utf-8").splitlines():
        heading_match = _HEADING_RE.match(raw_line)
        if heading_match is not None:
            sec = heading_match.group(1)
            anchors.add(sec)
            current_top = sec.split(".")[0]
            continue
        if current_top is None:
            continue
        step_match = _LIST_STEP_RE.match(raw_line)
        if step_match is not None:
            step_num, suffix = step_match.group(1), step_match.group(2)
            anchors.add(f"{current_top}.{step_num}{suffix}")
            if suffix:
                anchors.add(f"{current_top}.{step_num}")
    return frozenset(anchors)


def _extract_citation_section(entry: str) -> str | None:
    match = _CITATION_RE.match(entry.strip())
    if match is None:
        return None
    return match.group(1)


def _iter_vault_modules() -> list[object]:
    modules: list[object] = []
    for mod_info in pkgutil.iter_modules(_vault_pkg.__path__):
        if mod_info.ispkg:
            continue
        name = f"{_vault_pkg.__name__}.{mod_info.name}"
        mod = importlib.import_module(name)
        if hasattr(mod, "BLUEPRINT_DEPS"):
            modules.append(mod)
    return modules


def _gather_cases() -> list[tuple[str, str, str, str]]:
    cases: list[tuple[str, str, str, str]] = []
    for mod in _iter_vault_modules():
        deps = getattr(mod, "BLUEPRINT_DEPS")
        for blueprint_file, section_info in deps.items():
            sections = section_info.get("sections_implemented", [])
            for entry in sections:
                sec = _extract_citation_section(entry)
                if sec is not None:
                    cases.append(
                        (
                            mod.__name__,
                            blueprint_file,
                            sec,
                            entry,
                        )
                    )
    return cases


@pytest.mark.parametrize(
    "module_name,blueprint_file,section_num,entry",
    _gather_cases(),
)
def test_blueprint_deps_section_citations_resolve(
    module_name: str,
    blueprint_file: str,
    section_num: str,
    entry: str,
) -> None:
    """Every cited ``§X.Y[.Z]`` anchor must be a real heading in the blueprint."""
    blueprint_path = _BLUEPRINT_DIR / blueprint_file
    assert blueprint_path.is_file(), (
        f"{module_name} cites blueprint {blueprint_file!r} which does not "
        f"exist at {blueprint_path}"
    )
    headings = _headings_in(blueprint_path)
    assert section_num in headings, (
        f"{module_name} BLUEPRINT_DEPS cites {entry!r} but §{section_num} "
        f"is not a heading in {blueprint_file}. "
        f"Known headings (sample): "
        f"{sorted(headings)[:20]}"
    )


class TestCitationParser:
    """Guards on the regex itself — if these drift, the fixture silently passes."""

    def test_parses_leading_section_symbol(self) -> None:
        assert _extract_citation_section("§2.7 FDBrokerRequest mint") == "2.7"

    def test_parses_without_section_symbol(self) -> None:
        assert _extract_citation_section("2.7 FDBrokerRequest mint") == "2.7"

    def test_parses_three_level_section(self) -> None:
        assert _extract_citation_section("§4.10.4 post-gate allowlist") == "4.10.4"

    def test_rejects_non_section_prefix(self) -> None:
        assert _extract_citation_section("BT14.a per-org init marker") is None

    def test_extracts_bare_section_single_level(self) -> None:
        assert _extract_citation_section("§8 concrete numbers") == "8"


class TestHeadingParser:
    def test_section_02_blueprint_has_expected_anchors(self) -> None:
        headings = _headings_in(_BLUEPRINT_DIR / "section_02_vault_topology.md")
        assert "2.7" in headings
        assert "2.9" in headings
        assert "3.3" in headings
        assert "4.10.4" in headings
        assert "4.10.6" in headings

    def test_section_02_blueprint_lacks_nonexistent_anchor(self) -> None:
        headings = _headings_in(_BLUEPRINT_DIR / "section_02_vault_topology.md")
        assert "4.13" not in headings, (
            "§4.13 must not exist in section_02 — Batch 3 2026-04-21 "
            "remediation pinned this; restoring §4.13 would silently "
            "re-introduce the research_db_query_skill anchor bug."
        )

import ast
from dataclasses import dataclass
from pathlib import Path

from pipeline.nervous_system.scout_enrichment.aln_enrichment import (
    EnrichedOpportunityRecord,
    build_assistance_listing_index,
    extract_opportunity_aln,
    join_opportunities_to_assistance_listings,
    normalize_aln,
)

@dataclass
class MockOpp:
    id: str
    cfda_number: str = None
    assistance_listing_number: str = None

@dataclass
class MockListing:
    id: str
    assistance_listing_number: str


def test_normalize_aln_accepts_standard_format():
    assert normalize_aln("10.001") == "10.001"


def test_normalize_aln_strips_spacing():
    assert normalize_aln(" 10 . 001 ") == "10.001"


def test_normalize_aln_accepts_unpunctuated_five_digit():
    assert normalize_aln("10001") == "10.001"


def test_normalize_aln_handles_short_suffix_deterministically():
    assert normalize_aln("10.1") == "10.001"
    assert normalize_aln("10.10") == "10.010"


def test_normalize_aln_rejects_blank_and_junk():
    assert normalize_aln("") is None
    assert normalize_aln("N/A") is None
    assert normalize_aln("TBD") is None
    assert normalize_aln("abc") is None
    assert normalize_aln(None) is None


def test_normalize_aln_rejects_multiple_decimals():
    assert normalize_aln("10.00.1") is None


def test_build_assistance_listing_index_keys_by_normalized_aln_only():
    l1 = MockListing(id="1", assistance_listing_number="10.001")
    l2 = MockListing(id="2", assistance_listing_number=" 10 . 001 ")

    idx = build_assistance_listing_index([l1, l2])
    assert "10.001" in idx
    assert len(idx["10.001"]) == 2
    assert idx["10.001"][0] is l1
    assert idx["10.001"][1] is l2


def test_left_join_preserves_all_grants_gov_opportunities():
    opps = [MockOpp(id="1"), MockOpp(id="2"), MockOpp(id="3")]
    res = join_opportunities_to_assistance_listings(opps, [])
    assert len(res) == 3
    assert res[0].opportunity is opps[0]
    assert res[1].opportunity is opps[1]
    assert res[2].opportunity is opps[2]


def test_enrichment_matched_attaches_sam_gov_listing():
    opp = MockOpp(id="1", cfda_number="10.001")
    listing = MockListing(id="L1", assistance_listing_number="10.001")

    res = join_opportunities_to_assistance_listings([opp], [listing])
    assert len(res) == 1
    assert res[0].enrichment_status == "matched"
    assert res[0].assistance_listing is listing
    assert res[0].assistance_listing_number_normalized == "10.001"


def test_enrichment_missing_aln_preserves_opportunity_with_null_listing():
    opp = MockOpp(id="1") # No ALN
    res = join_opportunities_to_assistance_listings([opp], [])
    assert len(res) == 1
    assert res[0].enrichment_status == "missing_aln"
    assert res[0].assistance_listing is None


def test_enrichment_malformed_aln_preserves_opportunity_with_null_listing():
    opp = MockOpp(id="1", cfda_number="TBD")
    res = join_opportunities_to_assistance_listings([opp], [])
    assert len(res) == 1
    assert res[0].enrichment_status == "malformed_aln"
    assert res[0].assistance_listing is None


def test_enrichment_unmatched_aln_preserves_opportunity_with_null_listing():
    opp = MockOpp(id="1", cfda_number="10.001")
    res = join_opportunities_to_assistance_listings([opp], [])
    assert len(res) == 1
    assert res[0].enrichment_status == "unmatched"
    assert res[0].assistance_listing is None


def test_enrichment_ambiguous_aln_does_not_guess():
    opp = MockOpp(id="1", cfda_number="10.001")
    l1 = MockListing(id="L1", assistance_listing_number="10.001")
    l2 = MockListing(id="L2", assistance_listing_number="10.001")

    res = join_opportunities_to_assistance_listings([opp], [l1, l2])
    assert len(res) == 1
    assert res[0].enrichment_status == "ambiguous"
    assert res[0].assistance_listing is None


def test_enrichment_does_not_mutate_original_records():
    opp = MockOpp(id="1", cfda_number="10.001")
    listing = MockListing(id="L1", assistance_listing_number="10.001")

    res = join_opportunities_to_assistance_listings([opp], [listing])
    assert res[0].opportunity.id == "1"
    assert res[0].opportunity.cfda_number == "10.001"
    assert not hasattr(res[0].opportunity, "enrichment_status")


def _get_module_source():
    p = Path(__file__).parent.parent.parent / "pipeline" / "nervous_system" / "scout_enrichment" / "aln_enrichment.py"
    with open(p, "r", encoding="utf-8") as f:
        return f.read(), str(p)


def test_no_llm_or_model_imports():
    src, path = _get_module_source()
    tree = ast.parse(src, filename=path)
    banned = {"openai", "anthropic", "google.generativeai", "llm", "vllm", "ollama"}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert alias.name.split('.')[0] not in banned
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                assert node.module.split('.')[0] not in banned


def test_no_network_imports():
    src, path = _get_module_source()
    tree = ast.parse(src, filename=path)
    banned = {"requests", "httpx", "aiohttp", "urllib", "socket", "playwright", "selenium"}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert alias.name.split('.')[0] not in banned
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                assert node.module.split('.')[0] not in banned


def test_no_dynamic_import_or_eval_escape_hatches():
    src, _ = _get_module_source()
    banned = ["importlib", "__import__", "eval(", "exec("]
    for b in banned:
        assert b not in src


def test_no_authority_expansion_language():
    src, _ = _get_module_source()
    src_lower = src.lower()
    banned = [
        "crawl", "scrape", "discover urls", "discover_url", "autonomous",
        "submit", "portal upload", "partner_alert", "outreach",
        "candidate_generation", "drafting", "all_model_access", "frontier_eligible"
    ]
    for b in banned:
        assert b not in src_lower


def test_no_funder_terrain_import_or_path_reference():
    src, _ = _get_module_source()
    assert "funder_terrain" not in src


def test_no_ui_export_application_guide_references():
    src, _ = _get_module_source()
    banned = ["apps/", "export", "final_packet", "application_guide"]
    for b in banned:
        assert b not in src

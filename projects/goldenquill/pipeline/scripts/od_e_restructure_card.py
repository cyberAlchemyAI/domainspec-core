#!/usr/bin/env python3
"""
OD-E §18.6 v2 dual-track restructure helper.

Reads a multi-track CLC card YAML, partitions entries into track_a / track_b
per per-card partition spec, and writes restructured YAML preserving header
comments + lifecycle/metadata at root.

Heuristic: each list-of-dict-or-string entry is tagged track_a / track_b /
shared by matching against per-card marker phrases in note/description/
criterion/rubric_example/section_name/form_id/flag fields. Shared entries
appear in BOTH tracks (each track is required to be self-contained per the
§18.6 v2 schema oneOf branch 2).

This script is intentionally explicit + conservative: partition errors will
be caught at the L-005 Thesis dispatch + LOCK ceremony operator review.
Entries the script cannot confidently partition default to shared (= present
in both tracks) so Scribe behavior is never silently track-stripped.
"""

import sys
import re
import yaml
from pathlib import Path
from collections import OrderedDict


# Track-marker regex per card slug. Order matters: track_a checked first
# (e.g., "Track A" / "TRACK A" / "track_a"); track_b next; otherwise shared.
TRACK_MARKERS = {
    "sponsorship_corporate": {
        "track_a": [
            r"\bTrack A\b", r"\bTRACK A\b", r"\btrack_a\b",
            r"\bsponsorship[- _]track\b", r"\bbenefits[- _]exchange\b",
            r"\bsponsorship[- _]deck\b", r"\bcause[- _]marketing\b",
            r"\bcommercial co-?venturer\b", r"\bcorporate sponsorship\b",
            r"\bUBIT\b", r"\bbenefits package\b", r"\btier\b",
            r"\bactivation\b", r"\bcsr\b", r"\bbrand alignment\b",
            r"\bemployee giving\b", r"\bcybergrants\b", r"\bbenevity\b",
            r"\byourcause\b", r"\bbonterra\b", r"\baudience demographics\b",
            r"\bsponsor benefits\b", r"\bimpressions\b", r"\bsponsorship payment\b",
        ],
        "track_b": [
            r"\bTrack B\b", r"\bTRACK B\b", r"\btrack_b\b",
            r"\bcorporate[- _]foundation\b", r"\bcorp[- _]foundation\b",
            r"\bcorporate foundation grant\b", r"\bfoundation-style\b",
            r"\bfoundation grant\b", r"\b990-?PF\b", r"\bcorporate gift acknowledgment\b",
            r"\bcorporate foundation program\b",
        ],
    },
    "credit_underwriting": {
        "track_a": [
            r"\bdebt\b", r"\bloan\b", r"\bCDFI\b", r"\bSBA\b",
            r"\b7\(a\)\b", r"\b504\b", r"\bmicroloan\b", r"\bUSDA B&I\b",
            r"\bIntermediary Relending\b", r"\brevolving loan\b",
            r"\bDSCR\b", r"\bdebt service\b", r"\bcollateral\b",
            r"\brepayment\b", r"\bcredit history\b", r"\bunderwriter\b",
            r"\bowner equity\b", r"\bborrower\b", r"\bcovenant\b",
            r"\bguarantor\b", r"\bguarantee\b", r"\bcredit analyst\b",
            r"\bloan committee\b", r"\bworking capital\b", r"\bterm loan\b",
            r"\bcash flow\b", r"\bpro forma\b", r"\bbalance sheet\b",
        ],
        "track_b": [
            r"\bgrant track\b", r"\bcapitalization grant\b", r"\bloan loss reserve grant\b",
            r"\bgrant-loan combo\b", r"\bRD grant\b", r"\bgrant[- _]style\b",
            r"\bgrant agreement\b", r"\bmission-fit\b", r"\bcapacity grant\b",
            r"\bCDFI Fund\b", r"\bRural Development grant\b",
        ],
    },
    "market_access": {
        "track_a": [
            r"\bSBIR Phase II\b", r"\bSBIR Phase 2\b", r"\bPhase II\b",
            r"\bSBIR R&D\b", r"\bPhase[- _]II[- _]further\b",
            r"\bsbir_phase_ii\b", r"\bsbir phase ii\b",
            r"\bSTTR\b", r"\bSBIR/STTR\b", r"\bSBIR\b",
            r"\btechnical feasibility\b", r"\bpeer review\b",
            r"\bbroader impacts\b", r"\bintellectual merit\b",
            r"\bcommercialization-readiness\b", r"\bSBIR program manager\b",
        ],
        "track_b": [
            r"\bSBIR Phase III\b", r"\bSBIR Phase 3\b", r"\bPhase III\b",
            r"\bsbir_phase_iii\b", r"\bsbir phase iii\b",
            r"\bcommercialization\b", r"\bgo-to-market\b",
            r"\bbuyer commit\b", r"\bchannel strategy\b", r"\brevenue model\b",
            r"\bcompetitive position\b", r"\bdelivery capacity\b",
            r"\bunit economics\b", r"\bprocurement vehicle\b",
            r"\bsole-source contract\b", r"\bprivate capital\b",
            r"\bdistribut\b", r"\bsales channel\b", r"\bbuyer\b",
            r"\bpurchase order\b", r"\bmarket study\b", r"\bcustomer pipeline\b",
            r"\bmarket development\b", r"\bVAPG\b", r"\bvalue-?added producer\b",
        ],
    },
}

# Per-card track metadata
TRACK_META = {
    "sponsorship_corporate": {
        "track_a": {
            "track_name": "benefits_exchange",
            "track_description": (
                "Corporate sponsorship + cause marketing + employee giving — "
                "transactional benefits-exchange instrument. Underwriting is "
                "decision-maker-driven (CMO / CSR Director / Community Relations / "
                "Brand Manager) on audience fit + brand alignment + visibility "
                "value + activation execution + measurable reach + reputational "
                "safety + relationship pathway + renewal potential. Sponsorship "
                "deck is the primary application artifact; corporate sponsorship "
                "rarely uses standardized forms. Scribe MUST default to "
                "sponsorship-deck shape (audience + benefits + activation + "
                "measurement) NOT grant-proposal shape (mission + capacity + "
                "outcomes + budget) for Track A opportunities. UBIT / IRS Reg. "
                "§1.513-4 qualified-sponsorship safe harbor + state commercial "
                "co-venturer registration apply on this track."
            ),
        },
        "track_b": {
            "track_name": "corp_foundation_grant",
            "track_description": (
                "Corporate-foundation grants — behave like private foundation "
                "grants with CSR overlay. Underwriting is foundation-style "
                "structured-rubric scoring (mission-fit + capacity + outcomes + "
                "budget reasonableness) with parent-company brand-alignment "
                "screen layered on top. Reviewer profile: corporate foundation "
                "program staff + corporate parent brand review. Portals: "
                "Cybergrants / Benevity / YourCause / Bonterra (corp-administered) "
                "+ Foundant / Submittable / Fluxx (foundation-standard). Scribe "
                "MUST default to foundation-grant proposal shape (organizational "
                "background + statement of need + project description + outcomes "
                "+ sustainability + budget justification) NOT sponsorship-deck "
                "shape for Track B opportunities. IRS Pub. 1771 corporate-gift "
                "acknowledgment applies; UBIT does not (Track B is charitable "
                "transfer, not benefits exchange)."
            ),
        },
    },
    "credit_underwriting": {
        "track_a": {
            "track_name": "debt",
            "track_description": (
                "Debt instruments — CDFI loans + SBA 7(a)/504/Microloan + USDA "
                "Business & Industry / Community Facilities / Intermediary "
                "Relending + state revolving loan funds + mission-aligned "
                "community lenders. Underwriting is repayment-capacity driven: "
                "cash flow, debt service coverage (DSCR ≥1.20-1.25x typical), "
                "collateral, credit history, owner equity, management capacity, "
                "financial controls, use of funds, risk mitigation, guarantor "
                "strength, covenant compliance. Reviewer profile: lenders / "
                "credit analysts / loan committees / CDFI underwriters / SBA "
                "lenders. Scribe MUST NOT draft grant-language proposals on "
                "Track A opportunities — that is the structural failure mode "
                "Option A prevents. Pro forma, balance sheet, income statement, "
                "debt schedule, collateral documentation, owner-equity injection "
                "evidence are load-bearing."
            ),
        },
        "track_b": {
            "track_name": "grant",
            "track_description": (
                "Grant-style capital that behaves like credit-readiness funding "
                "— capitalization grants + loan loss reserve grants + USDA Rural "
                "Development grant-loan combos + CDFI-Fund-administered capacity "
                "grants + financial-systems-readiness grants. Underwriting is "
                "grant-style: mission-fit + capacity + outcomes + budget "
                "reasonableness + financial-systems-readiness (a subset of "
                "debt-track financial_controls criterion). Reviewer profile: "
                "foundation program officers / CDFI Fund staff / USDA RD "
                "program officers. Scribe MUST default to foundation-grant "
                "proposal shape for Track B opportunities; do not import "
                "debt-track DSCR / collateral / repayment framing — those are "
                "structurally incorrect on Track B."
            ),
        },
    },
    "market_access": {
        "track_a": {
            "track_name": "sbir_phase_ii",
            "track_description": (
                "SBIR Phase II — further SBIR R&D funds with NIH / NSF / DOD / "
                "DOE / USDA program variations. Underwriting extends from "
                "Phase I demonstration: technical feasibility extended to "
                "commercialization-readiness; team capability; intellectual "
                "merit + broader impacts (NIH/NSF variations) or program-of-"
                "record alignment (DOD/DOE). Reviewer profile: SBIR program "
                "managers + peer reviewers (technical SMEs). Phase II "
                "proposals are R&D-driven and read like research proposals "
                "with explicit commercialization-readiness sections; Scribe "
                "MUST treat Track A as research-and-development drafting, NOT "
                "go-to-market drafting. Phase II awards typically $750k-$1.5M "
                "over 24 months."
            ),
        },
        "track_b": {
            "track_name": "sbir_phase_iii",
            "track_description": (
                "SBIR Phase III — commercialization without further SBIR funds. "
                "Funding source is private capital + procurement vehicles "
                "(sole-source contracts available to SBIR Phase II awardees "
                "under the SBIR Phase III authority — no further SBIR "
                "competition). Underwriting is commercial: buyer commitments, "
                "channel strategy, revenue model, competitive position, "
                "delivery capacity, unit economics. Reviewer profile: "
                "commercial procurement officers / private investors / "
                "strategic partners. Scribe MUST treat Track B as go-to-market "
                "drafting (buyer + channel + revenue) NOT R&D drafting. The "
                "broader §18.6 v1 market_access content (VAPG / SBA / market "
                "development / Build to Scale / institutional procurement) is "
                "Track-B-shape — it inherits to this track. Phase III is "
                "non-competitive sole-source under SBA / agency-specific rules."
            ),
        },
    },
}


def detect_track(text):
    """Return 'a', 'b', 'shared', or None for a text blob."""
    if not text:
        return "shared"
    t = str(text)
    return None  # placeholder; bound at runtime per-card


def make_detector(card_slug):
    markers = TRACK_MARKERS[card_slug]
    a_pats = [re.compile(p, re.IGNORECASE) for p in markers["track_a"]]
    b_pats = [re.compile(p, re.IGNORECASE) for p in markers["track_b"]]

    def detect(text):
        if not text:
            return "shared"
        t = str(text)
        a_hit = any(p.search(t) for p in a_pats)
        b_hit = any(p.search(t) for p in b_pats)
        if a_hit and not b_hit:
            return "a"
        if b_hit and not a_hit:
            return "b"
        if a_hit and b_hit:
            return "shared"
        return "shared"

    return detect


def entry_text(entry):
    """Concatenate semantic text from a dict entry for partition detection."""
    if isinstance(entry, str):
        return entry
    if not isinstance(entry, dict):
        return ""
    parts = []
    for key in (
        "criterion", "description", "rubric_example", "note",
        "section_name", "form_id", "flag", "red_team_probe",
        "framework", "applicability", "commitment_type",
        "measurement_method", "portal", "typical_use",
    ):
        v = entry.get(key)
        if v:
            parts.append(str(v))
    # Also scan all string values for marker hits
    for v in entry.values():
        if isinstance(v, str):
            parts.append(v)
        elif isinstance(v, list):
            for item in v:
                if isinstance(item, str):
                    parts.append(item)
                elif isinstance(item, dict):
                    for vv in item.values():
                        if isinstance(vv, str):
                            parts.append(vv)
    return " | ".join(parts)


def partition_list(items, detect):
    a_items, b_items = [], []
    for item in items:
        track = detect(entry_text(item))
        if track == "a":
            a_items.append(item)
        elif track == "b":
            b_items.append(item)
        else:  # shared -> both tracks
            a_items.append(item)
            b_items.append(item)
    return a_items, b_items


def partition_dict(d, detect):
    """For evidence_weights-style dict[name -> {weight, rationale, ...}]."""
    a_d, b_d = {}, {}
    for k, v in d.items():
        # Use the value's rationale + the key itself for detection
        text = k + " | " + entry_text(v if isinstance(v, dict) else {"_": v})
        track = detect(text)
        if track == "a":
            a_d[k] = v
        elif track == "b":
            b_d[k] = v
        else:
            a_d[k] = v
            b_d[k] = v
    return a_d, b_d


def partition_reviewer_profile(rp, detect):
    """reviewer_profile_typical: dict with reviewer_types (list), reviewer_priorities (list), common_red_flags_from_reviewer_pov (list), source_citation (str)."""
    a_rp = {}
    b_rp = {}
    for k, v in rp.items():
        if isinstance(v, list):
            a_list, b_list = [], []
            for item in v:
                track = detect(item if isinstance(item, str) else entry_text(item))
                if track == "a":
                    a_list.append(item)
                elif track == "b":
                    b_list.append(item)
                else:
                    a_list.append(item)
                    b_list.append(item)
            a_rp[k] = a_list
            b_rp[k] = b_list
        else:
            a_rp[k] = v
            b_rp[k] = v
    return a_rp, b_rp


def partition_reporting_requirements(rr, detect):
    a_rr, b_rr = {}, {}
    for k, v in rr.items():
        if isinstance(v, dict):
            # e.g., performance_reporting: {frequency: str, content_required: list[str]}
            a_inner, b_inner = {}, {}
            for ik, iv in v.items():
                if isinstance(iv, list):
                    a_list, b_list = [], []
                    for item in iv:
                        track = detect(item if isinstance(item, str) else entry_text(item))
                        if track == "a":
                            a_list.append(item)
                        elif track == "b":
                            b_list.append(item)
                        else:
                            a_list.append(item)
                            b_list.append(item)
                    a_inner[ik] = a_list
                    b_inner[ik] = b_list
                else:
                    a_inner[ik] = iv
                    b_inner[ik] = iv
            a_rr[k] = a_inner
            b_rr[k] = b_inner
        else:
            a_rr[k] = v
            b_rr[k] = v
    return a_rr, b_rr


def partition_budget_structure(bs, detect):
    """budget_structure_conventions: dict with track-prefixed sub-keys typically."""
    # Per-card: many sponsorship_corporate sub-keys are already prefixed
    # track_a_* / track_b_*. Honor explicit prefixes; for generic keys, share.
    a_bs, b_bs = {}, {}
    for k, v in bs.items():
        kl = k.lower()
        if kl.startswith("track_a_") or "track_a" in kl:
            a_bs[k] = v
        elif kl.startswith("track_b_") or "track_b" in kl:
            b_bs[k] = v
        else:
            # Use detect on the value
            track = detect(k + " | " + entry_text(v if isinstance(v, dict) else {"_": str(v)}))
            if track == "a":
                a_bs[k] = v
            elif track == "b":
                b_bs[k] = v
            else:
                a_bs[k] = v
                b_bs[k] = v
    return a_bs, b_bs


def partition_commitment_tracking(ct, detect):
    a_ct, b_ct = {}, {}
    for k, v in ct.items():
        if k == "typical_commitments_extracted" and isinstance(v, list):
            a_list, b_list = partition_list(v, detect)
            a_ct[k] = a_list
            b_ct[k] = b_list
        elif k == "proposal_commitments_yaml_extension":
            # Share at both tracks but rename to be track-aware
            a_ct[k] = v
            b_ct[k] = v
        else:
            a_ct[k] = v
            b_ct[k] = v
    return a_ct, b_ct


TRACK_SPECIFIC_FIELDS = [
    "underwriting_criteria",
    "scoring_weight_patterns",
    "evidence_weights",
    "common_application_forms",
    "narrative_section_patterns",
    "budget_structure_conventions",
    "reviewer_profile_typical",
    "common_portals",
    "common_red_flags",
    "reporting_requirements_typical",
    "compliance_obligations",
    "commitment_tracking_pattern",
    "common_funders_observed",
    "provenance_requirements",
]

ROOT_FIELDS = [
    "schema_version",
    "card_axis",
    "card_id",
    "slug",
    "display_name",
    "funding_mechanism_summary",
    "tilth_clc_id",
    "lifecycle",
    "_research_metadata",
]


def restructure(card_path: Path, slug: str):
    raw = card_path.read_text()
    # Preserve header comment block: everything before the first top-level YAML key
    lines = raw.split("\n")
    header_lines = []
    body_start = 0
    for i, line in enumerate(lines):
        if re.match(r"^[a-zA-Z_]", line):
            body_start = i
            break
        header_lines.append(line)
    header = "\n".join(header_lines).rstrip() + "\n"

    doc = yaml.safe_load(raw)
    detect = make_detector(slug)

    out = OrderedDict()
    # Shared metadata at root
    for k in ROOT_FIELDS:
        if k in doc:
            out[k] = doc[k]

    # Build track_a + track_b
    meta_a = TRACK_META[slug]["track_a"]
    meta_b = TRACK_META[slug]["track_b"]

    track_a = OrderedDict([
        ("track_name", meta_a["track_name"]),
        ("track_description", meta_a["track_description"]),
    ])
    track_b = OrderedDict([
        ("track_name", meta_b["track_name"]),
        ("track_description", meta_b["track_description"]),
    ])

    for field in TRACK_SPECIFIC_FIELDS:
        if field not in doc:
            continue
        val = doc[field]
        if field in (
            "underwriting_criteria",
            "scoring_weight_patterns",
            "common_application_forms",
            "narrative_section_patterns",
            "common_portals",
            "common_red_flags",
            "compliance_obligations",
            "common_funders_observed",
        ):
            a, b = partition_list(val, detect)
            track_a[field] = a
            track_b[field] = b
        elif field == "evidence_weights":
            a, b = partition_dict(val, detect)
            track_a[field] = a
            track_b[field] = b
        elif field == "budget_structure_conventions":
            a, b = partition_budget_structure(val, detect)
            track_a[field] = a
            track_b[field] = b
        elif field == "reviewer_profile_typical":
            a, b = partition_reviewer_profile(val, detect)
            track_a[field] = a
            track_b[field] = b
        elif field == "reporting_requirements_typical":
            a, b = partition_reporting_requirements(val, detect)
            track_a[field] = a
            track_b[field] = b
        elif field == "commitment_tracking_pattern":
            a, b = partition_commitment_tracking(val, detect)
            track_a[field] = a
            track_b[field] = b
        elif field == "provenance_requirements":
            # Provenance kept shared (apply to both tracks)
            track_a[field] = val
            track_b[field] = val

    out["track_a"] = track_a
    out["track_b"] = track_b

    # Preserve _review_handback + _schema_status + _oq6_anchor at root if present
    for extra in ("_oq6_anchor", "_schema_status", "_review_handback"):
        if extra in doc:
            out[extra] = doc[extra]

    # Render YAML
    # Use PyYAML with allow_unicode + sort_keys=False to preserve insertion order
    class OrderedDumper(yaml.SafeDumper):
        pass

    def _dict_representer(dumper, data):
        return dumper.represent_mapping(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, data.items())

    OrderedDumper.add_representer(OrderedDict, _dict_representer)

    yaml_body = yaml.dump(
        out,
        Dumper=OrderedDumper,
        allow_unicode=True,
        sort_keys=False,
        width=120,
        default_flow_style=False,
    )

    # Inject the §18.6 v2 restructure marker into the header
    marker = (
        "\n# ===========================================================================\n"
        "# §18.6 v2 DUAL-TRACK STRUCTURAL SEPARATION (OD-E, DRAFT 2026-05-16)\n"
        "# ===========================================================================\n"
        "# This card was restructured under Option A (top-level track_a:/track_b:\n"
        "# containers) per OD-E surfaced at WAVE_2_CLOSE_SYNTHESIS.md §CC-5.\n"
        f"# Shared metadata stays at root; track-specific content lives in track_a\n"
        f"# ({meta_a['track_name']}) and track_b ({meta_b['track_name']}).\n"
        "#\n"
        "# Partition heuristic: per-entry Track A / Track B / shared classification\n"
        "# via pipeline/scripts/od_e_restructure_card.py marker regex. Entries with\n"
        "# explicit 'Track A:' / 'Track B:' / 'TRACK A' / 'TRACK B' markers in their\n"
        "# notes / descriptions partition cleanly; entries without markers default\n"
        "# to BOTH tracks (shared baseline) so neither track is silently stripped.\n"
        "#\n"
        "# Operator review at LOCK ceremony will verify partition correctness;\n"
        "# L-005 strict two-cycle Thesis dispatch (Editor / Judge / Red Team)\n"
        "# reserved for ceremony per pre-staging discipline.\n"
        "# ===========================================================================\n"
    )

    final = header.rstrip("\n") + marker + "\n" + yaml_body
    card_path.write_text(final)
    print(f"[restructured] {card_path} -> shared_root + track_a({meta_a['track_name']}) + track_b({meta_b['track_name']})")
    print(f"  track_a fields: {list(track_a.keys())}")
    print(f"  track_b fields: {list(track_b.keys())}")


if __name__ == "__main__":
    repo_root = Path(__file__).resolve().parent
    if len(sys.argv) > 1:
        repo_root = Path(sys.argv[1]).resolve()
    for slug in ("sponsorship_corporate", "credit_underwriting", "market_access"):
        p = repo_root / "pipeline" / "cards" / "CLC" / f"{slug}.yaml"
        if not p.exists():
            print(f"[skip] {p} not found")
            continue
        restructure(p, slug)

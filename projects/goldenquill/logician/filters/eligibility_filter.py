"""
eligibility_filter.py — Zero-token pre-filter for grant opportunities

Deterministic keyword/phrase filtering before any LLM evaluation.
Fail-fast: if a disqualifier appears, the opportunity is dropped immediately.
No API calls. No tokens. Pure string matching.

Applicant profile: MycoSymbiotics Cooperative
- For-profit small business (PA Cooperative Corporation)
- Located: Pittsburgh / Camp Hill, PA (Allegheny + Cumberland Counties)
- Sectors: food/ag, land remediation, arts, technology (Golden Quill)
- Entity types: cooperative, small business, for-profit
- NOT: state/local government, tribal, IHE (university), large business, nonprofit 501c3
- SAM registered: yes
- UEI: [pending]
"""

import re
from typing import Optional

# ─────────────────────────────────────────────
# HARD DISQUALIFIERS
# If ANY of these appear in title or synopsis → DROP
# ─────────────────────────────────────────────
HARD_DISQUALIFIERS = [
    # Entity type exclusions
    "state governments only",
    "state and local governments",
    "local governments only",
    "tribal governments only",
    "tribal nations only",
    "federally recognized tribe",
    "institutions of higher education only",
    "universities only",
    "nonprofits only",
    "non-profits only",
    "501(c)(3) only",
    "501c3 only",
    "public bodies only",
    "government entities only",
    "housing authorities",
    "school districts only",
    "faith-based organizations only",

    # Geographic exclusions (non-PA/non-applicable)
    "alaska native",
    "hawaii only",
    "puerto rico only",
    "u.s. territories only",
    "district of columbia only",

    # Sector hard misses for Golden Quill
    "veterinary",
    "livestock disease",
    "aquaculture only",
    "fisheries only",
    "forestry only",
    "wildfire only",
    "geothermal",
    "nuclear",
    "missile",
    "defense contractor",
    "weapons",
    "military installations",
    "law enforcement only",
    "corrections only",
    "substance abuse treatment",
    "mental health services only",
    "housing construction",
    "homeless shelter",
    "early childhood only",
    "k-12 only",
    "elementary school",
    "child care only",
    "international development only",
    "foreign assistance",
    "embassy",
    "overseas",
    "beluga whale",
    "landslide",
    "heliophysics",
    "astronomy",
    "oceanography",
    "nuclear regulatory",
    "radiation",
    "drug-free communities",

    # Program type misses
    "formula grant",  # formula grants go to states, not businesses
    "continuation only",
    "competing continuation",
    "reentry program",
    "prisoner reentry",
    "offender",
    "incarcerated",
]

# ─────────────────────────────────────────────
# SOFT DISQUALIFIERS
# These LOWER confidence but don't auto-drop.
# Flag for human review.
# ─────────────────────────────────────────────
SOFT_DISQUALIFIERS = [
    "nonprofit preferred",
    "501(c) preferred",
    "university partner required",
    "requires state match",
    "disaster supplemental",  # usually geography-locked
    "region 08",  # EPA Region 8 is Mountain West, not PA (PA = Region 3)
    "region 09",
    "region 10",
    "region 1",   # New England
    "appalachian",  # worth checking but PA eligibility varies by county
]

# ─────────────────────────────────────────────
# POSITIVE SIGNALS
# These INCREASE relevance score. Not required.
# ─────────────────────────────────────────────
POSITIVE_SIGNALS = [
    "small business",
    "cooperative",
    "for-profit",
    "rural",
    "agriculture",
    "agricultural",
    "food",
    "specialty crop",
    "technology",
    "innovation",
    "sbir",
    "sttr",
    "pennsylvania",
    " pa ",
    "appalachian",
    "pittsburg",
    "software",
    "artificial intelligence",
    "data",
    "renewable energy",
    "solar",
    "energy efficiency",
    "workforce development",
    "commercialization",
    "startup",
    "entrepreneur",
    "microenterprise",
    "producer",
    "value-added",
    "regenerative",
    "mushroom",
    "fungi",
    "remediation",
    "arts",
    "regional",
    "economic development",
]

# ─────────────────────────────────────────────
# AGENCY WHITELIST
# These agencies are known to fund our profile.
# Others get neutral score.
# ─────────────────────────────────────────────
AGENCY_WHITELIST = [
    "USDA-NIFA", "USDA-RBCS", "USDA-RD", "NSF", "DOC-EDA",
    "SBA", "DOE-ARPA", "DOE-GFO", "EPA", "DOL-ETA",
    "HUD",  # sometimes relevant for cooperative housing/community
]

# ─────────────────────────────────────────────
# AGENCY BLACKLIST
# These almost never fund our profile.
# ─────────────────────────────────────────────
AGENCY_BLACKLIST = [
    "NASA-HQ", "NASA", "DOD-", "USDOJ", "HHS-CDC",
    "DOS-",   # Dept of State — international programs
    "DOI-BOR",  # Bureau of Reclamation — water infrastructure
    "DOD-COE",  # Army Corps of Engineers
    "NRC",    # Nuclear Regulatory Commission
]


def normalize(text: str) -> str:
    """Lowercase and collapse whitespace for matching."""
    return re.sub(r'\s+', ' ', (text or '').lower().strip())


def filter_opportunity(opp: dict) -> dict:
    """
    Filter a single opportunity dict.

    Expected keys: title, synopsis/description, agencyCode, closeDate, id

    Returns dict with:
      - keep: bool
      - reason: str
      - confidence: float (0.0–1.0)
      - signals: list of matched positive signals
      - flags: list of matched soft disqualifiers
    """
    title = normalize(opp.get('title', ''))
    synopsis = normalize(opp.get('synopsis', '') or opp.get('description', '') or '')
    agency = (opp.get('agencyCode') or '').upper()
    combined = title + ' ' + synopsis

    # ── HARD DISQUALIFIER CHECK ──
    for phrase in HARD_DISQUALIFIERS:
        if phrase in combined:
            return {
                'keep': False,
                'reason': f'hard_disqualifier: "{phrase}"',
                'confidence': 0.0,
                'signals': [],
                'flags': [],
            }

    # ── AGENCY BLACKLIST ──
    for bl in AGENCY_BLACKLIST:
        if agency.startswith(bl):
            return {
                'keep': False,
                'reason': f'agency_blacklist: {agency}',
                'confidence': 0.0,
                'signals': [],
                'flags': [],
            }

    # ── SOFT DISQUALIFIERS ──
    flags = [p for p in SOFT_DISQUALIFIERS if p in combined]

    # ── POSITIVE SIGNALS ──
    signals = [p for p in POSITIVE_SIGNALS if p in combined]
    score = len(signals) / max(len(POSITIVE_SIGNALS), 1)

    # Agency whitelist boost
    agency_boost = 0.0
    for wl in AGENCY_WHITELIST:
        if agency.startswith(wl):
            agency_boost = 0.15
            break

    confidence = min(1.0, score + agency_boost)

    # Drop if zero signals and not whitelisted
    if confidence < 0.05 and not agency_boost:
        return {
            'keep': False,
            'reason': 'no_positive_signals',
            'confidence': confidence,
            'signals': signals,
            'flags': flags,
        }

    return {
        'keep': True,
        'reason': 'passed',
        'confidence': round(confidence, 3),
        'signals': signals,
        'flags': flags,
    }


def filter_batch(opportunities: list, min_confidence: float = 0.05) -> tuple:
    """
    Filter a list of opportunity dicts.

    Returns (kept, dropped) tuple of lists.
    Each kept item has filter result merged in.
    """
    kept = []
    dropped = []

    for opp in opportunities:
        result = filter_opportunity(opp)
        opp_copy = dict(opp)
        opp_copy['_filter'] = result

        if result['keep'] and result['confidence'] >= min_confidence:
            kept.append(opp_copy)
        else:
            dropped.append(opp_copy)

    # Sort kept by confidence descending
    kept.sort(key=lambda x: x['_filter']['confidence'], reverse=True)
    return kept, dropped


if __name__ == '__main__':
    # Self-test
    test_opps = [
        {'title': 'USDA NIFA SBIR Phase I Agricultural Technology', 'agencyCode': 'USDA-NIFA', 'synopsis': 'small business innovation research food agriculture cooperative'},
        {'title': 'Drug-Free Communities Support Program', 'agencyCode': 'HHS-CDC-NCIPC', 'synopsis': 'substance abuse prevention local governments'},
        {'title': 'NSF Small Business Innovation Research Technology', 'agencyCode': 'NSF', 'synopsis': 'small business for-profit technology commercialization'},
        {'title': 'ROSES25 Heliophysics Technology', 'agencyCode': 'NASA-HQ', 'synopsis': 'heliophysics astronomy research'},
        {'title': 'Rural Energy for America REAP Solar', 'agencyCode': 'USDA-RBCS', 'synopsis': 'renewable energy solar small business agricultural producer cooperative'},
        {'title': 'EDA Build to Scale Venture Challenge', 'agencyCode': 'DOC-EDA', 'synopsis': 'innovation entrepreneurship small business technology commercialization regional economic development'},
        {'title': 'Tribal Governments Water Infrastructure', 'agencyCode': 'DOI-BOR', 'synopsis': 'tribal governments only water storage'},
    ]

    kept, dropped = filter_batch(test_opps)
    print(f"KEPT: {len(kept)} | DROPPED: {len(dropped)}")
    print("\n--- KEPT ---")
    for o in kept:
        f = o['_filter']
        print(f"  ✅ [{o['agencyCode']}] {o['title']}")
        print(f"     confidence: {f['confidence']} | signals: {f['signals'][:4]}")
    print("\n--- DROPPED ---")
    for o in dropped:
        f = o['_filter']
        print(f"  ❌ [{o.get('agencyCode','?')}] {o['title']}")
        print(f"     reason: {f['reason']}")

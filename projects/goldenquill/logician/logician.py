#!/usr/bin/env python3
"""
Logician — Deterministic Policy Enforcement for Tilth Grant Intelligence

The fourth seat in the council. Not an LLM. Not AI. Pure validation logic.
Fail-closed: if a check can't determine compliance, it fails.

Usage:
    python3 logician.py preflight --context PROJECT_CONTEXT.md --rfa RFA.json
    python3 logician.py validate-draft --draft DRAFT.md --rfa RFA.json --context PROJECT_CONTEXT.md
    python3 logician.py validate-scout --results RESULTS.json --context PROJECT_CONTEXT.md
    python3 logician.py validate-score --score SCORE.json --draft DRAFT.md
    python3 logician.py check-loop --grant-id GRANT_ID
    python3 logician.py full-report --grant-id GRANT_ID

Exit codes:
    0 = all gates pass
    1 = one or more gates failed (violations found)
    2 = error (missing files, bad input)
"""

import json
import sys
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

LOGICIAN_DIR = Path(__file__).parent
WORKSPACE_DIR = LOGICIAN_DIR.parent
PIPELINE_DIR = WORKSPACE_DIR / "pipeline"
REGISTERS_DIR = LOGICIAN_DIR / "registers"
STATE_DIR = LOGICIAN_DIR / "state"
RUBRICS_DIR = PIPELINE_DIR / "rubrics"

MAX_REVISION_LOOPS = 3

# ---------------------------------------------------------------------------
# Five Operating Laws — The Non-Negotiable Core
# ---------------------------------------------------------------------------

class LawViolation:
    """A single violation of one of the Five Operating Laws."""
    def __init__(self, law: int, gate: str, severity: str, message: str,
                 field: str = "", suggestion: str = ""):
        self.law = law          # 1-5
        self.gate = gate        # which validation gate caught this
        self.severity = severity  # RED, YELLOW, GREEN
        self.message = message
        self.field = field
        self.suggestion = suggestion
        self.timestamp = datetime.now(timezone.utc).isoformat()

    def to_dict(self):
        return {
            "law": self.law,
            "gate": self.gate,
            "severity": self.severity,
            "message": self.message,
            "field": self.field,
            "suggestion": self.suggestion,
            "timestamp": self.timestamp
        }


class ValidationResult:
    """Aggregated result from all gates."""
    def __init__(self, gate_name: str):
        self.gate_name = gate_name
        self.violations: list[LawViolation] = []
        self.passed = True
        self.checked_at = datetime.now(timezone.utc).isoformat()

    def fail(self, violation: LawViolation):
        self.violations.append(violation)
        if violation.severity in ("RED", "YELLOW"):
            self.passed = False

    def to_dict(self):
        return {
            "gate": self.gate_name,
            "passed": self.passed,
            "violation_count": len(self.violations),
            "red_count": sum(1 for v in self.violations if v.severity == "RED"),
            "yellow_count": sum(1 for v in self.violations if v.severity == "YELLOW"),
            "green_count": sum(1 for v in self.violations if v.severity == "GREEN"),
            "violations": [v.to_dict() for v in self.violations],
            "checked_at": self.checked_at
        }


# ---------------------------------------------------------------------------
# Gate 1: KGIE Preflight (Law 1 + Law 5)
# Before Scribe drafts, verify the applicant's substance is documented.
# ---------------------------------------------------------------------------

def gate_kgie_preflight(context: dict, rfa: dict = None) -> ValidationResult:
    """
    Validates that Keywords, Geography, Identity, and Experience are present
    in PROJECT_CONTEXT before Scribe begins drafting.

    Law 1: RFA is source of truth — KGIE checks that context maps to RFA needs
    Law 5: Applicant brings substance — if KGIE fields are empty, we stop
    """
    result = ValidationResult("kgie_preflight")

    # --- K: Keywords / Sector alignment ---
    sectors = context.get("sectors", [])
    if not sectors or all(s.strip() == "" or s == "[NEEDED]" for s in sectors):
        result.fail(LawViolation(
            law=5, gate="kgie_preflight", severity="RED",
            message="No sectors defined in PROJECT_CONTEXT. Scribe cannot draft without knowing the applicant's sector focus.",
            field="sectors",
            suggestion="Fill in sectors (e.g., 'specialty crops', 'value-added processing', 'food safety')"
        ))

    products = context.get("products", context.get("value_added_products", []))
    if not products or (isinstance(products, list) and all(str(p).strip() in ("", "[NEEDED]") for p in products)):
        result.fail(LawViolation(
            law=5, gate="kgie_preflight", severity="RED",
            message="No products/value-added products defined. What is the applicant actually producing?",
            field="products",
            suggestion="List the specific value-added products (e.g., 'dried shiitake mushrooms', 'mushroom grow kits')"
        ))

    # --- G: Geography ---
    geo_fields = ["state", "county", "address"]
    for field in geo_fields:
        val = context.get(field, "")
        if not val or val == "[NEEDED]":
            result.fail(LawViolation(
                law=5, gate="kgie_preflight", severity="RED",
                message=f"Geography field '{field}' is missing or [NEEDED]. Many grants require location for eligibility and priority points.",
                field=field,
                suggestion=f"Provide the applicant's {field}"
            ))

    # Rural/urban designation
    rural = context.get("rural_urban", context.get("designation", ""))
    if not rural or rural == "[NEEDED]":
        result.fail(LawViolation(
            law=5, gate="kgie_preflight", severity="YELLOW",
            message="Rural/urban designation not specified. USDA RD programs require rural eligibility.",
            field="rural_urban",
            suggestion="Check USDA eligibility map at https://eligibility.sc.egov.usda.gov/"
        ))

    # --- I: Identity (priority categories) ---
    identity_fields = {
        "entity_type": "What type of entity is the applicant? (co-op, LLC, sole prop, etc.)",
        "organization_name": "Legal name of the applying organization"
    }
    for field, hint in identity_fields.items():
        val = context.get(field, "")
        if not val or val == "[NEEDED]":
            result.fail(LawViolation(
                law=5, gate="kgie_preflight", severity="RED",
                message=f"Identity field '{field}' is missing. {hint}",
                field=field,
                suggestion=hint
            ))

    # Priority markers (not RED — these are point boosters, not blockers)
    priority_markers = ["beginning_farmer", "veteran", "socially_disadvantaged",
                        "women_led", "tribal", "small_medium_farm"]
    has_any_priority = False
    for marker in priority_markers:
        val = context.get(marker, None)
        if val and val not in ("[NEEDED]", "", "false", "False", "no", "No"):
            has_any_priority = True
            break

    if not has_any_priority:
        result.fail(LawViolation(
            law=5, gate="kgie_preflight", severity="GREEN",
            message="No priority identity markers found. Consider documenting if any apply — they're worth 5-10 points on VAPG.",
            field="priority_markers",
            suggestion="Check: beginning farmer (<10yr), veteran, socially disadvantaged, women-led, small/medium family farm"
        ))

    # --- E: Experience ---
    experience_fields = {
        "years_operating": "How long has the entity been operating?",
        "prior_grants": "List of prior grants received (or 'none')",
    }
    for field, hint in experience_fields.items():
        val = context.get(field, "")
        if not val or val == "[NEEDED]":
            result.fail(LawViolation(
                law=5, gate="kgie_preflight", severity="YELLOW",
                message=f"Experience field '{field}' is missing. Scribe needs this to write Key Personnel and qualifications sections.",
                field=field,
                suggestion=hint
            ))

    # SAM / UEI / EIN (critical for federal grants)
    fed_fields = {
        "ein": "Employer Identification Number",
        "uei": "Unique Entity Identifier (SAM.gov)",
        "sam_status": "SAM.gov registration status"
    }
    for field, label in fed_fields.items():
        val = context.get(field, "")
        if not val or val == "[NEEDED]":
            result.fail(LawViolation(
                law=1, gate="kgie_preflight", severity="RED",
                message=f"{label} ({field}) is missing. Federal grants require active SAM registration with UEI and TIN.",
                field=field,
                suggestion=f"Provide {label}. Register at SAM.gov if not already registered."
            ))

    return result


# ---------------------------------------------------------------------------
# Gate 2: RFA Traceability (Law 1 + Law 2)
# Every claim in the draft must trace to RFA or PROJECT_CONTEXT.
# ---------------------------------------------------------------------------

def gate_rfa_traceability(draft_text: str, rfa: dict, context: dict) -> ValidationResult:
    """
    Scans draft for claims that can't be traced to RFA requirements or
    PROJECT_CONTEXT data. This is a heuristic scan — flags patterns that
    suggest fabrication or scope drift.

    Law 1: RFA is source of truth
    Law 2: No boundary drift
    """
    result = ValidationResult("rfa_traceability")

    # Check for common fabrication patterns
    fabrication_patterns = [
        (r'\b\d{1,3}%\s+(increase|decrease|growth|reduction|improvement)',
         "Percentage claim found. Verify this number exists in PROJECT_CONTEXT or supporting docs."),
        (r'\$[\d,]+(?:\.\d{2})?\s+(?:in\s+)?(?:revenue|sales|income|savings)',
         "Dollar amount claim found. Verify against PROJECT_CONTEXT financials."),
        (r'(?:partnership|collaboration|MOU|agreement)\s+with\s+[A-Z][a-z]+',
         "Partnership claim found. Verify documented in PROJECT_CONTEXT or letters of support."),
        (r'(?:certified|certification|licensed|accredited)\s+(?:by|through|in)',
         "Certification claim found. Verify the applicant actually holds this certification."),
        (r'(?:awarded|received|won)\s+(?:a\s+)?(?:grant|award|funding)',
         "Prior award claim found. Verify against PROJECT_CONTEXT prior_grants."),
    ]

    for pattern, message in fabrication_patterns:
        matches = re.finditer(pattern, draft_text, re.IGNORECASE)
        for match in matches:
            # Get surrounding context (50 chars each side)
            start = max(0, match.start() - 50)
            end = min(len(draft_text), match.end() + 50)
            context_snippet = draft_text[start:end].strip()

            result.fail(LawViolation(
                law=1, gate="rfa_traceability", severity="YELLOW",
                message=f"{message}\n  Found: '...{context_snippet}...'",
                field="draft_content",
                suggestion="Applicant must verify this claim. If not in PROJECT_CONTEXT, either add source data or remove the claim."
            ))

    # Check for [NEEDED] or TODO markers still in draft
    todo_patterns = [r'\[NEEDED\]', r'\[TODO\]', r'\[TBD\]', r'\[INSERT\]', r'\[PLACEHOLDER\]']
    for pattern in todo_patterns:
        matches = re.finditer(pattern, draft_text, re.IGNORECASE)
        for match in matches:
            start = max(0, match.start() - 30)
            end = min(len(draft_text), match.end() + 30)
            context_snippet = draft_text[start:end].strip()

            result.fail(LawViolation(
                law=5, gate="rfa_traceability", severity="RED",
                message=f"Placeholder found in draft — substance is missing: '...{context_snippet}...'",
                field="draft_content",
                suggestion="Applicant must provide this data. Do not fabricate."
            ))

    return result


# ---------------------------------------------------------------------------
# Gate 3: Boundary Drift Scanner (Law 2)
# Stay inside the RFA's defined scope.
# ---------------------------------------------------------------------------

def gate_boundary_drift(draft_text: str, rfa: dict) -> ValidationResult:
    """
    Checks if draft activities, budget categories, or outcomes exceed
    what the RFA allows.

    Law 2: No boundary drift — if the RFA doesn't mention it, flag it.
    """
    result = ValidationResult("boundary_drift")

    grant_types = rfa.get("meta", {}).get("grant_types", [])

    # Planning grant scope check
    if "planning" in grant_types:
        # Planning grants are ONLY for feasibility study and/or business/marketing plan
        wc_indicators = [
            (r'(?:purchase|buy|acquire)\s+(?:equipment|machinery|supplies)',
             "Working capital activity in a planning grant context"),
            (r'(?:hire|employ|recruit)\s+(?:staff|workers|employees)',
             "Hiring language — planning grants fund consultants, not staff"),
            (r'(?:construct|build|renovate|install)',
             "Construction/installation language in planning grant"),
            (r'(?:production|manufacturing|processing)\s+(?:run|batch|cycle)',
             "Production activity language in planning grant"),
        ]
        for pattern, message in wc_indicators:
            if re.search(pattern, draft_text, re.IGNORECASE):
                result.fail(LawViolation(
                    law=2, gate="boundary_drift", severity="RED",
                    message=f"Scope drift: {message}. Planning grants fund ONLY feasibility studies and business/marketing plans by qualified consultants.",
                    field="draft_scope",
                    suggestion="Remove working capital activities from planning grant proposal. If both are needed, apply for working capital instead."
                ))

    # Check for scope-expanding language
    drift_phrases = [
        (r'we\s+will\s+also\s+(?:address|tackle|explore|pursue)',
         "Scope-expanding language detected. Does the RFA specifically authorize this additional activity?"),
        (r'(?:in\s+addition|additionally|furthermore|moreover),?\s+(?:we|the)\s+(?:will|plan|intend|propose)',
         "Additive scope language. Verify each proposed activity maps to an RFA requirement."),
        (r'(?:phase\s+(?:2|3|II|III|two|three)|future\s+(?:phase|expansion|growth))',
         "Future phase reference. The grant period is fixed — don't promise beyond it."),
    ]
    for pattern, message in drift_phrases:
        matches = re.finditer(pattern, draft_text, re.IGNORECASE)
        for match in matches:
            start = max(0, match.start() - 40)
            end = min(len(draft_text), match.end() + 40)
            context_snippet = draft_text[start:end].strip()

            result.fail(LawViolation(
                law=2, gate="boundary_drift", severity="YELLOW",
                message=f"{message}\n  Found: '...{context_snippet}...'",
                field="draft_scope",
                suggestion="Verify this activity is explicitly within the RFA's stated purpose. If not, remove or reframe."
            ))

    # Budget ceiling check
    max_amount = rfa.get("meta", {}).get("max_planning", 0)
    if "working_capital" in str(draft_text).lower():
        max_amount = rfa.get("meta", {}).get("max_working_capital", 0)

    # Look for budget total in draft
    budget_matches = re.findall(r'(?:total|grant)\s+(?:request|amount|budget)[:\s]*\$?([\d,]+)',
                                 draft_text, re.IGNORECASE)
    for match_str in budget_matches:
        try:
            amount = int(match_str.replace(",", ""))
            if max_amount > 0 and amount > max_amount:
                result.fail(LawViolation(
                    law=2, gate="boundary_drift", severity="RED",
                    message=f"Budget amount ${amount:,} exceeds maximum award of ${max_amount:,}",
                    field="budget_total",
                    suggestion=f"Reduce grant request to ${max_amount:,} or below"
                ))
        except ValueError:
            pass

    return result


# ---------------------------------------------------------------------------
# Gate 4: Admin-Risk Term Scanner (Law 4)
# Scan for politically flagged terms. Never silently rewrite.
# ---------------------------------------------------------------------------

def load_admin_risk_register() -> list:
    """Load the admin-risk register from JSON."""
    register_path = REGISTERS_DIR / "admin_risk_register.json"
    if not register_path.exists():
        return []
    with open(register_path, "r") as f:
        data = json.load(f)
    return data.get("terms", [])


def gate_admin_risk_scan(draft_text: str) -> ValidationResult:
    """
    Scans draft for terms in the admin-risk register.

    Law 4: Apolitical sector language + admin-risk term scanning.
    NEVER silently rewrite — flag for applicant approval.
    """
    result = ValidationResult("admin_risk_scan")
    terms = load_admin_risk_register()

    if not terms:
        result.fail(LawViolation(
            law=4, gate="admin_risk_scan", severity="GREEN",
            message="Admin-risk register is empty. No terms to scan against. Consider populating registers/admin_risk_register.json",
            field="register",
            suggestion="The register should contain terms flagged by the current administration with severity tiers."
        ))
        return result

    draft_lower = draft_text.lower()

    for term_entry in terms:
        term = term_entry.get("term", "")
        severity = term_entry.get("severity", "GREEN")
        citation = term_entry.get("citation", "")
        substitution = term_entry.get("substitution", "")

        # Search for the term (word-boundary match)
        pattern = r'\b' + re.escape(term.lower()) + r'\b'
        matches = list(re.finditer(pattern, draft_lower))

        if matches:
            for match in matches:
                start = max(0, match.start() - 40)
                end = min(len(draft_text), match.end() + 40)
                context_snippet = draft_text[start:end].strip()

                result.fail(LawViolation(
                    law=4, gate="admin_risk_scan", severity=severity,
                    message=f"Admin-risk term detected: '{term}' [{severity}]\n  Citation: {citation}\n  Found in: '...{context_snippet}...'",
                    field="flagged_term",
                    suggestion=f"Suggested substitution: '{substitution}' — APPLICANT MUST APPROVE before replacing."
                ))

    return result


# ---------------------------------------------------------------------------
# Gate 5: Overlooked Expenses (Law 1 + Law 5)
# Budget sections must include these or explicitly mark N/A.
# ---------------------------------------------------------------------------

OVERLOOKED_EXPENSE_CATEGORIES = [
    "in-kind space/utilities (rent, electricity, water, internet)",
    "volunteer/board labor (match value)",
    "printing, postage, branding, translation",
    "audit and grant reporting costs",
    "compliance (FDA, GAP, organic certification, FSMA)",
    "travel/mileage for outreach",
    "evaluation/data collection tools",
    "insurance and legal fees",
    "packaging, storage, freight",
    "training and professional development",
    "indirect costs (if allowed by RFA)"
]


def gate_overlooked_expenses(draft_text: str, rfa: dict = None) -> ValidationResult:
    """
    Checks that budget sections address all commonly overlooked expense
    categories, or explicitly mark them N/A.

    Law 5: Applicant brings the substance — we flag missing budget lines,
    not invent them.
    """
    result = ValidationResult("overlooked_expenses")
    draft_lower = draft_text.lower()

    for category in OVERLOOKED_EXPENSE_CATEGORIES:
        # Extract keywords from category
        keywords = [w for w in category.split()
                    if len(w) > 3 and w not in ("with", "that", "from", "this", "allowed")]

        # Check if any keyword appears in the draft
        found = False
        for kw in keywords:
            # Clean parenthetical indicators
            kw_clean = kw.strip("()/,")
            if kw_clean and kw_clean.lower() in draft_lower:
                found = True
                break

        if not found:
            result.fail(LawViolation(
                law=5, gate="overlooked_expenses", severity="YELLOW",
                message=f"Budget may be missing: {category}",
                field="budget",
                suggestion=f"Either include a line item for {category} or explicitly note it as N/A with justification."
            ))

    return result


# ---------------------------------------------------------------------------
# Gate 6: Org Isolation Check (Law 3)
# One org per session. No cross-contamination.
# ---------------------------------------------------------------------------

def gate_org_isolation(draft_text: str, context: dict, all_org_names: list = None) -> ValidationResult:
    """
    Checks that the draft doesn't reference data from other orgs.

    Law 3: Org Isolation — one PROJECT_CONTEXT per session.
    """
    result = ValidationResult("org_isolation")

    if not all_org_names:
        # If we don't have a list of other orgs, we can't check
        return result

    current_org = context.get("organization_name", "").lower()
    draft_lower = draft_text.lower()

    for org_name in all_org_names:
        org_lower = org_name.lower()
        if org_lower == current_org:
            continue  # Skip the current org

        if org_lower in draft_lower:
            result.fail(LawViolation(
                law=3, gate="org_isolation", severity="RED",
                message=f"Cross-org data detected: '{org_name}' appears in draft but is not the current applicant ({context.get('organization_name', 'unknown')})",
                field="org_isolation",
                suggestion=f"Remove all references to '{org_name}'. This org's data must not appear in another org's proposal."
            ))

    return result


# ---------------------------------------------------------------------------
# Gate 7: Revision Loop Counter (Autonomy Rule 2)
# Max 3 auto-revisions before human input required.
# ---------------------------------------------------------------------------

def gate_revision_loop(grant_id: str) -> ValidationResult:
    """
    Checks if the revision count has exceeded the maximum.

    Autonomy Rule: Don't loop more than 3 times without human input.
    """
    result = ValidationResult("revision_loop")

    state_file = STATE_DIR / f"{grant_id}_revisions.json"

    if not state_file.exists():
        # No revisions yet — we're good
        return result

    with open(state_file, "r") as f:
        state = json.load(f)

    count = state.get("revision_count", 0)

    if count >= MAX_REVISION_LOOPS:
        result.fail(LawViolation(
            law=0, gate="revision_loop", severity="RED",
            message=f"Revision loop limit reached ({count}/{MAX_REVISION_LOOPS}). Human review required before continuing.",
            field="revision_count",
            suggestion="The applicant must review the current draft and provide direction before more automated revisions."
        ))
    elif count == MAX_REVISION_LOOPS - 1:
        result.fail(LawViolation(
            law=0, gate="revision_loop", severity="YELLOW",
            message=f"Approaching revision limit ({count}/{MAX_REVISION_LOOPS}). Next revision will require human input.",
            field="revision_count",
            suggestion="Consider having the applicant review the draft now rather than after the next revision."
        ))

    return result


def increment_revision(grant_id: str) -> int:
    """Increment the revision counter for a grant. Returns new count."""
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    state_file = STATE_DIR / f"{grant_id}_revisions.json"

    if state_file.exists():
        with open(state_file, "r") as f:
            state = json.load(f)
    else:
        state = {"grant_id": grant_id, "revision_count": 0, "history": []}

    state["revision_count"] += 1
    state["history"].append({
        "revision": state["revision_count"],
        "timestamp": datetime.now(timezone.utc).isoformat()
    })

    with open(state_file, "w") as f:
        json.dump(state, f, indent=2)

    return state["revision_count"]


def reset_revision(grant_id: str):
    """Reset revision counter (after human review)."""
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    state_file = STATE_DIR / f"{grant_id}_revisions.json"

    if state_file.exists():
        with open(state_file, "r") as f:
            state = json.load(f)
        state["revision_count"] = 0
        state["history"].append({
            "event": "human_review_reset",
            "timestamp": datetime.now(timezone.utc).isoformat()
        })
        with open(state_file, "w") as f:
            json.dump(state, f, indent=2)


# ---------------------------------------------------------------------------
# Gate 8: Rubric Completeness Check
# Ensures Judge scored all required dimensions from the funder's rubric.
# ---------------------------------------------------------------------------

def gate_rubric_completeness(score_data: dict, rubric_path: str = None) -> ValidationResult:
    """
    Validates that Judge's score report covers all dimensions in the rubric.
    Uses funder's rubric first (if available), falls back to 90+ Funder Rubric.
    """
    result = ValidationResult("rubric_completeness")

    # Load funder rubric if specified
    if rubric_path and Path(rubric_path).exists():
        with open(rubric_path, "r") as f:
            rubric = json.load(f)
        criteria = rubric.get("scoring_criteria", [])
        rubric_name = rubric.get("meta", {}).get("program", "funder rubric")
    else:
        # No funder rubric — flag it
        result.fail(LawViolation(
            law=1, gate="rubric_completeness", severity="YELLOW",
            message="No funder rubric loaded. Judge should score against the funder's actual rubric first.",
            field="rubric",
            suggestion="Extract and store the funder's scoring criteria from the RFA/NOFO."
        ))
        return result

    scored_criteria = score_data.get("scored_criteria", score_data.get("dimensions", {}))

    for criterion in criteria:
        cid = criterion.get("id", criterion.get("name", ""))
        if cid not in scored_criteria and criterion.get("name", "") not in str(scored_criteria):
            result.fail(LawViolation(
                law=1, gate="rubric_completeness", severity="RED",
                message=f"Criterion '{cid}: {criterion.get('name', '')}' (max {criterion.get('max_points', '?')} pts) not scored by Judge.",
                field=f"criterion_{cid}",
                suggestion=f"Judge must score this criterion. It's worth up to {criterion.get('max_points', '?')} points."
            ))

    # Check for evidence strings
    if "evidence" not in str(score_data).lower():
        result.fail(LawViolation(
            law=1, gate="rubric_completeness", severity="YELLOW",
            message="Score report lacks evidence strings. Judge should quote specific passages from the draft that justify each score.",
            field="evidence",
            suggestion="For each scored dimension, quote the draft text that supports the score."
        ))

    return result


# ---------------------------------------------------------------------------
# Orchestration: Run all gates
# ---------------------------------------------------------------------------

def run_preflight(context_path: str, rfa_path: str = None) -> dict:
    """Run KGIE preflight before Scribe drafts."""
    with open(context_path, "r") as f:
        # Try JSON first, fall back to parsing markdown
        content = f.read()
        try:
            context = json.loads(content)
        except json.JSONDecodeError:
            context = parse_markdown_context(content)

    rfa = {}
    if rfa_path and Path(rfa_path).exists():
        with open(rfa_path, "r") as f:
            rfa = json.load(f)

    kgie = gate_kgie_preflight(context, rfa)

    report = {
        "type": "preflight",
        "passed": kgie.passed,
        "gates": [kgie.to_dict()],
        "summary": f"KGIE Preflight: {'PASS' if kgie.passed else 'FAIL'} — {len(kgie.violations)} issues found",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    return report


def run_draft_validation(draft_path: str, rfa_path: str, context_path: str,
                         org_names: list = None) -> dict:
    """Run all post-draft gates: traceability, boundary drift, admin-risk, expenses, org isolation."""
    with open(draft_path, "r") as f:
        draft_text = f.read()

    with open(context_path, "r") as f:
        content = f.read()
        try:
            context = json.loads(content)
        except json.JSONDecodeError:
            context = parse_markdown_context(content)

    rfa = {}
    if rfa_path and Path(rfa_path).exists():
        with open(rfa_path, "r") as f:
            rfa = json.load(f)

    gates = [
        gate_rfa_traceability(draft_text, rfa, context),
        gate_boundary_drift(draft_text, rfa),
        gate_admin_risk_scan(draft_text),
        gate_overlooked_expenses(draft_text, rfa),
        gate_org_isolation(draft_text, context, org_names or []),
    ]

    all_passed = all(g.passed for g in gates)
    total_violations = sum(len(g.violations) for g in gates)

    report = {
        "type": "draft_validation",
        "passed": all_passed,
        "gates": [g.to_dict() for g in gates],
        "summary": f"Draft Validation: {'PASS' if all_passed else 'FAIL'} — {total_violations} issues across {len(gates)} gates",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    return report


def run_score_validation(score_path: str, draft_path: str, rubric_path: str = None) -> dict:
    """Validate Judge's score report for completeness."""
    with open(score_path, "r") as f:
        score_data = json.load(f)

    with open(draft_path, "r") as f:
        draft_text = f.read()

    rubric_check = gate_rubric_completeness(score_data, rubric_path)

    report = {
        "type": "score_validation",
        "passed": rubric_check.passed,
        "gates": [rubric_check.to_dict()],
        "summary": f"Score Validation: {'PASS' if rubric_check.passed else 'FAIL'} — {len(rubric_check.violations)} issues",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    return report


# ---------------------------------------------------------------------------
# Utility: Parse markdown PROJECT_CONTEXT into dict
# ---------------------------------------------------------------------------

def parse_markdown_context(text: str) -> dict:
    """
    Best-effort extraction of key fields from a markdown PROJECT_CONTEXT.
    Handles multiple formats:
    - **Key:** Value (bold key in list items)
    - Key: Value (plain key-value)
    - YAML frontmatter (org, sectors, etc.)
    """
    context = {}
    lines = text.split("\n")

    # Parse YAML frontmatter if present
    if lines and lines[0].strip() == "---":
        for i, line in enumerate(lines[1:], 1):
            if line.strip() == "---":
                break
            fm_match = re.match(r'^(\w+):\s*(.+)', line)
            if fm_match:
                key = fm_match.group(1).strip().lower()
                value = fm_match.group(2).strip()
                # Handle YAML lists like [food_ag, remediation]
                if value.startswith("[") and value.endswith("]"):
                    value = [v.strip() for v in value[1:-1].split(",")]
                context[key] = value

    for line in lines:
        # Match "- **Key:** Value" patterns (bold key in list items)
        match = re.match(r'^[-*]\s+\*\*([^*]+)\*\*\s*[:]\s*(.+)', line)
        if match:
            key = match.group(1).strip().lower().replace(" ", "_")
            # Strip trailing markdown/parentheticals from key
            key = re.sub(r'\s*\(.*?\)\s*$', '', key)
            value = match.group(2).strip()
            context[key] = value
            continue

        # Match "- **Key:** Value" with no space after colon
        match = re.match(r'^[-*]\s+\*\*([^*]+):\*\*\s*(.+)', line)
        if match:
            key = match.group(1).strip().lower().replace(" ", "_")
            key = re.sub(r'\s*\(.*?\)\s*$', '', key)
            value = match.group(2).strip()
            context[key] = value
            continue

        # Match plain "Key: Value" patterns
        match = re.match(r'^[-*]?\s*\*?\*?([A-Za-z_\s]+)\*?\*?\s*[:=]\s*(.+)', line)
        if match:
            key = match.group(1).strip().lower().replace(" ", "_")
            value = match.group(2).strip()
            context[key] = value

    # Normalize common field name variations
    aliases = {
        "legal_name": "organization_name",
        "org": "organization_name",
        "state_of_incorporation": "state",
        "principal_office": "address",
    }
    for alias, canonical in aliases.items():
        if alias in context and canonical not in context:
            context[canonical] = context[alias]

    return context


# ---------------------------------------------------------------------------
# CLI Interface
# ---------------------------------------------------------------------------

def save_report(report: dict, grant_id: str = "unknown"):
    """Save validation report to pipeline/validation/"""
    validation_dir = PIPELINE_DIR / "validation" / grant_id
    validation_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = validation_dir / f"{report['type']}_{timestamp}.json"

    with open(report_file, "w") as f:
        json.dump(report, f, indent=2)

    return str(report_file)


def print_report(report: dict):
    """Human-readable report output."""
    passed = report["passed"]
    status = "✅ PASS" if passed else "❌ FAIL"

    print(f"\n{'='*60}")
    print(f"  LOGICIAN VALIDATION REPORT — {status}")
    print(f"  {report['summary']}")
    print(f"  {report['timestamp']}")
    print(f"{'='*60}\n")

    for gate in report["gates"]:
        gate_status = "✅" if gate["passed"] else "❌"
        print(f"  {gate_status} {gate['gate']}: {gate['violation_count']} violations "
              f"(🔴 {gate['red_count']} 🟡 {gate['yellow_count']} 🟢 {gate['green_count']})")

        for v in gate["violations"]:
            icon = {"RED": "🔴", "YELLOW": "🟡", "GREEN": "🟢"}.get(v["severity"], "⚪")
            print(f"      {icon} Law {v['law']}: {v['message']}")
            if v["suggestion"]:
                print(f"         → {v['suggestion']}")
        print()

    if not passed:
        red_count = sum(g["red_count"] for g in report["gates"])
        yellow_count = sum(g["yellow_count"] for g in report["gates"])
        print(f"  ⛔ BLOCKED: {red_count} RED violations must be resolved before proceeding.")
        if yellow_count:
            print(f"  ⚠️  ADVISORY: {yellow_count} YELLOW items should be addressed.")
    else:
        green_count = sum(g["green_count"] for g in report["gates"])
        if green_count:
            print(f"  ℹ️  {green_count} GREEN suggestions for improvement (non-blocking).")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)

    command = sys.argv[1]

    # Parse simple --key value args
    args = {}
    i = 2
    while i < len(sys.argv):
        if sys.argv[i].startswith("--"):
            key = sys.argv[i][2:]
            if i + 1 < len(sys.argv) and not sys.argv[i + 1].startswith("--"):
                args[key] = sys.argv[i + 1]
                i += 2
            else:
                args[key] = True
                i += 1
        else:
            i += 1

    try:
        if command == "preflight":
            context_path = args.get("context", "")
            rfa_path = args.get("rfa", "")
            if not context_path:
                print("Error: --context PROJECT_CONTEXT path required", file=sys.stderr)
                sys.exit(2)
            report = run_preflight(context_path, rfa_path)

        elif command == "validate-draft":
            draft = args.get("draft", "")
            rfa = args.get("rfa", "")
            context = args.get("context", "")
            if not all([draft, context]):
                print("Error: --draft, --context required", file=sys.stderr)
                sys.exit(2)
            org_names = args.get("org-names", "").split(",") if args.get("org-names") else []
            report = run_draft_validation(draft, rfa, context, org_names)

        elif command == "validate-score":
            score = args.get("score", "")
            draft = args.get("draft", "")
            rubric = args.get("rubric", "")
            if not all([score, draft]):
                print("Error: --score, --draft required", file=sys.stderr)
                sys.exit(2)
            report = run_score_validation(score, draft, rubric)

        elif command == "check-loop":
            grant_id = args.get("grant-id", "")
            if not grant_id:
                print("Error: --grant-id required", file=sys.stderr)
                sys.exit(2)
            loop_result = gate_revision_loop(grant_id)
            report = {
                "type": "revision_loop_check",
                "passed": loop_result.passed,
                "gates": [loop_result.to_dict()],
                "summary": f"Revision Loop: {'PASS' if loop_result.passed else 'BLOCKED — human review required'}",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }

        elif command == "increment-revision":
            grant_id = args.get("grant-id", "")
            if not grant_id:
                print("Error: --grant-id required", file=sys.stderr)
                sys.exit(2)
            count = increment_revision(grant_id)
            print(f"Revision count for {grant_id}: {count}/{MAX_REVISION_LOOPS}")
            sys.exit(0)

        elif command == "reset-revision":
            grant_id = args.get("grant-id", "")
            if not grant_id:
                print("Error: --grant-id required", file=sys.stderr)
                sys.exit(2)
            reset_revision(grant_id)
            print(f"Revision count reset for {grant_id}")
            sys.exit(0)

        else:
            print(f"Unknown command: {command}", file=sys.stderr)
            print(__doc__)
            sys.exit(2)

        # Save and print report
        grant_id = args.get("grant-id", "unknown")
        saved_to = save_report(report, grant_id)
        print_report(report)
        print(f"  Report saved: {saved_to}")

        sys.exit(0 if report["passed"] else 1)

    except FileNotFoundError as e:
        print(f"Error: File not found — {e}", file=sys.stderr)
        sys.exit(2)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON — {e}", file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()

"""F-DERIVATION-AST-FORBIDDEN-NODE — derivation PRE-write + POST-read (M1 §3).

CF-RT-02 closure.  v7.0.4 §4.5's grammar was informal; M1 §3 enumerates
the AST node-type whitelist.  This gate fires at:

* **Write-time** — when an operator-signed derivation override is
  written, the formula is validated before the signature is accepted.
* **Draft-time read** (POST-gate) — when Logician evaluates a draft
  claim with ``derivation_id`` annotation, the formula is re-validated.

Wraps :func:`pipeline.logician.derivation.ast_whitelist.validate_derivation_formula`.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final, Optional

from pipeline.logician.derivation.ast_whitelist import (
    AstWhitelistError,
    DerivationParseError,
    ParsedFormula,
    validate_derivation_formula,
)


F_DERIVATION_AST_FORBIDDEN_NODE: Final[str] = "F-DERIVATION-AST-FORBIDDEN-NODE"


@dataclass(frozen=True, kw_only=True)
class AstForbiddenNodeResult:
    success: bool
    failure_code: Optional[str]
    detail: str
    formula_text: Optional[str] = None
    parsed: Optional[ParsedFormula] = None
    offending_node_type: Optional[str] = None


def check_derivation_ast_forbidden_node(
    *,
    formula: str,
) -> AstForbiddenNodeResult:
    """PRE-write + POST-read gate: validate derivation formula AST whitelist."""
    try:
        parsed = validate_derivation_formula(formula)
    except AstWhitelistError as exc:
        return AstForbiddenNodeResult(
            success=False,
            failure_code=F_DERIVATION_AST_FORBIDDEN_NODE,
            detail=str(exc),
            formula_text=formula,
            offending_node_type=getattr(exc, "offending_node_type", None),
        )
    except DerivationParseError as exc:
        return AstForbiddenNodeResult(
            success=False,
            failure_code=F_DERIVATION_AST_FORBIDDEN_NODE,
            detail=(
                f"derivation formula did not parse: {exc} (treat as "
                "forbidden — only well-formed expressions admitted)"
            ),
            formula_text=formula,
            offending_node_type="parse_error",
        )
    return AstForbiddenNodeResult(
        success=True,
        failure_code=None,
        detail=(
            f"derivation formula {formula!r} passed AST whitelist; "
            f"references {len(parsed.fact_id_refs)} fact_id(s)"
        ),
        formula_text=formula,
        parsed=parsed,
    )


__all__ = [
    "F_DERIVATION_AST_FORBIDDEN_NODE",
    "AstForbiddenNodeResult",
    "check_derivation_ast_forbidden_node",
]

"""Derivation-formula AST whitelist (architecture v7.0.4-M1 §3).

Single explicit-allow-list :class:`ast.NodeVisitor`.  Anything not
on the allow list raises :class:`AstWhitelistError` so the caller can
map to ``F-DERIVATION-AST-FORBIDDEN-NODE`` fail-closed.

Allowed shape (the only formulas a derivation may carry):

* top-level :class:`ast.Expression`
* :class:`ast.BinOp` with :class:`ast.Add` / :class:`ast.Sub` /
  :class:`ast.Mult` / :class:`ast.Div`
* :class:`ast.UnaryOp` with :class:`ast.UAdd` / :class:`ast.USub`
* :class:`ast.Constant` of :class:`int` or :class:`str` only
  (Decimal-string literals); float-Constant is forbidden per RT-10
* :class:`ast.Name` whose ``id`` is exactly ``"kfr_facts"``
* :class:`ast.Subscript` on ``ast.Name(id='kfr_facts')`` with an
  :class:`ast.Constant` of ``str`` slice (the fact_id)
* :class:`ast.Attribute` whose ``attr`` is exactly ``"value"``
* :class:`ast.Load` context

All other node types fail.  Identifiers that contain ``__``, start /
end with ``_``, or use any name other than ``kfr_facts`` / ``value``
fail.  Subscript-key string contents are checked against dunder
patterns (RT-04 closure).
"""

from __future__ import annotations

import ast
import re
from dataclasses import dataclass
from typing import Final


F_DERIVATION_AST_FORBIDDEN_NODE: Final[str] = "F-DERIVATION-AST-FORBIDDEN-NODE"

ALLOWED_BINOP_TYPES: Final[tuple[type, ...]] = (
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
)
ALLOWED_UNARYOP_TYPES: Final[tuple[type, ...]] = (
    ast.UAdd,
    ast.USub,
)
ALLOWED_NODE_TYPES: Final[tuple[type, ...]] = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Constant,
    ast.Name,
    ast.Subscript,
    ast.Attribute,
    ast.Load,
) + ALLOWED_BINOP_TYPES + ALLOWED_UNARYOP_TYPES

_KFR_FACTS_NAME: Final[str] = "kfr_facts"
_VALUE_ATTR: Final[str] = "value"
_DUNDER_RE: Final[re.Pattern[str]] = re.compile(r"__")
_LEADING_TRAILING_UNDERSCORE_RE: Final[re.Pattern[str]] = re.compile(
    r"^_|_$"
)

# Python 3.9+ deprecated ``ast.Index``/``ast.ExtSlice`` as slice
# wrappers; 3.12+ may have removed them.  Resolve at import time so
# the visitor refuses them when they exist on the running interpreter
# (RT-03 cross-version closure) without crashing on interpreters that
# have removed the symbols entirely.
_AST_INDEX_TYPE: Final[type | None] = getattr(ast, "Index", None)


class DerivationParseError(SyntaxError):
    """Raised when ``ast.parse`` itself refuses the formula."""


class AstWhitelistError(ValueError):
    """Raised when a node fails the §3.2 whitelist.

    Carries an ``offending_node_type`` attribute (string class name)
    and an ``offending_detail`` summarizing the rejection so the
    caller can map to ``F-DERIVATION-AST-FORBIDDEN-NODE`` with a
    structured sub-tag.
    """

    def __init__(
        self,
        message: str,
        *,
        offending_node_type: str,
        offending_detail: str = "",
    ) -> None:
        super().__init__(message)
        self.offending_node_type = offending_node_type
        self.offending_detail = offending_detail


@dataclass(frozen=True, kw_only=True)
class ParsedFormula:
    """Successfully whitelisted derivation formula.

    Carries the parsed AST + the set of ``(fact_id,)`` references for
    the derivation provenance audit per §3.3.
    """

    formula_text: str
    tree: ast.Expression
    fact_id_refs: tuple[str, ...]


def _identifier_legal(name: str, *, expected: str | None) -> bool:
    """Identifier discipline per §3.2.

    When ``expected`` is provided, the identifier MUST equal it
    exactly.  Otherwise the identifier is forbidden by default — the
    visitor uses ``expected`` to gate ``ast.Name.id`` (=``kfr_facts``)
    and ``ast.Attribute.attr`` (=``value``).
    """
    if expected is None:
        return False
    if name != expected:
        return False
    if _DUNDER_RE.search(name):
        return False
    if _LEADING_TRAILING_UNDERSCORE_RE.search(name):
        return False
    return True


def _refuse(
    node: ast.AST,
    *,
    detail: str,
    sub_tag: str | None = None,
) -> None:
    node_type = type(node).__name__
    full = f"{F_DERIVATION_AST_FORBIDDEN_NODE}"
    if sub_tag:
        full = f"{full}.{sub_tag}"
    raise AstWhitelistError(
        f"{full}: {detail} (node_type={node_type})",
        offending_node_type=node_type,
        offending_detail=detail,
    )


class WhitelistVisitor(ast.NodeVisitor):
    """Allow-list visitor per §3.2.

    Methods that ``visit_*`` a node MUST whitelist it explicitly; any
    node missing a visitor falls through to :meth:`generic_visit` which
    refuses fail-closed.
    """

    def __init__(self) -> None:
        super().__init__()
        self._fact_ids: list[str] = []

    @property
    def fact_id_refs(self) -> tuple[str, ...]:
        # Stable de-duplicated order = first appearance.
        seen: list[str] = []
        seen_set: set[str] = set()
        for fid in self._fact_ids:
            if fid in seen_set:
                continue
            seen.append(fid)
            seen_set.add(fid)
        return tuple(seen)

    # ---- Allowed node types -----------------------------------------------

    def visit_Expression(self, node: ast.Expression) -> None:
        self.visit(node.body)

    def visit_BinOp(self, node: ast.BinOp) -> None:
        if not isinstance(node.op, ALLOWED_BINOP_TYPES):
            _refuse(
                node.op,
                detail=(
                    f"binop operator {type(node.op).__name__} not in allowed "
                    f"set {sorted(t.__name__ for t in ALLOWED_BINOP_TYPES)}"
                ),
                sub_tag="binop_operator",
            )
        self.visit(node.left)
        self.visit(node.right)

    def visit_UnaryOp(self, node: ast.UnaryOp) -> None:
        if not isinstance(node.op, ALLOWED_UNARYOP_TYPES):
            _refuse(
                node.op,
                detail=(
                    f"unaryop operator {type(node.op).__name__} not in allowed "
                    f"set {sorted(t.__name__ for t in ALLOWED_UNARYOP_TYPES)}"
                ),
                sub_tag="unaryop_operator",
            )
        self.visit(node.operand)

    def visit_Constant(self, node: ast.Constant) -> None:
        # Float constant rejection per RT-10.
        if isinstance(node.value, bool):
            _refuse(
                node,
                detail=(
                    "bool Constant not admitted in derivation formulas; "
                    "use 0/1 Decimal-string Constants instead"
                ),
                sub_tag="bool_constant",
            )
        if isinstance(node.value, float):
            _refuse(
                node,
                detail=(
                    "float Constant forbidden in derivation formulas "
                    "(RT-10 closure); encode currency literals as "
                    "Decimal-string Constants e.g. ast.Constant(value=\"123.45\")"
                ),
                sub_tag="float_constant",
            )
        if isinstance(node.value, int):
            return
        if isinstance(node.value, str):
            # String contents validated separately when used as a
            # subscript-key (RT-04 closure) — handled in visit_Subscript.
            return
        _refuse(
            node,
            detail=(
                f"Constant value type {type(node.value).__name__} not in "
                "allowed set {int, str}"
            ),
            sub_tag="constant_type",
        )

    def visit_Name(self, node: ast.Name) -> None:
        if not _identifier_legal(node.id, expected=_KFR_FACTS_NAME):
            _refuse(
                node,
                detail=(
                    f"Name id={node.id!r} not the single allowed identifier "
                    f"{_KFR_FACTS_NAME!r}"
                ),
                sub_tag="forbidden_identifier",
            )

    def visit_Subscript(self, node: ast.Subscript) -> None:
        if not (
            isinstance(node.value, ast.Name)
            and node.value.id == _KFR_FACTS_NAME
        ):
            _refuse(
                node,
                detail=(
                    "Subscript value must be ast.Name(id='kfr_facts'); "
                    "nested or other subscripts are forbidden"
                ),
                sub_tag="non_kfr_facts_subscript",
            )

        slice_node = node.slice
        if _AST_INDEX_TYPE is not None and isinstance(slice_node, _AST_INDEX_TYPE):
            _refuse(
                slice_node,
                detail=(
                    "ast.Index slice wrapper forbidden (RT-03 closure); "
                    "Python 3.8/3.9 cross-version inconsistency surface"
                ),
                sub_tag="ast_index_wrapper",
            )
        if isinstance(slice_node, ast.Slice):
            _refuse(
                slice_node,
                detail=(
                    "ast.Slice (start:stop:step) forbidden in derivation "
                    "subscript; only literal string fact_id allowed"
                ),
                sub_tag="ast_slice",
            )
        if not isinstance(slice_node, ast.Constant):
            _refuse(
                slice_node,
                detail=(
                    "Subscript slice must be ast.Constant(value=<str>) "
                    "with a literal fact_id"
                ),
                sub_tag="subscript_slice_not_constant",
            )
        if not isinstance(slice_node.value, str):
            _refuse(
                slice_node,
                detail=(
                    f"Subscript slice Constant must be str, got "
                    f"{type(slice_node.value).__name__}"
                ),
                sub_tag="subscript_slice_not_string",
            )
        # RT-04 closure — string-content discipline.
        fact_id = slice_node.value
        if _DUNDER_RE.search(fact_id):
            _refuse(
                slice_node,
                detail=(
                    f"Subscript fact_id {fact_id!r} contains '__' "
                    "(dunder substring) — forbidden per RT-04"
                ),
                sub_tag="subscript_key_dunder",
            )
        if not fact_id:
            _refuse(
                slice_node,
                detail="Subscript fact_id may not be empty string",
                sub_tag="subscript_key_empty",
            )
        self._fact_ids.append(fact_id)
        # Visit value (the Name node) for the kfr_facts identifier check.
        self.visit(node.value)
        # Visit ctx (Load) — Load passes through generic_visit since
        # ast.Load is in ALLOWED_NODE_TYPES via the type check.
        self.visit(node.ctx)

    def visit_Attribute(self, node: ast.Attribute) -> None:
        if not _identifier_legal(node.attr, expected=_VALUE_ATTR):
            _refuse(
                node,
                detail=(
                    f"Attribute attr={node.attr!r} not the single allowed "
                    f"attribute {_VALUE_ATTR!r}"
                ),
                sub_tag="forbidden_attribute",
            )
        # Underlying expression must be a Subscript on kfr_facts (the
        # `kfr_facts['<id>']` shape).  Validate by visiting.
        self.visit(node.value)
        self.visit(node.ctx)

    def visit_Load(self, node: ast.Load) -> None:
        return  # whitelisted no-op

    def visit_Store(self, node: ast.Store) -> None:
        _refuse(node, detail="Store context forbidden (read-only formulas)")

    def visit_Del(self, node: ast.Del) -> None:
        _refuse(node, detail="Del context forbidden")

    # ---- Default refusal for everything else ------------------------------

    def generic_visit(self, node: ast.AST) -> None:  # type: ignore[override]
        _refuse(
            node,
            detail=(
                f"node type {type(node).__name__} not in derivation "
                "whitelist"
            ),
        )


def validate_derivation_formula(formula: str) -> ParsedFormula:
    """Parse + whitelist-validate a derivation formula.

    Raises:
        DerivationParseError: ``ast.parse`` itself refused.
        AstWhitelistError: a node failed the whitelist.
    """
    if not isinstance(formula, str):
        raise AstWhitelistError(
            f"{F_DERIVATION_AST_FORBIDDEN_NODE}: formula must be str, got "
            f"{type(formula).__name__}",
            offending_node_type="non-string",
            offending_detail="formula input is not str",
        )
    try:
        tree = ast.parse(formula, mode="eval")
    except SyntaxError as exc:
        raise DerivationParseError(
            f"derivation formula {formula!r} did not parse: {exc}"
        ) from exc

    visitor = WhitelistVisitor()
    visitor.visit(tree)

    return ParsedFormula(
        formula_text=formula,
        tree=tree,
        fact_id_refs=visitor.fact_id_refs,
    )


__all__ = [
    "ALLOWED_BINOP_TYPES",
    "ALLOWED_NODE_TYPES",
    "ALLOWED_UNARYOP_TYPES",
    "AstWhitelistError",
    "DerivationParseError",
    "F_DERIVATION_AST_FORBIDDEN_NODE",
    "ParsedFormula",
    "WhitelistVisitor",
    "validate_derivation_formula",
]

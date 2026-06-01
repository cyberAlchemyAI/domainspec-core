from __future__ import annotations

import ast
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator

from pipeline.linting._rule_types import Rule, Violation

# ---------------------------------------------------------------------------
# R7 — AST_PREFLIGHT_DOMINATES_FD_REQUEST — CFG-dominance check
# ---------------------------------------------------------------------------
#
# Every `fd_broker.request(...)` sink in `pipeline/loop/**` or
# `pipeline/scout/**` must be CFG-dominated by an `if <SENTINEL>:` guard
# whose `<SENTINEL>` is a module-scope `typing.Final[bool]` with a *literal*
# initializer (B-v5-01). Cross-module sentinels resolved via ImportFrom
# against sibling tree (B-v5-03). Short-circuit `and` admits; `or` rejects
# (B-v5-01 short-circuit handling).


_PREFLIGHT_BUILTIN_BOOLS: frozenset[str] = frozenset({"True", "False"})


@dataclass(frozen=True, kw_only=True)
class _PreflightSentinel:
    """Resolved module-scope `Final[bool]` sentinel."""

    name: str
    literal_init: bool  # True when initializer is literal-only per B-v5-01
    line: int
    origin: Path  # source file where the sentinel was declared


def _is_final_bool_annotation(node: ast.expr | None) -> bool:
    if node is None:
        return False
    # Accept `Final[bool]`, `typing.Final[bool]`.
    if isinstance(node, ast.Subscript):
        value = node.value
        name = None
        if isinstance(value, ast.Name):
            name = value.id
        elif isinstance(value, ast.Attribute):
            name = value.attr
        if name == "Final":
            slc = node.slice
            if isinstance(slc, ast.Name) and slc.id == "bool":
                return True
    return False


def _sentinel_initializer_is_literal(node: ast.expr) -> bool:
    """B-v5-01: literal-only initializer — no Call / Attribute / Subscript."""
    for sub in ast.walk(node):
        if isinstance(sub, (ast.Call, ast.Subscript)):
            return False
        if isinstance(sub, ast.Attribute):
            return False
    # Leaves must be Constants or Names of builtin booleans.
    for sub in ast.walk(node):
        if isinstance(sub, ast.Name):
            if sub.id not in _PREFLIGHT_BUILTIN_BOOLS:
                return False
        elif isinstance(sub, ast.Constant):
            if not isinstance(sub.value, bool):
                # Allow bool constants only at leaves — anything else rejects.
                return False
    return True


def _find_module_sentinels(tree: ast.AST) -> dict[str, _PreflightSentinel]:
    """Locate every module-scope `Final[bool]` annotated assignment."""
    sentinels: dict[str, _PreflightSentinel] = {}
    if not isinstance(tree, ast.Module):
        return sentinels
    for node in tree.body:
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            if not _is_final_bool_annotation(node.annotation):
                continue
            name = node.target.id
            if node.value is None:
                continue
            literal = _sentinel_initializer_is_literal(node.value)
            sentinels[name] = _PreflightSentinel(
                name=name,
                literal_init=literal,
                line=node.lineno,
                origin=Path(""),
            )
    return sentinels


def _find_tree_root(path: Path) -> Path | None:
    """Walk upward from `path` to locate the workspace root containing a
    `pipeline/` directory.
    """
    for parent in path.parents:
        if (parent / "pipeline").is_dir():
            return parent
    return None


_R7_RESOLVE_SURFACES: tuple[str, ...] = (
    "pipeline.scout",
    "pipeline.section_02",
    "pipeline.loop",
    "pipeline.logician",
)


def _resolve_imported_sentinel(
    local_name: str, tree: ast.AST, path: Path
) -> _PreflightSentinel | None:
    """Resolve a locally imported name to its originating module's sentinel.

    Bounded to the Scout / Section 2 / loop / logician surfaces per B-v5-03.
    Any import outside the bounded surface returns ``None`` (fail-closed).
    """
    # Scan module-level ImportFrom nodes for the local name.
    if not isinstance(tree, ast.Module):
        return None
    for node in tree.body:
        if not isinstance(node, ast.ImportFrom):
            continue
        mod = node.module or ""
        for alias in node.names:
            local = alias.asname or alias.name
            if local != local_name:
                continue
            if not any(
                mod == s or mod.startswith(s + ".") for s in _R7_RESOLVE_SURFACES
            ):
                return None
            root = _find_tree_root(path)
            if root is None:
                return None
            target_path = root / Path(mod.replace(".", "/") + ".py")
            if not target_path.is_file():
                target_path = root / Path(mod.replace(".", "/")) / "__init__.py"
            if not target_path.is_file():
                return None
            try:
                src = target_path.read_text(encoding="utf-8")
                origin_tree = ast.parse(src, filename=str(target_path))
            except (OSError, SyntaxError, UnicodeDecodeError):
                return None
            origin_name = alias.name
            origin_sentinels = _find_module_sentinels(origin_tree)
            sentinel = origin_sentinels.get(origin_name)
            if sentinel is None:
                return None
            # Re-home the sentinel to record the origin file for diagnostics.
            return _PreflightSentinel(
                name=sentinel.name,
                literal_init=sentinel.literal_init,
                line=sentinel.line,
                origin=target_path,
            )
    return None


def _set_parent_links(tree: ast.AST) -> None:
    """Attach a ``_ast_parent`` link to each child node for upward walks."""
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            child._ast_parent = node  # type: ignore[attr-defined]


def _is_fd_broker_request_call(node: ast.Call) -> bool:
    # `fd_broker.request(...)` or `fd_broker.request_fd(...)`
    func = node.func
    if not isinstance(func, ast.Attribute):
        return False
    if func.attr not in {"request", "request_fd"}:
        return False
    base = func.value
    if isinstance(base, ast.Name) and base.id == "fd_broker":
        return True
    if isinstance(base, ast.Attribute) and base.attr == "fd_broker":
        return True
    return False


def _r7_target_section(path: Path) -> str | None:
    """R7 scope (blueprint §7.16 + A-v4-02).

    Targets preflight-dominance enforcement at the two surfaces where
    the blueprint names it explicitly:

    - ``pipeline/loop/**/*.py`` — M5/M14 router-integrity loop call
      sites that synthesize fd_broker.request via adapters.
    - ``pipeline/scout/channel_f_*.py`` — the websearch channel family
      whose fd_broker.request call path is blueprint-named in §7.16.

    Channel-A/-B/-C/-D/-E keep their own nonce-reserve-release discipline
    and are out of scope for R7 (blueprint §7.16 ✦ A-v4-02 narrowing).
    """
    parts = path.parent.parts
    if "pipeline" not in parts:
        return None
    if "loop" in parts:
        return "loop"
    if "scout" in parts and path.name.startswith("channel_f_"):
        return "scout"
    return None


@dataclass(frozen=True, kw_only=True)
class _R7GuardVerdict:
    dominated: bool
    sentinel_name: str | None
    reason_tag: str | None  # only set on non-dominated with a specific cause
    message_suffix: str = ""


def _r7_classify_test(
    test: ast.expr,
    sentinel_names: set[str],
) -> tuple[str | None, str | None]:
    """Return ``(sentinel_name, or_rejection_tag)`` for a guard test.

    - Bare `ast.Name(id=X)` where X ∈ sentinel_names → dominator.
    - `ast.BoolOp(op=And, values=[...])` → dominator if any leaf is a bare
      sentinel name (short-circuit admits first-position or any-position).
    - `ast.BoolOp(op=Or, values=[...])` with a sentinel anywhere → explicit
      short-circuit-OR rejection.
    - Anything else → no dominator.
    """
    if isinstance(test, ast.Name):
        if test.id in sentinel_names:
            return test.id, None
        return None, None
    if isinstance(test, ast.BoolOp):
        names_in_test = {
            v.id for v in test.values if isinstance(v, ast.Name)
        }
        matched = names_in_test & sentinel_names
        if isinstance(test.op, ast.And):
            if matched:
                return next(iter(matched)), None
            return None, None
        if isinstance(test.op, ast.Or):
            if matched:
                return None, "fd_request_preflight_short_circuit_or_bypass"
            return None, None
    return None, None


def _r7_find_guard(
    sink: ast.Call, sentinel_names: set[str]
) -> _R7GuardVerdict:
    """Walk upward from the sink, looking for an `if SENTINEL:` dominator."""
    cur: ast.AST | None = getattr(sink, "_ast_parent", None)
    child: ast.AST = sink
    while cur is not None:
        if isinstance(cur, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Module)):
            break
        if isinstance(cur, ast.If):
            # The sink dominates only if it's reached via `body`, not `orelse`.
            if child in cur.body or _is_descendant_of_list(child, cur.body):
                name, or_tag = _r7_classify_test(cur.test, sentinel_names)
                if name is not None:
                    return _R7GuardVerdict(
                        dominated=True,
                        sentinel_name=name,
                        reason_tag=None,
                    )
                if or_tag is not None:
                    return _R7GuardVerdict(
                        dominated=False,
                        sentinel_name=None,
                        reason_tag=or_tag,
                    )
        child = cur
        cur = getattr(cur, "_ast_parent", None)
    return _R7GuardVerdict(dominated=False, sentinel_name=None, reason_tag=None)


def _is_descendant_of_list(node: ast.AST, body: list) -> bool:
    # True if any element of body is node OR an ancestor of node.
    for element in body:
        if element is node:
            return True
        for sub in ast.walk(element):
            if sub is node:
                return True
    return False


def _check_ast_preflight_dominates_fd_request(
    tree: ast.AST, path: Path
) -> Iterator[Violation]:
    section = _r7_target_section(path)
    if section is None:
        return

    # Find every fd_broker.request sink.
    sinks: list[ast.Call] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and _is_fd_broker_request_call(node):
            sinks.append(node)
    if not sinks:
        return

    # Attach parent links so we can walk upward from the sink.
    _set_parent_links(tree)

    local_sentinels = _find_module_sentinels(tree)
    # Names resolvable as sentinels: locally-declared + importable.
    # We resolve imported names lazily when needed to avoid redundant I/O.
    sentinel_cache: dict[str, _PreflightSentinel | None] = dict(local_sentinels)

    def _resolve(name: str) -> _PreflightSentinel | None:
        if name in sentinel_cache:
            return sentinel_cache[name]
        resolved = _resolve_imported_sentinel(name, tree, path)
        sentinel_cache[name] = resolved
        return resolved

    # Collect candidate sentinel names from: local Finals + all top-level
    # ImportFrom targets bounded to known surfaces. This is the name-set the
    # CFG walker tests each `if` against.
    candidate_names: set[str] = set(local_sentinels.keys())
    if isinstance(tree, ast.Module):
        for node in tree.body:
            if isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    local = alias.asname or alias.name
                    candidate_names.add(local)

    for sink in sinks:
        verdict = _r7_find_guard(sink, candidate_names)

        # Explicit short-circuit-OR bypass: reject before the generic
        # "not dominated" path so the more-specific tag wins.
        if verdict.reason_tag == "fd_request_preflight_short_circuit_or_bypass":
            yield Violation(
                rule_name="AST_PREFLIGHT_DOMINATES_FD_REQUEST",
                reason_tag=verdict.reason_tag,
                file=path,
                line=sink.lineno,
                col=sink.col_offset,
                message=(
                    "fd_broker.request sink is guarded by a short-circuit "
                    "`or` — the fallback branch reaches the sink without "
                    "preflight; refactor to `and` or unconditional guard"
                ),
            )
            continue

        if not verdict.dominated:
            tag = f"{section}_fd_request_not_preflight_dominated"
            yield Violation(
                rule_name="AST_PREFLIGHT_DOMINATES_FD_REQUEST",
                reason_tag=tag,
                file=path,
                line=sink.lineno,
                col=sink.col_offset,
                message=(
                    "fd_broker.request sink is not CFG-dominated by a "
                    "module-scope `Final[bool]` preflight sentinel (§7.16)"
                ),
            )
            continue

        # Dominator found — verify sentinel is literal-init (B-v5-01) and,
        # if imported, resolvable against the bounded surface (B-v5-03).
        assert verdict.sentinel_name is not None
        sentinel = _resolve(verdict.sentinel_name)
        if sentinel is None:
            yield Violation(
                rule_name="AST_PREFLIGHT_DOMINATES_FD_REQUEST",
                reason_tag=f"{section}_fd_request_not_preflight_dominated",
                file=path,
                line=sink.lineno,
                col=sink.col_offset,
                message=(
                    f"guard sentinel {verdict.sentinel_name!r} could not be "
                    "resolved within the bounded module surface (B-v5-03)"
                ),
            )
            continue
        if not sentinel.literal_init:
            yield Violation(
                rule_name="AST_PREFLIGHT_DOMINATES_FD_REQUEST",
                reason_tag="fd_request_preflight_sentinel_non_literal",
                file=path,
                line=sink.lineno,
                col=sink.col_offset,
                message=(
                    f"guard sentinel {verdict.sentinel_name!r} has a "
                    "non-literal initializer (Call/Attribute/Subscript in "
                    "sub-tree) — B-v5-01 requires literal-only init"
                ),
            )
            continue



AST_PREFLIGHT_DOMINATES_FD_REQUEST = Rule(
    name="AST_PREFLIGHT_DOMINATES_FD_REQUEST",
    reason_tag="ast_preflight_dominates_fd_request",
    target_glob="pipeline/**/*.py",
    check=_check_ast_preflight_dominates_fd_request,
    description=(
        "Every fd_broker.request(...) sink under pipeline/loop/ or "
        "pipeline/scout/ must be CFG-dominated by an `if <SENTINEL>:` guard "
        "where <SENTINEL> is a module-scope Final[bool] with a literal-only "
        "initializer (B-v5-01). Cross-module sentinels resolved against the "
        "bounded Scout / Section 2 / loop / logician surface (B-v5-03). "
        "Short-circuit `and` admits; `or` rejects with a specific tag. "
        "Blueprint: section_03_scout.md §7.16, refinements A-v3-07, A-v4-02, "
        "B-v5-01, B-v5-03."
    ),
)

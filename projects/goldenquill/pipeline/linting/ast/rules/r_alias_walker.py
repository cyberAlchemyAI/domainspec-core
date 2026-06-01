from __future__ import annotations

import ast
from pathlib import Path
from typing import Iterator

from pipeline.linting._rule_types import Rule, Violation

_VAULT_PATH_PREFIXES: tuple[str, ...] = ("orgs/", "vault_shared/")
_LLM_PROVIDER_ROOTS: tuple[str, ...] = (
    "anthropic",
    "openai",
    "groq",
    "google.generativeai",
    "ollama",
)

def _is_banned_provider(module: str) -> bool:
    for root in _LLM_PROVIDER_ROOTS:
        if module == root or module.startswith(root + "."):
            return True
    return False

_OP_DECISION_ATTR = "operator_decision"
_DYNAMIC_EXEC_BUILTINS: frozenset[str] = frozenset({"eval", "exec", "compile"})

# ---------------------------------------------------------------------------
# R6 — AST_NO_INDIRECT_VAULT_READ — alias / attribute-chain / dynamic-import
# ---------------------------------------------------------------------------
#
# Closes the alias/attribute-chain/dynamic-import bypass class that R1/R3/R5
# intentionally admit under the v0.1 trusted-operator envelope. Blueprint
# anchors: section_03_scout.md §7.16, refinements A-v3-03 (base), A-v4-03
# (ImportFrom + rebinding alias tracking), B-v5-02 (termination guard).
#
# A single fixed-point alias walker over the whole module resolves local
# names to canonical handles:
#   builtin:<name>        — the Python builtin (`open`, `eval`, `setattr`, …)
#   module:<dotted>       — a module reference (`import pathlib as p`)
#   attr:<dotted>         — an attribute-path rooted in a module
#   obj:<dotted>          — an *instance* produced by `pathlib.Path(...)` call
#   literal:<value>       — a compile-time string literal
#
# Resolution is conservative: a name is treated as an alias only when we can
# statically prove the rhs token, otherwise `None`. The fixed-point loop is
# bounded by ``_MAX_ALIAS_WALKER_STEPS``; exhausting the cap raises
# ``AliasWalkerNonTerminationError`` so the module fails closed (B-v5-02).


_MAX_ALIAS_WALKER_STEPS: int = 1000

_R6_BUILTIN_SEEDS: tuple[str, ...] = (
    "open",
    "eval",
    "exec",
    "compile",
    "setattr",
    "getattr",
    "__import__",
)


class AliasWalkerNonTerminationError(Exception):
    """Alias walker exceeded the B-v5-02 decidability cap.

    Raised when the per-module fixed-point loop cannot reach a stable point
    within ``_MAX_ALIAS_WALKER_STEPS`` iterations. A module whose alias graph
    resists decidability within the cap is, by policy, not admissible.
    """


class _AliasResolver:
    """Per-module forward alias resolver (R6).

    Seeds builtins + imports, then iterates ``ast.Assign`` nodes to a fixed
    point. Attribute chains, ``getattr(obj, "name")`` with constant name,
    and ``pathlib.Path(...)`` instance construction are tracked.
    """

    def __init__(self, tree: ast.AST, *, max_steps: int = _MAX_ALIAS_WALKER_STEPS) -> None:
        self.bindings: dict[str, str] = {}
        self.steps: int = 0
        self.max_steps: int = max_steps
        self._seed(tree)
        self._iterate(tree)

    def _seed(self, tree: ast.AST) -> None:
        for b in _R6_BUILTIN_SEEDS:
            self.bindings[b] = f"builtin:{b}"
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.asname:
                        self.bindings[alias.asname] = f"module:{alias.name}"
                    else:
                        head = alias.name.split(".")[0]
                        self.bindings[head] = f"module:{head}"
            elif isinstance(node, ast.ImportFrom):
                mod = node.module or ""
                for alias in node.names:
                    local = alias.asname or alias.name
                    if mod:
                        self.bindings[local] = f"attr:{mod}.{alias.name}"
                    else:
                        self.bindings[local] = f"attr:{alias.name}"

    def _iterate(self, tree: ast.AST) -> None:
        """Fixed-point with *sticky-write* semantics — a name's first
        resolvable binding wins; reassignments do not overwrite. This is
        both conservative (any reassignment is assumed to preserve the
        alias for rule-check purposes — false-positive risk accepted under
        the trusted-operator envelope) and terminating: because bindings
        is monotonically extended each iteration, convergence is bounded
        by the number of assigns in the module. The explicit cap
        ``max_steps`` exists as a decidability backstop.
        """
        assigns = [
            n
            for n in ast.walk(tree)
            if isinstance(n, ast.Assign)
            and len(n.targets) == 1
            and isinstance(n.targets[0], ast.Name)
        ]
        changed = True
        while changed:
            self.steps += 1
            if self.steps > self.max_steps:
                raise AliasWalkerNonTerminationError(
                    f"alias walker exceeded {self.max_steps} iteration cap "
                    f"(B-v5-02); module is not admissible"
                )
            changed = False
            for node in assigns:
                target = node.targets[0]
                assert isinstance(target, ast.Name)
                if target.id in self.bindings:
                    continue  # sticky-write: first binding wins
                resolved = self.resolve(node.value)
                if resolved is None:
                    continue
                self.bindings[target.id] = resolved
                changed = True

    def resolve(self, node: ast.AST) -> str | None:
        if isinstance(node, ast.Name):
            return self.bindings.get(node.id)
        if isinstance(node, ast.Constant):
            if isinstance(node.value, str):
                return f"literal:{node.value}"
            return None
        if isinstance(node, ast.Attribute):
            base = self.resolve(node.value)
            if base is None:
                return None
            # `builtins.<name>` collapses to the builtin token when <name>
            # is a known builtin — the attribute form is equivalent to the
            # bare builtin for R6's purposes (A-v3-03 attribute-chain).
            if base == "module:builtins" and node.attr in (
                set(_R6_BUILTIN_SEEDS) | {"eval", "exec", "compile"}
            ):
                return f"builtin:{node.attr}"
            if base.startswith("module:"):
                return f"attr:{base[len('module:') :]}.{node.attr}"
            if base.startswith("attr:"):
                return f"attr:{base[len('attr:') :]}.{node.attr}"
            if base.startswith("obj:"):
                return f"attr:{base[len('obj:') :]}.{node.attr}"
            return None
        if isinstance(node, ast.Call):
            func_resolved = self.resolve(node.func)
            # `pathlib.Path(...)` returns an `obj:pathlib.Path` instance.
            if func_resolved == "attr:pathlib.Path":
                return "obj:pathlib.Path"
            # `getattr(obj, "name")` — resolve to obj.name if both resolvable.
            if func_resolved == "builtin:getattr" and len(node.args) >= 2:
                obj_resolved = self.resolve(node.args[0])
                name_arg = node.args[1]
                if not (isinstance(name_arg, ast.Constant) and isinstance(name_arg.value, str)):
                    return None
                attr_name = name_arg.value
                if isinstance(node.args[0], ast.Name) and node.args[0].id in {
                    "__builtins__",
                    "builtins",
                }:
                    if attr_name in _R6_BUILTIN_SEEDS or attr_name in {
                        "eval",
                        "exec",
                        "compile",
                    }:
                        return f"builtin:{attr_name}"
                if obj_resolved is None:
                    return None
                if obj_resolved.startswith("module:"):
                    return f"attr:{obj_resolved[len('module:') :]}.{attr_name}"
                if obj_resolved.startswith("attr:"):
                    return f"attr:{obj_resolved[len('attr:') :]}.{attr_name}"
            return None
        return None


def _r6_target_section(path: Path) -> str | None:
    parts = path.parent.parts
    # Map to the *innermost* matching section — loop/ wins over pipeline/.
    if "loop" in parts and "pipeline" in parts:
        return "loop"
    if "scout" in parts and "pipeline" in parts:
        return "scout"
    if "logician" in parts and "pipeline" in parts:
        return "logician"
    return None


def _r6_emit(
    path: Path, node: ast.AST, reason_tag: str, message: str
) -> Violation:
    return Violation(
        rule_name="AST_NO_INDIRECT_VAULT_READ",
        reason_tag=reason_tag,
        file=path,
        line=getattr(node, "lineno", 1),
        col=getattr(node, "col_offset", 0),
        message=message,
    )


def _r6_first_str_arg(call: ast.Call) -> str | None:
    if not call.args:
        return None
    first = call.args[0]
    if isinstance(first, ast.Constant) and isinstance(first.value, str):
        return first.value
    return None


def _check_ast_no_indirect_vault_read(
    tree: ast.AST, path: Path
) -> Iterator[Violation]:
    section = _r6_target_section(path)
    if section is None:
        return
    import sys
    mod = sys.modules.get("pipeline.linting.ast_lint")
    max_steps = getattr(mod, "_MAX_ALIAS_WALKER_STEPS", _MAX_ALIAS_WALKER_STEPS) if mod else _MAX_ALIAS_WALKER_STEPS

    try:
        resolver = _AliasResolver(tree, max_steps=max_steps)
    except AliasWalkerNonTerminationError:
        yield Violation(
            rule_name="AST_NO_INDIRECT_VAULT_READ",
            reason_tag="ast_alias_walker_overflow",
            file=path,
            line=1,
            col=0,
            message=(
                "alias walker exceeded decidability cap "
                f"({max_steps}) — module not admissible (B-v5-02)"
            ),
        )
        return

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue

        func_resolved = resolver.resolve(node.func)

        # ------------------------------------------------------------------
        # Logician: indirect vault_read via alias / attribute / Path chain
        # ------------------------------------------------------------------
        if section == "logician":
            vault_literal: str | None = None
            # (a) Direct rebound / attribute-form `open(...)` call with literal path.
            if func_resolved == "builtin:open":
                vault_literal = _r6_first_str_arg(node)
                # Skip the R3 case where the func is a bare ast.Name("open") —
                # that shape is already caught by R3 and would double-emit here.
                if isinstance(node.func, ast.Name) and node.func.id == "open":
                    vault_literal = None
            # (b) `Path("orgs/...").open(...)` — call on the attribute of a Path-instance.
            elif (
                isinstance(node.func, ast.Attribute)
                and node.func.attr == "open"
                and isinstance(node.func.value, ast.Call)
            ):
                inner = node.func.value
                inner_func = resolver.resolve(inner.func)
                if inner_func == "attr:pathlib.Path":
                    vault_literal = _r6_first_str_arg(inner)

            if vault_literal is not None and any(
                vault_literal.startswith(p) for p in _VAULT_PATH_PREFIXES
            ):
                yield _r6_emit(
                    path,
                    node,
                    "logician_indirect_vault_read_via_alias",
                    (
                        f"indirect open of vault path {vault_literal!r} via "
                        "alias / attribute chain — route via vault broker"
                    ),
                )
                continue

            # (c) Dynamic import of an LLM provider:
            #     importlib.import_module("<provider>") / __import__("<provider>")
            if func_resolved in {
                "attr:importlib.import_module",
                "builtin:__import__",
            }:
                mod_literal = _r6_first_str_arg(node)
                if mod_literal is not None and _is_banned_provider(mod_literal):
                    yield _r6_emit(
                        path,
                        node,
                        "logician_indirect_llm_client_via_alias",
                        (
                            f"indirect LLM-client import of {mod_literal!r} via "
                            "dynamic import — forbidden under §7.4"
                        ),
                    )
                    continue

        # ------------------------------------------------------------------
        # Scout: indirect dynamic code / indirect operator_decision write
        # ------------------------------------------------------------------
        if section == "scout":
            # (a) Rebound / attribute-form / getattr-resolved eval/exec/compile.
            if func_resolved in {
                "builtin:eval",
                "builtin:exec",
                "builtin:compile",
            }:
                # Skip the R5 case where the func is a bare ast.Name matching
                # the builtin — R5 already catches that shape.
                if not (
                    isinstance(node.func, ast.Name)
                    and node.func.id in _DYNAMIC_EXEC_BUILTINS
                ):
                    yield _r6_emit(
                        path,
                        node,
                        "scout_indirect_dynamic_code_via_alias",
                        (
                            f"indirect {func_resolved[len('builtin:') :]}() "
                            "call via alias / attribute chain — forbidden "
                            "under §7.16"
                        ),
                    )
                    continue

            # (b) Dynamic setattr with literal-aliased "operator_decision".
            if path.name != "review_stage.py" and func_resolved == "builtin:setattr":
                if len(node.args) >= 2:
                    name_arg = node.args[1]
                    resolved_name = resolver.resolve(name_arg)
                    if (
                        isinstance(name_arg, ast.Name)
                        and resolved_name == f"literal:{_OP_DECISION_ATTR}"
                    ):
                        yield _r6_emit(
                            path,
                            node,
                            "scout_indirect_operator_decision_write_via_alias",
                            (
                                "indirect setattr of 'operator_decision' via "
                                "aliased literal — only review_stage.py may "
                                "write operator_decision"
                            ),
                        )
                        continue

        # ------------------------------------------------------------------
        # Loop: indirect logician-internal access via package-alias chain
        # ------------------------------------------------------------------
        if section == "loop":
            # `import pipeline.logician as L; L.cedar_eval.evaluate(...)`
            #  → func_resolved becomes "attr:pipeline.logician.cedar_eval.evaluate"
            if (
                func_resolved is not None
                and func_resolved.startswith("attr:pipeline.logician.")
            ):
                # Public surface is `attr:pipeline.logician.<symbol>` with a
                # single trailing segment; internal access is two-or-more.
                tail = func_resolved[len("attr:pipeline.logician.") :]
                if "." in tail:
                    yield _r6_emit(
                        path,
                        node,
                        "loop_indirect_logician_internal_via_alias",
                        (
                            "indirect access to pipeline.logician internals "
                            "via package-level attribute chain "
                            f"({func_resolved[len('attr:') :]}) — use the "
                            "public pipeline.logician API"
                        ),
                    )
                    continue



AST_NO_INDIRECT_VAULT_READ = Rule(
    name="AST_NO_INDIRECT_VAULT_READ",
    reason_tag="ast_no_indirect_vault_read",
    target_glob="pipeline/**/*.py",
    check=_check_ast_no_indirect_vault_read,
    description=(
        "Closes alias / attribute-chain / dynamic-import bypasses of R1/R3/R5. "
        "A single fixed-point alias walker (cap _MAX_ALIAS_WALKER_STEPS per "
        "B-v5-02) resolves local names to canonical handles and rejects "
        "indirect vault opens, dynamic LLM-client imports, indirect "
        "operator_decision setattr, indirect eval/exec/compile, and "
        "attribute-chain access into pipeline.logician internals. "
        "Blueprint: section_03_scout.md §7.16, refinements A-v3-03, A-v4-03, "
        "B-v5-02."
    ),
)

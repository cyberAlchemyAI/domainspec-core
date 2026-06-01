"""R-ARCHIVIST-NO-CANONICAL-MUTATE — low-level rename primitives extension.

§4 v2.x.1 corrective amendment (Cycle-1 closures applied 2026-05-10) —
closes Tilth-RT-07 PARTIAL by extending the
R-ARCHIVIST-NO-CANONICAL-MUTATE predicate body in
``pipeline/linting/ast_lint.py`` with six low-level rename primitives
(five from disposition packet §3.1 + ``os.renames`` per Cycle-1 Red
Team RT-09 fold-in).

Spec card: ``pipeline/blueprint/v0.1/section_15_archivist.md`` §15.9.3
(R-ARCHIVIST-NO-CANONICAL-MUTATE — Archivist seat may NOT mutate
canonical substrate state by any direct write-intent call, by
subprocess-of-canonical-CLI, by foreign-helper file-write import, OR
— per this corrective — by low-level rename primitive that atomically
overwrites a forbidden canonical path with content prepared in an
allowed-prefix tempfile).

Forbidden-call enumeration (this rule):

==========================================================  =======================================
Primitive                                                   Sub-tag (reason_tag)
==========================================================  =======================================
``os.replace(src, dst)``                                    ``archivist_auto_apply_attempted.low_level_rename_replace``
``os.rename(src, dst)``                                     ``archivist_auto_apply_attempted.low_level_rename_rename``
``os.renames(src, dst)``                                    ``archivist_auto_apply_attempted.low_level_rename_renames``
``shutil.move(src, dst)``                                   ``archivist_auto_apply_attempted.low_level_rename_shutil_move``
``shutil.copy(src, dst)``  /  ``shutil.copy2(src, dst)``    ``archivist_auto_apply_attempted.low_level_rename_shutil_copy``
``shutil.copyfile(src, dst)`` / ``shutil.copytree(src,dst)``
``os.link(src, dst)`` / ``os.symlink(src, dst)``            ``archivist_auto_apply_attempted.low_level_rename_os_link``
==========================================================  =======================================

Every fire emits failure code ``F-ARCHIVIST-AUTO-APPLY-ATTEMPTED``
(carried in the ``Violation.message`` body so the failure-code
attribution travels with the diagnostic).

Threat model.  Under v7 LOCKED A1 + A4 (single-client + operator-trusted
preflight) the residual exploit is contributor-discipline-shaped: a
contributor writing Archivist seat code might prepare a tempfile inside
an allowed-prefix path (``orgs/<slug>/archivist_digests/.tmp``) and
then atomically rename it over a forbidden canonical path
(``orgs/<slug>/vault/kfr/register.yaml``).  AST-lint enumeration is
the compile-time defense; the runtime-guard wrapper extension at
§15.9.3 line 521 (lands at §15 v1.x first ship) is the runtime
defense; the single source of truth for the forbidden-call set is THIS
module (per §4 v2.x.1 amendment §3.3).

Static-analysis limitations (intentionally out-of-scope under
v7 LOCKED A4).  The resolver is conservative.  Dynamic-call shapes are
NOT tracked: ``getattr(os, 'replace')(...)``, ``os.__dict__['replace']
(...)``, ``_x = os.replace; _x(...)``, ``sys.modules['os'].replace
(...)``, ``from os import *``, and Path-method equivalents
(``pathlib.Path(src).rename(dst)``) all evade the AST-lint enumeration.
These are documented as bounded-by-A1+A4 in the §4 v2.x.1 amendment §8
threat-model framing and §11 deferred-dispositions register.  Promotion
to MED severity is bound to v2 multi-tenant context via Section O.5
per the row-170 transparent-disposition pattern (v7.0.4-M1 + WS-D
v7.0.5 + WS-B v7.0.7 + §15 v1 + WS-L §4 v2.x precedents).

Pure-Python; runs as part of :data:`pipeline.linting.ast_lint.DEFAULT_RULES`.
"""

from __future__ import annotations

import ast
from pathlib import Path
from types import MappingProxyType
from typing import Iterator, Mapping

from pipeline.linting._rule_types import Rule, Violation

# ---------------------------------------------------------------------------
# Target glob — Archivist seat package only.
# Mirrors the runtime guard wrapper scope at §15.9.3 (Archivist seat module
# imports the wrapper at module load); cross-section drift here is itself a
# §15.9.3 violation (foreign-file-write-helper import + foreign-seat-module
# import).  The rule is therefore narrowly scoped to the Archivist tree.
# ---------------------------------------------------------------------------

_ARCHIVIST_TARGET_GLOB = "pipeline/orchestrator/seats/archivist/**/*.py"

# Failure code attribution — carried in the Violation.message body so the
# failure-code attribution travels with the diagnostic regardless of the
# (deliberately narrow) reason_tag.
_FAILURE_CODE = "F-ARCHIVIST-AUTO-APPLY-ATTEMPTED"

# ---------------------------------------------------------------------------
# Forbidden-primitive table.  The mapping is (module_name, attr_name) →
# sub-tag.  Module name is the canonical dotted import path; the resolver
# walks Attribute chains and ImportFrom rebinds to match either form.
# ---------------------------------------------------------------------------

# (module_dotted_path, attribute_name) → sub-tag (without the leading dot —
# the dot is added at emit time so the disposition-packet acceptance form
# ``".low_level_rename_replace" in result.sub_tags`` matches the wire
# representation in the reason_tag).
_FORBIDDEN_PRIMITIVES: dict[tuple[str, str], str] = {
    ("os", "replace"): "low_level_rename_replace",
    ("os", "rename"): "low_level_rename_rename",
    # os.renames is the recursive-rename wrapper; same shape as os.rename
    # for atomic-substrate purposes (Cycle-1 RT-09 fold-in).
    ("os", "renames"): "low_level_rename_renames",
    ("shutil", "move"): "low_level_rename_shutil_move",
    # shutil.copy family — all four primitives collapse to the same sub-tag
    # because the §4 v2.x.1 disposition packet groups them under a single
    # sub-tag (".low_level_rename_shutil_copy").
    ("shutil", "copy"): "low_level_rename_shutil_copy",
    ("shutil", "copy2"): "low_level_rename_shutil_copy",
    ("shutil", "copyfile"): "low_level_rename_shutil_copy",
    ("shutil", "copytree"): "low_level_rename_shutil_copy",
    # os.link / os.symlink — same sub-tag per disposition packet.
    ("os", "link"): "low_level_rename_os_link",
    ("os", "symlink"): "low_level_rename_os_link",
}


def _collect_imports(tree: ast.AST) -> dict[str, str]:
    """Map every local name to its canonical module identity.

    Returns a dict from local-binding-name → canonical module dotted path,
    covering both ``import os`` (``os`` → ``"os"``), ``import os as o``
    (``o`` → ``"os"``), and ``from os import replace as r`` (``r`` →
    ``"os.replace"``).  Walks the *whole* tree (not just module-top-level)
    so function-scoped imports are also caught.

    The mapping is one-way: a local name → its origin.  Subsequent rebinds
    of the same name to a non-module value are not tracked (the rule is
    conservative under v7 LOCKED A4 operator-trusted-preflight envelope).
    """
    out: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                local = alias.asname or alias.name.split(".")[0]
                # Bind the head of the dotted path; ``import os.path``
                # rebinds ``os`` to ``os`` (and downstream resolution
                # walks the Attribute chain).
                if alias.asname:
                    out[local] = alias.name
                else:
                    out[local] = local
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            for alias in node.names:
                local = alias.asname or alias.name
                if mod:
                    out[local] = f"{mod}.{alias.name}"
                else:
                    out[local] = alias.name
    return out


def _resolve_callable_to_module_attr(
    func: ast.AST, imports: dict[str, str]
) -> tuple[str, str] | None:
    """Resolve a Call.func to a (module, attr) pair if possible.

    Two shapes handled (matching the forbidden primitives):

    1. ``ast.Attribute(value=ast.Name('os'), attr='replace')`` — the
       canonical ``os.replace(...)`` call shape.  We resolve ``os`` to
       its canonical module via the imports table.
    2. ``ast.Name('replace')`` — happens when the function was imported
       via ``from os import replace``.  The imports table maps the local
       name to ``"os.replace"`` and we split on the last dot.

    Returns ``None`` if the callable cannot be statically resolved to a
    (module, attr) pair on the forbidden list.
    """
    # Shape (1): Attribute on Name — direct module.method call.
    if isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name):
        local = func.value.id
        canonical = imports.get(local)
        if canonical is None:
            return None
        return (canonical, func.attr)
    # Shape (2): bare Name resolved through `from ... import` rebind.
    if isinstance(func, ast.Name):
        canonical_full = imports.get(func.id)
        if canonical_full is None or "." not in canonical_full:
            return None
        mod, _, attr = canonical_full.rpartition(".")
        return (mod, attr)
    return None


def _check_archivist_no_canonical_mutate(
    tree: ast.AST, path: Path
) -> Iterator[Violation]:
    """Emit a Violation for every Call to a forbidden low-level rename primitive."""
    imports = _collect_imports(tree)
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        resolved = _resolve_callable_to_module_attr(node.func, imports)
        if resolved is None:
            continue
        sub_tag = _FORBIDDEN_PRIMITIVES.get(resolved)
        if sub_tag is None:
            continue
        mod, attr = resolved
        yield Violation(
            rule_name="R-ARCHIVIST-NO-CANONICAL-MUTATE",
            # reason_tag carries the leading dot so the acceptance assertion
            # ``".low_level_rename_replace" in result.sub_tags`` (per the
            # §4 v2.x.1 disposition packet stub) matches the wire form.
            reason_tag=f"archivist_auto_apply_attempted.{sub_tag}",
            file=path,
            line=node.lineno,
            col=node.col_offset,
            message=(
                f"{_FAILURE_CODE}: {mod}.{attr}(...) is a forbidden "
                "low-level rename primitive in Archivist seat code; "
                "the Archivist proposes-only contract forbids any "
                "atomic-rename / file-copy / hard-link / symlink primitive "
                "regardless of source-path prefix because the destination "
                "argument can resolve to a canonical-substrate path at "
                "runtime (per §15.9.3 + §4 v2.x.1 corrective)"
            ),
        )


ARCHIVIST_NO_CANONICAL_MUTATE: Rule = Rule(
    name="R-ARCHIVIST-NO-CANONICAL-MUTATE",
    reason_tag="archivist_no_canonical_mutate",
    target_glob=_ARCHIVIST_TARGET_GLOB,
    check=_check_archivist_no_canonical_mutate,
    description=(
        "Forbid low-level rename primitives in "
        "pipeline/orchestrator/seats/archivist/**.  Six primitives + "
        "shutil.copy fan-out collapse to six sub-tags under the "
        "F-ARCHIVIST-AUTO-APPLY-ATTEMPTED failure code: os.replace, "
        "os.rename, os.renames, shutil.move, "
        "shutil.copy/copy2/copyfile/copytree, os.link/os.symlink.  "
        "Closes Tilth-RT-07 PARTIAL via §4 v2.x.1 corrective amendment "
        "2026-05-10 (Cycle-1 RT-09 + RT-14 + RT-15 fold-ins applied); "
        "runtime-guard wrapper extension for os.replace/os.rename/"
        "shutil.move lands at §15.9.3 line 521 v1.x first ship (single "
        "source of truth for the forbidden-call set is this module's "
        "MappingProxyType-wrapped FORBIDDEN_PRIMITIVES export)."
    ),
)


# Public surface — exported by name from ast_lint via the _wsl_slice4
# pattern (or equivalent lazy-import block in ast_lint.py's DEFAULT_RULES
# extension hook).
#
# Cycle-1 RT-14 fold-in: the re-exported public view is wrapped in
# ``MappingProxyType`` so that downstream consumers cannot accidentally
# (or maliciously) mutate the forbidden-primitive table at runtime to
# silence the rule.  Attempts to write to ``FORBIDDEN_PRIMITIVES[key]``
# raise ``TypeError`` deterministically.  The internal mutable source
# of truth remains ``_FORBIDDEN_PRIMITIVES`` (module-private).
FORBIDDEN_PRIMITIVES: Mapping[tuple[str, str], str] = MappingProxyType(
    _FORBIDDEN_PRIMITIVES
)

__all__ = [
    "ARCHIVIST_NO_CANONICAL_MUTATE",
    "FORBIDDEN_PRIMITIVES",
]

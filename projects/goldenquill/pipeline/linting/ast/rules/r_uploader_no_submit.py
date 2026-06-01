from __future__ import annotations

import ast
from pathlib import Path
from typing import Iterator

from pipeline.linting._rule_types import Rule, Violation
from pipeline.linting.ast.runner import _glob_matches_path
from pipeline.linting.ast.rules.r_alias_walker import _AliasResolver, _MAX_ALIAS_WALKER_STEPS, AliasWalkerNonTerminationError

# ---------------------------------------------------------------------------
# R-UPLOADER-NO-SUBMIT — allow-listed callable-name discipline
# ---------------------------------------------------------------------------
#
# The Uploader is "prepare-and-stage discipline only — operator clicks final
# submit on funder portal" (architecture v7.0.6). Auto-submit is
# architecturally prohibited; F-UPLOADER-AUTOSUBMIT-ATTEMPTED is one of the
# three layers of defense.
#
# A regex blocklist of HTTP method names (httpx.post / requests.put / …) is
# trivially defeated by aliasing or alternative client libraries. Instead,
# this rule operates from an ALLOW-LIST: every ``ast.Call`` under
# ``pipeline/orchestrator/seats/uploader.py`` and
# ``pipeline/orchestrator/seats/uploader_adapters/`` must resolve to a
# callable name on the allow-list. Anything else is a R-UPLOADER-NO-SUBMIT
# violation.
#
# The allow-list is conservative — it covers what the Uploader and its seven
# adapters demonstrably need (file I/O, hashing, datetime, dataclass
# primitives, document-parsing libraries, regex, internal Tilth modules)
# and explicitly admits ``subprocess.run`` for the LibreOffice headless
# conversion path only.

_UPLOADER_TARGET_GLOBS: tuple[str, ...] = (
    "pipeline/orchestrator/seats/uploader.py",
    "pipeline/orchestrator/seats/uploader_adapters/*.py",
)


# Allow-list of callable-resolution tokens (per the R6 _AliasResolver alphabet:
# "builtin:<name>", "module:<dotted>", "attr:<dotted-prefix>"). Any callable
# that resolves to a token on this list is admitted. Anything else fires
# R-UPLOADER-NO-SUBMIT.
#
# The list is intentionally conservative; extend as the Uploader and its
# adapters land real implementations and need additional callables.
UPLOADER_ALLOW_LIST: frozenset[str] = frozenset({
    # ------------------------------------------------------------------
    # Builtins (Python core; no I/O, no networking)
    # ------------------------------------------------------------------
    "builtin:str", "builtin:int", "builtin:float", "builtin:bool",
    "builtin:list", "builtin:tuple", "builtin:dict", "builtin:set",
    "builtin:frozenset", "builtin:bytes", "builtin:bytearray",
    "builtin:print", "builtin:len", "builtin:range", "builtin:enumerate",
    "builtin:zip", "builtin:sorted", "builtin:reversed", "builtin:min",
    "builtin:max", "builtin:sum", "builtin:any", "builtin:all",
    "builtin:isinstance", "builtin:issubclass", "builtin:hasattr",
    "builtin:getattr", "builtin:setattr", "builtin:repr", "builtin:hash",
    "builtin:id", "builtin:type", "builtin:object", "builtin:iter",
    "builtin:next", "builtin:abs", "builtin:round", "builtin:divmod",
    "builtin:open",  # local file I/O permitted; vault I/O is policy-gated
    "builtin:format", "builtin:vars", "builtin:locals", "builtin:globals",
    "builtin:callable", "builtin:property", "builtin:staticmethod",
    "builtin:classmethod", "builtin:super", "builtin:slice",
    "builtin:NotImplementedError", "builtin:ValueError", "builtin:TypeError",
    "builtin:KeyError", "builtin:RuntimeError", "builtin:OSError",
    "builtin:FileNotFoundError", "builtin:IOError", "builtin:Exception",
    # ------------------------------------------------------------------
    # Standard library — file / data primitives
    # ------------------------------------------------------------------
    "module:hashlib",
    "attr:hashlib.sha3_512", "attr:hashlib.sha256", "attr:hashlib.sha512",
    "attr:hashlib.md5", "attr:hashlib.new",
    "module:datetime", "module:timezone",
    "attr:datetime.datetime", "attr:datetime.date", "attr:datetime.time",
    "attr:datetime.timedelta", "attr:datetime.timezone", "attr:datetime.UTC",
    "attr:datetime.datetime.now", "attr:datetime.datetime.utcnow",
    "attr:datetime.datetime.fromisoformat",
    "module:pathlib",
    "attr:pathlib.Path", "attr:pathlib.PurePath",
    "module:os", "module:os.path",
    "attr:os.path.join", "attr:os.path.exists", "attr:os.path.isfile",
    "attr:os.path.isdir", "attr:os.path.dirname", "attr:os.path.basename",
    "attr:os.path.splitext", "attr:os.path.abspath", "attr:os.path.relpath",
    "attr:os.path.normpath",
    "attr:os.makedirs", "attr:os.fspath", "attr:os.environ",
    "module:json",
    "attr:json.dump", "attr:json.dumps", "attr:json.load", "attr:json.loads",
    "module:yaml",
    "attr:yaml.safe_load", "attr:yaml.safe_dump",
    "module:re",
    "attr:re.compile", "attr:re.match", "attr:re.search", "attr:re.sub",
    "attr:re.findall", "attr:re.split",
    "module:base64",
    "attr:base64.b64encode", "attr:base64.b64decode",
    "module:uuid",
    "attr:uuid.uuid4", "attr:uuid.uuid5",
    # ------------------------------------------------------------------
    # Standard library — typing / dataclass / abc / functools / itertools
    # ------------------------------------------------------------------
    "module:typing",
    "attr:typing.cast", "attr:typing.get_type_hints",
    "attr:typing.runtime_checkable",
    "module:dataclasses",
    "attr:dataclasses.dataclass", "attr:dataclasses.field",
    "attr:dataclasses.replace", "attr:dataclasses.asdict",
    "attr:dataclasses.astuple", "attr:dataclasses.is_dataclass",
    "attr:dataclasses.fields", "attr:dataclasses.MISSING",
    "module:abc",
    "attr:abc.abstractmethod", "attr:abc.ABC",
    "module:functools",
    "attr:functools.lru_cache", "attr:functools.cache",
    "attr:functools.partial", "attr:functools.reduce", "attr:functools.wraps",
    "module:itertools",
    "attr:itertools.chain", "attr:itertools.product", "attr:itertools.groupby",
    "attr:itertools.islice", "attr:itertools.tee", "attr:itertools.cycle",
    "module:collections",
    "attr:collections.OrderedDict", "attr:collections.defaultdict",
    "attr:collections.Counter", "attr:collections.namedtuple",
    "attr:collections.deque",
    "module:collections.abc",
    "module:contextlib",
    "attr:contextlib.contextmanager", "attr:contextlib.suppress",
    "attr:contextlib.closing",
    "module:copy",
    "attr:copy.copy", "attr:copy.deepcopy",
    "module:enum",
    "attr:enum.Enum", "attr:enum.IntEnum", "attr:enum.auto",
    # ------------------------------------------------------------------
    # Document-parsing libraries (per ADR-001 substrate; wrapped as
    # Pydantic AI tools — but the names appear in the AST)
    # ------------------------------------------------------------------
    "module:docx",
    "attr:docx.Document",
    "attr:docx.shared",
    "module:pypdf",
    "attr:pypdf.PdfReader", "attr:pypdf.PdfWriter",
    "module:openpyxl",
    "attr:openpyxl.load_workbook", "attr:openpyxl.Workbook",
    # ------------------------------------------------------------------
    # subprocess — admitted EXCLUSIVELY for LibreOffice headless conversion.
    # The runtime callsite must pass `check=True` and reference `soffice`
    # or `libreoffice` in argv[0]. The allow-list admits the call shape;
    # static analysis cannot prove argv-binding semantics, so the discipline
    # rests on code review for any subprocess.run callsite.
    # ------------------------------------------------------------------
    "module:subprocess",
    "attr:subprocess.run",
    "attr:subprocess.CalledProcessError",
    # ------------------------------------------------------------------
    # Tilth-internal modules — pipeline.* is fully trusted
    # ------------------------------------------------------------------
    # We admit by prefix match (see _is_uploader_allowed); this entry is
    # informational and not consulted directly.
})


# Module-name prefixes that admit any callable resolving under them
# (pipeline.* covers every Tilth-internal module without enumerating
# specific symbols).
_UPLOADER_ALLOW_PREFIXES: tuple[str, ...] = (
    "module:pipeline",
    "attr:pipeline.",
    # Self-references resolved during analysis
    "module:pipeline.orchestrator",
    "attr:pipeline.orchestrator.",
)


def _is_uploader_allowed(token: str | None) -> bool:
    """Return True iff a resolved-callable token is on the Uploader allow-list."""
    if token is None:
        # Unresolvable callable — fail-closed. We cannot prove it isn't a
        # submission API. The AST-lint sandbox's job is to reject ambiguity.
        return False
    if token in UPLOADER_ALLOW_LIST:
        return True
    for prefix in _UPLOADER_ALLOW_PREFIXES:
        if token == prefix or token.startswith(prefix):
            return True
    return False


# Python builtins that the alias resolver doesn't seed (it seeds only the
# bypass-relevant set). For R-UPLOADER-NO-SUBMIT, we treat a much broader
# set of bare-name builtin calls as implicitly admitted because they have
# no networking / submission semantics. This list is conservative — names
# here are pure-Python primitives.
_UPLOADER_BARE_BUILTIN_ADMITS: frozenset[str] = frozenset({
    "any", "all", "len", "min", "max", "sum", "abs", "round", "divmod",
    "sorted", "reversed", "enumerate", "zip", "map", "filter", "iter",
    "next", "range", "list", "tuple", "dict", "set", "frozenset",
    "bytes", "bytearray", "str", "int", "float", "bool", "complex",
    "print", "repr", "hash", "id", "type", "object", "isinstance",
    "issubclass", "hasattr", "getattr", "setattr", "delattr", "callable",
    "format", "vars", "locals", "globals", "dir", "ascii", "bin", "hex",
    "oct", "chr", "ord", "pow", "input", "memoryview", "slice", "super",
    "property", "staticmethod", "classmethod",
    # Common exception constructors used in scaffold / runtime checks
    "Exception", "ValueError", "TypeError", "KeyError", "IndexError",
    "RuntimeError", "OSError", "FileNotFoundError", "IOError",
    "NotImplementedError", "StopIteration", "AttributeError",
    "ArithmeticError", "AssertionError", "ImportError", "LookupError",
    "NameError", "OverflowError", "PermissionError", "ZeroDivisionError",
    "UnicodeError", "UnicodeDecodeError", "UnicodeEncodeError",
})


def _check_uploader_no_submit(
    tree: ast.AST, path: Path
) -> Iterator[Violation]:
    """Allow-list every ``ast.Call`` in the Uploader / adapters tree.

    Any call whose resolved callable is not on the allow-list is reported
    as R-UPLOADER-NO-SUBMIT. Aliased imports (`from httpx import post as
    p; p(...)`) collapse via the shared _AliasResolver to a token like
    ``attr:httpx.post`` which is not on the allow-list, so the rule fires.

    Admit policy (in order):
      1. Resolved token is on the UPLOADER_ALLOW_LIST or under an allowed
         module prefix (pipeline.*).
      2. Bare-name call to a Python builtin in
         _UPLOADER_BARE_BUILTIN_ADMITS — pure-Python primitives with no
         networking / submission semantics.
      3. Method call on `self.<chain>` or `cls.<chain>` — admitted because
         dataclass methods and instance methods are project-internal by
         construction.
      4. Bare-name call to a name defined locally in this module (def,
         class, assign, import) — admitted as a project-internal symbol.
      5. Method call on a value that the resolver maps to a callable on
         the allow-list (e.g. ``hashlib.sha3_512(x).hexdigest()`` — the
         outer call's func is ``Attribute(value=Call(...), attr='hexdigest')``;
         the inner call's func resolves to ``attr:hashlib.sha3_512`` which
         is allow-listed, so the chained method call is admitted).
      6. Method call on a Name that resolves to a Tilth-internal module
         or attribute — same logic as (1) but applied to the Attribute root.
    """
    try:
        resolver = _AliasResolver(tree, max_steps=_MAX_ALIAS_WALKER_STEPS)
    except AliasWalkerNonTerminationError:
        yield Violation(
            rule_name="R_UPLOADER_NO_SUBMIT",
            reason_tag="uploader_alias_walker_overflow",
            file=path,
            line=1,
            col=0,
            message=(
                "alias walker exceeded decidability cap "
                f"({_MAX_ALIAS_WALKER_STEPS}) — module not admissible"
            ),
        )
        return

    local_names = _collect_local_names(tree)
    imported_names = _collect_imported_names(tree)
    # Locally-assigned names are local_names minus import bindings. Imports
    # populate ``local_names`` so the alias resolver can chase them, but for
    # admit rules (4)/(7) — which trust runtime-value identity — we must NOT
    # treat import bindings as locally-assigned. An imported callable like
    # ``import httpx; httpx.post(...)`` would otherwise be admitted via (7)
    # because ``httpx`` is in ``local_names``. Imports must resolve through
    # the explicit allow-list (rule 1/6), never the locality fallback.
    assigned_names = local_names - imported_names

    def _attr_root(node: ast.AST) -> ast.AST:
        cur = node
        while isinstance(cur, ast.Attribute):
            cur = cur.value
        return cur

    def _admit(func: ast.AST) -> bool:
        token = resolver.resolve(func)
        # (1) Direct allow-list hit (module, attr, obj, builtin token).
        if _is_uploader_allowed(token):
            return True
        # (2) Bare-name builtin admit list.
        if isinstance(func, ast.Name) and func.id in _UPLOADER_BARE_BUILTIN_ADMITS:
            return True
        # (3) Method call rooted at self/cls.
        if isinstance(func, ast.Attribute):
            root = _attr_root(func)
            if isinstance(root, ast.Name) and root.id in {"self", "cls"}:
                return True
        # (4) Bare-name call to a name *assigned locally* in this module
        #     (def, class, assign, for, with, args). Excludes imports —
        #     imports must resolve via the explicit allow-list.
        if isinstance(func, ast.Name) and func.id in assigned_names:
            return True
        # (5) Method call whose receiver is itself an allow-listed call.
        #     E.g. ``hashlib.sha3_512(x).hexdigest()`` — the outer
        #     Attribute.value is the inner Call. Recursively admit.
        if isinstance(func, ast.Attribute):
            recv = func.value
            if isinstance(recv, ast.Call):
                if _admit(recv.func):
                    return True
            # (6) Method call on a Name that resolves to an allow-listed
            #     module/attr token (e.g. ``manifest.entries`` chains).
            recv_token = resolver.resolve(recv)
            if recv_token is not None and _is_uploader_allowed(recv_token):
                return True
            # (7) Method call on Name bound by local *assignment* — admit
            #     (it's a runtime value whose type we can't statically prove,
            #     but we admit local-bound variables under the trusted-
            #     operator envelope). Imports are explicitly NOT admitted
            #     here; they must reach the explicit allow-list.
            if isinstance(recv, ast.Name) and recv.id in assigned_names:
                return True
            # (8) Method call on a Subscript / Tuple / List / Dict literal
            #     (e.g. ``[x, y][0].method()``, ``{}.get(...)``) — admit.
            if isinstance(recv, (ast.Subscript, ast.Tuple, ast.List, ast.Dict, ast.Set)):
                return True
            # (9) Method call rooted at a Constant (e.g. ``"x".strip()``) — admit.
            root = _attr_root(func)
            if isinstance(root, ast.Constant):
                return True
        # Lambda invocation, walrus expression, etc. — admit.
        if isinstance(func, (ast.Lambda, ast.NamedExpr, ast.IfExp)):
            return True
        return False

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if _admit(node.func):
            continue
        token = resolver.resolve(node.func)
        yield Violation(
            rule_name="R_UPLOADER_NO_SUBMIT",
            reason_tag="uploader_call_outside_allow_list",
            file=path,
            line=node.lineno,
            col=node.col_offset,
            message=(
                f"R-UPLOADER-NO-SUBMIT: callable {token!r} is not on the "
                "Uploader allow-list — extend UPLOADER_ALLOW_LIST in "
                "pipeline/linting/ast_lint.py if this is a legitimate "
                "Uploader / adapter dependency"
            ),
        )


def _collect_imported_names(tree: ast.AST) -> set[str]:
    """Names introduced by import / from-import statements — module-scoped.

    Used by R-UPLOADER-NO-SUBMIT to discriminate import-bound names from
    locally-assigned ones. Imported names must reach the explicit allow-list;
    they cannot be admitted via the locality fallbacks in ``_admit`` rules
    (4) and (7).
    """
    out: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                out.add(alias.asname or alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                out.add(alias.asname or alias.name)
    return out


def _collect_local_names(tree: ast.AST) -> set[str]:
    """Names bound by def / class / assign / for / with / import — module-scoped."""
    out: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            out.add(node.name)
        elif isinstance(node, ast.Assign):
            for tgt in node.targets:
                if isinstance(tgt, ast.Name):
                    out.add(tgt.id)
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            out.add(node.target.id)
        elif isinstance(node, ast.For) and isinstance(node.target, ast.Name):
            out.add(node.target.id)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                out.add(alias.asname or alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                out.add(alias.asname or alias.name)
        elif isinstance(node, ast.With):
            for item in node.items:
                if isinstance(item.optional_vars, ast.Name):
                    out.add(item.optional_vars.id)
        elif isinstance(node, ast.arguments):
            for a in node.args + node.posonlyargs + node.kwonlyargs:
                out.add(a.arg)
            if node.vararg:
                out.add(node.vararg.arg)
            if node.kwarg:
                out.add(node.kwarg.arg)
        elif isinstance(node, ast.Lambda):
            for a in node.args.args:
                out.add(a.arg)
    return out


def _check_uploader_no_submit_multi(
    tree: ast.AST, path: Path
) -> Iterator[Violation]:
    """Multi-glob target wrapper — applies the rule under either glob."""
    if not any(_glob_matches_path(g, path) for g in _UPLOADER_TARGET_GLOBS):
        return
    yield from _check_uploader_no_submit(tree, path)


UPLOADER_NO_SUBMIT = Rule(
    name="R_UPLOADER_NO_SUBMIT",
    reason_tag="uploader_call_outside_allow_list",
    # Glob is intentionally permissive — we filter inside the check via
    # the multi-target wrapper to handle both uploader.py and
    # uploader_adapters/*.py.
    target_glob="pipeline/orchestrator/seats/**/*.py",
    check=_check_uploader_no_submit_multi,
    description=(
        "Allow-list every callable in pipeline/orchestrator/seats/uploader.py "
        "and pipeline/orchestrator/seats/uploader_adapters/. The Uploader is "
        "prepare-and-stage-only per architecture v7.0.6 — any callable not on "
        "UPLOADER_ALLOW_LIST is an F-UPLOADER-AUTOSUBMIT-ATTEMPTED defense-"
        "layer-1 violation. Aliased / attribute-chain / dynamic-import "
        "bypasses are caught via the shared _AliasResolver. Blueprint: §12.9.3."
    ),
)



R_UPLOADER_NO_SUBMIT = Rule(
    name="R_UPLOADER_NO_SUBMIT",
    reason_tag="uploader_call_outside_allow_list",
    # Glob is intentionally permissive — we filter inside the check via
    # the multi-target wrapper to handle both uploader.py and
    # uploader_adapters/*.py.
    target_glob="pipeline/orchestrator/seats/**/*.py",
    check=_check_uploader_no_submit_multi,
    description=(
        "Allow-list every callable in pipeline/orchestrator/seats/uploader.py "
        "and pipeline/orchestrator/seats/uploader_adapters/. The Uploader is "
        "prepare-and-stage-only per architecture v7.0.6 — any callable not on "
        "the allow list is blocked. Blueprint: section_16_uploader.md §5.2."
    ),
)

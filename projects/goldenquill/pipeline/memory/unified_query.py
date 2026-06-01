"""Unified memory-retrieval registry for the 15 memory registers.

Scope
-----
The architecture proficiency assessment (2026-05-11, Dim 8 = 4/10) named
the fragmented retrieval surface as the single load-bearing
Beta-blocker on the memory-competence axis. This module is the
**operator-facing read-only retrieval registry**: one
``RegisterAdapter`` per memory surface, BM25-class ranking across the
union, provenance preserved on every result, Law-3 org-isolation
enforced at the adapter boundary.

Registers
---------
Workspace-scoped (accessible without ``--org``)::

    1. lessons_json           pipeline/institutional_memory/lessons.json
    2. memory_md              MEMORY.md
    3. daily_logs             daily_logs/*.md
    4. lock_history           pipeline/engineering/lock_history.v1.jsonl
    5. memory_files           memory/*.md  (Cowork auto-memory dir)
    6. benchmarks             vault_shared/benchmarks/register.yaml
    7. funder_intelligence    vault_shared/funder_intelligence/register.yaml
    8. handoffs               pipeline/handoffs/*.md
    9. match_db               vault_shared/match_db/register.yaml  (placeholder
                              — workspace-shared Match DB aggregate per
                              v7.0.5 SPEC; read-only adapter is no-op
                              until the file lands at Stage-5)
   10. cards                  pipeline/cards/**/*.yaml  (CIC/CLC/matrix/memory
                              profile working content — NOT the signed
                              bundles at vault_shared/cards/)
   11. docs                   docs/**/*.md

Per-org-scoped (require ``--org <slug>``)::

   12. kfr                    orgs/<slug>/vault/kfr/register.yaml
   13. classification_register orgs/<slug>/vault/classification/register.yaml
   14. reflection_packets     orgs/<slug>/vault/operational/reflection_packets/*.json
   15. match_database         orgs/<slug>/match_database/register.yaml

Law-3 isolation
---------------
* Workspace-scoped adapters are readable workspace-wide.
* Per-org adapters require an explicit ``org`` argument. ``None`` returns
  zero documents (not "all orgs" — that would be the cross-org read Law
  3 forbids).
* The reserved slug ``_TEMPLATE`` is rejected as if it were a real org.
* Cross-org calls (``adapter.enumerate(org="A")`` followed by
  ``adapter.enumerate(org="B")`` in the same query call) are prevented
  structurally — :func:`Registry.query` accepts a single ``org`` and
  passes it to every per-org adapter exactly once.

Discipline
----------
* **Read-only.** No adapter writes, mutates, or deletes any register
  file. The contract is enumerate-only.
* **No third-party imports.** BM25 is implemented in stdlib + PyYAML
  (already pinned in ``pyproject.toml``). Avoids substrate-pin drag at
  v0.1 Beta finalization.
* **Provenance preserved.** Every :class:`QueryResult` carries a
  :class:`Provenance` with register name, source path, locator (line /
  row / file / id), and an excerpt suitable for citation.
* **Deterministic.** BM25 is order-stable on equal scores; the
  enumerate methods walk files in sorted order; result tie-break is
  ``(score desc, register asc, locator asc)``.

What this module is NOT
-----------------------
* Not a vector index. v0.1 Beta substrate is sparse BM25; the
  assessment's optional ``bge-large-en-v1.5`` dense-vector path is
  deferred (not pinned in pyproject; out of scope per substrate-pin
  rules).
* Not a LOCK-class amendment. Pure operational utility.
* Not a writer. ``tilth memory consolidate-index`` is the writer.
"""

from __future__ import annotations

import json
import math
import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Iterator, Mapping, Optional, Sequence

import yaml


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------


# Workspace-scoped register names (no ``--org`` required).
WORKSPACE_REGISTERS: tuple[str, ...] = (
    "lessons_json",
    "memory_md",
    "daily_logs",
    "lock_history",
    "memory_files",
    "benchmarks",
    "funder_intelligence",
    "handoffs",
    "match_db",
    "cards",
    "docs",
)


# Per-org-scoped register names (``--org`` required).
PER_ORG_REGISTERS: tuple[str, ...] = (
    "kfr",
    "classification_register",
    "reflection_packets",
    "match_database",
)


# Full set — order is the canonical ``list-registers`` order.
ALL_REGISTERS: tuple[str, ...] = WORKSPACE_REGISTERS + PER_ORG_REGISTERS


# Reserved slug names that must never resolve to a real org.
RESERVED_SLUGS: frozenset[str] = frozenset({"_TEMPLATE", "_template"})


# Tokenizer regex — lowercase Unicode-word matching. Stable, stdlib-only.
_TOKEN_RE = re.compile(r"[A-Za-z0-9_]+")


# Default excerpt window (characters around the matched span).
DEFAULT_EXCERPT_WINDOW: int = 240


# Default query result limit.
DEFAULT_QUERY_LIMIT: int = 10


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------


class UnifiedQueryError(Exception):
    """Base error for unified_query operations."""


class Law3Violation(UnifiedQueryError):
    """Raised when a per-org register is accessed without an org slug
    or with a reserved slug, OR when a cross-org leakage attempt is
    structurally detected.
    """


class UnknownRegisterError(UnifiedQueryError):
    """Raised when an unknown register name is referenced."""


# ---------------------------------------------------------------------------
# Provenance + result dataclasses
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Provenance:
    """Where a result came from.

    Attributes
    ----------
    register
        Canonical register name (one of :data:`ALL_REGISTERS`).
    source_path
        Repo-relative path to the file the result was drawn from.
    locator
        Within-file pointer — line number, row index, JSONL row, YAML
        list index, or opaque ID — formatted as a short string. The
        adapter chooses the most-useful locator type per register.
    org
        Org slug if the register is per-org, else ``None``.
    """

    register: str
    source_path: str
    locator: str
    org: Optional[str] = None


@dataclass(frozen=True)
class Document:
    """A single retrievable unit emitted by an adapter."""

    text: str
    provenance: Provenance
    # Adapter-specific structured payload, optional. Adapters may emit
    # the parsed YAML / JSON object alongside the text for callers that
    # want structured access in addition to BM25 ranking.
    raw: Optional[Mapping[str, object]] = None


@dataclass(frozen=True)
class QueryResult:
    """A ranked match.

    Tie-break order is ``(-score, register, locator)`` so identical
    scores are emitted deterministically.
    """

    score: float
    register: str
    provenance: Provenance
    snippet: str
    raw: Optional[Mapping[str, object]] = None


@dataclass(frozen=True)
class RegisterInfo:
    """Summary line for :func:`Registry.list_registers`."""

    name: str
    scope: str  # "workspace" | "per_org"
    source_path_pattern: str
    document_count: int
    last_modified_iso: Optional[str]
    exists: bool


# ---------------------------------------------------------------------------
# BM25 (stdlib-only)
# ---------------------------------------------------------------------------


def tokenize(text: str) -> list[str]:
    """Lowercased Unicode-word tokenization.

    Stable across Python versions; no locale dependence; no stemmer
    (sparse BM25 is sufficient for the v0.1 Beta retrieval contract).
    """

    return [m.group(0).lower() for m in _TOKEN_RE.finditer(text)]


class _BM25Index:
    """Minimal BM25 Okapi index over a corpus of token lists.

    Parameters mirror standard BM25 (k1=1.5, b=0.75) and are
    intentionally not exposed — v0.1 has no benchmark to justify
    tuning them.
    """

    __slots__ = (
        "_k1",
        "_b",
        "_n",
        "_avgdl",
        "_df",
        "_idf",
        "_doc_freqs",
        "_doc_lens",
    )

    def __init__(self, corpus_tokens: Sequence[Sequence[str]]) -> None:
        self._k1 = 1.5
        self._b = 0.75
        self._n = len(corpus_tokens)
        self._doc_lens = [len(d) for d in corpus_tokens]
        total = sum(self._doc_lens)
        self._avgdl = (total / self._n) if self._n > 0 else 0.0
        df: Counter[str] = Counter()
        doc_freqs: list[Counter[str]] = []
        for d in corpus_tokens:
            counts = Counter(d)
            doc_freqs.append(counts)
            df.update(counts.keys())
        self._df = df
        self._doc_freqs = doc_freqs
        # Robertson-Sparck-Jones IDF, +1 smoothing
        self._idf = {
            term: math.log(1.0 + (self._n - dfi + 0.5) / (dfi + 0.5))
            for term, dfi in df.items()
        }

    def score(self, query_tokens: Sequence[str], doc_idx: int) -> float:
        if self._n == 0 or self._avgdl == 0.0:
            return 0.0
        dl = self._doc_lens[doc_idx]
        freqs = self._doc_freqs[doc_idx]
        norm = 1.0 - self._b + self._b * (dl / self._avgdl)
        score = 0.0
        for q in query_tokens:
            idf = self._idf.get(q)
            if idf is None:
                continue
            tf = freqs.get(q, 0)
            if tf == 0:
                continue
            num = tf * (self._k1 + 1)
            den = tf + self._k1 * norm
            score += idf * (num / den)
        return score


# ---------------------------------------------------------------------------
# Adapter base
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class RegisterAdapter:
    """Read-only adapter for a single memory register.

    Concrete adapters are constructed via the module-level factories
    (e.g. :func:`_make_lessons_json_adapter`) and registered in
    :data:`_ADAPTER_FACTORIES`. The factory pattern keeps adapter
    state immutable (frozen dataclass) and lets the Registry pass per-
    query parameters (``repo_root``, ``org``) explicitly rather than
    smuggling them through adapter state.
    """

    name: str
    scope: str  # "workspace" | "per_org"
    source_path_pattern: str

    def enumerate(
        self,
        *,
        repo_root: Path,
        org: Optional[str],
    ) -> Iterator[Document]:
        """Yield :class:`Document` instances from this register.

        Subclasses override via the dispatch table at the bottom of
        this module. The base implementation raises so that any
        forgotten registration surfaces loudly.
        """

        raise NotImplementedError(self.name)

    def existence_probe(
        self,
        *,
        repo_root: Path,
        org: Optional[str],
    ) -> tuple[bool, Optional[Path]]:
        """Return ``(exists, primary_path)``.

        ``primary_path`` is the canonical file/directory the adapter
        reads. Used by :func:`Registry.list_registers` for the
        last-modified column.
        """

        raise NotImplementedError(self.name)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _validate_org(org: Optional[str]) -> str:
    if org is None:
        raise Law3Violation(
            "per-org adapter accessed without --org; Law 3 (Org Isolation) "
            "forbids implicit cross-org reads"
        )
    if not org:
        raise Law3Violation("org slug is empty")
    if org in RESERVED_SLUGS:
        raise Law3Violation(f"reserved slug not allowed as org: {org!r}")
    if "/" in org or ".." in org or org.startswith("."):
        raise Law3Violation(f"malformed org slug: {org!r}")
    return org


def _excerpt(text: str, query_tokens: Sequence[str], window: int = DEFAULT_EXCERPT_WINDOW) -> str:
    """Cheap snippet centered on the first matching query token."""

    if not text:
        return ""
    if not query_tokens:
        return text[:window].strip()
    lower = text.lower()
    best_pos = -1
    for q in query_tokens:
        pos = lower.find(q)
        if pos != -1 and (best_pos == -1 or pos < best_pos):
            best_pos = pos
    if best_pos == -1:
        return text[:window].strip()
    start = max(0, best_pos - window // 2)
    end = min(len(text), best_pos + window // 2)
    snippet = text[start:end].strip()
    if start > 0:
        snippet = "…" + snippet
    if end < len(text):
        snippet = snippet + "…"
    return snippet


def _safe_iso_mtime(path: Path) -> Optional[str]:
    try:
        from datetime import datetime, timezone

        return (
            datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
            .isoformat()
            .replace("+00:00", "Z")
        )
    except (OSError, ValueError):
        return None


def _safe_read_text(path: Path) -> Optional[str]:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def _safe_yaml_load(path: Path) -> Optional[object]:
    text = _safe_read_text(path)
    if text is None:
        return None
    try:
        return yaml.safe_load(text)
    except yaml.YAMLError:
        return None


# ---------------------------------------------------------------------------
# Concrete adapters
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class _LessonsJsonAdapter(RegisterAdapter):
    name: str = "lessons_json"
    scope: str = "workspace"
    source_path_pattern: str = "pipeline/institutional_memory/lessons.json"

    def _path(self, repo_root: Path) -> Path:
        return repo_root / self.source_path_pattern

    def existence_probe(self, *, repo_root: Path, org: Optional[str]):
        p = self._path(repo_root)
        return (p.exists(), p)

    def enumerate(self, *, repo_root: Path, org: Optional[str]):
        p = self._path(repo_root)
        text = _safe_read_text(p)
        if text is None:
            return
        try:
            obj = json.loads(text)
        except json.JSONDecodeError:
            return
        lessons = obj.get("lessons", []) if isinstance(obj, dict) else []
        for i, lesson in enumerate(lessons):
            if not isinstance(lesson, dict):
                continue
            lid = str(lesson.get("id", f"row-{i}"))
            title = str(lesson.get("title", ""))
            pattern = str(lesson.get("pattern", ""))
            pre_check = str(lesson.get("pre_check", ""))
            origin = str(lesson.get("origin", ""))
            severity = str(lesson.get("severity", ""))
            text_body = " ".join(
                t for t in (lid, title, pattern, pre_check, origin, severity) if t
            )
            yield Document(
                text=text_body,
                provenance=Provenance(
                    register=self.name,
                    source_path=self.source_path_pattern,
                    locator=lid,
                ),
                raw=lesson,
            )


@dataclass(frozen=True)
class _MemoryMdAdapter(RegisterAdapter):
    name: str = "memory_md"
    scope: str = "workspace"
    source_path_pattern: str = "MEMORY.md"

    def _path(self, repo_root: Path) -> Path:
        return repo_root / self.source_path_pattern

    def existence_probe(self, *, repo_root: Path, org: Optional[str]):
        p = self._path(repo_root)
        return (p.exists(), p)

    def enumerate(self, *, repo_root: Path, org: Optional[str]):
        p = self._path(repo_root)
        text = _safe_read_text(p)
        if text is None:
            return
        for i, line in enumerate(text.splitlines(), start=1):
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            yield Document(
                text=stripped,
                provenance=Provenance(
                    register=self.name,
                    source_path=self.source_path_pattern,
                    locator=f"line-{i}",
                ),
            )


@dataclass(frozen=True)
class _DailyLogsAdapter(RegisterAdapter):
    name: str = "daily_logs"
    scope: str = "workspace"
    source_path_pattern: str = "daily_logs/*.md"

    def _dir(self, repo_root: Path) -> Path:
        return repo_root / "daily_logs"

    def existence_probe(self, *, repo_root: Path, org: Optional[str]):
        d = self._dir(repo_root)
        return (d.exists() and d.is_dir(), d)

    def enumerate(self, *, repo_root: Path, org: Optional[str]):
        d = self._dir(repo_root)
        if not d.is_dir():
            return
        for path in sorted(d.glob("*.md")):
            text = _safe_read_text(path)
            if text is None:
                continue
            rel = path.relative_to(repo_root).as_posix()
            yield Document(
                text=text,
                provenance=Provenance(
                    register=self.name,
                    source_path=rel,
                    locator=path.name,
                ),
            )


@dataclass(frozen=True)
class _LockHistoryAdapter(RegisterAdapter):
    name: str = "lock_history"
    scope: str = "workspace"
    source_path_pattern: str = "pipeline/engineering/lock_history.v1.jsonl"

    def _path(self, repo_root: Path) -> Path:
        return repo_root / self.source_path_pattern

    def existence_probe(self, *, repo_root: Path, org: Optional[str]):
        p = self._path(repo_root)
        return (p.exists(), p)

    def enumerate(self, *, repo_root: Path, org: Optional[str]):
        p = self._path(repo_root)
        text = _safe_read_text(p)
        if text is None:
            return
        for i, line in enumerate(text.splitlines(), start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                row = json.loads(stripped)
            except json.JSONDecodeError:
                continue
            if not isinstance(row, dict):
                continue
            module = str(row.get("module", ""))
            section = str(row.get("blueprint_section", ""))
            verdict = str(row.get("review_verdict", ""))
            notes = str(row.get("findings_note", ""))
            cls = str(row.get("lock_class", ""))
            text_body = " ".join(
                t for t in (module, section, verdict, notes, cls) if t
            )
            yield Document(
                text=text_body,
                provenance=Provenance(
                    register=self.name,
                    source_path=self.source_path_pattern,
                    locator=f"row-{i}",
                ),
                raw=row,
            )


@dataclass(frozen=True)
class _MemoryFilesAdapter(RegisterAdapter):
    name: str = "memory_files"
    scope: str = "workspace"
    source_path_pattern: str = "memory/*.md"

    def _dir(self, repo_root: Path) -> Path:
        return repo_root / "memory"

    def existence_probe(self, *, repo_root: Path, org: Optional[str]):
        d = self._dir(repo_root)
        return (d.exists() and d.is_dir(), d)

    def enumerate(self, *, repo_root: Path, org: Optional[str]):
        d = self._dir(repo_root)
        if not d.is_dir():
            return
        for path in sorted(d.glob("*.md")):
            text = _safe_read_text(path)
            if text is None:
                continue
            rel = path.relative_to(repo_root).as_posix()
            yield Document(
                text=text,
                provenance=Provenance(
                    register=self.name,
                    source_path=rel,
                    locator=path.name,
                ),
            )


@dataclass(frozen=True)
class _YamlRegisterAdapter(RegisterAdapter):
    """Shared base for the YAML register files (benchmarks /
    funder_intelligence / match_db / kfr / classification /
    match_database).

    Reads the YAML, picks the top-level list/dict the register
    advertises, and emits one Document per entry.
    """

    list_keys: tuple[str, ...] = ()

    def _path(self, repo_root: Path, org: Optional[str]) -> Path:
        raise NotImplementedError

    def _entries(self, obj: object) -> Iterable[tuple[str, dict]]:
        if obj is None:
            return
        if not isinstance(obj, dict):
            return
        for key in self.list_keys:
            entries = obj.get(key)
            if isinstance(entries, list):
                for i, e in enumerate(entries):
                    if isinstance(e, dict):
                        # Prefer a stable id field if present.
                        ident = (
                            e.get("id")
                            or e.get("match_id")
                            or e.get("benchmark_id")
                            or e.get("doc_id")
                            or e.get("funder_id")
                            or f"{key}-{i}"
                        )
                        yield (str(ident), e)
            elif isinstance(entries, dict):
                for k, v in entries.items():
                    if isinstance(v, dict):
                        yield (str(k), v)


@dataclass(frozen=True)
class _BenchmarksAdapter(_YamlRegisterAdapter):
    name: str = "benchmarks"
    scope: str = "workspace"
    source_path_pattern: str = "vault_shared/benchmarks/register.yaml"
    list_keys: tuple[str, ...] = ("benchmarks", "entries")

    def _path(self, repo_root: Path, org: Optional[str]) -> Path:
        return repo_root / self.source_path_pattern

    def existence_probe(self, *, repo_root: Path, org: Optional[str]):
        p = self._path(repo_root, org)
        return (p.exists(), p)

    def enumerate(self, *, repo_root: Path, org: Optional[str]):
        p = self._path(repo_root, org)
        obj = _safe_yaml_load(p)
        for ident, entry in self._entries(obj):
            text_body = _dict_to_text(entry)
            yield Document(
                text=text_body,
                provenance=Provenance(
                    register=self.name,
                    source_path=self.source_path_pattern,
                    locator=ident,
                ),
                raw=entry,
            )


@dataclass(frozen=True)
class _FunderIntelligenceAdapter(_YamlRegisterAdapter):
    name: str = "funder_intelligence"
    scope: str = "workspace"
    source_path_pattern: str = "vault_shared/funder_intelligence/register.yaml"
    list_keys: tuple[str, ...] = ("documents", "funders", "entries")

    def _path(self, repo_root: Path, org: Optional[str]) -> Path:
        return repo_root / self.source_path_pattern

    def existence_probe(self, *, repo_root: Path, org: Optional[str]):
        p = self._path(repo_root, org)
        return (p.exists(), p)

    def enumerate(self, *, repo_root: Path, org: Optional[str]):
        p = self._path(repo_root, org)
        obj = _safe_yaml_load(p)
        for ident, entry in self._entries(obj):
            text_body = _dict_to_text(entry)
            yield Document(
                text=text_body,
                provenance=Provenance(
                    register=self.name,
                    source_path=self.source_path_pattern,
                    locator=ident,
                ),
                raw=entry,
            )


@dataclass(frozen=True)
class _MatchDbAdapter(_YamlRegisterAdapter):
    """Workspace-shared Match DB placeholder.

    Per v7.0.5, the workspace-shared Match DB aggregate is SPEC-locked
    but not built. The adapter is a read-only no-op until a file lands
    at the documented path. This keeps the registry's 13-register
    surface complete and the brief's distinction between the
    workspace concept and the per-org realization respected.
    """

    name: str = "match_db"
    scope: str = "workspace"
    source_path_pattern: str = "vault_shared/match_db/register.yaml"
    list_keys: tuple[str, ...] = ("matches", "entries")

    def _path(self, repo_root: Path, org: Optional[str]) -> Path:
        return repo_root / self.source_path_pattern

    def existence_probe(self, *, repo_root: Path, org: Optional[str]):
        p = self._path(repo_root, org)
        return (p.exists(), p)

    def enumerate(self, *, repo_root: Path, org: Optional[str]):
        p = self._path(repo_root, org)
        obj = _safe_yaml_load(p)
        for ident, entry in self._entries(obj):
            text_body = _dict_to_text(entry)
            yield Document(
                text=text_body,
                provenance=Provenance(
                    register=self.name,
                    source_path=self.source_path_pattern,
                    locator=ident,
                ),
                raw=entry,
            )


@dataclass(frozen=True)
class _HandoffsAdapter(RegisterAdapter):
    name: str = "handoffs"
    scope: str = "workspace"
    source_path_pattern: str = "pipeline/handoffs/*.md"

    def _dir(self, repo_root: Path) -> Path:
        return repo_root / "pipeline" / "handoffs"

    def existence_probe(self, *, repo_root: Path, org: Optional[str]):
        d = self._dir(repo_root)
        return (d.exists() and d.is_dir(), d)

    def enumerate(self, *, repo_root: Path, org: Optional[str]):
        d = self._dir(repo_root)
        if not d.is_dir():
            return
        for path in sorted(d.glob("*.md")):
            text = _safe_read_text(path)
            if text is None:
                continue
            rel = path.relative_to(repo_root).as_posix()
            yield Document(
                text=text,
                provenance=Provenance(
                    register=self.name,
                    source_path=rel,
                    locator=path.name,
                ),
            )


@dataclass(frozen=True)
class _KfrAdapter(_YamlRegisterAdapter):
    name: str = "kfr"
    scope: str = "per_org"
    source_path_pattern: str = "orgs/<slug>/vault/kfr/register.yaml"
    list_keys: tuple[str, ...] = ("facts",)

    def _path(self, repo_root: Path, org: Optional[str]) -> Path:
        return repo_root / "orgs" / _validate_org(org) / "vault" / "kfr" / "register.yaml"

    def existence_probe(self, *, repo_root: Path, org: Optional[str]):
        if org is None or org in RESERVED_SLUGS:
            return (False, None)
        try:
            p = self._path(repo_root, org)
        except Law3Violation:
            return (False, None)
        return (p.exists(), p)

    def enumerate(self, *, repo_root: Path, org: Optional[str]):
        p = self._path(repo_root, org)
        obj = _safe_yaml_load(p)
        rel = p.relative_to(repo_root).as_posix() if p.is_relative_to(repo_root) else str(p)
        for ident, entry in self._entries(obj):
            text_body = _dict_to_text(entry)
            yield Document(
                text=text_body,
                provenance=Provenance(
                    register=self.name,
                    source_path=rel,
                    locator=ident,
                    org=org,
                ),
                raw=entry,
            )


@dataclass(frozen=True)
class _ClassificationRegisterAdapter(_YamlRegisterAdapter):
    name: str = "classification_register"
    scope: str = "per_org"
    source_path_pattern: str = "orgs/<slug>/vault/classification/register.yaml"
    list_keys: tuple[str, ...] = ("entries", "fields")

    def _path(self, repo_root: Path, org: Optional[str]) -> Path:
        return (
            repo_root
            / "orgs"
            / _validate_org(org)
            / "vault"
            / "classification"
            / "register.yaml"
        )

    def existence_probe(self, *, repo_root: Path, org: Optional[str]):
        if org is None or org in RESERVED_SLUGS:
            return (False, None)
        try:
            p = self._path(repo_root, org)
        except Law3Violation:
            return (False, None)
        return (p.exists(), p)

    def enumerate(self, *, repo_root: Path, org: Optional[str]):
        p = self._path(repo_root, org)
        obj = _safe_yaml_load(p)
        rel = p.relative_to(repo_root).as_posix() if p.is_relative_to(repo_root) else str(p)
        for ident, entry in self._entries(obj):
            text_body = _dict_to_text(entry)
            yield Document(
                text=text_body,
                provenance=Provenance(
                    register=self.name,
                    source_path=rel,
                    locator=ident,
                    org=org,
                ),
                raw=entry,
            )


@dataclass(frozen=True)
class _ReflectionPacketsAdapter(RegisterAdapter):
    name: str = "reflection_packets"
    scope: str = "per_org"
    source_path_pattern: str = "orgs/<slug>/vault/operational/reflection_packets/*.json"

    def _dir(self, repo_root: Path, org: Optional[str]) -> Path:
        return (
            repo_root
            / "orgs"
            / _validate_org(org)
            / "vault"
            / "operational"
            / "reflection_packets"
        )

    def existence_probe(self, *, repo_root: Path, org: Optional[str]):
        if org is None or org in RESERVED_SLUGS:
            return (False, None)
        try:
            d = self._dir(repo_root, org)
        except Law3Violation:
            return (False, None)
        return (d.exists() and d.is_dir(), d)

    def enumerate(self, *, repo_root: Path, org: Optional[str]):
        d = self._dir(repo_root, org)
        if not d.is_dir():
            return
        for path in sorted(d.glob("*.json")):
            text = _safe_read_text(path)
            if text is None:
                continue
            try:
                obj = json.loads(text)
            except json.JSONDecodeError:
                continue
            rel = path.relative_to(repo_root).as_posix() if path.is_relative_to(repo_root) else str(path)
            text_body = _dict_to_text(obj) if isinstance(obj, dict) else text
            yield Document(
                text=text_body,
                provenance=Provenance(
                    register=self.name,
                    source_path=rel,
                    locator=path.name,
                    org=org,
                ),
                raw=obj if isinstance(obj, dict) else None,
            )


@dataclass(frozen=True)
class _MatchDatabaseAdapter(_YamlRegisterAdapter):
    name: str = "match_database"
    scope: str = "per_org"
    source_path_pattern: str = "orgs/<slug>/match_database/register.yaml"
    list_keys: tuple[str, ...] = ("matches", "entries")

    def _path(self, repo_root: Path, org: Optional[str]) -> Path:
        return (
            repo_root
            / "orgs"
            / _validate_org(org)
            / "match_database"
            / "register.yaml"
        )

    def existence_probe(self, *, repo_root: Path, org: Optional[str]):
        if org is None or org in RESERVED_SLUGS:
            return (False, None)
        try:
            p = self._path(repo_root, org)
        except Law3Violation:
            return (False, None)
        return (p.exists(), p)

    def enumerate(self, *, repo_root: Path, org: Optional[str]):
        p = self._path(repo_root, org)
        obj = _safe_yaml_load(p)
        rel = p.relative_to(repo_root).as_posix() if p.is_relative_to(repo_root) else str(p)
        for ident, entry in self._entries(obj):
            text_body = _dict_to_text(entry)
            yield Document(
                text=text_body,
                provenance=Provenance(
                    register=self.name,
                    source_path=rel,
                    locator=ident,
                    org=org,
                ),
                raw=entry,
            )


@dataclass(frozen=True)
class _CardsAdapter(RegisterAdapter):
    """Workspace-scoped adapter for the card content tree.

    Walks ``pipeline/cards/`` for ``*.yaml`` content and emits one
    :class:`Document` per card file. Cards (Customer Identity, Capital
    Logic, plus matrix / memory profiles) are first-class content —
    operator-facing retrieval should reach them the same way it
    reaches lessons or handoffs.

    Card YAML files in this tree are not signed assets — those live
    under ``vault_shared/cards/``. The signed bundles are intentionally
    NOT enumerated here; this is the working-content surface only.
    """

    name: str = "cards"
    scope: str = "workspace"
    source_path_pattern: str = "pipeline/cards/**/*.yaml"

    def _dir(self, repo_root: Path) -> Path:
        return repo_root / "pipeline" / "cards"

    def existence_probe(self, *, repo_root: Path, org: Optional[str]):
        d = self._dir(repo_root)
        return (d.exists() and d.is_dir(), d)

    def enumerate(self, *, repo_root: Path, org: Optional[str]):
        d = self._dir(repo_root)
        if not d.is_dir():
            return
        for path in sorted(d.rglob("*.yaml")):
            text = _safe_read_text(path)
            if text is None:
                continue
            obj: object = None
            try:
                obj = yaml.safe_load(text)
            except yaml.YAMLError:
                obj = None
            rel = path.relative_to(repo_root).as_posix()
            text_body = _dict_to_text(obj) if isinstance(obj, dict) else text
            yield Document(
                text=text_body,
                provenance=Provenance(
                    register=self.name,
                    source_path=rel,
                    locator=rel,
                ),
                raw=obj if isinstance(obj, dict) else None,
            )


@dataclass(frozen=True)
class _DocsAdapter(RegisterAdapter):
    """Workspace-scoped adapter for ``docs/**/*.md``.

    Walks the ``docs/`` directory recursively and emits one
    :class:`Document` per markdown file. Skips files / directories
    under hidden (``.``-prefixed) path components defensively.
    """

    name: str = "docs"
    scope: str = "workspace"
    source_path_pattern: str = "docs/**/*.md"

    def _dir(self, repo_root: Path) -> Path:
        return repo_root / "docs"

    def existence_probe(self, *, repo_root: Path, org: Optional[str]):
        d = self._dir(repo_root)
        return (d.exists() and d.is_dir(), d)

    def enumerate(self, *, repo_root: Path, org: Optional[str]):
        d = self._dir(repo_root)
        if not d.is_dir():
            return
        for path in sorted(d.rglob("*.md")):
            if any(part.startswith(".") for part in path.relative_to(d).parts):
                continue
            text = _safe_read_text(path)
            if text is None:
                continue
            rel = path.relative_to(repo_root).as_posix()
            yield Document(
                text=text,
                provenance=Provenance(
                    register=self.name,
                    source_path=rel,
                    locator=path.name,
                ),
            )


def _dict_to_text(d: object) -> str:
    """Flatten a dict / nested structure into a search-tokenizable
    string. Stable across runs (sorted keys).
    """

    if d is None:
        return ""
    if isinstance(d, str):
        return d
    if isinstance(d, (int, float, bool)):
        return str(d)
    if isinstance(d, dict):
        parts = []
        for k in sorted(d.keys(), key=str):
            v = d[k]
            parts.append(f"{k}: {_dict_to_text(v)}")
        return " ".join(parts)
    if isinstance(d, (list, tuple)):
        return " ".join(_dict_to_text(x) for x in d)
    return str(d)


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------


_ADAPTERS: dict[str, RegisterAdapter] = {
    "lessons_json": _LessonsJsonAdapter(),
    "memory_md": _MemoryMdAdapter(),
    "daily_logs": _DailyLogsAdapter(),
    "lock_history": _LockHistoryAdapter(),
    "memory_files": _MemoryFilesAdapter(),
    "benchmarks": _BenchmarksAdapter(),
    "funder_intelligence": _FunderIntelligenceAdapter(),
    "match_db": _MatchDbAdapter(),
    "handoffs": _HandoffsAdapter(),
    "cards": _CardsAdapter(),
    "docs": _DocsAdapter(),
    "kfr": _KfrAdapter(),
    "classification_register": _ClassificationRegisterAdapter(),
    "reflection_packets": _ReflectionPacketsAdapter(),
    "match_database": _MatchDatabaseAdapter(),
}


def get_adapter(name: str) -> RegisterAdapter:
    """Look up the adapter for a register name, raising
    :class:`UnknownRegisterError` if absent.
    """

    try:
        return _ADAPTERS[name]
    except KeyError as exc:
        raise UnknownRegisterError(f"unknown register: {name!r}") from exc


def all_adapters() -> tuple[RegisterAdapter, ...]:
    """Return adapters in canonical (workspace-first) order."""

    return tuple(_ADAPTERS[name] for name in ALL_REGISTERS)


@dataclass(frozen=True)
class Registry:
    """Holds the adapter set + dispatches list/inspect/query calls.

    Frozen by design — there is one canonical Registry per process and
    it is constructed by :func:`make_registry`. Tests can substitute by
    constructing a Registry with a custom adapter map (see
    :func:`Registry.with_adapters`).
    """

    adapters: Mapping[str, RegisterAdapter] = field(default_factory=lambda: _ADAPTERS)

    # ------------------------------------------------------------------
    # Construction helpers
    # ------------------------------------------------------------------

    @classmethod
    def default(cls) -> "Registry":
        return cls(adapters=_ADAPTERS)

    def with_adapters(self, adapters: Mapping[str, RegisterAdapter]) -> "Registry":
        return Registry(adapters=adapters)

    # ------------------------------------------------------------------
    # list-registers
    # ------------------------------------------------------------------

    def list_registers(
        self,
        *,
        repo_root: Path,
        org: Optional[str] = None,
    ) -> list[RegisterInfo]:
        out: list[RegisterInfo] = []
        for name in self.adapters:
            adapter = self.adapters[name]
            # Workspace adapters always probe. Per-org adapters probe
            # only when an org is supplied; otherwise the row is shown
            # with exists=False + count=0 so list-registers stays
            # informative without leaking org existence.
            if adapter.scope == "per_org" and (org is None or org in RESERVED_SLUGS):
                out.append(
                    RegisterInfo(
                        name=name,
                        scope=adapter.scope,
                        source_path_pattern=adapter.source_path_pattern,
                        document_count=0,
                        last_modified_iso=None,
                        exists=False,
                    )
                )
                continue
            exists, primary = adapter.existence_probe(repo_root=repo_root, org=org)
            count = 0
            if exists:
                try:
                    for _ in adapter.enumerate(repo_root=repo_root, org=org):
                        count += 1
                except Law3Violation:
                    count = 0
                except Exception:
                    # Defensive — a malformed register should not crash
                    # list-registers; surface it as count=0.
                    count = 0
            last_iso = _safe_iso_mtime(primary) if (exists and primary is not None) else None
            out.append(
                RegisterInfo(
                    name=name,
                    scope=adapter.scope,
                    source_path_pattern=adapter.source_path_pattern,
                    document_count=count,
                    last_modified_iso=last_iso,
                    exists=exists,
                )
            )
        return out

    # ------------------------------------------------------------------
    # inspect
    # ------------------------------------------------------------------

    def inspect(
        self,
        *,
        register: str,
        repo_root: Path,
        org: Optional[str] = None,
    ) -> list[Document]:
        adapter = self.adapters.get(register)
        if adapter is None:
            raise UnknownRegisterError(f"unknown register: {register!r}")
        if adapter.scope == "per_org":
            _validate_org(org)
        try:
            return list(adapter.enumerate(repo_root=repo_root, org=org))
        except Law3Violation:
            raise

    # ------------------------------------------------------------------
    # query
    # ------------------------------------------------------------------

    def query(
        self,
        *,
        query: str,
        repo_root: Path,
        org: Optional[str] = None,
        registers: Optional[Sequence[str]] = None,
        limit: int = DEFAULT_QUERY_LIMIT,
    ) -> list[QueryResult]:
        if not query.strip():
            raise UnifiedQueryError("query is empty")
        q_tokens = tokenize(query)
        # Decide which adapters to walk.
        targets: list[RegisterAdapter]
        if registers is None:
            targets = []
            for name in self.adapters:
                adapter = self.adapters[name]
                if adapter.scope == "per_org" and (org is None or org in RESERVED_SLUGS):
                    # Law-3: skip per-org adapters when no org given.
                    continue
                targets.append(adapter)
        else:
            targets = []
            for name in registers:
                if name not in self.adapters:
                    raise UnknownRegisterError(f"unknown register: {name!r}")
                adapter = self.adapters[name]
                if adapter.scope == "per_org":
                    _validate_org(org)
                targets.append(adapter)

        # Collect documents.
        docs: list[Document] = []
        for adapter in targets:
            try:
                docs.extend(adapter.enumerate(repo_root=repo_root, org=org))
            except Law3Violation:
                raise
            except Exception:
                # Defensive — malformed register should not crash query.
                continue

        if not docs:
            return []

        corpus = [tokenize(d.text) for d in docs]
        index = _BM25Index(corpus)
        scored: list[QueryResult] = []
        for i, doc in enumerate(docs):
            score = index.score(q_tokens, i)
            if score <= 0.0:
                continue
            scored.append(
                QueryResult(
                    score=score,
                    register=doc.provenance.register,
                    provenance=doc.provenance,
                    snippet=_excerpt(doc.text, q_tokens),
                    raw=doc.raw,
                )
            )

        # Deterministic tie-break: (-score, register, locator)
        scored.sort(
            key=lambda r: (-r.score, r.register, r.provenance.locator)
        )
        return scored[:limit]


def make_registry() -> Registry:
    """Module-level convenience for callers that don't want to import
    :class:`Registry` directly.
    """

    return Registry.default()


__all__ = [
    "ALL_REGISTERS",
    "DEFAULT_EXCERPT_WINDOW",
    "DEFAULT_QUERY_LIMIT",
    "Document",
    "Law3Violation",
    "PER_ORG_REGISTERS",
    "Provenance",
    "QueryResult",
    "RegisterAdapter",
    "RegisterInfo",
    "Registry",
    "UnifiedQueryError",
    "UnknownRegisterError",
    "WORKSPACE_REGISTERS",
    "all_adapters",
    "get_adapter",
    "make_registry",
    "tokenize",
]

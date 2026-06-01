# Spec card — pipeline.sovereignty.topology

**STATUS:** LOCKED

**Blueprint anchor:** `pipeline/blueprint/v0.1/section_1_sovereignty_envelope.md` §1 inventory row 7 (v6); §7.5 unit tests `test_topology_doc_sourced_whitelist_*`; §6.7 F-ISOLATION-* failure codes
**Blueprint hash-at-card:** `<to-populate-at-LOCK>`
**Spec-card version:** v1
**Round:** B (2026-04-19)
**Futureproofing scope:** §4.1 public API boundary / §4.6 BLUEPRINT_DEPS / §4.9 regression corpus / §4.10 type hints / §4.11 blueprint-citing docstrings / E-002 case-normalized identifiers

## Public API (goes in `__all__`)

- `is_doc_sourced_path(path: Path, *, bound_slug: str, repo_root: Path) -> bool` — returns True iff the resolved path falls under one of the five DOC_SOURCED roots AND resolves to a real (non-symlink-escaped) location.
- `DocSourcedRoot` frozen dataclass — enumerates the five whitelisted roots with their pattern strings.
- `DOC_SOURCED_ROOTS: tuple[DocSourcedRoot, ...]` — the five-entry tuple. Module-level constant.
- `canonicalize_vault_path(path: Path, *, repo_root: Path) -> Path` — resolve symlinks, reject escapes outside repo_root, return canonical path. (Amended 2026-04-19 post-committee: `repo_root` kwarg is required — it anchors the symlink-escape walk in §Algorithm step 3. Earlier signature draft omitted it; D-10 of `drift_log_2026-04-19.md` records the amendment.)
- `PathEscapedRoot` exception — raised when canonicalization reveals the path escapes its claimed root.
- `SymlinkRejected` exception — raised when a path component is a symlink that would escape.

## Data structures

```python
@dataclass(frozen=True, kw_only=True)
class DocSourcedRoot:
    label: str                        # e.g. "rfa", "org", "dossier", "rubrics", "institutional_memory"
    path_template: str                # e.g. "rfa/", "orgs/{slug}/", "pipeline/rubrics/"
    slug_parameterized: bool          # True iff path_template contains "{slug}"

DOC_SOURCED_ROOTS = (
    DocSourcedRoot(label="rfa",                    path_template="rfa/",                             slug_parameterized=False),
    DocSourcedRoot(label="org",                    path_template="orgs/{slug}/",                     slug_parameterized=True),
    DocSourcedRoot(label="dossier",                path_template="orgs/{slug}/dossier/entities/",    slug_parameterized=True),
    DocSourcedRoot(label="rubrics",                path_template="pipeline/rubrics/",                slug_parameterized=False),
    DocSourcedRoot(label="institutional_memory",   path_template="pipeline/institutional_memory/",   slug_parameterized=False),
)
```

## Algorithms

### `is_doc_sourced_path`

Per blueprint §7.5 test expectations:

1. Type-check args: `path` is `Path`, `bound_slug` is `str`, `repo_root` is `Path`. Else `TypeError`.
2. Resolve `repo_root` to absolute (strict). If not a directory, `PathEscapedRoot`.
3. For each `DocSourcedRoot` in `DOC_SOURCED_ROOTS`:
   - Substitute `{slug}` with `bound_slug` if `slug_parameterized`.
   - Compute `expected_prefix = repo_root / substituted_template` (no trailing-slash normalization).
   - Attempt `path.resolve(strict=False)` → `resolved`.
   - If `resolved` is not relative to `expected_prefix` via `Path.is_relative_to`, continue to next root.
   - Else: additionally verify no component along the walk from `repo_root` to `resolved` is a symlink that escapes. If yes: raise `SymlinkRejected`. If no: return True.
4. If no root matched: return False.

### `canonicalize_vault_path`

1. Type-check `path` is `Path`.
2. `path.resolve(strict=True)` — must exist.
3. Walk parents from the resolved path back toward root; if any component is a symlink whose target leaves `repo_root`, raise `SymlinkRejected`.
4. Return the resolved absolute path.

Org-slug consistency: consumers who pass `bound_slug` should pre-canonicalize via `pipeline.sovereignty.canonical_slug()` from Round A. topology.py does NOT re-canonicalize the slug; the caller is responsible.

## Failure codes

Per blueprint §6.7 (Isolation-related):

- `PathEscapedRoot` — path resolves outside the claimed root (post-symlink-resolution).
- `SymlinkRejected` — path contains a symlink component pointing outside the root.
- `TypeError` at public-surface entry for non-Path / non-str args.

No `F-ISOLATION-*` codes fire directly from topology.py; the isolation module (Round D) consumes these exceptions and maps them to `F-ISO-*` failures at the boundary.

## Test surface

Target ≥ 20 tests.

### Property tests
- `is_doc_sourced_path` is reflexive over the five roots: every `repo_root / root.path_template` path is True.
- No path outside the five roots is True under any `bound_slug`.
- `canonicalize_vault_path` is idempotent: `canonicalize(canonicalize(x)) == canonicalize(x)`.
- The five roots are disjoint except for the `org` root overlapping `dossier` (dossier is a subset).

### Failure-code tests
- Type errors on all public functions (wrong types for path, bound_slug, repo_root).
- Path that resolves to `orgs/other_slug/...` with `bound_slug="my_slug"` → False (not `True` via the `org` root, because the slug substitution mismatches).
- Symlink at `orgs/my_slug/malicious → /etc/passwd` when passed → `SymlinkRejected` via `canonicalize_vault_path`.
- `PathEscapedRoot` when `repo_root / "orgs/my_slug/../outside"` is passed and `../outside` resolves above repo_root.
- Reserved reserved-slug-parameter like `_template` as `bound_slug` → underlying `is_doc_sourced_path` returns False (no `orgs/_template/` should be allocatable per §4.3 M3 reserved names).

### Corpus tests
- `tests/corpus/topology/v1/doc_sourced_vectors.json` — preserved (path, bound_slug, expected) triples covering all five roots, all edge cases, all symlink scenarios.

### Blueprint §7.5 regression tests (MUST pass)
- `test_topology_doc_sourced_whitelist_rejects_cache_path`
- `test_topology_doc_sourced_whitelist_accepts_five_roots`
- (prefix matches; see blueprint for full names)

## Futureproofing commitments

- Public API via `__all__`; downstream sections import from `pipeline.sovereignty`, NEVER from `pipeline.sovereignty.topology` directly (enforced by §4.1 AST-lint).
- `BLUEPRINT_DEPS` populated at top of module.
- Fully typed with `Path`, `str`, `tuple[DocSourcedRoot, ...]`.
- Docstring citations `[§7.5]`, `[§1 row 7]`.
- Schema version N/A (module produces no artifacts).
- Crypto-agility N/A (module has no crypto surface).
- Round-A lesson pre-check:
  - E-001 enforce-by-default: every public function validates types before semantics.
  - E-002 case-normalized identifiers: DocSourcedRoot labels are lowercase slugs.
  - E-003 strict-NFC rule: N/A (paths are byte-level, not Unicode-tolerant).
  - E-004 committee fallback: N/A (applies to router.yaml not this module).

## Dependencies

- `pipeline.sovereignty.org_slug.canonical_slug` — caller responsibility to pre-canonicalize slug; topology.py does NOT import this
- `pathlib.Path` — stdlib
- No cross-section imports

## Done definition

- ≥ 20 pytest tests covering every public function, every failure mode, every blueprint §7.5 regression vector.
- `pytest tests/sovereignty/test_topology.py` green.
- Cumulative suite stays green (Round-A tests unchanged).
- Lines-of-code target ~270 per blueprint §1 row 7 (retroactively amended 2026-04-19 post-committee E3 synthesis — original ~180 estimate did not account for defensive `_walk_for_symlink_escape` walker + `_validate_entry_args` slug-canonicality gate + symlink-escape-walk anchor logic); accept ±25% (203-338 acceptable). Drift D-14 records the retroactive estimate adjustment.
- All public symbols in `pipeline/sovereignty/__init__.py` `__all__`.
- No import from `pipeline.sovereignty.topology` anywhere in tests except where testing a private helper (E1 rule).

## Out of scope (Round B — stubbed or deferred)

- `isolation.OrgRootNamespace` context manager — Round D module (depends on topology).
- Linux bind-mount implementation — Round D.
- `within_org_root` predicate — blueprint §3.11d says this lives in `isolation.py`, not `topology.py`. Do not implement here.
- Session-binding checks — Round E.

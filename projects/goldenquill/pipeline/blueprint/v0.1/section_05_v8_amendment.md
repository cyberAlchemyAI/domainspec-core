---
title: Blueprint §5 Pipeline — Amendment v8 (Track-registry adoption per R.PF1)
filed: 2026-05-10
operator: Josh
amendment_status: **LOCKED 2026-05-10** — authored 2026-05-10 in WS-G Code phase per `pipeline/planning/v0_2_dispatch_plan_2026-05-09.md` §WS-G. L-005 Cycle 1 dispatched 2026-05-10 (live cross-family bridge: Editor=Llama 3.3 70B/Groq + Judge=Gemini 2.5 Pro/Google + Red Team=GPT-OSS 120B/Groq); Editor + Judge READY_TO_LOCK; Red Team REQUIRES_FIXES (RT-01/02 HIGH; RT-03/04 MED; RT-05/06/07 LOW). Cycle-1 closures applied to amendment text + `pipeline/loop/track_registry.py` + `tests/loop/test_track_registry.py` (37 tests pass; +6 from Cycle-1 closures). Cycle-2 verification dispatched 2026-05-10 — unanimous READY_TO_LOCK across all three reviewers (Editor + Judge clean; Red Team `blocking: false / verdict: PASS` with RT-01/02/03/05/06/07 CLOSED + RT-04 REOPEN at MED + 5 NEW residuals NF-01..05 all MED/LOW non-blocking). Per L-005 strict-two-audit discipline, non-blocking residuals deferred to future spin per §10 OQ-9. F-PIPELINE-TRACK-FROZEN PRE-gate (architecture-side dormant per v7 §R.PF1) ACTIVATED against the LOCKED text of this amendment at lock time; F-PIPELINE-TRACK-FROZEN audit PASSED — registry exposes the v0.2 extension surface as R.PF1 demands; carve-out for grandfathered runners bounded by §7.19. Audit trail: `pipeline/validation/v5_v8_thesis_2026-05-10/`.
parent_lock: pipeline/blueprint/v0.1/section_05_pipeline.md (§5 v6 LOCKED 2026-04-19; §5 v7 amendment LOCKED 2026-05-02 row 132 — Red Team in inner loop)
companion_amendments:
  - pipeline/blueprint/v0.1/section_06_operating_envelope.md (§6.7 track-registry host schema, v1-r1 LOCKED 2026-04-21 — host schema is the upstream contract this amendment consumes)
architecture_parent: pipeline/architecture/v0.1/tilth_architecture_locked.md (v7 A1-A12 LOCKED 2026-04-19; §R.PF1 §5 Pipeline track-abstraction extensibility commitment; §6 Operating Envelope §A6 — track-registry mechanism host)
prerequisite_interlock: §6 v1-r1 LOCKED 2026-04-21 publishes the track-registry schema at §6.7. This amendment consumes that schema; §6 LOCK is a hard prerequisite.
discipline: L-005 two-audit + §13 audit-binding (R.PF1 dormant-PRE-gate-activation pattern); F-INDEX-STALE PRE-gate; Five Laws (§E)
bundling_rationale: §5 v8 is the §5 spin that LANDS R.PF1 — the v7 architectural pull-forward committing §5 to a track-registry abstraction such that adding a new track (`report` for R.3, `content` for R.2, `tdsl_query` for R.1, future tracks) is a router.yaml row + new prompt templates only. v8 ships with two ACTIVE tracks (`submission`, `eval`) plus one FORWARD-COMPAT row (`report`, shippable_in: v0.2) so the registry mechanism is exercised end-to-end at v0.1 LOCK without prematurely shipping R.3 reporting capability.
paired_commit_sec00_5: 12 new §0.5 rows for §5 v8 surface (1 module — `pipeline.loop.track_registry`; 1 dataclass — `Track`; 1 dataclass — `TrackRegistry`; 5 errors — `TrackRegistryError`, `RegistrySchemaError`, `TrackNotFound`, `TrackNotShippable`, `TrackShapeUnimplemented`; 4 functions — `load_track_registry`, `load_track_registry_from_yaml_text` [Cycle-1 RT-04 closure], `get_track`, `dispatch_track`). All STABLE tier; F-PIPELINE-TRACK-FROZEN remains DORMANT_UNTIL_SECTION_5_V8_LOCK on §0.5 row 112 until this amendment LOCKs (which flips the DORMANT_UNTIL to ACTIVE).
---

## Amendment intent

Architecture v7 §R.PF1 (LOCKED 2026-04-19) commits §5 Pipeline to a
**track-registry abstraction** such that:

> Adding a new track (`report` for R.3 reporting; `content` for R.2 content
> production; `tdsl_query` for R.1 TDSL lookup; future tracks) requires only
> a new router.yaml registry row + new prompt templates — **NOT a §5
> re-architecture, NOT a new §3 module per track, NOT a new §4.N mechanism
> per track.**

§5 v6 LOCKED 2026-04-19 hard-codes two entry points:

- `submission_mode` (RFA → council → signed bundle) — driver
  `pipeline/loop/run_pipeline.py`
- `eval_mode` (per-operator local calibration harness) — driver
  `pipeline/loop/run_eval_pipeline.py`

§1 Purpose, §3 Modules (`pipeline.loop.run_eval_pipeline`), and §4.15
Mechanism each bind these two modes by name. Adding a third mode (e.g.,
`report_mode` for v0.2 R.3) under v6's pattern would require §1 + §3 +
§4.N additions per track — exactly the re-architecture R.PF1 forbids.

§6 Operating Envelope v1-r1 LOCKED 2026-04-21 §6.7 publishes the host
track-registry schema. **This amendment is §5's adoption of that schema.**
F-PIPELINE-TRACK-FROZEN — the architecture-side dormant PRE-gate — wakes
at THIS amendment's LOCK time and audits the LOCKED text against R.PF1's
commitment. A v8 amendment that hard-codes `{submission, eval}` without
exposing the registry fails the audit.

This amendment is **narrow and bounded**:

1. **Adds §3 module `pipeline.loop.track_registry`** — registry loader +
   dispatcher. Owns the §6.7 schema-consumer surface. Ships with two
   active rows (`submission`, `eval`) and one forward-compat row
   (`report`, shippable_in: v0.2).
2. **Adds §3.2 dataclass `Track`** — frozen, kw_only, slots=True; one per
   registry row. Carries the §6.7 host-schema fields plus the R.PF1 §5
   follow-on bindings (Scribe prompt template, Judge rubric, Red Team
   probe template, vault subtree, output schema).
3. **Adds §3.2 dataclass `TrackRegistry`** — frozen, kw_only, slots=True;
   wraps the deterministic-order tuple of (name, Track) pairs.
4. **Adds §3.2 error class hierarchy** — `TrackRegistryError` base with
   four subclasses: `RegistrySchemaError`, `TrackNotFound`,
   `TrackNotShippable`, `TrackShapeUnimplemented`. Each carries a
   `F-PIPE-TRACK-*` trigger string.
5. **Adds §4.16 mechanism — track-agnostic dispatcher.** `dispatch_track`
   resolves a track name through the registry, enforces the
   `shippable_in` gate, and routes to the matching pipeline-shape
   implementation. Pipeline shapes that have no v0.1 implementation
   binding raise `TrackShapeUnimplemented` (fail-closed).
6. **Adds §6 failure-code prefixes** — `F-PIPE-TRACK-NOT-FOUND`,
   `F-PIPE-TRACK-NOT-SHIPPABLE`, `F-PIPE-TRACK-SHAPE-UNIMPLEMENTED`. These
   are runtime registry-lookup failures distinct from the architecture-
   side LOCK-time `F-PIPELINE-TRACK-FROZEN` audit gate.
7. **Adds §8 constant** `TILTH_VERSION_FAMILY: Final[str] = "v0.1"` with
   module-load integrity asserts (V1 inline-literal rebind-resistance
   pattern, mirroring TAB_ORDERING and EVAL_MODE_ALLOWED_INTENTS).
8. **Adds §9 tests** for the loader (well-formed + 11 malformed cases),
   the three-row dispatch (submission, eval, report stub), the
   shippable_in gate, and the on-disk router.yaml round-trip.
9. **Names but does NOT alter** the existing `pipeline.loop.run_pipeline`
   and `pipeline.loop.run_eval_pipeline` driver functions. R.PF1's
   commitment is that ADDING tracks is data-driven; v8 does not
   re-architect the existing tracks' implementations. The two existing
   capstones become *bindings the registry routes to*, addressed by their
   `pipeline_shape` strings.
10. **Reserves but does NOT implement** the `report` /
    `prior_commitments_to_council_to_signed_report` pipeline shape. R.3
    reporting is v0.2 horizon; the registry row is present in router.yaml
    so the schema is exercised, but `dispatch_track` refuses it at v0.1
    runtime via the `shippable_in: v0.2` gate.

This is a targeted amendment. Existing §5.1–§5.10 (submission run-
lifecycle), §4.12 (eval_mode), §4.15 (eval-mode entry point), §4.7
(POST-gate + council-split routing from v7), §5.6 (forward-dep
predicates), §5.7 (InvocationRecord schema from v6), §5.8 (STR
derivation), all failure codes F-PIPE-01 through F-PIPE-23, and all v5/
v6/v7 invariants are preserved without change. The amendment adds new
surface; it does not touch existing surface.

---

## §3 Modules — new module `pipeline.loop.track_registry`

Under `pipeline/loop/`:

| Path | Role |
|------|------|
| **(v8)** `pipeline/loop/track_registry.py` | §4.16 — registry loader (`load_track_registry`), YAML-text loader with duplicate-key detection (`load_track_registry_from_yaml_text`, Cycle-1 RT-04 closure), name lookup with shippable_in gate (`get_track`), track-agnostic dispatcher (`dispatch_track`), `Track` + `TrackRegistry` dataclasses, error hierarchy. Consumes the §6.7 host schema; produces frozen registry instances. |
| **(v8)** `tests/loop/test_track_registry.py` | §9.10 — four test classes: `TestTrackRegistryLoader` (schema validation), `TestThreeTrackDispatch` (submission/eval/report-stub routing), `TestRouterYamlOnDisk` (workspace router.yaml round-trip), `TestCycle1Closures` (RT-02 / RT-03 / RT-04 / RT-07 regression — 6 tests added 2026-05-10). |

The module is a pure-Python registry consumer with **no §4 Logician
internal imports** (R2 LOOP_LOGICIAN_BAN compliance) and **no direct file
I/O** (caller passes a parsed YAML mapping; the on-disk loader uses
`yaml.safe_load(Path.read_text())` at the dispatching call-site, not
inside the registry module).

---

## §3.2 Owned data structures

### §3.2.7 (NEW v8) `Track`

One per registry row. Fields per §6.7 host schema + R.PF1 §5 follow-on
bindings (the architecture-side commitment that each row binds (a)
Scribe prompt template, (b) Judge rubric, (c) Red Team probe template,
(d) vault subtree for output, (e) output schema).

```python
@dataclass(frozen=True, slots=True, kw_only=True)
class Track:
    name: str                      # registry key (e.g., "submission")
    kind: str                      # always "track" per §6.7
    pipeline_shape: str            # e.g. "rfa_to_council_to_signed_bundle"
    prompt_template_root: str      # e.g. "pipeline/prompts/submission/"
    failure_code_prefix: str       # e.g. "F-PIPE-SUBMIT-"
    cross_family_rigor: str        # "required" | "not_required"
    shippable_in: str              # e.g. "v0.1", "v0.2"
    # R.PF1 §5 follow-on bindings (architecture-side):
    scribe_prompt_template: str    # (a)
    judge_rubric_ref: str          # (b)
    red_team_probe_template: str   # (c)
    output_vault_subtree: str      # (d) — {org_slug}/{run_id} placeholders permitted
    output_schema: str             # (e) — schema name (e.g. "SubmissionBundle")
```

**Frozen-instance discipline.** `Track` is `frozen=True`; rebinding any
field after construction raises `dataclasses.FrozenInstanceError`. This
is the v0.1 instance of the rebind-resistance pattern (V1 / V5/MA-11)
applied at the dataclass layer.

### §3.2.8 (NEW v8) `TrackRegistry`

Frozen wrapper around the deterministic-order tuple of (name, Track)
pairs. Declaration order is preserved across YAML → dataclass parse so
audit replays are byte-stable.

```python
@dataclass(frozen=True, slots=True, kw_only=True)
class TrackRegistry:
    tracks: tuple[tuple[str, Track], ...]

    def as_mapping(self) -> Mapping[str, Track]: ...
    def names(self) -> tuple[str, ...]: ...
```

### §3.2.9 (NEW v8) Error class hierarchy

`TrackRegistryError` is the abstract base; four concrete subclasses
discriminate the failure path:

- `RegistrySchemaError` — loader-time: row malformed, missing required
  key, unknown key, kind != "track", invalid cross_family_rigor, empty
  string field. Per §6.7 the loader is fail-closed; unknown keys are
  rejected (silently swallowing them would defeat the
  F-PIPELINE-TRACK-FROZEN audit pattern at LOCK time).
- `TrackNotFound` — `dispatch_track` / `get_track` lookup miss.
  Trigger code: `F-PIPE-TRACK-NOT-FOUND`.
- `TrackNotShippable` — track row exists but `shippable_in` is later
  than `current_version`. Trigger code: `F-PIPE-TRACK-NOT-SHIPPABLE`.
  This is the §6.7 forward-compatibility safety: an operator cannot
  accidentally start a `shippable_in: v0.2` track on a v0.1 Tilth.
- `TrackShapeUnimplemented` — track's `pipeline_shape` has no v0.1
  implementation binding (or the matching runner argument was not
  supplied). Trigger code: `F-PIPE-TRACK-SHAPE-UNIMPLEMENTED`. Distinct
  from `TrackNotShippable`: a row may be marked `shippable_in: v0.1`
  but reference a forward-compat `pipeline_shape` string.

---

## §4.16 (NEW v8) — Track-registry mechanism

**Purpose.** §4.16 publishes the data-driven binding §5 Pipeline
consumes to dispatch a council round under one of N tracks. Each
registry row binds a track name to its prompt templates, rubric, probe
template, vault subtree, and output schema. §5 itself becomes
track-agnostic at the dispatcher boundary; per-track behavior lives in
the prompt templates and (transparently) in the
implementation-bound pipeline-shape function.

**Registry source.** `router.yaml` under §6 Operating Envelope publishes
a top-level `tracks:` mapping (per §6.7 schema). This amendment does
NOT mandate where in `router.yaml` the section appears; it only
mandates the schema. The workspace router.yaml at §5 v8 LOCK ships:

```yaml
tracks:
  submission:
    kind: track
    pipeline_shape: rfa_to_council_to_signed_bundle
    prompt_template_root: pipeline/prompts/submission/
    failure_code_prefix: F-PIPE-SUBMIT-
    cross_family_rigor: required
    shippable_in: v0.1
    scribe_prompt_template: pipeline/prompts/submission/scribe.md
    judge_rubric_ref: pipeline/rubrics/vapg_fy26.json
    red_team_probe_template: pipeline/prompts/submission/red_team_probe.md
    output_vault_subtree: orgs/{org_slug}/vault/submissions/{run_id}/
    output_schema: SubmissionBundle

  eval:
    kind: track
    pipeline_shape: operator_harness_to_per_seat_calibration
    prompt_template_root: pipeline/prompts/eval/
    failure_code_prefix: F-PIPE-EVAL-
    cross_family_rigor: not_required
    shippable_in: v0.1
    scribe_prompt_template: pipeline/prompts/eval/scribe.md
    judge_rubric_ref: pipeline/rubrics/vapg_fy26.json
    red_team_probe_template: pipeline/prompts/eval/red_team_probe.md
    output_vault_subtree: orgs/{org_slug}/golden_set/calibration_reports/
    output_schema: CalibrationReport

  report:
    # v0.2 R.3 forward-compat row. Present in registry; refused at
    # dispatch time per shippable_in: v0.2.
    kind: track
    pipeline_shape: prior_commitments_to_council_to_signed_report
    prompt_template_root: pipeline/prompts/report/
    failure_code_prefix: F-PIPE-REPORT-
    cross_family_rigor: required
    shippable_in: v0.2
    scribe_prompt_template: pipeline/prompts/report/scribe.md
    judge_rubric_ref: pipeline/rubrics/proposal_commitments.json
    red_team_probe_template: pipeline/prompts/report/red_team_probe.md
    output_vault_subtree: orgs/{org_slug}/vault/reports/{run_id}/
    output_schema: GrantReport
```

**Loader contract — `load_track_registry(source: Mapping[str, Any]) -> TrackRegistry`.**

1. `source` MUST be a mapping; reject otherwise with `RegistrySchemaError`.
2. `source.tracks` MUST exist, be a non-empty mapping; reject otherwise.
3. Each row's key MUST be a non-empty string with no duplicates.
4. Each row MUST carry exactly the eleven keys in `_REQUIRED_TRACK_KEYS`
   (six §6.7 host-schema fields + five R.PF1 follow-on bindings).
   Missing keys → `RegistrySchemaError`. Unknown keys →
   `RegistrySchemaError` (forward-compat extensions require a §5 spin
   per R.PF1).
5. `kind` MUST equal the literal `"track"`.
6. `cross_family_rigor` MUST be `"required"` or `"not_required"`.
7. All eleven string fields MUST be non-empty.
8. **(Cycle-1 RT-03 closure)** `output_vault_subtree` MUST contain the
   substring `"{org_slug}"`; otherwise `RegistrySchemaError`. This is the
   loader-side enforcement of §7.20 (per-org rendering placeholder is a
   Law-3 isolation invariant; a row that omits the placeholder would
   silently render to a workspace-shared path).

The returned registry is frozen; its `as_mapping()` method returns a
fresh defensive-copy dict view; its `names()` method returns the
declaration-order tuple of names.

**YAML-text loader contract (Cycle-1 RT-04 closure) —
`load_track_registry_from_yaml_text(yaml_text: str) -> TrackRegistry`.**

PyYAML's default `safe_load` silently overwrites duplicate mapping keys
at the parser level. By the time `load_track_registry`'s `seen` set sees
the parsed mapping, only the LAST occurrence of any duplicate key
survives — so the in-mapping duplicate-detection logic is dead code for
the YAML-text input case. An attacker (or a careless operator) could
craft a `router.yaml` where `submission:` appears twice with differing
values; the on-disk loader call-site would silently accept the last
occurrence and the duplicate-detection in `load_track_registry` would
never fire.

`load_track_registry_from_yaml_text` installs a strict `SafeLoader`
subclass with a custom mapping constructor that raises
`RegistrySchemaError` on any duplicate mapping key inside the document
— at the `tracks:` level OR at any nested mapping level (e.g., a
duplicate `shippable_in:` inside one row). Trigger string:
`F-PIPE-TRACK-REGISTRY-DUPLICATE-KEY` (folded into `RegistrySchemaError`
surface; not promoted to a top-level F-PIPE-TRACK-* code per §6 row
table — the duplicate-key case is loader-side schema malformation, not
a runtime registry-lookup failure).

**The on-disk loader call-site (loading workspace router.yaml at
pipeline startup) MUST use `load_track_registry_from_yaml_text` rather
than calling `yaml.safe_load` directly.** The in-mapping
`load_track_registry(source: Mapping)` continues to accept synthetic
test fixtures where the caller has already constructed the mapping; the
duplicate-detection is then defense-in-depth (a programmatically
constructed mapping cannot carry duplicate keys, but the explicit check
defends against future introspection-based mapping construction).

**Lookup contract — `get_track(registry, name, *, current_version) -> Track`.**

1. If `name` is not in the registry → raise `TrackNotFound`.
2. If `track.shippable_in > current_version` (lexicographic compare on
   `vM.N` strings) → raise `TrackNotShippable`.
3. Otherwise return the `Track`.

`current_version` defaults to `TILTH_VERSION_FAMILY` (the
constant pinned at module load); tests pass synthetic values to
exercise the forward-compat path.

**Dispatcher contract — `dispatch_track(registry, name, *, current_version, submission_runner, eval_runner, submission_kwargs, eval_kwargs) -> Any`.**

1. Resolve `name` via `get_track` (which enforces the shippable_in gate).
2. If `track.pipeline_shape` is not in `_V0_1_IMPLEMENTED_SHAPES`
   (= `{"rfa_to_council_to_signed_bundle",
       "operator_harness_to_per_seat_calibration"}`) → raise
   `TrackShapeUnimplemented`.
3. If shape is `rfa_to_council_to_signed_bundle`: invoke
   `submission_runner(**submission_kwargs)`. Production wires
   `pipeline.loop.run_pipeline.run_pipeline_5_seat`.
4. If shape is `operator_harness_to_per_seat_calibration`: invoke
   `eval_runner(**eval_kwargs)`. Production wires
   `pipeline.loop.run_eval_pipeline.run_eval_pipeline`.
5. Both runners are passed via dependency injection (E-017 pattern); a
   missing runner argument fails-closed with `TrackShapeUnimplemented`.
6. **Dispatch is BY `pipeline_shape`, NOT by which runners the caller
   supplies.** (Cycle-1 RT-07 closure.) Supplying a `submission_runner`
   to a track whose `pipeline_shape` is
   `operator_harness_to_per_seat_calibration` results in
   `submission_runner` being unused (no leak); the eval-shape branch
   fires (or fails-closed if `eval_runner=None`). Conversely, supplying
   `eval_runner` to a submission-shape track does not cause the eval
   runner to fire on submission data. The dispatcher's safety property
   is "shape decides; supply does not."
7. **(Cycle-1 RT-02 closure — runtime-rebind sentinel.)** The `if/elif`
   chain in steps 3-4 names exactly the two grandfathered shapes. If
   `_V0_1_IMPLEMENTED_SHAPES` is monkey-patched at runtime to admit a
   third shape (a documented attack surface — the module-load assert in
   §8 only fires at import), the gate at step 2 admits the new shape,
   but neither if-arm matches it, so dispatch falls through to a
   defensive raise of `TrackShapeUnimplemented` carrying the literal
   message `"_V0_1_IMPLEMENTED_SHAPES has been rebound at runtime"`.
   This is the **runtime sentinel** complementing the module-load
   assert: even with a successful monkey-patch, dispatch fail-closes.
   Future refactors (Judge DC-01, deferred — see §10 OQ-8) that
   introduce a `runners: Mapping[str, Callable]` lookup MUST preserve a
   semantically-equivalent runtime sentinel before retiring the
   `if/elif` chain.

**Adding a new track at v0.2 (the R.PF1 commitment).** Adding `report`,
`content`, or `tdsl_query` as v0.2 active tracks requires:

(a) Append the row to `router.yaml` `tracks:` with `shippable_in: v0.2`
    or whatever current Tilth version supports it.
(b) Add the per-seat prompt templates at the declared
    `prompt_template_root`.
(c) Add the rubric JSON / probe template files at the declared paths.
(d) If the track introduces a NEW pipeline_shape (e.g.,
    `prior_commitments_to_council_to_signed_report`), implement that
    shape's runner function and bind it via a new `report_runner`
    argument added to `dispatch_track`. **Adding a new pipeline_shape
    binding is a §5 spin** — it's the only step that touches §5 code,
    and R.PF1 explicitly permits it (the commitment is "no §3 module
    per track" + "no §4.N mechanism per track", not "no new shape
    binding ever"). A track that REUSES an existing shape (e.g., a v0.2
    sector-tuned submission flow that shares
    `rfa_to_council_to_signed_bundle`) requires zero §5 code changes.

**F-PIPELINE-TRACK-FROZEN audit at this amendment's LOCK.** §6.7
publishes the dormant PRE-gate: at v8 LOCK time, the gate scans §5's
LOCKED text AND `pipeline/loop/run_*.py` for hard-coded track-by-name
references outside the registry loader. The v8 implementation:

- **Inside the registry loader** (`pipeline/loop/track_registry.py`):
  the literal strings `"submission"`, `"eval"`, `"report"` appear as
  YAML keys in fixtures, error messages, and known-shape names. This
  is THE registry loader and is exempt by definition.
- **Outside the registry loader, inside the grandfathered runners**:
  the §5 v6 / v7 code (`run_pipeline`, `run_eval_pipeline`) carries
  inline-literal `"submission"` and `"eval"` mode gates as defence-in-
  depth. Per §6.7's audit semantics these are **track-shape
  implementation internals**, not registry-dispatch references —
  analogous to a function's local `if/elif` on a discriminated union.
  v8 does NOT touch these code paths; refactoring them would be a
  separate spin (R12.B is already at capstone scope; further compression
  is post-v0.1). **(Cycle-1 RT-01 closure — carve-out is bounded, not
  open-ended.)** The two grandfathered literals are the ONLY track-by-
  name literals permitted in `pipeline/loop/run_*.py`. §7.19 (NEW v8)
  freezes this bound: no THIRD track-by-name literal may be introduced
  in any `pipeline/loop/run_*.py` after v8 LOCK. A v0.2 author adding
  `if mode == "report": ...` to `run_pipeline.py` to dodge the registry
  is an architectural violation, scanned against §7.19 by the LOCK-time
  gate of any subsequent §5 spin.

The audit obligation is therefore that v8 EXPOSES the registry such
that **future tracks** can be added without §5 refactoring **AND** that
no new mode-string match arms accumulate inside the grandfathered
runners. The existing run_pipeline / run_eval_pipeline mode-gates are
existing implementation; what matters is that the dispatcher path is
registry-driven going forward AND that the dodge-via-runner-internals
escape hatch is closed.

---

## §6 Failure codes — three new

| Code | Sub-trigger | When | Severity | Save-state | Test |
|------|-------------|------|----------|------------|------|
| **F-PIPE-TRACK-NOT-FOUND** | _registry-lookup-miss_ | `dispatch_track` / `get_track` asked for a name not in registry | INFO (caller error) | None — caller-side error before any state | §9.10 `test_unknown_track_raises_track_not_found` |
| **F-PIPE-TRACK-NOT-SHIPPABLE** | _shippable_in-gate-deny_ | `track.shippable_in > current_version` | INFO (forward-compat safety) | None — no state minted yet | §9.10 `test_report_track_refused_at_v0_1_via_shippable_gate` |
| **F-PIPE-TRACK-SHAPE-UNIMPLEMENTED** | _shape-not-in-implemented-set_ OR _runner-not-supplied_ | `track.pipeline_shape ∉ _V0_1_IMPLEMENTED_SHAPES` OR submission_runner / eval_runner is `None` | CRIT — fail-closed | None — no state minted yet | §9.10 `test_report_track_dispatchable_at_v0_2_but_shape_unimplemented` + the two `*_dispatch_without_*_runner_fails_closed` tests |

These are runtime registry-lookup failures, NOT the LOCK-time
F-PIPELINE-TRACK-FROZEN audit gate (which is architecture-side per
§6.7). The two are complementary: F-PIPELINE-TRACK-FROZEN audits the
SOURCE TEXT of §5 LOCKs; the F-PIPE-TRACK-* family handles RUNTIME
lookup failures.

---

## §7 Invariants — six new (three from initial draft + three from Cycle-1 closures)

- **§7.16 (v8) Registry source-of-truth.** The track-registry consumed
  by `dispatch_track` MUST be loaded from `router.yaml`'s `tracks:`
  mapping (or a test fixture mirroring the same schema). No code path
  may construct a `Track` or `TrackRegistry` from inline-literal
  arguments at runtime (defence-in-depth — the test fixtures
  themselves go through `load_track_registry`).
- **§7.17 (v8) Frozen-instance discipline.** `Track` and
  `TrackRegistry` are both `frozen=True`; mutation attempts raise
  `FrozenInstanceError`. This is the §3.2.7 / §3.2.8 invariant
  re-asserted at the §7 invariant layer.
- **§7.18 (v8) shippable_in monotonicity.** A track's `shippable_in`
  MAY only be lowered (made more permissive) across §5 spins, never
  raised. v0.1 → v0.2 promotion is fine; v0.1 → v0.2 demotion of a
  previously-shipped track is forbidden (it would silently brick
  in-flight runs on the older Tilth version). This invariant is a
  LOCK-time audit obligation, not a runtime gate.
- **§7.19 (v8 — Cycle-1 RT-01 closure) No new track-by-name literals
  in grandfathered runners.** The two existing track-by-name inline
  literals — `pipeline/loop/run_pipeline.py:"submission"` and
  `pipeline/loop/run_eval_pipeline.py:"eval"` — are the ONLY track-by-
  name literals permitted in any `pipeline/loop/run_*.py` after v8
  LOCK. Adding a third track-by-name literal (e.g.,
  `if mode == "report": ...` inside `run_pipeline.py`) is an
  architectural violation that bypasses the data-driven registry. The
  F-PIPELINE-TRACK-FROZEN audit at any subsequent §5 spin LOCK-time
  scans BOTH §5 blueprint text AND `pipeline/loop/run_*.py` for new
  literal additions. Mechanical AST-lint enforcement is deferred to a
  future spin (see §10 OQ-6); v0.1 LOCK relies on this textual
  invariant + the F-PIPELINE-TRACK-FROZEN audit. New tracks integrate
  via the `dispatch_track` DI seam (extending `_V0_1_IMPLEMENTED_SHAPES`
  and adding a runner argument), which is the only §5 code change R.PF1
  permits per §4.16 "Adding a new track at v0.2" subsection.
- **§7.20 (v8 — Cycle-1 RT-03 closure) `output_vault_subtree` MUST
  contain `{org_slug}` placeholder.** Every registry row's
  `output_vault_subtree` field MUST contain the literal substring
  `"{org_slug}"`. The placeholder is the binding point at which the
  rendering site (existing §2 vault-write CAS-and-Cedar discipline)
  enforces per-org isolation under Law 3. A row that omits the
  placeholder would silently render to a workspace-shared path and
  breach Law 3. Loader-side enforcement (see §4.16 loader contract
  clause 8) raises `RegistrySchemaError` at parse time; runtime
  rendering does not need to re-check (the value is already validated
  in the frozen `Track`).
- **§7.21 (v8 — Cycle-1 RT-05 closure documentation) `shippable_in`
  lex-compare bounded by single-major-version assumption.** The
  lexicographic compare in `get_track` between `shippable_in` and
  `current_version` is correct ONLY for `vM.N` strings where `M` is
  fixed across the comparison. The current implementation is NOT safe
  beyond single-digit majors: `"v1.0"` lex-compares less-than
  `"v0.9"` because `"1" < "0"` is false but `"v1.0" > "v0.9"` returns
  the wrong result for naive monotonic-version intent (`"v0.10"` also
  lex-compares less-than `"v0.9"` because `"0.10" < "0.9"` lex). This
  is acceptable at v0.1 because the only versions in flight are `v0.1`
  and `v0.2` and both share the same major; any spin that crosses
  `v0.9 → v0.10` or `v0.x → v1.0` MUST upgrade `get_track` to a strict
  version-tuple compare (e.g.,
  `tuple(int(p) for p in v.lstrip("v").split("."))`) before the spin
  LOCKs. Pre-condition tracked at §10 OQ-4.

---

## §8 Constants — one new

| Constant | Value | Reason |
|----------|-------|--------|
| **(v8)** `TILTH_VERSION_FAMILY: Final[str] = "v0.1"` | `"v0.1"` | §6.7 forward-compatibility safety: v0.1 Tilth refuses to dispatch a `shippable_in: v0.2` track. The constant pins the v0.1 self-version for the shippable_in gate. At v0.2 LOCK, the constant moves with the Tilth release. Module-load integrity assert pattern (V1) — `assert _V0_1_IMPLEMENTED_SHAPES == frozenset({"rfa_to_council_to_signed_bundle", "operator_harness_to_per_seat_calibration"})` and `len(...) == 2` rebind-resistance (mirrors `EVAL_MODE_ALLOWED_INTENTS` discipline). |

---

## §9 Tests — one new section §9.10

`tests/loop/test_track_registry.py` ships three test classes:

### §9.10.1 `TestTrackRegistryLoader` (schema validation, 14 tests)

- `test_well_formed_loads_three_tracks` — happy path
- `test_loaded_tracks_are_frozen_dataclasses` — frozen-instance assertion
- `test_loaded_track_carries_all_eleven_fields` — all R.PF1 + §6.7
  fields are present
- `test_source_must_be_a_mapping` — schema-error on non-mapping
- `test_source_must_have_tracks_key` — schema-error on missing
  `tracks:` key
- `test_tracks_must_be_a_mapping` — schema-error on non-mapping tracks
- `test_empty_tracks_rejected` — schema-error on empty tracks mapping
- `test_row_must_be_a_mapping` — schema-error on non-mapping row
- `test_row_missing_required_key` — schema-error on missing required key
- `test_row_with_unknown_key_rejected` — schema-error on extra key
  (forward-compat-extension hard-stop)
- `test_row_kind_must_be_track` — schema-error on `kind != "track"`
- `test_row_cross_family_rigor_must_be_in_closed_set` — schema-error on
  unknown rigor value
- `test_row_string_field_must_be_non_empty` — schema-error on empty str
- `test_row_string_field_must_be_string` — schema-error on non-str type
- `test_track_names_preserved_in_declaration_order` — order stability

### §9.10.2 `TestThreeTrackDispatch` (dispatcher routing, 11 tests)

- `test_submission_track_routes_to_submission_runner` — happy path
- `test_eval_track_routes_to_eval_runner` — happy path
- `test_report_track_refused_at_v0_1_via_shippable_gate` — the §6.7
  forward-compat safety
- `test_report_track_dispatchable_at_v0_2_but_shape_unimplemented` — at
  v0.2 the shippable_in gate passes but the unimplemented shape gate
  catches
- `test_unknown_track_raises_track_not_found`
- `test_submission_dispatch_without_submission_runner_fails_closed`
- `test_eval_dispatch_without_eval_runner_fails_closed`
- `test_dispatch_kwargs_default_to_empty`
- `test_get_track_shippable_gate_directly` — direct get_track exercise
- `test_get_track_unknown_name_raises`

### §9.10.3 `TestRouterYamlOnDisk` (workspace round-trip, 6 tests)

- `test_workspace_router_yaml_parses_into_registry` — the on-disk file
  parses cleanly
- `test_workspace_router_yaml_submission_is_v0_1_shippable`
- `test_workspace_router_yaml_eval_is_v0_1_shippable`
- `test_workspace_router_yaml_report_is_v0_2_forward_compat`
- `test_workspace_router_yaml_failure_code_prefixes_unique`
- `test_workspace_router_yaml_prompt_roots_unique`

### §9.10.4 (Cycle-1 closures) `TestCycle1Closures` (RT-02 / RT-03 / RT-04 / RT-07 regression, 6 tests)

- `test_output_vault_subtree_must_contain_org_slug_placeholder` — RT-03 fail-closed
- `test_output_vault_subtree_with_org_slug_anywhere_passes` — RT-03 happy
- `test_yaml_text_with_duplicate_track_keys_is_rejected` — RT-04 fail-closed
- `test_yaml_text_well_formed_loads` — RT-04 happy
- `test_rebind_to_admit_new_shape_caught_by_dispatcher_fallthrough` — RT-02 runtime sentinel
- `test_dispatch_uses_pipeline_shape_not_caller_runner_supply` — RT-07 dispatch-by-shape

**Total v8 test additions: 37 (across the four classes — 31 from the
initial draft plus 6 from Cycle-1 closures).**

---

## §10 Open Questions for Thesis attention

1. **Registry source path — single source-of-truth or per-deployment derivation?**
   Per CLAUDE.md and v7.0.7 amendment, router.yaml is a per-deployment
   template derived at white-glove onboarding. This means the
   workspace's `router.yaml` is the dev-node source of truth, and
   each customer Golden Quill has its own `router.yaml` derived from
   it + their classification register + SN-LLC's current best-of-
   breed cloud routing template. **Question:** does the track-
   registry travel with the per-deployment derivation, or is it
   pinned at the SN-LLC release layer (i.e., new tracks ship via
   SN-LLC router-template updates only)? Author's preliminary
   recommendation: SN-LLC pins the track set at release; per-
   deployment derivation only swaps in the operator's classification-
   driven seat bindings. Tracks are a global product surface, not a
   per-customer toggle.

2. **`pipeline_shape` enum vocabulary as v8 closed set?** The closed
   set `_V0_1_IMPLEMENTED_SHAPES` currently lives as a frozenset
   constant in `pipeline/loop/track_registry.py`. The v8 LOCK pins it
   at two values; future v0.2 spins extend it. **Question:** should
   the closed set move to §0.5 Interface Index as a primitive_kind
   row, so D-05 audit catches drift? Author preference: yes, but
   that's a §0.5 v9 amendment scoped to v0.2 work — out of scope for
   this v8 LOCK.

3. **Forward-compat row count — three or one at v8 LOCK?** R.PF1
   names three forward-compat tracks (`report`, `content`,
   `tdsl_query`). v8 ships only the `report` row (R.3 reporting is
   the highest-value v0.2 vertical per `project_report_vertical.md`).
   **Question:** should v8 ship all three forward-compat rows, or
   only `report`? Author preference: ship only `report` (the next
   active track); shipping all three risks over-committing to
   pipeline_shape names that v0.2 spins might rename. The schema
   accommodates additions — adding `content` and `tdsl_query` rows
   later is a router.yaml append, not a §5 spin.

4. **Lexicographic `shippable_in` comparison — adequate at v0.1?** The
   `v0.1 < v0.2 < ... < v0.9` comparison is correct lexicographically.
   The `v1.0` ordering swap (where lex-compare would say `"v0.9" >
   "v1.0"` if either party were missing leading-zero padding) is out
   of v0.1 scope. **Question:** flag this as a §5 next-spin obligation
   if v0.1 → v1.0 ever crosses, or live with the implicit
   single-major-version invariant? Author preference: live with it —
   v1.0 is far horizon and any version-comparison logic upgrade is
   trivial when needed.

5. **The existing `"submission"` / `"eval"` inline-literal mode gates
   in `run_pipeline.py` / `run_eval_pipeline.py` — refactor to
   registry lookups now or defer?** Current state: the mode literals
   are used as defence-in-depth shields (e.g., `_assert_eval_mode_intent`,
   `assert run_state.mode == "submission"`). v8 does NOT touch them.
   **Question:** does F-PIPELINE-TRACK-FROZEN's "no track-by-name
   hardcodes outside the registry loader" interpretation REQUIRE
   these to be refactored? Author position (see §4.16 audit
   discussion): no — these are pipeline-shape-implementation
   internals, analogous to a function's `if/elif` on a discriminated
   union. The R.PF1 commitment is about ADDING tracks, not about
   eliminating every literal mention of "submission" / "eval" in the
   v0.1 codebase. **Cycle-1 disposition (RT-01 closure):** Red Team
   confirmed the carve-out reading but flagged that it is exploitable
   if open-ended (a v0.2 author could add a third literal "just inside
   the runner" and dodge F-PIPELINE-TRACK-FROZEN). The carve-out is
   now BOUNDED by §7.19 (NEW v8): exactly the two existing literals
   are grandfathered; any third literal is an architectural violation.
   F-PIPELINE-TRACK-FROZEN audit scope is widened to scan
   `pipeline/loop/run_*.py` in addition to §5 blueprint text.

6. **(NEW Cycle-1) AST-lint rule for §7.19 mechanical enforcement.**
   §7.19 freezes the carve-out at exactly the two grandfathered
   literals, but enforcement is currently textual: F-PIPELINE-TRACK-
   FROZEN audit scans the LOCKED text + the runner files at LOCK
   time. A mechanical AST-lint rule
   (`R-PIPE-TRACK-NO-NEW-MODE-LITERAL`) that flags any new
   `if/elif/match` arm matching a track-name literal in
   `pipeline/loop/run_*.py` would catch violations on every commit
   rather than only at LOCK time. Author preference: deferred to a
   v0.2 §4 Logician spin (the AST-lint substrate already exists per
   §12 Uploader v1's `R-UPLOADER-NO-SUBMIT` precedent — the rule is
   one more entry in `pipeline/linting/ast_lint.py`). Not a v8 LOCK
   blocker.

7. **(NEW Cycle-1) RT-06 declined — `x_`-prefix forward-compat key
   relaxation.** Red Team proposed allowing `x_`-prefixed keys to be
   silently ignored as a forward-compat extension path. **Author
   declined.** Strict-key-rejection is the load-bearing R.PF1
   commitment per §4.16 loader contract clause 4. Allowing `x_` keys
   would defeat the F-PIPELINE-TRACK-FROZEN audit's ability to detect
   schema drift. §6.7 host-schema extensions are a §6 + §5 paired-
   spin event by design (when §6.7 v2 adds a new field, §5 v9 spins
   simultaneously to consume it; this is the intended discipline, not
   a friction to optimize away).

8. **(NEW Cycle-1) Judge DC-01 deferred — `runners` as Mapping for
   future-proofing.** Judge surfaced that `dispatch_track`'s explicit
   `submission_runner` / `eval_runner` arguments will accumulate as
   v0.2+ shapes ship. A future refactor passing
   `runners: Mapping[str, Callable]` and looking up by
   `track.pipeline_shape` would stabilize the function signature.
   **Deferred to a post-v0.1 spin per Judge's own non-blocking
   classification.** Constraint imposed by §4.16 dispatcher contract
   clause 7: any such refactor MUST preserve the runtime-rebind
   sentinel that the current `if/elif` chain provides as a side-
   effect (e.g., by validating the looked-up callable's identity
   against a checksum or a registry-of-runners dataclass). Tracked so
   the future spin does not retire the sentinel by accident.

9. **(NEW Cycle-2) Non-blocking residuals from Audit #2 — deferred
   to future spin.** Cycle-2 verification dispatch surfaced one
   REOPEN at MED + five NEW MED/LOW residuals beyond the seven
   Cycle-1 closures. Red Team explicitly classified `blocking: false`
   and verdict `PASS`. Per L-005 strict-two-audit discipline these
   residuals do NOT trigger a Cycle 3; they are tracked here for a
   future §5 spin or paired Logician/AST-lint amendment.

   - **RT-04 REOPEN (MED) — non-mechanical enforcement of "MUST use
     `load_track_registry_from_yaml_text`" discipline.** No on-disk
     `yaml.safe_load` call-site exists yet for `router.yaml`, so
     v0.1 LOCK has no live violation. Future spin: add an AST-lint
     rule `R-PIPE-NO-RAW-YAML-FOR-ROUTER` that flags any
     `yaml.safe_load` call whose argument string contains
     `router.yaml`, OR introduce a thin wrapper module
     `pipeline.loop.router_yaml` that owns the on-disk read path
     and refuses to be bypassed. Bundle with §10 OQ-6 AST-lint
     deferral.
   - **NF-01 (MED) — direct `Track` construction bypasses schema
     validation.** §7.16 already enjoins this at the invariant
     layer; mechanical enforcement via `Track.__post_init__`
     (re-running the eleven-field + `{org_slug}` check at every
     instance construction site) is the deferred fix. Trade-off:
     `__post_init__` validation runs at every test-fixture
     construction and may complicate the dataclass hierarchy
     (e.g., synthetic test instances built field-by-field). Decide
     at the future spin whether to (a) add `__post_init__`
     unconditionally, (b) gate it behind a module-level flag
     defaulting to enforce-at-runtime, or (c) ship a builder
     factory that funnels all `Track` construction through it.
   - **NF-02 (LOW) — same theme as RT-04 REOPEN (documentation-
     only enforcement).** Bundle with RT-04 REOPEN closure.
   - **NF-03 (LOW) — false alarm.** Red Team posited that
     `"{org_slug}" in s` accepts `"{org_slug"` (missing closing
     brace). It does not — the substring `"{org_slug}"` is the
     full seven-character literal including the closing brace, so
     a path missing the closing brace fails the check. Recording
     here so future reviewers do not re-raise it.
   - **NF-04 (LOW) — §7.19 wording assumes runner names remain
     static.** If a future refactor introduces a constant
     indirection (`MODE_SUBMISSION = "submission"; if mode ==
     MODE_SUBMISSION:`), the freeze-on-string-literal would not
     catch the indirection. Doc-only strengthening recommended in
     a future spin: extend §7.19 to cover "any
     track-mode-discrimination pattern" (string literal, named
     constant, enum value, match-statement arm) inside
     `pipeline/loop/run_*.py`. v0.1 ships with no such indirection
     in the grandfathered runners; the gap is a doc precision
     issue, not a live attack surface.
   - **NF-05 (LOW) — test coverage gap on nested duplicate keys.**
     The `_NoDuplicatesSafeLoader` mapping constructor handles ANY
     duplicate at any depth (its `if key in mapping` check fires
     uniformly), but the test suite only exercises top-level
     duplicate track names. Easy add of a regression test
     `test_yaml_text_with_nested_duplicate_keys_is_rejected`
     deferred to a future spin (or to §11 Intake's spin if it
     extends the YAML loader pattern).

---

## §11 Law map

| Law | v8 surface |
|-----|------------|
| Law 1 (RFA Is Truth) | `Track.scribe_prompt_template` references the funder dialect; the registry binds, does not author. |
| Law 2 (No Boundary Drift) | `Track.judge_rubric_ref` binds the rubric; runtime cannot substitute another rubric. |
| Law 3 (Org Isolation) | `Track.output_vault_subtree` carries `{org_slug}` placeholder; per-org isolation enforced at the rendering site (existing §2 vault-write CAS-and-Cedar discipline). |
| Law 4 (Apolitical / Admin-Risk) | The registry is content-blind; admin-risk scanning runs against rendered prompts, not template references. |
| Law 5 (Applicant Brings Substance) | The registry binds templates only; applicant data flows through the existing Scribe / Editor / Judge / Red Team pipeline. |

---

## §12 Non-ownership

§5 v8 amendment does NOT own:

- §6.7 host-schema definition (owned by §6 Operating Envelope; v8
  consumes).
- The on-disk `router.yaml` document layout (owned by §6 + the
  workspace deployment).
- The per-shape pipeline implementation (owned by `run_pipeline.py`
  and `run_eval_pipeline.py`; v8 binds them via dispatcher).
- The §0.5 Interface Index row format (owned by §0.5; v8 paired-commit
  appends rows).
- The F-PIPELINE-TRACK-FROZEN architectural PRE-gate (owned by
  architecture v7 §R.PF1; activated AT v8 LOCK time, not by v8).

---

## §13 Closure

§5 v8 LANDS the architectural pull-forward R.PF1. v0.1 ships:

- two ACTIVE tracks (`submission`, `eval`) consumed via the registry
- one FORWARD-COMPAT row (`report`, refused at runtime via
  `shippable_in: v0.2`)
- the registry mechanism itself, exercised by **37 new tests** (31 from
  the initial draft + 6 from Cycle-1 closures) + the workspace
  `router.yaml` round-trip
- the YAML-text loader helper `load_track_registry_from_yaml_text` that
  rejects duplicate mapping keys at parse time (Cycle-1 RT-04 closure)
- six new §7 invariants (three from initial draft + three from Cycle-1
  closures: §7.19 carve-out bounded; §7.20 `{org_slug}` placeholder;
  §7.21 lex-compare hazard documented)

v0.2 R.3 reporting becomes a router.yaml row + new prompt templates +
one new pipeline-shape runner binding (the `prior_commitments_*` shape).
v0.2 R.2 content production and v0.2 R.1 TDSL query each follow the
same shape: a row + templates + a runner binding for any new shape.
**No §3 module per track. No §4.N mechanism per track. No new
track-by-name literal in any `pipeline/loop/run_*.py` (§7.19).** R.PF1
honored.

---

## Compound-commit interaction (v0.1 architectural invariant)

Per `pipeline/engineering/spec_cards/compound_commit.md` and §2 v7.1
§4.10.7, the LOCK of §5 v8 is itself a compound transaction:
`{section_05_v8_amendment.md, section_00_5_section_05_v8_amendment.md}`
MUST commit atomically via the §2 vault dispatcher's
`commit_compound_txn()` entry point with `kind = index_amendment`.

Hash-binding rule per §4.11 predicate: the §0.5 v8 amendment's
`section_05_v8_anchor_hash` field MUST equal SHA-3-512(§5 v8 file bytes).
The §0.5 amendment is not yet authored at this DRAFT stage — it lands
at LOCK as the paired commit (11 rows: 1 module + 1 dataclass + 1
dataclass + 5 errors + 3 functions, all STABLE tier).

---

## What Audit #1 must verify (Cowork Thesis phase)

Per `pipeline/planning/v0_2_dispatch_plan_2026-05-09.md` §WS-G Cowork
phase: L-005 two-audit cycle, cross-family per WS-B (osascript →
openclaw bridge; Editor on Llama 3.3 70B; Judge on Gemini 2.5 Pro;
Red Team on GPT-OSS 120B).

F-PIPELINE-TRACK-FROZEN architectural commitment is the audit rubric:

1. **Does the amendment expose the registry such that report_mode
   (and content_mode, tdsl_query_mode) registers via row + prompt
   template only?** — verify §4.16 reads this way and that the
   loader / dispatcher do not hard-code a closed track set
   beyond `_V0_1_IMPLEMENTED_SHAPES` (which is closed-but-extension-
   safe per §10 Open Question 2).
2. **Does the amendment hard-code a closed track set?** — verify
   `_V0_1_IMPLEMENTED_SHAPES` is the only closed set, that it carries
   exactly two members at v0.1, and that the dispatcher's fall-
   through path raises `TrackShapeUnimplemented` rather than
   defaulting to a hard-coded route.
3. **Does the runtime registry-lookup failure family
   (F-PIPE-TRACK-*) replace or merely complement the LOCK-time
   F-PIPELINE-TRACK-FROZEN audit gate?** — verify §6 Failure-codes
   table makes the distinction explicit.
4. **Does §10 OQ-5 read defensibly?** — the existing `"submission"`
   / `"eval"` inline-literal mode gates are NOT being refactored at
   v8; verify the audit accepts the "pipeline-shape implementation
   internals" reading or surfaces a residual.
5. **Does the workspace router.yaml round-trip pass?** —
   `TestRouterYamlOnDisk` is a regression guard against schema
   drift between the on-disk YAML and the loader.
6. **D-05 checks 1–5 pass at Audit #1 start.**

---

**Authoring summary.** v8 is the §5 spin that LANDS R.PF1. The
amendment adds one module, two dataclasses, five errors, three
functions, three failure codes, three invariants, one constant, and
one test section (31 tests). It does not touch existing surface; it
binds existing surface (`run_pipeline_5_seat`, `run_eval_pipeline`)
via a registry-driven dispatcher. v0.2's R.1 TDSL, R.2 Content, and
R.3 Reporting tracks each become a router.yaml row + prompt templates
+ (where new pipeline_shape) one runner binding — never a §3 module
per track, never a §4.N mechanism per track.

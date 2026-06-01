# Spec card — pipeline.seats.editor (Round 1: adapter entry + OpenClaw-skill dispatch wrapper)

**STATUS:** PRE-STAGED 2026-04-21 — authored at Scribe R1 dispatch-time under OQ-1 resolution (adapter for v0.1.0). Soft-blocked on Scribe R2 LOCK (Editor consumes `SectionDraft` shape — stable after R2, not R1). Parent card: `section_7_council_seats_pipeline_modules.md` (Lane A step 5; Editor = 2-session arc per §5).

**Framework:** per `pipeline/templates/component_analysis_template.md` (Five Laws, Four Rules, failure-mode taxonomy, dev-vs-prod, standard interface pattern — not restated).

**Blueprint anchors:**
- `pipeline/blueprint/v0.1/section_07_scribe.md` **v1.1.1 LOCKED 2026-04-21** — `SectionDraft` schema consumed by Editor (input side; R2 LOCK is the hard pin for the shape).
- `pipeline/blueprint/v0.1/section_00_5_interface_index.md` — row `pipeline.contract.editor` line 499 is a one-line stub pointing at `section_05_v5#§5.2`. **[NEEDED from §0.5]:** Editor row set (EditorInput / EditorOutput / FlaggedTerm / ToneFeedback / `F-EDITOR-*` codes) is not yet enumerated at §0.5. Row-appends land at R1 LOCK as `pipeline.contract.editor.input.v1`, `pipeline.contract.editor.output.v1`, `pipeline.contract.editor.flagged_term.v1`, `pipeline.contract.editor.tone_feedback.v1`, `pipeline.seats.editor.adapter.v1`, `pipeline.seats.editor.seat.v1`.
- `pipeline/blueprint/v0.1/section_05_pipeline.md` v6 LOCKED 2026-04-18 — §4.4 Editor `invoke_seat` subprocess contract (Editor timeout = 180_000 ms inline literal; cross-family != Scribe.landed_family).
- `pipeline/blueprint/v0.1/section_04_logician.md` v2.1 LOCKED + v2.2 consolidated amendment — PRE/POST gate-runner contracts. **[NEEDED from §4]:** `F-EDITOR-OUTPUT-SHAPE` + `F-EDITOR-REWROTE-INSTEAD-OF-FLAGGED` slots not yet allocated in the §4.2.1 gate table; allocation lands via §4 v2.3 (or narrow amendment) before R1 LOCK.
- `pipeline/blueprint/v0.1/section_06_operating_envelope.md` v1-r1 LOCKED 2026-04-21 — §7.15 prerequisite interlock SATISFIED. Editor adapter does not compile prompts itself (skill carries the prompt); F-CONTEXT-PLACEMENT applies only insofar as the skill prompt is audited by §6's prompt-template lint at the skill boundary — out of R1 scope.
- `pipeline/architecture/v0.1/tilth_architecture_locked.md` v7 §D.3 Editor role, §F.1 SFR (Editor is **SFR-exempt** — feedback, not verdict; no three-block Premises/Execution/Conclusion format required).
- `skills/editor/SKILL.md` — the OpenClaw skill Editor adapter wraps. Load-bearing contract: output is JSON per SKILL.md lines 194-241 (top-level keys `readability`, `strengths[]`, `suggestions[]`, `gaps[]`; each `suggestions[].options[]` carries 2-3 labeled replacement options). R1 adapter maps this shape 1:1 into typed dataclasses.
- `pipeline/orchestrator/seats/editor.py` — legacy CLI-side adapter (pre-pipeline); same skill prompt + validation discipline. Reference implementation for `strip_fences` / `extract_json` / 2-3-replacement invariant. R1 lifts the validation predicates verbatim; replaces CLI argparse + `router.call_seat` with subprocess-entry + skill-dispatch.

**Blueprint hash-at-card** (compute at R1 Code-session open; pin in BLUEPRINT_DEPS):
- `section_07_scribe.md` — compute at R1 open (soft; R2 LOCK re-pins)
- `section_00_5_interface_index.md` — compute at R1 open
- `section_05_pipeline.md` — compute at R1 open
- `section_04_logician.md` — compute at R1 open (post-`F-EDITOR-*` slot allocation)
- `skills/editor/SKILL.md` — compute at R1 open (adapter is version-pinned to skill contract)

**Spec-card version:** v1 (adapter pattern per OQ-1 resolution 2026-04-21; full port is v0.1.1 roadmap if drift surfaces)
**Round:** §8 Editor Round 1 — adapter entry module + skill dispatch wrapper + output shape validator + basic tests
**Canonical home:** `pipeline/seats/editor/` (NEW — parallel to `pipeline/seats/scribe/` + `pipeline/seats/scout/` per parent spec §2)

---

## 1. Purpose

Promote Editor from **OpenClaw-skill-only** (`skills/editor/SKILL.md` + legacy CLI at `pipeline/orchestrator/seats/editor.py`) to a **production pipeline seat module** under `pipeline/seats/editor/` that satisfies `pipeline.loop.seat_runner.invoke_editor`'s subprocess contract (§4.4), routes through Logician PRE/POST gates, and emits typed output consumable by downstream Scribe-revision iteration.

**Adapter rationale (OQ-1 resolution).** Per parent spec §4 Option A + operator decision 2026-04-21: Editor uses the **thin adapter** pattern for v0.1.0; full port is v0.1.1 if drift surfaces. Rationale:

- Editor's skill logic is mostly heuristic pattern-matching (jargon flag, 2-3 replacement options, taxonomy sort) wrapped around LLM clarity-reading. The load-bearing content is the SKILL.md system prompt + the 2-3-replacement invariant — both preserve verbatim under adapter.
- Editor is SFR-exempt (architecture §F.1), so there is no three-block verdict format to enforce at the output boundary. The output contract is structured feedback with well-defined JSON (already schema-validated in `pipeline/orchestrator/seats/editor.py:166-217`).
- Adapter scope = 1-2 sessions total (R1 adapter + optional R2 polish) versus 3-4 sessions for a full port. The saved 2 sessions stay in critical path for Scribe R3 + Judge R3 where port-now is non-negotiable.
- Josh has won 3 grants in 2026 using the Editor skill as-is; the skill prompt is operator-vetted. Adapter preserves it.

**Zero-LLM scope at R1.** Adapter's own code is deterministic Python. The LLM call happens inside the skill subprocess — adapter only orchestrates (envelope transform in, dispatch out, output parse + validate back). Tests inject a fake skill-subprocess launcher per E-017 pattern.

**Out of scope at R1.** Full-port Python prompt template, provider-adapter layer (`pipeline.providers.<provider>.complete()`), in-process skill invocation, retry-with-clarification bounded loop on malformed output (land at R2 if needed), cross-family live consult beyond what `seat_runner` already enforces. Also out: §8 Editor blueprint authoring — this spec card scopes the R1 code round only; §8 blueprint round (parent spec §5 "Editor R1 blueprint authoring") is a separate track the operator may open in parallel to populate §0.5 rows before R1 LOCK.

## 2. Module layout

```
pipeline/seats/editor/
  __init__.py              # public surface + BLUEPRINT_DEPS
  types.py                 # frozen kw_only dataclasses:
                           #   EditorInput (wraps tuple[SectionDraft, ...] + rfa_excerpt + dialect)
                           #   FlaggedTerm (section_ref, issue_type, severity, excerpt,
                           #                why_it_hurts, replacement_options: tuple[str, ...])
                           #   ReplacementOption (label, text, note)
                           #   TaxonomyCheck (goals/outputs/outcomes/objectives + miscategorizations)
                           #   ToneFeedback (prose; operator-visible; overall_readability)
                           #   EditorOutput (flagged_terms: tuple[FlaggedTerm, ...], tone_feedback: ToneFeedback, quick_wins: tuple[str, ...], terms_to_verify: tuple[str, ...])
                           #   EditorSkillInvocation (what gets sent to the skill subprocess)
  adapter.py               # transform EditorInput -> skill stdin JSON; invoke skill via injected SkillLauncher Protocol;
                           #   parse skill stdout via strip_fences + extract_json (lifted from orchestrator/seats/editor.py:139-156);
                           #   map skill JSON -> EditorOutput; raise F_EDITOR_OUTPUT_SHAPE on shape violation
  seat.py                  # subprocess entry (same shape as Scribe R3's seat.py — stdin JSON envelope, stdout JSON output, minimal-env-whitelisted):
                           #   decode SeatEnvelope stdin; run Logician PRE-gate (F_PRE_CROSS_ORG_READ + E-017 injected gate_runner);
                           #   dispatch via adapter; run Logician POST-gate (F-EDITOR-* suite);
                           #   emit EditorOutput JSON to stdout (no fences, no commentary — Rule 4)
  BLUEPRINT_DEPS           # engineering process §4.6 hash pins for §7 + §0.5 + §4 + §5 + skills/editor/SKILL.md
```

Corpus fixtures live under `tests/corpus/editor/v1/` (parallel to Scribe R1 corpus):
```
tests/corpus/editor/v1/
  pass/
    vapg_clean_draft/             # SectionDraft[] input + expected EditorOutput shape
    reap_clean_draft/
  fail/
    skill_output_missing_options/  # skill returned replacements=[] (1 option) → F-EDITOR-OUTPUT-SHAPE
    skill_output_rewritten_body/   # skill attempted whole-draft rewrite → F-EDITOR-REWROTE-INSTEAD-OF-FLAGGED
    skill_output_non_json/         # skill returned prose with no JSON block → F-EDITOR-OUTPUT-SHAPE
    skill_subprocess_timeout/      # skill subprocess timed out → F-PIPE-06 cascade advance
```

## 3. Public API (Round 1)

`pipeline/seats/editor/__init__.py` declares:

```python
__all__ = (
    # Input/output shapes
    "EditorInput",
    "EditorOutput",
    "FlaggedTerm",
    "ReplacementOption",
    "TaxonomyCheck",
    "ToneFeedback",
    "EditorSkillInvocation",
    # Adapter surface
    "SkillLauncher",                 # Protocol (E-017 seam)
    "invoke_editor_adapter",         # transform + dispatch + parse + validate
    "parse_skill_output",            # skill JSON -> EditorOutput (pure, testable alone)
    "validate_editor_output_shape",  # EditorOutput -> raises F-EDITOR-OUTPUT-SHAPE on violation
    # Failure codes (strings; exception classes owned by pipeline.logician)
    "F_EDITOR_OUTPUT_SHAPE",              # "F-EDITOR-OUTPUT-SHAPE"
    "F_EDITOR_REWROTE_INSTEAD_OF_FLAGGED", # "F-EDITOR-REWROTE-INSTEAD-OF-FLAGGED"
    "F_EDITOR_SINGLE_REPLACEMENT",        # "F-EDITOR-SINGLE-REPLACEMENT" (2-3 invariant)
    "F_EDITOR_SKILL_SUBPROCESS_FAIL",     # "F-EDITOR-SKILL-SUBPROCESS-FAIL"
    "F_EDITOR_SKILL_OUTPUT_MALFORMED_JSON", # "F-EDITOR-SKILL-OUTPUT-MALFORMED-JSON"
    "F_EDITOR_SKILL_TIMEOUT",             # "F-EDITOR-SKILL-TIMEOUT"
    # Entry binding for seat_runner subprocess
    "main",                          # seat.py entry — reads stdin, writes stdout
)
```

## 4. Design decisions

1. **Adapter-not-port (OQ-1 resolution).** Skill subprocess is the LLM call; adapter is pure transform + validate. Skill prompt preserved verbatim at `skills/editor/SKILL.md` — adapter hash-pins the skill file in BLUEPRINT_DEPS so any skill-prompt edit shows up as a BLUEPRINT_DEPS drift at CI.
2. **`SkillLauncher` Protocol (E-017 injected-callable seam; 12th firing candidate).** Production wires clawdis subprocess; tests inject deterministic fake that returns canned JSON per corpus fixture. Production launcher shape:
   ```python
   class SkillLauncher(Protocol):
       def __call__(
           self,
           *,
           skill_slug: Literal["editor"],
           stdin_payload: bytes,
           timeout_ms: int,
       ) -> SkillSubprocessResult: ...
   ```
   Timeout inline-literal at adapter dispatch site (180_000 ms — matches `seat_runner` §4.4 Editor timeout; V1 rebind-resistance per E-023).
3. **Frozen kw_only dataclasses across all shapes.** Same discipline as Scribe R1 (§4.10 engineering-process + Round-J parent-lock pattern). Every shape carries `__post_init__` invariant checks — frozen-ness is mutation-prevention, not invariant-enforcement.
4. **`EditorOutput` mixed structured + prose.** `flagged_terms: tuple[FlaggedTerm, ...]` is machine-consumable (downstream Scribe revision can iterate); `tone_feedback: ToneFeedback` is operator-visible prose (carries `overall_readability.verdict` + `grade_level_estimate` + `key_message` per SKILL.md line 200). Rule 4 (clean output) applies to the structured side; prose side is read-only operator surface and stays free-form.
5. **2-3 replacement invariant enforced at validate, not at parse.** `parse_skill_output` populates `FlaggedTerm.replacement_options` verbatim from skill JSON; `validate_editor_output_shape` asserts `2 <= len(options) <= 3` and raises `F_EDITOR_SINGLE_REPLACEMENT` on violation. Keeps parse and validate separable + testable.
6. **Rewrite-detection heuristic (Law 4 enforcement).** `F_EDITOR_REWROTE_INSTEAD_OF_FLAGGED` fires if any `FlaggedTerm.replacement_options` collectively cover > 40% of the source `SectionDraft.body_text` (skill attempted whole-draft rewrite rather than point-fix). Threshold is inline-literal per V1. Operator-tunable at R2 if false-positives surface on dense-prose fixtures.
7. **Skill-output parse fragility hardening (parent spec §9 failure mode).** `parse_skill_output` uses `strip_fences` + `extract_json` (lifted verbatim from `pipeline/orchestrator/seats/editor.py:139-156` — Josh's 3-grant-proven parse discipline). Any JSON decode failure raises `F_EDITOR_SKILL_OUTPUT_MALFORMED_JSON`. Retry-with-clarification bounded at N=2 is R2 scope (parent spec §9 mitigation); R1 raises on first malformed output.
8. **Skill subprocess dispatch pattern.** Adapter constructs the skill stdin payload as:
   ```json
   {
     "draft_markdown": "<SectionDraft[] rendered to markdown>",
     "rfa_excerpt": "<RFA first 4000 chars per orchestrator/seats/editor.py:126-128>",
     "dialect": "<conservative|centrist|progressive|soul_fire>",
     "session_id": "<TILTH_SESSION_ID>",
     "org_slug": "<TILTH_ORG_SLUG>"
   }
   ```
   Skill stdout is expected to be the JSON schema documented in `skills/editor/SKILL.md` lines 194-241. Adapter maps this 1:1 into `EditorOutput` via `parse_skill_output`. **[NEEDED at R1 LOCK]:** skill stdin envelope schema row-append at §0.5 as `pipeline.contract.editor.skill_stdin.v1`.
9. **PRE-gate binding.**
   - `F_PRE_CROSS_ORG_READ` — Logician caller-provided check (§4.2.1 caller-supplied set). Editor adapter does not read from `orgs/` directly (skill subprocess does, via the pre-compiled prompt); but the seat.py entry asserts `TILTH_ORG_SLUG` matches the envelope's org_slug and refuses mismatched invocation.
10. **POST-gate binding.**
    - `F_EDITOR_OUTPUT_SHAPE` — structural: `EditorOutput.flagged_terms` is tuple, each `FlaggedTerm` has non-empty `excerpt` + `why_it_hurts` + 2-3 `replacement_options`; `tone_feedback.overall_readability.score_10` is in `0..10`.
    - `F_EDITOR_REWROTE_INSTEAD_OF_FLAGGED` — Law 4 enforcement (rewrite-detection heuristic per decision 6).
    - `F_EDITOR_SINGLE_REPLACEMENT` — 2-3 invariant violation.
    All three live as POST-gate slots in §4.2.1 (NEEDED allocation — see blueprint anchors). Gate-runner invocation happens at seat.py layer, not adapter layer (Round 4 AST-lint R2 `loop-logician-ban` does NOT apply to `pipeline/seats/`; parent spec §8).
11. **BLUEPRINT_DEPS declaration** (per engineering process §4.6 + L-015):
    ```python
    BLUEPRINT_DEPS = {
        "pipeline/blueprint/v0.1/section_07_scribe.md": {
            "sha256_16": "<computed-at-LOCK>",
            "sections": ("§7.5",),  # SectionDraft shape
        },
        "pipeline/blueprint/v0.1/section_00_5_interface_index.md": {
            "sha256_16": "<computed-at-LOCK>",
            "rows": (499,),  # pipeline.contract.editor stub (plus new rows added at R1 LOCK)
        },
        "pipeline/blueprint/v0.1/section_05_pipeline.md": {
            "sha256_16": "<computed-at-LOCK>",
            "sections": ("§4.4",),  # Editor invoke contract
        },
        "pipeline/blueprint/v0.1/section_04_logician.md": {
            "sha256_16": "<computed-at-LOCK>",
            "sections": ("§4.2.1",),  # PRE/POST slot table
        },
        "skills/editor/SKILL.md": {
            "sha256_16": "<computed-at-LOCK>",  # adapter is version-pinned to skill contract
            "contract": "JSON output schema lines 194-241",
        },
    }
    ```

## 5. Invariant checklist (per-dataclass `__post_init__`)

- `EditorInput.__post_init__`:
  - `len(section_drafts) >= 1` (at least one section to edit).
  - `dialect ∈ frozenset({"conservative", "centrist", "progressive", "soul_fire"})` — inline literal per V1.
  - `rfa_excerpt` is str (may be empty if RFA absent; skill handles fallback).
- `FlaggedTerm.__post_init__`:
  - `issue_type ∈ frozenset({"jargon", "hedge_language", "buried_claim", "goal_output_confusion", "passive_voice", "dialect_mismatch", "redundancy", "ambiguity", "specificity_gap"})` — inline literal (lifted from `orchestrator/seats/editor.py:159-162` + `specificity_gap` per SKILL.md §3 line 71-78).
  - `severity ∈ frozenset({"high", "medium", "low"})` — inline literal.
  - `len(excerpt.strip()) > 0`.
  - `len(why_it_hurts.strip()) > 0`.
  - `2 <= len(replacement_options) <= 3` — but NOTE: this invariant is enforced at `validate_editor_output_shape`, not `__post_init__`, because the parse path must be able to construct a `FlaggedTerm` with malformed options so the validator can report the violation via a clean F-code. `__post_init__` permits 0-3; validator enforces 2-3.
- `ReplacementOption.__post_init__`:
  - `label ∈ frozenset({"A", "B", "C"})`.
  - `len(text.strip()) > 0`.
- `ToneFeedback.__post_init__`:
  - `0 <= overall_readability.score_10 <= 10`.
  - `len(overall_readability.verdict.strip()) > 0`.
- `EditorOutput.__post_init__`:
  - `flagged_terms` is tuple (immutable).
  - `terms_to_verify` is tuple of str (admin-risk candidate flags — Logician consumes separately).

## 6. Adapter algorithm (pseudocode)

```
def invoke_editor_adapter(
    input_: EditorInput,
    *,
    skill_launcher: SkillLauncher,            # E-017 injected seam
    clock: Callable[[], datetime] = _default_utc_now,
) -> EditorOutput:
    # 1. Render SectionDraft[] to markdown (preserves section boundaries)
    draft_md = _render_section_drafts_to_markdown(input_.section_drafts)

    # 2. Construct skill stdin envelope
    invocation = EditorSkillInvocation(
        draft_markdown=draft_md,
        rfa_excerpt=input_.rfa_excerpt[:4000],   # match orchestrator/seats/editor.py:128
        dialect=input_.dialect,
        session_id=input_.session_id,
        org_slug=input_.org_slug,
        invocation_at_utc=clock(),
    )
    stdin_payload = json.dumps(_asdict(invocation)).encode("utf-8")

    # 3. Dispatch via injected launcher (180_000 ms inline-literal timeout — V1 rebind-resistance)
    try:
        skill_result = skill_launcher(
            skill_slug="editor",
            stdin_payload=stdin_payload,
            timeout_ms=180_000,
        )
    except TimeoutError as exc:
        raise F_EDITOR_SKILL_TIMEOUT(...) from exc
    except Exception as exc:
        raise F_EDITOR_SKILL_SUBPROCESS_FAIL(...) from exc

    # 4. Parse skill stdout — strip_fences + extract_json (lifted from orchestrator/seats/editor.py:139-156)
    try:
        skill_json = parse_skill_output(skill_result.stdout)
    except Exception as exc:
        raise F_EDITOR_SKILL_OUTPUT_MALFORMED_JSON(...) from exc

    # 5. Map skill JSON -> EditorOutput (pure transform)
    output = _map_skill_json_to_editor_output(skill_json, clock=clock)

    # 6. Validate shape (raises F-EDITOR-* on violation — Logician POST-gate surface)
    validate_editor_output_shape(output, source_section_drafts=input_.section_drafts)

    return output
```

Helpers `_render_section_drafts_to_markdown`, `_map_skill_json_to_editor_output`, `_default_utc_now` are module-private and pure. E-017 injected-clock seam mirrors Scribe R1.

## 7. Test surface (target: 25+ tests + 10 adversarial; E-024 ~1.5× = expect ~37-50 landed; coverage ≥ 95%)

**Rationale for lower floor vs Scribe R1 (40+):** adapter is a smaller surface than a full port (no Phase 0 extractor, no KGIE predicate, no SMART generator, no dialect code-switch — all of that lives inside the skill prompt). E-024 multiplier still applies (Protocol + V1 + E-023 trident present).

**Type-shape tests (happy path — 8+):**
- Every frozen dataclass constructible with the full documented field set.
- `__all__` export surface matches exactly (no leakage, no missing symbols).
- `EditorInput` rejects empty `section_drafts` tuple; rejects invalid dialect; accepts empty `rfa_excerpt`.
- `FlaggedTerm` accepts malformed `replacement_options` (len 0, 1, 4, 5) — invariant enforced at validator, not post_init.
- `ReplacementOption` rejects label "D"; rejects empty text.

**Adapter happy-path tests (6+):**
- VAPG clean draft fixture → skill returns well-formed JSON → `EditorOutput` constructed with ≥1 `FlaggedTerm`, `tone_feedback.overall_readability.score_10 in 0..10`.
- REAP clean draft fixture → same.
- Injected fake `SkillLauncher` returns canned corpus JSON; adapter produces deterministic output under fixed clock (idempotence).
- Markdown rendering of multi-section `SectionDraft[]` preserves section headings + body in a format the skill can parse (fixture pins the rendered bytes).
- Skill stdin envelope construction: `EditorSkillInvocation` asdict-serializes to the documented keys (draft_markdown, rfa_excerpt, dialect, session_id, org_slug, invocation_at_utc).

**Validator tests (6+):**
- `validate_editor_output_shape` PASS on canned happy-path `EditorOutput`.
- `replacement_options=[]` → `F_EDITOR_SINGLE_REPLACEMENT` raised.
- `replacement_options=[single]` → `F_EDITOR_SINGLE_REPLACEMENT` raised.
- `replacement_options=[a, b, c, d]` → `F_EDITOR_SINGLE_REPLACEMENT` raised (>3 also fails).
- `flagged_terms[*].replacement_options[*].text` collectively > 40% of source body length → `F_EDITOR_REWROTE_INSTEAD_OF_FLAGGED` raised.
- `overall_readability.score_10 = 11` → `F_EDITOR_OUTPUT_SHAPE` raised.

**Adversarial tests (10+, per parent spec §9 failure modes + E-023 discipline):**
- `skill_launcher` raises `TimeoutError` → `F_EDITOR_SKILL_TIMEOUT` raised with cause chain preserved.
- `skill_launcher` raises generic `subprocess.CalledProcessError` → `F_EDITOR_SKILL_SUBPROCESS_FAIL` raised.
- Skill stdout = `"```json\n{...}\n```"` (fenced) → `strip_fences` unwraps, adapter succeeds.
- Skill stdout = `"Here is my analysis:\n{...}"` (prose-wrapped JSON) → `extract_json` locates object, adapter succeeds.
- Skill stdout = `"This is not JSON."` → `F_EDITOR_SKILL_OUTPUT_MALFORMED_JSON` raised.
- Skill stdout = `"[...]"` (top-level JSON array, not object) → `F_EDITOR_SKILL_OUTPUT_MALFORMED_JSON` raised (per `default_judge_parse` parallel at `seat_runner.py:343-349`).
- Skill stdout empty (skill crashed silently) → `F_EDITOR_SKILL_OUTPUT_MALFORMED_JSON` raised.
- `object.__setattr__` on frozen `EditorOutput` field raises (documents frozen invariant).
- Injected clock raises `RuntimeError` → adapter propagates, does not swallow.
- Skill JSON with unknown `issue_type` (e.g., "climate_nostalgia") → `__post_init__` rejects with clear message; adapter wraps as `F_EDITOR_OUTPUT_SHAPE`.

**E-017 provider-seam pattern tests (3+):**
- Adapter works with three distinct `SkillLauncher` implementations (fake_happy, fake_timeout, fake_malformed) without code change.
- Production launcher wiring is NOT exercised in unit tests (integration test at R2 or at §5 E2E round).
- Launcher Protocol runtime-checkable via `isinstance(fake, SkillLauncher)`.

**E-027 considerations:** Editor's binding is Meta (`groq/llama-3.3-70b-versatile`) primary + OpenAI (`openai/gpt-4o-mini`) fallback — neither is Qwen3-32B, so E-027 payload-ceiling caveat does not apply. Document in threat-model docstring.

## 8. Done definition (R1)

- Module exists at `pipeline/seats/editor/` with `__init__.py`, `types.py`, `adapter.py`, `seat.py`, `BLUEPRINT_DEPS`.
- Public API surface exactly matches §3 — `__all__` leakage = LOCK fail.
- Every §5 invariant enforced via `__post_init__` (except the 2-3 replacement invariant, which is validator-enforced per §4 decision 5).
- Adapter-skill integration tests pass with injected fake `SkillLauncher`.
- Output shape validation tests cover all six F-EDITOR-* codes (PASS + FAIL cases each).
- Fixture corpus at `tests/corpus/editor/v1/{pass,fail}/` with ≥ 2 pass + ≥ 4 fail fixtures populated (matches parent spec §8 `≥4 pass + ≥6 fail`, scaled down for adapter scope).
- **Coverage ≥ 95%** on `pipeline/seats/editor/` module tree.
- **AST-lint R1-R7 clean** — seat code imports from `pipeline.logician` (POST-gate dispatch at seat.py), stdlib only elsewhere. R2 `loop-logician-ban` does not apply to `pipeline/seats/` (parent spec §8).
- **BLUEPRINT_DEPS sha-pinned** against §7 + §0.5 + §5 + §4 + `skills/editor/SKILL.md`; L-015 regression test `test_blueprint_deps_citations.py` extended to validate `pipeline/seats/editor/BLUEPRINT_DEPS` cited sections/rows/skill-contract resolve.
- **§0.5 row-appends filed** (6 rows per blueprint anchors: editor input/output/flagged_term/tone_feedback/adapter/seat).
- **§4 PRE/POST slot allocation filed** (3 slots: F_EDITOR_OUTPUT_SHAPE + F_EDITOR_REWROTE_INSTEAD_OF_FLAGGED + F_EDITOR_SINGLE_REPLACEMENT).
- **Full suite green** (current baseline includes Scribe R1 +40-60 tests; R1 expected delta ≈ +37-50 tests per E-024).
- **LOCK row** appended to `pipeline/engineering/lock_history.v1.jsonl` with reviewer tokens (if committee dispatched), test count, F-code surface.
- **Self-LOCK eligibility.** R1 is a thin-adapter-first-seat round. §5 precedent (12 consecutive self-LOCKs R3→R12.B) covers pure-Python scope rounds; Scribe R1 is self-LOCK-eligible for the same reason. Editor R1 **self-LOCK eligible** on the same grounds IF cross-family concerns don't surface during LOCK-prep (no LLM call at the adapter layer — the skill subprocess is the LLM boundary, already cross-family-reviewed at the skill itself). **Operator's call.** Default: self-LOCK if AST-lint + coverage + full-suite pass clean on single cycle; dispatch committee only if rewrite-detection heuristic threshold (40%) shows flakiness on real fixtures or if the §4 PRE/POST-slot allocation surfaces unexpected coupling with other seats' F-code surfaces.

## 9. Committee composition (if committee is dispatched)

Editor production binding = Meta (Llama 3.3 70B primary + OpenAI gpt-4o-mini fallback). Standard five-reviewer Code Thesis Committee per `router.yaml` `code_reviewer_{1..5}`:

- `code_reviewer_1` = openai/codex (OpenAI)
- `code_reviewer_2` = alibaba/qwen3-32b (Alibaba)
- `code_reviewer_3` = meta/llama-3.3-70b (Meta) **← same family as Editor production binding**
- `code_reviewer_4` = gpt-oss-120b (OpenAI-OSS)
- `code_reviewer_5` = kimi-k2 (Moonshot)

**Cross-family collision.** Per architecture A3 + parent spec §7: if an Editor-seat code review has `code_reviewer_3` (Meta) in the roster, that reviewer shares family with Editor's production binding. Two disposition options:

- **Option A (recommended at R1):** No collision at R1 because R1 is **adapter code** — it does NOT invoke an LLM; the LLM call lives inside the skill subprocess, which is a separate trust boundary. The code-review committee is reviewing the adapter's Python code for correctness + blueprint adherence, not the skill's LLM behaviour. Cross-family rigor applies to production-LLM-call review, not to adapter-code review. Keep `code_reviewer_3 = meta/llama-3.3-70b`.
- **Option B (fallback if operator rejects Option A):** Substitute `code_reviewer_3` with `kimi-k2` or `gpt-oss-120b` for the Editor R1 round only (round-local deviation, logged in dispatch README per E-027 Option 3 precedent).

Operator call at dispatch time. Option A is the cleaner read of A3 (family-rigor governs production LLM-ensemble composition, not code-review composition); Option B is the conservative read.

## 10. Failure modes (delta — framework taxonomy per template §3)

- **Aspiration-as-enforcement on §8 blueprint absence (L-006):** R1 ships an adapter module whose output contract is pinned by `skills/editor/SKILL.md` + this spec card, NOT by a LOCKED §8 blueprint. If the §8 blueprint round eventually authors a different `EditorOutput` shape than R1's adapter emits, drift surfaces. Mitigation: §8 blueprint round (if opened) treats the R1 adapter's `EditorOutput` as the starting fixture; any shape change requires a coordinated R2 amendment. Pre-check: spec card declares adapter shape as **provisional** until §8 LOCK (or explicit no-blueprint decision at v0.1).
- **Skill-adapter output parse fragility (parent spec §9):** LLM inside the skill may wrap JSON in prose fences, emit partial JSON, or add `<think>` block preambles (E-027 parallel for Meta Llama 3.3 on long contexts). Mitigation at R1: `strip_fences` + `extract_json` per `orchestrator/seats/editor.py:139-156`; on parse failure, raise `F_EDITOR_SKILL_OUTPUT_MALFORMED_JSON` — no silent fallback. Retry-with-clarification bounded at N=2 deferred to R2.
- **Rewrite-detection heuristic false positive (§4 decision 6):** 40% body-coverage threshold may fire on dense-prose sections where legitimate replacements happen to be near-length clones of the original (e.g., passive → active rewrites preserving sentence length). Mitigation: adversarial test includes a "legitimate long replacement" fixture that passes the threshold; threshold is inline-literal so operator can tune at R2 without touching other code.
- **Skill subprocess silent failure (E-023 residual):** clawdis subprocess may exit 0 with empty stdout (skill crashed after launch, before writing JSON). Mitigation: empty-stdout adversarial test raises `F_EDITOR_SKILL_OUTPUT_MALFORMED_JSON`; adapter never trusts exit code, always validates stdout shape.
- **Skill-file drift without BLUEPRINT_DEPS update (L-015):** operator edits `skills/editor/SKILL.md` without updating adapter BLUEPRINT_DEPS → adapter continues running against stale contract. Mitigation: L-015 regression test validates skill SHA at every test run; CI fails on drift. Forces operator to coordinate skill + adapter updates.

## 11. Hardenings (delta — template §4 checklist)

- [ ] Frozen, kw-only, slots=True on every dataclass (A-13 memory-layout discipline — 8GB dev node).
- [ ] `__post_init__` invariant enforcement on every frozen dataclass (except 2-3 replacement invariant per §4 decision 5).
- [ ] `__all__` in `__init__.py` is a tuple literal (V1 rebind-resistance).
- [ ] `SkillLauncher` Protocol runtime-checkable + injected at every test call site (E-017 discipline; 12th firing).
- [ ] Inline-literal timeout (180_000 ms) at adapter dispatch site (V1 + E-023).
- [ ] Threat-model docstring at adapter.py + seat.py top: documents (a) trusted-operator envelope per §3.11 v5, (b) skill-subprocess trust boundary, (c) E-027 non-applicability (Editor binding is Meta, not Qwen), (d) deferred retry-with-clarification scope to R2.
- [ ] E-027 + E-028 discipline: since adapter dispatches to skill (not to a code-review committee directly), the payload-size ceiling concern is between skill and provider — not between adapter and reviewer. Document N/A explicitly.
- [ ] E-023 residual handling: skill subprocess failure, malformed JSON, timeout — all three raise named F-codes, none swallow silently.
- [ ] BLUEPRINT_DEPS pin present + L-015 citation-check clean + skill-file SHA pinned.
- [ ] Coverage ≥ 95%; happy-path + fail-path parity on every F-EDITOR-* code.

## 12. Open questions for operator

- **OQ-1 — §8 Editor blueprint round: open now or defer?** Parent spec §5 lists Editor R1 blueprint authoring as a prerequisite to R2 code. At v0.1.0 with adapter pattern, the load-bearing output contract is `skills/editor/SKILL.md` + this spec card — a formal §8 blueprint may be redundant for the adapter scope. **Recommendation:** defer §8 blueprint round until v0.1.1 port decision; R1 adapter ships without it. If operator wants the audit trail, dispatch §8 in parallel (Thesis authoring rounds parallel to code rounds is precedent per §5 + Scout pattern).
- **OQ-2 — §0.5 row-append ownership.** 6 new rows land at R1 LOCK (editor input/output/flagged_term/tone_feedback/adapter/seat). Propose: row-append happens in the same commit as R1 LOCK (not a separate §0.5 amendment round). Parallel to Scribe R1's ~30-row append discipline per §7.17. Confirm or require separate §0.5 amendment round.
- **OQ-3 — `F-EDITOR-*` POST-gate slot allocation in §4.2.1.** 3 slots needed (output shape, rewrote-instead-of-flagged, single-replacement). Options: (a) narrow §4 v2.3 amendment before R1 LOCK; (b) land slots in §4.2.1 as part of R1 LOCK's `companion_code` table (same precedent as Logician v2.2 Wave gates). **Recommendation:** Option (b) — minimize blueprint-amendment ceremony for adapter-scope changes; §4 owners can audit the slots at R1 LOCK review.
- **OQ-4 — Rewrite-detection threshold (40%).** Inline-literal tunable. Soul-fire dialect drafts tend to be shorter + more poetic; a 40% threshold may false-positive on legitimate editorial tightening in that register. **Recommendation:** ship 40% at R1; instrument the threshold via telemetry (count of near-threshold fires) for R2 calibration.
- **OQ-5 — Self-LOCK or committee dispatch at R1?** Adapter is pure-Python + one Protocol seam + validator predicates. Prior §5 single-cycle self-LOCK precedent applies (no LLM call at adapter layer). **Recommendation:** self-LOCK if clean single-cycle; dispatch committee only if fixture integration surfaces unexpected coupling (§4 POST-gate slot interactions, skill-file contract drift).
- **OQ-6 — Skill stdin envelope row-append timing.** §0.5 row `pipeline.contract.editor.skill_stdin.v1` pins the JSON envelope shape the adapter sends to the skill subprocess. This row is an interface with clawdis/OpenClaw, not with another pipeline seat. **Recommendation:** row-append at R1 LOCK alongside the other 6; annotate as "clawdis boundary contract — not a pipeline-internal row" for future-maintainer clarity.

## 13. Non-goals at R1

- No full Python port of the skill's prompt logic — v0.1.1 if drift surfaces.
- No retry-with-clarification bounded loop on malformed output — R2 scope.
- No in-process LLM invocation — adapter always dispatches via subprocess.
- No provider-adapter-layer (`pipeline.providers.<provider>.complete()`) integration — adapter layer is entirely clawdis-subprocess-wrapped at v0.1.0.
- No §8 blueprint authoring — separate track (if opened).
- No §6 prompt-template lint integration — skill prompt is operator-vetted, not pipeline-compiled.
- No cross-family telemetry emission at adapter layer — `seat_runner` enforces cross-family via live families-so-far consult; adapter does not re-implement.
- No SFR format emission — Editor is SFR-exempt per architecture §F.1.

## 14. Unblocks

- **Editor R2** — polish + edge cases (retry-with-clarification, rewrite-detection threshold calibration, any §8 blueprint-induced shape deltas). 1 code session, smaller surface than R1.
- **Editor whole-seat LOCK** — at R2 LOCK, Editor seat is LOCKED-as-a-whole. Feeds revision-loop (§5 R5) with real `EditorOutput` for Scribe R3's second-iteration drafting.
- **Judge R2** — Judge consumes `SectionDraft` + `claim_evidence_map` from Scribe, not `EditorOutput`. No direct dependency on Editor LOCK, but Editor LOCK closes one axis of the three-way cross-family rigor (Scribe Anthropic + Editor Meta + Judge Google).
- **§5 E2E integration (Lane A step 6)** — requires all three seats LOCKED; Editor is the mid-dependency.

## 15. Artifacts (placeholders — populated at Code-session open)

- Spec-card SHA (this file): `<computed-at-pre-stage>`
- BLUEPRINT_DEPS hashes: `<per-anchor-at-R1-open>`
- LOCK row index in `pipeline/engineering/lock_history.v1.jsonl`: `<appended-at-LOCK>`
- Test count at LOCK: floor ≥ 25 + 10 adv = 35; expect ~37-50 per E-024 1.5×.
- Coverage at LOCK: target ≥ 95%.
- Full-suite delta at LOCK: target +37-50 tests over Scribe R1 baseline.

## 16. Changelog

- **v1 PRE-STAGED 2026-04-21.** Authored at Scribe R1 dispatch-time under operator OQ-1 resolution (adapter for v0.1.0, port deferred to v0.1.1). Soft-blocked on Scribe R2 LOCK (`SectionDraft` shape consumption). Hard prerequisites (§5 v6, §4 v2.1+v2.2, §6 v1-r1) all SATISFIED. Parent spec card line 99-101 forward-reference now resolves to this card. Six OQs carry recommendations — operator review before R1 code-session open.

*End spec card — PRE-STAGED; awaits Scribe R2 LOCK + operator OQ review before Editor R1 Code session opens.*

# Spec card — pipeline.orchestrator.scribe_prompt_assembler

**Blueprint anchor:** `pipeline/blueprint/v0.1/section_07_scribe.md` §6.11 shell-hash semantics; CLAUDE.md substrate § Pydantic AI orchestration.
**Spec-card version:** v1
**Round:** post-v0.1 (v0.2 roadmap)
**Priority:** v0.2 high — `ScribeEnvelope.compiled_prompt + compiled_prompt_shell_sha3_512` are required inputs for the envelope-builder, currently caller-supplied.
**Origin:** Surfaced 2026-05-08 during v0.2 wire-in work. The envelope-builder (`pipeline/orchestrator/scribe_envelope_builder.py`) accepts pre-assembled prompt + shell hash; this spec card defines the assembler that produces them.

---

## Purpose

The Scribe seat consumes an envelope whose `compiled_prompt` is already assembled and `compiled_prompt_shell_sha3_512` is already computed. Until this assembler lands, the envelope-builder relies on the caller to do both — meaning the caller has to know prompt-shell internals.

This module owns prompt assembly so callers can pass structured inputs (RFA + section + project_context + sector + dialect + admin-risk register) and receive `(compiled_prompt, shell_hash)` ready for envelope construction.

---

## Open-question resolutions

Eight design decisions made up-front so implementation isn't gated on operator review:

| Q | Resolution |
|---|---|
| **1. Section template structure** | Six-block template: (1) System frame [immutable] (2) Role frame [immutable] (3) RFA header [per-RFA, sourced from `RfaExtractedRecord`] (4) Section task [per-section, sourced from `SectionSpec`] (5) Project context + sector knowledge [per-org/grant] (6) Output contract [immutable, JSON shape Scribe must return]. |
| **2. Section template storage** | Python module — `pipeline/orchestrator/scribe_prompt_templates.py` — with immutable blocks as `Final[str]` constants. **No per-section template files.** Section-specific content comes from the RFA's `SectionSpec.required_content_cues` field; templates would over-rigidify across the diverse RFAs Tilth handles. |
| **3. Shell hash boundary** | `shell_hash = sha3_512(SYSTEM_FRAME + ROLE_FRAME + OUTPUT_CONTRACT + rfa_content_sha3_512)`. Covers the cross-section immutable structure plus the bound RFA. Mutable blocks (4-5) intentionally excluded — they vary per draft and aren't part of the contract pin. |
| **4. RFA injection** | Inline summary only: `program_name + cfda_or_aln + section_structure[i] + key_terms (top 12 by RFA mention frequency) + match_requirement + evaluation_criteria`. **Full RFA body NOT inlined** — token budget. The RFA content hash is referenced in the prompt as a verification anchor. |
| **5. Sector pack splice** | Block 5 (project context). Sector knowledge appears as a Markdown sub-section under `## Sector context: <sector>` — matches the existing `render_sector_context_block` output verbatim. The block 5 assembler consumes the rendered string from `merge_pack_into_project_context(...)["sector_knowledge"]["rendered_block"]`. |
| **6. Admin-risk register snapshot** | Threaded into block 5 as a JSON-serialized list under `## Admin-risk register snapshot` heading. When `operator_override_dialect` is set, an `OPERATOR OVERRIDE` notice is prepended to block 4 declaring the dialect lock. |
| **7. PROJECT_CONTEXT.md parser** | **Out of scope.** Caller passes an already-parsed `Mapping[str, Any]` (matching `ScribeEnvelope.project_context` shape). Parser is a separate v0.2 item (`pipeline/sovereignty/project_context_envelope.py` likely candidate). |
| **8. `operator_override_dialect`** | When set, prepend block 4 with: `"OPERATOR OVERRIDE: this section is to be drafted in dialect=<override> regardless of any auto-classification."` This makes the override visible in the prompt body so Scribe's output reflects it AND auditable in the shell-hashed structure (no — overrides change block 4 which is mutable, NOT in shell hash; visibility is purely instructional). |

---

## Architecture

### Pipeline

```
build_scribe_prompt(...) 
  → assemble_block_3_rfa_header(rfa_record, section_index)
  → assemble_block_4_section_task(rfa_record, section_index, override_dialect)
  → assemble_block_5_context(project_context, pack, admin_risk_snapshot)
  → concatenate(BLOCK_1, BLOCK_2, block_3, block_4, block_5, BLOCK_6)
  → compute shell_hash
  → return (compiled_prompt, shell_hash)
```

All block assemblers are pure functions: input-in, output-out, no I/O, no clock, deterministic.

### Properties

- **Deterministic:** identical inputs → identical (compiled_prompt, shell_hash).
- **Hash discipline:** `shell_hash` covers exactly the immutable cross-section structure + RFA pin. Operator-override-induced changes to block 4 are intentionally NOT in the shell hash (they're per-draft, audited via a different surface).
- **No new substrate deps:** stdlib only (hashlib, json), reuses existing types from `scribe.types` + `scribe.knowledge_packs`.
- **Backward-compat:** envelope-builder doesn't need any signature change. Caller swaps from "compute prompt+hash myself" to "call build_scribe_prompt(...)".

---

## Public API

```python
# pipeline.orchestrator.scribe_prompt_assembler

@dataclass(frozen=True, kw_only=True, slots=True)
class AssembledPrompt:
    compiled_prompt: str
    compiled_prompt_shell_sha3_512: str  # 128 lowercase hex
    section_index: int                   # which section_structure entry was consumed


def build_scribe_prompt(
    *,
    rfa_record: RfaExtractedRecord,
    section_index: int,                  # 0-based index into rfa.section_structure
    project_context: Mapping[str, Any],
    sector: str | None = None,           # passes through to knowledge_packs
    funder_dialect: str,
    operator_override_dialect: str | None = None,
    admin_risk_register_snapshot: Mapping[str, Any] | None = None,
) -> AssembledPrompt: ...


def compute_shell_hash(rfa_content_sha3_512: str) -> str:
    """Helper — exposed so callers can verify shell-hash without rebuilding the prompt."""
    ...
```

The envelope-builder currently has these inputs:

```python
build_scribe_envelope(
    ...
    compiled_prompt: str,
    compiled_prompt_shell_sha3_512: str,
    ...
)
```

After this assembler lands, the typical orchestrator flow becomes:

```python
ap = build_scribe_prompt(rfa_record=..., section_index=..., ...)
envelope = build_scribe_envelope(
    ...,
    compiled_prompt=ap.compiled_prompt,
    compiled_prompt_shell_sha3_512=ap.compiled_prompt_shell_sha3_512,
    ...,
)
```

---

## Data structures

```python
@dataclass(frozen=True, kw_only=True, slots=True)
class AssembledPrompt:
    compiled_prompt: str
    compiled_prompt_shell_sha3_512: str
    section_index: int
```

No new types beyond `AssembledPrompt`. All inputs reuse existing dataclasses from `pipeline.seats.scribe.types`.

---

## Block content (illustrative — final wording resolved at implementation)

### Block 1 — SYSTEM_FRAME (Final[str], in shell)

```
You are Scribe, a deterministic seat in the Tilth grant intelligence
substrate. You draft grant-application sections from a Request for
Applications (RFA), a project context, and operator-locked framing
constraints. You operate under five Laws (RFA-is-truth, ...). You
return ONLY the JSON shape specified in the Output Contract.
```

### Block 2 — ROLE_FRAME (Final[str], in shell)

```
Your task is to draft ONE section per invocation. The section's
boundaries, point allocation, and required content cues are pinned
in Block 4. You may NOT exceed the section's character/word limit
nor address content outside the section's scope.
```

### Block 6 — OUTPUT_CONTRACT (Final[str], in shell)

```
Return a JSON object matching:
{
  "section_drafts": [{
    "section_id": "<from envelope>",
    "body": "<your draft text>",
    "claim_evidence_map": [...],   # per claim_evidence dataclass schema
    "confidence_declaration": "...",
    "admin_risk_flags": [...]
  }],
  "admin_risk_flags": [...]
}
```

---

## Test surface

### Determinism tests
- Identical inputs → identical `compiled_prompt` byte-for-byte.
- Identical inputs → identical `shell_hash`.
- Different `funder_dialect` → identical `shell_hash` (dialect is in mutable block 5).
- Different RFA content hash → different `shell_hash`.

### Hash boundary tests
- Mutate Block 5 content (project_context entries) → `shell_hash` UNCHANGED.
- Mutate Block 4 content (`operator_override_dialect`) → `shell_hash` UNCHANGED.
- Mutate the RFA `rfa_content_sha3_512` → `shell_hash` CHANGES.
- Modify the SYSTEM_FRAME / ROLE_FRAME / OUTPUT_CONTRACT constants → `shell_hash` CHANGES (regression detection).

### Sector pack integration
- `sector=None` → no `## Sector context` heading in prompt body.
- `sector="regenerative_ag"` → seed pack content rendered under heading.
- Sector + override-dialect both supplied → both surface in their respective blocks.

### Round-trip with envelope-builder
- `build_scribe_prompt(...)` → `build_scribe_envelope(..., compiled_prompt=..., compiled_prompt_shell_sha3_512=...)` → envelope's `__post_init__` invariants pass.
- Round-trip via `emit_scribe_envelope_bytes` + `decode_envelope` preserves prompt + shell hash byte-for-byte.

---

## Dependencies

- Stdlib: `hashlib` (sha3_512), `json` (admin-risk snapshot serialization), `dataclasses`, `typing`.
- Existing Tilth: `pipeline.seats.scribe.types` (RfaExtractedRecord, SectionSpec, EvaluationCriterion); `pipeline.seats.scribe.knowledge_packs` (load_sector_pack, render_sector_context_block, merge_pack_into_project_context); `pipeline.orchestrator.scribe_envelope_builder` (consumes the output).
- **No new substrate deps.**

---

## Interaction with existing surfaces

| Surface | Relation |
|---|---|
| `scribe_envelope_builder.build_scribe_envelope` | **Downstream consumer.** Takes the assembler's output as input. No signature change to the builder needed. |
| `scribe.types.ScribeEnvelope.__post_init__` | **Validates the assembler's hash.** 128-hex / lowercase / non-empty checks already in place. |
| `scribe.types.RfaExtractedRecord` | **Primary input.** Block 3 + Block 4 are derived from this. |
| `scribe.knowledge_packs.merge_pack_into_project_context` | **Consumed by Block 5.** Already shipped. |
| `scribe.dialect.Dialect` (closed enum) | **Block 4 input.** `funder_dialect` + `operator_override_dialect` validated against the enum at envelope-construction time (already in `ScribeEnvelope.__post_init__`). |
| `pipeline.sovereignty.project_context_envelope` | **PROJECT_CONTEXT.md parser** — separate v0.2 item. Until it lands, callers pass an already-parsed mapping. |
| Admin-risk register loader | Caller threads a snapshot mapping into the assembler. Loader is a separate v0.2 concern. |

---

## Risks and mitigations

| Risk | Mitigation |
|---|---|
| Block constants get accidentally edited and silently change shell hash | Tests assert SHA3-512 of the constants matches a known fixture hash. Any constant edit must update the fixture explicitly — no silent drift. |
| RFA section structure varies more than `SectionSpec` accommodates | `SectionSpec.required_content_cues` is a `tuple[str, ...]` allowing arbitrary cue text. Variance handled by RFA author at extraction time, not by template. |
| Token budget exceeded by long PROJECT_CONTEXT or sector pack | Block 5 caps applied: PROJECT_CONTEXT serialized with `max_chars` truncation; sector pack already capped at 24 facts in `render_sector_context_block`. Operator can raise via explicit args. |
| Operator override on dialect introduces ambiguity for downstream classifier | Override is purely instructional in block 4. The envelope's `funder_dialect` + `operator_override_dialect` fields are the canonical signal Logician/Editor reads — Scribe's prompt-block override is for prompt steering only. |
| Future Pydantic-AI integration changes prompt structure | Spec card is for v0.2 plain-prompt; PAI integration is a v0.3+ refactor where this assembler likely splits into a `BasePromptBuilder` PAI mixes into. Out of scope here. |

---

## Implementation sequencing

Single round, ~250-350 LOC production + ~250-300 LOC tests:

1. **Round v0.2.A** — `scribe_prompt_templates.py` constants + hash discipline.
2. **Round v0.2.B** — block 3-5 assemblers (RFA header, section task, context + sector + admin-risk snapshot).
3. **Round v0.2.C** — `build_scribe_prompt` orchestration entry + `AssembledPrompt` dataclass + tests.

Estimated total: 1-2 days operator-supervised. Smaller than fact-drift gate; comparable to spine-drift loader.

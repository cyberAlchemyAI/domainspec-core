"""pipeline.seats.judge.types — §9 Judge Round 1 shape-only dataclasses.

Spec card: ``pipeline/engineering/spec_cards/section_09_judge_round_1_types_and_rubric_primitives.md``
(PRE-STAGED 2026-04-21).

Round 1 ships only **shape**: frozen, kw_only, slots=True dataclasses for
:class:`Rubric`, :class:`RubricCriterion`, :class:`RubricSubCriterion`,
:class:`CriterionScore`, :class:`JudgeInput`, :class:`JudgeOutput`; plus
forward-:class:`Protocol` contracts (:class:`SectionDraftLike`,
:class:`ClaimEvidenceLike`, :class:`LLMCallFn`) that bind to Scribe R3's
concrete ``SectionDraft`` at Judge R2 open via the E-026 ``__module__``
lineage check.

Threat model (R1):

- **In scope at R1.** Construction-time invariants on every dataclass:
  closed-set scorer role, hex-formatted rubric_sha256 (lowercase, 64
  chars), tz-aware datetimes, score / max_points bounds, confidence in
  ``[0.0, 1.0]``.
- **Out of scope at R1, deferred to R3.** Evidence-in-draft verification
  (Logician POST-gate ``F-JUDGE-EVIDENCE-NOT-IN-DRAFT``), LLM provider
  binding, cross-family routing, rubric-library dispatch, SFR format
  emission, subprocess entry, rubric-hash-drift PRE-gate.

§7 design decision pin: every frozen dataclass is ``kw_only=True`` so
field additions in v0.2 cannot silently reorder positional calls (A-13
memory-layout discipline; Scribe precedent).

The forward-Protocols here document exactly the surface Judge reads from
Scribe's ``SectionDraft`` (``section_name``, ``section_order``,
``body_text``, ``claim_evidence_map``). Judge R2 ships the
``__module__``-lineage assertion test that binds these to the concrete
Scribe shape; Judge R1 unit tests inject deterministic stubs that
satisfy the Protocols structurally.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Final, Literal, Mapping, Protocol, runtime_checkable


# ---------------------------------------------------------------------------
# Closed-set Literal aliases
# ---------------------------------------------------------------------------

RubricScorerRole = Literal["review_panel", "state_office", "administrator"]

# Inline-literal frozen set — V1 rebind-resistance per §7 design decision 9.
_RUBRIC_SCORER_ROLES: Final[frozenset[str]] = frozenset(
    {"review_panel", "state_office", "administrator"}
)


# ---------------------------------------------------------------------------
# §9 R1 failure-code constants — strings only at R1; R3 wires the gates.
# ---------------------------------------------------------------------------

F_JUDGE_RUBRIC_MALFORMED: Final[str] = "F-JUDGE-RUBRIC-MALFORMED"
F_JUDGE_CRITERION_MISSING: Final[str] = "F-JUDGE-CRITERION-MISSING"
F_JUDGE_SCORE_UNPARSEABLE: Final[str] = "F-JUDGE-SCORE-UNPARSEABLE"
F_JUDGE_EVIDENCE_NOT_IN_DRAFT: Final[str] = "F-JUDGE-EVIDENCE-NOT-IN-DRAFT"
F_JUDGE_SCORE_OUT_OF_BOUND: Final[str] = "F-JUDGE-SCORE-OUT-OF-BOUND"
F_JUDGE_RUBRIC_HASH_DRIFT: Final[str] = "F-JUDGE-RUBRIC-HASH-DRIFT"


# ---------------------------------------------------------------------------
# Shared hex-format helpers (canonical-bytes SHA-256 / SHA-3-512 discipline).
# ---------------------------------------------------------------------------

_HEX_CHARS: Final[frozenset[str]] = frozenset("0123456789abcdef")
_RUBRIC_SHA256_HEX_LEN: Final[int] = 64
_RFA_SHA3_512_HEX_LEN: Final[int] = 128


def _is_lowercase_hex(s: str) -> bool:
    return len(s) > 0 and all(ch in _HEX_CHARS for ch in s)


# ---------------------------------------------------------------------------
# Forward-Protocols — bind to Scribe R3's SectionDraft at Judge R2 open.
# ---------------------------------------------------------------------------


@runtime_checkable
class ClaimEvidenceLike(Protocol):
    """Forward-Protocol mirroring Scribe R2.5 :class:`ClaimEvidence`.

    Judge consumes ``claim_text`` + ``evidence_kind`` + ``source_pointer``
    on a per-claim basis when (R3) cross-checking Scribe's own evidence
    map against the Judge LLM's evidence quote.

    **R3 Protocol amendment (§7.a option b).** R1 originally declared
    ``evidence_text`` + ``source_field``; Scribe R2.5 ships
    ``ClaimEvidence`` with ``evidence_kind`` (Literal["RFA",
    "PROJECT_CONTEXT", "USER_DATA"]) + ``source_pointer``. The Protocol
    is amended at R3 to match Scribe's actual fields — only Judge
    consumes this Protocol externally, so the amendment does not break
    any outside-Judge consumer (verified per R3 spec card §7.a grep).
    The E-026 lineage assertion at
    :mod:`tests.seats.judge.test_e026_section_draft_bind` flips from
    "divergence pinned" to "structural conformance verified" at R3.
    """

    claim_text: str
    evidence_kind: str
    source_pointer: str


@runtime_checkable
class SectionDraftLike(Protocol):
    """Forward-Protocol mirroring Scribe R2.5 :class:`SectionDraft`.

    Judge reads exactly four fields: ``section_name`` (for prompt
    composition), ``section_order`` (for ordered scoring), ``body_text``
    (for verbatim-quote evidence-in-draft verification at R3), and
    ``claim_evidence_map`` (for cross-checking Scribe's own evidence
    sources at R2/R3 confidence-low branches).
    """

    section_name: str
    section_order: int
    body_text: str
    claim_evidence_map: tuple[ClaimEvidenceLike, ...]


@runtime_checkable
class LLMCallFn(Protocol):
    """E-017 injected-callable seam (12th+ formal firing).

    Production binds ``router.yaml`` ``tilth.judge`` primary
    (``google/gemini-2.5-pro``) at R3. Unit tests inject deterministic
    fakes returning canned strings.

    Contract: takes a compiled prompt string + max_tokens int; returns
    the raw model text output. Parsing of that output happens in
    :func:`pipeline.seats.judge.dimension_scorer.score_dimension` — the
    seam itself does no parsing.
    """

    def __call__(self, *, prompt: str, max_tokens: int) -> str: ...


# ---------------------------------------------------------------------------
# Rubric shapes (§9 R1 — VAPG FY26 JSON shape pinned)
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True, slots=True)
class RubricSubCriterion:
    """One subcriterion under a parent :class:`RubricCriterion`.

    Examples (VAPG FY26): ``a.i`` (Technological feasibility, max 10),
    ``a.ii`` (Operational efficiency, max 10), ``a.iii`` (Profitability
    and economic sustainability, max 10).

    ``tiers`` is a tuple of frozen mappings (each tier carries
    ``points`` + ``description``); empty when not applicable.
    """

    id: str
    name: str
    max_points: int
    must_address: tuple[str, ...]
    tiers: tuple[Mapping[str, Any], ...]

    def __post_init__(self) -> None:
        if not self.id.strip():
            raise ValueError("RubricSubCriterion.id is empty.")
        if not self.name.strip():
            raise ValueError(
                f"RubricSubCriterion.name is empty for id={self.id!r}."
            )
        if self.max_points < 0:
            raise ValueError(
                f"RubricSubCriterion({self.id!r}).max_points must be >= 0; "
                f"got {self.max_points!r}."
            )


@dataclass(frozen=True, kw_only=True, slots=True)
class RubricCriterion:
    """One scoring criterion in a :class:`Rubric`.

    Examples (VAPG FY26): ``a`` (Nature of the proposed venture, 30 pts,
    review_panel scorer, 3 subcriteria), ``b`` (Qualifications of Key
    Personnel, 20 pts, review_panel scorer, no subcriteria), ``g``
    (Administrator priority categories, 10 pts, administrator scorer,
    discretionary, no subcriteria).

    Either ``subcriteria`` or ``tiers`` must be non-empty — a criterion
    with both empty is incoherent (no scoring guidance) and is rejected
    at construction time.
    """

    id: str
    name: str
    max_points: int
    scorer: RubricScorerRole
    subcriteria: tuple[RubricSubCriterion, ...]
    must_address: tuple[str, ...]
    tiers: tuple[Mapping[str, Any], ...]

    def __post_init__(self) -> None:
        if not self.id.strip():
            raise ValueError("RubricCriterion.id is empty.")
        if not self.name.strip():
            raise ValueError(
                f"RubricCriterion.name is empty for id={self.id!r}."
            )
        if self.max_points < 0:
            raise ValueError(
                f"RubricCriterion({self.id!r}).max_points must be >= 0; "
                f"got {self.max_points!r}."
            )
        if self.scorer not in _RUBRIC_SCORER_ROLES:
            raise ValueError(
                f"RubricCriterion({self.id!r}).scorer must be one of "
                f"{sorted(_RUBRIC_SCORER_ROLES)}; got {self.scorer!r}."
            )
        # Administrator-discretionary criteria (e.g. VAPG FY26 criterion
        # 'g') may carry their scoring guidance in a non-tier shape
        # (``categories`` in VAPG). Only review_panel and state_office
        # criteria are required to ship tiers OR subcriteria.
        if (
            self.scorer != "administrator"
            and not self.subcriteria
            and not self.tiers
        ):
            raise ValueError(
                f"RubricCriterion({self.id!r}, scorer={self.scorer!r}) is "
                f"incoherent: both subcriteria and tiers are empty (no "
                f"scoring guidance)."
            )
        # Subcriteria id uniqueness within the criterion.
        seen_sub_ids: set[str] = set()
        for sub in self.subcriteria:
            if sub.id in seen_sub_ids:
                raise ValueError(
                    f"RubricCriterion({self.id!r}) has duplicate "
                    f"subcriterion id {sub.id!r}."
                )
            seen_sub_ids.add(sub.id)


@dataclass(frozen=True, kw_only=True, slots=True)
class Rubric:
    """A scoring rubric loaded from ``pipeline/rubrics/<program>.json``.

    ``rubric_sha256`` is the canonical-bytes SHA-256 of the rubric JSON
    payload (sort_keys=True, separators=(",", ":"), ensure_ascii=False,
    UTF-8 encoded). It pins which rubric the score was computed against.

    ``min_score`` and ``max_score`` describe the score band the funder
    publishes (for VAPG FY26: 50 / 100). Sum-of-criterion-max-points need
    not equal ``max_score`` exactly (some rubrics carry discretionary
    caps), but ``max_score`` must be >= ``min_score`` and >= the sum of
    criterion max_points (so that any actual-score is reachable).
    """

    program_code: str
    funder: str
    nofo_number: str
    max_score: int
    min_score: int
    criteria: tuple[RubricCriterion, ...]
    rubric_sha256: str
    loaded_at_utc: datetime

    def __post_init__(self) -> None:
        if not self.program_code.strip():
            raise ValueError("Rubric.program_code is empty.")
        if not self.funder.strip():
            raise ValueError("Rubric.funder is empty.")
        if not self.nofo_number.strip():
            raise ValueError("Rubric.nofo_number is empty.")
        if self.max_score < 0:
            raise ValueError(
                f"Rubric.max_score must be >= 0; got {self.max_score!r}."
            )
        if self.min_score < 0:
            raise ValueError(
                f"Rubric.min_score must be >= 0; got {self.min_score!r}."
            )
        if self.min_score > self.max_score:
            raise ValueError(
                f"Rubric.min_score ({self.min_score}) > max_score "
                f"({self.max_score})."
            )
        if not self.criteria:
            raise ValueError("Rubric.criteria must be non-empty.")
        if len(self.rubric_sha256) != _RUBRIC_SHA256_HEX_LEN:
            raise ValueError(
                f"Rubric.rubric_sha256 must be {_RUBRIC_SHA256_HEX_LEN} "
                f"hex chars (canonical SHA-256); got "
                f"{len(self.rubric_sha256)!r}."
            )
        if not _is_lowercase_hex(self.rubric_sha256):
            raise ValueError(
                "Rubric.rubric_sha256 must be lowercase hex per §6 "
                "canonical-bytes discipline."
            )
        if self.loaded_at_utc.tzinfo is None:
            raise ValueError("Rubric.loaded_at_utc must be timezone-aware.")
        # Criterion id uniqueness across the rubric.
        seen_ids: set[str] = set()
        for crit in self.criteria:
            if crit.id in seen_ids:
                raise ValueError(
                    f"Rubric has duplicate criterion id {crit.id!r}."
                )
            seen_ids.add(crit.id)
        # max_score must be >= sum-of-criterion-max-points (sanity: any
        # achievable rolled-up score must fit inside the rubric band).
        sum_crit_max = sum(c.max_points for c in self.criteria)
        if self.max_score < sum_crit_max:
            raise ValueError(
                f"Rubric.max_score ({self.max_score}) < sum of criterion "
                f"max_points ({sum_crit_max})."
            )


# ---------------------------------------------------------------------------
# Scoring shapes (§9 R1 — Judge candidate emission, R3 gate verifies)
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True, slots=True)
class CriterionScore:
    """A single Judge candidate score against one criterion or subcriterion.

    ``evidence_quote`` MUST be a verbatim substring of at least one
    :class:`SectionDraftLike.body_text` — but this is enforced at R3 by
    Logician POST-gate ``F-JUDGE-EVIDENCE-NOT-IN-DRAFT``. R1 only emits
    the candidate quote; the gate verifies.

    ``rationale`` is short prose explaining the score — NOT evidence;
    safe to paraphrase. Only ``evidence_quote`` is held to verbatim
    discipline.
    """

    criterion_id: str
    score: int
    evidence_quote: str
    confidence: float
    rationale: str

    def __post_init__(self) -> None:
        if not self.criterion_id.strip():
            raise ValueError("CriterionScore.criterion_id is empty.")
        if self.score < 0:
            raise ValueError(
                f"CriterionScore({self.criterion_id!r}).score must be >= 0; "
                f"got {self.score!r}."
            )
        if not (0.0 <= self.confidence <= 1.0):
            raise ValueError(
                f"CriterionScore({self.criterion_id!r}).confidence must be "
                f"in [0.0, 1.0]; got {self.confidence!r}."
            )


@dataclass(frozen=True, kw_only=True, slots=True)
class JudgeInput:
    """Bundled input to Judge R2 scoring orchestrator.

    R1 does NOT consume :class:`JudgeInput` (no orchestrator at R1) —
    the shape is shipped at R1 so R2 can compose it without redefining.

    ``rfa_content_sha3_512`` is the 128-hex SHA-3-512 of the RFA content
    this scoring run is against (matches Scribe R1's
    ``RfaExtractedRecord.rfa_content_sha3_512`` discipline).
    """

    section_drafts: tuple[SectionDraftLike, ...]
    rubric: Rubric
    rfa_content_sha3_512: str

    def __post_init__(self) -> None:
        if not self.section_drafts:
            raise ValueError("JudgeInput.section_drafts must be non-empty.")
        if len(self.rfa_content_sha3_512) != _RFA_SHA3_512_HEX_LEN:
            raise ValueError(
                f"JudgeInput.rfa_content_sha3_512 must be "
                f"{_RFA_SHA3_512_HEX_LEN} hex chars (full SHA-3-512); got "
                f"{len(self.rfa_content_sha3_512)!r}."
            )
        if not _is_lowercase_hex(self.rfa_content_sha3_512):
            raise ValueError(
                "JudgeInput.rfa_content_sha3_512 must be lowercase hex."
            )


@dataclass(frozen=True, kw_only=True, slots=True)
class JudgeOutput:
    """Bundled output from Judge scoring (R1 shape; consumed by Judge R2 verdict_assembler).

    ``rubric_sha256`` and ``rfa_content_sha3_512`` are repeated from the
    inputs for audit traceability — a downstream auditor can re-hash the
    on-disk rubric JSON + RFA content and compare against these pinned
    values to detect drift between score time and audit time
    (``F-JUDGE-RUBRIC-HASH-DRIFT`` PRE-gate at R3).

    ``total_score`` is the sum of ``criterion_scores[*].score``;
    ``max_total`` is the sum of the corresponding criterion max_points
    (for the criteria that were actually scored). R1 ships the shape;
    R2 :func:`pipeline.seats.judge.verdict_assembler.assemble_verdict`
    computes the values and constructs.
    """

    criterion_scores: tuple[CriterionScore, ...]
    total_score: int
    max_total: int
    rubric_sha256: str
    rfa_content_sha3_512: str
    scored_at_utc: datetime

    def __post_init__(self) -> None:
        if not self.criterion_scores:
            raise ValueError(
                "JudgeOutput.criterion_scores must be non-empty."
            )
        if self.total_score < 0:
            raise ValueError(
                f"JudgeOutput.total_score must be >= 0; got "
                f"{self.total_score!r}."
            )
        if self.max_total < 0:
            raise ValueError(
                f"JudgeOutput.max_total must be >= 0; got "
                f"{self.max_total!r}."
            )
        if self.total_score > self.max_total:
            raise ValueError(
                f"JudgeOutput.total_score ({self.total_score}) > max_total "
                f"({self.max_total})."
            )
        if len(self.rubric_sha256) != _RUBRIC_SHA256_HEX_LEN:
            raise ValueError(
                f"JudgeOutput.rubric_sha256 must be "
                f"{_RUBRIC_SHA256_HEX_LEN} hex chars; got "
                f"{len(self.rubric_sha256)!r}."
            )
        if not _is_lowercase_hex(self.rubric_sha256):
            raise ValueError(
                "JudgeOutput.rubric_sha256 must be lowercase hex."
            )
        if len(self.rfa_content_sha3_512) != _RFA_SHA3_512_HEX_LEN:
            raise ValueError(
                f"JudgeOutput.rfa_content_sha3_512 must be "
                f"{_RFA_SHA3_512_HEX_LEN} hex chars; got "
                f"{len(self.rfa_content_sha3_512)!r}."
            )
        if not _is_lowercase_hex(self.rfa_content_sha3_512):
            raise ValueError(
                "JudgeOutput.rfa_content_sha3_512 must be lowercase hex."
            )
        if self.scored_at_utc.tzinfo is None:
            raise ValueError(
                "JudgeOutput.scored_at_utc must be timezone-aware."
            )


# ---------------------------------------------------------------------------
# Responsiveness shapes (§9 R2 — mapper output consumed by JudgeVerdict)
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True, slots=True)
class ResponsivenessEntry:
    """One responsiveness factor pulled from the rubric JSON for a criterion.

    A "responsiveness factor" is a categorical claim about applicant
    identity, project category, or beneficiary group (vs. technical
    proposal quality). For VAPG FY26 these live under criterion ``f``
    (priority points — ``qualifying_categories`` / ``qualifying_applicants``
    / ``must_benefit``) and criterion ``g`` (administrator priority
    categories — ``categories[*].name``). Other rubrics surface analogous
    fields under different keys; the mapper extracts a known closed-set
    of factor keys (see
    :data:`pipeline.seats.judge.responsiveness_mapper.KNOWN_RESPONSIVENESS_FACTOR_KEYS`).

    ``factor_values`` is a tuple of strings — for ``categories`` style
    factors the names are flattened. Empty tuples are rejected at
    construction (a factor with no values is not a real responsiveness
    factor — silently dropping it would mask a malformed rubric).
    """

    criterion_id: str
    factor_name: str
    factor_values: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.criterion_id.strip():
            raise ValueError("ResponsivenessEntry.criterion_id is empty.")
        if not self.factor_name.strip():
            raise ValueError(
                f"ResponsivenessEntry.factor_name is empty for "
                f"criterion_id={self.criterion_id!r}."
            )
        if not self.factor_values:
            raise ValueError(
                f"ResponsivenessEntry({self.criterion_id!r}, "
                f"{self.factor_name!r}).factor_values must be non-empty."
            )
        for i, v in enumerate(self.factor_values):
            if not isinstance(v, str) or not v.strip():
                raise ValueError(
                    f"ResponsivenessEntry({self.criterion_id!r}, "
                    f"{self.factor_name!r}).factor_values[{i}] must be a "
                    f"non-empty string; got {v!r}."
                )


@dataclass(frozen=True, kw_only=True, slots=True)
class ResponsivenessMap:
    """Tuple-of-:class:`ResponsivenessEntry` produced by
    :func:`pipeline.seats.judge.responsiveness_mapper.build_responsiveness_map`.

    Empty tuples are permitted — a rubric may have no responsiveness
    factors (technical-only rubric). Duplicate
    ``(criterion_id, factor_name)`` pairs are rejected at construction
    time — the mapper deduplicates input or fails loud, never silently
    overwrites.
    """

    entries: tuple[ResponsivenessEntry, ...]

    def __post_init__(self) -> None:
        seen: set[tuple[str, str]] = set()
        for entry in self.entries:
            key = (entry.criterion_id, entry.factor_name)
            if key in seen:
                raise ValueError(
                    f"ResponsivenessMap has duplicate "
                    f"(criterion_id={entry.criterion_id!r}, "
                    f"factor_name={entry.factor_name!r}) entry."
                )
            seen.add(key)


# ---------------------------------------------------------------------------
# JudgeVerdict (§9 R2 — full assembled-verdict shape)
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True, slots=True)
class JudgeVerdict:
    """§9 R2 assembled-verdict shape — composes :class:`JudgeOutput` with
    rubric metadata + responsiveness map + assembly timestamp.

    Built by :func:`pipeline.seats.judge.verdict_assembler.assemble_verdict`
    from a tuple of :class:`CriterionScore` instances + a :class:`Rubric`
    + the section drafts that were scored. The single-rubric-per-invocation
    design decision (per spec card §5) means one ``JudgeVerdict`` per
    Judge run; multi-rubric merging into a ``JudgeVerdictBundle`` is
    deferred to a future round if the §9 blueprint mandates it.

    The Pre-gate for ``F-JUDGE-EVIDENCE-NOT-IN-DRAFT`` runs inside
    ``assemble_verdict`` before the :class:`JudgeVerdict` is constructed —
    every ``criterion_scores[*].evidence_quote`` must be a verbatim
    substring of at least one scored draft's ``body_text``. R3 wires the
    enforcing Logician POST-gate; R2 ships the substring check at
    assembly time.

    Construction-time invariants:

    - ``rubric_program_code`` is non-empty and matches
      ``judge_output``-time rubric code (assembler enforces equality
      against :attr:`Rubric.program_code`).
    - ``assembled_at_utc`` is timezone-aware.
    - ``assembled_at_utc >= judge_output.scored_at_utc`` — assembly
      cannot precede scoring.
    """

    judge_output: JudgeOutput
    rubric_program_code: str
    responsiveness_map: ResponsivenessMap
    assembled_at_utc: datetime

    def __post_init__(self) -> None:
        if not self.rubric_program_code.strip():
            raise ValueError("JudgeVerdict.rubric_program_code is empty.")
        if self.assembled_at_utc.tzinfo is None:
            raise ValueError(
                "JudgeVerdict.assembled_at_utc must be timezone-aware."
            )
        if self.assembled_at_utc < self.judge_output.scored_at_utc:
            raise ValueError(
                f"JudgeVerdict.assembled_at_utc "
                f"({self.assembled_at_utc.isoformat()}) precedes "
                f"judge_output.scored_at_utc "
                f"({self.judge_output.scored_at_utc.isoformat()})."
            )


__all__ = [
    # Rubric shapes
    "Rubric",
    "RubricCriterion",
    "RubricSubCriterion",
    "RubricScorerRole",
    # Scoring shapes
    "CriterionScore",
    "JudgeInput",
    "JudgeOutput",
    # R2 verdict + responsiveness shapes
    "JudgeVerdict",
    "ResponsivenessEntry",
    "ResponsivenessMap",
    # Forward-Protocols
    "SectionDraftLike",
    "ClaimEvidenceLike",
    "LLMCallFn",
    # F-code constants (§9 R1)
    "F_JUDGE_RUBRIC_MALFORMED",
    "F_JUDGE_CRITERION_MISSING",
    "F_JUDGE_SCORE_UNPARSEABLE",
    "F_JUDGE_EVIDENCE_NOT_IN_DRAFT",
    "F_JUDGE_SCORE_OUT_OF_BOUND",
    "F_JUDGE_RUBRIC_HASH_DRIFT",
]

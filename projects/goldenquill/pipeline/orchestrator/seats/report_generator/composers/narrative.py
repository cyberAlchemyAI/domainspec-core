"""§14.6.1 narrative sub-section composer.

Reads: operational-data ``narrative_entries`` sub-kind +
``proposal_commitments`` PROMOTED rows + ``reporting_template``
``narrative`` field requirements. Each required field (e.g.
``accomplishments_narrative`` / ``challenges_narrative`` /
``adjustments_narrative``) is drafted by Scribe; each draft sentence
becomes one :class:`ClaimEntry` with at least one operational-data
narrative_entries OR proposal_commitments source.

KGIE preflight is extended: every claim has at least one
:class:`ClaimEntry` source (the per-claim invariant from §14.5.1).
Composer-level enforcement runs before return.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping, Optional, Sequence

from .._schemas import ClaimEntry, SourceRef
from ._base import (
    ClockCallable,
    ComposerError,
    HashBytesCallable,
    ScribeFieldSpec,
    ScribeProtocol,
    VaultReadIntentCallable,
    compute_claim_id,
    encode_for_hash,
    split_paragraph_into_sentences,
    split_text_into_paragraphs,
)


_SUB_SECTION: str = "narrative"


@dataclass(frozen=True, kw_only=True)
class NarrativeEntryRow:
    """Pre-parsed view of one ``narrative_entries`` operational-data row.

    Fields the composer reads from the read intent's parsed output.
    """

    entry_id: str
    source_path: str
    text: str
    content_sha3_512: str
    period_n: int
    related_commitment_ids: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True, kw_only=True)
class PromotedCommitmentSourceRow:
    """Pre-parsed view of one PROMOTED ``proposal_commitments`` row.

    Subset of §11 v1 schema relevant to claim-source authoring.
    """

    commitment_id: str
    scope_tags_at_commitment: tuple[str, ...]
    commitment_text: str
    required_sub_sections: tuple[str, ...]
    evaluation_criteria: tuple[Mapping[str, object], ...] = field(default_factory=tuple)


@dataclass(frozen=True, kw_only=True)
class NarrativeDeps:
    """Injected dependencies for :func:`compose_narrative`.

    * ``read_narrative_entries`` — reads operational-data
      narrative_entries sub-kind under
      ``orgs/<slug>/vault/operational/grants/<grant_id>/period_<n>/narrative_entries/``.
      Returns a tuple of :class:`NarrativeEntryRow`.
    * ``read_promoted_commitments`` — reads proposal_commitments.yaml +
      filters status=PROMOTED. Returns a tuple of
      :class:`PromotedCommitmentSourceRow`.
    * ``read_template_field_specs`` — reads reporting_template.yaml +
      extracts the ``narrative`` sub-section's required field specs.
    * ``scribe`` — drafting callable per :class:`ScribeProtocol`.
    * ``clock`` — UTC ISO-8601 string source.
    * ``hash_bytes`` — SHA3-512 hex of bytes.
    """

    read_narrative_entries: VaultReadIntentCallable
    read_promoted_commitments: VaultReadIntentCallable
    read_template_field_specs: VaultReadIntentCallable
    scribe: ScribeProtocol
    clock: ClockCallable
    hash_bytes: HashBytesCallable


@dataclass(frozen=True, kw_only=True)
class NarrativeResult:
    """Composer output: markdown fragment + per-claim list."""

    markdown_fragment: str
    claims: tuple[ClaimEntry, ...]
    fields_drafted: tuple[str, ...]


def compose_narrative(
    *,
    deps: NarrativeDeps,
    org_slug: str,
    grant_id: str,
    period_n: int,
    operational_data_root: str,
    proposal_commitments_path: str,
    reporting_template_path: str,
) -> NarrativeResult:
    """Compose the ``narrative`` sub-section per §14.6.1.

    Returns the markdown fragment + the tuple of :class:`ClaimEntry`
    rows (one per draft sentence). Each claim has at least one
    operational-data narrative_entries OR proposal_commitments source.

    Composer-level invariants enforced BEFORE return:

    1. ``len(field_specs) >= 1`` (the funder requires at least one narrative
       field; otherwise the sub-section should not be in scope).
    2. Every claim ``claim_kind == "narrative"``.
    3. Every claim ``sub_section == "narrative"``.
    4. Every claim has at least one source (also enforced by
       :class:`ClaimEntry.__post_init__`; composer surfaces with context).
    5. ``claim_id`` matches :func:`compute_claim_id` for re-derivation
       at audit time.
    """
    if not org_slug or not isinstance(org_slug, str):
        raise ComposerError("org_slug must be a non-empty string")
    if period_n < 1:
        raise ComposerError(f"period_n must be >= 1; got {period_n!r}")

    field_specs_raw = deps.read_template_field_specs(
        kind="reporting_template",
        path=reporting_template_path,
        sub_section=_SUB_SECTION,
    )
    field_specs = _coerce_field_specs(field_specs_raw)
    if not field_specs:
        raise ComposerError(
            f"narrative sub-section in scope but reporting_template at "
            f"{reporting_template_path!r} has no narrative field specs"
        )

    narrative_entries_raw = deps.read_narrative_entries(
        kind="operational_data",
        sub_kind="narrative_entries",
        path=f"{operational_data_root.rstrip('/')}/narrative_entries",
        period_n=period_n,
    )
    narrative_entries = _coerce_narrative_entries(narrative_entries_raw)

    promoted_rows_raw = deps.read_promoted_commitments(
        kind="proposal_commitments",
        path=proposal_commitments_path,
    )
    promoted_rows = _coerce_promoted_rows(promoted_rows_raw)

    # Build a source pool: every narrative_entries row + every
    # PROMOTED commitment row whose required_sub_sections include
    # "narrative". Scribe receives these as candidate sources.
    relevant_commitments = tuple(
        c for c in promoted_rows if _SUB_SECTION in c.required_sub_sections
    )

    claims: list[ClaimEntry] = []
    drafted_field_names: list[str] = []
    md_parts: list[str] = []
    # Global paragraph offset across all narrative fields — §14.5.1's
    # paragraph_index is the position in the FULL sub-section markdown,
    # not within a single field. This guarantees claim_id uniqueness
    # across multiple narrative fields with identical drafted content.
    paragraph_offset = 0

    for spec in field_specs:
        drafted_field_names.append(spec.field_name)
        sources_for_scribe = _scribe_sources_for_field(
            narrative_entries=narrative_entries,
            commitments=relevant_commitments,
        )
        drafted_text = deps.scribe(spec=spec, sources=sources_for_scribe)
        if not isinstance(drafted_text, str):
            raise ComposerError(
                f"Scribe returned non-string for field {spec.field_name!r}: "
                f"{type(drafted_text).__name__}"
            )
        md_parts.append(f"### {_format_field_heading(spec.field_name)}\n\n{drafted_text}")

        # The field heading is itself a paragraph in the assembled
        # sub-section markdown — bump the offset so the first content
        # paragraph after the heading lands at its true global index.
        paragraph_offset += 1

        # Derive per-sentence claims; map each sentence to its sources
        # (the composer takes the conservative pooling rule: every
        # narrative_entries row + every relevant PROMOTED commitment
        # becomes a candidate source; Scribe's own discipline is to
        # ensure the sentence actually derives from these sources; the
        # F-REPORT-COMMITMENT-UNTRACED gate at finalize re-checks
        # entailment per RT-1a).
        paragraphs = split_text_into_paragraphs(drafted_text)
        for p_idx_local, paragraph in enumerate(paragraphs):
            p_idx = paragraph_offset + p_idx_local
            sentences = split_paragraph_into_sentences(paragraph)
            for s_idx, sentence in enumerate(sentences):
                claim_id = compute_claim_id(
                    sub_section=_SUB_SECTION,
                    paragraph_index=p_idx,
                    sentence_index=s_idx,
                    claim_text=sentence,
                )
                refs = _source_refs_for_sentence(
                    narrative_entries=narrative_entries,
                    commitments=relevant_commitments,
                    hash_bytes=deps.hash_bytes,
                )
                if not refs:
                    raise ComposerError(
                        f"narrative composer: sentence {claim_id!r} has no "
                        f"candidate sources (operational-data + commitments "
                        f"both empty)"
                    )
                claims.append(
                    ClaimEntry(
                        claim_id=claim_id,
                        sub_section=_SUB_SECTION,
                        claim_text=sentence,
                        claim_kind="narrative",
                        sources=refs,
                    )
                )
        # Advance the offset past this field's paragraphs so the next
        # field's content starts at the right global index.
        paragraph_offset += len(paragraphs)

    _validate_composer_invariants(claims=tuple(claims))

    return NarrativeResult(
        markdown_fragment="\n\n".join(md_parts),
        claims=tuple(claims),
        fields_drafted=tuple(drafted_field_names),
    )


# ---------------------------------------------------------------------------
# Helpers — coercion + invariant checks
# ---------------------------------------------------------------------------


def _coerce_field_specs(raw: object) -> tuple[ScribeFieldSpec, ...]:
    if raw is None:
        return ()
    if not isinstance(raw, (list, tuple)):
        raise ComposerError(
            f"narrative field specs must be list/tuple; got {type(raw).__name__}"
        )
    specs: list[ScribeFieldSpec] = []
    for idx, row in enumerate(raw):
        if isinstance(row, ScribeFieldSpec):
            specs.append(row)
            continue
        if not isinstance(row, Mapping):
            raise ComposerError(
                f"narrative field spec[{idx}] not Mapping: {type(row).__name__}"
            )
        field_name = row.get("field") or row.get("field_name")
        if not isinstance(field_name, str) or not field_name:
            raise ComposerError(
                f"narrative field spec[{idx}] missing 'field'/'field_name'"
            )
        max_len = row.get("max_length_chars")
        min_len = row.get("required_min_length_chars")
        specs.append(
            ScribeFieldSpec(
                sub_section=_SUB_SECTION,
                field_name=field_name,
                kind="narrative",
                max_length_chars=max_len if isinstance(max_len, int) else None,
                required_min_length_chars=min_len if isinstance(min_len, int) else None,
            )
        )
    return tuple(specs)


def _coerce_narrative_entries(raw: object) -> tuple[NarrativeEntryRow, ...]:
    if raw is None:
        return ()
    if not isinstance(raw, (list, tuple)):
        raise ComposerError(
            f"narrative_entries must be list/tuple; got {type(raw).__name__}"
        )
    rows: list[NarrativeEntryRow] = []
    for idx, row in enumerate(raw):
        if isinstance(row, NarrativeEntryRow):
            rows.append(row)
            continue
        if not isinstance(row, Mapping):
            raise ComposerError(
                f"narrative_entries[{idx}] not Mapping: {type(row).__name__}"
            )
        try:
            rows.append(
                NarrativeEntryRow(
                    entry_id=str(row["entry_id"]),
                    source_path=str(row["source_path"]),
                    text=str(row["text"]),
                    content_sha3_512=str(row["content_sha3_512"]),
                    period_n=int(row["period_n"]),
                    related_commitment_ids=tuple(
                        str(c) for c in row.get("related_commitment_ids", ())
                    ),
                )
            )
        except KeyError as exc:
            raise ComposerError(
                f"narrative_entries[{idx}] missing key {exc!s}"
            ) from exc
    return tuple(rows)


def _coerce_promoted_rows(raw: object) -> tuple[PromotedCommitmentSourceRow, ...]:
    if raw is None:
        return ()
    if not isinstance(raw, (list, tuple)):
        raise ComposerError(
            f"promoted commitments must be list/tuple; got {type(raw).__name__}"
        )
    rows: list[PromotedCommitmentSourceRow] = []
    for idx, row in enumerate(raw):
        if isinstance(row, PromotedCommitmentSourceRow):
            rows.append(row)
            continue
        if not isinstance(row, Mapping):
            raise ComposerError(
                f"promoted_commitments[{idx}] not Mapping: {type(row).__name__}"
            )
        try:
            rows.append(
                PromotedCommitmentSourceRow(
                    commitment_id=str(row["commitment_id"]),
                    scope_tags_at_commitment=tuple(
                        str(s) for s in row.get(
                            "scope_tags_at_commitment",
                            row.get("scope_tags", ()),
                        )
                    ),
                    commitment_text=str(row.get("commitment_text", "")),
                    required_sub_sections=tuple(
                        str(s) for s in row.get("required_sub_sections", ())
                    ),
                    evaluation_criteria=tuple(
                        dict(c) if isinstance(c, Mapping) else {}
                        for c in row.get("evaluation_criteria", ())
                    ),
                )
            )
        except KeyError as exc:
            raise ComposerError(
                f"promoted_commitments[{idx}] missing key {exc!s}"
            ) from exc
    return tuple(rows)


def _scribe_sources_for_field(
    *,
    narrative_entries: Sequence[NarrativeEntryRow],
    commitments: Sequence[PromotedCommitmentSourceRow],
) -> tuple[Mapping[str, object], ...]:
    """Assemble candidate source dicts for Scribe."""
    out: list[Mapping[str, object]] = []
    for entry in narrative_entries:
        out.append(
            {
                "kind": "operational_data",
                "sub_kind": "narrative_entries",
                "entry_id": entry.entry_id,
                "source_path": entry.source_path,
                "text": entry.text,
                "content_sha3_512": entry.content_sha3_512,
                "related_commitment_ids": list(entry.related_commitment_ids),
            }
        )
    for c in commitments:
        out.append(
            {
                "kind": "proposal_commitments",
                "commitment_id": c.commitment_id,
                "scope_tags_at_commitment": list(c.scope_tags_at_commitment),
                "commitment_text": c.commitment_text,
            }
        )
    return tuple(out)


def _source_refs_for_sentence(
    *,
    narrative_entries: Sequence[NarrativeEntryRow],
    commitments: Sequence[PromotedCommitmentSourceRow],
    hash_bytes: HashBytesCallable,
) -> tuple[SourceRef, ...]:
    """Build SourceRef tuple — every narrative_entries row + every relevant
    commitment.

    The composer is conservative: every operational-data narrative_entries
    row is a candidate source, plus every relevant PROMOTED commitment.
    F-REPORT-COMMITMENT-UNTRACED at finalize re-checks entailment per
    RT-1a. The composer ensures structural completeness only.
    """
    refs: list[SourceRef] = []
    for entry in narrative_entries:
        refs.append(
            SourceRef(
                kind="operational_data",
                sub_kind="narrative_entries",
                source_path=entry.source_path,
                source_row_id=entry.entry_id,
                source_content_sha3_512=entry.content_sha3_512,
            )
        )
    for c in commitments:
        refs.append(
            SourceRef(
                kind="proposal_commitments",
                commitment_id=c.commitment_id,
                commitment_status="PROMOTED",
                scope_tags_at_commitment=c.scope_tags_at_commitment,
            )
        )
    return tuple(refs)


def _format_field_heading(field_name: str) -> str:
    """Human-readable heading from snake_case field name."""
    return field_name.replace("_", " ").strip().capitalize()


def _validate_composer_invariants(*, claims: tuple[ClaimEntry, ...]) -> None:
    """Composer-level invariant gate — runs before return."""
    if not claims:
        # Empty narrative sub-section permitted IF no field specs / no
        # sources; we surface as ComposerError because the caller only
        # invokes this composer when narrative is in scope.
        raise ComposerError(
            "narrative composer produced zero claims; verify Scribe + "
            "narrative_entries + commitments are non-empty"
        )
    for c in claims:
        if c.sub_section != _SUB_SECTION:
            raise ComposerError(
                f"claim {c.claim_id!r} sub_section={c.sub_section!r}; expected "
                f"{_SUB_SECTION!r}"
            )
        if c.claim_kind != "narrative":
            raise ComposerError(
                f"claim {c.claim_id!r} claim_kind={c.claim_kind!r}; expected "
                f"'narrative'"
            )
        if not c.sources:
            raise ComposerError(
                f"claim {c.claim_id!r} has no sources (composer-level check)"
            )


__all__ = [
    "NarrativeDeps",
    "NarrativeEntryRow",
    "NarrativeResult",
    "PromotedCommitmentSourceRow",
    "compose_narrative",
]

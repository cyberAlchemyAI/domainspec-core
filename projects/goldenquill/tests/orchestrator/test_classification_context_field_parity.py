"""Drift gate — router + provider_boundary ClassificationContext field parity.

§4 v2.x.6 §11.2 (DC-02 + RT-05 fold-ins) — OD-1 ratified architectural
decoupling between the router's public ``ClassificationContext`` and the
wrapper's internal ``ClassificationContext``. The coercion helper
``router._coerce_to_provider_boundary_context`` silently drops any field that
exists in one type and not the other; this test converts silent-drop into a
noisy failure.

The two types share field names (``inputs``, ``classified_values``,
``slot_positions``, ``high_stakes_flag_values``, ``post_fill_draft``); the
wrapper's ``ClassificationContext`` carries two ADDITIONAL fields
(``cycle_id`` + ``payload_sha3_512_commitment``) introduced by §4 v2.x.5
Cycle-1 RT-05 cross-cycle replay defense. Those two are the SOLE permitted
drift; any other delta breaks the coercion helper.
"""

from __future__ import annotations

from dataclasses import fields

from pipeline.orchestrator.provider_boundary import ClassificationContext as PBC
from pipeline.orchestrator.router import ClassificationContext as RC

#: Known-permitted field-set delta — wrapper carries two extra replay-defense
#: fields that the router-public CC does not expose. Any drift OUTSIDE this
#: delta is a noisy failure per OD-1.
EXPECTED_PBC_ONLY_FIELDS: frozenset[str] = frozenset(
    {"cycle_id", "payload_sha3_512_commitment"}
)


def test_classification_context_shared_field_names() -> None:
    """Router-public CC fields must be a subset of provider_boundary CC fields."""
    rc_names = {f.name for f in fields(RC)}
    pbc_names = {f.name for f in fields(PBC)}
    router_only = rc_names - pbc_names
    assert router_only == set(), (
        f"router.ClassificationContext has field(s) absent from "
        f"provider_boundary.ClassificationContext: {sorted(router_only)}. "
        "_coerce_to_provider_boundary_context would silently drop them — "
        "either align the types or extend the helper."
    )


def test_classification_context_pbc_only_fields_are_the_known_delta() -> None:
    """provider_boundary CC additions must stay inside the known-permitted delta."""
    rc_names = {f.name for f in fields(RC)}
    pbc_names = {f.name for f in fields(PBC)}
    pbc_only = pbc_names - rc_names
    unexpected = pbc_only - EXPECTED_PBC_ONLY_FIELDS
    assert unexpected == set(), (
        f"provider_boundary.ClassificationContext has unexpected extra field(s) "
        f"{sorted(unexpected)}. Update EXPECTED_PBC_ONLY_FIELDS in this test "
        "AND extend _coerce_to_provider_boundary_context to handle them, OR "
        "add the field to router.ClassificationContext."
    )


def test_classification_context_shared_field_type_annotations() -> None:
    """Shared field type annotations must match byte-for-byte.

    Cycle-1 Judge DC-02 + Red Team RT-05 fold-in: name-set parity catches
    additions/deletions but NOT semantic drift (same name, divergent type).
    Forward-reference strings are compared as-is; `typing.get_type_hints`
    resolution is a v2.x.7 hardening item per RT-C2-04 deferral.
    """
    rc_fields = {f.name: f.type for f in fields(RC)}
    pbc_fields = {f.name: f.type for f in fields(PBC)}
    shared = set(rc_fields) & set(pbc_fields)
    mismatches = {
        name: (rc_fields[name], pbc_fields[name])
        for name in shared
        if rc_fields[name] != pbc_fields[name]
    }
    assert mismatches == {}, (
        f"ClassificationContext field-type drift detected: {mismatches}. "
        "Same field names but different type annotations. "
        "_coerce_to_provider_boundary_context needs adjustment or the "
        "annotations need re-alignment."
    )

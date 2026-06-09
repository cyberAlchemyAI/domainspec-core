#!/usr/bin/env python3
"""Validate Body War Inventory example templates and negative fixtures."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


REQUIRED_FILES = {
    "cards": "cards.example.json",
    "selectors": "selector-index.example.json",
    "links": "link-index.example.json",
    "gaps": "gap-risk-index.example.json",
    "index": "index.example.json",
    "retrieval": "retrieval.example.json",
}

REQUIRED_CARD_FIELDS = {
    "id",
    "schema_version",
    "profile",
    "card_type",
    "title",
    "summary",
    "source_refs",
    "authority_level",
    "tags",
    "selection_reason",
    "captured",
    "promotion_status",
    "promotion_owner",
    "updated_at",
}

CARD_TYPES = {
    "source-summary",
    "concept",
    "method",
    "claim",
    "question",
    "context",
    "relation-candidate",
    "contradiction-candidate",
    "operational-lesson",
}

SELECTOR_TYPES = {"file", "heading", "line-span", "anchor", "query", "fragment"}
PROFILES = {"full", "minimal"}
AUTHORITY_LEVELS = {
    "raw-source",
    "session-evidence",
    "discovery-baseline",
    "inventory-knowledge",
    "ontology-candidate",
    "downstream-governed-ref",
}
PROMOTION_STATUSES = {"captured", "candidate", "proposed", "promoted", "rejected", "superseded", "blocked"}
PROMOTION_OWNERS = {
    "none",
    "inventory",
    "ontology-vault",
    "definitions-governance",
    "context-builder",
    "invoke",
    "repository-harness",
    "other",
}

REQUIRED_GAPS = {
    "gap.body-war.pilot-validation-city",
    "gap.body-war.first-park-track-set",
    "gap.body-war.track-boundary-format",
    "gap.body-war.app-backed-validation-implementation",
}


class ValidationError(Exception):
    pass


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        raise ValidationError(f"{path}: JSON parse failed: {exc}") from exc


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def list_duplicates(values: list[str]) -> list[str]:
    seen: set[str] = set()
    dupes: set[str] = set()
    for value in values:
        if value in seen:
            dupes.add(value)
        seen.add(value)
    return sorted(dupes)


def validate_source_ref(repo_root: Path, ref: dict[str, Any], label: str) -> None:
    require(isinstance(ref.get("path"), str) and ref["path"], f"{label}: source ref missing path")
    require(isinstance(ref.get("selector"), str) and ref["selector"], f"{label}: source ref missing selector")
    require(ref.get("selector_type") in SELECTOR_TYPES, f"{label}: invalid selector_type {ref.get('selector_type')!r}")
    if ref["selector_type"] == "line-span":
        require(isinstance(ref.get("start_line"), int), f"{label}: line-span missing start_line")
        require(isinstance(ref.get("end_line"), int), f"{label}: line-span missing end_line")
        require(ref["start_line"] <= ref["end_line"], f"{label}: line-span start_line after end_line")
    require((repo_root / ref["path"]).exists(), f"{label}: source path does not exist: {ref['path']}")


def validate_cards(repo_root: Path, cards_doc: dict[str, Any]) -> set[str]:
    cards = cards_doc.get("cards")
    require(isinstance(cards, list) and cards, "cards.example.json: cards must be a non-empty array")
    card_ids = [card.get("id") for card in cards]
    require(all(isinstance(card_id, str) and card_id for card_id in card_ids), "cards: every card needs an id")
    dupes = list_duplicates(card_ids)
    require(not dupes, f"cards: duplicate ids: {', '.join(dupes)}")

    for card in cards:
        card_id = card["id"]
        missing = REQUIRED_CARD_FIELDS - set(card)
        require(not missing, f"{card_id}: missing fields: {', '.join(sorted(missing))}")
        require(card["schema_version"] == "inventory.evidence-card.v0.2", f"{card_id}: wrong schema_version")
        require(card["profile"] in PROFILES, f"{card_id}: invalid profile")
        require(card["card_type"] in CARD_TYPES, f"{card_id}: invalid card_type")
        require(card["authority_level"] in AUTHORITY_LEVELS, f"{card_id}: invalid authority_level")
        require(card["promotion_status"] in PROMOTION_STATUSES, f"{card_id}: invalid promotion_status")
        require(card["promotion_owner"] in PROMOTION_OWNERS, f"{card_id}: invalid promotion_owner")
        if card["promotion_status"] in {"promoted", "rejected", "superseded", "blocked"}:
            require(card["promotion_owner"] != "none", f"{card_id}: terminal promotion status needs owner")
        source_refs = card["source_refs"]
        require(isinstance(source_refs, list) and source_refs, f"{card_id}: source_refs must be non-empty")
        for ref in source_refs:
            validate_source_ref(repo_root, ref, f"{card_id}")
        if card["profile"] == "full":
            require(isinstance(card.get("handoff_targets"), list), f"{card_id}: full card missing handoff_targets")
            require(isinstance(card.get("trace"), list) and card["trace"], f"{card_id}: full card missing trace")
        claim_shape = card.get("claim_shape")
        if claim_shape:
            notice = claim_shape.get("non_authority_notice", "")
            require(isinstance(notice, str) and notice, f"{card_id}: claim_shape missing non_authority_notice")
    return set(card_ids)


def validate_selectors(repo_root: Path, selectors_doc: dict[str, Any], card_ids: set[str]) -> set[str]:
    selectors = selectors_doc.get("selectors")
    require(isinstance(selectors, list) and selectors, "selector-index.example.json: selectors must be non-empty")
    selector_ids = [selector.get("selector_id") for selector in selectors]
    require(all(isinstance(selector_id, str) and selector_id for selector_id in selector_ids), "selectors: every selector needs selector_id")
    dupes = list_duplicates(selector_ids)
    require(not dupes, f"selectors: duplicate ids: {', '.join(dupes)}")
    for selector in selectors:
        selector_id = selector["selector_id"]
        validate_source_ref(repo_root, selector.get("source_ref", {}), selector_id)
        cards = selector.get("cards")
        require(isinstance(cards, list), f"{selector_id}: cards must be an array")
        for card_id in cards:
            require(card_id in card_ids, f"{selector_id}: unknown card id {card_id}")
    return set(selector_ids)


def validate_links(links_doc: dict[str, Any], card_ids: set[str], selector_ids: set[str]) -> set[str]:
    vocabulary = set(links_doc.get("edge_vocabulary") or [])
    require(vocabulary, "link-index.example.json: missing edge_vocabulary")
    links = links_doc.get("links")
    require(isinstance(links, list) and links, "link-index.example.json: links must be non-empty")
    for link in links:
        link_id = link.get("link_id", "<missing-link-id>")
        require(link.get("edge") in vocabulary, f"{link_id}: unknown link edge {link.get('edge')!r}")
        require(link.get("authority") == "inventory-read-model", f"{link_id}: authority must be inventory-read-model")
        notice = link.get("non_authority_notice")
        require(isinstance(notice, str) and notice, f"{link_id}: missing non_authority_notice")
        for key in ("from", "to"):
            value = link.get(key)
            require(isinstance(value, str) and value, f"{link_id}: missing {key}")
            if value.startswith("inventory.card."):
                require(value in card_ids, f"{link_id}: {key} points to unknown card {value}")
            if value.startswith("selector."):
                require(value in selector_ids, f"{link_id}: {key} points to unknown selector {value}")
    return vocabulary


def validate_gaps(gaps_doc: dict[str, Any], repo_root: Path) -> set[str]:
    gaps = gaps_doc.get("gaps")
    require(isinstance(gaps, list) and gaps, "gap-risk-index.example.json: gaps must be non-empty")
    gap_ids = {gap.get("gap_id") for gap in gaps}
    missing_gaps = REQUIRED_GAPS - gap_ids
    require(not missing_gaps, f"missing required gaps: {', '.join(sorted(missing_gaps))}")
    for gap in gaps:
        gap_id = gap.get("gap_id", "<missing-gap-id>")
        require(isinstance(gap.get("owner"), str) and gap["owner"], f"{gap_id}: missing owner")
        require(isinstance(gap.get("next_action"), str) and gap["next_action"], f"{gap_id}: missing next_action")
        refs = gap.get("source_refs")
        require(isinstance(refs, list) and refs, f"{gap_id}: source_refs must be non-empty")
        for ref in refs:
            validate_source_ref(repo_root, ref, gap_id)
    return gap_ids


def validate_retrieval(retrieval_doc: dict[str, Any], card_ids: set[str], selector_ids: set[str], gap_ids: set[str]) -> None:
    selected_cards = retrieval_doc.get("selected_cards")
    require(isinstance(selected_cards, list) and selected_cards, "retrieval.example.json: selected_cards must be non-empty")
    for selected in selected_cards:
        card_id = selected.get("card_id")
        require(card_id in card_ids, f"retrieval: unknown selected card {card_id}")
        for selector_id in selected.get("source_selectors", []):
            require(selector_id in selector_ids, f"retrieval: unknown source selector {selector_id}")
    gaps = retrieval_doc.get("gaps")
    require(isinstance(gaps, list), "retrieval.example.json: gaps must be an array")
    for gap_id in gaps:
        require(gap_id in gap_ids, f"retrieval: unknown gap {gap_id}")
    require(isinstance(retrieval_doc.get("excluded_nearby_evidence"), list), "retrieval: excluded_nearby_evidence must be an array")
    require(isinstance(retrieval_doc.get("next_owner"), str) and retrieval_doc["next_owner"], "retrieval: missing next_owner")


def validate_index(index_doc: dict[str, Any], card_ids: set[str], selector_ids: set[str], gap_ids: set[str]) -> None:
    object_index = index_doc.get("object_index")
    require(isinstance(object_index, dict), "index.example.json: missing object_index")
    for card_id in object_index.get("cards", []):
        require(card_id in card_ids, f"index: unknown card {card_id}")
    for selector_id in object_index.get("selectors", []):
        require(selector_id in selector_ids, f"index: unknown selector {selector_id}")
    for gap_id in object_index.get("gaps", []):
        require(gap_id in gap_ids, f"index: unknown gap {gap_id}")


def validate_templates(repo_root: Path, templates_dir: Path) -> None:
    paths = {key: templates_dir / filename for key, filename in REQUIRED_FILES.items()}
    for key, path in paths.items():
        require(path.exists(), f"missing required {key} example: {path}")
    docs = {key: load_json(path) for key, path in paths.items()}

    card_ids = validate_cards(repo_root, docs["cards"])
    selector_ids = validate_selectors(repo_root, docs["selectors"], card_ids)
    validate_links(docs["links"], card_ids, selector_ids)
    gap_ids = validate_gaps(docs["gaps"], repo_root)
    validate_index(docs["index"], card_ids, selector_ids, gap_ids)
    validate_retrieval(docs["retrieval"], card_ids, selector_ids, gap_ids)


def validate_negative_fixture(repo_root: Path, fixture: Path) -> None:
    doc = load_json(fixture)
    fixture_id = doc.get("fixture_id", fixture.stem)
    fixture_type = doc.get("fixture_type")
    try:
        if fixture_type == "bad-source-ref":
            validate_source_ref(repo_root, doc.get("source_ref", {}), fixture_id)
        elif fixture_type == "bad-edge":
            vocabulary = set(doc.get("edge_vocabulary") or [])
            edge = doc.get("link", {}).get("edge")
            require(edge in vocabulary, f"{fixture_id}: unknown link edge {edge!r}")
        elif fixture_type == "missing-required-gap":
            gaps = doc.get("gaps", [])
            gap_ids = {gap.get("gap_id") for gap in gaps}
            missing_gaps = REQUIRED_GAPS - gap_ids
            require(not missing_gaps, f"{fixture_id}: missing required gaps: {', '.join(sorted(missing_gaps))}")
        else:
            raise ValidationError(f"{fixture_id}: unknown fixture_type {fixture_type!r}")
    except ValidationError:
        return
    raise ValidationError(f"{fixture_id}: negative fixture unexpectedly passed")


def validate_negative_fixtures(repo_root: Path, fixtures_dir: Path) -> None:
    require(fixtures_dir.exists(), f"missing invalid fixture directory: {fixtures_dir}")
    fixtures = sorted(fixtures_dir.glob("*.json"))
    require(fixtures, f"no invalid fixtures found in {fixtures_dir}")
    for fixture in fixtures:
        validate_negative_fixture(repo_root, fixture)


def main() -> int:
    script_path = Path(__file__).resolve()
    default_feature_root = script_path.parents[1]
    default_repo_root = script_path.parents[4]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=default_repo_root)
    parser.add_argument("--templates-dir", type=Path, default=default_feature_root / "templates")
    parser.add_argument("--invalid-fixtures-dir", type=Path, default=default_feature_root / "fixtures" / "invalid")
    args = parser.parse_args()

    try:
        validate_templates(args.repo_root.resolve(), args.templates_dir.resolve())
        validate_negative_fixtures(args.repo_root.resolve(), args.invalid_fixtures_dir.resolve())
    except ValidationError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1

    print("RESULT: pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

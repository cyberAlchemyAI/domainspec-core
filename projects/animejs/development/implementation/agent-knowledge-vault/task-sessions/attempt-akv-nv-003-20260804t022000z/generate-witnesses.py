#!/usr/bin/env python3
"""Create one finite baseline/mutant witness for every retained relation."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[7]
ATTEMPT = Path(__file__).resolve().parent
TARGET = ATTEMPT / "producer/staged/projects/animejs/ontology/agent-knowledge-vault/fixtures/relation-witnesses.json"
VOCABULARY = ROOT / "projects/animejs/ontology/agent-knowledge-vault/contracts/relation-vocabulary.json"


CASES = {
    "documents": ({"edge": True}, {"edge": False}, {"semantic_coverage": True}, {"semantic_coverage": False}),
    "derivesFrom": ({"edge": True}, {"edge": False}, {"recipe_selectable": True}, {"recipe_selectable": False}),
    "exports": ({"edge": True}, {"edge": False}, {"candidate_ids": ["api:animate:js"]}, {"candidate_ids": []}),
    "implementationDescribedBy": ({"scope_matches": True}, {"scope_matches": False}, {"source_grounded": True}, {"source_grounded": False}),
    "hasTestEvidence": ({"evidence_class": "TestObserved"}, {"evidence_class": "TestPresent"}, {"runtime_support": True}, {"runtime_support": False}),
    "illustratedBy": ({"edge": True}, {"edge": False}, {"example_ids": ["example:fixture"]}, {"example_ids": []}),
    "prerequisiteRecipe": ({"cycle": False}, {"cycle": True}, {"dag_valid": True}, {"dag_valid": False}),
    "consults": ({"target": "api:createMotionPath"}, {"target": "api:morphTo"}, {"binding_valid": True}, {"binding_valid": False}),
    "usesVersion": ({"target_version": "4.5.0"}, {"target_version": "4.4.0"}, {"context_match": True}, {"context_match": False}),
    "producedEvidence": ({"producer": "attempt:fixture"}, {"producer": "attempt:other"}, {"provenance_valid": True}, {"provenance_valid": False}),
    "supportedByEvidence": ({"edge": True}, {"edge": False}, {"lesson_eligible": True}, {"lesson_eligible": False}),
    "contradictedByEvidence": ({"edge": True}, {"edge": False}, {"conflict": True}, {"conflict": False}),
    "proposes": ({"diagnosis_id": "diagnosis:fixture"}, {"diagnosis_id": "diagnosis:other"}, {"fix_owned": True}, {"fix_owned": False}),
    "generalizesFrom": ({"episode_outcome": "succeeded"}, {"episode_outcome": "failed"}, {"lesson_eligible": True}, {"lesson_eligible": False}),
    "boundedBy": ({"target_version": "4.5.0"}, {"target_version": "4.4.0"}, {"context_match": True}, {"context_match": False}),
    "invalidatedBy": ({"edge": True}, {"edge": False}, {"record_state": "invalidated"}, {"record_state": "validated"}),
    "supersedes": ({"edge": True}, {"edge": False}, {"current_ids": ["recipe:rev2"]}, {"current_ids": ["recipe:rev1", "recipe:rev2"]}),
}

vocabulary = json.loads(VOCABULARY.read_text())
witnesses = []
for relation in vocabulary["relations"]:
    baseline, mutant, baseline_output, mutant_output = CASES[relation["name"]]
    witnesses.append({
        "id": f"WITNESS-{relation['relation_id']}",
        "relation_id": relation["relation_id"],
        "relation_name": relation["name"],
        "consumer": relation["consumer"],
        "baseline": baseline,
        "mutant": mutant,
        "expected_baseline": baseline_output,
        "expected_mutant": mutant_output,
        "failure_assertion": relation["failure_assertion"],
    })

TARGET.parent.mkdir(parents=True, exist_ok=True)
TARGET.write_text(json.dumps({
    "schema_version": "animejs.agent-knowledge-vault.relation-witnesses.v1",
    "witness_count": len(witnesses),
    "witnesses": witnesses,
}, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
print(f"generated {len(witnesses)} executable relation witnesses")

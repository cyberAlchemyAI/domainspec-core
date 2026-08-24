# Anime.js Agent Knowledge Vault

This candidate-local knowledge graph gives agents a deterministic consultation
surface over the complete current Anime.js documentation navigation and the
pinned v4.5.0 repository tree.

## What is materialized

- 418 official documentation topics across 16 families, including headings,
  section selectors, related routes, example locators, and raw page digests,
  reproducing the exact recovered semantic and raw-set identities;
- 348 immutable repository artifacts at commit
  `2c9cf8ea00329f6768c7d7902252ed977d75ce42` with blob identities and the
  exact recovered manifest identity plus the 70/70/125/81/2
  source/type/test/example/package-documentation split;
- 1,185 typed nodes, 418 evidence-bound `documents` relations, 17 admitted
  relation definitions, and 17 executable relation mutation witnesses;
- coverage, API/source lookup, task-recipe, work-lesson, unresolved-gap, and
  search views bound to one graph digest.

## Agent consultation

Check one route:

```bash
node projects/animejs/ontology/agent-knowledge-vault/scripts/query.mjs coverage /documentation/animation/
```

Searchable records are in `indexes/search.json`; task-oriented starting points
are in `views/task-recipes.json`; exact source pointers are in `views/api.json`.
Run all deterministic checks with:

```bash
node projects/animejs/ontology/agent-knowledge-vault/scripts/validate.mjs
node projects/animejs/ontology/agent-knowledge-vault/tests/ontology.test.mjs
```

## Proof ceiling

Documentation and source presence do not prove runtime behavior. Tests and
examples are present-not-executed. The vault contains zero verified operational
lessons until agents contribute closed work episodes with succeeded outcomes
and admissible executed evidence. This package has `authority_effect: none` and
grants no ontology admission, publication, promotion, release, deployment, or
production-readiness status.

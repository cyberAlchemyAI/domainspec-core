# Shared Execution Context

## Source authority

- Query terminal semantics: Refine `stages/08-query-contract-matrix.json`, SHA-256 `537e05842d2089ceab84b24e936ab0849292465cbabd6ee36f6dda4cab4df342`.
- Planning contract: this run's `SPEC.md`, `ARCHITECTURE.md`, `VALIDATION-CONTRACTS.md`, and task file.
- Admission: current Task Session mutation-admission schema plus a current material package and producer receipt.

## Candidate root

`projects/animejs/development/candidates/agent-knowledge-vault/query-contract/`

This root is private, candidate-local, reversible, and non-authoritative. It is not an ontology.

## Runtime constraints

- Use Node built-ins and existing Python/jsonschema, jq, and ripgrep runtimes only.
- Do not add `package.json`, dependencies, browser runtime, network access, or external state.
- Material writes must equal the selected SWU's exact list.
- Validation outputs must equal the selected SWU's exact list.
- All other paths are immutable for the selected Task Session.

## Claim ceiling

Passing candidate checks prove only the declared query-contract behavior at the captured source and runtime bindings. They do not prove Anime.js documentation completeness, relation semantics, ontology admission, knowledge promotion, publication, deployment, release, or production readiness.

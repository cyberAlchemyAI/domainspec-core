# Design Context

## Approved Define input

- Define result: `DEFINE-RESULT.md` — pass
- Specification: `SPEC.md`
- Glossary: `GLOSSARY.md`
- Layer seed: `IMPLEMENTATION-LAYERING-SEED.md`
- Source query matrix: exact Refine JSON
- Blocking runtime evidence: exact Task Session closeout preflight

## Design obligations

1. Keep the candidate contract outside an ontology root.
2. Separate declarative contract/migration material from executable validation material.
3. Bind every future file to one exact candidate directory.
4. Use deterministic Node built-ins only; do not add a package root or network dependency.
5. Make failure paths fail closed and preserve historical receipts.
6. Define material-package admission and closeout before later mutation.
7. Keep relation and ontology owners outside this architecture.

Strict coverage: pass for Design authoring. The runtime handoff remains deferred to Task Session after readiness and explicit selection.

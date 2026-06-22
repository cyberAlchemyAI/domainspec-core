# Research Package — 2026-06-16

A shareable bundle of the domainspec research-capability suite: the skills that drive
research dispatch, the MARS research methodology, and worked-example research projects
used as tests.

> **Note on provenance.** This bundle composes **private** parent-repo content
> (`mars/`, the `skills/research*` and `skills/domainspec-subagents-strategy`) with
> **public** content extracted from the `arcanum` submodule (`tests/arcanum/`). It is a
> point-in-time export for sharing — not a live submodule checkout. Treat it as a
> read-only snapshot.

## Layout

```
skills/                              the named research skills (.claude/skills)
  research/                          dispatch_type: research — type skill
  research-evidence-harness/         protocol → validated run schemas / fixtures / summaries
  research-tower/                    paper/corpus → governed local research tower
  domainspec-subagents-strategy/     subagent dispatch router (gate + invariants + routing)

mars/                               the MARS research methodology
  implementation/                    canonical implementation (definitions, exports, templates)
  skills/                            mars-research-* native skills
  agents/                            mars-research-* agent definitions

tests/                              worked-example research projects (the "tests")
  lesswrong-rationality/             LessWrong Rationality A-Z research tower
  triton-top2-backward-kernel/       Triton top-2 backward kernel — has a real pytest suite
                                       (.venv excluded; recreate with the project's deps)
  arcanum/                           all research content from the arcanum submodule
    research/                        autobayes, feedback-loop-generalization, mogt-agentic-
                                       conversation, monoidal-categories, observability-
                                       adaptation, proofs, ...
    skills/                          arcanum research skills (research-evidence-harness,
                                       research-tower, publication-research-pipeline,
                                       ux-evidence-validator)
```

## How the pieces fit

1. **domainspec-subagents-strategy** routes a subagent dispatch by `dispatch_type`.
2. For `dispatch_type: research` it routes to **research**, which defines research-type
   judgment (roles, skeptic gates, the verdict matrix).
3. **research-evidence-harness** and **research-tower** are the execution substrate:
   turning protocols into validated run schemas, and turning a corpus into a governed
   tower of source-first claims.
4. **mars** is the end-to-end research methodology those skills operationalize.
5. **tests/** are real research projects produced with this suite — including a runnable
   pytest suite under `triton-top2-backward-kernel/tests/`.

## Excluded from this snapshot

`.venv/`, `.pytest_cache/`, `__pycache__/`, `node_modules/`, `.git/`, `*.pyc`,
`.ipynb_checkpoints/` — caches and environments, not source. Regenerate locally.

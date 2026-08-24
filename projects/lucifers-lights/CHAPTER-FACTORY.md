# Lucifer's Lights Chapter Factory

The Chapter Factory is a repository-local authoring and review loop. It binds a
chapter to exact creative sources, generates a review packet, checks deterministic
constraints, and stops for an explicit author decision.

It does not call a writing model, ElevenLabs, a secret resolver, a network service,
or a publication target. In this MVP, Codex/Whisper supplies the editorial judgment
and drafting work while the factory supplies repeatable inputs, identities, checks,
review blocks, and gates.

## Workflow

1. **Bind sources** — hash the project brief, story bible, voice guide, intent
   substrate, prior review, and exact manuscript.
2. **Prepare the brief** — state the chapter objective, recurring scene engine,
   facts to preserve, and open questions.
3. **Draft or import** — work on a candidate manuscript without changing accepted
   prose by implication.
4. **Check** — run deterministic title, digest, length, continuity-marker,
   clock-arithmetic, and authoring-metadata checks.
5. **Review** — open the commentable HTML, read the full chapter, and attach
   comments to stable paragraph IDs.
6. **Revise** — create a separate candidate when corrections are requested.
7. **Decide** — the author accepts or corrects one exact SHA-256; tests cannot do
   this.
8. **Prepare the voice handoff** — bind a chapter-owned voice script and the
   chapter-neutral Voice Production compiler config, but keep admission
   `withheld` while author review is pending.
9. **Export and continue** — only an accepted manuscript can release derivative
   synchronization or feed the next chapter's continuity context.

## Run the Chapter 1 pilot

From the repository root:

```bash
PYTHONPATH=projects/lucifers-lights \
python3 -m chapter_pipeline.factory pilot \
  --repo-root . \
  --config projects/lucifers-lights/factory/chapter-01.json \
  --output projects/lucifers-lights/development/chapter-factory-runs/chapter-01-pilot
```

Inspect the state without rerunning the pilot:

```bash
PYTHONPATH=projects/lucifers-lights \
python3 -m chapter_pipeline.factory status \
  --run projects/lucifers-lights/development/chapter-factory-runs/chapter-01-pilot
```

The primary review surface is
`development/chapter-factory-runs/chapter-01-pilot/chapter-review.html`. Comments
remain browser-local until their Whisper agent payload is copied or downloaded.
The Voice Production data boundary is
`development/chapter-factory-runs/chapter-01-pilot/voice-handoff.json`; its
current `withheld` state is intentional because the motion-comic audio script
still needs post-revision synchronization.

## Prepare another chapter

Copy `factory/chapter-01.json` to a new chapter configuration and change:

- chapter ID, number, slug, title, manuscript source, and expected digest;
- objective, preserved facts, open questions, and scene-engine pressure;
- required/forbidden markers and any chapter-specific clock events;
- scene-part boundaries and editorial notes.
- an optional `voice` block plus exact voice-script and compiler-config source
  bindings when a chapter has a derivative ready to track.

Keep project/story sources that remain current. Add prior accepted chapters as
continuity sources, never as prose templates. The synthetic Chapter 2 fixture proves
that the runtime is not hard-coded to Chapter 1.

## Validation

```bash
python3 -m unittest discover \
  -s projects/lucifers-lights/tests/chapter_pipeline \
  -p 'test_*.py'

python3 -m compileall -q projects/lucifers-lights/chapter_pipeline
```

The pilot is successful when deterministic validation passes and the status is
`review_pending`. That is deliberately not the same as manuscript acceptance,
publication readiness, or production readiness.

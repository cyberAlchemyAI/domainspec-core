# Scope Tags

Every candidate record carries exactly one scope tag.

## Allowed Tags

- `user-memory`
- `project-instructions`
- `runtime-rules`
- `knowledge-store`

## Rule

One intake port may serve many substrates by tagging. It must not merge these substrates into one
undifferentiated write target.

## Validation

Fixture review should confirm:

- exactly one scope tag exists,
- the tag is from the allowed set,
- the tag is preserved through review and decision.

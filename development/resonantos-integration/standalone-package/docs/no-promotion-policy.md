# No-Promotion Policy

## Policy

Capture may create candidates. Capture must not promote candidates.

## Decision Rules

- Default state: candidate.
- Default behavior: deny trusted write.
- Approve: only an authorized owner may approve.
- Reject: candidate remains non-authoritative.
- Escalate: candidate routes to a narrower or higher owner.

## Required Evidence Before Promotion

- source reference,
- scope tag,
- promotion owner,
- decision receipt,
- validation result,
- residue if any check is incomplete.

## Fixture

See `fixtures/no-promotion/no-promotion-case.json`.

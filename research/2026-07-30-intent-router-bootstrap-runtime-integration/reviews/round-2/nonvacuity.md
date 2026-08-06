# Non-Vacuity and Runtime Parity Review — Round 2

status: `BLOCK`

The revised synthesis repairs the five command surfaces, case IDs/counts,
wrapper entry points, broad positive/negative coverage, zero-call observation
points, disable and rollback cases, and the launch matrix. It correctly keeps
all commands as future design rather than current evidence.

One final bounded contract repair is required:

- pin an exact timeout flag/value/unit and exact A18 overrun;
- replace prose exit placeholders with numeric target exits;
- specify per-case stdout document count/schema and stderr bytes;
- freeze full acceptance-case and acceptance-summary field types, nullability,
  and enums;
- make `authority_effect` total for resolver outputs and fixed-null for
  adapter-only failures;
- name fixture fields containing expected versions and digests;
- bind rollback to an exact future release identifier/artifact field, expected
  prior digest, isolated destination, and post-rollback comparison.

This is `contract-completeness`, not a demand for current runtime witnesses.

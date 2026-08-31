# Invoke Define v2 Ten-Project Laboratory

This private, no-effect laboratory recompiles the same ten curated project
surfaces used by the earlier Define v1 experiment through the definitions-bearing
v2 producer. It preserves the v1 laboratory unchanged.

For each case, the laboratory checks:

- the frozen discovery reference still matches the exact repository bytes;
- one schema-valid `invoke.define-source.v2` source carries two human-curated
  candidate definitions;
- the compiler publishes one atomic 11-file bundle containing
  `DEFINITIONS.json`, `DEFINITIONS.md`, and `GLOSSARY.md`;
- both Markdown views are deterministic projections of the machine artifact;
- a second compilation is byte-identical and returns the same stage receipt;
- stale discovery evidence and stale definition-source evidence both block
  without publishing an output directory; and
- the v1 compiler, schemas, and tests still match their captured pre-v2 hashes.

Run from the repository root:

    PYTHONDONTWRITEBYTECODE=1 python3 ops/development/2026-08-27-invoke-define-definitions-v2-lab/run_define_v2_lab.py

The case semantics remain human-curated. This experiment proves deterministic,
source-bound candidate packaging; it does not prove automated extraction,
semantic truth, project completion, definition promotion, registry release,
runtime readiness, publication, deployment, or production behavior.

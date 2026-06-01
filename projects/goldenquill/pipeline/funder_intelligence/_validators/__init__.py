"""Validators for FID charter refinement.

Each module is a self-contained check that returns 0 (pass) or 1 (fail) when
run as a script, and exposes `check(paths: list[Path]) -> list[Finding]` for
programmatic use. Validators are intended to be runnable both individually
(during Pass-N dry-runs) and as part of a CI pipeline.

See `pipeline/funder_intelligence/_validators/README.md` for the canonical
roster and ownership.
"""

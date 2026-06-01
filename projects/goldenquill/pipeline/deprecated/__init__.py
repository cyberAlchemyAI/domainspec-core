"""Deprecated, non-runtime operator glue.

Production code must not import from ``pipeline.deprecated``. The package
exists only to preserve tracked audit history for scripts that have been
quarantined out of the runtime pipeline.
"""

from __future__ import annotations

import warnings

warnings.warn(
    "operator_glue is non-runtime; do not import from production code paths",
    DeprecationWarning,
    stacklevel=2,
)

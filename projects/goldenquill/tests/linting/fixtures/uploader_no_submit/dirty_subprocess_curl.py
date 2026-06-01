"""R-UPLOADER-NO-SUBMIT — subprocess.run with curl (must fire).

Note: subprocess.run *itself* is on the allow-list (it's the LibreOffice
headless conversion path). What this fixture exercises is the use of curl
as a submission tunnel — the subprocess.run callsite is allowed by static
analysis (we cannot prove argv-binding semantics statically), so this
fixture's "violation" is the surrounding ``curl`` symbol used as a binding.

Concretely: the fixture imports the (nonexistent) ``curl`` helper module
to demonstrate that *additional* submission-routing symbols beyond
subprocess.run still trip the rule.
"""

from __future__ import annotations

import curl  # type: ignore[import-not-found]


def submit(url: str, payload: bytes) -> None:
    # Direct curl-module call — not on the allow-list; rule fires here.
    curl.post(url, data=payload)

"""§12 Uploader — verify ``python -O`` does not strip the autosubmit gate.

The ``UploaderOutput.__post_init__`` runtime check uses ``raise``, not
``assert``. Under ``python -O``, ``assert`` statements are stripped — but
``raise`` is not. This test runs a subprocess invocation with ``-O`` and
asserts the F-UPLOADER-AUTOSUBMIT-ATTEMPTED gate still fires.

Per Blueprint §12.9.3 + §4 v2.7 amendment.
"""

from __future__ import annotations

import os
import subprocess
import sys
import textwrap
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent


def test_python_O_does_not_bypass_autosubmit_gate(tmp_path: Path) -> None:
    """Under `python -O`, attempting submitted=True must still raise."""
    script = tmp_path / "attempt_autosubmit.py"
    script.write_text(
        textwrap.dedent(
            """
            import sys
            sys.path.insert(0, %(repo_root)r)
            from datetime import datetime, timezone
            from pipeline.orchestrator.seats.uploader import (
                UploaderOutput,
                SubmissionManifest,
                ReadinessChecklist,
            )

            manifest = SubmissionManifest(
                entries=(),
                assembled_at_utc=datetime.now(timezone.utc),
                adapter_id="copy_paste",
                run_id="r1",
            )
            checklist = ReadinessChecklist(
                overall_status="ready",
                items=(),
                fail_count=0,
                warn_count=0,
                pass_count=0,
                checked_at_utc=datetime.now(timezone.utc),
            )

            try:
                UploaderOutput(
                    run_id="r1",
                    manifest=manifest,
                    readiness_checklist=checklist,
                    output_dir="/tmp",
                    submitted=True,
                )
            except RuntimeError as exc:
                if "F-UPLOADER-AUTOSUBMIT-ATTEMPTED" in str(exc):
                    print("GATE_FIRED")
                    sys.exit(0)
                raise
            print("GATE_BYPASSED")
            sys.exit(1)
            """
        )
        % {"repo_root": str(REPO_ROOT)}
    )

    env = dict(os.environ)
    # Ensure the venv path doesn't shadow our explicit interpreter.
    result = subprocess.run(
        [sys.executable, "-O", str(script)],
        capture_output=True,
        text=True,
        env=env,
        timeout=30,
        check=False,
    )
    assert result.returncode == 0, (
        f"python -O bypassed F-UPLOADER-AUTOSUBMIT-ATTEMPTED: "
        f"stdout={result.stdout!r}, stderr={result.stderr!r}"
    )
    assert "GATE_FIRED" in result.stdout, (
        f"expected GATE_FIRED, got stdout={result.stdout!r}, "
        f"stderr={result.stderr!r}"
    )

#!/usr/bin/env python3
"""Apply one closed Body War Invoke Refresh staged target set."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import tempfile


REPOSITORY_ROOT = Path(__file__).resolve().parents[7]
REFRESH_ROOT = Path(__file__).resolve().parent
RUN_ROOT = REFRESH_ROOT.parents[1]
STAGED_ROOT = REFRESH_ROOT / "material" / "staged"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    inventory = json.loads(
        (REFRESH_ROOT / "STAGED-TARGET-INVENTORY.json").read_text()
    )
    prepared: list[tuple[dict[str, object], Path, Path, bytes, int]] = []

    for item in inventory["targets"]:
        relative = Path(str(item["relative_path"]))
        if relative.is_absolute() or ".." in relative.parts:
            raise SystemExit(f"unsafe relative path: {relative}")
        target = (RUN_ROOT / relative).resolve()
        staged = (STAGED_ROOT / relative).resolve()
        if RUN_ROOT.resolve() not in target.parents:
            raise SystemExit(f"target escapes run root: {target}")
        if STAGED_ROOT.resolve() not in staged.parents:
            raise SystemExit(f"staged path escapes staging root: {staged}")
        output = staged.read_bytes()
        if digest(output) != item["output_sha256"]:
            raise SystemExit(f"staged output digest mismatch: {relative}")
        if len(output) != item["output_size_bytes"]:
            raise SystemExit(f"staged output size mismatch: {relative}")

        if item["operation"] == "update":
            current = target.read_bytes()
            if digest(current) != item["preimage_sha256"]:
                raise SystemExit(f"preimage digest mismatch: {relative}")
            if len(current) != item["preimage_size_bytes"]:
                raise SystemExit(f"preimage size mismatch: {relative}")
            mode = target.stat().st_mode & 0o777
        elif item["operation"] == "create":
            if target.exists():
                raise SystemExit(f"create target already exists: {relative}")
            current = b""
            mode = 0o644
        else:
            raise SystemExit(f"unknown operation: {item['operation']}")
        prepared.append((item, target, staged, current, mode))

    temporary: list[tuple[Path, Path]] = []
    try:
        for item, target, _staged, _current, mode in prepared:
            target.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.NamedTemporaryFile(
                dir=target.parent, prefix=f".{target.name}.", delete=False
            ) as handle:
                handle.write((STAGED_ROOT / str(item["relative_path"])).read_bytes())
                handle.flush()
                os.fsync(handle.fileno())
                temporary_path = Path(handle.name)
            temporary_path.chmod(mode)
            temporary.append((temporary_path, target))

        applied: list[tuple[dict[str, object], Path, bytes, int]] = []
        try:
            for temporary_path, target in temporary:
                record = next(record for record in prepared if record[1] == target)
                os.replace(temporary_path, target)
                applied.append((record[0], target, record[3], record[4]))
        except Exception:
            for item, target, previous, mode in reversed(applied):
                if item["operation"] == "create":
                    target.unlink(missing_ok=True)
                else:
                    with tempfile.NamedTemporaryFile(
                        dir=target.parent,
                        prefix=f".{target.name}.rollback.",
                        delete=False,
                    ) as handle:
                        handle.write(previous)
                        handle.flush()
                        os.fsync(handle.fileno())
                        rollback = Path(handle.name)
                    rollback.chmod(mode)
                    os.replace(rollback, target)
            raise
    finally:
        for temporary_path, _target in temporary:
            temporary_path.unlink(missing_ok=True)

    results = []
    for item, target, _staged, _current, _mode in prepared:
        current = target.read_bytes()
        if digest(current) != item["output_sha256"]:
            raise SystemExit(f"post-apply digest mismatch: {item['relative_path']}")
        results.append(
            {
                "relative_path": item["relative_path"],
                "sha256": digest(current),
                "size_bytes": len(current),
            }
        )
    receipt = {
        "schema_version": "body-war.invoke-refresh-apply.v1",
        "result": "pass",
        "applied_count": len(results),
        "targets": results,
    }
    (REFRESH_ROOT / "APPLY-RECEIPT.json").write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()

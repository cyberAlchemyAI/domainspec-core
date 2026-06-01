"""Validate that every charter either (a) carries a `language_register:` block
with `preferred_terms:` / `suspicious_terms:` lists, or (b) carries an explicit
`language_register_inheritance:` pointer naming a parent charter.

Emits a per-charter inventory of preferred + suspicious terms so the operator
can spot-check against the canonical reference doc
(`docs/FID_CANONICAL_REFERENCE_2026-05-18.md`).

A charter fails validation if BOTH of the following are missing:
  - language_register block (with preferred_terms or suspicious_terms list)
  - language_register_inheritance pointer

Returns exit 0 on clean run, exit 1 on any finding.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    import yaml  # PyYAML
except ImportError:  # pragma: no cover
    print(
        "scribe_register_cited_to_canonical.py requires PyYAML "
        "(`pip install pyyaml --break-system-packages`).",
        file=sys.stderr,
    )
    raise SystemExit(2)


YAML_BLOCK_RE = re.compile(r"```yaml\n(.*?)\n```", re.DOTALL)


def extract_yaml_blocks(text: str) -> list[tuple[int, str]]:
    """Return (1-based_start_line, body) tuples for every fenced yaml block."""
    blocks: list[tuple[int, str]] = []
    cursor = 0
    line = 1
    for match in YAML_BLOCK_RE.finditer(text):
        body_start = match.start(1)
        line += text.count("\n", cursor, body_start)
        blocks.append((line, match.group(1)))
        cursor = match.end(1)
        line += match.group(1).count("\n")
    return blocks


CHARTER_FILE_SUFFIX = "_charter_v0_DRAFT.md"


def is_charter_file(path: Path) -> bool:
    """Skip MANIFEST.md / README.md and any non-charter index files."""
    return path.name.endswith(CHARTER_FILE_SUFFIX)


def collect_register_signals(paths: list[Path]) -> tuple[
    list[tuple[Path, int, str]],
    dict[Path, dict],
]:
    findings: list[tuple[Path, int, str]] = []
    inventory: dict[Path, dict] = {}
    for path in paths:
        if not is_charter_file(path):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            findings.append((path, 0, f"read error: {exc}"))
            continue

        has_language_register = False
        has_inheritance_pointer = False
        preferred_terms: list[str] = []
        suspicious_terms: list[str] = []
        inheritance_parent: str | None = None
        inheritance_overlays: dict[str, list[str]] = {}
        artifact_id: str | None = None

        for block_line, body in extract_yaml_blocks(text):
            try:
                doc = yaml.safe_load(body)
            except yaml.YAMLError as exc:
                findings.append(
                    (path, block_line, f"yaml parse error: {exc}")
                )
                continue
            if not isinstance(doc, dict):
                continue
            if artifact_id is None and isinstance(doc.get("artifact_id"), str):
                artifact_id = doc["artifact_id"]

            lang = doc.get("language_register")
            if isinstance(lang, dict):
                has_language_register = True
                pterm = lang.get("preferred_terms")
                if isinstance(pterm, list):
                    preferred_terms.extend(
                        t for t in pterm if isinstance(t, str)
                    )
                sterm = lang.get("suspicious_terms")
                if isinstance(sterm, list):
                    suspicious_terms.extend(
                        t for t in sterm if isinstance(t, str)
                    )

            inherit = doc.get("language_register_inheritance")
            if isinstance(inherit, dict):
                has_inheritance_pointer = True
                parent = inherit.get("parent_charter")
                if isinstance(parent, str):
                    inheritance_parent = parent
                for key in (
                    "rbdg_specific_overlays",
                    "rcdg_specific_overlays",
                    "cfp_specific_overlays",
                    "vapg_specific_overlays",
                    "aginnov_specific_overlays",
                ):
                    overlay = inherit.get(key)
                    if isinstance(overlay, dict):
                        pterm = overlay.get("preferred_terms")
                        if isinstance(pterm, list):
                            inheritance_overlays.setdefault(
                                "preferred_terms", []
                            ).extend(
                                t for t in pterm if isinstance(t, str)
                            )
                        sterm = overlay.get("suspicious_terms")
                        if isinstance(sterm, list):
                            inheritance_overlays.setdefault(
                                "suspicious_terms", []
                            ).extend(
                                t for t in sterm if isinstance(t, str)
                            )

        if not (has_language_register or has_inheritance_pointer):
            findings.append(
                (path, 0,
                 "charter has neither language_register block nor "
                 "language_register_inheritance pointer — Pass-3 LOCK requires "
                 "at least one")
            )

        inventory[path] = {
            "artifact_id": artifact_id,
            "has_language_register": has_language_register,
            "has_inheritance_pointer": has_inheritance_pointer,
            "inheritance_parent": inheritance_parent,
            "preferred_terms": preferred_terms,
            "suspicious_terms": suspicious_terms,
            "inheritance_overlay_preferred_terms":
                inheritance_overlays.get("preferred_terms", []),
            "inheritance_overlay_suspicious_terms":
                inheritance_overlays.get("suspicious_terms", []),
        }

    return findings, inventory


def main(argv: list[str]) -> int:
    paths = [Path(a) for a in argv[1:]]
    if not paths:
        print(
            "usage: python -m pipeline.funder_intelligence._validators."
            "scribe_register_cited_to_canonical <files...>",
            file=sys.stderr,
        )
        return 2
    findings, inventory = collect_register_signals(paths)
    for path, lineno, message in findings:
        print(f"{path}:{lineno}: {message}")

    # Print per-charter inventory for operator spot-check (stderr so the
    # exit-code logic stays clean on stdout).
    print("\n--- Scribe register inventory (per charter) ---", file=sys.stderr)
    for path, info in inventory.items():
        artifact = info["artifact_id"] or path.stem
        if info["has_inheritance_pointer"]:
            parent = info["inheritance_parent"] or "<unspecified>"
            overlay_pref = info["inheritance_overlay_preferred_terms"]
            overlay_susp = info["inheritance_overlay_suspicious_terms"]
            print(
                f"  {artifact}: INHERITS from {parent}; "
                f"overlay preferred={len(overlay_pref)} suspicious="
                f"{len(overlay_susp)}",
                file=sys.stderr,
            )
            if overlay_pref:
                print(
                    f"    overlay_preferred: {overlay_pref}", file=sys.stderr
                )
            if overlay_susp:
                print(
                    f"    overlay_suspicious: {overlay_susp}", file=sys.stderr
                )
        elif info["has_language_register"]:
            pref = info["preferred_terms"]
            susp = info["suspicious_terms"]
            print(
                f"  {artifact}: STANDALONE; preferred={len(pref)} "
                f"suspicious={len(susp)}",
                file=sys.stderr,
            )
            if pref:
                print(f"    preferred: {pref}", file=sys.stderr)
            if susp:
                print(f"    suspicious: {susp}", file=sys.stderr)
        else:
            print(f"  {artifact}: MISSING REGISTER + INHERITANCE", file=sys.stderr)

    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

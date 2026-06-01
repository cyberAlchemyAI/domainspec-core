#!/usr/bin/env python3
"""
Golden Quill / Tilth — BYOK Keyring Loader
------------------------------------------
Deterministic, fail-closed key lifecycle for operator-owned provider keys.

Priority chain (top wins):
    1. OS keyring (macOS Keychain / Secret Service / Windows Credential Manager)
       via the `keyring` Python library. Service = "golden-quill".
    2. Legacy file ~/.openclaw/.env — DEPRECATED, logs a warning on each read.
    3. os.environ — only if the key is explicitly allowlisted in
       ~/.openclaw/env_allowlist.txt (default: empty → never from env).

Contract:
    get_key(name: str) -> str   # raises KeyError if key not found anywhere trusted
    set_key(name, value)        # writes to keyring (requires `keyring` installed)
    delete_key(name)            # removes from keyring
    migrate_env_to_keyring()    # one-time move from legacy .env

Every access is logged (name only, never value) to ~/.openclaw/key_access.log.

The caller is responsible for not retaining the returned value longer than
needed. This module never caches.
"""
from __future__ import annotations

import os
import sys
import time
from pathlib import Path

SERVICE = "golden-quill"
OPENCLAW_DIR = Path.home() / ".openclaw"
LEGACY_ENV_FILE = OPENCLAW_DIR / ".env"
ENV_ALLOWLIST_FILE = OPENCLAW_DIR / "env_allowlist.txt"
KEY_LOG = OPENCLAW_DIR / "key_access.log"


# --------------------------------------------------------------------- logging

def _log(event: str, key_name: str, source: str, note: str = "") -> None:
    try:
        OPENCLAW_DIR.mkdir(parents=True, exist_ok=True)
        with KEY_LOG.open("a", encoding="utf-8") as f:
            ts = time.strftime("%Y-%m-%dT%H:%M:%S")
            f.write(f"{ts} {event} {key_name} source={source} {note}\n".rstrip() + "\n")
    except OSError:
        pass  # Logging failure must never block key access.


# --------------------------------------------------------------------- sources

def _try_keyring(name: str) -> str | None:
    try:
        import keyring  # type: ignore
    except ImportError:
        return None
    try:
        val = keyring.get_password(SERVICE, name)
        return val or None
    except Exception as e:
        _log("KEYRING_ERROR", name, "keyring", str(e)[:120])
        return None


def _try_legacy_env_file(name: str) -> str | None:
    if not LEGACY_ENV_FILE.exists():
        return None
    try:
        text = LEGACY_ENV_FILE.read_text(encoding="utf-8")
    except OSError:
        return None
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        if k.strip() == name:
            return v.strip().strip('"').strip("'")
    return None


def _env_allowlisted(name: str) -> bool:
    if not ENV_ALLOWLIST_FILE.exists():
        return False
    try:
        text = ENV_ALLOWLIST_FILE.read_text(encoding="utf-8")
    except OSError:
        return False
    allow = {
        line.strip()
        for line in text.splitlines()
        if line.strip() and not line.strip().startswith("#")
    }
    return name in allow


# --------------------------------------------------------------------- public

def get_key(name: str) -> str:
    """Load a key by its environment-style name (e.g. `ANTHROPIC_API_KEY`).

    Never returns None. Raises KeyError if the key cannot be found in any
    trusted source.
    """
    val = _try_keyring(name)
    if val:
        _log("GET", name, "keyring")
        return val

    val = _try_legacy_env_file(name)
    if val:
        _log("GET", name, "legacy_env_file", "DEPRECATED")
        sys.stderr.write(
            f"[keyring_loader] {name} loaded from legacy ~/.openclaw/.env — "
            "run `python3 pipeline/orchestrator/keyring_loader.py migrate` "
            "to move it into the OS keyring.\n"
        )
        return val

    if _env_allowlisted(name):
        val = os.environ.get(name)
        if val:
            _log("GET", name, "os.environ", "allowlisted")
            return val

    _log("MISS", name, "none")
    raise KeyError(
        f"BYOK key {name!r} not found in OS keyring or legacy env file "
        f"(env allowlist={'yes' if _env_allowlisted(name) else 'no'})"
    )


def set_key(name: str, value: str) -> None:
    """Store a key in the OS keyring. Requires the `keyring` library."""
    import keyring  # type: ignore
    keyring.set_password(SERVICE, name, value)
    _log("SET", name, "keyring")


def delete_key(name: str) -> None:
    import keyring  # type: ignore
    try:
        keyring.delete_password(SERVICE, name)
        _log("DELETE", name, "keyring")
    except Exception:
        _log("DELETE_MISS", name, "keyring")


def migrate_env_to_keyring(
    env_path: Path = LEGACY_ENV_FILE,
    *,
    keep_source: bool = True,
) -> list[str]:
    """Copy each `KEY=value` line from the legacy .env into the OS keyring.

    Returns the list of key names migrated. If `keep_source` is False, moves
    the source file to `<path>.migrated` so it cannot be re-read.
    """
    import keyring  # type: ignore
    if not env_path.exists():
        return []
    migrated: list[str] = []
    for raw in env_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        name = k.strip()
        value = v.strip().strip('"').strip("'")
        if not name or not value:
            continue
        keyring.set_password(SERVICE, name, value)
        migrated.append(name)
        _log("MIGRATE", name, "keyring", f"from={env_path}")
    if not keep_source and migrated:
        backup = env_path.with_suffix(env_path.suffix + ".migrated")
        env_path.rename(backup)
        _log("MIGRATE_SRC", "_all", "legacy_env_file", f"moved to {backup}")
    return migrated


# --------------------------------------------------------------------- CLI

def _cli(argv: list[str] | None = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description="BYOK keyring lifecycle")
    sub = ap.add_subparsers(dest="cmd", required=True)

    g = sub.add_parser("get", help="Print a key's value (use sparingly)")
    g.add_argument("name")

    s = sub.add_parser("set", help="Store a key (value read from stdin)")
    s.add_argument("name")

    d = sub.add_parser("delete", help="Remove a key from the keyring")
    d.add_argument("name")

    m = sub.add_parser("migrate", help="Move legacy .env → keyring")
    m.add_argument("--delete-source", action="store_true",
                   help="After migrate, rename .env to .env.migrated")

    sub.add_parser("status", help="Show keyring backend + presence of each common key")

    args = ap.parse_args(argv)

    if args.cmd == "get":
        try:
            print(get_key(args.name))
            return 0
        except KeyError as e:
            print(str(e), file=sys.stderr)
            return 1

    if args.cmd == "set":
        value = sys.stdin.read().strip()
        if not value:
            print("error: empty value on stdin", file=sys.stderr)
            return 2
        set_key(args.name, value)
        print(f"stored {args.name} in keyring (service={SERVICE})")
        return 0

    if args.cmd == "delete":
        delete_key(args.name)
        print(f"deleted {args.name} from keyring (if present)")
        return 0

    if args.cmd == "migrate":
        names = migrate_env_to_keyring(keep_source=not args.delete_source)
        print(f"migrated {len(names)} keys: {', '.join(names) if names else '(none)'}")
        return 0

    if args.cmd == "status":
        try:
            import keyring  # type: ignore
            print(f"keyring backend: {keyring.get_keyring()}")
        except ImportError:
            print("keyring library NOT installed — run `pip3 install --user keyring`")
            return 1
        common = [
            "ANTHROPIC_API_KEY", "GROQ_API_KEY",
            "OPENAI_API_KEY", "GOOGLE_API_KEY",
        ]
        for n in common:
            try:
                val = get_key(n)
                print(f"  {n:<24s} ✓ ({len(val)} chars)")
            except KeyError:
                print(f"  {n:<24s} ✗ (missing)")
        return 0

    return 2


if __name__ == "__main__":
    sys.exit(_cli())

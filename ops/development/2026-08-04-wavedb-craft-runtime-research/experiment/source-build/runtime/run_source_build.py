#!/usr/bin/env python3
"""Execute one fresh, exact reviewed-source WaveDB native build attempt."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


CLAIM_CEILING = "one-local-linux-x86_64-reviewed-source-build-observation"
INSTALL_COMMAND = ["npm", "ci", "--ignore-scripts", "--no-audit", "--fund=false"]
STAGES = [
    "source",
    "dependencies",
    "generated-source",
    "build",
    "addon-load",
    "upstream-tests",
    "empty-value-canary",
    "scope-audit",
]


class BuildBlocked(Exception):
    def __init__(self, code: str, detail: str) -> None:
        super().__init__(detail)
        self.code = code
        self.detail = detail


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def exact_ref(root: Path, path: Path) -> dict[str, Any]:
    resolved = path.resolve()
    resolved.relative_to(root)
    content = resolved.read_bytes()
    return {
        "path": resolved.relative_to(root).as_posix(),
        "sha256": sha256_bytes(content),
        "size_bytes": len(content),
    }


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(value, indent=2, sort_keys=True) + "\n"
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(payload, encoding="utf-8")
    os.replace(temporary, path)


def safe_child(root: Path, relative: str, label: str) -> Path:
    if not relative or Path(relative).is_absolute() or ".." in Path(relative).parts:
        raise BuildBlocked("PATH_SCOPE_VIOLATION", f"unsafe {label}: {relative}")
    candidate = (root / relative).resolve(strict=False)
    try:
        candidate.relative_to(root)
    except ValueError as error:
        raise BuildBlocked("PATH_SCOPE_VIOLATION", f"{label} escapes source-build root") from error
    parent = candidate.parent
    while parent != root.parent and parent != root:
        if parent.is_symlink():
            raise BuildBlocked("PATH_SCOPE_VIOLATION", f"symlink in {label} parent chain")
        parent = parent.parent
    return candidate


def tree_manifest(root: Path) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    if not root.exists():
        return entries
    if root.is_file() and not root.is_symlink():
        content = root.read_bytes()
        return [{"path": root.name, "sha256": sha256_bytes(content), "size_bytes": len(content)}]
    for path in sorted(
        item
        for item in root.rglob("*")
        if item.is_file()
        and not item.is_symlink()
        and ".git" not in item.relative_to(root).parts
    ):
        content = path.read_bytes()
        entries.append(
            {
                "path": path.relative_to(root).as_posix(),
                "sha256": sha256_bytes(content),
                "size_bytes": len(content),
            }
        )
    return entries


def tree_digest(root: Path) -> str:
    payload = json.dumps(tree_manifest(root), sort_keys=True, separators=(",", ":")).encode()
    return sha256_bytes(payload)


class Runner:
    def __init__(self, args: argparse.Namespace) -> None:
        self.args = args
        self.root = args.source_build_root.resolve()
        if not self.root.is_dir():
            raise BuildBlocked("PATH_SCOPE_VIOLATION", "source-build root does not exist")
        self.attempt = safe_child(self.root, f".work/{args.attempt_id}", "attempt path")
        self.evidence = safe_child(self.root, args.evidence_dir, "evidence path")
        if self.attempt.exists() or self.evidence.exists():
            raise BuildBlocked("ATTEMPT_COLLISION", "attempt or evidence target already exists")
        self.source = self.attempt / "source"
        self.node_root = self.source / "bindings" / "nodejs"
        self.logs = self.evidence / "logs"
        self.command_records: list[dict[str, Any]] = []
        self.stage_status: list[dict[str, str]] = []

    def command(
        self,
        stage: str,
        argv: list[str],
        cwd: Path,
        *,
        environment: dict[str, str] | None = None,
        timeout: int = 3600,
    ) -> str:
        if stage not in STAGES:
            raise BuildBlocked("COMMAND_TABLE_VIOLATION", f"unknown stage: {stage}")
        cwd.resolve().relative_to(self.attempt.resolve())
        command_id = f"{len(self.command_records) + 1:02d}-{stage}"
        log_path = self.logs / f"{command_id}.log"
        started = time.time_ns()
        env = None
        if environment is not None:
            env = os.environ.copy()
            env.update(environment)
        try:
            result = subprocess.run(
                argv,
                cwd=cwd,
                env=env,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=timeout,
                check=False,
            )
            output = result.stdout[-2_000_000:]
            exit_code = result.returncode
        except subprocess.TimeoutExpired as error:
            output = (error.stdout or "")[-2_000_000:] + "\nCOMMAND_TIMEOUT\n"
            exit_code = 124
        ended = time.time_ns()
        log_path.parent.mkdir(parents=True, exist_ok=True)
        log_path.write_text(output, encoding="utf-8")
        self.command_records.append(
            {
                "id": command_id,
                "stage": stage,
                "argv": argv,
                "cwd": cwd.resolve().relative_to(self.attempt.resolve()).as_posix(),
                "started_ns": started,
                "ended_ns": ended,
                "exit_code": exit_code,
                "log": exact_ref(self.root, log_path),
            }
        )
        if exit_code != 0:
            raise BuildBlocked(f"{stage.upper().replace('-', '_')}_COMMAND_FAILED", f"command failed: {argv[0]}")
        return output.rstrip()

    def check_identity(self, label: str, observed: str, expected: str) -> None:
        if expected not in observed:
            raise BuildBlocked("TOOLCHAIN_IDENTITY_MISMATCH", f"{label}: expected {expected!r}, observed {observed!r}")

    def run(self) -> Path:
        self.attempt.mkdir(parents=True)
        self.evidence.mkdir(parents=True)
        forbidden_before = {path: tree_digest((self.args.workspace_root / path).resolve()) for path in self.args.forbidden_path}

        self.command("source", ["git", "clone", "--no-checkout", "--filter=blob:none", self.args.source_url, str(self.source)], self.attempt)
        self.command("source", ["git", "checkout", "--detach", self.args.source_commit], self.source)
        self.command("source", ["git", "submodule", "sync", "--recursive"], self.source)
        self.command("source", ["git", "submodule", "update", "--init", "--recursive"], self.source)
        commit = self.command("source", ["git", "rev-parse", "HEAD"], self.source)
        if commit != self.args.source_commit:
            raise BuildBlocked("SOURCE_COMMIT_MISMATCH", "checked-out commit differs")
        status = self.command("source", ["git", "status", "--porcelain=v1", "--untracked-files=no"], self.source)
        if status:
            raise BuildBlocked("SOURCE_TREE_DIRTY", "tracked source is dirty before build")
        submodule_text = self.command("source", ["git", "submodule", "status", "--recursive"], self.source)
        submodules = []
        for line in submodule_text.splitlines():
            marker = line[:1]
            fields = line[1:].strip().split()
            if marker not in (" ",) or len(fields) < 2:
                raise BuildBlocked("SUBMODULE_IDENTITY_MISMATCH", f"unclean submodule record: {line}")
            submodules.append({"commit": fields[0], "path": fields[1], "status": "clean"})

        expected_files = {
            "package-lock.json": self.args.expected_package_lock_sha256,
            "package.json": self.args.expected_package_json_sha256,
            "binding.gyp": self.args.expected_binding_gyp_sha256,
            "scripts/build.js": self.args.expected_build_js_sha256,
            "scripts/copy-sources.js": self.args.expected_copy_sources_js_sha256,
        }
        observed_files: dict[str, str] = {}
        for relative, expected in expected_files.items():
            path = self.node_root / relative
            if not path.is_file():
                raise BuildBlocked("SOURCE_BUILD_FILE_MISMATCH", f"missing {relative}")
            observed = sha256_bytes(path.read_bytes())
            if observed != expected:
                raise BuildBlocked("SOURCE_BUILD_FILE_MISMATCH", f"digest mismatch: {relative}")
            observed_files[relative] = observed
        source_manifest_path = self.evidence / "source-manifest.json"
        write_json(
            source_manifest_path,
            {
                "root_commit": commit,
                "recursive_submodules": submodules,
                "root_build_files": observed_files,
                "tracked_files": tree_manifest(self.source),
            },
        )
        self.stage_status.append({"id": "source", "status": "pass"})

        tool_commands = {
            "node": (["node", "--version"], self.args.expected_node),
            "npm": (["npm", "--version"], self.args.expected_npm),
            "python": (["python3", "--version"], self.args.expected_python),
            "gcc": (["gcc", "--version"], self.args.expected_gcc),
            "gxx": (["g++", "--version"], self.args.expected_gxx),
            "make": (["make", "--version"], self.args.expected_make),
            "ld": (["ld", "--version"], self.args.expected_ld),
        }
        toolchain: dict[str, str] = {"platform": platform.platform(), "machine": platform.machine()}
        for label, (argv, expected) in tool_commands.items():
            observed = self.command("dependencies", argv, self.node_root, timeout=60).splitlines()[0]
            self.check_identity(label, observed, expected)
            toolchain[label] = observed

        lock_before = sha256_bytes((self.node_root / "package-lock.json").read_bytes())
        self.command("dependencies", INSTALL_COMMAND, self.node_root, timeout=1800)
        lock_after = sha256_bytes((self.node_root / "package-lock.json").read_bytes())
        if lock_after != lock_before:
            raise BuildBlocked("LOCKFILE_DRIFT", "package-lock changed during npm ci")
        npm_tree_raw = self.command("dependencies", ["npm", "ls", "--all", "--json"], self.node_root, timeout=300)
        dependency_manifest_path = self.evidence / "dependency-manifest.json"
        write_json(
            dependency_manifest_path,
            {
                "lockfile_sha256": lock_after,
                "install_command": INSTALL_COMMAND,
                "lifecycle_scripts_disabled": True,
                "npm_tree": json.loads(npm_tree_raw),
                "node_modules_manifest": tree_manifest(self.node_root / "node_modules"),
                "toolchain": toolchain,
            },
        )
        self.stage_status.append({"id": "dependencies", "status": "pass"})

        self.command("generated-source", ["node", "scripts/copy-sources.js"], self.node_root, timeout=300)
        generated_manifest_path = self.evidence / "generated-source-manifest.json"
        generated_entries = tree_manifest(self.node_root / "c_src")
        if not generated_entries:
            raise BuildBlocked("GENERATED_SOURCE_EMPTY", "c_src manifest is empty")
        write_json(generated_manifest_path, {"files": generated_entries})
        self.stage_status.append({"id": "generated-source", "status": "pass"})

        build_env = {"WAVEDB_OPENSSL": "1", "OPENSSL_ROOT": self.args.openssl_root}
        self.command("build", ["node", "scripts/build.js"], self.node_root, environment=build_env, timeout=3600)
        addons = sorted(self.node_root.glob("build/Release/*.node"))
        if len(addons) != 1 or addons[0].name != "wavedb.node":
            raise BuildBlocked("ADDON_CARDINALITY_MISMATCH", f"expected one wavedb.node, found {len(addons)}")
        addon = addons[0]
        build_manifest_path = self.evidence / "build-manifest.json"
        write_json(
            build_manifest_path,
            {
                "openssl": {"enabled": True, "root": self.args.openssl_root},
                "addon": exact_ref(self.root, addon),
                "build_tree": tree_manifest(self.node_root / "build"),
            },
        )
        self.stage_status.append({"id": "build", "status": "pass"})

        self.command("addon-load", ["node", "-e", "require('./lib/wavedb.js')"], self.node_root, timeout=60)
        self.stage_status.append({"id": "addon-load", "status": "pass"})
        test_files = [path.relative_to(self.node_root).as_posix() for path in sorted((self.node_root / "test").glob("*.test.js"))]
        if not test_files:
            raise BuildBlocked("UPSTREAM_TEST_SET_EMPTY", "no upstream tests resolved")
        self.command(
            "upstream-tests",
            ["node", "node_modules/mocha/bin/mocha.js", *test_files],
            self.node_root,
            timeout=3600,
        )
        self.stage_status.append({"id": "upstream-tests", "status": "pass"})

        canary = """
const fs = require('fs');
const os = require('os');
const path = require('path');
const {WaveDB} = require('./lib/wavedb.js');
const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'wavedb-empty-canary-'));
let db;
try {
  db = new WaveDB(dir, {enablePersist: false, syncOnly: true});
  db.putSync('canary/empty', '');
  if (db.getSync('canary/empty') !== '') throw new Error('empty value did not round trip');
} finally {
  if (db) db.close();
  fs.rmSync(dir, {recursive: true, force: true});
}
""".strip()
        self.command("empty-value-canary", ["node", "-e", canary], self.node_root, timeout=60)
        self.stage_status.append({"id": "empty-value-canary", "status": "pass"})

        forbidden_after = {path: tree_digest((self.args.workspace_root / path).resolve()) for path in self.args.forbidden_path}
        if forbidden_before != forbidden_after:
            raise BuildBlocked("FORBIDDEN_EFFECT", "a forbidden workspace path changed")
        self.stage_status.append({"id": "scope-audit", "status": "pass"})

        test_manifest_path = self.evidence / "test-manifest.json"
        write_json(
            test_manifest_path,
            {
                "addon_load": "pass",
                "upstream": "pass",
                "upstream_files": test_files,
                "empty_value_canary": "pass",
                "temporary_store_policy": "system-temp-created-and-removed",
            },
        )
        receipt = {
            "schema_version": "wavedb-reviewed-source-build.v1",
            "attempt_id": self.args.attempt_id,
            "verdict": "pass",
            "failure_code": None,
            "claim_ceiling": CLAIM_CEILING,
            "claims": [CLAIM_CEILING],
            "source": {
                "url": self.args.source_url,
                "root_commit": commit,
                "clean_tracked_baseline": True,
                "recursive_submodules": {"recursive_checked": True, "entries": submodules},
                "root_build_files": observed_files,
            },
            "dependency": {
                "lockfile_sha256": lock_after,
                "lockfile_unchanged": True,
                "install_command": INSTALL_COMMAND,
                "lifecycle_scripts_disabled": True,
            },
            "toolchain": toolchain,
            "openssl": {"enabled": True, "root": self.args.openssl_root},
            "stages": self.stage_status,
            "tests": {"addon_load": "pass", "upstream": "pass", "empty_value_canary": "pass"},
            "effects": {
                "craft_access": False,
                "git_mutation": False,
                "publication": False,
                "deployment": False,
                "unclassified": [],
            },
            "evidence": {
                "source_manifest": exact_ref(self.root, source_manifest_path),
                "dependency_manifest": exact_ref(self.root, dependency_manifest_path),
                "generated_source_manifest": exact_ref(self.root, generated_manifest_path),
                "build_manifest": exact_ref(self.root, build_manifest_path),
                "test_manifest": exact_ref(self.root, test_manifest_path),
                "addon": exact_ref(self.root, addon),
                "logs": [record["log"] for record in self.command_records],
            },
        }
        candidate = self.evidence / ".candidate-source-build-receipt.json"
        terminal = self.evidence / "source-build-receipt.json"
        write_json(candidate, receipt)
        validation = subprocess.run(
            [
                sys.executable,
                str(self.args.validator),
                str(candidate),
                "--source-build-root",
                str(self.root),
                "--expected-source-commit",
                self.args.source_commit,
                "--expected-lockfile-sha256",
                self.args.expected_package_lock_sha256,
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            check=False,
        )
        if validation.returncode != 0:
            raise BuildBlocked("TERMINAL_VALIDATION_FAILED", validation.stdout.strip())
        os.replace(candidate, terminal)
        return terminal

    def write_block(self, error: BuildBlocked) -> Path | None:
        try:
            self.evidence.mkdir(parents=True, exist_ok=True)
            path = self.evidence / "source-build-block-receipt.json"
            write_json(
                path,
                {
                    "schema_version": "wavedb-reviewed-source-build-block.v1",
                    "attempt_id": self.args.attempt_id,
                    "verdict": "block",
                    "failure_code": error.code,
                    "detail": error.detail,
                    "commands": self.command_records,
                    "addon_handoff": None,
                    "claim_ceiling": CLAIM_CEILING,
                },
            )
            return path
        except OSError:
            return None


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--execute", action="store_true", help="required acknowledgement for live execution")
    result.add_argument("--workspace-root", required=True, type=Path)
    result.add_argument("--source-build-root", required=True, type=Path)
    result.add_argument("--attempt-id", required=True)
    result.add_argument("--evidence-dir", required=True)
    result.add_argument("--source-url", required=True)
    result.add_argument("--source-commit", required=True)
    result.add_argument("--expected-package-lock-sha256", required=True)
    result.add_argument("--expected-package-json-sha256", required=True)
    result.add_argument("--expected-binding-gyp-sha256", required=True)
    result.add_argument("--expected-build-js-sha256", required=True)
    result.add_argument("--expected-copy-sources-js-sha256", required=True)
    result.add_argument("--expected-node", required=True)
    result.add_argument("--expected-npm", required=True)
    result.add_argument("--expected-python", required=True)
    result.add_argument("--expected-gcc", required=True)
    result.add_argument("--expected-gxx", required=True)
    result.add_argument("--expected-make", required=True)
    result.add_argument("--expected-ld", required=True)
    result.add_argument("--openssl-root", required=True)
    result.add_argument("--validator", required=True, type=Path)
    result.add_argument("--forbidden-path", action="append", default=[])
    return result


def main() -> int:
    args = parser().parse_args()
    if not args.execute:
        print("BLOCK: --execute is required", file=sys.stderr)
        return 2
    args.workspace_root = args.workspace_root.resolve()
    try:
        runner = Runner(args)
        terminal = runner.run()
    except BuildBlocked as error:
        receipt = locals().get("runner") and runner.write_block(error)
        print(json.dumps({"verdict": "block", "code": error.code, "detail": error.detail, "receipt": str(receipt) if receipt else None}, sort_keys=True))
        return 1
    print(json.dumps({"verdict": "pass", "receipt": str(terminal)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

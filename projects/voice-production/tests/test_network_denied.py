from __future__ import annotations

import ast
import contextlib
import inspect
import io
import json
import socket
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


STAGING_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(STAGING_ROOT))

import voice_workflow  # noqa: E402
from voice_production.compiler_config import (  # noqa: E402
    compiler_config_from_json_bytes,
)


CSV_PATH = Path(
    "projects/lucifers-lights/drafts/graphic-novel/chapter-01/audio/"
    "elevenlabs-voiceover-studio.csv"
)
CONFIG_PATH = Path("projects/lucifers-lights/factory/voice/chapter-01.json")
HANDOFF_PATH = Path(
    "projects/lucifers-lights/development/chapter-factory-runs/"
    "chapter-01-pilot/voice-handoff.json"
)


def source_path() -> Path:
    return REPOSITORY_ROOT / CSV_PATH


def compiler_config():
    return compiler_config_from_json_bytes(
        (REPOSITORY_ROOT / CONFIG_PATH).read_bytes()
    )


def denied_network():
    denied = AssertionError("network or DNS access crossed the L0 boundary")
    return (
        mock.patch.object(socket, "socket", side_effect=denied),
        mock.patch.object(socket, "create_connection", side_effect=denied),
        mock.patch.object(socket, "getaddrinfo", side_effect=denied),
        mock.patch.object(socket, "gethostbyname", side_effect=denied),
        mock.patch.object(socket, "gethostbyname_ex", side_effect=denied),
        mock.patch.object(socket, "gethostbyaddr", side_effect=denied),
    )


class NetworkDeniedTests(unittest.TestCase):
    def test_workflow_passes_while_socket_and_dns_helpers_raise(self) -> None:
        patches = denied_network()
        with patches[0], patches[1], patches[2], patches[3], patches[4], patches[5]:
            result = voice_workflow.run_workflow(
                source_path().read_bytes(), compiler_config=compiler_config()
            )
        self.assertEqual(
            result.value["effects"],
            {
                "audio_artifacts_materialized": 0,
                "credential_resolver_calls": 0,
                "dns_calls": 0,
                "external_messages": 0,
                "network_calls": 0,
                "provider_calls": 0,
            },
        )

    def test_cli_reads_only_the_local_source_and_prints_redacted_json(self) -> None:
        output = io.StringIO()
        patches = denied_network()
        with (
            patches[0],
            patches[1],
            patches[2],
            patches[3],
            patches[4],
            patches[5],
            contextlib.redirect_stdout(output),
        ):
            status = voice_workflow.main(
                [
                    str(source_path()),
                    str(REPOSITORY_ROOT / CONFIG_PATH),
                    str(REPOSITORY_ROOT / HANDOFF_PATH),
                    "--repo-root",
                    str(REPOSITORY_ROOT),
                ]
            )
        self.assertEqual(status, 0)
        parsed = json.loads(output.getvalue())
        self.assertEqual(parsed["schema_version"], voice_workflow.SUMMARY_SCHEMA)
        self.assertEqual(parsed["effects"]["network_calls"], 0)

    def test_cli_rejects_handoff_drift_before_workflow(self) -> None:
        handoff = json.loads((REPOSITORY_ROOT / HANDOFF_PATH).read_text())
        handoff["admission"]["state"] = "withheld"
        with tempfile.TemporaryDirectory(
            prefix=".handoff-drift-", dir=STAGING_ROOT
        ) as directory:
            handoff_path = Path(directory) / "voice-handoff.json"
            handoff_path.write_text(json.dumps(handoff), encoding="utf-8")
            with mock.patch.object(
                voice_workflow,
                "run_workflow",
                side_effect=AssertionError("workflow must remain unopened"),
            ):
                with self.assertRaisesRegex(
                    voice_workflow.FactoryHandoffError,
                    "does not grant local compile admission",
                ):
                    voice_workflow.main(
                        [
                            str(source_path()),
                            str(REPOSITORY_ROOT / CONFIG_PATH),
                            str(handoff_path),
                            "--repo-root",
                            str(REPOSITORY_ROOT),
                        ]
                    )

    def test_import_surface_has_no_effectful_runtime_modules(self) -> None:
        tree = ast.parse(inspect.getsource(voice_workflow))
        imports: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(alias.name.split(".", 1)[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                imports.add(node.module.split(".", 1)[0])
        self.assertFalse(
            imports & {"http", "requests", "socket", "subprocess", "urllib"}
        )
        source = inspect.getsource(voice_workflow).casefold()
        self.assertNotIn("environ[", source)
        self.assertNotIn("getenv(", source)


if __name__ == "__main__":
    unittest.main()

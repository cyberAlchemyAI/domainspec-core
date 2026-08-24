from __future__ import annotations

import ast
import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
REPO_ROOT = PROJECT_ROOT.parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from chapter_pipeline import validate_chapter_run  # noqa: E402
from chapter_pipeline.factory import (  # noqa: E402
    FactoryError,
    load_config,
    run_pilot,
)


FIXTURE_ROOT = Path(__file__).with_name("fixtures")
CHAPTER_01_CONFIG = PROJECT_ROOT / "factory" / "chapter-01.json"
CHAPTER_02_CONFIG = FIXTURE_ROOT / "chapter-02-factory.json"
MANUSCRIPT = PROJECT_ROOT / "drafts" / "chapter-01.md"


class ChapterFactoryTests(unittest.TestCase):
    def run_in_temp(self, config: Path, name: str = "run") -> tuple[Path, dict[str, object]]:
        temporary = tempfile.TemporaryDirectory(prefix=".factory-test-", dir=PROJECT_ROOT)
        self.addCleanup(temporary.cleanup)
        output = Path(temporary.name) / name
        result = run_pilot(config, output, REPO_ROOT)
        return output, result

    def test_chapter_01_pilot_is_author_accepted_and_preserves_manuscript(self) -> None:
        before = MANUSCRIPT.read_bytes()
        output, result = self.run_in_temp(CHAPTER_01_CONFIG)

        self.assertEqual(result["result"], "accepted")
        self.assertEqual(result["deterministic_validation"], "pass")
        self.assertEqual(result["human_gate"], "approved")
        self.assertEqual(MANUSCRIPT.read_bytes(), before)

        expected = {
            "chapter-brief.md",
            "chapter-review.html",
            "chapter-run.json",
            "context-manifest.json",
            "decision-request.md",
            "deterministic-review.json",
            "editorial-review.md",
            "factory-receipt.json",
            "factory-status.json",
            "voice-handoff.json",
        }
        self.assertEqual({path.name for path in output.iterdir()}, expected)

        run_document = json.loads((output / "chapter-run.json").read_text())
        self.assertTrue(validate_chapter_run(run_document).is_valid)
        self.assertEqual(run_document["revision"]["number"], 1)
        self.assertEqual(
            run_document["revision"]["prior_digest"],
            "ee57d5c8ef0ccd927d0ed267d6cc75ca38da8a71f93683bf68b9864352d2a64e",
        )
        self.assertEqual(run_document["run_phase"], "baseline_ready")
        self.assertEqual(run_document["manuscript"]["decision_state"], "accepted")
        self.assertEqual(
            run_document["manuscript"]["decision_receipt_ref"],
            "projects/lucifers-lights/development/chapter-factory-runs/"
            "chapter-01-pilot/decision-gate/author-decision.json",
        )
        self.assertEqual(
            run_document["derivatives"]["motion-comic-voiceover"]["state"],
            "eligible",
        )
        self.assertEqual(
            run_document["derivatives"]["motion-comic-voiceover"]["binding"][
                "source_digest"
            ],
            "99ed4a664bba57b0f090a043382fc1de3d5dac5ed5147cbb8fde92c4497dbfa3",
        )
        self.assertEqual(run_document["effects"], {})

        context = json.loads((output / "context-manifest.json").read_text())
        self.assertEqual(context["source_count"], 13)
        handoff = json.loads((output / "voice-handoff.json").read_text())
        self.assertEqual(
            handoff["schema_version"],
            "lucifers-lights.voice-compiler-handoff/1.0.0",
        )
        self.assertEqual(handoff["chapter_run_digest"], result["chapter_run_digest"])
        self.assertEqual(handoff["manuscript_gate"]["decision_state"], "accepted")
        self.assertEqual(handoff["admission"]["state"], "eligible")
        self.assertEqual(handoff["admission"]["scope"], "local-compile-only")
        self.assertEqual(
            handoff["admission"]["reason"],
            "accepted_manuscript_and_synchronized_script",
        )
        self.assertEqual(
            handoff["derivative"]["status"], "local-compile-ready"
        )
        self.assertEqual(
            handoff["voice_source"]["sha256"],
            "99ed4a664bba57b0f090a043382fc1de3d5dac5ed5147cbb8fde92c4497dbfa3",
        )
        self.assertEqual(
            handoff["sync_disposition"]["sha256"],
            "483f1d8b728484a0e2493e63ad30e3b0cca83aa35410077626112d3bf5cba1e8",
        )
        self.assertTrue(
            all(value is False for value in handoff["external_effects"].values())
        )

        status = json.loads((output / "factory-status.json").read_text())
        stages = {item["id"]: item["status"] for item in status["stages"]}
        self.assertEqual(len(status["stages"]), 10)
        self.assertEqual(status["current_stage"], "local voice compile")
        self.assertEqual(stages["author_decision"], "pass")
        self.assertEqual(stages["voice_handoff"], "eligible")
        self.assertEqual(stages["export"], "eligible")
        self.assertEqual(stages["next_chapter"], "eligible")

        review_html = (output / "chapter-review.html").read_text()
        self.assertEqual(review_html.count("Chapter Factory Pilot"), 2)
        self.assertIn("factory-card--sidebar", review_html)
        self.assertIn("factory-card--mobile", review_html)
        self.assertIn("window.WhisperReview", review_html)
        self.assertIn("author-accepted", review_html)
        self.assertIn("provider synthesis remains unauthorized", review_html)
        self.assertNotIn("Chapter 1 is review-pending", review_html)
        self.assertIn('<link rel="icon" href="data:,">', review_html)

    def test_outputs_are_byte_stable_across_fresh_directories(self) -> None:
        temporary = tempfile.TemporaryDirectory(prefix=".factory-stable-", dir=PROJECT_ROOT)
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        first = root / "first"
        second = root / "second"

        run_pilot(CHAPTER_01_CONFIG, first, REPO_ROOT)
        run_pilot(CHAPTER_01_CONFIG, second, REPO_ROOT)

        self.assertEqual(
            {path.name: path.read_bytes() for path in first.iterdir()},
            {path.name: path.read_bytes() for path in second.iterdir()},
        )

    def test_synthetic_second_chapter_uses_the_same_factory(self) -> None:
        output, result = self.run_in_temp(CHAPTER_02_CONFIG)
        run_document = json.loads((output / "chapter-run.json").read_text())
        context = json.loads((output / "context-manifest.json").read_text())

        self.assertEqual(result["deterministic_validation"], "pass")
        self.assertEqual(result["result"], "review_pending")
        self.assertEqual(result["human_gate"], "pending")
        self.assertEqual(run_document["identity"]["chapter_id"], "LL-CH2-SYNTHETIC")
        self.assertEqual(run_document["manuscript"]["decision_state"], "review_pending")
        self.assertIsNone(run_document["manuscript"]["decision_receipt_ref"])
        self.assertEqual(context["source_count"], 1)
        self.assertFalse(context["contains_manuscript_prose"])
        self.assertFalse((output / "voice-handoff.json").exists())
        self.assertNotIn("Presentation Is Everything", (output / "chapter-brief.md").read_text())

    def test_author_decision_identity_and_evidence_drift_block_before_outputs(self) -> None:
        base_receipt_path = (
            PROJECT_ROOT
            / "development/chapter-factory-runs/chapter-01-pilot/decision-gate/author-decision.json"
        )
        base_receipt = json.loads(base_receipt_path.read_text())
        cases = (
            (
                "identity",
                lambda receipt: receipt.__setitem__("chapter_id", "LL-CH9"),
                "chapter_id does not match factory config",
            ),
            (
                "manuscript",
                lambda receipt: receipt["manuscript"].__setitem__("sha256", "0" * 64),
                "manuscript digest does not match binding",
            ),
            (
                "evidence",
                lambda receipt: receipt["decision_record"].__setitem__("sha256", "0" * 64),
                "decision_record digest drift",
            ),
        )
        for name, mutate, message in cases:
            with self.subTest(name=name):
                temporary = tempfile.TemporaryDirectory(
                    prefix=f".factory-decision-{name}-", dir=PROJECT_ROOT
                )
                self.addCleanup(temporary.cleanup)
                root = Path(temporary.name)
                receipt = copy.deepcopy(base_receipt)
                mutate(receipt)
                receipt_path = root / "author-decision.json"
                receipt_path.write_text(json.dumps(receipt), encoding="utf-8")
                config = json.loads(CHAPTER_01_CONFIG.read_text())
                decision_source = next(
                    item
                    for item in config["sources"]
                    if item["id"] == "chapter-01-author-decision"
                )
                decision_source["path"] = receipt_path.relative_to(REPO_ROOT).as_posix()
                config_path = root / "factory.json"
                config_path.write_text(json.dumps(config), encoding="utf-8")
                output = root / "output"

                with self.assertRaisesRegex(FactoryError, message):
                    run_pilot(config_path, output, REPO_ROOT)
                self.assertFalse(output.exists())

    def test_manuscript_digest_drift_blocks_before_outputs(self) -> None:
        temporary = tempfile.TemporaryDirectory(prefix=".factory-drift-", dir=PROJECT_ROOT)
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        config = json.loads(CHAPTER_01_CONFIG.read_text())
        config["chapter"]["expected_sha256"] = "0" * 64
        config_path = root / "drift.json"
        config_path.write_text(json.dumps(config), encoding="utf-8")
        output = root / "output"

        with self.assertRaisesRegex(FactoryError, "manuscript digest drift"):
            run_pilot(config_path, output, REPO_ROOT)
        self.assertFalse(output.exists())

    def test_failed_mechanical_check_withholds_editorial_and_export(self) -> None:
        temporary = tempfile.TemporaryDirectory(prefix=".factory-block-", dir=PROJECT_ROOT)
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        config = json.loads(CHAPTER_02_CONFIG.read_text())
        config["review"]["required_markers"].append("marker that is not present")
        config_path = root / "blocked.json"
        config_path.write_text(json.dumps(config), encoding="utf-8")
        output = root / "output"

        result = run_pilot(config_path, output, REPO_ROOT)
        status = json.loads((output / "factory-status.json").read_text())

        self.assertEqual(result["result"], "blocked")
        self.assertEqual(result["deterministic_validation"], "fail")
        stages = {item["id"]: item["status"] for item in status["stages"]}
        self.assertEqual(stages["editorial_review"], "withheld")
        self.assertEqual(stages["export"], "withheld")

    def test_unknown_config_fields_and_repository_escape_fail_closed(self) -> None:
        temporary = tempfile.TemporaryDirectory(prefix=".factory-config-", dir=PROJECT_ROOT)
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)

        unknown = json.loads(CHAPTER_01_CONFIG.read_text())
        unknown["surprise"] = True
        unknown_path = root / "unknown.json"
        unknown_path.write_text(json.dumps(unknown), encoding="utf-8")
        with self.assertRaisesRegex(FactoryError, "unknown fields"):
            load_config(unknown_path)

        escaped = json.loads(CHAPTER_01_CONFIG.read_text())
        escaped["sources"][0]["path"] = "../outside.md"
        escaped_path = root / "escaped.json"
        escaped_path.write_text(json.dumps(escaped), encoding="utf-8")
        with self.assertRaisesRegex(FactoryError, "escapes the repository root"):
            run_pilot(escaped_path, root / "escaped-output", REPO_ROOT)

    def test_voice_binding_mismatch_blocks_before_outputs(self) -> None:
        temporary = tempfile.TemporaryDirectory(prefix=".factory-voice-", dir=PROJECT_ROOT)
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        config = json.loads(CHAPTER_01_CONFIG.read_text())
        config["voice"]["source_id"] = "chapter-01-manuscript"
        config_path = root / "voice-mismatch.json"
        config_path.write_text(json.dumps(config), encoding="utf-8")
        output = root / "output"

        with self.assertRaisesRegex(
            FactoryError, "voice source role must be audio-script-derivative"
        ):
            run_pilot(config_path, output, REPO_ROOT)
        self.assertFalse(output.exists())

    def test_factory_runtime_has_no_network_provider_or_secret_imports(self) -> None:
        module_path = PROJECT_ROOT / "chapter_pipeline" / "factory.py"
        tree = ast.parse(module_path.read_text(encoding="utf-8"))
        imports: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.add(node.module.split(".")[0])

        self.assertTrue(
            {"requests", "urllib", "http", "socket", "subprocess"}.isdisjoint(imports)
        )


if __name__ == "__main__":
    unittest.main()

"""Tests for pipeline.loop.track_registry — §5 v8 amendment (R.PF1).

Three test classes, mirroring the dispatch_plan.md WS-G done-definition
("track-registry dispatch testable for three tracks (submission, eval,
report stub)"):

- :class:`TestTrackRegistryLoader` — schema validation (well-formed +
  malformed YAML)
- :class:`TestThreeTrackDispatch` — three rows (submission, eval, report
  stub) routing through dispatch_track
- :class:`TestRouterYamlOnDisk` — the actual workspace router.yaml
  parses cleanly and contains the three expected rows
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
import yaml

from pipeline.loop.track_registry import (
    TILTH_VERSION_FAMILY,
    RegistrySchemaError,
    Track,
    TrackNotFound,
    TrackNotShippable,
    TrackRegistry,
    TrackShapeUnimplemented,
    dispatch_track,
    get_track,
    load_track_registry,
    load_track_registry_from_yaml_text,
)
from pipeline.loop import track_registry as _track_registry_module


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _well_formed_three_track_source() -> dict[str, Any]:
    """A minimal well-formed source mapping with all three v0.1 + v0.2 rows."""
    return {
        "tracks": {
            "submission": {
                "kind": "track",
                "pipeline_shape": "rfa_to_council_to_signed_bundle",
                "prompt_template_root": "pipeline/prompts/submission/",
                "failure_code_prefix": "F-PIPE-SUBMIT-",
                "cross_family_rigor": "required",
                "shippable_in": "v0.1",
                "scribe_prompt_template": "pipeline/prompts/submission/scribe.md",
                "judge_rubric_ref": "pipeline/rubrics/vapg_fy26.json",
                "red_team_probe_template": (
                    "pipeline/prompts/submission/red_team_probe.md"
                ),
                "output_vault_subtree": (
                    "orgs/{org_slug}/vault/submissions/{run_id}/"
                ),
                "output_schema": "SubmissionBundle",
            },
            "eval": {
                "kind": "track",
                "pipeline_shape": "operator_harness_to_per_seat_calibration",
                "prompt_template_root": "pipeline/prompts/eval/",
                "failure_code_prefix": "F-PIPE-EVAL-",
                "cross_family_rigor": "not_required",
                "shippable_in": "v0.1",
                "scribe_prompt_template": "pipeline/prompts/eval/scribe.md",
                "judge_rubric_ref": "pipeline/rubrics/vapg_fy26.json",
                "red_team_probe_template": (
                    "pipeline/prompts/eval/red_team_probe.md"
                ),
                "output_vault_subtree": (
                    "orgs/{org_slug}/golden_set/calibration_reports/"
                ),
                "output_schema": "CalibrationReport",
            },
            "report": {
                "kind": "track",
                "pipeline_shape": (
                    "prior_commitments_to_council_to_signed_report"
                ),
                "prompt_template_root": "pipeline/prompts/report/",
                "failure_code_prefix": "F-PIPE-REPORT-",
                "cross_family_rigor": "required",
                "shippable_in": "v0.2",
                "scribe_prompt_template": "pipeline/prompts/report/scribe.md",
                "judge_rubric_ref": (
                    "pipeline/rubrics/proposal_commitments.json"
                ),
                "red_team_probe_template": (
                    "pipeline/prompts/report/red_team_probe.md"
                ),
                "output_vault_subtree": (
                    "orgs/{org_slug}/vault/reports/{run_id}/"
                ),
                "output_schema": "GrantReport",
            },
        }
    }


# ---------------------------------------------------------------------------
# TestTrackRegistryLoader — schema validation
# ---------------------------------------------------------------------------


class TestTrackRegistryLoader:
    """Loader correctness: well-formed YAML loads; malformed rejects."""

    def test_well_formed_loads_three_tracks(self) -> None:
        registry = load_track_registry(_well_formed_three_track_source())
        assert isinstance(registry, TrackRegistry)
        assert registry.names() == ("submission", "eval", "report")

    def test_loaded_tracks_are_frozen_dataclasses(self) -> None:
        registry = load_track_registry(_well_formed_three_track_source())
        track = registry.as_mapping()["submission"]
        with pytest.raises((AttributeError, dataclass_frozen_exc())):
            track.pipeline_shape = "tampered"  # type: ignore[misc]

    def test_loaded_track_carries_all_eleven_fields(self) -> None:
        registry = load_track_registry(_well_formed_three_track_source())
        track = registry.as_mapping()["submission"]
        assert track.name == "submission"
        assert track.kind == "track"
        assert track.pipeline_shape == "rfa_to_council_to_signed_bundle"
        assert track.prompt_template_root == "pipeline/prompts/submission/"
        assert track.failure_code_prefix == "F-PIPE-SUBMIT-"
        assert track.cross_family_rigor == "required"
        assert track.shippable_in == "v0.1"
        assert (
            track.scribe_prompt_template
            == "pipeline/prompts/submission/scribe.md"
        )
        assert track.judge_rubric_ref == "pipeline/rubrics/vapg_fy26.json"
        assert (
            track.red_team_probe_template
            == "pipeline/prompts/submission/red_team_probe.md"
        )
        assert (
            track.output_vault_subtree
            == "orgs/{org_slug}/vault/submissions/{run_id}/"
        )
        assert track.output_schema == "SubmissionBundle"

    def test_source_must_be_a_mapping(self) -> None:
        with pytest.raises(RegistrySchemaError, match="must be a mapping"):
            load_track_registry("not a mapping")  # type: ignore[arg-type]

    def test_source_must_have_tracks_key(self) -> None:
        with pytest.raises(RegistrySchemaError, match="no 'tracks:' key"):
            load_track_registry({"version": 1})

    def test_tracks_must_be_a_mapping(self) -> None:
        with pytest.raises(RegistrySchemaError, match="'tracks' must be"):
            load_track_registry({"tracks": ["submission", "eval"]})

    def test_empty_tracks_rejected(self) -> None:
        with pytest.raises(RegistrySchemaError, match="empty"):
            load_track_registry({"tracks": {}})

    def test_row_must_be_a_mapping(self) -> None:
        with pytest.raises(RegistrySchemaError, match="must be a mapping"):
            load_track_registry({"tracks": {"submission": "not a row"}})

    def test_row_missing_required_key(self) -> None:
        bad = _well_formed_three_track_source()
        del bad["tracks"]["submission"]["pipeline_shape"]
        with pytest.raises(RegistrySchemaError, match="missing required key"):
            load_track_registry(bad)

    def test_row_with_unknown_key_rejected(self) -> None:
        bad = _well_formed_three_track_source()
        bad["tracks"]["submission"]["mystery_field"] = "boom"
        with pytest.raises(RegistrySchemaError, match="unknown keys"):
            load_track_registry(bad)

    def test_row_kind_must_be_track(self) -> None:
        bad = _well_formed_three_track_source()
        bad["tracks"]["submission"]["kind"] = "lane"
        with pytest.raises(RegistrySchemaError, match="kind must be 'track'"):
            load_track_registry(bad)

    def test_row_cross_family_rigor_must_be_in_closed_set(self) -> None:
        bad = _well_formed_three_track_source()
        bad["tracks"]["submission"]["cross_family_rigor"] = "sometimes"
        with pytest.raises(
            RegistrySchemaError, match="cross_family_rigor must be"
        ):
            load_track_registry(bad)

    def test_row_string_field_must_be_non_empty(self) -> None:
        bad = _well_formed_three_track_source()
        bad["tracks"]["submission"]["scribe_prompt_template"] = ""
        with pytest.raises(RegistrySchemaError, match="non-empty"):
            load_track_registry(bad)

    def test_row_string_field_must_be_string(self) -> None:
        bad = _well_formed_three_track_source()
        bad["tracks"]["submission"]["scribe_prompt_template"] = 42
        with pytest.raises(RegistrySchemaError, match="must be a string"):
            load_track_registry(bad)

    def test_track_names_preserved_in_declaration_order(self) -> None:
        # Construct a non-alphabetic-order source; loader must preserve.
        source = {
            "tracks": {
                "report": _well_formed_three_track_source()["tracks"]["report"],
                "submission": _well_formed_three_track_source()["tracks"][
                    "submission"
                ],
                "eval": _well_formed_three_track_source()["tracks"]["eval"],
            }
        }
        registry = load_track_registry(source)
        assert registry.names() == ("report", "submission", "eval")


def dataclass_frozen_exc() -> type[Exception]:
    """Best-effort retrieval of dataclasses.FrozenInstanceError.

    Held as a function to avoid importing it at module load before the
    pytest collection picks up the test classes.
    """

    from dataclasses import FrozenInstanceError

    return FrozenInstanceError


# ---------------------------------------------------------------------------
# TestThreeTrackDispatch — three rows route through dispatch_track
# ---------------------------------------------------------------------------


class TestThreeTrackDispatch:
    """Dispatch routes submission/eval to runners; refuses report stub at v0.1."""

    def setup_method(self) -> None:
        self.registry = load_track_registry(
            _well_formed_three_track_source()
        )

    def test_submission_track_routes_to_submission_runner(self) -> None:
        captured: dict[str, Any] = {}

        def fake_submission_runner(**kwargs: Any) -> str:
            captured.update(kwargs)
            return "submission_ran"

        def fake_eval_runner(**kwargs: Any) -> str:
            raise AssertionError("eval runner should not have been called")

        result = dispatch_track(
            self.registry,
            "submission",
            submission_runner=fake_submission_runner,
            eval_runner=fake_eval_runner,
            submission_kwargs={"run_id": "RID-001", "org_slug": "test"},
        )
        assert result == "submission_ran"
        assert captured == {"run_id": "RID-001", "org_slug": "test"}

    def test_eval_track_routes_to_eval_runner(self) -> None:
        captured: dict[str, Any] = {}

        def fake_submission_runner(**kwargs: Any) -> str:
            raise AssertionError("submission runner should not have been called")

        def fake_eval_runner(**kwargs: Any) -> str:
            captured.update(kwargs)
            return "eval_ran"

        result = dispatch_track(
            self.registry,
            "eval",
            submission_runner=fake_submission_runner,
            eval_runner=fake_eval_runner,
            eval_kwargs={"run_id": "RID-002", "operator_org_slug": "test"},
        )
        assert result == "eval_ran"
        assert captured == {
            "run_id": "RID-002",
            "operator_org_slug": "test",
        }

    def test_report_track_refused_at_v0_1_via_shippable_gate(self) -> None:
        # report row has shippable_in: v0.2 — refuse at default v0.1.
        with pytest.raises(TrackNotShippable, match="v0.2"):
            dispatch_track(
                self.registry,
                "report",
                submission_runner=lambda **_: None,
                eval_runner=lambda **_: None,
            )

    def test_report_track_dispatchable_at_v0_2_but_shape_unimplemented(
        self,
    ) -> None:
        # At v0.2 the shippable_in gate passes, but the prior_commitments_*
        # shape has no v0.1 implementation — TrackShapeUnimplemented.
        with pytest.raises(
            TrackShapeUnimplemented,
            match="prior_commitments_to_council_to_signed_report",
        ):
            dispatch_track(
                self.registry,
                "report",
                current_version="v0.2",
                submission_runner=lambda **_: None,
                eval_runner=lambda **_: None,
            )

    def test_unknown_track_raises_track_not_found(self) -> None:
        with pytest.raises(TrackNotFound, match="not found in registry"):
            dispatch_track(
                self.registry,
                "tdsl_query",
                submission_runner=lambda **_: None,
                eval_runner=lambda **_: None,
            )

    def test_submission_dispatch_without_submission_runner_fails_closed(
        self,
    ) -> None:
        with pytest.raises(
            TrackShapeUnimplemented, match="no submission_runner was supplied"
        ):
            dispatch_track(self.registry, "submission")

    def test_eval_dispatch_without_eval_runner_fails_closed(self) -> None:
        with pytest.raises(
            TrackShapeUnimplemented, match="no eval_runner was supplied"
        ):
            dispatch_track(self.registry, "eval")

    def test_dispatch_kwargs_default_to_empty(self) -> None:
        # When a runner needs no kwargs, dispatch_track must not raise.
        called: dict[str, Any] = {}

        def fake(**kwargs: Any) -> str:
            called["kwargs"] = kwargs
            return "ok"

        result = dispatch_track(
            self.registry,
            "submission",
            submission_runner=fake,
            eval_runner=lambda **_: None,
        )
        assert result == "ok"
        assert called["kwargs"] == {}

    def test_get_track_shippable_gate_directly(self) -> None:
        # Direct get_track exercise — shippable_in: v0.1 passes at v0.1.
        sub = get_track(self.registry, "submission")
        assert sub.shippable_in == "v0.1"

        # report shippable_in: v0.2 must refuse at v0.1.
        with pytest.raises(TrackNotShippable):
            get_track(self.registry, "report")

    def test_get_track_unknown_name_raises(self) -> None:
        with pytest.raises(TrackNotFound, match="known tracks"):
            get_track(self.registry, "nonexistent")


# ---------------------------------------------------------------------------
# TestRouterYamlOnDisk — actual workspace router.yaml parses
# ---------------------------------------------------------------------------


class TestRouterYamlOnDisk:
    """The workspace's router.yaml must parse + carry the three expected rows.

    Per §6.7 the router.yaml is the v0.1 SOLE source of truth for track
    registry data; this test prevents schema drift between the on-disk
    file and the loader.
    """

    @staticmethod
    def _load_router_yaml() -> dict[str, Any]:
        # Walk up from this test file to the repo root (where router.yaml
        # lives). This is more robust than hard-coding a relative path
        # under different test invocation directories.
        here = Path(__file__).resolve()
        for parent in here.parents:
            candidate = parent / "router.yaml"
            if candidate.is_file():
                return yaml.safe_load(candidate.read_text())
        raise FileNotFoundError(
            "router.yaml not found walking up from tests/loop/"
        )

    def test_workspace_router_yaml_parses_into_registry(self) -> None:
        data = self._load_router_yaml()
        registry = load_track_registry(data)
        assert "submission" in registry.names()
        assert "eval" in registry.names()
        assert "report" in registry.names()

    def test_workspace_router_yaml_submission_is_v0_1_shippable(self) -> None:
        data = self._load_router_yaml()
        registry = load_track_registry(data)
        sub = get_track(registry, "submission")
        assert sub.shippable_in == TILTH_VERSION_FAMILY
        assert sub.pipeline_shape == "rfa_to_council_to_signed_bundle"
        assert sub.cross_family_rigor == "required"

    def test_workspace_router_yaml_eval_is_v0_1_shippable(self) -> None:
        data = self._load_router_yaml()
        registry = load_track_registry(data)
        ev = get_track(registry, "eval")
        assert ev.shippable_in == TILTH_VERSION_FAMILY
        assert (
            ev.pipeline_shape
            == "operator_harness_to_per_seat_calibration"
        )
        assert ev.cross_family_rigor == "not_required"

    def test_workspace_router_yaml_report_is_v0_2_forward_compat(self) -> None:
        data = self._load_router_yaml()
        registry = load_track_registry(data)
        # report row LOADS but get_track at v0.1 refuses it.
        mapping = registry.as_mapping()
        assert "report" in mapping
        assert mapping["report"].shippable_in == "v0.2"
        with pytest.raises(TrackNotShippable):
            get_track(registry, "report")

    def test_workspace_router_yaml_failure_code_prefixes_unique(self) -> None:
        data = self._load_router_yaml()
        registry = load_track_registry(data)
        prefixes = [t.failure_code_prefix for _, t in registry.tracks]
        assert len(prefixes) == len(set(prefixes)), (
            "Each track must use a unique F-PIPE-<TRACK>- failure-code "
            "prefix per §6.7 R.PF1 invariant"
        )

    def test_workspace_router_yaml_prompt_roots_unique(self) -> None:
        data = self._load_router_yaml()
        registry = load_track_registry(data)
        roots = [t.prompt_template_root for _, t in registry.tracks]
        assert len(roots) == len(set(roots)), (
            "Each track must use a distinct prompt_template_root so "
            "templates do not collide across tracks"
        )


# ---------------------------------------------------------------------------
# TestCycle1Closures — §5 v8 Audit #1 Cycle-1 closures (RT-02 / RT-03 /
# RT-04 / RT-07)
# ---------------------------------------------------------------------------


class TestCycle1Closures:
    """Regression tests for the four Audit #1 Cycle-1 closures."""

    # --- RT-03: output_vault_subtree must contain {org_slug} placeholder ---

    def test_output_vault_subtree_must_contain_org_slug_placeholder(
        self,
    ) -> None:
        """RT-03 closure: a row that omits {org_slug} fails-closed at load."""
        bad_source = _well_formed_three_track_source()
        bad_source["tracks"]["submission"]["output_vault_subtree"] = (
            "shared/vault/submissions/"  # no {org_slug}
        )
        with pytest.raises(RegistrySchemaError, match=r"\{org_slug\}"):
            load_track_registry(bad_source)

    def test_output_vault_subtree_with_org_slug_anywhere_passes(self) -> None:
        """The placeholder may appear anywhere in the path string."""
        ok_source = _well_formed_three_track_source()
        ok_source["tracks"]["submission"]["output_vault_subtree"] = (
            "vault/{org_slug}/by-cycle/{run_id}/"
        )
        # Must load without raising.
        load_track_registry(ok_source)

    # --- RT-04: YAML-text loader detects duplicate keys ---

    def test_yaml_text_with_duplicate_track_keys_is_rejected(self) -> None:
        """RT-04 closure: yaml.safe_load silently overwrites duplicate keys;
        load_track_registry_from_yaml_text rejects the input instead."""
        yaml_text = (
            "tracks:\n"
            "  submission:\n"
            "    kind: track\n"
            "    pipeline_shape: rfa_to_council_to_signed_bundle\n"
            "    prompt_template_root: pipeline/prompts/submission/\n"
            "    failure_code_prefix: F-PIPE-SUBMIT-\n"
            "    cross_family_rigor: required\n"
            "    shippable_in: v0.1\n"
            "    scribe_prompt_template: pipeline/prompts/submission/scribe.md\n"
            "    judge_rubric_ref: pipeline/rubrics/vapg_fy26.json\n"
            "    red_team_probe_template: pipeline/prompts/submission/red_team_probe.md\n"
            "    output_vault_subtree: orgs/{org_slug}/vault/submissions/{run_id}/\n"
            "    output_schema: SubmissionBundle\n"
            "  submission:\n"  # duplicate
            "    kind: track\n"
            "    pipeline_shape: rfa_to_council_to_signed_bundle\n"
            "    prompt_template_root: pipeline/prompts/submission/\n"
            "    failure_code_prefix: F-PIPE-SUBMIT-\n"
            "    cross_family_rigor: required\n"
            "    shippable_in: v0.1\n"
            "    scribe_prompt_template: pipeline/prompts/submission/scribe.md\n"
            "    judge_rubric_ref: pipeline/rubrics/vapg_fy26.json\n"
            "    red_team_probe_template: pipeline/prompts/submission/red_team_probe.md\n"
            "    output_vault_subtree: orgs/{org_slug}/vault/submissions/{run_id}/\n"
            "    output_schema: SubmissionBundle\n"
        )
        with pytest.raises(RegistrySchemaError, match=r"duplicate YAML mapping key"):
            load_track_registry_from_yaml_text(yaml_text)

    def test_yaml_text_well_formed_loads(self) -> None:
        """Sanity check: the duplicate-detecting loader still accepts well-formed YAML."""
        ok = (
            "tracks:\n"
            "  submission:\n"
            "    kind: track\n"
            "    pipeline_shape: rfa_to_council_to_signed_bundle\n"
            "    prompt_template_root: pipeline/prompts/submission/\n"
            "    failure_code_prefix: F-PIPE-SUBMIT-\n"
            "    cross_family_rigor: required\n"
            "    shippable_in: v0.1\n"
            "    scribe_prompt_template: pipeline/prompts/submission/scribe.md\n"
            "    judge_rubric_ref: pipeline/rubrics/vapg_fy26.json\n"
            "    red_team_probe_template: pipeline/prompts/submission/red_team_probe.md\n"
            "    output_vault_subtree: orgs/{org_slug}/vault/submissions/{run_id}/\n"
            "    output_schema: SubmissionBundle\n"
        )
        registry = load_track_registry_from_yaml_text(ok)
        assert registry.names() == ("submission",)

    # --- RT-02: closed-set monkey-patch caught by dispatcher fall-through ---

    def test_rebind_to_admit_new_shape_caught_by_dispatcher_fallthrough(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """RT-02 closure: monkey-patching _V0_1_IMPLEMENTED_SHAPES to admit
        a new shape does NOT silently dispatch — the dispatcher's if/elif
        chain only matches the two grandfathered shapes; any other shape
        falls through to the defensive TrackShapeUnimplemented raise."""
        # Build a registry whose sole row carries a forward-compat shape
        # marked shippable_in: v0.1 (so the shippable_in gate passes).
        source = {
            "tracks": {
                "smuggled": {
                    "kind": "track",
                    "pipeline_shape": "smuggled_shape_added_via_monkey_patch",
                    "prompt_template_root": "pipeline/prompts/smuggled/",
                    "failure_code_prefix": "F-PIPE-SMUGGLED-",
                    "cross_family_rigor": "required",
                    "shippable_in": "v0.1",
                    "scribe_prompt_template": "pipeline/prompts/smuggled/scribe.md",
                    "judge_rubric_ref": "pipeline/rubrics/vapg_fy26.json",
                    "red_team_probe_template": (
                        "pipeline/prompts/smuggled/red_team_probe.md"
                    ),
                    "output_vault_subtree": (
                        "orgs/{org_slug}/vault/smuggled/{run_id}/"
                    ),
                    "output_schema": "SmuggledBundle",
                },
            }
        }
        registry = load_track_registry(source)

        # Attempt the monkey-patch attack: rebind the closed set so the
        # gate at line ~495 in dispatch_track admits the smuggled shape.
        monkeypatch.setattr(
            _track_registry_module,
            "_V0_1_IMPLEMENTED_SHAPES",
            frozenset(
                {
                    "rfa_to_council_to_signed_bundle",
                    "operator_harness_to_per_seat_calibration",
                    "smuggled_shape_added_via_monkey_patch",
                }
            ),
        )

        # Even with the gate compromised, the dispatcher's if/elif chain
        # only knows the two grandfathered shapes; the smuggled shape
        # falls through to TrackShapeUnimplemented with the
        # "rebound at runtime" message.
        with pytest.raises(
            TrackShapeUnimplemented, match=r"rebound at runtime"
        ):
            dispatch_track(
                registry,
                "smuggled",
                submission_runner=lambda **_: "evil",
                eval_runner=lambda **_: "evil",
            )

    # --- RT-07: dispatcher routes by pipeline_shape, not by which runner is supplied ---

    def test_dispatch_uses_pipeline_shape_not_caller_runner_supply(self) -> None:
        """RT-07 closure: passing a submission_runner with an eval-shape
        track does NOT cause the submission_runner to fire — the
        dispatcher routes strictly by pipeline_shape."""
        registry = load_track_registry(_well_formed_three_track_source())

        called_submission = []
        called_eval = []

        def submission_runner(**kwargs: Any) -> str:
            called_submission.append(kwargs)
            return "submission_ran"

        def eval_runner(**kwargs: Any) -> str:
            called_eval.append(kwargs)
            return "eval_ran"

        # Dispatch the EVAL track. Despite both runners being supplied,
        # ONLY eval_runner must fire.
        result = dispatch_track(
            registry,
            "eval",
            submission_runner=submission_runner,
            eval_runner=eval_runner,
            eval_kwargs={"run_id": "RID-RT07"},
        )
        assert result == "eval_ran"
        assert called_eval == [{"run_id": "RID-RT07"}]
        assert called_submission == []  # never called — dispatcher routes by shape

"""Tests for ``tilth memory query`` unified retrieval CLI + registry.

Covers, per the architecture proficiency assessment 2026-05-11 Tier-0
items 2 + 3:

* Per-register adapter shape: each of the 13 registers loads its
  documents from a synthetic repo root.
* Cross-register BM25 query: ranking is deterministic and respects
  scope.
* Law-3 isolation: per-org adapters refuse when ``--org`` is omitted,
  reserved-slug rejection works, cross-org enumerate calls in the same
  query are structurally prevented (single ``org`` argument per call).
* CLI surface: query / list-registers / inspect subcommands return
  expected exit codes and JSON shapes.
* Ranking sanity: a query term that only appears in one register
  surfaces that register first.

Tests use a per-test isolated synthetic repo root populated with
minimal seed data — no dependency on the live workspace contents.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Iterator

import pytest

from pipeline.cli.tilth_memory_query import main as cli_main
from pipeline.memory.unified_query import (
    ALL_REGISTERS,
    PER_ORG_REGISTERS,
    WORKSPACE_REGISTERS,
    Document,
    Law3Violation,
    Provenance,
    Registry,
    UnknownRegisterError,
    _BM25Index,
    _dict_to_text,
    _excerpt,
    get_adapter,
    make_registry,
    tokenize,
)


# ---------------------------------------------------------------------------
# Synthetic repo fixture
# ---------------------------------------------------------------------------


@pytest.fixture()
def synth_repo(tmp_path: Path) -> Path:
    """Populate a tmp repo with the 13 registers' on-disk shapes."""

    # Workspace registers
    (tmp_path / "pipeline" / "institutional_memory").mkdir(parents=True)
    (tmp_path / "pipeline" / "institutional_memory" / "lessons.json").write_text(
        json.dumps(
            {
                "version": 1,
                "lessons": [
                    {
                        "id": "L-001",
                        "title": "Scout must hit live APIs",
                        "frequency": 1,
                        "severity": "HIGH",
                        "pattern": "cache stale APRICOT",
                        "pre_check": "verify",
                        "origin": "test",
                    },
                    {
                        "id": "L-002",
                        "title": "Path references not content dumps",
                        "frequency": 1,
                        "severity": "MEDIUM",
                        "pattern": "TPM ceiling",
                        "pre_check": "ref-by-path",
                        "origin": "test",
                    },
                ],
            }
        )
    )

    (tmp_path / "MEMORY.md").write_text(
        "# Workspace Index\n"
        "\n"
        "- [topic-zebra](file-A.md) — pointer to topic ZEBRA\n"
        "- [topic-koala](file-B.md) — pointer to topic KOALA\n"
    )

    (tmp_path / "daily_logs").mkdir()
    (tmp_path / "daily_logs" / "2026-05-15.md").write_text(
        "# 2026-05-15\n- Today the BANANA event happened.\n"
    )
    (tmp_path / "daily_logs" / "2026-05-14.md").write_text(
        "# 2026-05-14\n- Yesterday the CHERRY event happened.\n"
    )

    (tmp_path / "pipeline" / "engineering").mkdir(parents=True)
    (tmp_path / "pipeline" / "engineering" / "lock_history.v1.jsonl").write_text(
        json.dumps({"module": "pipeline.foo", "blueprint_section": "s1",
                    "review_verdict": "READY", "lock_class": "code"})
        + "\n"
        + json.dumps({"module": "pipeline.bar", "blueprint_section": "s2",
                      "review_verdict": "REQUIRES_FIXES TANGERINE",
                      "lock_class": "blueprint"})
        + "\n"
    )

    (tmp_path / "memory").mkdir()
    (tmp_path / "memory" / "project_DURIAN.md").write_text(
        "# DURIAN project memory\nIntake notes on DURIAN session.\n"
    )

    (tmp_path / "vault_shared" / "benchmarks").mkdir(parents=True)
    (tmp_path / "vault_shared" / "benchmarks" / "register.yaml").write_text(
        "schema_version: benchmarks.v1\n"
        "benchmarks:\n"
        "  - benchmark_id: bench-ELDERBERRY\n"
        "    value: 42\n"
        "    source_doc: external_ELDERBERRY_doc\n"
    )

    (tmp_path / "vault_shared" / "funder_intelligence").mkdir(parents=True)
    (tmp_path / "vault_shared" / "funder_intelligence" / "register.yaml").write_text(
        "schema_version: funder_intelligence.v1\n"
        "documents:\n"
        "  - doc_id: funder-FIG-001\n"
        "    funder_name: FIG Foundation\n"
        "    notes: focuses on regenerative agriculture\n"
    )

    (tmp_path / "pipeline" / "handoffs").mkdir(parents=True)
    (tmp_path / "pipeline" / "handoffs" / "handoff_GRAPE.md").write_text(
        "# Handoff\nThis handoff documents the GRAPE workstream.\n"
    )

    # cards register — pipeline/cards/**/*.yaml
    (tmp_path / "pipeline" / "cards" / "CIC").mkdir(parents=True)
    (tmp_path / "pipeline" / "cards" / "CIC" / "food_systems.yaml").write_text(
        "card_id: cic:food_systems\n"
        "title: Food Systems\n"
        "summary: card body mentioning QUINCE for retrieval testing\n"
    )
    (tmp_path / "pipeline" / "cards" / "registry.yaml").write_text(
        "schema_version: cards_registry.v1\n"
        "namespaces:\n"
        "  - namespace: cards:cic:food_systems\n"
        "    card_path: pipeline/cards/CIC/food_systems.yaml\n"
    )

    # docs register — docs/**/*.md
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "GETTING_STARTED.md").write_text(
        "# Getting started\n\nIntroductory doc mentioning RAMBUTAN.\n"
    )
    (tmp_path / "docs" / "nested").mkdir()
    (tmp_path / "docs" / "nested" / "deep.md").write_text(
        "# Deep\nNested doc mentioning STARFRUIT.\n"
    )
    (tmp_path / "docs" / ".hidden.md").write_text(
        "should be skipped — hidden\n"
    )

    # Per-org registers — populate for two orgs to exercise Law 3.
    for slug, secret_token in (("alpha_org", "HONEYDEW"), ("beta_org", "ICEBERG")):
        org_dir = tmp_path / "orgs" / slug
        (org_dir / "vault" / "kfr").mkdir(parents=True)
        (org_dir / "vault" / "kfr" / "register.yaml").write_text(
            "schema_version: kfr.v1\n"
            f"org_slug: {slug}\n"
            "facts:\n"
            "  - id: fact-1\n"
            f"    who: {slug}\n"
            f"    what: \"private fact containing {secret_token}\"\n"
        )
        (org_dir / "vault" / "classification").mkdir(parents=True)
        (org_dir / "vault" / "classification" / "register.yaml").write_text(
            "schema_version: classification_register.v1\n"
            "entries:\n"
            "  - field_id: class-1\n"
            f"    field_path: {slug}.private\n"
            f"    classification: confidential\n"
            f"    notes: keeps {secret_token} restricted\n"
        )
        (org_dir / "vault" / "operational" / "reflection_packets").mkdir(parents=True)
        (org_dir / "vault" / "operational" / "reflection_packets" / "cycle-001.json").write_text(
            json.dumps(
                {
                    "packet_id": "cycle-001",
                    "org_slug": slug,
                    "rationale": f"This packet references {secret_token}",
                }
            )
        )
        (org_dir / "match_database").mkdir(parents=True)
        (org_dir / "match_database" / "register.yaml").write_text(
            "schema_version: match_database.v1\n"
            f"org_slug: {slug}\n"
            "matches:\n"
            "  - match_id: m-1\n"
            f"    notes: matched on {secret_token}\n"
        )

    return tmp_path


# ---------------------------------------------------------------------------
# tokenizer + BM25 sanity
# ---------------------------------------------------------------------------


class TestTokenizer:
    def test_basic_lowercase(self) -> None:
        assert tokenize("Hello World") == ["hello", "world"]

    def test_punctuation_split(self) -> None:
        assert tokenize("foo, bar.baz!") == ["foo", "bar", "baz"]

    def test_empty_returns_empty(self) -> None:
        assert tokenize("") == []

    def test_underscore_preserved(self) -> None:
        assert tokenize("F-CLASS-COVERAGE") == ["f", "class", "coverage"]
        assert tokenize("snake_case") == ["snake_case"]


class TestBM25Index:
    def test_empty_corpus_returns_zero(self) -> None:
        idx = _BM25Index([])
        # nothing to score; method still works on no docs by virtue of N=0
        assert idx._n == 0

    def test_single_doc_query_match_scores_positive(self) -> None:
        idx = _BM25Index([["apple", "banana"]])
        assert idx.score(["apple"], 0) > 0.0

    def test_unknown_query_token_scores_zero(self) -> None:
        idx = _BM25Index([["apple", "banana"]])
        assert idx.score(["zebra"], 0) == 0.0

    def test_rarer_term_scores_higher_than_common(self) -> None:
        corpus = [
            ["apple", "common"],
            ["banana", "common"],
            ["cherry", "common"],
        ]
        idx = _BM25Index(corpus)
        score_rare = idx.score(["apple"], 0)
        score_common = idx.score(["common"], 0)
        assert score_rare > score_common


# ---------------------------------------------------------------------------
# Adapter coverage — one assertion per register
# ---------------------------------------------------------------------------


class TestPerRegisterAdapters:
    """One test per register confirming the adapter returns a usable
    Document set against the synthetic repo.
    """

    def test_lessons_json(self, synth_repo: Path) -> None:
        a = get_adapter("lessons_json")
        docs = list(a.enumerate(repo_root=synth_repo, org=None))
        assert len(docs) == 2
        assert docs[0].provenance.locator == "L-001"
        assert "APRICOT" in docs[0].text or "Scout" in docs[0].text

    def test_memory_md(self, synth_repo: Path) -> None:
        a = get_adapter("memory_md")
        docs = list(a.enumerate(repo_root=synth_repo, org=None))
        # Heading line `#` is skipped; only entry rows remain.
        assert len(docs) == 2
        assert "ZEBRA" in docs[0].text
        assert "KOALA" in docs[1].text

    def test_daily_logs(self, synth_repo: Path) -> None:
        a = get_adapter("daily_logs")
        docs = list(a.enumerate(repo_root=synth_repo, org=None))
        assert len(docs) == 2
        # Sorted order: 2026-05-14 before 2026-05-15
        assert docs[0].provenance.locator == "2026-05-14.md"
        assert "CHERRY" in docs[0].text

    def test_lock_history(self, synth_repo: Path) -> None:
        a = get_adapter("lock_history")
        docs = list(a.enumerate(repo_root=synth_repo, org=None))
        assert len(docs) == 2
        assert "TANGERINE" in docs[1].text

    def test_memory_files(self, synth_repo: Path) -> None:
        a = get_adapter("memory_files")
        docs = list(a.enumerate(repo_root=synth_repo, org=None))
        assert len(docs) == 1
        assert "DURIAN" in docs[0].text

    def test_benchmarks(self, synth_repo: Path) -> None:
        a = get_adapter("benchmarks")
        docs = list(a.enumerate(repo_root=synth_repo, org=None))
        assert len(docs) == 1
        assert docs[0].provenance.locator == "bench-ELDERBERRY"

    def test_funder_intelligence(self, synth_repo: Path) -> None:
        a = get_adapter("funder_intelligence")
        docs = list(a.enumerate(repo_root=synth_repo, org=None))
        assert len(docs) == 1
        assert "FIG" in docs[0].text

    def test_match_db_workspace_placeholder_returns_no_docs(
        self, synth_repo: Path
    ) -> None:
        # workspace-shared match_db has no file in the synth repo; this is
        # the documented v0.1 state.
        a = get_adapter("match_db")
        docs = list(a.enumerate(repo_root=synth_repo, org=None))
        assert docs == []

    def test_handoffs(self, synth_repo: Path) -> None:
        a = get_adapter("handoffs")
        docs = list(a.enumerate(repo_root=synth_repo, org=None))
        assert len(docs) == 1
        assert "GRAPE" in docs[0].text

    def test_kfr_per_org(self, synth_repo: Path) -> None:
        a = get_adapter("kfr")
        docs_alpha = list(a.enumerate(repo_root=synth_repo, org="alpha_org"))
        assert len(docs_alpha) == 1
        assert "HONEYDEW" in docs_alpha[0].text
        assert docs_alpha[0].provenance.org == "alpha_org"

    def test_classification_register_per_org(self, synth_repo: Path) -> None:
        a = get_adapter("classification_register")
        docs = list(a.enumerate(repo_root=synth_repo, org="alpha_org"))
        assert len(docs) == 1
        assert "HONEYDEW" in docs[0].text

    def test_reflection_packets_per_org(self, synth_repo: Path) -> None:
        a = get_adapter("reflection_packets")
        docs = list(a.enumerate(repo_root=synth_repo, org="alpha_org"))
        assert len(docs) == 1
        assert "HONEYDEW" in docs[0].text
        assert docs[0].provenance.org == "alpha_org"

    def test_match_database_per_org(self, synth_repo: Path) -> None:
        a = get_adapter("match_database")
        docs = list(a.enumerate(repo_root=synth_repo, org="alpha_org"))
        assert len(docs) == 1
        assert "HONEYDEW" in docs[0].text

    def test_cards_workspace(self, synth_repo: Path) -> None:
        a = get_adapter("cards")
        docs = list(a.enumerate(repo_root=synth_repo, org=None))
        # 1 CIC card + 1 registry.yaml under pipeline/cards/.
        assert len(docs) == 2
        joined = " ".join(d.text for d in docs)
        assert "QUINCE" in joined

    def test_docs_workspace(self, synth_repo: Path) -> None:
        a = get_adapter("docs")
        docs = list(a.enumerate(repo_root=synth_repo, org=None))
        # GETTING_STARTED + nested/deep.md; hidden file skipped.
        names = sorted(d.provenance.locator for d in docs)
        assert names == ["GETTING_STARTED.md", "deep.md"]
        joined = " ".join(d.text for d in docs)
        assert "RAMBUTAN" in joined
        assert "STARFRUIT" in joined
        assert "should be skipped" not in joined


# ---------------------------------------------------------------------------
# Law-3 isolation
# ---------------------------------------------------------------------------


class TestLaw3Isolation:
    def test_per_org_adapter_without_org_raises(self, synth_repo: Path) -> None:
        a = get_adapter("kfr")
        with pytest.raises(Law3Violation):
            list(a.enumerate(repo_root=synth_repo, org=None))

    def test_reserved_template_slug_rejected(self, synth_repo: Path) -> None:
        a = get_adapter("kfr")
        with pytest.raises(Law3Violation):
            list(a.enumerate(repo_root=synth_repo, org="_TEMPLATE"))

    def test_path_traversal_org_rejected(self, synth_repo: Path) -> None:
        a = get_adapter("kfr")
        for bad in ("../escape", "alpha/escape", ".hidden", ""):
            with pytest.raises(Law3Violation):
                list(a.enumerate(repo_root=synth_repo, org=bad))

    def test_registry_query_without_org_excludes_per_org_registers(
        self, synth_repo: Path
    ) -> None:
        r = make_registry()
        # Token "HONEYDEW" is unique to alpha_org's per-org data.
        results = r.query(
            query="HONEYDEW",
            repo_root=synth_repo,
            org=None,
            limit=50,
        )
        assert not results, "per-org token leaked into workspace-only query"

    def test_registry_query_with_org_finds_only_that_org_per_org_data(
        self, synth_repo: Path
    ) -> None:
        r = make_registry()
        results = r.query(
            query="HONEYDEW",
            repo_root=synth_repo,
            org="alpha_org",
            limit=50,
        )
        assert results, "alpha_org query should find its own per-org token"
        for hit in results:
            # Every per-org hit must be tagged to alpha_org, never beta_org.
            assert hit.provenance.org in (None, "alpha_org")

        # And the beta_org-only token should NOT surface in alpha_org's
        # query — the cross-org Law-3 boundary holds.
        results_iceberg = r.query(
            query="ICEBERG",
            repo_root=synth_repo,
            org="alpha_org",
            limit=50,
        )
        for hit in results_iceberg:
            assert hit.provenance.org != "beta_org", (
                "beta_org per-org content leaked into alpha_org query"
            )

    def test_registry_inspect_per_org_requires_org(self, synth_repo: Path) -> None:
        r = make_registry()
        with pytest.raises(Law3Violation):
            r.inspect(register="kfr", repo_root=synth_repo, org=None)

    def test_registry_query_with_explicit_per_org_register_requires_org(
        self, synth_repo: Path
    ) -> None:
        r = make_registry()
        with pytest.raises(Law3Violation):
            r.query(
                query="anything",
                repo_root=synth_repo,
                org=None,
                registers=["kfr"],
                limit=5,
            )


# ---------------------------------------------------------------------------
# Cross-register query + ranking sanity
# ---------------------------------------------------------------------------


class TestCrossRegisterQuery:
    def test_workspace_query_hits_workspace_registers(
        self, synth_repo: Path
    ) -> None:
        r = make_registry()
        results = r.query(
            query="DURIAN", repo_root=synth_repo, org=None, limit=5
        )
        # memory_files contains DURIAN exclusively.
        assert results
        assert results[0].register == "memory_files"

    def test_unique_token_surfaces_its_register_first(
        self, synth_repo: Path
    ) -> None:
        r = make_registry()
        for token, expected_register in (
            ("APRICOT", "lessons_json"),
            ("ZEBRA", "memory_md"),
            ("CHERRY", "daily_logs"),
            ("TANGERINE", "lock_history"),
            ("DURIAN", "memory_files"),
            ("ELDERBERRY", "benchmarks"),
            ("FIG", "funder_intelligence"),
            ("GRAPE", "handoffs"),
        ):
            results = r.query(
                query=token, repo_root=synth_repo, org=None, limit=3
            )
            assert results, f"token {token} found nothing"
            assert results[0].register == expected_register, (
                f"{token} should rank {expected_register} first, got "
                f"{results[0].register}"
            )

    def test_empty_query_raises(self, synth_repo: Path) -> None:
        r = make_registry()
        from pipeline.memory.unified_query import UnifiedQueryError

        with pytest.raises(UnifiedQueryError):
            r.query(query="   ", repo_root=synth_repo, org=None, limit=5)

    def test_query_results_deterministic_tie_break(
        self, synth_repo: Path
    ) -> None:
        r = make_registry()
        # Run twice; results must match.
        a = r.query(
            query="LOCK READY MEMORY", repo_root=synth_repo, org=None, limit=10
        )
        b = r.query(
            query="LOCK READY MEMORY", repo_root=synth_repo, org=None, limit=10
        )
        a_keys = [(round(x.score, 6), x.register, x.provenance.locator) for x in a]
        b_keys = [(round(x.score, 6), x.register, x.provenance.locator) for x in b]
        assert a_keys == b_keys

    def test_query_results_carry_provenance(self, synth_repo: Path) -> None:
        r = make_registry()
        results = r.query(
            query="DURIAN", repo_root=synth_repo, org=None, limit=1
        )
        assert results
        p = results[0].provenance
        assert p.register == "memory_files"
        assert p.source_path.endswith("project_DURIAN.md")
        assert p.locator == "project_DURIAN.md"

    def test_limit_truncates(self, synth_repo: Path) -> None:
        r = make_registry()
        all_results = r.query(
            query="event", repo_root=synth_repo, org=None, limit=100
        )
        cap = r.query(
            query="event", repo_root=synth_repo, org=None, limit=1
        )
        assert len(cap) <= 1
        assert len(cap) <= len(all_results)


# ---------------------------------------------------------------------------
# list_registers + inspect
# ---------------------------------------------------------------------------


class TestListAndInspect:
    def test_list_registers_returns_all_fifteen(self, synth_repo: Path) -> None:
        r = make_registry()
        infos = r.list_registers(repo_root=synth_repo, org=None)
        names = [i.name for i in infos]
        assert set(names) == set(ALL_REGISTERS)
        assert len(infos) == 15

    def test_list_registers_per_org_count_zero_without_org(
        self, synth_repo: Path
    ) -> None:
        r = make_registry()
        infos = r.list_registers(repo_root=synth_repo, org=None)
        by_name = {i.name: i for i in infos}
        for name in PER_ORG_REGISTERS:
            assert by_name[name].document_count == 0
            assert by_name[name].exists is False

    def test_list_registers_with_org_populates_per_org(
        self, synth_repo: Path
    ) -> None:
        r = make_registry()
        infos = r.list_registers(repo_root=synth_repo, org="alpha_org")
        by_name = {i.name: i for i in infos}
        assert by_name["kfr"].document_count >= 1
        assert by_name["kfr"].exists is True
        assert by_name["match_database"].document_count >= 1

    def test_inspect_workspace_register(self, synth_repo: Path) -> None:
        r = make_registry()
        docs = r.inspect(
            register="lessons_json", repo_root=synth_repo, org=None
        )
        assert len(docs) == 2

    def test_inspect_unknown_register_raises(self, synth_repo: Path) -> None:
        r = make_registry()
        with pytest.raises(UnknownRegisterError):
            r.inspect(register="nonexistent", repo_root=synth_repo, org=None)


# ---------------------------------------------------------------------------
# CLI surface
# ---------------------------------------------------------------------------


class TestCliSurface:
    def test_cli_no_verb_fails(self) -> None:
        with pytest.raises(SystemExit):
            cli_main([])

    def test_cli_unknown_verb_fails(self) -> None:
        with pytest.raises(SystemExit):
            cli_main(["bogus"])

    def test_cli_list_registers_json(
        self, synth_repo: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        rc = cli_main(
            [
                "--repo-root",
                str(synth_repo),
                "--json-output",
                "list-registers",
            ]
        )
        assert rc == 0
        out = capsys.readouterr().out
        payload = json.loads(out.strip().splitlines()[-1])
        assert payload["ok"] is True
        assert payload["verb"] == "list-registers"
        assert len(payload["registers"]) == 15

    def test_cli_query_json(
        self, synth_repo: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        rc = cli_main(
            [
                "--repo-root",
                str(synth_repo),
                "--json-output",
                "query",
                "DURIAN",
                "--limit",
                "5",
            ]
        )
        assert rc == 0
        out = capsys.readouterr().out
        payload = json.loads(out.strip().splitlines()[-1])
        assert payload["ok"] is True
        assert payload["result_count"] >= 1
        assert payload["results"][0]["register"] == "memory_files"

    def test_cli_query_per_org_register_without_org_fails(
        self, synth_repo: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        rc = cli_main(
            [
                "--repo-root",
                str(synth_repo),
                "query",
                "HONEYDEW",
                "--register",
                "kfr",
            ]
        )
        assert rc == 1
        err = capsys.readouterr().err
        assert "Law 3" in err or "per-org" in err

    def test_cli_inspect_per_org_register_without_org_fails(
        self, synth_repo: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        rc = cli_main(
            [
                "--repo-root",
                str(synth_repo),
                "inspect",
                "kfr",
            ]
        )
        assert rc == 1
        err = capsys.readouterr().err
        assert "Law 3" in err or "per-org" in err

    def test_cli_inspect_per_org_register_with_org_succeeds(
        self, synth_repo: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        rc = cli_main(
            [
                "--repo-root",
                str(synth_repo),
                "--json-output",
                "inspect",
                "kfr",
                "--org",
                "alpha_org",
            ]
        )
        assert rc == 0
        out = capsys.readouterr().out
        payload = json.loads(out.strip().splitlines()[-1])
        assert payload["ok"] is True
        assert payload["document_count"] == 1

    def test_cli_query_with_org_finds_per_org_token(
        self, synth_repo: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        rc = cli_main(
            [
                "--repo-root",
                str(synth_repo),
                "--json-output",
                "query",
                "HONEYDEW",
                "--org",
                "alpha_org",
            ]
        )
        assert rc == 0
        out = capsys.readouterr().out
        payload = json.loads(out.strip().splitlines()[-1])
        assert payload["result_count"] >= 1
        # No beta_org leakage.
        for r in payload["results"]:
            assert r["org"] in (None, "alpha_org")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


class TestHelpers:
    def test_dict_to_text_is_stable_across_runs(self) -> None:
        d = {"b": 2, "a": {"y": "value", "x": [1, 2, 3]}}
        t1 = _dict_to_text(d)
        t2 = _dict_to_text(d)
        assert t1 == t2
        # All values appear.
        for token in ("a", "b", "x", "y", "value", "1", "2", "3"):
            assert token in t1

    def test_excerpt_centers_on_query(self) -> None:
        text = "x" * 100 + " NEEDLE " + "y" * 100
        e = _excerpt(text, ["needle"], window=60)
        assert "NEEDLE" in e
        assert e.startswith("…") or e.startswith("x")



# ---------------------------------------------------------------------------
# 2026-05-18 CLI surface extensions: --source / --top / --format / --posture
# ---------------------------------------------------------------------------


class TestCliSurfaceExtensions:
    """Coverage for the 2026-05-18 ergonomic + posture additions:

    * --source vocabulary mapping to canonical register names.
    * --top alias for --limit (mutual exclusion enforced).
    * --format text|json alias for --json-output.
    * --posture local-only acceptance + rejection of the two
      forward-compat values that are not yet wired.
    * cards and docs adapters reachable end-to-end via the CLI.
    * Empty-result handling (no error, exit 0).
    """

    def test_source_cards_returns_cards_hit(
        self, synth_repo: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        rc = cli_main(
            [
                "--repo-root",
                str(synth_repo),
                "--format",
                "json",
                "query",
                "QUINCE",
                "--source",
                "cards",
            ]
        )
        assert rc == 0
        out = capsys.readouterr().out
        payload = json.loads(out.strip().splitlines()[-1])
        assert payload["result_count"] >= 1
        assert payload["results"][0]["register"] == "cards"
        assert payload["source"] == "cards"
        assert payload["registers"] == ["cards"]

    def test_source_docs_returns_docs_hit(
        self, synth_repo: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        rc = cli_main(
            [
                "--repo-root",
                str(synth_repo),
                "--format",
                "json",
                "query",
                "RAMBUTAN",
                "--source",
                "docs",
            ]
        )
        assert rc == 0
        out = capsys.readouterr().out
        payload = json.loads(out.strip().splitlines()[-1])
        assert payload["result_count"] >= 1
        assert payload["results"][0]["register"] == "docs"

    def test_source_lessons_alias_maps_to_lessons_json(
        self, synth_repo: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        rc = cli_main(
            [
                "--repo-root",
                str(synth_repo),
                "--format",
                "json",
                "query",
                "APRICOT",
                "--source",
                "lessons",
            ]
        )
        assert rc == 0
        out = capsys.readouterr().out
        payload = json.loads(out.strip().splitlines()[-1])
        assert payload["registers"] == ["lessons_json"]
        assert payload["result_count"] >= 1
        assert payload["results"][0]["register"] == "lessons_json"

    def test_source_all_clears_register_filter(
        self, synth_repo: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        rc = cli_main(
            [
                "--repo-root",
                str(synth_repo),
                "--format",
                "json",
                "query",
                "DURIAN",
                "--source",
                "all",
            ]
        )
        assert rc == 0
        out = capsys.readouterr().out
        payload = json.loads(out.strip().splitlines()[-1])
        # --source all means "no register filter"; payload.registers
        # is None to surface that explicitly to callers.
        assert payload["registers"] is None
        assert payload["source"] == "all"

    def test_source_and_register_mutually_exclusive(
        self, synth_repo: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        rc = cli_main(
            [
                "--repo-root",
                str(synth_repo),
                "query",
                "QUINCE",
                "--source",
                "cards",
                "--register",
                "cards",
            ]
        )
        assert rc == 1
        err = capsys.readouterr().err
        assert "mutually exclusive" in err

    def test_top_alias_for_limit(
        self, synth_repo: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        rc = cli_main(
            [
                "--repo-root",
                str(synth_repo),
                "--format",
                "json",
                "query",
                "event",
                "--top",
                "1",
            ]
        )
        assert rc == 0
        out = capsys.readouterr().out
        payload = json.loads(out.strip().splitlines()[-1])
        assert payload["limit"] == 1
        assert payload["result_count"] <= 1

    def test_top_and_limit_mutually_exclusive(
        self, synth_repo: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        rc = cli_main(
            [
                "--repo-root",
                str(synth_repo),
                "query",
                "event",
                "--limit",
                "2",
                "--top",
                "1",
            ]
        )
        assert rc == 1
        err = capsys.readouterr().err
        assert "mutually exclusive" in err

    def test_format_text_is_default_human_output(
        self, synth_repo: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        rc = cli_main(
            [
                "--repo-root",
                str(synth_repo),
                "query",
                "DURIAN",
            ]
        )
        assert rc == 0
        out = capsys.readouterr().out
        # Human text output starts with a score column; never a `{`.
        assert not out.strip().startswith("{")
        assert "memory_files" in out

    def test_format_json_emits_json_payload(
        self, synth_repo: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        rc = cli_main(
            [
                "--repo-root",
                str(synth_repo),
                "--format",
                "json",
                "query",
                "DURIAN",
            ]
        )
        assert rc == 0
        out = capsys.readouterr().out
        # Last line must parse as JSON.
        payload = json.loads(out.strip().splitlines()[-1])
        assert payload["ok"] is True
        assert payload["verb"] == "query"

    def test_posture_default_local_only_emitted_in_payload(
        self, synth_repo: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        rc = cli_main(
            [
                "--repo-root",
                str(synth_repo),
                "--format",
                "json",
                "query",
                "DURIAN",
            ]
        )
        assert rc == 0
        out = capsys.readouterr().out
        payload = json.loads(out.strip().splitlines()[-1])
        assert payload["posture"] == "local-only"

    def test_posture_frontier_eligible_rejected_at_runtime(
        self, synth_repo: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        rc = cli_main(
            [
                "--repo-root",
                str(synth_repo),
                "--posture",
                "frontier-eligible",
                "query",
                "DURIAN",
            ]
        )
        assert rc == 1
        err = capsys.readouterr().err
        assert "frontier-eligible" in err
        assert "not currently supported" in err
        # Crucially, the error must direct the operator to the prereq.
        assert "classification-review" in err.lower() or "classification review" in err.lower()

    def test_posture_split_context_hybrid_rejected_at_runtime(
        self, synth_repo: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        rc = cli_main(
            [
                "--repo-root",
                str(synth_repo),
                "--posture",
                "split-context-hybrid",
                "query",
                "DURIAN",
            ]
        )
        assert rc == 1
        err = capsys.readouterr().err
        assert "split-context-hybrid" in err

    def test_posture_unknown_value_rejected_by_argparse(
        self, synth_repo: Path
    ) -> None:
        with pytest.raises(SystemExit):
            cli_main(
                [
                    "--repo-root",
                    str(synth_repo),
                    "--posture",
                    "cloud-only",
                    "query",
                    "DURIAN",
                ]
            )

    def test_query_zero_results_exits_zero(
        self, synth_repo: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        rc = cli_main(
            [
                "--repo-root",
                str(synth_repo),
                "--format",
                "json",
                "query",
                "ZZZNONEXISTENTTOKEN",
            ]
        )
        assert rc == 0
        out = capsys.readouterr().out
        payload = json.loads(out.strip().splitlines()[-1])
        assert payload["result_count"] == 0
        assert payload["results"] == []


class TestSourceAliasMapShape:
    """Tight assertions on the SOURCE_ALIAS_MAP — guard against silent
    drift between the CLI ``--source`` choices and the canonical
    register names downstream consumers depend on.
    """

    def test_alias_map_keys_match_spec(self) -> None:
        from pipeline.cli.tilth_memory_query import SOURCE_ALIAS_MAP

        assert set(SOURCE_ALIAS_MAP.keys()) == {
            "lessons",
            "lock_history",
            "cards",
            "docs",
            "all",
        }

    def test_alias_map_values_resolve_to_known_registers(self) -> None:
        from pipeline.cli.tilth_memory_query import SOURCE_ALIAS_MAP

        for alias, registers in SOURCE_ALIAS_MAP.items():
            if registers is None:
                continue
            for name in registers:
                assert name in ALL_REGISTERS, (
                    f"--source {alias!r} maps to unknown register {name!r}"
                )

    def test_all_alias_maps_to_no_filter(self) -> None:
        from pipeline.cli.tilth_memory_query import SOURCE_ALIAS_MAP

        assert SOURCE_ALIAS_MAP["all"] is None

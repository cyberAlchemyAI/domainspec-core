"""tilth wpfa CLI tests. [§17.7.4, §2.14.6 — Layer 4 of three-layer defense]"""

from __future__ import annotations

import pytest

from pipeline.cli.tilth_wpfa import BANNED_FLAGS, _reject_banned_flags, main


class TestBannedFlagRejection:
    @pytest.mark.parametrize("banned", BANNED_FLAGS)
    def test_each_banned_flag_rejected(self, banned: str) -> None:
        with pytest.raises(SystemExit, match=banned):
            _reject_banned_flags([banned])

    @pytest.mark.parametrize("banned", BANNED_FLAGS)
    def test_banned_flag_with_equals_rejected(self, banned: str) -> None:
        # --yes=true should fail too (the flag value form)
        with pytest.raises(SystemExit, match=banned):
            _reject_banned_flags([f"{banned}=true"])

    def test_innocuous_flag_passes(self) -> None:
        _reject_banned_flags(["--repo-root", "/tmp"])

    def test_main_rejects_banned_via_argv(self) -> None:
        with pytest.raises(SystemExit, match="--yes"):
            main(["--yes", "pdf", "emit"])


class TestArgparseStructure:
    def test_pdf_emit_requires_subparser(self) -> None:
        with pytest.raises(SystemExit):
            main(["pdf"])  # missing required subverb

    def test_registry_requires_subverb(self) -> None:
        with pytest.raises(SystemExit):
            main(["registry"])  # missing required subverb

    def test_no_verb_fails(self) -> None:
        with pytest.raises(SystemExit):
            main([])

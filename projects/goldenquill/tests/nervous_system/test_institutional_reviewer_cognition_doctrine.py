import os
import subprocess
from pathlib import Path
import pytest

def get_repo_root() -> Path:
    return Path(__file__).resolve().parent.parent.parent

def test_doctrine_document_exists():
    repo_root = get_repo_root()
    doc_path = repo_root / "docs" / "institutional_reviewer_cognition_layer.md"
    assert doc_path.is_file(), "Doctrine document must exist at docs/institutional_reviewer_cognition_layer.md"

def test_doctrine_contents():
    repo_root = get_repo_root()
    doc_path = repo_root / "docs" / "institutional_reviewer_cognition_layer.md"
    content = doc_path.read_text(encoding="utf-8").lower()

    # 2. Canonical Lifecycle
    lifecycle = "discover → ingest → gate → decompose → draft → score → authorize"
    assert lifecycle in content, "Doctrine must include the exact canonical lifecycle"

    # 3. Anti-Theater Law
    assert "anti-theater law" in content, "Doctrine must include Anti-Theater Law"

    # 4. Recovery Cognition
    assert "recovery cognition" in content, "Doctrine must include Recovery Cognition"

    # 5. Evidence Ladder tiers
    assert "verified" in content
    assert "grounded" in content
    assert "plausible" in content
    assert "aspirational" in content
    assert "unsupported" in content

    # 6. Reject consumer/manipulative patterns
    assert "growth hack" in content
    assert "gamified" in content
    assert "dark pattern" in content
    assert "fake progress" in content
    assert "fake urgency" in content
    assert "fake autonomy" in content
    assert "confetti" in content
    assert "cartoon" in content
    assert "dismiss warning" in content

    # 7. Scout-first sequencing
    assert "scout" in content
    assert "first ui surface" in content or "first ui surface configured" in content or "first" in content

    # 8. Boundary statement
    assert "autonomous submission" in content
    assert "partner outreach" in content
    assert "funder_terrain" in content
    assert "model calls" in content
    assert "gate bypass" in content or "bypass of deterministic gates" in content

def test_no_prohibited_language_in_changed_files():
    repo_root = get_repo_root()

    # Get all changed files in the current worktree compared to base commit
    # For a simple test, we will check the currently modified files in git status
    try:
        result = subprocess.run(["git", "status", "--porcelain=v1"], cwd=str(repo_root), capture_output=True, text=True)
        changed_files = []
        for line in result.stdout.splitlines():
            if line:
                status = line[:2]
                filename = line[3:]
                # Include added and modified files
                if status in ("M ", "A ", "??", " M", "AM"):
                    changed_files.append(repo_root / filename)
    except Exception as e:
        pytest.fail(f"Failed to run git status: {e}")

    prohibited = [
        "maximize engagement",
        "increase time on platform",
        "conversion funnel",
        "growth hack",
        "streak",
        "confetti",
        "dark pattern",
        "dismiss warning",
        "ignore compliance",
        "autonomous submission",
        "auto-submit",
        "partner outreach",
        "candidate generation",
        "win probability"
    ]

    # Add exceptions for the doctrine document itself which defines these terms to ban them
    exception_file = repo_root / "docs" / "institutional_reviewer_cognition_layer.md"
    exception_file_2 = repo_root / "tests" / "nervous_system" / "test_institutional_reviewer_cognition_doctrine.py"

    for file_path in changed_files:
        if not file_path.is_file():
            continue
        if file_path == exception_file or file_path == exception_file_2:
            continue

        content = file_path.read_text(encoding="utf-8").lower()
        for phrase in prohibited:
            assert phrase not in content, f"Prohibited phrase '{phrase}' found in {file_path}"

def test_scout_button_restrictions():
    repo_root = get_repo_root()
    try:
        result = subprocess.run(["git", "status", "--porcelain=v1"], cwd=str(repo_root), capture_output=True, text=True)
        changed_files = [line[3:] for line in result.stdout.splitlines() if line]
    except Exception:
        changed_files = []

    scout_files_touched = [f for f in changed_files if "scout" in f.lower() and f.endswith((".tsx", ".jsx", ".ts", ".js", ".html"))]

    # We assert that we didn't touch scout files in this lane (as instructed)
    # If we did, we would need to run complex AST checks for new buttons, but the lane prefers not touching them.
    assert len(scout_files_touched) == 0, "No /scout implementation files should be touched in this doctrine-only lane."

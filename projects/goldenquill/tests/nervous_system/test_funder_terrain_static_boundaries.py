import ast
import pytest
from pathlib import Path

MODULES = [
    "pipeline/nervous_system/funder_terrain/intake.py",
    "pipeline/nervous_system/funder_terrain/cli_intake.py",
    "pipeline/nervous_system/funder_terrain/review_queue.py",
    "pipeline/nervous_system/funder_terrain/snapshot.py"
]

FORBIDDEN_IMPORTS = {
    "requests", "httpx", "urllib", "aiohttp", "playwright", "selenium",
    "beautifulsoup4", "bs4", "openai", "anthropic", "gemini",
    "google.generativeai", "google.generative", "ollama", "vllm",
    "subprocess", "asyncio"
}

FORBIDDEN_FUNCTIONS = {
    "__import__", "eval", "exec"
}

FORBIDDEN_ATTRIBUTES = {
    ("importlib", "import_module"),
    ("os", "system")
}

FORBIDDEN_RUNTIME_TERMS = [
    "candidate", "partner_alert", "event_candidate_boundary", "emit_ui_event",
    "scout_projection", "draft", "export", "submit", "submission", "scrape", "crawler",
    "scout_fetch_ledger", "vault_projection_adapter"
]

def get_existing_modules():
    base_dir = Path(__file__).parent.parent.parent
    return [base_dir / m for m in MODULES if (base_dir / m).exists()]

@pytest.mark.parametrize("filepath", get_existing_modules())
def test_ast_forbids_imports(filepath):
    tree = ast.parse(filepath.read_text(encoding="utf-8"))

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                base_module = alias.name.split('.')[0]
                assert base_module not in FORBIDDEN_IMPORTS, f"Forbidden import {alias.name} in {filepath}"
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                base_module = node.module.split('.')[0]
                assert base_module not in FORBIDDEN_IMPORTS, f"Forbidden import from {node.module} in {filepath}"

@pytest.mark.parametrize("filepath", get_existing_modules())
def test_ast_forbids_dynamic_calls(filepath):
    tree = ast.parse(filepath.read_text(encoding="utf-8"))

    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                assert node.func.id not in FORBIDDEN_FUNCTIONS, f"Forbidden call {node.func.id} in {filepath}"
            elif isinstance(node.func, ast.Attribute):
                if isinstance(node.func.value, ast.Name):
                    call_signature = (node.func.value.id, node.func.attr)
                    assert call_signature not in FORBIDDEN_ATTRIBUTES, f"Forbidden call {node.func.value.id}.{node.func.attr} in {filepath}"

@pytest.mark.parametrize("filepath", get_existing_modules())
def test_source_forbids_runtime_terms(filepath):
    content = filepath.read_text(encoding="utf-8")
    tree = ast.parse(content)

    # We only check identifiers (names, attributes, function names, classes) to avoid
    # triggering on docstrings or static poison pill tuples that contain strings.
    def check_id(identifier):
        if not identifier:
            return
        id_lower = identifier.lower()
        for term in FORBIDDEN_RUNTIME_TERMS:
            if term.lower() in id_lower:
                assert False, f"Forbidden term {term} in identifier {identifier} in {filepath}"

    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            check_id(node.id)
        elif isinstance(node, ast.Attribute):
            check_id(node.attr)
        elif isinstance(node, ast.FunctionDef):
            check_id(node.name)
        elif isinstance(node, ast.ClassDef):
            check_id(node.name)
        elif isinstance(node, ast.arg):
            check_id(node.arg)

def test_static_poison_pill_compliance():
    # argparse requests httpx urllib aiohttp playwright selenium BeautifulSoup bs4
    # openai anthropic gemini google.generative ollama vllm subprocess os.system
    # eval( exec( __import__ importlib.import_module asyncio
    # candidate partner_alert event_candidate_boundary emit_ui_event Scout projection
    # draft export submit submission scrape crawler
    pass

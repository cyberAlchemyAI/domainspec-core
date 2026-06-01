import ast
from pathlib import Path

import pytest


ADAPTER_PATH = Path("pipeline/nervous_system/scout_adapters/channel_g_local.py")


def test_adapter_imports_only_allowed_modules():
    source = ADAPTER_PATH.read_text(encoding="utf-8")
    tree = ast.parse(source)

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                pytest.fail(f"Forbidden import: {alias.name}")
        elif isinstance(node, ast.ImportFrom):
            if node.module != "pipeline.scout._channel_g_parser":
                pytest.fail(f"Forbidden from-import module: {node.module}")
            allowed_names = {"ChannelGParseResult", "parse_channel_g_csv_text"}
            for alias in node.names:
                if alias.name not in allowed_names:
                    pytest.fail(f"Forbidden imported name: {alias.name}")


def test_adapter_does_not_import_forbidden_modules():
    source = ADAPTER_PATH.read_text(encoding="utf-8")
    tree = ast.parse(source)

    forbidden_modules = {
        "requests", "httpx", "urllib", "aiohttp", "playwright", "selenium",
        "bs4", "BeautifulSoup", "openai", "anthropic", "gemini", "google.generative",
        "ollama", "vllm", "sqlite", "sqlalchemy", "subprocess", "os", "pathlib", "importlib"
    }

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                base_module = alias.name.split('.')[0]
                if base_module in forbidden_modules:
                    pytest.fail(f"Imported forbidden module: {base_module}")
        elif isinstance(node, ast.ImportFrom):
            base_module = node.module.split('.')[0] if node.module else ""
            if base_module in forbidden_modules:
                pytest.fail(f"Imported from forbidden module: {base_module}")


def test_adapter_does_not_contain_forbidden_action_terms():
    source = ADAPTER_PATH.read_text(encoding="utf-8")
    tree = ast.parse(source)

    # Remove docstrings
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.body and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Constant):
                if isinstance(node.body[0].value.value, str):
                    node.body.pop(0)

    code_without_docstrings = ast.unparse(tree).lower()

    forbidden_terms = [
        "fetch", "scrape", "crawl", "browser", "search", "candidate_generation",
        "partner_alert", "draft", "export", "submit", "submission", "database",
        "insert", "update", "delete"
    ]

    for term in forbidden_terms:
        assert term not in code_without_docstrings, f"Forbidden term found in source: {term}"


def test_adapter_is_thin_delegation_boundary():
    source = ADAPTER_PATH.read_text(encoding="utf-8")
    tree = ast.parse(source)

    func_node = None
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == "ingest_local_channel_g_csv":
            func_node = node
            break

    assert func_node is not None, "Function ingest_local_channel_g_csv not found"

    # Verify the return statement is a direct call to parse_channel_g_csv_text
    return_node = None
    for node in func_node.body:
        if isinstance(node, ast.Return):
            return_node = node
            break

    assert return_node is not None, "No return statement found"
    assert isinstance(return_node.value, ast.Call), "Return value is not a function call"

    call_func = return_node.value.func
    assert isinstance(call_func, ast.Name) or (isinstance(call_func, ast.Attribute) and call_func.attr == "parse_channel_g_csv_text")
    if isinstance(call_func, ast.Name):
        assert call_func.id == "parse_channel_g_csv_text", "Return call is not parse_channel_g_csv_text"


def test_adapter_does_not_mutate_global_state():
    source = ADAPTER_PATH.read_text(encoding="utf-8")
    tree = ast.parse(source)

    for node in ast.walk(tree):
        if isinstance(node, ast.Global):
            pytest.fail("Found 'global' keyword in adapter")
        if isinstance(node, ast.Nonlocal):
            pytest.fail("Found 'nonlocal' keyword in adapter")

    module_assignments = [n for n in tree.body if isinstance(n, ast.Assign) or isinstance(n, ast.AnnAssign)]
    assert len(module_assignments) == 0, "Module-level assignments found"

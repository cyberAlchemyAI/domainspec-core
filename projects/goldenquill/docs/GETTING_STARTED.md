# Getting Started

Development environment setup for Tilth v0.1 on an M1 Mac Mini (8 GB RAM).

## Prerequisites

- macOS (Apple Silicon — M1 or later)
- Python 3.11+ (the project uses `kw_only=True` dataclasses and other 3.10+ features; `pyproject.toml` pins `>=3.11`)
- Git
- Ollama (for local Scout inference)

**Important:** System Python on macOS is 3.9 and cannot even *collect* the test suite. Always use the virtual environment.

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/jinks412/golden-quill.git
cd golden-quill
```

### 2. Create the virtual environment

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

Verify the interpreter:

```bash
python --version
# Should print Python 3.11.x or higher
```

### 3. Install dependencies

```bash
pip install -e ".[dev]"
```

This installs the project in editable mode with dev dependencies (pytest, coverage, linting tools).

### 4. Install Ollama

Scout runs locally on `mistral:7b` via Ollama. Install and pull the model:

```bash
# Install Ollama (if not already installed)
brew install ollama

# Start the Ollama daemon
ollama serve &

# Pull the Scout model
ollama pull mistral:7b
```

Verify Ollama is serving:

```bash
curl -s http://localhost:11434/api/tags | python -m json.tool
```

### 5. Set up API keys (BYOK)

Create a `.env` file in the project root (this file is gitignored):

```bash
# Required for Scribe (Claude Sonnet 4.6)
ANTHROPIC_API_KEY=sk-ant-...

# Required for Judge (Gemini 2.5 Pro)
GOOGLE_API_KEY=...

# Required for Editor + Red Team (Groq-hosted models)
GROQ_API_KEY=gsk_...

# Optional — OpenAI for Red Team escalation (GPT-5.1)
OPENAI_API_KEY=sk-...
```

Model routing is defined in `router.yaml`. Edit only that file to change model bindings.

## Running Tests

**Always use the virtual environment interpreter.** The pinned test runner script handles this:

```bash
# Preferred — uses the correct interpreter automatically
./scripts/run_tests.sh

# Or invoke pytest directly through the venv
.venv/bin/python3 -m pytest tests/ logician/tests/ -v
```

**Never** run `python3 -m pytest` without activating the venv first — system Python 3.9 will report collection errors that are not real failures.

### Test categories

The suite includes unit tests, adversarial tests (prefixed `test_adv_`), integration tests, property-based tests (BT-series), and fuzz tests. Current count: ~6,800 test functions.

### Coverage

```bash
.venv/bin/python3 -m pytest tests/ --cov=pipeline --cov=logician --cov-report=term-missing
```

### AST lint check

The project enforces structural lint rules via AST analysis (no banned imports, no dynamic attribute access in security-critical paths, etc.):

```bash
.venv/bin/python3 -m pytest tests/linting/test_ast_lint.py -v
```

## Project Layout

```
pipeline/
  architecture/     # locked architecture docs (v7, A1-A12)
  blueprint/        # section-by-section build specs
  engineering/      # lock history, spec cards, process docs
  seats/            # council seat implementations
  orchestrator/     # pipeline orchestration
  rubrics/          # funder rubric library
tests/              # full test suite
logician/           # deterministic validation engine
router.yaml         # model bindings (sole source of truth)
SOUL.md             # operating principles (Five Laws, Four Rules)
```

## Dev Hardware Notes

The M1 Mac Mini with 8 GB RAM is the dev-tier target. The pipeline uses 20% safety margins on this hardware. Production Golden Quills run 128 GB+ with 5-10% margins.

Ollama running `mistral:7b` fits comfortably in 8 GB alongside the test suite. Larger models (for testing Scribe/Judge/Editor locally) require cloud API fallback on this hardware.

## Workflow

See [GIT_WORKFLOW.md](GIT_WORKFLOW.md) for commit conventions and branching strategy.

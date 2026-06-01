# Frontend Boundary

This document defines the strict architectural boundaries and directories for the frontend layer of the Tilth system. Future agents and engineers MUST respect these definitions to prevent prototype/scaffold code from drifting into the production path.

## Directory Definitions

* `apps/tilth_ui_react/`
  **Target UI.** This is the canonical frontend. It is a Vite React application that expects a standard API backend. It does NOT invoke system commands or call language models directly.

* `apps/tilth_ui/`
  **Legacy Scaffold / Archive.** This is the old Stitch HTML + `server.mjs` prototype. It is retained strictly as historical scaffold and a test reference. Do not add new features here. Do not treat this as a parallel UI.

* `pipeline/deprecated/operator_glue/tilth_scout_ui.py`
  **Dev Bridge Only.** This is a temporary prototyping CLI used for fast iteration. It bypasses production boundaries (like the F-CLASS verification and orchestrator classification). It must NOT be invoked by the React application in production.

* `localhost:8000`
  **FastAPI Nervous System.** This is the expected backend for the React application. The React app connects to this port via a `/api` Vite proxy. The FastAPI backend is the layer that has authority to interact with the governed Scout / Logician / Memory / Model Access Boundary.

## The Production Target Path

```text
React Client (apps/tilth_ui_react)
  ↓
/api proxy
  ↓
FastAPI/Pydantic Nervous System (localhost:8000)
  ↓
governed Python services (Scout / Logician / etc)
```

## Anti-Patterns (Do Not Do These)

1. **Do not wire React to shell scripts or subprocesses.** `apps/tilth_ui_react` should never attempt to execute `pipeline/deprecated/operator_glue/tilth_scout_ui.py` via `child_process` or `subprocess`.
2. **Do not point React directly to model providers.** The frontend should not hold API keys or call Anthropic/OpenAI/Ollama directly.
3. **Do not reintroduce `server.mjs`.** The previous Node/Express proxy layer used by the Stitch prototype is deprecated. Do not resurrect it to serve the React application.

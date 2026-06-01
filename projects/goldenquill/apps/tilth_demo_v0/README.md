# Tilth Demo v0 — Funding Workbench

Clickable demo of the Tilth UI for marketing capture and operator dogfooding. Runs on the Mac Mini alongside OpenClaw. Lives at `apps/tilth_demo_v0/` so the real production UI can land later at `apps/tilth_ui/` without confusion.

## What this is

A working FastAPI + static-HTML application that renders seven screens — Home, Client Vault, Pipeline, Opportunity Read-Pass, Grant Module Mapper, Draft Workbench, Evidence Ledger, Blockers & Next Actions — over the FIT Farms client folder. Files appear in the UI as they land on disk. Agent runs dispatch through the OpenClaw `tilth` agent. The UI never owns LLM logic; it watches files, shells out to OpenClaw, and streams the results back.

Two modes:

- **live** (default on the Mac Mini) — reads from `~/Downloads/GoldenQuill/orgs/fit_farms/`, fires agent runs through OpenClaw, watches the file system for real events.
- **demo** — reads from `apps/tilth_demo_v0/fixtures/` instead, with simulated delays. Same UI code path. For website asset capture on any machine and for the five fabricated orgs that don't have live deployments.

## Architecture

```
apps/tilth_demo_v0/
├── server.py              FastAPI shell — static serving, SSE endpoints, mode flag
├── openclaw_bridge.py     subprocess wrapper around `openclaw agent run`
├── pyproject.toml         deps: fastapi, uvicorn, watchdog, httpx
├── static/
│   ├── index.html         single-page app, hash routing, 7 screens
│   ├── style.css          dark sidebar + light content area, marketing-screen fidelity
│   └── app.js             hash routing, SSE listeners, file-event animation
└── fixtures/
    └── orgs.json          six demo orgs (FIT Farms + 5 fabricated CIC archetypes)
```

The FastAPI server imports `pipeline.logician` and `pipeline.privacy` directly for gate evaluation and classification routing. LLM dispatch goes through `openclaw_bridge.dispatch()` which shells out to the `openclaw` CLI with the correct PATH.

## Run

```bash
cd ~/Downloads/GoldenQuill/apps/tilth_demo_v0
pip install -e .
uvicorn server:app --reload --port 8000
# open http://127.0.0.1:8000 in a browser
```

Add `--mode demo` to launch against fixtures instead of live data.

## What this is NOT

Not the production Tilth UI. Not auth, not real model routing, not full database, not production security, not user roles, not real portal integration. Phase A.0 dogfood scaffold for capture + iteration. The real Tilth UI lands at `apps/tilth_ui/` after a separate v1 Thesis Team architecture round.

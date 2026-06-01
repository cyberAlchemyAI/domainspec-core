"""
Tilth Demo v0 — FastAPI server.

Serves the static UI on / and exposes a small API surface for:
  - GET  /api/orgs                          → list of orgs in current mode
  - GET  /api/orgs/{slug}                   → one org's profile + state
  - GET  /api/orgs/{slug}/opportunities     → in-flight opportunities for this org
  - POST /api/agents/{seat}/run             → dispatch a seat via OpenClaw, streamed via SSE
  - GET  /api/events/files/{slug}           → SSE stream of file-creation events on orgs/{slug}/
  - GET  /api/health                        → bridge + gateway health snapshot

Mode flag: --mode live (default) reads from ~/Downloads/GoldenQuill/orgs/{slug}/
           --mode demo            reads from apps/tilth_demo_v0/fixtures/orgs.json

The server imports pipeline.logician and pipeline.privacy where useful for gate
evaluation and classification routing. LLM dispatch is via openclaw_bridge.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path
from typing import AsyncIterator

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

import openclaw_bridge

# ---- mode + paths ----------------------------------------------------------

DEMO_MODE = os.environ.get("TILTH_DEMO_MODE", "live")  # "live" | "demo"
APP_DIR = Path(__file__).resolve().parent
STATIC_DIR = APP_DIR / "static"
FIXTURES_DIR = APP_DIR / "fixtures"
WORKSPACE_ROOT = openclaw_bridge.workspace_root()
ORGS_DIR = WORKSPACE_ROOT / "orgs"


def fixtures() -> dict:
    """Load fixture data once per call (small file, hot reload is fine)."""
    with (FIXTURES_DIR / "orgs.json").open() as f:
        return json.load(f)


# ---- app -------------------------------------------------------------------

app = FastAPI(title="Tilth Demo v0", docs_url=None, redoc_url=None)


@app.get("/api/health")
async def health() -> dict:
    return {
        "mode": DEMO_MODE,
        "workspace_root": str(WORKSPACE_ROOT),
        "openclaw": await openclaw_bridge.health_check(),
    }


@app.get("/api/orgs")
async def list_orgs() -> JSONResponse:
    """Six org cards for the Home dashboard."""
    return JSONResponse(fixtures()["orgs"])


@app.get("/api/orgs/{slug}")
async def get_org(slug: str) -> JSONResponse:
    """One org's profile + state."""
    orgs = {o["slug"]: o for o in fixtures()["orgs"]}
    if slug not in orgs:
        return JSONResponse({"error": f"unknown org: {slug}"}, status_code=404)
    org = dict(orgs[slug])
    # In live mode, FIT Farms data merges on-disk PROJECT_CONTEXT + memory briefs.
    # Other orgs always read from fixtures.
    if DEMO_MODE == "live" and slug == "fit_farms":
        on_disk = _read_fit_farms_live()
        if on_disk:
            org["live_overlay"] = on_disk
    return JSONResponse(org)


@app.get("/api/orgs/{slug}/opportunities")
async def get_opportunities(slug: str) -> JSONResponse:
    orgs = {o["slug"]: o for o in fixtures()["orgs"]}
    if slug not in orgs:
        return JSONResponse({"error": f"unknown org: {slug}"}, status_code=404)
    return JSONResponse(orgs[slug].get("opportunities", []))


# ---- SSE: agent dispatch ---------------------------------------------------

@app.post("/api/agents/{seat}/run")
async def run_agent(seat: str, req: Request) -> StreamingResponse:
    """Dispatch a seat via OpenClaw. Streams structured SSE events.

    Event shapes:
      event: start    data: {"seat": "...", "session_id": "...", "cmd": "..."}
      event: stdout   data: {"text": "..."}      (raw line from openclaw)
      event: result   data: {"text": "...", "meta": {...}}    (parsed payload)
      event: done     data: {"ok": true|false, "exit_code": int}
      event: error    data: {"text": "..."}
    """
    body = await req.json()
    prompt = body.get("prompt", "")
    if not prompt:
        return JSONResponse({"error": "missing prompt"}, status_code=400)

    async def sse(event: str, data: dict) -> str:
        return f"event: {event}\ndata: {json.dumps(data)}\n\n"

    async def gen() -> AsyncIterator[str]:
        if DEMO_MODE == "demo":
            canned = fixtures().get("simulated_runs", {}).get(seat, [
                {"event": "start", "data": {"seat": seat}},
                {"event": "stdout", "data": {"text": f"[demo mode] seat={seat} acknowledged.\n"}},
                {"event": "done", "data": {"ok": True}},
            ])
            for step in canned:
                await asyncio.sleep(0.6)
                # Map legacy "token" to "stdout" for UI consistency
                evt_name = "stdout" if step["event"] == "token" else step["event"]
                yield await sse(evt_name, step["data"])
            return

        # live mode — real openclaw dispatch
        yield await sse("start", {"seat": seat})
        exit_code: int = -1
        try:
            async for evt in openclaw_bridge.dispatch_agent_turn(prompt):
                kind = evt.get("kind")
                if kind == "session":
                    yield await sse("start", {
                        "seat": seat,
                        "session_id": evt.get("session_id"),
                        "cmd": evt.get("cmd"),
                    })
                elif kind == "stdout":
                    yield await sse("stdout", {"text": evt.get("text", "")})
                elif kind == "result":
                    data = evt.get("data", {})
                    # Extract the agent's visible reply (if shaped like the
                    # openclaw agent --json envelope we observed).
                    text = ""
                    try:
                        payloads = data.get("result", {}).get("payloads", [])
                        if payloads and isinstance(payloads, list):
                            text = payloads[0].get("text", "") or ""
                    except (AttributeError, IndexError, TypeError):
                        pass
                    meta = {}
                    try:
                        meta = data.get("result", {}).get("meta", {}) or {}
                    except (AttributeError, TypeError):
                        pass
                    yield await sse("result", {"text": text, "meta": meta, "raw": data})
                elif kind == "exit":
                    exit_code = int(evt.get("code", -1))
                elif kind == "error":
                    yield await sse("error", {"text": evt.get("text", "")})
        except Exception as e:
            yield await sse("error", {"text": f"dispatch failed: {e!r}"})
        yield await sse("done", {"ok": exit_code == 0, "exit_code": exit_code})

    return StreamingResponse(gen(), media_type="text/event-stream", headers={
        "Cache-Control": "no-cache",
        "X-Accel-Buffering": "no",
    })


# ---- scout result reader ---------------------------------------------------

@app.get("/api/orgs/{slug}/scout_results")
async def scout_results(slug: str) -> JSONResponse:
    """Read scout_pass.json (and Funders_Master.xlsx metadata) for an org.

    Returns the parsed Scout output if present, or {"rows": []} if not.
    """
    org_dir = ORGS_DIR / slug if DEMO_MODE == "live" else FIXTURES_DIR
    scout_json = org_dir / "grants" / "scout_pass.json"
    funders_xlsx = org_dir / "grants" / "Funders_Master.xlsx"

    if scout_json.exists():
        try:
            with scout_json.open() as f:
                data = json.load(f)
            rows = data if isinstance(data, list) else data.get("rows") or data.get("opportunities") or []
            return JSONResponse({
                "rows": rows,
                "source": str(scout_json),
                "funders_master_exists": funders_xlsx.exists(),
                "last_modified": scout_json.stat().st_mtime,
            })
        except (json.JSONDecodeError, OSError) as e:
            return JSONResponse({"rows": [], "error": str(e)})

    return JSONResponse({"rows": [], "funders_master_exists": funders_xlsx.exists()})


# ---- SSE: file events ------------------------------------------------------

@app.get("/api/events/files/{slug}")
async def file_events(slug: str) -> StreamingResponse:
    """
    SSE stream of file create/modify/delete events on orgs/{slug}/.

    In demo mode, replays a canned event sequence to animate the marketing capture.
    In live mode, watchdog.Observer pushes real file events into an asyncio.Queue.
    """
    target_dir = ORGS_DIR / slug if DEMO_MODE == "live" else None

    async def gen() -> AsyncIterator[str]:
        if DEMO_MODE == "demo" or not (target_dir and target_dir.exists()):
            canned = fixtures().get("simulated_file_events", {}).get(slug, [])
            for evt in canned:
                await asyncio.sleep(evt.get("delay_sec", 0.8))
                yield f"event: file\ndata: {json.dumps(evt)}\n\n"
            return
        # live mode: watchdog
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler

        queue: asyncio.Queue = asyncio.Queue(maxsize=200)
        loop = asyncio.get_running_loop()

        class Handler(FileSystemEventHandler):
            def on_any_event(self, event):
                payload = {
                    "type": event.event_type,
                    "path": event.src_path,
                    "is_directory": event.is_directory,
                }
                try:
                    loop.call_soon_threadsafe(queue.put_nowait, payload)
                except asyncio.QueueFull:
                    pass

        observer = Observer()
        observer.schedule(Handler(), str(target_dir), recursive=True)
        observer.start()
        try:
            while True:
                try:
                    evt = await asyncio.wait_for(queue.get(), timeout=15.0)
                    yield f"event: file\ndata: {json.dumps(evt)}\n\n"
                except asyncio.TimeoutError:
                    yield ": keepalive\n\n"
        finally:
            observer.stop()
            observer.join(timeout=3.0)

    return StreamingResponse(gen(), media_type="text/event-stream")


# ---- live helpers ----------------------------------------------------------

def _read_fit_farms_live() -> dict | None:
    """Read FIT Farms on-disk state for live overlay."""
    fit_dir = ORGS_DIR / "fit_farms"
    if not fit_dir.exists():
        return None
    out: dict = {"on_disk": True, "path": str(fit_dir)}
    pc = fit_dir / "PROJECT_CONTEXT.md"
    if pc.exists():
        out["project_context_bytes"] = pc.stat().st_size
        out["project_context_mtime"] = pc.stat().st_mtime
    memory = fit_dir / "memory"
    if memory.exists():
        out["memory_files"] = sorted(p.name for p in memory.glob("*.md"))
    grants = fit_dir / "grants"
    if grants.exists():
        out["grants_files"] = sorted(p.name for p in grants.iterdir() if p.is_file())
    return out


# ---- static files (last, so /api/* wins routing) ---------------------------

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
async def root_index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/{path:path}")
async def static_fallback(path: str) -> FileResponse:
    """SPA-style routing — unmatched non-API paths serve index.html."""
    f = STATIC_DIR / path
    if f.exists() and f.is_file():
        return FileResponse(f)
    return FileResponse(STATIC_DIR / "index.html")


# ---- CLI -------------------------------------------------------------------

def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Tilth Demo v0 server")
    p.add_argument("--mode", choices=["live", "demo"], default="live")
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=8000)
    p.add_argument("--reload", action="store_true")
    return p.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    os.environ["TILTH_DEMO_MODE"] = args.mode
    import uvicorn
    uvicorn.run("server:app", host=args.host, port=args.port, reload=args.reload)

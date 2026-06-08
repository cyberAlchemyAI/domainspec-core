#!/usr/bin/env python3
"""Body War / TROQAR Strava-linked MVP backend.

This intentionally uses only Python's standard library so the first pilot can
run in the repository without a dependency install step.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import mimetypes
import os
import secrets
import time
import urllib.error
import urllib.parse
import urllib.request
from http import HTTPStatus
from http.cookies import SimpleCookie
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


ROOT = Path(__file__).resolve().parent
STATIC_DIR = ROOT / "static"
DATA_DIR = ROOT / "data"
TOKEN_STORE = DATA_DIR / "strava-tokens.json"
SUBMISSION_STORE = DATA_DIR / "track-submissions.json"
TRACK_STORE = DATA_DIR / "tracks.json"

STRAVA_AUTHORIZE_URL = "https://www.strava.com/oauth/authorize"
STRAVA_TOKEN_URL = "https://www.strava.com/oauth/token"
STRAVA_API_BASE = "https://www.strava.com/api/v3"
DEFAULT_SCOPE = "read,activity:read"
ACCESS_TOKEN_REFRESH_WINDOW_SECONDS = 3600


def load_dotenv() -> None:
    env_file = ROOT / ".env"
    if not env_file.exists():
        return
    for raw_line in env_file.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_dotenv()


def env(name: str, default: str = "") -> str:
    return os.environ.get(name, default)


HOST = env("BODY_WAR_HOST", "127.0.0.1")
PORT = int(env("BODY_WAR_PORT", "5174"))
PUBLIC_BASE_URL = env("BODY_WAR_PUBLIC_BASE_URL", f"http://{HOST}:{PORT}")
STRAVA_REDIRECT_URI = env(
    "STRAVA_REDIRECT_URI", f"{PUBLIC_BASE_URL}/api/auth/strava/callback"
)
SESSION_SECRET = env("BODY_WAR_SESSION_SECRET") or env("SESSION_SECRET") or "dev-secret-change-me"


def ensure_default_files() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not TOKEN_STORE.exists():
        write_json(TOKEN_STORE, {"athletes": {}})
    if not SUBMISSION_STORE.exists():
        write_json(SUBMISSION_STORE, {"submissions": []})
    if not TRACK_STORE.exists():
        write_json(
            TRACK_STORE,
            {
                "tracks": [
                    {
                        "id": "craft-distill-blocker",
                        "name": "Craft Distill Blocker",
                        "pilot": "internal",
                        "description": "Aggregate Refine receipt status, grounded by recursive ledger evidence.",
                        "controller_metric": "aggregate_refine_receipt_status",
                    },
                    {
                        "id": "park-track-alpha",
                        "name": "Park Track Alpha",
                        "pilot": "body-war",
                        "description": "Placeholder physical track for the later real-world runner pilot.",
                        "controller_metric": "fastest_verified_time",
                    },
                ]
            },
        )


def read_json(path: Path, fallback):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return fallback


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sign(value: str) -> str:
    mac = hmac.new(SESSION_SECRET.encode(), value.encode(), hashlib.sha256).digest()
    return base64.urlsafe_b64encode(mac).decode().rstrip("=")


def signed_cookie(value: str) -> str:
    return f"{value}.{sign(value)}"


def verify_cookie(value: str | None) -> str | None:
    if not value or "." not in value:
        return None
    raw, signature = value.rsplit(".", 1)
    if hmac.compare_digest(sign(raw), signature):
        return raw
    return None


def parse_cookies(header: str | None) -> dict[str, str]:
    parsed = SimpleCookie()
    if header:
        parsed.load(header)
    return {key: morsel.value for key, morsel in parsed.items()}


def json_response(handler: SimpleHTTPRequestHandler, payload, status=HTTPStatus.OK):
    body = json.dumps(payload, indent=2, sort_keys=True).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


def redirect(handler: SimpleHTTPRequestHandler, location: str, cookies: list[str] | None = None):
    handler.send_response(HTTPStatus.FOUND)
    handler.send_header("Location", location)
    for cookie in cookies or []:
        handler.send_header("Set-Cookie", cookie)
    handler.end_headers()


def form_post(url: str, data: dict):
    encoded = urllib.parse.urlencode(data).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=encoded,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    return request_json(request)


def request_json(request: urllib.request.Request):
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Strava HTTP {exc.code}: {detail}") from exc


def strava_get(path: str, token: str, query: dict | None = None):
    url = f"{STRAVA_API_BASE}{path}"
    if query:
        url += "?" + urllib.parse.urlencode(query)
    request = urllib.request.Request(
        url,
        headers={"Authorization": f"Bearer {token}", "Accept": "application/json"},
        method="GET",
    )
    return request_json(request)


def strava_configured() -> bool:
    return bool(env("STRAVA_CLIENT_ID") and env("STRAVA_CLIENT_SECRET"))


def token_store() -> dict:
    ensure_default_files()
    return read_json(TOKEN_STORE, {"athletes": {}})


def save_token_store(store: dict) -> None:
    write_json(TOKEN_STORE, store)


def public_athlete(token_record: dict | None):
    if not token_record:
        return None
    athlete = token_record.get("athlete") or {}
    return {
        "id": athlete.get("id"),
        "firstname": athlete.get("firstname"),
        "lastname": athlete.get("lastname"),
        "profile": athlete.get("profile_medium") or athlete.get("profile"),
        "scope": token_record.get("scope", ""),
        "expires_at": token_record.get("expires_at"),
    }


def current_token_record(handler: SimpleHTTPRequestHandler):
    cookies = parse_cookies(handler.headers.get("Cookie"))
    athlete_id = verify_cookie(cookies.get("bw_athlete"))
    if not athlete_id:
        return None, None
    store = token_store()
    return athlete_id, store.get("athletes", {}).get(athlete_id)


def persist_token_response(payload: dict):
    athlete = payload.get("athlete") or {}
    athlete_id = str(athlete.get("id") or "")
    if not athlete_id:
        raise RuntimeError("Strava token response did not include athlete.id")
    store = token_store()
    store.setdefault("athletes", {})[athlete_id] = {
        "athlete": athlete,
        "scope": payload.get("scope", ""),
        "token_type": payload.get("token_type", "Bearer"),
        "access_token": payload.get("access_token"),
        "refresh_token": payload.get("refresh_token"),
        "expires_at": payload.get("expires_at"),
        "updated_at": int(time.time()),
    }
    save_token_store(store)
    return athlete_id


def access_token_for(handler: SimpleHTTPRequestHandler) -> tuple[str | None, dict | None]:
    athlete_id, record = current_token_record(handler)
    if not athlete_id or not record:
        return None, None
    expires_at = int(record.get("expires_at") or 0)
    if expires_at - int(time.time()) > ACCESS_TOKEN_REFRESH_WINDOW_SECONDS:
        return record.get("access_token"), record
    refreshed = form_post(
        STRAVA_TOKEN_URL,
        {
            "client_id": env("STRAVA_CLIENT_ID"),
            "client_secret": env("STRAVA_CLIENT_SECRET"),
            "grant_type": "refresh_token",
            "refresh_token": record.get("refresh_token", ""),
        },
    )
    record.update(
        {
            "access_token": refreshed.get("access_token"),
            "refresh_token": refreshed.get("refresh_token", record.get("refresh_token")),
            "expires_at": refreshed.get("expires_at"),
            "updated_at": int(time.time()),
        }
    )
    store = token_store()
    store.setdefault("athletes", {})[athlete_id] = record
    save_token_store(store)
    return record.get("access_token"), record


class BodyWarHandler(SimpleHTTPRequestHandler):
    server_version = "BodyWarPilot/0.1"

    def log_message(self, format: str, *args) -> None:
        if env("BODY_WAR_LOG_REQUESTS", "1") == "1":
            super().log_message(format, *args)

    def do_GET(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path.startswith("/api/"):
            self.handle_api_get(parsed)
            return
        self.serve_static(parsed.path)

    def do_POST(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path.startswith("/api/"):
            self.handle_api_post(parsed)
            return
        json_response(self, {"error": "not_found"}, HTTPStatus.NOT_FOUND)

    def handle_api_get(self, parsed) -> None:
        if parsed.path == "/api/status":
            _athlete_id, record = current_token_record(self)
            json_response(
                self,
                {
                    "configured": strava_configured(),
                    "connected": bool(record),
                    "athlete": public_athlete(record),
                    "redirect_uri": STRAVA_REDIRECT_URI,
                    "scope": DEFAULT_SCOPE,
                },
            )
            return
        if parsed.path == "/api/auth/strava/start":
            if not strava_configured():
                json_response(
                    self,
                    {
                        "error": "strava_not_configured",
                        "message": "Set STRAVA_CLIENT_ID and STRAVA_CLIENT_SECRET in projects/body-war/app/.env.",
                    },
                    HTTPStatus.BAD_REQUEST,
                )
                return
            state = secrets.token_urlsafe(24)
            query = urllib.parse.urlencode(
                {
                    "client_id": env("STRAVA_CLIENT_ID"),
                    "redirect_uri": STRAVA_REDIRECT_URI,
                    "response_type": "code",
                    "approval_prompt": "auto",
                    "scope": DEFAULT_SCOPE,
                    "state": state,
                }
            )
            redirect(
                self,
                f"{STRAVA_AUTHORIZE_URL}?{query}",
                [f"bw_state={signed_cookie(state)}; HttpOnly; SameSite=Lax; Path=/; Max-Age=600"],
            )
            return
        if parsed.path == "/api/auth/strava/callback":
            self.handle_strava_callback(parsed)
            return
        if parsed.path == "/api/activities":
            token, _record = access_token_for(self)
            if not token:
                json_response(self, {"error": "not_connected"}, HTTPStatus.UNAUTHORIZED)
                return
            query = urllib.parse.parse_qs(parsed.query)
            page = query.get("page", ["1"])[0]
            per_page = query.get("per_page", ["20"])[0]
            activities = strava_get(
                "/athlete/activities",
                token,
                {"page": page, "per_page": per_page},
            )
            json_response(self, {"activities": activities})
            return
        if parsed.path == "/api/tracks":
            json_response(self, read_json(TRACK_STORE, {"tracks": []}))
            return
        if parsed.path == "/api/submissions":
            json_response(self, read_json(SUBMISSION_STORE, {"submissions": []}))
            return
        json_response(self, {"error": "not_found"}, HTTPStatus.NOT_FOUND)

    def handle_api_post(self, parsed) -> None:
        if parsed.path == "/api/submissions":
            payload = self.read_body_json()
            athlete_id, record = current_token_record(self)
            if not athlete_id or not record:
                json_response(self, {"error": "not_connected"}, HTTPStatus.UNAUTHORIZED)
                return
            submission = {
                "id": secrets.token_urlsafe(10),
                "created_at": int(time.time()),
                "athlete_id": athlete_id,
                "athlete_name": " ".join(
                    filter(
                        None,
                        [
                            (record.get("athlete") or {}).get("firstname"),
                            (record.get("athlete") or {}).get("lastname"),
                        ],
                    )
                ),
                "track_id": payload.get("track_id"),
                "activity_id": payload.get("activity_id"),
                "activity_name": payload.get("activity_name"),
                "moving_time": payload.get("moving_time"),
                "distance": payload.get("distance"),
                "average_speed": payload.get("average_speed"),
                "status": "submitted",
                "authority": "hybrid",
                "public_controller_metric": "fastest_verified_time",
                "parallel_evidence": "composite_score_pending",
            }
            store = read_json(SUBMISSION_STORE, {"submissions": []})
            store.setdefault("submissions", []).append(submission)
            write_json(SUBMISSION_STORE, store)
            json_response(self, {"submission": submission}, HTTPStatus.CREATED)
            return
        json_response(self, {"error": "not_found"}, HTTPStatus.NOT_FOUND)

    def handle_strava_callback(self, parsed) -> None:
        query = urllib.parse.parse_qs(parsed.query)
        if "error" in query:
            redirect(self, f"/?auth_error={urllib.parse.quote(query['error'][0])}")
            return
        code = query.get("code", [""])[0]
        state = query.get("state", [""])[0]
        cookies = parse_cookies(self.headers.get("Cookie"))
        expected_state = verify_cookie(cookies.get("bw_state"))
        if not code or not expected_state or expected_state != state:
            redirect(self, "/?auth_error=invalid_state")
            return
        try:
            token_payload = form_post(
                STRAVA_TOKEN_URL,
                {
                    "client_id": env("STRAVA_CLIENT_ID"),
                    "client_secret": env("STRAVA_CLIENT_SECRET"),
                    "code": code,
                    "grant_type": "authorization_code",
                },
            )
            athlete_id = persist_token_response(token_payload)
            redirect(
                self,
                "/?connected=1",
                [
                    f"bw_athlete={signed_cookie(athlete_id)}; HttpOnly; SameSite=Lax; Path=/; Max-Age=2592000",
                    "bw_state=; HttpOnly; SameSite=Lax; Path=/; Max-Age=0",
                ],
            )
        except RuntimeError as exc:
            redirect(self, f"/?auth_error={urllib.parse.quote(str(exc))}")

    def read_body_json(self) -> dict:
        length = int(self.headers.get("Content-Length") or "0")
        if length <= 0:
            return {}
        raw = self.rfile.read(length).decode("utf-8")
        return json.loads(raw or "{}")

    def serve_static(self, path: str) -> None:
        target = STATIC_DIR / (path.lstrip("/") or "index.html")
        if target.is_dir():
            target = target / "index.html"
        try:
            resolved = target.resolve()
            resolved.relative_to(STATIC_DIR.resolve())
        except ValueError:
            json_response(self, {"error": "invalid_path"}, HTTPStatus.BAD_REQUEST)
            return
        if not resolved.exists():
            resolved = STATIC_DIR / "index.html"
        body = resolved.read_bytes()
        content_type = mimetypes.guess_type(str(resolved))[0] or "application/octet-stream"
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main() -> None:
    ensure_default_files()
    server = ThreadingHTTPServer((HOST, PORT), BodyWarHandler)
    print(f"Body War pilot app: http://{HOST}:{PORT}")
    print(f"Strava callback URL: {STRAVA_REDIRECT_URI}")
    server.serve_forever()


if __name__ == "__main__":
    main()

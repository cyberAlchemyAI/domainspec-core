# Body War Pilot App

This is the first app-backed validation channel for TROQAR / Body War. It links an athlete through Strava OAuth, fetches recent runs, and lets the pilot operator submit one activity to a pilot track.

The app is intentionally small and dependency-free:

- `server.py` serves the static UI and backend API.
- `static/` contains the browser app.
- `data/` stores local pilot JSON data and Strava tokens during development. It is ignored by git.

## Setup

1. Create a Strava API application.
2. Set its callback domain for local testing. Strava permits `localhost` and `127.0.0.1` callback URLs.
3. Copy `.env.example` to `.env`.
4. Fill in `STRAVA_CLIENT_ID`, `STRAVA_CLIENT_SECRET`, and `BODY_WAR_SESSION_SECRET`.

```bash
cp .env.example .env
python3 server.py
```

Open:

```text
http://127.0.0.1:5174
```

Callback URL:

```text
http://127.0.0.1:5174/api/auth/strava/callback
```

## API Surface

| Route                           | Purpose                                                   |
| ------------------------------- | --------------------------------------------------------- |
| `GET /api/status`               | Returns Strava configuration and connection status.       |
| `GET /api/auth/strava/start`    | Starts Strava OAuth.                                      |
| `GET /api/auth/strava/callback` | Exchanges the OAuth code for tokens.                      |
| `GET /api/activities`           | Lists recent Strava activities for the connected athlete. |
| `GET /api/tracks`               | Lists pilot tracks.                                       |
| `GET /api/submissions`          | Lists submitted pilot evidence.                           |
| `POST /api/submissions`         | Records an activity as evidence for a track.              |

## Pilot Authority

This follows the hybrid decision from `docs/decisions/mvp-readiness.md`:

- public controller metric: fastest verified time,
- richer evidence substrate: composite score and activity metadata captured for later analysis.

For the Craft internal pilot, the analogous authority is:

- public readiness controller: aggregate Refine receipt status,
- richer evidence substrate: recursive-ledger MVP evidence.

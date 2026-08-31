# Body War Pilot App

This is the first app-backed validation channel for TROQAR / Body War. It links
an athlete through Strava OAuth, fetches recent runs, and lets the pilot
operator submit one activity to a pilot track.

The app is intentionally small and uses the shared TypeScript auth package for
core principal, permission, session, and token use cases. Body War owns the
browser-cookie adapter, CSRF/origin guards, Strava OAuth adapter, provider token
custody, runner profile records, and activity redaction.

- `server.ts` serves the static UI and backend API.
- `static/` contains the browser app.
- `data/` stores local pilot track/submission JSON during development. It is
  ignored by git.
- `src/auth/` adapts Body War browser sessions and Strava provider state to
  `../../auth-user-management/`.
- `src/infrastructure/postgres/` contains the Body War Drizzle schema and
  migration runner. Auth package migrations are applied from the package, not
  re-generated inside this app.

## Setup

1. Copy `.env.example` to `.env`.
2. Keep `BODY_WAR_STRAVA_FAKE=1` for local fake-Strava login, or create a
   Strava API application and fill in `STRAVA_CLIENT_ID`,
   `STRAVA_CLIENT_SECRET`, and `STRAVA_REDIRECT_URI`.
3. Fill in `BODY_WAR_SESSION_SECRET` and `BODY_WAR_TOKEN_PROTECTION_SECRET`.
4. Use `BODY_WAR_AUTH_BACKEND=memory` for local development without Postgres,
   or set `BODY_WAR_AUTH_BACKEND=postgres` with `BODY_WAR_DATABASE_URL`.

```bash
cp .env.example .env
pnpm install
pnpm run build
pnpm start
```

The committed files under `drizzle/` are the migration authority. Automatic
Drizzle generation is intentionally unavailable until a vulnerability-free
generator is selected; do not install an ad hoc generator.

## Private Strava geometry export

The one-shot exporter discovers recent activities for the authenticated athlete,
then retrieves their GPS, distance, and time streams. It does not add a public
API route and writes private, Git-ignored evidence under `.runtime/geometry/`.
The legacy local submission store contains fixture-style activity identifiers,
so it is not the default live source.

Test one activity first:

```bash
chmod 600 .env data/strava-tokens.json
pnpm run geometry:export -- --limit 1
```

Then export the bounded recent-activity set:

```bash
pnpm run geometry:export
```

By default the exporter inspects one page of 30 recent activities. Use
`--pages`, `--per-page`, repeated `--activity-id`, or `--help` for an explicitly
bounded selection. `--source submitted` is available only when a submission
store contains real numeric Strava activity identifiers; fixture identifiers
fail before any network request.

The default outputs are `strava-activities.geojson` and `export-report.json`.
They contain private location evidence and remain candidate inputs only; they
do not establish source-backed track geometry. If Strava returns no activities
under `activity:read`, reconnecting with `activity:read_all` is required to
include activities whose visibility is “Only Me.”

The explicit private-activity reconnect command starts a ten-minute loopback
callback listener and prints the Strava consent URL. It updates the same ignored
legacy token store only after state validation, full scope acceptance, and
the selected athlete-account validation:

```bash
pnpm run geometry:reconnect -- --include-private
```

Run this only when the athlete has explicitly agreed to share “Only Me”
activities for this private local export.

To add a separately consenting partner, use a fresh authorization session and
preserve each athlete as a separate token-store entry:

```bash
pnpm run geometry:reconnect -- \
  --include-private \
  --add-athlete \
  --public-callback-url https://<temporary-host>/api/auth/strava/callback
```

After more than one athlete is stored, every export must select one explicitly
with `--athlete-key`; separate output paths keep private location histories from
being combined by default.

The Docker E2E harness starts a local Postgres container, applies auth package
and Body War Drizzle-generated migrations, and runs the fake-Strava login flow:

```bash
pnpm run e2e:all
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
| `POST /api/auth/logout`         | Revokes the server session and clears auth cookies.       |
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

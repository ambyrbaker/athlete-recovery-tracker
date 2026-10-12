# Athlete Recovery & Rehab Tracker

A personal, single-user React + FastAPI + SQLite tracker with training, daily wellness, and physical therapy CRUD; a dashboard; 14-day sleep and training-load charts; and accessible daily-value tables.

## Run locally

From the repository root:

```sh
python3 -m venv backend/venv
backend/venv/bin/python -m pip install -r requirements.txt
npm install --prefix frontend
npm run build --prefix frontend
backend/venv/bin/python -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000
```

Open http://127.0.0.1:8000. The FastAPI server serves the built React application and its API. API documentation: http://127.0.0.1:8000/docs.

For frontend development, keep the backend running and run `npm run dev --prefix frontend` in another terminal. Open the Vite URL (normally http://127.0.0.1:5173). Vite proxies `/api` to the backend, so no broad CORS policy is needed. Rebuild and restart FastAPI when switching to production serving.

## Data and behavior

- The default SQLite path is anchored to `backend/recovery_tracker.db`, regardless of the startup directory. Existing data is retained. Startup only creates missing tables, including `pt_sessions`.
- Override with `DATABASE_URL` for a separate environment. Back up SQLite with its backup command before moving or deploying personal records. No sample data is inserted.
- Existing `/training/` and `/wellness/` endpoints remain available. `/pt/` supports the same POST, GET, GET by ID, PUT, DELETE operations. The frontend uses equivalent `/api` routes.
- Training load = duration in minutes × RPE, expressed in arbitrary units (AU). RPE is 1–10.
- Dashboard week = Monday through today, using the browser's local date. Duration is the total training duration in that period. Trends show the last 14 calendar days. Future entries are retained in histories but excluded from dashboard summaries.
- Multiple wellness entries per day are supported without overwriting records. Today's card uses the latest ID; sleep trends average all entries per date. Weekly soreness/stress average all entries during the week. Missing wellness values are shown as unknown, not zero.
- IDs are database identities, not row positions. List responses sort by date and then ID descending. The previous relative database URL could open a different file when launched from another directory; the fixed path prevents that ambiguity.
- PT records contain date, exercise, sets, repetitions, duration, pain, and notes. This app logs exercises; it does not prescribe treatment.
- This is a local personal app with no authentication. Do not expose it publicly without adding authentication and access controls.

## Verify

```sh
backend/venv/bin/python -m pip install -r requirements-dev.txt
PYTHONPATH=backend backend/venv/bin/python -m unittest discover -s backend/tests -v
node --test frontend/src/metrics.test.js
npm run build --prefix frontend
```

API tests run on a temporary SQLite database and cover all three CRUD flows, ID consistency, persistence across app lifespans, missing records, and invalid inputs. They do not modify `backend/recovery_tracker.db`.

## Opening animation

The black/navy/white introduction plays once per browser tab session (about 2.4 seconds). Skip intro or Escape dismisses it immediately. Reduced-motion preferences use a brief fade without line drawing or movement. Reloading the same tab skips the intro; open a fresh tab to view it again. Session storage is optional and no athlete data is stored there.

## WHOOP dashboard integration

The dashboard fetches `GET /api/whoop/recovery` independently of training, wellness, and PT data. It displays the latest record timestamp, recovery score, HRV (ms), resting heart rate (bpm), SpO₂ (%), and skin temperature (°C). Missing values are shown as —. WHOOP values do not overwrite wellness records or affect the existing dashboard calculations.

Use the backend that already serves WHOOP (currently port 8000). Build with `npm run build --prefix frontend`, then open `http://127.0.0.1:8000/`. For development, run `npm run dev --prefix frontend`; its `/api` proxy preserves the prefix for all APIs. An older backend process must be restarted if it has not loaded the WHOOP router.

Verification:

```sh
node --test frontend/src/services/whoop.test.js frontend/src/metrics.test.js
npm run build --prefix frontend
```

On Overview, confirm all five readings and the timestamp match `/api/whoop/recovery` (values are rounded for display). Select Refresh to fetch again. Navigate to Training, Wellness, and Physical therapy to confirm existing logs still work. The panel shows loading, not-connected, expired-session, unavailable-data, and generic-error states. Service tests mock those responses without changing or deleting real tokens. Network failures and invalid JSON show a safe retry message; raw backend errors are not displayed.

Connect/Reconnect opens the existing `/api/whoop/connect` route in a new tab. Complete the backend's existing OAuth flow, return to the dashboard, and select Refresh. The frontend never reads, stores, or sends WHOOP credentials. Automatic token refresh is intentionally not implemented; expired sessions require reconnecting. No new frontend dependencies are required.

WHOOP backend setup requires `WHOOP_CLIENT_ID`, `WHOOP_CLIENT_SECRET`, and `WHOOP_REDIRECT_URI` in your local environment (or an ignored `.env` file loaded from the backend working directory). Register the matching `/api/whoop/callback` URL in your WHOOP app. Credentials and `.whoop_tokens.json` are intentionally excluded from Git; each local installation must connect its own account.

import json
from pathlib import Path
import os
import secrets
from urllib.parse import urlencode

from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse

load_dotenv()

router = APIRouter(prefix="/api/whoop", tags=["WHOOP"])

WHOOP_CLIENT_ID = os.getenv("WHOOP_CLIENT_ID")
WHOOP_REDIRECT_URI = os.getenv("WHOOP_REDIRECT_URI")

AUTHORIZE_URL = "https://api.prod.whoop.com/oauth/oauth2/auth"

# Temporary development-only state storage.
# We'll replace this with session-based storage.
pending_states = set()

TOKEN_FILE = Path(__file__).resolve().parents[2] / ".whoop_tokens.json"


def save_whoop_tokens(tokens: dict):
    # Create a private file before writing sensitive tokens.
    fd = os.open(
        TOKEN_FILE,
        os.O_WRONLY | os.O_CREAT | os.O_TRUNC,
        0o600,
    )

    with os.fdopen(fd, "w") as file:
        json.dump(tokens, file)

    TOKEN_FILE.chmod(0o600)

def load_whoop_tokens():
    if not TOKEN_FILE.exists():
        raise HTTPException(
            status_code=401,
            detail="WHOOP is not connected",
        )

    with TOKEN_FILE.open("r") as file:
        return json.load(file)

@router.get("/connect")
def connect_whoop():
    if not WHOOP_CLIENT_ID or not WHOOP_REDIRECT_URI:
        raise HTTPException(
            status_code=500,
            detail="WHOOP OAuth settings are missing"
        )

    state = secrets.token_urlsafe(32)
    pending_states.add(state)

    params = {
        "client_id": WHOOP_CLIENT_ID,
        "redirect_uri": WHOOP_REDIRECT_URI,
        "response_type": "code",
        "scope": "read:recovery read:sleep read:cycles read:workout offline",
        "state": state,
    }

    authorization_url = f"{AUTHORIZE_URL}?{urlencode(params)}"
    return RedirectResponse(url=authorization_url)
import httpx
from fastapi import Query

WHOOP_CLIENT_SECRET = os.getenv("WHOOP_CLIENT_SECRET")
TOKEN_URL = "https://api.prod.whoop.com/oauth/oauth2/token"


@router.get("/callback")
async def whoop_callback(
    code: str | None = None,
    state: str | None = None,
    error: str | None = None,
):
    if error:
        raise HTTPException(status_code=400, detail="WHOOP authorization was denied")

    if not code or not state or state not in pending_states:
        raise HTTPException(status_code=400, detail="Invalid WHOOP OAuth callback")

    pending_states.remove(state)

    if not WHOOP_CLIENT_ID or not WHOOP_CLIENT_SECRET:
        raise HTTPException(status_code=500, detail="WHOOP credentials are missing")

    async with httpx.AsyncClient(timeout=20.0) as client:
        response = await client.post(
            TOKEN_URL,
            data={
                "grant_type": "authorization_code",
                "code": code,
                "client_id": WHOOP_CLIENT_ID,
                "client_secret": WHOOP_CLIENT_SECRET,
                "redirect_uri": WHOOP_REDIRECT_URI,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
    if response.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail=f"WHOOP token exchange failed (HTTP {response.status_code})",
        )

    tokens = response.json()

    if not tokens.get("access_token"):
        raise HTTPException(
            status_code=502,
            detail="WHOOP did not return an access token",
        )

    save_whoop_tokens(tokens)

    return {
        "message": "WHOOP authorization succeeded",
        "token_received": True,
        "refresh_token_received": bool(tokens.get("refresh_token")),
    }

    if response.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail=f"WHOOP token exchange failed (HTTP {response.status_code})",
        )

    tokens = response.json()

    # Development only: never return access or refresh tokens to the browser.
    return {
        "message": "WHOOP authorization succeeded",
        "token_received": bool(tokens.get("access_token")),
        "refresh_token_received": bool(tokens.get("refresh_token")),
    }
@router.get("/recovery")
async def get_whoop_recovery():
    tokens = load_whoop_tokens()
    access_token = tokens.get("access_token")

    if not access_token:
        raise HTTPException(
            status_code=401,
            detail="WHOOP access token is missing",
        )

    async with httpx.AsyncClient(timeout=20.0) as client:
        response = await client.get(
            "https://api.prod.whoop.com/developer/v2/recovery",
            headers={
                "Authorization": f"Bearer {access_token}",
            },
            params={"limit": 1},
        )

    if response.status_code == 401:
        raise HTTPException(
            status_code=401,
            detail="WHOOP access token expired; refresh is needed",
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail=f"WHOOP recovery request failed (HTTP {response.status_code})",
        )

    data = response.json()

    records = data.get("records", [])

    if not records:
        return {"message": "No WHOOP recovery data available"}

    recovery = records[0]
    score = recovery.get("score") or {}

    return {
        "date": recovery.get("created_at"),
        "recovery_score": score.get("recovery_score"),
        "hrv_rmssd_milli": score.get("hrv_rmssd_milli"),
        "resting_heart_rate": score.get("resting_heart_rate"),
        "spo2_percentage": score.get("spo2_percentage"),
        "skin_temp_celsius": score.get("skin_temp_celsius"),
    }
"""KisanVaani backend: serves the frontend and proxies ElevenLabs text-to-speech.
The API key stays on the server. If no key is set, /api/tts returns 503 and the
frontend falls back to the browser's built-in voice."""
import os
from pathlib import Path

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

ROOT = Path(__file__).parent.parent
load_dotenv(ROOT / ".env")

KEY = os.getenv("ELEVENLABS_API_KEY", "").strip()
VOICE = os.getenv("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM").strip()
MODEL = os.getenv("ELEVENLABS_MODEL", "eleven_multilingual_v2").strip()

app = FastAPI(title="KisanVaani")


class TTS(BaseModel):
    text: str


@app.get("/api/health")
def health():
    return {"ok": True, "elevenlabs": bool(KEY)}


@app.post("/api/tts")
async def tts(body: TTS):
    if not KEY:
        raise HTTPException(503, "ELEVENLABS_API_KEY not set")
    text = body.text.strip()[:1200]
    async with httpx.AsyncClient(timeout=30) as c:
        r = await c.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}",
            headers={"xi-api-key": KEY, "Accept": "audio/mpeg"},
            json={"text": text, "model_id": MODEL},
        )
    if r.status_code != 200:
        print("ElevenLabs error:", r.status_code, r.text[:300])
        raise HTTPException(502, f"ElevenLabs error {r.status_code}")
    return Response(r.content, media_type="audio/mpeg")


app.mount("/", StaticFiles(directory=ROOT / "frontend", html=True), name="web")
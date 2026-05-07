import logging
import os
from pathlib import Path

import httpx


log = logging.getLogger("voice-gateway")

ELEVENLABS_API = "https://api.elevenlabs.io/v1"


def read_secret(path: str) -> str:
    try:
        return Path(path).read_text().strip()
    except FileNotFoundError:
        return ""


def elevenlabs_configured() -> bool:
    api_key = read_secret(os.getenv("ELEVENLABS_API_KEY_FILE", ""))
    voice_id = read_secret(os.getenv("ELEVENLABS_VOICE_ID_FILE", ""))
    return bool(api_key and voice_id and api_key != "placeholder")


async def synthesize_ulaw(text: str) -> bytes:
    api_key = read_secret(os.getenv("ELEVENLABS_API_KEY_FILE", ""))
    voice_id = read_secret(os.getenv("ELEVENLABS_VOICE_ID_FILE", ""))
    model_id = os.getenv("ELEVENLABS_MODEL_ID", "eleven_flash_v2_5")

    if not api_key or not voice_id:
        raise RuntimeError("ElevenLabs key or voice id missing")

    url = f"{ELEVENLABS_API}/text-to-speech/{voice_id}/stream"
    params = {
        "output_format": "ulaw_8000",
        "optimize_streaming_latency": "3",
    }
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json",
    }
    payload = {
        "text": text,
        "model_id": model_id,
        "voice_settings": {
            "stability": 0.45,
            "similarity_boost": 0.85,
            "style": 0.25,
            "use_speaker_boost": True,
        },
    }

    chunks: list[bytes] = []
    async with httpx.AsyncClient(timeout=30) as client:
        async with client.stream("POST", url, params=params, headers=headers, json=payload) as response:
            if response.status_code >= 400:
                body = await response.aread()
                raise RuntimeError(f"ElevenLabs TTS failed {response.status_code}: {body[:300]!r}")

            async for chunk in response.aiter_bytes():
                if chunk:
                    chunks.append(chunk)

    audio = b"".join(chunks)
    log.info("elevenlabs synthesized ulaw bytes=%d", len(audio))
    return audio
